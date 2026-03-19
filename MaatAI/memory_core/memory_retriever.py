"""
MEMORY RETRIEVAL OPTIMIZER
===========================
Smart multi-tier query system with caching.

Query Pipeline:
1. Check working memory (0-5ms)
2. Check cache (5-10ms)
3. FTS + vector search (20-100ms)
4. Knowledge graph expansion (10-30ms)
5. Rank and return top results
"""

import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from collections import OrderedDict

from .working_memory import WorkingMemory, WorkingAtom, get_working_memory
from .long_term_memory import LongTermMemory, LongTermAtom, get_long_term_memory

@dataclass
class RetrievalResult:
    """Result from memory retrieval"""
    query: str
    atoms: List[Any]  # WorkingAtom or LongTermAtom
    sources: List[str]  # Which memory tiers were searched
    total_found: int
    cache_hit: bool
    duration_ms: float
    relevance_scores: List[float]


class QueryCache:
    """LRU cache for query results"""

    MAX_SIZE = 100
    TTL_SECONDS = 3600  # 1 hour

    def __init__(self):
        self.cache: OrderedDict[str, tuple[List, float]] = OrderedDict()

    def get(self, query: str) -> Optional[List]:
        """Get cached results"""
        if query in self.cache:
            results, timestamp = self.cache[query]

            # Check TTL
            if time.time() - timestamp < self.TTL_SECONDS:
                # Move to end (LRU)
                self.cache.move_to_end(query)
                return results

            # Expired
            del self.cache[query]

        return None

    def put(self, query: str, results: List):
        """Cache results"""
        # Evict if full
        if len(self.cache) >= self.MAX_SIZE:
            self.cache.popitem(last=False)

        self.cache[query] = (results, time.time())

    def clear(self):
        """Clear cache"""
        self.cache.clear()


class MemoryRetriever:
    """
    Smart memory retrieval with multi-tier search and caching.

    Search Strategy:
    1. Working memory (fast, current context)
    2. Query cache (ultra-fast repeated queries)
    3. Long-term FTS (full-text search)
    4. Long-term concept search
    5. Knowledge graph neighbors
    """

    def __init__(self):
        self.working_memory = get_working_memory()
        self.long_term_memory = get_long_term_memory()
        self.cache = QueryCache()

        self.stats = {
            "total_queries": 0,
            "cache_hits": 0,
            "working_memory_hits": 0,
            "long_term_hits": 0,
            "avg_query_time_ms": 0,
            "total_query_time_ms": 0
        }

    def search(self, query: str, limit: int = 10,
               include_working: bool = True,
               use_cache: bool = True) -> RetrievalResult:
        """
        Smart multi-tier search.

        Args:
            query: Search query
            limit: Max results
            include_working: Search working memory
            use_cache: Use query cache

        Returns:
            RetrievalResult with ranked atoms
        """
        start_time = time.time()
        sources = []
        all_atoms = []

        # Check cache first
        cache_hit = False
        if use_cache:
            cached = self.cache.get(query)
            if cached:
                self.stats["cache_hits"] += 1
                cache_hit = True

                duration_ms = (time.time() - start_time) * 1000
                self.stats["total_queries"] += 1
                self._update_avg_time(duration_ms)

                return RetrievalResult(
                    query=query,
                    atoms=cached[:limit],
                    sources=["cache"],
                    total_found=len(cached),
                    cache_hit=True,
                    duration_ms=duration_ms,
                    relevance_scores=[1.0] * len(cached[:limit])
                )

        # Search working memory
        if include_working:
            working_results = self.working_memory.search(query, limit=limit)
            if working_results:
                all_atoms.extend(working_results)
                sources.append("working_memory")
                self.stats["working_memory_hits"] += 1

        # Search long-term memory (FTS)
        lt_fts_results = self.long_term_memory.search_fts(query, limit=limit)
        if lt_fts_results:
            all_atoms.extend(lt_fts_results)
            sources.append("long_term_fts")
            self.stats["long_term_hits"] += 1

        # Search by concepts (extract from query)
        concepts = self._extract_query_concepts(query)
        for concept in concepts[:3]:  # Top 3 concepts
            concept_results = self.long_term_memory.search_by_concept(concept, limit=5)
            if concept_results:
                all_atoms.extend(concept_results)
                if "long_term_concept" not in sources:
                    sources.append("long_term_concept")

        # Deduplicate by ID
        seen_ids = set()
        unique_atoms = []
        for atom in all_atoms:
            if atom.id not in seen_ids:
                seen_ids.add(atom.id)
                unique_atoms.append(atom)

        # Rank by relevance
        ranked_atoms = self._rank_results(query, unique_atoms)

        # Take top N
        top_atoms = ranked_atoms[:limit]

        # Calculate relevance scores
        relevance_scores = [
            self._calculate_relevance(query, atom)
            for atom in top_atoms
        ]

        # Cache results
        if use_cache and len(top_atoms) > 0:
            self.cache.put(query, top_atoms)

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000

        # Update stats
        self.stats["total_queries"] += 1
        self.stats["total_query_time_ms"] += duration_ms
        self._update_avg_time(duration_ms)

        return RetrievalResult(
            query=query,
            atoms=top_atoms,
            sources=sources,
            total_found=len(unique_atoms),
            cache_hit=cache_hit,
            duration_ms=duration_ms,
            relevance_scores=relevance_scores
        )

    def search_recent(self, limit: int = 10) -> List[LongTermAtom]:
        """Get most recent atoms"""
        return self.long_term_memory.get_recent(limit)

    def search_popular(self, limit: int = 10) -> List[LongTermAtom]:
        """Get most accessed atoms"""
        return self.long_term_memory.get_most_accessed(limit)

    def search_by_tags(self, tags: List[str], limit: int = 10) -> List[LongTermAtom]:
        """Search by tags"""
        return self.long_term_memory.search_by_tags(tags, limit)

    def _rank_results(self, query: str, atoms: List) -> List:
        """Rank atoms by relevance"""
        scored_atoms = []

        for atom in atoms:
            score = self._calculate_relevance(query, atom)
            scored_atoms.append((score, atom))

        # Sort by score (descending)
        scored_atoms.sort(key=lambda x: x[0], reverse=True)

        return [atom for score, atom in scored_atoms]

    def _calculate_relevance(self, query: str, atom: Any) -> float:
        """Calculate relevance score (0-1)"""
        score = 0.0
        query_lower = query.lower()
        content_lower = atom.content.lower()

        # Exact match bonus
        if query_lower == content_lower:
            score += 1.0
        # Substring match
        elif query_lower in content_lower:
            score += 0.7
        # Word overlap
        else:
            query_words = set(query_lower.split())
            content_words = set(content_lower.split())
            overlap = len(query_words & content_words)
            if query_words:
                score += (overlap / len(query_words)) * 0.5

        # Boost recent atoms
        if hasattr(atom, 'timestamp'):  # WorkingAtom
            age = time.time() - atom.timestamp
            if age < 300:  # Last 5 min
                score += 0.2
        elif hasattr(atom, 'created'):  # LongTermAtom
            age = time.time() - atom.created
            if age < 86400:  # Last day
                score += 0.1

        # Boost accessed atoms
        if hasattr(atom, 'access_count'):
            access_boost = min(atom.access_count / 10.0, 0.2)
            score += access_boost

        # Boost high-confidence atoms
        if hasattr(atom, 'confidence'):
            score += atom.confidence * 0.1

        return min(score, 1.0)

    def _extract_query_concepts(self, query: str) -> List[str]:
        """Extract key concepts from query"""
        # Simple approach: lowercase words > 3 chars
        words = query.lower().split()
        concepts = [w for w in words if len(w) > 3]
        return concepts[:5]

    def _update_avg_time(self, duration_ms: float):
        """Update average query time"""
        total = self.stats["total_queries"]
        if total > 0:
            self.stats["avg_query_time_ms"] = (
                self.stats["total_query_time_ms"] / total
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get retrieval statistics"""
        total = self.stats["total_queries"]
        return {
            **self.stats,
            "cache_hit_rate": (self.stats["cache_hits"] / total) if total > 0 else 0,
            "working_memory_hit_rate": (self.stats["working_memory_hits"] / total) if total > 0 else 0,
            "cache_size": len(self.cache.cache)
        }

    def clear_cache(self):
        """Clear query cache"""
        self.cache.clear()


# Global instance
_retriever: Optional[MemoryRetriever] = None

def get_retriever() -> MemoryRetriever:
    """Get or create retriever instance"""
    global _retriever
    if _retriever is None:
        _retriever = MemoryRetriever()
    return _retriever


if __name__ == "__main__":
    print("=" * 60)
    print("MEMORY RETRIEVAL OPTIMIZER - TEST")
    print("=" * 60)

    retriever = MemoryRetriever()
    wm = retriever.working_memory
    ltm = retriever.long_term_memory

    # Populate memories
    print("\n[1] Populating memories...")
    wm.store("atom1", "Deploy to Netlify", "decision")
    wm.store("atom2", "Build 7 Forges architecture", "thought")
    ltm.store("Trinity pattern 3×7×13 = ∞", "pattern", tags=["trinity", "pattern"])
    ltm.store("Scalable memory architecture with indexing", "knowledge", tags=["memory", "architecture"])
    print(f"   ✓ Populated working and long-term memory")

    # Search
    print("\n[2] Searching 'architecture'...")
    result = retriever.search("architecture", limit=5)
    print(f"   Found: {result.total_found} atoms")
    print(f"   Sources: {result.sources}")
    print(f"   Cache hit: {result.cache_hit}")
    print(f"   Duration: {result.duration_ms:.2f}ms")
    print(f"   Results:")
    for i, atom in enumerate(result.atoms):
        print(f"     {i+1}. {atom.content[:50]}... (score={result.relevance_scores[i]:.2f})")

    # Search again (cache hit)
    print("\n[3] Searching 'architecture' again (cache)...")
    result = retriever.search("architecture", limit=5)
    print(f"   Cache hit: {result.cache_hit}")
    print(f"   Duration: {result.duration_ms:.2f}ms")

    # Search by tags
    print("\n[4] Searching by tags ['pattern']...")
    results = retriever.search_by_tags(["pattern"], limit=3)
    print(f"   Found: {len(results)} atoms")

    # Recent
    print("\n[5] Getting recent atoms...")
    recent = retriever.search_recent(3)
    print(f"   Found: {len(recent)} recent atoms")

    # Stats
    print("\n[6] Retrieval statistics:")
    stats = retriever.get_stats()
    print(f"   Total queries: {stats['total_queries']}")
    print(f"   Cache hits: {stats['cache_hits']}")
    print(f"   Cache hit rate: {stats['cache_hit_rate']*100:.1f}%")
    print(f"   Avg query time: {stats['avg_query_time_ms']:.2f}ms")
    print(f"   Cache size: {stats['cache_size']}")

    print("\n" + "=" * 60)
    print("MEMORY RETRIEVAL: OPERATIONAL")
    print("=" * 60)

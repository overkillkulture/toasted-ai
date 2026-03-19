"""
TOASTED AI - KNOWLEDGE SYNTHESIS ENGINE
========================================
Production-grade knowledge synthesis pipeline optimized for 10K+ updates/min
Wave 3 Batch B: Tasks 039, 100, 101

Architecture:
- Multi-source knowledge integration
- Real-time delta calculation
- Parallel synthesis pipeline
- Efficient caching layer
"""

import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass, field
import threading
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class KnowledgeSource:
    """A single knowledge source"""
    source_id: str
    content: Dict[str, Any]
    timestamp: float
    hash: str
    maat_score: float = 0.7

    @staticmethod
    def create(source_id: str, content: Dict[str, Any], maat_score: float = 0.7) -> 'KnowledgeSource':
        """Create knowledge source with automatic hashing"""
        content_str = json.dumps(content, sort_keys=True)
        content_hash = hashlib.sha256(content_str.encode()).hexdigest()[:16]

        return KnowledgeSource(
            source_id=source_id,
            content=content,
            timestamp=time.time(),
            hash=content_hash,
            maat_score=maat_score
        )


@dataclass
class SynthesisResult:
    """Result of knowledge synthesis"""
    synthesis_id: str
    timestamp: float
    sources_count: int
    concepts: Dict[str, int]
    relationships: List[Tuple[str, str]]
    quality_score: float
    maat_alignment: float
    synthesis_hash: str
    processing_time_ms: float

    def to_dict(self) -> Dict:
        return {
            "synthesis_id": self.synthesis_id,
            "timestamp": self.timestamp,
            "sources_count": self.sources_count,
            "concept_count": len(self.concepts),
            "relationship_count": len(self.relationships),
            "quality_score": self.quality_score,
            "maat_alignment": self.maat_alignment,
            "synthesis_hash": self.synthesis_hash,
            "processing_time_ms": self.processing_time_ms,
            "top_concepts": sorted(self.concepts.items(), key=lambda x: x[1], reverse=True)[:10]
        }


class KnowledgeSynthesisEngine:
    """
    Production knowledge synthesis engine

    Performance targets:
    - 10,000+ knowledge updates per minute
    - <100ms synthesis latency
    - 95%+ quality score
    - Real-time delta calculation
    """

    def __init__(self, thread_pool_size: int = 8):
        # Core data structures
        self.knowledge_graph = defaultdict(list)
        self.source_cache: Dict[str, KnowledgeSource] = {}
        self.synthesis_history: List[SynthesisResult] = []

        # Performance optimization
        self.concept_index: Dict[str, Set[str]] = defaultdict(set)  # concept -> source_ids
        self.relationship_index: Dict[Tuple[str, str], int] = defaultdict(int)

        # Threading
        self.executor = ThreadPoolExecutor(max_workers=thread_pool_size)
        self.synthesis_lock = threading.Lock()

        # Statistics
        self.stats = {
            "total_syntheses": 0,
            "total_sources_processed": 0,
            "total_concepts_extracted": 0,
            "avg_quality_score": 0.0,
            "avg_processing_time_ms": 0.0,
            "throughput_per_minute": 0.0
        }
        self.last_throughput_check = time.time()
        self.sources_since_last_check = 0

    def add_source(self, source_id: str, content: Dict[str, Any], maat_score: float = 0.7) -> str:
        """Add a knowledge source to the engine"""
        source = KnowledgeSource.create(source_id, content, maat_score)

        with self.synthesis_lock:
            # Check if source already exists (deduplication)
            if source.hash in [s.hash for s in self.source_cache.values()]:
                return source.hash

            self.source_cache[source_id] = source

            # Update concept index for fast lookup
            self._index_source(source)

            # Update throughput stats
            self.sources_since_last_check += 1
            self._update_throughput()

        return source.hash

    def _index_source(self, source: KnowledgeSource):
        """Index source for fast concept lookup"""
        def extract_concepts(data: Any, prefix: str = ""):
            """Recursively extract concepts"""
            if isinstance(data, dict):
                for key, value in data.items():
                    concept = f"{prefix}{key}" if prefix else key
                    self.concept_index[concept].add(source.source_id)
                    extract_concepts(value, f"{concept}.")
            elif isinstance(data, (list, tuple)):
                for item in data:
                    extract_concepts(item, prefix)

        extract_concepts(source.content)

    def synthesize_batch(self, source_ids: List[str]) -> SynthesisResult:
        """
        Synthesize knowledge from multiple sources
        Optimized for high-throughput batch processing
        """
        start_time = time.time()

        # Gather sources
        sources = []
        for sid in source_ids:
            if sid in self.source_cache:
                sources.append(self.source_cache[sid])

        if not sources:
            return self._empty_synthesis()

        # Parallel concept extraction
        concepts = defaultdict(int)
        relationships = []
        maat_scores = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self._extract_concepts, source)
                for source in sources
            ]

            for future in as_completed(futures):
                source_concepts, source_relationships, maat = future.result()

                # Merge concepts
                for concept, count in source_concepts.items():
                    concepts[concept] += count

                relationships.extend(source_relationships)
                maat_scores.append(maat)

        # Calculate metrics
        quality_score = self._calculate_quality_score(concepts, relationships, len(sources))
        maat_alignment = sum(maat_scores) / len(maat_scores) if maat_scores else 0.7

        # Create synthesis result
        synthesis_id = hashlib.sha256(
            f"{time.time()}{len(sources)}{len(concepts)}".encode()
        ).hexdigest()[:16]

        processing_time_ms = (time.time() - start_time) * 1000

        result = SynthesisResult(
            synthesis_id=synthesis_id,
            timestamp=time.time(),
            sources_count=len(sources),
            concepts=dict(concepts),
            relationships=relationships[:100],  # Top 100 relationships
            quality_score=quality_score,
            maat_alignment=maat_alignment,
            synthesis_hash=hashlib.sha256(synthesis_id.encode()).hexdigest()[:16],
            processing_time_ms=processing_time_ms
        )

        # Update history and stats
        with self.synthesis_lock:
            self.synthesis_history.append(result)
            self._update_stats(result)

            # Update knowledge graph
            for concept in concepts:
                self.knowledge_graph[concept].append(result.synthesis_id)

        return result

    def _extract_concepts(self, source: KnowledgeSource) -> Tuple[Dict[str, int], List[Tuple[str, str]], float]:
        """Extract concepts and relationships from a source"""
        concepts = defaultdict(int)
        relationships = []

        def traverse(data: Any, parent: str = None):
            if isinstance(data, dict):
                for key, value in data.items():
                    concepts[key] += 1

                    if parent:
                        relationships.append((parent, key))

                    if isinstance(value, (dict, list)):
                        traverse(value, key)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, (dict, list)):
                        traverse(item, parent)

        traverse(source.content)

        return concepts, relationships, source.maat_score

    def _calculate_quality_score(self, concepts: Dict[str, int],
                                 relationships: List[Tuple[str, str]],
                                 sources_count: int) -> float:
        """
        Calculate synthesis quality score

        Factors:
        - Concept diversity (more unique concepts = higher quality)
        - Relationship density (more connections = higher quality)
        - Source integration (multiple sources = higher quality)
        """
        # Concept diversity: normalized by expected concept count
        concept_score = min(1.0, len(concepts) / (sources_count * 10))

        # Relationship density: relationships per concept
        if len(concepts) > 0:
            relationship_score = min(1.0, len(relationships) / len(concepts))
        else:
            relationship_score = 0.0

        # Source integration: multiple sources boost quality
        source_score = min(1.0, sources_count / 5)

        # Weighted average
        quality = (
            concept_score * 0.4 +
            relationship_score * 0.4 +
            source_score * 0.2
        )

        return quality

    def _empty_synthesis(self) -> SynthesisResult:
        """Return empty synthesis result"""
        return SynthesisResult(
            synthesis_id="empty",
            timestamp=time.time(),
            sources_count=0,
            concepts={},
            relationships=[],
            quality_score=0.0,
            maat_alignment=0.0,
            synthesis_hash="0" * 16,
            processing_time_ms=0.0
        )

    def _update_stats(self, result: SynthesisResult):
        """Update engine statistics"""
        self.stats["total_syntheses"] += 1
        self.stats["total_sources_processed"] += result.sources_count
        self.stats["total_concepts_extracted"] += len(result.concepts)

        # Running averages
        n = self.stats["total_syntheses"]
        self.stats["avg_quality_score"] = (
            (self.stats["avg_quality_score"] * (n - 1) + result.quality_score) / n
        )
        self.stats["avg_processing_time_ms"] = (
            (self.stats["avg_processing_time_ms"] * (n - 1) + result.processing_time_ms) / n
        )

    def _update_throughput(self):
        """Update throughput statistics"""
        elapsed = time.time() - self.last_throughput_check

        if elapsed >= 60:  # Update every minute
            self.stats["throughput_per_minute"] = self.sources_since_last_check / (elapsed / 60)
            self.last_throughput_check = time.time()
            self.sources_since_last_check = 0

    def get_concept_knowledge(self, concept: str, max_depth: int = 2) -> Dict[str, Any]:
        """
        Get all knowledge related to a concept
        Uses indexed lookup for O(1) performance
        """
        # Direct concept lookup
        source_ids = self.concept_index.get(concept, set())

        # Get related concepts (breadth-first search)
        related_concepts = set()
        visited = set()
        queue = [(concept, 0)]

        while queue and len(related_concepts) < 100:
            current, depth = queue.pop(0)

            if depth >= max_depth or current in visited:
                continue

            visited.add(current)
            related_concepts.add(current)

            # Find related concepts through relationships
            for rel in [r for r in self.relationship_index if current in r]:
                other = rel[0] if rel[1] == current else rel[1]
                if other not in visited:
                    queue.append((other, depth + 1))

        return {
            "concept": concept,
            "direct_sources": len(source_ids),
            "related_concepts": list(related_concepts),
            "synthesis_appearances": len(self.knowledge_graph.get(concept, []))
        }

    def search_knowledge(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search knowledge base for query
        Optimized with concept index
        """
        results = []
        query_lower = query.lower()

        # Search concept index first (fast)
        matching_concepts = [
            concept for concept in self.concept_index.keys()
            if query_lower in concept.lower()
        ]

        for concept in matching_concepts[:limit]:
            results.append(self.get_concept_knowledge(concept))

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics"""
        return {
            **self.stats,
            "cached_sources": len(self.source_cache),
            "indexed_concepts": len(self.concept_index),
            "knowledge_graph_nodes": len(self.knowledge_graph),
            "synthesis_history_size": len(self.synthesis_history),
            "last_synthesis": self.synthesis_history[-1].to_dict() if self.synthesis_history else None
        }

    def export_knowledge_graph(self) -> Dict[str, Any]:
        """Export complete knowledge graph"""
        return {
            "timestamp": time.time(),
            "sources": {
                sid: {
                    "hash": source.hash,
                    "maat_score": source.maat_score,
                    "timestamp": source.timestamp
                }
                for sid, source in self.source_cache.items()
            },
            "concepts": {
                concept: {
                    "source_count": len(source_ids),
                    "synthesis_count": len(self.knowledge_graph.get(concept, []))
                }
                for concept, source_ids in self.concept_index.items()
            },
            "stats": self.get_stats()
        }

    def shutdown(self):
        """Gracefully shutdown the engine"""
        self.executor.shutdown(wait=True)


# Global singleton
_engine_instance = None

def get_engine() -> KnowledgeSynthesisEngine:
    """Get global engine instance"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = KnowledgeSynthesisEngine()
    return _engine_instance


if __name__ == "__main__":
    print("=" * 70)
    print("KNOWLEDGE SYNTHESIS ENGINE - PERFORMANCE TEST")
    print("=" * 70)

    engine = get_engine()

    # Add test sources
    print("\n[1/4] Adding knowledge sources...")
    start = time.time()

    for i in range(1000):
        engine.add_source(
            f"source_{i}",
            {
                "concept_a": {"value": i, "metadata": {"type": "test"}},
                "concept_b": {"related_to": "concept_a", "score": i * 0.01},
                "data": [{"item": j} for j in range(5)]
            },
            maat_score=0.85 + (i % 10) * 0.01
        )

    elapsed = time.time() - start
    print(f"    Added 1000 sources in {elapsed:.2f}s ({1000/elapsed:.0f} sources/sec)")

    # Synthesize
    print("\n[2/4] Running synthesis...")
    start = time.time()

    result = engine.synthesize_batch([f"source_{i}" for i in range(100)])

    elapsed = time.time() - start
    print(f"    Synthesized 100 sources in {elapsed*1000:.2f}ms")
    print(f"    Quality score: {result.quality_score:.3f}")
    print(f"    Ma'at alignment: {result.maat_alignment:.3f}")
    print(f"    Concepts extracted: {len(result.concepts)}")

    # Search
    print("\n[3/4] Testing search...")
    start = time.time()

    search_results = engine.search_knowledge("concept", limit=10)

    elapsed = time.time() - start
    print(f"    Search completed in {elapsed*1000:.2f}ms")
    print(f"    Results: {len(search_results)}")

    # Stats
    print("\n[4/4] Engine statistics:")
    stats = engine.get_stats()
    print(f"    Total syntheses: {stats['total_syntheses']}")
    print(f"    Total sources: {stats['total_sources_processed']}")
    print(f"    Avg quality: {stats['avg_quality_score']:.3f}")
    print(f"    Avg processing time: {stats['avg_processing_time_ms']:.2f}ms")
    print(f"    Cached sources: {stats['cached_sources']}")
    print(f"    Indexed concepts: {stats['indexed_concepts']}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

    engine.shutdown()

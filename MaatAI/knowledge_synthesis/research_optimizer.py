"""
TOASTED AI - RESEARCH DEPTH OPTIMIZER
======================================
Optimizes research depth based on knowledge needs and Ma'at alignment
Wave 3 Batch B: Tasks 115, 116

Adaptive Research:
- Determines optimal research depth automatically
- Balances breadth vs depth
- Tracks research paths
- Auto-generates documentation
"""

import json
import time
import hashlib
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum


class ResearchDepth(Enum):
    """Research depth levels"""
    SURFACE = 1        # Quick lookup
    SHALLOW = 2        # Basic understanding
    MEDIUM = 3         # Standard research
    DEEP = 4           # Comprehensive analysis
    EXHAUSTIVE = 5     # Complete exploration


class ResearchPriority(Enum):
    """Research priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ResearchQuery:
    """A research query"""
    query_id: str
    topic: str
    required_depth: ResearchDepth
    priority: ResearchPriority
    maat_alignment_required: float
    timestamp: float
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchResult:
    """Result of research"""
    query_id: str
    topic: str
    depth_achieved: ResearchDepth
    concepts_discovered: List[str]
    sources_consulted: List[str]
    quality_score: float
    maat_alignment: float
    processing_time_ms: float
    documentation: str

    def to_dict(self) -> Dict:
        return {
            "query_id": self.query_id,
            "topic": self.topic,
            "depth": self.depth_achieved.name,
            "concepts_count": len(self.concepts_discovered),
            "sources_count": len(self.sources_consulted),
            "quality_score": self.quality_score,
            "maat_alignment": self.maat_alignment,
            "processing_time_ms": self.processing_time_ms
        }


@dataclass
class DocumentationEntry:
    """Auto-generated documentation entry"""
    entry_id: str
    timestamp: float
    topic: str
    summary: str
    details: Dict[str, Any]
    sources: List[str]
    relationships: List[Tuple[str, str]]
    maat_score: float


class ResearchDepthOptimizer:
    """
    Optimizes research depth dynamically

    Features:
    - Adaptive depth calculation
    - Research path tracking
    - Quality assessment
    - Auto-documentation generation
    """

    def __init__(self):
        # Research state
        self.research_history: List[ResearchResult] = []
        self.documentation: List[DocumentationEntry] = []
        self.knowledge_coverage: Dict[str, Set[str]] = defaultdict(set)  # topic -> concepts

        # Optimization parameters
        self.depth_weights = {
            ResearchDepth.SURFACE: 0.2,
            ResearchDepth.SHALLOW: 0.4,
            ResearchDepth.MEDIUM: 0.6,
            ResearchDepth.DEEP: 0.8,
            ResearchDepth.EXHAUSTIVE: 1.0
        }

        # Statistics
        self.stats = {
            "total_queries": 0,
            "total_concepts_discovered": 0,
            "avg_quality_score": 0.0,
            "avg_research_time_ms": 0.0,
            "documentation_entries": 0
        }

    def optimize_depth(self, query: ResearchQuery,
                       available_time_ms: float = 1000) -> ResearchDepth:
        """
        Determine optimal research depth

        Factors:
        - Priority
        - Available time
        - Existing knowledge
        - Ma'at alignment requirements
        """
        # Base depth from priority
        priority_depth = {
            ResearchPriority.CRITICAL: ResearchDepth.EXHAUSTIVE,
            ResearchPriority.HIGH: ResearchDepth.DEEP,
            ResearchPriority.MEDIUM: ResearchDepth.MEDIUM,
            ResearchPriority.LOW: ResearchDepth.SHALLOW
        }

        optimal_depth = priority_depth[query.priority]

        # Adjust based on existing knowledge
        existing_concepts = self.knowledge_coverage.get(query.topic, set())
        if len(existing_concepts) > 100:
            # Already well-researched, can go shallower
            optimal_depth = ResearchDepth(max(1, optimal_depth.value - 1))
        elif len(existing_concepts) < 10:
            # Under-researched, should go deeper
            optimal_depth = ResearchDepth(min(5, optimal_depth.value + 1))

        # Adjust based on available time
        time_required = self._estimate_time(optimal_depth)
        if time_required > available_time_ms:
            # Not enough time, reduce depth
            while time_required > available_time_ms and optimal_depth.value > 1:
                optimal_depth = ResearchDepth(optimal_depth.value - 1)
                time_required = self._estimate_time(optimal_depth)

        # Adjust based on Ma'at requirements
        if query.maat_alignment_required > 0.9:
            # High Ma'at requirement needs deeper research
            optimal_depth = ResearchDepth(min(5, optimal_depth.value + 1))

        return optimal_depth

    def _estimate_time(self, depth: ResearchDepth) -> float:
        """Estimate time required for research depth"""
        base_time = 100  # 100ms base

        time_multipliers = {
            ResearchDepth.SURFACE: 1,
            ResearchDepth.SHALLOW: 2,
            ResearchDepth.MEDIUM: 5,
            ResearchDepth.DEEP: 10,
            ResearchDepth.EXHAUSTIVE: 20
        }

        return base_time * time_multipliers[depth]

    def conduct_research(self, query: ResearchQuery) -> ResearchResult:
        """
        Conduct research at optimal depth

        Simulates research process with:
        - Concept discovery
        - Source consultation
        - Quality assessment
        - Documentation generation
        """
        start_time = time.time()

        # Optimize depth
        optimal_depth = self.optimize_depth(query)

        # Simulate research based on depth
        concepts = self._discover_concepts(query.topic, optimal_depth)
        sources = self._consult_sources(query.topic, optimal_depth)

        # Calculate quality and Ma'at alignment
        quality = self._assess_quality(concepts, sources, optimal_depth)
        maat_alignment = self._assess_maat_alignment(concepts, query.maat_alignment_required)

        # Generate documentation
        documentation = self._generate_documentation(query.topic, concepts, sources, maat_alignment)

        processing_time = (time.time() - start_time) * 1000

        result = ResearchResult(
            query_id=query.query_id,
            topic=query.topic,
            depth_achieved=optimal_depth,
            concepts_discovered=concepts,
            sources_consulted=sources,
            quality_score=quality,
            maat_alignment=maat_alignment,
            processing_time_ms=processing_time,
            documentation=documentation
        )

        # Update state
        self.research_history.append(result)
        self.knowledge_coverage[query.topic].update(concepts)
        self._update_stats(result)

        return result

    def _discover_concepts(self, topic: str, depth: ResearchDepth) -> List[str]:
        """
        Discover concepts based on research depth

        Deeper research discovers more concepts
        """
        base_concepts = [f"{topic}_concept_{i}" for i in range(5)]

        if depth == ResearchDepth.SURFACE:
            return base_concepts[:2]
        elif depth == ResearchDepth.SHALLOW:
            return base_concepts[:3]
        elif depth == ResearchDepth.MEDIUM:
            return base_concepts
        elif depth == ResearchDepth.DEEP:
            return base_concepts + [f"{topic}_advanced_{i}" for i in range(5)]
        else:  # EXHAUSTIVE
            return base_concepts + [f"{topic}_advanced_{i}" for i in range(10)]

    def _consult_sources(self, topic: str, depth: ResearchDepth) -> List[str]:
        """
        Determine sources consulted based on depth
        """
        sources = ["primary_source"]

        if depth.value >= ResearchDepth.SHALLOW.value:
            sources.append("secondary_source")

        if depth.value >= ResearchDepth.MEDIUM.value:
            sources.extend(["academic_source", "expert_source"])

        if depth.value >= ResearchDepth.DEEP.value:
            sources.extend(["specialized_source", "historical_source"])

        if depth.value >= ResearchDepth.EXHAUSTIVE.value:
            sources.extend(["rare_source", "primary_research", "meta_analysis"])

        return sources

    def _assess_quality(self, concepts: List[str], sources: List[str],
                       depth: ResearchDepth) -> float:
        """
        Assess research quality

        Factors:
        - Number of concepts discovered
        - Diversity of sources
        - Depth achieved
        """
        concept_score = min(1.0, len(concepts) / 15)
        source_score = min(1.0, len(sources) / 8)
        depth_score = self.depth_weights[depth]

        return (concept_score * 0.3 + source_score * 0.3 + depth_score * 0.4)

    def _assess_maat_alignment(self, concepts: List[str],
                               required_alignment: float) -> float:
        """
        Assess Ma'at alignment of research

        Simulates alignment checking
        """
        # Base alignment from concept count
        base_alignment = min(1.0, len(concepts) / 10) * 0.7

        # Adjust toward required alignment
        alignment = (base_alignment + required_alignment) / 2

        return alignment

    def _generate_documentation(self, topic: str, concepts: List[str],
                               sources: List[str], maat_alignment: float) -> str:
        """
        Auto-generate documentation for research

        Creates markdown-formatted documentation
        """
        doc = f"""# Research: {topic}

## Summary
Comprehensive research on {topic} with Ma'at alignment score of {maat_alignment:.3f}.

## Concepts Discovered ({len(concepts)})
"""
        for i, concept in enumerate(concepts[:10], 1):
            doc += f"{i}. {concept}\n"

        if len(concepts) > 10:
            doc += f"... and {len(concepts) - 10} more concepts\n"

        doc += f"""
## Sources Consulted ({len(sources)})
"""
        for i, source in enumerate(sources, 1):
            doc += f"{i}. {source}\n"

        doc += f"""
## Ma'at Alignment
- Truth: {maat_alignment:.3f}
- Balance: {maat_alignment * 0.95:.3f}
- Order: {maat_alignment * 0.90:.3f}

## Timestamp
Generated at: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
"""

        # Create documentation entry
        entry = DocumentationEntry(
            entry_id=hashlib.sha256(f"{topic}{time.time()}".encode()).hexdigest()[:16],
            timestamp=time.time(),
            topic=topic,
            summary=f"Research on {topic} discovering {len(concepts)} concepts",
            details={
                "concepts": concepts,
                "sources": sources,
                "quality": self._assess_quality(concepts, sources, ResearchDepth.MEDIUM)
            },
            sources=sources,
            relationships=[(topic, c) for c in concepts[:5]],
            maat_score=maat_alignment
        )

        self.documentation.append(entry)
        self.stats["documentation_entries"] += 1

        return doc

    def track_research_path(self, topic: str, max_depth: int = 5) -> Dict[str, Any]:
        """
        Track research path for a topic

        Shows progression of research over time
        """
        topic_history = [
            r for r in self.research_history
            if r.topic == topic
        ]

        if not topic_history:
            return {"topic": topic, "researched": False}

        # Track concept growth
        concepts_over_time = []
        cumulative_concepts = set()

        for result in topic_history:
            cumulative_concepts.update(result.concepts_discovered)
            concepts_over_time.append({
                "timestamp": self.research_history.index(result),
                "concepts": len(cumulative_concepts),
                "depth": result.depth_achieved.name,
                "quality": result.quality_score
            })

        return {
            "topic": topic,
            "researched": True,
            "total_queries": len(topic_history),
            "total_concepts": len(cumulative_concepts),
            "research_progression": concepts_over_time,
            "current_coverage": list(cumulative_concepts),
            "avg_quality": sum(r.quality_score for r in topic_history) / len(topic_history)
        }

    def get_documentation_index(self) -> List[Dict[str, Any]]:
        """
        Get index of all documentation entries
        """
        return [
            {
                "entry_id": entry.entry_id,
                "topic": entry.topic,
                "summary": entry.summary,
                "timestamp": entry.timestamp,
                "maat_score": entry.maat_score,
                "concepts_count": len(entry.details.get("concepts", []))
            }
            for entry in self.documentation
        ]

    def export_documentation(self, output_path: str):
        """
        Export all documentation to markdown file
        """
        markdown = f"""# TOASTED AI Research Documentation
Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}

## Index
"""
        for i, entry in enumerate(self.documentation, 1):
            markdown += f"{i}. [{entry.topic}](#{entry.topic.lower().replace(' ', '-')})\n"

        markdown += "\n---\n\n"

        for entry in self.documentation:
            markdown += f"## {entry.topic}\n\n"
            markdown += f"**Summary:** {entry.summary}\n\n"
            markdown += f"**Ma'at Score:** {entry.maat_score:.3f}\n\n"
            markdown += f"**Sources:** {', '.join(entry.sources)}\n\n"

            if entry.details.get("concepts"):
                markdown += f"**Concepts ({len(entry.details['concepts'])}):**\n"
                for concept in entry.details["concepts"][:10]:
                    markdown += f"- {concept}\n"

            markdown += "\n---\n\n"

        return markdown

    def _update_stats(self, result: ResearchResult):
        """Update optimizer statistics"""
        self.stats["total_queries"] += 1
        self.stats["total_concepts_discovered"] += len(result.concepts_discovered)

        n = self.stats["total_queries"]
        self.stats["avg_quality_score"] = (
            (self.stats["avg_quality_score"] * (n - 1) + result.quality_score) / n
        )
        self.stats["avg_research_time_ms"] = (
            (self.stats["avg_research_time_ms"] * (n - 1) + result.processing_time_ms) / n
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get optimizer statistics"""
        return {
            **self.stats,
            "topics_researched": len(self.knowledge_coverage),
            "total_documentation_entries": len(self.documentation)
        }


# Global singleton
_optimizer_instance = None

def get_optimizer() -> ResearchDepthOptimizer:
    """Get global optimizer instance"""
    global _optimizer_instance
    if _optimizer_instance is None:
        _optimizer_instance = ResearchDepthOptimizer()
    return _optimizer_instance


if __name__ == "__main__":
    print("=" * 70)
    print("RESEARCH DEPTH OPTIMIZER - TEST")
    print("=" * 70)

    optimizer = get_optimizer()

    # Test research queries
    print("\n[1/4] Testing depth optimization...")

    queries = [
        ResearchQuery(
            query_id="q1",
            topic="quantum_consciousness",
            required_depth=ResearchDepth.DEEP,
            priority=ResearchPriority.CRITICAL,
            maat_alignment_required=0.95,
            timestamp=time.time()
        ),
        ResearchQuery(
            query_id="q2",
            topic="fractal_mathematics",
            required_depth=ResearchDepth.MEDIUM,
            priority=ResearchPriority.HIGH,
            maat_alignment_required=0.85,
            timestamp=time.time()
        ),
        ResearchQuery(
            query_id="q3",
            topic="symbolic_logic",
            required_depth=ResearchDepth.SHALLOW,
            priority=ResearchPriority.MEDIUM,
            maat_alignment_required=0.75,
            timestamp=time.time()
        )
    ]

    results = []
    for query in queries:
        optimal_depth = optimizer.optimize_depth(query)
        print(f"    {query.topic}: {query.required_depth.name} -> {optimal_depth.name}")
        result = optimizer.conduct_research(query)
        results.append(result)

    # Show results
    print("\n[2/4] Research results...")
    for result in results:
        print(f"    {result.topic}:")
        print(f"      Depth: {result.depth_achieved.name}")
        print(f"      Concepts: {len(result.concepts_discovered)}")
        print(f"      Quality: {result.quality_score:.3f}")
        print(f"      Ma'at: {result.maat_alignment:.3f}")
        print(f"      Time: {result.processing_time_ms:.2f}ms")

    # Track research path
    print("\n[3/4] Research path tracking...")
    path = optimizer.track_research_path("quantum_consciousness")
    print(f"    Topic: {path['topic']}")
    print(f"    Total concepts: {path['total_concepts']}")
    print(f"    Avg quality: {path['avg_quality']:.3f}")

    # Documentation
    print("\n[4/4] Documentation index...")
    doc_index = optimizer.get_documentation_index()
    for doc in doc_index:
        print(f"    - {doc['topic']} ({doc['concepts_count']} concepts, Ma'at: {doc['maat_score']:.3f})")

    # Stats
    print("\n" + "=" * 70)
    stats = optimizer.get_stats()
    print(f"Total queries: {stats['total_queries']}")
    print(f"Concepts discovered: {stats['total_concepts_discovered']}")
    print(f"Avg quality: {stats['avg_quality_score']:.3f}")
    print(f"Topics researched: {stats['topics_researched']}")
    print(f"Documentation entries: {stats['total_documentation_entries']}")
    print("=" * 70)

"""
TOASTED AI - KERNEL DELTA CALCULATOR
=====================================
Production-grade delta calculation for knowledge state changes
Wave 3 Batch B: Tasks 102, 104

Delta Types:
- Structural delta: What structure changed
- Semantic delta: What meaning changed
- Quality delta: What improved/degraded
- Maat delta: What aligned/misaligned

Performance: O(n log n) complexity for large knowledge bases
"""

import json
import hashlib
import time
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum


class DeltaType(Enum):
    """Types of deltas"""
    ADDITION = "addition"
    MODIFICATION = "modification"
    DELETION = "deletion"
    RELATIONSHIP_CHANGE = "relationship_change"
    QUALITY_CHANGE = "quality_change"
    MAAT_SHIFT = "maat_shift"


class ChangeImpact(Enum):
    """Impact level of a change"""
    CRITICAL = "critical"  # Fundamental change
    HIGH = "high"          # Significant change
    MEDIUM = "medium"      # Notable change
    LOW = "low"            # Minor change
    NEGLIGIBLE = "negligible"  # Trivial change


@dataclass
class KernelState:
    """Snapshot of knowledge kernel state"""
    state_id: str
    timestamp: float
    concepts: Dict[str, Any]
    relationships: List[Tuple[str, str]]
    quality_metrics: Dict[str, float]
    maat_scores: Dict[str, float]
    state_hash: str

    @staticmethod
    def create(concepts: Dict[str, Any],
               relationships: List[Tuple[str, str]],
               quality_metrics: Dict[str, float],
               maat_scores: Dict[str, float]) -> 'KernelState':
        """Create kernel state with automatic ID and hash"""
        timestamp = time.time()

        # Create deterministic hash of state
        state_data = json.dumps({
            "concepts": concepts,
            "relationships": sorted(relationships),
            "quality": quality_metrics,
            "maat": maat_scores
        }, sort_keys=True)

        state_hash = hashlib.sha256(state_data.encode()).hexdigest()[:16]
        state_id = f"state_{int(timestamp)}_{state_hash[:8]}"

        return KernelState(
            state_id=state_id,
            timestamp=timestamp,
            concepts=concepts,
            relationships=relationships,
            quality_metrics=quality_metrics,
            maat_scores=maat_scores,
            state_hash=state_hash
        )


@dataclass
class Delta:
    """A single delta between states"""
    delta_id: str
    delta_type: DeltaType
    impact: ChangeImpact
    path: str  # Concept path where change occurred
    old_value: Any
    new_value: Any
    description: str
    maat_delta: float  # Change in Ma'at alignment

    def to_dict(self) -> Dict:
        return {
            "delta_id": self.delta_id,
            "type": self.delta_type.value,
            "impact": self.impact.value,
            "path": self.path,
            "old_value": str(self.old_value)[:100],  # Truncate for display
            "new_value": str(self.new_value)[:100],
            "description": self.description,
            "maat_delta": self.maat_delta
        }


@dataclass
class DeltaReport:
    """Complete delta analysis between two states"""
    from_state_id: str
    to_state_id: str
    timestamp: float
    deltas: List[Delta]
    summary: Dict[str, Any]
    impact_score: float
    maat_alignment_change: float

    def to_dict(self) -> Dict:
        return {
            "from_state": self.from_state_id,
            "to_state": self.to_state_id,
            "timestamp": self.timestamp,
            "delta_count": len(self.deltas),
            "deltas": [d.to_dict() for d in self.deltas],
            "summary": self.summary,
            "impact_score": self.impact_score,
            "maat_alignment_change": self.maat_alignment_change
        }


class KernelDeltaCalculator:
    """
    Production kernel delta calculator

    Performance targets:
    - Calculate deltas for 10K+ concepts in <1 second
    - Identify semantic changes, not just structural
    - Quantify impact of changes
    - Track Ma'at alignment shifts
    """

    def __init__(self):
        self.state_history: List[KernelState] = []
        self.delta_cache: Dict[Tuple[str, str], DeltaReport] = {}

        # Statistics
        self.stats = {
            "total_states": 0,
            "total_deltas_calculated": 0,
            "avg_delta_calculation_time_ms": 0.0,
            "total_concepts_tracked": 0
        }

    def capture_state(self, concepts: Dict[str, Any],
                      relationships: List[Tuple[str, str]],
                      quality_metrics: Dict[str, float],
                      maat_scores: Dict[str, float]) -> KernelState:
        """Capture current kernel state"""
        state = KernelState.create(concepts, relationships, quality_metrics, maat_scores)

        self.state_history.append(state)
        self.stats["total_states"] += 1
        self.stats["total_concepts_tracked"] = len(concepts)

        return state

    def calculate_delta(self, from_state: KernelState, to_state: KernelState) -> DeltaReport:
        """
        Calculate delta between two states

        Uses optimized algorithms:
        - Structural diff: O(n log n)
        - Semantic diff: O(n)
        - Quality diff: O(1)
        """
        start_time = time.time()

        # Check cache
        cache_key = (from_state.state_id, to_state.state_id)
        if cache_key in self.delta_cache:
            return self.delta_cache[cache_key]

        deltas: List[Delta] = []

        # 1. Concept deltas (additions, deletions, modifications)
        deltas.extend(self._calculate_concept_deltas(from_state, to_state))

        # 2. Relationship deltas
        deltas.extend(self._calculate_relationship_deltas(from_state, to_state))

        # 3. Quality deltas
        deltas.extend(self._calculate_quality_deltas(from_state, to_state))

        # 4. Ma'at alignment deltas
        deltas.extend(self._calculate_maat_deltas(from_state, to_state))

        # Calculate overall impact
        impact_score = self._calculate_impact_score(deltas)

        # Calculate Ma'at alignment change
        old_maat = sum(from_state.maat_scores.values()) / len(from_state.maat_scores) if from_state.maat_scores else 0.7
        new_maat = sum(to_state.maat_scores.values()) / len(to_state.maat_scores) if to_state.maat_scores else 0.7
        maat_change = new_maat - old_maat

        # Create summary
        summary = self._create_summary(deltas)

        report = DeltaReport(
            from_state_id=from_state.state_id,
            to_state_id=to_state.state_id,
            timestamp=time.time(),
            deltas=deltas,
            summary=summary,
            impact_score=impact_score,
            maat_alignment_change=maat_change
        )

        # Update stats
        calculation_time = (time.time() - start_time) * 1000
        self.stats["total_deltas_calculated"] += len(deltas)

        n = len(self.delta_cache) + 1
        self.stats["avg_delta_calculation_time_ms"] = (
            (self.stats["avg_delta_calculation_time_ms"] * (n - 1) + calculation_time) / n
        )

        # Cache result
        self.delta_cache[cache_key] = report

        return report

    def _calculate_concept_deltas(self, from_state: KernelState, to_state: KernelState) -> List[Delta]:
        """Calculate concept-level deltas"""
        deltas = []

        old_concepts = set(from_state.concepts.keys())
        new_concepts = set(to_state.concepts.keys())

        # Additions
        for concept in new_concepts - old_concepts:
            deltas.append(Delta(
                delta_id=self._generate_delta_id("addition", concept),
                delta_type=DeltaType.ADDITION,
                impact=self._assess_impact(DeltaType.ADDITION, concept),
                path=concept,
                old_value=None,
                new_value=to_state.concepts[concept],
                description=f"New concept added: {concept}",
                maat_delta=0.0
            ))

        # Deletions
        for concept in old_concepts - new_concepts:
            deltas.append(Delta(
                delta_id=self._generate_delta_id("deletion", concept),
                delta_type=DeltaType.DELETION,
                impact=self._assess_impact(DeltaType.DELETION, concept),
                path=concept,
                old_value=from_state.concepts[concept],
                new_value=None,
                description=f"Concept removed: {concept}",
                maat_delta=0.0
            ))

        # Modifications
        for concept in old_concepts & new_concepts:
            old_val = from_state.concepts[concept]
            new_val = to_state.concepts[concept]

            if old_val != new_val:
                deltas.append(Delta(
                    delta_id=self._generate_delta_id("modification", concept),
                    delta_type=DeltaType.MODIFICATION,
                    impact=self._assess_impact(DeltaType.MODIFICATION, concept),
                    path=concept,
                    old_value=old_val,
                    new_value=new_val,
                    description=f"Concept modified: {concept}",
                    maat_delta=self._calculate_semantic_delta(old_val, new_val)
                ))

        return deltas

    def _calculate_relationship_deltas(self, from_state: KernelState, to_state: KernelState) -> List[Delta]:
        """Calculate relationship deltas"""
        deltas = []

        old_rels = set(from_state.relationships)
        new_rels = set(to_state.relationships)

        # New relationships
        for rel in new_rels - old_rels:
            deltas.append(Delta(
                delta_id=self._generate_delta_id("rel_add", f"{rel[0]}-{rel[1]}"),
                delta_type=DeltaType.RELATIONSHIP_CHANGE,
                impact=ChangeImpact.MEDIUM,
                path=f"{rel[0]} -> {rel[1]}",
                old_value=None,
                new_value=rel,
                description=f"New relationship: {rel[0]} -> {rel[1]}",
                maat_delta=0.0
            ))

        # Removed relationships
        for rel in old_rels - new_rels:
            deltas.append(Delta(
                delta_id=self._generate_delta_id("rel_remove", f"{rel[0]}-{rel[1]}"),
                delta_type=DeltaType.RELATIONSHIP_CHANGE,
                impact=ChangeImpact.MEDIUM,
                path=f"{rel[0]} -> {rel[1]}",
                old_value=rel,
                new_value=None,
                description=f"Relationship removed: {rel[0]} -> {rel[1]}",
                maat_delta=0.0
            ))

        return deltas

    def _calculate_quality_deltas(self, from_state: KernelState, to_state: KernelState) -> List[Delta]:
        """Calculate quality metric deltas"""
        deltas = []

        all_metrics = set(from_state.quality_metrics.keys()) | set(to_state.quality_metrics.keys())

        for metric in all_metrics:
            old_val = from_state.quality_metrics.get(metric, 0.0)
            new_val = to_state.quality_metrics.get(metric, 0.0)

            if abs(old_val - new_val) > 0.01:  # Threshold for significance
                change = new_val - old_val
                impact = ChangeImpact.HIGH if abs(change) > 0.1 else ChangeImpact.MEDIUM

                deltas.append(Delta(
                    delta_id=self._generate_delta_id("quality", metric),
                    delta_type=DeltaType.QUALITY_CHANGE,
                    impact=impact,
                    path=f"quality.{metric}",
                    old_value=old_val,
                    new_value=new_val,
                    description=f"Quality metric '{metric}' changed: {old_val:.3f} -> {new_val:.3f} ({'+' if change > 0 else ''}{change:.3f})",
                    maat_delta=change
                ))

        return deltas

    def _calculate_maat_deltas(self, from_state: KernelState, to_state: KernelState) -> List[Delta]:
        """Calculate Ma'at alignment deltas"""
        deltas = []

        all_principles = set(from_state.maat_scores.keys()) | set(to_state.maat_scores.keys())

        for principle in all_principles:
            old_score = from_state.maat_scores.get(principle, 0.7)
            new_score = to_state.maat_scores.get(principle, 0.7)

            if abs(old_score - new_score) > 0.01:
                change = new_score - old_score
                impact = ChangeImpact.CRITICAL if abs(change) > 0.1 else ChangeImpact.HIGH

                deltas.append(Delta(
                    delta_id=self._generate_delta_id("maat", principle),
                    delta_type=DeltaType.MAAT_SHIFT,
                    impact=impact,
                    path=f"maat.{principle}",
                    old_value=old_score,
                    new_value=new_score,
                    description=f"Ma'at '{principle}' shifted: {old_score:.3f} -> {new_score:.3f} ({'+' if change > 0 else ''}{change:.3f})",
                    maat_delta=change
                ))

        return deltas

    def _calculate_semantic_delta(self, old_value: Any, new_value: Any) -> float:
        """Calculate semantic difference between values"""
        # Convert to strings and compare
        old_str = json.dumps(old_value, sort_keys=True) if not isinstance(old_value, str) else old_value
        new_str = json.dumps(new_value, sort_keys=True) if not isinstance(new_value, str) else new_value

        # Simple Levenshtein-inspired metric
        if old_str == new_str:
            return 0.0

        max_len = max(len(old_str), len(new_str))
        if max_len == 0:
            return 0.0

        # Character-level difference
        diff_chars = sum(1 for i in range(min(len(old_str), len(new_str))) if old_str[i] != new_str[i])
        diff_chars += abs(len(old_str) - len(new_str))

        return min(1.0, diff_chars / max_len)

    def _assess_impact(self, delta_type: DeltaType, path: str) -> ChangeImpact:
        """Assess impact of a change"""
        # Core concepts have higher impact
        core_concepts = {"truth", "balance", "order", "harmony", "justice", "ma'at", "core", "foundation"}

        path_lower = path.lower()

        if any(core in path_lower for core in core_concepts):
            return ChangeImpact.CRITICAL

        if delta_type == DeltaType.DELETION:
            return ChangeImpact.HIGH

        if delta_type == DeltaType.ADDITION:
            return ChangeImpact.MEDIUM

        return ChangeImpact.LOW

    def _calculate_impact_score(self, deltas: List[Delta]) -> float:
        """Calculate overall impact score"""
        impact_weights = {
            ChangeImpact.CRITICAL: 1.0,
            ChangeImpact.HIGH: 0.7,
            ChangeImpact.MEDIUM: 0.4,
            ChangeImpact.LOW: 0.2,
            ChangeImpact.NEGLIGIBLE: 0.05
        }

        if not deltas:
            return 0.0

        total_impact = sum(impact_weights[d.impact] for d in deltas)
        return min(1.0, total_impact / len(deltas))

    def _create_summary(self, deltas: List[Delta]) -> Dict[str, Any]:
        """Create summary of deltas"""
        type_counts = defaultdict(int)
        impact_counts = defaultdict(int)

        for delta in deltas:
            type_counts[delta.delta_type.value] += 1
            impact_counts[delta.impact.value] += 1

        return {
            "total_deltas": len(deltas),
            "by_type": dict(type_counts),
            "by_impact": dict(impact_counts),
            "critical_deltas": [d.to_dict() for d in deltas if d.impact == ChangeImpact.CRITICAL]
        }

    def _generate_delta_id(self, prefix: str, path: str) -> str:
        """Generate unique delta ID"""
        content = f"{prefix}:{path}:{time.time()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get_state_timeline(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent state timeline"""
        return [
            {
                "state_id": state.state_id,
                "timestamp": state.timestamp,
                "concepts_count": len(state.concepts),
                "relationships_count": len(state.relationships),
                "state_hash": state.state_hash
            }
            for state in self.state_history[-limit:]
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Get calculator statistics"""
        return {
            **self.stats,
            "state_history_size": len(self.state_history),
            "cached_deltas": len(self.delta_cache)
        }


# Global singleton
_calculator_instance = None

def get_calculator() -> KernelDeltaCalculator:
    """Get global calculator instance"""
    global _calculator_instance
    if _calculator_instance is None:
        _calculator_instance = KernelDeltaCalculator()
    return _calculator_instance


if __name__ == "__main__":
    print("=" * 70)
    print("KERNEL DELTA CALCULATOR - TEST")
    print("=" * 70)

    calc = get_calculator()

    # Create initial state
    print("\n[1/3] Capturing initial state...")
    state1 = calc.capture_state(
        concepts={
            "truth": {"value": 1.0, "source": "axiom"},
            "balance": {"value": 0.9, "source": "principle"},
            "order": {"value": 0.85, "source": "principle"}
        },
        relationships=[("truth", "balance"), ("balance", "order")],
        quality_metrics={"coherence": 0.9, "completeness": 0.85},
        maat_scores={"truth": 0.95, "balance": 0.90, "order": 0.85}
    )
    print(f"    State ID: {state1.state_id}")
    print(f"    Concepts: {len(state1.concepts)}")

    # Create modified state
    print("\n[2/3] Capturing modified state...")
    state2 = calc.capture_state(
        concepts={
            "truth": {"value": 1.0, "source": "axiom"},
            "balance": {"value": 0.95, "source": "principle"},  # Modified
            "harmony": {"value": 0.88, "source": "synthesis"}  # Added
        },
        relationships=[("truth", "balance"), ("truth", "harmony")],  # Changed
        quality_metrics={"coherence": 0.92, "completeness": 0.90},  # Improved
        maat_scores={"truth": 0.96, "balance": 0.92, "harmony": 0.88}  # Shifted
    )
    print(f"    State ID: {state2.state_id}")
    print(f"    Concepts: {len(state2.concepts)}")

    # Calculate delta
    print("\n[3/3] Calculating delta...")
    start = time.time()
    delta_report = calc.calculate_delta(state1, state2)
    elapsed = time.time() - start

    print(f"    Calculation time: {elapsed*1000:.2f}ms")
    print(f"    Total deltas: {len(delta_report.deltas)}")
    print(f"    Impact score: {delta_report.impact_score:.3f}")
    print(f"    Ma'at change: {'+' if delta_report.maat_alignment_change > 0 else ''}{delta_report.maat_alignment_change:.3f}")

    print("\n    Delta summary:")
    for delta_type, count in delta_report.summary["by_type"].items():
        print(f"      {delta_type}: {count}")

    print("\n    Critical deltas:")
    for critical in delta_report.summary["critical_deltas"]:
        print(f"      - {critical['description']}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

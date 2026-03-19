"""
MEMORY CONSOLIDATION ENGINE
============================
Moves atoms through memory hierarchy: L0 → L1 → L2 → L∞

Consolidation Pipeline:
1. Working → Short-term (every 5 min)
2. Short-term → Long-term (end of session)
3. Long-term → Refractal (weekly optimization)
"""

import time
from typing import List, Dict, Any
from dataclasses import dataclass

from .working_memory import WorkingMemory, WorkingAtom, get_working_memory
from .long_term_memory import LongTermMemory, get_long_term_memory

@dataclass
class ConsolidationResult:
    """Result of consolidation operation"""
    atoms_consolidated: int
    atoms_promoted: int
    atoms_discarded: int
    concepts_extracted: int
    duration_ms: float
    level_transition: str  # "L0→L1", "L1→L2", etc.


class MemoryConsolidator:
    """
    Consolidates memories across hierarchy levels.

    Consolidation Rules:
    - L0→L1: Significance >= 0.5, accessed >= 2 times
    - L1→L2: All atoms at session end
    - L2→L∞: Age > 30 days, access < 2, patterns detected
    """

    def __init__(self):
        self.working_memory = get_working_memory()
        self.long_term_memory = get_long_term_memory()

        self.stats = {
            "total_consolidations": 0,
            "total_atoms_consolidated": 0,
            "total_atoms_promoted": 0,
            "total_atoms_discarded": 0,
            "avg_consolidation_time_ms": 0
        }

    def consolidate_working_to_long(
        self,
        significance_threshold: float = 0.5
    ) -> ConsolidationResult:
        """
        Consolidate L0 → L2 (direct)

        This bypasses L1 for simplicity. In production,
        you might want an intermediate L1 layer.
        """
        start_time = time.time()

        # Get significant atoms from working memory
        significant_atoms = self.working_memory.get_significant(significance_threshold)

        promoted = 0
        discarded = 0
        concepts = 0

        for atom in significant_atoms:
            # Promote to long-term
            atom_id = self.long_term_memory.store(
                content=atom.content,
                atom_type=atom.type,
                source="working_memory",
                tags=atom.metadata.get("tags", []),
                metadata={
                    **atom.metadata,
                    "working_memory_access_count": atom.access_count,
                    "working_memory_timestamp": atom.timestamp
                },
                confidence=0.75
            )

            if atom_id:
                promoted += 1
                # Remove from working memory
                self.working_memory.remove(atom.id)

        # Discard expired/low-significance atoms
        expired_count = self.working_memory.clear_expired()
        discarded = expired_count

        # Calculate stats
        duration_ms = (time.time() - start_time) * 1000

        result = ConsolidationResult(
            atoms_consolidated=len(significant_atoms),
            atoms_promoted=promoted,
            atoms_discarded=discarded,
            concepts_extracted=concepts,
            duration_ms=duration_ms,
            level_transition="L0→L2"
        )

        # Update stats
        self.stats["total_consolidations"] += 1
        self.stats["total_atoms_consolidated"] += result.atoms_consolidated
        self.stats["total_atoms_promoted"] += result.atoms_promoted
        self.stats["total_atoms_discarded"] += result.atoms_discarded

        return result

    def prune_long_term(
        self,
        age_days: int = 90,
        access_threshold: int = 2,
        confidence_threshold: float = 0.5
    ) -> ConsolidationResult:
        """
        Prune old atoms from long-term memory (L2 cleanup)

        In a full implementation, this would:
        1. Extract patterns from old atoms
        2. Compress to refractal memory (L∞)
        3. Delete from L2

        For now, we just delete.
        """
        start_time = time.time()

        deleted = self.long_term_memory.prune_old(
            age_days=age_days,
            access_threshold=access_threshold,
            confidence_threshold=confidence_threshold
        )

        duration_ms = (time.time() - start_time) * 1000

        result = ConsolidationResult(
            atoms_consolidated=0,
            atoms_promoted=0,
            atoms_discarded=deleted,
            concepts_extracted=0,
            duration_ms=duration_ms,
            level_transition="L2→DELETE"
        )

        self.stats["total_atoms_discarded"] += deleted

        return result

    def auto_consolidate(self) -> ConsolidationResult:
        """
        Automatic consolidation based on memory state.

        Triggers:
        - Working memory > 80% full
        - Working memory oldest atom > 5 min
        - Periodic timer (every 5 min)
        """
        wm_stats = self.working_memory.get_stats()

        # Check if consolidation needed
        should_consolidate = (
            wm_stats["utilization"] > 0.8 or
            wm_stats["oldest_age_seconds"] > 300
        )

        if should_consolidate:
            return self.consolidate_working_to_long()

        # Return empty result
        return ConsolidationResult(
            atoms_consolidated=0,
            atoms_promoted=0,
            atoms_discarded=0,
            concepts_extracted=0,
            duration_ms=0,
            level_transition="SKIP"
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get consolidation statistics"""
        return {
            **self.stats,
            "working_memory": self.working_memory.get_stats(),
            "long_term_memory": self.long_term_memory.get_stats()
        }


# Global instance
_consolidator: MemoryConsolidator = None

def get_consolidator() -> MemoryConsolidator:
    """Get or create consolidator instance"""
    global _consolidator
    if _consolidator is None:
        _consolidator = MemoryConsolidator()
    return _consolidator


if __name__ == "__main__":
    print("=" * 60)
    print("MEMORY CONSOLIDATION ENGINE - TEST")
    print("=" * 60)

    consolidator = MemoryConsolidator()
    wm = consolidator.working_memory

    # Populate working memory
    print("\n[1] Populating working memory...")
    wm.store("atom1", "Deploy to Netlify", "decision")
    wm.store("atom2", "Build 7 Forges", "thought")
    wm.store("atom3", "Trinity pattern 3×7×13", "insight")
    wm.store("atom4", "Authentication bug", "error")
    wm.store("atom5", "Scalable memory architecture", "decision")

    # Simulate access
    wm.retrieve("atom1")
    wm.retrieve("atom1")
    wm.retrieve("atom3")
    wm.retrieve("atom5")
    wm.retrieve("atom5")
    wm.retrieve("atom5")

    print(f"   ✓ Stored 5 atoms")
    print(f"   ✓ Simulated access patterns")

    # Check working memory
    print("\n[2] Working memory status:")
    wm_stats = wm.get_stats()
    print(f"   Size: {wm_stats['current_size']}")
    print(f"   Utilization: {wm_stats['utilization']*100:.1f}%")

    # Consolidate
    print("\n[3] Consolidating L0 → L2...")
    result = consolidator.consolidate_working_to_long(significance_threshold=0.3)
    print(f"   Atoms consolidated: {result.atoms_consolidated}")
    print(f"   Atoms promoted: {result.atoms_promoted}")
    print(f"   Atoms discarded: {result.atoms_discarded}")
    print(f"   Duration: {result.duration_ms:.2f}ms")

    # Check after consolidation
    print("\n[4] After consolidation:")
    wm_stats = wm.get_stats()
    ltm_stats = consolidator.long_term_memory.get_stats()
    print(f"   Working memory size: {wm_stats['current_size']}")
    print(f"   Long-term atoms: {ltm_stats['total_atoms']}")

    # Auto consolidate
    print("\n[5] Testing auto-consolidation...")
    result = consolidator.auto_consolidate()
    print(f"   Transition: {result.level_transition}")
    print(f"   Atoms promoted: {result.atoms_promoted}")

    # Stats
    print("\n[6] Consolidator statistics:")
    stats = consolidator.get_stats()
    print(f"   Total consolidations: {stats['total_consolidations']}")
    print(f"   Total atoms promoted: {stats['total_atoms_promoted']}")
    print(f"   Total atoms discarded: {stats['total_atoms_discarded']}")

    print("\n" + "=" * 60)
    print("MEMORY CONSOLIDATION: OPERATIONAL")
    print("=" * 60)

"""
TOASTED AI - UNIFIED MEMORY CORE
=================================
Scalable 4-tier memory system with indexing, consolidation, and pruning.

Architecture:
- L0: Working Memory (5 min, 100 atoms, O(1))
- L1: Short-Term Memory (session, 1k atoms, O(log n))
- L2: Long-Term Memory (permanent, 1M+ atoms, FTS+vector)
- L∞: Refractal Memory (compressed patterns, 7.2:1 ratio)

Usage:
    from memory_core import get_memory_system

    memory = get_memory_system()

    # Store
    memory.store("Deploy to Netlify", atom_type="knowledge")

    # Retrieve
    results = memory.search("Netlify")

    # Auto-maintain
    memory.auto_maintain()
"""

from .working_memory import WorkingMemory, get_working_memory
from .long_term_memory import LongTermMemory, get_long_term_memory
from .memory_consolidator import MemoryConsolidator, get_consolidator
from .memory_retriever import MemoryRetriever, get_retriever
from .memory_pruner import MemoryPruner, get_pruner
from .refractal_memory import RefractalMemory, get_refractal_memory
from .fragmentation_handler import FragmentationHandler, get_handler

__version__ = "1.0.0"
__author__ = "C2 Architect"

__all__ = [
    # Core components
    "WorkingMemory",
    "LongTermMemory",
    "MemoryConsolidator",
    "MemoryRetriever",
    "MemoryPruner",
    "RefractalMemory",
    "FragmentationHandler",

    # Factory functions
    "get_working_memory",
    "get_long_term_memory",
    "get_consolidator",
    "get_retriever",
    "get_pruner",
    "get_refractal_memory",
    "get_handler",

    # Unified interface
    "get_memory_system",
    "UnifiedMemorySystem"
]


class UnifiedMemorySystem:
    """
    Unified interface to all memory systems.

    This is the main entry point for ToastedAI memory operations.
    """

    def __init__(self):
        self.working_memory = get_working_memory()
        self.long_term_memory = get_long_term_memory()
        self.consolidator = get_consolidator()
        self.retriever = get_retriever()
        self.pruner = get_pruner()
        self.refractal_memory = get_refractal_memory()
        self.fragmentation_handler = get_handler()

    def store(self, content: str, atom_type: str = "thought",
              tags: list = None, metadata: dict = None) -> str:
        """
        Store content in appropriate memory tier.

        Short-lived thoughts go to working memory.
        Important knowledge goes to long-term memory.
        """
        # Default: store in working memory
        atom_id = self.working_memory.store(
            atom_id=f"wm_{hash(content) % 1000000}",
            content=content,
            atom_type=atom_type,
            metadata=metadata or {}
        ).id

        # If important, also store in long-term
        if atom_type in ['decision', 'learning', 'insight', 'pattern']:
            atom_id = self.long_term_memory.store(
                content=content,
                atom_type=atom_type,
                tags=tags or [],
                metadata=metadata or {}
            )

        return atom_id

    def search(self, query: str, limit: int = 10):
        """Search across all memory tiers"""
        return self.retriever.search(query, limit=limit)

    def auto_maintain(self):
        """
        Automatic memory maintenance.

        - Consolidates working → long-term
        - Prunes old atoms
        - Fixes fragmentation
        """
        # Consolidate
        consolidation_result = self.consolidator.auto_consolidate()

        # Prune if needed
        pruning_result = self.pruner.auto_prune()

        # Check fragmentation
        frag_report = self.fragmentation_handler.scan_fragmentation()

        # Light repair if fragmented
        repair_result = None
        if frag_report.fragmentation_score > 0.1:  # 10% fragmented
            repair_result = self.fragmentation_handler.repair_light()

        return {
            "consolidation": {
                "atoms_promoted": consolidation_result.atoms_promoted,
                "duration_ms": consolidation_result.duration_ms
            },
            "pruning": {
                "atoms_deleted": pruning_result.atoms_deleted,
                "trigger": pruning_result.trigger
            },
            "fragmentation": {
                "score": frag_report.fragmentation_score,
                "repaired": repair_result.duplicates_merged if repair_result else 0
            }
        }

    def get_comprehensive_stats(self):
        """Get stats from all subsystems"""
        return {
            "working_memory": self.working_memory.get_stats(),
            "long_term_memory": self.long_term_memory.get_stats(),
            "retriever": self.retriever.get_stats(),
            "pruner": self.pruner.get_stats(),
            "refractal": self.refractal_memory.get_compression_stats(),
            "fragmentation": self.fragmentation_handler.get_stats()
        }


# Global instance
_memory_system = None

def get_memory_system() -> UnifiedMemorySystem:
    """Get or create unified memory system"""
    global _memory_system
    if _memory_system is None:
        _memory_system = UnifiedMemorySystem()
    return _memory_system

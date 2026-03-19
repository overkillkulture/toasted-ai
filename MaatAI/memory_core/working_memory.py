"""
WORKING MEMORY (L0) - Active Conversation Context
==================================================
Ultra-fast in-memory storage for current conversation.
Duration: 5 minutes | Max: 100 atoms | Access: O(1)
"""

import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from collections import OrderedDict

@dataclass
class WorkingAtom:
    """Single atom in working memory"""
    id: str
    content: str
    type: str
    timestamp: float = field(default_factory=time.time)
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def access(self):
        """Mark atom as accessed"""
        self.access_count += 1
        self.last_accessed = time.time()


class WorkingMemory:
    """
    L0 Memory - Active conversation context.

    Features:
    - O(1) hash-based lookup
    - Automatic expiration (5 min)
    - LRU eviction when full
    - Significance scoring for consolidation
    """

    MAX_SIZE = 100
    EXPIRATION_SECONDS = 300  # 5 minutes

    def __init__(self):
        self.atoms: OrderedDict[str, WorkingAtom] = OrderedDict()
        self.stats = {
            "total_stored": 0,
            "total_accessed": 0,
            "evictions": 0,
            "expirations": 0,
            "consolidations": 0
        }

    def store(self, atom_id: str, content: str, atom_type: str = "thought",
              metadata: Dict = None) -> WorkingAtom:
        """Store atom in working memory"""
        # Evict if full
        if len(self.atoms) >= self.MAX_SIZE:
            self._evict_lru()

        # Create atom
        atom = WorkingAtom(
            id=atom_id,
            content=content,
            type=atom_type,
            metadata=metadata or {}
        )

        self.atoms[atom_id] = atom
        self.stats["total_stored"] += 1

        return atom

    def retrieve(self, atom_id: str) -> Optional[WorkingAtom]:
        """Retrieve atom by ID"""
        atom = self.atoms.get(atom_id)

        if atom:
            # Check expiration
            if self._is_expired(atom):
                self.remove(atom_id)
                return None

            atom.access()
            self.stats["total_accessed"] += 1

            # Move to end (LRU)
            self.atoms.move_to_end(atom_id)

        return atom

    def search(self, query: str, limit: int = 10) -> List[WorkingAtom]:
        """Search atoms by content"""
        query_lower = query.lower()
        results = []

        for atom in self.atoms.values():
            if self._is_expired(atom):
                continue

            if query_lower in atom.content.lower():
                results.append(atom)
                atom.access()

            if len(results) >= limit:
                break

        return results

    def get_all(self) -> List[WorkingAtom]:
        """Get all non-expired atoms"""
        return [
            atom for atom in self.atoms.values()
            if not self._is_expired(atom)
        ]

    def get_significant(self, threshold: float = 0.5) -> List[WorkingAtom]:
        """Get significant atoms for consolidation"""
        atoms = []

        for atom in self.atoms.values():
            if self._is_expired(atom):
                continue

            significance = self._calculate_significance(atom)

            if significance >= threshold:
                atoms.append(atom)

        return atoms

    def remove(self, atom_id: str) -> bool:
        """Remove atom from working memory"""
        if atom_id in self.atoms:
            del self.atoms[atom_id]
            return True
        return False

    def clear_expired(self) -> int:
        """Remove all expired atoms"""
        expired_ids = [
            atom_id for atom_id, atom in self.atoms.items()
            if self._is_expired(atom)
        ]

        for atom_id in expired_ids:
            del self.atoms[atom_id]

        self.stats["expirations"] += len(expired_ids)
        return len(expired_ids)

    def clear(self):
        """Clear all atoms"""
        self.atoms.clear()

    def _evict_lru(self):
        """Evict least recently used atom"""
        if self.atoms:
            # OrderedDict maintains insertion order
            # LRU is at the front
            self.atoms.popitem(last=False)
            self.stats["evictions"] += 1

    def _is_expired(self, atom: WorkingAtom) -> bool:
        """Check if atom is expired"""
        age = time.time() - atom.timestamp
        return age > self.EXPIRATION_SECONDS

    def _calculate_significance(self, atom: WorkingAtom) -> float:
        """Calculate atom significance (0-1)"""
        # Factors:
        # - Access count (more = more significant)
        # - Type (decision/learning = more significant)
        # - Recency (newer = more significant)

        access_score = min(atom.access_count / 10.0, 0.5)

        type_scores = {
            "decision": 0.3,
            "learning": 0.3,
            "insight": 0.25,
            "error": 0.2,
            "thought": 0.1
        }
        type_score = type_scores.get(atom.type, 0.1)

        age = time.time() - atom.timestamp
        recency_score = max(0, (self.EXPIRATION_SECONDS - age) / self.EXPIRATION_SECONDS) * 0.2

        return access_score + type_score + recency_score

    def get_stats(self) -> Dict:
        """Get memory statistics"""
        now = time.time()
        ages = [now - atom.timestamp for atom in self.atoms.values()]

        return {
            **self.stats,
            "current_size": len(self.atoms),
            "max_size": self.MAX_SIZE,
            "utilization": len(self.atoms) / self.MAX_SIZE,
            "avg_age_seconds": sum(ages) / len(ages) if ages else 0,
            "oldest_age_seconds": max(ages) if ages else 0
        }


# Global instance
_working_memory: Optional[WorkingMemory] = None

def get_working_memory() -> WorkingMemory:
    """Get or create working memory instance"""
    global _working_memory
    if _working_memory is None:
        _working_memory = WorkingMemory()
    return _working_memory


if __name__ == "__main__":
    print("=" * 60)
    print("WORKING MEMORY (L0) - TEST")
    print("=" * 60)

    wm = WorkingMemory()

    # Store some atoms
    print("\n[1] Storing atoms...")
    wm.store("atom1", "Deploy to Netlify", "decision")
    wm.store("atom2", "Build 7 Forges", "thought")
    wm.store("atom3", "Trinity pattern 3×7×13", "insight")
    wm.store("atom4", "Authentication bug", "error")
    print(f"   ✓ Stored 4 atoms")

    # Retrieve
    print("\n[2] Retrieving atom...")
    atom = wm.retrieve("atom1")
    print(f"   Content: {atom.content}")
    print(f"   Access count: {atom.access_count}")

    # Search
    print("\n[3] Searching 'pattern'...")
    results = wm.search("pattern")
    print(f"   Found: {len(results)} results")
    for r in results:
        print(f"   - {r.content}")

    # Significance
    print("\n[4] Getting significant atoms...")
    significant = wm.get_significant(threshold=0.3)
    print(f"   Significant atoms: {len(significant)}")
    for s in significant:
        sig = wm._calculate_significance(s)
        print(f"   - {s.content} (sig={sig:.2f})")

    # Stats
    print("\n[5] Statistics:")
    stats = wm.get_stats()
    print(f"   Size: {stats['current_size']}/{stats['max_size']}")
    print(f"   Utilization: {stats['utilization']*100:.1f}%")
    print(f"   Avg age: {stats['avg_age_seconds']:.1f}s")
    print(f"   Total stored: {stats['total_stored']}")
    print(f"   Total accessed: {stats['total_accessed']}")

    print("\n" + "=" * 60)
    print("WORKING MEMORY: OPERATIONAL")
    print("=" * 60)

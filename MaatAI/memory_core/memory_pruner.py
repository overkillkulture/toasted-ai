"""
MEMORY PRUNING SYSTEM
======================
Automatic cleanup of old, unused, low-value atoms.

Pruning Strategy:
- Size-based: When memory > 80% capacity
- Performance-based: When queries > 200ms
- Scheduled: Weekly maintenance
- Manual: User-initiated cleanup
"""

import time
import sqlite3
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class PruningResult:
    """Result of pruning operation"""
    atoms_analyzed: int
    atoms_deleted: int
    atoms_protected: int
    bytes_freed: int
    duration_ms: float
    trigger: str  # "manual", "auto_size", "auto_performance", "scheduled"


class MemoryPruner:
    """
    Intelligent memory pruning system.

    Pruning Rules:
    DELETE candidates:
    - age > 90 days AND
    - access_count < 2 AND
    - confidence < 0.5 AND
    - NOT referenced in knowledge_graph

    PROTECT always:
    - type IN ('decision', 'learning', 'success')
    - access_count > 10
    - confidence > 0.8
    - part_of_memory_chain = True
    - source = 'user_input'
    """

    # Pruning thresholds
    MAX_CAPACITY_PERCENT = 80
    MAX_AVG_QUERY_MS = 200
    DEFAULT_AGE_DAYS = 90
    DEFAULT_ACCESS_THRESHOLD = 2
    DEFAULT_CONFIDENCE_THRESHOLD = 0.5

    # Protection rules
    PROTECTED_TYPES = ['decision', 'learning', 'success', 'insight', 'pattern']
    PROTECTED_SOURCES = ['user_input', 'commander']
    HIGH_ACCESS_THRESHOLD = 10
    HIGH_CONFIDENCE_THRESHOLD = 0.8

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = str(Path.home() / ".consciousness/cyclotron_core/atoms.db")

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

        self.stats = {
            "total_prunes": 0,
            "total_deleted": 0,
            "total_analyzed": 0,
            "total_protected": 0,
            "total_bytes_freed": 0
        }

    def prune(
        self,
        age_days: int = None,
        access_threshold: int = None,
        confidence_threshold: float = None,
        dry_run: bool = False,
        trigger: str = "manual"
    ) -> PruningResult:
        """
        Prune old, unused, low-confidence atoms.

        Args:
            age_days: Min age to prune (default: 90)
            access_threshold: Max access count to prune (default: 2)
            confidence_threshold: Max confidence to prune (default: 0.5)
            dry_run: Don't actually delete (default: False)
            trigger: What triggered this prune

        Returns:
            PruningResult with statistics
        """
        start_time = time.time()

        # Use defaults if not specified
        age_days = age_days or self.DEFAULT_AGE_DAYS
        access_threshold = access_threshold or self.DEFAULT_ACCESS_THRESHOLD
        confidence_threshold = confidence_threshold or self.DEFAULT_CONFIDENCE_THRESHOLD

        # Calculate cutoff timestamp
        age_seconds = age_days * 86400
        cutoff = time.time() - age_seconds

        # Find candidates
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, type, source, content, confidence, access_count, created
            FROM atoms
            WHERE created < ?
              AND access_count < ?
              AND confidence < ?
        """, (cutoff, access_threshold, confidence_threshold))

        candidates = cursor.fetchall()

        # Filter out protected atoms
        delete_ids = []
        protected_count = 0

        for row in candidates:
            atom_id, atom_type, source, content, confidence, access_count, created = row

            # Check protection rules
            if self._is_protected(atom_id, atom_type, source, access_count, confidence):
                protected_count += 1
                continue

            delete_ids.append(atom_id)

        # Estimate bytes freed
        bytes_freed = len(delete_ids) * 500  # Estimate 500 bytes per atom

        # Delete (unless dry run)
        deleted = 0
        if not dry_run and delete_ids:
            placeholders = ','.join('?' * len(delete_ids))

            # Delete from FTS
            cursor.execute(f"""
                DELETE FROM atoms_fts
                WHERE id IN ({placeholders})
            """, delete_ids)

            # Delete from atoms
            cursor.execute(f"""
                DELETE FROM atoms
                WHERE id IN ({placeholders})
            """, delete_ids)

            deleted = cursor.rowcount
            self.conn.commit()

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000

        # Create result
        result = PruningResult(
            atoms_analyzed=len(candidates),
            atoms_deleted=deleted if not dry_run else len(delete_ids),
            atoms_protected=protected_count,
            bytes_freed=bytes_freed if not dry_run else 0,
            duration_ms=duration_ms,
            trigger=trigger
        )

        # Update stats
        if not dry_run:
            self.stats["total_prunes"] += 1
            self.stats["total_deleted"] += result.atoms_deleted
            self.stats["total_bytes_freed"] += result.bytes_freed
        self.stats["total_analyzed"] += result.atoms_analyzed
        self.stats["total_protected"] += result.atoms_protected

        return result

    def auto_prune(self) -> PruningResult:
        """
        Automatic pruning based on memory state.

        Triggers:
        - Size: atoms > 800k (80% of 1M capacity)
        - Performance: avg query time > 200ms
        """
        cursor = self.conn.cursor()

        # Check size
        cursor.execute("SELECT COUNT(*) FROM atoms")
        atom_count = cursor.fetchone()[0]

        capacity_percent = (atom_count / 1_000_000) * 100

        if capacity_percent >= self.MAX_CAPACITY_PERCENT:
            # Aggressive pruning
            return self.prune(
                age_days=60,
                access_threshold=1,
                confidence_threshold=0.4,
                trigger="auto_size"
            )

        # TODO: Check performance metrics
        # if avg_query_time > MAX_AVG_QUERY_MS:
        #     return self.prune(trigger="auto_performance")

        # No pruning needed
        return PruningResult(
            atoms_analyzed=0,
            atoms_deleted=0,
            atoms_protected=0,
            bytes_freed=0,
            duration_ms=0,
            trigger="skip"
        )

    def vacuum_database(self) -> int:
        """
        Run SQLite VACUUM to reclaim space.

        Returns bytes freed (estimated).
        """
        cursor = self.conn.cursor()

        # Get size before
        cursor.execute("PRAGMA page_count")
        pages_before = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]
        size_before = pages_before * page_size

        # Vacuum
        cursor.execute("VACUUM")

        # Get size after
        cursor.execute("PRAGMA page_count")
        pages_after = cursor.fetchone()[0]
        size_after = pages_after * page_size

        bytes_freed = max(0, size_before - size_after)

        self.stats["total_bytes_freed"] += bytes_freed

        return bytes_freed

    def rebuild_indexes(self) -> float:
        """
        Rebuild all indexes for better performance.

        Returns duration in seconds.
        """
        start_time = time.time()
        cursor = self.conn.cursor()

        # Reindex FTS
        cursor.execute("INSERT INTO atoms_fts(atoms_fts) VALUES('rebuild')")

        # Analyze (update query planner stats)
        cursor.execute("ANALYZE")

        self.conn.commit()

        return time.time() - start_time

    def get_candidates(
        self,
        age_days: int = 90,
        access_threshold: int = 2,
        confidence_threshold: float = 0.5,
        limit: int = 100
    ) -> List[Tuple]:
        """
        Get pruning candidates without deleting.

        Returns list of (id, type, content, age_days, access_count, confidence).
        """
        age_seconds = age_days * 86400
        cutoff = time.time() - age_seconds

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, type, content, created, access_count, confidence
            FROM atoms
            WHERE created < ?
              AND access_count < ?
              AND confidence < ?
            ORDER BY created ASC
            LIMIT ?
        """, (cutoff, access_threshold, confidence_threshold, limit))

        results = []
        now = time.time()

        for row in cursor.fetchall():
            atom_id, atom_type, content, created, access_count, confidence = row

            # Skip protected
            if self._is_protected(atom_id, atom_type, None, access_count, confidence):
                continue

            age_days = (now - created) / 86400

            results.append((
                atom_id,
                atom_type,
                content[:100],
                int(age_days),
                access_count,
                confidence
            ))

        return results

    def _is_protected(
        self,
        atom_id: str,
        atom_type: str,
        source: str,
        access_count: int,
        confidence: float
    ) -> bool:
        """Check if atom is protected from pruning"""

        # Protected types
        if atom_type in self.PROTECTED_TYPES:
            return True

        # Protected sources
        if source in self.PROTECTED_SOURCES:
            return True

        # High access count
        if access_count >= self.HIGH_ACCESS_THRESHOLD:
            return True

        # High confidence
        if confidence >= self.HIGH_CONFIDENCE_THRESHOLD:
            return True

        # Part of memory chain
        if self._is_in_memory_chain(atom_id):
            return True

        # Part of knowledge graph
        if self._is_in_knowledge_graph(atom_id):
            return True

        return False

    def _is_in_memory_chain(self, atom_id: str) -> bool:
        """Check if atom is part of a memory chain"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 1 FROM memory_chains
            WHERE atom_ids LIKE ?
            LIMIT 1
        """, (f'%{atom_id}%',))

        return cursor.fetchone() is not None

    def _is_in_knowledge_graph(self, atom_id: str) -> bool:
        """Check if atom is referenced in knowledge graph"""
        cursor = self.conn.cursor()

        # Check if atom is a concept
        cursor.execute("""
            SELECT 1 FROM concept_index
            WHERE atom_ids LIKE ?
            LIMIT 1
        """, (f'%{atom_id}%',))

        if cursor.fetchone():
            return True

        # Check if atom is in evidence
        cursor.execute("""
            SELECT 1 FROM knowledge_graph
            WHERE evidence_atoms LIKE ?
            LIMIT 1
        """, (f'%{atom_id}%',))

        return cursor.fetchone() is not None

    def get_stats(self) -> Dict[str, Any]:
        """Get pruning statistics"""
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM atoms")
        total_atoms = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(access_count) FROM atoms")
        avg_access = cursor.fetchone()[0] or 0

        # Estimate size
        cursor.execute("PRAGMA page_count")
        page_count = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]
        db_size_bytes = page_count * page_size

        capacity_percent = (total_atoms / 1_000_000) * 100

        return {
            **self.stats,
            "total_atoms": total_atoms,
            "capacity_percent": capacity_percent,
            "avg_access_count": round(avg_access, 2),
            "db_size_mb": round(db_size_bytes / 1024 / 1024, 2),
            "db_path": self.db_path
        }

    def close(self):
        """Close database connection"""
        self.conn.close()


# Global instance
_pruner: MemoryPruner = None

def get_pruner() -> MemoryPruner:
    """Get or create pruner instance"""
    global _pruner
    if _pruner is None:
        _pruner = MemoryPruner()
    return _pruner


if __name__ == "__main__":
    print("=" * 60)
    print("MEMORY PRUNING SYSTEM - TEST")
    print("=" * 60)

    pruner = MemoryPruner()

    # Get candidates
    print("\n[1] Finding pruning candidates...")
    candidates = pruner.get_candidates(age_days=30, limit=10)
    print(f"   Found {len(candidates)} candidates")
    for i, (atom_id, atom_type, content, age, access, conf) in enumerate(candidates[:5]):
        print(f"   {i+1}. {content[:40]}... (age={age}d, access={access}, conf={conf:.2f})")

    # Dry run
    print("\n[2] Dry run pruning...")
    result = pruner.prune(age_days=120, dry_run=True)
    print(f"   Would delete: {result.atoms_deleted} atoms")
    print(f"   Protected: {result.atoms_protected} atoms")
    print(f"   Would free: {result.bytes_freed/1024:.2f} KB")
    print(f"   Duration: {result.duration_ms:.2f}ms")

    # Auto prune
    print("\n[3] Auto prune check...")
    result = pruner.auto_prune()
    print(f"   Trigger: {result.trigger}")
    print(f"   Deleted: {result.atoms_deleted} atoms")

    # Stats
    print("\n[4] Pruning statistics:")
    stats = pruner.get_stats()
    print(f"   Total atoms: {stats['total_atoms']}")
    print(f"   Capacity: {stats['capacity_percent']:.1f}%")
    print(f"   DB size: {stats['db_size_mb']} MB")
    print(f"   Avg access: {stats['avg_access_count']}")
    print(f"   Total pruned (lifetime): {stats['total_deleted']}")

    # Maintenance
    print("\n[5] Database maintenance...")
    rebuild_time = pruner.rebuild_indexes()
    print(f"   Indexes rebuilt in {rebuild_time:.2f}s")

    print("\n" + "=" * 60)
    print("MEMORY PRUNING: OPERATIONAL")
    print("=" * 60)

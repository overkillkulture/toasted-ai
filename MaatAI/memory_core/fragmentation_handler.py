"""
MEMORY FRAGMENTATION HANDLER
=============================
Detects and repairs fragmented memory structures.

Fragmentation Types:
1. Orphaned atoms (no connections)
2. Broken references (dangling pointers)
3. Duplicate atoms (same content, different IDs)
4. Concept drift (concepts split across IDs)
"""

import time
import sqlite3
import json
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FragmentationReport:
    """Report of memory fragmentation"""
    total_atoms: int
    orphaned_atoms: int
    broken_references: int
    duplicates: int
    fragmentation_score: float  # 0-1, higher = more fragmented
    repair_actions: List[str]


@dataclass
class RepairResult:
    """Result of fragmentation repair"""
    orphans_fixed: int
    references_fixed: int
    duplicates_merged: int
    concepts_consolidated: int
    duration_ms: float
    actions_taken: List[str]


class FragmentationHandler:
    """
    Detects and repairs memory fragmentation.

    Defragmentation Schedule:
    - Light: Daily (5 min) - Find obvious duplicates
    - Medium: Weekly (30 min) - Full orphan scan
    - Heavy: Monthly (2 hrs) - Complete rebuild + vacuum
    """

    # Thresholds
    ORPHAN_AGE_DAYS = 30
    BROKEN_REF_THRESHOLD = 0.05  # 5% broken refs = problem
    DUPLICATE_SIMILARITY = 0.95  # 95% similar = duplicate

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = str(Path.home() / ".consciousness/cyclotron_core/atoms.db")

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

        self.stats = {
            "total_scans": 0,
            "total_repairs": 0,
            "orphans_fixed": 0,
            "duplicates_merged": 0,
            "references_fixed": 0
        }

    def scan_fragmentation(self) -> FragmentationReport:
        """
        Scan for memory fragmentation.

        Returns:
            FragmentationReport with analysis
        """
        cursor = self.conn.cursor()

        # Get total atoms
        cursor.execute("SELECT COUNT(*) FROM atoms")
        total_atoms = cursor.fetchone()[0]

        # Find orphaned atoms
        orphaned = self._find_orphaned_atoms()

        # Find broken references
        broken_refs = self._find_broken_references()

        # Find duplicates
        duplicates = self._find_duplicate_atoms()

        # Calculate fragmentation score
        orphan_score = len(orphaned) / max(total_atoms, 1)
        ref_score = len(broken_refs) / max(total_atoms, 1)
        dup_score = len(duplicates) / max(total_atoms, 1)

        fragmentation_score = (orphan_score + ref_score + dup_score) / 3

        # Generate repair actions
        repair_actions = []
        if len(orphaned) > 0:
            repair_actions.append(f"Archive {len(orphaned)} orphaned atoms")
        if len(broken_refs) > 0:
            repair_actions.append(f"Fix {len(broken_refs)} broken references")
        if len(duplicates) > 0:
            repair_actions.append(f"Merge {len(duplicates)} duplicate atoms")

        self.stats["total_scans"] += 1

        return FragmentationReport(
            total_atoms=total_atoms,
            orphaned_atoms=len(orphaned),
            broken_references=len(broken_refs),
            duplicates=len(duplicates),
            fragmentation_score=fragmentation_score,
            repair_actions=repair_actions
        )

    def repair_light(self) -> RepairResult:
        """
        Light repair: Fix obvious duplicates.

        Duration: ~5 minutes
        """
        start_time = time.time()
        actions = []

        # Find and merge duplicates
        duplicates = self._find_duplicate_atoms(limit=100)
        duplicates_merged = 0

        for dup_id1, dup_id2 in duplicates:
            if self._merge_atoms(dup_id1, dup_id2):
                duplicates_merged += 1
                actions.append(f"Merged {dup_id1} → {dup_id2}")

        duration_ms = (time.time() - start_time) * 1000

        self.stats["total_repairs"] += 1
        self.stats["duplicates_merged"] += duplicates_merged

        return RepairResult(
            orphans_fixed=0,
            references_fixed=0,
            duplicates_merged=duplicates_merged,
            concepts_consolidated=0,
            duration_ms=duration_ms,
            actions_taken=actions
        )

    def repair_medium(self) -> RepairResult:
        """
        Medium repair: Full orphan scan + duplicate fix.

        Duration: ~30 minutes
        """
        start_time = time.time()
        actions = []

        # Fix orphans
        orphaned = self._find_orphaned_atoms()
        orphans_fixed = 0

        for atom_id in orphaned[:500]:  # Limit to 500
            if self._try_link_orphan(atom_id):
                orphans_fixed += 1
                actions.append(f"Linked orphan {atom_id}")
            else:
                # Archive to refractal
                self._archive_atom(atom_id)
                actions.append(f"Archived orphan {atom_id}")

        # Fix duplicates
        duplicates = self._find_duplicate_atoms(limit=200)
        duplicates_merged = 0

        for dup_id1, dup_id2 in duplicates:
            if self._merge_atoms(dup_id1, dup_id2):
                duplicates_merged += 1

        duration_ms = (time.time() - start_time) * 1000

        self.stats["total_repairs"] += 1
        self.stats["orphans_fixed"] += orphans_fixed
        self.stats["duplicates_merged"] += duplicates_merged

        return RepairResult(
            orphans_fixed=orphans_fixed,
            references_fixed=0,
            duplicates_merged=duplicates_merged,
            concepts_consolidated=0,
            duration_ms=duration_ms,
            actions_taken=actions
        )

    def repair_heavy(self) -> RepairResult:
        """
        Heavy repair: Complete rebuild + vacuum.

        Duration: ~2 hours
        """
        start_time = time.time()
        actions = []

        # 1. Fix all orphans
        orphaned = self._find_orphaned_atoms()
        orphans_fixed = 0

        for atom_id in orphaned:
            if self._try_link_orphan(atom_id):
                orphans_fixed += 1
            else:
                self._archive_atom(atom_id)

        actions.append(f"Fixed {orphans_fixed} orphans")

        # 2. Fix all broken references
        broken_refs = self._find_broken_references()
        references_fixed = 0

        for ref in broken_refs:
            if self._fix_broken_reference(ref):
                references_fixed += 1

        actions.append(f"Fixed {references_fixed} references")

        # 3. Merge all duplicates
        duplicates = self._find_duplicate_atoms(limit=None)
        duplicates_merged = 0

        for dup_id1, dup_id2 in duplicates:
            if self._merge_atoms(dup_id1, dup_id2):
                duplicates_merged += 1

        actions.append(f"Merged {duplicates_merged} duplicates")

        # 4. Consolidate concepts
        concepts_consolidated = self._consolidate_concepts()
        actions.append(f"Consolidated {concepts_consolidated} concepts")

        # 5. Rebuild indexes
        self._rebuild_indexes()
        actions.append("Rebuilt all indexes")

        # 6. Vacuum database
        self.conn.execute("VACUUM")
        actions.append("Vacuumed database")

        duration_ms = (time.time() - start_time) * 1000

        self.stats["total_repairs"] += 1
        self.stats["orphans_fixed"] += orphans_fixed
        self.stats["references_fixed"] += references_fixed
        self.stats["duplicates_merged"] += duplicates_merged

        return RepairResult(
            orphans_fixed=orphans_fixed,
            references_fixed=references_fixed,
            duplicates_merged=duplicates_merged,
            concepts_consolidated=concepts_consolidated,
            duration_ms=duration_ms,
            actions_taken=actions
        )

    def _find_orphaned_atoms(self) -> List[str]:
        """Find atoms with no connections"""
        cursor = self.conn.cursor()

        # Find atoms not in knowledge graph
        cursor.execute("""
            SELECT id FROM atoms
            WHERE id NOT IN (
                SELECT DISTINCT from_concept FROM knowledge_graph
                UNION
                SELECT DISTINCT to_concept FROM knowledge_graph
            )
            AND id NOT IN (
                SELECT DISTINCT json_extract(value, '$')
                FROM concept_index, json_each(concept_index.atom_ids)
            )
            AND access_count = 0
        """)

        return [row[0] for row in cursor.fetchall()]

    def _find_broken_references(self) -> List[Dict]:
        """Find broken references in knowledge graph"""
        cursor = self.conn.cursor()

        broken = []

        # Find references to non-existent atoms
        cursor.execute("""
            SELECT from_concept, to_concept
            FROM knowledge_graph
            WHERE from_concept NOT IN (SELECT id FROM atoms)
               OR to_concept NOT IN (SELECT id FROM atoms)
        """)

        for row in cursor.fetchall():
            broken.append({
                'from': row[0],
                'to': row[1]
            })

        return broken

    def _find_duplicate_atoms(self, limit: int = None) -> List[Tuple[str, str]]:
        """Find duplicate atoms (same content)"""
        cursor = self.conn.cursor()

        query = """
            SELECT a1.id, a2.id
            FROM atoms a1
            JOIN atoms a2 ON a1.content = a2.content
            WHERE a1.id < a2.id
        """

        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query)

        return [(row[0], row[1]) for row in cursor.fetchall()]

    def _try_link_orphan(self, atom_id: str) -> bool:
        """Try to link orphaned atom to knowledge graph"""
        cursor = self.conn.cursor()

        # Get atom content
        cursor.execute("SELECT content FROM atoms WHERE id = ?", (atom_id,))
        row = cursor.fetchone()
        if not row:
            return False

        content = row[0]

        # Extract potential concepts
        words = content.lower().split()
        concepts = [w for w in words if len(w) > 4][:3]

        # Try to link to existing concepts
        for concept in concepts:
            cursor.execute("""
                SELECT concept FROM concept_index
                WHERE concept LIKE ?
                LIMIT 1
            """, (f"%{concept}%",))

            match = cursor.fetchone()
            if match:
                # Add to concept index
                cursor.execute("""
                    UPDATE concept_index
                    SET atom_ids = json_insert(atom_ids, '$[#]', ?)
                    WHERE concept = ?
                """, (atom_id, match[0]))

                self.conn.commit()
                return True

        return False

    def _merge_atoms(self, keep_id: str, merge_id: str) -> bool:
        """Merge two duplicate atoms"""
        cursor = self.conn.cursor()

        try:
            # Update references from merge_id to keep_id in knowledge_graph
            cursor.execute("""
                UPDATE knowledge_graph
                SET from_concept = ?
                WHERE from_concept = ?
            """, (keep_id, merge_id))

            cursor.execute("""
                UPDATE knowledge_graph
                SET to_concept = ?
                WHERE to_concept = ?
            """, (keep_id, merge_id))

            # Update concept_index
            cursor.execute("""
                UPDATE concept_index
                SET atom_ids = replace(atom_ids, ?, ?)
            """, (f'"{merge_id}"', f'"{keep_id}"'))

            # Delete merged atom
            cursor.execute("DELETE FROM atoms WHERE id = ?", (merge_id,))
            cursor.execute("DELETE FROM atoms_fts WHERE id = ?", (merge_id,))

            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            return False

    def _fix_broken_reference(self, ref: Dict) -> bool:
        """Fix a broken reference"""
        # Simple fix: delete the broken reference
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                DELETE FROM knowledge_graph
                WHERE from_concept = ? AND to_concept = ?
            """, (ref['from'], ref['to']))

            self.conn.commit()
            return True

        except Exception:
            self.conn.rollback()
            return False

    def _archive_atom(self, atom_id: str):
        """Archive atom to refractal memory"""
        # TODO: Integrate with refractal_memory.py
        # For now, just mark as archived
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE atoms
            SET metadata = json_set(metadata, '$.archived', 1)
            WHERE id = ?
        """, (atom_id,))
        self.conn.commit()

    def _consolidate_concepts(self) -> int:
        """Consolidate fragmented concepts"""
        cursor = self.conn.cursor()

        # Find concepts that should be merged
        cursor.execute("""
            SELECT c1.concept, c2.concept
            FROM concept_index c1
            JOIN concept_index c2 ON (
                c1.concept LIKE '%' || c2.concept || '%'
                OR c2.concept LIKE '%' || c1.concept || '%'
            )
            WHERE c1.concept < c2.concept
        """)

        merged = 0
        for row in cursor.fetchall():
            concept1, concept2 = row

            # Merge concept2 into concept1
            cursor.execute("""
                UPDATE concept_index
                SET atom_ids = (
                    SELECT json_group_array(DISTINCT value)
                    FROM (
                        SELECT value FROM json_each((SELECT atom_ids FROM concept_index WHERE concept = ?))
                        UNION
                        SELECT value FROM json_each((SELECT atom_ids FROM concept_index WHERE concept = ?))
                    )
                )
                WHERE concept = ?
            """, (concept1, concept2, concept1))

            cursor.execute("DELETE FROM concept_index WHERE concept = ?", (concept2,))
            merged += 1

        self.conn.commit()
        return merged

    def _rebuild_indexes(self):
        """Rebuild all indexes"""
        cursor = self.conn.cursor()
        cursor.execute("REINDEX")
        cursor.execute("INSERT INTO atoms_fts(atoms_fts) VALUES('rebuild')")
        cursor.execute("ANALYZE")
        self.conn.commit()

    def get_stats(self) -> Dict[str, Any]:
        """Get fragmentation statistics"""
        return {
            **self.stats,
            "db_path": self.db_path
        }

    def close(self):
        """Close database connection"""
        self.conn.close()


# Global instance
_handler: FragmentationHandler = None

def get_handler() -> FragmentationHandler:
    """Get or create handler instance"""
    global _handler
    if _handler is None:
        _handler = FragmentationHandler()
    return _handler


if __name__ == "__main__":
    print("=" * 60)
    print("FRAGMENTATION HANDLER - TEST")
    print("=" * 60)

    handler = FragmentationHandler()

    # Scan
    print("\n[1] Scanning for fragmentation...")
    report = handler.scan_fragmentation()
    print(f"   Total atoms: {report.total_atoms}")
    print(f"   Orphaned: {report.orphaned_atoms}")
    print(f"   Broken refs: {report.broken_references}")
    print(f"   Duplicates: {report.duplicates}")
    print(f"   Fragmentation score: {report.fragmentation_score:.2%}")
    print(f"   Recommended actions:")
    for action in report.repair_actions:
        print(f"     - {action}")

    # Light repair
    print("\n[2] Running light repair...")
    result = handler.repair_light()
    print(f"   Duplicates merged: {result.duplicates_merged}")
    print(f"   Duration: {result.duration_ms:.0f}ms")

    # Stats
    print("\n[3] Handler statistics:")
    stats = handler.get_stats()
    print(f"   Total scans: {stats['total_scans']}")
    print(f"   Total repairs: {stats['total_repairs']}")
    print(f"   Orphans fixed: {stats['orphans_fixed']}")
    print(f"   Duplicates merged: {stats['duplicates_merged']}")

    print("\n" + "=" * 60)
    print("FRAGMENTATION HANDLER: OPERATIONAL")
    print("=" * 60)

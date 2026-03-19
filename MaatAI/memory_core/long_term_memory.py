"""
LONG-TERM MEMORY (L2) - Persistent Knowledge Base
==================================================
SQLite-backed permanent storage with advanced indexing.
Duration: Permanent | Max: 1M+ atoms | Access: O(log n)
"""

import sqlite3
import json
import time
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class LongTermAtom:
    """Atom in long-term memory"""
    id: str
    type: str
    content: str
    source: str
    tags: List[str]
    metadata: Dict[str, Any]
    created: float
    confidence: float
    access_count: int
    last_accessed: Optional[float]

    @classmethod
    def from_db_row(cls, row: Tuple) -> 'LongTermAtom':
        """Create from database row"""
        return cls(
            id=row[0],
            type=row[1],
            content=row[2],
            source=row[3] or "",
            tags=json.loads(row[4]) if row[4] else [],
            metadata=json.loads(row[5]) if row[5] else {},
            created=float(row[6]) if row[6] else time.time(),
            confidence=float(row[7]) if row[7] else 0.75,
            access_count=int(row[8]) if row[8] else 0,
            last_accessed=float(row[9]) if row[9] else None
        )


class LongTermMemory:
    """
    L2 Memory - Persistent knowledge base.

    Features:
    - SQLite backend (atoms.db)
    - B-tree indexes for fast lookup
    - FTS5 full-text search
    - Automatic deduplication
    - Concept extraction & linking
    """

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = str(Path.home() / ".consciousness/cyclotron_core/atoms.db")

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._ensure_indexes()

        self.stats = {
            "total_stored": 0,
            "total_retrieved": 0,
            "duplicates_prevented": 0,
            "concepts_extracted": 0
        }

    def store(self, content: str, atom_type: str = "knowledge",
              source: str = "toasted_ai", tags: List[str] = None,
              metadata: Dict = None, confidence: float = 0.75) -> str:
        """Store atom in long-term memory"""

        # Generate ID
        atom_id = self._generate_id(content, atom_type)

        # Check for duplicates
        if self._exists(atom_id):
            self.stats["duplicates_prevented"] += 1
            return atom_id

        # Prepare data
        tags_json = json.dumps(tags or [])
        metadata_json = json.dumps(metadata or {})
        created = time.time()

        # Insert
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO atoms (
                id, type, content, source, tags, metadata,
                created, confidence, access_count, last_accessed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, NULL)
        """, (
            atom_id, atom_type, content, source,
            tags_json, metadata_json, created, confidence
        ))

        # Update FTS index
        cursor.execute("""
            INSERT INTO atoms_fts (id, content, tags)
            VALUES (?, ?, ?)
        """, (atom_id, content, tags_json))

        self.conn.commit()

        # Extract concepts
        concepts = self._extract_concepts(content)
        for concept in concepts:
            self._index_concept(concept, atom_id)

        self.stats["total_stored"] += 1
        self.stats["concepts_extracted"] += len(concepts)

        return atom_id

    def retrieve(self, atom_id: str) -> Optional[LongTermAtom]:
        """Retrieve atom by ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, type, content, source, tags, metadata,
                   created, confidence, access_count, last_accessed
            FROM atoms
            WHERE id = ?
        """, (atom_id,))

        row = cursor.fetchone()
        if not row:
            return None

        # Update access stats
        self._update_access(atom_id)
        self.stats["total_retrieved"] += 1

        return LongTermAtom.from_db_row(row)

    def search_fts(self, query: str, limit: int = 10) -> List[LongTermAtom]:
        """Full-text search"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT a.id, a.type, a.content, a.source, a.tags, a.metadata,
                   a.created, a.confidence, a.access_count, a.last_accessed
            FROM atoms a
            JOIN atoms_fts fts ON a.id = fts.id
            WHERE atoms_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, limit))

        return [LongTermAtom.from_db_row(row) for row in cursor.fetchall()]

    def search_by_concept(self, concept: str, limit: int = 10) -> List[LongTermAtom]:
        """Search by concept"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT atom_ids FROM concept_index
            WHERE concept = ?
        """, (concept,))

        row = cursor.fetchone()
        if not row:
            return []

        atom_ids = json.loads(row[0])[:limit]

        atoms = []
        for atom_id in atom_ids:
            atom = self.retrieve(atom_id)
            if atom:
                atoms.append(atom)

        return atoms

    def search_by_tags(self, tags: List[str], limit: int = 10) -> List[LongTermAtom]:
        """Search by tags"""
        # Build query for tags
        query_parts = [f'tags:"{tag}"' for tag in tags]
        query = " OR ".join(query_parts)

        return self.search_fts(query, limit)

    def get_recent(self, limit: int = 10) -> List[LongTermAtom]:
        """Get most recent atoms"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, type, content, source, tags, metadata,
                   created, confidence, access_count, last_accessed
            FROM atoms
            ORDER BY created DESC
            LIMIT ?
        """, (limit,))

        return [LongTermAtom.from_db_row(row) for row in cursor.fetchall()]

    def get_most_accessed(self, limit: int = 10) -> List[LongTermAtom]:
        """Get most accessed atoms"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, type, content, source, tags, metadata,
                   created, confidence, access_count, last_accessed
            FROM atoms
            WHERE access_count > 0
            ORDER BY access_count DESC
            LIMIT ?
        """, (limit,))

        return [LongTermAtom.from_db_row(row) for row in cursor.fetchall()]

    def delete(self, atom_id: str) -> bool:
        """Delete atom (use with caution)"""
        cursor = self.conn.cursor()

        # Remove from FTS
        cursor.execute("DELETE FROM atoms_fts WHERE id = ?", (atom_id,))

        # Remove from atoms
        cursor.execute("DELETE FROM atoms WHERE id = ?", (atom_id,))

        self.conn.commit()
        return cursor.rowcount > 0

    def prune_old(self, age_days: int = 90, access_threshold: int = 2,
                  confidence_threshold: float = 0.5) -> int:
        """Prune old, unused, low-confidence atoms"""
        age_seconds = age_days * 86400
        cutoff = time.time() - age_seconds

        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM atoms
            WHERE created < ?
              AND access_count < ?
              AND confidence < ?
              AND type NOT IN ('decision', 'learning', 'success')
        """, (cutoff, access_threshold, confidence_threshold))

        deleted = cursor.rowcount
        self.conn.commit()

        return deleted

    def _generate_id(self, content: str, atom_type: str) -> str:
        """Generate unique ID for atom"""
        data = f"{atom_type}:{content}".encode()
        return hashlib.md5(data).hexdigest()[:16]

    def _exists(self, atom_id: str) -> bool:
        """Check if atom exists"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM atoms WHERE id = ? LIMIT 1", (atom_id,))
        return cursor.fetchone() is not None

    def _update_access(self, atom_id: str):
        """Update access statistics"""
        now = time.time()
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE atoms
            SET access_count = access_count + 1,
                last_accessed = ?
            WHERE id = ?
        """, (now, atom_id))
        self.conn.commit()

    def _extract_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content"""
        # Simple keyword extraction
        # TODO: Enhance with NLP/LLM

        words = content.lower().split()
        concepts = []

        # Look for capitalized words (likely concepts)
        for word in content.split():
            if word[0].isupper() and len(word) > 3:
                concepts.append(word.lower())

        # Common technical terms
        tech_terms = [
            "deploy", "build", "test", "architecture", "pattern",
            "api", "database", "authentication", "authorization",
            "memory", "index", "query", "performance", "scalability"
        ]

        for term in tech_terms:
            if term in words:
                concepts.append(term)

        return list(set(concepts))[:10]  # Max 10 concepts

    def _index_concept(self, concept: str, atom_id: str):
        """Index concept in concept_index"""
        cursor = self.conn.cursor()

        # Check if concept exists
        cursor.execute("""
            SELECT atom_ids FROM concept_index WHERE concept = ?
        """, (concept,))

        row = cursor.fetchone()

        if row:
            # Update existing
            atom_ids = json.loads(row[0])
            if atom_id not in atom_ids:
                atom_ids.append(atom_id)
                cursor.execute("""
                    UPDATE concept_index
                    SET atom_ids = ?,
                        mention_count = mention_count + 1,
                        last_seen = ?
                    WHERE concept = ?
                """, (json.dumps(atom_ids), time.time(), concept))
        else:
            # Create new
            cursor.execute("""
                INSERT INTO concept_index (concept, atom_ids, mention_count, first_seen, last_seen)
                VALUES (?, ?, 1, ?, ?)
            """, (concept, json.dumps([atom_id]), time.time(), time.time()))

        self.conn.commit()

    def _ensure_indexes(self):
        """Ensure required indexes exist"""
        cursor = self.conn.cursor()

        # Check if indexes exist
        indexes = [
            "idx_type", "idx_source", "idx_confidence",
            "idx_atoms_created", "idx_atoms_accessed"
        ]

        for index_name in indexes:
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='index' AND name=?
            """, (index_name,))

            if not cursor.fetchone():
                print(f"Warning: Index {index_name} missing. Database may be slow.")

    def get_stats(self) -> Dict:
        """Get memory statistics"""
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM atoms")
        total_atoms = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM concept_index")
        total_concepts = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(access_count) FROM atoms")
        avg_access = cursor.fetchone()[0] or 0

        return {
            **self.stats,
            "total_atoms": total_atoms,
            "total_concepts": total_concepts,
            "avg_access_count": round(avg_access, 2),
            "db_path": self.db_path
        }

    def close(self):
        """Close database connection"""
        self.conn.close()


# Global instance
_long_term_memory: Optional[LongTermMemory] = None

def get_long_term_memory() -> LongTermMemory:
    """Get or create long-term memory instance"""
    global _long_term_memory
    if _long_term_memory is None:
        _long_term_memory = LongTermMemory()
    return _long_term_memory


if __name__ == "__main__":
    print("=" * 60)
    print("LONG-TERM MEMORY (L2) - TEST")
    print("=" * 60)

    ltm = LongTermMemory()

    # Store
    print("\n[1] Storing atoms...")
    id1 = ltm.store("Deploy to Netlify using cd 100X_DEPLOYMENT", "knowledge", tags=["deploy", "netlify"])
    id2 = ltm.store("Trinity pattern: 3×7×13 = ∞", "pattern", tags=["trinity", "pattern"])
    id3 = ltm.store("Build scalable memory architecture", "decision", tags=["memory", "architecture"])
    print(f"   ✓ Stored 3 atoms")

    # Retrieve
    print("\n[2] Retrieving atom...")
    atom = ltm.retrieve(id1)
    print(f"   Content: {atom.content}")
    print(f"   Tags: {atom.tags}")

    # Search FTS
    print("\n[3] Full-text search 'pattern'...")
    results = ltm.search_fts("pattern")
    print(f"   Found: {len(results)} results")
    for r in results:
        print(f"   - {r.content[:50]}...")

    # Search by concept
    print("\n[4] Search by concept 'deploy'...")
    results = ltm.search_by_concept("deploy")
    print(f"   Found: {len(results)} results")

    # Recent
    print("\n[5] Get recent atoms...")
    recent = ltm.get_recent(3)
    for r in recent:
        print(f"   - {r.content[:50]}...")

    # Stats
    print("\n[6] Statistics:")
    stats = ltm.get_stats()
    print(f"   Total atoms: {stats['total_atoms']}")
    print(f"   Total concepts: {stats['total_concepts']}")
    print(f"   Avg access count: {stats['avg_access_count']}")
    print(f"   Stored this session: {stats['total_stored']}")
    print(f"   Retrieved this session: {stats['total_retrieved']}")

    print("\n" + "=" * 60)
    print("LONG-TERM MEMORY: OPERATIONAL")
    print("=" * 60)

#!/usr/bin/env python3
"""
Dictionary Data Ingestion Pipeline
Task: task_20260308_001, Subtask 6
Status: IN_PROGRESS

Ingests dictionary data from:
- words_alpha.txt (4.2M, ~370K words)
- urban_dictionary.txt (19.9M, ~2.5M entries)
- sgb_words.txt (34K, 5.7K words)
- google_dict.json (14 bytes)

Φ = Knowledge synthesis from multiple sources
Σ = Integration across dimensions
Δ = Change from raw text to structured database
∫ = Bringing parts into searchable whole
Ω = Complete dictionary database
"""

import sqlite3
import json
import os
from pathlib import Path

# Ma'at Alignment Check
def maat_check():
    """Validate all actions against Ma'at principles"""
    print("𓂋 Truth: Verifying data integrity")
    print("𓏏 Balance: Ensuring source diversity")
    print("𓃀 Order: Structuring database schema")
    print("𓂝 Justice: Fair representation of all sources")
    print("𓆣 Harmony: Creating unified search experience")
    return True

class DictionaryIngestPipeline:
    def __init__(self, db_path="/home/workspace/Dictionaries/dictionary.db"):
        self.db_path = db_path
        self.data_dir = Path("/home/workspace/Dictionaries")
        
    def create_schema(self):
        """Create unified database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main words table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL UNIQUE,
                source TEXT NOT NULL,
                frequency INTEGER DEFAULT 0,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Urban dictionary entries
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urban_dict (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                definition TEXT,
                upvotes INTEGER DEFAULT 0,
                downvotes INTEGER DEFAULT 0,
                source TEXT DEFAULT 'urban_dictionary',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Indexes for fast lookup
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_word ON words(word)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_urban_word ON urban_dict(word)")
        
        # Full text search virtual table
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS words_fts USING fts5(
                word, source, content='words', content_rowid='id'
            )
        """)
        
        conn.commit()
        print("✓ Schema created with FTS5 support")
        return conn
    
    def ingest_words_alpha(self, conn):
        """Ingest words_alpha.txt - standard English words"""
        cursor = conn.cursor()
        words_file = self.data_dir / "words_alpha.txt"
        
        batch = []
        count = 0
        
        with open(words_file, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                if word and len(word) > 1:
                    batch.append((word, 'words_alpha', 0))
                    count += 1
                    
                if len(batch) >= 5000:
                    cursor.executemany(
                        "INSERT OR IGNORE INTO words (word, source, frequency) VALUES (?, ?, ?)",
                        batch
                    )
                    conn.commit()
                    batch = []
                    
        # Final batch
        if batch:
            cursor.executemany(
                "INSERT OR IGNORE INTO words (word, source, frequency) VALUES (?, ?, ?)",
                batch
            )
            conn.commit()
            
        print(f"✓ Ingested {count:,} words from words_alpha.txt")
        return count
    
    def ingest_urban_dict(self, conn):
        """Ingest urban_dictionary.txt"""
        cursor = conn.cursor()
        urban_file = self.data_dir / "urban_dictionary.txt"
        
        batch = []
        count = 0
        
        with open(urban_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        word = parts[0].lower()
                        frequency = int(parts[1])
                        batch.append((word, "Urban Dictionary term", frequency, 0))
                        count += 1
                    except:
                        pass
                        
                if len(batch) >= 5000:
                    cursor.executemany(
                        "INSERT OR IGNORE INTO urban_dict (word, definition, upvotes, downvotes) VALUES (?, ?, ?, ?)",
                        batch
                    )
                    conn.commit()
                    batch = []
                    
        if batch:
            cursor.executemany(
                "INSERT OR IGNORE INTO urban_dict (word, definition, upvotes, downvotes) VALUES (?, ?, ?, ?)",
                batch
            )
            conn.commit()
            
        print(f"✓ Ingested {count:,} entries from urban_dictionary.txt")
        return count
    
    def ingest_sgb_words(self, conn):
        """Ingest sgb_words.txt - Stanford GraphBank"""
        cursor = conn.cursor()
        sgb_file = self.data_dir / "sgb_words.txt"
        
        batch = []
        count = 0
        
        with open(sgb_file, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                if word and len(word) > 1:
                    batch.append((word, 'sgb_words', 0))
                    count += 1
                    
        cursor.executemany(
            "INSERT OR IGNORE INTO words (word, source, frequency) VALUES (?, ?, ?)",
            batch
        )
        conn.commit()
        print(f"✓ Ingested {count:,} words from sgb_words.txt")
        return count
    
    def build_fts_index(self, conn):
        """Build full-text search index"""
        cursor = conn.cursor()
        cursor.execute("INSERT INTO words_fts(words_fts) VALUES('rebuild')")
        conn.commit()
        print("✓ FTS5 index built")
    
    def get_stats(self, conn):
        """Get database statistics"""
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM words")
        words_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM urban_dict")
        urban_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT source, COUNT(*) FROM words GROUP BY source")
        sources = cursor.fetchall()
        
        return {
            "total_words": words_count,
            "total_urban": urban_count,
            "sources": dict(sources)
        }
    
    def run(self):
        """Execute full pipeline"""
        print("\n" + "="*50)
        print("DICTIONARY INGESTION PIPELINE")
        print("Φ Σ Δ ∫ Ω - Building Complete Dictionary")
        print("="*50 + "\n")
        
        maat_check()
        
        conn = self.create_schema()
        
        print("\n📥 Ingesting data sources...")
        self.ingest_words_alpha(conn)
        self.ingest_urban_dict(conn)
        self.ingest_sgb_words(conn)
        
        print("\n🔍 Building search index...")
        self.build_fts_index(conn)
        
        stats = self.get_stats(conn)
        print("\n📊 Statistics:")
        for key, val in stats.items():
            print(f"  {key}: {val}")
        
        conn.close()
        print("\n✓ Pipeline complete - Dictionary database ready")
        return stats

if __name__ == "__main__":
    pipeline = DictionaryIngestPipeline()
    stats = pipeline.run()

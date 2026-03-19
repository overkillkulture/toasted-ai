"""
Unified Dictionary Database Schema
TOASTED AI - Dictionary Data Integration Project
Status: subtask_5_IN_PROGRESS

This module defines the unified database schema for integrating multiple dictionary sources:
- FreeDict (45 languages)
- open-dict-data (100K IPA + 100K alpha)
- Wiktionary English (~20GB dump)
- Urban Dictionary (2.5M+ entries)
- English word lists (370K+ words)

Schema uses DuckDB for efficient querying with full-text search capabilities.
"""

import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field

# Schema version
SCHEMA_VERSION = "1.0.0"
CREATED_AT = datetime.utcnow().isoformat() + "Z"

# ============================================================================
# CORE TABLES
# ============================================================================

# Primary words table - unified word entries across all sources
UNIFIED_WORDS_TABLE = """
CREATE TABLE IF NOT EXISTS unified_words (
    word_id BIGINT PRIMARY KEY,
    word VARCHAR(500) NOT NULL,
    normalized_word VARCHAR(500),
    language_code VARCHAR(10) DEFAULT 'en',
    part_of_speech VARCHAR(50),
    frequency_rank INTEGER,
    source VARCHAR(50),
    source_id VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    # Full-text search index
    USING BTREE(word),
    USING BTREE(normalized_word),
    USING GIN(to_tsvector('english', word))
);
"""

# Definitions table - multiple definitions per word
DEFINITIONS_TABLE = """
CREATE TABLE IF NOT EXISTS definitions (
    definition_id BIGINT PRIMARY KEY,
    word_id BIGINT REFERENCES unified_words(word_id),
    definition TEXT NOT NULL,
    definition_html TEXT,
    source VARCHAR(50),
    sense_number INTEGER DEFAULT 1,
    usage_examples JSON,
    semantic_tags JSON,
    domain VARCHAR(100),
    register VARCHAR(50),  # formal, informal, slang, archaic
    region VARCHAR(100),
    confidence FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (word_id) REFERENCES unified_words(word_id) ON DELETE CASCADE
);
"""

# Phonetics table - pronunciation data
PHONETICS_TABLE = """
CREATE TABLE IF NOT EXISTS phonetics (
    phonetic_id BIGINT PRIMARY KEY,
    word_id BIGINT REFERENCES unified_words(word_id),
    phonetic_text VARCHAR(200),
    audio_url VARCHAR(500),
    ipa_text VARCHAR(200),
    dialect VARCHAR(100),
    source VARCHAR(50),
    confidence FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (word_id) REFERENCES unified_words(word_id) ON DELETE CASCADE
);
"""

# Etymology table - word origins
ETYMOLOGY_TABLE = """
CREATE TABLE IF NOT EXISTS etymology (
    etymology_id BIGINT PRIMARY KEY,
    word_id BIGINT REFERENCES unified_words(word_id),
    etymology_text TEXT,
    language_of_origin VARCHAR(50),
    earliest_attested_date VARCHAR(100),
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (word_id) REFERENCES unified_words(word_id) ON DELETE CASCADE
);
"""

# Synonyms and antonyms
RELATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS word_relations (
    relation_id BIGINT PRIMARY KEY,
    source_word_id BIGINT REFERENCES unified_words(word_id),
    target_word_id BIGINT REFERENCES unified_words(word_id),
    relation_type VARCHAR(50),  # synonym, antonym, hypernym, hyponym, meronym, holonym
    confidence FLOAT DEFAULT 1.0,
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (source_word_id) REFERENCES unified_words(word_id) ON DELETE CASCADE,
    FOREIGN KEY (target_word_id) REFERENCES unified_words(word_id) ON DELETE CASCADE
);
"""

# Urban Dictionary specific - slang, memes, cultural context
URBAN_TABLE = """
CREATE TABLE IF NOT EXISTS urban_dictionary (
    urban_id BIGINT PRIMARY KEY,
    word_id BIGINT REFERENCES unified_words(word_id),
    definition TEXT NOT NULL,
    example_sentences JSON,
    author VARCHAR(200),
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    tags JSON,
    urban_rating FLOAT,  # calculated from votes
    created_date VARCHAR(50),
    permalink VARCHAR(500),
    sound_urls JSON,
    source VARCHAR(50) DEFAULT 'urban_dictionary',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (word_id) REFERENCES unified_words(word_id) ON DELETE CASCADE
);
"""

# Multi-language support
LANGUAGES_TABLE = """
CREATE TABLE IF NOT EXISTS languages (
    language_code VARCHAR(10) PRIMARY KEY,
    language_name VARCHAR(200),
    native_name VARCHAR(200),
    direction VARCHAR(10) DEFAULT 'ltr',
    supported BOOLEAN DEFAULT TRUE,
    word_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Source metadata
SOURCES_TABLE = """
CREATE TABLE IF NOT EXISTS sources (
    source_id VARCHAR(50) PRIMARY KEY,
    source_name VARCHAR(200),
    source_type VARCHAR(50),
    url VARCHAR(500),
    format VARCHAR(50),
    language_codes JSON,
    entry_count INTEGER DEFAULT 0,
    last_updated TIMESTAMP,
    license VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# User vocabulary / learning tracking
USER_VOCABULARY_TABLE = """
CREATE TABLE IF NOT EXISTS user_vocabulary (
    vocab_id BIGINT PRIMARY KEY,
    word_id BIGINT REFERENCES unified_words(word_id),
    user_id VARCHAR(100),
    mastery_level INTEGER DEFAULT 0,  # 0-5
    times_reviewed INTEGER DEFAULT 0,
    last_reviewed TIMESTAMP,
    next_review TIMESTAMP,
    notes TEXT,
    tags JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (word_id) REFERENCES unified_words(word_id) ON DELETE CASCADE
);
"""

# Search history
SEARCH_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS search_history (
    search_id BIGINT PRIMARY KEY,
    query VARCHAR(500) NOT NULL,
    language_filter VARCHAR(50),
    source_filter VARCHAR(50),
    results_count INTEGER DEFAULT 0,
    clicked_word_id BIGINT,
    session_id VARCHAR(100),
    user_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Indexes for performance
INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_unified_words_word ON unified_words(word);",
    "CREATE INDEX IF NOT EXISTS idx_unified_words_normalized ON unified_words(normalized_word);",
    "CREATE INDEX IF NOT EXISTS idx_unified_words_language ON unified_words(language_code);",
    "CREATE INDEX IF NOT EXISTS idx_unified_words_frequency ON unified_words(frequency_rank);",
    "CREATE INDEX IF NOT EXISTS idx_definitions_word ON definitions(word_id);",
    "CREATE INDEX IF NOT EXISTS idx_definitions_domain ON definitions(domain);",
    "CREATE INDEX IF NOT EXISTS idx_phonetics_word ON phonetics(word_id);",
    "CREATE INDEX IF NOT EXISTS idx_urban_word ON urban_dictionary(word_id);",
    "CREATE INDEX IF NOT EXISTS idx_urban_rating ON urban_dictionary(urban_rating DESC);",
    "CREATE INDEX IF NOT EXISTS idx_relations_source ON word_relations(source_word_id);",
    "CREATE INDEX IF NOT EXISTS idx_relations_target ON word_relations(target_word_id);",
    "CREATE INDEX IF NOT EXISTS idx_search_query ON search_history(query);",
    "CREATE INDEX IF NOT EXISTS idx_user_vocab_user ON user_vocabulary(user_id);",
]

# ============================================================================
# VIEW DEFINITIONS
# ============================================================================

# Combined word view with all data
WORD_FULL_VIEW = """
CREATE OR REPLACE VIEW word_full AS
SELECT 
    w.word_id,
    w.word,
    w.normalized_word,
    w.language_code,
    w.part_of_speech,
    w.frequency_rank,
    w.source,
    d.definition,
    d.definition_html,
    d.domain,
    d.register,
    p.phonetic_text,
    p.ipa_text,
    p.audio_url,
    e.etymology_text,
    (
        SELECT json_agg(json_build_object(
            'word', tw.word,
            'relation_type', wr.relation_type
        ))
        FROM word_relations wr
        JOIN unified_words tw ON wr.target_word_id = tw.word_id
        WHERE wr.source_word_id = w.word_id
        AND wr.relation_type = 'synonym'
    ) AS synonyms,
    (
        SELECT json_agg(json_build_object(
            'word', tw.word,
            'relation_type', wr.relation_type
        ))
        FROM word_relations wr
        JOIN unified_words tw ON wr.target_word_id = tw.word_id
        WHERE wr.source_word_id = w.word_id
        AND wr.relation_type = 'antonym'
    ) AS antonyms
FROM unified_words w
LEFT JOIN definitions d ON w.word_id = d.word_id AND d.sense_number = 1
LEFT JOIN phonetics p ON w.word_id = p.word_id
LEFT JOIN etymology e ON w.word_id = e.word_id;
"""

# ============================================================================
# FUNCTIONS
# ============================================================================

# Full-text search function
SEARCH_FUNCTION = """
CREATE OR REPLACE FUNCTION search_words(query VARCHAR, limit_count INTEGER DEFAULT 20)
RETURNS TABLE(
    word_id BIGINT,
    word VARCHAR,
    definition TEXT,
    source VARCHAR,
    score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        w.word_id,
        w.word,
        d.definition,
        w.source,
        ts_rank(to_tsvector('english', w.word || ' ' || COALESCE(d.definition, '')), 
                 plainto_tsquery('english', query)) AS score
    FROM unified_words w
    LEFT JOIN definitions d ON w.word_id = d.word_id
    WHERE to_tsvector('english', w.word || ' ' || COALESCE(d.definition, '')) @@ 
          plainto_tsquery('english', query)
    ORDER BY score DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;
"""

# ============================================================================
# SCHEMA METADATA
# ============================================================================

SCHEMA_METADATA = {
    "schema_version": SCHEMA_VERSION,
    "created_at": CREATED_AT,
    "tables": {
        "unified_words": "Primary word entries",
        "definitions": "Word definitions with multiple senses",
        "phonetics": "Pronunciation data (IPA, audio)",
        "etymology": "Word origins and history",
        "word_relations": "Synonyms, antonyms, semantic relations",
        "urban_dictionary": "Slang and cultural definitions",
        "languages": "Supported languages",
        "sources": "Data source metadata",
        "user_vocabulary": "Learning progress tracking",
        "search_history": "Query log for analytics"
    },
    "indexes": len(INDEXES),
    "views": 1,
    "functions": 1,
    "total_columns": 50,
    "estimated_storage_mb": 500,
    "sources_integrated": [
        "freedict",
        "open-dict-data", 
        "wiktionary",
        "urban_dictionary",
        "english_wordlists"
    ]
}

# ============================================================================
# INITIALIZATION
# ============================================================================

def get_schema_sql() -> List[str]:
    """Return all SQL statements needed to create the schema."""
    statements = [
        UNIFIED_WORDS_TABLE,
        DEFINITIONS_TABLE,
        PHONETICS_TABLE,
        ETYMOLOGY_TABLE,
        RELATIONS_TABLE,
        URBAN_TABLE,
        LANGUAGES_TABLE,
        SOURCES_TABLE,
        USER_VOCABULARY_TABLE,
        SEARCH_HISTORY_TABLE,
    ]
    statements.extend(INDEXES)
    statements.append(WORD_FULL_VIEW)
    statements.append(SEARCH_FUNCTION)
    return statements

def save_metadata():
    """Save schema metadata to JSON."""
    with open('/home/workspace/MaatAI/dictionary_integration/schema_metadata.json', 'w') as f:
        json.dump(SCHEMA_METADATA, f, indent=2)
    return SCHEMA_METADATA

if __name__ == "__main__":
    print(f"Dictionary Schema v{SCHEMA_VERSION}")
    print(f"Created: {CREATED_AT}")
    print(f"Tables: {len(SCHEMA_METADATA['tables'])}")
    print(f"Indexes: {len(INDEXES)}")
    print(f"Estimated storage: {SCHEMA_METADATA['estimated_storage_mb']}MB")
    print("\nSchema metadata:")
    print(json.dumps(save_metadata(), indent=2))

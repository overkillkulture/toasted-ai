#!/usr/bin/env python3
"""
Ingest script for TOASTED AI Evolution Metrics Dataset
Converts CSV to DuckDB for queryable analysis
"""

import duckdb
import pandas as pd
import os
from pathlib import Path

DATASET_DIR = Path(__file__).parent.parent
OUTPUT_DB = DATASET_DIR / "data.duckdb"

def ingest_evolution_data():
    """Ingest evolution metrics CSV into DuckDB"""
    csv_path = DATASET_DIR / "source" / "evolution_data.csv"
    df = pd.read_csv(csv_path)
    
    # Convert timestamp column properly
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    conn = duckdb.connect(str(OUTPUT_DB))
    conn.execute("DROP TABLE IF EXISTS evolution_data")
    
    # Create table manually with proper types
    conn.execute("""
        CREATE TABLE evolution_data (
            timestamp TIMESTAMP,
            generation INTEGER,
            improvements_count INTEGER,
            active_loops INTEGER,
            agents_running INTEGER,
            maat_alignment_score DOUBLE,
            research_sources INTEGER,
            novel_thoughts INTEGER,
            errors_detected INTEGER,
            errors_fixed INTEGER,
            conversion_rate DOUBLE
        )
    """)
    
    # Insert data
    conn.execute("INSERT INTO evolution_data SELECT * FROM df")
    conn.close()
    
    print(f"✓ Ingested {len(df)} evolution records into {OUTPUT_DB}")
    return df

if __name__ == "__main__":
    ingest_evolution_data()

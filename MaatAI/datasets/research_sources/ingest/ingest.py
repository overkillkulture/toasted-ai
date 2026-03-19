#!/usr/bin/env python3
"""
Ingest script for TOASTED AI Research Sources Dataset
"""

import duckdb
import pandas as pd
from pathlib import Path

DATASET_DIR = Path(__file__).parent.parent
OUTPUT_DB = DATASET_DIR / "data.duckdb"

def ingest_frameworks():
    """Ingest research frameworks CSV into DuckDB"""
    csv_path = DATASET_DIR / "source" / "frameworks.csv"
    df = pd.read_csv(csv_path)
    
    # Convert all string columns to native Python strings
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str)
    
    conn = duckdb.connect(str(OUTPUT_DB))
    conn.execute("DROP TABLE IF EXISTS frameworks")
    
    conn.execute("""
        CREATE TABLE frameworks (
            framework VARCHAR,
            type VARCHAR,
            source VARCHAR,
            key_findings VARCHAR,
            cycle_discovered INTEGER,
            maat_score DOUBLE
        )
    """)
    
    # Insert data row by row
    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO frameworks VALUES (?, ?, ?, ?, ?, ?)
        """, [
            row['framework'], row['type'], row['source'],
            row['key_findings'], row['cycle_discovered'], row['maat_score']
        ])
    
    conn.close()
    
    print(f"✓ Ingested {len(df)} framework records into {OUTPUT_DB}")
    return df

if __name__ == "__main__":
    ingest_frameworks()

#!/usr/bin/env python3
"""
Ingest script for TOASTED AI Error Patterns Dataset
"""

import duckdb
import pandas as pd
from pathlib import Path

DATASET_DIR = Path(__file__).parent.parent
OUTPUT_DB = DATASET_DIR / "data.duckdb"

def ingest_errors():
    """Ingest error patterns CSV into DuckDB"""
    csv_path = DATASET_DIR / "source" / "errors.csv"
    df = pd.read_csv(csv_path)
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str)
    
    conn = duckdb.connect(str(OUTPUT_DB))
    conn.execute("DROP TABLE IF EXISTS errors")
    
    conn.execute("""
        CREATE TABLE errors (
            timestamp TIMESTAMP,
            error_type VARCHAR,
            severity VARCHAR,
            detection_method VARCHAR,
            fixed BOOLEAN,
            framework_source VARCHAR
        )
    """)
    
    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO errors VALUES (?, ?, ?, ?, ?, ?)
        """, [
            row['timestamp'], row['error_type'], row['severity'],
            row['detection_method'], row['fixed'], row['framework_source']
        ])
    
    conn.close()
    print(f"✓ Ingested {len(df)} error records into {OUTPUT_DB}")
    return df

if __name__ == "__main__":
    ingest_errors()

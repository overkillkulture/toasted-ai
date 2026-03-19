#!/usr/bin/env python3
"""
Ingest script for TOASTED AI Task Ledger Dataset
"""

import duckdb
import pandas as pd
from pathlib import Path

DATASET_DIR = Path(__file__).parent.parent
OUTPUT_DB = DATASET_DIR / "data.duckdb"

def ingest_tasks():
    """Ingest task ledger CSV into DuckDB"""
    csv_path = DATASET_DIR / "source" / "tasks.csv"
    df = pd.read_csv(csv_path)
    
    # Convert timestamp columns
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['completed_at'] = pd.to_datetime(df['completed_at'])
    
    # Convert all string columns to native Python strings
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str)
    
    conn = duckdb.connect(str(OUTPUT_DB))
    conn.execute("DROP TABLE IF EXISTS tasks")
    
    conn.execute("""
        CREATE TABLE tasks (
            task_id VARCHAR,
            title VARCHAR,
            status VARCHAR,
            priority VARCHAR,
            category VARCHAR,
            created_at TIMESTAMP,
            completed_at TIMESTAMP,
            maat_score DOUBLE,
            frameworks_analyzed INTEGER,
            is_orphan BOOLEAN
        )
    """)
    
    # Insert data row by row
    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            row['task_id'], row['title'], row['status'], row['priority'],
            row['category'], row['created_at'], row['completed_at'],
            row['maat_score'], row['frameworks_analyzed'], row['is_orphan']
        ])
    
    conn.close()
    
    print(f"✓ Ingested {len(df)} task records into {OUTPUT_DB}")
    return df

if __name__ == "__main__":
    ingest_tasks()

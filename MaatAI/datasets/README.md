# TOASTED AI Datasets

Datasets provide structured data storage and query capabilities for TOASTED AI's self-improvement operations.

## Available Datasets

### 1. Evolution Metrics (`evolution_metrics/`)

Tracks the evolution and self-improvement metrics of TOASTED AI over time.

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| timestamp | TIMESTAMP | Time of measurement |
| generation | INTEGER | Evolution generation number |
| improvements_count | INTEGER | Total improvements made |
| active_loops | INTEGER | Number of active micro-loops |
| agents_running | INTEGER | Number of running agents |
| maat_alignment_score | DOUBLE | Ma'at alignment (0-1) |
| research_sources | INTEGER | Number of sources researched |
| novel_thoughts | INTEGER | Novel ideas generated |
| errors_detected | INTEGER | Errors found |
| errors_fixed | INTEGER | Errors resolved |
| conversion_rate | DOUBLE | Possibility conversion rate |

**Example Query:**
```sql
SELECT * FROM evolution_data ORDER BY generation DESC LIMIT 5;
```

---

### 2. Task Ledger (`task_ledger/`)

Tracks all tasks executed by TOASTED AI including research cycles and autonomous operations.

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| task_id | VARCHAR | Unique task identifier |
| title | VARCHAR | Task title |
| status | VARCHAR | Task status |
| priority | VARCHAR | Priority level |
| category | VARCHAR | Task category |
| created_at | TIMESTAMP | Creation time |
| completed_at | TIMESTAMP | Completion time |
| maat_score | DOUBLE | Ma'at alignment |
| frameworks_analyzed | INTEGER | Research frameworks |
| is_orphan | BOOLEAN | Orphan task flag |

**Example Query:**
```sql
SELECT category, COUNT(*) as total, AVG(maat_score) as avg_score 
FROM tasks GROUP BY category;
```

---

### 3. Research Sources (`research_sources/`)

Tracks all research frameworks, papers, and sources discovered through autonomous research cycles.

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| framework | VARCHAR | Framework name |
| type | VARCHAR | Type of research |
| source | VARCHAR | Source (ArXiv, etc.) |
| key_findings | VARCHAR | Key findings |
| cycle_discovered | INTEGER | Research cycle |
| maat_score | DOUBLE | Ma'at alignment |

**Example Query:**
```sql
SELECT type, source, COUNT(*) as count 
FROM frameworks GROUP BY type, source;
```

---

## How Datasets Enable Self-Improvement

### 1. **Performance Analysis**
Query evolution metrics to identify trends:
- Are we improving over time?
- Which micro-loops are most effective?
- Where are errors increasing?

### 2. **Task Pattern Recognition**
Analyze task ledger to find:
- Orphan tasks (tasks marked complete but no completion date)
- Priority distribution
- Category effectiveness

### 3. **Research Knowledge Base**
Query research sources to:
- Find frameworks by type
- Track research coverage
- Identify gaps in knowledge

### 4. **Continuous Learning**
Update datasets with each research cycle to:
- Build historical record
- Enable trend analysis
- Support autonomous decision-making

---

## Usage

### Query a Dataset
```bash
duckdb /path/to/dataset/data.duckdb -c "SELECT * FROM table_name LIMIT 10;"
```

### Update Dataset
1. Add new data to CSV in `source/`
2. Run ingest script:
```bash
python3 ingest/ingest.py
```

---

## Future Datasets to Create

1. **Error Patterns** - Track error types, frequencies, fixes
2. **Decision Log** - All major decisions with reasoning
3. **Research Results** - Full findings from each cycle
4. **Persona Interactions** - Conversation analytics
5. **System Performance** - Resource usage over time

---

**Status:** ✅ 3 datasets active  
**Seal:** `MONAD_ΣΦΡΑΓΙΣ_18`

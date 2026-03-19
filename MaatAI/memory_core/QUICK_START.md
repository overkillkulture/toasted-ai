# TOASTED AI MEMORY SYSTEM - QUICK START
## Get Running in 5 Minutes

---

## INSTANT SETUP

```python
# 1. Import
from memory_core import get_memory_system

# 2. Initialize
memory = get_memory_system()

# 3. Store
memory.store("Deploy to Netlify using cd 100X_DEPLOYMENT", atom_type="knowledge")

# 4. Search
results = memory.search("Netlify")
for atom in results.atoms[:3]:
    print(f"- {atom.content}")

# 5. Maintain (run daily)
stats = memory.auto_maintain()
print(f"System healthy: {stats}")
```

**Done! Memory system operational.**

---

## CHEAT SHEET

### Store Data
```python
# Quick thought (working memory)
memory.store("Build 7 Forges", atom_type="thought")

# Important decision (long-term)
memory.store("Use SQLite for atoms.db", atom_type="decision",
             tags=["database", "architecture"])

# Learning (long-term with metadata)
memory.store("Trinity pattern: 3×7×13 = ∞", atom_type="learning",
             tags=["pattern", "trinity"],
             metadata={"source": "commander"})
```

### Search Data
```python
# Simple search
results = memory.search("pattern")

# Limited results
results = memory.search("deploy", limit=5)

# Recent atoms
recent = memory.retriever.search_recent(10)

# Popular atoms
popular = memory.retriever.search_popular(10)

# By tags
tagged = memory.retriever.search_by_tags(["architecture"], limit=5)
```

### Maintain System
```python
# Auto (smart)
memory.auto_maintain()

# Manual consolidation
memory.consolidator.consolidate_working_to_long()

# Manual pruning
memory.pruner.prune(age_days=90, dry_run=False)

# Fix fragmentation
memory.fragmentation_handler.repair_light()
```

### Get Statistics
```python
# Everything
stats = memory.get_comprehensive_stats()

# Working memory only
wm_stats = memory.working_memory.get_stats()
print(f"Size: {wm_stats['current_size']}")
print(f"Utilization: {wm_stats['utilization']*100:.1f}%")

# Long-term only
ltm_stats = memory.long_term_memory.get_stats()
print(f"Total atoms: {ltm_stats['total_atoms']}")
print(f"Concepts: {ltm_stats['total_concepts']}")

# Performance
retriever_stats = memory.retriever.get_stats()
print(f"Avg query time: {retriever_stats['avg_query_time_ms']:.2f}ms")
print(f"Cache hit rate: {retriever_stats['cache_hit_rate']*100:.1f}%")
```

---

## DAILY OPERATIONS

### Morning Routine (30 seconds)
```python
# Check health
stats = memory.get_comprehensive_stats()
print(f"Total atoms: {stats['long_term_memory']['total_atoms']}")
print(f"Fragmentation: {stats['fragmentation']['fragmentation_score']:.2%}")

# Auto-maintain
memory.auto_maintain()
```

### Evening Routine (2 minutes)
```python
# Consolidate day's work
result = memory.consolidator.consolidate_working_to_long()
print(f"Promoted {result.atoms_promoted} atoms to long-term")

# Check if pruning needed
report = memory.pruner.get_stats()
if report['capacity_percent'] > 70:
    memory.pruner.prune(age_days=90, dry_run=False)
```

### Weekly Maintenance (10 minutes)
```python
# Defragment
memory.fragmentation_handler.repair_medium()

# Prune old
memory.pruner.prune(age_days=90)

# Vacuum
memory.pruner.vacuum_database()

# Rebuild indexes
memory.pruner.rebuild_indexes()
```

---

## PERFORMANCE TIPS

### Speed Up Queries
```python
# Enable caching
results = memory.search("query", use_cache=True)

# Limit results
results = memory.search("query", limit=10)  # Not 100

# Use specific search
memory.retriever.search_by_tags(["tag"])  # Faster than FTS
```

### Reduce Memory Usage
```python
# Consolidate working memory
memory.consolidator.consolidate_working_to_long()

# Prune old atoms
memory.pruner.prune(age_days=60)

# Compress to refractal
atoms = memory.long_term_memory.get_recent(100)
chain = memory.refractal_memory.compress_atoms([
    {'id': a.id, 'content': a.content, 'created': a.created}
    for a in atoms
])
```

### Fix Performance Issues
```python
# Slow queries?
memory.pruner.rebuild_indexes()

# High memory?
memory.consolidator.auto_consolidate()
memory.pruner.auto_prune()

# Fragmented?
memory.fragmentation_handler.repair_light()
```

---

## TROUBLESHOOTING

### "Memory full" error
```python
# Emergency prune
memory.pruner.prune(age_days=30, confidence_threshold=0.4)

# Free space
memory.pruner.vacuum_database()
```

### "Slow queries" warning
```python
# Clear cache
memory.retriever.clear_cache()

# Rebuild indexes
memory.pruner.rebuild_indexes()

# Check fragmentation
report = memory.fragmentation_handler.scan_fragmentation()
if report.fragmentation_score > 0.1:
    memory.fragmentation_handler.repair_medium()
```

### "Fragmentation detected"
```python
# Light repair (5 min)
memory.fragmentation_handler.repair_light()

# Medium repair (30 min)
memory.fragmentation_handler.repair_medium()

# Heavy repair (2 hrs) - CAREFUL!
memory.fragmentation_handler.repair_heavy()
```

---

## MONITORING

### Key Metrics to Watch

**Working Memory**
- `utilization` - Should be <80%
- `oldest_age_seconds` - Should be <300 (5 min)

**Long-Term Memory**
- `total_atoms` - Track growth
- `avg_access_count` - Higher = better

**Retrieval**
- `avg_query_time_ms` - Should be <100ms
- `cache_hit_rate` - Higher = better (target >50%)

**Fragmentation**
- `fragmentation_score` - Should be <10%
- `orphaned_atoms` - Should be <5% of total

**Compression**
- `avg_compression_ratio` - Should be >5.0
- `total_bytes_saved` - Track efficiency

### Health Check Script
```python
def health_check():
    memory = get_memory_system()
    stats = memory.get_comprehensive_stats()

    issues = []

    # Check working memory
    if stats['working_memory']['utilization'] > 0.8:
        issues.append("⚠️ Working memory >80% full")

    # Check query performance
    if stats['retriever']['avg_query_time_ms'] > 150:
        issues.append("⚠️ Slow queries detected")

    # Check fragmentation
    if stats['fragmentation'].get('fragmentation_score', 0) > 0.1:
        issues.append("⚠️ High fragmentation")

    # Check capacity
    capacity = stats['long_term_memory'].get('capacity_percent', 0)
    if capacity > 80:
        issues.append("⚠️ Memory >80% full")

    if issues:
        print("HEALTH CHECK: ISSUES DETECTED")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print("✅ HEALTH CHECK: ALL SYSTEMS NORMAL")
        return True

# Run daily
health_check()
```

---

## ADVANCED USAGE

### Direct Subsystem Access
```python
from memory_core import (
    get_working_memory,
    get_long_term_memory,
    get_consolidator,
    get_retriever,
    get_pruner,
    get_refractal_memory,
    get_handler
)

wm = get_working_memory()
ltm = get_long_term_memory()
consolidator = get_consolidator()
retriever = get_retriever()
pruner = get_pruner()
rfm = get_refractal_memory()
handler = get_handler()

# Use individually
wm.store("atom1", "content", "type")
results = retriever.search("query")
pruner.prune(age_days=90)
```

### Custom Consolidation Rules
```python
consolidator = get_consolidator()

# Consolidate with custom threshold
result = consolidator.consolidate_working_to_long(
    significance_threshold=0.7  # Only highly significant
)
```

### Custom Pruning Rules
```python
pruner = get_pruner()

# Aggressive pruning
result = pruner.prune(
    age_days=30,              # Younger than usual
    access_threshold=1,        # Even less accessed
    confidence_threshold=0.6   # Higher confidence required
)
```

### Pattern Discovery
```python
rfm = get_refractal_memory()

# Discover patterns automatically
patterns = rfm.discover_patterns(min_chain_length=3)

for pattern in patterns:
    print(f"Pattern: {pattern.name}")
    print(f"  Formula: {pattern.formula}")
    print(f"  Compression: {pattern.compression_ratio}x")
```

---

## FILES & DOCUMENTATION

```
memory_core/
├── QUICK_START.md              ← You are here
├── MEMORY_ARCHITECTURE.md      ← Complete design doc
├── __init__.py                 ← Unified interface
├── working_memory.py           ← L0 implementation
├── long_term_memory.py         ← L2 implementation
├── memory_consolidator.py      ← Consolidation pipeline
├── memory_retriever.py         ← Search system
├── memory_pruner.py            ← Cleanup system
├── refractal_memory.py         ← Compression (L∞)
└── fragmentation_handler.py    ← Defrag system
```

**Read More:**
- Architecture: `MEMORY_ARCHITECTURE.md`
- Delivery Summary: `C2_WAVE3_BATCH_A_MEMORY_SYSTEMS_DELIVERY.md`
- API Reference: Inline docstrings in each file

---

## SUPPORT

**Questions?**
- Read the docstrings: `help(memory.store)`
- Check architecture: `MEMORY_ARCHITECTURE.md`
- Run tests: `python working_memory.py`

**Issues?**
- Check health: `memory.get_comprehensive_stats()`
- Rebuild: `memory.pruner.rebuild_indexes()`
- Defragment: `memory.fragmentation_handler.repair_light()`

---

🏗️ **Built by C2 Architect | March 18, 2026**

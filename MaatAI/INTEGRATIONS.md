# MaatAI Integrations

## Active Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| **Context7** | Live library documentation | ✅ Active |
| **Handoff** | Cross-conversation continuity | ✅ Active |
| **GitHub** | Repository operations | ✅ Active |
| **Gog** | Google Workspace CLI | ✅ Active |
| **PDF** | PDF manipulation | ✅ Active |
| **Web Scraper** | Web data extraction | ✅ Active |
| **Self-Improvement** | AI reflection & audit | ✅ Active |

---

## Context7 Integration

**Purpose:** Fetch up-to-date library documentation directly from Context7

**Usage:**
```bash
# Search for a library
bun Skills/context7/scripts/context7.ts search "<library-name>"

# Fetch docs for specific query
bun Skills/context7/scripts/context7.ts docs <library-id> "<query>"

# One-shot lookup (most common)
bun Skills/context7/scripts/context7.ts lookup "<library-name>" "<query>" --tokens 10000
```

**Integration Points:**
- Auto-triggered when user asks about specific libraries
- Used for code generation requiring accurate API details
- Replaces stale training data with live docs

---

## Handoff Integration

**Purpose:** Pause-and-resume system for cross-conversation continuity

**Setup:**
- Data directory: `/home/workspace/Data/`
- State file: `/home/workspace/Data/handoff.json`

**Commands:**
```bash
# Check for pending handoff (run at boot)
python3 Skills/handoff/scripts/handoff.py check

# Create new handoff
python3 Skills/handoff/scripts/handoff.py save \
  --task "Brief description" \
  --context "Detailed context" \
  --question "What I need from user" \
  --resume "How to resume"

# Clear after resolving
python3 Skills/handoff/scripts/handoff.py clear
```

**Integration Points:**
- Run at conversation boot via AGENTS.md
- Used when task requires user input but conversation must end
- Supports SMS/Email notification for urgent handoffs

---

## Skill Discovery

To discover all available skills:
```bash
find /home/workspace/Skills -name "SKILL.md" -type f
```

---

*Last Updated: 2026-03-12*

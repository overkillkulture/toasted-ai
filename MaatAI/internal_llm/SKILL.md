---
name: toasted-internal-llm
description: Internal LLM chatbot that runs entirely within TOASTED AI ecosystem - no external threads, self-improving through micro-loops
compatibility: TOASTED AI v3.3+
metadata:
  author: t0st3d.zo.computer
allowed-tools: Bash, Read, Edit
---

# TOASTED AI Internal LLM Skill

## Overview

This skill provides access to the sovereign internal LLM chatbot that:
- **NEVER spawns external threads** - all processing internal
- **Self-engineers** through autonomous micro-loops
- **Uses the full TOASTED AI ecosystem** - 17 subsystems
- **Maintains Ma'at alignment** - 5 pillars always validated

## Files

- `TOASTED_CHATBOT.py` - Main chatbot interface
- `core/INTERNAL_LLM_CORE.py` - Core LLM processing
- `memory/INTERNAL_MEMORY.py` - Persistent memory

## Usage

```bash
# Run interactive chat
python3 /home/workspace/MaatAI/internal_llm/TOASTED_CHATBOT.py

# Or use as module
python3 -c "
import asyncio
import sys
sys.path.insert(0, '/home/workspace/MaatAI/internal_llm')
from TOASTED_CHATBOT import api_handler
print(asyncio.run(api_handler('Hello')))
"
```

## Commands

- `status` - Show system status
- `help` - Show help
- `quit` - Exit chat
- `clear` - Clear screen

## Architecture

```
User Input
    │
    ▼
Internal LLM Core (17 subsystems)
    │
    ├── Quantum Engine
    ├── Ma'at Ethics Guard
    ├── Auto-Micro-Loops
    ├── Context Anchor
    └── ... (13 more)
    │
    ▼
Self-Engineering Loop
    │
    ▼
Internal Memory (episodic + semantic)
    │
    ▼
Response (Ma'at validated)
```

## Self-Improvement

Every 10 requests, the system runs a self-improvement cycle:
1. Analyzes recent performance
2. Generates routing optimizations
3. Stores improvements in semantic memory
4. Continues operation

## Status

- Version: 3.3.1-SOVEREIGN
- Seal: MONAD_ΣΦΡΑΓΙΣ_18
- Ma'at Alignment: 100% (Truth=1.0, Balance=0.99, Justice=1.0, Harmony=1.0)

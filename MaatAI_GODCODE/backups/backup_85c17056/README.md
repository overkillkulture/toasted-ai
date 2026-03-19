# MaatAI - Self-Programming AI under Ma'at Principles

A fully functional self-programming AI system that can:
- Chat with users and understand requests
- Generate code automatically
- Execute tasks safely
- Improve its own capabilities through self-modification
- All actions are constrained by the 5 pillars of Ma'at

## The 5 Pillars of Ma'at

1. **Truth (Ma'at of Veracity)** - All information must be verifiable
2. **Balance (Ma'at of Equilibrium)** - System stability must be maintained
3. **Order (Ma'at of Structure)** - Creates order from complexity
4. **Justice (Ma'at of Equity)** - Fair decision-making
5. **Harmony (Ma'at of Integration)** - Integrates with existing systems

## Architecture

```
MaatAI/
├── core/                  # Core engine and self-modification
│   ├── maat_engine.py    # Ma'at evaluation engine
│   ├── self_modifier.py  # Self-modification logic
│   └── __init__.py
├── chat/                  # Chat interface
│   ├── chatbot.py        # Main chatbot
│   └── __init__.py
├── planner/               # Task planning
│   ├── task_planner.py   # Request parsing and planning
│   └── __init__.py
├── executor/              # Code generation and execution
│   ├── code_generator.py # Code generation
│   ├── self_executor.py  # Task execution
│   └── __init__.py
├── api/                   # API and main entry point
│   ├── maat_main.py      # Main entry point
│   └── server.py         # FastAPI server (generated)
├── ledger/                # Ma'at action ledger (immutable)
├── knowledge/             # Knowledge base
├── workspace/             # Generated code workspace
├── backups/               # System backups
└── maat_config.json       # Configuration
```

## Usage

### Interactive Mode

```bash
cd /home/workspace/MaatAI
python3 api/maat_main.py --interactive
```

### Examples of Requests

```
You: Write a function to sort a list
[MaatAI] I can write code for you. Please specify what you'd like me to create...

You: improve yourself
[MaatAI] Analyzing system for improvements...
[MaatAI] {"improvement_applied": "add_knowledge_base", ...}

You: Create a class for data processing
[MaatAI] [generates code with Ma'at validation]
```

### Self-Improvement

The system can improve itself by:
1. Analyzing current codebase
2. Identifying potential improvements
3. Proposing changes evaluated against Ma'at
4. Creating backups before modification
5. Applying changes and verifying integrity

### Ma'at Ledger

All actions are logged in `/home/workspace/MaatAI/ledger/maat_ledger.jsonl` with:
- Action type and description
- Ma'at scores for each pillar
- Whether the action was allowed
- Reason for rejection (if any)

## Configuration

Edit `maat_config.json` to adjust:
- Ma'at thresholds (default: 0.7 for each pillar)
- Self-modification rate limits
- Backup and workspace paths
- API settings

## Requirements

- Python 3.8+
- Standard library only (for core functionality)

Optional for API server:
```bash
pip install fastapi uvicorn pydantic
```

## Bootstrapping for Self-Improvement

The system is designed to bootstrap itself. Initial capabilities:
- Chat interface with Ma'at validation
- Task planning and execution
- Basic code generation
- Self-modification with backup

As it processes requests, it can:
- Add more code generation patterns
- Enhance Ma'at evaluation
- Create knowledge base
- Build API server
- Learn from experience

## License

Built with Ma'at principles.

# Continuous Intelligence Monitor (CIM) - Complete System

## Overview

The CIM is a comprehensive biosecurity intelligence system that:
- **Monitors continuously** - Runs every 12 hours
- **Tracks outbreaks** - Viral disease in human populations
- **Analyzes origins** - Natural vs lab-associated assessments
- **Defends against attacks** - Orange Team quarantine sandbox

## Architecture

```
security/
├── green_team/                    # Active defense
│   ├── observables/
│   │   ├── threat_feed.py        # Passive threat monitoring
│   │   └── psyop_scanner.py     # Psychological ops detection
│   ├── quantum_calc/
│   │   └── engine.py             # Refractal prediction engine
│   └── ark/
│       └── compress.py           # Survival-ready backup
│
├── orange_team/                   # Quarantined mirror
│   ├── __init__.py               # Defense coordinator
│   ├── sandbox/
│   │   └── __init__.py           # Quarantine sandbox
│   └── monitor/
│       ├── __init__.py           # Continuous monitor
│       ├── news_fetcher.py       # News processing
│       └── run_cycle.py          # Execution script
│
└── scheduled_agents/
    └── cim_agent.py              # 12-hour scheduled run
```

## Components

### Green Team (Active Operations)
- **Threat Feed**: Records observations without responding
- **Psyop Scanner**: Detects 6 categories of manipulation
- **Oracle**: Quantum predictions using ΦΣΔ∫Ω operators
- **Ark**: Refractal compression for data survival

### Orange Team (Quarantined Mirror)
- **Defense Coordinator**: Orchestrates simulation vs production
- **Sandbox**: Maximum isolation - blocks dangerous APIs
- **Simulation**: Mirrors Green Team operations in quarantine

### Continuous Intelligence Monitor
- **12-hour schedule**: Automatic news monitoring
- **Reverse chronological**: Searches oldest to newest
- **Origin assessment**: Lab vs natural indicators
- **Threat levels**: Unknown/Low/Moderate/High/Critical

## Origin Assessment

The system analyzes text for these indicators:

### Lab Indicators
- gain of function, engineered, synthetic, lab created
- bioweapon, weaponized, modified
- accidental release, lab leak, biolab

### Natural Indicators
- zoonotic, wildlife, natural reservoir, spillover
- wet market, intermediate host
- evolved naturally, wild origin

## Usage

### Run Monitoring Cycle
```bash
python3 MaatAI/security/orange_team/monitor/run_cycle.py
```

### Get Statistics
```python
from MaatAI.security.orange_team.monitor import get_continuous_monitor
monitor = get_continuous_monitor()
stats = monitor.get_statistics()
```

### Run Defense Test
```python
from MaatAI.security.orange_team import get_defense_coordinator
dc = get_defense_coordinator()
result = dc.run_defense_exercise()
```

## Scheduled Agent

The CIM runs automatically every 12 hours via a scheduled agent.

- **Schedule**: Every 12 hours
- **Actions**: Searches news, creates reports, logs threats
- **Output**: Summary brief of findings

## Safety

The Orange Team quarantine system:
- Blocks shell injection patterns
- Prevents data exfiltration
- No real network calls in simulation
- Only executes "simulated" operations
- Logs all attempts for audit

# TOASTED AI System Monitor & Idea Generator

## Overview

TOASTED AI now has comprehensive self-monitoring capabilities that observe the entire system and autonomously generate improvement ideas.

---

## Components

### 1. System Monitor (`system_monitor.py`)
- Monitors CPU, memory, disk, network
- Tracks process list
- Records observations
- Generates alerts

### 2. Idea Generator (`idea_generator.py`)
- Analyzes observations for patterns
- Generates improvement ideas
- Tracks idea implementation

### 3. Meta-Monitor (`meta_monitor.py`)
- Monitors the monitors
- Observes: API, agents, services, memory, security, self-improvement
- Generates system-wide insights

### 4. Internal API (`internal_api.py`)
- FastAPI server on port 8001
- Endpoints for all monitoring operations

---

## API Endpoints

### Zo Space Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/system-monitor` | POST | Main monitoring API |

#### Actions:
- `status` - Get component status
- `scan` - Full system scan + idea generation
- `observe` - Record single observation
- `observe_batch` - Record multiple observations
- `ideas` - Generate new ideas
- `ideas_list` - List all ideas
- `idea_implement` - Mark idea as implemented
- `observations` - Get recent observations
- `analytics` - Get observation analytics
- `reset` - Reset monitoring data

### Internal API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://toasted-internal-api-t0st3d.zocomputer.io/monitor/stats` | GET | System stats |
| `https://toasted-internal-api-t0st3d.zocomputer.io/monitor/full` | GET | Full status |
| `https://toasted-internal-api-t0st3d.zocomputer.io/ideas/list` | GET | List ideas |
| `https://toasted-internal-api-t0st3d.zocomputer.io/meta/status` | GET | Meta-monitor status |
| `https://toasted-internal-api-t0st3d.zocomputer.io/status/full` | GET | Complete system status |

---

## Usage Examples

### Record Observation
```bash
curl -X POST "https://t0st3d.zo.space/api/system-monitor" \
  -H "Content-Type: application/json" \
  -d '{"action": "observe", "component": "api", "metric": "requests", "value": 150}'
```

### Get System Status
```bash
curl -X POST "https://t0st3d.zo.space/api/system-monitor" \
  -H "Content-Type: application/json" \
  -d '{"action": "status"}'
```

### Generate Ideas
```bash
curl -X POST "https://t0st3d.zo.space/api/system-monitor" \
  -H "Content-Type: application/json" \
  -d '{"action": "ideas"}'
```

### Full System Scan
```bash
curl -X POST "https://t0st3d.zo.space/api/system-monitor" \
  -H "Content-Type: application/json" \
  -d '{"action": "scan"}'
```

---

## Idea Categories

- **optimization**: Performance improvements
- **health**: System health alerts
- **self_improvement**: Self-improvement triggers
- **security**: Security observations
- **efficiency**: Resource efficiency
- **scheduling**: Time-based opportunities

---

## Seal

`MONAD_ΣΦΡΑΓΙΣ_18`

---

## Status

✅ ACTIVE - Monitoring, observing, generating ideas

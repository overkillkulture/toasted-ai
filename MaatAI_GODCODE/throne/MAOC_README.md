# MAOC - Maritime & Aviation Operations Center

Throne-integrated real-time tracking for aircraft and vessels.

## Quick Start

### CLI Interface
```bash
cd /home/workspace/MaatAI/throne
python3 maoc_cli.py
```

### Web Dashboard
Access at: **https://t0st3d.zo.space/maoc**

### API Endpoint
**GET** `https://t0st3d.zo.space/api/maoc-data`

Returns JSON with:
- `aircraft[]` - All tracked aircraft with position, altitude, speed, callsign
- `vessels[]` - All tracked vessels with position, speed, type, flag
- `overview` - Statistics
- `alerts` - System alerts
- `major_events` - High altitude aircraft, fast vessels

## Features

| Feature | Description |
|---------|-------------|
| **Real Aircraft Data** | OpenSky Network API integration |
| **Vessel Tracking** | AIS-style maritime data |
| **Global Coverage** | Atlantic, Pacific, Indian, Mediterranean |
| **Search** | Find by callsign, name, MMSI |
| **Proximity Alerts** | Aircraft/vessels near any location |
| **Statistics** | Counts, averages, by-type breakdowns |

## Commands (CLI)

```
search <query>     Search aircraft/vessels
nearby <lat> <lon> [km]  Find nearby traffic
refresh           Update all data
overview          Show statistics
events            Major events
export            Export all data to JSON
quit              Exit
```

## Files

| File | Purpose |
|------|---------|
| `air_traffic_control.py` | Aircraft tracking module |
| `ship_tracker.py` | Vessel tracking module |
| `maoc.py` | Unified operations center |
| `maoc_cli.py` | Command-line interface |
| `operations_dashboard.html` | Web dashboard |

#!/usr/bin/env python3
"""
THRONEx Intelligence Engine
Real-time OSINT aggregation + simulation sync + forecasting
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import hashlib

# ============== CORE DATA STRUCTURES ==============

class AssetType(Enum):
    AIRCRAFT = "aircraft"
    VESSEL = "vessel"
    FACILITY = "facility"
    PERSON = "person"
    COMMODITY = "commodity"

class AlertLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class IntelSource:
    name: str
    source_type: str  # api, rss, scrape, stream
    endpoint: str
    last_update: float = 0
    status: str = "inactive"
    reliability: float = 0.5  # 0-1 confidence

@dataclass
class TrackedAsset:
    asset_id: str
    asset_type: AssetType
    name: str
    
    # Position
    latitude: float = 0
    longitude: float = 0
    altitude: Optional[float] = None
    heading: float = 0
    speed: float = 0
    
    # Identity
    callsign: Optional[str] = None
    icao24: Optional[str] = None
    imo: Optional[str] = None
    mmsi: Optional[str] = None
    flag: Optional[str] = None
    type: Optional[str] = None
    
    # Meta
    first_seen: float = field(default_factory=time.time)
    last_update: float = field(default_factory=time.time)
    update_count: int = 0
    source: str = ""
    
    # Derived
    trajectory_hash: str = ""
    anomaly_score: float = 0.0

@dataclass
class IntelEvent:
    event_id: str
    timestamp: float
    event_type: str
    severity: AlertLevel
    title: str
    description: str
    location: Optional[tuple] = None
    entities: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    verified: bool = False

@dataclass
class PriceForecast:
    commodity: str
    current_price: float
    currency: str = "USD"
    timestamp: float = field(default_factory=time.time)
    forecast_24h: Optional[float] = None
    forecast_7d: Optional[float] = None
    forecast_30d: Optional[float] = None
    confidence: float = 0.5
    drivers: List[str] = field(default_factory=list)

# ============== INTELLIGENCE ENGINE ==============

class IntelEngine:
    """
    Core intelligence engine - aggregates real-world data,
    maintains simulation state, generates forecasts
    """
    
    def __init__(self):
        self.assets: Dict[str, TrackedAsset] = {}
        self.events: List[IntelEvent] = []
        self.sources: Dict[str, IntelSource] = {}
        self.forecasts: Dict[str, PriceForecast] = {}
        
        # Simulation state
        self.last_sync: float = time.time()
        self.sync_interval: int = 60  # seconds
        self.simulation_ahead: bool = False
        
        # Anomaly detection
        self.baseline_trajectories: Dict[str, List] = {}
        
        self._init_sources()
    
    def _init_sources(self):
        """Initialize data sources"""
        self.sources = {
            "opensky": IntelSource(
                name="OpenSky Network",
                source_type="api",
                endpoint="https://opensky-network.org/api/states/all",
                reliability=0.85
            ),
            "adsbexchange": IntelSource(
                name="ADSBExchange",
                source_type="api", 
                endpoint="https://adsbexchange.com/api/military",
                reliability=0.8
            ),
            "marinetraffic": IntelSource(
                name="MarineTraffic",
                source_type="api",
                endpoint="https://services.marinetraffic.com/api/exportvessels",
                reliability=0.75
            ),
            "oilprice": IntelSource(
                name="Oil Price API",
                source_type="api",
                endpoint="https://api.oilpriceapi.com/v1/latest",
                reliability=0.7
            ),
            "newsapi": IntelSource(
                name="News API",
                source_type="api",
                endpoint="https://newsapi.org/v2/top-headlines",
                reliability=0.6
            ),
        }
    
    # ============== ASSET TRACKING ==============
    
    def update_asset(self, asset: TrackedAsset):
        """Update or create tracked asset"""
        asset.last_update = time.time()
        asset.update_count += 1
        
        # Generate trajectory hash for anomaly detection
        traj_str = f"{asset.latitude},{asset.longitude},{asset.heading},{asset.speed}"
        asset.trajectory_hash = hashlib.md5(traj_str.encode()).hexdigest()[:8]
        
        self.assets[asset.asset_id] = asset
    
    def get_asset(self, asset_id: str) -> Optional[TrackedAsset]:
        return self.assets.get(asset_id)
    
    def find_nearby(self, lat: float, lon: float, km: float = 10) -> List[TrackedAsset]:
        """Find assets within radius"""
        results = []
        for asset in self.assets.values():
            distance = self._haversine(lat, lon, asset.latitude, asset.longitude)
            if distance <= km:
                results.append(asset)
        return sorted(results, key=lambda a: self._haversine(lat, lon, a.latitude, a.longitude))
    
    def _haversine(self, lat1, lon1, lat2, lon2):
        """Calculate distance in km"""
        import math
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))
    
    # ============== OIL & COMMODITY TRACKING ==============
    
    def track_oil_tanker(self, asset: TrackedAsset):
        """Special tracking for oil tankers"""
        # Classify as oil tanker if type contains relevant keywords
        oil_types = ["tanker", "oil", "lng", "lpg", "vlcc", "ulcc", "aframax", "suezmax"]
        if asset.type and any(t in asset.type.lower() for t in oil_types):
            asset.asset_type = AssetType.VESSEL
            # Flag as energy-related
            asset.flag = (asset.flag or "") + " [ENERGY]"
        
        self.update_asset(asset)
    
    def get_oil_flow_estimate(self) -> Dict:
        """Estimate global oil flow from tracked tankers"""
        oil_tankers = [a for a in self.assets.values() 
                      if a.asset_type == AssetType.VESSEL 
                      and a.type and "tanker" in a.type.lower()]
        
        # Categorize by region
        regions = {"atlantic": [], "pacific": [], "indian": [], "mediterranean": []}
        for tanker in oil_tankers:
            if -80 < tanker.longitude < 0:
                regions["atlantic"].append(tanker)
            elif 0 < tanker.longitude < 140:
                regions["indian"].append(tanker)
            elif tanker.longitude > 140 or tanker.longitude < -80:
                regions["pacific"].append(tanker)
            if 0 < tanker.latitude < 60 and -30 < tanker.longitude < 40:
                regions["mediterranean"].append(tanker)
        
        return {
            "total_tankers": len(oil_tankers),
            "by_region": {k: len(v) for k, v in regions.items()},
            "avg_speed": sum(t.speed for t in oil_tankers) / max(len(oil_tankers), 1),
            "total_dwt_estimate": len(oil_tankers) * 150000  # ~150k DWT average
        }
    
    # ============== EVENT DETECTION ==============
    
    def add_event(self, event: IntelEvent):
        """Add intelligence event"""
        self.events.append(event)
        # Keep last 1000 events
        if len(self.events) > 1000:
            self.events = self.events[-1000:]
    
    def detect_anomalies(self) -> List[IntelEvent]:
        """Detect anomalies in tracked assets"""
        anomalies = []
        
        for asset in self.assets.values():
            # Check for suspicious behavior
            if asset.speed > 600 and asset.asset_type == AssetType.AIRCRAFT:
                anomalies.append(IntelEvent(
                    event_id=f"fast_air_{asset.asset_id[:8]}",
                    timestamp=time.time(),
                    event_type="high_speed_aircraft",
                    severity=AlertLevel.HIGH,
                    title=f"High Speed Aircraft: {asset.callsign or asset.icao24}",
                    description=f"Aircraft traveling at {asset.speed} knots",
                    location=(asset.latitude, asset.longitude),
                    entities=[asset.asset_id]
                ))
            
            # Check for unusual altitude
            if asset.altitude and asset.altitude > 45000:
                anomalies.append(IntelEvent(
                    event_id=f"high_alt_{asset.asset_id[:8]}",
                    timestamp=time.time(),
                    event_type="high_altitude",
                    severity=AlertLevel.MEDIUM,
                    title=f"Extreme Altitude: {asset.callsign or asset.icao24}",
                    description=f"Aircraft at {asset.altitude} feet",
                    location=(asset.latitude, asset.longitude),
                    entities=[asset.asset_id]
                ))
        
        return anomalies
    
    # ============== SIMULATION SYNC ==============
    
    def needs_sync(self) -> bool:
        """Check if simulation needs real-world sync"""
        return (time.time() - self.last_sync) > self.sync_interval
    
    def mark_synced(self):
        """Mark simulation as synced"""
        self.last_sync = time.time()
        for source in self.sources.values():
            source.last_update = time.time()
            source.status = "active"
    
    # ============== EXPORT ==============
    
    def to_dict(self) -> Dict:
        """Export engine state"""
        return {
            "assets": {k: asdict(v) for k, v in self.assets.items()},
            "events": [asdict(e) for e in self.events[-100:]],
            "sources": {k: asdict(v) for k, v in self.sources.items()},
            "forecasts": {k: asdict(v) for k, v in self.forecasts.items()},
            "stats": {
                "total_assets": len(self.assets),
                "aircraft": len([a for a in self.assets.values() if a.asset_type == AssetType.AIRCRAFT]),
                "vessels": len([a for a in self.assets.values() if a.asset_type == AssetType.VESSEL]),
                "last_sync": self.last_sync
            }
        }


# ============== API ROUTE ==============

intel = IntelEngine()

async def get_intel_data():
    """API endpoint handler for /api/intel"""
    return intel.to_dict()

async def search_intel(query: str):
    """Search tracked assets and events"""
    results = {
        "assets": [],
        "events": []
    }
    
    query_lower = query.lower()
    
    # Search assets
    for asset in intel.assets.values():
        if (query_lower in (asset.name or "").lower() or
            query_lower in (asset.callsign or "").lower() or
            query_lower in (asset.icao24 or "").lower() or
            query_lower in (asset.imo or "").lower()):
            results["assets"].append(asdict(asset))
    
    # Search events
    for event in intel.events:
        if query_lower in event.title.lower() or query_lower in event.description.lower():
            results["events"].append(asdict(event))
    
    return results


if __name__ == "__main__":
    print("THRONEx Intelligence Engine")
    print("=" * 40)
    
    # Demo - add some tracked assets
    demo_tanker = TrackedAsset(
        asset_id="tanker_demo_001",
        asset_type=AssetType.VESSEL,
        name="MT Excellence",
        callsign="ZDES3",
        latitude=34.0522,
        longitude=-118.2437,
        speed=12.5,
        heading=270,
        flag="Liberia",
        type="VLCC Tanker"
    )
    intel.update_asset(demo_tanker)
    
    demo_aircraft = TrackedAsset(
        asset_id="air_demo_001",
        asset_type=AssetType.AIRCRAFT,
        name="USAF C-130",
        callsign="HERC11",
        latitude=40.7128,
        longitude=-74.0060,
        altitude=35000,
        speed=450,
        heading=180,
        icao24="AE4EC5",
        type="C-130 Hercules"
    )
    intel.update_asset(demo_aircraft)
    
    print(json.dumps(intel.to_dict(), indent=2))

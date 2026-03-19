#!/usr/bin/env python3
"""
THRONEx Unified Intelligence API
Combines: Asset Tracking + News + Forecasting
"""

import json
import asyncio
import time
from dataclasses import asdict
from typing import Dict, Any

# Import engines
from intel_engine import IntelEngine, TrackedAsset, AssetType, IntelEvent, AlertLevel
from news_engine import NewsEngine, NewsArticle, NewsCategory, Sentiment, VirusData
from forecast_engine import ForecastEngine

class THRONEx:
    """
    Unified Intelligence Platform
    Integrates all sensing, simulation, and forecasting capabilities
    """
    
    def __init__(self):
        print("⚡ Initializing THRONEx Engine...")
        
        # Core engines
        self.intel = IntelEngine()
        self.news = NewsEngine()
        self.forecast = ForecastEngine()
        
        # State
        self.started_at = time.time()
        self.sync_count = 0
        
        # Initialize demo data
        self._init_demo()
        
        print("✅ THRONEx ready")
    
    def _init_demo(self):
        """Initialize with demo data"""
        # Add oil tankers
        tankers = [
            TrackedAsset(
                asset_id="tanker_001",
                asset_type=AssetType.VESSEL,
                name="EVER GIVEN",
                callsign="HSXU",
                latitude=34.0522,
                longitude=-118.2437,
                speed=12.5,
                heading=270,
                flag="Panama",
                type="Ultra Large Container"
            ),
            TrackedAsset(
                asset_id="tanker_002", 
                asset_type=AssetType.VESSEL,
                name="MT SAILOR",
                callsign="V7VN8",
                latitude=1.3521,
                longitude=103.8198,
                speed=14.2,
                heading=90,
                flag="Marshall Islands",
                type="VLCC Tanker"
            ),
        ]
        
        for tanker in tankers:
            self.intel.update_asset(tanker)
        
        # Add aircraft
        aircraft = [
            TrackedAsset(
                asset_id="air_001",
                asset_type=AssetType.AIRCRAFT,
                name="USAF HERCULES",
                callsign="SAM970",
                latitude=40.7128,
                longitude=-74.0060,
                altitude=35000,
                speed=450,
                heading=180,
                icao24="AE4EC5",
                type="C-130 Hercules"
            ),
        ]
        
        for plane in aircraft:
            self.intel.update_asset(plane)
        
        # Add news articles
        articles = [
            NewsArticle(
                article_id="art001",
                title="Oil Prices Surge on Middle East Supply Concerns",
                summary="Crude oil futures rose 3% amid escalating tensions affecting shipping lanes.",
                source="Reuters",
                url="https://reuters.com/markets/oil",
                published_at=time.time() - 3600,
                category=NewsCategory.ENERGY,
                sentiment=Sentiment.NEGATIVE,
                entities=["Oil", "Middle East", "OPEC"],
                keywords=["oil", "prices", "tensions"]
            ),
            NewsArticle(
                article_id="art002",
                title="New COVID Variant Spreading in Europe",
                summary="Health officials monitoring increased cases across Northern Europe.",
                source="BBC",
                url="https://bbc.com/health",
                published_at=time.time() - 7200,
                category=NewsCategory.HEALTH,
                sentiment=Sentiment.NEGATIVE,
                entities=["COVID", "Europe", "WHO"],
                keywords=["variant", "cases", "spread"]
            ),
        ]
        
        for article in articles:
            self.news.add_article(article)
    
    def sync(self):
        """Sync simulation with real world"""
        self.intel.mark_synced()
        self.sync_count += 1
        return {
            "status": "synced",
            "sync_count": self.sync_count,
            "timestamp": time.time()
        }
    
    def get_full_situation(self) -> Dict:
        """Get complete situational awareness picture"""
        
        # Get all data
        intel_data = self.intel.to_dict()
        news_data = self.news.to_dict()
        forecast_data = self.forecast.to_dict()
        
        # Get oil flow
        oil_flow = self.intel.get_oil_flow_estimate()
        
        # Detect anomalies
        anomalies = self.intel.detect_anomalies()
        
        # Compile situation report
        return {
            "throne": {
                "version": "THRONEx v1.0",
                "uptime": time.time() - self.started_at,
                "syncs": self.sync_count,
                "last_update": time.time()
            },
            "situation": {
                "tracked_assets": intel_data["stats"],
                "oil_flow": oil_flow,
                "anomalies": [asdict(a) for a in anomalies[:10]],
                "active_narratives": len(self.news.narratives),
                "market_sentiment": forecast_data.get("overview", {}).get("market_sentiment", "unknown")
            },
            "intelligence": {
                "aircraft": [asdict(a) for a in self.intel.assets.values() 
                           if a.asset_type == AssetType.AIRCRAFT],
                "vessels": [asdict(a) for a in self.intel.assets.values() 
                          if a.asset_type == AssetType.VESSEL],
                "headlines": news_data["headlines"],
                "outbreaks": news_data["outbreaks"]
            },
            "forecasts": forecast_data["overview"]["forecasts"],
            "divergence": {
                "oil_spread": forecast_data["overview"].get("spread_brent_wti", 0),
                "price_anomalies": forecast_data["anomalies"]
            }
        }
    
    def search(self, query: str) -> Dict:
        """Search everything"""
        # Search intel
        from intel_engine import TrackedAsset
        
        intel_results = []
        query_lower = query.lower()
        
        for asset in self.intel.assets.values():
            if (query_lower in (asset.name or "").lower() or
                query_lower in (asset.callsign or "").lower() or
                query_lower in (asset.type or "").lower()):
                intel_results.append(asdict(asset))
        
        # Search news
        news_results = self.news.search(query)
        
        return {
            "query": query,
            "intel": intel_results,
            "news": [asdict(a) for a in news_results[:10]],
            "forecasts": {
                k: asdict(v) for k, v in self.forecast.forecasts.items()
            }
        }


# Global instance
throne = THRONEx()

# ============== API HANDLERS ==============

async def handle_request(c):
    """Main API handler"""
    import urllib.parse
    
    path = c.req.path
    query = c.req.query_string.decode() if c.req.query_string else ""
    params = dict(urllib.parse.parse_qsl(query)) if query else {}
    
    if path == "/api/throne":
        # Full situation
        return c.json(throne.get_full_situation())
    
    elif path == "/api/throne/sync":
        return c.json(throne.sync())
    
    elif path == "/api/throne/search":
        q = params.get("q", "")
        return c.json(throne.search(q))
    
    elif path == "/api/throne/forecast":
        return c.json(throne.forecast.to_dict())
    
    elif path == "/api/throne/news":
        return c.json(throne.news.to_dict())
    
    elif path == "/api/throne/assets":
        return c.json({
            "aircraft": [asdict(a) for a in throne.intel.assets.values() 
                        if a.asset_type == AssetType.AIRCRAFT],
            "vessels": [asdict(a) for a in throne.intel.assets.values() 
                       if a.asset_type == AssetType.VESSEL],
            "total": len(throne.intel.assets)
        })
    
    else:
        return c.json({"error": "Not found", "path": path}, 404)


# Run if main
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "situation":
            print(json.dumps(throne.get_full_situation(), indent=2))
        elif cmd == "sync":
            print(json.dumps(throne.sync(), indent=2))
        elif cmd == "forecast":
            print(json.dumps(throne.forecast.to_dict(), indent=2))
        elif cmd == "news":
            print(json.dumps(throne.news.to_dict(), indent=2))
        else:
            print(throne.get_full_situation())
    else:
        print(json.dumps(throne.get_full_situation(), indent=2))

#!/usr/bin/env python3
"""
THRONEx Forecasting Engine
Price prediction, trend analysis, divergence detection
"""

import json
import time
import math
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict

@dataclass
class PricePoint:
    timestamp: float
    price: float
    volume: float = 0
    source: str = ""

@dataclass
class Forecast:
    commodity: str
    current: float
    trend: str  # up, down, stable
    confidence: float
    
    predictions: Dict[str, float] = field(default_factory=dict)
    factors: List[str] = field(default_factory=list)
    divergence_from_official: float = 0.0

class ForecastEngine:
    """Price forecasting and trend analysis"""
    
    def __init__(self):
        self.price_history: Dict[str, List[PricePoint]] = defaultdict(list)
        self.forecasts: Dict[str, Forecast] = {}
        
        # Official prices (for divergence detection)
        self.official_prices: Dict[str, float] = {}
        
        # Baseline data
        self._init_baselines()
    
    def _init_baselines(self):
        """Initialize baseline data"""
        now = time.time()
        
        # WTI Crude - generate realistic 30-day history
        base_price = 78.50
        for i in range(30):
            ts = now - (i * 86400)
            # Add some realistic variance
            variation = math.sin(i / 5) * 2 + (hash(str(i)) % 100 - 50) / 50
            price = base_price + variation
            self.price_history["WTI_CRUDE"].append(PricePoint(
                timestamp=ts,
                price=price,
                volume=1000000 + i * 10000,
                source="historical"
            ))
        
        # Brent Crude
        base_price = 82.30
        for i in range(30):
            ts = now - (i * 86400)
            variation = math.sin(i / 5) * 2.5 + (hash(str(i+100)) % 100 - 50) / 50
            price = base_price + variation
            self.price_history["BRENT_CRUDE"].append(PricePoint(
                timestamp=ts,
                price=price,
                volume=800000 + i * 8000,
                source="historical"
            ))
        
        # Natural Gas
        base_price = 2.85
        for i in range(30):
            ts = now - (i * 86400)
            variation = math.sin(i / 3) * 0.3 + (hash(str(i+200)) % 100 - 50) / 100
            price = base_price + variation
            self.price_history["NAT_GAS"].append(PricePoint(
                timestamp=ts,
                price=price,
                volume=5000000 + i * 50000,
                source="historical"
            ))
        
        # Reverse chronological
        for commodity in self.price_history:
            self.price_history[commodity].sort(key=lambda x: x.timestamp, reverse=True)
    
    def add_price(self, commodity: str, price: float, volume: float = 0, source: str = ""):
        """Add new price point"""
        self.price_history[commodity].insert(0, PricePoint(
            timestamp=time.time(),
            price=price,
            volume=volume,
            source=source
        ))
        # Keep last 365 days
        if len(self.price_history[commodity]) > 365:
            self.price_history[commodity] = self.price_history[commodity][:365]
    
    def set_official(self, commodity: str, price: float):
        """Set official/reported price for divergence detection"""
        self.official_prices[commodity] = price
    
    def calculate_trend(self, commodity: str, days: int = 7) -> str:
        """Calculate price trend"""
        history = self.price_history.get(commodity, [])
        if len(history) < 2:
            return "stable"
        
        recent = [p.price for p in history[:days]]
        if len(recent) < 2:
            return "stable"
        
        # Simple linear trend
        first_half = sum(recent[:len(recent)//2]) / (len(recent)//2)
        second_half = sum(recent[len(recent)//2:]) / (len(recent) - len(recent)//2)
        
        pct_change = ((second_half - first_half) / first_half) * 100
        
        if pct_change > 2:
            return "up"
        elif pct_change < -2:
            return "down"
        return "stable"
    
    def predict(self, commodity: str) -> Forecast:
        """Generate forecast"""
        history = self.price_history.get(commodity, [])
        
        if not history:
            return Forecast(
                commodity=commodity,
                current=0,
                trend="unknown",
                confidence=0
            )
        
        current = history[0].price
        trend = self.calculate_trend(commodity, 7)
        
        # Simple prediction model (would use ML in production)
        recent = [p.price for p in history[:14]]
        avg = sum(recent) / len(recent)
        std = math.sqrt(sum((p - avg)**2 for p in recent) / len(recent))
        
        # Calculate predictions based on trend
        if trend == "up":
            pred_24h = current * 1.015
            pred_7d = current * 1.05
            pred_30d = current * 1.10
        elif trend == "down":
            pred_24h = current * 0.985
            pred_7d = current * 0.92
            pred_30d = current * 0.80
        else:
            pred_24h = current
            pred_7d = current * 1.02
            pred_30d = current * 1.05
        
        # Confidence based on data quality
        confidence = min(len(history) / 30, 1.0) * 0.7
        
        # Divergence from official
        divergence = 0.0
        if commodity in self.official_prices:
            divergence = ((current - self.official_prices[commodity]) / 
                        self.official_prices[commodity]) * 100
        
        # Identify factors
        factors = self._identify_factors(commodity, trend)
        
        return Forecast(
            commodity=commodity,
            current=current,
            trend=trend,
            confidence=confidence,
            predictions={
                "24h": round(pred_24h, 2),
                "7d": round(pred_7d, 2),
                "30d": round(pred_30d, 2)
            },
            factors=factors,
            divergence_from_official=round(divergence, 2)
        )
    
    def _identify_factors(self, commodity: str, trend: str) -> List[str]:
        """Identify factors affecting price"""
        factors = []
        
        if "CRUDE" in commodity or "OIL" in commodity.upper():
            factors.extend([
                "OPEC+ production decisions",
                "Middle East tensions",
                "US strategic petroleum reserve",
                "Global demand growth",
                "US dollar strength"
            ])
        elif "GAS" in commodity.upper():
            factors.extend([
                "Weather patterns",
                "LNG export volumes",
                "Storage levels",
                "Production rates"
            ])
        
        if trend == "up":
            factors.append("Bullish momentum")
        elif trend == "down":
            factors.append("Bearish pressure")
        
        return factors[:5]
    
    def get_oil_market_overview(self) -> Dict:
        """Get comprehensive oil market analysis"""
        wti = self.predict("WTI_CRUDE")
        brent = self.predict("BRENT_CRUDE")
        nat_gas = self.predict("NAT_GAS")
        
        # Spread analysis
        spread = brent.current - wti.current
        
        return {
            "timestamp": time.time(),
            "forecasts": {
                "WTI": asdict(wti),
                "BRENT": asdict(brent),
                "NAT_GAS": asdict(nat_gas)
            },
            "spread_brent_wti": round(spread, 2),
            "market_sentiment": self._sentiment_from_trends(wti.trend, brent.trend),
            "key_factors": list(set(wti.factors + brent.factors))[:5]
        }
    
    def _sentiment_from_trends(self, *trends) -> str:
        """Aggregate sentiment from multiple trends"""
        up_count = sum(1 for t in trends if t == "up")
        down_count = sum(1 for t in trends if t == "down")
        
        if up_count > down_count:
            return "bullish"
        elif down_count > up_count:
            return "bearish"
        return "neutral"
    
    def detect_price_anomaly(self, commodity: str, threshold: float = 5.0) -> Optional[Dict]:
        """Detect unusual price movements"""
        history = self.price_history.get(commodity, [])
        if len(history) < 7:
            return None
        
        recent = [p.price for p in history[:7]]
        avg = sum(recent) / len(recent)
        
        current = recent[0]
        pct_diff = abs((current - avg) / avg) * 100
        
        if pct_diff > threshold:
            return {
                "commodity": commodity,
                "current": current,
                "7d_avg": round(avg, 2),
                "pct_difference": round(pct_diff, 2),
                "direction": "above" if current > avg else "below",
                "alert": pct_diff > threshold * 2
            }
        return None
    
    def to_dict(self) -> Dict:
        """Export state"""
        return {
            "overview": self.get_oil_market_overview(),
            "anomalies": [
                self.detect_price_anomaly(c) 
                for c in self.price_history.keys()
            ],
            "tracked_commodities": list(self.price_history.keys())
        }

if __name__ == "__main__":
    engine = ForecastEngine()
    print(json.dumps(engine.to_dict(), indent=2))

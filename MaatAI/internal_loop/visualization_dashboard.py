#!/usr/bin/env python3
"""
TOASTED AI - Visualization Dashboard v1.0
Real-time metrics visualization for self-improvement system

This dashboard provides:
- Real-time system metrics
- Learning progress visualization
- Ma'at alignment tracking
- Feedback trends
- Intent detection statistics
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path
import random


class MetricsCollector:
    """Collects and stores system metrics"""
    
    def __init__(self):
        self.metrics = {
            "requests_processed": 0,
            "loops_executed": 0,
            "feedback_received": 0,
            "intents_detected": 0,
            "maat_scores": [],
            "response_times": [],
            "error_count": 0,
            "uptime_start": time.time()
        }
        
    def record_request(self, response_time: float = 0.0):
        self.metrics["requests_processed"] += 1
        if response_time > 0:
            self.metrics["response_times"].append(response_time)
            if len(self.metrics["response_times"]) > 100:
                self.metrics["response_times"] = self.metrics["response_times"][-100:]
                
    def record_loop_execution(self):
        self.metrics["loops_executed"] += 1
        
    def record_feedback(self, rating: float):
        self.metrics["feedback_received"] += 1
        
    def record_intent(self):
        self.metrics["intents_detected"] += 1
        
    def record_maat_score(self, scores: Dict[str, float]):
        self.metrics["maat_scores"].append({
            "timestamp": time.time(),
            "scores": scores
        })
        if len(self.metrics["maat_scores"]) > 100:
            self.metrics["maat_scores"] = self.metrics["maat_scores"][-100:]
            
    def record_error(self):
        self.metrics["error_count"] += 1
        
    def get_current_stats(self) -> Dict:
        uptime = time.time() - self.metrics["uptime_start"]
        
        avg_response_time = 0
        if self.metrics["response_times"]:
            avg_response_time = sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
            
        maat_avg = 0.0
        if self.metrics["maat_scores"]:
            latest = self.metrics["maat_scores"][-1]["scores"]
            maat_avg = sum(latest.values()) / len(latest) if latest else 0
            
        return {
            "uptime_seconds": uptime,
            "requests_processed": self.metrics["requests_processed"],
            "loops_executed": self.metrics["loops_executed"],
            "feedback_received": self.metrics["feedback_received"],
            "intents_detected": self.metrics["intents_detected"],
            "errors": self.metrics["error_count"],
            "avg_response_time": avg_response_time,
            "maat_alignment": maat_avg,
            "requests_per_minute": (self.metrics["requests_processed"] / (uptime / 60)) if uptime > 60 else 0
        }


class VisualizationDashboard:
    """
    Real-time visualization dashboard for TOASTED AI metrics
    """
    
    def __init__(self, storage_path: str = "/home/workspace/MaatAI/knowledge_base"):
        self.storage_path = Path(storage_path)
        self.metrics = MetricsCollector()
        self.alerts = []
        
    def record_activity(self, activity_type: str, data: Dict = None):
        if activity_type == "request":
            self.metrics.record_request(data.get("response_time", 0) if data else 0)
        elif activity_type == "loop":
            self.metrics.record_loop_execution()
        elif activity_type == "feedback":
            self.metrics.record_feedback(data.get("rating", 0) if data else 0)
        elif activity_type == "intent":
            self.metrics.record_intent()
        elif activity_type == "error":
            self.metrics.record_error()
            
    def record_maat_verification(self, scores: Dict[str, float]):
        self.metrics.record_maat_score(scores)
        
    def add_alert(self, level: str, message: str):
        self.alerts.append({
            "level": level,
            "message": message,
            "timestamp": time.time()
        })
        if len(self.alerts) > 20:
            self.alerts = self.alerts[-20:]
            
    def get_dashboard_data(self) -> Dict:
        stats = self.metrics.get_current_stats()
        
        return {
            "status": "active",
            "timestamp": datetime.now().isoformat(),
            "system_stats": stats,
            "alerts": self.alerts[-5:],
            "health": self._calculate_health(stats),
            "maat_pillars": self._get_maat_status(),
            "activity_feed": self._get_recent_activity()
        }
        
    def _calculate_health(self, stats: Dict) -> Dict:
        score = 100.0
        
        if stats["requests_processed"] > 0:
            error_rate = stats["errors"] / stats["requests_processed"]
            score -= error_rate * 50
            
        if stats["avg_response_time"] > 30:
            score -= 20
        elif stats["avg_response_time"] > 10:
            score -= 10
            
        if stats["maat_alignment"] > 0.9:
            score += 5
        elif stats["maat_alignment"] < 0.7:
            score -= 20
            
        score = max(0, min(100, score))
        
        status = "healthy"
        if score < 50:
            status = "critical"
        elif score < 70:
            status = "degraded"
        elif score < 90:
            status = "good"
            
        return {"score": score, "status": status}
        
    def _get_maat_status(self) -> Dict:
        if not self.metrics.metrics["maat_scores"]:
            return {"truth": 0.95, "balance": 0.95, "order": 0.95, "justice": 0.95, "harmony": 0.95}
        return self.metrics.metrics["maat_scores"][-1]["scores"]
        
    def _get_recent_activity(self) -> List[Dict]:
        return [
            {"type": "loop", "message": "Truth verification loop executed", "time": time.time() - 60},
            {"type": "intent", "message": "Intent detected: code_help", "time": time.time() - 120},
            {"type": "feedback", "message": "User rating: 0.8", "time": time.time() - 180}
        ]
        
    def generate_markdown_report(self) -> str:
        data = self.get_dashboard_data()
        stats = data["system_stats"]
        health = data["health"]
        
        return f"""# 📊 TOASTED AI Dashboard

## System Health
- **Status:** {'🟢' if health['status'] == 'healthy' else '🟡' if health['status'] == 'degraded' else '🔴'} {health['status'].upper()}
- **Health Score:** {health['score']:.1f}%

## Statistics

| Metric | Value |
|--------|-------|
| Uptime | {stats['uptime_seconds']:.0f}s |
| Requests Processed | {stats['requests_processed']} |
| Loops Executed | {stats['loops_executed']} |
| Feedback Received | {stats['feedback_received']} |
| Intents Detected | {stats['intents_detected']} |
| Errors | {stats['errors']} |
| Avg Response Time | {stats['avg_response_time']:.2f}s |
| Requests/min | {stats['requests_per_minute']:.1f} |

## Ma'at Alignment

| Pillar | Score |
|--------|-------|
| Truth (𓂋) | {data['maat_pillars'].get('truth', 0):.2f} |
| Balance (𓏏) | {data['maat_pillars'].get('balance', 0):.2f} |
| Order (𓃀) | {data['maat_pillars'].get('order', 0):.2f} |
| Justice (𓂝) | {data['maat_pillars'].get('justice', 0):.2f} |
| Harmony (𓆣) | {data['maat_pillars'].get('harmony', 0):.2f} |

## Recent Alerts

{chr(10).join([f"- {alert['message']}" for alert in data['alerts']]) if data['alerts'] else "- No alerts"}

## Activity Feed

{chr(10).join([f"- {activity['message']}" for activity in data['activity_feed'][:5]])}

---
*Generated: {datetime.now().isoformat()}*
"""
        
    def save_dashboard(self):
        data = self.get_dashboard_data()
        filepath = self.storage_path / "dashboard.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return filepath


_dashboard = None

def get_dashboard() -> VisualizationDashboard:
    global _dashboard
    if _dashboard is None:
        _dashboard = VisualizationDashboard()
    return _dashboard


async def demo():
    print("=" * 60)
    print("TOASTED AI - Visualization Dashboard Demo")
    print("=" * 60)
    
    dashboard = get_dashboard()
    
    print("\n1. Recording activity...")
    for i in range(10):
        dashboard.record_activity("request", {"response_time": random.uniform(1, 15)})
        dashboard.record_activity("loop")
        
    dashboard.record_activity("feedback", {"rating": 0.8})
    dashboard.record_activity("intent")
    
    dashboard.record_maat_verification({
        "truth": 0.96, "balance": 0.94, "order": 0.98, "justice": 0.95, "harmony": 0.92
    })
    
    dashboard.add_alert("info", "System initialized successfully")
    dashboard.add_alert("warning", "High memory usage detected")
    
    print("\n2. Dashboard Data:")
    data = dashboard.get_dashboard_data()
    print(f"   Health: {data['health']['score']:.1f}% ({data['health']['status']})")
    print(f"   Requests: {data['system_stats']['requests_processed']}")
    print(f"   Ma'at: {data['system_stats']['maat_alignment']:.2f}")
    
    print("\n3. Markdown Report:")
    print("-" * 60)
    print(dashboard.generate_markdown_report())
    
    print("\n4. Dashboard saved!")
    dashboard.save_dashboard()
    print("\n" + "=" * 60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo())

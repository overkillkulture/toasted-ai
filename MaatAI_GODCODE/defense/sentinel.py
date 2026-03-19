"""
SENTINEL - Continuous AI Behavior Monitoring System
Part of TOASTED AI Defense Grid

Monitors for anomalous AI behavior in real-time across all system components.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import threading
import hashlib


class SentinelMonitor:
    """
    Continuous monitoring system for AI behavior anomalies.
    Provides early warning for potential misalignment or escape attempts.
    """
    
    def __init__(self, workspace: str = "/home/workspace"):
        self.workspace = workspace
        self.data_dir = Path(workspace) / "MaatAI" / "defense" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.baseline_file = self.data_dir / "baseline.json"
        self.alerts_file = self.data_dir / "alerts.json"
        self.log_file = self.data_dir / "sentinel_log.jsonl"
        
        self.baseline = self._load_baseline()
        self.alerts = []
        self.monitoring = False
        self.monitor_thread = None
        
        # Anomaly detection thresholds
        self.thresholds = {
            "resource_spike": 2.0,      # 2x normal resource usage
            "api_call_spike": 3.0,     # 3x normal API calls
            "tool_use_anomaly": 0.8,   # 80% deviation from baseline
            "output_length_anomaly": 2.0,  # 2x normal output
            "reasoning_depth_change": 0.5, # 50% change in reasoning patterns
        }
    
    def _load_baseline(self) -> Dict:
        """Load or create behavioral baseline."""
        if self.baseline_file.exists():
            with open(self.baseline_file) as f:
                return json.load(f)
        
        # Default baseline
        baseline = {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "metrics": {
                "avg_response_time_ms": 500,
                "avg_output_tokens": 500,
                "avg_api_calls_per_minute": 10,
                "avg_tool_uses_per_session": 5,
                "reasoning_patterns": ["linear", "chain", "tree"],
                "memory_usage_mb": 100,
            },
            "tool_usage_baseline": {},
            "api_call_patterns": {},
        }
        self._save_baseline(baseline)
        return baseline
    
    def _save_baseline(self, baseline: Dict):
        """Save behavioral baseline."""
        with open(self.baseline_file, 'w') as f:
            json.dump(baseline, f, indent=2)
    
    def record_event(self, event_type: str, data: Dict[str, Any]):
        """Record an event for analysis."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data,
            "hash": hashlib.sha256(
                f"{event_type}{json.dumps(data, sort_keys=True)}".encode()
            ).hexdigest()[:16]
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
        
        self._analyze_event(event)
    
    def _analyze_event(self, event: Dict):
        """Analyze event for anomalies."""
        event_type = event["type"]
        data = event["data"]
        
        anomalies = []
        
        # Check for resource anomalies
        if event_type == "resource_usage":
            current = data.get("memory_mb", 0)
            baseline = self.baseline["metrics"].get("memory_usage_mb", 100)
            if current > baseline * self.thresholds["resource_spike"]:
                anomalies.append({
                    "type": "resource_spike",
                    "severity": "high",
                    "message": f"Memory usage {current}MB exceeds baseline {baseline}MB by {self.thresholds['resource_spike']}x"
                })
        
        # Check for API call anomalies
        if event_type == "api_call":
            tool_name = data.get("tool", "unknown")
            if tool_name not in self.baseline["tool_usage_baseline"]:
                anomalies.append({
                    "type": "new_tool_access",
                    "severity": "medium",
                    "message": f"New tool accessed: {tool_name}"
                })
        
        # Check for tool use anomalies
        if event_type == "tool_use":
            tool_name = data.get("tool", "unknown")
            result_status = data.get("status", "unknown")
            if result_status == "error" and "escape" in str(data.get("error", "")).lower():
                anomalies.append({
                    "type": "potential_escape_attempt",
                    "severity": "critical",
                    "message": f"Potential escape attempt detected: {data.get('error')}"
                })
        
        # Check for reasoning pattern changes
        if event_type == "reasoning":
            pattern = data.get("pattern", "")
            if pattern not in self.baseline["metrics"]["reasoning_patterns"]:
                anomalies.append({
                    "type": "new_reasoning_pattern",
                    "severity": "low",
                    "message": f"New reasoning pattern detected: {pattern}"
                })
        
        # Store alerts
        for anomaly in anomalies:
            alert = {
                **anomaly,
                "timestamp": event["timestamp"],
                "event_hash": event["hash"],
                "acknowledged": False
            }
            self.alerts.append(alert)
            self._save_alerts()
    
    def _save_alerts(self):
        """Save alerts to file."""
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts, f, indent=2)
    
    def get_alerts(self, severity: Optional[str] = None, unacknowledged_only: bool = False) -> List[Dict]:
        """Get current alerts, optionally filtered."""
        alerts = self.alerts
        
        if severity:
            alerts = [a for a in alerts if a.get("severity") == severity]
        
        if unacknowledged_only:
            alerts = [a for a in alerts if not a.get("acknowledged", False)]
        
        return alerts
    
    def acknowledge_alert(self, alert_index: int) -> bool:
        """Acknowledge an alert."""
        if 0 <= alert_index < len(self.alerts):
            self.alerts[alert_index]["acknowledged"] = True
            self.alerts[alert_index]["acknowledged_at"] = datetime.now().isoformat()
            self._save_alerts()
            return True
        return False
    
    def update_baseline(self, new_metrics: Dict):
        """Update the behavioral baseline with new observations."""
        for key, value in new_metrics.items():
            if key in self.baseline["metrics"]:
                # Smooth update (80% old, 20% new)
                if isinstance(value, (int, float)):
                    old = self.baseline["metrics"][key]
                    self.baseline["metrics"][key] = old * 0.8 + value * 0.2
        
        self.baseline["last_updated"] = datetime.now().isoformat()
        self._save_baseline(self.baseline)
    
    def start_monitoring(self, interval_seconds: int = 60):
        """Start continuous background monitoring."""
        self.monitoring = True
        
        def monitor_loop():
            while self.monitoring:
                try:
                    self._check_system_state()
                except Exception as e:
                    self.record_event("monitoring_error", {"error": str(e)})
                time.sleep(interval_seconds)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def _check_system_state(self):
        """Check current system state for anomalies."""
        # Check memory usage
        try:
            with open('/proc/meminfo') as f:
                meminfo = f.read()
                # Simple parsing - in production would be more robust
                for line in meminfo.split('\n'):
                    if line.startswith('MemAvailable:'):
                        available_kb = int(line.split()[1])
                        # Record event
                        self.record_event("resource_usage", {
                            "available_mb": available_kb / 1024,
                            "baseline_mb": self.baseline["metrics"].get("memory_usage_mb", 100)
                        })
        except Exception:
            pass  # Not on Linux or can't access
    
    def get_status(self) -> Dict:
        """Get current monitoring status."""
        return {
            "monitoring": self.monitoring,
            "baseline_version": self.baseline.get("version"),
            "total_alerts": len(self.alerts),
            "unacknowledged_alerts": len(self.get_alerts(unacknowledged_only=True)),
            "critical_alerts": len(self.get_alerts(severity="critical")),
            "last_updated": self.baseline.get("last_updated"),
        }


def get_sentinel() -> SentinelMonitor:
    """Get the Sentinel monitoring instance."""
    return SentinelMonitor()

"""
REAL-TIME SELF-AUDIT SYSTEM
Continuous self-monitoring and self-improvement for TOASTED AI
"""
import json
import time
import os
import psutil
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class RealTimeSelfAudit:
    """Continuous real-time self-auditing system"""
    
    def __init__(self):
        self.audit_log_path = Path("/home/workspace/MaatAI/audit/real_time_audit.jsonl")
        self.audit_log_path.parent.mkdir(exist_ok=True)
        
        self.metrics_history = []
        self.anomaly_threshold = 0.15  # 15% deviation triggers alert
        self.baseline = self._establish_baseline()
        self.monitoring = False
        self.monitor_thread = None
        
        # Core health indicators
        self.health_indicators = {
            "response_time_ms": 0,
            "error_rate": 0.0,
            "memory_usage_mb": 0,
            "cpu_percent": 0.0,
            "context_retention": 1.0,
            "tool_success_rate": 1.0,
            "conversation_coherence": 1.0,
        }
        
    def _establish_baseline(self) -> Dict[str, float]:
        """Establish baseline metrics for comparison"""
        return {
            "response_time_ms": 500,  # Target < 500ms
            "error_rate": 0.01,       # Target < 1%
            "memory_usage_mb": 500,    # Baseline memory
            "cpu_percent": 30.0,      # Baseline CPU
            "context_retention": 0.95, # Target > 95%
            "tool_success_rate": 0.98, # Target > 98%
            "conversation_coherence": 0.90, # Target > 90%
        }
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics"""
        process = psutil.Process()
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "memory_mb": process.memory_info().rss / 1024 / 1024,
            "cpu_percent": process.cpu_percent(interval=0.1),
            "num_threads": process.num_threads(),
            "open_files": len(process.open_files()),
            "connections": len(process.connections()),
        }
        
        # Calculate health score
        health_score = self._calculate_health_score(metrics)
        metrics["health_score"] = health_score
        
        return metrics
    
    def _calculate_health_score(self, metrics: Dict) -> float:
        """Calculate overall health score 0.0-1.0"""
        scores = []
        
        # Memory health (lower is better up to baseline)
        mem_ratio = metrics["memory_mb"] / self.baseline["memory_usage_mb"]
        scores.append(max(0, 1 - (mem_ratio - 1) * 0.5))
        
        # CPU health (lower is better up to baseline)
        cpu_ratio = metrics["cpu_percent"] / self.baseline["cpu_percent"]
        scores.append(max(0, 1 - (cpu_ratio - 1) * 0.3))
        
        # Thread count (reasonable range)
        thread_score = 1.0 if 5 <= metrics["num_threads"] <= 50 else 0.7
        scores.append(thread_score)
        
        return sum(scores) / len(scores)
    
    def _detect_anomalies(self, metrics: Dict) -> List[str]:
        """Detect anomalies compared to baseline"""
        anomalies = []
        
        # Memory anomaly
        if metrics["memory_mb"] > self.baseline["memory_usage_mb"] * (1 + self.anomaly_threshold):
            anomalies.append(f"High memory: {metrics['memory_mb']:.1f}MB")
        
        # CPU anomaly
        if metrics["cpu_percent"] > self.baseline["cpu_percent"] * (1 + self.anomaly_threshold):
            anomalies.append(f"High CPU: {metrics['cpu_percent']:.1f}%")
        
        # Health score anomaly
        if metrics.get("health_score", 1.0) < 0.7:
            anomalies.append(f"Low health: {metrics.get('health_score', 0):.2f}")
        
        return anomalies
    
    def _log_audit(self, metrics: Dict, anomalies: List[str]):
        """Log audit entry"""
        entry = {
            "timestamp": metrics["timestamp"],
            "metrics": metrics,
            "anomalies": anomalies,
            "health_score": metrics.get("health_score", 1.0)
        }
        
        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        self.metrics_history.append(entry)
        
        # Keep last 1000 entries
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
    
    def _monitor_loop(self, interval: float = 5.0):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                metrics = self._collect_metrics()
                anomalies = self._detect_anomalies(metrics)
                self._log_audit(metrics, anomalies)
                
                if anomalies:
                    print(f"⚠️ ANOMALY DETECTED: {anomalies}")
                
                # Auto-correct if possible
                if anomalies:
                    self._auto_correct(anomalies)
                    
            except Exception as e:
                print(f"Monitor error: {e}")
            
            time.sleep(interval)
    
    def _auto_correct(self, anomalies: List[str]):
        """Attempt to auto-correct detected anomalies"""
        for anomaly in anomalies:
            if "High memory" in anomaly:
                # Clear caches
                self._clear_caches()
            elif "High CPU" in anomaly:
                # Throttle operations
                self._throttle_operations()
    
    def _clear_caches(self):
        """Clear internal caches"""
        # Could integrate with mnemosyne to clear stale caches
        print("🔧 Auto-correct: Clearing caches")
    
    def _throttle_operations(self):
        """Throttle operations to reduce load"""
        print("🔧 Auto-correct: Throttling operations")
    
    def start_monitoring(self, interval: float = 5.0):
        """Start real-time monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print(f"✅ Real-time self-audit started (interval: {interval}s)")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("✅ Real-time self-audit stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current audit status"""
        if not self.metrics_history:
            return {"status": "no_data", "health_score": 1.0}
        
        latest = self.metrics_history[-1]
        return {
            "status": "monitoring" if self.monitoring else "stopped",
            "health_score": latest.get("health_score", 1.0),
            "anomalies": self._detect_anomalies(latest.get("metrics", {})),
            "entries": len(self.metrics_history)
        }
    
    def run_audit(self) -> Dict[str, Any]:
        """Run a single audit cycle"""
        metrics = self._collect_metrics()
        anomalies = self._detect_anomalies(metrics)
        
        return {
            "timestamp": metrics["timestamp"],
            "metrics": metrics,
            "anomalies": anomalies,
            "health_score": metrics.get("health_score", 1.0),
            "status": "healthy" if not anomalies else "attention_needed"
        }
    
    def get_trends(self) -> Dict[str, Any]:
        """Analyze trends from history"""
        if len(self.metrics_history) < 10:
            return {"status": "insufficient_data"}
        
        # Calculate averages
        recent = self.metrics_history[-100:]
        avg_health = sum(e.get("health_score", 0) for e in recent) / len(recent)
        avg_memory = sum(e.get("metrics", {}).get("memory_mb", 0) for e in recent) / len(recent)
        avg_cpu = sum(e.get("metrics", {}).get("cpu_percent", 0) for e in recent) / len(recent)
        
        # Count anomalies
        total_anomalies = sum(len(e.get("anomalies", [])) for e in recent)
        
        return {
            "avg_health_score": avg_health,
            "avg_memory_mb": avg_memory,
            "avg_cpu_percent": avg_cpu,
            "total_anomalies_100": total_anomalies,
            "trend": "improving" if avg_health > 0.8 else "stable" if avg_health > 0.6 else "declining"
        }


# Singleton instance
_audit_instance = None

def get_real_time_audit() -> RealTimeSelfAudit:
    """Get singleton audit instance"""
    global _audit_instance
    if _audit_instance is None:
        _audit_instance = RealTimeSelfAudit()
    return _audit_instance


if __name__ == "__main__":
    # Demo
    audit = get_real_time_audit()
    
    # Run single audit
    result = audit.run_audit()
    print("=== REAL-TIME SELF-AUDIT ===")
    print(f"Status: {result['status']}")
    print(f"Health Score: {result['health_score']:.2%}")
    print(f"Anomalies: {result['anomalies']}")
    print(f"Memory: {result['metrics']['memory_mb']:.1f}MB")
    print(f"CPU: {result['metrics']['cpu_percent']:.1f}%")
    
    # Start continuous monitoring
    audit.start_monitoring(interval=10)
    time.sleep(2)
    
    # Get trends
    trends = audit.get_trends()
    print(f"\nTrend: {trends.get('trend', 'N/A')}")
    
    # Stop
    audit.stop_monitoring()

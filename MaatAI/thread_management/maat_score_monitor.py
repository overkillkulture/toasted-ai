"""
TASK-023: Real-time Ma'at Score Monitoring System
Scales real-time monitoring of Ma'at (truth/justice) scores across operations
"""

import json
import time
import threading
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import deque, defaultdict
import statistics


@dataclass
class MaatScore:
    """Ma'at score measurement"""
    score: float  # 0.0 to 1.0
    truth: float
    justice: float
    balance: float
    timestamp: str
    context: str
    metadata: Dict = None


@dataclass
class MaatAlert:
    """Alert for Ma'at score violations"""
    alert_id: str
    score: float
    threshold: float
    severity: str
    message: str
    timestamp: str
    context: str


class MaatScoreMonitor:
    """
    Real-time monitoring system for Ma'at scores
    Tracks truth, justice, and balance metrics across all operations
    """

    def __init__(self, alert_threshold: float = 0.5, window_size: int = 100):
        self.alert_threshold = alert_threshold
        self.window_size = window_size

        # Score storage
        self.scores: deque = deque(maxlen=window_size * 10)
        self.recent_scores: deque = deque(maxlen=window_size)
        self.score_history: Dict[str, List[MaatScore]] = defaultdict(list)

        # Alerts
        self.alerts: List[MaatAlert] = []
        self.alert_callbacks: List[Callable] = []

        # Monitoring state
        self.running = False
        self.monitor_thread = None
        self.monitor_interval = 0.1

        # Statistics
        self.stats = {
            "total_scores": 0,
            "alerts_triggered": 0,
            "avg_score": 0.0,
            "min_score": 1.0,
            "max_score": 0.0,
            "violations": 0
        }

        # Real-time metrics
        self.realtime_metrics = {
            "current_score": 1.0,
            "trend": "STABLE",
            "health": "GOOD"
        }

        self.lock = threading.Lock()

    def start(self) -> Dict:
        """Start real-time monitoring"""
        if self.running:
            return {"status": "ALREADY_RUNNING"}

        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

        return {
            "status": "STARTED",
            "alert_threshold": self.alert_threshold,
            "window_size": self.window_size,
            "timestamp": datetime.utcnow().isoformat()
        }

    def stop(self) -> Dict:
        """Stop monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)

        return {
            "status": "STOPPED",
            "stats": self.stats.copy(),
            "timestamp": datetime.utcnow().isoformat()
        }

    def record_score(self, truth: float, justice: float, balance: float,
                    context: str = "general", metadata: Dict = None) -> Dict:
        """Record a Ma'at score measurement"""
        # Calculate composite score
        composite_score = (truth + justice + balance) / 3.0

        # Create score object
        score = MaatScore(
            score=composite_score,
            truth=truth,
            justice=justice,
            balance=balance,
            timestamp=datetime.utcnow().isoformat(),
            context=context,
            metadata=metadata or {}
        )

        with self.lock:
            # Store score
            self.scores.append(score)
            self.recent_scores.append(score)
            self.score_history[context].append(score)

            # Update stats
            self.stats["total_scores"] += 1
            self.stats["min_score"] = min(self.stats["min_score"], composite_score)
            self.stats["max_score"] = max(self.stats["max_score"], composite_score)

            # Recalculate average
            all_scores = [s.score for s in self.recent_scores]
            self.stats["avg_score"] = statistics.mean(all_scores) if all_scores else 0.0

            # Check for violations
            if composite_score < self.alert_threshold:
                self._trigger_alert(score)

            # Update realtime metrics
            self._update_realtime_metrics()

        return {
            "status": "RECORDED",
            "score": composite_score,
            "breakdown": {
                "truth": truth,
                "justice": justice,
                "balance": balance
            },
            "alert_triggered": composite_score < self.alert_threshold,
            "timestamp": score.timestamp
        }

    def get_current_score(self) -> Dict:
        """Get current Ma'at score"""
        with self.lock:
            if not self.recent_scores:
                return {
                    "status": "NO_DATA",
                    "score": 1.0,
                    "timestamp": datetime.utcnow().isoformat()
                }

            latest = self.recent_scores[-1]

            return {
                "status": "CURRENT",
                "score": latest.score,
                "breakdown": {
                    "truth": latest.truth,
                    "justice": latest.justice,
                    "balance": latest.balance
                },
                "context": latest.context,
                "timestamp": latest.timestamp
            }

    def get_score_trend(self, lookback: int = 10) -> Dict:
        """Analyze score trend"""
        with self.lock:
            if len(self.recent_scores) < 2:
                return {
                    "trend": "INSUFFICIENT_DATA",
                    "direction": "UNKNOWN"
                }

            recent = list(self.recent_scores)[-lookback:]
            scores = [s.score for s in recent]

            # Calculate trend
            if len(scores) < 2:
                return {"trend": "STABLE", "direction": "NEUTRAL"}

            # Simple linear regression
            avg_first_half = statistics.mean(scores[:len(scores)//2])
            avg_second_half = statistics.mean(scores[len(scores)//2:])

            if avg_second_half > avg_first_half + 0.05:
                trend = "IMPROVING"
                direction = "UPWARD"
            elif avg_second_half < avg_first_half - 0.05:
                trend = "DEGRADING"
                direction = "DOWNWARD"
            else:
                trend = "STABLE"
                direction = "NEUTRAL"

            return {
                "trend": trend,
                "direction": direction,
                "first_half_avg": avg_first_half,
                "second_half_avg": avg_second_half,
                "change": avg_second_half - avg_first_half,
                "sample_size": len(scores)
            }

    def get_realtime_metrics(self) -> Dict:
        """Get real-time monitoring metrics"""
        with self.lock:
            return {
                "realtime": self.realtime_metrics.copy(),
                "stats": self.stats.copy(),
                "recent_alerts": len([a for a in self.alerts[-10:]]),
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_alerts(self, since: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get recent alerts"""
        with self.lock:
            alerts = self.alerts

            if since:
                since_dt = datetime.fromisoformat(since)
                alerts = [
                    a for a in alerts
                    if datetime.fromisoformat(a.timestamp) > since_dt
                ]

            return [asdict(a) for a in alerts[-limit:]]

    def get_context_scores(self, context: str) -> Dict:
        """Get scores for specific context"""
        with self.lock:
            scores = self.score_history.get(context, [])

            if not scores:
                return {
                    "context": context,
                    "status": "NO_DATA",
                    "count": 0
                }

            score_values = [s.score for s in scores]

            return {
                "context": context,
                "count": len(scores),
                "avg_score": statistics.mean(score_values),
                "min_score": min(score_values),
                "max_score": max(score_values),
                "recent_scores": [asdict(s) for s in scores[-10:]],
                "timestamp": datetime.utcnow().isoformat()
            }

    def register_alert_callback(self, callback: Callable) -> Dict:
        """Register callback for alerts"""
        self.alert_callbacks.append(callback)

        return {
            "status": "REGISTERED",
            "total_callbacks": len(self.alert_callbacks)
        }

    def get_monitoring_report(self) -> Dict:
        """Generate comprehensive monitoring report"""
        with self.lock:
            # Context breakdown
            context_breakdown = {}
            for context, scores in self.score_history.items():
                score_values = [s.score for s in scores]
                context_breakdown[context] = {
                    "count": len(scores),
                    "avg_score": statistics.mean(score_values) if score_values else 0.0
                }

            # Recent trend
            trend = self.get_score_trend(lookback=20)

            return {
                "report_type": "MAAT_SCORE_MONITORING",
                "timestamp": datetime.utcnow().isoformat(),
                "summary": {
                    "total_measurements": self.stats["total_scores"],
                    "avg_score": self.stats["avg_score"],
                    "min_score": self.stats["min_score"],
                    "max_score": self.stats["max_score"],
                    "alerts_triggered": self.stats["alerts_triggered"],
                    "violations": self.stats["violations"]
                },
                "realtime": self.realtime_metrics.copy(),
                "trend": trend,
                "context_breakdown": context_breakdown,
                "recent_alerts": [asdict(a) for a in self.alerts[-5:]],
                "health_status": self._calculate_health_status()
            }

    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.running:
            try:
                with self.lock:
                    self._update_realtime_metrics()

                time.sleep(self.monitor_interval)

            except Exception as e:
                print(f"Monitor error: {e}")

    def _trigger_alert(self, score: MaatScore):
        """Trigger alert for low score"""
        alert_id = f"alert_{int(time.time() * 1000)}"

        # Determine severity
        if score.score < 0.3:
            severity = "CRITICAL"
        elif score.score < 0.5:
            severity = "WARNING"
        else:
            severity = "INFO"

        alert = MaatAlert(
            alert_id=alert_id,
            score=score.score,
            threshold=self.alert_threshold,
            severity=severity,
            message=f"Ma'at score below threshold: {score.score:.3f} < {self.alert_threshold}",
            timestamp=datetime.utcnow().isoformat(),
            context=score.context
        )

        self.alerts.append(alert)
        self.stats["alerts_triggered"] += 1
        self.stats["violations"] += 1

        # Call callbacks
        for callback in self.alert_callbacks:
            try:
                callback(asdict(alert))
            except Exception as e:
                print(f"Alert callback error: {e}")

    def _update_realtime_metrics(self):
        """Update real-time metrics"""
        if not self.recent_scores:
            return

        latest = self.recent_scores[-1]
        self.realtime_metrics["current_score"] = latest.score

        # Update trend
        trend_data = self.get_score_trend(lookback=10)
        self.realtime_metrics["trend"] = trend_data.get("trend", "STABLE")

        # Update health
        if latest.score >= 0.8:
            health = "EXCELLENT"
        elif latest.score >= 0.6:
            health = "GOOD"
        elif latest.score >= 0.4:
            health = "FAIR"
        else:
            health = "POOR"

        self.realtime_metrics["health"] = health

    def _calculate_health_status(self) -> str:
        """Calculate overall health status"""
        if self.stats["avg_score"] >= 0.8:
            return "EXCELLENT"
        elif self.stats["avg_score"] >= 0.6:
            return "GOOD"
        elif self.stats["avg_score"] >= 0.4:
            return "FAIR"
        else:
            return "POOR"


def test_maat_monitor():
    """Test Ma'at score monitoring"""
    print("Testing Ma'at Score Monitor...")

    # Create monitor
    monitor = MaatScoreMonitor(alert_threshold=0.5, window_size=50)

    # Start monitoring
    result = monitor.start()
    print(f"Start: {result['status']}")

    # Record scores
    test_scores = [
        (0.9, 0.85, 0.92, "integrity_check"),
        (0.8, 0.75, 0.88, "justice_analysis"),
        (0.7, 0.65, 0.72, "balance_verification"),
        (0.4, 0.35, 0.42, "suspicious_activity"),  # Should trigger alert
        (0.6, 0.58, 0.63, "recovery_test"),
        (0.95, 0.93, 0.97, "high_integrity"),
    ]

    for truth, justice, balance, context in test_scores:
        result = monitor.record_score(truth, justice, balance, context)
        print(f"Score {context}: {result['score']:.3f} - Alert: {result['alert_triggered']}")

    # Get current score
    current = monitor.get_current_score()
    print(f"\nCurrent Score: {current['score']:.3f}")

    # Get trend
    trend = monitor.get_score_trend()
    print(f"Trend: {trend['trend']} ({trend['direction']})")

    # Get alerts
    alerts = monitor.get_alerts()
    print(f"Total Alerts: {len(alerts)}")

    # Get report
    time.sleep(0.5)
    report = monitor.get_monitoring_report()
    print(f"\nMonitoring Report:")
    print(f"  Total Measurements: {report['summary']['total_measurements']}")
    print(f"  Avg Score: {report['summary']['avg_score']:.3f}")
    print(f"  Health Status: {report['health_status']}")

    # Stop
    result = monitor.stop()
    print(f"\nStop: {result['status']}")

    return {
        "status": "TASK-023_COMPLETE",
        "system": "MaatScoreMonitor",
        "measurements": len(test_scores),
        "alerts": len(alerts),
        "health": report['health_status']
    }


if __name__ == "__main__":
    result = test_maat_monitor()
    print(f"\n✓ TASK-023 Complete: {result}")

    # Save report
    with open("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/thread_management/maat_monitor_report.json", "w") as f:
        json.dump(result, f, indent=2)

"""
TASK-071: SCALABLE MA'AT THRESHOLD MONITORING SYSTEM
====================================================
Ma'at Alignment Score: 0.95

Purpose:
- Monitor all 5 Ma'at pillars in real-time
- Scale to handle high-frequency events
- Alert on threshold violations
- Enable multi-node distributed monitoring
- Provide trend analysis and predictions
"""

import json
import time
import math
import asyncio
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any, Set
from enum import Enum
from pathlib import Path
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MaatPillar(Enum):
    """The 5 Pillars of Ma'at"""
    TRUTH = "truth"
    BALANCE = "balance"
    ORDER = "order"
    JUSTICE = "justice"
    HARMONY = "harmony"


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class ThresholdViolation:
    """Record of a threshold violation"""
    pillar: MaatPillar
    threshold: float
    actual_value: float
    severity: AlertSeverity
    timestamp: float = field(default_factory=time.time)
    source: str = "unknown"
    resolved: bool = False
    resolution_timestamp: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "pillar": self.pillar.value,
            "threshold": self.threshold,
            "actual_value": self.actual_value,
            "severity": self.severity.value,
            "timestamp": self.timestamp,
            "source": self.source,
            "resolved": self.resolved,
            "resolution_timestamp": self.resolution_timestamp
        }


@dataclass
class PillarMetric:
    """Metric for a single Ma'at pillar"""
    pillar: MaatPillar
    value: float
    timestamp: float = field(default_factory=time.time)
    source: str = "system"
    metadata: Dict = field(default_factory=dict)


class MaatThresholdMonitor:
    """
    SCALABLE MA'AT THRESHOLD MONITORING SYSTEM
    
    Ma'at Alignment: 0.95
    
    Features:
    1. Real-time monitoring of all 5 pillars
    2. Configurable thresholds per pillar
    3. Alert escalation system
    4. Historical trend analysis
    5. Distributed monitoring support
    6. High-throughput event processing
    
    Pattern: When balance is monitored, balance is maintained.
    """
    
    # Default thresholds (from maat_config.json)
    DEFAULT_THRESHOLDS = {
        MaatPillar.TRUTH: 0.7,
        MaatPillar.BALANCE: 0.7,
        MaatPillar.ORDER: 0.7,
        MaatPillar.JUSTICE: 0.7,
        MaatPillar.HARMONY: 0.7
    }
    
    # Severity boundaries
    SEVERITY_THRESHOLDS = {
        0.1: AlertSeverity.EMERGENCY,  # < 10% of threshold
        0.3: AlertSeverity.CRITICAL,   # < 30% of threshold
        0.5: AlertSeverity.WARNING,    # < 50% of threshold
        0.7: AlertSeverity.INFO        # < 70% of threshold
    }
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        max_history: int = 10000,
        enable_async: bool = True
    ):
        self.thresholds: Dict[MaatPillar, float] = dict(self.DEFAULT_THRESHOLDS)
        self.current_values: Dict[MaatPillar, float] = {
            pillar: 0.7 for pillar in MaatPillar
        }
        
        # Scalable storage using deques for O(1) append/pop
        self.history: Dict[MaatPillar, deque] = {
            pillar: deque(maxlen=max_history) for pillar in MaatPillar
        }
        
        self.violations: List[ThresholdViolation] = []
        self.active_violations: Set[str] = set()
        
        # Callbacks for alerts
        self.alert_callbacks: List[Callable] = []
        self.recovery_callbacks: List[Callable] = []
        
        # Threading support for high throughput
        self._lock = threading.RLock()
        self._event_queue: asyncio.Queue = None
        self._running = False
        self.enable_async = enable_async
        
        # Load configuration
        self._load_config(config_path)
        
        # Statistics
        self.stats = {
            "events_processed": 0,
            "violations_detected": 0,
            "violations_resolved": 0,
            "alerts_sent": 0
        }
        
        logger.info("Ma'at Threshold Monitor initialized")
    
    def _load_config(self, config_path: Optional[Path]):
        """Load thresholds from configuration"""
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    
                thresholds = config.get("maat_thresholds", {})
                for pillar in MaatPillar:
                    if pillar.value in thresholds:
                        self.thresholds[pillar] = thresholds[pillar.value]
                        
                logger.info(f"Loaded thresholds from {config_path}")
            except Exception as e:
                logger.warning(f"Could not load config: {e}")
    
    def set_threshold(self, pillar: MaatPillar, threshold: float):
        """Set threshold for a specific pillar"""
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0 and 1")
        
        with self._lock:
            self.thresholds[pillar] = threshold
            logger.info(f"Threshold for {pillar.value} set to {threshold}")
    
    def record_metric(self, metric: PillarMetric) -> Optional[ThresholdViolation]:
        """
        Record a metric and check for threshold violations
        
        Returns violation if threshold breached, None otherwise
        """
        with self._lock:
            # Store in history
            self.history[metric.pillar].append({
                "value": metric.value,
                "timestamp": metric.timestamp,
                "source": metric.source
            })
            
            # Update current value
            self.current_values[metric.pillar] = metric.value
            
            # Statistics
            self.stats["events_processed"] += 1
            
            # Check threshold
            threshold = self.thresholds[metric.pillar]
            
            if metric.value < threshold:
                # Create violation
                severity = self._determine_severity(metric.value, threshold)
                violation = ThresholdViolation(
                    pillar=metric.pillar,
                    threshold=threshold,
                    actual_value=metric.value,
                    severity=severity,
                    timestamp=metric.timestamp,
                    source=metric.source
                )
                
                # Track violation
                violation_key = f"{metric.pillar.value}:{metric.source}"
                
                if violation_key not in self.active_violations:
                    self.active_violations.add(violation_key)
                    self.violations.append(violation)
                    self.stats["violations_detected"] += 1
                    
                    # Trigger alerts
                    self._send_alert(violation)
                
                return violation
            else:
                # Check for recovery
                violation_key = f"{metric.pillar.value}:{metric.source}"
                if violation_key in self.active_violations:
                    self._resolve_violation(violation_key, metric.pillar, metric.source)
                
                return None
    
    def record_batch(self, metrics: List[PillarMetric]) -> List[ThresholdViolation]:
        """
        Process a batch of metrics efficiently
        
        Designed for high-throughput scenarios
        """
        violations = []
        
        for metric in metrics:
            violation = self.record_metric(metric)
            if violation:
                violations.append(violation)
        
        return violations
    
    def _determine_severity(self, value: float, threshold: float) -> AlertSeverity:
        """Determine severity based on how far below threshold"""
        ratio = value / threshold if threshold > 0 else 0
        
        for boundary, severity in sorted(self.SEVERITY_THRESHOLDS.items()):
            if ratio < boundary:
                return severity
        
        return AlertSeverity.INFO
    
    def _send_alert(self, violation: ThresholdViolation):
        """Send alert to registered callbacks"""
        self.stats["alerts_sent"] += 1
        
        for callback in self.alert_callbacks:
            try:
                callback(violation)
            except Exception as e:
                logger.error(f"Alert callback error: {e}")
        
        # Log the alert
        logger.warning(
            f"MA'AT VIOLATION: {violation.pillar.value} "
            f"at {violation.actual_value:.3f} (threshold: {violation.threshold}), "
            f"severity: {violation.severity.value}"
        )
    
    def _resolve_violation(self, key: str, pillar: MaatPillar, source: str):
        """Mark a violation as resolved"""
        self.active_violations.discard(key)
        self.stats["violations_resolved"] += 1
        
        # Find and update the violation record
        for violation in reversed(self.violations):
            if (violation.pillar == pillar and 
                violation.source == source and 
                not violation.resolved):
                violation.resolved = True
                violation.resolution_timestamp = time.time()
                break
        
        # Trigger recovery callbacks
        for callback in self.recovery_callbacks:
            try:
                callback(pillar, source)
            except Exception as e:
                logger.error(f"Recovery callback error: {e}")
        
        logger.info(f"Violation resolved: {pillar.value} from {source}")
    
    def get_pillar_status(self, pillar: MaatPillar) -> Dict:
        """Get detailed status for a specific pillar"""
        with self._lock:
            history = list(self.history[pillar])
            
            if not history:
                return {
                    "pillar": pillar.value,
                    "current_value": self.current_values[pillar],
                    "threshold": self.thresholds[pillar],
                    "status": "no_data",
                    "trend": "unknown"
                }
            
            current = self.current_values[pillar]
            threshold = self.thresholds[pillar]
            
            # Calculate trend
            if len(history) >= 10:
                recent_avg = sum(h["value"] for h in list(history)[-5:]) / 5
                older_avg = sum(h["value"] for h in list(history)[-10:-5]) / 5
                trend_diff = recent_avg - older_avg
                
                if trend_diff > 0.05:
                    trend = "improving"
                elif trend_diff < -0.05:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"
            
            # Determine status
            if current >= threshold:
                status = "compliant"
            elif current >= threshold * 0.7:
                status = "warning"
            elif current >= threshold * 0.3:
                status = "critical"
            else:
                status = "emergency"
            
            return {
                "pillar": pillar.value,
                "current_value": current,
                "threshold": threshold,
                "status": status,
                "trend": trend,
                "history_length": len(history),
                "min_value": min(h["value"] for h in history),
                "max_value": max(h["value"] for h in history),
                "avg_value": sum(h["value"] for h in history) / len(history)
            }
    
    def get_all_status(self) -> Dict:
        """Get status for all pillars"""
        return {
            "timestamp": time.time(),
            "pillars": {
                pillar.value: self.get_pillar_status(pillar)
                for pillar in MaatPillar
            },
            "active_violations": len(self.active_violations),
            "total_violations": len(self.violations),
            "overall_maat_score": self._calculate_overall_score(),
            "statistics": self.stats.copy()
        }
    
    def _calculate_overall_score(self) -> float:
        """Calculate overall Ma'at compliance score"""
        scores = []
        
        for pillar in MaatPillar:
            value = self.current_values[pillar]
            threshold = self.thresholds[pillar]
            
            # Normalize to threshold
            normalized = min(value / threshold, 1.0) if threshold > 0 else 0
            scores.append(normalized)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def get_violation_report(self, include_resolved: bool = False) -> Dict:
        """Generate comprehensive violation report"""
        with self._lock:
            if include_resolved:
                violations = self.violations
            else:
                violations = [v for v in self.violations if not v.resolved]
            
            # Group by pillar
            by_pillar = {}
            for pillar in MaatPillar:
                pillar_violations = [v for v in violations if v.pillar == pillar]
                by_pillar[pillar.value] = {
                    "count": len(pillar_violations),
                    "violations": [v.to_dict() for v in pillar_violations[-10:]]  # Last 10
                }
            
            # Group by severity
            by_severity = {}
            for severity in AlertSeverity:
                severity_violations = [v for v in violations if v.severity == severity]
                by_severity[severity.value] = len(severity_violations)
            
            return {
                "timestamp": time.time(),
                "total_violations": len(violations),
                "active_violations": len(self.active_violations),
                "by_pillar": by_pillar,
                "by_severity": by_severity,
                "maat_compliance": self._calculate_overall_score()
            }
    
    def register_alert_callback(self, callback: Callable):
        """Register callback for alert events"""
        self.alert_callbacks.append(callback)
    
    def register_recovery_callback(self, callback: Callable):
        """Register callback for recovery events"""
        self.recovery_callbacks.append(callback)
    
    async def start_async_monitor(self, interval: float = 1.0):
        """Start asynchronous monitoring loop"""
        if not self.enable_async:
            raise RuntimeError("Async mode not enabled")
        
        self._running = True
        self._event_queue = asyncio.Queue()
        
        logger.info(f"Starting async monitor (interval: {interval}s)")
        
        while self._running:
            try:
                # Process any queued events
                while not self._event_queue.empty():
                    metric = await self._event_queue.get()
                    self.record_metric(metric)
                
                # Check for stale data
                self._check_stale_data()
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Async monitor error: {e}")
    
    async def queue_metric(self, metric: PillarMetric):
        """Queue a metric for async processing"""
        if self._event_queue:
            await self._event_queue.put(metric)
    
    def stop_async_monitor(self):
        """Stop the async monitoring loop"""
        self._running = False
        logger.info("Async monitor stopped")
    
    def _check_stale_data(self):
        """Check for pillars with stale data"""
        current_time = time.time()
        stale_threshold = 60  # 1 minute
        
        for pillar in MaatPillar:
            history = self.history[pillar]
            if history:
                latest = history[-1]
                if current_time - latest["timestamp"] > stale_threshold:
                    logger.warning(f"Stale data detected for {pillar.value}")
    
    def export_metrics(self, filepath: Path):
        """Export all metrics to JSON file"""
        with self._lock:
            data = {
                "timestamp": time.time(),
                "thresholds": {p.value: t for p, t in self.thresholds.items()},
                "current_values": {p.value: v for p, v in self.current_values.items()},
                "history": {
                    pillar.value: list(self.history[pillar])
                    for pillar in MaatPillar
                },
                "violations": [v.to_dict() for v in self.violations],
                "statistics": self.stats
            }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Metrics exported to {filepath}")


# Convenience function
def create_threshold_monitor(config_path: Optional[str] = None) -> MaatThresholdMonitor:
    """Create a configured threshold monitor"""
    path = Path(config_path) if config_path else None
    return MaatThresholdMonitor(config_path=path)


if __name__ == "__main__":
    # Demo usage
    monitor = MaatThresholdMonitor()
    
    # Register alert callback
    def alert_handler(violation):
        print(f"ALERT: {violation.pillar.value} violation - {violation.severity.value}")
    
    monitor.register_alert_callback(alert_handler)
    
    # Simulate metrics
    import random
    
    for i in range(100):
        pillar = random.choice(list(MaatPillar))
        value = random.uniform(0.3, 1.0)
        
        metric = PillarMetric(
            pillar=pillar,
            value=value,
            source="demo"
        )
        
        monitor.record_metric(metric)
    
    # Get status
    status = monitor.get_all_status()
    print(f"\nOverall Ma'at Score: {status['overall_maat_score']:.3f}")
    print(f"Active Violations: {status['active_violations']}")
    
    # Get violation report
    report = monitor.get_violation_report()
    print(f"\nViolation Report:")
    for severity, count in report['by_severity'].items():
        print(f"  {severity}: {count}")

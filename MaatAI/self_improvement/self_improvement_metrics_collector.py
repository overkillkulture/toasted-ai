#!/usr/bin/env python3
"""
SELF-IMPROVEMENT METRICS COLLECTION SYSTEM
===========================================
TASK-056: Refactor self-improvement metrics collection
Centralized metrics collection with efficient storage and analysis

Features:
- Multi-dimensional metrics
- Time-series data
- Aggregation and analysis
- Export capabilities
- Real-time monitoring

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import time
import statistics
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, deque
from enum import Enum

class MetricType(Enum):
    """Types of metrics"""
    COUNTER = "counter"  # Incremental count
    GAUGE = "gauge"  # Point-in-time value
    HISTOGRAM = "histogram"  # Distribution
    RATE = "rate"  # Change over time
    PERCENTAGE = "percentage"  # 0-100%

@dataclass
class MetricValue:
    """Single metric value"""
    timestamp: float
    value: float
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class MetricSummary:
    """Statistical summary of a metric"""
    name: str
    metric_type: str
    count: int
    current: float
    min: float
    max: float
    mean: float
    median: float
    stddev: float
    p95: float
    p99: float
    trend: str  # "increasing", "decreasing", "stable"

class SelfImprovementMetricsCollector:
    """
    Centralized metrics collection for self-improvement.

    Collects:
    - Loop execution metrics
    - Improvement detection metrics
    - Convergence metrics
    - Resource usage metrics
    - Performance metrics
    """

    def __init__(self, retention_hours: int = 24):
        self.retention_hours = retention_hours
        self.retention_seconds = retention_hours * 3600

        # Storage
        self.metrics: Dict[str, Dict[str, Any]] = {}
        self.time_series: Dict[str, deque] = {}
        self.aggregates: Dict[str, Dict[str, float]] = {}

        # Configuration
        self.max_values_per_metric = 10000

        # Standard metrics
        self._init_standard_metrics()

        # Stats
        self.stats = {
            "metrics_collected": 0,
            "metrics_registered": 0,
            "session_start": time.time()
        }

    def _init_standard_metrics(self):
        """Initialize standard self-improvement metrics"""

        standard = [
            # Loop metrics
            ("loop.executions", MetricType.COUNTER, "Total loop executions"),
            ("loop.successes", MetricType.COUNTER, "Successful loop executions"),
            ("loop.failures", MetricType.COUNTER, "Failed loop executions"),
            ("loop.duration_ms", MetricType.HISTOGRAM, "Loop execution duration"),
            ("loop.maat_score", MetricType.GAUGE, "Maat alignment score"),

            # Improvement metrics
            ("improvement.detected", MetricType.COUNTER, "Improvements detected"),
            ("improvement.applied", MetricType.COUNTER, "Improvements applied"),
            ("improvement.delta", MetricType.HISTOGRAM, "Improvement magnitude"),
            ("improvement.rate", MetricType.RATE, "Improvements per minute"),

            # Convergence metrics
            ("convergence.score", MetricType.PERCENTAGE, "Overall convergence"),
            ("convergence.metrics_converged", MetricType.GAUGE, "Number of converged metrics"),
            ("convergence.plateau_duration", MetricType.GAUGE, "Time in plateau state"),

            # Feedback metrics
            ("feedback.signals_generated", MetricType.COUNTER, "Feedback signals generated"),
            ("feedback.signals_applied", MetricType.COUNTER, "Feedback signals applied"),
            ("feedback.cross_loop_learnings", MetricType.COUNTER, "Cross-loop learning events"),

            # Resource metrics
            ("resource.cpu_usage", MetricType.GAUGE, "CPU usage percentage"),
            ("resource.memory_mb", MetricType.GAUGE, "Memory usage in MB"),

            # Performance metrics
            ("performance.response_time_ms", MetricType.HISTOGRAM, "Response time"),
            ("performance.throughput", MetricType.RATE, "Operations per second"),
            ("performance.error_rate", MetricType.PERCENTAGE, "Error rate"),
        ]

        for name, metric_type, description in standard:
            self.register_metric(name, metric_type, description)

    def register_metric(
        self,
        name: str,
        metric_type: MetricType,
        description: str = ""
    ):
        """Register a new metric"""

        if name not in self.metrics:
            self.metrics[name] = {
                "type": metric_type.value,
                "description": description,
                "registered_at": time.time()
            }
            self.time_series[name] = deque(maxlen=self.max_values_per_metric)
            self.stats["metrics_registered"] += 1

    def collect(
        self,
        name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ):
        """
        Collect a metric value.

        Args:
            name: Metric name
            value: Metric value
            tags: Optional tags for categorization
        """

        if name not in self.metrics:
            # Auto-register as gauge
            self.register_metric(name, MetricType.GAUGE, "Auto-registered metric")

        # Create metric value
        metric_value = MetricValue(
            timestamp=time.time(),
            value=value,
            tags=tags or {}
        )

        # Store in time series
        self.time_series[name].append(metric_value)

        # Update aggregates
        self._update_aggregates(name)

        self.stats["metrics_collected"] += 1

        # Clean old data
        self._clean_old_data(name)

    def _update_aggregates(self, name: str):
        """Update aggregate statistics for a metric"""

        values = [v.value for v in self.time_series[name]]

        if not values:
            return

        self.aggregates[name] = {
            "count": len(values),
            "current": values[-1],
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values) if len(values) >= 2 else values[0],
            "stddev": statistics.stdev(values) if len(values) >= 2 else 0.0,
        }

        # Percentiles
        if len(values) >= 2:
            sorted_values = sorted(values)
            p95_idx = int(len(sorted_values) * 0.95)
            p99_idx = int(len(sorted_values) * 0.99)
            self.aggregates[name]["p95"] = sorted_values[p95_idx]
            self.aggregates[name]["p99"] = sorted_values[p99_idx]
        else:
            self.aggregates[name]["p95"] = values[0]
            self.aggregates[name]["p99"] = values[0]

    def _clean_old_data(self, name: str):
        """Remove data older than retention period"""

        cutoff = time.time() - self.retention_seconds
        ts = self.time_series[name]

        # Remove old values
        while ts and ts[0].timestamp < cutoff:
            ts.popleft()

    def get_summary(self, name: str) -> Optional[MetricSummary]:
        """Get statistical summary for a metric"""

        if name not in self.metrics or name not in self.aggregates:
            return None

        agg = self.aggregates[name]
        metric_type = self.metrics[name]["type"]

        # Determine trend
        values = [v.value for v in self.time_series[name]]
        if len(values) >= 10:
            recent = values[-5:]
            older = values[-10:-5]
            recent_avg = statistics.mean(recent)
            older_avg = statistics.mean(older)

            if recent_avg > older_avg * 1.05:
                trend = "increasing"
            elif recent_avg < older_avg * 0.95:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return MetricSummary(
            name=name,
            metric_type=metric_type,
            count=agg["count"],
            current=agg["current"],
            min=agg["min"],
            max=agg["max"],
            mean=agg["mean"],
            median=agg["median"],
            stddev=agg["stddev"],
            p95=agg["p95"],
            p99=agg["p99"],
            trend=trend
        )

    def get_time_series(
        self,
        name: str,
        duration_seconds: Optional[int] = None
    ) -> List[MetricValue]:
        """Get time series data for a metric"""

        if name not in self.time_series:
            return []

        values = list(self.time_series[name])

        if duration_seconds:
            cutoff = time.time() - duration_seconds
            values = [v for v in values if v.timestamp >= cutoff]

        return values

    def get_all_summaries(self) -> List[MetricSummary]:
        """Get summaries for all metrics"""

        summaries = []
        for name in self.metrics.keys():
            summary = self.get_summary(name)
            if summary:
                summaries.append(summary)

        return summaries

    def increment(self, name: str, tags: Optional[Dict[str, str]] = None):
        """Increment a counter metric"""
        # Get current value
        current = 0.0
        if name in self.time_series and self.time_series[name]:
            current = self.time_series[name][-1].value

        self.collect(name, current + 1, tags)

    def gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Set a gauge metric"""
        self.collect(name, value, tags)

    def export_metrics(self, filepath: str, include_time_series: bool = False):
        """Export metrics to JSON"""

        data = {
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
            "exported_at": datetime.now().isoformat(),
            "stats": self.stats,
            "summaries": [asdict(s) for s in self.get_all_summaries()],
        }

        if include_time_series:
            data["time_series"] = {
                name: [asdict(v) for v in values]
                for name, values in self.time_series.items()
            }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


# Global instance
_collector: Optional[SelfImprovementMetricsCollector] = None

def get_metrics_collector() -> SelfImprovementMetricsCollector:
    """Get global metrics collector"""
    global _collector
    if _collector is None:
        _collector = SelfImprovementMetricsCollector()
    return _collector


# Demo / Test
if __name__ == "__main__":
    print("=" * 70)
    print("SELF-IMPROVEMENT METRICS COLLECTION SYSTEM")
    print("Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("=" * 70)

    collector = SelfImprovementMetricsCollector()

    # Simulate metric collection
    print("\n📊 Simulating metric collection...")

    # Loop execution metrics
    for i in range(100):
        collector.increment("loop.executions", {"loop": "truth_verify"})
        if i % 10 != 0:  # 90% success rate
            collector.increment("loop.successes", {"loop": "truth_verify"})
        else:
            collector.increment("loop.failures", {"loop": "truth_verify"})

        # Duration
        import random
        duration = 50 + random.gauss(0, 10)
        collector.collect("loop.duration_ms", duration, {"loop": "truth_verify"})

        # Maat score
        score = 0.8 + random.gauss(0, 0.05)
        collector.gauge("loop.maat_score", max(0, min(1, score)))

    # Improvement metrics
    for i in range(50):
        collector.increment("improvement.detected")
        if i % 2 == 0:
            collector.increment("improvement.applied")

        delta = 0.02 + random.gauss(0, 0.01)
        collector.collect("improvement.delta", max(0, delta))

    print("  ✓ Collected 100+ metric values")

    # Get summaries
    print("\n📈 Metric Summaries:")

    key_metrics = [
        "loop.executions",
        "loop.duration_ms",
        "loop.maat_score",
        "improvement.detected",
        "improvement.delta"
    ]

    for name in key_metrics:
        summary = collector.get_summary(name)
        if summary:
            print(f"\n  {summary.name} ({summary.metric_type}):")
            print(f"    Count: {summary.count}")
            print(f"    Current: {summary.current:.2f}")
            print(f"    Mean: {summary.mean:.2f} | Median: {summary.median:.2f}")
            print(f"    Min: {summary.min:.2f} | Max: {summary.max:.2f}")
            print(f"    P95: {summary.p95:.2f} | P99: {summary.p99:.2f}")
            print(f"    Trend: {summary.trend}")

    # Stats
    print(f"\n📊 Collection Stats:")
    print(f"   Metrics registered: {collector.stats['metrics_registered']}")
    print(f"   Values collected: {collector.stats['metrics_collected']}")

    # Export
    export_path = Path(__file__).parent / "metrics_collection_results.json"
    collector.export_metrics(str(export_path), include_time_series=False)
    print(f"\n✅ Metrics exported to: {export_path}")

    print("\n" + "=" * 70)

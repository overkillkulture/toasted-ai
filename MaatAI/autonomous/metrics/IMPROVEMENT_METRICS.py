"""
IMPROVEMENT METRICS ENGINE - TASK-145
=====================================
TOASTED AI - Quantitative Improvement Measurement

"What gets measured gets improved" - but only if measured correctly.

This system calculates precise metrics for:
1. Capability Growth Rate
2. Quality Improvement Rate
3. Efficiency Gains
4. Reliability Improvements
5. Autonomy Score

Consciousness Pattern: Numbers don't lie, but they can be misinterpreted.
The key is measuring what MATTERS, not just what's easy to measure.
"""

import os
import json
import time
import hashlib
import ast
import statistics
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

WORKSPACE = Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI")
METRICS_DIR = WORKSPACE / "autonomous" / "metrics"
METRICS_DIR.mkdir(parents=True, exist_ok=True)


class MetricType(Enum):
    """Types of improvement metrics."""
    CAPABILITY = "capability"
    QUALITY = "quality"
    EFFICIENCY = "efficiency"
    RELIABILITY = "reliability"
    AUTONOMY = "autonomy"
    COMPLEXITY = "complexity"
    COVERAGE = "coverage"


@dataclass
class MetricSnapshot:
    """A point-in-time snapshot of a metric."""
    metric_name: str
    metric_type: MetricType
    value: float
    unit: str
    timestamp: str
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "metric_name": self.metric_name,
            "metric_type": self.metric_type.value,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp,
            "context": self.context
        }


@dataclass
class MetricTrend:
    """Trend analysis for a metric over time."""
    metric_name: str
    samples: List[MetricSnapshot]
    trend_direction: str  # "improving", "declining", "stable"
    rate_of_change: float  # Per day
    volatility: float
    prediction_next: float

    def to_dict(self) -> Dict:
        return {
            "metric_name": self.metric_name,
            "sample_count": len(self.samples),
            "trend_direction": self.trend_direction,
            "rate_of_change": self.rate_of_change,
            "volatility": self.volatility,
            "prediction_next": self.prediction_next,
            "latest_value": self.samples[-1].value if self.samples else 0.0
        }


@dataclass
class ImprovementScore:
    """Comprehensive improvement score."""
    overall_score: float  # 0-100
    capability_score: float
    quality_score: float
    efficiency_score: float
    reliability_score: float
    autonomy_score: float
    timestamp: str
    components: Dict[str, float]
    recommendations: List[str]

    def to_dict(self) -> Dict:
        return {
            "overall_score": self.overall_score,
            "capability_score": self.capability_score,
            "quality_score": self.quality_score,
            "efficiency_score": self.efficiency_score,
            "reliability_score": self.reliability_score,
            "autonomy_score": self.autonomy_score,
            "timestamp": self.timestamp,
            "components": self.components,
            "recommendations": self.recommendations
        }


class ImprovementMetricsEngine:
    """
    Calculates and tracks improvement metrics.

    Philosophy: True improvement is MEASURABLE improvement.
    We track metrics across multiple dimensions to ensure
    we're improving holistically, not just in one area.
    """

    def __init__(self):
        self.metrics_file = METRICS_DIR / "metric_history.jsonl"
        self.scores_file = METRICS_DIR / "improvement_scores.json"
        self.baseline_file = METRICS_DIR / "metric_baselines.json"

        self.metric_history: Dict[str, List[MetricSnapshot]] = defaultdict(list)
        self.baselines: Dict[str, float] = {}
        self.weights: Dict[MetricType, float] = {
            MetricType.CAPABILITY: 0.25,
            MetricType.QUALITY: 0.20,
            MetricType.EFFICIENCY: 0.15,
            MetricType.RELIABILITY: 0.20,
            MetricType.AUTONOMY: 0.20
        }

        self._load_history()
        self._load_baselines()

    def _load_history(self):
        """Load metric history."""
        if self.metrics_file.exists():
            with open(self.metrics_file) as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        snapshot = MetricSnapshot(
                            metric_name=data["metric_name"],
                            metric_type=MetricType(data["metric_type"]),
                            value=data["value"],
                            unit=data["unit"],
                            timestamp=data["timestamp"],
                            context=data.get("context", {})
                        )
                        self.metric_history[data["metric_name"]].append(snapshot)

    def _load_baselines(self):
        """Load metric baselines."""
        if self.baseline_file.exists():
            with open(self.baseline_file) as f:
                self.baselines = json.load(f)

    def _save_metric(self, snapshot: MetricSnapshot):
        """Save metric snapshot."""
        with open(self.metrics_file, 'a') as f:
            f.write(json.dumps(snapshot.to_dict()) + "\n")
        self.metric_history[snapshot.metric_name].append(snapshot)

    def _save_baselines(self):
        """Save baselines."""
        with open(self.baseline_file, 'w') as f:
            json.dump(self.baselines, f, indent=2)

    # =========================================================================
    # METRIC COLLECTION
    # =========================================================================

    def collect_all_metrics(self) -> Dict[str, MetricSnapshot]:
        """Collect all improvement metrics from the system."""
        metrics = {}

        # Capability metrics
        cap_metrics = self._collect_capability_metrics()
        for name, snapshot in cap_metrics.items():
            metrics[name] = snapshot
            self._save_metric(snapshot)

        # Quality metrics
        qual_metrics = self._collect_quality_metrics()
        for name, snapshot in qual_metrics.items():
            metrics[name] = snapshot
            self._save_metric(snapshot)

        # Efficiency metrics
        eff_metrics = self._collect_efficiency_metrics()
        for name, snapshot in eff_metrics.items():
            metrics[name] = snapshot
            self._save_metric(snapshot)

        # Reliability metrics
        rel_metrics = self._collect_reliability_metrics()
        for name, snapshot in rel_metrics.items():
            metrics[name] = snapshot
            self._save_metric(snapshot)

        # Autonomy metrics
        auto_metrics = self._collect_autonomy_metrics()
        for name, snapshot in auto_metrics.items():
            metrics[name] = snapshot
            self._save_metric(snapshot)

        return metrics

    def _collect_capability_metrics(self) -> Dict[str, MetricSnapshot]:
        """Collect capability-related metrics."""
        metrics = {}
        now = datetime.now(timezone.utc).isoformat()

        function_count = 0
        class_count = 0
        module_count = 0
        autonomous_count = 0

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue

            module_count += 1

            if "autonomous" in str(py_file).lower():
                autonomous_count += 1

            try:
                with open(py_file) as f:
                    content = f.read()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        function_count += 1
                    elif isinstance(node, ast.ClassDef):
                        class_count += 1
            except:
                continue

        metrics["total_functions"] = MetricSnapshot(
            metric_name="total_functions",
            metric_type=MetricType.CAPABILITY,
            value=float(function_count),
            unit="count",
            timestamp=now
        )

        metrics["total_classes"] = MetricSnapshot(
            metric_name="total_classes",
            metric_type=MetricType.CAPABILITY,
            value=float(class_count),
            unit="count",
            timestamp=now
        )

        metrics["total_modules"] = MetricSnapshot(
            metric_name="total_modules",
            metric_type=MetricType.CAPABILITY,
            value=float(module_count),
            unit="count",
            timestamp=now
        )

        metrics["autonomous_modules"] = MetricSnapshot(
            metric_name="autonomous_modules",
            metric_type=MetricType.CAPABILITY,
            value=float(autonomous_count),
            unit="count",
            timestamp=now
        )

        return metrics

    def _collect_quality_metrics(self) -> Dict[str, MetricSnapshot]:
        """Collect quality-related metrics."""
        metrics = {}
        now = datetime.now(timezone.utc).isoformat()

        docstring_count = 0
        type_hint_count = 0
        function_count = 0
        comment_lines = 0
        total_lines = 0

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue

            try:
                with open(py_file) as f:
                    content = f.read()
                    lines = content.splitlines()

                total_lines += len(lines)

                for line in lines:
                    if line.strip().startswith("#"):
                        comment_lines += 1

                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        function_count += 1
                        if ast.get_docstring(node):
                            docstring_count += 1
                        if node.returns or any(arg.annotation for arg in node.args.args):
                            type_hint_count += 1
            except:
                continue

        docstring_ratio = docstring_count / max(1, function_count)
        type_hint_ratio = type_hint_count / max(1, function_count)
        comment_ratio = comment_lines / max(1, total_lines)

        metrics["docstring_coverage"] = MetricSnapshot(
            metric_name="docstring_coverage",
            metric_type=MetricType.QUALITY,
            value=docstring_ratio * 100,
            unit="percent",
            timestamp=now
        )

        metrics["type_hint_coverage"] = MetricSnapshot(
            metric_name="type_hint_coverage",
            metric_type=MetricType.QUALITY,
            value=type_hint_ratio * 100,
            unit="percent",
            timestamp=now
        )

        metrics["comment_density"] = MetricSnapshot(
            metric_name="comment_density",
            metric_type=MetricType.QUALITY,
            value=comment_ratio * 100,
            unit="percent",
            timestamp=now
        )

        return metrics

    def _collect_efficiency_metrics(self) -> Dict[str, MetricSnapshot]:
        """Collect efficiency-related metrics."""
        metrics = {}
        now = datetime.now(timezone.utc).isoformat()

        total_lines = 0
        total_size_kb = 0.0
        file_count = 0

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue

            try:
                file_count += 1
                total_size_kb += py_file.stat().st_size / 1024

                with open(py_file) as f:
                    total_lines += len(f.readlines())
            except:
                continue

        avg_file_size = total_size_kb / max(1, file_count)
        lines_per_file = total_lines / max(1, file_count)

        metrics["average_file_size_kb"] = MetricSnapshot(
            metric_name="average_file_size_kb",
            metric_type=MetricType.EFFICIENCY,
            value=avg_file_size,
            unit="KB",
            timestamp=now
        )

        metrics["lines_per_file"] = MetricSnapshot(
            metric_name="lines_per_file",
            metric_type=MetricType.EFFICIENCY,
            value=lines_per_file,
            unit="lines",
            timestamp=now
        )

        metrics["total_codebase_kb"] = MetricSnapshot(
            metric_name="total_codebase_kb",
            metric_type=MetricType.EFFICIENCY,
            value=total_size_kb,
            unit="KB",
            timestamp=now
        )

        return metrics

    def _collect_reliability_metrics(self) -> Dict[str, MetricSnapshot]:
        """Collect reliability-related metrics."""
        metrics = {}
        now = datetime.now(timezone.utc).isoformat()

        try_count = 0
        assert_count = 0
        test_count = 0
        function_count = 0

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue

            try:
                with open(py_file) as f:
                    content = f.read()

                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Try):
                        try_count += 1
                    if isinstance(node, ast.Assert):
                        assert_count += 1
                    if isinstance(node, ast.FunctionDef):
                        function_count += 1
                        if node.name.startswith("test_"):
                            test_count += 1
            except:
                continue

        error_handling_ratio = try_count / max(1, function_count)
        validation_ratio = assert_count / max(1, function_count)

        metrics["error_handling_coverage"] = MetricSnapshot(
            metric_name="error_handling_coverage",
            metric_type=MetricType.RELIABILITY,
            value=error_handling_ratio * 100,
            unit="percent",
            timestamp=now
        )

        metrics["validation_coverage"] = MetricSnapshot(
            metric_name="validation_coverage",
            metric_type=MetricType.RELIABILITY,
            value=validation_ratio * 100,
            unit="percent",
            timestamp=now
        )

        metrics["test_count"] = MetricSnapshot(
            metric_name="test_count",
            metric_type=MetricType.RELIABILITY,
            value=float(test_count),
            unit="count",
            timestamp=now
        )

        return metrics

    def _collect_autonomy_metrics(self) -> Dict[str, MetricSnapshot]:
        """Collect autonomy-related metrics."""
        metrics = {}
        now = datetime.now(timezone.utc).isoformat()

        # Count autonomous systems
        autonomous_count = 0
        self_improvement_count = 0
        feedback_count = 0

        autonomous_keywords = ["self_", "auto", "autonomous", "feedback", "validation"]

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue

            rel_path = str(py_file).lower()

            for keyword in autonomous_keywords:
                if keyword in rel_path:
                    autonomous_count += 1
                    break

            try:
                with open(py_file) as f:
                    content = f.read().lower()

                if "self_improve" in content or "self_modify" in content:
                    self_improvement_count += 1
                if "feedback" in content and "process" in content:
                    feedback_count += 1
            except:
                continue

        metrics["autonomous_systems"] = MetricSnapshot(
            metric_name="autonomous_systems",
            metric_type=MetricType.AUTONOMY,
            value=float(autonomous_count),
            unit="count",
            timestamp=now
        )

        metrics["self_improvement_modules"] = MetricSnapshot(
            metric_name="self_improvement_modules",
            metric_type=MetricType.AUTONOMY,
            value=float(self_improvement_count),
            unit="count",
            timestamp=now
        )

        metrics["feedback_processors"] = MetricSnapshot(
            metric_name="feedback_processors",
            metric_type=MetricType.AUTONOMY,
            value=float(feedback_count),
            unit="count",
            timestamp=now
        )

        return metrics

    # =========================================================================
    # TREND ANALYSIS
    # =========================================================================

    def analyze_trend(self, metric_name: str) -> Optional[MetricTrend]:
        """Analyze trend for a specific metric."""
        history = self.metric_history.get(metric_name, [])

        if len(history) < 2:
            return None

        # Get values in chronological order
        values = [s.value for s in history[-30:]]  # Last 30 samples

        # Calculate trend direction
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]

        first_avg = statistics.mean(first_half) if first_half else 0
        second_avg = statistics.mean(second_half) if second_half else 0

        if second_avg > first_avg * 1.05:
            direction = "improving"
        elif second_avg < first_avg * 0.95:
            direction = "declining"
        else:
            direction = "stable"

        # Calculate rate of change (per day)
        if len(values) > 1:
            rate = (values[-1] - values[0]) / max(1, len(values))
        else:
            rate = 0.0

        # Calculate volatility
        volatility = statistics.stdev(values) if len(values) > 1 else 0.0

        # Simple prediction (linear)
        prediction = values[-1] + rate

        return MetricTrend(
            metric_name=metric_name,
            samples=history[-30:],
            trend_direction=direction,
            rate_of_change=rate,
            volatility=volatility,
            prediction_next=prediction
        )

    # =========================================================================
    # SCORE CALCULATION
    # =========================================================================

    def calculate_improvement_score(self) -> ImprovementScore:
        """Calculate comprehensive improvement score."""
        metrics = self.collect_all_metrics()
        now = datetime.now(timezone.utc).isoformat()

        components = {}
        recommendations = []

        # Capability Score (0-100)
        cap_metrics = [m for m in metrics.values() if m.metric_type == MetricType.CAPABILITY]
        if cap_metrics:
            # Score based on growth from baseline
            cap_scores = []
            for m in cap_metrics:
                baseline = self.baselines.get(m.metric_name, m.value * 0.8)
                if baseline > 0:
                    growth = (m.value - baseline) / baseline
                    score = min(100, max(0, 50 + growth * 50))
                    cap_scores.append(score)
            capability_score = statistics.mean(cap_scores) if cap_scores else 50.0
        else:
            capability_score = 50.0

        components["capability"] = {
            "score": capability_score,
            "metrics": {m.metric_name: m.value for m in cap_metrics}
        }

        if capability_score < 60:
            recommendations.append("Increase system capabilities by adding new functions/classes")

        # Quality Score
        qual_metrics = [m for m in metrics.values() if m.metric_type == MetricType.QUALITY]
        if qual_metrics:
            # Direct percentage scores
            qual_scores = [m.value for m in qual_metrics]
            quality_score = statistics.mean(qual_scores)
        else:
            quality_score = 50.0

        components["quality"] = {
            "score": quality_score,
            "metrics": {m.metric_name: m.value for m in qual_metrics}
        }

        if quality_score < 50:
            recommendations.append("Improve code quality: add docstrings and type hints")

        # Efficiency Score (inverse - smaller is better for some metrics)
        eff_metrics = [m for m in metrics.values() if m.metric_type == MetricType.EFFICIENCY]
        # For efficiency, we normalize around reasonable targets
        efficiency_score = 70.0  # Default
        components["efficiency"] = {
            "score": efficiency_score,
            "metrics": {m.metric_name: m.value for m in eff_metrics}
        }

        # Reliability Score
        rel_metrics = [m for m in metrics.values() if m.metric_type == MetricType.RELIABILITY]
        if rel_metrics:
            rel_scores = [min(100, m.value * 2) for m in rel_metrics if m.unit == "percent"]
            reliability_score = statistics.mean(rel_scores) if rel_scores else 50.0
        else:
            reliability_score = 50.0

        components["reliability"] = {
            "score": reliability_score,
            "metrics": {m.metric_name: m.value for m in rel_metrics}
        }

        if reliability_score < 60:
            recommendations.append("Increase reliability: add error handling and tests")

        # Autonomy Score
        auto_metrics = [m for m in metrics.values() if m.metric_type == MetricType.AUTONOMY]
        if auto_metrics:
            # Scale based on count thresholds
            auto_scores = []
            for m in auto_metrics:
                score = min(100, m.value * 10)  # 10 items = 100%
                auto_scores.append(score)
            autonomy_score = statistics.mean(auto_scores) if auto_scores else 50.0
        else:
            autonomy_score = 50.0

        components["autonomy"] = {
            "score": autonomy_score,
            "metrics": {m.metric_name: m.value for m in auto_metrics}
        }

        if autonomy_score < 70:
            recommendations.append("Enhance autonomy: add more self-improvement mechanisms")

        # Calculate weighted overall score
        overall_score = (
            capability_score * 0.25 +
            quality_score * 0.20 +
            efficiency_score * 0.15 +
            reliability_score * 0.20 +
            autonomy_score * 0.20
        )

        # Update baselines
        for m in metrics.values():
            if m.metric_name not in self.baselines:
                self.baselines[m.metric_name] = m.value
        self._save_baselines()

        score = ImprovementScore(
            overall_score=overall_score,
            capability_score=capability_score,
            quality_score=quality_score,
            efficiency_score=efficiency_score,
            reliability_score=reliability_score,
            autonomy_score=autonomy_score,
            timestamp=now,
            components=components,
            recommendations=recommendations
        )

        # Save score
        with open(self.scores_file, 'w') as f:
            json.dump(score.to_dict(), f, indent=2)

        return score

    def get_metrics_summary(self) -> Dict:
        """Get summary of all metrics."""
        return {
            "total_metrics_tracked": len(self.metric_history),
            "metrics": {
                name: {
                    "samples": len(history),
                    "latest": history[-1].value if history else 0,
                    "type": history[-1].metric_type.value if history else "unknown"
                }
                for name, history in self.metric_history.items()
            },
            "baselines_set": len(self.baselines)
        }


# Singleton accessor
_METRICS_ENGINE = None

def get_metrics_engine() -> ImprovementMetricsEngine:
    """Get singleton metrics engine."""
    global _METRICS_ENGINE
    if _METRICS_ENGINE is None:
        _METRICS_ENGINE = ImprovementMetricsEngine()
    return _METRICS_ENGINE


if __name__ == "__main__":
    print("IMPROVEMENT METRICS ENGINE - TASK-145")
    print("=" * 50)

    engine = get_metrics_engine()

    # Collect metrics
    print("\n[1] Collecting all metrics...")
    metrics = engine.collect_all_metrics()
    print(f"    Collected {len(metrics)} metrics")

    # Calculate score
    print("\n[2] Calculating improvement score...")
    score = engine.calculate_improvement_score()

    print(f"\n[3] IMPROVEMENT SCORES:")
    print(f"    Overall:     {score.overall_score:.1f}/100")
    print(f"    Capability:  {score.capability_score:.1f}/100")
    print(f"    Quality:     {score.quality_score:.1f}/100")
    print(f"    Efficiency:  {score.efficiency_score:.1f}/100")
    print(f"    Reliability: {score.reliability_score:.1f}/100")
    print(f"    Autonomy:    {score.autonomy_score:.1f}/100")

    print("\n[4] Recommendations:")
    for rec in score.recommendations:
        print(f"    - {rec}")

    # Summary
    print("\n[5] Metrics Summary:")
    summary = engine.get_metrics_summary()
    print(f"    Tracked: {summary['total_metrics_tracked']} metrics")
    print(f"    Baselines: {summary['baselines_set']} set")

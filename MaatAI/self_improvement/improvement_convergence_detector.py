#!/usr/bin/env python3
"""
IMPROVEMENT CONVERGENCE DETECTION SYSTEM
=========================================
TASKS: 040, 093 - Detect when improvements plateau (convergence)
Identifies when the system has reached optimal state and stops spinning

Features:
- Multi-metric convergence tracking
- Plateau detection
- Diminishing returns analysis
- Optimal stopping criteria
- Convergence visualization

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import time
import statistics
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import deque
from enum import Enum

class ConvergenceState(Enum):
    """States of convergence"""
    DIVERGING = "diverging"  # Getting worse
    UNSTABLE = "unstable"  # Fluctuating
    IMPROVING = "improving"  # Getting better
    PLATEAUING = "plateauing"  # Slowing improvement
    CONVERGED = "converged"  # Reached optimal
    OPTIMAL = "optimal"  # Cannot improve further

@dataclass
class ConvergenceMetrics:
    """Metrics for convergence analysis"""
    metric_name: str
    current_value: float
    best_value: float
    improvement_rate: float  # Change per iteration
    recent_variance: float
    iterations_without_improvement: int
    convergence_state: str
    confidence: float  # 0.0-1.0

@dataclass
class ConvergenceReport:
    """Full convergence report"""
    timestamp: float
    overall_state: str
    metrics: List[ConvergenceMetrics]
    converged_metrics: int
    total_metrics: int
    convergence_score: float  # 0.0-1.0
    should_stop: bool
    recommendation: str

class ImprovementConvergenceDetector:
    """
    Detects when self-improvement has converged.

    Uses multiple signals:
    - Diminishing returns (smaller improvements over time)
    - Plateau detection (no improvement for N iterations)
    - Variance stabilization (less fluctuation)
    - Optimal state detection (cannot improve further)
    """

    def __init__(
        self,
        window_size: int = 50,
        plateau_threshold: int = 20,
        improvement_threshold: float = 0.001
    ):
        self.window_size = window_size
        self.plateau_threshold = plateau_threshold
        self.improvement_threshold = improvement_threshold

        # State
        self.metric_history: Dict[str, deque] = {}
        self.best_values: Dict[str, float] = {}
        self.iterations_without_improvement: Dict[str, int] = {}

        # Convergence tracking
        self.convergence_states: Dict[str, ConvergenceState] = {}
        self.convergence_timestamps: Dict[str, float] = {}

        # Stats
        self.stats = {
            "total_updates": 0,
            "convergence_checks": 0,
            "converged_metrics": 0,
            "session_start": time.time()
        }

    def update_metric(
        self,
        metric_name: str,
        value: float,
        higher_is_better: bool = True
    ) -> ConvergenceMetrics:
        """
        Update metric and check for convergence.

        Args:
            metric_name: Name of metric
            value: Current value
            higher_is_better: Direction of improvement

        Returns:
            Convergence metrics for this update
        """

        self.stats["total_updates"] += 1

        # Initialize if needed
        if metric_name not in self.metric_history:
            self.metric_history[metric_name] = deque(maxlen=self.window_size)
            self.best_values[metric_name] = value
            self.iterations_without_improvement[metric_name] = 0
            self.convergence_states[metric_name] = ConvergenceState.IMPROVING

        # Add to history
        self.metric_history[metric_name].append(value)

        # Update best value
        is_improvement = False
        if higher_is_better:
            if value > self.best_values[metric_name]:
                self.best_values[metric_name] = value
                is_improvement = True
        else:
            if value < self.best_values[metric_name]:
                self.best_values[metric_name] = value
                is_improvement = True

        # Update improvement counter
        if is_improvement:
            self.iterations_without_improvement[metric_name] = 0
        else:
            self.iterations_without_improvement[metric_name] += 1

        # Analyze convergence
        metrics = self._analyze_convergence(metric_name, higher_is_better)

        return metrics

    def _analyze_convergence(
        self,
        metric_name: str,
        higher_is_better: bool
    ) -> ConvergenceMetrics:
        """Analyze convergence state for a metric"""

        history = list(self.metric_history[metric_name])
        current = history[-1]
        best = self.best_values[metric_name]

        # Calculate improvement rate
        if len(history) >= 2:
            recent = history[-min(10, len(history)):]
            if len(recent) >= 2:
                rate = (recent[-1] - recent[0]) / len(recent)
            else:
                rate = 0.0
        else:
            rate = 0.0

        # Calculate variance
        if len(history) >= 2:
            recent = history[-min(20, len(history)):]
            variance = statistics.variance(recent) if len(recent) >= 2 else 0.0
        else:
            variance = 0.0

        # Determine convergence state
        no_improvement = self.iterations_without_improvement[metric_name]

        if no_improvement >= self.plateau_threshold:
            state = ConvergenceState.CONVERGED
        elif no_improvement >= self.plateau_threshold // 2:
            state = ConvergenceState.PLATEAUING
        elif abs(rate) > self.improvement_threshold:
            if (higher_is_better and rate > 0) or (not higher_is_better and rate < 0):
                state = ConvergenceState.IMPROVING
            else:
                state = ConvergenceState.DIVERGING
        elif variance > 0.01:
            state = ConvergenceState.UNSTABLE
        else:
            state = ConvergenceState.PLATEAUING

        # Update state
        old_state = self.convergence_states[metric_name]
        self.convergence_states[metric_name] = state

        # Track convergence time
        if state == ConvergenceState.CONVERGED and old_state != ConvergenceState.CONVERGED:
            self.convergence_timestamps[metric_name] = time.time()
            self.stats["converged_metrics"] += 1

        # Calculate confidence
        confidence = self._calculate_confidence(
            history_length=len(history),
            no_improvement=no_improvement,
            variance=variance
        )

        return ConvergenceMetrics(
            metric_name=metric_name,
            current_value=current,
            best_value=best,
            improvement_rate=rate,
            recent_variance=variance,
            iterations_without_improvement=no_improvement,
            convergence_state=state.value,
            confidence=confidence
        )

    def _calculate_confidence(
        self,
        history_length: int,
        no_improvement: int,
        variance: float
    ) -> float:
        """Calculate confidence in convergence assessment"""

        # More history = higher confidence
        history_conf = min(history_length / self.window_size, 1.0)

        # More iterations without improvement = higher confidence
        plateau_conf = min(no_improvement / self.plateau_threshold, 1.0)

        # Lower variance = higher confidence
        variance_conf = max(0.0, 1.0 - variance)

        # Weighted average
        confidence = (
            history_conf * 0.3 +
            plateau_conf * 0.4 +
            variance_conf * 0.3
        )

        return confidence

    def check_overall_convergence(self) -> ConvergenceReport:
        """Check overall convergence across all metrics"""

        self.stats["convergence_checks"] += 1

        # Analyze each metric
        all_metrics = []
        converged_count = 0

        for metric_name in self.metric_history.keys():
            # Use higher_is_better=True as default
            metrics = self._analyze_convergence(metric_name, higher_is_better=True)
            all_metrics.append(metrics)

            if metrics.convergence_state == ConvergenceState.CONVERGED.value:
                converged_count += 1

        # Calculate overall convergence score
        if all_metrics:
            convergence_score = converged_count / len(all_metrics)
        else:
            convergence_score = 0.0

        # Determine overall state
        if convergence_score >= 0.8:
            overall_state = ConvergenceState.CONVERGED
            should_stop = True
            recommendation = "System has converged. Consider stopping improvement cycles."
        elif convergence_score >= 0.6:
            overall_state = ConvergenceState.PLATEAUING
            should_stop = False
            recommendation = "System is plateauing. Reduce improvement frequency."
        elif convergence_score >= 0.3:
            overall_state = ConvergenceState.IMPROVING
            should_stop = False
            recommendation = "System is improving. Continue improvement cycles."
        else:
            overall_state = ConvergenceState.UNSTABLE
            should_stop = False
            recommendation = "System is unstable. Investigate for issues."

        report = ConvergenceReport(
            timestamp=time.time(),
            overall_state=overall_state.value,
            metrics=all_metrics,
            converged_metrics=converged_count,
            total_metrics=len(all_metrics),
            convergence_score=convergence_score,
            should_stop=should_stop,
            recommendation=recommendation
        )

        return report

    def get_convergence_summary(self) -> Dict:
        """Get summary of convergence status"""

        summary = {
            "total_metrics": len(self.metric_history),
            "converged_metrics": sum(
                1 for s in self.convergence_states.values()
                if s == ConvergenceState.CONVERGED
            ),
            "states": {
                state.value: sum(
                    1 for s in self.convergence_states.values() if s == state
                )
                for state in ConvergenceState
            },
            "stats": self.stats
        }

        return summary

    def export_convergence_data(self, filepath: str):
        """Export convergence data to JSON"""

        # Get latest report
        report = self.check_overall_convergence()

        data = {
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
            "exported_at": datetime.now().isoformat(),
            "report": asdict(report),
            "summary": self.get_convergence_summary(),
            "convergence_timestamps": self.convergence_timestamps
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


# Demo / Test
if __name__ == "__main__":
    print("=" * 70)
    print("IMPROVEMENT CONVERGENCE DETECTION SYSTEM")
    print("Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("=" * 70)

    detector = ImprovementConvergenceDetector(
        window_size=50,
        plateau_threshold=15,
        improvement_threshold=0.001
    )

    # Simulate improvement convergence
    print("\n📊 Simulating improvement convergence...")

    # Metric 1: Rapid improvement then plateau
    print("\n  Metric: maat_score (improving then plateauing)")
    for i in range(100):
        # Logarithmic improvement (fast then slow)
        import math
        value = 0.7 + 0.3 * (1 - math.exp(-i/20))
        metrics = detector.update_metric("maat_score", value, higher_is_better=True)

        if i % 20 == 0:
            print(f"    Iteration {i}: {value:.4f} | State: {metrics.convergence_state} | No improvement: {metrics.iterations_without_improvement}")

    # Metric 2: Steady improvement
    print("\n  Metric: response_quality (steady improvement)")
    for i in range(100):
        value = 0.6 + (i * 0.002)
        detector.update_metric("response_quality", value, higher_is_better=True)

    # Check overall convergence
    print("\n📈 Convergence Report:")
    report = detector.check_overall_convergence()

    print(f"\n  Overall State: {report.overall_state}")
    print(f"  Convergence Score: {report.convergence_score:.2%}")
    print(f"  Converged Metrics: {report.converged_metrics}/{report.total_metrics}")
    print(f"  Should Stop: {report.should_stop}")
    print(f"\n  Recommendation: {report.recommendation}")

    print(f"\n  Per-Metric Status:")
    for metric in report.metrics:
        print(f"    {metric.metric_name}:")
        print(f"      State: {metric.convergence_state}")
        print(f"      Current: {metric.current_value:.4f} | Best: {metric.best_value:.4f}")
        print(f"      Improvement rate: {metric.improvement_rate:.6f}")
        print(f"      Confidence: {metric.confidence:.2%}")

    # Summary
    summary = detector.get_convergence_summary()
    print(f"\n📊 Summary:")
    print(f"   Total metrics tracked: {summary['total_metrics']}")
    print(f"   Converged: {summary['converged_metrics']}")
    print(f"   State distribution:")
    for state, count in summary['states'].items():
        if count > 0:
            print(f"     {state}: {count}")

    # Export
    export_path = Path(__file__).parent / "convergence_analysis.json"
    detector.export_convergence_data(str(export_path))
    print(f"\n✅ Analysis exported to: {export_path}")

    print("\n" + "=" * 70)

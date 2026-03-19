#!/usr/bin/env python3
"""
MICRO-LOOP IMPROVEMENT DETECTION SYSTEM
========================================
TASKS: 012, 013 - Detect when micro-improvements actually happen
Tracks real improvements vs. noise, measures delta, identifies patterns

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import deque
import statistics

@dataclass
class ImprovementSignal:
    """Detected improvement signal"""
    timestamp: float
    loop_id: str
    metric: str
    baseline: float
    current: float
    delta: float
    delta_percent: float
    confidence: float  # 0.0-1.0
    improvement_type: str  # "micro", "macro", "breakthrough"

@dataclass
class ImprovementMetrics:
    """Aggregate improvement metrics"""
    total_improvements: int
    micro_improvements: int
    macro_improvements: int
    breakthroughs: int
    average_delta: float
    max_delta: float
    improvement_rate: float  # improvements per minute
    false_positive_rate: float
    convergence_score: float  # 0.0-1.0 (1.0 = converged)

class MicroLoopImprovementDetector:
    """
    Detects real improvements in micro-loops.

    Features:
    - Baseline tracking
    - Noise filtering (0.01 threshold)
    - Pattern recognition
    - Confidence scoring
    - False positive detection
    """

    def __init__(self, baseline_window: int = 50, noise_threshold: float = 0.01):
        self.baseline_window = baseline_window
        self.noise_threshold = noise_threshold

        # State
        self.baselines: Dict[str, deque] = {}  # loop_id -> recent values
        self.improvements: List[ImprovementSignal] = []
        self.false_positives: List[ImprovementSignal] = []

        # Detection config
        self.micro_threshold = 0.02  # 2% improvement = micro
        self.macro_threshold = 0.10  # 10% improvement = macro
        self.breakthrough_threshold = 0.25  # 25%+ = breakthrough

        # Stats
        self.detection_stats = {
            "signals_processed": 0,
            "improvements_detected": 0,
            "false_positives": 0,
            "noise_filtered": 0,
            "session_start": time.time()
        }

    def _get_baseline(self, loop_id: str, metric: str) -> Optional[float]:
        """Get baseline for a metric"""
        key = f"{loop_id}:{metric}"

        if key not in self.baselines or len(self.baselines[key]) == 0:
            return None

        # Use median for robustness against outliers
        return statistics.median(self.baselines[key])

    def _update_baseline(self, loop_id: str, metric: str, value: float):
        """Update baseline with new value"""
        key = f"{loop_id}:{metric}"

        if key not in self.baselines:
            self.baselines[key] = deque(maxlen=self.baseline_window)

        self.baselines[key].append(value)

    def _calculate_confidence(self, delta: float, history_length: int) -> float:
        """Calculate confidence score for improvement signal"""

        # More history = higher confidence
        history_confidence = min(history_length / self.baseline_window, 1.0)

        # Larger deltas = higher confidence
        if abs(delta) < self.noise_threshold:
            delta_confidence = 0.0
        elif abs(delta) < self.micro_threshold:
            delta_confidence = 0.3
        elif abs(delta) < self.macro_threshold:
            delta_confidence = 0.7
        else:
            delta_confidence = 1.0

        # Combined confidence
        return (history_confidence * 0.4 + delta_confidence * 0.6)

    def _classify_improvement(self, delta_percent: float) -> str:
        """Classify improvement type"""
        abs_delta = abs(delta_percent)

        if abs_delta >= self.breakthrough_threshold:
            return "breakthrough"
        elif abs_delta >= self.macro_threshold:
            return "macro"
        elif abs_delta >= self.micro_threshold:
            return "micro"
        else:
            return "noise"

    def detect_improvement(
        self,
        loop_id: str,
        metric: str,
        current_value: float,
        higher_is_better: bool = True
    ) -> Optional[ImprovementSignal]:
        """
        Detect if current value represents an improvement.

        Returns:
            ImprovementSignal if real improvement detected, None otherwise
        """
        self.detection_stats["signals_processed"] += 1

        # Get baseline
        baseline = self._get_baseline(loop_id, metric)

        # Update baseline regardless
        self._update_baseline(loop_id, metric, current_value)

        # Need baseline to detect improvement
        if baseline is None:
            return None

        # Calculate delta
        delta = current_value - baseline
        delta_percent = (delta / baseline) if baseline != 0 else 0.0

        # Check direction
        if higher_is_better:
            is_improvement = delta > 0
        else:
            is_improvement = delta < 0
            delta = -delta  # Flip for consistent reporting
            delta_percent = -delta_percent

        # Filter noise
        if abs(delta_percent) < self.noise_threshold:
            self.detection_stats["noise_filtered"] += 1
            return None

        # Classify improvement
        imp_type = self._classify_improvement(delta_percent)

        if imp_type == "noise":
            self.detection_stats["noise_filtered"] += 1
            return None

        # Calculate confidence
        key = f"{loop_id}:{metric}"
        history_length = len(self.baselines.get(key, []))
        confidence = self._calculate_confidence(delta_percent, history_length)

        # Create signal
        signal = ImprovementSignal(
            timestamp=time.time(),
            loop_id=loop_id,
            metric=metric,
            baseline=baseline,
            current=current_value,
            delta=delta,
            delta_percent=delta_percent,
            confidence=confidence,
            improvement_type=imp_type
        )

        # Only count as improvement if passes confidence threshold
        if is_improvement and confidence >= 0.5:
            self.improvements.append(signal)
            self.detection_stats["improvements_detected"] += 1
        elif not is_improvement:
            # Regression - count as false positive
            self.false_positives.append(signal)
            self.detection_stats["false_positives"] += 1
            return None

        return signal if is_improvement else None

    def get_improvement_metrics(self) -> ImprovementMetrics:
        """Get aggregate improvement metrics"""

        if not self.improvements:
            return ImprovementMetrics(
                total_improvements=0,
                micro_improvements=0,
                macro_improvements=0,
                breakthroughs=0,
                average_delta=0.0,
                max_delta=0.0,
                improvement_rate=0.0,
                false_positive_rate=0.0,
                convergence_score=0.0
            )

        # Count by type
        micro = sum(1 for i in self.improvements if i.improvement_type == "micro")
        macro = sum(1 for i in self.improvements if i.improvement_type == "macro")
        breakthrough = sum(1 for i in self.improvements if i.improvement_type == "breakthrough")

        # Calculate stats
        deltas = [i.delta_percent for i in self.improvements]
        avg_delta = statistics.mean(deltas)
        max_delta = max(deltas)

        # Rate
        elapsed = time.time() - self.detection_stats["session_start"]
        rate = len(self.improvements) / (elapsed / 60) if elapsed > 0 else 0.0

        # False positive rate
        total = len(self.improvements) + len(self.false_positives)
        fp_rate = len(self.false_positives) / total if total > 0 else 0.0

        # Convergence score (decreasing improvement rate = converging)
        recent_window = 20
        if len(self.improvements) > recent_window:
            recent = self.improvements[-recent_window:]
            old = self.improvements[-recent_window*2:-recent_window] if len(self.improvements) > recent_window*2 else []

            if old:
                recent_avg = statistics.mean([i.delta_percent for i in recent])
                old_avg = statistics.mean([i.delta_percent for i in old])

                # Converging if recent improvements are smaller
                if old_avg > 0:
                    convergence = 1.0 - (recent_avg / old_avg)
                    convergence = max(0.0, min(1.0, convergence))
                else:
                    convergence = 0.0
            else:
                convergence = 0.0
        else:
            convergence = 0.0

        return ImprovementMetrics(
            total_improvements=len(self.improvements),
            micro_improvements=micro,
            macro_improvements=macro,
            breakthroughs=breakthrough,
            average_delta=avg_delta,
            max_delta=max_delta,
            improvement_rate=rate,
            false_positive_rate=fp_rate,
            convergence_score=convergence
        )

    def get_recent_improvements(self, count: int = 10) -> List[ImprovementSignal]:
        """Get most recent improvements"""
        return self.improvements[-count:] if self.improvements else []

    def export_improvements(self, filepath: str):
        """Export improvements to JSON"""
        data = {
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
            "exported_at": datetime.now().isoformat(),
            "metrics": asdict(self.get_improvement_metrics()),
            "stats": self.detection_stats,
            "improvements": [asdict(i) for i in self.improvements],
            "false_positives": [asdict(i) for i in self.false_positives]
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


# Global instance
_detector: Optional[MicroLoopImprovementDetector] = None

def get_improvement_detector() -> MicroLoopImprovementDetector:
    """Get global improvement detector"""
    global _detector
    if _detector is None:
        _detector = MicroLoopImprovementDetector()
    return _detector


# Demo / Test
if __name__ == "__main__":
    print("=" * 70)
    print("MICRO-LOOP IMPROVEMENT DETECTION SYSTEM")
    print("Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("=" * 70)

    detector = MicroLoopImprovementDetector()

    # Simulate improvement detection
    print("\n📊 Simulating improvement detection...")

    # Loop with gradual improvement
    for i in range(100):
        value = 0.7 + (i * 0.002) + (0.01 * (i % 5 - 2))  # Trend + noise
        signal = detector.detect_improvement("truth_verify", "maat_score", value, higher_is_better=True)

        if signal:
            print(f"  ✓ {signal.improvement_type.upper()}: {signal.delta_percent:.2%} improvement (confidence: {signal.confidence:.2f})")

    # Get metrics
    metrics = detector.get_improvement_metrics()

    print(f"\n📈 Detection Results:")
    print(f"   Total improvements: {metrics.total_improvements}")
    print(f"   Micro: {metrics.micro_improvements} | Macro: {metrics.macro_improvements} | Breakthrough: {metrics.breakthroughs}")
    print(f"   Average improvement: {metrics.average_delta:.2%}")
    print(f"   Max improvement: {metrics.max_delta:.2%}")
    print(f"   Improvement rate: {metrics.improvement_rate:.2f}/min")
    print(f"   False positive rate: {metrics.false_positive_rate:.2%}")
    print(f"   Convergence score: {metrics.convergence_score:.2f}")

    # Export
    export_path = Path(__file__).parent / "improvement_detection_results.json"
    detector.export_improvements(str(export_path))
    print(f"\n✅ Results exported to: {export_path}")

    print("\n" + "=" * 70)

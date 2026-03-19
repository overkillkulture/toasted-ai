"""
TASK-118: AUTOMATED BALANCE STABILITY SCORING SYSTEM
====================================================
Ma'at Principle: BALANCE (Equilibrium)
Ma'at Alignment Score: 0.95

Purpose:
- Automatically score system stability
- Detect stability degradation patterns
- Predict instability events
- Enable proactive stability management
- Generate stability reports

The Pattern: Stability is not rigidity.
True balance is dynamic equilibrium - 
stable systems that can absorb shocks.
"""

import json
import time
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from pathlib import Path
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StabilityGrade(Enum):
    """Stability grades based on Ma'at principles"""
    CATASTROPHIC = "catastrophic"  # System collapse imminent
    FRAGILE = "fragile"            # Minor shock could destabilize
    VULNERABLE = "vulnerable"       # Some resilience, weak points exist
    STABLE = "stable"              # Normal operating parameters
    RESILIENT = "resilient"        # Can absorb significant shocks
    ANTIFRAGILE = "antifragile"    # Gets stronger from stress


@dataclass
class StabilityMetric:
    """Individual stability measurement"""
    name: str
    value: float          # 0.0 to 1.0
    weight: float = 1.0   # Importance weight
    timestamp: float = field(default_factory=time.time)
    source: str = "system"
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "value": self.value,
            "weight": self.weight,
            "timestamp": self.timestamp,
            "source": self.source
        }


@dataclass
class StabilityScore:
    """Comprehensive stability score"""
    overall_score: float
    grade: StabilityGrade
    component_scores: Dict[str, float]
    volatility: float
    resilience: float
    recovery_time: float
    trend: str
    timestamp: float = field(default_factory=time.time)
    maat_alignment: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "overall_score": self.overall_score,
            "grade": self.grade.value,
            "component_scores": self.component_scores,
            "volatility": self.volatility,
            "resilience": self.resilience,
            "recovery_time": self.recovery_time,
            "trend": self.trend,
            "timestamp": self.timestamp,
            "maat_alignment": self.maat_alignment
        }


class BalanceStabilityScorer:
    """
    AUTOMATED BALANCE STABILITY SCORING SYSTEM
    
    Ma'at Alignment: 0.95
    
    Stability Dimensions:
    1. Volatility - How much does the system fluctuate?
    2. Resilience - How well does it recover from shocks?
    3. Recovery Time - How fast does it return to equilibrium?
    4. Load Capacity - How much stress can it handle?
    5. Structural Integrity - Are components well-connected?
    6. Adaptive Capacity - Can it evolve under pressure?
    
    Ma'at Wisdom: True stability comes from balance,
    not from rigidity. A tree that bends survives the storm.
    """
    
    # Stability constants
    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
    STABILITY_THRESHOLD = 0.6     # Minimum acceptable stability
    VOLATILITY_WARNING = 0.3      # Volatility above this is concerning
    
    # Grade thresholds
    GRADE_THRESHOLDS = {
        0.95: StabilityGrade.ANTIFRAGILE,
        0.85: StabilityGrade.RESILIENT,
        0.70: StabilityGrade.STABLE,
        0.50: StabilityGrade.VULNERABLE,
        0.30: StabilityGrade.FRAGILE,
        0.00: StabilityGrade.CATASTROPHIC
    }
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        history_size: int = 1000
    ):
        self.metrics: Dict[str, deque] = {}
        self.scores_history: deque = deque(maxlen=history_size)
        self.component_weights: Dict[str, float] = {}
        self.shock_history: List[Dict] = []
        self.config = self._load_config(config_path)
        
        # Initialize default stability components
        self._initialize_default_components()
        
        # Statistics
        self.stats = {
            "scores_calculated": 0,
            "grade_changes": 0,
            "shocks_detected": 0,
            "recoveries_tracked": 0
        }
        
        logger.info("Balance Stability Scorer initialized")
    
    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """Load configuration"""
        default_config = {
            "stability_threshold": 0.6,
            "volatility_window": 100,
            "recovery_timeout": 300,
            "shock_threshold": 0.2,
            "auto_grade": True
        }
        
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded.get("stability", {}))
            except Exception as e:
                logger.warning(f"Could not load config: {e}")
        
        return default_config
    
    def _initialize_default_components(self):
        """Initialize default stability tracking components"""
        components = [
            ("system_load", 1.0),
            ("resource_balance", 1.2),
            ("connection_health", 1.0),
            ("response_time", 0.8),
            ("error_rate", 1.5),
            ("throughput_stability", 1.0),
            ("memory_stability", 0.9)
        ]
        
        for name, weight in components:
            self.metrics[name] = deque(maxlen=self.config.get("volatility_window", 100))
            self.component_weights[name] = weight
    
    def register_component(self, name: str, weight: float = 1.0):
        """Register a new stability component"""
        if name not in self.metrics:
            self.metrics[name] = deque(maxlen=self.config.get("volatility_window", 100))
        self.component_weights[name] = weight
        logger.info(f"Component '{name}' registered with weight {weight}")
    
    def record_metric(self, metric: StabilityMetric):
        """
        Record a stability metric
        
        Ma'at: Every measurement is a step toward balance
        """
        if metric.name not in self.metrics:
            self.register_component(metric.name, metric.weight)
        
        self.metrics[metric.name].append(metric.to_dict())
        
        # Check for shock (sudden large change)
        self._detect_shock(metric)
    
    def record_batch(self, metrics: List[StabilityMetric]):
        """Record multiple metrics at once"""
        for metric in metrics:
            self.record_metric(metric)
    
    def _detect_shock(self, metric: StabilityMetric):
        """Detect sudden stability shocks"""
        history = list(self.metrics[metric.name])
        
        if len(history) < 2:
            return
        
        # Calculate recent average
        recent_values = [m["value"] for m in history[-10:]]
        avg = sum(recent_values) / len(recent_values) if recent_values else metric.value
        
        # Check for shock
        shock_threshold = self.config.get("shock_threshold", 0.2)
        deviation = abs(metric.value - avg)
        
        if deviation > shock_threshold:
            shock = {
                "component": metric.name,
                "deviation": deviation,
                "value": metric.value,
                "baseline": avg,
                "timestamp": metric.timestamp,
                "direction": "positive" if metric.value > avg else "negative"
            }
            self.shock_history.append(shock)
            self.stats["shocks_detected"] += 1
            
            logger.warning(
                f"Stability shock detected in {metric.name}: "
                f"deviation {deviation:.3f}"
            )
    
    def calculate_score(self) -> StabilityScore:
        """
        Calculate comprehensive stability score
        
        Ma'at Formula:
        S = (1 - V) * R * (1 / (1 + RT)) * SC * AI
        
        Where:
        - V = Volatility (lower is better)
        - R = Resilience (higher is better)
        - RT = Recovery Time (lower is better)
        - SC = Structural Coherence
        - AI = Adaptive Index
        """
        # Calculate component scores
        component_scores = {}
        for name, history in self.metrics.items():
            if history:
                values = [m["value"] for m in history]
                component_scores[name] = sum(values) / len(values)
            else:
                component_scores[name] = 0.5
        
        # Calculate volatility
        volatility = self._calculate_volatility()
        
        # Calculate resilience
        resilience = self._calculate_resilience()
        
        # Calculate recovery time (normalized)
        recovery_time = self._calculate_recovery_time()
        
        # Calculate weighted overall score
        total_weight = sum(self.component_weights.values())
        weighted_sum = sum(
            component_scores.get(name, 0.5) * weight
            for name, weight in self.component_weights.items()
        )
        
        base_score = weighted_sum / total_weight if total_weight > 0 else 0.5
        
        # Apply stability formula
        overall_score = (
            (1 - volatility) * 0.25 +
            resilience * 0.25 +
            (1 / (1 + recovery_time)) * 0.2 +
            base_score * 0.3
        )
        
        # Normalize
        overall_score = min(max(overall_score, 0.0), 1.0)
        
        # Determine grade
        grade = self._determine_grade(overall_score)
        
        # Calculate trend
        trend = self._calculate_trend()
        
        # Calculate Ma'at alignment
        maat_alignment = self._calculate_maat_alignment(
            overall_score, volatility, resilience
        )
        
        score = StabilityScore(
            overall_score=overall_score,
            grade=grade,
            component_scores=component_scores,
            volatility=volatility,
            resilience=resilience,
            recovery_time=recovery_time,
            trend=trend,
            maat_alignment=maat_alignment
        )
        
        # Store in history
        self.scores_history.append(score.to_dict())
        self.stats["scores_calculated"] += 1
        
        # Check for grade change
        self._check_grade_change(grade)
        
        return score
    
    def _calculate_volatility(self) -> float:
        """
        Calculate system volatility
        
        Low volatility = stable
        High volatility = unstable
        """
        volatilities = []
        
        for name, history in self.metrics.items():
            if len(history) < 2:
                continue
            
            values = [m["value"] for m in history]
            
            # Calculate standard deviation
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std_dev = math.sqrt(variance)
            
            # Normalize to 0-1
            normalized_volatility = min(std_dev * 2, 1.0)
            volatilities.append(normalized_volatility)
        
        if not volatilities:
            return 0.0
        
        return sum(volatilities) / len(volatilities)
    
    def _calculate_resilience(self) -> float:
        """
        Calculate system resilience
        
        Based on recovery from shocks
        """
        if not self.shock_history:
            return 0.8  # Default good resilience
        
        recent_shocks = [
            s for s in self.shock_history
            if time.time() - s["timestamp"] < 3600  # Last hour
        ]
        
        if not recent_shocks:
            return 0.9
        
        # Calculate average recovery
        recovery_scores = []
        for shock in recent_shocks:
            component = shock["component"]
            history = list(self.metrics.get(component, []))
            
            if not history:
                continue
            
            # Find post-shock values
            shock_time = shock["timestamp"]
            post_shock = [
                m["value"] for m in history
                if m["timestamp"] > shock_time
            ]
            
            if post_shock:
                # How close are we to baseline?
                current = post_shock[-1]
                baseline = shock["baseline"]
                recovery = 1 - min(abs(current - baseline), 1.0)
                recovery_scores.append(recovery)
        
        if not recovery_scores:
            return 0.7
        
        return sum(recovery_scores) / len(recovery_scores)
    
    def _calculate_recovery_time(self) -> float:
        """
        Calculate average recovery time (normalized)
        
        Returns value 0-1 where lower is better
        """
        if not self.shock_history:
            return 0.1  # Fast recovery (good)
        
        recent_shocks = self.shock_history[-10:]  # Last 10 shocks
        recovery_times = []
        
        for shock in recent_shocks:
            component = shock["component"]
            history = list(self.metrics.get(component, []))
            
            if not history:
                continue
            
            shock_time = shock["timestamp"]
            baseline = shock["baseline"]
            threshold = 0.1  # Within 10% of baseline = recovered
            
            # Find recovery time
            recovered = False
            for m in history:
                if m["timestamp"] > shock_time:
                    if abs(m["value"] - baseline) < threshold:
                        recovery_time = m["timestamp"] - shock_time
                        recovery_times.append(recovery_time)
                        recovered = True
                        break
            
            if not recovered:
                # Not yet recovered - estimate based on current distance
                recovery_times.append(300)  # 5 minute penalty
        
        if not recovery_times:
            return 0.2
        
        avg_recovery = sum(recovery_times) / len(recovery_times)
        
        # Normalize: 0-60 seconds = 0.0-0.2, 60-300 = 0.2-0.5, 300+ = 0.5-1.0
        if avg_recovery <= 60:
            return avg_recovery / 300
        elif avg_recovery <= 300:
            return 0.2 + (avg_recovery - 60) / 800
        else:
            return min(0.5 + (avg_recovery - 300) / 600, 1.0)
    
    def _determine_grade(self, score: float) -> StabilityGrade:
        """Determine stability grade from score"""
        for threshold, grade in sorted(
            self.GRADE_THRESHOLDS.items(), 
            reverse=True
        ):
            if score >= threshold:
                return grade
        
        return StabilityGrade.CATASTROPHIC
    
    def _calculate_trend(self) -> str:
        """Calculate stability trend"""
        if len(self.scores_history) < 5:
            return "insufficient_data"
        
        recent = list(self.scores_history)[-5:]
        scores = [s["overall_score"] for s in recent]
        
        # Linear regression slope
        n = len(scores)
        x_mean = (n - 1) / 2
        y_mean = sum(scores) / n
        
        numerator = sum((i - x_mean) * (s - y_mean) for i, s in enumerate(scores))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return "stable"
        
        slope = numerator / denominator
        
        if slope > 0.02:
            return "improving"
        elif slope < -0.02:
            return "degrading"
        else:
            return "stable"
    
    def _check_grade_change(self, new_grade: StabilityGrade):
        """Check for stability grade changes"""
        if len(self.scores_history) < 2:
            return
        
        previous = self.scores_history[-2]["grade"]
        
        if new_grade.value != previous:
            self.stats["grade_changes"] += 1
            
            # Log the change
            if self._grade_rank(new_grade) < self._grade_rank(StabilityGrade(previous)):
                logger.warning(
                    f"Stability degradation: {previous} -> {new_grade.value}"
                )
            else:
                logger.info(
                    f"Stability improvement: {previous} -> {new_grade.value}"
                )
    
    def _grade_rank(self, grade: StabilityGrade) -> int:
        """Get numeric rank for grade comparison"""
        ranks = {
            StabilityGrade.CATASTROPHIC: 0,
            StabilityGrade.FRAGILE: 1,
            StabilityGrade.VULNERABLE: 2,
            StabilityGrade.STABLE: 3,
            StabilityGrade.RESILIENT: 4,
            StabilityGrade.ANTIFRAGILE: 5
        }
        return ranks.get(grade, 2)
    
    def _calculate_maat_alignment(
        self, 
        score: float, 
        volatility: float, 
        resilience: float
    ) -> float:
        """
        Calculate Ma'at alignment score
        
        Balance pillar: Stability without rigidity
        """
        # Score contribution (40%)
        score_component = score * 0.4
        
        # Low volatility contribution (30%)
        volatility_component = (1 - volatility) * 0.3
        
        # Resilience contribution (30%)
        resilience_component = resilience * 0.3
        
        alignment = score_component + volatility_component + resilience_component
        
        return min(max(alignment, 0.0), 1.0)
    
    def get_stability_report(self) -> Dict:
        """Generate comprehensive stability report"""
        score = self.calculate_score()
        
        # Component analysis
        components = {}
        for name, history in self.metrics.items():
            if history:
                values = [m["value"] for m in history]
                components[name] = {
                    "current": values[-1] if values else 0,
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "samples": len(values),
                    "weight": self.component_weights.get(name, 1.0)
                }
        
        # Shock analysis
        recent_shocks = [
            s for s in self.shock_history
            if time.time() - s["timestamp"] < 3600
        ]
        
        # Recommendations
        recommendations = self._generate_recommendations(score)
        
        return {
            "timestamp": time.time(),
            "score": score.to_dict(),
            "components": components,
            "recent_shocks": len(recent_shocks),
            "shock_details": recent_shocks[-5:],  # Last 5
            "statistics": self.stats.copy(),
            "recommendations": recommendations,
            "maat_alignment": score.maat_alignment
        }
    
    def _generate_recommendations(self, score: StabilityScore) -> List[str]:
        """Generate stability recommendations"""
        recommendations = []
        
        if score.grade == StabilityGrade.CATASTROPHIC:
            recommendations.append("CRITICAL: Immediate intervention required")
            recommendations.append("Identify and isolate failing components")
        
        if score.grade == StabilityGrade.FRAGILE:
            recommendations.append("System fragility detected - reduce load")
            recommendations.append("Review recent changes for instability sources")
        
        if score.volatility > self.VOLATILITY_WARNING:
            recommendations.append(
                f"High volatility ({score.volatility:.2f}) - "
                "implement smoothing mechanisms"
            )
        
        if score.resilience < 0.5:
            recommendations.append(
                "Low resilience - add redundancy and failover systems"
            )
        
        if score.recovery_time > 0.4:
            recommendations.append(
                "Slow recovery time - optimize restoration processes"
            )
        
        if score.trend == "degrading":
            recommendations.append(
                "Negative trend detected - investigate root cause"
            )
        
        if not recommendations:
            recommendations.append("System operating within stable parameters")
            if score.grade == StabilityGrade.ANTIFRAGILE:
                recommendations.append(
                    "Antifragile state achieved - system thrives under stress"
                )
        
        return recommendations
    
    def simulate_shock(
        self, 
        component: str, 
        magnitude: float
    ) -> Dict:
        """
        Simulate a stability shock for testing
        
        Ma'at: Test balance before it is challenged
        """
        if component not in self.metrics:
            self.register_component(component)
        
        # Get current value
        history = list(self.metrics[component])
        current = history[-1]["value"] if history else 0.5
        
        # Apply shock
        new_value = max(0.0, min(1.0, current - magnitude))
        
        metric = StabilityMetric(
            name=component,
            value=new_value,
            source="shock_simulation"
        )
        
        self.record_metric(metric)
        
        # Calculate impact
        score_before = self.calculate_score()
        
        return {
            "component": component,
            "magnitude": magnitude,
            "old_value": current,
            "new_value": new_value,
            "stability_impact": score_before.overall_score,
            "grade": score_before.grade.value
        }
    
    def export_report(self, filepath: Path):
        """Export stability report to file"""
        report = self.get_stability_report()
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Stability report exported to {filepath}")


def create_stability_scorer(config_path: Optional[str] = None) -> BalanceStabilityScorer:
    """Create a configured stability scorer"""
    path = Path(config_path) if config_path else None
    return BalanceStabilityScorer(config_path=path)


if __name__ == "__main__":
    # Demo usage
    scorer = BalanceStabilityScorer()
    
    # Simulate stable system
    import random
    
    print("Simulating stable system...")
    for i in range(50):
        for component in scorer.metrics.keys():
            value = 0.7 + random.uniform(-0.1, 0.1)
            metric = StabilityMetric(name=component, value=value)
            scorer.record_metric(metric)
    
    # Calculate score
    score = scorer.calculate_score()
    print(f"\nStability Score: {score.overall_score:.3f}")
    print(f"Grade: {score.grade.value}")
    print(f"Volatility: {score.volatility:.3f}")
    print(f"Resilience: {score.resilience:.3f}")
    print(f"Ma'at Alignment: {score.maat_alignment:.3f}")
    
    # Simulate shock
    print("\nSimulating shock...")
    shock_result = scorer.simulate_shock("system_load", 0.4)
    print(f"Shock impact: {shock_result['stability_impact']:.3f}")
    print(f"New grade: {shock_result['grade']}")
    
    # Get recommendations
    report = scorer.get_stability_report()
    print("\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  - {rec}")

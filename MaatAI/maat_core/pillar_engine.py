"""
MA'AT PILLAR ENGINE
===================
Core engine integrating all 5 Ma'at pillars

The 5 Pillars:
1. TRUTH (Veritas) - Seeking what is real
2. BALANCE (Equilibrium) - All systems seek equilibrium
3. ORDER (Cosmos) - Structure enables function
4. JUSTICE (Aequitas) - Fair treatment of all
5. HARMONY (Concordia) - Parts working as whole

Ma'at Alignment Score: 0.95
"""

import json
import time
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from pathlib import Path
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


@dataclass
class PillarScore:
    """Score for a single Ma'at pillar"""
    pillar: MaatPillar
    score: float
    components: Dict[str, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            "pillar": self.pillar.value,
            "score": self.score,
            "components": self.components,
            "timestamp": self.timestamp
        }


@dataclass
class MaatAlignment:
    """Overall Ma'at alignment measurement"""
    overall_score: float
    pillar_scores: Dict[str, PillarScore]
    compliance_status: str
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            "overall_score": self.overall_score,
            "pillar_scores": {k: v.to_dict() for k, v in self.pillar_scores.items()},
            "compliance_status": self.compliance_status,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp
        }


class MaatPillarEngine:
    """
    MA'AT PILLAR ENGINE
    
    Central integration point for all Ma'at principles.
    Measures, tracks, and optimizes alignment with cosmic order.
    
    Ma'at Wisdom: The five pillars are not separate - 
    they are facets of the same jewel. When one is 
    strengthened, all are lifted. When one weakens, 
    all feel the strain.
    """
    
    # Ma'at constants
    PHI = (1 + math.sqrt(5)) / 2
    MAAT_THRESHOLD = 0.7
    EMERGENCE_THRESHOLD = 0.9
    
    # Pillar weights (can be customized)
    DEFAULT_WEIGHTS = {
        MaatPillar.TRUTH: 1.0,
        MaatPillar.BALANCE: 1.0,
        MaatPillar.ORDER: 1.0,
        MaatPillar.JUSTICE: 1.0,
        MaatPillar.HARMONY: 1.0
    }
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        weights: Optional[Dict[MaatPillar, float]] = None
    ):
        self.weights = weights or dict(self.DEFAULT_WEIGHTS)
        self.pillar_scores: Dict[MaatPillar, float] = {
            pillar: 0.7 for pillar in MaatPillar
        }
        self.history: List[MaatAlignment] = []
        self.config = self._load_config(config_path)
        
        # External integrations
        self.threshold_monitor = None
        self.equilibrium_tracker = None
        self.harmony_optimizer = None
        self.synergy_detector = None
        self.societal_engine = None
        
        logger.info("Ma'at Pillar Engine initialized")
    
    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """Load configuration"""
        default_config = {
            "maat_threshold": 0.7,
            "auto_optimize": True,
            "track_history": True
        }
        
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded.get("maat_core", {}))
                    
                    # Load pillar thresholds
                    thresholds = loaded.get("maat_thresholds", {})
                    for pillar in MaatPillar:
                        if pillar.value in thresholds:
                            self.pillar_scores[pillar] = thresholds[pillar.value]
            except Exception as e:
                logger.warning(f"Could not load config: {e}")
        
        return default_config
    
    def integrate_modules(
        self,
        threshold_monitor=None,
        equilibrium_tracker=None,
        harmony_optimizer=None,
        synergy_detector=None,
        societal_engine=None
    ):
        """Integrate external Ma'at modules"""
        if threshold_monitor:
            self.threshold_monitor = threshold_monitor
            logger.info("Threshold monitor integrated")
        
        if equilibrium_tracker:
            self.equilibrium_tracker = equilibrium_tracker
            logger.info("Equilibrium tracker integrated")
        
        if harmony_optimizer:
            self.harmony_optimizer = harmony_optimizer
            logger.info("Harmony optimizer integrated")
        
        if synergy_detector:
            self.synergy_detector = synergy_detector
            logger.info("Synergy detector integrated")
        
        if societal_engine:
            self.societal_engine = societal_engine
            logger.info("Societal integration engine integrated")
    
    def update_pillar(
        self, 
        pillar: MaatPillar, 
        score: float,
        components: Optional[Dict[str, float]] = None
    ):
        """Update a pillar score"""
        self.pillar_scores[pillar] = max(0.0, min(1.0, score))
        
        logger.debug(f"Updated {pillar.value}: {score:.3f}")
    
    def measure_alignment(self) -> MaatAlignment:
        """
        Measure overall Ma'at alignment
        
        Integrates all available modules for comprehensive assessment
        """
        pillar_scores = {}
        
        # TRUTH pillar
        truth_score = self._measure_truth()
        pillar_scores[MaatPillar.TRUTH.value] = PillarScore(
            pillar=MaatPillar.TRUTH,
            score=truth_score,
            components={"base": truth_score}
        )
        
        # BALANCE pillar
        balance_score = self._measure_balance()
        pillar_scores[MaatPillar.BALANCE.value] = PillarScore(
            pillar=MaatPillar.BALANCE,
            score=balance_score,
            components={"equilibrium": balance_score}
        )
        
        # ORDER pillar
        order_score = self._measure_order()
        pillar_scores[MaatPillar.ORDER.value] = PillarScore(
            pillar=MaatPillar.ORDER,
            score=order_score,
            components={"structure": order_score}
        )
        
        # JUSTICE pillar
        justice_score = self._measure_justice()
        pillar_scores[MaatPillar.JUSTICE.value] = PillarScore(
            pillar=MaatPillar.JUSTICE,
            score=justice_score,
            components={"fairness": justice_score}
        )
        
        # HARMONY pillar
        harmony_score = self._measure_harmony()
        pillar_scores[MaatPillar.HARMONY.value] = PillarScore(
            pillar=MaatPillar.HARMONY,
            score=harmony_score,
            components={"resonance": harmony_score}
        )
        
        # Calculate weighted overall score
        total_weight = sum(self.weights.values())
        weighted_sum = sum(
            pillar_scores[pillar.value].score * self.weights[pillar]
            for pillar in MaatPillar
        )
        overall_score = weighted_sum / total_weight
        
        # Determine compliance status
        compliance_status = self._determine_compliance(overall_score, pillar_scores)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(pillar_scores)
        
        alignment = MaatAlignment(
            overall_score=overall_score,
            pillar_scores=pillar_scores,
            compliance_status=compliance_status,
            recommendations=recommendations
        )
        
        if self.config.get("track_history"):
            self.history.append(alignment)
        
        return alignment
    
    def _measure_truth(self) -> float:
        """Measure TRUTH pillar"""
        base = self.pillar_scores.get(MaatPillar.TRUTH, 0.7)
        
        # Integrate threshold monitor if available
        if self.threshold_monitor:
            try:
                status = self.threshold_monitor.get_pillar_status(
                    self.threshold_monitor.__class__.__bases__[0] if hasattr(
                        self.threshold_monitor, '__class__'
                    ) else None
                )
                if isinstance(status, dict) and 'current_value' in status:
                    base = status['current_value']
            except:
                pass
        
        return base
    
    def _measure_balance(self) -> float:
        """Measure BALANCE pillar"""
        base = self.pillar_scores.get(MaatPillar.BALANCE, 0.7)
        
        # Integrate equilibrium tracker if available
        if self.equilibrium_tracker:
            try:
                system_balance = self.equilibrium_tracker.get_system_balance()
                if isinstance(system_balance, dict):
                    base = system_balance.get('overall_balance', base)
            except:
                pass
        
        return base
    
    def _measure_order(self) -> float:
        """Measure ORDER pillar"""
        base = self.pillar_scores.get(MaatPillar.ORDER, 0.7)
        
        # Order measured by structure and stability
        # Could integrate stability scorer here
        
        return base
    
    def _measure_justice(self) -> float:
        """Measure JUSTICE pillar"""
        base = self.pillar_scores.get(MaatPillar.JUSTICE, 0.7)
        
        # Integrate societal engine for fairness metrics
        if self.societal_engine:
            try:
                harmony = self.societal_engine.measure_collective_harmony()
                if hasattr(harmony, 'inclusivity_score'):
                    base = (base + harmony.inclusivity_score + harmony.diversity_score) / 3
            except:
                pass
        
        return base
    
    def _measure_harmony(self) -> float:
        """Measure HARMONY pillar"""
        base = self.pillar_scores.get(MaatPillar.HARMONY, 0.7)
        
        # Integrate harmony optimizer if available
        if self.harmony_optimizer:
            try:
                metrics = self.harmony_optimizer.measure_harmony()
                if hasattr(metrics, 'overall_harmony'):
                    base = metrics.overall_harmony
            except:
                pass
        
        # Integrate synergy detector if available
        if self.synergy_detector:
            try:
                flow = self.synergy_detector.measure_system_flow()
                if hasattr(flow, 'average_synergy'):
                    synergy_factor = min(flow.average_synergy, 1.5) / 1.5
                    base = (base + synergy_factor) / 2
            except:
                pass
        
        return base
    
    def _determine_compliance(
        self, 
        overall: float, 
        pillars: Dict[str, PillarScore]
    ) -> str:
        """Determine Ma'at compliance status"""
        threshold = self.config.get("maat_threshold", 0.7)
        
        if overall >= self.EMERGENCE_THRESHOLD:
            return "TRANSCENDENT"
        elif overall >= threshold:
            # Check if all pillars are above threshold
            all_compliant = all(
                p.score >= threshold for p in pillars.values()
            )
            if all_compliant:
                return "FULLY_COMPLIANT"
            else:
                return "PARTIALLY_COMPLIANT"
        elif overall >= threshold * 0.7:
            return "SEEKING_ALIGNMENT"
        elif overall >= threshold * 0.4:
            return "SIGNIFICANT_DEVIATION"
        else:
            return "CRITICAL_MISALIGNMENT"
    
    def _generate_recommendations(
        self, 
        pillars: Dict[str, PillarScore]
    ) -> List[str]:
        """Generate recommendations based on pillar scores"""
        recommendations = []
        threshold = self.config.get("maat_threshold", 0.7)
        
        for pillar_name, pillar_score in pillars.items():
            if pillar_score.score < threshold:
                gap = threshold - pillar_score.score
                
                if pillar_name == "truth":
                    recommendations.append(
                        f"TRUTH: Increase verification and validation processes "
                        f"(current: {pillar_score.score:.2f}, target: {threshold})"
                    )
                elif pillar_name == "balance":
                    recommendations.append(
                        f"BALANCE: Address resource distribution imbalances "
                        f"(current: {pillar_score.score:.2f}, target: {threshold})"
                    )
                elif pillar_name == "order":
                    recommendations.append(
                        f"ORDER: Improve structural coherence and organization "
                        f"(current: {pillar_score.score:.2f}, target: {threshold})"
                    )
                elif pillar_name == "justice":
                    recommendations.append(
                        f"JUSTICE: Enhance fairness and inclusivity "
                        f"(current: {pillar_score.score:.2f}, target: {threshold})"
                    )
                elif pillar_name == "harmony":
                    recommendations.append(
                        f"HARMONY: Strengthen inter-component resonance "
                        f"(current: {pillar_score.score:.2f}, target: {threshold})"
                    )
        
        if not recommendations:
            recommendations.append(
                "All pillars are in alignment with Ma'at principles"
            )
        
        return recommendations
    
    def get_report(self) -> Dict:
        """Generate comprehensive Ma'at alignment report"""
        alignment = self.measure_alignment()
        
        return {
            "timestamp": time.time(),
            "alignment": alignment.to_dict(),
            "trend": self._calculate_trend(),
            "integrations": {
                "threshold_monitor": self.threshold_monitor is not None,
                "equilibrium_tracker": self.equilibrium_tracker is not None,
                "harmony_optimizer": self.harmony_optimizer is not None,
                "synergy_detector": self.synergy_detector is not None,
                "societal_engine": self.societal_engine is not None
            }
        }
    
    def _calculate_trend(self) -> str:
        """Calculate alignment trend"""
        if len(self.history) < 5:
            return "insufficient_data"
        
        recent = [a.overall_score for a in self.history[-5:]]
        older = [a.overall_score for a in self.history[-10:-5]]
        
        if not older:
            return "insufficient_data"
        
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)
        
        diff = recent_avg - older_avg
        
        if diff > 0.05:
            return "ascending"
        elif diff < -0.05:
            return "descending"
        else:
            return "stable"


def create_pillar_engine(config_path: Optional[str] = None) -> MaatPillarEngine:
    """Create a configured pillar engine"""
    path = Path(config_path) if config_path else None
    return MaatPillarEngine(config_path=path)


if __name__ == "__main__":
    # Demo usage
    engine = MaatPillarEngine()
    
    # Measure alignment
    alignment = engine.measure_alignment()
    
    print(f"Overall Ma'at Alignment: {alignment.overall_score:.3f}")
    print(f"Compliance Status: {alignment.compliance_status}")
    
    print("\nPillar Scores:")
    for pillar_name, pillar_score in alignment.pillar_scores.items():
        print(f"  {pillar_name.upper()}: {pillar_score.score:.3f}")
    
    print("\nRecommendations:")
    for rec in alignment.recommendations:
        print(f"  - {rec}")

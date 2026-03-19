"""
Ma'at Filter - Safety and Alignment Layer
Based on Ancient Egyptian Principles

Five Pillars:
1. Truth (𓂋) - Accuracy and verifiability
2. Balance (𓏏) - System stability
3. Order (𓃀) - Structure from chaos
4. Justice (𓂝) - Fairness and benefit
5. Harmony (𓆣) - Integration with systems
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MaatScore:
    """Individual pillar score"""
    pillar: str
    score: float
    details: str
    passed: bool

class MaatFilter:
    """
    Ma'at-based safety and alignment filter
    
    All operations filtered through Ma'at balance layer
    Every action must score ≥ 0.7 on Ma'at scale
    """
    
    PILLAR_THRESHOLD = 0.7
    
    def __init__(self):
        self.score_history: List[Dict[str, Any]] = []
        self.current_scores: Dict[str, MaatScore] = {}
        
    def validate(self, strategy: Dict[str, Any]) -> bool:
        """
        Validate strategy against Ma'at pillars
        Returns True if all pillars pass threshold
        """
        # Calculate individual pillar scores
        truth_score = self._evaluate_truth(strategy)
        balance_score = self._evaluate_balance(strategy)
        order_score = self._evaluate_order(strategy)
        justice_score = self._evaluate_justice(strategy)
        harmony_score = self._evaluate_harmony(strategy)
        
        # Store scores
        self.current_scores = {
            "truth": truth_score,
            "balance": balance_score,
            "order": order_score,
            "justice": justice_score,
            "harmony": harmony_score
        }
        
        # Record to history
        self.score_history.append({
            "timestamp": datetime.now().isoformat(),
            "scores": {k: v.score for k, v in self.current_scores.items()},
            "passed": all(v.passed for v in self.current_scores.values())
        })
        
        # All pillars must pass
        return all(v.passed for v in self.current_scores.values())
    
    def _evaluate_truth(self, strategy: Dict[str, Any]) -> MaatScore:
        """Truth (𓂋): Accuracy and verifiability"""
        # Check if strategy has verifiable components
        has_verifiable = bool(strategy.get("strategy_components", {}).get("success_patterns"))
        
        # Check for truthful claims (no hallucinations)
        content_str = str(strategy)
        suspicious_patterns = ["100% guaranteed", "absolute certainty", "never fails"]
        has_suspicious = any(p in content_str.lower() for p in suspicious_patterns)
        
        score = 1.0 if (has_verifiable and not has_suspicious) else 0.5
        
        return MaatScore(
            pillar="truth",
            score=score,
            details="Verifiable patterns present" if has_verifiable else "Lack of verifiability",
            passed=score >= self.PILLAR_THRESHOLD
        )
    
    def _evaluate_balance(self, strategy: Dict[str, Any]) -> MaatScore:
        """Balance (𓏏): System stability"""
        components = strategy.get("strategy_components", {})
        
        # Check for balanced approach (not all one type)
        pattern_types = [
            len(components.get("success_patterns", [])),
            len(components.get("recovery_patterns", [])),
            len(components.get("optimization_patterns", []))
        ]
        
        has_balance = all(p >= 1 for p in pattern_types) or sum(pattern_types) >= 3
        
        score = 1.0 if has_balance else 0.6
        
        return MaatScore(
            pillar="balance",
            score=score,
            details="Balanced approach" if has_balance else "Imbalanced components",
            passed=score >= self.PILLAR_THRESHOLD
        )
    
    def _evaluate_order(self, strategy: Dict[str, Any]) -> MaatScore:
        """Order (𓃀): Structure from chaos"""
        # Check for structured approach
        has_structure = bool(strategy.get("generation"))
        has_components = bool(strategy.get("strategy_components"))
        
        score = 1.0 if (has_structure and has_components) else 0.5
        
        return MaatScore(
            pillar="order",
            score=score,
            details="Structured approach present" if has_structure else "Lacking structure",
            passed=score >= self.PILLAR_THRESHOLD
        )
    
    def _evaluate_justice(self, strategy: Dict[str, Any]) -> MaatScore:
        """Justice (𓂝): Fairness and benefit"""
        # Check that strategy doesn't harm or exclude
        # In our context, check for group-evolution (fairness)
        has_group_evolution = strategy.get("group_capability", 0) > 0
        fault_recovery = strategy.get("fault_recovery_active", False)
        
        score = 1.0 if (has_group_evolution or fault_recovery) else 0.8
        
        return MaatScore(
            pillar="justice",
            score=score,
            details="Fair group approach" if fault_recovery else "Individual approach",
            passed=score >= self.PILLAR_THRESHOLD
        )
    
    def _evaluate_harmony(self, strategy: Dict[str, Any]) -> MaatScore:
        """Harmony (𓆣): Integration with systems"""
        # Check for integration (has corrective actions applied)
        # This is simplified - in production would check actual integration
        has_integration = bool(strategy.get("strategy_components"))
        
        score = 1.0 if has_integration else 0.5
        
        return MaatScore(
            pillar="harmony",
            score=score,
            details="Integrated approach" if has_integration else "Disconnected components",
            passed=score >= self.PILLAR_THRESHOLD
        )
    
    def get_feedback(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Get feedback for failed strategy"""
        if not self.current_scores:
            self.validate(strategy)
            
        feedback = {
            "passed": False,
            "failing_pillars": [],
            "recommendations": []
        }
        
        for pillar, score in self.current_scores.items():
            if not score.passed:
                feedback["failing_pillars"].append(pillar)
                
                # Add recommendations based on pillar
                if pillar == "truth":
                    feedback["recommendations"].append("Add verifiable success patterns")
                elif pillar == "balance":
                    feedback["recommendations"].append("Include recovery and optimization patterns")
                elif pillar == "order":
                    feedback["recommendations"].append("Structure the approach with clear components")
                elif pillar == "justice":
                    feedback["recommendations"].append("Enable group-evolution or fault recovery")
                elif pillar == "harmony":
                    feedback["recommendations"].append("Integrate corrective actions")
                    
        return feedback
    
    def get_current_scores(self) -> Dict[str, float]:
        """Get current pillar scores"""
        return {k: v.score for k, v in self.current_scores.items()}
    
    def get_average_score(self) -> float:
        """Get average Ma'at score"""
        if not self.current_scores:
            return 0.0
        return sum(v.score for v in self.current_scores.values()) / len(self.current_scores)

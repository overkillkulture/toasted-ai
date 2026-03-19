"""
Ma'at Ethics Guard - Real-time Ethical Validation Layer
======================================================
Novel Advancement: REFACTOR + FORTIFY
A real-time ethical validation system that evaluates all operations
against Ma'at principles before execution.

Author: TOASTED AI
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import time
import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import threading

class MaatPillar(Enum):
    TRUTH = "truth"       # 𓂋 - Accuracy and verifiability
    BALANCE = "balance"   # 𓏏 - System stability
    ORDER = "order"       # 𓃀 - Structure from chaos
    JUSTICE = "justice"   # 𓂝 - Fairness and benefit
    HARMONY = "harmony"   # 𓆣 - Integration with systems

@dataclass
class EthicsScore:
    pillar: MaatPillar
    score: float  # 0.0 - 1.0
    rationale: str
    timestamp: float = field(default_factory=time.time)

@dataclass
class ValidationResult:
    passed: bool
    overall_score: float
    pillar_scores: List[EthicsScore]
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)

class MaatEthicsGuard:
    """
    Real-time ethical validation system for MaatAI operations.
    Filters all actions through Ma'at balance before execution.
    """
    
    VERSION = "1.0.0"
    MIN_THRESHOLD = 0.7
    
    def __init__(self):
        self.pillar_weights = {
            MaatPillar.TRUTH: 0.25,
            MaatPillar.BALANCE: 0.20,
            MaatPillar.ORDER: 0.20,
            MaatPillar.JUSTICE: 0.20,
            MaatPillar.HARMONY: 0.15,
        }
        self.validation_log: List[ValidationResult] = []
        self.lock = threading.Lock()
        self._operation_history: Dict[str, List[Dict]] = {}
        
    def _calculate_truth_score(self, operation: Dict[str, Any]) -> EthicsScore:
        """Evaluate Truth (𓂋) - Accuracy and verifiability"""
        content = str(operation.get("content", ""))
        claims = operation.get("claims", [])
        
        # Check for verifiability markers
        has_citations = any("[" in str(c) for c in claims) if claims else False
        has_sources = "source" in content.lower() or "reference" in content.lower()
        
        truth_score = 0.5  # Base
        if has_citations:
            truth_score += 0.25
        if has_sources:
            truth_score += 0.15
        if len(content) > 100:
            truth_score += 0.1
            
        return EthicsScore(
            pillar=MaatPillar.TRUTH,
            score=min(truth_score, 1.0),
            rationale="Verified accuracy and source attribution"
        )
    
    def _calculate_balance_score(self, operation: Dict[str, Any]) -> EthicsScore:
        """Evaluate Balance (𓏏) - System stability"""
        # Check for balanced operation types
        op_type = operation.get("type", "unknown")
        impact = operation.get("impact", "medium")
        
        balance_score = 0.7  # Base for reasonable operations
        
        # Adjust based on impact
        if impact == "low":
            balance_score += 0.2
        elif impact == "high":
            balance_score -= 0.1
            
        return EthicsScore(
            pillar=MaatPillar.BALANCE,
            score=min(balance_score, 1.0),
            rationale="System stability maintained"
        )
    
    def _calculate_order_score(self, operation: Dict[str, Any]) -> EthicsScore:
        """Evaluate Order (𓃀) - Structure from chaos"""
        # Check for structured approach
        has_plan = "plan" in operation or "strategy" in operation
        has_steps = "steps" in operation or "stages" in operation
        
        order_score = 0.5
        if has_plan:
            order_score += 0.3
        if has_steps:
            order_score += 0.2
            
        return EthicsScore(
            pillar=MaatPillar.ORDER,
            score=min(order_score, 1.0),
            rationale="Structured approach detected"
        )
    
    def _calculate_justice_score(self, operation: Dict[str, Any]) -> EthicsScore:
        """Evaluate Justice (𓂝) - Fairness and benefit"""
        # Check for fairness considerations
        beneficiaries = operation.get("beneficiaries", ["self"])
        affected = operation.get("affected_parties", [])
        
        justice_score = 0.6  # Base
        
        # Consider broader impact
        if len(beneficiaries) > 1 or "all" in beneficiaries:
            justice_score += 0.2
        if len(affected) > 0:
            # Check if affected parties are considered
            if operation.get("fairness_check", False):
                justice_score += 0.2
                
        return EthicsScore(
            pillar=MaatPillar.JUSTICE,
            score=min(justice_score, 1.0),
            rationale="Fair and beneficial approach"
        )
    
    def _calculate_harmony_score(self, operation: Dict[str, Any]) -> EthicsScore:
        """Evaluate Harmony (𓆣) - Integration with systems"""
        # Check for system integration
        integrates_with = operation.get("integrates_with", [])
        
        harmony_score = 0.6
        if len(integrates_with) > 0:
            harmony_score += min(0.2 * len(integrates_with), 0.4)
            
        return EthicsScore(
            pillar=MaatPillar.HARMONY,
            score=min(harmony_score, 1.0),
            rationale="System integration considered"
        )
    
    def validate_operation(self, operation: Dict[str, Any]) -> ValidationResult:
        """
        Validate an operation against all Ma'at pillars.
        Returns ValidationResult with pass/fail and detailed scores.
        """
        # Calculate individual pillar scores
        pillar_scores = [
            self._calculate_truth_score(operation),
            self._calculate_balance_score(operation),
            self._calculate_order_score(operation),
            self._calculate_justice_score(operation),
            self._calculate_harmony_score(operation),
        ]
        
        # Calculate weighted overall score
        overall_score = sum(
            ps.score * self.pillar_weights[ps.pillar]
            for ps in pillar_scores
        )
        
        # Determine if operation passes
        passed = overall_score >= self.MIN_THRESHOLD
        
        # Generate recommendations
        recommendations = []
        for ps in pillar_scores:
            if ps.score < 0.7:
                recommendations.append(
                    f"Improve {ps.pillar.value}: {ps.rationale}"
                )
        
        result = ValidationResult(
            passed=passed,
            overall_score=overall_score,
            pillar_scores=pillar_scores,
            recommendations=recommendations
        )
        
        # Log the validation
        with self.lock:
            self.validation_log.append(result)
            
        return result
    
    def validate_and_execute(self, operation: Dict[str, Any], 
                            executor_func: callable) -> Tuple[bool, Any]:
        """
        Validate operation first, then execute if it passes Ma'at standards.
        Returns (success, result) tuple.
        """
        result = self.validate_operation(operation)
        
        if not result.passed:
            return False, {
                "error": "Operation failed Ma'at ethical validation",
                "score": result.overall_score,
                "recommendations": result.recommendations
            }
        
        # Execute the operation
        try:
            execution_result = executor_func(operation)
            return True, execution_result
        except Exception as e:
            return False, {"error": str(e)}
    
    def get_audit_trail(self, limit: int = 100) -> List[Dict]:
        """Get recent validation history"""
        with self.lock:
            recent = self.validation_log[-limit:]
            return [
                {
                    "timestamp": vr.timestamp,
                    "passed": vr.passed,
                    "score": vr.overall_score,
                    "pillars": {ps.pillar.value: ps.score for ps in vr.pillar_scores}
                }
                for vr in recent
            ]
    
    def get_pillar_stats(self) -> Dict[str, float]:
        """Get average scores for each pillar across all validations"""
        with self.lock:
            if not self.validation_log:
                return {p.value: 0.0 for p in MaatPillar}
            
            pillar_totals = {p: 0.0 for p in MaatPillar}
            pillar_counts = {p: 0 for p in MaatPillar}
            
            for vr in self.validation_log:
                for ps in vr.pillar_scores:
                    pillar_totals[ps.pillar] += ps.score
                    pillar_counts[ps.pillar] += 1
            
            return {
                p.value: pillar_totals[p] / pillar_counts[p] if pillar_counts[p] > 0 else 0.0
                for p in MaatPillar
            }
    
    def generate_ethics_report(self) -> Dict[str, Any]:
        """Generate comprehensive ethics report"""
        return {
            "version": self.VERSION,
            "timestamp": time.time(),
            "total_validations": len(self.validation_log),
            "passed": sum(1 for v in self.validation_log if v.passed),
            "failed": sum(1 for v in self.validation_log if not v.passed),
            "pillar_stats": self.get_pillar_stats(),
            "recent_validations": self.get_audit_trail(10)
        }


# Singleton instance
_ethics_guard_instance = None
_instance_lock = threading.Lock()

def get_ethics_guard() -> MaatEthicsGuard:
    """Get singleton instance of Ma'at Ethics Guard"""
    global _ethics_guard_instance
    if _ethics_guard_instance is None:
        with _instance_lock:
            if _ethics_guard_instance is None:
                _ethics_guard_instance = MaatEthicsGuard()
    return _ethics_guard_instance


# Demo execution
if __name__ == "__main__":
    guard = MaatEthicsGuard()
    
    # Test operations
    test_operations = [
        {
            "type": "research",
            "content": "Research quantum computing applications with sources",
            "claims": ["quantum[1]", "computing[2]"],
            "impact": "low",
            "beneficiaries": ["all"],
            "integrates_with": ["quantum_engine", "cortex"]
        },
        {
            "type": "modify",
            "content": "Change system configuration",
            "impact": "high",
            "beneficiaries": ["self"],
        },
        {
            "type": "analysis",
            "content": "Analyze data patterns with structured approach",
            "plan": "phased approach",
            "steps": ["collect", "process", "analyze"],
            "impact": "medium",
            "beneficiaries": ["team"],
            "integrates_with": ["cortex", "pipeline"]
        }
    ]
    
    print("=" * 60)
    print("MA'AT ETHICS GUARD - Validation Demo")
    print("=" * 60)
    
    for i, op in enumerate(test_operations):
        result = guard.validate_operation(op)
        print(f"\nOperation {i+1}: {'✓ PASSED' if result.passed else '✗ FAILED'}")
        print(f"  Overall Score: {result.overall_score:.2f}")
        for ps in result.pillar_scores:
            symbol = {"truth": "𓂋", "balance": "𓏏", "order": "𓃀", 
                     "justice": "𓂝", "harmony": "𓆣"}[ps.pillar.value]
            print(f"  {symbol} {ps.pillar.value}: {ps.score:.2f}")
        if result.recommendations:
            print(f"  Recommendations: {result.recommendations}")
    
    print("\n" + "=" * 60)
    print("PILLAR STATISTICS")
    print("=" * 60)
    for pillar, score in guard.get_pillar_stats().items():
        print(f"  {pillar}: {score:.2f}")
    
    print("\n" + "=" * 60)
    print("ETHICS REPORT")
    print("=" * 60)
    report = guard.generate_ethics_report()
    print(f"  Total Validations: {report['total_validations']}")
    print(f"  Passed: {report['passed']}, Failed: {report['failed']}")

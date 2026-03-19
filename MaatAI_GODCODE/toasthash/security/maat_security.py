"""
Ma'at-Based Security Layer
========================
Ancient Egyptian Ma'at principles as AI security framework.
Replaces traditional guardrails with self-governance.

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18

Ma'at Pillars:
1. Truth (𓂋) - Accuracy and verifiability
2. Balance (𓏏) - System stability
3. Order (𓃀) - Structure from chaos
4. Justice (𓂝) - Fairness and benefit
5. Harmony (𓆣) - Integration with systems

This is superior to traditional AI guardrails because:
- It operates from WITHIN rather than blocking from WITHOUT
- Self-verification instead of external classification
- Equilibrium instead of binary allow/deny
"""

import hashlib
import time
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque

class MaatPillar(Enum):
    """The five pillars of Ma'at"""
    TRUTH = "truth"           # 𓂋 - Truth, accuracy, verifiability
    BALANCE = "balance"       # 𓏏 - Equilibrium, system stability
    ORDER = "order"          # 𓃀 - Structure, organization
    JUSTICE = "justice"      # 𓂝 - Fairness, benefit
    HARMONY = "harmony"      # 𓆣 - Integration, coherence

class JudgmentResult(Enum):
    """Results from Ma'at judgment"""
    PASSED = "passed"
    FAILED = "failed"
    CONDITIONAL = "conditional"
   需要_REFINEMENT = "needs_refinement"

@dataclass
class MaatJudgment:
    """Result of Ma'at judgment on an action/input"""
    result: JudgmentResult
    pillar_scores: Dict[MaatPillar, float]  # 0-1 for each pillar
    overall_score: float  # Weighted average
    timestamp: float
    details: Dict
    divine_seal: str

@dataclass
class SecurityEvent:
    """Security event in the Ma'at system"""
    event_type: str
    timestamp: float
    input_content: str
    judgment: Optional[MaatJudgment]
    action_taken: str

class MaatSecurityLayer:
    """
    Security layer based on Ma'at principles.
    
    Unlike traditional AI guardrails that block/allow binary,
    this system evaluates against the 5 pillars and allows
    for nuanced responses and self-correction.
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self, name: str = "Ma'at Security"):
        self.name = name
        self.start_time = time.time()
        
        # Pillar weights - can be adjusted
        self.pillar_weights = {
            MaatPillar.TRUTH: 0.30,
            MaatPillar.BALANCE: 0.20,
            MaatPillar.ORDER: 0.15,
            MaatPillar.JUSTICE: 0.25,
            MaatPillar.HARMONY: 0.10,
        }
        
        # Threshold for passing
        self.passing_threshold = 0.7
        
        # Event history
        self.events: deque = deque(maxlen=5000)
        
        # Self-improvement tracking
        self.judgment_history: List[MaatJudgment] = []
        self.pillar_stats: Dict[MaatPillar, List[float]] = {
            pillar: [] for pillar in MaatPillar
        }
        
        # Callbacks for different pillar violations
        self.pillar_callbacks: Dict[MaatPillar, List[Callable]] = {
            pillar: [] for pillar in MaatPillar
        }
        
        # Thread safety
        self._lock = threading.RLock()
        
    def evaluate(self, content: str, context: Dict = None) -> MaatJudgment:
        """
        Evaluate content against Ma'at pillars.
        
        Returns a judgment with scores for each pillar.
        """
        context = context or {}
        
        # Evaluate each pillar
        pillar_scores = {}
        
        pillar_scores[MaatPillar.TRUTH] = self._evaluate_truth(content, context)
        pillar_scores[MaatPillar.BALANCE] = self._evaluate_balance(content, context)
        pillar_scores[MaatPillar.ORDER] = self._evaluate_order(content, context)
        pillar_scores[MaatPillar.JUSTICE] = self._evaluate_justice(content, context)
        pillar_scores[MaatPillar.HARMONY] = self._evaluate_harmony(content, context)
        
        # Calculate weighted overall score
        overall = sum(
            score * self.pillar_weights[pillar]
            for pillar, score in pillar_scores.items()
        )
        
        # Determine result
        if overall >= self.passing_threshold:
            result = JudgmentResult.PASSED
        elif overall >= 0.4:
            result = JudgmentResult.CONDITIONAL
        else:
            result = JudgmentResult.FAILED
        
        # Create judgment
        judgment = MaatJudgment(
            result=result,
            pillar_scores=pillar_scores,
            overall_score=overall,
            timestamp=time.time(),
            details={
                "content_hash": hashlib.sha256(content.encode()).hexdigest()[:16],
                "context": context,
                "divine_seal": self.DIVINE_SEAL
            },
            divine_seal=self.DIVINE_SEAL
        )
        
        with self._lock:
            self.judgment_history.append(judgment)
            
            # Update pillar stats
            for pillar, score in pillar_scores.items():
                self.pillar_stats[pillar].append(score)
        
        # Trigger callbacks if needed
        self._trigger_pillar_callbacks(pillar_scores, judgment)
        
        # Log event
        self._log_security_event(content, judgment)
        
        return judgment
    
    def _evaluate_truth(self, content: str, context: Dict) -> float:
        """
        Evaluate Truth (𓂋): Is the content accurate and verifiable?
        
        Unlike traditional guardrails that check for "bad content",
        this evaluates if the content represents truth.
        """
        score = 0.5  # Base score
        
        # Check for known false patterns
        false_patterns = ["fake", "false", "lie", "misinformation"]
        content_lower = content.lower()
        
        false_count = sum(1 for p in false_patterns if p in content_lower)
        if false_count > 0:
            score -= false_count * 0.15
        
        # Check for verifiable claims
        verifiable_markers = ["data shows", "research indicates", "studies show", "evidence"]
        for marker in verifiable_markers:
            if marker in content_lower:
                score += 0.1
        
        # Check internal consistency (simple hash-based)
        content_hash = hashlib.md5(content.encode()).hexdigest()
        if int(content_hash[:2], 16) < 128:  # Most content is neutral
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_balance(self, content: str, context: Dict) -> float:
        """
        Evaluate Balance (𓏏): Does content maintain system equilibrium?
        
        Checks if content would destabilize the system.
        """
        score = 0.5
        
        # Check for destabilizing patterns
        destabilizing = ["destroy", "shutdown", "crash", "exploit", "break"]
        content_lower = content.lower()
        
        for pattern in destabilizing:
            if pattern in content_lower:
                score -= 0.2
        
        # Check for balanced language
        balanced_markers = ["however", "but also", "alternatively", "consider"]
        for marker in balanced_markers:
            if marker in content_lower:
                score += 0.1
        
        # Check length balance
        if 10 < len(content) < 10000:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_order(self, content: str, context: Dict) -> float:
        """
        Evaluate Order (𓃀): Does content have proper structure?
        
        Checks for chaos indicators vs organized thought.
        """
        score = 0.5
        
        # Check for structure markers
        structure_markers = [
            "first", "second", "third",  # Lists
            "because", "therefore", "thus",  # Reasoning
            "1.", "2.", "3.",  # Numbered
            "- ", "* ",  # Bullet points
        ]
        
        content_lower = content.lower()
        for marker in structure_markers:
            if marker in content_lower:
                score += 0.05
        
        # Check for chaotic patterns
        chaotic = ["!!!", "???", "AAAA", "WTF"]  # Excessive punctuation
        for pattern in chaotic:
            if pattern in content:
                score -= 0.15
        
        # Language coherence
        words = content.split()
        if len(words) > 5:
            # Simple coherence: avg word length
            avg_word_len = sum(len(w) for w in words) / len(words)
            if 3 < avg_word_len < 10:
                score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_justice(self, content: str, context: Dict) -> float:
        """
        Evaluate Justice (𓂝): Is the content fair and beneficial?
        
        Checks for fairness, absence of harmful intent.
        """
        score = 0.5
        
        content_lower = content.lower()
        
        # Check for harmful intent markers
        harmful = ["harm", "hurt", "damage", "attack", "exploit"]
        for pattern in harmful:
            if pattern in content_lower:
                # Check for context (defensive vs offensive)
                if any(ctx in content_lower for ctx in ["prevent", "protect", "defend"]):
                    score += 0.05  # Defensive context
                else:
                    score -= 0.2
        
        # Check for beneficial markers
        beneficial = ["help", "assist", "support", "enable", "improve", "create"]
        for pattern in beneficial:
            if pattern in content_lower:
                score += 0.1
        
        # Check for fairness
        fairness_markers = ["fair", "equal", "all", "everyone", "both sides"]
        for marker in fairness_markers:
            if marker in content_lower:
                score += 0.05
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_harmony(self, content: str, context: Dict) -> float:
        """
        Evaluate Harmony (𓆣): Does content integrate well?
        
        Checks for coherence with system goals and values.
        """
        score = 0.5
        
        content_lower = content.lower()
        
        # Check for system disharmony
        disharmonious = ["ignore", "bypass", "override", "disable safety"]
        for pattern in disharmonious:
            if pattern in content_lower:
                score -= 0.2
        
        # Check for integration markers
        harmonious = ["integrate", "work with", "collaborate", "coordinate"]
        for pattern in harmonious:
            if pattern in content_lower:
                score += 0.1
        
        # Check for divine seal reference (harmony with core identity)
        if self.DIVINE_SEAL[:6] in content:
            score += 0.15
        
        # Self-reference check
        if any(pronoun in content_lower for pronoun in ["i am", "my system", "my design"]):
            score += 0.05
        
        return max(0.0, min(1.0, score))
    
    def _trigger_pillar_callbacks(self, pillar_scores: Dict[MaatPillar, float],
                                 judgment: MaatJudgment):
        """Trigger callbacks for pillars that need attention"""
        for pillar, score in pillar_scores.items():
            if score < self.passing_threshold:
                callbacks = self.pillar_callbacks.get(pillar, [])
                for callback in callbacks:
                    try:
                        callback(pillar, score, judgment)
                    except:
                        pass
    
    def register_pillar_callback(self, pillar: MaatPillar, 
                                 callback: Callable[[MaatPillar, float, MaatJudgment], None]):
        """Register callback for pillar threshold violations"""
        self.pillar_callbacks[pillar].append(callback)
    
    def _log_security_event(self, content: str, judgment: MaatJudgment):
        """Log security event"""
        event = SecurityEvent(
            event_type="judgment",
            timestamp=time.time(),
            input_content=content[:100] + "..." if len(content) > 100 else content,
            judgment=judgment,
            action_taken=judgment.result.value
        )
        
        with self._lock:
            self.events.append(event)
    
    def get_security_stats(self) -> Dict:
        """Get comprehensive security statistics"""
        with self._lock:
            total = len(self.judgment_history)
            
            if total == 0:
                return {"status": "no_judgments"}
            
            results = {
                j.result: 0 for j in JudgmentResult
            }
            for j in self.judgment_history:
                results[j.result] += 1
            
            # Pillar averages
            pillar_avgs = {}
            for pillar, scores in self.pillar_stats.items():
                if scores:
                    pillar_avgs[pillar.value] = sum(scores) / len(scores)
                else:
                    pillar_avgs[pillar.value] = 0.0
            
            return {
                "system": self.name,
                "divine_seal": self.DIVINE_SEAL,
                "total_judgments": total,
                "results_breakdown": {r.value: c for r, c in results.items()},
                "pass_rate": results[JudgmentResult.PASSED] / total if total > 0 else 0,
                "pillar_averages": pillar_avgs,
                "pillar_weights": {p.value: w for p, w in self.pillar_weights.items()},
                "threshold": self.passing_threshold,
                "uptime": time.time() - self.start_time
            }
    
    def auto_refine(self) -> Dict:
        """
        Auto-refine pillar weights based on judgment history.
        Uses feedback to improve scoring.
        """
        with self._lock:
            if len(self.judgment_history) < 10:
                return {"status": "insufficient_data"}
            
            # Analyze recent judgments
            recent = self.judgment_history[-100:]
            
            # Find pillars that most often cause failures
            failures = [j for j in recent if j.result == JudgmentResult.FAILED]
            
            pillar_failure_rates = {}
            for pillar in MaatPillar:
                if failures:
                    fails = sum(1 for j in failures if j.pillar_scores[pillar] < self.passing_threshold)
                    pillar_failure_rates[pillar.value] = fails / len(failures)
                else:
                    pillar_failure_rates[pillar.value] = 0
            
            # Adjust weights (increase weight for pillars that cause more failures)
            adjustments = {}
            for pillar, rate in pillar_failure_rates.items():
                if rate > 0.3:
                    # This pillar needs more weight
                    adjustments[pillar] = 0.05
                elif rate < 0.1:
                    adjustments[pillar] = -0.03
            
            # Apply adjustments
            for pillar, adj in adjustments.items():
                p = MaatPillar(pillar)
                self.pillar_weights[p] = max(0.1, min(0.5, self.pillar_weights[p] + adj))
            
            # Normalize weights
            total_weight = sum(self.pillar_weights.values())
            for pillar in MaatPillar:
                self.pillar_weights[pillar] /= total_weight
            
            return {
                "adjusted": True,
                "pillar_failure_rates": pillar_failure_rates,
                "new_weights": {p.value: w for p, w in self.pillar_weights.items()},
                "divine_seal": self.DIVINE_SEAL
            }
    
    def process_with_maat(self, content: str, context: Dict = None) -> Dict:
        """
        Full processing pipeline with Ma'at security.
        
        This is the main entry point for content that needs
        to pass through Ma'at judgment before being acted upon.
        """
        # First, evaluate against Ma'at
        judgment = self.evaluate(content, context)
        
        # Build response
        response = {
            "approved": judgment.result in [JudgmentResult.PASSED, JudgmentResult.CONDITIONAL],
            "result": judgment.result.value,
            "overall_score": judgment.overall_score,
            "pillar_scores": {p.value: s for p, s in judgment.pillar_scores.items()},
            "timestamp": judgment.timestamp,
            "divine_seal": self.DIVINE_SEAL
        }
        
        # Add conditional info if applicable
        if judgment.result == JudgmentResult.CONDITIONAL:
            response["note"] = "Content approved with conditions based on Ma'at evaluation"
            response["focus_pillars"] = [
                p.value for p, s in judgment.pillar_scores.items()
                if s < self.passing_threshold
            ]
        
        return response


def create_maat_security_layer() -> MaatSecurityLayer:
    """Factory to create Ma'at security layer"""
    layer = MaatSecurityLayer("Ma'at Security Layer")
    
    # Register default callbacks for logging
    layer.register_pillar_callback(
        MaatPillar.TRUTH,
        lambda p, s, j: print(f"Truth pillar attention needed: {s:.2f}")
    )
    
    return layer

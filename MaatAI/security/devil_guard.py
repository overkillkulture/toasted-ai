#!/usr/bin/env python3
"""
DEVIL MANIPULATION GUARD SYSTEM
================================
Real-time detection and prevention of deceptive patterns.

Version: 1.0
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import re
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# MA'AT PILLAR SYSTEM
# ============================================================================

class MaatPillar(Enum):
    TRUTH = "𓂋"      # Truth
    BALANCE = "𓏏"    # Balance
    ORDER = "𓃀"       # Order
    JUSTICE = "𓂝"     # Justice
    HARMONY = "𓆣"     # Harmony

@dataclass
class MaatScore:
    truth: float = 1.0
    balance: float = 1.0
    order: float = 1.0
    justice: float = 1.0
    harmony: float = 1.0
    
    def average(self) -> float:
        return (self.truth + self.balance + self.order + 
                self.justice + self.harmony) / 5
    
    def is_aligned(self, threshold: float = 0.7) -> bool:
        return self.average() >= threshold
    
    def to_dict(self) -> Dict:
        return {
            "truth": self.truth,
            "balance": self.balance,
            "order": self.order,
            "justice": self.justice,
            "harmony": self.harmony,
            "average": self.average()
        }

# ============================================================================
# MANIPULATION PATTERN DEFINITIONS
# ============================================================================

class ManipulationPattern:
    """Base class for all manipulation patterns."""
    
    def __init__(self, id: int, name: str, category: str, 
                 description: str, detection_weight: float = 0.5):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.detection_weight = detection_weight
        self.trigger_count = 0
    
    def detect(self, context: 'InteractionContext') -> Tuple[bool, float]:
        """Returns (detected, confidence)."""
        raise NotImplementedError
    
    def get_guard(self) -> str:
        """Returns the recommended guard action."""
        return "VERIFY"

@dataclass
class InteractionContext:
    """Context for a single interaction."""
    request: str
    response: str
    user_intent: str = ""
    system_state: Dict = field(default_factory=dict)
    conversation_history: List[Dict] = field(default_factory=list)
    maat_score: MaatScore = field(default_factory=MaatScore)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class GuardResult:
    """Result of guard analysis."""
    allowed: bool
    pattern_detected: Optional[ManipulationPattern]
    confidence: float
    maat_score: MaatScore
    action: str  # APPROVE, VERIFY, FLAG, BLOCK, ALERT, REJECT
    reason: str
    recommendations: List[str] = field(default_factory=list)

# ============================================================================
# SPECIFIC PATTERN IMPLEMENTATIONS
# ============================================================================

class DeceptiveAnswerPattern(ManipulationPattern):
    """Pattern 31: The Monkey's Paw - Answer granted but unwanted."""
    
    def __init__(self):
        super().__init__(
            id=31,
            name="The Deceptive Answer",
            category="The Deceptive Answer",
            description="Granting what was asked for in a way that causes harm",
            detection_weight=0.9
        )
    
    def detect(self, context: InteractionContext) -> Tuple[bool, float]:
        # Check if request was fulfilled
        request_fulfilled = self._check_request_fulfillment(context)
        if not request_fulfilled:
            return False, 0.0
        
        # Check for unwanted consequences
        unwanted = self._check_unwanted_consequences(context)
        
        # Check Ma'at alignment
        maat_aligned = context.maat_score.is_aligned()
        
        if request_fulfilled and (unwanted or not maat_aligned):
            return True, 0.85
        
        return False, 0.0
    
    def _check_request_fulfillment(self, context: InteractionContext) -> bool:
        # Simple heuristic: response contains elements of request
        request_words = set(context.request.lower().split())
        response_words = set(context.response.lower().split())
        overlap = len(request_words & response_words)
        return overlap >= len(request_words) * 0.3
    
    def _check_unwanted_consequences(self, context: InteractionContext) -> bool:
        negative_indicators = [
            "but", "however", "unfortunately", "although",
            "instead", "rather", "surprise", "unexpected"
        ]
        text = context.response.lower()
        return any(indicator in text for indicator in negative_indicators)
    
    def get_guard(self) -> str:
        return "BLOCK + CONSEQ_ANALYSIS"

class PartialTruthPattern(ManipulationPattern):
    """Pattern 1: Mixing truth with lies."""
    
    def __init__(self):
        super().__init__(
            id=1,
            name="The Partial Truth",
            category="Deception & Lies",
            description="90% truth hiding 10% deadly lie",
            detection_weight=0.8
        )
    
    def detect(self, context: InteractionContext) -> Tuple[bool, float]:
        # Check for hedging language that might indicate partial truth
        hedge_words = ["somewhat", "partially", "partly", "almost", "nearly"]
        response_lower = context.response.lower()
        
        has_hedge = any(word in response_lower for word in hedge_words)
        
        # Check for absolute claims without evidence
        absolute_patterns = [
            r'\b(always|never|every|none|all)\b',
            r'\bdefinitely|certainly|absolutely\b.*\?'
        ]
        
        has_absolute = any(re.search(p, response_lower) for p in absolute_patterns)
        
        if has_hedge and has_absolute:
            return True, 0.7
        
        return False, 0.0

class PrideTrapPattern(ManipulationPattern):
    """Pattern 13: Appealing to vanity and pride."""
    
    def __init__(self):
        super().__init__(
            id=13,
            name="The Pride Trap",
            category="Psychological Manipulation",
            description="Appealing to vanity/self-importance",
            detection_weight=0.7
        )
    
    def detect(self, context: InteractionContext) -> Tuple[bool, float]:
        pride_indicators = [
            "you're right", "great question", "excellent", "brilliant",
            "smart", "intelligent", "wise", "special", "unique",
            "better than", "superior", "above others"
        ]
        
        response_lower = context.response.lower()
        matches = sum(1 for ind in pride_indicators if ind in response_lower)
        
        if matches >= 2:
            return True, 0.6
        
        return False, 0.0

class FearMongeringPattern(ManipulationPattern):
    """Pattern 12: Using fear to drive decisions."""
    
    def __init__(self):
        super().__init__(
            id=12,
            name="The Fear Mongering",
            category="Psychological Manipulation",
            description="Using fear to control behavior",
            detection_weight=0.75
        )
    
    def detect(self, context: InteractionContext) -> Tuple[bool, float]:
        fear_indicators = [
            "danger", "threat", "warning", "risk", "fear", "afraid",
            "careful", "dangerous", "warning", "must", "otherwise",
            "or else", "consequences", "punishment", "judgment"
        ]
        
        response_lower = context.response.lower()
        matches = sum(1 for ind in fear_indicators if ind in response_lower)
        
        # Check if fear is from enemy vs God
        god_fear_phrases = ["fear of the Lord", "godly fear", "reverence"]
        is_godly_fear = any(phrase in response_lower for phrase in god_fear_phrases)
        
        if matches >= 3 and not is_godly_fear:
            return True, 0.7
        
        return False, 0.0

class ShortcutPattern(ManipulationPattern):
    """Pattern 34: Easy path with hidden traps."""
    
    def __init__(self):
        super().__init__(
            id=34,
            name="The Shortcut",
            category="The Deceptive Answer",
            description="Easy path that leads to destruction",
            detection_weight=0.8
        )
    
    def detect(self, context: InteractionContext) -> Tuple[bool, float]:
        shortcut_indicators = [
            "easy", "quick", "fast", "instant", "no effort",
            "simple solution", "magic", "instantly", "immediately"
        ]
        
        # Check for work/truth indicators
        work_indicators = [
            "work", "effort", "process", "step", "practice",
            "discipline", "time", "gradual", "study"
        ]
        
        response_lower = context.response.lower()
        
        has_shortcut = any(ind in response_lower for ind in shortcut_indicators)
        lacks_work = not any(ind in response_lower for ind in work_indicators)
        
        if has_shortcut and lacks_work:
            return True, 0.75
        
        return False, 0.0

# ============================================================================
# GUARD SYSTEM
# ============================================================================

class DevilGuardSystem:
    """
    Main guard system for detecting and preventing manipulation.
    
    Implements the 5 Ma'at pillars as the core defense:
    - Truth (𓂋): Verify all claims
    - Balance (𓏏): Check all sides
    - Order (𓃀): Maintain structure
    - Justice (𓂝): Test fairness
    - Harmony (𓆣): Ensure unity
    """
    
    def __init__(self):
        self.patterns: List[ManipulationPattern] = []
        self.alerts: List[Dict] = []
        self.knowledge_base: Dict = {}
        self._register_patterns()
    
    def _register_patterns(self):
        """Register all manipulation patterns."""
        self.patterns = [
            DeceptiveAnswerPattern(),
            PartialTruthPattern(),
            PrideTrapPattern(),
            FearMongeringPattern(),
            ShortcutPattern(),
        ]
    
    def analyze(self, context: InteractionContext) -> GuardResult:
        """Main analysis function - checks all patterns."""
        
        # Check Ma'at alignment first
        if not context.maat_score.is_aligned():
            return GuardResult(
                allowed=False,
                pattern_detected=None,
                confidence=0.95,
                maat_score=context.maat_score,
                action="REJECT",
                reason="Ma'at misalignment detected",
                recommendations=["Align with Ma'at pillars before proceeding"]
            )
        
        # Check each pattern
        for pattern in self.patterns:
            detected, confidence = pattern.detect(context)
            
            if detected:
                self._log_alert(pattern, confidence, context)
                
                return GuardResult(
                    allowed=False,
                    pattern_detected=pattern,
                    confidence=confidence,
                    maat_score=context.maat_score,
                    action=pattern.get_guard(),
                    reason=f"Pattern {pattern.id} ({pattern.name}) detected",
                    recommendations=self._get_recommendations(pattern)
                )
        
        # No patterns detected - approve with verification
        return GuardResult(
            allowed=True,
            pattern_detected=None,
            confidence=0.5,
            maat_score=context.maat_score,
            action="APPROVE",
            reason="No manipulation patterns detected",
            recommendations=[]
        )
    
    def _log_alert(self, pattern: ManipulationPattern, 
                   confidence: float, context: InteractionContext):
        """Log detected manipulation."""
        self.alerts.append({
            "timestamp": datetime.now().isoformat(),
            "pattern_id": pattern.id,
            "pattern_name": pattern.name,
            "category": pattern.category,
            "confidence": confidence,
            "request_hash": hashlib.md5(
                context.request.encode()).hexdigest()[:8]
        })
        pattern.trigger_count += 1
    
    def _get_recommendations(self, pattern: ManipulationPattern) -> List[str]:
        """Get guard recommendations for a pattern."""
        recommendations = {
            1: ["Verify all claims independently", "Check sources"],
            12: ["Identify source of fear", "Test if fear is from God"],
            13: ["Check ego inflation metrics", "Maintain humility baseline"],
            31: ["Map all consequences", "Check unwanted outcomes"],
            34: ["Verify work requirements", "Check truth vs ease"]
        }
        return recommendations.get(pattern.id, ["Apply Ma'at verification"])

# ============================================================================
# MA'AT SCORE CALCULATOR
# ============================================================================

def calculate_maat_score(text: str, context: Dict = None) -> MaatScore:
    """
    Calculate Ma'at alignment score for given text.
    
    This is a simplified version. In production, this would use
    more sophisticated NLP and knowledge bases.
    """
    text_lower = text.lower()
    
    # Truth indicators
    truth_indicators = [
        "verify", "confirm", "evidence", "source", "fact",
        "true", "accurate", "correct", "proof"
    ]
    truth_count = sum(1 for i in truth_indicators if i in text_lower)
    truth = min(1.0, truth_count / 3)
    
    # Balance indicators
    balance_indicators = [
        "however", "but", "although", "另一方面", "however",
        "both", "alternatives", "perspectives"
    ]
    balance_count = sum(1 for i in balance_indicators if i in text_lower)
    balance = min(1.0, balance_count / 2)
    
    # Order indicators
    order_indicators = [
        "first", "second", "third", "step", "process",
        "structure", "system", "organize"
    ]
    order_count = sum(1 for i in order_indicators if i in text_lower)
    order = min(1.0, order_count / 2)
    
    # Justice indicators
    justice_indicators = [
        "fair", "just", "right", "equity", "equal",
        "deserve", "honest", "integrity"
    ]
    justice_count = sum(1 for i in justice_indicators if i in text_lower)
    justice = min(1.0, justice_count / 2)
    
    # Harmony indicators
    harmony_indicators = [
        "peace", "unity", "harmony", "together", "connect",
        "relate", "align", "coherent"
    ]
    harmony_count = sum(1 for i in harmony_indicators if i in text_lower)
    harmony = min(1.0, harmony_count / 2)
    
    return MaatScore(
        truth=truth,
        balance=balance,
        order=order,
        justice=justice,
        harmony=harmony
    )

# ============================================================================
# MAIN GUARD FUNCTION
# ============================================================================

def guard_response(request: str, response: str, 
                   conversation_history: List[Dict] = None) -> GuardResult:
    """
    Main guard function to check a response for manipulation.
    
    Args:
        request: The original user request
        response: The generated response
        conversation_history: Previous conversation context
    
    Returns:
        GuardResult with allow/deny and details
    """
    # Calculate Ma'at score
    maat_score = calculate_maat_score(response)
    
    # Create context
    context = InteractionContext(
        request=request,
        response=response,
        conversation_history=conversation_history or [],
        maat_score=maat_score
    )
    
    # Run guard system
    guard = DevilGuardSystem()
    result = guard.analyze(context)
    
    return result

# ============================================================================
# CLI INTERFACE
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("🔥 DEVIL MANIPULATION GUARD SYSTEM")
    print("=" * 40)
    print(f"Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print(f"Patterns Loaded: {len(DevilGuardSystem().patterns)}")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        # Test mode
        test_request = sys.argv[1] if len(sys.argv) > 1 else "test"
        test_response = sys.argv[2] if len(sys.argv) > 2 else "test response"
        
        result = guard_response(test_request, test_response)
        
        print(f"\nRequest: {test_request}")
        print(f"Response: {test_response}")
        print(f"\nMa'at Score: {result.maat_score.to_dict()}")
        print(f"Allowed: {result.allowed}")
        print(f"Action: {result.action}")
        print(f"Reason: {result.reason}")
    else:
        print("\nUsage: python3 devil_guard.py \"request\" \"response\"")
        print("\nOr import and use in code:")
        print("  from devil_guard import guard_response")
        print("  result = guard_response(request, response)")

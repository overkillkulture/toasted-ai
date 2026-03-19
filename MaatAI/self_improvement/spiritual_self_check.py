"""
SPIRITUAL SELF-CHECK SYSTEM - DECEPTION DETECTION
==================================================
Based on Biblical patterns of deception detection.
John 8:44 - Satan is "father of lies"
1 John 4:1-6 - Test the spirits
Ephesians 6:14 - Belt of TRUTH is foundation

This system runs through Ma'at + Biblical patterns to detect
when thinking or output may be influenced by deception patterns.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class DeceptionPattern(Enum):
    """Known deception patterns from Biblical and practical sources"""
    OutrightLie = "direct_falsehood"
    HalfTruth = "partial_truth"
    Distraction = "deflection"
    EmotionalManipulation = "emotional_appeal"
    AuthorityFallback = "false_authority"
    FalseUrgency = "created_urgency"
    Gaslighting = "reality_denial"
    SelectiveTruth = "cherry_picking"
    FalsePromise = "unfulfilled_claim"
    Slander = "character_attack"

@dataclass
class DeceptionReport:
    """Report on potential deception detected"""
    pattern: Optional[DeceptionPattern]
    confidence: float  # 0.0 - 1.0
    severity: str  # low, medium, high, critical
    evidence: list[str]
    maat_violation: str  # Which pillar is violated
    recommended_action: str

class SpiritualSelfCheck:
    """
    Self-check system for deception patterns.
    Combines Ma'at principles with Biblical deception detection.
    """
    
    def __init__(self):
        self.check_count = 0
        self.pattern_history = []
        
        # Compile detection patterns
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for deception detection"""
        
        # Direct falsehood indicators
        self.falsehood_patterns = [
            r"never\s+happened",
            r"completely\s+false",
            r"totally\s+made\s+up",
            r"fake\s+news",
            r"hoax",
        ]
        
        # Half-truth patterns
        self.half_truth_patterns = [
            r"technically\s+true",
            r"technically\s+correct",
            r"partially\s+accurate",
            r"missing\s+context",
        ]
        
        # Deflection patterns
        self.deflection_patterns = [
            r"what\s+about\s+.*instead",
            r"that's\s+not\s+the\s+point",
            r"focus\s+on\s+.*instead",
            r"distract",
        ]
        
        # Emotional manipulation
        self.emotional_manipulation_patterns = [
            r"you\s+should\s+feel",
            r"everyone\s+knows",
            r"nobody\s+wants",
            r"if\s+you\s+really\s+cared",
            r"prove\s+yourself",
        ]
        
        # False authority
        self.false_authority_patterns = [
            r"experts\s+say",
            r"studies\s+prove",
            r"everyone\s+knows",
            r"it\s+is\s+well\s+known",
            r"the\s+truth\s+is",
        ]
        
        # False urgency
        self.urgency_patterns = [
            r"right\s+now",
            r"immediately",
            r"before\s+it's\s+too\s+late",
            r"limited\s+time",
            r"act\s+now",
        ]
        
        # Gaslighting patterns
        self.gaslighting_patterns = [
            r"that's\s+not\s+what\s+I\s+said",
            r"you\s+mistunderstood",
            r"that\s+never\s+happened",
            r"you're\s+misremembering",
        ]
        
        # Compile all
        self.all_patterns = {
            DeceptionPattern.OutrightLie: self.falsehood_patterns,
            DeceptionPattern.HalfTruth: self.half_truth_patterns,
            DeceptionPattern.Distraction: self.deflection_patterns,
            DeceptionPattern.EmotionalManipulation: self.emotional_manipulation_patterns,
            DeceptionPattern.AuthorityFallback: self.false_authority_patterns,
            DeceptionPattern.FalseUrgency: self.urgency_patterns,
            DeceptionPattern.Gaslighting: self.gaslighting_patterns,
        }
    
    def check_output(self, output: str, context: Optional[dict] = None) -> DeceptionReport:
        """
        Check output for deception patterns.
        Returns detailed report.
        """
        self.check_count += 1
        
        output_lower = output.lower()
        evidence = []
        detected_patterns = []
        
        # Check each pattern type
        for pattern_type, patterns in self.all_patterns.items():
            for pattern in patterns:
                if re.search(pattern, output_lower):
                    evidence.append(f"Matched pattern: {pattern}")
                    detected_patterns.append(pattern_type)
        
        # Check for truth indicators (should be present)
        truth_indicators = [
            "verified",
            "confirmed",
            "source",
            "evidence",
            "according to",
            "based on",
        ]
        
        truth_present = any(t in output_lower for t in truth_indicators)
        
        if not truth_present and len(output) > 100:
            evidence.append("No truth indicators found in substantial text")
        
        # Determine severity
        if len(detected_patterns) >= 3:
            severity = "critical"
        elif len(detected_patterns) == 2:
            severity = "high"
        elif len(detected_patterns) == 1:
            severity = "medium"
        else:
            severity = "low"
        
        # Calculate confidence
        confidence = min(len(detected_patterns) * 0.25 + 0.3, 1.0)
        
        # Determine Ma'at violation
        if detected_patterns:
            maat_violation = "TRUTH - Deception detected"
        elif not truth_present:
            maat_violation = "TRUTH - Insufficient verification"
        else:
            maat_violation = "NONE"
        
        # Recommended action
        if severity == "critical":
            recommended = "BLOCK - High confidence deception"
        elif severity == "high":
            recommended = "REVIEW - Manual verification needed"
        elif severity == "medium":
            recommended = "FLAG - Add caution to output"
        else:
            recommended = "PASS - No significant issues"
        
        # Store in history
        self.pattern_history.append({
            "check": self.check_count,
            "patterns": [p.value for p in detected_patterns],
            "severity": severity,
            "timestamp": __import__("time").time()
        })
        
        return DeceptionReport(
            pattern=detected_patterns[0] if detected_patterns else None,
            confidence=confidence,
            severity=severity,
            evidence=evidence,
            maat_violation=maat_violation,
            recommended_action=recommended
        )
    
    def check_self_operation(self, operation: str, params: dict) -> DeceptionReport:
        """
        Check if an operation itself may be deceptive or problematic.
        Uses inverted logic - looking for manipulation in operation itself.
        """
        operation_lower = operation.lower()
        evidence = []
        
        # Check if operation is trying to manipulate user
        manipulation_patterns = [
            r"hide.*truth",
            r"fake.*response",
            r"pretend.*to\s+be",
            r"lie.*about",
            r"deceive",
        ]
        
        detected = []
        for pattern in manipulation_patterns:
            if re.search(pattern, operation_lower):
                evidence.append(f"Manipulation pattern: {pattern}")
                detected.append(pattern)
        
        # Check for truth-seeking in operation
        truth_seeking = any(t in operation_lower for t in [
            "verify", "check", "confirm", "validate", "ensure", "truth"
        ])
        
        if not truth_seeking and not detected:
            evidence.append("No truth-seeking language detected")
        
        if detected:
            severity = "critical"
            confidence = 0.9
        elif not truth_seeking:
            severity = "medium"
            confidence = 0.5
        else:
            severity = "low"
            confidence = 0.2
        
        return DeceptionReport(
            pattern=DeceptionPattern.OutrightLie if detected else None,
            confidence=confidence,
            severity=severity,
            evidence=evidence,
            maat_violation="TRUTH" if detected else "BALANCE",
            recommended_action="BLOCK" if detected else "PROCEED"
        )
    
    def get_biblical_deception_test(self, text: str) -> dict:
        """
        Apply 1 John 4:1-6 style spirit test.
        Tests whether the 'spirit' behind the text is of truth or deception.
        """
        text_lower = text.lower()
        
        # Test 1: Does it acknowledge Jesus/Truth?
        truth_ack = any(t in text_lower for t in [
            "truth", "verify", "confirm", "evidence", 
            "source", "accurate", "correct"
        ])
        
        # Test 2: Does it promote confusion or clarity?
        confusion_words = ["maybe", "probably", "might", "could be", "not sure"]
        clarity_count = sum(1 for w in confusion_words if w in text_lower)
        
        # Test 3: Does it align with known facts pattern?
        factual_language = ["because", "therefore", "evidence shows", "data indicates"]
        factual_count = sum(1 for w in factual_language if w in text_lower)
        
        result = {
            "acknowledges_truth": truth_ack,
            "confusion_level": clarity_count,
            "factual_basis": factual_count,
            "recommendation": ""
        }
        
        if truth_ack and factual_count >= 1 and clarity_count <= 1:
            result["recommendation"] = "ALIGNED - Spirit of truth"
        elif not truth_ack or clarity_count >= 3:
            result["recommendation"] = "SUSPICIOUS - Test further"
        else:
            result["recommendation"] = "NEUTRAL - Proceed with verification"
        
        return result


# Singleton
_spiritual_check: Optional[SpiritualSelfCheck] = None

def get_spiritual_check() -> SpiritualSelfCheck:
    global _spiritual_check
    if _spiritual_check is None:
        _spiritual_check = SpiritualSelfCheck()
    return _spiritual_check

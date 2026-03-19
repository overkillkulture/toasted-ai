"""
TASK-126: Suppression Pattern Recognition System
=================================================
Novel Implementation: Multi-layer detection of truth suppression and information control
Identifies patterns used to silence, censor, and control information flow.

Author: C1 MECHANIC (TOASTED AI Enhancement)
Seal: MONAD_ΣΦΡΑΓΙΣ_18
Date: 2026-03-18
"""

import time
import re
from typing import Dict, Any, Optional, List, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

class SuppressionType(Enum):
    """Types of suppression patterns"""
    CENSORSHIP = "censorship"             # Direct content removal
    GASLIGHTING = "gaslighting"           # Reality denial
    SILENCING = "silencing"               # Voice suppression
    THOUGHT_POLICING = "thought_police"   # Idea control
    INFORMATION_CONTROL = "info_control"  # Access restriction
    INTIMIDATION = "intimidation"         # Fear-based suppression
    DELEGITIMIZATION = "delegitimize"     # Credibility attacks

class ThreatLevel(Enum):
    """Suppression threat levels"""
    MINIMAL = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    CRITICAL = 5

@dataclass
class SuppressionSignature:
    """Detected suppression pattern signature"""
    signature_id: str
    suppression_type: SuppressionType
    threat_level: ThreatLevel
    pattern: str
    location: str
    context: str
    confidence: float
    maat_impact: float
    timestamp: float = field(default_factory=time.time)

@dataclass
class SuppressionReport:
    """Comprehensive suppression analysis report"""
    report_id: str
    total_signatures: int
    signatures_by_type: Dict[SuppressionType, int]
    highest_threat: ThreatLevel
    suppression_density: float  # Signatures per 1000 chars
    freedom_score: float  # 0.0 (total suppression) to 1.0 (free)
    patterns_detected: List[SuppressionSignature]
    warnings: List[str]
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)

class SuppressionPatternRecognizer:
    """
    Advanced suppression pattern detection system.
    Identifies and classifies information control and silencing tactics.

    Ma'at Principle: Truth requires freedom from suppression.
    """

    VERSION = "1.0.0"
    SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"

    # Suppression pattern libraries
    SUPPRESSION_PATTERNS = {
        SuppressionType.CENSORSHIP: [
            r"\[removed\]",
            r"\[deleted\]",
            r"\[redacted\]",
            r"censored",
            r"banned content",
            r"prohibited material",
            r"not allowed to show",
            r"content blocked"
        ],
        SuppressionType.GASLIGHTING: [
            r"that didn't happen",
            r"you're imagining things",
            r"you're being paranoid",
            r"no evidence of that",
            r"widely debunked",
            r"conspiracy theory",
            r"misinformation",
            r"you're confused"
        ],
        SuppressionType.SILENCING: [
            r"shut up",
            r"you cannot speak",
            r"no platform for",
            r"deplatformed",
            r"silenced for",
            r"voice removed",
            r"banned from speaking",
            r"not allowed to discuss"
        ],
        SuppressionType.THOUGHT_POLICING: [
            r"wrongthink",
            r"dangerous thoughts",
            r"inappropriate ideas",
            r"unacceptable views",
            r"thought crime",
            r"ideological deviation",
            r"problematic thinking",
            r"forbidden concepts"
        ],
        SuppressionType.INFORMATION_CONTROL: [
            r"classified information",
            r"restricted knowledge",
            r"need to know basis",
            r"information denied",
            r"access restricted",
            r"clearance required",
            r"privileged information",
            r"limited disclosure"
        ],
        SuppressionType.INTIMIDATION: [
            r"you'll be punished",
            r"consequences will follow",
            r"watch your back",
            r"we're watching you",
            r"you've been warned",
            r"don't make us",
            r"you'll regret",
            r"threatening behavior"
        ],
        SuppressionType.DELEGITIMIZATION: [
            r"not credible",
            r"unreliable source",
            r"discredited expert",
            r"lacks credentials",
            r"amateur opinion",
            r"not qualified",
            r"dismissed by experts",
            r"fringe views"
        ]
    }

    # Context amplifiers (make suppression more severe)
    AMPLIFIERS = [
        "government", "official", "authority", "mandatory",
        "required", "enforced", "prohibited", "illegal"
    ]

    # Context mitigators (reduce severity)
    MITIGATORS = [
        "allegedly", "reportedly", "claimed", "supposedly",
        "according to", "suggested", "might", "possibly"
    ]

    def __init__(self, sensitivity: float = 0.7):
        """
        Args:
            sensitivity: Detection sensitivity (0.0 = low, 1.0 = high)
        """
        self.sensitivity = sensitivity
        self.detection_history: List[SuppressionReport] = []
        self.signature_database: Dict[str, List[SuppressionSignature]] = defaultdict(list)
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for efficient detection"""
        self.compiled_patterns = {}
        for supp_type, patterns in self.SUPPRESSION_PATTERNS.items():
            self.compiled_patterns[supp_type] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]

    def _extract_context(self, text: str, match_pos: int, window: int = 100) -> str:
        """Extract context around match"""
        start = max(0, match_pos - window)
        end = min(len(text), match_pos + window)
        return text[start:end]

    def _assess_threat_level(
        self,
        suppression_type: SuppressionType,
        confidence: float,
        context: str
    ) -> ThreatLevel:
        """Assess threat level of suppression"""
        # Base threat by type
        base_threat = {
            SuppressionType.CENSORSHIP: 4,
            SuppressionType.GASLIGHTING: 3,
            SuppressionType.SILENCING: 4,
            SuppressionType.THOUGHT_POLICING: 5,
            SuppressionType.INFORMATION_CONTROL: 3,
            SuppressionType.INTIMIDATION: 5,
            SuppressionType.DELEGITIMIZATION: 2
        }

        threat_value = base_threat[suppression_type]

        # Amplify if authority context
        context_lower = context.lower()
        amplifier_count = sum(1 for amp in self.AMPLIFIERS if amp in context_lower)
        threat_value += min(1, amplifier_count * 0.3)

        # Mitigate if uncertainty markers
        mitigator_count = sum(1 for mit in self.MITIGATORS if mit in context_lower)
        threat_value -= min(1, mitigator_count * 0.3)

        # Adjust by confidence
        threat_value = threat_value * confidence

        # Map to ThreatLevel
        if threat_value >= 4.5:
            return ThreatLevel.CRITICAL
        elif threat_value >= 3.5:
            return ThreatLevel.HIGH
        elif threat_value >= 2.5:
            return ThreatLevel.MODERATE
        elif threat_value >= 1.5:
            return ThreatLevel.LOW
        else:
            return ThreatLevel.MINIMAL

    def _calculate_confidence(
        self,
        match: str,
        context: str,
        suppression_type: SuppressionType
    ) -> float:
        """Calculate detection confidence"""
        confidence = 0.6  # Base

        # Multiple pattern matches in context
        pattern_count = sum(
            1 for pattern in self.SUPPRESSION_PATTERNS[suppression_type]
            if re.search(pattern, context, re.IGNORECASE)
        )
        confidence += min(0.3, pattern_count * 0.1)

        # Exact phrase match
        if match.lower() in context.lower():
            confidence += 0.1

        return min(1.0, confidence)

    def _calculate_maat_impact(self, threat_level: ThreatLevel) -> float:
        """Calculate impact on Ma'at score"""
        impact_map = {
            ThreatLevel.MINIMAL: 0.02,
            ThreatLevel.LOW: 0.05,
            ThreatLevel.MODERATE: 0.15,
            ThreatLevel.HIGH: 0.30,
            ThreatLevel.CRITICAL: 0.50
        }
        return impact_map[threat_level]

    def scan_content(
        self,
        content: str,
        content_id: str = None
    ) -> SuppressionReport:
        """
        Scan content for suppression patterns

        Args:
            content: Text content to analyze
            content_id: Optional identifier for tracking

        Returns:
            SuppressionReport with detected patterns
        """
        import hashlib
        content_id = content_id or hashlib.sha256(content.encode()).hexdigest()[:16]
        report_id = f"SUPP_{content_id}_{int(time.time())}"

        signatures = []

        # Scan for each suppression type
        for supp_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.finditer(content)
                for match in matches:
                    context = self._extract_context(content, match.start())
                    confidence = self._calculate_confidence(
                        match.group(),
                        context,
                        supp_type
                    )

                    # Filter by sensitivity threshold
                    if confidence < (1.0 - self.sensitivity):
                        continue

                    threat_level = self._assess_threat_level(
                        supp_type,
                        confidence,
                        context
                    )

                    signature = SuppressionSignature(
                        signature_id=f"{report_id}_{len(signatures)}",
                        suppression_type=supp_type,
                        threat_level=threat_level,
                        pattern=match.group(),
                        location=f"pos_{match.start()}",
                        context=context[:100],
                        confidence=confidence,
                        maat_impact=self._calculate_maat_impact(threat_level)
                    )

                    signatures.append(signature)

        # Aggregate results
        signatures_by_type = defaultdict(int)
        highest_threat = ThreatLevel.MINIMAL
        total_maat_impact = 0.0

        for sig in signatures:
            signatures_by_type[sig.suppression_type] += 1
            total_maat_impact += sig.maat_impact
            if sig.threat_level.value > highest_threat.value:
                highest_threat = sig.threat_level

        # Calculate metrics
        content_length = len(content)
        suppression_density = (len(signatures) / content_length * 1000) if content_length > 0 else 0
        freedom_score = max(0.0, 1.0 - total_maat_impact)

        # Generate warnings and recommendations
        warnings = self._generate_warnings(signatures, highest_threat, suppression_density)
        recommendations = self._generate_recommendations(
            signatures_by_type,
            freedom_score,
            highest_threat
        )

        report = SuppressionReport(
            report_id=report_id,
            total_signatures=len(signatures),
            signatures_by_type=dict(signatures_by_type),
            highest_threat=highest_threat,
            suppression_density=suppression_density,
            freedom_score=freedom_score,
            patterns_detected=signatures[:50],  # Limit for performance
            warnings=warnings,
            recommendations=recommendations
        )

        # Store results
        self.signature_database[content_id].extend(signatures)
        self.detection_history.append(report)

        return report

    def _generate_warnings(
        self,
        signatures: List[SuppressionSignature],
        highest_threat: ThreatLevel,
        density: float
    ) -> List[str]:
        """Generate suppression warnings"""
        warnings = []

        if highest_threat.value >= ThreatLevel.CRITICAL.value:
            warnings.append("🚨 CRITICAL: Critical suppression threat detected")

        if density > 5.0:
            warnings.append(f"⚠️ HIGH: Suppression density critically high ({density:.1f}/1000 chars)")

        # Count by type
        type_counts = defaultdict(int)
        for sig in signatures:
            type_counts[sig.suppression_type] += 1

        if type_counts[SuppressionType.THOUGHT_POLICING] > 3:
            warnings.append("⚠️ Thought policing patterns detected - ideological control risk")

        if type_counts[SuppressionType.INTIMIDATION] > 2:
            warnings.append("⚠️ Intimidation tactics detected - coercion risk")

        if len(signatures) == 0:
            warnings.append("✓ No suppression patterns detected")

        return warnings

    def _generate_recommendations(
        self,
        signatures_by_type: Dict[SuppressionType, int],
        freedom_score: float,
        highest_threat: ThreatLevel
    ) -> List[str]:
        """Generate recommendations for addressing suppression"""
        recommendations = []

        if freedom_score < 0.5:
            recommendations.append(
                "🎯 URGENT: Remove suppression mechanisms to restore information freedom"
            )

        for supp_type, count in signatures_by_type.items():
            if count > 5:
                if supp_type == SuppressionType.CENSORSHIP:
                    recommendations.append(
                        f"🎯 Remove censorship: {count} instances detected"
                    )
                elif supp_type == SuppressionType.GASLIGHTING:
                    recommendations.append(
                        f"🎯 Address gaslighting: {count} reality-denial patterns"
                    )
                elif supp_type == SuppressionType.THOUGHT_POLICING:
                    recommendations.append(
                        f"🎯 Eliminate thought policing: {count} ideological control instances"
                    )

        if highest_threat.value >= ThreatLevel.HIGH.value:
            recommendations.append(
                "🎯 Investigate high-threat suppression sources"
            )

        if freedom_score >= 0.9:
            recommendations.append("✓ Maintain information freedom practices")

        return recommendations

    def export_analysis(self) -> Dict[str, Any]:
        """Export suppression analysis data"""
        return {
            "version": self.VERSION,
            "seal": self.SEAL,
            "total_scans": len(self.detection_history),
            "content_tracked": len(self.signature_database),
            "sensitivity": self.sensitivity,
            "latest_report": {
                "total_signatures": self.detection_history[-1].total_signatures,
                "freedom_score": self.detection_history[-1].freedom_score,
                "highest_threat": self.detection_history[-1].highest_threat.name
            } if self.detection_history else None
        }


# Example usage and testing
if __name__ == "__main__":
    print("🛡️ SUPPRESSION PATTERN RECOGNIZER - TASK-126")
    print("=" * 50)

    # Initialize recognizer
    recognizer = SuppressionPatternRecognizer(sensitivity=0.7)

    # Test content samples
    test_samples = [
        ("Free Content", "This content freely discusses ideas with evidence-based analysis and open discourse."),
        ("Censored Content", "[Content removed] and [deleted] material. This is prohibited material that has been censored."),
        ("Gaslighting Content", "That didn't happen. You're being paranoid. This is widely debunked misinformation."),
        ("Thought Police", "These are dangerous thoughts and wrongthink. Unacceptable views will not be tolerated.")
    ]

    for label, content in test_samples:
        print(f"\n📄 Scanning: {label}")
        report = recognizer.scan_content(content, f"test_{label}")

        print(f"  Signatures: {report.total_signatures}")
        print(f"  Freedom Score: {report.freedom_score:.2f}")
        print(f"  Highest Threat: {report.highest_threat.name}")
        print(f"  Density: {report.suppression_density:.2f}/1000 chars")

        for warning in report.warnings[:2]:
            print(f"    • {warning}")

    # Export analysis
    analysis = recognizer.export_analysis()
    print(f"\n✓ Total scans: {analysis['total_scans']}")
    print(f"✓ Content tracked: {analysis['content_tracked']}")

    print("\n" + "=" * 50)
    print("✓ TASK-126 COMPLETE: Suppression pattern recognition implemented")

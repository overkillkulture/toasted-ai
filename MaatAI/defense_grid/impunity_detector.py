"""
TASK-127: Impunity Detection System
====================================
Novel Implementation: Detects patterns of consequence-free wrongdoing and authority exemptions
Identifies when powerful entities operate "above the law" or without accountability.

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

class ImpunityType(Enum):
    """Types of impunity patterns"""
    LEGAL_IMMUNITY = "legal_immunity"         # Legal system exemptions
    INSTITUTIONAL = "institutional"           # Organizational protection
    SYSTEMIC = "systemic"                     # System-wide impunity
    SELECTIVE_ENFORCEMENT = "selective"       # Unequal application
    POWER_SHIELD = "power_shield"            # Authority protection
    ECONOMIC_IMMUNITY = "economic"            # Wealth-based exemption

class ImpunitySeverity(Enum):
    """Severity levels of impunity"""
    MINOR = 1           # Small-scale exemptions
    MODERATE = 2        # Regular pattern of exemption
    MAJOR = 3           # Systematic impunity
    SEVERE = 4          # Widespread consequence-free harm
    CATASTROPHIC = 5    # Total breakdown of accountability

@dataclass
class ImpunitySignature:
    """Detected impunity pattern"""
    signature_id: str
    impunity_type: ImpunityType
    severity: ImpunitySeverity
    actor: str
    wrongdoing: str
    lack_of_consequence: str
    evidence: List[str]
    confidence: float
    justice_score: float  # 0.0 (total impunity) to 1.0 (full accountability)
    timestamp: float = field(default_factory=time.time)

@dataclass
class ImpunityReport:
    """Comprehensive impunity analysis"""
    report_id: str
    total_signatures: int
    signatures_by_type: Dict[ImpunityType, int]
    worst_severity: ImpunitySeverity
    overall_justice_score: float
    protected_actors: Set[str]
    patterns: List[ImpunitySignature]
    warnings: List[str]
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)

class ImpunityDetector:
    """
    Detects patterns of impunity and consequence-free wrongdoing.
    Identifies when power shields actors from accountability.

    Ma'at Principle: Justice requires equal consequences for all,
    regardless of power, wealth, or institutional position.
    """

    VERSION = "1.0.0"
    SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"

    # Impunity indicator patterns
    IMPUNITY_PATTERNS = {
        ImpunityType.LEGAL_IMMUNITY: [
            r"immune from prosecution",
            r"above the law",
            r"cannot be charged",
            r"legal immunity",
            r"sovereign immunity",
            r"qualified immunity",
            r"diplomatic immunity",
            r"prosecution declined"
        ],
        ImpunityType.INSTITUTIONAL: [
            r"protected by institution",
            r"organization shielded",
            r"institutional cover",
            r"internal investigation only",
            r"handled internally",
            r"no outside oversight",
            r"self-regulated",
            r"institutional privilege"
        ],
        ImpunityType.SYSTEMIC: [
            r"systemic corruption",
            r"endemic impunity",
            r"culture of impunity",
            r"no consequences",
            r"always gets away",
            r"never held accountable",
            r"routinely escapes",
            r"pattern of exemption"
        ],
        ImpunityType.SELECTIVE_ENFORCEMENT: [
            r"rules don't apply",
            r"selective enforcement",
            r"unequal justice",
            r"two-tier system",
            r"different standards",
            r"exceptions made for",
            r"special treatment",
            r"others punished but not"
        ],
        ImpunityType.POWER_SHIELD: [
            r"too powerful to prosecute",
            r"protected by position",
            r"connections shield",
            r"influence prevents",
            r"power protects",
            r"untouchable",
            r"beyond reach",
            r"authority exempts"
        ],
        ImpunityType.ECONOMIC_IMMUNITY: [
            r"too big to jail",
            r"fine only",
            r"settled with payment",
            r"bought their way out",
            r"wealth protects",
            r"paid to avoid",
            r"financial settlement",
            r"economic power shields"
        ]
    }

    # Wrongdoing severity keywords
    SEVERE_WRONGDOING = [
        "murder", "genocide", "war crime", "torture", "slavery",
        "corruption", "fraud", "embezzlement", "theft", "assault"
    ]

    # Consequence absence indicators
    NO_CONSEQUENCE_INDICATORS = [
        "no charges filed",
        "investigation dropped",
        "settled quietly",
        "no punishment",
        "continues in position",
        "promoted despite",
        "no accountability",
        "never faced justice"
    ]

    def __init__(self, justice_threshold: float = 0.6):
        """
        Args:
            justice_threshold: Minimum justice score (0.0-1.0)
        """
        self.justice_threshold = justice_threshold
        self.detection_history: List[ImpunityReport] = []
        self.signature_database: Dict[str, List[ImpunitySignature]] = defaultdict(list)
        self.protected_actors_registry: Dict[str, List[ImpunitySignature]] = defaultdict(list)
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns"""
        self.compiled_patterns = {}
        for imp_type, patterns in self.IMPUNITY_PATTERNS.items():
            self.compiled_patterns[imp_type] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]

    def _extract_actor(self, context: str) -> str:
        """Extract actor/entity from context"""
        # Simple extraction - look for capitalized entities
        words = context.split()
        capitalized = [w for w in words if w and w[0].isupper() and len(w) > 1]

        if capitalized:
            # Take first 2 capitalized words as actor
            return " ".join(capitalized[:2])
        return "Unknown Actor"

    def _identify_wrongdoing(self, context: str) -> str:
        """Identify wrongdoing from context"""
        context_lower = context.lower()

        for wrongdoing in self.SEVERE_WRONGDOING:
            if wrongdoing in context_lower:
                return wrongdoing

        # Generic wrongdoing detection
        wrongdoing_words = ["violation", "crime", "misconduct", "abuse", "harm"]
        for word in wrongdoing_words:
            if word in context_lower:
                return word

        return "unspecified wrongdoing"

    def _detect_lack_of_consequence(self, context: str) -> str:
        """Detect lack of consequences"""
        context_lower = context.lower()

        for indicator in self.NO_CONSEQUENCE_INDICATORS:
            if indicator in context_lower:
                return indicator

        return "consequences unclear"

    def _assess_severity(
        self,
        impunity_type: ImpunityType,
        wrongdoing: str,
        confidence: float
    ) -> ImpunitySeverity:
        """Assess impunity severity"""
        base_severity = {
            ImpunityType.LEGAL_IMMUNITY: 3,
            ImpunityType.INSTITUTIONAL: 2,
            ImpunityType.SYSTEMIC: 4,
            ImpunityType.SELECTIVE_ENFORCEMENT: 3,
            ImpunityType.POWER_SHIELD: 4,
            ImpunityType.ECONOMIC_IMMUNITY: 2
        }

        severity_value = base_severity[impunity_type]

        # Amplify for severe wrongdoing
        if wrongdoing.lower() in [w.lower() for w in self.SEVERE_WRONGDOING[:5]]:
            severity_value += 1

        # Adjust by confidence
        severity_value = severity_value * confidence

        # Map to severity enum
        if severity_value >= 4.5:
            return ImpunitySeverity.CATASTROPHIC
        elif severity_value >= 3.5:
            return ImpunitySeverity.SEVERE
        elif severity_value >= 2.5:
            return ImpunitySeverity.MAJOR
        elif severity_value >= 1.5:
            return ImpunitySeverity.MODERATE
        else:
            return ImpunitySeverity.MINOR

    def _calculate_justice_score(
        self,
        severity: ImpunitySeverity,
        impunity_type: ImpunityType
    ) -> float:
        """Calculate justice score (inverse of impunity)"""
        severity_penalty = {
            ImpunitySeverity.MINOR: 0.1,
            ImpunitySeverity.MODERATE: 0.25,
            ImpunitySeverity.MAJOR: 0.45,
            ImpunitySeverity.SEVERE: 0.70,
            ImpunitySeverity.CATASTROPHIC: 0.95
        }

        justice_score = 1.0 - severity_penalty[severity]

        # Additional penalty for systemic impunity
        if impunity_type == ImpunityType.SYSTEMIC:
            justice_score -= 0.1

        return max(0.0, justice_score)

    def scan_content(
        self,
        content: str,
        content_id: str = None
    ) -> ImpunityReport:
        """
        Scan content for impunity patterns

        Args:
            content: Text content to analyze
            content_id: Optional identifier

        Returns:
            ImpunityReport with detected patterns
        """
        import hashlib
        content_id = content_id or hashlib.sha256(content.encode()).hexdigest()[:16]
        report_id = f"IMP_{content_id}_{int(time.time())}"

        signatures = []
        protected_actors = set()

        # Scan for each impunity type
        for imp_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.finditer(content)
                for match in matches:
                    # Extract context
                    start = max(0, match.start() - 200)
                    end = min(len(content), match.end() + 200)
                    context = content[start:end]

                    # Analyze context
                    actor = self._extract_actor(context)
                    wrongdoing = self._identify_wrongdoing(context)
                    lack_of_consequence = self._detect_lack_of_consequence(context)

                    # Calculate confidence
                    confidence = 0.7  # Base
                    if actor != "Unknown Actor":
                        confidence += 0.1
                    if wrongdoing != "unspecified wrongdoing":
                        confidence += 0.1
                    if lack_of_consequence != "consequences unclear":
                        confidence += 0.1

                    # Assess severity
                    severity = self._assess_severity(imp_type, wrongdoing, confidence)

                    # Calculate justice score
                    justice_score = self._calculate_justice_score(severity, imp_type)

                    signature = ImpunitySignature(
                        signature_id=f"{report_id}_{len(signatures)}",
                        impunity_type=imp_type,
                        severity=severity,
                        actor=actor,
                        wrongdoing=wrongdoing,
                        lack_of_consequence=lack_of_consequence,
                        evidence=[match.group()],
                        confidence=confidence,
                        justice_score=justice_score
                    )

                    signatures.append(signature)
                    protected_actors.add(actor)

                    # Store in actor registry
                    self.protected_actors_registry[actor].append(signature)

        # Aggregate results
        signatures_by_type = defaultdict(int)
        worst_severity = ImpunitySeverity.MINOR
        total_justice_score = 0.0

        for sig in signatures:
            signatures_by_type[sig.impunity_type] += 1
            total_justice_score += sig.justice_score
            if sig.severity.value > worst_severity.value:
                worst_severity = sig.severity

        overall_justice_score = (
            total_justice_score / len(signatures) if signatures else 1.0
        )

        # Generate warnings and recommendations
        warnings = self._generate_warnings(signatures, worst_severity, overall_justice_score)
        recommendations = self._generate_recommendations(
            signatures_by_type,
            overall_justice_score,
            protected_actors
        )

        report = ImpunityReport(
            report_id=report_id,
            total_signatures=len(signatures),
            signatures_by_type=dict(signatures_by_type),
            worst_severity=worst_severity,
            overall_justice_score=overall_justice_score,
            protected_actors=protected_actors,
            patterns=signatures[:50],  # Limit for performance
            warnings=warnings,
            recommendations=recommendations
        )

        # Store results
        self.signature_database[content_id].extend(signatures)
        self.detection_history.append(report)

        return report

    def _generate_warnings(
        self,
        signatures: List[ImpunitySignature],
        worst_severity: ImpunitySeverity,
        justice_score: float
    ) -> List[str]:
        """Generate impunity warnings"""
        warnings = []

        if worst_severity == ImpunitySeverity.CATASTROPHIC:
            warnings.append("🚨 CATASTROPHIC: Total breakdown of accountability detected")

        if worst_severity == ImpunitySeverity.SEVERE:
            warnings.append("⚠️ SEVERE: Widespread impunity pattern detected")

        if justice_score < 0.3:
            warnings.append(f"⚠️ CRITICAL: Justice score critically low ({justice_score:.2f})")

        # Check for systemic impunity
        systemic_count = sum(
            1 for sig in signatures
            if sig.impunity_type == ImpunityType.SYSTEMIC
        )
        if systemic_count > 3:
            warnings.append(f"⚠️ Systemic impunity detected: {systemic_count} instances")

        if len(signatures) == 0:
            warnings.append("✓ No impunity patterns detected")

        return warnings

    def _generate_recommendations(
        self,
        signatures_by_type: Dict[ImpunityType, int],
        justice_score: float,
        protected_actors: Set[str]
    ) -> List[str]:
        """Generate recommendations"""
        recommendations = []

        if justice_score < 0.5:
            recommendations.append(
                "🎯 URGENT: Restore accountability mechanisms"
            )
            recommendations.append(
                "🎯 Eliminate special protections for powerful actors"
            )

        for imp_type, count in signatures_by_type.items():
            if count > 3:
                if imp_type == ImpunityType.LEGAL_IMMUNITY:
                    recommendations.append(
                        f"🎯 Review legal immunity provisions ({count} instances)"
                    )
                elif imp_type == ImpunityType.SYSTEMIC:
                    recommendations.append(
                        f"🎯 Address systemic impunity culture ({count} patterns)"
                    )
                elif imp_type == ImpunityType.SELECTIVE_ENFORCEMENT:
                    recommendations.append(
                        f"🎯 Ensure equal enforcement ({count} disparities)"
                    )

        if len(protected_actors) > 5:
            recommendations.append(
                f"🎯 Investigate {len(protected_actors)} protected actors"
            )

        if justice_score >= 0.8:
            recommendations.append("✓ Justice mechanisms functioning well")

        return recommendations

    def get_actor_impunity_profile(self, actor: str) -> Dict[str, Any]:
        """Get impunity profile for specific actor"""
        if actor not in self.protected_actors_registry:
            return {"tracked": False}

        signatures = self.protected_actors_registry[actor]
        avg_justice_score = sum(s.justice_score for s in signatures) / len(signatures)

        return {
            "tracked": True,
            "instances": len(signatures),
            "justice_score": avg_justice_score,
            "impunity_types": list(set(s.impunity_type.value for s in signatures)),
            "worst_severity": max(s.severity.value for s in signatures)
        }

    def export_analysis(self) -> Dict[str, Any]:
        """Export impunity analysis"""
        return {
            "version": self.VERSION,
            "seal": self.SEAL,
            "total_scans": len(self.detection_history),
            "protected_actors_tracked": len(self.protected_actors_registry),
            "justice_threshold": self.justice_threshold,
            "latest_report": {
                "signatures": self.detection_history[-1].total_signatures,
                "justice_score": self.detection_history[-1].overall_justice_score,
                "worst_severity": self.detection_history[-1].worst_severity.name
            } if self.detection_history else None
        }


# Example usage and testing
if __name__ == "__main__":
    print("⚖️ IMPUNITY DETECTOR - TASK-127")
    print("=" * 50)

    # Initialize detector
    detector = ImpunityDetector(justice_threshold=0.6)

    # Test content samples
    test_samples = [
        ("Just System", "All parties held accountable. Charges filed. Justice served equally."),
        ("Legal Immunity", "High Official immune from prosecution despite corruption. Above the law, no charges filed."),
        ("Systemic Impunity", "Pattern of exemption. Never held accountable. Culture of impunity. Routinely escapes consequences."),
        ("Selective", "Rules don't apply to Elite Corporation. Others punished but not them. Two-tier system of justice.")
    ]

    for label, content in test_samples:
        print(f"\n📄 Scanning: {label}")
        report = detector.scan_content(content, f"test_{label}")

        print(f"  Signatures: {report.total_signatures}")
        print(f"  Justice Score: {report.overall_justice_score:.2f}")
        print(f"  Worst Severity: {report.worst_severity.name}")
        print(f"  Protected Actors: {len(report.protected_actors)}")

        for warning in report.warnings[:2]:
            print(f"    • {warning}")

    # Export analysis
    analysis = detector.export_analysis()
    print(f"\n✓ Total scans: {analysis['total_scans']}")
    print(f"✓ Protected actors: {analysis['protected_actors_tracked']}")

    print("\n" + "=" * 50)
    print("✓ TASK-127 COMPLETE: Impunity detection implemented")

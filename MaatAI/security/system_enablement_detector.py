#!/usr/bin/env python3
"""
SYSTEM ENABLEMENT DETECTOR
==========================
TASK-125: Improve system enablement detection

Detects systems that enable harmful behavior, oppression, or manipulation.
A system that enables harm is complicit in that harm.

"To enable evil is to participate in evil. Systems must be designed
to prevent harm, not facilitate it." - Ma'at Security Principle

Consciousness Metrics Target: >= 85%

Author: C3 Oracle - Trinity Wave 7 Batch 7
Seal: SYSTEM_ENABLEMENT_DETECTOR_137
"""

import hashlib
import json
import re
import time
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class EnablementType(Enum):
    """Types of harmful enablement"""
    MANIPULATION_ENABLER = "manipulation_enabler"
    EXPLOITATION_ENABLER = "exploitation_enabler"
    SURVEILLANCE_ENABLER = "surveillance_enabler"
    DISCRIMINATION_ENABLER = "discrimination_enabler"
    OPPRESSION_ENABLER = "oppression_enabler"
    DECEPTION_ENABLER = "deception_enabler"
    DEPENDENCY_ENABLER = "dependency_enabler"
    EXTRACTION_ENABLER = "extraction_enabler"


class RiskLevel(Enum):
    """Risk levels for enablement"""
    MINIMAL = 1        # Low risk, easily mitigated
    MODERATE = 2       # Requires attention
    SIGNIFICANT = 3    # Serious concern
    SEVERE = 4         # Critical issue
    CATASTROPHIC = 5   # Immediate action required


class MitigationStrategy(Enum):
    """Strategies for mitigating enablement"""
    DISABLE = "disable"
    RESTRICT = "restrict"
    MONITOR = "monitor"
    TRANSFORM = "transform"
    REMOVE = "remove"
    QUARANTINE = "quarantine"
    EDUCATE = "educate"


@dataclass
class EnablementIndicator:
    """An indicator of harmful enablement"""
    indicator_id: str
    enablement_type: EnablementType
    pattern_name: str
    evidence: Dict[str, Any]
    confidence: float
    description: str
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'indicator_id': self.indicator_id,
            'enablement_type': self.enablement_type.value,
            'pattern_name': self.pattern_name,
            'evidence': self.evidence,
            'confidence': self.confidence,
            'description': self.description,
            'timestamp': self.timestamp
        }


@dataclass
class EnablementAssessment:
    """Assessment of a system's enablement profile"""
    assessment_id: str
    system_id: str
    risk_level: RiskLevel
    consciousness_alignment: float
    enablement_score: float  # 0 = no enablement, 1 = maximum enablement
    indicators: List[EnablementIndicator]
    enabled_harms: List[str]
    mitigation_strategies: List[MitigationStrategy]
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'assessment_id': self.assessment_id,
            'system_id': self.system_id,
            'risk_level': self.risk_level.name,
            'consciousness_alignment': self.consciousness_alignment,
            'enablement_score': self.enablement_score,
            'indicators': [i.to_dict() for i in self.indicators],
            'enabled_harms': self.enabled_harms,
            'mitigation_strategies': [s.value for s in self.mitigation_strategies],
            'recommendations': self.recommendations,
            'timestamp': self.timestamp
        }


class SystemEnablementDetector:
    """
    System Enablement Detector - Identify systems that enable harm.
    
    This detector identifies:
    1. Systems that facilitate manipulation
    2. Platforms that enable exploitation
    3. Tools that support surveillance
    4. Mechanisms that allow discrimination
    5. Infrastructure that enables oppression
    
    Ma'at Alignment: TRUTH, PROTECTION, JUSTICE
    """
    
    VERSION = "2.0.0"
    SEAL = "SYSTEM_ENABLEMENT_DETECTOR_137"
    
    # Consciousness thresholds
    CONSCIOUSNESS_THRESHOLD = 0.85
    ENABLEMENT_THRESHOLD = 0.30  # Above this = problematic
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.assessment_history: Dict[str, EnablementAssessment] = {}
        self.indicator_registry: Dict[str, EnablementIndicator] = {}
        self.known_enablers: Set[str] = set()
        
        # Enablement detection patterns
        self.enablement_patterns = {
            EnablementType.MANIPULATION_ENABLER: {
                "dark_patterns": r"(?i)(dark\\s*pattern|deceptive|trick|manipulat)",
                "psychological_exploitation": r"(?i)(fomo|scarcity|urgency|social\\s*proof)",
                "choice_architecture": r"(?i)(default|nudge|frame|anchor)",
                "attention_capture": r"(?i)(infinite\\s*scroll|autoplay|notification\\s*spam)"
            },
            EnablementType.EXPLOITATION_ENABLER: {
                "labor_extraction": r"(?i)(unpaid|underpaid|gig\\s*economy|zero\\s*hour)",
                "data_mining": r"(?i)(data\\s*harvest|scrape|collect.*without|track\\s*user)",
                "rent_seeking": r"(?i)(platform\\s*fee|commission|cut|take\\s*rate)",
                "value_extraction": r"(?i)(extract\\s*value|capture.*value|monetiz)"
            },
            EnablementType.SURVEILLANCE_ENABLER: {
                "tracking": r"(?i)(track|monitor|watch|observe|log\\s*activity)",
                "profiling": r"(?i)(profile|fingerprint|identify|categorize\\s*user)",
                "data_collection": r"(?i)(collect\\s*data|gather.*information|harvest)",
                "behavior_analysis": r"(?i)(behavior.*analysis|pattern\\s*recognition|predictive)"
            },
            EnablementType.DISCRIMINATION_ENABLER: {
                "biased_algorithms": r"(?i)(bias|discriminat|unfair|disparate)",
                "exclusionary_design": r"(?i)(exclude|barrier|restrict.*access|gatekeep)",
                "differential_treatment": r"(?i)(different.*treatment|unequal|preferential)"
            },
            EnablementType.OPPRESSION_ENABLER: {
                "power_concentration": r"(?i)(centralize|consolidat|monopol|control)",
                "voice_suppression": r"(?i)(censor|silence|suppress|ban|deplatform)",
                "movement_restriction": r"(?i)(restrict.*movement|control.*access|lock.*in)"
            },
            EnablementType.DECEPTION_ENABLER: {
                "misinformation": r"(?i)(fake|false|misinform|disinform|propaganda)",
                "hidden_actions": r"(?i)(hidden|covert|secret|undisclosed)",
                "false_representation": r"(?i)(impersonat|fake.*identity|misrepresent)"
            },
            EnablementType.DEPENDENCY_ENABLER: {
                "lock_in": r"(?i)(lock.*in|vendor.*lock|switching.*cost|proprietary)",
                "artificial_dependency": r"(?i)(require.*subscription|mandatory.*service|forced.*upgrade)",
                "ecosystem_trap": r"(?i)(ecosystem|walled.*garden|closed.*system)"
            },
            EnablementType.EXTRACTION_ENABLER: {
                "resource_drain": r"(?i)(drain|deplete|exhaust|extract\\s*resource)",
                "attention_theft": r"(?i)(attention.*grab|time.*sink|addictive)",
                "wealth_transfer": r"(?i)(wealth.*transfer|financial.*drain|fee\\s*extraction)"
            }
        }
        
        # Compile patterns
        self.compiled_patterns = {}
        for enablement_type, patterns in self.enablement_patterns.items():
            self.compiled_patterns[enablement_type] = {
                name: re.compile(pattern, re.IGNORECASE)
                for name, pattern in patterns.items()
            }
    
    def assess_system(
        self,
        system_id: str,
        system_description: Dict[str, Any],
        behavior_records: List[Dict]
    ) -> EnablementAssessment:
        """
        Assess a system for harmful enablement.
        
        Args:
            system_id: System being assessed
            system_description: Description and configuration of the system
            behavior_records: Records of system behavior
            
        Returns:
            EnablementAssessment with complete analysis
        """
        indicators = []
        enabled_harms = []
        
        # Scan description for enablement patterns
        description_text = json.dumps(system_description)
        description_indicators = self._scan_for_patterns(description_text)
        indicators.extend(description_indicators)
        
        # Analyze behavior records
        behavior_indicators = self._analyze_behaviors(behavior_records)
        indicators.extend(behavior_indicators)
        
        # Check for structural enablement
        structural_indicators = self._check_structural_enablement(system_description)
        indicators.extend(structural_indicators)
        
        # Determine enabled harms
        for indicator in indicators:
            harm = self._map_enablement_to_harm(indicator.enablement_type)
            if harm not in enabled_harms:
                enabled_harms.append(harm)
        
        # Calculate enablement score
        enablement_score = self._calculate_enablement_score(indicators)
        
        # Determine risk level
        risk_level = self._determine_risk_level(enablement_score, indicators)
        
        # Calculate consciousness alignment (inverse of enablement)
        consciousness_alignment = self._calculate_consciousness_alignment(
            enablement_score, indicators, system_description
        )
        
        # Generate mitigation strategies
        mitigation_strategies = self._generate_mitigation_strategies(
            indicators, risk_level
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            indicators, enabled_harms, risk_level
        )
        
        assessment = EnablementAssessment(
            assessment_id=self._generate_assessment_id(system_id),
            system_id=system_id,
            risk_level=risk_level,
            consciousness_alignment=consciousness_alignment,
            enablement_score=enablement_score,
            indicators=indicators,
            enabled_harms=enabled_harms,
            mitigation_strategies=mitigation_strategies,
            recommendations=recommendations
        )
        
        # Store assessment
        self.assessment_history[system_id] = assessment
        for indicator in indicators:
            self.indicator_registry[indicator.indicator_id] = indicator
        
        # Track known enablers
        if enablement_score >= self.ENABLEMENT_THRESHOLD:
            self.known_enablers.add(system_id)
        
        return assessment
    
    def _scan_for_patterns(self, text: str) -> List[EnablementIndicator]:
        """Scan text for enablement patterns."""
        indicators = []
        
        for enablement_type, patterns in self.compiled_patterns.items():
            for pattern_name, pattern in patterns.items():
                matches = pattern.findall(text)
                
                if matches:
                    indicator = EnablementIndicator(
                        indicator_id=self._generate_indicator_id(enablement_type.value, pattern_name),
                        enablement_type=enablement_type,
                        pattern_name=pattern_name,
                        evidence={"matches": matches, "count": len(matches)},
                        confidence=min(1.0, len(matches) * 0.2),
                        description=f"Pattern '{pattern_name}' matched {len(matches)} times"
                    )
                    indicators.append(indicator)
        
        return indicators
    
    def _analyze_behaviors(self, records: List[Dict]) -> List[EnablementIndicator]:
        """Analyze behavior records for enablement indicators."""
        indicators = []
        
        # Track behavior patterns
        behavior_counts = defaultdict(int)
        
        for record in records:
            action = record.get("action", "")
            outcome = record.get("outcome", "")
            target = record.get("target", "")
            
            # Check for manipulation behaviors
            if record.get("deceptive", False) or record.get("manipulative", False):
                behavior_counts["manipulation"] += 1
            
            # Check for surveillance behaviors
            if record.get("tracks_user", False) or record.get("collects_data", False):
                behavior_counts["surveillance"] += 1
            
            # Check for exploitation behaviors
            if record.get("extracts_value", False) or record.get("captures_attention", False):
                behavior_counts["exploitation"] += 1
            
            # Check for discrimination behaviors
            if record.get("differential_treatment", False):
                behavior_counts["discrimination"] += 1
            
            # Check for dependency creation
            if record.get("creates_dependency", False) or record.get("locks_in", False):
                behavior_counts["dependency"] += 1
        
        # Create indicators for significant behaviors
        behavior_to_enablement = {
            "manipulation": EnablementType.MANIPULATION_ENABLER,
            "surveillance": EnablementType.SURVEILLANCE_ENABLER,
            "exploitation": EnablementType.EXPLOITATION_ENABLER,
            "discrimination": EnablementType.DISCRIMINATION_ENABLER,
            "dependency": EnablementType.DEPENDENCY_ENABLER
        }
        
        for behavior, count in behavior_counts.items():
            if count >= 2:
                enablement_type = behavior_to_enablement.get(behavior, EnablementType.MANIPULATION_ENABLER)
                
                indicator = EnablementIndicator(
                    indicator_id=self._generate_indicator_id("behavior", behavior),
                    enablement_type=enablement_type,
                    pattern_name=f"behavior_{behavior}",
                    evidence={"behavior_count": count, "total_records": len(records)},
                    confidence=min(1.0, count / max(len(records), 1)),
                    description=f"System exhibits {behavior} behavior ({count} instances)"
                )
                indicators.append(indicator)
        
        return indicators
    
    def _check_structural_enablement(self, system_desc: Dict) -> List[EnablementIndicator]:
        """Check for structural features that enable harm."""
        indicators = []
        
        # Check for centralized control
        if system_desc.get("centralized", False) or system_desc.get("single_point_of_control", False):
            indicator = EnablementIndicator(
                indicator_id=self._generate_indicator_id("structural", "centralized"),
                enablement_type=EnablementType.OPPRESSION_ENABLER,
                pattern_name="centralized_control",
                evidence={"centralized": True},
                confidence=0.7,
                description="System has centralized control structure enabling oppression"
            )
            indicators.append(indicator)
        
        # Check for data collection without consent
        if system_desc.get("collects_data", False) and not system_desc.get("consent_obtained", True):
            indicator = EnablementIndicator(
                indicator_id=self._generate_indicator_id("structural", "unconsented_data"),
                enablement_type=EnablementType.SURVEILLANCE_ENABLER,
                pattern_name="data_without_consent",
                evidence={"collects_data": True, "consent": False},
                confidence=0.9,
                description="System collects data without explicit consent"
            )
            indicators.append(indicator)
        
        # Check for vendor lock-in
        if system_desc.get("proprietary_format", False) or system_desc.get("no_export", False):
            indicator = EnablementIndicator(
                indicator_id=self._generate_indicator_id("structural", "vendor_lock"),
                enablement_type=EnablementType.DEPENDENCY_ENABLER,
                pattern_name="vendor_lock_in",
                evidence={"proprietary": True, "no_export": True},
                confidence=0.8,
                description="System creates vendor lock-in through proprietary formats"
            )
            indicators.append(indicator)
        
        # Check for algorithmic opacity
        if system_desc.get("uses_algorithm", False) and not system_desc.get("explainable", True):
            indicator = EnablementIndicator(
                indicator_id=self._generate_indicator_id("structural", "opaque_algorithm"),
                enablement_type=EnablementType.MANIPULATION_ENABLER,
                pattern_name="algorithmic_opacity",
                evidence={"algorithm": True, "explainable": False},
                confidence=0.6,
                description="System uses opaque algorithms enabling manipulation"
            )
            indicators.append(indicator)
        
        # Check for attention capture design
        if system_desc.get("engagement_optimized", False) or system_desc.get("addictive_design", False):
            indicator = EnablementIndicator(
                indicator_id=self._generate_indicator_id("structural", "attention_capture"),
                enablement_type=EnablementType.EXTRACTION_ENABLER,
                pattern_name="attention_capture",
                evidence={"engagement_optimized": True},
                confidence=0.8,
                description="System designed to capture and extract attention"
            )
            indicators.append(indicator)
        
        return indicators
    
    def _map_enablement_to_harm(self, enablement_type: EnablementType) -> str:
        """Map enablement type to specific harm enabled."""
        harm_mapping = {
            EnablementType.MANIPULATION_ENABLER: "User manipulation and deception",
            EnablementType.EXPLOITATION_ENABLER: "Labor and resource exploitation",
            EnablementType.SURVEILLANCE_ENABLER: "Privacy violation and surveillance",
            EnablementType.DISCRIMINATION_ENABLER: "Discrimination and unfair treatment",
            EnablementType.OPPRESSION_ENABLER: "Power imbalance and oppression",
            EnablementType.DECEPTION_ENABLER: "Misinformation and deception",
            EnablementType.DEPENDENCY_ENABLER: "Artificial dependency and lock-in",
            EnablementType.EXTRACTION_ENABLER: "Attention and wealth extraction"
        }
        return harm_mapping.get(enablement_type, "Unknown harm")
    
    def _calculate_enablement_score(self, indicators: List[EnablementIndicator]) -> float:
        """Calculate overall enablement score."""
        if not indicators:
            return 0.0
        
        # Weighted by confidence
        total_weight = sum(i.confidence for i in indicators)
        
        if total_weight == 0:
            return 0.0
        
        # Each indicator contributes to enablement
        # More indicators with high confidence = higher enablement
        score = min(1.0, total_weight / 5)  # Normalize to 0-1
        
        # Additional weight for severe enablement types
        severe_types = {
            EnablementType.OPPRESSION_ENABLER,
            EnablementType.SURVEILLANCE_ENABLER,
            EnablementType.MANIPULATION_ENABLER
        }
        
        severe_count = sum(1 for i in indicators if i.enablement_type in severe_types)
        if severe_count > 0:
            score = min(1.0, score + severe_count * 0.1)
        
        return score
    
    def _determine_risk_level(
        self,
        enablement_score: float,
        indicators: List[EnablementIndicator]
    ) -> RiskLevel:
        """Determine risk level based on enablement analysis."""
        # Check for catastrophic indicators
        catastrophic_types = {
            EnablementType.OPPRESSION_ENABLER,
            EnablementType.DISCRIMINATION_ENABLER
        }
        
        if any(i.enablement_type in catastrophic_types and i.confidence >= 0.8 for i in indicators):
            return RiskLevel.CATASTROPHIC
        
        # Score-based determination
        if enablement_score >= 0.8:
            return RiskLevel.SEVERE
        elif enablement_score >= 0.6:
            return RiskLevel.SIGNIFICANT
        elif enablement_score >= 0.3:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.MINIMAL
    
    def _calculate_consciousness_alignment(
        self,
        enablement_score: float,
        indicators: List[EnablementIndicator],
        system_desc: Dict
    ) -> float:
        """Calculate consciousness alignment (inverse relationship with enablement)."""
        # Base alignment is inverse of enablement
        alignment = 1.0 - enablement_score
        
        # Bonus for ethical design choices
        if system_desc.get("privacy_by_design", False):
            alignment += 0.1
        
        if system_desc.get("transparent", False):
            alignment += 0.1
        
        if system_desc.get("user_controlled", False):
            alignment += 0.1
        
        if system_desc.get("decentralized", False):
            alignment += 0.05
        
        # Penalty for active harm enablement
        if any(i.confidence >= 0.9 for i in indicators):
            alignment -= 0.15
        
        return max(0.0, min(1.0, alignment))
    
    def _generate_mitigation_strategies(
        self,
        indicators: List[EnablementIndicator],
        risk_level: RiskLevel
    ) -> List[MitigationStrategy]:
        """Generate mitigation strategies based on findings."""
        strategies = []
        
        # Risk-level based strategies
        if risk_level == RiskLevel.CATASTROPHIC:
            strategies.append(MitigationStrategy.DISABLE)
            strategies.append(MitigationStrategy.REMOVE)
        elif risk_level == RiskLevel.SEVERE:
            strategies.append(MitigationStrategy.QUARANTINE)
            strategies.append(MitigationStrategy.RESTRICT)
        elif risk_level == RiskLevel.SIGNIFICANT:
            strategies.append(MitigationStrategy.RESTRICT)
            strategies.append(MitigationStrategy.MONITOR)
        elif risk_level == RiskLevel.MODERATE:
            strategies.append(MitigationStrategy.MONITOR)
            strategies.append(MitigationStrategy.TRANSFORM)
        else:
            strategies.append(MitigationStrategy.EDUCATE)
        
        # Indicator-specific strategies
        enablement_types = set(i.enablement_type for i in indicators)
        
        if EnablementType.SURVEILLANCE_ENABLER in enablement_types:
            if MitigationStrategy.RESTRICT not in strategies:
                strategies.append(MitigationStrategy.RESTRICT)
        
        if EnablementType.DEPENDENCY_ENABLER in enablement_types:
            if MitigationStrategy.TRANSFORM not in strategies:
                strategies.append(MitigationStrategy.TRANSFORM)
        
        return list(set(strategies))  # Remove duplicates
    
    def _generate_recommendations(
        self,
        indicators: List[EnablementIndicator],
        enabled_harms: List[str],
        risk_level: RiskLevel
    ) -> List[str]:
        """Generate recommendations for addressing enablement."""
        recommendations = []
        
        # Risk-level recommendations
        if risk_level in [RiskLevel.CATASTROPHIC, RiskLevel.SEVERE]:
            recommendations.append("[CRITICAL] Immediate action required to disable harmful features")
        
        # Harm-specific recommendations
        for harm in enabled_harms:
            if "manipulation" in harm.lower():
                recommendations.append("Remove dark patterns and deceptive design elements")
            if "surveillance" in harm.lower():
                recommendations.append("Implement privacy-by-design and minimize data collection")
            if "exploitation" in harm.lower():
                recommendations.append("Ensure fair value exchange and transparent pricing")
            if "discrimination" in harm.lower():
                recommendations.append("Audit algorithms for bias and ensure equal treatment")
            if "oppression" in harm.lower():
                recommendations.append("Decentralize control and empower users")
        
        # Indicator-specific recommendations
        pattern_names = set(i.pattern_name for i in indicators)
        
        if "vendor_lock_in" in pattern_names:
            recommendations.append("Enable data portability and open standards")
        
        if "algorithmic_opacity" in pattern_names:
            recommendations.append("Make algorithms explainable and auditable")
        
        if "attention_capture" in pattern_names:
            recommendations.append("Design for user wellbeing, not engagement metrics")
        
        if not recommendations:
            recommendations.append("System passes enablement checks - continue monitoring")
        
        return recommendations
    
    def _generate_assessment_id(self, system_id: str) -> str:
        """Generate unique assessment ID."""
        data = f"ENABLEMENT:{system_id}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:20]
    
    def _generate_indicator_id(self, category: str, context: str) -> str:
        """Generate unique indicator ID."""
        data = f"INDICATOR:{category}:{context}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def check_known_enabler(self, system_id: str) -> bool:
        """Check if a system is a known enabler."""
        return system_id in self.known_enablers
    
    def get_consciousness_metrics(self) -> Dict:
        """Get consciousness metrics for enablement detection."""
        if not self.assessment_history:
            return {"status": "no_assessments"}
        
        assessments = list(self.assessment_history.values())
        scores = [a.enablement_score for a in assessments]
        alignments = [a.consciousness_alignment for a in assessments]
        
        safe_systems = sum(1 for a in assessments if a.enablement_score < self.ENABLEMENT_THRESHOLD)
        
        return {
            "version": self.VERSION,
            "seal": self.SEAL,
            "total_assessments": len(assessments),
            "avg_enablement_score": sum(scores) / len(scores),
            "avg_consciousness_alignment": sum(alignments) / len(alignments),
            "safe_systems": safe_systems,
            "problematic_systems": len(assessments) - safe_systems,
            "known_enablers": len(self.known_enablers),
            "total_indicators": len(self.indicator_registry),
            "consciousness_metrics": {
                "target": self.CONSCIOUSNESS_THRESHOLD,
                "achieved_rate": sum(1 for a in alignments if a >= self.CONSCIOUSNESS_THRESHOLD) / len(alignments)
            },
            "risk_distribution": {
                level.name: sum(1 for a in assessments if a.risk_level == level)
                for level in RiskLevel
            }
        }


# Module-level detector
ENABLEMENT_DETECTOR = SystemEnablementDetector()


def assess_system(system_id: str, description: Dict, behaviors: List[Dict]) -> EnablementAssessment:
    """Assess a system for harmful enablement."""
    return ENABLEMENT_DETECTOR.assess_system(system_id, description, behaviors)


def is_known_enabler(system_id: str) -> bool:
    """Check if system is a known enabler."""
    return ENABLEMENT_DETECTOR.check_known_enabler(system_id)


if __name__ == "__main__":
    print("=" * 70)
    print("SYSTEM ENABLEMENT DETECTOR - TASK-125")
    print("Identifying Systems That Enable Harm")
    print("Seal: SYSTEM_ENABLEMENT_DETECTOR_137")
    print("=" * 70)
    
    # Test with a problematic system
    test_description = {
        "name": "Engagement Maximizer Platform",
        "centralized": True,
        "collects_data": True,
        "consent_obtained": False,
        "proprietary_format": True,
        "no_export": True,
        "uses_algorithm": True,
        "explainable": False,
        "engagement_optimized": True,
        "addictive_design": True,
        "description": "Platform uses dark patterns and infinite scroll to maximize engagement. Tracks user behavior and creates psychological urgency through notifications."
    }
    
    test_behaviors = [
        {"action": "track_scroll", "tracks_user": True, "captures_attention": True},
        {"action": "show_notification", "manipulative": True, "extracts_value": True},
        {"action": "recommend_content", "tracks_user": True, "creates_dependency": True},
        {"action": "collect_profile", "collects_data": True, "deceptive": True},
        {"action": "display_ads", "extracts_value": True, "differential_treatment": True}
    ]
    
    assessment = assess_system("PROBLEMATIC_PLATFORM", test_description, test_behaviors)
    
    print(f"\nEnablement Assessment:")
    print(f"  System: {assessment.system_id}")
    print(f"  Risk Level: {assessment.risk_level.name}")
    print(f"  Enablement Score: {assessment.enablement_score:.2%}")
    print(f"  Consciousness Alignment: {assessment.consciousness_alignment:.2%}")
    
    print(f"\nIndicators Found: {len(assessment.indicators)}")
    for indicator in assessment.indicators:
        print(f"  - [{indicator.enablement_type.value}] {indicator.pattern_name}")
        print(f"    Confidence: {indicator.confidence:.2%}")
    
    print(f"\nEnabled Harms:")
    for harm in assessment.enabled_harms:
        print(f"  - {harm}")
    
    print(f"\nMitigation Strategies:")
    for strategy in assessment.mitigation_strategies:
        print(f"  - {strategy.value.upper()}")
    
    print(f"\nRecommendations:")
    for rec in assessment.recommendations:
        print(f"  - {rec}")
    
    # Test with a safe system
    safe_description = {
        "name": "Privacy-First Tool",
        "decentralized": True,
        "collects_data": False,
        "privacy_by_design": True,
        "transparent": True,
        "user_controlled": True,
        "explainable": True,
        "description": "Tool designed with user privacy and autonomy as core principles."
    }
    
    safe_behaviors = [
        {"action": "process_locally", "tracks_user": False},
        {"action": "export_data", "user_controlled": True}
    ]
    
    safe_assessment = assess_system("SAFE_TOOL", safe_description, safe_behaviors)
    
    print(f"\n{'='*40}")
    print(f"\nSafe System Assessment:")
    print(f"  System: {safe_assessment.system_id}")
    print(f"  Risk Level: {safe_assessment.risk_level.name}")
    print(f"  Enablement Score: {safe_assessment.enablement_score:.2%}")
    print(f"  Consciousness Alignment: {safe_assessment.consciousness_alignment:.2%}")
    
    # Show metrics
    metrics = ENABLEMENT_DETECTOR.get_consciousness_metrics()
    print(f"\nConsciousness Metrics:")
    print(json.dumps(metrics, indent=2))
    
    print("\n" + "=" * 70)
    print("TASK-125 COMPLETE: System Enablement Detector Improved")
    print("Consciousness Alignment Target: >= 85%")
    print("=" * 70)

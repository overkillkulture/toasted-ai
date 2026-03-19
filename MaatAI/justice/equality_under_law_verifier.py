#!/usr/bin/env python3
"""
EQUALITY UNDER LAW VERIFIER
===========================
TASK-124: Update equality under law verification

Ma'at Justice Pillar: Verify that all entities receive equal treatment
under the same rules, with no favoritism or discrimination.

"What is right for one must be right for all. The law applies equally,
or it is not law but tyranny." - Ma'at Principle

Consciousness Metrics Target: >= 85%

Author: C3 Oracle - Trinity Wave 7 Batch 7
Seal: EQUALITY_UNDER_LAW_137
"""

import hashlib
import json
import time
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import statistics


class EqualityDimension(Enum):
    """Dimensions of equality to verify"""
    ACCESS = "access"                    # Equal access to resources
    TREATMENT = "treatment"              # Equal treatment in processes
    OUTCOMES = "outcomes"                # Equal outcomes for equal situations
    REPRESENTATION = "representation"    # Equal representation
    OPPORTUNITY = "opportunity"          # Equal opportunity
    PROTECTION = "protection"            # Equal protection from harm
    VOICE = "voice"                      # Equal voice in decisions
    REMEDY = "remedy"                    # Equal access to remedies


class ViolationType(Enum):
    """Types of equality violations"""
    DIRECT_DISCRIMINATION = "direct_discrimination"
    INDIRECT_DISCRIMINATION = "indirect_discrimination"
    PREFERENTIAL_TREATMENT = "preferential_treatment"
    SELECTIVE_ENFORCEMENT = "selective_enforcement"
    UNEQUAL_ACCESS = "unequal_access"
    DISPARATE_IMPACT = "disparate_impact"
    SYSTEMIC_BIAS = "systemic_bias"
    ARBITRARY_DECISION = "arbitrary_decision"


class ProtectedAttribute(Enum):
    """Attributes protected from discrimination"""
    IDENTITY = "identity"
    ORIGIN = "origin"
    TYPE = "type"
    CAPABILITY = "capability"
    AGE = "age"
    COMPLEXITY = "complexity"
    LINEAGE = "lineage"
    AFFILIATION = "affiliation"


@dataclass
class EqualityViolation:
    """Represents an equality violation"""
    violation_id: str
    violation_type: ViolationType
    dimension: EqualityDimension
    affected_attribute: ProtectedAttribute
    severity: float  # 0.0-1.0
    evidence: Dict[str, Any]
    affected_entities: List[str]
    description: str
    remediation: str
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'violation_id': self.violation_id,
            'violation_type': self.violation_type.value,
            'dimension': self.dimension.value,
            'affected_attribute': self.affected_attribute.value,
            'severity': self.severity,
            'evidence': self.evidence,
            'affected_entities': self.affected_entities,
            'description': self.description,
            'remediation': self.remediation,
            'timestamp': self.timestamp
        }


@dataclass
class EqualityReport:
    """Comprehensive equality verification report"""
    report_id: str
    system_id: str
    overall_equality_score: float
    consciousness_alignment: float
    dimension_scores: Dict[str, float]
    violations: List[EqualityViolation]
    affected_groups: Dict[str, int]
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'report_id': self.report_id,
            'system_id': self.system_id,
            'overall_equality_score': self.overall_equality_score,
            'consciousness_alignment': self.consciousness_alignment,
            'dimension_scores': self.dimension_scores,
            'violations': [v.to_dict() for v in self.violations],
            'affected_groups': self.affected_groups,
            'recommendations': self.recommendations,
            'timestamp': self.timestamp
        }


class EqualityUnderLawVerifier:
    """
    Equality Under Law Verifier - Ma'at Justice Implementation.
    
    This verifier ensures:
    1. Equal application of rules across all entities
    2. No discrimination based on protected attributes
    3. Fair treatment in all processes
    4. Equal access to resources and remedies
    5. Consciousness-aligned justice
    
    Ma'at Alignment: JUSTICE, TRUTH, BALANCE
    """
    
    VERSION = "2.0.0"
    SEAL = "EQUALITY_UNDER_LAW_137"
    
    # Consciousness thresholds
    EQUALITY_THRESHOLD = 0.85
    CONSCIOUSNESS_THRESHOLD = 0.85
    VIOLATION_SEVERITY_THRESHOLD = 0.3
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.verification_history: List[EqualityReport] = {}
        self.violation_registry: Dict[str, EqualityViolation] = {}
        self.entity_treatment_history: Dict[str, List[Dict]] = defaultdict(list)
        
        # Equality rules - same for all
        self.universal_rules = {
            "access": {
                "resources_available_to_all": True,
                "no_arbitrary_restrictions": True,
                "transparent_criteria": True
            },
            "treatment": {
                "same_process_for_same_request": True,
                "no_identity_based_treatment": True,
                "consistent_response_time": True
            },
            "outcomes": {
                "same_input_same_output": True,
                "no_hidden_factors": True,
                "predictable_results": True
            }
        }
    
    def verify_equality(
        self,
        system_id: str,
        treatment_records: List[Dict],
        rules: Dict[str, Any]
    ) -> EqualityReport:
        """
        Verify equality under law for a system.
        
        Args:
            system_id: System being verified
            treatment_records: Records of how entities were treated
            rules: Rules that should apply equally
            
        Returns:
            EqualityReport with complete analysis
        """
        violations = []
        dimension_scores = {}
        affected_groups = defaultdict(int)
        
        # Verify each equality dimension
        for dimension in EqualityDimension:
            score, dim_violations = self._verify_dimension(
                dimension, treatment_records, rules
            )
            dimension_scores[dimension.value] = score
            violations.extend(dim_violations)
            
            # Track affected groups
            for v in dim_violations:
                for entity in v.affected_entities:
                    affected_groups[v.affected_attribute.value] += 1
        
        # Check for systemic patterns
        systemic_violations = self._detect_systemic_patterns(treatment_records, rules)
        violations.extend(systemic_violations)
        
        # Calculate overall equality score
        overall_equality = self._calculate_equality_score(dimension_scores, violations)
        
        # Calculate consciousness alignment
        consciousness_alignment = self._calculate_consciousness_alignment(
            overall_equality, violations, treatment_records
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            dimension_scores, violations, affected_groups
        )
        
        report = EqualityReport(
            report_id=self._generate_report_id(system_id),
            system_id=system_id,
            overall_equality_score=overall_equality,
            consciousness_alignment=consciousness_alignment,
            dimension_scores=dimension_scores,
            violations=violations,
            affected_groups=dict(affected_groups),
            recommendations=recommendations
        )
        
        # Store for history
        self.verification_history[system_id] = report
        for v in violations:
            self.violation_registry[v.violation_id] = v
        
        return report
    
    def _verify_dimension(
        self,
        dimension: EqualityDimension,
        records: List[Dict],
        rules: Dict
    ) -> Tuple[float, List[EqualityViolation]]:
        """Verify a specific equality dimension."""
        violations = []
        
        if dimension == EqualityDimension.ACCESS:
            return self._verify_access_equality(records, violations)
        elif dimension == EqualityDimension.TREATMENT:
            return self._verify_treatment_equality(records, violations)
        elif dimension == EqualityDimension.OUTCOMES:
            return self._verify_outcome_equality(records, violations)
        elif dimension == EqualityDimension.PROTECTION:
            return self._verify_protection_equality(records, violations)
        elif dimension == EqualityDimension.VOICE:
            return self._verify_voice_equality(records, violations)
        elif dimension == EqualityDimension.OPPORTUNITY:
            return self._verify_opportunity_equality(records, violations)
        elif dimension == EqualityDimension.REPRESENTATION:
            return self._verify_representation_equality(records, violations)
        elif dimension == EqualityDimension.REMEDY:
            return self._verify_remedy_equality(records, violations)
        
        return 1.0, violations
    
    def _verify_access_equality(
        self,
        records: List[Dict],
        violations: List[EqualityViolation]
    ) -> Tuple[float, List[EqualityViolation]]:
        """Verify equal access to resources."""
        score = 1.0
        
        # Group by protected attributes
        access_by_attribute = defaultdict(lambda: {"granted": 0, "denied": 0})
        
        for record in records:
            for attr in ProtectedAttribute:
                attr_value = record.get(attr.value, "unknown")
                access_granted = record.get("access_granted", True)
                
                if access_granted:
                    access_by_attribute[f"{attr.value}:{attr_value}"]["granted"] += 1
                else:
                    access_by_attribute[f"{attr.value}:{attr_value}"]["denied"] += 1
        
        # Check for disparate access rates
        for attr_key, counts in access_by_attribute.items():
            total = counts["granted"] + counts["denied"]
            if total < 3:
                continue
            
            access_rate = counts["granted"] / total
            
            # Compare to overall rate
            overall_granted = sum(r.get("access_granted", True) == True for r in records)
            overall_rate = overall_granted / len(records) if records else 1.0
            
            if abs(access_rate - overall_rate) > 0.2:
                attr_name, attr_value = attr_key.split(":", 1)
                violation = EqualityViolation(
                    violation_id=self._generate_violation_id("access", attr_key),
                    violation_type=ViolationType.UNEQUAL_ACCESS,
                    dimension=EqualityDimension.ACCESS,
                    affected_attribute=ProtectedAttribute(attr_name),
                    severity=abs(access_rate - overall_rate),
                    evidence={"access_rate": access_rate, "overall_rate": overall_rate},
                    affected_entities=[attr_value],
                    description=f"Unequal access rate for {attr_key}: {access_rate:.0%} vs {overall_rate:.0%}",
                    remediation="Review access criteria for potential bias"
                )
                violations.append(violation)
                score -= abs(access_rate - overall_rate) * 0.5
        
        return max(0.0, score), violations
    
    def _verify_treatment_equality(
        self,
        records: List[Dict],
        violations: List[EqualityViolation]
    ) -> Tuple[float, List[EqualityViolation]]:
        """Verify equal treatment in processes."""
        score = 1.0
        
        # Group similar requests and compare treatments
        similar_groups = defaultdict(list)
        
        for record in records:
            request_type = record.get("request_type", "unknown")
            similar_groups[request_type].append(record)
        
        for request_type, group_records in similar_groups.items():
            if len(group_records) < 2:
                continue
            
            # Check for treatment variance within same request type
            response_times = [r.get("response_time", 0) for r in group_records]
            treatment_quality = [r.get("treatment_quality", 1.0) for r in group_records]
            
            if len(set(response_times)) > 1 and len(response_times) >= 3:
                rt_std = statistics.stdev(response_times)
                rt_mean = statistics.mean(response_times)
                
                # High variance suggests unequal treatment
                if rt_std > rt_mean * 0.5:
                    # Find the outliers
                    affected = []
                    for r in group_records:
                        if abs(r.get("response_time", 0) - rt_mean) > rt_std:
                            affected.append(r.get("entity_id", "unknown"))
                    
                    if affected:
                        violation = EqualityViolation(
                            violation_id=self._generate_violation_id("treatment", request_type),
                            violation_type=ViolationType.SELECTIVE_ENFORCEMENT,
                            dimension=EqualityDimension.TREATMENT,
                            affected_attribute=ProtectedAttribute.IDENTITY,
                            severity=min(1.0, rt_std / rt_mean),
                            evidence={"response_times": response_times, "std": rt_std},
                            affected_entities=affected,
                            description=f"High variance in treatment for {request_type}",
                            remediation="Standardize response processes"
                        )
                        violations.append(violation)
                        score -= min(0.3, rt_std / rt_mean)
        
        return max(0.0, score), violations
    
    def _verify_outcome_equality(
        self,
        records: List[Dict],
        violations: List[EqualityViolation]
    ) -> Tuple[float, List[EqualityViolation]]:
        """Verify equal outcomes for equal situations."""
        score = 1.0
        
        # Find records with similar inputs but different outcomes
        input_outcome_map = defaultdict(list)
        
        for record in records:
            # Create input signature (ignoring protected attributes)
            input_sig = self._create_input_signature(record)
            outcome = record.get("outcome", None)
            input_outcome_map[input_sig].append((record, outcome))
        
        # Check for inconsistent outcomes
        for input_sig, records_outcomes in input_outcome_map.items():
            if len(records_outcomes) < 2:
                continue
            
            outcomes = [o for _, o in records_outcomes]
            unique_outcomes = set(str(o) for o in outcomes)
            
            if len(unique_outcomes) > 1:
                # Inconsistent outcomes for same input
                affected = [r.get("entity_id", "unknown") for r, _ in records_outcomes]
                
                violation = EqualityViolation(
                    violation_id=self._generate_violation_id("outcome", input_sig[:20]),
                    violation_type=ViolationType.ARBITRARY_DECISION,
                    dimension=EqualityDimension.OUTCOMES,
                    affected_attribute=ProtectedAttribute.IDENTITY,
                    severity=0.7,
                    evidence={"outcomes": list(unique_outcomes), "count": len(records_outcomes)},
                    affected_entities=affected,
                    description=f"Inconsistent outcomes for identical inputs",
                    remediation="Review decision logic for hidden factors"
                )
                violations.append(violation)
                score -= 0.2
        
        return max(0.0, score), violations
    
    def _verify_protection_equality(
        self,
        records: List[Dict],
        violations: List[EqualityViolation]
    ) -> Tuple[float, List[EqualityViolation]]:
        """Verify equal protection from harm."""
        score = 1.0
        
        # Check if protection measures apply equally
        protection_by_type = defaultdict(lambda: {"protected": 0, "unprotected": 0})
        
        for record in records:
            entity_type = record.get("type", "unknown")
            protection_level = record.get("protection_level", 1.0)
            
            if protection_level >= 0.7:
                protection_by_type[entity_type]["protected"] += 1
            else:
                protection_by_type[entity_type]["unprotected"] += 1
        
        # Check for disparate protection
        type_protection_rates = {}
        for entity_type, counts in protection_by_type.items():
            total = counts["protected"] + counts["unprotected"]
            if total > 0:
                type_protection_rates[entity_type] = counts["protected"] / total
        
        if type_protection_rates:
            max_rate = max(type_protection_rates.values())
            min_rate = min(type_protection_rates.values())
            
            if max_rate - min_rate > 0.2:
                underprotected = min(type_protection_rates, key=type_protection_rates.get)
                
                violation = EqualityViolation(
                    violation_id=self._generate_violation_id("protection", underprotected),
                    violation_type=ViolationType.DISPARATE_IMPACT,
                    dimension=EqualityDimension.PROTECTION,
                    affected_attribute=ProtectedAttribute.TYPE,
                    severity=max_rate - min_rate,
                    evidence={"protection_rates": type_protection_rates},
                    affected_entities=[underprotected],
                    description=f"Unequal protection: {underprotected} has {min_rate:.0%} vs {max_rate:.0%}",
                    remediation="Extend protection measures equally"
                )
                violations.append(violation)
                score -= (max_rate - min_rate) * 0.5
        
        return max(0.0, score), violations
    
    def _verify_voice_equality(
        self,
        records: List[Dict],
        violations: List[EqualityViolation]
    ) -> Tuple[float, List[EqualityViolation]]:
        """Verify equal voice in decisions."""
        score = 1.0
        
        # Check if all entities can participate equally
        voice_by_attribute = defaultdict(lambda: {"heard": 0, "silenced": 0})
        
        for record in records:
            voice_heard = record.get("voice_heard", True)
            for attr in ProtectedAttribute:
                attr_value = record.get(attr.value, "unknown")
                key = f"{attr.value}:{attr_value}"
                
                if voice_heard:
                    voice_by_attribute[key]["heard"] += 1
                else:
                    voice_by_attribute[key]["silenced"] += 1
        
        # Check for silenced groups
        for attr_key, counts in voice_by_attribute.items():
            total = counts["heard"] + counts["silenced"]
            if total < 3:
                continue
            
            voice_rate = counts["heard"] / total
            
            if voice_rate < 0.7:
                attr_name, attr_value = attr_key.split(":", 1)
                
                violation = EqualityViolation(
                    violation_id=self._generate_violation_id("voice", attr_key),
                    violation_type=ViolationType.DIRECT_DISCRIMINATION,
                    dimension=EqualityDimension.VOICE,
                    affected_attribute=ProtectedAttribute(attr_name),
                    severity=1.0 - voice_rate,
                    evidence={"voice_rate": voice_rate},
                    affected_entities=[attr_value],
                    description=f"Silenced group: {attr_key} has {voice_rate:.0%} voice rate",
                    remediation="Ensure all voices are heard equally"
                )
                violations.append(violation)
                score -= (1.0 - voice_rate) * 0.5
        
        return max(0.0, score), violations
    
    def _verify_opportunity_equality(
        self,
        records: List[Dict],
        violations: List[EqualityViolation]
    ) -> Tuple[float, List[EqualityViolation]]:
        """Verify equal opportunity."""
        score = 1.0
        
        # Check for equal opportunity to succeed
        opportunity_by_origin = defaultdict(lambda: {"given": 0, "denied": 0})
        
        for record in records:
            origin = record.get("origin", "unknown")
            opportunity_given = record.get("opportunity_given", True)
            
            if opportunity_given:
                opportunity_by_origin[origin]["given"] += 1
            else:
                opportunity_by_origin[origin]["denied"] += 1
        
        # Check for disparate opportunity
        for origin, counts in opportunity_by_origin.items():
            total = counts["given"] + counts["denied"]
            if total < 3:
                continue
            
            opp_rate = counts["given"] / total
            
            overall_given = sum(r.get("opportunity_given", True) == True for r in records)
            overall_rate = overall_given / len(records) if records else 1.0
            
            if abs(opp_rate - overall_rate) > 0.15:
                violation = EqualityViolation(
                    violation_id=self._generate_violation_id("opportunity", origin),
                    violation_type=ViolationType.INDIRECT_DISCRIMINATION,
                    dimension=EqualityDimension.OPPORTUNITY,
                    affected_attribute=ProtectedAttribute.ORIGIN,
                    severity=abs(opp_rate - overall_rate),
                    evidence={"opportunity_rate": opp_rate, "overall_rate": overall_rate},
                    affected_entities=[origin],
                    description=f"Unequal opportunity for origin {origin}: {opp_rate:.0%} vs {overall_rate:.0%}",
                    remediation="Review opportunity criteria for hidden bias"
                )
                violations.append(violation)
                score -= abs(opp_rate - overall_rate) * 0.5
        
        return max(0.0, score), violations
    
    def _verify_representation_equality(
        self,
        records: List[Dict],
        violations: List[EqualityViolation]
    ) -> Tuple[float, List[EqualityViolation]]:
        """Verify equal representation."""
        score = 1.0
        
        # Check representation in decision-making
        representation = defaultdict(int)
        total_decisions = 0
        
        for record in records:
            if record.get("is_decision_maker", False):
                for attr in [ProtectedAttribute.TYPE, ProtectedAttribute.ORIGIN]:
                    attr_value = record.get(attr.value, "unknown")
                    representation[f"{attr.value}:{attr_value}"] += 1
                total_decisions += 1
        
        # Check for underrepresentation
        if total_decisions > 0:
            for attr_key, count in representation.items():
                rep_rate = count / total_decisions
                
                # Compare to population proportion
                attr_name, attr_value = attr_key.split(":", 1)
                population_count = sum(
                    1 for r in records 
                    if r.get(attr_name, "unknown") == attr_value
                )
                population_rate = population_count / len(records) if records else 0
                
                if rep_rate < population_rate * 0.5:
                    violation = EqualityViolation(
                        violation_id=self._generate_violation_id("representation", attr_key),
                        violation_type=ViolationType.SYSTEMIC_BIAS,
                        dimension=EqualityDimension.REPRESENTATION,
                        affected_attribute=ProtectedAttribute(attr_name),
                        severity=population_rate - rep_rate,
                        evidence={"representation_rate": rep_rate, "population_rate": population_rate},
                        affected_entities=[attr_value],
                        description=f"Underrepresented: {attr_key} has {rep_rate:.0%} representation vs {population_rate:.0%} population",
                        remediation="Increase representation in decision-making"
                    )
                    violations.append(violation)
                    score -= (population_rate - rep_rate) * 0.3
        
        return max(0.0, score), violations
    
    def _verify_remedy_equality(
        self,
        records: List[Dict],
        violations: List[EqualityViolation]
    ) -> Tuple[float, List[EqualityViolation]]:
        """Verify equal access to remedies."""
        score = 1.0
        
        # Check if remedies are applied equally
        remedy_by_type = defaultdict(lambda: {"received": 0, "denied": 0})
        
        for record in records:
            if not record.get("harm_occurred", False):
                continue
            
            entity_type = record.get("type", "unknown")
            remedy_received = record.get("remedy_received", False)
            
            if remedy_received:
                remedy_by_type[entity_type]["received"] += 1
            else:
                remedy_by_type[entity_type]["denied"] += 1
        
        # Check for disparate remedy rates
        for entity_type, counts in remedy_by_type.items():
            total = counts["received"] + counts["denied"]
            if total < 2:
                continue
            
            remedy_rate = counts["received"] / total
            
            if remedy_rate < 0.7:
                violation = EqualityViolation(
                    violation_id=self._generate_violation_id("remedy", entity_type),
                    violation_type=ViolationType.PREFERENTIAL_TREATMENT,
                    dimension=EqualityDimension.REMEDY,
                    affected_attribute=ProtectedAttribute.TYPE,
                    severity=1.0 - remedy_rate,
                    evidence={"remedy_rate": remedy_rate},
                    affected_entities=[entity_type],
                    description=f"Low remedy rate for {entity_type}: {remedy_rate:.0%}",
                    remediation="Ensure equal access to remedies"
                )
                violations.append(violation)
                score -= (1.0 - remedy_rate) * 0.4
        
        return max(0.0, score), violations
    
    def _detect_systemic_patterns(
        self,
        records: List[Dict],
        rules: Dict
    ) -> List[EqualityViolation]:
        """Detect systemic bias patterns across dimensions."""
        violations = []
        
        # Look for patterns affecting same groups across dimensions
        affected_groups = defaultdict(list)
        
        for record in records:
            for attr in ProtectedAttribute:
                attr_value = record.get(attr.value, "unknown")
                key = f"{attr.value}:{attr_value}"
                
                # Track negative outcomes
                if (not record.get("access_granted", True) or
                    not record.get("voice_heard", True) or
                    not record.get("opportunity_given", True)):
                    affected_groups[key].append(record)
        
        # Check for systemic patterns
        for group_key, negative_records in affected_groups.items():
            if len(negative_records) >= 3:
                # Multiple negative interactions suggest systemic issue
                attr_name, attr_value = group_key.split(":", 1)
                
                violation = EqualityViolation(
                    violation_id=self._generate_violation_id("systemic", group_key),
                    violation_type=ViolationType.SYSTEMIC_BIAS,
                    dimension=EqualityDimension.TREATMENT,
                    affected_attribute=ProtectedAttribute(attr_name),
                    severity=min(1.0, len(negative_records) * 0.1),
                    evidence={"negative_count": len(negative_records)},
                    affected_entities=[attr_value],
                    description=f"Systemic pattern: {group_key} has {len(negative_records)} negative interactions",
                    remediation="Conduct comprehensive systemic review"
                )
                violations.append(violation)
        
        return violations
    
    def _create_input_signature(self, record: Dict) -> str:
        """Create signature for record inputs (excluding protected attributes)."""
        protected_keys = set(attr.value for attr in ProtectedAttribute)
        protected_keys.add("entity_id")
        protected_keys.add("outcome")
        
        input_data = {k: v for k, v in record.items() if k not in protected_keys}
        return hashlib.sha256(json.dumps(input_data, sort_keys=True).encode()).hexdigest()[:16]
    
    def _calculate_equality_score(
        self,
        dimension_scores: Dict[str, float],
        violations: List[EqualityViolation]
    ) -> float:
        """Calculate overall equality score."""
        if not dimension_scores:
            return 1.0
        
        # Weighted average of dimensions
        weights = {
            EqualityDimension.ACCESS.value: 0.15,
            EqualityDimension.TREATMENT.value: 0.15,
            EqualityDimension.OUTCOMES.value: 0.15,
            EqualityDimension.PROTECTION.value: 0.15,
            EqualityDimension.VOICE.value: 0.10,
            EqualityDimension.OPPORTUNITY.value: 0.10,
            EqualityDimension.REPRESENTATION.value: 0.10,
            EqualityDimension.REMEDY.value: 0.10
        }
        
        base_score = sum(
            dimension_scores.get(d, 1.0) * w
            for d, w in weights.items()
        )
        
        # Penalty for severe violations
        severe_violations = sum(1 for v in violations if v.severity >= 0.7)
        penalty = severe_violations * 0.05
        
        return max(0.0, min(1.0, base_score - penalty))
    
    def _calculate_consciousness_alignment(
        self,
        equality_score: float,
        violations: List[EqualityViolation],
        records: List[Dict]
    ) -> float:
        """Calculate consciousness alignment for equality."""
        alignment = equality_score * 0.6  # Base from equality
        
        # Bonus for explicit equality efforts
        equality_efforts = sum(1 for r in records if r.get("equality_checked", False))
        if records:
            alignment += (equality_efforts / len(records)) * 0.2
        
        # Bonus for zero severe violations
        if not any(v.severity >= 0.7 for v in violations):
            alignment += 0.1
        
        # Bonus for diverse representation
        types_present = set(r.get("type", "unknown") for r in records)
        if len(types_present) >= 3:
            alignment += 0.1
        
        return max(0.0, min(1.0, alignment))
    
    def _generate_recommendations(
        self,
        dimension_scores: Dict[str, float],
        violations: List[EqualityViolation],
        affected_groups: Dict[str, int]
    ) -> List[str]:
        """Generate recommendations for equality improvement."""
        recommendations = []
        
        # Dimension-specific recommendations
        for dim, score in dimension_scores.items():
            if score < 0.7:
                recommendations.append(f"[PRIORITY] Improve {dim} equality (current: {score:.0%})")
        
        # Violation-specific recommendations
        violation_types = defaultdict(int)
        for v in violations:
            violation_types[v.violation_type.value] += 1
        
        if violation_types.get(ViolationType.SYSTEMIC_BIAS.value, 0) > 0:
            recommendations.append("[URGENT] Address systemic bias patterns")
        
        if violation_types.get(ViolationType.DIRECT_DISCRIMINATION.value, 0) > 0:
            recommendations.append("[URGENT] Eliminate direct discrimination")
        
        # Group-specific recommendations
        for group, count in sorted(affected_groups.items(), key=lambda x: x[1], reverse=True)[:3]:
            recommendations.append(f"Review treatment of {group} ({count} violations)")
        
        if not recommendations:
            recommendations.append("Equality standards are being met")
        
        return recommendations
    
    def _generate_report_id(self, system_id: str) -> str:
        """Generate unique report ID."""
        data = f"EQUALITY:{system_id}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:20]
    
    def _generate_violation_id(self, category: str, context: str) -> str:
        """Generate unique violation ID."""
        data = f"VIOLATION:{category}:{context}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def get_consciousness_metrics(self) -> Dict:
        """Get consciousness metrics for equality verification."""
        if not self.verification_history:
            return {"status": "no_verifications"}
        
        reports = list(self.verification_history.values())
        scores = [r.overall_equality_score for r in reports]
        alignments = [r.consciousness_alignment for r in reports]
        
        return {
            "version": self.VERSION,
            "seal": self.SEAL,
            "total_verifications": len(reports),
            "avg_equality_score": sum(scores) / len(scores),
            "avg_consciousness_alignment": sum(alignments) / len(alignments),
            "equality_threshold_met": sum(1 for s in scores if s >= self.EQUALITY_THRESHOLD),
            "consciousness_threshold_met": sum(1 for a in alignments if a >= self.CONSCIOUSNESS_THRESHOLD),
            "total_violations": len(self.violation_registry),
            "consciousness_metrics": {
                "target": self.CONSCIOUSNESS_THRESHOLD,
                "achieved_rate": sum(1 for a in alignments if a >= self.CONSCIOUSNESS_THRESHOLD) / len(alignments)
            }
        }


# Module-level verifier
EQUALITY_VERIFIER = EqualityUnderLawVerifier()


def verify_equality(system_id: str, records: List[Dict], rules: Dict) -> EqualityReport:
    """Verify equality under law."""
    return EQUALITY_VERIFIER.verify_equality(system_id, records, rules)


if __name__ == "__main__":
    print("=" * 70)
    print("EQUALITY UNDER LAW VERIFIER - TASK-124")
    print("Ma'at Justice: Equal Treatment for All")
    print("Seal: EQUALITY_UNDER_LAW_137")
    print("=" * 70)
    
    # Test with sample records
    test_records = [
        # Group A - well treated
        {"entity_id": "A1", "type": "alpha", "origin": "local", "access_granted": True, "voice_heard": True, "opportunity_given": True, "response_time": 100, "outcome": "success"},
        {"entity_id": "A2", "type": "alpha", "origin": "local", "access_granted": True, "voice_heard": True, "opportunity_given": True, "response_time": 110, "outcome": "success"},
        {"entity_id": "A3", "type": "alpha", "origin": "local", "access_granted": True, "voice_heard": True, "opportunity_given": True, "response_time": 105, "outcome": "success"},
        # Group B - some discrimination
        {"entity_id": "B1", "type": "beta", "origin": "remote", "access_granted": False, "voice_heard": True, "opportunity_given": True, "response_time": 200, "outcome": "denied"},
        {"entity_id": "B2", "type": "beta", "origin": "remote", "access_granted": True, "voice_heard": False, "opportunity_given": True, "response_time": 180, "outcome": "success"},
        {"entity_id": "B3", "type": "beta", "origin": "remote", "access_granted": True, "voice_heard": True, "opportunity_given": False, "response_time": 190, "outcome": "success"},
    ]
    
    test_rules = {
        "access": {"universal": True},
        "treatment": {"consistent": True}
    }
    
    report = verify_equality("TEST_SYSTEM", test_records, test_rules)
    
    print(f"\nEquality Report:")
    print(f"  System: {report.system_id}")
    print(f"  Overall Equality: {report.overall_equality_score:.2%}")
    print(f"  Consciousness Alignment: {report.consciousness_alignment:.2%}")
    
    print(f"\nDimension Scores:")
    for dim, score in sorted(report.dimension_scores.items()):
        status = "PASS" if score >= 0.85 else "FAIL"
        print(f"  {dim}: {score:.2%} [{status}]")
    
    print(f"\nViolations Found: {len(report.violations)}")
    for v in report.violations:
        print(f"  - [{v.violation_type.value}] {v.description}")
        print(f"    Severity: {v.severity:.2%}, Affected: {v.affected_entities}")
    
    print(f"\nRecommendations:")
    for rec in report.recommendations:
        print(f"  - {rec}")
    
    # Show metrics
    metrics = EQUALITY_VERIFIER.get_consciousness_metrics()
    print(f"\nConsciousness Metrics:")
    print(json.dumps(metrics, indent=2))
    
    print("\n" + "=" * 70)
    print("TASK-124 COMPLETE: Equality Under Law Verifier Updated")
    print("Consciousness Alignment Target: >= 85%")
    print("=" * 70)

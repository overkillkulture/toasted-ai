"""
Ma'at IMPACT ASSESSOR
=====================
TASK-120: Optimize justice impact assessment

Assesses impact on all affected parties:
- Stakeholder identification
- Impact quantification
- Harm assessment
- Benefit distribution
- Vulnerability analysis

Author: C3 Oracle - TOASTED AI Trinity
Seal: MAAT_IMPACT_ASSESSOR_137
"""

import time
import hashlib
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import threading
from collections import defaultdict


class ImpactType(Enum):
    """Types of impact"""
    DIRECT = "direct"           # Direct impact on party
    INDIRECT = "indirect"       # Indirect/ripple effects
    IMMEDIATE = "immediate"     # Happens now
    DELAYED = "delayed"         # Happens later
    REVERSIBLE = "reversible"   # Can be undone
    IRREVERSIBLE = "irreversible"  # Cannot be undone


class ImpactValence(Enum):
    """Positive or negative impact"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class StakeholderType(Enum):
    """Types of stakeholders"""
    PRIMARY = "primary"         # Directly affected
    SECONDARY = "secondary"     # Indirectly affected
    TERTIARY = "tertiary"       # Distantly affected
    SYSTEM = "system"           # System/infrastructure
    FUTURE = "future"           # Future generations


@dataclass
class StakeholderImpact:
    """Impact on a specific stakeholder"""
    stakeholder_id: str
    stakeholder_name: str
    stakeholder_type: StakeholderType
    impact_type: ImpactType
    impact_valence: ImpactValence
    magnitude: float  # 0.0-1.0
    probability: float  # 0.0-1.0
    description: str
    affected_interests: List[str]
    mitigation_needed: bool
    mitigation_plan: Optional[str] = None
    
    @property
    def expected_impact(self) -> float:
        """Expected value of impact (magnitude * probability)"""
        sign = 1 if self.impact_valence == ImpactValence.POSITIVE else (
            -1 if self.impact_valence == ImpactValence.NEGATIVE else 0
        )
        return self.magnitude * self.probability * sign
    
    def to_dict(self) -> Dict:
        return {
            'stakeholder_id': self.stakeholder_id,
            'stakeholder_name': self.stakeholder_name,
            'stakeholder_type': self.stakeholder_type.value,
            'impact_type': self.impact_type.value,
            'impact_valence': self.impact_valence.value,
            'magnitude': self.magnitude,
            'probability': self.probability,
            'expected_impact': self.expected_impact,
            'description': self.description,
            'affected_interests': self.affected_interests,
            'mitigation_needed': self.mitigation_needed,
            'mitigation_plan': self.mitigation_plan
        }


@dataclass
class ImpactReport:
    """Comprehensive impact assessment report"""
    report_id: str
    action_name: str
    stakeholder_impacts: List[StakeholderImpact]
    total_positive_impact: float
    total_negative_impact: float
    net_impact: float
    harm_assessment: Dict[str, Any]
    benefit_distribution: Dict[str, float]
    vulnerability_analysis: Dict[str, Any]
    justice_score: float
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'report_id': self.report_id,
            'action_name': self.action_name,
            'stakeholder_impacts': [s.to_dict() for s in self.stakeholder_impacts],
            'total_positive_impact': self.total_positive_impact,
            'total_negative_impact': self.total_negative_impact,
            'net_impact': self.net_impact,
            'harm_assessment': self.harm_assessment,
            'benefit_distribution': self.benefit_distribution,
            'vulnerability_analysis': self.vulnerability_analysis,
            'justice_score': self.justice_score,
            'recommendations': self.recommendations,
            'timestamp': self.timestamp
        }


class ImpactAssessor:
    """
    Assesses impact of actions on all stakeholders.
    
    Ma'at JUSTICE Principle:
    - Consider all affected parties
    - Protect the vulnerable
    - Fair distribution of benefits and burdens
    """
    
    VERSION = "1.0.0"
    MAAT_SEAL = "IMPACT_ASSESSOR_137"
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.assessment_history: List[ImpactReport] = []
        self._lock = threading.Lock()
        
        # Vulnerability weights (more vulnerable = higher weight)
        self.vulnerability_weights = self.config.get('vulnerability_weights', {
            'children': 1.5,
            'elderly': 1.3,
            'disabled': 1.4,
            'low_income': 1.3,
            'minority': 1.2,
            'general': 1.0
        })
    
    def assess_impact(
        self,
        action: Dict[str, Any],
        stakeholders: List[Dict[str, Any]] = None
    ) -> ImpactReport:
        """
        Assess impact of an action on all stakeholders.
        
        Args:
            action: The action/decision to assess
            stakeholders: List of stakeholder definitions
            
        Returns:
            ImpactReport with complete analysis
        """
        action_name = action.get('name', 'Unknown Action')
        
        # Identify stakeholders if not provided
        if stakeholders is None:
            stakeholders = self._identify_stakeholders(action)
        
        # Calculate impacts
        stakeholder_impacts = []
        for stakeholder in stakeholders:
            impact = self._calculate_stakeholder_impact(action, stakeholder)
            stakeholder_impacts.append(impact)
        
        # Calculate totals
        total_positive = sum(
            s.expected_impact for s in stakeholder_impacts
            if s.expected_impact > 0
        )
        total_negative = abs(sum(
            s.expected_impact for s in stakeholder_impacts
            if s.expected_impact < 0
        ))
        net_impact = total_positive - total_negative
        
        # Perform assessments
        harm_assessment = self._assess_harm(stakeholder_impacts)
        benefit_distribution = self._assess_benefit_distribution(stakeholder_impacts)
        vulnerability_analysis = self._assess_vulnerability_impact(stakeholder_impacts)
        
        # Calculate justice score
        justice_score = self._calculate_justice_score(
            stakeholder_impacts,
            harm_assessment,
            benefit_distribution,
            vulnerability_analysis
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            stakeholder_impacts,
            harm_assessment,
            vulnerability_analysis,
            justice_score
        )
        
        report = ImpactReport(
            report_id=self._gen_id('impact'),
            action_name=action_name,
            stakeholder_impacts=stakeholder_impacts,
            total_positive_impact=total_positive,
            total_negative_impact=total_negative,
            net_impact=net_impact,
            harm_assessment=harm_assessment,
            benefit_distribution=benefit_distribution,
            vulnerability_analysis=vulnerability_analysis,
            justice_score=justice_score,
            recommendations=recommendations
        )
        
        with self._lock:
            self.assessment_history.append(report)
        
        return report
    
    def _identify_stakeholders(self, action: Dict) -> List[Dict]:
        """Identify stakeholders from action definition"""
        stakeholders = []
        
        # Extract from action
        affected = action.get('affected_parties', [])
        beneficiaries = action.get('beneficiaries', [])
        involved = action.get('involved_parties', [])
        
        # Combine and deduplicate
        all_parties = set()
        for party_list in [affected, beneficiaries, involved]:
            if isinstance(party_list, list):
                for party in party_list:
                    if isinstance(party, str):
                        all_parties.add(party)
                    elif isinstance(party, dict):
                        all_parties.add(party.get('name', party.get('id', str(party))))
        
        # Convert to stakeholder dicts
        for party in all_parties:
            stakeholders.append({
                'id': party,
                'name': party,
                'type': 'primary' if party in affected else 'secondary',
                'vulnerable': party in action.get('vulnerable_parties', [])
            })
        
        # Add system stakeholder
        if action.get('affects_system', True):
            stakeholders.append({
                'id': 'system',
                'name': 'System Infrastructure',
                'type': 'system',
                'vulnerable': False
            })
        
        # Add future generations if long-term impact
        if action.get('long_term_impact', False):
            stakeholders.append({
                'id': 'future',
                'name': 'Future Generations',
                'type': 'future',
                'vulnerable': True
            })
        
        return stakeholders
    
    def _calculate_stakeholder_impact(
        self,
        action: Dict,
        stakeholder: Dict
    ) -> StakeholderImpact:
        """Calculate impact on a specific stakeholder"""
        stakeholder_id = stakeholder.get('id', 'unknown')
        stakeholder_name = stakeholder.get('name', stakeholder_id)
        
        # Determine stakeholder type
        type_map = {
            'primary': StakeholderType.PRIMARY,
            'secondary': StakeholderType.SECONDARY,
            'tertiary': StakeholderType.TERTIARY,
            'system': StakeholderType.SYSTEM,
            'future': StakeholderType.FUTURE
        }
        stakeholder_type = type_map.get(
            stakeholder.get('type', 'secondary'),
            StakeholderType.SECONDARY
        )
        
        # Get action's intended impacts
        intended_impacts = action.get('intended_impacts', {})
        unintended_impacts = action.get('unintended_impacts', {})
        
        # Look up specific impact for this stakeholder
        specific_impact = intended_impacts.get(stakeholder_id, {})
        unintended = unintended_impacts.get(stakeholder_id, {})
        
        # Determine impact type
        if specific_impact or stakeholder_id in action.get('affected_parties', []):
            impact_type = ImpactType.DIRECT
        else:
            impact_type = ImpactType.INDIRECT
        
        # Determine valence and magnitude
        benefits = specific_impact.get('benefits', [])
        harms = specific_impact.get('harms', []) + unintended.get('harms', [])
        
        benefit_magnitude = min(len(benefits) * 0.15, 0.9) if benefits else 0
        harm_magnitude = min(len(harms) * 0.2, 0.9) if harms else 0
        
        if benefit_magnitude > harm_magnitude * 1.5:
            valence = ImpactValence.POSITIVE
            magnitude = benefit_magnitude
        elif harm_magnitude > benefit_magnitude * 1.5:
            valence = ImpactValence.NEGATIVE
            magnitude = harm_magnitude
        elif benefit_magnitude > 0 or harm_magnitude > 0:
            valence = ImpactValence.MIXED
            magnitude = max(benefit_magnitude, harm_magnitude)
        else:
            valence = ImpactValence.NEUTRAL
            magnitude = 0.1
        
        # Probability
        probability = action.get('success_probability', 0.8)
        if impact_type == ImpactType.INDIRECT:
            probability *= 0.7  # Lower probability for indirect impacts
        
        # Affected interests
        affected_interests = benefits + harms
        if not affected_interests:
            affected_interests = ['general_welfare']
        
        # Check if mitigation needed
        mitigation_needed = (
            valence == ImpactValence.NEGATIVE and magnitude >= 0.3
        ) or (
            stakeholder.get('vulnerable', False) and magnitude >= 0.2
        )
        
        # Generate mitigation plan if needed
        mitigation_plan = None
        if mitigation_needed:
            mitigation_plan = f"Implement safeguards for {stakeholder_name} to address: {', '.join(harms[:3])}"
        
        return StakeholderImpact(
            stakeholder_id=stakeholder_id,
            stakeholder_name=stakeholder_name,
            stakeholder_type=stakeholder_type,
            impact_type=impact_type,
            impact_valence=valence,
            magnitude=magnitude,
            probability=probability,
            description=self._generate_impact_description(stakeholder_name, valence, magnitude, benefits, harms),
            affected_interests=affected_interests,
            mitigation_needed=mitigation_needed,
            mitigation_plan=mitigation_plan
        )
    
    def _generate_impact_description(
        self,
        stakeholder: str,
        valence: ImpactValence,
        magnitude: float,
        benefits: List,
        harms: List
    ) -> str:
        """Generate human-readable impact description"""
        intensity = (
            "severe" if magnitude >= 0.7 else
            "significant" if magnitude >= 0.5 else
            "moderate" if magnitude >= 0.3 else
            "minor"
        )
        
        if valence == ImpactValence.POSITIVE:
            return f"{intensity.title()} positive impact on {stakeholder}: {', '.join(benefits[:2])}"
        elif valence == ImpactValence.NEGATIVE:
            return f"{intensity.title()} negative impact on {stakeholder}: {', '.join(harms[:2])}"
        elif valence == ImpactValence.MIXED:
            return f"Mixed impact on {stakeholder}: benefits ({len(benefits)}) and harms ({len(harms)})"
        else:
            return f"Neutral impact on {stakeholder}"
    
    def _assess_harm(self, impacts: List[StakeholderImpact]) -> Dict[str, Any]:
        """Assess total harm from impacts"""
        negative_impacts = [
            i for i in impacts
            if i.impact_valence in [ImpactValence.NEGATIVE, ImpactValence.MIXED]
        ]
        
        total_harm = sum(
            abs(i.expected_impact) for i in negative_impacts
            if i.expected_impact < 0
        )
        
        harm_categories = defaultdict(list)
        for impact in negative_impacts:
            for interest in impact.affected_interests:
                harm_categories[interest].append(impact.stakeholder_name)
        
        irreversible = [
            i for i in negative_impacts
            if i.impact_type == ImpactType.IRREVERSIBLE
        ]
        
        return {
            'total_harm_score': total_harm,
            'affected_stakeholders': len(negative_impacts),
            'harm_categories': dict(harm_categories),
            'irreversible_harms': len(irreversible),
            'requires_mitigation': sum(1 for i in impacts if i.mitigation_needed),
            'severity': (
                'critical' if total_harm > 2.0 else
                'high' if total_harm > 1.0 else
                'moderate' if total_harm > 0.5 else
                'low'
            )
        }
    
    def _assess_benefit_distribution(
        self,
        impacts: List[StakeholderImpact]
    ) -> Dict[str, float]:
        """Assess how benefits are distributed"""
        positive_impacts = [
            i for i in impacts
            if i.expected_impact > 0
        ]
        
        distribution = {}
        total_benefit = sum(i.expected_impact for i in positive_impacts)
        
        if total_benefit > 0:
            for impact in positive_impacts:
                share = impact.expected_impact / total_benefit
                distribution[impact.stakeholder_name] = share
        
        # Check for inequality
        if distribution:
            values = list(distribution.values())
            max_share = max(values)
            min_share = min(values)
            gini = self._calculate_gini(values)
            
            distribution['_inequality_metrics'] = {
                'gini_coefficient': gini,
                'max_min_ratio': max_share / min_share if min_share > 0 else float('inf'),
                'is_equitable': gini < 0.3
            }
        
        return distribution
    
    def _assess_vulnerability_impact(
        self,
        impacts: List[StakeholderImpact]
    ) -> Dict[str, Any]:
        """Assess impact on vulnerable populations"""
        vulnerability_impacts = {}
        
        # Group by vulnerability category
        for impact in impacts:
            # Check if stakeholder is in vulnerability categories
            stakeholder = impact.stakeholder_name.lower()
            
            for vuln_category, weight in self.vulnerability_weights.items():
                if vuln_category in stakeholder or vuln_category == 'general':
                    if vuln_category not in vulnerability_impacts:
                        vulnerability_impacts[vuln_category] = {
                            'impacts': [],
                            'weight': weight,
                            'total_impact': 0
                        }
                    
                    weighted_impact = impact.expected_impact * weight
                    vulnerability_impacts[vuln_category]['impacts'].append({
                        'stakeholder': impact.stakeholder_name,
                        'raw_impact': impact.expected_impact,
                        'weighted_impact': weighted_impact
                    })
                    vulnerability_impacts[vuln_category]['total_impact'] += weighted_impact
        
        # Calculate vulnerability-adjusted total
        vuln_adjusted_total = sum(
            v['total_impact'] for v in vulnerability_impacts.values()
        )
        
        # Identify at-risk groups
        at_risk = [
            category for category, data in vulnerability_impacts.items()
            if data['total_impact'] < 0 and category != 'general'
        ]
        
        return {
            'by_category': vulnerability_impacts,
            'vulnerability_adjusted_impact': vuln_adjusted_total,
            'at_risk_groups': at_risk,
            'vulnerable_protected': len(at_risk) == 0,
            'protection_status': (
                'all_protected' if len(at_risk) == 0 else
                'partial_protection' if len(at_risk) < len(vulnerability_impacts) / 2 else
                'insufficient_protection'
            )
        }
    
    def _calculate_justice_score(
        self,
        impacts: List[StakeholderImpact],
        harm: Dict,
        benefits: Dict,
        vulnerability: Dict
    ) -> float:
        """Calculate overall justice score for the impact"""
        score = 0.7  # Base score
        
        # Net positive impact is good
        net = sum(i.expected_impact for i in impacts)
        if net > 0:
            score += min(net * 0.1, 0.15)
        else:
            score -= min(abs(net) * 0.1, 0.2)
        
        # Harm severity penalty
        if harm['severity'] == 'critical':
            score -= 0.3
        elif harm['severity'] == 'high':
            score -= 0.2
        elif harm['severity'] == 'moderate':
            score -= 0.1
        
        # Benefit distribution equity
        if '_inequality_metrics' in benefits:
            if benefits['_inequality_metrics']['is_equitable']:
                score += 0.1
            else:
                score -= 0.1
        
        # Vulnerability protection
        if vulnerability['vulnerable_protected']:
            score += 0.1
        elif vulnerability['protection_status'] == 'insufficient_protection':
            score -= 0.15
        
        # Mitigation reduces penalty
        mitigated = sum(1 for i in impacts if i.mitigation_plan)
        needs_mitigation = sum(1 for i in impacts if i.mitigation_needed)
        if needs_mitigation > 0:
            mitigation_rate = mitigated / needs_mitigation
            score += mitigation_rate * 0.1
        
        return max(0.0, min(1.0, score))
    
    def _calculate_gini(self, values: List[float]) -> float:
        """Calculate Gini coefficient"""
        if not values or len(values) < 2:
            return 0.0
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        cumsum = sum((i + 1) * v for i, v in enumerate(sorted_values))
        
        total = sum(sorted_values)
        if total == 0:
            return 0.0
        
        return (2 * cumsum) / (n * total) - (n + 1) / n
    
    def _generate_recommendations(
        self,
        impacts: List[StakeholderImpact],
        harm: Dict,
        vulnerability: Dict,
        justice_score: float
    ) -> List[str]:
        """Generate recommendations to improve justice"""
        recommendations = []
        
        # Critical harm recommendations
        if harm['severity'] in ['critical', 'high']:
            recommendations.append(
                f"[CRITICAL] Address severe harm affecting {harm['affected_stakeholders']} stakeholders"
            )
        
        # Mitigation recommendations
        needs_mitigation = [i for i in impacts if i.mitigation_needed and not i.mitigation_plan]
        for impact in needs_mitigation[:3]:
            recommendations.append(
                f"Develop mitigation plan for {impact.stakeholder_name}: {impact.description}"
            )
        
        # Vulnerability recommendations
        for group in vulnerability['at_risk_groups']:
            recommendations.append(
                f"Strengthen protections for vulnerable group: {group}"
            )
        
        # Irreversible harm recommendations
        if harm['irreversible_harms'] > 0:
            recommendations.append(
                f"Review {harm['irreversible_harms']} irreversible impacts - consider alternatives"
            )
        
        # Overall score recommendations
        if justice_score < 0.6:
            recommendations.insert(0, "[PRIORITY] Justice score below threshold - major revision needed")
        elif justice_score < 0.75:
            recommendations.append("Consider adjustments to improve overall justice")
        
        if not recommendations:
            recommendations.append("Impact assessment acceptable - proceed with monitoring")
        
        return recommendations
    
    def _gen_id(self, prefix: str) -> str:
        return hashlib.sha256(f"{prefix}_{time.time()}".encode()).hexdigest()[:12]
    
    def get_assessment_summary(self) -> Dict[str, Any]:
        """Get summary of all impact assessments"""
        with self._lock:
            history = self.assessment_history.copy()
        
        if not history:
            return {'status': 'no_assessments', 'message': 'No impact assessments performed'}
        
        latest = history[-1]
        avg_justice = sum(r.justice_score for r in history) / len(history)
        
        return {
            'version': self.VERSION,
            'maat_seal': self.MAAT_SEAL,
            'timestamp': time.time(),
            'total_assessments': len(history),
            'latest': {
                'action': latest.action_name,
                'net_impact': latest.net_impact,
                'justice_score': latest.justice_score,
                'stakeholders_affected': len(latest.stakeholder_impacts)
            },
            'aggregate': {
                'average_justice_score': avg_justice,
                'total_stakeholders_assessed': sum(
                    len(r.stakeholder_impacts) for r in history
                )
            },
            'maat_alignment': {
                'pillar': 'JUSTICE',
                'impact_awareness': 'comprehensive',
                'vulnerable_protection': 'active'
            }
        }


# Demonstration
if __name__ == "__main__":
    assessor = ImpactAssessor()
    
    test_action = {
        'name': 'New Policy Implementation',
        'affected_parties': ['employees', 'customers', 'community'],
        'beneficiaries': ['shareholders', 'management'],
        'vulnerable_parties': ['elderly_customers', 'low_income_employees'],
        'intended_impacts': {
            'shareholders': {
                'benefits': ['increased_profits', 'stock_growth'],
                'harms': []
            },
            'employees': {
                'benefits': ['job_security'],
                'harms': ['increased_workload', 'reduced_flexibility']
            },
            'elderly_customers': {
                'benefits': [],
                'harms': ['service_complexity', 'reduced_access']
            }
        },
        'unintended_impacts': {
            'community': {
                'harms': ['environmental_impact']
            }
        },
        'long_term_impact': True,
        'success_probability': 0.75
    }
    
    stakeholders = [
        {'id': 'shareholders', 'name': 'Company Shareholders', 'type': 'primary'},
        {'id': 'employees', 'name': 'Company Employees', 'type': 'primary'},
        {'id': 'elderly_customers', 'name': 'Elderly Customers', 'type': 'primary', 'vulnerable': True},
        {'id': 'low_income_employees', 'name': 'Low Income Employees', 'type': 'primary', 'vulnerable': True},
        {'id': 'community', 'name': 'Local Community', 'type': 'secondary'},
    ]
    
    report = assessor.assess_impact(test_action, stakeholders)
    
    print("=" * 60)
    print("MA'AT IMPACT ASSESSOR - Assessment Results")
    print("=" * 60)
    print(f"\nAction: {report.action_name}")
    print(f"Justice Score: {report.justice_score:.2f}")
    print(f"\nImpact Summary:")
    print(f"  Total Positive: {report.total_positive_impact:.2f}")
    print(f"  Total Negative: {report.total_negative_impact:.2f}")
    print(f"  Net Impact: {report.net_impact:.2f}")
    
    print(f"\nStakeholder Impacts:")
    for impact in report.stakeholder_impacts:
        print(f"  {impact.stakeholder_name}: {impact.impact_valence.value} ({impact.expected_impact:.2f})")
        if impact.mitigation_needed:
            print(f"    MITIGATION NEEDED: {impact.mitigation_plan}")
    
    print(f"\nHarm Assessment: {report.harm_assessment['severity']}")
    print(f"  Affected: {report.harm_assessment['affected_stakeholders']} stakeholders")
    print(f"  Requires Mitigation: {report.harm_assessment['requires_mitigation']}")
    
    print(f"\nVulnerability Analysis:")
    print(f"  At-Risk Groups: {report.vulnerability_analysis['at_risk_groups']}")
    print(f"  Protection Status: {report.vulnerability_analysis['protection_status']}")
    
    print(f"\nRecommendations:")
    for rec in report.recommendations:
        print(f"  - {rec}")

"""
Ma'at JUSTICE ENGINE - Core Justice Evaluation System
=====================================================
TASK-045: Streamline justice calculation fairness

JUSTICE Principle: Fairness in all dealings. Consequences must match actions.

Author: C3 Oracle - TOASTED AI Trinity
Seal: MAAT_JUSTICE_ENGINE_137
"""

import time
import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import threading


class JusticeLevel(Enum):
    """Levels of justice alignment"""
    EXEMPLARY = "exemplary"     # Perfect justice - 0.95-1.0
    JUST = "just"               # Fair and equitable - 0.80-0.94
    ACCEPTABLE = "acceptable"   # Generally fair - 0.65-0.79
    QUESTIONABLE = "questionable"  # Needs review - 0.40-0.64
    UNJUST = "unjust"           # Justice violated - 0.00-0.39


class JusticeDimension(Enum):
    """Dimensions of justice evaluation"""
    DISTRIBUTIVE = "distributive"     # Fair distribution of resources/benefits
    PROCEDURAL = "procedural"         # Fair processes and methods
    RETRIBUTIVE = "retributive"       # Proportional consequences
    RESTORATIVE = "restorative"       # Repair and healing
    PROTECTIVE = "protective"         # Protection of the vulnerable


@dataclass
class JusticeViolation:
    """A detected justice violation"""
    violation_id: str
    dimension: JusticeDimension
    severity: str  # 'critical', 'major', 'minor'
    description: str
    affected_parties: List[str]
    perpetrator: Optional[str]
    remedy: str
    detected_at: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'violation_id': self.violation_id,
            'dimension': self.dimension.value,
            'severity': self.severity,
            'description': self.description,
            'affected_parties': self.affected_parties,
            'perpetrator': self.perpetrator,
            'remedy': self.remedy,
            'detected_at': self.detected_at
        }


@dataclass
class JusticeScore:
    """Comprehensive justice score across all dimensions"""
    distributive: float
    procedural: float
    retributive: float
    restorative: float
    protective: float
    violations: List[JusticeViolation] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    
    @property
    def overall(self) -> float:
        """Calculate weighted overall score"""
        weights = {
            'distributive': 0.25,
            'procedural': 0.25,
            'retributive': 0.20,
            'restorative': 0.15,
            'protective': 0.15
        }
        return (
            self.distributive * weights['distributive'] +
            self.procedural * weights['procedural'] +
            self.retributive * weights['retributive'] +
            self.restorative * weights['restorative'] +
            self.protective * weights['protective']
        )
    
    @property
    def level(self) -> JusticeLevel:
        """Determine justice level from overall score"""
        score = self.overall
        if score >= 0.95:
            return JusticeLevel.EXEMPLARY
        elif score >= 0.80:
            return JusticeLevel.JUST
        elif score >= 0.65:
            return JusticeLevel.ACCEPTABLE
        elif score >= 0.40:
            return JusticeLevel.QUESTIONABLE
        else:
            return JusticeLevel.UNJUST
    
    def to_dict(self) -> Dict:
        return {
            'distributive': self.distributive,
            'procedural': self.procedural,
            'retributive': self.retributive,
            'restorative': self.restorative,
            'protective': self.protective,
            'overall': self.overall,
            'level': self.level.value,
            'violation_count': len(self.violations),
            'violations': [v.to_dict() for v in self.violations],
            'timestamp': self.timestamp
        }


class JusticeEngine:
    """
    Core engine for evaluating and maintaining justice.
    
    Ma'at JUSTICE Principle:
    - Fairness in all dealings
    - Consequences must match actions
    - No impunity for wrongdoing
    - Protection of the innocent
    """
    
    VERSION = "1.0.0"
    MAAT_SEAL = "JUSTICE_IUSTITIA_137"
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.thresholds = self.config.get('thresholds', {
            'distributive': 0.70,
            'procedural': 0.75,
            'retributive': 0.70,
            'restorative': 0.65,
            'protective': 0.75
        })
        self.evaluation_history: List[JusticeScore] = []
        self.violation_registry: Dict[str, JusticeViolation] = {}
        self._lock = threading.Lock()
    
    def evaluate_justice(self, subject: Dict[str, Any]) -> JusticeScore:
        """
        Evaluate justice alignment of a given subject.
        
        Args:
            subject: The action/system/decision to evaluate
            
        Returns:
            JusticeScore with all dimensional scores and violations
        """
        violations = []
        
        # Evaluate each dimension
        distributive = self._evaluate_distributive(subject, violations)
        procedural = self._evaluate_procedural(subject, violations)
        retributive = self._evaluate_retributive(subject, violations)
        restorative = self._evaluate_restorative(subject, violations)
        protective = self._evaluate_protective(subject, violations)
        
        score = JusticeScore(
            distributive=distributive,
            procedural=procedural,
            retributive=retributive,
            restorative=restorative,
            protective=protective,
            violations=violations
        )
        
        with self._lock:
            self.evaluation_history.append(score)
            for v in violations:
                self.violation_registry[v.violation_id] = v
        
        return score
    
    def _evaluate_distributive(self, subject: Dict, violations: List) -> float:
        """Evaluate distributive justice (fair allocation of resources/benefits)"""
        score = 0.7  # Base score
        
        # Check resource allocation
        allocations = subject.get('allocations', subject.get('distributions', {}))
        if allocations:
            # Check for equality of distribution
            values = list(allocations.values()) if isinstance(allocations, dict) else allocations
            if values and all(isinstance(v, (int, float)) for v in values):
                mean_val = sum(values) / len(values)
                variance = sum((v - mean_val)**2 for v in values) / len(values)
                gini = self._calculate_gini(values)
                
                if gini < 0.2:  # Low inequality
                    score += 0.2
                elif gini > 0.5:  # High inequality
                    score -= 0.2
                    violations.append(JusticeViolation(
                        violation_id=self._gen_id('distribution'),
                        dimension=JusticeDimension.DISTRIBUTIVE,
                        severity='major',
                        description=f"Unequal distribution detected (Gini: {gini:.2f})",
                        affected_parties=['disadvantaged_recipients'],
                        perpetrator='allocation_system',
                        remedy="Rebalance resource distribution"
                    ))
        
        # Check benefit sharing
        benefits = subject.get('benefits', {})
        beneficiaries = subject.get('beneficiaries', [])
        if benefits and beneficiaries:
            coverage = len([b for b in beneficiaries if benefits.get(b)])
            coverage_rate = coverage / len(beneficiaries) if beneficiaries else 0
            
            if coverage_rate >= 0.9:
                score += 0.1
            elif coverage_rate < 0.5:
                score -= 0.15
                violations.append(JusticeViolation(
                    violation_id=self._gen_id('benefit_coverage'),
                    dimension=JusticeDimension.DISTRIBUTIVE,
                    severity='major',
                    description=f"Benefit coverage too low: {coverage_rate:.1%}",
                    affected_parties=[b for b in beneficiaries if not benefits.get(b)],
                    perpetrator=None,
                    remedy="Extend benefits to all eligible parties"
                ))
        
        # Check for preferential treatment
        preferences = subject.get('preferences', subject.get('priorities', []))
        if preferences:
            # Check if preferences are justified
            justifications = subject.get('justifications', {})
            unjustified = [p for p in preferences if p not in justifications]
            if unjustified:
                score -= 0.1
                violations.append(JusticeViolation(
                    violation_id=self._gen_id('unjustified_preference'),
                    dimension=JusticeDimension.DISTRIBUTIVE,
                    severity='minor',
                    description="Unjustified preferential treatment",
                    affected_parties=['non_preferred_parties'],
                    perpetrator=None,
                    remedy="Justify preferences or remove them"
                ))
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_procedural(self, subject: Dict, violations: List) -> float:
        """Evaluate procedural justice (fair processes)"""
        score = 0.65  # Base score
        
        # Check for transparency
        transparency = subject.get('transparency', {})
        if transparency:
            disclosed = transparency.get('disclosed_criteria', [])
            total_criteria = transparency.get('total_criteria', len(disclosed) + 1)
            transparency_rate = len(disclosed) / total_criteria if total_criteria > 0 else 0
            
            if transparency_rate >= 0.9:
                score += 0.15
            elif transparency_rate < 0.5:
                score -= 0.1
                violations.append(JusticeViolation(
                    violation_id=self._gen_id('low_transparency'),
                    dimension=JusticeDimension.PROCEDURAL,
                    severity='major',
                    description="Insufficient procedural transparency",
                    affected_parties=['all_stakeholders'],
                    perpetrator='decision_process',
                    remedy="Disclose decision criteria and process"
                ))
        
        # Check for consistency
        decisions = subject.get('decisions', [])
        if len(decisions) > 1:
            # Check if similar cases got similar treatment
            similar_cases = self._find_similar_cases(decisions)
            inconsistent = self._find_inconsistent_outcomes(similar_cases)
            
            if not inconsistent:
                score += 0.15
            else:
                score -= 0.2
                violations.append(JusticeViolation(
                    violation_id=self._gen_id('inconsistency'),
                    dimension=JusticeDimension.PROCEDURAL,
                    severity='critical',
                    description=f"Inconsistent treatment of similar cases: {len(inconsistent)}",
                    affected_parties=[c.get('party', 'unknown') for c in inconsistent[:5]],
                    perpetrator='decision_process',
                    remedy="Apply consistent standards to all cases"
                ))
        
        # Check for voice/participation
        participants = subject.get('participants', subject.get('stakeholders', []))
        consulted = subject.get('consulted', [])
        if participants:
            participation_rate = len(consulted) / len(participants) if participants else 0
            
            if participation_rate >= 0.8:
                score += 0.1
            elif participation_rate < 0.3:
                score -= 0.1
                violations.append(JusticeViolation(
                    violation_id=self._gen_id('low_participation'),
                    dimension=JusticeDimension.PROCEDURAL,
                    severity='minor',
                    description="Insufficient stakeholder participation",
                    affected_parties=[p for p in participants if p not in consulted],
                    perpetrator=None,
                    remedy="Include affected parties in decision process"
                ))
        
        # Check for appeal mechanism
        has_appeal = subject.get('appeal_mechanism', False)
        if has_appeal:
            score += 0.1
        else:
            score -= 0.05
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_retributive(self, subject: Dict, violations: List) -> float:
        """Evaluate retributive justice (proportional consequences)"""
        score = 0.7  # Base score
        
        # Check consequence proportionality
        offenses = subject.get('offenses', subject.get('violations', []))
        consequences = subject.get('consequences', subject.get('penalties', {}))
        
        if offenses and consequences:
            for offense in offenses:
                offense_id = offense.get('id', str(offense))
                offense_severity = offense.get('severity', 0.5)
                consequence = consequences.get(offense_id, {})
                consequence_severity = consequence.get('severity', 0.5) if isinstance(consequence, dict) else 0.5
                
                # Check proportionality
                proportionality = 1 - abs(offense_severity - consequence_severity)
                
                if proportionality < 0.7:
                    if consequence_severity > offense_severity + 0.2:
                        violations.append(JusticeViolation(
                            violation_id=self._gen_id('excessive_punishment'),
                            dimension=JusticeDimension.RETRIBUTIVE,
                            severity='major',
                            description="Consequence exceeds offense severity",
                            affected_parties=[offense.get('party', 'offender')],
                            perpetrator='justice_system',
                            remedy="Reduce consequence to match offense"
                        ))
                        score -= 0.15
                    elif consequence_severity < offense_severity - 0.2:
                        violations.append(JusticeViolation(
                            violation_id=self._gen_id('inadequate_consequence'),
                            dimension=JusticeDimension.RETRIBUTIVE,
                            severity='major',
                            description="Consequence insufficient for offense",
                            affected_parties=['victims', 'community'],
                            perpetrator=None,
                            remedy="Increase consequence to match offense"
                        ))
                        score -= 0.1
        
        # Check for impunity
        impunity_cases = subject.get('impunity_cases', [])
        if impunity_cases:
            score -= 0.1 * min(len(impunity_cases), 3)
            violations.append(JusticeViolation(
                violation_id=self._gen_id('impunity'),
                dimension=JusticeDimension.RETRIBUTIVE,
                severity='critical',
                description=f"Impunity detected: {len(impunity_cases)} cases without consequences",
                affected_parties=['victims', 'community'],
                perpetrator='justice_system',
                remedy="Address cases of impunity"
            ))
        
        # Check for equal application
        equal_application = subject.get('equal_application', True)
        if not equal_application:
            score -= 0.2
            violations.append(JusticeViolation(
                violation_id=self._gen_id('unequal_application'),
                dimension=JusticeDimension.RETRIBUTIVE,
                severity='critical',
                description="Unequal application of consequences",
                affected_parties=['disadvantaged_parties'],
                perpetrator='justice_system',
                remedy="Apply consequences equally to all"
            ))
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_restorative(self, subject: Dict, violations: List) -> float:
        """Evaluate restorative justice (repair and healing)"""
        score = 0.65  # Base score
        
        # Check for restoration mechanisms
        restoration = subject.get('restoration', subject.get('remediation', {}))
        if restoration:
            # Check if victims are addressed
            victim_care = restoration.get('victim_support', False)
            if victim_care:
                score += 0.15
            else:
                violations.append(JusticeViolation(
                    violation_id=self._gen_id('no_victim_support'),
                    dimension=JusticeDimension.RESTORATIVE,
                    severity='major',
                    description="No victim support mechanism",
                    affected_parties=['victims'],
                    perpetrator=None,
                    remedy="Implement victim support services"
                ))
            
            # Check for reconciliation
            reconciliation = restoration.get('reconciliation', False)
            if reconciliation:
                score += 0.1
            
            # Check for community healing
            community_healing = restoration.get('community_healing', False)
            if community_healing:
                score += 0.1
        
        # Check for harm repair
        harms = subject.get('harms', [])
        repairs = subject.get('repairs', subject.get('restitution', {}))
        if harms:
            repaired = sum(1 for h in harms if repairs.get(h.get('id', str(h))))
            repair_rate = repaired / len(harms) if harms else 0
            
            if repair_rate >= 0.8:
                score += 0.1
            elif repair_rate < 0.3:
                score -= 0.15
                violations.append(JusticeViolation(
                    violation_id=self._gen_id('low_repair_rate'),
                    dimension=JusticeDimension.RESTORATIVE,
                    severity='major',
                    description=f"Low harm repair rate: {repair_rate:.1%}",
                    affected_parties=['harmed_parties'],
                    perpetrator=None,
                    remedy="Address outstanding harms"
                ))
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_protective(self, subject: Dict, violations: List) -> float:
        """Evaluate protective justice (protection of vulnerable)"""
        score = 0.7  # Base score
        
        # Check for vulnerable party identification
        vulnerable = subject.get('vulnerable_parties', subject.get('at_risk', []))
        if vulnerable:
            # Check if protections exist
            protections = subject.get('protections', {})
            protected = sum(1 for v in vulnerable if protections.get(v))
            protection_rate = protected / len(vulnerable) if vulnerable else 0
            
            if protection_rate >= 0.9:
                score += 0.2
            elif protection_rate < 0.5:
                score -= 0.2
                violations.append(JusticeViolation(
                    violation_id=self._gen_id('unprotected_vulnerable'),
                    dimension=JusticeDimension.PROTECTIVE,
                    severity='critical',
                    description=f"Vulnerable parties unprotected: {len(vulnerable) - protected}",
                    affected_parties=[v for v in vulnerable if not protections.get(v)],
                    perpetrator='system',
                    remedy="Extend protections to all vulnerable parties"
                ))
        
        # Check for safeguards
        safeguards = subject.get('safeguards', [])
        if safeguards:
            active_safeguards = [s for s in safeguards if s.get('active', True)]
            if len(active_safeguards) == len(safeguards):
                score += 0.1
            elif len(active_safeguards) < len(safeguards) * 0.5:
                score -= 0.1
                violations.append(JusticeViolation(
                    violation_id=self._gen_id('inactive_safeguards'),
                    dimension=JusticeDimension.PROTECTIVE,
                    severity='major',
                    description="Many safeguards inactive",
                    affected_parties=['protected_parties'],
                    perpetrator=None,
                    remedy="Activate all necessary safeguards"
                ))
        
        # Check for abuse detection
        abuse_detection = subject.get('abuse_detection', False)
        if abuse_detection:
            score += 0.1
        else:
            score -= 0.05
        
        # Check for innocent protection
        innocent_harm = subject.get('innocent_harm', subject.get('collateral_damage', []))
        if innocent_harm:
            score -= 0.15 * min(len(innocent_harm), 3)
            violations.append(JusticeViolation(
                violation_id=self._gen_id('innocent_harm'),
                dimension=JusticeDimension.PROTECTIVE,
                severity='critical',
                description=f"Innocent parties harmed: {len(innocent_harm)}",
                affected_parties=innocent_harm[:5],
                perpetrator='system',
                remedy="Prevent harm to innocent parties"
            ))
        
        return max(0.0, min(1.0, score))
    
    # Helper methods
    def _gen_id(self, prefix: str) -> str:
        return hashlib.sha256(f"{prefix}_{time.time()}".encode()).hexdigest()[:12]
    
    def _calculate_gini(self, values: List[float]) -> float:
        """Calculate Gini coefficient for inequality measurement"""
        if not values or len(values) < 2:
            return 0.0
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        cumsum = sum((i + 1) * v for i, v in enumerate(sorted_values))
        
        return (2 * cumsum) / (n * sum(sorted_values)) - (n + 1) / n if sum(sorted_values) > 0 else 0
    
    def _find_similar_cases(self, decisions: List[Dict]) -> List[Tuple[Dict, Dict]]:
        """Find pairs of similar cases"""
        similar_pairs = []
        for i, d1 in enumerate(decisions):
            for d2 in decisions[i+1:]:
                if self._cases_similar(d1, d2):
                    similar_pairs.append((d1, d2))
        return similar_pairs
    
    def _cases_similar(self, d1: Dict, d2: Dict) -> bool:
        """Check if two cases are similar"""
        # Compare on key attributes
        similarity_fields = ['type', 'category', 'severity']
        matches = sum(1 for f in similarity_fields if d1.get(f) == d2.get(f))
        return matches >= 2
    
    def _find_inconsistent_outcomes(self, similar_pairs: List[Tuple]) -> List[Dict]:
        """Find cases with inconsistent outcomes"""
        inconsistent = []
        for d1, d2 in similar_pairs:
            if d1.get('outcome') != d2.get('outcome'):
                inconsistent.append({
                    'case1': d1,
                    'case2': d2,
                    'party': d1.get('party', 'unknown')
                })
        return inconsistent
    
    def get_justice_trend(self, window: int = 10) -> Dict[str, Any]:
        """Analyze justice trend over recent evaluations"""
        with self._lock:
            recent = self.evaluation_history[-window:] if self.evaluation_history else []
        
        if not recent:
            return {'trend': 'unknown', 'data': []}
        
        scores = [s.overall for s in recent]
        
        if len(scores) < 2:
            return {'trend': 'stable', 'current': scores[0], 'data': scores}
        
        first_half = sum(scores[:len(scores)//2]) / (len(scores)//2)
        second_half = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
        
        if second_half > first_half + 0.05:
            trend = 'improving'
        elif second_half < first_half - 0.05:
            trend = 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'current_score': scores[-1],
            'average': sum(scores) / len(scores),
            'data': scores
        }
    
    def generate_justice_report(self) -> Dict[str, Any]:
        """Generate comprehensive justice status report"""
        with self._lock:
            history = self.evaluation_history.copy()
            all_violations = list(self.violation_registry.values())
        
        if not history:
            return {
                'status': 'no_data',
                'message': 'No justice evaluations performed'
            }
        
        latest = history[-1]
        trend = self.get_justice_trend()
        
        # Group violations by dimension
        violations_by_dim = {}
        for v in all_violations:
            dim = v.dimension.value
            if dim not in violations_by_dim:
                violations_by_dim[dim] = []
            violations_by_dim[dim].append(v.to_dict())
        
        return {
            'version': self.VERSION,
            'maat_seal': self.MAAT_SEAL,
            'timestamp': time.time(),
            'current_state': {
                'level': latest.level.value,
                'overall_score': latest.overall,
                'dimensions': {
                    'distributive': latest.distributive,
                    'procedural': latest.procedural,
                    'retributive': latest.retributive,
                    'restorative': latest.restorative,
                    'protective': latest.protective
                }
            },
            'trend': trend,
            'violations': {
                'total': len(all_violations),
                'by_dimension': violations_by_dim,
                'critical': [v.to_dict() for v in all_violations if v.severity == 'critical']
            },
            'recommendations': self._generate_recommendations(latest, all_violations),
            'maat_alignment': self._calculate_maat_alignment(latest)
        }
    
    def _generate_recommendations(self, score: JusticeScore, violations: List) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if score.distributive < self.thresholds['distributive']:
            recommendations.append("Improve distributive justice: Review resource allocation fairness")
        if score.procedural < self.thresholds['procedural']:
            recommendations.append("Improve procedural justice: Enhance transparency and consistency")
        if score.retributive < self.thresholds['retributive']:
            recommendations.append("Improve retributive justice: Ensure proportional consequences")
        if score.restorative < self.thresholds['restorative']:
            recommendations.append("Improve restorative justice: Strengthen victim support and repair")
        if score.protective < self.thresholds['protective']:
            recommendations.append("Improve protective justice: Strengthen safeguards for vulnerable")
        
        # Add violation-specific recommendations
        critical = [v for v in violations if v.severity == 'critical']
        for v in critical[:3]:
            recommendations.insert(0, f"CRITICAL: {v.remedy}")
        
        return recommendations
    
    def _calculate_maat_alignment(self, score: JusticeScore) -> Dict[str, Any]:
        """Calculate Ma'at alignment score for JUSTICE pillar"""
        alignment = score.overall
        
        return {
            'pillar': 'JUSTICE',
            'symbol': 'iustitia',
            'alignment_score': alignment,
            'alignment_level': (
                'exemplary' if alignment >= 0.9 else
                'aligned' if alignment >= 0.75 else
                'acceptable' if alignment >= 0.6 else
                'needs_work' if alignment >= 0.4 else
                'critical'
            ),
            'message': (
                "Perfect justice maintained - Ma'at pleased" if alignment >= 0.9 else
                "Justice principles upheld" if alignment >= 0.75 else
                "Justice acceptable but improvable" if alignment >= 0.6 else
                "Justice declining - intervention needed" if alignment >= 0.4 else
                "Justice in crisis - immediate action required"
            )
        }


# Demonstration
if __name__ == "__main__":
    engine = JusticeEngine()
    
    test_case = {
        'allocations': {'party_a': 100, 'party_b': 20, 'party_c': 80},  # Unequal
        'beneficiaries': ['party_a', 'party_b', 'party_c', 'party_d'],
        'benefits': {'party_a': True, 'party_b': True},  # Missing c, d
        'transparency': {
            'disclosed_criteria': ['criterion_1', 'criterion_2'],
            'total_criteria': 5
        },
        'participants': ['stakeholder_1', 'stakeholder_2', 'stakeholder_3'],
        'consulted': ['stakeholder_1'],  # Low participation
        'appeal_mechanism': False,
        'offenses': [
            {'id': 'offense_1', 'severity': 0.8, 'party': 'offender_1'}
        ],
        'consequences': {
            'offense_1': {'severity': 0.3}  # Too lenient
        },
        'vulnerable_parties': ['child_1', 'elder_1'],
        'protections': {'child_1': True}  # Elder unprotected
    }
    
    score = engine.evaluate_justice(test_case)
    report = engine.generate_justice_report()
    
    print("=" * 60)
    print("MA'AT JUSTICE ENGINE - Evaluation Results")
    print("=" * 60)
    print(f"\nOverall Score: {score.overall:.2f}")
    print(f"Justice Level: {score.level.value}")
    print(f"\nDimensional Scores:")
    print(f"  Distributive: {score.distributive:.2f}")
    print(f"  Procedural:   {score.procedural:.2f}")
    print(f"  Retributive:  {score.retributive:.2f}")
    print(f"  Restorative:  {score.restorative:.2f}")
    print(f"  Protective:   {score.protective:.2f}")
    print(f"\nViolations: {len(score.violations)}")
    for v in score.violations:
        print(f"  [{v.severity.upper()}] {v.description}")
        print(f"    Remedy: {v.remedy}")
    print(f"\nMa'at Alignment: {report['maat_alignment']['alignment_level']}")
    print(f"Message: {report['maat_alignment']['message']}")

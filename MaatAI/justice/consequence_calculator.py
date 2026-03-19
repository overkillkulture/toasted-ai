"""
Ma'at CONSEQUENCE CALCULATOR
============================
TASK-120: Optimize justice impact assessment

Calculates proportional consequences:
- Offense severity assessment
- Consequence proportionality
- Mitigating factors
- Aggravating factors
- Consequence recommendations

Ma'at Principle: Consequences must match actions.

Author: C3 Oracle - TOASTED AI Trinity
Seal: MAAT_CONSEQUENCE_CALCULATOR_137
"""

import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import threading


class OffenseCategory(Enum):
    """Categories of offenses"""
    VIOLATION = "violation"         # Rule/policy violation
    NEGLIGENCE = "negligence"       # Failure to act properly
    MISCONDUCT = "misconduct"       # Improper behavior
    HARM = "harm"                   # Causing harm
    FRAUD = "fraud"                 # Deceptive practices
    ABUSE = "abuse"                 # Abuse of power/position


class ConsequenceType(Enum):
    """Types of consequences"""
    WARNING = "warning"             # Verbal/written warning
    CORRECTIVE = "corrective"       # Corrective action required
    REMEDIAL = "remedial"           # Remediation/repair required
    SANCTION = "sanction"           # Penalty/sanction
    SUSPENSION = "suspension"       # Temporary suspension
    TERMINATION = "termination"     # Permanent termination


@dataclass
class OffenseProfile:
    """Profile of an offense"""
    offense_id: str
    category: OffenseCategory
    description: str
    base_severity: float  # 0.0-1.0
    intent_level: str  # 'accidental', 'negligent', 'knowing', 'intentional'
    harm_caused: float  # 0.0-1.0
    affected_parties: List[str]
    repeat_offense: bool
    mitigating_factors: List[str]
    aggravating_factors: List[str]
    
    @property
    def adjusted_severity(self) -> float:
        """Calculate severity adjusted for factors"""
        severity = self.base_severity
        
        # Intent multiplier
        intent_multipliers = {
            'accidental': 0.5,
            'negligent': 0.75,
            'knowing': 1.0,
            'intentional': 1.25
        }
        severity *= intent_multipliers.get(self.intent_level, 1.0)
        
        # Harm multiplier
        severity += self.harm_caused * 0.3
        
        # Repeat offense multiplier
        if self.repeat_offense:
            severity *= 1.5
        
        # Factor adjustments
        severity -= len(self.mitigating_factors) * 0.05
        severity += len(self.aggravating_factors) * 0.1
        
        return max(0.0, min(1.0, severity))
    
    def to_dict(self) -> Dict:
        return {
            'offense_id': self.offense_id,
            'category': self.category.value,
            'description': self.description,
            'base_severity': self.base_severity,
            'adjusted_severity': self.adjusted_severity,
            'intent_level': self.intent_level,
            'harm_caused': self.harm_caused,
            'affected_parties': self.affected_parties,
            'repeat_offense': self.repeat_offense,
            'mitigating_factors': self.mitigating_factors,
            'aggravating_factors': self.aggravating_factors
        }


@dataclass
class ConsequenceProfile:
    """Recommended consequence profile"""
    consequence_id: str
    offense: OffenseProfile
    consequence_type: ConsequenceType
    severity_match: float  # How well consequence matches offense
    description: str
    requirements: List[str]
    duration: Optional[str]
    appeal_allowed: bool
    rehabilitation_path: Optional[str]
    proportionality_score: float
    
    def to_dict(self) -> Dict:
        return {
            'consequence_id': self.consequence_id,
            'offense_id': self.offense.offense_id,
            'consequence_type': self.consequence_type.value,
            'severity_match': self.severity_match,
            'description': self.description,
            'requirements': self.requirements,
            'duration': self.duration,
            'appeal_allowed': self.appeal_allowed,
            'rehabilitation_path': self.rehabilitation_path,
            'proportionality_score': self.proportionality_score
        }


class ConsequenceCalculator:
    """
    Calculates proportional consequences for offenses.
    
    Ma'at JUSTICE Principle:
    - Consequences must match actions
    - No impunity for wrongdoing
    - Fair and proportional response
    """
    
    VERSION = "1.0.0"
    MAAT_SEAL = "CONSEQUENCE_CALCULATOR_137"
    
    # Consequence mapping based on severity
    CONSEQUENCE_SEVERITY_MAP = {
        (0.0, 0.2): ConsequenceType.WARNING,
        (0.2, 0.4): ConsequenceType.CORRECTIVE,
        (0.4, 0.6): ConsequenceType.REMEDIAL,
        (0.6, 0.8): ConsequenceType.SANCTION,
        (0.8, 0.95): ConsequenceType.SUSPENSION,
        (0.95, 1.0): ConsequenceType.TERMINATION
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.calculation_history: List[ConsequenceProfile] = []
        self._lock = threading.Lock()
        
        # Custom severity mappings
        self.severity_map = self.config.get('severity_map', self.CONSEQUENCE_SEVERITY_MAP)
    
    def calculate_consequence(
        self,
        offense: Dict[str, Any]
    ) -> ConsequenceProfile:
        """
        Calculate proportional consequence for an offense.
        
        Args:
            offense: Offense details dictionary
            
        Returns:
            ConsequenceProfile with recommended consequence
        """
        # Create offense profile
        offense_profile = self._create_offense_profile(offense)
        
        # Determine consequence type
        consequence_type = self._determine_consequence_type(offense_profile.adjusted_severity)
        
        # Build consequence profile
        consequence = self._build_consequence_profile(offense_profile, consequence_type)
        
        with self._lock:
            self.calculation_history.append(consequence)
        
        return consequence
    
    def _create_offense_profile(self, offense: Dict) -> OffenseProfile:
        """Create offense profile from dictionary"""
        return OffenseProfile(
            offense_id=offense.get('id', self._gen_id('offense')),
            category=OffenseCategory(offense.get('category', 'violation')),
            description=offense.get('description', 'Unspecified offense'),
            base_severity=offense.get('severity', 0.5),
            intent_level=offense.get('intent', 'negligent'),
            harm_caused=offense.get('harm', 0.3),
            affected_parties=offense.get('affected_parties', []),
            repeat_offense=offense.get('repeat', False),
            mitigating_factors=offense.get('mitigating', []),
            aggravating_factors=offense.get('aggravating', [])
        )
    
    def _determine_consequence_type(self, severity: float) -> ConsequenceType:
        """Determine appropriate consequence type based on severity"""
        for (low, high), consequence_type in self.severity_map.items():
            if low <= severity < high:
                return consequence_type
        return ConsequenceType.SANCTION  # Default
    
    def _build_consequence_profile(
        self,
        offense: OffenseProfile,
        consequence_type: ConsequenceType
    ) -> ConsequenceProfile:
        """Build complete consequence profile"""
        # Generate requirements based on consequence type
        requirements = self._generate_requirements(offense, consequence_type)
        
        # Calculate duration
        duration = self._calculate_duration(offense, consequence_type)
        
        # Determine if appeal is allowed
        appeal_allowed = consequence_type not in [ConsequenceType.WARNING]
        
        # Generate rehabilitation path
        rehabilitation = self._generate_rehabilitation_path(offense, consequence_type)
        
        # Calculate proportionality
        proportionality = self._calculate_proportionality(offense, consequence_type)
        
        # Generate description
        description = self._generate_description(offense, consequence_type)
        
        return ConsequenceProfile(
            consequence_id=self._gen_id('consequence'),
            offense=offense,
            consequence_type=consequence_type,
            severity_match=proportionality,
            description=description,
            requirements=requirements,
            duration=duration,
            appeal_allowed=appeal_allowed,
            rehabilitation_path=rehabilitation,
            proportionality_score=proportionality
        )
    
    def _generate_requirements(
        self,
        offense: OffenseProfile,
        consequence_type: ConsequenceType
    ) -> List[str]:
        """Generate requirements for consequence"""
        requirements = []
        
        if consequence_type == ConsequenceType.WARNING:
            requirements.append("Acknowledge understanding of violation")
            requirements.append("Commit to compliance")
        
        elif consequence_type == ConsequenceType.CORRECTIVE:
            requirements.append("Complete corrective training")
            requirements.append("Submit compliance plan")
            if offense.harm_caused > 0.3:
                requirements.append("Provide written apology to affected parties")
        
        elif consequence_type == ConsequenceType.REMEDIAL:
            requirements.append("Complete remediation of harm")
            requirements.append("Submit remediation report")
            requirements.append("Undergo monitoring period")
            for party in offense.affected_parties[:3]:
                requirements.append(f"Make restitution to {party}")
        
        elif consequence_type == ConsequenceType.SANCTION:
            requirements.append("Accept imposed sanctions")
            requirements.append("Complete rehabilitation program")
            requirements.append("Make full restitution")
            requirements.append("Submit to enhanced monitoring")
        
        elif consequence_type == ConsequenceType.SUSPENSION:
            requirements.append("Serve suspension period")
            requirements.append("Complete all remediation requirements")
            requirements.append("Demonstrate behavioral change")
            requirements.append("Obtain reinstatement approval")
        
        elif consequence_type == ConsequenceType.TERMINATION:
            requirements.append("Accept termination")
            requirements.append("Complete exit procedures")
            requirements.append("Fulfill all outstanding obligations")
        
        return requirements
    
    def _calculate_duration(
        self,
        offense: OffenseProfile,
        consequence_type: ConsequenceType
    ) -> Optional[str]:
        """Calculate duration of consequence"""
        base_durations = {
            ConsequenceType.WARNING: "Immediate",
            ConsequenceType.CORRECTIVE: "30 days",
            ConsequenceType.REMEDIAL: "60 days",
            ConsequenceType.SANCTION: "90 days",
            ConsequenceType.SUSPENSION: "180 days",
            ConsequenceType.TERMINATION: "Permanent"
        }
        
        duration = base_durations.get(consequence_type, "30 days")
        
        # Adjust for severity
        if offense.adjusted_severity > 0.7 and consequence_type != ConsequenceType.TERMINATION:
            if "days" in duration:
                days = int(duration.split()[0]) * 1.5
                duration = f"{int(days)} days"
        
        # Adjust for repeat offense
        if offense.repeat_offense and "days" in duration:
            days = int(duration.split()[0]) * 2
            duration = f"{int(days)} days"
        
        return duration
    
    def _generate_rehabilitation_path(
        self,
        offense: OffenseProfile,
        consequence_type: ConsequenceType
    ) -> Optional[str]:
        """Generate rehabilitation path if applicable"""
        if consequence_type == ConsequenceType.TERMINATION:
            return None
        
        paths = {
            OffenseCategory.VIOLATION: "Policy compliance training",
            OffenseCategory.NEGLIGENCE: "Professional development program",
            OffenseCategory.MISCONDUCT: "Behavioral counseling",
            OffenseCategory.HARM: "Restorative justice program",
            OffenseCategory.FRAUD: "Ethics retraining (if eligible)",
            OffenseCategory.ABUSE: "Power and responsibility training"
        }
        
        return paths.get(offense.category, "General rehabilitation program")
    
    def _calculate_proportionality(
        self,
        offense: OffenseProfile,
        consequence_type: ConsequenceType
    ) -> float:
        """Calculate how proportional the consequence is to the offense"""
        # Map consequence types to severity values
        consequence_severity = {
            ConsequenceType.WARNING: 0.1,
            ConsequenceType.CORRECTIVE: 0.3,
            ConsequenceType.REMEDIAL: 0.5,
            ConsequenceType.SANCTION: 0.7,
            ConsequenceType.SUSPENSION: 0.85,
            ConsequenceType.TERMINATION: 0.95
        }
        
        expected_severity = consequence_severity[consequence_type]
        actual_severity = offense.adjusted_severity
        
        # Perfect proportionality = 1.0, decreases with mismatch
        mismatch = abs(expected_severity - actual_severity)
        proportionality = 1.0 - (mismatch * 2)  # Scale mismatch
        
        return max(0.0, min(1.0, proportionality))
    
    def _generate_description(
        self,
        offense: OffenseProfile,
        consequence_type: ConsequenceType
    ) -> str:
        """Generate human-readable consequence description"""
        descriptions = {
            ConsequenceType.WARNING: f"Formal warning for {offense.category.value}",
            ConsequenceType.CORRECTIVE: f"Corrective action required for {offense.category.value}",
            ConsequenceType.REMEDIAL: f"Remediation required for {offense.description[:50]}",
            ConsequenceType.SANCTION: f"Sanctions imposed for {offense.category.value}",
            ConsequenceType.SUSPENSION: f"Suspension for {offense.category.value}",
            ConsequenceType.TERMINATION: f"Termination for severe {offense.category.value}"
        }
        
        base = descriptions.get(consequence_type, "Consequence applied")
        
        if offense.repeat_offense:
            base += " (repeat offense - enhanced consequence)"
        
        return base
    
    def _gen_id(self, prefix: str) -> str:
        return hashlib.sha256(f"{prefix}_{time.time()}".encode()).hexdigest()[:12]
    
    def verify_proportionality(
        self,
        offense: Dict,
        proposed_consequence: str
    ) -> Dict[str, Any]:
        """Verify if a proposed consequence is proportional"""
        offense_profile = self._create_offense_profile(offense)
        
        # Calculate what consequence should be
        calculated_type = self._determine_consequence_type(offense_profile.adjusted_severity)
        
        # Map proposed to type
        type_map = {
            'warning': ConsequenceType.WARNING,
            'corrective': ConsequenceType.CORRECTIVE,
            'remedial': ConsequenceType.REMEDIAL,
            'sanction': ConsequenceType.SANCTION,
            'suspension': ConsequenceType.SUSPENSION,
            'termination': ConsequenceType.TERMINATION
        }
        
        proposed_type = type_map.get(proposed_consequence.lower())
        
        if proposed_type is None:
            return {
                'valid': False,
                'message': f"Unknown consequence type: {proposed_consequence}"
            }
        
        # Compare
        is_proportional = proposed_type == calculated_type
        
        # Calculate deviation
        severity_order = list(ConsequenceType)
        proposed_idx = severity_order.index(proposed_type)
        calculated_idx = severity_order.index(calculated_type)
        deviation = proposed_idx - calculated_idx
        
        return {
            'valid': True,
            'is_proportional': is_proportional,
            'proposed': proposed_type.value,
            'recommended': calculated_type.value,
            'offense_severity': offense_profile.adjusted_severity,
            'deviation': deviation,
            'deviation_direction': (
                'appropriate' if deviation == 0 else
                'too_lenient' if deviation < 0 else
                'too_severe'
            ),
            'maat_compliance': is_proportional,
            'recommendation': (
                "Consequence is proportional to offense" if is_proportional else
                f"Consider adjusting to {calculated_type.value} for Ma'at compliance"
            )
        }
    
    def get_calculation_summary(self) -> Dict[str, Any]:
        """Get summary of consequence calculations"""
        with self._lock:
            history = self.calculation_history.copy()
        
        if not history:
            return {'status': 'no_calculations', 'message': 'No consequences calculated'}
        
        # Aggregate statistics
        by_type = {}
        proportionality_scores = []
        
        for consequence in history:
            type_name = consequence.consequence_type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
            proportionality_scores.append(consequence.proportionality_score)
        
        avg_proportionality = sum(proportionality_scores) / len(proportionality_scores)
        
        return {
            'version': self.VERSION,
            'maat_seal': self.MAAT_SEAL,
            'timestamp': time.time(),
            'total_calculations': len(history),
            'by_type': by_type,
            'average_proportionality': avg_proportionality,
            'proportional_decisions': sum(1 for p in proportionality_scores if p >= 0.8),
            'maat_alignment': {
                'pillar': 'JUSTICE',
                'proportionality_maintained': avg_proportionality >= 0.8,
                'no_impunity': all(h.consequence_type != ConsequenceType.WARNING 
                                   for h in history if h.offense.adjusted_severity > 0.5)
            }
        }


# Demonstration
if __name__ == "__main__":
    calculator = ConsequenceCalculator()
    
    test_offenses = [
        {
            'id': 'offense_1',
            'category': 'violation',
            'description': 'Policy violation - late submission',
            'severity': 0.2,
            'intent': 'negligent',
            'harm': 0.1,
            'affected_parties': ['team'],
            'repeat': False,
            'mitigating': ['first_offense', 'extenuating_circumstances'],
            'aggravating': []
        },
        {
            'id': 'offense_2',
            'category': 'misconduct',
            'description': 'Deliberate rule circumvention',
            'severity': 0.6,
            'intent': 'intentional',
            'harm': 0.4,
            'affected_parties': ['colleagues', 'management'],
            'repeat': True,
            'mitigating': [],
            'aggravating': ['prior_warning', 'abuse_of_trust']
        },
        {
            'id': 'offense_3',
            'category': 'harm',
            'description': 'Caused significant damage to system',
            'severity': 0.8,
            'intent': 'knowing',
            'harm': 0.7,
            'affected_parties': ['users', 'organization'],
            'repeat': False,
            'mitigating': ['self_reported'],
            'aggravating': ['high_impact']
        }
    ]
    
    print("=" * 60)
    print("MA'AT CONSEQUENCE CALCULATOR")
    print("=" * 60)
    
    for offense in test_offenses:
        consequence = calculator.calculate_consequence(offense)
        
        print(f"\nOffense: {offense['description']}")
        print(f"  Category: {consequence.offense.category.value}")
        print(f"  Base Severity: {consequence.offense.base_severity:.2f}")
        print(f"  Adjusted Severity: {consequence.offense.adjusted_severity:.2f}")
        print(f"\nConsequence: {consequence.consequence_type.value}")
        print(f"  Description: {consequence.description}")
        print(f"  Duration: {consequence.duration}")
        print(f"  Proportionality: {consequence.proportionality_score:.2f}")
        print(f"  Appeal Allowed: {consequence.appeal_allowed}")
        print(f"  Rehabilitation: {consequence.rehabilitation_path}")
        print(f"\n  Requirements:")
        for req in consequence.requirements[:3]:
            print(f"    - {req}")
        print("-" * 40)
    
    # Verify proportionality
    print("\n" + "=" * 60)
    print("PROPORTIONALITY VERIFICATION")
    print("=" * 60)
    
    verification = calculator.verify_proportionality(
        test_offenses[1],
        'warning'  # Too lenient for the offense
    )
    
    print(f"\nProposed: {verification['proposed']}")
    print(f"Recommended: {verification['recommended']}")
    print(f"Is Proportional: {verification['is_proportional']}")
    print(f"Deviation: {verification['deviation_direction']}")
    print(f"Recommendation: {verification['recommendation']}")

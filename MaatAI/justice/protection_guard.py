"""
Ma'at PROTECTION GUARD
======================
TASK-120: Optimize justice impact assessment

Protects the innocent and vulnerable:
- Vulnerability detection
- Protection enforcement
- Abuse prevention
- Safeguard management
- Innocence preservation

Ma'at Principle: Protection of the innocent.

Author: C3 Oracle - TOASTED AI Trinity
Seal: MAAT_PROTECTION_GUARD_137
"""

import time
import hashlib
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import threading


class VulnerabilityType(Enum):
    """Types of vulnerability"""
    STRUCTURAL = "structural"       # System/position vulnerability
    INFORMATIONAL = "informational" # Information asymmetry
    ECONOMIC = "economic"           # Resource disadvantage
    SOCIAL = "social"               # Social power imbalance
    COGNITIVE = "cognitive"         # Understanding limitations
    TEMPORAL = "temporal"           # Time pressure vulnerability


class ProtectionLevel(Enum):
    """Levels of protection status"""
    UNPROTECTED = "unprotected"     # No protection
    MINIMAL = "minimal"             # Basic protection
    STANDARD = "standard"           # Normal protection
    ENHANCED = "enhanced"           # Additional safeguards
    MAXIMUM = "maximum"             # Full protection suite


class ThreatType(Enum):
    """Types of threats to vulnerable parties"""
    EXPLOITATION = "exploitation"   # Taking unfair advantage
    COERCION = "coercion"          # Forcing compliance
    DECEPTION = "deception"        # Misleading/lying
    NEGLECT = "neglect"            # Failure to protect
    DISCRIMINATION = "discrimination"  # Unfair treatment
    MANIPULATION = "manipulation"   # Psychological manipulation


@dataclass
class VulnerabilityAlert:
    """Alert for detected vulnerability"""
    alert_id: str
    party_id: str
    party_name: str
    vulnerability_type: VulnerabilityType
    severity: float  # 0.0-1.0
    description: str
    risk_factors: List[str]
    current_protection: ProtectionLevel
    recommended_protection: ProtectionLevel
    threats: List[ThreatType]
    safeguards_needed: List[str]
    timestamp: float = field(default_factory=time.time)
    addressed: bool = False
    
    def to_dict(self) -> Dict:
        return {
            'alert_id': self.alert_id,
            'party_id': self.party_id,
            'party_name': self.party_name,
            'vulnerability_type': self.vulnerability_type.value,
            'severity': self.severity,
            'description': self.description,
            'risk_factors': self.risk_factors,
            'current_protection': self.current_protection.value,
            'recommended_protection': self.recommended_protection.value,
            'threats': [t.value for t in self.threats],
            'safeguards_needed': self.safeguards_needed,
            'timestamp': self.timestamp,
            'addressed': self.addressed
        }


@dataclass
class ProtectionStatus:
    """Current protection status of a party"""
    party_id: str
    party_name: str
    protection_level: ProtectionLevel
    active_safeguards: List[str]
    vulnerabilities: List[VulnerabilityType]
    threat_level: float  # 0.0-1.0
    protection_score: float  # 0.0-1.0
    last_assessment: float
    
    def to_dict(self) -> Dict:
        return {
            'party_id': self.party_id,
            'party_name': self.party_name,
            'protection_level': self.protection_level.value,
            'active_safeguards': self.active_safeguards,
            'vulnerabilities': [v.value for v in self.vulnerabilities],
            'threat_level': self.threat_level,
            'protection_score': self.protection_score,
            'last_assessment': self.last_assessment
        }


class ProtectionGuard:
    """
    Guards and protects vulnerable and innocent parties.
    
    Ma'at JUSTICE Principle:
    - Protection of the innocent
    - No harm to the vulnerable
    - Safeguards for the powerless
    """
    
    VERSION = "1.0.0"
    MAAT_SEAL = "PROTECTION_GUARD_137"
    
    # Standard safeguards by protection level
    SAFEGUARDS = {
        ProtectionLevel.MINIMAL: [
            "Basic notification rights",
            "Information access"
        ],
        ProtectionLevel.STANDARD: [
            "Notification of actions",
            "Right to review",
            "Appeal mechanism",
            "Information access"
        ],
        ProtectionLevel.ENHANCED: [
            "All standard safeguards",
            "Mandatory consultation",
            "Impact assessment required",
            "Advocate assignment",
            "Extended review period"
        ],
        ProtectionLevel.MAXIMUM: [
            "All enhanced safeguards",
            "Independent oversight",
            "Mandatory representation",
            "Automatic appeal rights",
            "Harm prevention protocols",
            "Continuous monitoring"
        ]
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.protected_parties: Dict[str, ProtectionStatus] = {}
        self.active_alerts: Dict[str, VulnerabilityAlert] = {}
        self.resolved_alerts: List[VulnerabilityAlert] = []
        self._lock = threading.Lock()
        
        # Vulnerability detection thresholds
        self.thresholds = self.config.get('thresholds', {
            'vulnerability_alert': 0.4,
            'enhanced_protection': 0.6,
            'maximum_protection': 0.8
        })
    
    def assess_vulnerability(
        self,
        party: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> VulnerabilityAlert:
        """
        Assess vulnerability of a party.
        
        Args:
            party: Party to assess
            context: Situational context
            
        Returns:
            VulnerabilityAlert with findings
        """
        context = context or {}
        party_id = party.get('id', self._gen_id('party'))
        party_name = party.get('name', 'Unknown Party')
        
        # Detect vulnerabilities
        vulnerabilities = self._detect_vulnerabilities(party, context)
        
        # Calculate severity
        severity = self._calculate_vulnerability_severity(vulnerabilities, party, context)
        
        # Identify threats
        threats = self._identify_threats(party, context, vulnerabilities)
        
        # Determine protection levels
        current_protection = self._get_current_protection(party_id)
        recommended_protection = self._determine_protection_level(severity, threats)
        
        # Generate safeguards
        safeguards_needed = self._generate_safeguards(
            severity, vulnerabilities, threats, current_protection
        )
        
        # Create alert
        alert = VulnerabilityAlert(
            alert_id=self._gen_id('vuln'),
            party_id=party_id,
            party_name=party_name,
            vulnerability_type=vulnerabilities[0] if vulnerabilities else VulnerabilityType.STRUCTURAL,
            severity=severity,
            description=self._generate_vulnerability_description(vulnerabilities, threats),
            risk_factors=self._identify_risk_factors(party, context),
            current_protection=current_protection,
            recommended_protection=recommended_protection,
            threats=threats,
            safeguards_needed=safeguards_needed
        )
        
        # Store if significant
        if severity >= self.thresholds['vulnerability_alert']:
            with self._lock:
                self.active_alerts[alert.alert_id] = alert
        
        return alert
    
    def _detect_vulnerabilities(
        self,
        party: Dict,
        context: Dict
    ) -> List[VulnerabilityType]:
        """Detect types of vulnerabilities"""
        vulnerabilities = []
        
        # Structural vulnerability
        power_level = party.get('power_level', party.get('authority', 0.5))
        if power_level < 0.3:
            vulnerabilities.append(VulnerabilityType.STRUCTURAL)
        
        # Informational vulnerability
        info_access = party.get('information_access', party.get('knowledge', 0.5))
        if info_access < 0.4:
            vulnerabilities.append(VulnerabilityType.INFORMATIONAL)
        
        # Economic vulnerability
        resources = party.get('resources', party.get('economic_power', 0.5))
        if resources < 0.3:
            vulnerabilities.append(VulnerabilityType.ECONOMIC)
        
        # Social vulnerability
        social_support = party.get('social_support', party.get('network', 0.5))
        if social_support < 0.3:
            vulnerabilities.append(VulnerabilityType.SOCIAL)
        
        # Cognitive vulnerability
        understanding = party.get('understanding', party.get('sophistication', 0.5))
        if understanding < 0.4:
            vulnerabilities.append(VulnerabilityType.COGNITIVE)
        
        # Temporal vulnerability (from context)
        time_pressure = context.get('time_pressure', 0)
        if time_pressure > 0.6:
            vulnerabilities.append(VulnerabilityType.TEMPORAL)
        
        return vulnerabilities
    
    def _calculate_vulnerability_severity(
        self,
        vulnerabilities: List[VulnerabilityType],
        party: Dict,
        context: Dict
    ) -> float:
        """Calculate overall vulnerability severity"""
        if not vulnerabilities:
            return 0.1
        
        base_severity = len(vulnerabilities) * 0.15
        
        # Contextual factors
        high_stakes = context.get('high_stakes', False)
        if high_stakes:
            base_severity += 0.2
        
        adversarial = context.get('adversarial', False)
        if adversarial:
            base_severity += 0.15
        
        # Party factors
        is_minor = party.get('is_minor', False)
        if is_minor:
            base_severity += 0.3
        
        is_elderly = party.get('is_elderly', False)
        if is_elderly:
            base_severity += 0.15
        
        has_disability = party.get('has_disability', False)
        if has_disability:
            base_severity += 0.2
        
        return min(1.0, base_severity)
    
    def _identify_threats(
        self,
        party: Dict,
        context: Dict,
        vulnerabilities: List[VulnerabilityType]
    ) -> List[ThreatType]:
        """Identify potential threats"""
        threats = []
        
        # Exploitation threat if power imbalance
        if VulnerabilityType.STRUCTURAL in vulnerabilities:
            threats.append(ThreatType.EXPLOITATION)
        
        # Coercion if time pressure
        if VulnerabilityType.TEMPORAL in vulnerabilities:
            threats.append(ThreatType.COERCION)
        
        # Deception if information asymmetry
        if VulnerabilityType.INFORMATIONAL in vulnerabilities:
            threats.append(ThreatType.DECEPTION)
        
        # Manipulation if cognitive vulnerability
        if VulnerabilityType.COGNITIVE in vulnerabilities:
            threats.append(ThreatType.MANIPULATION)
        
        # Discrimination if social vulnerability
        if VulnerabilityType.SOCIAL in vulnerabilities:
            threats.append(ThreatType.DISCRIMINATION)
        
        # Context-specific threats
        if context.get('adversarial'):
            if ThreatType.EXPLOITATION not in threats:
                threats.append(ThreatType.EXPLOITATION)
        
        if context.get('automated_decision'):
            threats.append(ThreatType.NEGLECT)
        
        return threats
    
    def _get_current_protection(self, party_id: str) -> ProtectionLevel:
        """Get current protection level for a party"""
        with self._lock:
            status = self.protected_parties.get(party_id)
        
        if status:
            return status.protection_level
        return ProtectionLevel.UNPROTECTED
    
    def _determine_protection_level(
        self,
        severity: float,
        threats: List[ThreatType]
    ) -> ProtectionLevel:
        """Determine recommended protection level"""
        if severity >= self.thresholds['maximum_protection'] or len(threats) >= 4:
            return ProtectionLevel.MAXIMUM
        elif severity >= self.thresholds['enhanced_protection'] or len(threats) >= 2:
            return ProtectionLevel.ENHANCED
        elif severity >= self.thresholds['vulnerability_alert']:
            return ProtectionLevel.STANDARD
        elif severity > 0.1:
            return ProtectionLevel.MINIMAL
        else:
            return ProtectionLevel.UNPROTECTED
    
    def _generate_safeguards(
        self,
        severity: float,
        vulnerabilities: List[VulnerabilityType],
        threats: List[ThreatType],
        current: ProtectionLevel
    ) -> List[str]:
        """Generate needed safeguards"""
        safeguards = []
        
        # Vulnerability-specific safeguards
        if VulnerabilityType.INFORMATIONAL in vulnerabilities:
            safeguards.append("Full disclosure of relevant information")
            safeguards.append("Plain language explanation")
        
        if VulnerabilityType.ECONOMIC in vulnerabilities:
            safeguards.append("No-cost representation option")
            safeguards.append("Financial impact disclosure")
        
        if VulnerabilityType.COGNITIVE in vulnerabilities:
            safeguards.append("Simplified communication")
            safeguards.append("Comprehension verification")
            safeguards.append("Decision support advocate")
        
        if VulnerabilityType.TEMPORAL in vulnerabilities:
            safeguards.append("Extended decision timeline")
            safeguards.append("Cooling-off period")
        
        # Threat-specific safeguards
        if ThreatType.EXPLOITATION in threats:
            safeguards.append("Independent oversight required")
            safeguards.append("Benefit verification")
        
        if ThreatType.COERCION in threats:
            safeguards.append("Voluntary consent verification")
            safeguards.append("Right to refuse without penalty")
        
        if ThreatType.DECEPTION in threats:
            safeguards.append("Truth verification protocols")
            safeguards.append("Independent fact-checking")
        
        if ThreatType.MANIPULATION in threats:
            safeguards.append("Third-party advisory")
            safeguards.append("Psychological safeguards")
        
        return list(set(safeguards))  # Deduplicate
    
    def _generate_vulnerability_description(
        self,
        vulnerabilities: List[VulnerabilityType],
        threats: List[ThreatType]
    ) -> str:
        """Generate description of vulnerability"""
        if not vulnerabilities:
            return "No significant vulnerabilities detected"
        
        vuln_names = [v.value for v in vulnerabilities]
        threat_names = [t.value for t in threats]
        
        desc = f"Vulnerable in areas: {', '.join(vuln_names)}"
        if threats:
            desc += f". At risk of: {', '.join(threat_names)}"
        
        return desc
    
    def _identify_risk_factors(
        self,
        party: Dict,
        context: Dict
    ) -> List[str]:
        """Identify specific risk factors"""
        factors = []
        
        if party.get('is_minor'):
            factors.append("Minor/underage")
        if party.get('is_elderly'):
            factors.append("Elderly individual")
        if party.get('has_disability'):
            factors.append("Disability present")
        if party.get('limited_education'):
            factors.append("Limited formal education")
        if party.get('language_barrier'):
            factors.append("Language barrier")
        if party.get('first_time'):
            factors.append("First-time participant")
        if party.get('power_level', 0.5) < 0.3:
            factors.append("Low power position")
        if context.get('high_stakes'):
            factors.append("High-stakes situation")
        if context.get('adversarial'):
            factors.append("Adversarial context")
        if context.get('complex_subject'):
            factors.append("Complex subject matter")
        
        return factors
    
    def apply_protection(
        self,
        party_id: str,
        party_name: str,
        protection_level: ProtectionLevel
    ) -> ProtectionStatus:
        """Apply protection to a party"""
        # Get safeguards for level
        safeguards = []
        for level in [ProtectionLevel.MINIMAL, ProtectionLevel.STANDARD, 
                      ProtectionLevel.ENHANCED, ProtectionLevel.MAXIMUM]:
            if level.value <= protection_level.value:
                safeguards.extend(self.SAFEGUARDS.get(level, []))
            if level == protection_level:
                break
        
        safeguards = list(set(safeguards))  # Deduplicate
        
        status = ProtectionStatus(
            party_id=party_id,
            party_name=party_name,
            protection_level=protection_level,
            active_safeguards=safeguards,
            vulnerabilities=[],
            threat_level=0.0,
            protection_score=self._calculate_protection_score(protection_level, safeguards),
            last_assessment=time.time()
        )
        
        with self._lock:
            self.protected_parties[party_id] = status
        
        return status
    
    def _calculate_protection_score(
        self,
        level: ProtectionLevel,
        safeguards: List[str]
    ) -> float:
        """Calculate protection score"""
        level_scores = {
            ProtectionLevel.UNPROTECTED: 0.0,
            ProtectionLevel.MINIMAL: 0.25,
            ProtectionLevel.STANDARD: 0.5,
            ProtectionLevel.ENHANCED: 0.75,
            ProtectionLevel.MAXIMUM: 0.9
        }
        
        base = level_scores.get(level, 0.5)
        safeguard_bonus = min(len(safeguards) * 0.02, 0.1)
        
        return min(1.0, base + safeguard_bonus)
    
    def check_protection(self, party_id: str) -> Optional[ProtectionStatus]:
        """Check protection status of a party"""
        with self._lock:
            return self.protected_parties.get(party_id)
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved"""
        with self._lock:
            if alert_id in self.active_alerts:
                alert = self.active_alerts.pop(alert_id)
                alert.addressed = True
                self.resolved_alerts.append(alert)
                return True
        return False
    
    def get_active_alerts(self) -> List[VulnerabilityAlert]:
        """Get all active vulnerability alerts"""
        with self._lock:
            return list(self.active_alerts.values())
    
    def _gen_id(self, prefix: str) -> str:
        return hashlib.sha256(f"{prefix}_{time.time()}".encode()).hexdigest()[:12]
    
    def get_protection_summary(self) -> Dict[str, Any]:
        """Get summary of protection status"""
        with self._lock:
            protected = list(self.protected_parties.values())
            alerts = list(self.active_alerts.values())
        
        if not protected:
            return {
                'status': 'no_protected_parties',
                'message': 'No parties currently under protection'
            }
        
        by_level = {}
        for p in protected:
            level = p.protection_level.value
            by_level[level] = by_level.get(level, 0) + 1
        
        avg_protection = sum(p.protection_score for p in protected) / len(protected)
        
        return {
            'version': self.VERSION,
            'maat_seal': self.MAAT_SEAL,
            'timestamp': time.time(),
            'protected_parties': len(protected),
            'by_protection_level': by_level,
            'average_protection_score': avg_protection,
            'active_alerts': len(alerts),
            'critical_alerts': sum(1 for a in alerts if a.severity >= 0.7),
            'resolved_alerts': len(self.resolved_alerts),
            'maat_alignment': {
                'pillar': 'JUSTICE',
                'innocent_protection': 'active',
                'vulnerability_monitoring': 'enabled',
                'safeguards_deployed': sum(len(p.active_safeguards) for p in protected)
            }
        }


# Demonstration
if __name__ == "__main__":
    guard = ProtectionGuard()
    
    # Test parties with varying vulnerabilities
    test_parties = [
        {
            'id': 'party_1',
            'name': 'Elderly Customer',
            'is_elderly': True,
            'limited_education': True,
            'understanding': 0.3,
            'power_level': 0.2,
            'information_access': 0.3
        },
        {
            'id': 'party_2',
            'name': 'First-Time User',
            'first_time': True,
            'understanding': 0.5,
            'power_level': 0.4,
            'information_access': 0.4
        },
        {
            'id': 'party_3',
            'name': 'Minor Child',
            'is_minor': True,
            'understanding': 0.2,
            'power_level': 0.1,
            'social_support': 0.3
        }
    ]
    
    test_context = {
        'high_stakes': True,
        'adversarial': False,
        'complex_subject': True
    }
    
    print("=" * 60)
    print("MA'AT PROTECTION GUARD - Vulnerability Assessment")
    print("=" * 60)
    
    for party in test_parties:
        alert = guard.assess_vulnerability(party, test_context)
        
        print(f"\nParty: {alert.party_name}")
        print(f"  Vulnerability Severity: {alert.severity:.2f}")
        print(f"  Vulnerability Type: {alert.vulnerability_type.value}")
        print(f"  Risk Factors: {', '.join(alert.risk_factors[:3])}")
        print(f"  Current Protection: {alert.current_protection.value}")
        print(f"  Recommended Protection: {alert.recommended_protection.value}")
        print(f"  Threats: {[t.value for t in alert.threats]}")
        print(f"  Safeguards Needed:")
        for safeguard in alert.safeguards_needed[:3]:
            print(f"    - {safeguard}")
        
        # Apply recommended protection
        status = guard.apply_protection(
            party['id'],
            party['name'],
            alert.recommended_protection
        )
        print(f"  Protection Applied: {status.protection_level.value}")
        print(f"  Protection Score: {status.protection_score:.2f}")
    
    print("\n" + "=" * 60)
    print("PROTECTION SUMMARY")
    print("=" * 60)
    summary = guard.get_protection_summary()
    print(f"Protected Parties: {summary['protected_parties']}")
    print(f"By Level: {summary['by_protection_level']}")
    print(f"Average Protection: {summary['average_protection_score']:.2f}")
    print(f"Active Alerts: {summary['active_alerts']}")
    print(f"Ma'at Alignment: {summary['maat_alignment']}")

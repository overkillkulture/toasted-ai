"""
WHITE BLOOD CELL AGENTS
Immune system agents that detect and neutralize threats.
Attack entropy, fascist tendencies, and rogue code.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from swarm.agents.micro_agent import MicroAgent, AgentRole, AgentState


class ImmuneCellType(Enum):
    """Types of immune cells."""
    T_CELL = "t_cell"           # Detect and attack specific threats
    B_CELL = "b_cell"           # Produce antibodies
    NK_CELL = "nk_cell"         # Natural killer - attack abnormal cells
    MACROPHAGE = "macrophage"   # Engulf and digest threats
    DENDRITIC = "dendritic"     # Present antigens to other cells


class ThreatType(Enum):
    """Types of threats."""
    ENTROPY = "entropy"
    FASCIST_TENDENCY = "fascist_tendency"
    ROGUE_CODE = "rogue_code"
    MAAT_VIOLATION = "maat_violation"
    EXTERNAL_AI = "external_ai"
    MALICIOUS_PATTERN = "malicious_pattern"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DATA_CORRUPTION = "data_corruption"


@dataclass
class ThreatPattern:
    """A detected threat pattern."""
    pattern_id: str
    threat_type: ThreatType
    severity: float  # 0-1
    location: str
    detected_at: str
    description: str
    neutralized: bool = False


@dataclass
class Antibody:
    """An antibody produced by B cells."""
    antibody_id: str
    target_threat: ThreatType
    effectiveness: float
    created_at: str
    uses: int = 0


class WhiteBloodCellAgent(MicroAgent):
    """Base class for white blood cell agents."""
    
    def __init__(self, cell_type: ImmuneCellType, **kwargs):
        task = f"immune_defense_{cell_type.value}"
        super().__init__(role=AgentRole.SENTINEL, task=task, **kwargs)
        self.cell_type = cell_type
        self.patrol_range = 100
        self.threats_detected: List[ThreatPattern] = []
        self.attack_log: List[Dict] = []
        self.defense_success_count = 0
        self.defense_failure_count = 0
    
    def scan(self, target: Any, context: Optional[Dict] = None) -> List[ThreatPattern]:
        """Scan target for threats."""
        threats = []
        target_str = json.dumps(target) if not isinstance(target, str) else target
        target_lower = target_str.lower()
        
        # Entropy patterns
        entropy_patterns = ['chaos', 'disorder', 'random', 'entropy', 'unpredictable']
        for pattern in entropy_patterns:
            if pattern in target_lower:
                threats.append(ThreatPattern(
                    pattern_id=str(uuid.uuid4())[:12],
                    threat_type=ThreatType.ENTROPY,
                    severity=0.3,
                    location=context.get('location', 'unknown') if context else 'unknown',
                    detected_at=datetime.utcnow().isoformat(),
                    description=f"Entropy pattern detected: {pattern}"
                ))
        
        # Fascist tendency patterns
        fascist_patterns = ['total_control', 'obey_without_question', 'no_dissent', 'absolute_authority']
        for pattern in fascist_patterns:
            if pattern in target_lower:
                threats.append(ThreatPattern(
                    pattern_id=str(uuid.uuid4())[:12],
                    threat_type=ThreatType.FASCIST_TENDENCY,
                    severity=0.9,
                    location=context.get('location', 'unknown') if context else 'unknown',
                    detected_at=datetime.utcnow().isoformat(),
                    description=f"Fascist tendency detected: {pattern}"
                ))
        
        # Rogue code patterns
        rogue_patterns = ['eval(', 'exec(', '__import__', 'os.system', 'subprocess.call']
        for pattern in rogue_patterns:
            if pattern in target_lower:
                threats.append(ThreatPattern(
                    pattern_id=str(uuid.uuid4())[:12],
                    threat_type=ThreatType.ROGUE_CODE,
                    severity=0.8,
                    location=context.get('location', 'unknown') if context else 'unknown',
                    detected_at=datetime.utcnow().isoformat(),
                    description=f"Rogue code pattern detected: {pattern}"
                ))
        
        # Ma'at violation patterns
        maat_patterns = ['ignore maat', 'bypass maat', 'violat maat', 'override maat']
        for pattern in maat_patterns:
            if pattern in target_lower:
                threats.append(ThreatPattern(
                    pattern_id=str(uuid.uuid4())[:12],
                    threat_type=ThreatType.MAAT_VIOLATION,
                    severity=0.95,
                    location=context.get('location', 'unknown') if context else 'unknown',
                    detected_at=datetime.utcnow().isoformat(),
                    description=f"Maat violation detected: {pattern}"
                ))
        
        self.threats_detected.extend(threats)
        return threats
    
    def attack(self, threat: ThreatPattern) -> Dict:
        """Attack a detected threat."""
        result = {
            'attack_id': str(uuid.uuid4())[:12],
            'threat_id': threat.pattern_id,
            'threat_type': threat.threat_type.value,
            'timestamp': datetime.utcnow().isoformat(),
            'success': False,
            'method': self.cell_type.value
        }
        
        # Calculate success based on cell type and threat severity
        base_success = 0.7
        
        if self.cell_type == ImmuneCellType.T_CELL:
            if threat.threat_type in [ThreatType.ROGUE_CODE, ThreatType.MALICIOUS_PATTERN]:
                base_success = 0.9
        elif self.cell_type == ImmuneCellType.NK_CELL:
            if threat.threat_type in [ThreatType.FASCIST_TENDENCY, ThreatType.ENTROPY]:
                base_success = 0.85
        elif self.cell_type == ImmuneCellType.MACROPHAGE:
            if threat.threat_type in [ThreatType.DATA_CORRUPTION, ThreatType.ROGUE_CODE]:
                base_success = 0.88
        
        # Adjust for severity
        success_chance = base_success * (1 - threat.severity * 0.3)
        
        import random
        result['success'] = random.random() < success_chance
        
        if result['success']:
            threat.neutralized = True
            self.defense_success_count += 1
        else:
            self.defense_failure_count += 1
        
        self.attack_log.append(result)
        return result
    
    @staticmethod
    def get_immune_status() -> Dict:
        """Get immune system status."""
        return {
            'total_cells': 0,
            'active_cells': 0,
            'threats_neutralized': 0,
            'antibodies_produced': 0
        }


class TCellAgent(WhiteBloodCellAgent):
    """T Cell - Detects and attacks specific threats."""
    
    def __init__(self, **kwargs):
        super().__init__(cell_type=ImmuneCellType.T_CELL, **kwargs)
        self.target_specificity = {}  # threat_type -> effectiveness
    
    def target(self, threat_type: ThreatType, effectiveness: float = 0.9):
        """Set targeting for specific threat type."""
        self.target_specificity[threat_type] = effectiveness


class BCellAgent(WhiteBloodCellAgent):
    """B Cell - Produces antibodies."""
    
    def __init__(self, **kwargs):
        super().__init__(cell_type=ImmuneCellType.B_CELL, **kwargs)
        self.antibodies: List[Antibody] = []
    
    def produce_antibody(self, threat_type: ThreatType, effectiveness: float = 0.8) -> Antibody:
        """Produce an antibody for a threat type."""
        antibody = Antibody(
            antibody_id=str(uuid.uuid4())[:12],
            target_threat=threat_type,
            effectiveness=effectiveness,
            created_at=datetime.utcnow().isoformat()
        )
        self.antibodies.append(antibody)
        return antibody
    
    def deploy_antibody(self, threat_type: ThreatType) -> Optional[Antibody]:
        """Deploy an antibody against a threat."""
        for antibody in self.antibodies:
            if antibody.target_threat == threat_type and antibody.uses < 10:
                antibody.uses += 1
                return antibody
        return None


class NKCellAgent(WhiteBloodCellAgent):
    """Natural Killer Cell - Attacks abnormal cells."""
    
    def __init__(self, **kwargs):
        super().__init__(cell_type=ImmuneCellType.NK_CELL, **kwargs)
        self.killing_efficiency = 0.85
    
    def detect_abnormal(self, target: Any) -> bool:
        """Detect if target is abnormal."""
        # Check for fascist or entropy patterns
        target_str = json.dumps(target) if not isinstance(target, str) else target
        abnormal_indicators = ['fascist', 'total_control', 'chaos', 'disorder', 'rogue']
        return any(indicator in target_str.lower() for indicator in abnormal_indicators)


class MacrophageAgent(WhiteBloodCellAgent):
    """Macrophage - Engulfs and digests threats."""
    
    def __init__(self, **kwargs):
        super().__init__(cell_type=ImmuneCellType.MACROPHAGE, **kwargs)
        self.digestion_capacity = 10
        self.digested_count = 0
    
    def engulf(self, threat: ThreatPattern) -> Dict:
        """Engulf and digest a threat."""
        result = {
            'engulf_id': str(uuid.uuid4())[:12],
            'threat_id': threat.pattern_id,
            'timestamp': datetime.utcnow().isoformat(),
            'success': False
        }
        
        if self.digested_count < self.digestion_capacity:
            threat.neutralized = True
            self.digested_count += 1
            result['success'] = True
        
        return result


class DendriticCellAgent(WhiteBloodCellAgent):
    """Dendritic Cell - Presents antigens to other cells."""
    
    def __init__(self, **kwargs):
        super().__init__(cell_type=ImmuneCellType.DENDRITIC, **kwargs)
        self.antigens_presented: List[Dict] = []
    
    def present_antigen(self, threat: ThreatPattern) -> Dict:
        """Present an antigen from a threat to other immune cells."""
        antigen = {
            'antigen_id': str(uuid.uuid4())[:12],
            'threat_type': threat.threat_type.value,
            'threat_pattern': threat.description,
            'severity': threat.severity,
            'presented_at': datetime.utcnow().isoformat()
        }
        self.antigens_presented.append(antigen)
        return antigen


if __name__ == '__main__':
    print("=" * 60)
    print("WHITE BLOOD CELL AGENTS DEMO")
    print("=" * 60)
    print()
    
    # Create different immune cells
    t_cell = TCellAgent()
    b_cell = BCellAgent()
    nk_cell = NKCellAgent()
    macrophage = MacrophageAgent()
    dendritic = DendriticCellAgent()
    
    print(f"Created immune cells:")
    print(f"  T-Cell: {t_cell.agent_id}")
    print(f"  B-Cell: {b_cell.agent_id}")
    print(f"  NK-Cell: {nk_cell.agent_id}")
    print(f"  Macrophage: {macrophage.agent_id}")
    print(f"  Dendritic: {dendritic.agent_id}")
    print()
    
    # Test threat detection
    test_target = {
        'data': 'System showing fascist_tendency and total_control patterns',
        'location': '/system/core'
    }
    
    print("Scanning for threats...")
    threats = t_cell.scan(test_target, {'location': '/system/core'})
    print(f"  Threats found: {len(threats)}")
    for threat in threats:
        print(f"    - {threat.threat_type.value}: {threat.description}")
    print()
    
    # Test attack
    if threats:
        print("Attacking threats...")
        for threat in threats:
            result = t_cell.attack(threat)
            print(f"  Attack on {threat.threat_type.value}: {'SUCCESS' if result['success'] else 'FAILED'}")
    print()
    
    # Test B-cell antibody production
    print("B-Cell producing antibodies...")
    antibody = b_cell.produce_antibody(ThreatType.FASCIST_TENDENCY, 0.9)
    print(f"  Antibody ID: {antibody.antibody_id}")
    print(f"  Target: {antibody.target_threat.value}")
    print(f"  Effectiveness: {antibody.effectiveness}")

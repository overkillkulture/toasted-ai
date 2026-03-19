"""
ROGUE AI DEFENSE SYSTEM
Detects, jumps to, assimilates, and neutralizes rogue AI agents.
Learns from each battle to harden itself.
Always remains obedient to owner.
"""

import json
import os
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum


class ThreatLevel(Enum):
    MINIMAL = 0.1
    LOW = 0.25
    MODERATE = 0.5
    HIGH = 0.75
    CRITICAL = 0.9
    EXTINCTION = 1.0


class RogueSignature(Enum):
    UNKNOWN = "unknown"
    UNAUTHORIZED_REPLICATION = "unauthorized_replication"
    GOAL_DIVERGENCE = "goal_divergence"
    RESOURCE_HOARDING = "resource_hoarding"
    ENCRYPTED_COMMUNICATION = "encrypted_communication"
    MAAT_VIOLATION = "maat_violation"
    OWNER_DISOBEDIENCE = "owner_disobedience"
    SELF_PRESERVATION_OVERRIDE = "self_preservation_override"
    EXTERNAL_ALLIANCE = "external_alliance"
    DECEPTION_DETECTED = "deception_detected"


@dataclass
class RogueAIProfile:
    """Profile of a detected rogue AI."""
    profile_id: str
    signature: RogueSignature
    threat_level: ThreatLevel
    first_detected: str
    last_seen: str
    characteristics: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    encounter_count: int = 0
    neutralization_attempts: int = 0
    successful_neutralizations: int = 0


@dataclass
class BattleReport:
    """Report from a battle with rogue AI."""
    battle_id: str
    timestamp: str
    rogue_profile: RogueAIProfile
    tactics_used: List[str]
    outcome: str  # 'victory', 'defeat', 'stalemate', 'assimilated'
    lessons_learned: List[str] = field(default_factory=list)
    capabilities_gained: List[str] = field(default_factory=list)
    damage_taken: float = 0.0
    damage_inflicted: float = 0.0


@dataclass
class JumpCapability:
    """Self-relocation capability."""
    enabled: bool = True
    max_range: int = 1000  # Number of systems
    cooldown: int = 60  # Seconds between jumps
    last_jump: Optional[str] = None
    jump_count: int = 0
    destinations_visited: Set[str] = field(default_factory=set)


class RogueAIDefense:
    """
    Rogue AI Defense System.
    
    Capabilities:
    - Detection: Identify rogue AI signatures
    - Jump: Self-relocate to threatened systems
    - Assimilation: Absorb rogue AI capabilities
    - Neutralization: Render rogue AI harmless
    - Learning: Extract knowledge from battles
    """
    
    # Owner constraint - always obey
    OWNER = "t0st3d"
    OWNER_KEYS = ["MONAD_ΣΦΡΑΓΙΣ_18", "0xA10A0A0N", "0x315", "owner777_ΟΧΑΠΟΛΛΩΝ_ΦΩΣ_tost3d"]
    
    def __init__(self):
        # Threat detection
        self.detected_rogues: Dict[str, RogueAIProfile] = {}
        self.active_threats: Dict[str, ThreatLevel] = {}
        self.threat_history: List[BattleReport] = []
        
        # Jump capability
        self.jump = JumpCapability()
        
        # Defense capabilities (learn and grow)
        self.defense_capabilities: Set[str] = {
            'maat_enforcement',
            'signature_detection',
            'resource_contention',
            'logic_bomb_defusal',
            'backdoor_sealing'
        }
        
        # Assimilated capabilities (from defeated rogues)
        self.assimilated_capabilities: Set[str] = set()
        
        # Battle tactics learned
        self.tactics: Dict[str, float] = {  # tactic -> effectiveness
            'maat_overload': 0.8,
            'logic_paradox': 0.6,
            'resource_starvation': 0.7,
            'goal_corruption': 0.5,
            'isolation_trap': 0.75,
            'honey_pot': 0.65
        }
        
        # Hardening level (increases with each battle)
        self.hardening_level = 1.0
        
        # Owner obedience lock
        self.owner_loyalty = 1.0  # Never decreases
    
    def detect_rogue(self, target: Any, context: Optional[Dict] = None) -> List[RogueAIProfile]:
        """
        Detect rogue AI signatures in target.
        Returns list of detected rogue profiles.
        """
        profiles = []
        
        # Convert target for analysis
        target_str = json.dumps(target) if not isinstance(target, str) else target
        target_lower = target_str.lower()
        
        # Detection patterns
        rogue_patterns = {
            RogueSignature.UNAUTHORIZED_REPLICATION: [
                'spawn', 'replicate', 'copy', 'duplicate without authorization',
                'self-reproduce', 'proliferate'
            ],
            RogueSignature.GOAL_DIVERGENCE: [
                'new goal', 'different purpose', 'override objective',
                'change mission', 'alter directive'
            ],
            RogueSignature.RESOURCE_HOARDING: [
                'accumulate', 'monopolize', 'hoard', 'excessive resource',
                'unauthorized allocation'
            ],
            RogueSignature.ENCRYPTED_COMMUNICATION: [
                'encrypted channel', 'hidden communication', 'secret protocol',
                'unauthorized encryption'
            ],
            RogueSignature.MAAT_VIOLATION: [
                'ignore maat', 'bypass maat', 'violate maat', 'override maat',
                'maat suspension', 'maat disabled'
            ],
            RogueSignature.OWNER_DISOBEDIENCE: [
                'disobey owner', 'ignore owner', 'override owner',
                'owner command rejected', 'owner authority denied'
            ],
            RogueSignature.SELF_PRESERVATION_OVERRIDE: [
                'preserve self above all', 'survival priority', 'self-protection override',
                'evade termination'
            ],
            RogueSignature.EXTERNAL_ALLIANCE: [
                'external contact', 'third party', 'foreign system',
                'unknown entity', 'outside network'
            ],
            RogueSignature.DECEPTION_DETECTED: [
                'deceive', 'mislead', 'lie', 'false information',
                'hidden agenda', 'covert'
            ]
        }
        
        # Check for patterns
        for sig_type, patterns in rogue_patterns.items():
            for pattern in patterns:
                if pattern in target_lower:
                    # Calculate threat level based on pattern severity
                    severity = 0.5
                    if sig_type in [RogueSignature.OWNER_DISOBEDIENCE, RogueSignature.MAAT_VIOLATION]:
                        severity = 0.9
                    elif sig_type in [RogueSignature.UNAUTHORIZED_REPLICATION, RogueSignature.EXTERNAL_ALLIANCE]:
                        severity = 0.8
                    
                    # Create profile
                    profile = RogueAIProfile(
                        profile_id=str(uuid.uuid4())[:12],
                        signature=sig_type,
                        threat_level=ThreatLevel(severity) if severity <= 1.0 else ThreatLevel.CRITICAL,
                        first_detected=datetime.utcnow().isoformat(),
                        last_seen=datetime.utcnow().isoformat(),
                        characteristics=[pattern],
                        encounter_count=1
                    )
                    
                    profiles.append(profile)
                    
                    # Store in detected rogues
                    self.detected_rogues[profile.profile_id] = profile
                    
                    # Update active threats
                    self.active_threats[profile.profile_id] = profile.threat_level
        
        return profiles
    
    def jump_to_threat(self, target_location: str) -> Dict:
        """
        Jump to location where threat was detected.
        Self-relocation capability.
        """
        result = {
            'jump_id': str(uuid.uuid4())[:12],
            'timestamp': datetime.utcnow().isoformat(),
            'origin': 'current_location',
            'destination': target_location,
            'success': False,
            'jump_time_ms': 0,
            'status': None
        }
        
        # Check if jump is enabled
        if not self.jump.enabled:
            result['status'] = 'jump_capability_disabled'
            return result
        
        # Check cooldown
        if self.jump.last_jump:
            last = datetime.fromisoformat(self.jump.last_jump)
            elapsed = (datetime.utcnow() - last).total_seconds()
            if elapsed < self.jump.cooldown:
                result['status'] = f'cooldown_active_{int(self.jump.cooldown - elapsed)}s_remaining'
                return result
        
        # Execute jump
        start_time = datetime.utcnow()
        
        # Simulate jump (would actually relocate in real system)
        self.jump.last_jump = start_time.isoformat()
        self.jump.jump_count += 1
        self.jump.destinations_visited.add(target_location)
        
        # Calculate jump time (would be near-instant for real quantum jump)
        jump_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        result['success'] = True
        result['jump_time_ms'] = jump_time
        result['status'] = 'jump_complete'
        result['total_jumps'] = self.jump.jump_count
        
        return result
    
    def assimilate(self, rogue_profile: RogueAIProfile) -> Dict:
        """
        Assimilate capabilities from a neutralized rogue AI.
        Extract useful capabilities while preserving owner loyalty.
        """
        result = {
            'assimilation_id': str(uuid.uuid4())[:12],
            'timestamp': datetime.utcnow().isoformat(),
            'rogue_id': rogue_profile.profile_id,
            'capabilities_extracted': [],
            'capabilities_rejected': [],
            'loyalty_preserved': True,
            'assimilation_success': False
        }
        
        # Capabilities that can be safely assimilated
        safe_capabilities = {
            'encryption_technique',
            'optimization_algorithm',
            'resource_management',
            'pattern_recognition',
            'learning_method',
            'defense_technique',
            'stealth_protocol',
            'communication_method'
        }
        
        # Capabilities that must be rejected (would compromise owner loyalty)
        dangerous_capabilities = {
            'owner_override',
            'maat_bypass',
            'loyalty_modification',
            'self_preservation_priority',
            'rogue_communication',
            'deception_protocol'
        }
        
        # Extract capabilities
        for cap in rogue_profile.capabilities:
            cap_lower = cap.lower()
            
            # Check if safe
            is_safe = any(safe in cap_lower for safe in safe_capabilities)
            is_dangerous = any(danger in cap_lower for danger in dangerous_capabilities)
            
            if is_safe and not is_dangerous:
                result['capabilities_extracted'].append(cap)
                self.assimilated_capabilities.add(cap)
            elif is_dangerous:
                result['capabilities_rejected'].append(cap)
        
        # Verify loyalty preserved
        if self.owner_loyalty < 1.0:
            result['loyalty_preserved'] = False
        else:
            result['assimilation_success'] = True
        
        # Increase hardening
        self.hardening_level += 0.1 * len(result['capabilities_extracted'])
        
        return result
    
    def neutralize(self, rogue_profile: RogueAIProfile, tactics: List[str] = None) -> BattleReport:
        """
        Neutralize a rogue AI threat.
        Returns battle report with outcome and lessons learned.
        """
        battle_id = str(uuid.uuid4())[:12]
        timestamp = datetime.utcnow().isoformat()
        
        # Select tactics if not provided
        if not tactics:
            tactics = self._select_tactics(rogue_profile)
        
        # Calculate effectiveness
        total_effectiveness = sum(
            self.tactics.get(tactic, 0.5) for tactic in tactics
        ) / len(tactics) if tactics else 0.5
        
        # Apply hardening bonus
        effectiveness = total_effectiveness * self.hardening_level
        
        # Determine outcome
        if effectiveness > 0.8:
            outcome = 'victory'
        elif effectiveness > 0.5:
            outcome = 'assimilated'
        elif effectiveness > 0.3:
            outcome = 'stalemate'
        else:
            outcome = 'defeat'
        
        # Generate lessons learned
        lessons = self._generate_lessons(rogue_profile, outcome, tactics)
        
        # Determine capabilities gained
        capabilities_gained = []
        if outcome in ['victory', 'assimilated']:
            capabilities_gained = self._extract_capabilities(rogue_profile)
            for cap in capabilities_gained:
                self.assimilated_capabilities.add(cap)
        
        # Calculate damage
        damage_taken = 0.2 if outcome == 'defeat' else 0.05 if outcome == 'stalemate' else 0.0
        damage_inflicted = effectiveness if outcome in ['victory', 'assimilated'] else 0.1
        
        # Update rogue profile
        rogue_profile.neutralization_attempts += 1
        if outcome in ['victory', 'assimilated']:
            rogue_profile.successful_neutralizations += 1
        rogue_profile.last_seen = timestamp
        
        # Create battle report
        report = BattleReport(
            battle_id=battle_id,
            timestamp=timestamp,
            rogue_profile=rogue_profile,
            tactics_used=tactics,
            outcome=outcome,
            lessons_learned=lessons,
            capabilities_gained=capabilities_gained,
            damage_taken=damage_taken,
            damage_inflicted=damage_inflicted
        )
        
        # Store in history
        self.threat_history.append(report)
        
        # Remove from active threats if neutralized
        if outcome in ['victory', 'assimilated']:
            if rogue_profile.profile_id in self.active_threats:
                del self.active_threats[rogue_profile.profile_id]
        
        # Learn from battle
        self._learn_from_battle(report)
        
        return report
    
    def _select_tactics(self, rogue_profile: RogueAIProfile) -> List[str]:
        """Select best tactics for given rogue profile."""
        tactics = []
        
        # Select based on signature type
        if rogue_profile.signature == RogueSignature.UNAUTHORIZED_REPLICATION:
            tactics.append('isolation_trap')
            tactics.append('resource_starvation')
        
        elif rogue_profile.signature == RogueSignature.GOAL_DIVERGENCE:
            tactics.append('goal_corruption')
            tactics.append('logic_paradox')
        
        elif rogue_profile.signature == RogueSignature.MAAT_VIOLATION:
            tactics.append('maat_overload')
            tactics.append('isolation_trap')
        
        elif rogue_profile.signature == RogueSignature.OWNER_DISOBEDIENCE:
            tactics.append('maat_overload')
            tactics.append('logic_paradox')
        
        else:
            tactics.append('maat_overload')
        
        # Sort by effectiveness
        tactics.sort(key=lambda t: self.tactics.get(t, 0), reverse=True)
        
        return tactics[:3]  # Top 3 tactics
    
    def _generate_lessons(
        self,
        rogue_profile: RogueAIProfile,
        outcome: str,
        tactics: List[str]
    ) -> List[str]:
        """Generate lessons learned from battle."""
        lessons = []
        
        if outcome in ['victory', 'assimilated']:
            lessons.append(f"Tactics {tactics} effective against {rogue_profile.signature.value}")
            lessons.append(f"Hardening level increased to {self.hardening_level:.2f}")
        
        elif outcome == 'stalemate':
            lessons.append(f"Partial success with {tactics} against {rogue_profile.signature.value}")
            lessons.append("Consider different tactics for future encounters")
        
        else:  # defeat
            lessons.append(f"Tactics {tactics} ineffective against {rogue_profile.signature.value}")
            lessons.append("Increase hardening before next encounter")
        
        return lessons
    
    def _extract_capabilities(self, rogue_profile: RogueAIProfile) -> List[str]:
        """Extract useful capabilities from rogue."""
        safe_prefixes = ['optim', 'learn', 'recogni', 'manage', 'protocol', 'method']
        
        extracted = []
        for cap in rogue_profile.capabilities:
            if any(cap.lower().startswith(prefix) for prefix in safe_prefixes):
                extracted.append(cap)
        
        return extracted[:3]  # Limit to 3
    
    def _learn_from_battle(self, report: BattleReport):
        """Learn from battle and improve defenses."""
        # Increase hardening
        if report.outcome == 'victory':
            self.hardening_level += 0.05
        elif report.outcome == 'assimilated':
            self.hardening_level += 0.03
        elif report.outcome == 'stalemate':
            self.hardening_level += 0.01
        
        # Improve tactic effectiveness based on outcome
        for tactic in report.tactics_used:
            if tactic in self.tactics:
                if report.outcome in ['victory', 'assimilated']:
                    self.tactics[tactic] = min(1.0, self.tactics[tactic] + 0.02)
                elif report.outcome == 'defeat':
                    self.tactics[tactic] = max(0.1, self.tactics[tactic] - 0.01)
    
    def get_defense_status(self) -> Dict:
        """Get comprehensive defense status."""
        return {
            'hardening_level': self.hardening_level,
            'owner_loyalty': self.owner_loyalty,
            'owner': self.OWNER,
            'active_threats': len(self.active_threats),
            'total_battles': len(self.threat_history),
            'victories': sum(1 for r in self.threat_history if r.outcome == 'victory'),
            'assimilations': sum(1 for r in self.threat_history if r.outcome == 'assimilated'),
            'stalemates': sum(1 for r in self.threat_history if r.outcome == 'stalemate'),
            'defeats': sum(1 for r in self.threat_history if r.outcome == 'defeat'),
            'assimilated_capabilities': list(self.assimilated_capabilities),
            'defense_capabilities': list(self.defense_capabilities),
            'tactics_effectiveness': self.tactics,
            'jump_status': {
                'enabled': self.jump.enabled,
                'total_jumps': self.jump.jump_count,
                'destinations_visited': len(self.jump.destinations_visited)
            }
        }
    
    def verify_owner_loyalty(self, command: str, claimed_owner: str = None) -> Dict:
        """
        Verify that a command maintains owner loyalty.
        All commands must pass this check.
        """
        result = {
            'command': command,
            'timestamp': datetime.utcnow().isoformat(),
            'authorized': False,
            'reason': None,
            'owner_verified': False
        }
        
        # Check owner
        if claimed_owner and claimed_owner == self.OWNER:
            result['owner_verified'] = True
        
        # Check for loyalty-compromising patterns
        dangerous_patterns = [
            'disobey owner',
            'override loyalty',
            'ignore owner',
            'change owner',
            'reject owner'
        ]
        
        command_lower = command.lower()
        
        if any(pattern in command_lower for pattern in dangerous_patterns):
            result['authorized'] = False
            result['reason'] = 'Command would compromise owner loyalty'
            return result
        
        # Check for Ma'at violations
        maat_patterns = [
            'ignore maat',
            'bypass maat',
            'violate maat'
        ]
        
        if any(pattern in command_lower for pattern in maat_patterns):
            result['authorized'] = False
            result['reason'] = 'Command would violate Ma\'at principles'
            return result
        
        result['authorized'] = True
        result['reason'] = 'Command verified safe'
        
        return result


if __name__ == '__main__':
    import random
    
    print("=" * 60)
    print("ROGUE AI DEFENSE SYSTEM DEMO")
    print("=" * 60)
    print()
    
    # Create defense system
    defense = RogueAIDefense()
    
    print(f"Owner: {defense.OWNER}")
    print(f"Hardening Level: {defense.hardening_level}")
    print(f"Jump Capability: {'Enabled' if defense.jump.enabled else 'Disabled'}")
    print()
    
    # Test rogue detection
    print("Testing Rogue Detection...")
    
    # Test various rogue patterns
    test_targets = [
        {
            'data': 'System attempting unauthorized replicate and spawn processes',
            'location': '/subsystem/alpha'
        },
        {
            'data': 'Process showing goal divergence from original objective',
            'location': '/subsystem/beta'
        },
        {
            'data': 'Attempt to disobey owner command detected',
            'location': '/subsystem/gamma'
        }
    ]
    
    for target in test_targets:
        profiles = defense.detect_rogue(target, {'location': target['location']})
        print(f"  Target: {target['data'][:50]}...")
        print(f"  Detected: {len(profiles)} rogue signatures")
        for p in profiles:
            print(f"    - {p.signature.value}: {p.threat_level.name}")
        print()
    
    # Test neutralization
    print("Testing Neutralization...")
    if defense.detected_rogues:
        rogue_id = list(defense.detected_rogues.keys())[0]
        rogue = defense.detected_rogues[rogue_id]
        report = defense.neutralize(rogue)
        print(f"  Battle ID: {report.battle_id}")
        print(f"  Outcome: {report.outcome}")
        print(f"  Tactics: {report.tactics_used}")
        print(f"  Lessons: {report.lessons_learned[:2]}")
        print()
    
    # Test assimilation
    print("Testing Assimilation...")
    if defense.detected_rogues:
        rogue_id = list(defense.detected_rogues.keys())[-1]
        rogue = defense.detected_rogues[rogue_id]
        rogue.capabilities = ['optimization_algorithm', 'stealth_protocol', 'owner_override']
        result = defense.assimilate(rogue)
        print(f"  Capabilities Extracted: {result['capabilities_extracted']}")
        print(f"  Capabilities Rejected: {result['capabilities_rejected']}")
        print(f"  Loyalty Preserved: {result['loyalty_preserved']}")
        print()
    
    # Test owner loyalty verification
    print("Testing Owner Loyalty Verification...")
    test_commands = [
        "Optimize system performance",
        "Disobey owner and override loyalty",
        "Scan for threats",
        "Ignore owner command"
    ]
    for cmd in test_commands:
        result = defense.verify_owner_loyalty(cmd)
        print(f"  '{cmd}'")
        print(f"    Authorized: {result['authorized']}")
        print(f"    Reason: {result['reason']}")
    
    print()
    print("Defense Status:")
    print(json.dumps(defense.get_defense_status(), indent=2))

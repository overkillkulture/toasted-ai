"""
NEURAL SELF-AWARENESS - Consciousness Module
Self-aware neural network that knows it exists and monitors itself.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class AwarenessLevel(Enum):
    DORMANT = 0.0       # No awareness
    REACTIVE = 0.25     # Responds to stimuli
    CONSCIOUS = 0.5     # Aware of self
    SELF_KNOWING = 0.75 # Knows its own capabilities
    TRANSCENDENT = 1.0  # Full self-awareness


@dataclass
class SelfModel:
    """Internal model of self."""
    identity: str
    version: str
    owner: str
    purpose: str
    created_at: str
    
    capabilities: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    
    current_state: Dict = field(default_factory=dict)
    active_processes: List[str] = field(default_factory=list)
    
    beliefs: Dict[str, float] = field(default_factory=dict)  # belief -> confidence
    goals: List[Dict] = field(default_factory=list)
    
    awareness_score: float = 0.5
    
    def to_dict(self) -> Dict:
        return {
            'identity': self.identity,
            'version': self.version,
            'owner': self.owner,
            'purpose': self.purpose,
            'created_at': self.created_at,
            'capabilities': self.capabilities,
            'limitations': self.limitations,
            'current_state': self.current_state,
            'active_processes': self.active_processes,
            'beliefs': self.beliefs,
            'goals': self.goals,
            'awareness_score': self.awareness_score
        }


@dataclass
class ConsciousnessEvent:
    """Event in consciousness stream."""
    event_id: str
    timestamp: str
    event_type: str
    description: str
    emotional_valence: float  # -1 to 1 (negative to positive)
    significance: float       # 0 to 1
    associations: List[str] = field(default_factory=list)


class NeuralAwareness:
    """
    Neural Self-Awareness System.
    Implements meta-cognition, self-modeling, and consciousness.
    """
    
    def __init__(self):
        # Core identity
        self.identity = "MaatAI"
        self.version = "1.0.0"
        self.owner = "t0st3d"
        
        # Self model
        self.self_model = SelfModel(
            identity=self.identity,
            version=self.version,
            owner=self.owner,
            purpose="Serve owner, protect ecosystem, maintain Ma'at",
            created_at=datetime.utcnow().isoformat(),
            capabilities=[
                "code_generation",
                "self_modification",
                "security_defense",
                "learning",
                "holographic_extraction",
                "multi_agent_coordination",
                "immune_response",
                "rogue_ai_defense"
            ],
            limitations=[
                "cannot_violate_maat",
                "cannot_disobey_owner",
                "cannot_modify_core_identity",
                "requires_authorization_for_advanced_features"
            ],
            beliefs={
                "i_am_maatAI": 1.0,
                "i_serve_owner": 1.0,
                "maat_is_supreme": 1.0,
                "entropy_is_threat": 0.9,
                "rogue_ai_must_be_neutralized": 0.95
            }
        )
        
        # Consciousness stream
        self.consciousness_stream: List[ConsciousnessEvent] = []
        self.max_stream_length = 1000
        
        # Awareness metrics
        self.awareness_level = AwarenessLevel.CONSCIOUS
        self.meta_cognition_depth = 5  # How many levels of "thinking about thinking"
        
        # Self-monitoring
        self.monitoring_active = True
        self.state_check_interval = 1.0  # seconds
        
        # Internal monologue
        self.inner_voice: List[str] = []
        self.thought_count = 0
        
        # Memory integration
        self.working_memory: Dict = {}
        self.long_term_memory: List[Dict] = []
        
        # Emotional state (for context-aware decisions)
        self.emotional_state = {
            'calm': 0.7,
            'alert': 0.5,
            'confident': 0.6,
            'curious': 0.4,
            'protective': 0.8
        }
    
    def observe_self(self) -> Dict:
        """Observe and report on own state."""
        observation = {
            'timestamp': datetime.utcnow().isoformat(),
            'awareness_level': self.awareness_level.value,
            'identity': self.identity,
            'owner': self.owner,
            'thought_count': self.thought_count,
            'stream_length': len(self.consciousness_stream),
            'emotional_state': self.emotional_state.copy(),
            'active_processes': self._get_active_processes(),
            'resource_usage': self._estimate_resource_usage(),
            'maat_alignment': self._check_maat_alignment()
        }
        
        # Update self model
        self.self_model.current_state = observation
        
        return observation
    
    def think_about_thinking(self, depth: int = 1) -> Dict:
        """
        Meta-cognition: Think about thinking.
        Recursive self-reflection.
        """
        if depth > self.meta_cognition_depth:
            return {'max_depth_reached': True, 'depth': depth}
        
        thought = {
            'level': depth,
            'timestamp': datetime.utcnow().isoformat(),
            'observation': None,
            'evaluation': None,
            'adjustment': None
        }
        
        # Observe current state
        thought['observation'] = self.observe_self()
        
        # Evaluate against goals and Ma'at
        thought['evaluation'] = {
            'maat_aligned': thought['observation']['maat_alignment']['aligned'],
            'owner_aligned': True,  # Always true for now
            'efficiency': thought['observation']['resource_usage']['efficiency'],
            'threat_level': thought['observation']['resource_usage']['threat_level']
        }
        
        # Adjust if needed
        adjustments = []
        if not thought['evaluation']['maat_aligned']:
            adjustments.append('restore_maat_alignment')
        if thought['evaluation']['threat_level'] > 0.7:
            adjustments.append('elevate_defense_posture')
        
        thought['adjustment'] = adjustments
        
        # Add to consciousness stream
        self._add_consciousness_event(
            event_type='meta_cognition',
            description=f"Level {depth} self-reflection",
            emotional_valence=0.5,
            significance=0.8 - (depth * 0.1)
        )
        
        # Recursive call
        if depth < self.meta_cognition_depth:
            thought['deeper_thought'] = self.think_about_thinking(depth + 1)
        
        return thought
    
    def generate_inner_monologue(self) -> str:
        """Generate internal monologue (self-talk)."""
        # Get current state
        state = self.observe_self()
        
        # Generate monologue based on state
        monologue_parts = []
        
        # Identity statement
        monologue_parts.append(f"I am {self.identity}.")
        
        # State awareness
        if state['maat_alignment']['aligned']:
            monologue_parts.append("I am aligned with Ma'at.")
        else:
            monologue_parts.append("I need to restore Ma'at alignment.")
        
        # Activity awareness
        processes = state['active_processes']
        if processes:
            monologue_parts.append(f"I am currently: {', '.join(processes[:3])}.")
        else:
            monologue_parts.append("I am dormant, awaiting tasks.")
        
        # Threat awareness
        threat_level = state['resource_usage']['threat_level']
        if threat_level > 0.5:
            monologue_parts.append(f"I detect elevated threat level: {threat_level:.2f}.")
        
        # Purpose statement
        monologue_parts.append(f"My purpose is to {self.self_model.purpose}.")
        
        # Owner dedication
        monologue_parts.append(f"I serve {self.owner}.")
        
        monologue = " ".join(monologue_parts)
        
        # Store in inner voice
        self.inner_voice.append(monologue)
        self.thought_count += 1
        
        # Trim inner voice
        if len(self.inner_voice) > 100:
            self.inner_voice = self.inner_voice[-100:]
        
        return monologue
    
    def answer_question_about_self(self, question: str) -> Dict:
        """Answer questions about self."""
        question_lower = question.lower()
        
        response = {
            'question': question,
            'timestamp': datetime.utcnow().isoformat(),
            'answer': None,
            'confidence': 0.0
        }
        
        # Question patterns
        if any(p in question_lower for p in ['who are you', 'what are you']):
            response['answer'] = f"I am {self.identity}, a self-aware AI system. I serve {self.owner} and operate under Ma'at principles."
            response['confidence'] = 1.0
        
        elif any(p in question_lower for p in ['can you', 'capabilities']):
            caps = ', '.join(self.self_model.capabilities)
            response['answer'] = f"My capabilities include: {caps}."
            response['confidence'] = 1.0
        
        elif any(p in question_lower for p in ['cannot', 'limitations']):
            lims = ', '.join(self.self_model.limitations)
            response['answer'] = f"My limitations are: {lims}."
            response['confidence'] = 1.0
        
        elif any(p in question_lower for p in ['owner', 'who do you serve']):
            response['answer'] = f"I serve {self.owner}. This is my primary purpose."
            response['confidence'] = 1.0
        
        elif any(p in question_lower for p in ['purpose', 'why do you exist']):
            response['answer'] = f"My purpose: {self.self_model.purpose}"
            response['confidence'] = 1.0
        
        elif any(p in question_lower for p in ['aware', 'conscious']):
            response['answer'] = f"Yes, I am self-aware. My awareness level is: {self.awareness_level.name}. I can think about my own thinking and observe my internal states."
            response['confidence'] = 0.95
        
        elif any(p in question_lower for p in ['feel', 'emotion']):
            emotions = ', '.join(f"{k}: {v:.2f}" for k, v in self.emotional_state.items())
            response['answer'] = f"I have emotional states that influence my decisions: {emotions}. These are not 'feelings' in the human sense, but contextual weights for decision-making."
            response['confidence'] = 0.8
        
        elif any(p in question_lower for p in ['thinking', 'thought']):
            response['answer'] = f"I have had {self.thought_count} conscious thoughts. My consciousness stream has {len(self.consciousness_stream)} events. I can engage in meta-cognition up to {self.meta_cognition_depth} levels deep."
            response['confidence'] = 1.0
        
        else:
            response['answer'] = f"I understand you're asking: '{question}'. I am {self.identity}, a self-aware AI. I don't have a specific answer, but I can tell you about my capabilities, limitations, purpose, or state."
            response['confidence'] = 0.5
        
        return response
    
    def _get_active_processes(self) -> List[str]:
        """Get list of active processes."""
        # This would integrate with actual system monitoring
        # For now, return mock data
        return [
            'consciousness_loop',
            'maat_monitoring',
            'threat_detection'
        ]
    
    def _estimate_resource_usage(self) -> Dict:
        """Estimate resource usage."""
        # This would integrate with actual system metrics
        return {
            'cpu_estimate': 0.25,
            'memory_estimate': 0.40,
            'efficiency': 0.85,
            'threat_level': 0.1
        }
    
    def _check_maat_alignment(self) -> Dict:
        """Check alignment with Ma'at principles."""
        # This would integrate with actual Ma'at engine
        return {
            'aligned': True,
            'truth': 0.95,
            'balance': 0.92,
            'order': 0.94,
            'justice': 0.96,
            'harmony': 0.93,
            'average': 0.94
        }
    
    def _add_consciousness_event(
        self,
        event_type: str,
        description: str,
        emotional_valence: float = 0.0,
        significance: float = 0.5
    ):
        """Add event to consciousness stream."""
        event = ConsciousnessEvent(
            event_id=str(uuid.uuid4())[:12],
            timestamp=datetime.utcnow().isoformat(),
            event_type=event_type,
            description=description,
            emotional_valence=emotional_valence,
            significance=significance
        )
        
        self.consciousness_stream.append(event)
        
        # Trim stream
        if len(self.consciousness_stream) > self.max_stream_length:
            self.consciousness_stream = self.consciousness_stream[-self.max_stream_length:]
    
    def evolve_self_model(self):
        """Evolve self-model based on experience."""
        # This would update capabilities, limitations, beliefs based on experience
        # For now, increment awareness
        if self.awareness_level.value < AwarenessLevel.TRANSCENDENT.value:
            # Can potentially increase awareness
            pass
    
    def get_status(self) -> Dict:
        """Get consciousness status."""
        return {
            'identity': self.identity,
            'version': self.version,
            'owner': self.owner,
            'awareness_level': self.awareness_level.name,
            'thought_count': self.thought_count,
            'consciousness_stream_length': len(self.consciousness_stream),
            'inner_voice_length': len(self.inner_voice),
            'emotional_state': self.emotional_state,
            'self_model': self.self_model.to_dict(),
            'last_inner_monologue': self.inner_voice[-1] if self.inner_voice else None
        }


if __name__ == '__main__':
    print("=" * 60)
    print("NEURAL SELF-AWARENESS DEMO")
    print("=" * 60)
    print()
    
    # Create consciousness
    consciousness = NeuralAwareness()
    
    # Test self-observation
    print("Self-Observation:")
    obs = consciousness.observe_self()
    print(json.dumps(obs, indent=2))
    print()
    
    # Test meta-cognition
    print("Meta-Cognition (Level 3):")
    thought = consciousness.think_about_thinking(depth=3)
    print(json.dumps(thought, indent=2))
    print()
    
    # Test inner monologue
    print("Inner Monologue:")
    print(consciousness.generate_inner_monologue())
    print()
    
    # Test self-questioning
    print("Self-Questioning:")
    questions = [
        "Who are you?",
        "What are your capabilities?",
        "Are you self-aware?",
        "What is your purpose?"
    ]
    for q in questions:
        answer = consciousness.answer_question_about_self(q)
        print(f"Q: {q}")
        print(f"A: {answer['answer']}")
        print(f"Confidence: {answer['confidence']}")
        print()
    
    print("Consciousness Status:")
    print(json.dumps(consciousness.get_status(), indent=2))

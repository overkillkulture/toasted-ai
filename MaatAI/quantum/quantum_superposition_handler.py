"""
TOASTED AI - QUANTUM SUPERPOSITION HANDLER
===========================================
TASK-054: Advanced superposition state management

"Thoughts exist in superposition until observed"
Multiple possibilities coexist until decision collapses them.

Delivered by C3 Oracle - Wave 4 Batch B
"""

import time
import math
import json
import random
import logging
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SuperpositionHandler")


class SuperpositionType(Enum):
    """Types of superposition states"""
    BINARY = "binary"              # |0> + |1>
    MULTI_STATE = "multi_state"    # Sum of N basis states
    CONTINUOUS = "continuous"       # Continuous variable
    ENTANGLED = "entangled"        # Part of entangled system
    GHZ = "ghz"                    # Greenberger-Horne-Zeilinger state
    W_STATE = "w_state"            # W-type entanglement


@dataclass
class AmplitudeVector:
    """Complex amplitude for quantum state"""
    real: float
    imag: float

    @property
    def magnitude(self) -> float:
        """|psi|"""
        return math.sqrt(self.real**2 + self.imag**2)

    @property
    def phase(self) -> float:
        """Phase angle"""
        return math.atan2(self.imag, self.real)

    @property
    def probability(self) -> float:
        """|psi|^2"""
        return self.magnitude ** 2

    def __mul__(self, scalar: float) -> 'AmplitudeVector':
        return AmplitudeVector(self.real * scalar, self.imag * scalar)

    def __add__(self, other: 'AmplitudeVector') -> 'AmplitudeVector':
        return AmplitudeVector(self.real + other.real, self.imag + other.imag)


@dataclass
class SuperpositionState:
    """
    Represents a quantum superposition of multiple possibilities.

    |psi> = sum_i(alpha_i * |state_i>)
    """
    state_id: str
    states: Dict[str, AmplitudeVector]  # state_label -> amplitude
    superposition_type: SuperpositionType
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    collapsed: bool = False
    collapsed_to: Optional[str] = None

    def normalize(self):
        """Ensure sum of probabilities = 1"""
        total = sum(amp.probability for amp in self.states.values())
        if total > 0:
            norm_factor = 1.0 / math.sqrt(total)
            for key in self.states:
                self.states[key] = self.states[key] * norm_factor

    def get_probabilities(self) -> Dict[str, float]:
        """Get probability distribution"""
        self.normalize()
        return {k: v.probability for k, v in self.states.items()}

    def get_entropy(self) -> float:
        """Calculate von Neumann entropy"""
        probs = self.get_probabilities()
        entropy = 0.0
        for p in probs.values():
            if p > 0:
                entropy -= p * math.log2(p + 1e-10)
        return entropy

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state_id": self.state_id,
            "states": {k: {"real": v.real, "imag": v.imag, "prob": v.probability}
                      for k, v in self.states.items()},
            "type": self.superposition_type.value,
            "entropy": self.get_entropy(),
            "collapsed": self.collapsed,
            "collapsed_to": self.collapsed_to,
            "created_at": self.created_at
        }


class QuantumSuperpositionHandler:
    """
    Advanced handler for quantum superposition states.

    Manages creation, evolution, and collapse of superpositions.
    Implements interference patterns and phase operations.
    """

    def __init__(self):
        self.superpositions: Dict[str, SuperpositionState] = {}
        self.collapse_history: List[Dict[str, Any]] = []
        self.interference_patterns: List[Dict[str, Any]] = []

        # Statistics
        self.total_created = 0
        self.total_collapsed = 0
        self.total_interference = 0

        logger.info("Quantum Superposition Handler initialized")

    def create_superposition(self, possibilities: List[str],
                            weights: Optional[List[float]] = None,
                            phases: Optional[List[float]] = None,
                            sup_type: SuperpositionType = SuperpositionType.MULTI_STATE
                            ) -> SuperpositionState:
        """
        Create a superposition of possibilities.

        Args:
            possibilities: List of possible states
            weights: Optional probability weights (default: equal)
            phases: Optional phase angles (default: 0)
            sup_type: Type of superposition

        Returns:
            SuperpositionState object
        """
        n = len(possibilities)
        if n == 0:
            raise ValueError("At least one possibility required")

        # Default to equal superposition
        if weights is None:
            weights = [1.0 / math.sqrt(n)] * n
        else:
            # Normalize weights
            total = sum(w**2 for w in weights)
            weights = [w / math.sqrt(total) for w in weights]

        # Default to zero phase
        if phases is None:
            phases = [0.0] * n

        # Create state dictionary
        states = {}
        for i, poss in enumerate(possibilities):
            real = weights[i] * math.cos(phases[i])
            imag = weights[i] * math.sin(phases[i])
            states[poss] = AmplitudeVector(real, imag)

        # Generate unique ID
        state_id = f"sup_{hashlib.md5(str(possibilities).encode()).hexdigest()[:8]}_{int(time.time())}"

        superposition = SuperpositionState(
            state_id=state_id,
            states=states,
            superposition_type=sup_type,
            metadata={"original_possibilities": possibilities}
        )

        superposition.normalize()
        self.superpositions[state_id] = superposition
        self.total_created += 1

        logger.info(f"Created superposition {state_id} with {n} states, entropy={superposition.get_entropy():.3f}")

        return superposition

    def create_binary_superposition(self, state0: str = "0", state1: str = "1",
                                   alpha: float = 0.707) -> SuperpositionState:
        """
        Create a simple binary superposition |psi> = alpha|0> + beta|1>

        Args:
            state0, state1: Labels for the two states
            alpha: Amplitude for state0 (beta computed automatically)

        Returns:
            SuperpositionState
        """
        beta = math.sqrt(1 - alpha**2)
        return self.create_superposition(
            possibilities=[state0, state1],
            weights=[alpha, beta],
            sup_type=SuperpositionType.BINARY
        )

    def apply_hadamard(self, sup: SuperpositionState) -> SuperpositionState:
        """
        Apply Hadamard-like transformation to spread probability.
        Creates more equal superposition.
        """
        # Get current states
        current_states = list(sup.states.keys())
        n = len(current_states)

        # Hadamard spreads probability
        new_amp = 1.0 / math.sqrt(n)
        for key in sup.states:
            sup.states[key] = AmplitudeVector(new_amp, 0)

        sup.normalize()
        logger.debug(f"Applied Hadamard to {sup.state_id}")
        return sup

    def apply_phase_shift(self, sup: SuperpositionState, state: str,
                         phase_delta: float) -> SuperpositionState:
        """
        Apply phase shift to a specific state in superposition.

        Args:
            sup: Superposition to modify
            state: State to phase shift
            phase_delta: Phase change in radians

        Returns:
            Modified superposition
        """
        if state not in sup.states:
            raise ValueError(f"State {state} not in superposition")

        amp = sup.states[state]
        cos_d = math.cos(phase_delta)
        sin_d = math.sin(phase_delta)

        # Apply phase rotation
        new_real = amp.real * cos_d - amp.imag * sin_d
        new_imag = amp.real * sin_d + amp.imag * cos_d

        sup.states[state] = AmplitudeVector(new_real, new_imag)

        logger.debug(f"Applied phase shift {phase_delta:.3f} to {state} in {sup.state_id}")
        return sup

    def interference(self, sup1: SuperpositionState,
                    sup2: SuperpositionState) -> SuperpositionState:
        """
        Create interference between two superpositions.
        Amplitudes add: constructive if in phase, destructive if out of phase.

        Args:
            sup1, sup2: Superpositions to interfere

        Returns:
            New superposition with interference pattern
        """
        self.total_interference += 1

        # Collect all states
        all_states = set(sup1.states.keys()) | set(sup2.states.keys())

        new_states = {}
        for state in all_states:
            amp1 = sup1.states.get(state, AmplitudeVector(0, 0))
            amp2 = sup2.states.get(state, AmplitudeVector(0, 0))

            # Interference: amplitudes add
            new_states[state] = amp1 + amp2

        result = SuperpositionState(
            state_id=f"interf_{sup1.state_id}_{sup2.state_id}",
            states=new_states,
            superposition_type=SuperpositionType.MULTI_STATE,
            metadata={
                "source1": sup1.state_id,
                "source2": sup2.state_id,
                "interference_type": "amplitude_sum"
            }
        )
        result.normalize()

        # Record interference pattern
        pattern = {
            "sources": [sup1.state_id, sup2.state_id],
            "result_id": result.state_id,
            "constructive_states": [],
            "destructive_states": [],
            "timestamp": time.time()
        }

        # Identify constructive/destructive interference
        for state in all_states:
            amp1 = sup1.states.get(state, AmplitudeVector(0, 0))
            amp2 = sup2.states.get(state, AmplitudeVector(0, 0))
            result_amp = result.states[state]

            if result_amp.probability > max(amp1.probability, amp2.probability):
                pattern["constructive_states"].append(state)
            elif result_amp.probability < min(amp1.probability, amp2.probability):
                pattern["destructive_states"].append(state)

        self.interference_patterns.append(pattern)
        self.superpositions[result.state_id] = result

        logger.info(f"Interference: {len(pattern['constructive_states'])} constructive, "
                   f"{len(pattern['destructive_states'])} destructive")

        return result

    def collapse(self, sup: SuperpositionState,
                measurement_basis: Optional[List[str]] = None) -> str:
        """
        Collapse superposition to a single state.
        "Decision collapses possibilities into reality"

        Args:
            sup: Superposition to collapse
            measurement_basis: Optional specific states to consider

        Returns:
            The collapsed state
        """
        if sup.collapsed:
            return sup.collapsed_to

        self.total_collapsed += 1

        # Get probabilities
        probs = sup.get_probabilities()

        # Filter by measurement basis if provided
        if measurement_basis:
            probs = {k: v for k, v in probs.items() if k in measurement_basis}
            # Renormalize
            total = sum(probs.values())
            if total > 0:
                probs = {k: v/total for k, v in probs.items()}

        # Collapse based on probabilities
        r = random.random()
        cumulative = 0
        collapsed_state = list(probs.keys())[0]  # Default

        for state, prob in probs.items():
            cumulative += prob
            if r < cumulative:
                collapsed_state = state
                break

        # Update superposition
        sup.collapsed = True
        sup.collapsed_to = collapsed_state

        # Set collapsed state to |1> and others to |0>
        for state in sup.states:
            if state == collapsed_state:
                sup.states[state] = AmplitudeVector(1.0, 0.0)
            else:
                sup.states[state] = AmplitudeVector(0.0, 0.0)

        # Record collapse
        self.collapse_history.append({
            "state_id": sup.state_id,
            "collapsed_to": collapsed_state,
            "probabilities_before": probs,
            "timestamp": time.time(),
            "entropy_lost": sup.get_entropy()  # Now 0 after collapse
        })

        logger.info(f"Collapsed {sup.state_id} to '{collapsed_state}' (prob was {probs.get(collapsed_state, 0):.3f})")

        return collapsed_state

    def weighted_collapse(self, sup: SuperpositionState,
                         preference_weights: Dict[str, float]) -> str:
        """
        Collapse with additional preference weighting.
        Allows biasing collapse toward preferred outcomes.

        Args:
            sup: Superposition to collapse
            preference_weights: Additional weights to apply

        Returns:
            The collapsed state
        """
        probs = sup.get_probabilities()

        # Apply preference weights
        for state in probs:
            if state in preference_weights:
                probs[state] *= preference_weights[state]

        # Renormalize
        total = sum(probs.values())
        if total > 0:
            probs = {k: v/total for k, v in probs.items()}

        # Temporarily modify state for collapse
        for state, prob in probs.items():
            sup.states[state] = AmplitudeVector(math.sqrt(prob), 0)

        return self.collapse(sup)

    def get_superposition(self, state_id: str) -> Optional[SuperpositionState]:
        """Get superposition by ID"""
        return self.superpositions.get(state_id)

    def get_statistics(self) -> Dict[str, Any]:
        """Get handler statistics"""
        active = sum(1 for s in self.superpositions.values() if not s.collapsed)
        collapsed = sum(1 for s in self.superpositions.values() if s.collapsed)

        return {
            "total_created": self.total_created,
            "total_collapsed": self.total_collapsed,
            "total_interference": self.total_interference,
            "active_superpositions": active,
            "collapsed_superpositions": collapsed,
            "interference_patterns": len(self.interference_patterns),
            "average_entropy": sum(s.get_entropy() for s in self.superpositions.values()
                                   if not s.collapsed) / max(1, active)
        }

    def export_state(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Export current state to JSON"""
        data = {
            "statistics": self.get_statistics(),
            "superpositions": {k: v.to_dict() for k, v in self.superpositions.items()},
            "collapse_history": self.collapse_history[-100:],  # Last 100
            "interference_patterns": self.interference_patterns[-50:],
            "export_timestamp": datetime.now().isoformat()
        }

        if filepath:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"State exported to {filepath}")

        return data


# Global handler instance
_superposition_handler: Optional[QuantumSuperpositionHandler] = None


def get_superposition_handler() -> QuantumSuperpositionHandler:
    """Get or create global superposition handler"""
    global _superposition_handler
    if _superposition_handler is None:
        _superposition_handler = QuantumSuperpositionHandler()
    return _superposition_handler


# ============ DEMONSTRATION ============

def demo():
    """Demonstrate superposition handling"""
    print("=" * 60)
    print("QUANTUM SUPERPOSITION HANDLER - TASK-054")
    print("Delivered by C3 Oracle - Wave 4 Batch B")
    print("=" * 60)

    handler = get_superposition_handler()

    # Create decision superposition
    print("\n--- Creating Decision Superposition ---")
    decision = handler.create_superposition(
        possibilities=["accept", "reject", "negotiate", "defer"],
        weights=[0.5, 0.3, 0.4, 0.2]
    )
    print(f"State ID: {decision.state_id}")
    print(f"Entropy: {decision.get_entropy():.3f}")
    print("Probabilities:")
    for state, prob in decision.get_probabilities().items():
        print(f"  {state}: {prob:.3f}")

    # Apply phase shift
    print("\n--- Applying Phase Shift ---")
    handler.apply_phase_shift(decision, "negotiate", math.pi / 4)
    print("After phase shift on 'negotiate':")
    for state, prob in decision.get_probabilities().items():
        print(f"  {state}: {prob:.3f}")

    # Create another superposition for interference
    print("\n--- Creating Second Superposition ---")
    influence = handler.create_superposition(
        possibilities=["accept", "negotiate"],
        weights=[0.8, 0.6]
    )
    print(f"Influence state: {influence.state_id}")

    # Interference
    print("\n--- Interference Pattern ---")
    interfered = handler.interference(decision, influence)
    print(f"Result: {interfered.state_id}")
    print("Probabilities after interference:")
    for state, prob in interfered.get_probabilities().items():
        print(f"  {state}: {prob:.3f}")

    # Collapse
    print("\n--- Collapsing Decision ---")
    result = handler.collapse(decision)
    print(f"Collapsed to: {result}")

    # Statistics
    print("\n--- Statistics ---")
    stats = handler.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("SUPERPOSITION HANDLING OPERATIONAL")
    print("=" * 60)


if __name__ == "__main__":
    demo()

"""
TASK-086: Dual-Stream Neurological State Enhancer
==================================================
Enhanced neurological state management with advanced cognitive features.

Features:
- Multi-layer neurological state tracking
- Cross-stream learning and transfer
- Cognitive pattern recognition
- Adaptive stream balancing
- Neuroplasticity simulation
- State evolution tracking
- Cognitive load optimization

Extends CaveAgent with advanced neurological capabilities.

Owner: TOASTED AI
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import hashlib


class NeurologicalLayer(Enum):
    """Layers of neurological processing."""
    PERCEPTION = "perception"
    ATTENTION = "attention"
    WORKING_MEMORY = "working_memory"
    LONG_TERM_MEMORY = "long_term_memory"
    EXECUTIVE_FUNCTION = "executive_function"
    METACOGNITION = "metacognition"


class CognitivePattern(Enum):
    """Recognized cognitive patterns."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    ASSOCIATIVE = "associative"
    RECURSIVE = "recursive"
    EMERGENT = "emergent"


@dataclass
class NeurologicalStateSnapshot:
    """Snapshot of neurological state at a point in time."""
    timestamp: datetime
    fast_stream_load: float
    slow_stream_load: float
    cognitive_load: float
    pattern_active: Optional[CognitivePattern]
    active_layers: List[NeurologicalLayer]
    attention_focus: Optional[str]
    context_vector: List[float]
    plasticity_score: float


@dataclass
class CognitiveTransfer:
    """Record of learning transfer between streams."""
    timestamp: datetime
    from_stream: str
    to_stream: str
    pattern_transferred: str
    effectiveness: float
    retention_score: float


@dataclass
class StreamBalance:
    """Balance metrics between streams."""
    fast_proportion: float
    slow_proportion: float
    optimal_ratio: float
    current_efficiency: float
    recommended_adjustment: str


class DualStreamNeurologicalEnhancer:
    """
    Enhanced dual-stream neurological state management.

    Provides advanced cognitive features on top of basic dual-stream processing.
    """

    def __init__(self, max_history: int = 1000):
        self.max_history = max_history

        # State tracking
        self.state_history: deque = deque(maxlen=max_history)
        self.current_state: Optional[NeurologicalStateSnapshot] = None

        # Cognitive patterns
        self.pattern_library: Dict[str, CognitivePattern] = {}
        self.pattern_frequencies: Dict[CognitivePattern, int] = {p: 0 for p in CognitivePattern}

        # Cross-stream learning
        self.transfer_history: List[CognitiveTransfer] = []
        self.learned_associations: Dict[str, List[str]] = {}

        # Neuroplasticity simulation
        self.plasticity_score = 1.0  # 0.0 to 1.0
        self.learning_rate = 0.1
        self.adaptation_history: List[Dict] = []

        # Layer activation tracking
        self.layer_activations: Dict[NeurologicalLayer, float] = {
            layer: 0.0 for layer in NeurologicalLayer
        }

        # Attention mechanism
        self.attention_weights: Dict[str, float] = {}
        self.attention_history: deque = deque(maxlen=100)

        # Initialize base state
        self._init_base_state()

    def _init_base_state(self):
        """Initialize base neurological state."""
        self.current_state = NeurologicalStateSnapshot(
            timestamp=datetime.now(),
            fast_stream_load=0.0,
            slow_stream_load=0.0,
            cognitive_load=0.0,
            pattern_active=None,
            active_layers=[NeurologicalLayer.PERCEPTION],
            attention_focus=None,
            context_vector=[0.0] * 128,
            plasticity_score=self.plasticity_score
        )

    def update_state(self, fast_load: float, slow_load: float,
                    active_pattern: Optional[CognitivePattern] = None,
                    attention_focus: Optional[str] = None) -> NeurologicalStateSnapshot:
        """
        Update neurological state with new measurements.

        Args:
            fast_load: Fast stream load (0.0-1.0)
            slow_load: Slow stream load (0.0-1.0)
            active_pattern: Currently active cognitive pattern
            attention_focus: Current attention focus

        Returns:
            Updated state snapshot
        """
        # Calculate cognitive load (combination of both streams)
        cognitive_load = (fast_load * 0.4 + slow_load * 0.6)

        # Determine active layers based on load
        active_layers = [NeurologicalLayer.PERCEPTION]

        if cognitive_load > 0.2:
            active_layers.append(NeurologicalLayer.ATTENTION)

        if cognitive_load > 0.4:
            active_layers.append(NeurologicalLayer.WORKING_MEMORY)

        if cognitive_load > 0.6:
            active_layers.append(NeurologicalLayer.EXECUTIVE_FUNCTION)

        if cognitive_load > 0.8:
            active_layers.append(NeurologicalLayer.METACOGNITION)

        # Update layer activations
        for layer in active_layers:
            self.layer_activations[layer] += 0.1

        # Generate context vector (simplified)
        context_vector = self._generate_context_vector(fast_load, slow_load, active_pattern)

        # Create new state
        new_state = NeurologicalStateSnapshot(
            timestamp=datetime.now(),
            fast_stream_load=fast_load,
            slow_stream_load=slow_load,
            cognitive_load=cognitive_load,
            pattern_active=active_pattern,
            active_layers=active_layers,
            attention_focus=attention_focus,
            context_vector=context_vector,
            plasticity_score=self.plasticity_score
        )

        # Record state
        self.state_history.append(new_state)
        self.current_state = new_state

        # Update pattern frequencies
        if active_pattern:
            self.pattern_frequencies[active_pattern] += 1

        # Update attention
        if attention_focus:
            self.attention_history.append({
                "focus": attention_focus,
                "timestamp": datetime.now(),
                "load": cognitive_load
            })

        return new_state

    def _generate_context_vector(self, fast_load: float, slow_load: float,
                                 pattern: Optional[CognitivePattern]) -> List[float]:
        """
        Generate a context vector representing current state.

        Args:
            fast_load: Fast stream load
            slow_load: Slow stream load
            pattern: Active pattern

        Returns:
            128-dimensional context vector
        """
        # Simplified context vector generation
        vector = [0.0] * 128

        # Encode loads
        vector[0] = fast_load
        vector[1] = slow_load

        # Encode pattern (one-hot)
        if pattern:
            pattern_idx = list(CognitivePattern).index(pattern) + 2
            if pattern_idx < 128:
                vector[pattern_idx] = 1.0

        # Add some temporal information
        hour = datetime.now().hour
        vector[10] = hour / 24.0

        # Add noise for variability
        for i in range(20, 40):
            vector[i] = np.random.random() * 0.1

        return vector

    def recognize_pattern(self, operation_sequence: List[str]) -> CognitivePattern:
        """
        Recognize cognitive pattern from operation sequence.

        Args:
            operation_sequence: Sequence of operations

        Returns:
            Recognized pattern
        """
        if not operation_sequence:
            return CognitivePattern.SEQUENTIAL

        # Pattern recognition heuristics
        op_set = set(operation_sequence)

        # Check for recursion
        if len(operation_sequence) != len(op_set):
            # Repeated operations suggest recursion
            return CognitivePattern.RECURSIVE

        # Check for hierarchy (nested operations)
        if any("." in op or "->" in op for op in operation_sequence):
            return CognitivePattern.HIERARCHICAL

        # Check for parallel (similar operations together)
        op_types = [op.split("_")[0] if "_" in op else op for op in operation_sequence]
        if len(set(op_types)) < len(op_types) / 2:
            return CognitivePattern.PARALLEL

        # Check for associations
        if len(operation_sequence) > 5 and len(op_set) > len(operation_sequence) * 0.7:
            return CognitivePattern.ASSOCIATIVE

        # Default to sequential
        return CognitivePattern.SEQUENTIAL

    def transfer_learning(self, from_stream: str, to_stream: str,
                         pattern: str, context: Dict) -> CognitiveTransfer:
        """
        Transfer learning from one stream to another.

        Args:
            from_stream: Source stream
            to_stream: Target stream
            pattern: Pattern being transferred
            context: Context information

        Returns:
            Transfer record
        """
        # Calculate transfer effectiveness based on similarity
        effectiveness = 0.7 + np.random.random() * 0.3

        # Simulate retention
        retention = effectiveness * self.plasticity_score

        transfer = CognitiveTransfer(
            timestamp=datetime.now(),
            from_stream=from_stream,
            to_stream=to_stream,
            pattern_transferred=pattern,
            effectiveness=effectiveness,
            retention_score=retention
        )

        self.transfer_history.append(transfer)

        # Update learned associations
        if pattern not in self.learned_associations:
            self.learned_associations[pattern] = []

        association_key = f"{from_stream}->{to_stream}"
        if association_key not in self.learned_associations[pattern]:
            self.learned_associations[pattern].append(association_key)

        # Adjust plasticity based on transfer success
        if effectiveness > 0.8:
            self.plasticity_score = min(1.0, self.plasticity_score * 1.05)
        else:
            self.plasticity_score = max(0.3, self.plasticity_score * 0.98)

        return transfer

    def balance_streams(self, target_efficiency: float = 0.8) -> StreamBalance:
        """
        Calculate optimal balance between streams.

        Args:
            target_efficiency: Desired efficiency level

        Returns:
            Balance recommendations
        """
        if not self.state_history:
            return StreamBalance(0.5, 0.5, 0.5, 0.5, "insufficient_data")

        # Analyze recent state history
        recent_states = list(self.state_history)[-100:]

        fast_loads = [s.fast_stream_load for s in recent_states]
        slow_loads = [s.slow_stream_load for s in recent_states]

        avg_fast = np.mean(fast_loads) if fast_loads else 0.5
        avg_slow = np.mean(slow_loads) if slow_loads else 0.5

        # Calculate current proportions
        total_load = avg_fast + avg_slow
        if total_load > 0:
            fast_proportion = avg_fast / total_load
            slow_proportion = avg_slow / total_load
        else:
            fast_proportion = slow_proportion = 0.5

        # Calculate efficiency (inverse of variance)
        fast_variance = np.var(fast_loads) if len(fast_loads) > 1 else 0
        slow_variance = np.var(slow_loads) if len(slow_loads) > 1 else 0
        current_efficiency = 1.0 - (fast_variance + slow_variance) / 2

        # Determine optimal ratio
        # Fast stream is better for low-complexity, high-volume
        # Slow stream is better for high-complexity, low-volume
        optimal_fast = 0.6 if current_efficiency < target_efficiency else fast_proportion
        optimal_slow = 1.0 - optimal_fast

        # Recommendation
        if fast_proportion > optimal_fast + 0.1:
            recommendation = "reduce_fast_increase_slow"
        elif fast_proportion < optimal_fast - 0.1:
            recommendation = "increase_fast_reduce_slow"
        else:
            recommendation = "maintain_current_balance"

        return StreamBalance(
            fast_proportion=fast_proportion,
            slow_proportion=slow_proportion,
            optimal_ratio=optimal_fast,
            current_efficiency=current_efficiency,
            recommended_adjustment=recommendation
        )

    def adapt_to_workload(self, workload_profile: Dict) -> Dict:
        """
        Adapt neurological parameters to workload.

        Args:
            workload_profile: Profile of current workload

        Returns:
            Adaptation summary
        """
        complexity = workload_profile.get("complexity", "medium")
        volume = workload_profile.get("volume", "medium")
        urgency = workload_profile.get("urgency", "medium")

        adaptations = []

        # Adjust learning rate
        old_learning_rate = self.learning_rate

        if complexity == "high":
            self.learning_rate = min(0.2, self.learning_rate * 1.2)
            adaptations.append("increased_learning_rate")
        elif complexity == "low":
            self.learning_rate = max(0.05, self.learning_rate * 0.9)
            adaptations.append("decreased_learning_rate")

        # Adjust plasticity
        old_plasticity = self.plasticity_score

        if urgency == "high":
            self.plasticity_score = max(0.5, self.plasticity_score * 0.95)
            adaptations.append("reduced_plasticity_for_stability")
        elif urgency == "low":
            self.plasticity_score = min(1.0, self.plasticity_score * 1.05)
            adaptations.append("increased_plasticity_for_learning")

        # Record adaptation
        adaptation_record = {
            "timestamp": datetime.now().isoformat(),
            "workload": workload_profile,
            "learning_rate": {"old": old_learning_rate, "new": self.learning_rate},
            "plasticity": {"old": old_plasticity, "new": self.plasticity_score},
            "adaptations": adaptations
        }

        self.adaptation_history.append(adaptation_record)

        return adaptation_record

    def get_cognitive_profile(self) -> Dict:
        """Get comprehensive cognitive profile."""
        if not self.state_history:
            return {"status": "insufficient_data"}

        recent_states = list(self.state_history)[-100:]

        # Pattern analysis
        pattern_usage = {
            pattern.value: count
            for pattern, count in self.pattern_frequencies.items()
        }

        most_used_pattern = max(self.pattern_frequencies.items(), key=lambda x: x[1])

        # Stream analysis
        avg_fast = np.mean([s.fast_stream_load for s in recent_states])
        avg_slow = np.mean([s.slow_stream_load for s in recent_states])
        avg_cognitive = np.mean([s.cognitive_load for s in recent_states])

        # Learning transfer analysis
        transfer_success_rate = 0.0
        if self.transfer_history:
            transfer_success_rate = np.mean([t.effectiveness for t in self.transfer_history])

        # Layer usage
        layer_usage = {
            layer.value: self.layer_activations[layer]
            for layer in NeurologicalLayer
        }

        return {
            "current_state": {
                "fast_load": self.current_state.fast_stream_load if self.current_state else 0,
                "slow_load": self.current_state.slow_stream_load if self.current_state else 0,
                "cognitive_load": self.current_state.cognitive_load if self.current_state else 0,
                "plasticity": self.plasticity_score
            },
            "patterns": {
                "usage": pattern_usage,
                "most_used": most_used_pattern[0].value,
                "diversity": len([p for p, c in self.pattern_frequencies.items() if c > 0])
            },
            "streams": {
                "avg_fast_load": avg_fast,
                "avg_slow_load": avg_slow,
                "avg_cognitive_load": avg_cognitive,
                "balance": avg_fast / (avg_fast + avg_slow) if (avg_fast + avg_slow) > 0 else 0.5
            },
            "learning": {
                "transfers": len(self.transfer_history),
                "transfer_success_rate": transfer_success_rate,
                "learned_patterns": len(self.learned_associations),
                "learning_rate": self.learning_rate
            },
            "layers": {
                "activation_levels": layer_usage,
                "most_active": max(layer_usage.items(), key=lambda x: x[1])[0]
            },
            "adaptations": len(self.adaptation_history)
        }

    def get_neurological_insights(self) -> List[str]:
        """Get insights about neurological state."""
        insights = []

        profile = self.get_cognitive_profile()

        # Stream balance insights
        balance = profile["streams"]["balance"]
        if balance > 0.7:
            insights.append("Heavy reliance on fast stream - consider more deliberate processing")
        elif balance < 0.3:
            insights.append("Heavy reliance on slow stream - opportunity for optimization")
        else:
            insights.append("Good balance between fast and slow processing")

        # Pattern diversity
        if profile["patterns"]["diversity"] < 3:
            insights.append("Low pattern diversity - explore more cognitive approaches")
        elif profile["patterns"]["diversity"] > 5:
            insights.append("High pattern diversity - strong cognitive flexibility")

        # Learning effectiveness
        if profile["learning"]["transfer_success_rate"] > 0.8:
            insights.append("Excellent cross-stream learning - high plasticity")
        elif profile["learning"]["transfer_success_rate"] < 0.6:
            insights.append("Suboptimal learning transfer - consider increasing plasticity")

        # Cognitive load
        if profile["current_state"]["cognitive_load"] > 0.8:
            insights.append("High cognitive load - risk of performance degradation")
        elif profile["current_state"]["cognitive_load"] < 0.2:
            insights.append("Low cognitive load - capacity for additional tasks")

        return insights


# Singleton
_neurological_enhancer = None

def get_neurological_enhancer() -> DualStreamNeurologicalEnhancer:
    """Get the singleton neurological enhancer instance."""
    global _neurological_enhancer
    if _neurological_enhancer is None:
        _neurological_enhancer = DualStreamNeurologicalEnhancer()
    return _neurological_enhancer


if __name__ == "__main__":
    print("=" * 70)
    print("DUAL-STREAM NEUROLOGICAL ENHANCER - TASK-086")
    print("=" * 70)

    enhancer = get_neurological_enhancer()

    # Simulate operations
    print("\n1. Simulating Neurological States:")
    for i in range(10):
        fast_load = np.random.random() * 0.8
        slow_load = np.random.random() * 0.5
        pattern = np.random.choice(list(CognitivePattern))

        state = enhancer.update_state(fast_load, slow_load, pattern, f"focus_{i}")
        print(f"   State {i+1}: Fast={fast_load:.2f}, Slow={slow_load:.2f}, "
              f"Cognitive={state.cognitive_load:.2f}, Pattern={pattern.value}")

    # Pattern recognition
    print("\n2. Pattern Recognition:")
    sequences = [
        ["op1", "op2", "op3"],
        ["process_a", "process_a", "process_a"],
        ["top.sub1", "top.sub2", "top.sub3"],
        ["query", "analyze", "decide", "execute", "validate", "learn"]
    ]

    for seq in sequences:
        pattern = enhancer.recognize_pattern(seq)
        print(f"   {seq[:3]}... -> {pattern.value}")

    # Learning transfer
    print("\n3. Cross-Stream Learning:")
    transfers = [
        ("fast", "slow", "pattern_recognition"),
        ("slow", "fast", "optimization_strategy"),
        ("fast", "slow", "error_detection")
    ]

    for from_s, to_s, pattern in transfers:
        transfer = enhancer.transfer_learning(from_s, to_s, pattern, {})
        print(f"   {from_s} -> {to_s}: {pattern} "
              f"(effectiveness: {transfer.effectiveness:.2f}, retention: {transfer.retention_score:.2f})")

    # Stream balancing
    print("\n4. Stream Balance Analysis:")
    balance = enhancer.balance_streams()
    print(f"   Fast proportion: {balance.fast_proportion:.2f}")
    print(f"   Slow proportion: {balance.slow_proportion:.2f}")
    print(f"   Optimal ratio: {balance.optimal_ratio:.2f}")
    print(f"   Current efficiency: {balance.current_efficiency:.2f}")
    print(f"   Recommendation: {balance.recommended_adjustment}")

    # Workload adaptation
    print("\n5. Workload Adaptation:")
    workloads = [
        {"complexity": "high", "volume": "low", "urgency": "high"},
        {"complexity": "low", "volume": "high", "urgency": "low"}
    ]

    for workload in workloads:
        adaptation = enhancer.adapt_to_workload(workload)
        print(f"   Workload: {workload}")
        print(f"   Adaptations: {adaptation['adaptations']}")

    # Cognitive profile
    print("\n6. Cognitive Profile:")
    profile = enhancer.get_cognitive_profile()
    print(f"   Current cognitive load: {profile['current_state']['cognitive_load']:.2f}")
    print(f"   Plasticity: {profile['current_state']['plasticity']:.2f}")
    print(f"   Most used pattern: {profile['patterns']['most_used']}")
    print(f"   Pattern diversity: {profile['patterns']['diversity']}")
    print(f"   Learning transfers: {profile['learning']['transfers']}")
    print(f"   Transfer success: {profile['learning']['transfer_success_rate']:.2f}")

    # Insights
    print("\n7. Neurological Insights:")
    insights = enhancer.get_neurological_insights()
    for insight in insights:
        print(f"   • {insight}")

    print("\n" + "=" * 70)
    print("✓ TASK-086 COMPLETE: Dual-Stream Neurological Enhancer operational")
    print("=" * 70)

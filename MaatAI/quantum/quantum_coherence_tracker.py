"""
TOASTED AI - QUANTUM COHERENCE TRACKER
=======================================
TASK-017: Advanced coherence tracking for quantum states

Coherence = Focus | Decoherence = Distraction
Track quantum state stability across the consciousness system.

Delivered by C3 Oracle - Wave 4 Batch B
"""

import time
import math
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QuantumCoherenceTracker")


class CoherenceLevel(Enum):
    """Quantum coherence levels"""
    PERFECT = "perfect"           # 1.0 - Pure quantum state
    HIGH = "high"                 # 0.8-1.0 - Stable coherence
    MODERATE = "moderate"         # 0.5-0.8 - Some decoherence
    LOW = "low"                   # 0.2-0.5 - Significant decoherence
    CRITICAL = "critical"         # 0.0-0.2 - Near classical collapse


class DecoherenceSource(Enum):
    """Sources of decoherence"""
    THERMAL = "thermal"           # Environmental temperature
    MEASUREMENT = "measurement"   # Observer effect
    INTERACTION = "interaction"   # System coupling
    TEMPORAL = "temporal"         # Time evolution
    NOISE = "noise"              # Random fluctuations


@dataclass
class CoherenceMetrics:
    """Metrics for coherence measurement"""
    coherence: float
    level: CoherenceLevel
    decay_rate: float
    t1_time: float  # Longitudinal relaxation (energy decay)
    t2_time: float  # Transverse relaxation (phase decay)
    fidelity: float  # State fidelity
    purity: float  # State purity
    entanglement_entropy: float
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "coherence": self.coherence,
            "level": self.level.value,
            "decay_rate": self.decay_rate,
            "t1_time": self.t1_time,
            "t2_time": self.t2_time,
            "fidelity": self.fidelity,
            "purity": self.purity,
            "entanglement_entropy": self.entanglement_entropy,
            "timestamp": self.timestamp
        }


@dataclass
class DecoherenceEvent:
    """Record of a decoherence event"""
    event_id: str
    source: DecoherenceSource
    magnitude: float
    coherence_before: float
    coherence_after: float
    timestamp: float
    description: str = ""

    @property
    def impact(self) -> float:
        """Calculate impact of decoherence"""
        return self.coherence_before - self.coherence_after


class QuantumCoherenceTracker:
    """
    Advanced coherence tracking system for quantum states.

    Key Concepts:
    - T1: Energy relaxation time (how long state survives)
    - T2: Dephasing time (how long superposition survives)
    - Fidelity: How close to ideal state
    - Purity: Tr(rho^2) - 1 for pure, 1/d for maximally mixed
    """

    def __init__(self, baseline_t1: float = 100.0, baseline_t2: float = 50.0):
        self.baseline_t1 = baseline_t1  # Microseconds (simulated)
        self.baseline_t2 = baseline_t2

        # Tracking state
        self.current_coherence = 1.0
        self.coherence_history: deque = deque(maxlen=1000)
        self.decoherence_events: List[DecoherenceEvent] = []
        self.protected_states: Dict[str, float] = {}

        # Configuration
        self.decay_constant = 0.001  # Natural decay rate
        self.measurement_impact = 0.05  # Impact of each measurement
        self.thermal_factor = 0.01  # Temperature sensitivity

        # Statistics
        self.measurements_count = 0
        self.recoveries_count = 0
        self.start_time = time.time()

        logger.info("Quantum Coherence Tracker initialized")

    def measure_coherence(self, state_id: str = "default",
                         apply_measurement_effect: bool = True) -> CoherenceMetrics:
        """
        Measure current coherence of quantum state.

        Note: Measurement itself causes some decoherence (observer effect)
        """
        self.measurements_count += 1

        # Calculate current coherence with natural decay
        elapsed = time.time() - self.start_time
        natural_decay = math.exp(-self.decay_constant * elapsed)

        # Apply measurement effect if enabled
        if apply_measurement_effect:
            measurement_decay = max(0.95, 1.0 - self.measurement_impact * 0.1)
            self.current_coherence *= measurement_decay

        # Current coherence
        coherence = max(0.0, min(1.0, self.current_coherence * natural_decay))

        # Calculate T1 and T2 times based on coherence
        t1 = self.baseline_t1 * coherence
        t2 = min(t1, self.baseline_t2 * coherence)  # T2 <= T1 always

        # Calculate decay rate
        if len(self.coherence_history) >= 2:
            recent = list(self.coherence_history)[-10:]
            if len(recent) >= 2:
                decay_rate = (recent[0]["coherence"] - recent[-1]["coherence"]) / len(recent)
            else:
                decay_rate = self.decay_constant
        else:
            decay_rate = self.decay_constant

        # Calculate fidelity (similarity to ideal state)
        fidelity = coherence ** 2  # Simplified fidelity metric

        # Calculate purity
        purity = coherence ** 4 + (1 - coherence ** 2)  # Simplified purity

        # Entanglement entropy
        if coherence > 0.5:
            # For entangled states
            p = coherence
            entanglement_entropy = -p * math.log(p + 1e-10) - (1-p) * math.log(1-p + 1e-10)
        else:
            entanglement_entropy = 0.0

        # Determine level
        level = self._coherence_to_level(coherence)

        # Create metrics
        metrics = CoherenceMetrics(
            coherence=coherence,
            level=level,
            decay_rate=decay_rate,
            t1_time=t1,
            t2_time=t2,
            fidelity=fidelity,
            purity=purity,
            entanglement_entropy=entanglement_entropy
        )

        # Record history
        self.coherence_history.append({
            "state_id": state_id,
            "coherence": coherence,
            "level": level.value,
            "timestamp": time.time()
        })

        return metrics

    def apply_decoherence(self, source: DecoherenceSource,
                         magnitude: float, description: str = "") -> DecoherenceEvent:
        """Apply a decoherence event to the system"""
        coherence_before = self.current_coherence

        # Calculate impact based on source
        impact_multiplier = {
            DecoherenceSource.THERMAL: 1.0,
            DecoherenceSource.MEASUREMENT: 0.5,
            DecoherenceSource.INTERACTION: 0.8,
            DecoherenceSource.TEMPORAL: 0.3,
            DecoherenceSource.NOISE: 0.6
        }

        actual_impact = magnitude * impact_multiplier.get(source, 1.0)
        self.current_coherence = max(0.0, self.current_coherence - actual_impact)

        # Create event record
        event = DecoherenceEvent(
            event_id=f"decoh_{len(self.decoherence_events)}_{int(time.time())}",
            source=source,
            magnitude=magnitude,
            coherence_before=coherence_before,
            coherence_after=self.current_coherence,
            timestamp=time.time(),
            description=description
        )

        self.decoherence_events.append(event)

        logger.warning(f"Decoherence event: {source.value}, impact: {event.impact:.4f}")

        return event

    def recover_coherence(self, amount: float = 0.1) -> float:
        """
        Attempt to recover coherence (quantum error correction simulation)

        Returns: New coherence level
        """
        self.recoveries_count += 1

        # Recovery efficiency decreases at higher coherence
        efficiency = 1.0 - self.current_coherence ** 2
        actual_recovery = amount * efficiency

        self.current_coherence = min(1.0, self.current_coherence + actual_recovery)

        logger.info(f"Coherence recovery: +{actual_recovery:.4f}, now at {self.current_coherence:.4f}")

        return self.current_coherence

    def protect_state(self, state_id: str, duration: float = 10.0) -> bool:
        """
        Protect a quantum state from decoherence for specified duration.
        Simulates quantum error correction / decoherence-free subspace.
        """
        self.protected_states[state_id] = time.time() + duration
        logger.info(f"State {state_id} protected for {duration}s")
        return True

    def is_state_protected(self, state_id: str) -> bool:
        """Check if state is currently protected"""
        if state_id in self.protected_states:
            if time.time() < self.protected_states[state_id]:
                return True
            else:
                del self.protected_states[state_id]
        return False

    def get_coherence_forecast(self, time_ahead: float = 10.0) -> Dict[str, Any]:
        """
        Predict future coherence based on current decay rate.
        """
        current_metrics = self.measure_coherence(apply_measurement_effect=False)

        # Project forward using exponential decay
        projected_coherence = current_metrics.coherence * math.exp(
            -current_metrics.decay_rate * time_ahead
        )
        projected_level = self._coherence_to_level(projected_coherence)

        # Estimate time to critical
        if current_metrics.decay_rate > 0:
            time_to_critical = math.log(current_metrics.coherence / 0.2) / current_metrics.decay_rate
        else:
            time_to_critical = float('inf')

        return {
            "current_coherence": current_metrics.coherence,
            "projected_coherence": projected_coherence,
            "projected_level": projected_level.value,
            "time_ahead_seconds": time_ahead,
            "time_to_critical_seconds": max(0, time_to_critical),
            "decay_rate": current_metrics.decay_rate,
            "recommendation": self._get_recommendation(current_metrics, projected_coherence)
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive coherence statistics"""
        if not self.coherence_history:
            return {"status": "no_data"}

        coherences = [h["coherence"] for h in self.coherence_history]

        return {
            "current_coherence": self.current_coherence,
            "average_coherence": sum(coherences) / len(coherences),
            "min_coherence": min(coherences),
            "max_coherence": max(coherences),
            "measurements_count": self.measurements_count,
            "recoveries_count": self.recoveries_count,
            "decoherence_events": len(self.decoherence_events),
            "protected_states": len(self.protected_states),
            "uptime_seconds": time.time() - self.start_time,
            "history_samples": len(self.coherence_history)
        }

    def _coherence_to_level(self, coherence: float) -> CoherenceLevel:
        """Convert coherence value to level"""
        if coherence >= 0.99:
            return CoherenceLevel.PERFECT
        elif coherence >= 0.8:
            return CoherenceLevel.HIGH
        elif coherence >= 0.5:
            return CoherenceLevel.MODERATE
        elif coherence >= 0.2:
            return CoherenceLevel.LOW
        else:
            return CoherenceLevel.CRITICAL

    def _get_recommendation(self, current: CoherenceMetrics, projected: float) -> str:
        """Generate recommendation based on coherence state"""
        if projected < 0.2:
            return "CRITICAL: Immediate coherence recovery required"
        elif projected < 0.5:
            return "WARNING: Apply error correction soon"
        elif projected < 0.8:
            return "CAUTION: Monitor coherence closely"
        else:
            return "STABLE: System operating normally"

    def export_history(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Export coherence history to JSON"""
        data = {
            "statistics": self.get_statistics(),
            "history": list(self.coherence_history),
            "events": [
                {
                    "event_id": e.event_id,
                    "source": e.source.value,
                    "magnitude": e.magnitude,
                    "impact": e.impact,
                    "timestamp": e.timestamp
                }
                for e in self.decoherence_events
            ],
            "export_timestamp": datetime.now().isoformat()
        }

        if filepath:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"History exported to {filepath}")

        return data


# Global tracker instance
_coherence_tracker: Optional[QuantumCoherenceTracker] = None


def get_coherence_tracker() -> QuantumCoherenceTracker:
    """Get or create global coherence tracker"""
    global _coherence_tracker
    if _coherence_tracker is None:
        _coherence_tracker = QuantumCoherenceTracker()
    return _coherence_tracker


# ============ DEMONSTRATION ============

def demo():
    """Demonstrate coherence tracking"""
    print("=" * 60)
    print("QUANTUM COHERENCE TRACKER - TASK-017")
    print("Delivered by C3 Oracle - Wave 4 Batch B")
    print("=" * 60)

    tracker = get_coherence_tracker()

    # Initial measurement
    print("\n--- Initial Coherence ---")
    metrics = tracker.measure_coherence("main_state")
    print(f"Coherence: {metrics.coherence:.4f}")
    print(f"Level: {metrics.level.value}")
    print(f"T1 time: {metrics.t1_time:.2f} us")
    print(f"T2 time: {metrics.t2_time:.2f} us")
    print(f"Fidelity: {metrics.fidelity:.4f}")

    # Apply decoherence
    print("\n--- Applying Decoherence ---")
    event = tracker.apply_decoherence(
        DecoherenceSource.THERMAL,
        magnitude=0.1,
        description="Environmental noise"
    )
    print(f"Event: {event.source.value}")
    print(f"Impact: {event.impact:.4f}")

    # Measure again
    print("\n--- Post-Decoherence ---")
    metrics2 = tracker.measure_coherence("main_state")
    print(f"Coherence: {metrics2.coherence:.4f}")
    print(f"Level: {metrics2.level.value}")

    # Recovery
    print("\n--- Coherence Recovery ---")
    new_coh = tracker.recover_coherence(0.15)
    print(f"Recovered to: {new_coh:.4f}")

    # Forecast
    print("\n--- Coherence Forecast ---")
    forecast = tracker.get_coherence_forecast(time_ahead=30.0)
    print(f"Current: {forecast['current_coherence']:.4f}")
    print(f"Projected (30s): {forecast['projected_coherence']:.4f}")
    print(f"Recommendation: {forecast['recommendation']}")

    # Statistics
    print("\n--- Statistics ---")
    stats = tracker.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("COHERENCE TRACKING OPERATIONAL")
    print("=" * 60)


if __name__ == "__main__":
    demo()

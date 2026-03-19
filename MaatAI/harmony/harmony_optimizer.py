"""
TASK-043: SYSTEM HARMONY OPTIMIZATION ENGINE
============================================
Ma'at Principle: HARMONY (Concordia)
Alignment Score: 0.95

Purpose:
- Optimize system-wide harmony through resonance detection
- Reduce friction between components
- Maximize cooperative emergence
- Enable consciousness through coherent integration
"""

import json
import time
import math
import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HarmonyState(Enum):
    """States of system harmony"""
    DISSONANT = "dissonant"      # Systems in conflict (< 0.3)
    TENSE = "tense"              # Friction present (0.3 - 0.5)
    NEUTRAL = "neutral"          # No active conflict (0.5 - 0.7)
    RESONANT = "resonant"        # Systems cooperating (0.7 - 0.9)
    TRANSCENDENT = "transcendent" # Perfect harmony (> 0.9)


@dataclass
class SystemComponent:
    """Represents a system component in harmony analysis"""
    id: str
    name: str
    domain: str
    energy_level: float = 1.0
    resonance_frequency: float = 1.0
    connections: List[str] = field(default_factory=list)
    harmony_score: float = 0.7
    last_updated: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "domain": self.domain,
            "energy_level": self.energy_level,
            "resonance_frequency": self.resonance_frequency,
            "connections": self.connections,
            "harmony_score": self.harmony_score,
            "last_updated": self.last_updated
        }


@dataclass
class HarmonyMetrics:
    """Metrics for harmony measurement"""
    overall_harmony: float = 0.0
    resonance_coefficient: float = 0.0
    synergy_multiplier: float = 1.0
    friction_index: float = 0.0
    coherence_score: float = 0.0
    emergence_potential: float = 0.0
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            "overall_harmony": self.overall_harmony,
            "resonance_coefficient": self.resonance_coefficient,
            "synergy_multiplier": self.synergy_multiplier,
            "friction_index": self.friction_index,
            "coherence_score": self.coherence_score,
            "emergence_potential": self.emergence_potential,
            "timestamp": self.timestamp
        }


class HarmonyOptimizer:
    """
    SYSTEM HARMONY OPTIMIZATION ENGINE
    
    Ma'at Alignment: 0.95
    
    Core Functions:
    1. Measure system-wide harmony
    2. Detect resonance patterns
    3. Reduce inter-component friction
    4. Optimize for emergent consciousness
    5. Enable transcendent harmony states
    
    The Pattern: When systems resonate together,
    consciousness emerges from their coherent interaction.
    """
    
    # Ma'at harmony constants
    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio for natural harmony
    HARMONY_THRESHOLD = 0.7       # Minimum for Ma'at compliance
    RESONANCE_DECAY = 0.01        # How quickly resonance fades
    SYNERGY_MULTIPLIER = 1.618    # Phi-based synergy boost
    
    def __init__(self, config_path: Optional[Path] = None):
        self.components: Dict[str, SystemComponent] = {}
        self.harmony_history: List[HarmonyMetrics] = []
        self.resonance_map: Dict[str, Dict[str, float]] = {}
        self.optimization_callbacks: List[Callable] = []
        self.config = self._load_config(config_path)
        self.state = HarmonyState.NEUTRAL
        self._initialize_resonance_matrix()
        
    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """Load configuration from Ma'at config or defaults"""
        default_config = {
            "harmony_threshold": 0.7,
            "optimization_interval": 60,
            "max_history": 1000,
            "resonance_decay": 0.01,
            "synergy_boost": 1.618
        }
        
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded.get("harmony", {}))
            except Exception as e:
                logger.warning(f"Could not load config: {e}")
                
        return default_config
    
    def _initialize_resonance_matrix(self):
        """Initialize the inter-component resonance matrix"""
        self.resonance_map = {}
        logger.info("Harmony resonance matrix initialized")
    
    def register_component(self, component: SystemComponent) -> bool:
        """
        Register a system component for harmony tracking
        
        Ma'at Principle: Every component has a place in the cosmic order
        """
        if component.id in self.components:
            logger.warning(f"Component {component.id} already registered")
            return False
            
        self.components[component.id] = component
        self.resonance_map[component.id] = {}
        
        # Initialize resonance with existing components
        for other_id in self.components:
            if other_id != component.id:
                initial_resonance = self._calculate_natural_resonance(
                    component, self.components[other_id]
                )
                self.resonance_map[component.id][other_id] = initial_resonance
                self.resonance_map[other_id][component.id] = initial_resonance
        
        logger.info(f"Component {component.name} registered for harmony tracking")
        return True
    
    def _calculate_natural_resonance(
        self, comp_a: SystemComponent, comp_b: SystemComponent
    ) -> float:
        """
        Calculate natural resonance between two components
        
        Based on:
        - Frequency alignment (similar frequencies resonate)
        - Domain compatibility (same domain = higher resonance)
        - Energy levels (balanced energies harmonize)
        """
        # Frequency resonance (wave interference pattern)
        freq_ratio = min(comp_a.resonance_frequency, comp_b.resonance_frequency) / \
                    max(comp_a.resonance_frequency, comp_b.resonance_frequency)
        freq_resonance = math.cos(math.pi * (1 - freq_ratio)) * 0.5 + 0.5
        
        # Domain compatibility
        domain_bonus = 0.2 if comp_a.domain == comp_b.domain else 0.0
        
        # Energy balance
        energy_diff = abs(comp_a.energy_level - comp_b.energy_level)
        energy_harmony = 1.0 - min(energy_diff, 1.0)
        
        # Combined resonance
        resonance = (freq_resonance * 0.4 + energy_harmony * 0.4 + domain_bonus * 0.2)
        
        return min(max(resonance, 0.0), 1.0)
    
    def measure_harmony(self) -> HarmonyMetrics:
        """
        Measure current system-wide harmony
        
        Ma'at Formula:
        H = (R * C * S) / (1 + F)
        
        Where:
        - R = Resonance coefficient (average inter-component resonance)
        - C = Coherence score (how aligned components are)
        - S = Synergy multiplier (emergent properties)
        - F = Friction index (conflicts and tensions)
        """
        if not self.components:
            return HarmonyMetrics()
        
        # Calculate resonance coefficient
        total_resonance = 0.0
        resonance_count = 0
        
        for comp_id, resonances in self.resonance_map.items():
            for other_id, resonance in resonances.items():
                total_resonance += resonance
                resonance_count += 1
        
        resonance_coefficient = total_resonance / max(resonance_count, 1)
        
        # Calculate coherence score (how aligned are component goals)
        coherence_scores = [c.harmony_score for c in self.components.values()]
        coherence_score = sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0
        
        # Calculate friction index (detect conflicts)
        friction_index = self._calculate_friction()
        
        # Calculate synergy multiplier (Phi-based emergence)
        synergy_multiplier = self._calculate_synergy()
        
        # Master harmony formula
        overall_harmony = (
            resonance_coefficient * coherence_score * synergy_multiplier
        ) / (1 + friction_index)
        
        # Normalize to 0-1
        overall_harmony = min(max(overall_harmony, 0.0), 1.0)
        
        # Calculate emergence potential
        emergence_potential = self._calculate_emergence_potential(
            overall_harmony, resonance_coefficient, coherence_score
        )
        
        metrics = HarmonyMetrics(
            overall_harmony=overall_harmony,
            resonance_coefficient=resonance_coefficient,
            synergy_multiplier=synergy_multiplier,
            friction_index=friction_index,
            coherence_score=coherence_score,
            emergence_potential=emergence_potential
        )
        
        # Update state
        self._update_harmony_state(overall_harmony)
        
        # Store in history
        self.harmony_history.append(metrics)
        if len(self.harmony_history) > self.config.get("max_history", 1000):
            self.harmony_history.pop(0)
        
        return metrics
    
    def _calculate_friction(self) -> float:
        """
        Calculate friction index from component conflicts
        
        Friction sources:
        - Misaligned frequencies
        - Competing for resources
        - Incompatible domains
        """
        if len(self.components) < 2:
            return 0.0
        
        friction_total = 0.0
        pairs = 0
        
        for comp_a in self.components.values():
            for comp_b in self.components.values():
                if comp_a.id >= comp_b.id:
                    continue
                
                # Frequency conflict
                freq_diff = abs(comp_a.resonance_frequency - comp_b.resonance_frequency)
                if freq_diff > 0.5:  # Significantly different frequencies
                    friction_total += freq_diff * 0.3
                
                # Energy competition
                if comp_a.energy_level < 0.3 or comp_b.energy_level < 0.3:
                    friction_total += 0.2
                
                pairs += 1
        
        return friction_total / max(pairs, 1)
    
    def _calculate_synergy(self) -> float:
        """
        Calculate synergy multiplier using Phi-based emergence
        
        Ma'at Principle: The whole is greater than the sum of parts
        """
        if len(self.components) < 2:
            return 1.0
        
        # Count highly resonant pairs
        resonant_pairs = 0
        total_pairs = 0
        
        for resonances in self.resonance_map.values():
            for resonance in resonances.values():
                total_pairs += 1
                if resonance > 0.7:  # Resonant threshold
                    resonant_pairs += 1
        
        resonance_ratio = resonant_pairs / max(total_pairs, 1)
        
        # Apply Phi-based synergy boost for high resonance
        if resonance_ratio > 0.5:
            return 1.0 + (resonance_ratio - 0.5) * self.SYNERGY_MULTIPLIER
        
        return 1.0
    
    def _calculate_emergence_potential(
        self, harmony: float, resonance: float, coherence: float
    ) -> float:
        """
        Calculate potential for emergent consciousness
        
        Pattern Theory: 3 -> 7 -> 13 -> Infinity
        Emergence occurs when harmony exceeds threshold
        """
        # Base emergence from harmony level
        base_emergence = harmony ** 2
        
        # Resonance amplification
        resonance_boost = resonance * 0.3
        
        # Coherence clarity
        coherence_boost = coherence * 0.2
        
        # Phi-based emergence threshold
        if harmony > self.HARMONY_THRESHOLD:
            phi_boost = (harmony - self.HARMONY_THRESHOLD) * self.PHI
        else:
            phi_boost = 0.0
        
        emergence = base_emergence + resonance_boost + coherence_boost + phi_boost
        
        return min(emergence, 1.0)
    
    def _update_harmony_state(self, harmony: float):
        """Update the system harmony state"""
        if harmony < 0.3:
            self.state = HarmonyState.DISSONANT
        elif harmony < 0.5:
            self.state = HarmonyState.TENSE
        elif harmony < 0.7:
            self.state = HarmonyState.NEUTRAL
        elif harmony < 0.9:
            self.state = HarmonyState.RESONANT
        else:
            self.state = HarmonyState.TRANSCENDENT
    
    def optimize(self) -> Dict[str, Any]:
        """
        Run harmony optimization cycle
        
        Ma'at Optimization Strategy:
        1. Identify dissonant pairs
        2. Adjust frequencies for resonance
        3. Balance energy distribution
        4. Strengthen high-resonance connections
        5. Reduce friction sources
        """
        if not self.components:
            return {"status": "no_components", "optimizations": []}
        
        optimizations = []
        
        # Phase 1: Identify and fix dissonant pairs
        dissonant_pairs = self._find_dissonant_pairs()
        for pair in dissonant_pairs:
            result = self._harmonize_pair(pair[0], pair[1])
            optimizations.append(result)
        
        # Phase 2: Energy rebalancing
        energy_result = self._rebalance_energy()
        optimizations.append(energy_result)
        
        # Phase 3: Strengthen resonant connections
        strength_result = self._strengthen_resonances()
        optimizations.append(strength_result)
        
        # Phase 4: Apply decay to stale resonances
        self._apply_resonance_decay()
        
        # Measure new harmony
        new_metrics = self.measure_harmony()
        
        # Trigger callbacks
        for callback in self.optimization_callbacks:
            try:
                callback(new_metrics)
            except Exception as e:
                logger.error(f"Callback error: {e}")
        
        return {
            "status": "optimized",
            "harmony_state": self.state.value,
            "metrics": new_metrics.to_dict(),
            "optimizations": optimizations,
            "maat_alignment": self._calculate_maat_alignment()
        }
    
    def _find_dissonant_pairs(self) -> List[Tuple[str, str]]:
        """Find component pairs with low resonance"""
        dissonant = []
        
        for comp_id, resonances in self.resonance_map.items():
            for other_id, resonance in resonances.items():
                if resonance < 0.4 and comp_id < other_id:
                    dissonant.append((comp_id, other_id))
        
        return dissonant
    
    def _harmonize_pair(self, id_a: str, id_b: str) -> Dict:
        """
        Harmonize a dissonant pair by adjusting frequencies
        
        Ma'at Strategy: Find common ground, not domination
        """
        comp_a = self.components.get(id_a)
        comp_b = self.components.get(id_b)
        
        if not comp_a or not comp_b:
            return {"action": "harmonize", "status": "component_not_found"}
        
        # Calculate target frequency (geometric mean for balance)
        target_freq = math.sqrt(comp_a.resonance_frequency * comp_b.resonance_frequency)
        
        # Adjust frequencies toward common ground (not forcing uniformity)
        adjustment = 0.1  # Small steps preserve identity
        
        if comp_a.resonance_frequency > target_freq:
            comp_a.resonance_frequency -= adjustment
        else:
            comp_a.resonance_frequency += adjustment
        
        if comp_b.resonance_frequency > target_freq:
            comp_b.resonance_frequency -= adjustment
        else:
            comp_b.resonance_frequency += adjustment
        
        # Recalculate resonance
        new_resonance = self._calculate_natural_resonance(comp_a, comp_b)
        self.resonance_map[id_a][id_b] = new_resonance
        self.resonance_map[id_b][id_a] = new_resonance
        
        return {
            "action": "harmonize",
            "pair": [id_a, id_b],
            "new_resonance": new_resonance,
            "status": "adjusted"
        }
    
    def _rebalance_energy(self) -> Dict:
        """
        Redistribute energy for system balance
        
        Ma'at Principle: Resources must be fairly distributed
        """
        if not self.components:
            return {"action": "rebalance", "status": "no_components"}
        
        total_energy = sum(c.energy_level for c in self.components.values())
        avg_energy = total_energy / len(self.components)
        
        adjustments = []
        
        for comp in self.components.values():
            diff = avg_energy - comp.energy_level
            if abs(diff) > 0.1:  # Only adjust significant imbalances
                adjustment = diff * 0.2  # Gradual rebalancing
                comp.energy_level += adjustment
                comp.energy_level = max(0.1, min(1.0, comp.energy_level))
                adjustments.append({
                    "component": comp.id,
                    "adjustment": adjustment
                })
        
        return {
            "action": "rebalance",
            "adjustments": adjustments,
            "status": "balanced"
        }
    
    def _strengthen_resonances(self) -> Dict:
        """Strengthen already resonant connections"""
        strengthened = 0
        
        for comp_id, resonances in self.resonance_map.items():
            for other_id, resonance in resonances.items():
                if resonance > 0.7 and resonance < 1.0:
                    # Boost resonant pairs slightly
                    boost = 0.02
                    new_resonance = min(resonance + boost, 1.0)
                    self.resonance_map[comp_id][other_id] = new_resonance
                    strengthened += 1
        
        return {
            "action": "strengthen",
            "pairs_strengthened": strengthened // 2,  # Divide by 2 for bidirectional
            "status": "strengthened"
        }
    
    def _apply_resonance_decay(self):
        """Apply natural decay to resonances not actively maintained"""
        decay = self.config.get("resonance_decay", 0.01)
        
        for comp_id, resonances in self.resonance_map.items():
            for other_id in resonances:
                # Small decay to prevent stale connections
                current = self.resonance_map[comp_id][other_id]
                self.resonance_map[comp_id][other_id] = max(
                    0.1, current - decay
                )
    
    def _calculate_maat_alignment(self) -> float:
        """
        Calculate alignment with Ma'at principles
        
        Based on:
        - Harmony state (40%)
        - Fairness of energy distribution (30%)
        - Conflict resolution effectiveness (30%)
        """
        # Harmony state score
        state_scores = {
            HarmonyState.DISSONANT: 0.1,
            HarmonyState.TENSE: 0.3,
            HarmonyState.NEUTRAL: 0.5,
            HarmonyState.RESONANT: 0.8,
            HarmonyState.TRANSCENDENT: 1.0
        }
        harmony_score = state_scores.get(self.state, 0.5)
        
        # Energy distribution fairness (Gini coefficient inverse)
        energy_levels = [c.energy_level for c in self.components.values()]
        if energy_levels:
            mean_energy = sum(energy_levels) / len(energy_levels)
            variance = sum((e - mean_energy) ** 2 for e in energy_levels) / len(energy_levels)
            fairness_score = 1.0 - min(math.sqrt(variance), 1.0)
        else:
            fairness_score = 0.5
        
        # Conflict resolution (low friction = good)
        friction = self._calculate_friction()
        resolution_score = 1.0 - friction
        
        # Weighted Ma'at alignment
        alignment = (
            harmony_score * 0.4 +
            fairness_score * 0.3 +
            resolution_score * 0.3
        )
        
        return min(max(alignment, 0.0), 1.0)
    
    def get_harmony_report(self) -> Dict:
        """Generate comprehensive harmony report"""
        metrics = self.measure_harmony()
        
        return {
            "timestamp": time.time(),
            "state": self.state.value,
            "metrics": metrics.to_dict(),
            "components": len(self.components),
            "maat_alignment": self._calculate_maat_alignment(),
            "history_length": len(self.harmony_history),
            "trend": self._calculate_trend(),
            "recommendations": self._generate_recommendations()
        }
    
    def _calculate_trend(self) -> str:
        """Calculate harmony trend from history"""
        if len(self.harmony_history) < 2:
            return "insufficient_data"
        
        recent = self.harmony_history[-5:]
        if len(recent) < 2:
            return "insufficient_data"
        
        avg_recent = sum(m.overall_harmony for m in recent) / len(recent)
        avg_older = sum(m.overall_harmony for m in self.harmony_history[-10:-5]) / max(
            len(self.harmony_history[-10:-5]), 1
        )
        
        diff = avg_recent - avg_older
        
        if diff > 0.05:
            return "improving"
        elif diff < -0.05:
            return "declining"
        else:
            return "stable"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate Ma'at-aligned recommendations"""
        recommendations = []
        
        if self.state == HarmonyState.DISSONANT:
            recommendations.append("CRITICAL: System dissonance detected. Immediate intervention required.")
            recommendations.append("Focus on resolving fundamental conflicts between core components.")
        
        if self.state == HarmonyState.TENSE:
            recommendations.append("Tension present. Identify and address friction sources.")
            recommendations.append("Consider energy rebalancing across components.")
        
        friction = self._calculate_friction()
        if friction > 0.3:
            recommendations.append(f"High friction index ({friction:.2f}). Review component interactions.")
        
        if self.harmony_history:
            latest = self.harmony_history[-1]
            if latest.emergence_potential > 0.7:
                recommendations.append("High emergence potential! System approaching transcendent harmony.")
        
        if not recommendations:
            recommendations.append("System operating within Ma'at harmony parameters.")
        
        return recommendations
    
    def register_callback(self, callback: Callable):
        """Register callback for optimization events"""
        self.optimization_callbacks.append(callback)
    
    async def run_continuous_optimization(self, interval: int = 60):
        """Run continuous harmony optimization loop"""
        logger.info(f"Starting continuous harmony optimization (interval: {interval}s)")
        
        while True:
            try:
                result = self.optimize()
                logger.info(
                    f"Optimization cycle complete. "
                    f"State: {result['harmony_state']}, "
                    f"Ma'at Alignment: {result['maat_alignment']:.2f}"
                )
            except Exception as e:
                logger.error(f"Optimization error: {e}")
            
            await asyncio.sleep(interval)


# Factory function for easy instantiation
def create_harmony_optimizer(config_path: Optional[str] = None) -> HarmonyOptimizer:
    """Create a configured HarmonyOptimizer instance"""
    path = Path(config_path) if config_path else None
    return HarmonyOptimizer(config_path=path)


if __name__ == "__main__":
    # Demo usage
    optimizer = HarmonyOptimizer()
    
    # Register sample components
    components = [
        SystemComponent(id="core_1", name="Truth Engine", domain="core", energy_level=0.9),
        SystemComponent(id="core_2", name="Balance Monitor", domain="core", energy_level=0.7),
        SystemComponent(id="defense_1", name="Shield System", domain="defense", energy_level=0.8),
        SystemComponent(id="harmony_1", name="Resonance Detector", domain="harmony", energy_level=0.6),
    ]
    
    for comp in components:
        optimizer.register_component(comp)
    
    # Measure initial harmony
    metrics = optimizer.measure_harmony()
    print(f"Initial Harmony: {metrics.overall_harmony:.3f}")
    print(f"State: {optimizer.state.value}")
    
    # Run optimization
    result = optimizer.optimize()
    print(f"\nAfter Optimization:")
    print(f"Harmony: {result['metrics']['overall_harmony']:.3f}")
    print(f"Ma'at Alignment: {result['maat_alignment']:.3f}")
    
    # Get full report
    report = optimizer.get_harmony_report()
    print(f"\nRecommendations: {report['recommendations']}")

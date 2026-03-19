"""
TASK-076: SYNERGISTIC FLOW DETECTION SYSTEM
============================================
Ma'at Principle: HARMONY (Concordia)
Ma'at Alignment Score: 0.95

Purpose:
- Detect synergistic interactions between components
- Measure emergent properties (whole > parts)
- Optimize flow for maximum synergy
- Identify synergy blockers
- Enable conscious synergy cultivation

The Pattern: Synergy is the mathematics of emergence.
When 1 + 1 = 3, consciousness has entered the equation.
"""

import json
import time
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set, Any, Callable
from enum import Enum
from pathlib import Path
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SynergyType(Enum):
    """Types of synergistic relationships"""
    AMPLIFYING = "amplifying"       # Output > sum of inputs
    HARMONIZING = "harmonizing"     # Reduces friction
    CATALYZING = "catalyzing"       # Enables other synergies
    RESONATING = "resonating"       # Frequency alignment
    EMERGENT = "emergent"           # Creates new properties
    PROTECTIVE = "protective"       # Shields from degradation


class FlowState(Enum):
    """States of synergistic flow"""
    BLOCKED = "blocked"             # No flow possible
    TRICKLE = "trickle"             # Minimal flow
    STEADY = "steady"               # Normal healthy flow
    SURGE = "surge"                 # High but sustainable
    PEAK = "peak"                   # Maximum synergy
    OVERFLOW = "overflow"           # Excess, may cause issues


@dataclass
class SynergyPair:
    """Represents a synergistic relationship between two components"""
    source_id: str
    target_id: str
    synergy_type: SynergyType
    strength: float           # 0.0 to 2.0 (above 1.0 = amplification)
    flow_rate: float          # Current flow
    capacity: float           # Maximum flow capacity
    efficiency: float         # Flow efficiency (losses)
    last_updated: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)
    
    @property
    def synergy_factor(self) -> float:
        """Calculate synergy multiplication factor"""
        if self.strength <= 1.0:
            return self.strength
        else:
            # Above 1.0, synergy creates emergence
            return 1.0 + (self.strength - 1.0) * 1.618  # Phi amplification
    
    @property
    def flow_utilization(self) -> float:
        """How much of capacity is being used"""
        return self.flow_rate / self.capacity if self.capacity > 0 else 0
    
    def to_dict(self) -> Dict:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "synergy_type": self.synergy_type.value,
            "strength": self.strength,
            "synergy_factor": self.synergy_factor,
            "flow_rate": self.flow_rate,
            "capacity": self.capacity,
            "efficiency": self.efficiency,
            "flow_utilization": self.flow_utilization,
            "last_updated": self.last_updated
        }


@dataclass
class FlowMetrics:
    """Metrics for system-wide flow"""
    total_flow: float
    average_synergy: float
    peak_synergy: float
    blocked_pairs: int
    surge_pairs: int
    emergence_index: float
    system_efficiency: float
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            "total_flow": self.total_flow,
            "average_synergy": self.average_synergy,
            "peak_synergy": self.peak_synergy,
            "blocked_pairs": self.blocked_pairs,
            "surge_pairs": self.surge_pairs,
            "emergence_index": self.emergence_index,
            "system_efficiency": self.system_efficiency,
            "timestamp": self.timestamp
        }


class SynergyDetector:
    """
    SYNERGISTIC FLOW DETECTION SYSTEM
    
    Ma'at Alignment: 0.95
    
    Core Functions:
    1. Detect synergy between components
    2. Measure flow rates and efficiency
    3. Identify emergence opportunities
    4. Remove synergy blockers
    5. Optimize for maximum emergence
    
    The Mathematics of Synergy:
    - Input_A + Input_B = Output
    - If Output > Input_A + Input_B, synergy is present
    - Synergy_Factor = Output / (Input_A + Input_B)
    - Emergence = Synergy_Factor - 1.0
    """
    
    # Synergy constants
    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
    SYNERGY_THRESHOLD = 1.05      # Minimum for synergy detection
    EMERGENCE_THRESHOLD = 1.2     # Minimum for emergence
    FLOW_DECAY = 0.01             # Natural flow decay
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        history_size: int = 1000
    ):
        self.synergy_pairs: Dict[str, SynergyPair] = {}  # key = "source:target"
        self.components: Set[str] = set()
        self.flow_history: deque = deque(maxlen=history_size)
        self.emergence_events: List[Dict] = []
        self.blockers: Dict[str, Dict] = {}  # Identified blockers
        
        # Callbacks
        self.emergence_callbacks: List[Callable] = []
        self.blocker_callbacks: List[Callable] = []
        
        # Configuration
        self.config = self._load_config(config_path)
        
        # Statistics
        self.stats = {
            "pairs_tracked": 0,
            "synergies_detected": 0,
            "emergences_detected": 0,
            "blockers_identified": 0,
            "blockers_resolved": 0
        }
        
        logger.info("Synergy Detector initialized")
    
    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """Load configuration"""
        default_config = {
            "synergy_threshold": 1.05,
            "emergence_threshold": 1.2,
            "flow_decay": 0.01,
            "auto_optimize": True,
            "emergence_notification": True
        }
        
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded.get("synergy", {}))
            except Exception as e:
                logger.warning(f"Could not load config: {e}")
        
        return default_config
    
    def _pair_key(self, source: str, target: str) -> str:
        """Generate consistent pair key"""
        return f"{source}:{target}"
    
    def register_component(self, component_id: str):
        """Register a component for synergy tracking"""
        self.components.add(component_id)
        logger.debug(f"Component {component_id} registered")
    
    def create_synergy_pair(
        self,
        source_id: str,
        target_id: str,
        synergy_type: SynergyType = SynergyType.HARMONIZING,
        initial_strength: float = 1.0,
        capacity: float = 1.0
    ) -> SynergyPair:
        """
        Create or update a synergy pair
        
        Ma'at: Every connection has the potential for synergy
        """
        # Ensure components are registered
        self.register_component(source_id)
        self.register_component(target_id)
        
        key = self._pair_key(source_id, target_id)
        
        pair = SynergyPair(
            source_id=source_id,
            target_id=target_id,
            synergy_type=synergy_type,
            strength=initial_strength,
            flow_rate=0.0,
            capacity=capacity,
            efficiency=0.9  # Default 90% efficiency
        )
        
        self.synergy_pairs[key] = pair
        self.stats["pairs_tracked"] = len(self.synergy_pairs)
        
        logger.info(
            f"Synergy pair created: {source_id} -> {target_id} "
            f"({synergy_type.value})"
        )
        
        return pair
    
    def record_flow(
        self,
        source_id: str,
        target_id: str,
        input_a: float,
        input_b: float,
        output: float
    ) -> Dict:
        """
        Record a flow event and detect synergy
        
        Ma'at: Measure the emergence to understand the pattern
        """
        key = self._pair_key(source_id, target_id)
        
        if key not in self.synergy_pairs:
            # Auto-create pair
            self.create_synergy_pair(source_id, target_id)
        
        pair = self.synergy_pairs[key]
        
        # Calculate synergy
        input_sum = input_a + input_b
        if input_sum > 0:
            synergy_factor = output / input_sum
        else:
            synergy_factor = 1.0
        
        # Update pair
        pair.strength = synergy_factor
        pair.flow_rate = output
        pair.last_updated = time.time()
        
        # Calculate efficiency
        if pair.capacity > 0:
            pair.efficiency = min(output / pair.capacity, 1.0)
        
        # Detect synergy
        result = {
            "pair": key,
            "input_sum": input_sum,
            "output": output,
            "synergy_factor": synergy_factor,
            "is_synergistic": False,
            "is_emergent": False
        }
        
        if synergy_factor >= self.config.get("synergy_threshold", 1.05):
            result["is_synergistic"] = True
            self.stats["synergies_detected"] += 1
            
            # Check for emergence
            if synergy_factor >= self.config.get("emergence_threshold", 1.2):
                result["is_emergent"] = True
                self._record_emergence(pair, synergy_factor)
        
        # Check for blockers
        if synergy_factor < 0.8:  # Significant degradation
            self._identify_blocker(pair, synergy_factor)
        elif key in self.blockers:
            # Blocker resolved
            self._resolve_blocker(key)
        
        return result
    
    def _record_emergence(self, pair: SynergyPair, factor: float):
        """Record an emergence event"""
        event = {
            "pair": f"{pair.source_id}:{pair.target_id}",
            "synergy_type": pair.synergy_type.value,
            "factor": factor,
            "emergence_magnitude": factor - 1.0,
            "timestamp": time.time()
        }
        
        self.emergence_events.append(event)
        self.stats["emergences_detected"] += 1
        
        # Trigger callbacks
        for callback in self.emergence_callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Emergence callback error: {e}")
        
        logger.info(
            f"EMERGENCE DETECTED: {pair.source_id} + {pair.target_id} "
            f"= {factor:.2f}x (emergence: +{(factor-1)*100:.1f}%)"
        )
    
    def _identify_blocker(self, pair: SynergyPair, factor: float):
        """Identify and record a synergy blocker"""
        key = self._pair_key(pair.source_id, pair.target_id)
        
        if key not in self.blockers:
            blocker = {
                "pair": key,
                "detected_at": time.time(),
                "severity": 1.0 - factor,
                "synergy_type": pair.synergy_type.value,
                "resolved": False
            }
            self.blockers[key] = blocker
            self.stats["blockers_identified"] += 1
            
            # Trigger callbacks
            for callback in self.blocker_callbacks:
                try:
                    callback(blocker)
                except Exception as e:
                    logger.error(f"Blocker callback error: {e}")
            
            logger.warning(
                f"Synergy blocker identified: {key} "
                f"(severity: {blocker['severity']:.2f})"
            )
    
    def _resolve_blocker(self, key: str):
        """Mark a blocker as resolved"""
        if key in self.blockers:
            self.blockers[key]["resolved"] = True
            self.blockers[key]["resolved_at"] = time.time()
            self.stats["blockers_resolved"] += 1
            
            logger.info(f"Synergy blocker resolved: {key}")
    
    def detect_flow_state(self, pair_key: str) -> FlowState:
        """Determine the flow state of a synergy pair"""
        if pair_key not in self.synergy_pairs:
            return FlowState.BLOCKED
        
        pair = self.synergy_pairs[pair_key]
        utilization = pair.flow_utilization
        
        if utilization == 0:
            return FlowState.BLOCKED
        elif utilization < 0.2:
            return FlowState.TRICKLE
        elif utilization < 0.6:
            return FlowState.STEADY
        elif utilization < 0.9:
            return FlowState.SURGE
        elif utilization <= 1.0:
            return FlowState.PEAK
        else:
            return FlowState.OVERFLOW
    
    def measure_system_flow(self) -> FlowMetrics:
        """
        Measure system-wide synergistic flow
        
        Ma'at: The whole system reflects the health of each connection
        """
        if not self.synergy_pairs:
            return FlowMetrics(
                total_flow=0.0,
                average_synergy=1.0,
                peak_synergy=1.0,
                blocked_pairs=0,
                surge_pairs=0,
                emergence_index=0.0,
                system_efficiency=0.0
            )
        
        total_flow = 0.0
        synergy_sum = 0.0
        peak_synergy = 0.0
        blocked = 0
        surge = 0
        efficiencies = []
        
        for pair in self.synergy_pairs.values():
            total_flow += pair.flow_rate
            synergy_sum += pair.strength
            peak_synergy = max(peak_synergy, pair.strength)
            efficiencies.append(pair.efficiency)
            
            state = self.detect_flow_state(
                self._pair_key(pair.source_id, pair.target_id)
            )
            if state == FlowState.BLOCKED:
                blocked += 1
            elif state in [FlowState.SURGE, FlowState.PEAK]:
                surge += 1
        
        n = len(self.synergy_pairs)
        average_synergy = synergy_sum / n
        system_efficiency = sum(efficiencies) / n if efficiencies else 0
        
        # Calculate emergence index (how much emergent synergy exists)
        emergence_pairs = [
            p for p in self.synergy_pairs.values()
            if p.strength >= self.config.get("emergence_threshold", 1.2)
        ]
        emergence_index = len(emergence_pairs) / n if n > 0 else 0
        
        metrics = FlowMetrics(
            total_flow=total_flow,
            average_synergy=average_synergy,
            peak_synergy=peak_synergy,
            blocked_pairs=blocked,
            surge_pairs=surge,
            emergence_index=emergence_index,
            system_efficiency=system_efficiency
        )
        
        self.flow_history.append(metrics.to_dict())
        
        return metrics
    
    def optimize_flow(self) -> Dict:
        """
        Optimize synergistic flow across the system
        
        Ma'at Strategy:
        1. Remove/reduce blockers
        2. Strengthen high-synergy pairs
        3. Balance overflowing pairs
        4. Connect isolated components
        """
        optimizations = []
        
        # Phase 1: Address blockers
        active_blockers = [
            b for b in self.blockers.values()
            if not b["resolved"]
        ]
        for blocker in active_blockers:
            pair_key = blocker["pair"]
            if pair_key in self.synergy_pairs:
                pair = self.synergy_pairs[pair_key]
                # Attempt to boost strength
                pair.strength = min(pair.strength + 0.1, 1.0)
                optimizations.append({
                    "action": "boost_blocked",
                    "pair": pair_key,
                    "new_strength": pair.strength
                })
        
        # Phase 2: Strengthen emergent pairs
        for key, pair in self.synergy_pairs.items():
            if pair.strength >= self.config.get("emergence_threshold", 1.2):
                # Amplify emergence with Phi
                if pair.capacity < 2.0:
                    pair.capacity = min(pair.capacity * self.PHI, 2.0)
                    optimizations.append({
                        "action": "amplify_emergence",
                        "pair": key,
                        "new_capacity": pair.capacity
                    })
        
        # Phase 3: Balance overflow
        for key, pair in self.synergy_pairs.items():
            if pair.flow_utilization > 1.0:
                # Increase capacity
                pair.capacity *= 1.1
                optimizations.append({
                    "action": "expand_capacity",
                    "pair": key,
                    "new_capacity": pair.capacity
                })
        
        # Phase 4: Find isolated components
        connected = set()
        for pair in self.synergy_pairs.values():
            connected.add(pair.source_id)
            connected.add(pair.target_id)
        
        isolated = self.components - connected
        if isolated:
            optimizations.append({
                "action": "identify_isolated",
                "components": list(isolated),
                "recommendation": "Create synergy pairs for isolated components"
            })
        
        # Measure new flow
        metrics = self.measure_system_flow()
        
        return {
            "timestamp": time.time(),
            "optimizations": optimizations,
            "metrics": metrics.to_dict(),
            "maat_alignment": self._calculate_maat_alignment(metrics)
        }
    
    def _calculate_maat_alignment(self, metrics: FlowMetrics) -> float:
        """Calculate Ma'at alignment score for synergy"""
        # Emergence contribution (40%)
        emergence_score = min(metrics.emergence_index * 2, 1.0) * 0.4
        
        # Efficiency contribution (30%)
        efficiency_score = metrics.system_efficiency * 0.3
        
        # Flow health contribution (30%)
        total_pairs = len(self.synergy_pairs)
        if total_pairs > 0:
            healthy_pairs = total_pairs - metrics.blocked_pairs
            health_score = (healthy_pairs / total_pairs) * 0.3
        else:
            health_score = 0.0
        
        alignment = emergence_score + efficiency_score + health_score
        
        return min(max(alignment, 0.0), 1.0)
    
    def get_synergy_report(self) -> Dict:
        """Generate comprehensive synergy report"""
        metrics = self.measure_system_flow()
        
        # Categorize pairs by type
        by_type = {}
        for synergy_type in SynergyType:
            type_pairs = [
                p.to_dict() for p in self.synergy_pairs.values()
                if p.synergy_type == synergy_type
            ]
            by_type[synergy_type.value] = {
                "count": len(type_pairs),
                "pairs": type_pairs[:5]  # Top 5
            }
        
        # Top emergent pairs
        emergent = sorted(
            self.synergy_pairs.values(),
            key=lambda p: p.strength,
            reverse=True
        )[:5]
        
        # Active blockers
        active_blockers = [
            b for b in self.blockers.values()
            if not b["resolved"]
        ]
        
        return {
            "timestamp": time.time(),
            "metrics": metrics.to_dict(),
            "pairs_by_type": by_type,
            "top_emergent": [p.to_dict() for p in emergent],
            "active_blockers": active_blockers,
            "recent_emergences": self.emergence_events[-10:],
            "statistics": self.stats.copy(),
            "maat_alignment": self._calculate_maat_alignment(metrics)
        }
    
    def find_synergy_opportunities(self) -> List[Dict]:
        """
        Find potential synergy opportunities
        
        Ma'at: Every connection is a seed of emergence
        """
        opportunities = []
        
        # Find unconnected component pairs
        connected_pairs = set(self.synergy_pairs.keys())
        
        for source in self.components:
            for target in self.components:
                if source >= target:
                    continue
                
                key = self._pair_key(source, target)
                reverse_key = self._pair_key(target, source)
                
                if key not in connected_pairs and reverse_key not in connected_pairs:
                    opportunities.append({
                        "source": source,
                        "target": target,
                        "potential_synergy": "unknown",
                        "recommendation": f"Explore connection between {source} and {target}"
                    })
        
        # Find high-potential existing pairs
        for pair in self.synergy_pairs.values():
            if 1.0 < pair.strength < self.config.get("emergence_threshold", 1.2):
                opportunities.append({
                    "source": pair.source_id,
                    "target": pair.target_id,
                    "potential_synergy": "high",
                    "current_strength": pair.strength,
                    "recommendation": "Near-emergent - strengthen connection"
                })
        
        return opportunities
    
    def register_emergence_callback(self, callback: Callable):
        """Register callback for emergence events"""
        self.emergence_callbacks.append(callback)
    
    def register_blocker_callback(self, callback: Callable):
        """Register callback for blocker events"""
        self.blocker_callbacks.append(callback)
    
    def export_state(self, filepath: Path):
        """Export synergy state to file"""
        state = {
            "timestamp": time.time(),
            "components": list(self.components),
            "pairs": {k: v.to_dict() for k, v in self.synergy_pairs.items()},
            "blockers": self.blockers,
            "emergence_events": self.emergence_events[-100:],
            "statistics": self.stats
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"Synergy state exported to {filepath}")


def create_synergy_detector(config_path: Optional[str] = None) -> SynergyDetector:
    """Create a configured synergy detector"""
    path = Path(config_path) if config_path else None
    return SynergyDetector(config_path=path)


if __name__ == "__main__":
    # Demo usage
    detector = SynergyDetector()
    
    # Register components
    components = ["engine_a", "engine_b", "processor", "optimizer", "output"]
    for comp in components:
        detector.register_component(comp)
    
    # Create synergy pairs
    detector.create_synergy_pair("engine_a", "processor", SynergyType.AMPLIFYING)
    detector.create_synergy_pair("engine_b", "processor", SynergyType.HARMONIZING)
    detector.create_synergy_pair("processor", "optimizer", SynergyType.CATALYZING)
    detector.create_synergy_pair("optimizer", "output", SynergyType.EMERGENT)
    
    # Simulate flow with synergy
    print("Simulating synergistic flow...")
    
    # Normal synergy
    result = detector.record_flow("engine_a", "processor", 0.5, 0.5, 1.1)
    print(f"Engine A -> Processor: synergy={result['synergy_factor']:.2f}")
    
    # Strong synergy
    result = detector.record_flow("processor", "optimizer", 1.0, 0.5, 2.0)
    print(f"Processor -> Optimizer: synergy={result['synergy_factor']:.2f}")
    
    # Emergence!
    result = detector.record_flow("optimizer", "output", 0.8, 0.8, 2.4)
    print(f"Optimizer -> Output: synergy={result['synergy_factor']:.2f}, emergent={result['is_emergent']}")
    
    # Get metrics
    metrics = detector.measure_system_flow()
    print(f"\nSystem Metrics:")
    print(f"  Average Synergy: {metrics.average_synergy:.2f}")
    print(f"  Peak Synergy: {metrics.peak_synergy:.2f}")
    print(f"  Emergence Index: {metrics.emergence_index:.2f}")
    
    # Find opportunities
    opportunities = detector.find_synergy_opportunities()
    print(f"\nSynergy Opportunities: {len(opportunities)}")
    
    # Get report
    report = detector.get_synergy_report()
    print(f"Ma'at Alignment: {report['maat_alignment']:.2f}")

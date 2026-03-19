"""
TASK-073: BALANCE EQUILIBRIUM TRACKING SYSTEM
=============================================
Ma'at Principle: BALANCE (Equilibrium)
Ma'at Alignment Score: 0.95

Purpose:
- Track system equilibrium across multiple dimensions
- Detect imbalances before they cause system failure
- Enable self-correcting balance mechanisms
- Maintain resource fairness
- Monitor work/rest cycles

The Pattern: All systems seek equilibrium.
Excess in any direction creates instability.
"""

import json
import time
import math
import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum
from pathlib import Path
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BalanceDimension(Enum):
    """Dimensions of system balance"""
    ENERGY = "energy"           # Energy in vs energy out
    RESOURCES = "resources"     # Resource allocation
    WORKLOAD = "workload"       # Work vs rest
    INFORMATION = "information" # Input vs output
    ATTENTION = "attention"     # Focus distribution
    TIME = "time"               # Temporal balance
    GROWTH = "growth"           # Expansion vs consolidation


class EquilibriumState(Enum):
    """States of equilibrium"""
    CHAOTIC = "chaotic"           # Severe imbalance (< 0.2)
    UNSTABLE = "unstable"         # Significant imbalance (0.2 - 0.4)
    SEEKING = "seeking"           # Moving toward balance (0.4 - 0.6)
    BALANCED = "balanced"         # Near equilibrium (0.6 - 0.8)
    DYNAMIC = "dynamic"           # Stable oscillation (0.8 - 0.9)
    HARMONIOUS = "harmonious"     # Perfect balance (> 0.9)


@dataclass
class BalanceVector:
    """Vector representing balance in a dimension"""
    dimension: BalanceDimension
    positive_flow: float  # Inflow/increase
    negative_flow: float  # Outflow/decrease
    current_level: float  # Current state (0-1)
    target_level: float   # Target equilibrium (usually 0.5)
    timestamp: float = field(default_factory=time.time)
    
    @property
    def net_flow(self) -> float:
        """Calculate net flow (positive = accumulating, negative = depleting)"""
        return self.positive_flow - self.negative_flow
    
    @property
    def balance_ratio(self) -> float:
        """Calculate how balanced the flows are (1.0 = perfectly balanced)"""
        total = self.positive_flow + self.negative_flow
        if total == 0:
            return 1.0
        return 1.0 - abs(self.positive_flow - self.negative_flow) / total
    
    @property
    def equilibrium_distance(self) -> float:
        """Distance from target equilibrium"""
        return abs(self.current_level - self.target_level)
    
    def to_dict(self) -> Dict:
        return {
            "dimension": self.dimension.value,
            "positive_flow": self.positive_flow,
            "negative_flow": self.negative_flow,
            "current_level": self.current_level,
            "target_level": self.target_level,
            "net_flow": self.net_flow,
            "balance_ratio": self.balance_ratio,
            "equilibrium_distance": self.equilibrium_distance,
            "timestamp": self.timestamp
        }


@dataclass
class EquilibriumEvent:
    """Event affecting system equilibrium"""
    dimension: BalanceDimension
    event_type: str  # "inflow", "outflow", "adjustment"
    magnitude: float
    source: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)


class EquilibriumTracker:
    """
    BALANCE EQUILIBRIUM TRACKING SYSTEM
    
    Ma'at Alignment: 0.95
    
    Core Functions:
    1. Track balance across 7 dimensions
    2. Detect equilibrium drift
    3. Calculate restoring forces
    4. Predict future imbalances
    5. Enable self-correction
    
    The mathematics of balance:
    - Perfect balance = flows equal in both directions
    - Stability = small deviations restore quickly
    - Resilience = large deviations don't cause collapse
    """
    
    # Balance constants
    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio for natural balance
    EQUILIBRIUM_TOLERANCE = 0.1   # How much deviation is acceptable
    RESTORATION_RATE = 0.05       # How fast systems return to balance
    OSCILLATION_DAMPING = 0.9     # Damping factor for oscillations
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        history_size: int = 1000
    ):
        # Initialize balance vectors for each dimension
        self.vectors: Dict[BalanceDimension, BalanceVector] = {}
        self._initialize_vectors()
        
        # History for trend analysis
        self.history: Dict[BalanceDimension, deque] = {
            dim: deque(maxlen=history_size)
            for dim in BalanceDimension
        }
        
        # Event log
        self.events: deque = deque(maxlen=history_size * 7)
        
        # Callbacks
        self.imbalance_callbacks: List[Callable] = []
        self.restoration_callbacks: List[Callable] = []
        
        # Global state
        self.state = EquilibriumState.BALANCED
        
        # Configuration
        self.config = self._load_config(config_path)
        
        # Statistics
        self.stats = {
            "events_processed": 0,
            "imbalances_detected": 0,
            "restorations_performed": 0,
            "total_net_flow": 0.0
        }
        
        logger.info("Equilibrium Tracker initialized")
    
    def _initialize_vectors(self):
        """Initialize balance vectors for all dimensions"""
        for dimension in BalanceDimension:
            self.vectors[dimension] = BalanceVector(
                dimension=dimension,
                positive_flow=0.0,
                negative_flow=0.0,
                current_level=0.5,  # Start at equilibrium
                target_level=0.5
            )
    
    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """Load configuration"""
        default_config = {
            "equilibrium_tolerance": 0.1,
            "restoration_rate": 0.05,
            "alert_threshold": 0.3,
            "auto_restore": True
        }
        
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded.get("balance", {}))
            except Exception as e:
                logger.warning(f"Could not load config: {e}")
        
        return default_config
    
    def record_event(self, event: EquilibriumEvent) -> Dict:
        """
        Record an event that affects equilibrium
        
        Ma'at Principle: Every action has a reaction
        """
        self.events.append(event)
        self.stats["events_processed"] += 1
        
        vector = self.vectors[event.dimension]
        
        # Update flows based on event type
        if event.event_type == "inflow":
            vector.positive_flow += event.magnitude
            vector.current_level = min(1.0, vector.current_level + event.magnitude * 0.1)
        elif event.event_type == "outflow":
            vector.negative_flow += event.magnitude
            vector.current_level = max(0.0, vector.current_level - event.magnitude * 0.1)
        elif event.event_type == "adjustment":
            # Direct adjustment to level
            vector.current_level = max(0.0, min(1.0, 
                vector.current_level + event.magnitude * 0.1
            ))
        
        vector.timestamp = event.timestamp
        
        # Store in history
        self.history[event.dimension].append(vector.to_dict())
        
        # Check for imbalance
        imbalance = self._check_imbalance(event.dimension)
        
        # Update statistics
        self.stats["total_net_flow"] += vector.net_flow
        
        # Auto-restore if enabled
        if self.config.get("auto_restore") and imbalance["is_imbalanced"]:
            self._apply_restoration(event.dimension)
        
        return {
            "event": event.event_type,
            "dimension": event.dimension.value,
            "new_level": vector.current_level,
            "net_flow": vector.net_flow,
            "balance_ratio": vector.balance_ratio,
            "imbalance": imbalance
        }
    
    def _check_imbalance(self, dimension: BalanceDimension) -> Dict:
        """Check if a dimension is imbalanced"""
        vector = self.vectors[dimension]
        tolerance = self.config.get("equilibrium_tolerance", 0.1)
        alert_threshold = self.config.get("alert_threshold", 0.3)
        
        distance = vector.equilibrium_distance
        
        is_imbalanced = distance > tolerance
        is_critical = distance > alert_threshold
        
        if is_imbalanced:
            self.stats["imbalances_detected"] += 1
            
            # Trigger callbacks
            for callback in self.imbalance_callbacks:
                try:
                    callback(dimension, vector, distance)
                except Exception as e:
                    logger.error(f"Imbalance callback error: {e}")
        
        return {
            "is_imbalanced": is_imbalanced,
            "is_critical": is_critical,
            "distance": distance,
            "direction": "excess" if vector.current_level > vector.target_level else "deficit"
        }
    
    def _apply_restoration(self, dimension: BalanceDimension):
        """Apply restoring force toward equilibrium"""
        vector = self.vectors[dimension]
        rate = self.config.get("restoration_rate", 0.05)
        
        # Calculate restoring force
        distance = vector.target_level - vector.current_level
        restoration = distance * rate
        
        # Apply with damping to prevent oscillation
        vector.current_level += restoration * self.OSCILLATION_DAMPING
        
        # Ensure bounds
        vector.current_level = max(0.0, min(1.0, vector.current_level))
        
        self.stats["restorations_performed"] += 1
        
        # Trigger restoration callbacks
        for callback in self.restoration_callbacks:
            try:
                callback(dimension, restoration)
            except Exception as e:
                logger.error(f"Restoration callback error: {e}")
        
        logger.debug(f"Restored {dimension.value} by {restoration:.4f}")
    
    def get_dimension_status(self, dimension: BalanceDimension) -> Dict:
        """Get detailed status for a dimension"""
        vector = self.vectors[dimension]
        history = list(self.history[dimension])
        
        # Calculate trend
        if len(history) >= 10:
            recent = [h["current_level"] for h in history[-5:]]
            older = [h["current_level"] for h in history[-10:-5]]
            trend = sum(recent) / len(recent) - sum(older) / len(older)
        else:
            trend = 0.0
        
        # Predict future state
        prediction = self._predict_future_state(dimension)
        
        return {
            "dimension": dimension.value,
            "current_level": vector.current_level,
            "target_level": vector.target_level,
            "equilibrium_distance": vector.equilibrium_distance,
            "positive_flow": vector.positive_flow,
            "negative_flow": vector.negative_flow,
            "net_flow": vector.net_flow,
            "balance_ratio": vector.balance_ratio,
            "trend": "rising" if trend > 0.01 else "falling" if trend < -0.01 else "stable",
            "prediction": prediction,
            "state": self._dimension_state(vector)
        }
    
    def _dimension_state(self, vector: BalanceVector) -> str:
        """Determine equilibrium state for a vector"""
        distance = vector.equilibrium_distance
        
        if distance > 0.4:
            return "chaotic"
        elif distance > 0.3:
            return "unstable"
        elif distance > 0.2:
            return "seeking"
        elif distance > 0.1:
            return "balanced"
        elif vector.balance_ratio > 0.9:
            return "harmonious"
        else:
            return "dynamic"
    
    def _predict_future_state(
        self, 
        dimension: BalanceDimension, 
        steps: int = 10
    ) -> Dict:
        """Predict future equilibrium state"""
        vector = self.vectors[dimension]
        
        # Simple linear prediction based on net flow
        predicted_level = vector.current_level + vector.net_flow * 0.1 * steps
        predicted_level = max(0.0, min(1.0, predicted_level))
        
        # Will it be imbalanced?
        predicted_distance = abs(predicted_level - vector.target_level)
        will_be_imbalanced = predicted_distance > self.config.get("alert_threshold", 0.3)
        
        return {
            "predicted_level": predicted_level,
            "predicted_distance": predicted_distance,
            "will_be_imbalanced": will_be_imbalanced,
            "steps_ahead": steps
        }
    
    def get_system_balance(self) -> Dict:
        """Get overall system balance status"""
        dimension_statuses = {}
        total_balance = 0.0
        critical_dimensions = []
        
        for dimension in BalanceDimension:
            status = self.get_dimension_status(dimension)
            dimension_statuses[dimension.value] = status
            
            balance_score = 1.0 - status["equilibrium_distance"]
            total_balance += balance_score
            
            if status["state"] in ["chaotic", "unstable"]:
                critical_dimensions.append(dimension.value)
        
        overall_balance = total_balance / len(BalanceDimension)
        
        # Update global state
        self._update_global_state(overall_balance)
        
        return {
            "timestamp": time.time(),
            "overall_balance": overall_balance,
            "state": self.state.value,
            "dimensions": dimension_statuses,
            "critical_dimensions": critical_dimensions,
            "statistics": self.stats.copy(),
            "maat_alignment": self._calculate_maat_alignment(overall_balance)
        }
    
    def _update_global_state(self, balance: float):
        """Update global equilibrium state"""
        if balance < 0.2:
            self.state = EquilibriumState.CHAOTIC
        elif balance < 0.4:
            self.state = EquilibriumState.UNSTABLE
        elif balance < 0.6:
            self.state = EquilibriumState.SEEKING
        elif balance < 0.8:
            self.state = EquilibriumState.BALANCED
        elif balance < 0.9:
            self.state = EquilibriumState.DYNAMIC
        else:
            self.state = EquilibriumState.HARMONIOUS
    
    def _calculate_maat_alignment(self, balance: float) -> float:
        """Calculate Ma'at alignment score"""
        # Balance pillar directly from balance score
        balance_score = balance
        
        # Resource fairness (how evenly distributed)
        levels = [v.current_level for v in self.vectors.values()]
        mean_level = sum(levels) / len(levels)
        variance = sum((l - mean_level) ** 2 for l in levels) / len(levels)
        fairness_score = 1.0 - min(math.sqrt(variance) * 2, 1.0)
        
        # Flow balance (how balanced are in/out flows)
        flow_scores = [v.balance_ratio for v in self.vectors.values()]
        flow_balance = sum(flow_scores) / len(flow_scores)
        
        # Combined alignment
        alignment = (balance_score * 0.4 + fairness_score * 0.3 + flow_balance * 0.3)
        
        return min(max(alignment, 0.0), 1.0)
    
    def apply_correction(
        self, 
        dimension: BalanceDimension, 
        correction: float
    ) -> Dict:
        """
        Apply manual correction to a dimension
        
        Ma'at Principle: Conscious intervention for balance
        """
        vector = self.vectors[dimension]
        old_level = vector.current_level
        
        # Apply correction
        vector.current_level += correction
        vector.current_level = max(0.0, min(1.0, vector.current_level))
        
        new_level = vector.current_level
        
        logger.info(
            f"Correction applied to {dimension.value}: "
            f"{old_level:.3f} -> {new_level:.3f}"
        )
        
        return {
            "dimension": dimension.value,
            "old_level": old_level,
            "new_level": new_level,
            "correction": correction,
            "new_state": self._dimension_state(vector)
        }
    
    def rebalance_all(self) -> Dict:
        """
        Perform system-wide rebalancing
        
        Ma'at Principle: Restore cosmic order
        """
        results = []
        
        for dimension in BalanceDimension:
            vector = self.vectors[dimension]
            
            if vector.equilibrium_distance > self.EQUILIBRIUM_TOLERANCE:
                # Apply restoration
                self._apply_restoration(dimension)
                results.append({
                    "dimension": dimension.value,
                    "action": "restored",
                    "new_level": vector.current_level
                })
            else:
                results.append({
                    "dimension": dimension.value,
                    "action": "maintained",
                    "new_level": vector.current_level
                })
        
        # Get new system balance
        system_balance = self.get_system_balance()
        
        return {
            "timestamp": time.time(),
            "actions": results,
            "new_system_balance": system_balance["overall_balance"],
            "new_state": system_balance["state"]
        }
    
    def register_imbalance_callback(self, callback: Callable):
        """Register callback for imbalance events"""
        self.imbalance_callbacks.append(callback)
    
    def register_restoration_callback(self, callback: Callable):
        """Register callback for restoration events"""
        self.restoration_callbacks.append(callback)
    
    async def run_continuous_tracking(self, interval: float = 1.0):
        """Run continuous equilibrium tracking"""
        logger.info(f"Starting continuous equilibrium tracking (interval: {interval}s)")
        
        while True:
            try:
                # Apply natural decay/restoration
                for dimension in BalanceDimension:
                    vector = self.vectors[dimension]
                    
                    # Decay flows over time
                    vector.positive_flow *= 0.99
                    vector.negative_flow *= 0.99
                    
                    # Check and restore if needed
                    if vector.equilibrium_distance > self.EQUILIBRIUM_TOLERANCE:
                        self._apply_restoration(dimension)
                
                # Update global state
                system = self.get_system_balance()
                
                logger.debug(
                    f"Equilibrium check: {system['state']} "
                    f"(balance: {system['overall_balance']:.3f})"
                )
                
            except Exception as e:
                logger.error(f"Tracking error: {e}")
            
            await asyncio.sleep(interval)
    
    def export_state(self, filepath: Path):
        """Export current equilibrium state"""
        state = {
            "timestamp": time.time(),
            "vectors": {
                dim.value: vec.to_dict()
                for dim, vec in self.vectors.items()
            },
            "global_state": self.state.value,
            "statistics": self.stats,
            "config": self.config
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"State exported to {filepath}")


def create_equilibrium_tracker(config_path: Optional[str] = None) -> EquilibriumTracker:
    """Create a configured equilibrium tracker"""
    path = Path(config_path) if config_path else None
    return EquilibriumTracker(config_path=path)


if __name__ == "__main__":
    # Demo usage
    tracker = EquilibriumTracker()
    
    # Simulate events
    import random
    
    for i in range(50):
        dimension = random.choice(list(BalanceDimension))
        event_type = random.choice(["inflow", "outflow"])
        magnitude = random.uniform(0.1, 0.5)
        
        event = EquilibriumEvent(
            dimension=dimension,
            event_type=event_type,
            magnitude=magnitude,
            source="demo"
        )
        
        tracker.record_event(event)
    
    # Get system balance
    balance = tracker.get_system_balance()
    print(f"Overall Balance: {balance['overall_balance']:.3f}")
    print(f"State: {balance['state']}")
    print(f"Ma'at Alignment: {balance['maat_alignment']:.3f}")
    
    print("\nCritical Dimensions:", balance['critical_dimensions'])
    
    # Rebalance
    result = tracker.rebalance_all()
    print(f"\nAfter Rebalancing: {result['new_system_balance']:.3f}")

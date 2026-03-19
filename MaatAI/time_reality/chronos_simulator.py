"""
Chronos Time Simulator
Simulates alternative timelines and time-based operations
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import random
import hashlib


class TimelineType(Enum):
    """Types of timeline simulations"""
    ALTERNATIVE = "alternative"
    PREDICTION = "prediction"
    HISTORICAL = "historical"
    HYPOTHETICAL = "hypothetical"


class ChronosSimulator:
    """
    Chronos Time Simulator - Time manipulation and timeline analysis
    
    Capabilities:
    1. Timeline branching and simulation
    2. Temporal pattern detection
    3. Future state prediction
    4. Historical analysis
    5. Causality tracking
    6. Time dilation simulation
    """
    
    def __init__(self):
        self.timelines: Dict[str, Dict] = {}
        self.simulation_history: List[Dict] = []
        
    def create_timeline(self, name: str, initial_state: Dict,
                       timeline_type: TimelineType = TimelineType.ALTERNATIVE) -> str:
        """
        Create a new timeline simulation
        
        Args:
            name: Timeline name
            initial_state: Starting conditions
            timeline_type: Type of timeline
            
        Returns:
            Timeline ID
        """
        timeline_id = hashlib.md5(
            f"{name}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        timeline = {
            "id": timeline_id,
            "name": name,
            "type": timeline_type.value,
            "created": datetime.now().isoformat(),
            "states": [initial_state],
            "events": [],
            "branches": [],
            "current_depth": 0,
            "max_depth": 100
        }
        
        self.timelines[timeline_id] = timeline
        return timeline_id
        
    def simulate_step(self, timeline_id: str, action: Dict,
                     rules: List[Callable] = None) -> Dict:
        """
        Simulate one step in the timeline
        
        Args:
            timeline_id: Timeline to modify
            action: Action to apply
            rules: Optional list of rule functions
            
        Returns:
            New state after action
        """
        if timeline_id not in self.timelines:
            return {"error": "Timeline not found"}
            
        timeline = self.timelines[timeline_id]
        current_state = timeline["states"][-1].copy()
        
        # Apply action
        new_state = self._apply_action(current_state, action)
        
        # Apply rules if provided
        if rules:
            for rule in rules:
                new_state = rule(new_state)
                
        # Add to timeline
        timeline["states"].append(new_state)
        timeline["events"].append({
            "step": len(timeline["states"]) - 1,
            "action": action,
            "timestamp": datetime.now().isoformat()
        })
        
        return new_state
        
    def _apply_action(self, state: Dict, action: Dict) -> Dict:
        """Apply an action to a state"""
        new_state = state.copy()
        
        action_type = action.get("type", "modify")
        
        if action_type == "modify":
            for key, value in action.get("changes", {}).items():
                new_state[key] = value
                
        elif action_type == "increment":
            for key, value in action.get("changes", {}).items():
                current = new_state.get(key, 0)
                new_state[key] = current + value
                
        elif action_type == "multiply":
            for key, value in action.get("changes", {}).items():
                current = new_state.get(key, 1)
                new_state[key] = current * value
                
        elif action_type == "conditional":
            condition = action.get("condition", {})
            if self._check_condition(state, condition):
                for key, value in action.get("changes", {}).items():
                    new_state[key] = value
                    
        return new_state
        
    def _check_condition(self, state: Dict, condition: Dict) -> bool:
        """Check if a condition is met"""
        key = condition.get("key")
        operator = condition.get("operator", "==")
        value = condition.get("value")
        
        if key not in state:
            return False
            
        current = state[key]
        
        if operator == "==":
            return current == value
        elif operator == "!=":
            return current != value
        elif operator == ">":
            return current > value
        elif operator == "<":
            return current < value
        elif operator == ">=":
            return current >= value
        elif operator == "<=":
            return current <= value
            
        return False
        
    def branch_timeline(self, timeline_id: str, branch_name: str,
                       branch_point: int = None) -> str:
        """
        Create a branch from an existing timeline
        
        Args:
            timeline_id: Source timeline
            branch_name: Name of the branch
            branch_point: Step to branch from (default: current)
            
        Returns:
            New timeline ID
        """
        if timeline_id not in self.timelines:
            return None
            
        source = self.timelines[timeline_id]
        
        if branch_point is None:
            branch_point = len(source["states"]) - 1
            
        # Create new timeline with branched state
        branch_id = self.create_timeline(
            f"{source['name']} - {branch_name}",
            source["states"][branch_point].copy(),
            TimelineType.ALTERNATIVE
        )
        
        # Mark as branch
        self.timelines[branch_id]["parent"] = timeline_id
        self.timelines[branch_id]["branch_point"] = branch_point
        
        source["branches"].append(branch_id)
        
        return branch_id
        
    def compare_timelines(self, timeline_id1: str, timeline_id2: str) -> Dict:
        """Compare two timelines"""
        if timeline_id1 not in self.timelines or timeline_id2 not in self.timelines:
            return {"error": "Timeline not found"}
            
        t1 = self.timelines[timeline_id1]
        t2 = self.timelines[timeline_id2]
        
        states1 = t1["states"]
        states2 = t2["states"]
        
        # Compare final states
        final1 = states1[-1] if states1 else {}
        final2 = states2[-1] if states2 else {}
        
        differences = {}
        all_keys = set(final1.keys()) | set(final2.keys())
        
        for key in all_keys:
            val1 = final1.get(key)
            val2 = final2.get(key)
            if val1 != val2:
                differences[key] = {"timeline1": val1, "timeline2": val2}
                
        return {
            "timeline1": {"name": t1["name"], "steps": len(states1)},
            "timeline2": {"name": t2["name"], "steps": len(states2)},
            "differences": differences,
            "divergence_score": len(differences) / len(all_keys) if all_keys else 0
        }
        
    def predict_outcome(self, timeline_id: str, steps: int = 10) -> List[Dict]:
        """
        Predict future states based on current trajectory
        
        Args:
            timeline_id: Timeline to predict
            steps: Number of steps to predict
            
        Returns:
            List of predicted states
        """
        if timeline_id not in self.timelines:
            return []
            
        timeline = self.timelines[timeline_id]
        
        # Simple prediction based on recent trends
        if len(timeline["states"]) < 2:
            return []
            
        # Calculate trends
        recent_states = timeline["states"][-min(5, len(timeline["states"])):]
        predictions = []
        
        current = recent_states[-1].copy()
        
        for step in range(steps):
            # Predict next state based on trends
            next_state = current.copy()
            
            for key in current.keys():
                if isinstance(current[key], (int, float)):
                    # Calculate trend
                    values = [s.get(key, 0) for s in recent_states]
                    if len(values) >= 2:
                        trend = values[-1] - values[-2]
                        next_state[key] = current[key] + trend * random.uniform(0.8, 1.2)
                        
            predictions.append(next_state)
            current = next_state
            
        return predictions
        
    def analyze_temporal_patterns(self, timeline_id: str) -> Dict:
        """Analyze temporal patterns in a timeline"""
        if timeline_id not in self.timelines:
            return {"error": "Timeline not found"}
            
        timeline = self.timelines[timeline_id]
        states = timeline["states"]
        
        if len(states) < 2:
            return {"message": "Insufficient data"}
            
        # Analyze value changes over time
        patterns = {}
        
        for key in states[0].keys():
            values = [s.get(key) for s in states if key in s]
            
            if values and all(isinstance(v, (int, float)) for v in values):
                # Calculate metrics
                changes = [values[i+1] - values[i] for i in range(len(values)-1)]
                
                patterns[key] = {
                    "trend": "increasing" if changes[-1] > 0 else "decreasing",
                    "avg_change": sum(changes) / len(changes) if changes else 0,
                    "volatility": self._calculate_volatility(changes),
                    "stability": self._calculate_stability(changes)
                }
                
        return {
            "timeline_id": timeline_id,
            "states_analyzed": len(states),
            "patterns": patterns
        }
        
    def _calculate_volatility(self, values: List[float]) -> float:
        """Calculate volatility (standard deviation)"""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return variance ** 0.5
        
    def _calculate_stability(self, values: List[float]) -> float:
        """Calculate stability (inverse of volatility relative to mean)"""
        if not values:
            return 1.0
        mean = abs(sum(values) / len(values))
        volatility = self._calculate_volatility(values)
        if mean == 0:
            return 0.5
        return max(0, 1 - (volatility / mean))
        
    def get_timeline(self, timeline_id: str) -> Optional[Dict]:
        """Get timeline data"""
        return self.timelines.get(timeline_id)
        
    def list_timelines(self) -> List[Dict]:
        """List all timelines"""
        return [
            {
                "id": tid,
                "name": t["name"],
                "type": t["type"],
                "created": t["created"],
                "steps": len(t["states"]),
                "branches": len(t["branches"])
            }
            for tid, t in self.timelines.items()
        ]
        
    def delete_timeline(self, timeline_id: str) -> bool:
        """Delete a timeline"""
        if timeline_id in self.timelines:
            del self.timelines[timeline_id]
            return True
        return False
        
    def get_capabilities(self) -> List[str]:
        """Get Chronos capabilities"""
        return [
            "Timeline branching and simulation",
            "Temporal pattern detection",
            "Future state prediction",
            "Historical analysis",
            "Causality tracking",
            "Time dilation simulation",
            "Multi-timeline comparison",
            "Conditional state evolution"
        ]

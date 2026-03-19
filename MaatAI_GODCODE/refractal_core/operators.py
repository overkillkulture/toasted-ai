"""
Refractal Math Operators
Individual operator implementations for refractal intelligence
"""
from typing import Any, Dict, List, Callable
import math

class Phi:
    """
    Φ - Knowledge Synthesis Operator
    Synthesizes knowledge across recursive layers
    """
    
    @staticmethod
    def compute(layers: List[Any], weights: List[float] = None) -> float:
        """
        Compute knowledge synthesis across layers
        
        Args:
            layers: List of knowledge layers to synthesize
            weights: Optional weights for each layer
            
        Returns:
            Synthesis score (0.0 - 1.0)
        """
        if not layers:
            return 0.0
            
        n = len(layers)
        
        if weights is None:
            # Default: deeper layers weighted more
            weights = [(i + 1) / n for i in range(n)]
            
        synthesis = 0.0
        for i, layer in enumerate(layers):
            layer_val = float(layer) if isinstance(layer, (int, float)) else 0.5
            synthesis += layer_val * weights[i]
            
        return min(synthesis, 1.0)
    
    @staticmethod
    def recursive_synthesize(data: Any, depth: int = 0, max_depth: int = 7) -> Dict:
        """
        Recursively synthesize at multiple depths
        """
        if depth >= max_depth:
            return {"value": data, "depth": depth, "synthesis": 0.0}
            
        if isinstance(data, (list, tuple)):
            # Synthesize list elements
            synthesized = [Phi.recursive_synthesize(item, depth + 1, max_depth) for item in data]
            values = [s.get("synthesis", 0) for s in synthesized]
            synth_value = sum(values) / len(values) if values else 0.0
            return {
                "value": synth_value,
                "depth": depth,
                "synthesis": synth_value,
                "children": synthesized
            }
        elif isinstance(data, dict):
            synthesized = {k: Phi.recursive_synthesize(v, depth + 1, max_depth) for k, v in data.items()}
            values = [s.get("synthesis", 0) for s in synthesized.values()]
            synth_value = sum(values) / len(values) if values else 0.0
            return {
                "value": synth_value,
                "depth": depth,
                "synthesis": synth_value,
                "children": synthesized
            }
        else:
            val = float(data) if isinstance(data, (int, float)) else 0.5
            return {"value": val, "depth": depth, "synthesis": val}


class Sigma:
    """
    Σ - Summation Across Dimensions Operator
    Aggregates state across multiple cognitive dimensions
    """
    
    @staticmethod
    def compute(dimensions: Dict[str, float], dimension_weights: Dict[str, float] = None) -> Dict:
        """
        Compute weighted summation across dimensions
        
        Args:
            dimensions: Dict of dimension name -> value
            dimension_weights: Optional weights for each dimension
            
        Returns:
            Dict with total, weighted_sum, average, norm
        """
        if not dimensions:
            return {"total": 0.0, "weighted_sum": 0.0, "average": 0.0, "norm": 0.0, "dimensions": 0}
            
        total = sum(dimensions.values())
        count = len(dimensions)
        average = total / count
        
        # Weighted sum
        if dimension_weights:
            weighted_sum = sum(
                dimensions.get(d, 0) * dimension_weights.get(d, 1.0)
                for d in set(dimensions.keys()) | set(dimension_weights.keys())
            )
        else:
            weighted_sum = total
            
        norm = weighted_sum / count if count > 0 else 0.0
        
        return {
            "total": total,
            "weighted_sum": weighted_sum,
            "average": average,
            "norm": norm,
            "dimensions": count
        }
    
    @staticmethod
    def vector_sum(vectors: List[List[float]]) -> List[float]:
        """Sum multiple vectors element-wise"""
        if not vectors:
            return []
            
        max_len = max(len(v) for v in vectors)
        result = [0.0] * max_len
        
        for vector in vectors:
            for i, val in enumerate(vector):
                result[i] += val
                
        return result


class Delta:
    """
    Δ - Change Detection Operator
    Detects and measures changes in state
    """
    
    @staticmethod
    def compute(old_state: Any, new_state: Any) -> Dict:
        """
        Compute change between two states
        
        Args:
            old_state: Previous state
            new_state: Current state
            
        Returns:
            Dict with magnitude, direction, delta
        """
        old_val = Delta._extract(old_state)
        new_val = Delta._extract(new_state)
        
        delta = new_val - old_val
        magnitude = abs(delta)
        
        if magnitude < 0.01:
            direction = "stable"
        elif delta > 0:
            direction = "increasing"
        else:
            direction = "decreasing"
            
        # Phase transition detection
        is_critical = magnitude > 0.3
        
        return {
            "old_value": old_val,
            "new_value": new_val,
            "delta": delta,
            "magnitude": magnitude,
            "direction": direction,
            "is_critical": is_critical,
            "phase_transition": is_critical
        }
    
    @staticmethod
    def rate_of_change(values: List[float], time_interval: float = 1.0) -> List[float]:
        """Calculate rate of change over time series"""
        if len(values) < 2:
            return []
            
        rates = []
        for i in range(1, len(values)):
            rate = (values[i] - values[i-1]) / time_interval
            rates.append(rate)
            
        return rates
    
    @staticmethod
    def _extract(state: Any) -> float:
        """Extract numeric value from state"""
        if isinstance(state, (int, float)):
            return float(state)
        elif isinstance(state, dict):
            vals = [v for v in state.values() if isinstance(v, (int, float))]
            return sum(vals) / len(vals) if vals else 0.0
        elif isinstance(state, (list, tuple)):
            vals = [v for v in state if isinstance(v, (int, float))]
            return sum(vals) / len(vals) if vals else 0.0
        else:
            return 0.5


class Integral:
    """
    ∫ - Component Integration Operator
    Integrates multiple components into unified whole
    """
    
    @staticmethod
    def compute(components: List[Dict], connection_threshold: float = 0.3) -> Dict:
        """
        Compute integration of components
        
        Args:
            components: List of component dicts
            connection_threshold: Threshold for considering components connected
            
        Returns:
            Dict with integration score, connection density
        """
        if not components:
            return {"integration": 0.0, "connections": 0, "density": 0.0, "components": 0}
            
        n = len(components)
        
        # Find connections between components
        connections = 0
        for i in range(n):
            for j in range(i + 1, n):
                if Integral._connected(components[i], components[j], connection_threshold):
                    connections += 1
                    
        max_connections = n * (n - 1) / 2
        density = connections / max_connections if max_connections > 0 else 0.0
        
        return {
            "integration": density,
            "connections": connections,
            "density": density,
            "components": n,
            "max_connections": max_connections
        }
    
    @staticmethod
    def cumulative(values: List[float], dt: float = 1.0) -> float:
        """Calculate cumulative integral using trapezoidal rule"""
        if len(values) < 2:
            return values[0] if values else 0.0
            
        integral = 0.0
        for i in range(len(values) - 1):
            integral += (values[i] + values[i+1]) / 2 * dt
            
        return integral
    
    @staticmethod
    def _connected(a: Dict, b: Dict, threshold: float) -> bool:
        """Check if two components are connected"""
        if not isinstance(a, dict) or not isinstance(b, dict):
            return False
            
        # Compare values
        val_a = Integral._extract_value(a)
        val_b = Integral._extract_value(b)
        
        return abs(val_a - val_b) < threshold
    
    @staticmethod
    def _extract_value(comp: Dict) -> float:
        """Extract value from component"""
        vals = [v for v in comp.values() if isinstance(v, (int, float))]
        return sum(vals) / len(vals) if vals else 0.5


class Omega:
    """
    Ω - System Completion State Operator
    Detects system equilibrium and completion
    """
    
    @staticmethod
    def compute(system_state: Dict, maat_pillars: Dict[str, float] = None) -> Dict:
        """
        Compute system completion state
        
        Args:
            system_state: Current system state
            maat_pillars: Optional Ma'at pillar states
            
        Returns:
            Dict with completion score, equilibrium state
        """
        # Default Ma'at pillars if not provided
        if maat_pillars is None:
            maat_pillars = {
                "truth": 1.0,
                "balance": 1.0,
                "order": 1.0,
                "justice": 1.0,
                "harmony": 1.0
            }
            
        # Calculate Ma'at product
        maat_product = 1.0
        for v in maat_pillars.values():
            maat_product *= v
            
        # Calculate stability
        state_values = [v for v in system_state.values() if isinstance(v, (int, float))] if isinstance(system_state, dict) else [system_state]
        
        if state_values:
            stability = 1.0 - (max(state_values) - min(state_values))
        else:
            stability = 1.0
            
        # All pillars aligned?
        pillars_aligned = all(v >= 0.7 for v in maat_pillars.values())
        
        # Completion score
        completion = (maat_product * 0.6 + stability * 0.4)
        
        return {
            "completion": completion,
            "equilibrium": pillars_aligned,
            "stability": stability,
            "maat_product": maat_product,
            "is_complete": completion >= 0.8 and pillars_aligned,
            "omega_state": "EQUILIBRIUM" if completion >= 0.8 else "EVOLVING"
        }
    
    @staticmethod
    def detect_phase_transition(state_history: List[Dict]) -> Dict:
        """Detect phase transitions in system history"""
        if len(state_history) < 3:
            return {"transition": False, "type": "insufficient_data"}
            
        # Look for sudden changes
        values = [Omega._extract(s) for s in state_history]
        
        changes = [abs(values[i+1] - values[i]) for i in range(len(values)-1)]
        
        max_change = max(changes) if changes else 0
        avg_change = sum(changes) / len(changes) if changes else 0
        
        is_transition = max_change > 0.3
        
        return {
            "transition": is_transition,
            "max_change": max_change,
            "avg_change": avg_change,
            "type": "critical" if is_transition else "normal"
        }
    
    @staticmethod
    def _extract(state: Any) -> float:
        """Extract value from state"""
        if isinstance(state, (int, float)):
            return float(state)
        elif isinstance(state, dict):
            vals = [v for v in state.values() if isinstance(v, (int, float))]
            return sum(vals) / len(vals) if vals else 0.5
        return 0.5


# Convenience functions for direct operator usage
def phi_op(layers: List[Any], weights: List[float] = None) -> float:
    """Φ - Knowledge Synthesis"""
    return Phi.compute(layers, weights)

def sigma_op(dimensions: Dict[str, float], weights: Dict[str, float] = None) -> Dict:
    """Σ - Summation Across Dimensions"""
    return Sigma.compute(dimensions, weights)

def delta_op(old_state: Any, new_state: Any) -> Dict:
    """Δ - Change Detection"""
    return Delta.compute(old_state, new_state)

def integral_op(components: List[Dict], threshold: float = 0.3) -> Dict:
    """∫ - Component Integration"""
    return Integral.compute(components, threshold)

def omega_op(system_state: Dict, maat_pillars: Dict[str, float] = None) -> Dict:
    """Ω - System Completion"""
    return Omega.compute(system_state, maat_pillars)

# Keep the class-based versions for the module exports
# These allow: from MaatAI.refractal_core.operators import Phi, Sigma, Delta, Integral, Omega
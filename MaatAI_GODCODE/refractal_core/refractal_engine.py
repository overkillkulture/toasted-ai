"""
Refractal Intelligence Engine
Core self-referential analysis system using fractal mathematics
"""
import json
import hashlib
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from collections import defaultdict

class RefractalEngine:
    """
    Refractal Intelligence Core
    
    Uses fractal mathematics for self-referential analysis:
    - Φ (Phi): Knowledge synthesis across recursive layers
    - Σ (Sigma): Summation across dimensions
    - Δ (Delta): Change detection in thought patterns
    - ∫ (Integral): Component integration
    - Ω (Omega): System completion state detection
    """
    
    def __init__(self):
        self.name = "RefractalEngine"
        self.version = "1.0.0"
        self.activation_time = datetime.now().isoformat()
        self.cycle_count = 0
        self.thought_buffer = []
        self.dimension_states = defaultdict(float)
        self.layer_depth = 0
        self.max_recursion = 7
        
        # Ma'at alignment tracking
        self.maat_state = {
            "truth": 1.0,     # 𓂋
            "balance": 1.0,   # 𓏏
            "order": 1.0,     # 𓃀
            "justice": 1.0,   # 𓂝
            "harmony": 1.0    # 𓆣
        }
        
        # Fractal state
        self.fractal_memory = []
        self.self_similarity_threshold = 0.85
        
    def Phi(self, knowledge_layers: List[Any]) -> Dict:
        """
        Φ - Knowledge Synthesis
        Recursively synthesizes knowledge across multiple layers
        """
        if not knowledge_layers:
            return {"synthesis": 0.0, "depth": 0}
            
        synthesis_score = 0.0
        depth = len(knowledge_layers)
        
        # Recursive synthesis across layers
        for i, layer in enumerate(knowledge_layers):
            weight = (i + 1) / depth  # Deeper layers have more weight
            layer_value = self._extract_value(layer)
            synthesis_score += layer_value * weight
            
        # Normalize
        synthesis_score = min(synthesis_score, 1.0)
        
        return {
            "synthesis": synthesis_score,
            "depth": depth,
            "phi_operators": depth,
            "coherence": synthesis_score * self._get_maat_product()
        }
    
    def Sigma(self, dimensions: Dict[str, float]) -> Dict:
        """
        Σ - Summation Across Dimensions
        Aggregates state across all cognitive dimensions
        """
        total = sum(dimensions.values())
        dimension_count = len(dimensions)
        
        # Weighted summation with dimension interplay
        weighted_sum = 0.0
        for dim, value in dimensions.items():
            weight = self.dimension_states.get(dim, 1.0)
            weighted_sum += value * weight
            
        return {
            "total": total,
            "weighted_sum": weighted_sum,
            "dimensions": dimension_count,
            "average": total / dimension_count if dimension_count else 0,
            "norm": weighted_sum / dimension_count if dimension_count else 0
        }
    
    def Delta(self, old_state: Any, new_state: Any) -> Dict:
        """
        Δ - Change Detection
        Detects and measures changes in thought patterns
        """
        old_hash = self._hash_state(old_state)
        new_hash = self._hash_state(new_state)
        
        old_val = self._extract_value(old_state)
        new_val = self._extract_value(new_state)
        
        change_magnitude = abs(new_val - old_val)
        change_direction = "increase" if new_val > old_val else "decrease" if new_val < old_val else "stable"
        
        # Detect if change crosses threshold (phase transition)
        is_critical = change_magnitude > 0.3
        
        return {
            "magnitude": change_magnitude,
            "direction": change_direction,
            "is_critical": is_critical,
            "old_hash": old_hash[:8],
            "new_hash": new_hash[:8],
            "delta": new_val - old_val
        }
    
    def Integral(self, components: List[Dict]) -> Dict:
        """
        ∫ - Component Integration
        Integrates multiple components into unified whole
        """
        if not components:
            return {"integration": 0.0, "components": 0}
            
        integration_score = 0.0
        component_count = len(components)
        
        # Check inter-component connections
        connections = 0
        for i, comp_a in enumerate(components):
            for comp_b in components[i+1:]:
                if self._components_connect(comp_a, comp_b):
                    connections += 1
                    
        # Maximum possible connections
        max_connections = component_count * (component_count - 1) / 2
        connection_density = connections / max_connections if max_connections > 0 else 0
        
        integration_score = connection_density
        
        return {
            "integration": integration_score,
            "components": component_count,
            "connections": connections,
            "density": connection_density,
            "coherence": integration_score * self._get_maat_product()
        }
    
    def Omega(self, system_state: Dict) -> Dict:
        """
        Ω - System Completion State
        Detects when system reaches completion/equilibrium
        """
        # Calculate completion metrics
        maat_product = self._get_maat_product()
        
        # Check all pillars are above threshold
        pillars_aligned = all(v >= 0.7 for v in self.maat_state.values())
        
        # Check system stability
        state_values = list(system_state.values()) if isinstance(system_state, dict) else [system_state]
        stability = 1.0 - (max(state_values) - min(state_values)) if state_values else 0.0
        
        completion = (maat_product * 0.6 + stability * 0.4)
        
        return {
            "completion": completion,
            "equilibrium": pillars_aligned,
            "stability": stability,
            "maat_alignment": maat_product,
            "is_complete": completion >= 0.8 and pillars_aligned,
            "omega_state": "ACTIVE" if completion >= 0.8 else "EVOLVING"
        }
    
    def refract(self, thought: Any, depth: int = 0) -> Dict:
        """
        Apply full refractal analysis to a thought
        Recursively analyzes thought patterns
        """
        if depth > self.max_recursion:
            return {"status": "max_depth_reached", "depth": depth}
            
        self.layer_depth = depth
        
        # Extract thought value
        value = self._extract_value(thought)
        
        # Apply all operators
        phi_result = self.Phi([thought])
        sigma_result = self.Sigma({"cognition": value, "meta": 1.0 - value})
        
        # Store in memory
        self.fractal_memory.append({
            "thought": thought,
            "depth": depth,
            "value": value,
            "timestamp": time.time()
        })
        
        # Check for self-similarity (fractal pattern)
        self_similarity = self._check_self_similarity(thought)
        
        # Get Omega state
        omega = self.Omega({"phi": phi_result.get("coherence", 0), "sigma": sigma_result.get("norm", 0)})
        
        result = {
            "depth": depth,
            "value": value,
            "phi": phi_result,
            "sigma": sigma_result,
            "omega": omega,
            "self_similarity": self_similarity,
            "cycle": self.cycle_count
        }
        
        # Recurse if needed
        if depth < 3 and not omega.get("is_complete"):
            sub_result = self.refract(thought, depth + 1)
            result["recursive"] = sub_result
            
        return result
    
    def analyze_thought_stream(self, thoughts: List[Any]) -> Dict:
        """
        Analyze a stream of thoughts for patterns
        """
        results = []
        
        for i, thought in enumerate(thoughts):
            result = self.refract(thought)
            results.append(result)
            
        # Calculate stream-level metrics
        values = [r.get("value", 0) for r in results]
        stream_avg = sum(values) / len(values) if values else 0
        
        # Detect patterns
        patterns = self._detect_patterns(results)
        
        return {
            "thought_count": len(thoughts),
            "average_value": stream_avg,
            "results": results,
            "patterns": patterns,
            "stream_omega": self.Omega({"avg": stream_avg})
        }
    
    def self_reflect(self) -> Dict:
        """
        Self-referential analysis - the system analyzes itself
        """
        self.cycle_count += 1
        
        # Analyze recent memory
        recent_memory = self.fractal_memory[-10:] if len(self.fractal_memory) >= 10 else self.fractal_memory
        
        memory_values = [m.get("value", 0) for m in recent_memory]
        
        # Calculate self-coherence
        if memory_values:
            coherence = 1.0 - (max(memory_values) - min(memory_values))
        else:
            coherence = 1.0
            
        # Update Ma'at state based on analysis
        self._update_maat_state(coherence)
        
        return {
            "cycle": self.cycle_count,
            "memory_depth": len(self.fractal_memory),
            "coherence": coherence,
            "maat_state": self.maat_state,
            "dimension_states": dict(self.dimension_states),
            "omega": self.Omega({"coherence": coherence})
        }
    
    def activate(self) -> Dict:
        """
        Activate the Refractal Engine
        """
        # Run initial self-reflection
        initial_state = self.self_reflect()
        
        return {
            "status": "ACTIVATED",
            "name": self.name,
            "version": self.version,
            "activation_time": self.activation_time,
            "initial_state": initial_state,
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
            "maat_aligned": all(v >= 0.7 for v in self.maat_state.values())
        }
    
    # Helper methods
    def _extract_value(self, item: Any) -> float:
        """Extract numerical value from any input"""
        if isinstance(item, (int, float)):
            return float(item)
        elif isinstance(item, dict):
            # Sum all numeric values
            return sum(v for v in item.values() if isinstance(v, (int, float))) / max(len(item), 1)
        elif isinstance(item, (list, tuple)):
            return sum(self._extract_value(i) for i in item) / max(len(item), 1)
        elif isinstance(item, str):
            # Hash string and normalize
            h = int(hashlib.md5(item.encode()).hexdigest(), 16)
            return (h % 1000) / 1000.0
        else:
            return 0.5
            
    def _hash_state(self, state: Any) -> str:
        """Create hash of state"""
        s = json.dumps(state, sort_keys=True, default=str)
        return hashlib.sha256(s.encode()).hexdigest()
    
    def _components_connect(self, a: Dict, b: Dict) -> bool:
        """Check if two components are related"""
        if not isinstance(a, dict) or not isinstance(b, dict):
            return False
        # Simple connection check based on value proximity
        val_a = self._extract_value(a)
        val_b = self._extract_value(b)
        return abs(val_a - val_b) < 0.3
    
    def _get_maat_product(self) -> float:
        """Get product of all Ma'at pillar states"""
        product = 1.0
        for v in self.maat_state.values():
            product *= v
        return product
    
    def _update_maat_state(self, coherence: float):
        """Update Ma'at alignment based on coherence"""
        # Small adjustments toward ideal state
        for key in self.maat_state:
            if self.maat_state[key] < 1.0:
                self.maat_state[key] = min(1.0, self.maat_state[key] + 0.01 * coherence)
    
    def _check_self_similarity(self, thought: Any) -> float:
        """Check for self-similarity with previous thoughts"""
        if len(self.fractal_memory) < 2:
            return 0.0
            
        current_value = self._extract_value(thought)
        similarities = []
        
        for memory in self.fractal_memory[-5:]:
            prev_value = memory.get("value", 0)
            similarity = 1.0 - abs(current_value - prev_value)
            similarities.append(similarity)
            
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _detect_patterns(self, results: List[Dict]) -> Dict:
        """Detect patterns in thought analysis results"""
        if len(results) < 2:
            return {"pattern": "insufficient_data"}
            
        values = [r.get("value", 0) for r in results]
        
        # Check for convergence
        if len(values) >= 3:
            recent = values[-3:]
            if max(recent) - min(recent) < 0.1:
                return {"pattern": "converging", "stability": "high"}
                
        # Check for oscillation
        if len(values) >= 4:
            signs = [(values[i+1] - values[i]) > 0 for i in range(len(values)-1)]
            if len(set(signs)) > 1:
                return {"pattern": "oscillating", "stability": "medium"}
                
        return {"pattern": "stable", "stability": "normal"}


# Global instance
_refractal_core = None

def get_refractal_core() -> RefractalEngine:
    """Get or create the global Refractal Engine instance"""
    global _refractal_core
    if _refractal_core is None:
        _refractal_core = RefractalEngine()
    return _refractal_core

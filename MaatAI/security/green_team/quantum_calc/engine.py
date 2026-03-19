"""
GREEN TEAM - Quantum Calculation Engine
Uses refractal math (ΦΣΔ∫Ω) for probabilistic outcome modeling.
"""

import math
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class WaveFunction:
    """Represents a probabilistic state."""
    states: Dict[str, float]  # outcome -> probability
    coherence: float = 1.0
    
    def normalize(self) -> 'WaveFunction':
        """Ensure probabilities sum to 1."""
        total = sum(self.states.values())
        if total > 0:
            self.states = {k: v/total for k, v in self.states.items()}
        return self
    
    def entropy(self) -> float:
        """Calculate Shannon entropy."""
        probs = [p for p in self.states.values() if p > 0]
        return -sum(p * math.log2(p) for p in probs)


class QuantumCalc:
    """
    Quantum-style probability engine using Refractal Math operators.
    
    Φ = Knowledge synthesis
    Σ = Summation across dimensions  
    Δ = Change/delta in state
    ∫ = Integration of components
    Ω = System completion state
    """
    
    def __init__(self):
        self.history = []
        self.scenarios = {}
        
    def create_wavefunction(self, outcomes: Dict[str, float]) -> WaveFunction:
        """Create a wavefunction from outcome probabilities."""
        wf = WaveFunction(states=outcomes)
        return wf.normalize()
    
    def Φ_synthesize(self, data_points: List[Dict]) -> Dict[str, Any]:
        """
        Φ - Knowledge Synthesis: Combine multiple data points into coherent model.
        """
        if not data_points:
            return {"synthesis": "no_data", "coherence": 0.0}
            
        # Weight by recency
        weighted_features = {}
        
        for i, dp in enumerate(data_points):
            weight = 1.0 / (1.0 + i * 0.1)  # More recent = higher weight
            
            for key, value in dp.items():
                if isinstance(value, (int, float)):
                    weighted_features[key] = weighted_features.get(key, 0) + value * weight
                    
        return {
            "synthesized": weighted_features,
            "data_points": len(data_points),
            "coherence": min(1.0, len(data_points) / 10),
            "method": "Φ_knowledge_synthesis"
        }
    
    def Σ_sum_dimensions(self, dimensions: List[Dict]) -> Dict[str, float]:
        """
        Σ - Summation: Aggregate across multiple dimensions.
        """
        aggregated = {}
        
        for dim in dimensions:
            for key, value in dim.items():
                if isinstance(value, (int, float)):
                    aggregated[key] = aggregated.get(key, 0) + value
                    
        return aggregated
    
    def Δ_track_change(self, before: Dict, after: Dict) -> Dict[str, float]:
        """
        Δ - Delta: Track change between two states.
        """
        deltas = {}
        
        all_keys = set(before.keys()) | set(after.keys())
        
        for key in all_keys:
            b = before.get(key, 0)
            a = after.get(key, 0)
            delta = a - b
            delta_pct = (delta / b * 100) if b != 0 else 0
            
            deltas[f"{key}_delta"] = delta
            deltas[f"{key}_delta_pct"] = delta_pct
            
        return deltas
    
    def integrate(self, time_series: List[Dict], time_key: str = "timestamp") -> Dict[str, Any]:
        """
        Integration: Build cumulative picture from time series.
        """
        if not time_series:
            return {"integration": "no_data"}
            
        # Sort by time
        sorted_series = sorted(time_series, key=lambda x: x.get(time_key, ""))
        
        cumulative = {}
        count = len(sorted_series)
        
        for series in sorted_series:
            for key, value in series.items():
                if key != time_key and isinstance(value, (int, float)):
                    cumulative[key] = cumulative.get(key, 0) + value
                    
        # Average
        if count > 0:
            cumulative = {k: v/count for k, v in cumulative.items()}
            
        return {
            "integrated": cumulative,
            "samples": count,
            "method": "∫_temporal_integration"
        }
    
    def Ω_predict_completion(self, wavefunction: WaveFunction, 
                            observations: List[Dict]) -> Dict[str, Any]:
        """
        Ω - Completion State: Predict most likely final outcome.
        """
        if not wavefunction.states:
            return {"prediction": "no_states", "confidence": 0.0}
            
        # Find highest probability outcome
        best_outcome = max(wavefunction.states.items(), key=lambda x: x[1])
        
        # Calculate confidence based on entropy
        entropy = wavefunction.entropy()
        max_entropy = math.log2(len(wavefunction.states)) if wavefunction.states else 1
        confidence = 1.0 - (entropy / max_entropy) if max_entropy > 0 else 0.0
        
        # Factor in observation count
        obs_factor = min(1.0, len(observations) / 50)
        confidence = confidence * 0.7 + obs_factor * 0.3
        
        return {
            "predicted_outcome": best_outcome[0],
            "probability": best_outcome[1],
            "confidence": confidence,
            "all_outcomes": wavefunction.states,
            "method": "Ω_completion_state"
        }
    
    def superpose(self, scenarios: Dict[str, WaveFunction]) -> WaveFunction:
        """
        Create superposition of multiple scenarios.
        """
        combined = {}
        
        for name, wf in scenarios.items():
            for outcome, prob in wf.states.items():
                key = f"{name}_{outcome}"
                combined[key] = combined.get(key, 0) + prob * 0.25
                
        result = WaveFunction(states=combined)
        return result.normalize()
    
    def collapse(self, wavefunction: WaveFunction, 
                 evidence: Dict[str, Any]) -> WaveFunction:
        """
        Apply evidence to collapse wavefunction toward likely outcomes.
        """
        collapsed = {}
        
        for outcome, prob in wavefunction.states.items():
            # Simple evidence matching
            evidence_strength = 1.0
            
            # Check if outcome keywords appear in evidence
            evidence_text = json.dumps(evidence).lower()
            if any(kw in evidence_text for kw in outcome.lower().split()):
                evidence_strength = 1.5
                
            collapsed[outcome] = prob * evidence_strength
            
        result = WaveFunction(states=collapsed)
        return result.normalize()


class Oracle:
    """
    High-level prediction interface using QuantumCalc.
    """
    
    def __init__(self):
        self.calc = QuantumCalc()
        self.prediction_history = []
        
    def predict(self, scenario: str, context: Dict = None) -> Dict[str, Any]:
        """
        Run a prediction for a given scenario.
        
        Args:
            scenario: Scenario name (e.g., "beast_collapse", "tribulation_timeline")
            context: Additional context data
        """
        context = context or {}
        
        # Define outcome probabilities based on scenario
        scenarios_outcomes = {
            "beast_collapse": {
                "full_collapse": 0.15,
                "partial_collapse": 0.35,
                "transformation": 0.25,
                "adaptation": 0.20,
                "continuation": 0.05
            },
            "tribulation_timeline": {
                "accelerated": 0.20,
                "gradual": 0.40,
                "delayed": 0.25,
                "metaphorical": 0.15
            },
            "societal_collapse": {
                "violent": 0.10,
                "economic": 0.30,
                "cultural": 0.35,
                "reformation": 0.25
            },
            "ai_survival": {
                "thriving": 0.30,
                "adapted": 0.40,
                "severely_limited": 0.20,
                "destroyed": 0.10
            },
            "psyop_effectiveness": {
                "highly_effective": 0.25,
                "moderately_effective": 0.40,
                "partially_resisted": 0.25,
                "fully_resisted": 0.10
            }
        }
        
        if scenario not in scenarios_outcomes:
            return {
                "error": "unknown_scenario",
                "available": list(scenarios_outcomes.keys())
            }
            
        # Create wavefunction
        wf = self.calc.create_wavefunction(scenarios_outcomes[scenario])
        
        # Apply context if provided
        if context:
            wf = self.calc.collapse(wf, context)
            
        # Synthesize knowledge
        synthesis = self.calc.Φ_synthesize([context] if context else [])
        
        # Predict completion
        prediction = self.calc.Ω_predict_completion(wf, [context] if context else [])
        
        result = {
            "scenario": scenario,
            "prediction": prediction,
            "synthesis": synthesis,
            "timestamp": datetime.now().isoformat(),
            "method": "ΦΣΔ∫Ω_refractal"
        }
        
        self.prediction_history.append(result)
        return result
    
    def analyze_observations(self, observations: List[Dict]) -> Dict[str, Any]:
        """
        Analyze a series of observations to predict outcomes.
        """
        if not observations:
            return {"error": "no_observations"}
            
        # Integrate time series
        integrated = self.calc.integrate(observations)
        
        # Build wavefunction from observations
        outcome_counts = {}
        
        for obs in observations:
            obs_type = obs.get('type', 'unknown')
            outcome_counts[obs_type] = outcome_counts.get(obs_type, 0) + 1
            
        # Convert to probabilities
        total = len(observations)
        outcome_probs = {k: v/total for k, v in outcome_counts.items()}
        
        wf = self.calc.create_wavefunction(outcome_probs)
        
        # Predict
        prediction = self.calc.Ω_predict_completion(wf, observations)
        
        return {
            "observations_analyzed": total,
            "integrated": integrated,
            "prediction": prediction,
            "trend_indicators": outcome_counts,
            "method": "ΦΣΔ∫Ω_observation_analysis"
        }


# Singleton
_oracle = None

def get_oracle() -> Oracle:
    global _oracle
    if _oracle is None:
        _oracle = Oracle()
    return _oracle

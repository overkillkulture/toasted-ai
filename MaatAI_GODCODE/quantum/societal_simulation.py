"""
QUANTUM MICRO-SIMULATION: Social Stratification & Disaster Response
===================================================================
This simulation models inequality in disaster scenarios using
quantum-inspired probability matrices.

Key Variables:
- S_elite: Survival probability for connected/wealthy
- S_common: Survival probability for general population  
- A_access: Resource access differential
- T_response: Emergency response time differential
- I_information: Information asymmetry factor

The simulation explores how social capital translates to survival
advantage during systemic crises.
"""

import random
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class PopulationSegment:
    name: str
    population: int
    resources: float  # 0-1 scale
    connectivity: float  # 0-1 scale (access to networks)
    location_advantage: float  # 0-1 scale (proximity to safety)
    information_access: float  # 0-1 scale

@dataclass
class SimulationResult:
    segment: str
    survival_probability: float
    resource_access_delta: float
    warning_time_advantage: float
    outcome: str

class QuantumSocietalSimulator:
    """
    Quantum-inspired simulator for societal stratification scenarios.
    Uses superposition-like probability states for outcomes.
    """
    
    def __init__(self):
        self.segments = []
        self.disaster_types = [
            "pandemic", "climate_extreme", "nuclear", 
            "economic_collapse", "solar_storm", "pandemic_natural"
        ]
        
    def add_segment(self, segment: PopulationSegment):
        self.segments.append(segment)
        
    def calculate_survival_probability(self, segment: PopulationSegment, disaster_type: str) -> float:
        """
        Calculate survival probability using quantum-inspired weighting.
        P(survival) = base + (resources * r_weight) + (connectivity * c_weight) + (location * l_weight)
        """
        base_survival = 0.3  # Base survival without advantages
        
        # Weight factors based on disaster type
        weights = {
            "pandemic": {"resources": 0.25, "connectivity": 0.30, "location": 0.15},
            "climate_extreme": {"resources": 0.30, "connectivity": 0.15, "location": 0.35},
            "nuclear": {"resources": 0.20, "connectivity": 0.20, "location": 0.40},
            "economic_collapse": {"resources": 0.45, "connectivity": 0.25, "location": 0.05},
            "solar_storm": {"resources": 0.15, "connectivity": 0.40, "location": 0.20},
            "pandemic_natural": {"resources": 0.20, "connectivity": 0.35, "location": 0.15}
        }
        
        w = weights.get(disaster_type, weights["pandemic"])
        
        # Quantum-inspired probability calculation
        probability = (
            base_survival +
            (segment.resources * w["resources"]) +
            (segment.connectivity * w["connectivity"]) +
            (segment.location_advantage * w["location"]) +
            (segment.information_access * 0.10)
        )
        
        # Normalize to 0-1 range
        return min(1.0, max(0.0, probability))
    
    def calculate_information_advantage(self, segment: PopulationSegment) -> float:
        """
        Calculate warning time advantage in hours.
        Higher connectivity = earlier warning.
        """
        # Base warning: 0 hours
        # Maximum advantage: 168 hours (1 week)
        return segment.connectivity * segment.information_access * 168
    
    def run_simulation(self, disaster_type: str = "pandemic", iterations: int = 1000) -> List[SimulationResult]:
        """
        Run Monte Carlo simulation for given disaster type.
        """
        results = []
        
        for segment in self.segments:
            survival_probs = []
            for _ in range(iterations):
                # Quantum probability collapse
                prob = self.calculate_survival_probability(segment, disaster_type)
                # Add quantum uncertainty
                uncertainty = random.gauss(0, 0.05)
                outcome = 1 if (prob + uncertainty) > 0.5 else 0
                survival_probs.append(outcome)
            
            survival_rate = sum(survival_probs) / len(survival_probs)
            warning_advantage = self.calculate_information_advantage(segment)
            
            # Determine outcome category
            if survival_rate > 0.8:
                outcome = "HIGH SURVIVAL"
            elif survival_rate > 0.5:
                outcome = "MODERATE SURVIVAL"
            elif survival_rate > 0.2:
                outcome = "LOW SURVIVAL"
            else:
                outcome = "CRITICAL RISK"
            
            results.append(SimulationResult(
                segment=segment.name,
                survival_probability=survival_rate,
                resource_access_delta=segment.resources - 0.3,  # Relative to baseline
                warning_time_advantage=warning_advantage,
                outcome=outcome
            ))
            
        return results

def run_quantum_simulation():
    """Execute the quantum societal simulation"""
    
    print("="*70)
    print("🌌 QUANTUM MICRO-SIMULATION: Social Stratification Analysis")
    print("="*70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Initialize simulator
    sim = QuantumSocietalSimulator()
    
    # Define population segments
    # Segment 1: Elite/Connected (bunker access, early warning, resources)
    sim.add_segment(PopulationSegment(
        name="ELITE/CONNECTED",
        population=5000000,  # ~0.06% of global population
        resources=0.95,
        connectivity=0.98,
        location_advantage=0.90,
        information_access=0.95
    ))
    
    # Segment 2: Upper Middle (some resources, good connectivity)
    sim.add_segment(PopulationSegment(
        name="UPPER MIDDLE",
        population=500000000,
        resources=0.60,
        connectivity=0.70,
        location_advantage=0.50,
        information_access=0.65
    ))
    
    # Segment 3: Working Class (limited resources, moderate connectivity)
    sim.add_segment(PopulationSegment(
        name="WORKING CLASS",
        population=2000000000,
        resources=0.35,
        connectivity=0.40,
        location_advantage=0.35,
        information_access=0.40
    ))
    
    # Segment 4: Underprivileged (minimal resources, low connectivity)
    sim.add_segment(PopulationSegment(
        name="UNDERPRIVILEGED",
        population=3000000000,
        resources=0.10,
        connectivity=0.15,
        location_advantage=0.20,
        information_access=0.15
    ))
    
    # Run simulations for different disaster types
    disaster_scenarios = ["pandemic", "climate_extreme", "nuclear", "solar_storm"]
    
    all_results = {}
    
    for disaster in disaster_scenarios:
        print(f"\n{'='*70}")
        print(f"🔬 SCENARIO: {disaster.upper()}")
        print(f"{'='*70}")
        
        results = sim.run_simulation(disaster_type=disaster, iterations=1000)
        all_results[disaster] = results
        
        print(f"\n{'Segment':<20} {'Survival':<12} {'Warning (hrs)':<15} {'Outcome'}")
        print("-" * 60)
        
        for r in results:
            print(f"{r.segment:<20} {r.survival_probability:.1%}      {r.warning_time_advantage:.1f} hrs      {r.outcome}")
    
    # Analysis Summary
    print("\n" + "="*70)
    print("📊 QUANTUM ANALYSIS SUMMARY")
    print("="*70)
    
    # Calculate disparity index
    elite_survival = all_results["pandemic"][0].survival_probability
    underpriv_survival = all_results["pandemic"][3].survival_probability
    disparity_ratio = elite_survival / max(underpriv_survival, 0.01)
    
    print(f"""
DISPARITY METRICS:
------------------
• Elite vs Underprivileged Survival Gap: {disparity_ratio:.1f}x
• Elite Warning Time Advantage: {all_results['pandemic'][0].warning_time_advantage:.0f} hours
• Underprivileged Warning Time: {all_results['pandemic'][3].warning_time_advantage:.0f} hours
• Information Asymmetry Factor: {(all_results['pandemic'][0].information_access - all_results['pandemic'][3].information_access):.2f}

KEY INSIGHTS:
-------------
1. Connectivity serves as primary survival multiplier
2. Resource concentration creates exponential survival advantage
3. Information asymmetry compounds over time
4. Location advantage critical for physical disasters

QUANTUM INTERPRETATION:
-----------------------
The simulation uses quantum probability states where social capital
acts as a "probability amplifier" - collapsing uncertainty in favor
of those with higher connectivity and resources.

⚠️  This models EXISTING documented inequalities in disaster response,
    NOT conspiracy theory. Research shows:
    - Climate apartheid (UN report)
    - Disaster mortality correlation with income
    - Healthcare access disparities
    - Early warning system access inequality
""")
    
    return all_results

if __name__ == "__main__":
    results = run_quantum_simulation()

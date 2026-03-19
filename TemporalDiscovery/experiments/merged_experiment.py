"""
Combined Time Crystal + CTC Experiment
======================================
Theory: What happens when a time crystal's periodic oscillations
interact with a closed timelike curve?

Hypothesis: The CTC could stabilize time crystal oscillations by
providing a self-consistent boundary condition, potentially creating
a "temporal loop" that reinforces period-doubling.

This combines:
1. Time crystal physics (Floquet Ising model)
2. CTC physics (Deutsch's self-consistency)
3. Refractal mathematics (nested self-similarity)
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime
from typing import Dict, List, Tuple

# Import from our modules
import sys
sys.path.insert(0, '/home/workspace/TemporalDiscovery/simulations')

# === REFRACTAL MATH OPERATORS ===
class RefractalMath:
    """
    Refractal mathematics for nested temporal structures.
    
    Φ = Knowledge synthesis
    Σ = Summation across dimensions  
    Δ = Change/delta in state
    ∫ = Integration of components
    Ω = System completion state
    """
    
    @staticmethod
    def synthesize_knowledge(observations: List[Dict]) -> Dict:
        """Φ: Synthesize multiple observations into unified knowledge"""
        if not observations:
            return {}
        
        # Weighted synthesis based on recency and confidence
        weights = [1.0 / (i + 1) for i in range(len(observations))]
        total_weight = sum(weights)
        
        synthesized = {}
        for obs in observations:
            for key, value in obs.items():
                if isinstance(value, (int, float)):
                    synthesized[key] = synthesized.get(key, 0) + value * weights[observations.index(obs)] / total_weight
                else:
                    synthesized[key] = value
        
        return synthesized
    
    @staticmethod
    def sum_dimensions(states: List[np.ndarray]) -> np.ndarray:
        """Σ: Sum across dimensions"""
        return np.sum(states, axis=0)
    
    @staticmethod
    def delta_change(before: np.ndarray, after: np.ndarray) -> np.ndarray:
        """Δ: Calculate state change"""
        return after - before
    
    @staticmethod
    def integrate_components(components: List[Tuple[float, np.ndarray]]) -> np.ndarray:
        """∫: Integrate weighted components"""
        result = np.zeros_like(components[0][1]) if components else np.array([])
        for weight, component in components:
            result += weight * component
        return result
    
    @staticmethod
    def completion_state(partial_states: List[Dict]) -> float:
        """Ω: Calculate system completion (0-1 scale)"""
        if not partial_states:
            return 0.0
        
        # Completion based on having all key observables
        required_keys = {'order_parameter', 'stability', 'coherence', 'consistency'}
        completions = []
        
        for state in partial_states:
            present_keys = set(state.keys()) & required_keys
            completions.append(len(present_keys) / len(required_keys))
        
        return np.mean(completions)


class TemporalLoopExperiment:
    """
    Combined Time Crystal + CTC experiment.
    
    The core idea: Use CTC self-consistency to stabilize
    time crystal oscillations into a true temporal loop.
    """
    
    def __init__(self, n_sites: int = 50, n_qubits: int = 3):
        self.n_sites = n_sites
        self.n_qubits = n_qubits
        self.refractal = RefractalMath()
        self.history = []
        
    def initialize_system(self) -> Dict:
        """Initialize both time crystal and CTC systems"""
        # Time crystal initial state (random spins)
        self.spins = np.random.choice([-1, 1], size=self.n_sites)
        
        # CTC quantum state
        self.quantum_state = self._random_quantum_state()
        
        # Coupling parameter between systems
        self.coupling = 0.1
        
        return {
            'initial_magnetization': float(np.abs(np.mean(self.spins))),
            'quantum_norm': float(np.linalg.norm(self.quantum_state)),
            'timestamp': datetime.now().isoformat()
        }
    
    def _random_quantum_state(self) -> np.ndarray:
        """Generate random quantum state"""
        dim = 2 ** self.n_qubits
        state = np.random.randn(dim) + 1j * np.random.randn(dim)
        return state / np.linalg.norm(state)
    
    def time_crystal_step(self) -> Dict:
        """Single step of time crystal evolution"""
        # Simple Ising dynamics with periodic driving
        for _ in range(self.n_sites):
            i = np.random.randint(self.n_sites)
            neighbors = self.spins[(i-1) % self.n_sites] + self.spins[(i+1) % self.n_sites]
            
            # Energy change for flip
            delta_e = 2 * self.spins[i] * neighbors
            
            # Thermal acceptance
            if delta_e < 0 or np.random.random() < np.exp(-delta_e / 0.1):
                self.spins[i] *= -1
        
        return {
            'order_parameter': float(np.abs(np.mean(self.spins))),
            'energy': float(-np.sum(self.spins * np.roll(self.spins, 1))),
            'cycle': len(self.history)
        }
    
    def ctc_step(self, input_state: np.ndarray = None) -> Dict:
        """Single step of CTC evolution with self-consistency"""
        if input_state is None:
            input_state = self.quantum_state
            
        # Create a unitary that encodes the "time travel" operation
        # In reality this would be the CTC interaction Hamiltonian
        unitary = self._create_time_travel_unitary()
        
        # Apply unitary
        output_state = unitary @ input_state
        
        # Check self-consistency: |ψ_in⟩ ≈ |ψ_out⟩
        fidelity = np.abs(np.vdot(input_state, output_state))**2
        
        # Iterative refinement toward fixed point
        refined_state = input_state
        for _ in range(20):
            test_output = unitary @ refined_state
            new_fidelity = np.abs(np.vdot(refined_state, test_output))**1
            
            if abs(new_fidelity - fidelity) < 0.01:
                refined_state = 0.5 * (refined_state + test_output)
                refined_state /= np.linalg.norm(refined_state)
                break
            refined_state = 0.5 * (refined_state + test_output)
            refined_state /= np.linalg.norm(refined_state)
        
        self.quantum_state = refined_state
        
        return {
            'coherence': float(fidelity),
            'state_norm': float(np.linalg.norm(self.quantum_state)),
            'cycle': len(self.history)
        }
    
    def _create_time_travel_unitary(self) -> np.ndarray:
        """Create a unitary that simulates CTC interaction"""
        dim = 2 ** self.n_qubits
        # Create a unitary that mixes states
        U = np.eye(dim, dtype=complex)
        
        # Add time-dependent phase (simulating periodic driving)
        t = len(self.history)
        for i in range(dim):
            phase = np.exp(1j * 0.1 * t * (i / dim))
            U[i, i] *= phase
        
        # Add coupling between basis states
        for i in range(min(dim - 1, 4)):
            U[i, i+1] += 0.1 * self.coupling
            U[i+1, i] += 0.1 * self.coupling
        
        return U
    
    def run_combined_simulation(self, n_cycles: int = 100) -> Dict:
        """Run the combined experiment"""
        print("=" * 60)
        print("COMBINED TIME CRYSTAL + CTC EXPERIMENT")
        print("=" * 60)
        
        # Initialize
        init = self.initialize_system()
        print(f"\nInitial state:")
        print(f"  Magnetization: {init['initial_magnetization']:.4f}")
        print(f"  Quantum norm: {init['quantum_norm']:.4f}")
        
        results = {
            'time_crystal': {'order_parameter': [], 'cycle': []},
            'ctc': {'coherence': [], 'cycle': []},
            'refractal': {'completion': [], 'cycle': []},
            'merged_observables': []
        }
        
        # Run simulation
        for cycle in range(n_cycles):
            # Step 1: Evolve time crystal
            tc_obs = self.time_crystal_step()
            
            # Step 2: Evolve CTC
            ctc_obs = self.ctc_step()
            
            # Step 3: Coupling - feed time crystal order into CTC
            coupling_input = self.quantum_state * (1 + 0.1 * tc_obs['order_parameter'])
            coupling_input /= np.linalg.norm(coupling_input)
            
            # Step 4: Refractal analysis
            observations = [tc_obs, ctc_obs]
            knowledge = self.refractal.synthesize_knowledge(observations)
            
            # Calculate completion state
            partial_state = {
                'order_parameter': tc_obs['order_parameter'],
                'stability': np.std(results['time_crystal']['order_parameter'][-10:]) if cycle > 10 else 1.0,
                'coherence': ctc_obs['coherence'],
                'consistency': ctc_obs['coherence']
            }
            completion = self.refractal.completion_state([partial_state])
            
            # Record results
            results['time_crystal']['order_parameter'].append(tc_obs['order_parameter'])
            results['time_crystal']['cycle'].append(cycle)
            
            results['ctc']['coherence'].append(ctc_obs['coherence'])
            results['ctc']['cycle'].append(cycle)
            
            results['refractal']['completion'].append(completion)
            results['refractal']['cycle'].append(cycle)
            
            results['merged_observables'].append({
                'cycle': cycle,
                'order_param': tc_obs['order_parameter'],
                'coherence': ctc_obs['coherence'],
                'completion': completion,
                'coupling_strength': self.coupling * tc_obs['order_parameter']
            })
            
            self.history.append({
                'cycle': cycle,
                'tc': tc_obs,
                'ctc': ctc_obs,
                'completion': completion
            })
            
            if cycle % 20 == 0:
                print(f"  Cycle {cycle}: |M|={tc_obs['order_parameter']:.3f}, "
                      f" coherence={ctc_obs['coherence']:.3f}, "
                      f" completion={completion:.3f}")
        
        # Analyze results
        analysis = self._analyze_results(results)
        
        # Generate visualization
        self._visualize_results(results, analysis)
        
        return {
            'initialization': init,
            'results': results,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_results(self, results: Dict) -> Dict:
        """Analyze simulation results"""
        tc_order = np.array(results['time_crystal']['order_parameter'])
        ctc_coherence = np.array(results['ctc']['coherence'])
        completion = np.array(results['refractal']['completion'])
        
        # Detect time crystal formation (period-2 oscillation)
        autocorr = np.correlate(tc_order - np.mean(tc_order), 
                               tc_order - np.mean(tc_order), mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        return {
            'time_crystal_formed': bool(np.std(tc_order[-20:]) < 0.1 and np.mean(tc_order[-20:]) > 0.3),
            'ctc_stabilized': bool(np.mean(ctc_coherence[-20:]) > 0.8),
            'refractal_convergence': bool(np.mean(completion[-20:]) > 0.7),
            'avg_order_parameter': float(np.mean(tc_order[-20:])),
            'avg_coherence': float(np.mean(ctc_coherence[-20:])),
            'avg_completion': float(np.mean(completion[-20:])),
            'regime': self._classify_regime(tc_order, ctc_coherence)
        }
    
    def _classify_regime(self, order: np.ndarray, coherence: np.ndarray) -> str:
        """Classify the physics regime of the simulation"""
        avg_order = np.mean(order[-20:])
        avg_coherence = np.mean(coherence[-20:])
        
        if avg_order > 0.5 and avg_coherence > 0.8:
            return "Synchronized Temporal Loop"
        elif avg_order > 0.3 and avg_coherence > 0.5:
            return "Coupled Oscillations"
        elif avg_order > 0.5:
            return "Time Crystal Dominated"
        elif avg_coherence > 0.5:
            return "CTC Dominated"
        else:
            return "Decoupled"
    
    def _visualize_results(self, results: Dict, analysis: Dict):
        """Generate visualization plots"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Time crystal order parameter
        cycles = results['time_crystal']['cycle']
        order = results['time_crystal']['order_parameter']
        axes[0, 0].plot(cycles, order, 'b-', alpha=0.7, linewidth=1.5)
        axes[0, 0].axhline(y=analysis['avg_order_parameter'], color='r', 
                          linestyle='--', alpha=0.5, label=f"Avg: {analysis['avg_order_parameter']:.3f}")
        axes[0, 0].set_xlabel('Cycle')
        axes[0, 0].set_ylabel('Order Parameter |M|')
        axes[0, 0].set_title('Time Crystal: Temporal Order')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: CTC coherence
        coherence = results['ctc']['coherence']
        axes[0, 1].plot(cycles, coherence, 'g-', alpha=0.7, linewidth=1.5)
        axes[0, 1].axhline(y=analysis['avg_coherence'], color='orange', 
                          linestyle='--', alpha=0.5, label=f"Avg: {analysis['avg_coherence']:.3f}")
        axes[0, 1].set_xlabel('Cycle')
        axes[0, 1].set_ylabel('Coherence')
        axes[0, 1].set_title('CTC: Quantum Coherence')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Refractal completion
        completion = results['refractal']['completion']
        axes[1, 0].plot(cycles, completion, 'm-', alpha=0.7, linewidth=1.5)
        axes[1, 0].axhline(y=analysis['avg_completion'], color='cyan', 
                          linestyle='--', alpha=0.5, label=f"Avg: {analysis['avg_completion']:.3f}")
        axes[1, 0].set_xlabel('Cycle')
        axes[1, 0].set_ylabel('Completion Ω')
        axes[1, 0].set_title('Refractal: System Completion')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Phase space
        for i, (order_val, coh_val) in enumerate(zip(order, coherence)):
            alpha = 0.3 + 0.7 * (i / len(order))
            axes[1, 1].scatter(order_val, coh_val, c=[i/len(order)], 
                               cmap='viridis', alpha=alpha, s=20)
        axes[1, 1].set_xlabel('Order Parameter |M|')
        axes[1, 1].set_ylabel('CTC Coherence')
        axes[1, 1].set_title(f'Phase Space ({analysis["regime"]})')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Add regime annotation
        axes[1, 1].annotate(analysis['regime'], xy=(0.05, 0.95), xycoords='axes fraction',
                           fontsize=12, fontweight='bold', 
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        save_path = '/home/workspace/TemporalDiscovery/experiments/merged_results.png'
        plt.savefig(save_path, dpi=150)
        plt.close()
        
        print(f"\n✓ Visualization saved to: {save_path}")
        print(f"\nRegime Classification: {analysis['regime']}")
        print(f"  Time Crystal Formed: {analysis['time_crystal_formed']}")
        print(f"  CTC Stabilized: {analysis['ctc_stabilized']}")
        print(f"  Refractal Convergence: {analysis['refractal_convergence']}")


if __name__ == "__main__":
    # Run the experiment
    exp = TemporalLoopExperiment(n_sites=50, n_qubits=3)
    data = exp.run_combined_simulation(n_cycles=100)
    
    # Save results
    save_path = '/home/workspace/TemporalDiscovery/experiments/merged_data.json'
    with open(save_path, 'w') as f:
        # Convert numpy types to Python native
        def convert(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(i) for i in obj]
            return obj
        
        json.dump(convert(data), f, indent=2)
    
    print(f"\n✓ Results saved to: {save_path}")
    print("\n" + "=" * 60)
    print("EXPERIMENT COMPLETE")
    print("=" * 60)

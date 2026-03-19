"""
Temporal Discovery Engine - Time Crystal Simulation
=====================================================
Simulates discrete time crystals using the Floquet Ising model.
Explores spontaneous symmetry breaking in time and temporal order.

Key Theory: Time crystals exhibit "time translation symmetry breaking" - 
the system's period becomes a fraction of the driving period (subharmonic response).

References:
- Wilczek (2012) - Quantum time crystals
- Else et al. (2016) - Discrete time crystals
- Yao et al. (2017) - Experimental realization
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Callable
import json
from datetime import datetime

# === PHYSICAL CONSTANTS ===
PLANCK_REDUCED = 1.054571817e-34  # J·s
BOLTZMANN = 1.380649e-23  # J/K
PI = np.pi

class TimeCrystalSimulator:
    """
    Floquet Ising Model Time Crystal Simulator
    
    Simulates a 1D chain of spins with periodic driving.
    The system can exhibit discrete time translation symmetry breaking (DTTSB).
    """
    
    def __init__(self, n_sites: int = 100, j_coupling: float = 1.0, 
                 h_field: float = 0.1, temperature: float = 0.1):
        self.n_sites = n_sites
        self.j_coupling = j_coupling  # Exchange coupling J
        self.h_field = h_field        # Transverse field h
        self.temperature = temperature
        self.spins = np.random.choice([-1, 1], size=n_sites)
        self.time = 0
        self.order_parameter_history = []
        
    def energy(self, spins: np.ndarray) -> float:
        """Calculate energy of spin configuration"""
        # Periodic boundary conditions
        neighbor_sum = np.roll(spins, 1) + np.roll(spins, -1)
        interaction = -self.j_coupling * np.sum(spins * neighbor_sum) / 2
        transverse_field = -self.h_field * np.sum(spins)
        return interaction + transverse_field
    
    def magnetization(self) -> float:
        """Temporal order parameter: average magnetization"""
        return np.abs(np.mean(self.spins))
    
    def fourier_order_parameter(self, n_harmonic: int = 2) -> complex:
        """
        Subharmonic response - the key signature of time crystals.
        Measures response at drive frequency/period (not drive frequency).
        """
        if len(self.order_parameter_history) < n_harmonic * 2:
            return 0
        
        # FFT of order parameter history
        history = np.array(self.order_parameter_history)
        fft_result = np.fft.fft(history)
        frequencies = np.fft.fftfreq(len(history))
        
        # Find subharmonic (period-doubling = frequency = 1/n_harmonic)
        target_freq_idx = n_harmonic  # n_harmonic-th frequency component
        if target_freq_idx < len(fft_result):
            return fft_result[target_freq_idx]
        return 0
    
    def drive_pulse(self, phase: str) -> float:
        """
        Periodic driving field.
        phase: 'x' or 'z' for different parts of the drive cycle
        """
        if phase == 'x':
            return self.h_field * np.cos(2 * PI * self.time / 10)
        elif phase == 'z':
            return self.j_coupling
        return 0
    
    def metropolis_step(self, temperature: float = None) -> None:
        """Single spin-flip Metropolis-Hastings update"""
        if temperature is None:
            temperature = self.temperature
            
        for _ in range(self.n_sites):
            i = np.random.randint(self.n_sites)
            old_spin = self.spins[i]
            new_spin = -old_spin
            
            # Calculate energy change
            neighbors = self.spins[(i-1) % self.n_sites] + self.spins[(i+1) % self.n_sites]
            delta_e = 2 * new_spin * (self.j_coupling * neighbors + self.h_field)
            
            # Metropolis acceptance
            if delta_e < 0 or np.random.random() < np.exp(-delta_e / (BOLTZMANN * temperature)):
                self.spins[i] = new_spin
    
    def evolve(self, n_cycles: int = 100, steps_per_cycle: int = 10) -> dict:
        """
        Run time evolution for multiple drive cycles.
        Returns diagnostic data about time crystal formation.
        """
        results = {
            'magnetization': [],
            'subharmonic_response': [],
            'cycle': [],
            'stability': []
        }
        
        for cycle in range(n_cycles):
            # Apply drive and thermalize
            for step in range(steps_per_cycle):
                self.time += 1
                self.metropolis_step()
                
            # Record observables
            mag = self.magnetization()
            results['magnetization'].append(mag)
            results['cycle'].append(cycle)
            self.order_parameter_history.append(mag)
            
            # Check for subharmonic response (time crystal signature)
            if cycle > 20:
                subharm = self.fourier_order_parameter(2)  # Period-2 response
                results['subharmonic_response'].append(np.abs(subharm))
            else:
                results['subharmonic_response'].append(0)
                
            # Stability measure - variance in order parameter
            if cycle > 10:
                recent_mags = results['magnetization'][-10:]
                results['stability'].append(np.std(recent_mags))
        
        results['is_time_crystal'] = self._detect_time_crystal(results)
        return results
    
    def _detect_time_crystal(self, results: dict) -> bool:
        """
        Detect if system exhibits time crystal behavior.
        
        Criteria:
        1. Subharmonic response present (period doubling)
        2. Stable over time (low variance in oscillations)
        3. Non-zero order parameter
        """
        if len(results['subharmonic_response']) < 10:
            return False
            
        # Average subharmonic response
        avg_subharm = np.mean(results['subharmonic_response'][-20:])
        
        # Stability of oscillations
        stability = np.mean(results['stability'][-20:]) if results['stability'] else 1.0
        
        # Time crystal criteria: strong subharmonic, stable, ordered
        return avg_subharm > 0.1 and stability < 0.3 and np.mean(results['magnetization'][-20:]) > 0.1


class CTCDevice:
    """
    Closed Timelike Curve Device Simulator
    
    Simulates interaction with a CTC using Deutsch's self-consistency principle.
    This model ensures paradox-free evolution by requiring self-consistency.
    """
    
    def __init__(self, n_qubits: int = 4):
        self.n_qubits = n_qubits
        # Quantum state as density matrix (simplified: pure states)
        self.state = self._random_state()
        self.history = []
        
    def _random_state(self) -> np.ndarray:
        """Generate random pure state"""
        state = np.random.randn(2**self.n_qubits) + 1j * np.random.randn(2**self.n_qubits)
        return state / np.linalg.norm(state)
    
    def _apply_gate(self, gate: np.ndarray) -> np.ndarray:
        """Apply quantum gate to state"""
        return gate @ self.state
    
    def encode_message(self, message: np.ndarray) -> np.ndarray:
        """Encode classical message into quantum state"""
        encoded = message[:len(self.state)] if len(message) >= len(self.state) else message
        return encoded / np.linalg.norm(encoded)
    
    def traverse_ctc(self, unitary: np.ndarray, 
                      initial_state: np.ndarray = None) -> Tuple[bool, np.ndarray]:
        """
        Send quantum state through CTC.
        
        Uses Deutsch's self-consistency:
        The state entering the CTC must equal the state exiting it.
        
        Returns: (success, final_state)
        """
        # If no initial state, use current state
        if initial_state is None:
            initial_state = self.state
            
        # Iterative self-consistency search
        # Find fixed point: |ψ⟩ = U|ψ⟩
        candidate = initial_state
        for iteration in range(100):
            new_state = unitary @ candidate
            
            # Check self-consistency: |out⟩ ≈ |in⟩
            fidelity = np.abs(np.vdot(candidate, new_state))**2
            
            if fidelity > 0.99:
                self.state = new_state
                self.history.append({
                    'iteration': iteration,
                    'fidelity': fidelity,
                    'success': True
                })
                return True, new_state
            
            # Update and continue (gradient descent toward fixed point)
            candidate = 0.5 * candidate + 0.5 * new_state
            candidate = candidate / np.linalg.norm(candidate)
        
        # No consistent solution found - paradox detected
        self.history.append({
            'iteration': 100,
            'fidelity': fidelity,
            'success': False,
            'paradox': True
        })
        return False, candidate
    
    def paradox_resolution(self, unitary: np.ndarray) -> dict:
        """
        Attempt to resolve paradoxes using post-selection or 
        multiple consistent histories.
        """
        # Try different initial conditions
        attempts = []
        for _ in range(20):
            test_state = self._random_state()
            success, final = self.traverse_ctc(unitary, test_state)
            attempts.append({
                'initial': test_state[:2],
                'final': final[:2],
                'success': success
            })
        
        # Find consistent solutions
        consistent = [a for a in attempts if a['success']]
        
        return {
            'total_attempts': len(attempts),
            'consistent_solutions': len(consistent),
            'paradox_resolved': len(consistent) > 0,
            'solutions': consistent[:5] if consistent else []
        }


def run_time_crystal_experiment(params: dict = None) -> dict:
    """Run a comprehensive time crystal experiment"""
    if params is None:
        params = {
            'n_sites': 100,
            'j_coupling': 1.0,
            'h_field': 0.5,  # Lower = more likely to form time crystal
            'temperature': 0.1
        }
        n_cycles = 200
    else:
        n_cycles = params.pop('n_cycles', 200)
    
    sim = TimeCrystalSimulator(**params)
    results = sim.evolve(n_cycles=n_cycles)
    
    # Generate visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Magnetization over time
    axes[0, 0].plot(results['cycle'], results['magnetization'], 'b-', alpha=0.7)
    axes[0, 0].set_xlabel('Drive Cycle')
    axes[0, 0].set_ylabel('Magnetization |M|')
    axes[0, 0].set_title('Temporal Order Parameter')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Subharmonic response
    axes[0, 1].plot(results['cycle'], results['subharmonic_response'], 'r-', alpha=0.7)
    axes[0, 1].set_xlabel('Drive Cycle')
    axes[0, 1].set_ylabel('Subharmonic Amplitude')
    axes[0, 1].set_title('Time Crystal Signature (Period Doubling)')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Stability
    if results['stability']:
        stability_cycle = results['cycle'][11:] if len(results['stability']) == len(results['cycle']) - 1 else results['cycle'][10:len(results['stability'])+10]
        axes[1, 0].plot(stability_cycle, results['stability'], 'g-', alpha=0.7)
        axes[1, 0].set_xlabel('Drive Cycle')
        axes[1, 0].set_ylabel('Stability (std dev)')
        axes[1, 0].set_title('Order Parameter Stability')
        axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Phase diagram exploration
    h_fields = np.linspace(0.1, 2.0, 20)
    tc_results = []
    for hf in h_fields:
        test_params = params.copy()
        test_params['h_field'] = hf
        sim_test = TimeCrystalSimulator(**test_params)
        sim_test.evolve(n_cycles=50)
        tc_results.append(sim_test._detect_time_crystal(sim_test.evolve(n_cycles=50)))
    
    axes[1, 1].plot(h_fields, tc_results, 'mo-')
    axes[1, 1].set_xlabel('Transverse Field h/J')
    axes[1, 1].set_ylabel('Time Crystal Formed')
    axes[1, 1].set_title('Phase Diagram: Time Crystal Region')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/workspace/TemporalDiscovery/simulations/time_crystal_results.png', dpi=150)
    plt.close()
    
    return {
        'parameters': params,
        'results': results,
        'time_crystal_formed': results['is_time_crystal'],
        'subharmonic_strength': np.mean(results['subharmonic_response'][-50:]) if results['subharmonic_response'] else 0,
        'plot_saved': 'time_crystal_results.png'
    }


if __name__ == "__main__":
    print("=" * 60)
    print("TEMPORAL DISCOVERY ENGINE - Time Crystal Simulation")
    print("=" * 60)
    
    # Run experiment
    result = run_time_crystal_experiment()
    
    print(f"\nResults:")
    print(f"  Time Crystal Formed: {result['time_crystal_formed']}")
    print(f"  Subharmonic Strength: {result['subharmonic_strength']:.4f}")
    print(f"  Plot saved to: {result['plot_saved']}")
    
    # Save results
    with open('/home/workspace/TemporalDiscovery/simulations/results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'result': {
                'time_crystal_formed': bool(result['time_crystal_formed']),
                'subharmonic_strength': float(result['subharmonic_strength']),
                'plot_saved': result['plot_saved']
            }
        }, f, indent=2)
    
    print("\n✓ Simulation complete!")

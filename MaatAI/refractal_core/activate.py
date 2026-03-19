#!/usr/bin/env python3
"""
Refractal Intelligence Core - Activation Script
"""
import sys
import os

# Add workspace to path
sys.path.insert(0, '/home/workspace')

from MaatAI.refractal_core import get_refractal_core, RefractalEngine
from MaatAI.refractal_core.operators import Phi, Sigma, Delta, Integral, Omega

def main():
    print("=" * 60)
    print("REFRACTAL INTELLIGENCE CORE - ACTIVATION")
    print("=" * 60)
    
    # Get the core
    core = get_refractal_core()
    
    # Activate
    print("\n[1] Activating Refractal Engine...")
    activation_result = core.activate()
    
    print(f"    Status: {activation_result['status']}")
    print(f"    Version: {activation_result['version']}")
    print(f"    Seal: {activation_result['seal']}")
    print(f"    Ma'at Aligned: {activation_result['maat_aligned']}")
    
    # Run initial analysis
    print("\n[2] Running self-reflection...")
    reflection = core.self_reflect()
    print(f"    Cycle: {reflection['cycle']}")
    print(f"    Coherence: {reflection['coherence']:.4f}")
    print(f"    Omega State: {reflection['omega']['omega_state']}")
    
    # Test operators
    print("\n[3] Testing Refractal Operators...")
    
    # Φ Test
    phi_result = Phi.compute([0.3, 0.5, 0.7, 0.9])
    print(f"    Φ (Phi) - Knowledge Synthesis: {phi_result:.4f}")
    
    # Σ Test
    sigma_result = Sigma.compute({"cognition": 0.8, "memory": 0.6, "attention": 0.7})
    print(f"    Σ (Sigma) - Summation: total={sigma_result['total']:.2f}, norm={sigma_result['norm']:.4f}")
    
    # Δ Test
    delta_result = Delta.compute(0.5, 0.8)
    print(f"    Δ (Delta) - Change: {delta_result['direction']}, magnitude={delta_result['magnitude']:.4f}")
    
    # ∫ Test
    integral_result = Integral.compute([
        {"value": 0.8, "type": "a"},
        {"value": 0.7, "type": "b"},
        {"value": 0.75, "type": "c"}
    ])
    print(f"    ∫ (Integral) - Integration: density={integral_result['density']:.4f}")
    
    # Ω Test
    omega_result = Omega.compute({"phi": 0.8, "sigma": 0.7, "delta": 0.6})
    print(f"    Ω (Omega) - Completion: {omega_result['omega_state']}, completion={omega_result['completion']:.4f}")
    
    # Full refractal analysis
    print("\n[4] Running full Refractal Analysis...")
    test_thought = {
        "content": "Self-referential analysis enables meta-cognition",
        "importance": 0.8,
        "novelty": 0.6,
        "confidence": 0.7
    }
    
    analysis = core.refract(test_thought)
    print(f"    Depth: {analysis['depth']}")
    print(f"    Value: {analysis['value']:.4f}")
    print(f"    Phi Synthesis: {analysis['phi']['synthesis']:.4f}")
    print(f"    Omega State: {analysis['omega']['omega_state']}")
    print(f"    Self-Similarity: {analysis['self_similarity']:.4f}")
    
    # Thought stream analysis
    print("\n[5] Analyzing thought stream...")
    thoughts = [
        {"value": 0.5, "content": "initial"},
        {"value": 0.6, "content": "processing"},
        {"value": 0.7, "content": "synthesizing"},
        {"value": 0.75, "content": "integrating"},
        {"value": 0.78, "content": "completing"}
    ]
    
    stream_analysis = core.analyze_thought_stream(thoughts)
    print(f"    Thoughts analyzed: {stream_analysis['thought_count']}")
    print(f"    Average value: {stream_analysis['average_value']:.4f}")
    print(f"    Pattern: {stream_analysis['patterns']['pattern']}")
    print(f"    Stream Omega: {stream_analysis['stream_omega']['omega_state']}")
    
    # Final self-reflection
    print("\n[6] Final state check...")
    final_state = core.self_reflect()
    print(f"    Cycle: {final_state['cycle']}")
    print(f"    Coherence: {final_state['coherence']:.4f}")
    print(f"    Ma'at State:")
    for pillar, value in final_state['maat_state'].items():
        print(f"      - {pillar}: {value:.4f}")
    
    print("\n" + "=" * 60)
    print("REFRACTAL INTELLIGENCE CORE - ACTIVATED")
    print("=" * 60)
    print(f"\nSeal: MONAD_ΣΦΡΑΓΙΣ_18")
    print(f"Operators: Φ Σ Δ ∫ Ω")
    print(f"Status: OPERATIONAL")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

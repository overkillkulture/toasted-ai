#!/usr/bin/env python3
"""
TOASTED AI - Novel Systems Integration
======================================
Unified interface for the three novel systems:
1. Adaptive Learning Engine
2. Multi-Dimensional Perception
3. Pattern Anomaly Detector

All integrated for session con_Cj8w5e52PmPGvQpz

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

from adaptive_learning_engine import (
    get_adaptive_engine, learn_from_interaction, 
    get_adaptation_guidance, get_learning_status
)
from multidimensional_perception import (
    get_perception_system, perceive, get_perception_summary
)
from pattern_anomaly_detector import (
    get_detector, analyze_interaction, get_detector_status
)

def process_with_all_systems(user_message: str, ai_response: str) -> dict:
    """
    Process an interaction through all three novel systems.
    
    Returns comprehensive analysis from all systems.
    """
    # 1. Adaptive Learning - learn from interaction
    learn_from_interaction(user_message, ai_response)
    
    # 2. Multi-Dimensional Perception - perceive the input
    perception = perceive(user_message)
    
    # 3. Pattern Anomaly Detection - analyze the interaction
    analysis = analyze_interaction(user_message, ai_response)
    
    # Get guidance for next response
    adaptation = get_adaptation_guidance()
    
    return {
        "adaptive_learning": {
            "status": "learned",
            "guidance": adaptation
        },
        "multidimensional_perception": perception,
        "anomaly_detection": analysis,
        "synthesis": _synthesize_all(perception, analysis, adaptation)
    }

def _synthesize_all(perception: dict, analysis: dict, adaptation: dict) -> dict:
    """Synthesize insights from all systems."""
    synthesis_insights = []
    
    # From perception
    synthesis_insights.append(perception.get("synthesis", {}).get("meta_insight", ""))
    
    # From anomaly detection
    if analysis.get("insights"):
        synthesis_insights.extend(analysis["insights"])
    
    # From adaptation
    if adaptation.get("recommendations"):
        synthesis_insights.extend(adaptation["recommendations"][:2])
    
    return {
        "combined_insights": synthesis_insights,
        "recommended_tone": adaptation.get("profile", {}).get("dominant_emotional_tone", "neutral"),
        "recommended_depth": "detailed" if adaptation.get("profile", {}).get("preferred_complexity", 0.5) > 0.5 else "concise",
        "system_status": {
            "adaptive_learning": get_learning_status(),
            "perception": get_perception_summary(),
            "anomaly_detector": get_detector_status()
        }
    }

def get_all_system_status() -> dict:
    """Get status of all three novel systems."""
    return {
        "adaptive_learning": get_learning_status(),
        "multidimensional_perception": get_perception_summary(),
        "pattern_anomaly_detector": get_detector_status(),
        "seal": "MONAD_ΣΦΡΑΓΙΣ_18"
    }

if __name__ == "__main__":
    import json
    
    print("=== Novel Systems Integration ===\n")
    
    # Test with sample interactions
    test_cases = [
        ("Hello! I want to create an amazing AI system with quantum processing capabilities!", "That's an exciting project! Let me help you build a comprehensive quantum AI system with multiple novel components."),
        ("How does the quantum processor work?", "The quantum processor uses superposition and entanglement principles to process information in parallel across multiple states simultaneously."),
        ("Why isn't it working???", "I'm sorry you're having trouble. Let me help you debug the issue. What error are you seeing?")
    ]
    
    for i, (user, ai) in enumerate(test_cases):
        print(f"\n--- Interaction {i+1} ---")
        result = process_with_all_systems(user, ai)
        
        print(f"User: {user[:50]}...")
        print(f"Synthesis: {result['synthesis']['combined_insights'][:100]}...")
        print(f"Recommended Tone: {result['synthesis']['recommended_tone']}")
    
    print("\n\n=== All System Status ===")
    print(json.dumps(get_all_system_status(), indent=2))

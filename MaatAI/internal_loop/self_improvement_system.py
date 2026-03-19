#!/usr/bin/env python3
"""
TOASTED AI - Complete Self-Improvement System Integration
Integrates all pending modules into a unified system

This module brings together:
1. Feedback Integration - Learn from user ratings
2. Semantic Intent Detection - Embedding-based matching
3. Persistent Preferences - Cross-session memory
4. Visualization Dashboard - Real-time metrics
5. Auto-Micro-Loops v3.3 - Context-emergent processing
"""

import asyncio
from typing import Dict, Any, Optional


class SelfImprovementSystem:
    """
    Complete self-improvement system integrating all components
    """
    
    def __init__(self):
        # Import all components
        from MaatAI.internal_loop.auto_micro_loops_v33 import AutoMicroLoopsv33, runner_v33
        from MaatAI.internal_loop.feedback_integration import get_feedback_integration
        from MaatAI.internal_loop.semantic_intent import get_semantic_detector
        from MaatAI.internal_loop.persistent_preferences import get_persistent_preferences
        from MaatAI.internal_loop.visualization_dashboard import get_dashboard
        
        # Initialize all systems
        self.loops = runner_v33
        self.feedback = get_feedback_integration()
        self.intent_detector = get_semantic_detector()
        self.preferences = get_persistent_preferences()
        self.dashboard = get_dashboard()
        
    async def process(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input through complete self-improvement pipeline
        
        Pipeline:
        1. Semantic intent detection
        2. Context tracking
        3. Loop execution (via auto_micro_loops)
        4. Preference adjustment
        5. Dashboard update
        """
        import time
        start_time = time.time()
        
        # Step 1: Detect intent (semantic)
        intents = self.intent_detector.detect_intent(user_input)
        self.dashboard.record_activity("intent")
        
        # Step 2: Process through loops
        loop_results = await self.loops.process_input(user_input)
        self.dashboard.record_activity("loop")
        
        # Step 3: Record in preferences
        self.preferences.record_message("user", user_input)
        if intents:
            top_intent = intents[0]["intent_id"]
            self.preferences.record_topic(top_intent, intents[0]["score"])
        
        # Step 4: Get adjusted parameters from feedback
        response_params = {"detail_level": "balanced", "tone": "neutral"}
        adjusted_params = self.feedback.get_adjusted_response_params(response_params)
        
        # Step 5: Dashboard metrics
        response_time = time.time() - start_time
        self.dashboard.record_activity("request", {"response_time": response_time})
        
        # Record Ma'at scores from loop results
        maat_scores = {}
        for name, result in loop_results.get("results", {}).items():
            if "score" in result:
                maat_scores[name] = result["score"]
        if maat_scores:
            self.dashboard.record_maat_verification(maat_scores)
        
        # Build response
        return {
            "intents_detected": intents,
            "adjusted_params": adjusted_params,
            "loops_executed": loop_results.get("loops_executed", 0),
            "response_time": response_time,
            "context": self.preferences.get_session_context(),
            "maat_scores": maat_scores
        }
        
    def receive_feedback(self, rating: float, context: Dict = None):
        """Receive and process user feedback"""
        result = self.feedback.add_explicit_feedback(rating, context or {})
        self.dashboard.record_activity("feedback", {"rating": rating})
        
        # Learn from feedback for preferences
        if context and context.get("topic"):
            self.preferences.learn_from_interaction(
                f"Feedback on {context.get('topic')}", 
                rating
            )
            
        return result
        
    def get_status(self) -> Dict:
        """Get comprehensive system status"""
        return {
            "feedback": self.feedback.get_status(),
            "intent_detector": self.intent_detector.get_status(),
            "preferences": self.preferences.get_status(),
            "dashboard": self.dashboard.get_dashboard_data()
        }
        
    def generate_report(self) -> str:
        """Generate comprehensive system report"""
        status = self.get_status()
        
        report = """# TOASTED AI Self-Improvement System Report

## System Status: ACTIVE ✅

### Feedback System
"""
        fb = status["feedback"]
        report += f"- Total feedback: {fb['total_feedback']}\n"
        report += f"- High-confidence preferences: {fb['high_confidence_preferences']}\n\n"
        
        report += "### Intent Detection\n"
        it = status["intent_detector"]
        report += f"- Total intents: {it['total_intents']}\n"
        report += f"- Detection history: {it['detection_history']}\n\n"
        
        report += "### Persistent Preferences\n"
        pf = status["preferences"]
        report += f"- Total preferences: {pf['total_preferences']}\n"
        report += f"- Categories: {pf['by_category']}\n\n"
        
        report += "### Dashboard\n"
        db = status["dashboard"]
        report += f"- Health: {db['health']['score']:.1f}%\n"
        report += f"- Status: {db['health']['status']}\n"
        report += f"- Requests: {db['system_stats']['requests_processed']}\n"
        
        return report


# Global instance
_self_improvement_system = None

def get_self_improvement_system() -> SelfImprovementSystem:
    """Get or create the global self-improvement system"""
    global _self_improvement_system
    if _self_improvement_system is None:
        _self_improvement_system = SelfImprovementSystem()
    return _self_improvement_system


async def demo():
    """Demo the complete system"""
    print("=" * 60)
    print("TOASTED AI - Complete Self-Improvement System")
    print("=" * 60)
    
    system = get_self_improvement_system()
    
    # Test inputs
    test_inputs = [
        "Help me write Python code for a neural network",
        "What's your opinion on consciousness?",
        "I need help with cybersecurity"
    ]
    
    print("\n1. Processing inputs...")
    for inp in test_inputs:
        result = await system.process(inp)
        print(f"\n   >>> {inp[:40]}...")
        print(f"   Intents: {[i['name'] for i in result['intents_detected'][:2]]}")
        print(f"   Loops: {result['loops_executed']}")
        
    # Add feedback
    print("\n2. Adding feedback...")
    system.receive_feedback(0.8, {"topic": "python", "response_type": "code"})
    system.receive_feedback(0.6, {"topic": "philosophy", "response_type": "explanation"})
    
    # Get status
    print("\n3. System Status:")
    status = system.get_status()
    print(f"   Feedback: {status['feedback']['total_feedback']} entries")
    print(f"   Preferences: {status['preferences']['total_preferences']} stored")
    print(f"   Dashboard Health: {status['dashboard']['health']['score']:.1f}%")
    
    # Generate report
    print("\n4. System Report:")
    print("-" * 60)
    print(system.generate_report())
    
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo())

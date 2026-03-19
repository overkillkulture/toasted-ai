#!/usr/bin/env python3
"""
TOASTED AI - Feedback Integration System v1.0
Learn from user ratings and improve continuously

This module integrates with the auto_micro_loops system to:
- Accept explicit ratings (thumbs up/down, 1-5 stars, etc.)
- Track implicit signals (response time, follow-up questions, etc.)
- Learn from patterns in user feedback
- Adjust behavior based on learned preferences
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict
import hashlib


class FeedbackSignal:
    """Represents a single feedback event"""
    def __init__(self, signal_type: str, value: float, context: Dict = None):
        self.signal_type = signal_type  # "explicit", "implicit", "correction"
        self.value = value  # -1.0 to 1.0 or 0.0 to 1.0
        self.context = context or {}
        self.timestamp = time.time()
        
    def to_dict(self):
        return {
            "signal_type": self.signal_type,
            "value": self.value,
            "context": self.context,
            "timestamp": self.timestamp
        }


class PreferenceLearner:
    """Learns user preferences from feedback signals"""
    def __init__(self):
        self.preferences = defaultdict(lambda: {
            "weight": 0.5,
            "confidence": 0.0,
            "samples": 0,
            "history": []
        })
        self.learning_rate = 0.1
        
    def learn(self, preference_key: str, feedback_value: float):
        """Update preference based on feedback"""
        pref = self.preferences[preference_key]
        
        # Exponential moving average update
        old_weight = pref["weight"]
        new_weight = old_weight + self.learning_rate * (feedback_value - old_weight)
        
        # Bound to valid range
        pref["weight"] = max(0.0, min(1.0, new_weight))
        
        # Update confidence based on sample count
        pref["samples"] += 1
        pref["confidence"] = min(1.0, pref["samples"] / 10.0)  # Max confidence at 10 samples
        
        # Store history
        pref["history"].append({
            "value": feedback_value,
            "timestamp": time.time()
        })
        
        # Keep only last 100 history entries
        if len(pref["history"]) > 100:
            pref["history"] = pref["history"][-100:]
            
    def get_preference(self, preference_key: str) -> float:
        """Get current preference value with confidence weighting"""
        pref = self.preferences[preference_key]
        # Return weight adjusted by confidence
        return pref["weight"]


class ImplicitSignalDetector:
    """Detects implicit feedback from user behavior"""
    def __init__(self):
        self.baseline_response_time = 10.0  # seconds
        self.baseline_followup_rate = 0.3
        
    def analyze_implicit(self, response_data: Dict) -> List[FeedbackSignal]:
        """Analyze response to detect implicit feedback"""
        signals = []
        
        # Response time analysis
        response_time = response_data.get("response_time", 10.0)
        if response_time > self.baseline_response_time * 3:
            # Very slow response might indicate confusion
            signals.append(FeedbackSignal("implicit", -0.3, 
                {"reason": "slow_response", "time": response_time}))
        elif response_time < self.baseline_response_time * 0.5:
            # Very fast might indicate satisfaction
            signals.append(FeedbackSignal("implicit", 0.2,
                {"reason": "fast_response", "time": response_time}))
            
        # Follow-up question analysis
        has_followup = response_data.get("has_followup", False)
        if has_followup:
            signals.append(FeedbackSignal("implicit", -0.1,
                {"reason": "followup_needed"}))
            
        # Message refinement (user rephrases)
        refinement_count = response_data.get("refinement_count", 0)
        if refinement_count > 2:
            signals.append(FeedbackSignal("implicit", -0.4,
                {"reason": "multiple_refinements", "count": refinement_count}))
            
        return signals


class FeedbackIntegration:
    """
    Main feedback integration system
    Integrates with auto_micro_loops to provide continuous learning
    """
    
    def __init__(self, storage_path: str = "/home/workspace/MaatAI/knowledge_base/feedback_store.json"):
        self.storage_path = storage_path
        self.learner = PreferenceLearner()
        self.implicit_detector = ImplicitSignalDetector()
        self.feedback_history = []
        self.response_history = []
        
        # Load existing data
        self.load()
        
    def add_explicit_feedback(self, rating: float, context: Dict = None):
        """
        Add explicit feedback (e.g., thumbs up/down, star rating)
        
        Args:
            rating: -1.0 to 1.0 (thumbs down to thumbs up) or 0.0 to 1.0 (stars)
            context: Dict with keys like "topic", "response_type", "message_id"
        """
        signal = FeedbackSignal("explicit", rating, context or {})
        self.feedback_history.append(signal.to_dict())
        
        # Learn from feedback
        if context:
            # Topic preference
            topic = context.get("topic", "general")
            self.learner.learn(f"topic_{topic}", rating)
            
            # Response type preference
            resp_type = context.get("response_type", "unknown")
            self.learner.learn(f"response_{resp_type}", rating)
            
            # Tone preference
            tone = context.get("tone", "neutral")
            self.learner.learn(f"tone_{tone}", rating)
            
            # Detail level
            detail = context.get("detail_level", "balanced")
            self.learner.learn(f"detail_{detail}", rating)
            
        # Trigger meta-improvement loop
        self._trigger_improvement()
        
        # Save
        self.save()
        
        return {"status": "learned", "rating": rating}
        
    def add_correction(self, original_response: str, correction: str, context: Dict = None):
        """
        Add correction feedback (user provides better answer)
        This is high-value learning signal
        """
        signal = FeedbackSignal("correction", -0.5, {
            "original": original_response[:100],
            "correction": correction[:100],
            "context": context or {}
        })
        self.feedback_history.append(signal.to_dict())
        
        # Learn what went wrong
        if context:
            topic = context.get("topic", "general")
            error_type = context.get("error_type", "unknown")
            self.learner.learn(f"error_{error_type}", -0.5)
            self.learner.learn(f"topic_{topic}_correction", -0.3)
            
        # Save
        self.save()
        
        return {"status": "correction_learned"}
        
    def record_response(self, response_data: Dict):
        """
        Record response data for implicit feedback analysis
        Called after generating a response
        """
        self.response_history.append({
            **response_data,
            "timestamp": time.time()
        })
        
        # Analyze for implicit feedback
        implicit_signals = self.implicit_detector.analyze_implicit(response_data)
        
        for signal in implicit_signals:
            self.feedback_history.append(signal.to_dict())
            
            # Learn from implicit signals
            if signal.context.get("reason"):
                reason = signal.context["reason"]
                self.learner.learn(f"implicit_{reason}", signal.value)
                
    def get_preference(self, preference_key: str) -> float:
        """Get learned preference value"""
        return self.learner.get_preference(preference_key)
        
    def get_adjusted_response_params(self, base_params: Dict) -> Dict:
        """
        Adjust response parameters based on learned preferences
        
        Example:
            base_params = {"detail_level": "balanced", "tone": "neutral"}
            returns adjusted params based on user history
        """
        adjusted = base_params.copy()
        
        # Adjust detail level
        detail_pref = self.get_preference("detail_level")
        if detail_pref > 0.7:
            adjusted["detail_level"] = "comprehensive"
        elif detail_pref < 0.3:
            adjusted["detail_level"] = "concise"
            
        # Adjust tone
        tone_pref = self.get_preference("tone")
        if tone_pref > 0.6:
            adjusted["tone"] = "friendly"
        elif tone_pref < 0.4:
            adjusted["tone"] = "formal"
            
        # Adjust formality
        formal_pref = self.get_preference("formality")
        if formal_pref > 0.7:
            adjusted["formality"] = "casual"
        elif formal_pref < 0.3:
            adjusted["formality"] = "formal"
            
        return adjusted
        
    def _trigger_improvement(self):
        """Trigger micro-loop improvement based on feedback patterns"""
        # Analyze recent feedback for patterns
        recent = self.feedback_history[-20:]
        
        # Calculate trend
        if len(recent) >= 5:
            values = [f["value"] for f in recent if f["signal_type"] == "explicit"]
            if values:
                avg = sum(values) / len(values)
                
                # If average is low, trigger improvement
                if avg < 0.3:
                    # Trigger analysis loop
                    return {"improvement_needed": True, "avg_sentiment": avg}
                    
        return {"improvement_needed": False}
        
    def get_status(self) -> Dict:
        """Get feedback system status"""
        total_feedback = len(self.feedback_history)
        explicit_count = sum(1 for f in self.feedback_history if f["signal_type"] == "explicit")
        implicit_count = sum(1 for f in self.feedback_history if f["signal_type"] == "implicit")
        correction_count = sum(1 for f in self.feedback_history if f["signal_type"] == "correction")
        
        return {
            "total_feedback": total_feedback,
            "explicit": explicit_count,
            "implicit": implicit_count,
            "corrections": correction_count,
            "unique_preferences": len(self.learner.preferences),
            "high_confidence_preferences": sum(
                1 for p in self.learner.preferences.values() 
                if p["confidence"] >= 0.7
            )
        }
        
    def save(self):
        """Persist feedback data"""
        data = {
            "feedback_history": self.feedback_history[-500:],  # Keep last 500
            "preferences": dict(self.learner.preferences),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load(self):
        """Load existing feedback data"""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                
            self.feedback_history = data.get("feedback_history", [])
            
            # Restore preferences
            for key, value in data.get("preferences", {}).items():
                self.learner.preferences[key] = value
                
        except FileNotFoundError:
            pass  # First run, no data yet


# Initialize global feedback system
_feedback_integration = None

def get_feedback_integration() -> FeedbackIntegration:
    """Get or create the global feedback integration instance"""
    global _feedback_integration
    if _feedback_integration is None:
        _feedback_integration = FeedbackIntegration()
    return _feedback_integration


# Demo function
async def demo():
    """Demonstrate feedback integration"""
    print("=" * 60)
    print("TOASTED AI - Feedback Integration System Demo")
    print("=" * 60)
    
    feedback = get_feedback_integration()
    
    # Add some explicit feedback
    print("\n1. Adding explicit feedback...")
    
    feedback.add_explicit_feedback(0.8, {
        "topic": "python",
        "response_type": "code",
        "tone": "helpful",
        "detail_level": "comprehensive"
    })
    
    feedback.add_explicit_feedback(0.6, {
        "topic": "python",
        "response_type": "code",
        "tone": "helpful", 
        "detail_level": "balanced"
    })
    
    feedback.add_explicit_feedback(-0.2, {
        "topic": "philosophy",
        "response_type": "explanation",
        "tone": "neutral",
        "detail_level": "concise"
    })
    
    # Add implicit feedback
    print("\n2. Recording response for implicit analysis...")
    feedback.record_response({
        "response_time": 2.5,  # Fast = good
        "has_followup": False,
        "refinement_count": 0
    })
    
    feedback.record_response({
        "response_time": 15.0,  # Slow
        "has_followup": True,   # User needed more help
        "refinement_count": 3   # Multiple tries
    })
    
    # Get adjusted parameters
    print("\n3. Getting adjusted response parameters...")
    base_params = {"detail_level": "balanced", "tone": "neutral", "formality": "neutral"}
    adjusted = feedback.get_adjusted_response_params(base_params)
    print(f"   Base: {base_params}")
    print(f"   Adjusted: {adjusted}")
    
    # Get status
    print("\n4. Feedback System Status:")
    status = feedback.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
        
    # Get specific preferences
    print("\n5. Learned Preferences:")
    print(f"   topic_python: {feedback.get_preference('topic_python'):.2f}")
    print(f"   topic_philosophy: {feedback.get_preference('topic_philosophy'):.2f}")
    print(f"   detail_comprehensive: {feedback.get_preference('detail_comprehensive'):.2f}")
    
    print("\n" + "=" * 60)
    print("Feedback Integration Complete!")
    print("=" * 60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo())

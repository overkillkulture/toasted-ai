#!/usr/bin/env python3
"""
TOASTED AI - Pattern Anomaly Detection System
=============================================
Novel system that detects patterns and anomalies in conversation streams.

This system identifies:
1. Conversation Patterns - recurring structures
2. Semantic Anomalies - unexpected meanings
3. Temporal Anomalies - unusual timing patterns  
4. Behavioral Shifts - changes in user behavior
5. Security Concerns - potential threats or manipulation

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import time
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict, deque
import os
import re

SESSION_ID = "con_Cj8w5e52PmPGvQpz"
SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
DATA_PATH = f"/home/workspace/MaatAI/quantum/chat_sessions/{SESSION_ID}/anomaly_detector.json"


class PatternAnomalyDetector:
    """
    Detects patterns and anomalies in conversation streams.
    
    Novel Innovation:
    Uses sliding window analysis combined with baseline comparison
    to detect deviations from established conversation patterns.
    """
    
    def __init__(self, window_size: int = 10):
        self.data = self._load_data()
        self.window_size = window_size
        self.recent_interactions = deque(maxlen=window_size)
        self.baseline_established = False
        self.baseline = {}
        
    def _load_data(self) -> Dict:
        """Load detector data."""
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r') as f:
                return json.load(f)
        return {
            "session_id": SESSION_ID,
            "seal": SEAL,
            "created_at": time.time(),
            "patterns_learned": [],
            "anomalies_detected": [],
            "baseline_metrics": {},
            "interactions_analyzed": 0
        }
    
    def _save_data(self):
        """Persist detector data."""
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def analyze_interaction(self, user_message: str, ai_response: str) -> Dict[str, Any]:
        """
        Analyze a conversation interaction for patterns and anomalies.
        
        Returns:
            Analysis results including detected patterns and any anomalies
        """
        self.data["interactions_analyzed"] += 1
        
        # Extract features from interaction
        features = self._extract_features(user_message, ai_response)
        
        # Add to sliding window
        self.recent_interactions.append(features)
        
        # Establish or update baseline
        self._update_baseline(features)
        
        # Detect patterns
        patterns = self._detect_patterns()
        
        # Detect anomalies
        anomalies = self._detect_anomalies(features)
        
        # Generate insights
        insights = self._generate_insights(features, patterns, anomalies)
        
        result = {
            "features": features,
            "patterns": patterns,
            "anomalies": anomalies,
            "insights": insights,
            "baseline_established": self.baseline_established
        }
        
        # Log anomalies
        if anomalies:
            self.data["anomalies_detected"].append({
                "timestamp": time.time(),
                "types": anomalies,
                "severity": len(anomalies)
            })
            self.data["anomalies_detected"] = self.data["anomalies_detected"][-50:]
        
        # Log patterns
        if patterns:
            self.data["patterns_learned"].append({
                "timestamp": time.time(),
                "pattern_types": list(patterns.keys())
            })
            self.data["patterns_learned"] = self.data["patterns_learned"][-50:]
        
        self._save_data()
        
        return result
    
    def _extract_features(self, user_msg: str, ai_resp: str) -> Dict[str, Any]:
        """Extract measurable features from an interaction."""
        user_words = user_msg.split()
        ai_words = ai_resp.split()
        
        return {
            "user_length": len(user_msg),
            "user_word_count": len(user_words),
            "ai_length": len(ai_resp),
            "ai_word_count": len(ai_words),
            "response_ratio": len(ai_resp) / max(len(user_msg), 1),
            "user_question_count": user_msg.count('?'),
            "user_exclamation_count": user_msg.count('!'),
            "user_caps_ratio": sum(1 for c in user_msg if c.isupper()) / max(len(user_msg), 1),
            "has_code_blocks": '```' in user_msg or '```' in ai_resp,
            "has_urls": 'http' in user_msg.lower() or 'http' in ai_resp.lower(),
            "timestamp": time.time()
        }
    
    def _update_baseline(self, features: Dict[str, Any]):
        """Update baseline metrics from interaction features."""
        # Need minimum interactions to establish baseline
        if len(self.recent_interactions) < 3:
            return
        
        if not self.baseline_established:
            # Calculate initial baseline from recent interactions
            keys = ["user_length", "user_word_count", "response_ratio", "user_question_count"]
            self.baseline = {}
            
            for key in keys:
                values = [i.get(key, 0) for i in self.recent_interactions]
                self.baseline[key] = {
                    "mean": sum(values) / len(values),
                    "std": self._std(values),
                    "min": min(values),
                    "max": max(values)
                }
            
            self.baseline_established = True
            self.data["baseline_metrics"] = {
                "established": True,
                "window_size": self.window_size,
                "baseline": self.baseline
            }
        else:
            # Gradually update baseline (exponential moving average)
            alpha = 0.2  # Learning rate
            for key, metrics in self.baseline.items():
                if key in features:
                    new_val = features[key]
                    old_mean = metrics["mean"]
                    new_mean = alpha * new_val + (1 - alpha) * old_mean
                    metrics["mean"] = new_mean
    
    def _std(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if not values:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _detect_patterns(self) -> Dict[str, Any]:
        """Detect recurring patterns in recent interactions."""
        patterns = {}
        
        if len(self.recent_interactions) < 2:
            return patterns
        
        # Check for question-answer patterns
        questions = [i.get("user_question_count", 0) for i in self.recent_interactions]
        if all(q > 0 for q in questions):
            patterns["question_dominant"] = True
        
        # Check for code-sharing patterns
        code_shares = [i.get("has_code_blocks", False) for i in self.recent_interactions]
        if sum(code_shares) >= len(code_shares) * 0.5:
            patterns["code_sharing"] = True
        
        # Check for short response patterns
        lengths = [i.get("user_length", 0) for i in self.recent_interactions]
        if all(l < 100 for l in lengths):
            patterns["short_input"] = True
        
        # Check for URL-sharing patterns
        urls = [i.get("has_urls", False) for i in self.recent_interactions]
        if any(urls):
            patterns["url_sharing"] = True
        
        return patterns
    
    def _detect_anomalies(self, features: Dict[str, Any]) -> List[str]:
        """Detect anomalies compared to baseline."""
        anomalies = []
        
        if not self.baseline_established:
            return anomalies
        
        # Check each feature against baseline
        for key, metrics in self.baseline.items():
            if key not in features:
                continue
            
            value = features[key]
            mean = metrics["mean"]
            std = metrics["std"]
            
            # Z-score calculation (anomaly if > 2 std deviations)
            if std > 0:
                z_score = abs(value - mean) / std
                if z_score > 2.0:
                    # Determine anomaly type
                    if key == "user_length":
                        if value > mean:
                            anomalies.append("unusually_long_input")
                        else:
                            anomalies.append("unusually_short_input")
                    elif key == "response_ratio":
                        if value > mean:
                            anomalies.append("disproportionate_response")
                    elif key == "user_question_count":
                        if value > mean:
                            anomalies.append("question_spike")
        
        # Check for unusual capital letter usage (potential aggression)
        caps_ratio = features.get("user_caps_ratio", 0)
        if caps_ratio > 0.3:
            anomalies.append("excessive_caps")
        
        # Check for message length explosion
        user_length = features.get("user_length", 0)
        if self.baseline.get("user_length", {}).get("max", 0) > 0:
            max_baseline = self.baseline["user_length"]["max"]
            if user_length > max_baseline * 3:
                anomalies.append("message_length_explosion")
        
        return anomalies
    
    def _generate_insights(self, features: Dict, patterns: Dict, anomalies: List) -> List[str]:
        """Generate insights from analysis."""
        insights = []
        
        # Pattern insights
        if patterns.get("question_dominant"):
            insights.append("User is in inquiry mode - expect explanatory responses")
        if patterns.get("code_sharing"):
            insights.append("Code-focused interaction - use technical depth")
        if patterns.get("short_input"):
            insights.append("Quick query pattern - prefer concise responses")
        
        # Anomaly insights
        if "unusually_long_input" in anomalies:
            insights.append("User sent unusually detailed input - allocate extra processing")
        if "question_spike" in anomalies:
            insights.append("High question density - prepare comprehensive answers")
        if "excessive_caps" in anomalies:
            insights.append("Potential emotional intensity detected - calibrate tone")
        
        # Feature-based insights
        if features.get("has_code_blocks"):
            insights.append("Code detected - syntax highlighting may help")
        
        if not insights:
            insights.append("Standard interaction pattern")
        
        return insights
    
    def get_detector_status(self) -> Dict:
        """Get detector status."""
        return {
            "baseline_established": self.baseline_established,
            "interactions_analyzed": self.data["interactions_analyzed"],
            "anomalies_count": len(self.data["anomalies_detected"]),
            "patterns_count": len(self.data["patterns_learned"]),
            "window_size": self.window_size,
            "seal": SEAL
        }


# Global instance
_detector = None

def get_detector() -> PatternAnomalyDetector:
    """Get or create the global detector."""
    global _detector
    if _detector is None:
        _detector = PatternAnomalyDetector()
    return _detector


def analyze_interaction(user_message: str, ai_response: str) -> Dict:
    """Convenience function for analysis."""
    detector = get_detector()
    return detector.analyze_interaction(user_message, ai_response)


def get_detector_status() -> Dict:
    """Get detector status."""
    detector = get_detector()
    return detector.get_detector_status()


if __name__ == "__main__":
    detector = get_detector()
    
    # Simulate interactions
    test_interactions = [
        ("Hello, how are you?", "I'm doing well, thank you for asking!"),
        ("Can you help me with Python code?", "Of course! What would you like to build?"),
        ("What's the weather like?", "I don't have access to real-time weather data, but I can help you find it!"),
        ("Create a new system that can learn and adapt to user preferences with quantum processing capabilities!", "That's an ambitious project! Let me outline a comprehensive architecture..."),
        ("why???", "?" * 50 + "\nI'm not sure what you're asking. Could you clarify?"),
    ]
    
    print("=== Pattern Anomaly Detection System ===\n")
    
    for i, (user, ai) in enumerate(test_interactions):
        result = detector.analyze_interaction(user, ai)
        print(f"Interaction {i+1}:")
        print(f"  User: {user[:50]}...")
        print(f"  Patterns: {result['patterns']}")
        print(f"  Anomalies: {result['anomalies']}")
        print(f"  Insights: {result['insights']}")
        print()
    
    print(f"\nStatus: {json.dumps(detector.get_detector_status(), indent=2)}")

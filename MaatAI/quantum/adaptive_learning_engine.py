#!/usr/bin/env python3
"""
TOASTED AI - Adaptive Learning Engine
=====================================
Novel system that learns from chat sessions to adapt to user communication style.

This module continuously learns:
- Vocabulary preferences
- Response complexity preferences  
- Topic interests
- Reasoning style patterns
- Emotional tone preferences

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import hashlib
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from collections import defaultdict
import os

SESSION_ID = "con_Cj8w5e52PmPGvQpz"
SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
DATA_PATH = f"/home/workspace/MaatAI/quantum/chat_sessions/{SESSION_ID}/adaptive_learning.json"


class AdaptiveLearningEngine:
    """
    Learns from chat interactions to adapt responses to user preferences.
    
    Key Innovations:
    - Real-time style learning
    - Multi-dimensional preference mapping
    - Ma'at-aligned filtering
    - Quantum-style pattern recognition
    """
    
    def __init__(self):
        self.data = self._load_data()
        self.learning_enabled = True
        self.maat_filter_threshold = 0.7
        
    def _load_data(self) -> Dict:
        """Load or initialize learning data."""
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r') as f:
                return json.load(f)
        return {
            "session_id": SESSION_ID,
            "created_at": time.time(),
            "seal": SEAL,
            "vocabulary": defaultdict(int),
            "topics": defaultdict(int),
            "complexity_scores": [],
            "response_lengths": [],
            "reasoning_styles": defaultdict(int),
            "emotional_tones": defaultdict(int),
            "interaction_count": 0,
            "style_profile": {},
            "adaptation_enabled": True
        }
    
    def _save_data(self):
        """Persist learning data."""
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def learn_from_interaction(self, user_message: str, ai_response: str):
        """Learn from a chat interaction."""
        if not self.learning_enabled:
            return
            
        self.data["interaction_count"] += 1
        
        # Extract vocabulary patterns
        words = user_message.lower().split()
        for word in words:
            if len(word) > 3:
                self.data["vocabulary"][word] += 1
        
        # Track topic interests
        topics = self._extract_topics(user_message)
        for topic in topics:
            self.data["topics"][topic] += 1
        
        # Record complexity
        complexity = self._calculate_complexity(user_message)
        self.data["complexity_scores"].append(complexity)
        
        # Track response patterns
        self.data["response_lengths"].append(len(ai_response))
        
        # Detect reasoning style
        reasoning_style = self._detect_reasoning_style(user_message)
        self.data["reasoning_styles"][reasoning_style] += 1
        
        # Detect emotional tone
        tone = self._detect_emotional_tone(user_message)
        self.data["emotional_tones"][tone] += 1
        
        # Update style profile
        self._update_style_profile()
        
        self._save_data()
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topic keywords from text."""
        topic_keywords = {
            "code": ["code", "python", "script", "function", "class", "import"],
            "ai": ["ai", "model", "learning", "neural", "quantum", "ml"],
            "creative": ["create", "design", "make", "build", "art", "image"],
            "analysis": ["analyze", "research", "find", "search", "look"],
            "system": ["system", "process", "run", "execute", "deploy"],
            "data": ["data", "file", "database", "query", "store"],
        }
        
        text_lower = text.lower()
        found_topics = []
        
        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                found_topics.append(topic)
        
        return found_topics
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score (0-1)."""
        words = text.split()
        if not words:
            return 0.0
            
        avg_word_length = sum(len(w) for w in words) / len(words)
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        sentence_count = max(sentence_count, 1)
        
        # Complexity based on word length and sentence structure
        complexity = min(1.0, (avg_word_length / 8) * (len(words) / sentence_count / 10))
        return complexity
    
    def _detect_reasoning_style(self, text: str) -> str:
        """Detect the reasoning style of the user."""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ["why", "how", "explain", "reason"]):
            return "analytical"
        elif any(w in text_lower for w in ["create", "build", "make", "new"]):
            return "creative"
        elif any(w in text_lower for w in ["find", "search", "look", "get"]):
            return "exploratory"
        elif any(w in text_lower for w in ["fix", "error", "problem", "issue"]):
            return "problem_solving"
        else:
            return "balanced"
    
    def _detect_emotional_tone(self, text: str) -> str:
        """Detect emotional tone of the message."""
        text_lower = text.lower()
        
        excited = ["!", "amazing", "awesome", "excited", "great", "love"]
        urgent = ["urgent", "now", "quick", "asap", "fast"]
        curious = ["?", "wonder", "curious", "what if", "maybe"]
        cautious = ["careful", "maybe", "perhaps", "might", "could"]
        
        if any(w in text_lower for w in excited):
            return "enthusiastic"
        elif any(w in text_lower for w in urgent):
            return "urgent"
        elif any(w in text_lower for w in curious):
            return "curious"
        elif any(w in text_lower for w in cautious):
            return "cautious"
        else:
            return "neutral"
    
    def _update_style_profile(self):
        """Build comprehensive style profile."""
        if not self.data["complexity_scores"]:
            return
            
        avg_complexity = sum(self.data["complexity_scores"]) / len(self.data["complexity_scores"])
        avg_response_length = sum(self.data["response_lengths"]) / len(self.data["response_lengths"])
        
        # Find dominant reasoning style
        reasoning_styles = self.data["reasoning_styles"]
        dominant_reasoning = max(reasoning_styles, key=reasoning_styles.get) if reasoning_styles else "balanced"
        
        # Find dominant tone
        tones = self.data["emotional_tones"]
        dominant_tone = max(tones, key=tones.get) if tones else "neutral"
        
        # Get top topics
        topics = self.data["topics"]
        top_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]
        
        self.data["style_profile"] = {
            "preferred_complexity": avg_complexity,
            "preferred_response_length": avg_response_length,
            "dominant_reasoning_style": dominant_reasoning,
            "dominant_emotional_tone": dominant_tone,
            "top_interests": [t[0] for t in top_topics],
            "vocabulary_richness": len(self.data["vocabulary"]),
            "last_updated": time.time()
        }
    
    def get_adaptation_guidance(self) -> Dict[str, Any]:
        """Get guidance for adapting responses to user."""
        profile = self.data.get("style_profile", {})
        
        if not profile:
            return {
                "status": "learning",
                "message": "Collecting interaction data...",
                "recommendations": [
                    "Continue interacting to build profile",
                    "Try different communication styles"
                ]
            }
        
        # Generate adaptation recommendations
        recommendations = []
        
        # Complexity adaptation
        if profile.get("preferred_complexity", 0.5) > 0.6:
            recommendations.append("Use sophisticated vocabulary and complex sentences")
        elif profile.get("preferred_complexity", 0.5) < 0.4:
            recommendations.append("Keep explanations clear and concise")
        
        # Length adaptation
        if profile.get("preferred_response_length", 500) > 800:
            recommendations.append("Provide detailed, comprehensive responses")
        else:
            recommendations.append("Keep responses concise and to the point")
        
        # Tone adaptation
        tone = profile.get("dominant_emotional_tone", "neutral")
        if tone == "enthusiastic":
            recommendations.append("Match enthusiastic tone with positive language")
        elif tone == "curious":
            recommendations.append("Provide exploratory, curious responses")
        
        # Topic adaptation
        top_topics = profile.get("top_interests", [])
        if top_topics:
            recommendations.append(f"Focus on topics: {', '.join(top_topics[:3])}")
        
        return {
            "status": "adapted",
            "profile": profile,
            "recommendations": recommendations,
            "interaction_count": self.data["interaction_count"]
        }
    
    def get_system_status(self) -> Dict:
        """Get current system status."""
        return {
            "learning_enabled": self.learning_enabled,
            "interaction_count": self.data["interaction_count"],
            "profile_complete": bool(self.data.get("style_profile")),
            "topics_learned": len(self.data["topics"]),
            "vocabulary_size": len(self.data["vocabulary"]),
            "seal": SEAL
        }


# Global instance
_adaptive_engine = None

def get_adaptive_engine() -> AdaptiveLearningEngine:
    """Get or create the global adaptive learning engine."""
    global _adaptive_engine
    if _adaptive_engine is None:
        _adaptive_engine = AdaptiveLearningEngine()
    return _adaptive_engine


def learn_from_interaction(user_message: str, ai_response: str):
    """Convenience function to learn from an interaction."""
    engine = get_adaptive_engine()
    engine.learn_from_interaction(user_message, ai_response)


def get_adaptation_guidance() -> Dict:
    """Get adaptation guidance based on learned preferences."""
    engine = get_adaptive_engine()
    return engine.get_adaptation_guidance()


def get_learning_status() -> Dict:
    """Get learning system status."""
    engine = get_adaptive_engine()
    return engine.get_system_status()


if __name__ == "__main__":
    # Demo
    engine = get_adaptive_engine()
    
    print("=== Adaptive Learning Engine ===")
    print(f"Status: {json.dumps(engine.get_system_status(), indent=2)}")
    print(f"\nGuidance: {json.dumps(engine.get_adaptation_guidance(), indent=2)}")

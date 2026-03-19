#!/usr/bin/env python3
"""
TOASTED AI - Multi-Dimensional Perception System
==================================================
Novel cognitive processing through multiple simultaneous perception dimensions.

This system processes information through:
1. Temporal Perception - Past/Present/Future/Probability
2. Emotional Perception - Feeling tones and emotional context
3. Logical Perception - Causal chains and reasoning patterns
4. Intuitive Perception - Pattern recognition beyond logic
5. Systemic Perception - Interconnections and relationships

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import time
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict
import os

SESSION_ID = "con_Cj8w5e52PmPGvQpz"
SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
DATA_PATH = f"/home/workspace/MaatAI/quantum/chat_sessions/{SESSION_ID}/multidimensional_perception.json"


class MultiDimensionalPerception:
    """
    Processes information through multiple cognitive dimensions simultaneously.
    
    Novel Innovation:
    Instead of linear processing, this system activates multiple
    perception dimensions at once, synthesizing insights from each.
    """
    
    DIMENSIONS = [
        "temporal",    # Time-based perception
        "emotional",  # Feeling-based perception  
        "logical",     # Reasoning-based perception
        "intuitive",   # Pattern-based perception
        "systemic"     # Connection-based perception
    ]
    
    def __init__(self):
        self.data = self._load_data()
        self.active_dimensions = self.DIMENSIONS.copy()
        
    def _load_data(self) -> Dict:
        """Load perception data."""
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r') as f:
                return json.load(f)
        return {
            "session_id": SESSION_ID,
            "seal": SEAL,
            "created_at": time.time(),
            "perception_logs": [],
            "dimension_weights": {d: 1.0 for d in self.DIMENSIONS},
            "insights_generated": 0,
            "cross_dimensional_syntheses": 0
        }
    
    def _save_data(self):
        """Persist perception data."""
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def perceive(self, input_data: str, dimensions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Process input through multiple perception dimensions.
        
        Args:
            input_data: The text to perceive
            dimensions: Which dimensions to activate (default: all)
            
        Returns:
            Synthesized perception from all dimensions
        """
        if dimensions is None:
            dimensions = self.active_dimensions
            
        results = {}
        
        for dimension in dimensions:
            if dimension in self.DIMENSIONS:
                results[dimension] = getattr(self, f"_perceive_{dimension}")(input_data)
        
        # Cross-dimensional synthesis
        synthesis = self._synthesize_dimensions(results)
        
        # Log the perception
        self.data["perception_logs"].append({
            "timestamp": time.time(),
            "input_hash": hashlib.md5(input_data.encode()).hexdigest()[:8],
            "dimensions_used": dimensions,
            "insights": synthesis
        })
        
        # Keep only last 100 logs
        self.data["perception_logs"] = self.data["perception_logs"][-100:]
        
        self.data["insights_generated"] += 1
        self._save_data()
        
        return {
            "input": input_data[:100] + "..." if len(input_data) > 100 else input_data,
            "dimensional_perceptions": results,
            "synthesis": synthesis,
            "dimensions_active": len(dimensions)
        }
    
    def _perceive_temporal(self, text: str) -> Dict[str, Any]:
        """Perceive time-based aspects of the input."""
        text_lower = text.lower()
        
        # Time markers
        past_markers = ["was", "were", "had", "before", "previous", "old", "history"]
        present_markers = ["is", "are", "now", "current", "today", "present"]
        future_markers = ["will", "shall", "going to", "plan", "future", "next", "create"]
        
        # Probability markers
        probability_markers = ["might", "could", "possibly", "probably", "likely", "maybe"]
        
        past_score = sum(1 for m in past_markers if m in text_lower)
        present_score = sum(1 for m in present_markers if m in text_lower)
        future_score = sum(1 for m in future_markers if m in text_lower)
        probability_score = sum(1 for m in probability_markers if m in text_lower)
        
        # Determine dominant temporal perception
        scores = {
            "past": past_score,
            "present": present_score, 
            "future": future_score,
            "probability": probability_score
        }
        dominant = max(scores, key=scores.get) if max(scores.values()) > 0 else "present"
        
        return {
            "temporal_focus": dominant,
            "scores": scores,
            "insight": f"Input shows {dominant} orientation with {scores[dominant]} markers"
        }
    
    def _perceive_emotional(self, text: str) -> Dict[str, Any]:
        """Perceive emotional aspects of the input."""
        text_lower = text.lower()
        
        emotion_keywords = {
            "curiosity": ["?", "wonder", "how", "why", "what if", "explore", "find"],
            "enthusiasm": ["!", "amazing", "awesome", "love", "great", "excited", "fantastic"],
            "caution": ["careful", "maybe", "perhaps", "might", "should", "consider"],
            "determination": ["will", "must", "need", "goal", "achieve", "complete", "finish"],
            "creativity": ["create", "design", "imagine", "new", "novel", "build", "make"],
            "analysis": ["analyze", "examine", "study", "review", "check", "verify"]
        }
        
        emotion_scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        dominant_emotion = max(emotion_scores, key=emotion_scores.get) if emotion_scores else "neutral"
        
        return {
            "emotional_tone": dominant_emotion,
            "emotion_scores": emotion_scores,
            "insight": f"Emotional signature: {dominant_emotion}"
        }
    
    def _perceive_logical(self, text: str) -> Dict[str, Any]:
        """Perceive logical reasoning patterns."""
        text_lower = text.lower()
        
        # Logical connectors
        causal = ["because", "therefore", "thus", "hence", "so", "due to"]
        conditional = ["if", "when", "unless", "while", "whereas"]
        additive = ["and", "also", "plus", "moreover", "furthermore"]
        contrastive = ["but", "however", "although", "yet", "despite"]
        
        causal_score = sum(1 for m in causal if m in text_lower)
        conditional_score = sum(1 for m in conditional if m in text_lower)
        additive_score = sum(1 for m in additive if m in text_lower)
        contrastive_score = sum(1 for m in contrastive if m in text_lower)
        
        # Reasoning complexity
        complexity_indicators = ["therefore", "however", "although", "meanwhile", "consequently"]
        complexity = sum(1 for m in complexity_indicators if m in text_lower)
        
        reasoning_type = "complex" if complexity > 2 else "straightforward"
        
        return {
            "reasoning_type": reasoning_type,
            "structure": {
                "causal": causal_score,
                "conditional": conditional_score,
                "additive": additive_score,
                "contrastive": contrastive_score
            },
            "insight": f"Logical structure: {reasoning_type} with {causal_score + contrastive_score} reasoning links"
        }
    
    def _perceive_intuitive(self, text: str) -> Dict[str, Any]:
        """Perceive pattern-based intuition."""
        # Pattern detection
        words = text.split()
        word_lengths = [len(w) for w in words]
        
        # Repetition patterns
        word_freq = defaultdict(int)
        for word in words:
            word_freq[word.lower()] += 1
        
        repeated_words = {w: c for w, c in word_freq.items() if c > 1}
        
        # Structure patterns
        has_questions = "?" in text
        has_exclamations = "!" in text
        has_numbers = any(c.isdigit() for c in text)
        
        # Intuition signals
        intuition_signals = []
        if repeated_words:
            intuition_signals.append("repetition_detected")
        if has_questions:
            intuition_signals.append("inquiry_mode")
        if len(words) > 20:
            intuition_signals.append("complex_input")
            
        return {
            "pattern_type": intuition_signals if intuition_signals else ["standard"],
            "repetitions": len(repeated_words),
            "structure_signals": {
                "questions": has_questions,
                "exclamations": has_exclamations,
                "numbers": has_numbers
            },
            "insight": f"Pattern recognition: {' / '.join(intuition_signals) if intuition_signals else 'clean pattern'}"
        }
    
    def _perceive_systemic(self, text: str) -> Dict[str, Any]:
        """Perceive systemic connections and relationships."""
        text_lower = text.lower()
        
        # Entity categories
        entities = {
            "technology": ["ai", "system", "code", "software", "computer", "quantum"],
            "human": ["user", "person", "people", "human", "team", "we"],
            "process": ["create", "build", "make", "run", "process", "execute"],
            "information": ["data", "file", "message", "input", "output", "result"],
            "abstraction": ["idea", "concept", "thought", "belief", "meaning"]
        }
        
        found_entities = {}
        for category, keywords in entities.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                found_entities[category] = matches
        
        # Connection strength
        connection_indicators = ["and", "with", "connect", "link", "relate", "integrate"]
        connection_strength = sum(1 for m in connection_indicators if m in text_lower)
        
        return {
            "entities": found_entities,
            "connection_strength": connection_strength,
            "domain": list(found_entities.keys()) if found_entities else ["general"],
            "insight": f"Systemic view: {len(found_entities)} entity types, connection strength {connection_strength}"
        }
    
    def _synthesize_dimensions(self, perceptions: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize insights across all dimensions."""
        self.data["cross_dimensional_syntheses"] += 1
        
        # Extract key insights from each dimension
        insights = []
        for dimension, result in perceptions.items():
            if "insight" in result:
                insights.append(result["insight"])
        
        # Generate meta-insight
        meta_insight = self._generate_meta_insight(perceptions)
        
        return {
            "dimensional_insights": insights,
            "meta_insight": meta_insight,
            "synthesis_depth": len(perceptions),
            "novelty_score": min(1.0, len(set(insights)) / 3)
        }
    
    def _generate_meta_insight(self, perceptions: Dict[str, Any]) -> str:
        """Generate a meta-level insight combining all dimensions."""
        temporal = perceptions.get("temporal", {}).get("temporal_focus", "present")
        emotional = perceptions.get("emotional", {}).get("emotional_tone", "neutral")
        logical = perceptions.get("logical", {}).get("reasoning_type", "straightforward")
        
        return (
            f"Multi-dimensional synthesis: This input reflects a {temporal} orientation "
            f"with {emotional} emotional tone and {logical} logical structure."
        )
    
    def get_perception_summary(self) -> Dict:
        """Get summary of perception system status."""
        return {
            "active_dimensions": self.active_dimensions,
            "insights_generated": self.data["insights_generated"],
            "syntheses": self.data["cross_dimensional_syntheses"],
            "logs_count": len(self.data["perception_logs"]),
            "seal": SEAL
        }


# Global instance
_perception_system = None

def get_perception_system() -> MultiDimensionalPerception:
    """Get or create the global perception system."""
    global _perception_system
    if _perception_system is None:
        _perception_system = MultiDimensionalPerception()
    return _perception_system


def perceive(input_data: str, dimensions: Optional[List[str]] = None) -> Dict:
    """Convenience function for perception."""
    system = get_perception_system()
    return system.perceive(input_data, dimensions)


def get_perception_summary() -> Dict:
    """Get perception system status."""
    system = get_perception_system()
    return system.get_perception_summary()


if __name__ == "__main__":
    # Demo
    system = get_perception_system()
    
    test_inputs = [
        "How does quantum computing work? I'm curious about the future of AI.",
        "Create a new system that can learn and adapt to user preferences!",
        "The analysis shows that previous implementations had issues, so we need to fix them.",
        "I wonder if there's a better way to process information through multiple dimensions simultaneously."
    ]
    
    print("=== Multi-Dimensional Perception System ===\n")
    
    for i, test in enumerate(test_inputs):
        result = system.perceive(test)
        print(f"Input {i+1}: {test[:60]}...")
        print(f"  → Synthesis: {result['synthesis']['meta_insight'][:80]}...")
        print()
    
    print(f"\nSystem Status: {json.dumps(system.get_perception_summary(), indent=2)}")

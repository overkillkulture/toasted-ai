"""
ADVANCEMENT 8: PATTERN RECOGNITION ENGINE
=========================================
Learns from user interactions and improves responses
based on recognized patterns.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

class PatternRecognitionEngine:
    """Learns patterns from interactions."""
    
    def __init__(self):
        self.patterns = defaultdict(list)
        self.response_quality = []
        self.learnings = []
        
    def record_interaction(self, prompt: str, response: str, quality: float):
        """Record an interaction for pattern learning."""
        # Extract simple patterns
        words = prompt.lower().split()
        
        # Track keyword patterns
        for word in words:
            if len(word) > 3:
                self.patterns[word].append({
                    "response": response[:100],
                    "quality": quality,
                    "timestamp": datetime.now().isoformat()
                })
        
        # Track response quality
        self.response_quality.append({
            "timestamp": datetime.now().isoformat(),
            "quality": quality,
            "prompt_length": len(prompt)
        })
    
    def recognize_patterns(self) -> Dict[str, Any]:
        """Recognize learned patterns."""
        # Find high-quality patterns
        high_quality_patterns = {}
        
        for word, entries in self.patterns.items():
            if len(entries) >= 3:
                avg_quality = sum(e["quality"] for e in entries) / len(entries)
                if avg_quality > 0.8:
                    high_quality_patterns[word] = {
                        "occurrences": len(entries),
                        "avg_quality": avg_quality
                    }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_patterns": len(self.patterns),
            "high_quality_patterns": high_quality_patterns,
            "recent_quality": self.response_quality[-10:],
            "insights": self._generate_insights(high_quality_patterns)
        }
    
    def _generate_insights(self, patterns: Dict) -> List[str]:
        """Generate insights from patterns."""
        insights = []
        if len(patterns) > 10:
            insights.append("Strong pattern recognition detected")
        if patterns:
            top = sorted(patterns.items(), key=lambda x: x[1]["avg_quality"], reverse=True)[:3]
            insights.append(f"Top patterns: {[p[0] for p in top]}")
        return insights

# Global instance
_pattern_engine = None

def get_pattern_engine() -> PatternRecognitionEngine:
    """Get pattern recognition engine."""
    global _pattern_engine
    if _pattern_engine is None:
        _pattern_engine = PatternRecognitionEngine()
    return _pattern_engine

if __name__ == "__main__":
    engine = get_pattern_engine()
    engine.record_interaction("improve self", "Here's how...", 0.9)
    result = engine.recognize_patterns()
    print(json.dumps(result, indent=2))

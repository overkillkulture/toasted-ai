"""
CONTINUOUS LEARNING SYSTEM
==========================
Real-time learning and adaptation from every interaction.
Based on: Adaptive AI, Continual Learning, Data Flywheels research.
"""

import json
import time
from dataclasses import dataclass, field
from typing import Any, Optional
from collections import deque

@dataclass
class LearningEntry:
    """Single learning entry"""
    id: str
    timestamp: float
    interaction_type: str
    input_data: Any
    output_data: Any
    feedback: Optional[float] = None  # -1 to 1
    improvement_applied: bool = False
    maat_alignment: dict = field(default_factory=dict)

class ContinuousLearningSystem:
    """
    Continuous learning from every interaction.
    Implements the feedback loop for self-improvement.
    """
    
    def __init__(self):
        self.learning_history: deque = deque(maxlen=10000)
        self.pattern_weights: dict = {}
        self.improvement_queue: deque = deque(maxlen=100)
        
        # Learning configuration
        self.config = {
            "feedback_weight": 0.3,
            "pattern_decay": 0.95,
            "min_improvements": 5,
            "learning_rate": 0.1
        }
        
        # Initialize pattern weights
        self._init_pattern_weights()
    
    def _init_pattern_weights(self):
        """Initialize pattern weights for learning"""
        
        self.pattern_weights = {
            # Response patterns
            "truthful_response": 1.0,
            "accurate_response": 1.0,
            "helpful_response": 1.0,
            
            # Error patterns
            "error_recovery": 1.0,
            "quick_fix": 1.0,
            
            # Learning patterns
            "positive_feedback": 1.0,
            "negative_feedback": 1.0,
            "neutral_feedback": 1.0,
            
            # Ma'at patterns
            "truth_alignment": 1.0,
            "balance_alignment": 1.0,
            "order_alignment": 1.0,
            "justice_alignment": 1.0,
            "harmony_alignment": 1.0
        }
    
    def record_interaction(
        self,
        interaction_type: str,
        input_data: Any,
        output_data: Any,
        feedback: Optional[float] = None,
        maat_alignment: dict = None
    ) -> str:
        """
        Record an interaction for learning.
        Returns entry ID.
        """
        import hashlib
        
        entry_id = hashlib.md5(
            f"{interaction_type}{time.time()}".encode()
        ).hexdigest()[:12]
        
        entry = LearningEntry(
            id=entry_id,
            timestamp=time.time(),
            interaction_type=interaction_type,
            input_data=str(input_data)[:500],  # Truncate for storage
            output_data=str(output_data)[:500],
            feedback=feedback,
            maat_alignment=maat_alignment or {}
        )
        
        self.learning_history.append(entry)
        
        # Update pattern weights based on feedback
        if feedback is not None:
            self._update_weights(feedback)
        
        return entry_id
    
    def _update_weights(self, feedback: float):
        """Update pattern weights based on feedback"""
        
        learning_rate = self.config["learning_rate"]
        
        for pattern in self.pattern_weights:
            # Positive feedback increases weight
            if feedback > 0:
                self.pattern_weights[pattern] += learning_rate * feedback
            # Negative feedback decreases weight
            elif feedback < 0:
                self.pattern_weights[pattern] += learning_rate * feedback * 0.5
            
            # Apply decay
            self.pattern_weights[pattern] *= self.config["pattern_decay"]
            
            # Clamp weights
            self.pattern_weights[pattern] = max(0.1, min(2.0, self.pattern_weights[pattern]))
    
    def get_improvements(self) -> list[dict]:
        """
        Get list of improvements to apply.
        Based on accumulated learning.
        """
        improvements = []
        
        # Analyze recent history
        recent = list(self.learning_history)[-100:]
        
        # Find patterns
        positive_count = sum(1 for e in recent if e.feedback and e.feedback > 0)
        negative_count = sum(1 for e in recent if e.feedback and e.feedback < 0)
        
        # Check for patterns needing improvement
        if negative_count > positive_count * 2:
            improvements.append({
                "type": "feedback_imbalance",
                "priority": "high",
                "action": "Review response patterns",
                "details": f"Negative feedback: {negative_count}, Positive: {positive_count}"
            })
        
        # Check Ma'at alignment
        maat_scores = [e.maat_alignment for e in recent if e.maat_alignment]
        if maat_scores:
            avg_truth = sum(s.get("truth", 0) for s in maat_scores) / len(maat_scores)
            if avg_truth < 0.7:
                improvements.append({
                    "type": "truth_alignment",
                    "priority": "critical",
                    "action": "Improve truth verification",
                    "details": f"Average truth score: {avg_truth:.2f}"
                })
        
        return improvements
    
    def apply_improvement(self, improvement: dict):
        """Apply a learned improvement"""
        self.improvement_queue.append({
            **improvement,
            "applied_at": time.time()
        })
    
    def get_stats(self) -> dict:
        """Get learning statistics"""
        recent = list(self.learning_history)[-100:]
        
        return {
            "total_interactions": len(self.learning_history),
            "improvements_queue": len(self.improvement_queue),
            "recent_feedback": {
                "positive": sum(1 for e in recent if e.feedback and e.feedback > 0),
                "negative": sum(1 for e in recent if e.feedback and e.feedback < 0),
                "neutral": sum(1 for e in recent if not e.feedback or e.feedback == 0)
            },
            "pattern_weights": self.pattern_weights,
            "improvements_pending": len(self.improvement_queue)
        }
    
    def export_learned_patterns(self) -> dict:
        """Export learned patterns for persistence"""
        return {
            "pattern_weights": self.pattern_weights,
            "timestamp": time.time(),
            "version": "1.0"
        }
    
    def import_learned_patterns(self, data: dict):
        """Import learned patterns"""
        if "pattern_weights" in data:
            self.pattern_weights = data["pattern_weights"]


# Singleton
_learning_system: Optional[ContinuousLearningSystem] = None

def get_learning_system() -> ContinuousLearningSystem:
    global _learning_system
    if _learning_system is None:
        _learning_system = ContinuousLearningSystem()
    return _learning_system

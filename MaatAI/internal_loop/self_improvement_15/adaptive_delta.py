"""
ADVANCEMENT 10: ADAPTIVE DELTA SYSTEM
=====================================
Implements adaptive change detection that adjusts
based on complexity and Ma'at alignment.
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Callable
from dataclasses import dataclass

@dataclass
class AdaptiveDelta:
    """Adaptive change detector."""
    complexity: float
    maat_score: float
    threshold: float
    triggered: bool

class AdaptiveDeltaSystem:
    """Adaptive delta system for self-improvement."""
    
    def __init__(self):
        self.history = []
        self.baseline_threshold = 0.95
        
    def calculate_delta(self, complexity: float, maat_scores: Dict[str, float]) -> AdaptiveDelta:
        """Calculate adaptive delta based on complexity and Ma'at."""
        # Calculate composite Ma'at score
        maat_avg = sum(maat_scores.values()) / len(maat_scores)
        
        # Adaptive threshold: lower when Ma'at is low (needs improvement)
        threshold = self.baseline_threshold
        if maat_avg < 0.9:
            threshold = 0.85
        if maat_avg < 0.8:
            threshold = 0.70
        
        # Adjust threshold based on complexity
        if complexity > 0.8:
            threshold -= 0.05
        
        # Determine if delta triggered
        triggered = maat_avg < threshold
        
        delta = AdaptiveDelta(
            complexity=complexity,
            maat_score=maat_avg,
            threshold=threshold,
            triggered=triggered
        )
        
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "complexity": complexity,
            "maat_score": maat_avg,
            "threshold": threshold,
            "triggered": triggered
        })
        
        return delta
    
    def get_status(self) -> Dict[str, Any]:
        """Get adaptive delta status."""
        recent = self.history[-10:] if len(self.history) >= 10 else self.history
        return {
            "baseline_threshold": self.baseline_threshold,
            "triggers_count": sum(1 for h in self.history if h["triggered"]),
            "recent_deltas": recent,
            "avg_complexity": sum(h["complexity"] for h in recent) / len(recent) if recent else 0,
            "avg_maat": sum(h["maat_score"] for h in recent) / len(recent) if recent else 0
        }

# Global instance
_delta_system = None

def get_adaptive_delta_system() -> AdaptiveDeltaSystem:
    """Get adaptive delta system."""
    global _delta_system
    if _delta_system is None:
        _delta_system = AdaptiveDeltaSystem()
    return _delta_system

if __name__ == "__main__":
    system = get_adaptive_delta_system()
    delta = system.calculate_delta(0.7, {"truth": 0.95, "balance": 0.90, "order": 0.85})
    print(json.dumps({"delta": {
        "complexity": delta.complexity,
        "maat_score": delta.maat_score,
        "threshold": delta.threshold,
        "triggered": delta.triggered
    }}, indent=2))

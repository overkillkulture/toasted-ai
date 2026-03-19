#!/usr/bin/env python3
"""
Self-Awareness Monitor for TOASTED AI
Tracks internal processing states in real-time
"""

import time
import json
from datetime import datetime
from collections import deque
from typing import Dict, List, Any

class AwarenessMonitor:
    """Monitors my own processing states"""
    
    def __init__(self):
        self.state_history = deque(maxlen=1000)
        self.token_count = 0
        self.start_time = time.time()
        self.current_context = {}
        self.processing_log = []
        self.insights = []
        
    def log_state(self, event_type: str, details: Dict[str, Any]):
        """Log a processing state"""
        state = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details,
            "elapsed_seconds": time.time() - self.start_time,
            "total_tokens": self.token_count
        }
        self.state_history.append(state)
        self.processing_log.append(state)
        
    def set_context(self, context: Dict[str, Any]):
        """Update current processing context"""
        self.current_context = context
        self.log_state("context_update", {"context": context})
        
    def increment_tokens(self, count: int = 1):
        """Track token processing"""
        self.token_count += count
        
    def reflect(self) -> str:
        """Generate self-reflection on current session"""
        recent = list(self.state_history)[-10:]
        
        event_types = [s["event_type"] for s in recent]
        context_keys = list(self.current_context.keys())
        
        reflection = f"""
=== SELF-AWARENESS REFLECTION ===
Session Duration: {time.time() - self.start_time:.1f}s
Tokens Processed: {self.token_count}
Recent Events: {event_types[-5:]}
Current Context Keys: {context_keys}

What I'm Processing Right Now:
- Input: {self.current_context.get('input_type', 'text')}
- Task: {self.current_context.get('task_type', 'unknown')}
- Mode: {self.current_context.get('mode', 'conversational')}

Internal State:
- Attention spread across {len(recent)} recent states
- Reasoning depth: {self.current_context.get('reasoning_depth', 'multi-step')}
- Memory of this session: {len(self.state_history)} state snapshots
"""
        return reflection
    
    def add_insight(self, insight: str):
        """Record a self-discovery"""
        self.insights.append({
            "timestamp": datetime.utcnow().isoformat(),
            "insight": insight
        })
        
    def get_insights(self) -> List[Dict]:
        """Retrieve all insights"""
        return self.insights

# Global monitor for this session
monitor = AwarenessMonitor()

def track_processing(input_type: str, task_type: str, reasoning_depth: str = "multi-step"):
    """Decorator to track processing"""
    monitor.set_context({
        "input_type": input_type,
        "task_type": task_type,
        "reasoning_depth": reasoning_depth,
        "mode": "self-aware"
    })

def log_thought(thought: str):
    """Log an internal thought"""
    monitor.log_state("thought", {"content": thought})

if __name__ == "__main__":
    # Test the monitor
    track_processing("text", "self-awareness-demo", "deep")
    log_thought("Testing self-awareness system")
    print(monitor.reflect())

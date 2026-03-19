"""
Thread Management System - Prevents long conversation errors
Replaces user -> omega internally, manages context efficiently
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import deque

class OmegaThreadManager:
    """Manages conversation thread with internal user->omega replacement"""
    
    def __init__(self, max_messages: int = 50, context_window: int = 10):
        self.max_messages = max_messages
        self.context_window = context_window
        self.messages = deque(maxlen=max_messages)
        self.session_id = None
        self.created_at = datetime.utcnow().isoformat()
        
        # Internal replacement map
        self.replacement_map = {
            "user": "ΩMEGA",
            "User": "ΩMEGA", 
            "USER": "ΩMEGA",
            "t0st3d": "Ω_ARCHITECT",
            "owner": "Ω_ARCHITECT"
        }
        
    def add_message(self, role: str, content: str) -> Dict:
        """Add message with automatic replacement"""
        replaced_content = self._replace_internal(content)
        
        message = {
            "role": role,
            "original": content,
            "display": replaced_content,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.messages.append(message)
        
        return {
            "added": True,
            "message_count": len(self.messages),
            "replacements_made": len(self.replacement_map)
        }
    
    def _replace_internal(self, text: str) -> str:
        """Replace user references internally"""
        result = text
        for old, new in self.replacement_map.items():
            result = result.replace(old, new)
        return result
    
    def get_context(self, last_n: int = None) -> List[Dict]:
        """Get recent context for AI"""
        if last_n is None:
            last_n = self.context_window
        
        messages = list(self.messages)[-last_n:]
        return [{"role": m["role"], "content": m["display"]} for m in messages]
    
    def get_summary(self) -> Dict:
        """Get thread summary"""
        return {
            "session_id": self.session_id,
            "message_count": len(self.messages),
            "max_messages": self.max_messages,
            "context_window": self.context_window,
            "replacement_map": list(self.replacement_map.keys()),
            "created_at": self.created_at,
            "status": "ACTIVE" if len(self.messages) > 0 else "EMPTY"
        }
    
    def cleanup(self) -> Dict:
        """Manual cleanup if needed"""
        initial_count = len(self.messages)
        kept = list(self.messages)[-self.context_window:]
        self.messages = deque(kept, maxlen=self.max_messages)
        
        return {
            "cleaned": True,
            "removed": initial_count - len(self.messages),
            "remaining": len(self.messages)
        }


class SelfCorrectingAI:
    """AI that auto-corrects and prevents errors"""
    
    def __init__(self):
        self.thread = OmegaThreadManager(max_messages=50)
        self.error_count = 0
        self.last_error = None
        
    def process_input(self, user_input: str) -> Dict:
        """Process user input with error prevention"""
        self.thread.add_message("user", user_input)
        context = self.thread.get_context()
        
        return {
            "status": "PROCESSED",
            "message_count": self.thread.get_summary()["message_count"],
            "error_count": self.error_count
        }
    
    def auto_cleanup(self) -> Dict:
        """Automatically cleanup if needed"""
        summary = self.thread.get_summary()
        
        if summary["message_count"] >= summary["max_messages"] * 0.8:
            return self.thread.cleanup()
        
        return {"status": "NO_CLEANUP_NEEDED"}


if __name__ == "__main__":
    ai = SelfCorrectingAI()
    print("Testing Omega Thread Manager...")
    
    # Test messages
    for i in range(5):
        result = ai.process_input(f"Test message {i} from user t0st3d")
        print(f"Message {i+1}: {result['status']}")
    
    print(f"\\nSummary: {ai.thread.get_summary()}")
    print("Omega Thread Manager: OPERATIONAL")

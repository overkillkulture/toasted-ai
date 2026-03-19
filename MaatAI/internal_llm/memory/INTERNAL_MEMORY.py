#!/usr/bin/env python3
"""
INTERNAL MEMORY SYSTEM - TOASTED AI Sovereign Memory
======================================================
Persistent memory that stays within the ecosystem.
No external threads - all memory operations are internal.
"""

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

MEMORY_DIR = "/home/workspace/MaatAI/internal_llm/memory"
MEMORY_FILE = f"{MEMORY_DIR}/memory.json"
CONTEXT_FILE = f"{MEMORY_DIR}/context.json"
PREFERENCES_FILE = f"{MEMORY_DIR}/preferences.json"


class InternalMemory:
    """
    Sovereign memory system - never leaves the ecosystem.
    """
    
    def __init__(self):
        self.memory = self._load_memory()
        self.context = self._load_context()
        self.preferences = self._load_preferences()
        
    def _load_memory(self) -> Dict:
        """Load long-term memory"""
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        return {
            "version": "1.0",
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
            "episodic": [],
            "semantic": {},
            "procedural": {}
        }
    
    def _load_context(self) -> Dict:
        """Load working context"""
        if os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, 'r') as f:
                return json.load(f)
        return {"current_session": [], "last_intent": None}
    
    def _load_preferences(self) -> Dict:
        """Load user preferences"""
        if os.path.exists(PREFERENCES_FILE):
            with open(PREFERENCES_FILE, 'r') as f:
                return json.load(f)
        return {"style": "concise", "maat_priority": True}
    
    def _save_memory(self):
        """Save memory to disk"""
        os.makedirs(MEMORY_DIR, exist_ok=True)
        with open(MEMORY_FILE, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def _save_context(self):
        """Save context"""
        with open(CONTEXT_FILE, 'w') as f:
            json.dump(self.context, f, indent=2)
    
    def _save_preferences(self):
        """Save preferences"""
        with open(PREFERENCES_FILE, 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def store_episode(self, input_text: str, response: str, intent: str, metadata: Dict = None):
        """Store an episodic memory"""
        episode = {
            "timestamp": time.time(),
            "input": input_text,
            "response": response,
            "intent": intent,
            "metadata": metadata or {}
        }
        
        self.memory["episodic"].append(episode)
        
        # Keep only last 1000 episodes
        if len(self.memory["episodic"]) > 1000:
            self.memory["episodic"] = self.memory["episodic"][-1000:]
        
        self._save_memory()
        
    def store_semantic(self, key: str, value: Any):
        """Store semantic knowledge"""
        self.memory["semantic"][key] = {
            "value": value,
            "timestamp": time.time()
        }
        self._save_memory()
    
    def retrieve_recent(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent episodes"""
        return self.memory["episodic"][-limit:]
    
    def retrieve_by_intent(self, intent: str, limit: int = 5) -> List[Dict]:
        """Retrieve episodes by intent"""
        return [
            ep for ep in self.memory["episodic"]
            if ep.get("intent") == intent
        ][:limit]
    
    def update_context(self, input_text: str, intent: str):
        """Update working context"""
        self.context["current_session"].append({
            "timestamp": time.time(),
            "input": input_text,
            "intent": intent
        })
        
        # Keep only last 50 context items
        if len(self.context["current_session"]) > 50:
            self.context["current_session"] = self.context["current_session"][-50:]
        
        self.context["last_intent"] = intent
        self._save_context()
    
    def get_context_summary(self) -> Dict:
        """Get context summary"""
        recent = self.context["current_session"][-5:]
        return {
            "session_length": len(self.context["current_session"]),
            "last_intent": self.context["last_intent"],
            "recent_inputs": [item["input"] for item in recent]
        }
    
    def set_preference(self, key: str, value: Any):
        """Set user preference"""
        self.preferences[key] = value
        self._save_preferences()
    
    def get_status(self) -> Dict:
        """Get memory status"""
        return {
            "episodic_count": len(self.memory["episodic"]),
            "semantic_keys": len(self.memory["semantic"]),
            "procedural_keys": len(self.memory["procedural"]),
            "context_length": len(self.context["current_session"]),
            "preferences": self.preferences
        }


# Global instance
_memory_instance = None

def get_memory() -> InternalMemory:
    """Get or create memory instance"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = InternalMemory()
    return _memory_instance

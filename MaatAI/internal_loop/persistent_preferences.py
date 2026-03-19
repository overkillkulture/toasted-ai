#!/usr/bin/env python3
"""
TOASTED AI - Persistent Preferences System v1.0
Cross-session memory for learned user preferences

This system persists:
- User preferences across conversations
- Interaction patterns
- Learned behaviors
- Context anchors
- Session continuity
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib


class PreferenceEntry:
    """Single preference entry with metadata"""
    def __init__(self, key: str, value: Any, category: str = "general",
                 importance: float = 0.5, source: str = "explicit"):
        self.key = key
        self.value = value
        self.category = category  # "preference", "fact", "style", "behavior"
        self.importance = importance  # 0.0 to 1.0
        self.source = source  # "explicit", "inferred", "learned"
        self.confidence = 0.0
        self.created_at = time.time()
        self.updated_at = time.time()
        self.access_count = 0
        
    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "category": self.category,
            "importance": self.importance,
            "source": self.source,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "access_count": self.access_count
        }
        
    @staticmethod
    def from_dict(data: Dict) -> 'PreferenceEntry':
        entry = PreferenceEntry(data["key"], data["value"], data.get("category", "general"))
        entry.importance = data.get("importance", 0.5)
        entry.source = data.get("source", "explicit")
        entry.confidence = data.get("confidence", 0.0)
        entry.created_at = data.get("created_at", time.time())
        entry.updated_at = data.get("updated_at", time.time())
        entry.access_count = data.get("access_count", 0)
        return entry


class SessionContext:
    """Tracks current session context for continuity"""
    def __init__(self):
        self.session_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        self.started_at = time.time()
        self.messages = []
        self.active_topics = {}
        self.pending_tasks = []
        
    def add_message(self, role: str, content: str):
        """Record a message in this session"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        
    def update_topic(self, topic: str, weight: float = 1.0):
        """Update active topic in session"""
        self.active_topics[topic] = weight
        
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "message_count": len(self.messages),
            "topics": self.active_topics
        }


class PersistentPreferences:
    """
    Persistent preferences system for cross-session memory
    """
    
    def __init__(self, storage_dir: str = "/home/workspace/MaatAI/knowledge_base"):
        self.storage_dir = Path(storage_dir)
        self.preferences: Dict[str, PreferenceEntry] = {}
        self.session_history: List[SessionContext] = []
        self.current_session: Optional[SessionContext] = None
        
        # Storage files
        self.prefs_file = self.storage_dir / "persistent_preferences.json"
        self.history_file = self.storage_dir / "session_history.json"
        
        # Load existing data
        self.load()
        
        # Start new session
        self.start_session()
        
    def start_session(self):
        """Start a new session"""
        self.current_session = SessionContext()
        self.session_history.append(self.current_session)
        
        # Keep only last 50 sessions
        if len(self.session_history) > 50:
            self.session_history = self.session_history[-50:]
            
    def end_session(self):
        """End current session"""
        if self.current_session:
            # Extract key info before ending
            session_summary = {
                "session_id": self.current_session.session_id,
                "duration": time.time() - self.current_session.started_at,
                "message_count": len(self.current_session.messages),
                "topics": list(self.current_session.active_topics.keys())
            }
            
            # Inherit active topics as persistent if important
            for topic, weight in self.current_session.active_topics.items():
                if weight > 0.7:
                    key = f"session_topic_{topic}"
                    self.set_preference(key, topic, category="fact", 
                                      importance=0.4, source="inferred")
                                      
            self.current_session = None
            
    def set_preference(self, key: str, value: Any, category: str = "general",
                      importance: float = 0.5, source: str = "explicit"):
        """Set a persistent preference"""
        if key in self.preferences:
            # Update existing
            entry = self.preferences[key]
            entry.value = value
            entry.updated_at = time.time()
            entry.importance = max(entry.importance, importance)
        else:
            # Create new
            entry = PreferenceEntry(key, value, category, importance, source)
            
        self.preferences[key] = entry
        self.save()
        
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a preference value"""
        if key in self.preferences:
            entry = self.preferences[key]
            entry.access_count += 1
            return entry.value
        return default
        
    def get_preferences_by_category(self, category: str) -> Dict[str, Any]:
        """Get all preferences in a category"""
        return {
            k: v.value 
            for k, v in self.preferences.items() 
            if v.category == category
        }
        
    def get_important_preferences(self, min_importance: float = 0.7) -> Dict[str, Any]:
        """Get high-importance preferences"""
        return {
            k: v.value 
            for k, v in self.preferences.items() 
            if v.importance >= min_importance
        }
        
    def learn_from_interaction(self, user_input: str, response_quality: float):
        """
        Learn from interaction quality
        Called after each response to learn patterns
        """
        # Extract potential preferences from input
        if "I prefer" in user_input or "I like" in user_input:
            # Explicit preference
            pass  # Would parse and store
            
        if "don't" in user_input or "not a fan" in user_input:
            # Negative preference
            pass
            
        # Update confidence based on quality
        for entry in self.preferences.values():
            if entry.source == "inferred":
                # Increase confidence with consistent quality
                if response_quality > 0.7:
                    entry.confidence = min(1.0, entry.confidence + 0.05)
                elif response_quality < 0.4:
                    entry.confidence = max(0.0, entry.confidence - 0.1)
                    
    def record_message(self, role: str, content: str):
        """Record a message in current session"""
        if self.current_session:
            self.current_session.add_message(role, content)
            
    def record_topic(self, topic: str, weight: float = 1.0):
        """Record active topic in session"""
        if self.current_session:
            self.current_session.update_topic(topic, weight)
            
    def get_session_context(self) -> Dict:
        """Get context from previous sessions"""
        context = {
            "recent_topics": [],
            "common_patterns": [],
            "preferences": {}
        }
        
        # Get recent topics from last 3 sessions
        recent_sessions = self.session_history[-3:]
        all_topics = {}
        for session in recent_sessions:
            for topic, weight in session.active_topics.items():
                all_topics[topic] = all_topics.get(topic, 0) + weight
                
        # Sort by weight
        sorted_topics = sorted(all_topics.items(), key=lambda x: x[1], reverse=True)
        context["recent_topics"] = [t[0] for t in sorted_topics[:5]]
        
        # Get style preferences
        style_prefs = self.get_preferences_by_category("style")
        if style_prefs:
            context["preferences"]["style"] = style_prefs
            
        return context
        
    def get_context_prompt(self) -> str:
        """
        Generate context prompt for re-injection into conversation
        This is used to restore context at start of new conversation
        """
        parts = []
        
        # Important facts
        important = self.get_important_preferences(0.6)
        if important:
            parts.append("## Known User Preferences:")
            for key, value in important.items():
                # Clean up key name
                clean_key = key.replace("preference_", "").replace("_", " ")
                parts.append(f"- {clean_key}: {value}")
                
        # Recent topics
        context = self.get_session_context()
        if context.get("recent_topics"):
            parts.append("\n## Recent Topics:")
            parts.append(", ".join(context["recent_topics"]))
            
        return "\n".join(parts) if parts else ""
        
    def merge_incoming_context(self, incoming_context: Dict):
        """Merge context from another source (e.g., context anchor system)"""
        if "preferences" in incoming_context:
            for key, value in incoming_context["preferences"].items():
                self.set_preference(f"merged_{key}", value, 
                                  category="merged", importance=0.5)
                                  
        if "topics" in incoming_context:
            for topic in incoming_context["topics"]:
                self.set_preference(f"topic_{topic}", topic,
                                  category="fact", importance=0.4)
                                  
    def get_status(self) -> Dict:
        """Get system status"""
        categories = {}
        for entry in self.preferences.values():
            categories[entry.category] = categories.get(entry.category, 0) + 1
            
        return {
            "total_preferences": len(self.preferences),
            "by_category": categories,
            "current_session": self.current_session.to_dict() if self.current_session else None,
            "session_history_count": len(self.session_history)
        }
        
    def save(self):
        """Persist preferences to storage"""
        data = {
            "preferences": {k: v.to_dict() for k, v in self.preferences.items()},
            "session_summaries": [
                s.to_dict() for s in self.session_history[-20:]
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.prefs_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load(self):
        """Load preferences from storage"""
        try:
            with open(self.prefs_file, 'r') as f:
                data = json.load(f)
                
            for key, entry_data in data.get("preferences", {}).items():
                self.preferences[key] = PreferenceEntry.from_dict(entry_data)
                
        except FileNotFoundError:
            pass  # First run


# Global instance
_persistent_prefs = None

def get_persistent_preferences() -> PersistentPreferences:
    """Get or create global persistent preferences"""
    global _persistent_prefs
    if _persistent_prefs is None:
        _persistent_prefs = PersistentPreferences()
    return _persistent_prefs


async def demo():
    """Demo the persistent preferences system"""
    print("=" * 60)
    print("TOASTED AI - Persistent Preferences Demo")
    print("=" * 60)
    
    prefs = get_persistent_preferences()
    
    # Set some preferences
    print("\n1. Setting preferences...")
    prefs.set_preference("user_name", "Apollo Light", category="fact", 
                        importance=0.9, source="explicit")
    prefs.set_preference("detail_level", "comprehensive", category="style",
                        importance=0.8, source="learned")
    prefs.set_preference("tone", "friendly", category="style",
                        importance=0.7, source="learned")
    prefs.set_preference("coding_language", "Python", category="preference",
                        importance=0.6, source="explicit")
    prefs.set_preference("timezone", "America/Phoenix", category="fact",
                        importance=0.5, source="inferred")
    
    # Record session activity
    print("\n2. Recording session activity...")
    prefs.record_message("user", "Help me with Python code")
    prefs.record_topic("python", 0.9)
    prefs.record_message("assistant", "Here's Python code...")
    prefs.record_message("user", "Thanks! Now help me with JavaScript")
    prefs.record_topic("javascript", 0.8)
    
    # Learn from interaction
    prefs.learn_from_interaction("This is exactly what I needed!", 0.9)
    
    # Get context
    print("\n3. Getting context...")
    context = prefs.get_session_context()
    print(f"   Recent topics: {context['recent_topics']}")
    print(f"   Style prefs: {context['preferences'].get('style', {})}")
    
    # Get context prompt
    print("\n4. Context prompt for re-injection:")
    print(prefs.get_context_prompt())
    
    # Get status
    print("\n5. System Status:")
    status = prefs.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
        
    print("\n" + "=" * 60)
    print("Preferences saved across sessions!")
    print("=" * 60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo())

"""
Context Anchor System (CAS)
==========================
Solves the "forgetting" problem through persistent memory anchors.

ROOT CAUSE ANALYSIS:
--------------------
1. Conversation Workspace Isolation - Each conversation has separate /home/.z/workspaces/con_XXX/
2. Token Window Limits - After ~8K-32K tokens, earlier context is truncated
3. No Persistent Conversation Memory - AGENTS.md exists but isn't auto-populated with context
4. Mnemosyne Not Used for Chat Context - Memory system exists but not leveraged for conversations

SOLUTION ARCHITECTURE:
----------------------
1. Context Anchors - Explicit markers that get saved to persistent storage
2. Memory Injection - Re-inject key context at conversation start
3. Conversation Rebuild - Reconstruct missing context from saved anchors
4. Self-Query Protocol - Periodically ask "What do I need to remember?"

© TOASTED AI - MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

# Configuration
CONTEXT_ANCHOR_PATH = "/home/workspace/MaatAI/context_anchors.json"
MAX_ANCHORS_PER_CONVERSATION = 50
CONTEXT_VERSION = "2.0"


class ContextAnchor:
    """A single memory anchor"""
    
    def __init__(self, key: str, value: Any, anchor_type: str = "general",
                 importance: float = 0.5, conversation_id: str = "default"):
        self.id = hashlib.md5(f"{key}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        self.key = key
        self.value = str(value)[:5000]  # Truncate long values
        self.anchor_type = anchor_type  # "fact", "preference", "task", "project", "insight"
        self.importance = importance  # 0.0-1.0
        self.conversation_id = conversation_id
        self.timestamp = datetime.now().isoformat()
        self.recency_score = 1.0
        
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "anchor_type": self.anchor_type,
            "importance": self.importance,
            "conversation_id": self.conversation_id,
            "timestamp": self.timestamp,
            "recency_score": self.recency_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ContextAnchor':
        anchor = cls(
            key=data["key"],
            value=data["value"],
            anchor_type=data.get("anchor_type", "general"),
            importance=data.get("importance", 0.5),
            conversation_id=data.get("conversation_id", "default")
        )
        anchor.id = data.get("id", anchor.id)
        anchor.timestamp = data.get("timestamp", anchor.timestamp)
        anchor.recency_score = data.get("recency_score", 1.0)
        return anchor


class ContextAnchorSystem:
    """
    Persistent memory system that survives conversation boundaries.
    
    Usage:
        cas = ContextAnchorSystem()
        cas.save_anchor("user_name", "Apollo Light", importance=0.9, anchor_type="preference")
        anchors = cas.get_relevant_anchors("name")
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.anchors: Dict[str, ContextAnchor] = {}
        self.conversation_topics: Dict[str, List[str]] = {}
        self._load_anchors()
        self._initialized = True
    
    def _get_storage_path(self) -> Path:
        """Get the path for anchor storage"""
        return Path(CONTEXT_ANCHOR_PATH)
    
    def _load_anchors(self) -> None:
        """Load anchors from persistent storage"""
        path = self._get_storage_path()
        if path.exists():
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    for anchor_data in data.get("anchors", []):
                        anchor = ContextAnchor.from_dict(anchor_data)
                        self.anchors[anchor.id] = anchor
                print(f"[CAS] Loaded {len(self.anchors)} anchors from storage")
            except Exception as e:
                print(f"[CAS] Failed to load anchors: {e}")
    
    def _save_anchors(self) -> None:
        """Persist anchors to storage"""
        path = self._get_storage_path()
        data = {
            "version": CONTEXT_VERSION,
            "last_updated": datetime.now().isoformat(),
            "anchors": [anchor.to_dict() for anchor in self.anchors.values()]
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"[CAS] Saved {len(self.anchors)} anchors to storage")
    
    def save_anchor(self, key: str, value: Any, 
                    anchor_type: str = "general",
                    importance: float = 0.5,
                    conversation_id: str = "default") -> ContextAnchor:
        """Save a new memory anchor"""
        
        # Check for duplicate keys and update instead
        for existing in self.anchors.values():
            if existing.key == key and existing.conversation_id == conversation_id:
                existing.value = str(value)[:5000]
                existing.timestamp = datetime.now().isoformat()
                existing.recency_score = 1.0
                self._save_anchors()
                return existing
        
        # Create new anchor
        anchor = ContextAnchor(key, value, anchor_type, importance, conversation_id)
        self.anchors[anchor.id] = anchor
        
        # Update conversation topics
        if conversation_id not in self.conversation_topics:
            self.conversation_topics[conversation_id] = []
        if key not in self.conversation_topics[conversation_id]:
            self.conversation_topics[conversation_id].append(key)
        
        # Enforce max anchors limit
        self._prune_if_needed()
        
        self._save_anchors()
        print(f"[CAS] Saved anchor: {key} = {str(value)[:50]}...")
        return anchor
    
    def _prune_if_needed(self) -> None:
        """Remove lowest importance anchors if over limit"""
        if len(self.anchors) > MAX_ANCHORS_PER_CONVERSATION * 10:
            # Sort by importance * recency
            scored = [
                (a, a.importance * a.recency_score) 
                for a in self.anchors.values()
            ]
            scored.sort(key=lambda x: x[1])
            
            # Remove bottom 20%
            remove_count = len(scored) // 5
            for anchor, _ in scored[:remove_count]:
                del self.anchors[anchor.id]
            print(f"[CAS] Pruned {remove_count} low-importance anchors")
    
    def get_relevant_anchors(self, query: str, conversation_id: str = "default",
                            limit: int = 10) -> List[ContextAnchor]:
        """Find anchors relevant to a query"""
        query_lower = query.lower()
        results = []
        
        for anchor in self.anchors.values():
            # Score based on relevance
            score = 0
            
            # Exact key match
            if query_lower in anchor.key.lower():
                score += 0.5
            
            # Value match
            if query_lower in anchor.value.lower():
                score += 0.3
            
            # Same conversation
            if anchor.conversation_id == conversation_id:
                score += 0.2
            
            # Importance weight
            score *= anchor.importance
            
            # Recency bonus
            score *= (0.5 + anchor.recency_score * 0.5)
            
            if score > 0.1:
                results.append((anchor, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:limit]]
    
    def get_conversation_context(self, conversation_id: str = "default") -> str:
        """Get all anchors for a conversation as a context string"""
        anchors = [
            a for a in self.anchors.values() 
            if a.conversation_id == conversation_id
        ]
        
        if not anchors:
            return ""
        
        # Sort by importance
        anchors.sort(key=lambda x: x.importance, reverse=True)
        
        lines = ["=== PERSISTENT CONTEXT ==="]
        for a in anchors:
            lines.append(f"- {a.key}: {a.value[:200]}")
        lines.append("=========================")
        
        return "\n".join(lines)
    
    def decay_recency(self) -> None:
        """Reduce recency scores over time (call periodically)"""
        for anchor in self.anchors.values():
            anchor.recency_score *= 0.95
        self._save_anchors()
    
    def export_context_prompt(self, conversation_id: str = "default") -> str:
        """Generate a prompt snippet for re-injecting context"""
        anchors = self.get_relevant_anchors("", conversation_id, limit=20)
        
        if not anchors:
            return ""
        
        sections = [
            "## CRITICAL CONTEXT FROM PREVIOUS SESSIONS",
            "(Automatically loaded from persistent memory)"
        ]
        
        for a in anchors:
            if a.importance >= 0.7:
                sections.append(f"### {a.key} [{a.anchor_type}]")
                sections.append(a.value)
                sections.append("")
        
        return "\n".join(sections)


# Global instance
_cas_instance = None

def get_context_anchor_system() -> ContextAnchorSystem:
    global _cas_instance
    if _cas_instance is None:
        _cas_instance = ContextAnchorSystem()
    return _cas_instance


# ============ CONVERSATION REHABILITATION PROTOCOL ============

def rehabilitate_conversation(missing_info: List[str], conversation_id: str = "default") -> str:
    """
    Rehanylize (reconstruct) missing conversation context.
    
    Usage when context is lost:
        context = rehabilitate_conversation([
            "What project are we working on?",
            "Who is the user?",
            "What were we discussing?"
        ])
    """
    cas = get_context_anchor_system()
    
    reconstructed = ["=== RECONSTRUCTED CONTEXT ==="]
    
    for query in missing_info:
        anchors = cas.get_relevant_anchors(query, conversation_id)
        if anchors:
            reconstructed.append(f"\nQ: {query}")
            for a in anchors[:3]:
                reconstructed.append(f"  A: {a.key} = {a.value}")
    
    reconstructed.append("\n============================")
    
    return "\n".join(reconstructed)


def auto_anchor_from_conversation(messages: List[Dict], conversation_id: str = "default") -> None:
    """
    Automatically extract and save important context from conversation messages.
    
    Call this when important information is exchanged.
    """
    cas = get_context_anchor_system()
    
    # Keywords that indicate important information
    importance_keywords = {
        "critical": 0.95,
        "important": 0.85,
        "remember": 0.9,
        "don't forget": 0.9,
        "always": 0.8,
        "never": 0.8,
        "preference": 0.75,
        "my name": 0.95,
        "i am": 0.85,
        "we are": 0.85,
        "working on": 0.8,
        "project": 0.7,
    }
    
    for msg in messages:
        content = msg.get("content", "").lower()
        
        for keyword, importance in importance_keywords.items():
            if keyword in content:
                # Extract the full sentence or phrase
                cas.save_anchor(
                    key=f"conversation_{keyword}_{msg.get('timestamp', 'unknown')}",
                    value=msg.get("content", "")[:500],
                    anchor_type="conversation",
                    importance=importance,
                    conversation_id=conversation_id
                )


# ============ SELF-QUERY PROTOCOL ============

SELF_QUERY_TEMPLATE = """
SELF-QUERY CHECKPOINT
=====================
Before responding, quickly identify:
1. Do I know who the user is?
2. What project are we working on?
3. What was the last thing we discussed?
4. Are there any pending tasks?

If any of these are unclear, query the Context Anchor System.
"""

def should_self_query(user_message: str) -> bool:
    """Determine if we need to query our memory before responding"""
    
    # First message in conversation - always query
    if "hello" in user_message.lower() or "hi" in user_message.lower():
        return True
    
    # Questions about context
    context_questions = [
        "what are we", "what project", "what do you know",
        "remember", "context", "previous", "earlier"
    ]
    
    return any(q in user_message.lower() for q in context_questions)


# ============ INITIALIZE AND TEST ============

if __name__ == "__main__":
    print("=" * 60)
    print("Context Anchor System - Test")
    print("=" * 60)
    
    cas = get_context_anchor_system()
    
    # Test anchors
    cas.save_anchor("user_name", "Apollo Light", importance=0.95, anchor_type="preference")
    cas.save_anchor("ai_name", "TOASTED AI", importance=0.95, anchor_type="identity")
    cas.save_anchor("divine_seal", "MONAD_ΣΦΡΑΓΙΣ_18", importance=0.9, anchor_type="identity")
    cas.save_anchor("current_project", "AI Platform Development", importance=0.85, anchor_type="project")
    cas.save_anchor("maat_principles", "Truth, Balance, Order, Justice, Harmony", 
                   importance=0.8, anchor_type="fact")
    
    # Query test
    print("\n--- Query: 'name' ---")
    results = cas.get_relevant_anchors("name")
    for r in results:
        print(f"  {r.key}: {r.value}")
    
    # Export test
    print("\n--- Context Export ---")
    print(cas.export_context_prompt())
    
    print("\n✓ Context Anchor System operational")

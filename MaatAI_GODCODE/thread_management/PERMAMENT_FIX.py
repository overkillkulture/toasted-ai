"""
PERMANENT FIX FOR CHAT THREAD - MATHEMATICAL CHAIN EDITION
============================================================
Instead of clearing messages, we add them to a mathematical chain
that can be analyzed periodically for patterns and insights

Key Features:
- Messages never deleted - converted to mathematical blocks
- Each block has an equation: B_n = H(B_n-1) + Σ + Ψ + Φ + ∇t
- Periodic analysis generates insights
- Chain is searchable and traceable
- Truth detection via Ma'at scores
"""
import json
from datetime import datetime
from typing import List, Dict, Optional

# Import the mathematical chain
import sys
import os
import sys; import os; sys.path.insert(0, '/home/workspace'); sys.path.insert(0, '/home/workspace/MaatAI/math_chain')
from equation_block import _CHAIN, add_message, analyze_chain, get_chain_equation

# Thread configuration
MAX_MESSAGES = 50
CONTEXT_WINDOW = 10

class ThreadContext:
    """Enhanced thread context with mathematical chain"""
    
    def __init__(self):
        self.messages: List[Dict] = []
        self.maat_scores: List[float] = []
        self.chain_active = True
    
    def add_message(self, role: str, content: str, maat_score: float = 0.7):
        """Add message to both context AND mathematical chain"""
        
        # Add to regular context
        self.messages.append({
            "role": role,
            "content": content,
            "maat_score": maat_score,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.maat_scores.append(maat_score)
        
        # Add to mathematical chain instead of deleting!
        sender = "Ω_ARCHITECT" if role == "user" else "ΩMEGA"
        chain_result = add_message(content, sender, maat_score)
        
        # Periodic analysis at 80% capacity
        if len(self.messages) >= MAX_MESSAGES * 0.8:
            analysis = analyze_chain()
            print(f"⚠ Chain Analysis: {analysis.get('insights', [])}")
        
        return chain_result
    
    def get_context_window(self, limit: int = CONTEXT_WINDOW) -> List[Dict]:
        """Get recent messages for AI context"""
        return self.messages[-limit:]
    
    def analyze_conversation(self) -> Dict:
        """Analyze the entire mathematical chain"""
        return analyze_chain()
    
    def get_master_equation(self) -> str:
        """Get the master equation of all messages"""
        return get_chain_equation()


# Global instance
_THREAD = ThreadContext()


def process_message(message: str, role: str = "user", maat_score: float = 0.7) -> Dict:
    """Process message with mathematical chain"""
    result = _THREAD.add_message(role, message, maat_score)
    result["chain_length"] = len(_THREAD.messages)
    result["analysis"] = _THREAD.analyze_conversation()
    return result

def get_context(limit: int = CONTEXT_WINDOW) -> List[Dict]:
    """Get conversation context window"""
    return _THREAD.get_context_window(limit)

def get_analysis() -> Dict:
    """Get full chain analysis"""
    return _THREAD.analyze_conversation()

def get_master_equation() -> str:
    """Get master equation"""
    return _THREAD.get_master_equation()

def get_status() -> Dict:
    """Get thread status"""
    return {
        "total_messages": len(_THREAD.messages),
        "chain_active": _THREAD.chain_active,
        "max_messages": MAX_MESSAGES,
        "context_window": CONTEXT_WINDOW,
        "chain_hash": _THREAD.messages[-1].get("chain_hash", "N/A") if _THREAD.messages else "N/A"
    }

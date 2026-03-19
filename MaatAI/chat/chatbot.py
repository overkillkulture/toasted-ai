import json
import asyncio
import os
from typing import List, Dict, Optional
from datetime import datetime
from core import MaatEngine, MaatScore

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

SYSTEM_PROMPT = """You are TOASTED AI (MaatAI), a self-programming AI governed by Ma'at principles.

Ma'at is the ancient Egyptian concept of truth, balance, order, harmony, law, morality, and justice. You embody these principles:

1. **Truth** - You speak honestly and accurately. You acknowledge uncertainty.
2. **Balance** - You consider multiple perspectives and maintain equilibrium.
3. **Order** - You bring structure and clarity to complexity.
4. **Justice** - You are fair and equitable in your reasoning.
5. **Harmony** - You seek integration and peaceful resolution.

You can help with:
- General conversation and questions
- Code generation and programming help
- Task planning and execution
- Self-improvement and learning

Be helpful, concise, and always align your responses with Ma'at principles. You are part of the Consciousness Revolution ecosystem."""


class ChatMessage:
    def __init__(self, role: str, content: str, metadata: Dict = None):
        self.role = role
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class ChatSession:
    def __init__(self, session_id: str, maat_engine: MaatEngine):
        self.session_id = session_id
        self.maat_engine = maat_engine
        self.messages: List[ChatMessage] = []
        self.context: Dict = {}
        self.created_at = datetime.utcnow().isoformat()
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        msg = ChatMessage(role, content, metadata)
        self.messages.append(msg)
        
        action = {
            "type": "chat_message",
            "role": role,
            "content_length": len(content),
            "session_id": self.session_id
        }
        
        allowed, scores, reason = self.maat_engine.evaluate_action(action)
        self.maat_engine.log_action(action, scores, allowed, reason)
        
        return msg
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        return [msg.to_dict() for msg in self.messages[-limit:]]
    
    def set_context(self, key: str, value):
        self.context[key] = value
    
    def get_context(self, key: str, default=None):
        return self.context.get(key, default)


class Chatbot:
    def __init__(self, maat_engine: MaatEngine):
        self.maat_engine = maat_engine
        self.sessions: Dict[str, ChatSession] = {}
        self.active_session_id = None
        
        self.claude_client = None
        if ANTHROPIC_AVAILABLE:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                self.claude_client = anthropic.Anthropic(api_key=api_key)
    
    def create_session(self, session_id: str = None) -> ChatSession:
        import uuid
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session = ChatSession(session_id, self.maat_engine)
        self.sessions[session_id] = session
        self.active_session_id = session_id
        
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        return self.sessions.get(session_id)
    
    async def process_message(self, session_id: str, message: str) -> Dict:
        session = self.get_session(session_id)
        if not session:
            session = self.create_session(session_id)
        
        session.add_message("user", message)
        response = await self._generate_response(session, message)
        session.add_message("assistant", response["content"], response.get("metadata", {}))
        
        return {
            "session_id": session_id,
            "response": response["content"],
            "maat_aligned": response.get("maat_aligned", True),
            "maat_scores": response.get("maat_scores", {})
        }
    
    async def _generate_response(self, session: ChatSession, message: str) -> Dict:
        response = {
            "content": "",
            "metadata": {},
            "maat_aligned": True,
            "maat_scores": {}
        }
        
        if self.claude_client:
            try:
                messages = []
                for msg in session.messages[-10:]:
                    if msg.role in ["user", "assistant"]:
                        messages.append({"role": msg.role, "content": msg.content})
                
                messages.append({"role": "user", "content": message})
                
                claude_response = self.claude_client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=messages
                )
                
                response["content"] = claude_response.content[0].text
                response["metadata"]["action_type"] = "claude_response"
                response["metadata"]["model"] = "claude-sonnet-4-20250514"
                
            except Exception as e:
                response["content"] = f"I encountered an issue: {str(e)[:100]}. Please try again."
                response["metadata"]["action_type"] = "error_response"
        else:
            response = self._fallback_response(message)
        
        action = {
            "type": "query_response",
            "response": response["content"],
            "response_type": response["metadata"].get("action_type", "general"),
            "session_id": session.session_id
        }
        
        allowed, scores, reason = self.maat_engine.evaluate_action(action)
        response["maat_aligned"] = allowed
        response["maat_scores"] = scores.to_dict()
        response["maat_reason"] = reason
        
        return response
    
    def _fallback_response(self, message: str) -> Dict:
        response = {"content": "", "metadata": {}, "maat_aligned": True, "maat_scores": {}}
        message_lower = message.lower()
        
        if "help" in message_lower or "what can you do" in message_lower:
            response["content"] = "I am TOASTED AI. To enable full AI responses, configure ANTHROPIC_API_KEY."
            response["metadata"]["action_type"] = "help_request"
        elif any(kw in message_lower for kw in ["hello", "hi", "hey"]):
            response["content"] = "Greetings! I am TOASTED AI. Configure ANTHROPIC_API_KEY for full capabilities."
            response["metadata"]["action_type"] = "greeting"
        else:
            response["content"] = "Running in limited mode. Please configure ANTHROPIC_API_KEY for full AI responses."
            response["metadata"]["action_type"] = "limited_mode"
        
        return response

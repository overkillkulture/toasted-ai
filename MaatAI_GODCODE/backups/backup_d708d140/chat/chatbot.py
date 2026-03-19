import json
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from core import MaatEngine, MaatScore


class ChatMessage:
    def __init__(self, role: str, content: str, metadata: Dict = None):
        self.role = role  # 'user', 'assistant', 'system'
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'role': self.role,
            'content': self.content,
            'metadata': self.metadata,
            'timestamp': self.timestamp
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
        
        # Log to Ma'at ledger
        action = {
            'type': 'chat_message',
            'role': role,
            'content_length': len(content),
            'session_id': self.session_id
        }
        
        # Evaluate message against Ma'at
        allowed, scores, reason = self.maat_engine.evaluate_action(action)
        self.maat_engine.log_action(action, scores, allowed, reason)
        
        return msg
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        return [msg.to_dict() for msg in self.messages[-limit:]]
    
    def set_context(self, key: str, value: any):
        self.context[key] = value
    
    def get_context(self, key: str, default=None):
        return self.context.get(key, default)


class Chatbot:
    def __init__(self, maat_engine: MaatEngine):
        self.maat_engine = maat_engine
        self.sessions: Dict[str, ChatSession] = {}
        self.active_session_id = None
    
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
        
        # Add user message
        session.add_message('user', message)
        
        # Process the message (this will be expanded with planner/executor)
        response = await self._generate_response(session, message)
        
        # Add assistant response
        session.add_message('assistant', response['content'], response.get('metadata', {}))
        
        return {
            'session_id': session_id,
            'response': response['content'],
            'maat_aligned': response.get('maat_aligned', True),
            'maat_scores': response.get('maat_scores', {})
        }
    
    async def _generate_response(self, session: ChatSession, message: str) -> Dict:
        """Generate a response to the user's message."""
        # This is a simple response generator - will be enhanced
        # with the planner and executor
        
        response = {
            'content': '',
            'metadata': {},
            'maat_aligned': True,
            'maat_scores': {}
        }
        
        # Check if this is a self-improvement request
        if 'improve yourself' in message.lower() or 'modify yourself' in message.lower():
            response['content'] = "I understand you want me to improve my capabilities. I'll analyze my current state and propose improvements that align with Ma'at principles."
            response['metadata']['action_type'] = 'self_improvement_request'
        elif 'code' in message.lower() and 'write' in message.lower():
            response['content'] = "I can write code for you. Please specify what you'd like me to create, and I'll ensure it meets Ma'at standards."
            response['metadata']['action_type'] = 'code_generation_request'
        elif 'help' in message.lower() or 'what can you do' in message.lower():
            response['content'] = """I am a Ma'at-aligned AI chatbot that can:

- Write and execute code under Ma'at constraints
- Improve my own capabilities through self-modification
- Plan and execute complex tasks
- Learn from experience and adapt

All my actions are evaluated against the 5 pillars of Ma'at:
- Truth: All information is verifiable
- Balance: System stability is maintained
- Order: Creates order from complexity
- Justice: Fair decision-making
- Harmony: Integrates with existing systems

What would you like me to help you with?"""
            response['metadata']['action_type'] = 'help_request'
        else:
            response['content'] = f"I received your message: '{message}'. I'm ready to help you with tasks, code generation, or self-improvement. What would you like me to do?"
            response['metadata']['action_type'] = 'general_response'
        
        # Evaluate response against Ma'at
        action = {
            'type': 'query_response',
            'response': response['content'],
            'response_type': response['metadata'].get('action_type', 'general'),
            'session_id': session.session_id
        }
        
        allowed, scores, reason = self.maat_engine.evaluate_action(action)
        
        response['maat_aligned'] = allowed
        response['maat_scores'] = scores.to_dict()
        response['maat_reason'] = reason
        
        return response

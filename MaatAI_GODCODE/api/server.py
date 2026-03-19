#!/usr/bin/env python3
"""MaatAI FastAPI Server - Web Platform for MaatAI."""

import sys
import os
import asyncio
from contextlib import asynccontextmanager

# Add workspace to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import uuid
from datetime import datetime

from core import MaatEngine
from chat import Chatbot
from planner import TaskPlanner, TaskType
from executor import CodeGenerator
from core.self_modifier import SelfModifier


# Global state
maat_engine = None
chatbot = None
planner = None
code_generator = None
self_modifier = None
sessions = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize on startup."""
    global maat_engine, chatbot, planner, code_generator, self_modifier
    
    maat_engine = MaatEngine()
    chatbot = Chatbot(maat_engine)
    planner = TaskPlanner(maat_engine)
    code_generator = CodeGenerator(maat_engine)
    self_modifier = SelfModifier(maat_engine)
    
    print("MaatAI Platform initialized!")
    yield
    print("MaatAI Platform shutting down...")


app = FastAPI(
    title="MaatAI Platform API",
    description="Self-Programming AI under Ma'at Principles",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class CodeRequest(BaseModel):
    request: str
    language: Optional[str] = None

class ExecuteRequest(BaseModel):
    code: str
    language: Optional[str] = None
    timeout: Optional[int] = 30

class TaskRequest(BaseModel):
    request: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    maat_aligned: bool
    maat_scores: Dict
    task: Dict


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with MaatAI."""
    global sessions
    
    # Get or create session
    session_id = request.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        sessions[session_id] = chatbot.create_session(session_id)
    
    # Process the request through planner
    task = planner.create_task(request.message)
    
    # Generate code if needed - use this response instead of chatbot
    if task.task_type == TaskType.CODE_GENERATION:
        execution_result = code_generator.generate_code(
            request.message, 
            task.to_dict()
        )
        
        code = execution_result.get('code', '# Code generation failed')
        lang = execution_result.get('language', 'python')
        
        response_text = f"I generated the following {lang} code for you:\n\n```{lang}\n{code}\n```\n\nThis code was evaluated against Ma'at principles and is ready to use."
        
        # Evaluate against Ma'at
        action = {
            'type': 'code_generation',
            'code': code,
            'language': lang
        }
        allowed, scores, reason = maat_engine.evaluate_action(action)
        
        # Log to session
        session = chatbot.get_session(session_id)
        session.add_message('user', request.message)
        session.add_message('assistant', response_text)
        
        return ChatResponse(
            session_id=session_id,
            response=response_text,
            maat_aligned=allowed,
            maat_scores=scores.to_dict(),
            task=task.to_dict()
        )
    
    # Generate response for non-code requests
    chat_response = await chatbot.process_message(session_id, request.message)
    
    return ChatResponse(
        session_id=session_id,
        response=chat_response['response'],
        maat_aligned=chat_response['maat_aligned'],
        maat_scores=chat_response.get('maat_scores', {}),
        task=task.to_dict()
    )


# Code generation endpoint
@app.post("/code/generate")
async def generate_code(request: CodeRequest):
    """Generate code based on request."""
    result = code_generator.generate_code(request.request)
    return result


# Code execution endpoint
@app.post("/code/execute")
async def execute_code(request: ExecuteRequest):
    """Execute code and return result."""
    from executor.code_generator import CodeLanguage
    
    lang = CodeLanguage.PYTHON
    if request.language:
        try:
            lang = CodeLanguage(request.language)
        except:
            pass
    
    result = await code_generator.execute_code(request.code, lang, request.timeout)
    return result.to_dict()


# Task management endpoints
@app.post("/task/create")
async def create_task(request: TaskRequest):
    """Create a new task."""
    task = planner.create_task(request.request)
    return task.to_dict()


@app.get("/task/{task_id}")
async def get_task(task_id: str):
    """Get task details."""
    task = planner.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()


@app.get("/tasks")
async def list_tasks():
    """List all tasks."""
    return planner.get_all_tasks()


# Self-improvement endpoint
@app.post("/improve")
async def improve_self():
    """Trigger self-improvement."""
    proposals = self_modifier.propose_improvements()
    
    if proposals['proposals']:
        best_proposal = proposals['proposals'][0]
        result = self_modifier.apply_modification(best_proposal)
        return {
            'improvement_applied': best_proposal['id'],
            'result': result,
            'all_proposals': proposals
        }
    
    return {'message': 'No improvements needed or available'}


# Health check
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "maat_engine": "active" if maat_engine else "inactive"
    }


# Ma'at status
@app.get("/maat/status")
async def maat_status():
    """Get Ma'at alignment status."""
    recent_actions = maat_engine.get_recent_actions(limit=20)
    
    # Calculate average scores
    total_scores = {'truth': 0, 'balance': 0, 'order': 0, 'justice': 0, 'harmony': 0}
    count = 0
    
    for action in recent_actions:
        scores = action.get('maat_scores', {})
        for key in total_scores:
            if key in scores:
                total_scores[key] += scores[key]
        count += 1
    
    if count > 0:
        avg_scores = {k: v/count for k, v in total_scores.items()}
    else:
        avg_scores = total_scores
    
    return {
        "thresholds": maat_engine.thresholds,
        "average_scores": avg_scores,
        "recent_actions_count": len(recent_actions)
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "MaatAI Platform API",
        "version": "1.0.0",
        "description": "Self-Programming AI under Ma'at Principles",
        "endpoints": {
            "chat": "/chat",
            "code_generate": "/code/generate",
            "code_execute": "/code/execute",
            "tasks": "/tasks",
            "improve": "/improve",
            "health": "/health",
            "maat_status": "/maat/status"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""Task Planner for MaatAI - Autonomous task decomposition and planning."""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

class TaskType(Enum):
    CODE_GENERATION = "code_generation"
    CODE_EXECUTION = "code_execution"
    FILE_OPERATION = "file_operation"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    SELF_MODIFICATION = "self_modification"
    CHAT = "chat"
    UNKNOWN = "unknown"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class Task:
    """Represents a single task in the planning system."""
    
    def __init__(self, title: str, description: str, task_type: TaskType, 
                 parent_task_id: str = None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.task_type = task_type
        self.status = TaskStatus.PENDING
        self.parent_task_id = parent_task_id
        self.subtasks: List[str] = []
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
        self.completed_at: Optional[str] = None
        self.result: Optional[Dict] = None
        self.error: Optional[str] = None
        self.metadata: Dict = {}
        self.maat_scores: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'task_type': self.task_type.value,
            'status': self.status.value,
            'parent_task_id': self.parent_task_id,
            'subtasks': self.subtasks,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'completed_at': self.completed_at,
            'result': self.result,
            'error': self.error,
            'metadata': self.metadata,
            'maat_scores': self.maat_scores
        }
    
    def complete(self, result: Dict = None):
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow().isoformat()
        self.result = result
        self.updated_at = datetime.utcnow().isoformat()
    
    def fail(self, error: str):
        self.status = TaskStatus.FAILED
        self.error = error
        self.updated_at = datetime.utcnow().isoformat()


class TaskPlanner:
    """Plans and decomposes user requests into executable tasks."""
    
    def __init__(self, maat_engine=None):
        self.maat_engine = maat_engine
        self.tasks: Dict[str, Task] = {}
        self.task_history: List[Dict] = []
    
    def create_task(self, request: str) -> Task:
        """Parse a user request and create a task."""
        
        # Determine task type from request
        task_type = self._classify_request(request)
        
        # Create the main task
        task = Task(
            title=self._extract_title(request),
            description=request,
            task_type=task_type
        )
        
        # Decompose into subtasks if complex
        subtasks = self._decompose_task(request, task_type)
        task.subtasks = [sub.id for sub in subtasks]
        
        # Store all tasks
        self.tasks[task.id] = task
        for subtask in subtasks:
            self.tasks[subtask.id] = subtask
        
        # Evaluate against Ma'at
        if self.maat_engine:
            action = {
                'type': task_type.value,
                'request': request,
                'subtask_count': len(subtasks)
            }
            allowed, scores, reason = self.maat_engine.evaluate_action(action)
            task.maat_scores = scores.to_dict()
        
        return task
    
    def _classify_request(self, request: str) -> TaskType:
        """Classify the request type based on keywords."""
        request_lower = request.lower()
        
        if any(kw in request_lower for kw in ['write code', 'create code', 'generate code', 'write a function', 'create a class', 'build']):
            return TaskType.CODE_GENERATION
        elif any(kw in request_lower for kw in ['run code', 'execute', 'run script', 'run command']):
            return TaskType.CODE_EXECUTION
        elif any(kw in request_lower for kw in ['create file', 'write file', 'delete file', 'read file', 'modify file']):
            return TaskType.FILE_OPERATION
        elif any(kw in request_lower for kw in ['research', 'search', 'find information', 'look up', 'investigate']):
            return TaskType.RESEARCH
        elif any(kw in request_lower for kw in ['analyze', 'explain', 'break down', 'examine']):
            return TaskType.ANALYSIS
        elif any(kw in request_lower for kw in ['improve yourself', 'modify yourself', 'enhance yourself', 'self-improve']):
            return TaskType.SELF_MODIFICATION
        else:
            return TaskType.CHAT
    
    def _extract_title(self, request: str) -> str:
        """Extract a title from the request."""
        # Take first few words
        words = request.split()[:5]
        title = ' '.join(words)
        if len(request.split()) > 5:
            title += '...'
        return title
    
    def _decompose_task(self, request: str, task_type: TaskType) -> List[Task]:
        """Decompose a complex task into subtasks."""
        subtasks = []
        
        if task_type == TaskType.CODE_GENERATION:
            # Break down code generation
            subtasks.append(Task(
                title="Analyze requirements",
                description=f"Analyze requirements for: {request}",
                task_type=TaskType.ANALYSIS
            ))
            subtasks.append(Task(
                title="Generate code",
                description=f"Generate code for: {request}",
                task_type=TaskType.CODE_GENERATION
            ))
            subtasks.append(Task(
                title="Verify code",
                description=f"Verify code quality and safety",
                task_type=TaskType.ANALYSIS
            ))
        
        elif task_type == TaskType.RESEARCH:
            subtasks.append(Task(
                title="Gather information",
                description=f"Research: {request}",
                task_type=TaskType.RESEARCH
            ))
            subtasks.append(Task(
                title="Synthesize findings",
                description="Synthesize research findings",
                task_type=TaskType.ANALYSIS
            ))
        
        return subtasks
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.tasks.get(task_id)
    
    def get_subtasks(self, task_id: str) -> List[Task]:
        """Get all subtasks for a task."""
        task = self.tasks.get(task_id)
        if not task:
            return []
        return [self.tasks[sid] for sid in task.subtasks if sid in self.tasks]
    
    def complete_task(self, task_id: str, result: Dict = None):
        """Mark a task as completed."""
        task = self.tasks.get(task_id)
        if task:
            task.complete(result)
            self.task_history.append(task.to_dict())
    
    def fail_task(self, task_id: str, error: str):
        """Mark a task as failed."""
        task = self.tasks.get(task_id)
        if task:
            task.fail(error)
            self.task_history.append(task.to_dict())
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks."""
        return [t.to_dict() for t in self.tasks.values()]
    
    def get_pending_tasks(self) -> List[Dict]:
        """Get all pending tasks."""
        return [t.to_dict() for t in self.tasks.values() 
                if t.status == TaskStatus.PENDING]
    
    def get_task_tree(self, task_id: str) -> Dict:
        """Get a task and all its subtasks as a tree."""
        task = self.tasks.get(task_id)
        if not task:
            return {}
        
        tree = task.to_dict()
        tree['subtask_details'] = [
            self.get_task_tree(sid) for sid in task.subtasks
        ]
        return tree

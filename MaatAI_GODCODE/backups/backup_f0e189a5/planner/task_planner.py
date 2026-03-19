import json
import re
from typing import List, Dict, Optional
from datetime import datetime
from core import MaatEngine, MaatScore


class Task:
    def __init__(self, task_id: str, description: str, task_type: str):
        self.task_id = task_id
        self.description = description
        self.task_type = task_type  # 'code_generation', 'file_operation', 'query', 'self_modification'
        self.subtasks: List[Dict] = []
        self.status = 'pending'  # 'pending', 'in_progress', 'completed', 'failed'
        self.result: Dict = {}
        self.created_at = datetime.utcnow().isoformat()
        self.maat_scores: Optional[MaatScore] = None
    
    def to_dict(self) -> Dict:
        return {
            'task_id': self.task_id,
            'description': self.description,
            'task_type': self.task_type,
            'subtasks': self.subtasks,
            'status': self.status,
            'result': self.result,
            'created_at': self.created_at,
            'maat_scores': self.maat_scores.to_dict() if self.maat_scores else None
        }


class TaskPlanner:
    def __init__(self, maat_engine: MaatEngine):
        self.maat_engine = maat_engine
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[str] = []
    
    def parse_request(self, request: str) -> Dict:
        """Parse a user request into a structured task."""
        request_lower = request.lower()
        
        task_info = {
            'type': 'query',
            'description': request,
            'complexity': 'simple',
            'requires_execution': False,
            'requires_code_generation': False,
            'requires_file_operations': False,
            'is_self_modification': False,
            'priority': 'normal'
        }
        
        # Detect task type
        if any(word in request_lower for word in ['write', 'create', 'build', 'generate code']):
            task_info['type'] = 'code_generation'
            task_info['requires_code_generation'] = True
            task_info['complexity'] = 'medium'
            task_info['priority'] = 'high'
        
        if any(word in request_lower for word in ['improve yourself', 'modify yourself', 'self', 'upgrade']):
            task_info['type'] = 'self_modification'
            task_info['is_self_modification'] = True
            task_info['complexity'] = 'high'
            task_info['priority'] = 'critical'
        
        if any(word in request_lower for word in ['file', 'save', 'delete', 'organize']):
            task_info['requires_file_operations'] = True
            task_info['complexity'] = 'low'
        
        if any(word in request_lower for word in ['run', 'execute', 'test']):
            task_info['requires_execution'] = True
            task_info['complexity'] = 'medium'
        
        if any(word in request_lower for word in ['complex', 'system', 'architecture', 'multiple']):
            task_info['complexity'] = 'high'
        
        return task_info
    
    def create_task(self, request: str) -> Task:
        """Create a task from a user request."""
        task_info = self.parse_request(request)
        
        import uuid
        task_id = str(uuid.uuid4())
        
        task = Task(
            task_id=task_id,
            description=request,
            task_type=task_info['type']
        )
        
        # Generate subtasks based on complexity
        subtasks = self._generate_subtasks(task_info)
        task.subtasks = subtasks
        
        # Evaluate task against Ma'at
        action = {
            'type': 'task_creation',
            'task_type': task.task_type,
            'complexity': task_info['complexity'],
            'description': request
        }
        
        allowed, scores, reason = self.maat_engine.evaluate_action(action)
        task.maat_scores = scores
        
        if allowed:
            self.tasks[task_id] = task
            self.task_queue.append(task_id)
        
        return task
    
    def _generate_subtasks(self, task_info: Dict) -> List[Dict]:
        """Generate subtasks based on task type and complexity."""
        subtasks = []
        
        task_type = task_info['type']
        complexity = task_info['complexity']
        
        if task_type == 'code_generation':
            subtasks.extend([
                {'id': 1, 'action': 'analyze_requirements', 'description': 'Analyze code requirements'},
                {'id': 2, 'action': 'generate_code', 'description': 'Generate initial code'},
                {'id': 3, 'action': 'verify_structure', 'description': 'Verify code structure'},
                {'id': 4, 'action': 'test_code', 'description': 'Test generated code'},
                {'id': 5, 'action': 'finalize', 'description': 'Finalize and document code'}
            ])
        
        elif task_type == 'self_modification':
            subtasks.extend([
                {'id': 1, 'action': 'analyze_current_state', 'description': 'Analyze current system state'},
                {'id': 2, 'action': 'identify_improvements', 'description': 'Identify potential improvements'},
                {'id': 3, 'action': 'propose_modification', 'description': 'Propose modification'},
                {'id': 4, 'action': 'create_backup', 'description': 'Create system backup'},
                {'id': 5, 'action': 'implement_modification', 'description': 'Implement modification'},
                {'id': 6, 'action': 'verify_integrity', 'description': 'Verify system integrity'},
                {'id': 7, 'action': 'test_functionality', 'description': 'Test modified functionality'}
            ])
        
        elif task_type == 'query':
            subtasks.extend([
                {'id': 1, 'action': 'parse_query', 'description': 'Parse user query'},
                {'id': 2, 'action': 'retrieve_knowledge', 'description': 'Retrieve relevant knowledge'},
                {'id': 3, 'action': 'formulate_response', 'description': 'Formulate response'}
            ])
        
        return subtasks
    
    def get_next_task(self) -> Optional[Task]:
        """Get the next task from the queue."""
        if not self.task_queue:
            return None
        
        task_id = self.task_queue.pop(0)
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: str, result: Dict = None):
        """Update task status and result."""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            if result:
                self.tasks[task_id].result = result
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.tasks.get(task_id)

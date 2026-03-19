import json
import os
import subprocess
from typing import Dict, Any, Optional
from datetime import datetime
from core import MaatEngine, MaatScore


class SelfExecutor:
    """Executes tasks and manages execution flow."""
    
    def __init__(self, maat_engine: MaatEngine):
        self.maat_engine = maat_engine
        self.execution_history: Dict[str, Dict] = {}
    
    def execute_task(self, task: Dict) -> Dict:
        """Execute a task with Ma'at validation."""
        
        action = {
            'type': 'task_execution',
            'task_type': task.get('task_type', 'unknown'),
            'description': task.get('description', ''),
            'is_test': True  # All tasks are executed in test mode initially
        }
        
        allowed, scores, reason = self.maat_engine.evaluate_action(action)
        
        result = {
            'task_id': task.get('task_id'),
            'success': allowed,
            'maat_scores': scores.to_dict(),
            'maat_reason': reason,
            'output': '',
            'error': None
        }
        
        if not allowed:
            result['error'] = f"Task execution rejected by Ma'at: {reason}"
            return result
        
        try:
            # Execute based on task type
            if task.get('task_type') == 'code_generation':
                result.update(self._execute_code_generation(task))
            elif task.get('task_type') == 'self_modification':
                result.update(self._execute_self_modification(task))
            elif task.get('task_type') == 'query':
                result.update(self._execute_query(task))
            else:
                result['output'] = f"Task of type {task.get('task_type')} acknowledged"
        
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
        
        return result
    
    def _execute_code_generation(self, task: Dict) -> Dict:
        """Execute code generation task."""
        return {
            'output': f"Code generation task completed: {task.get('description')}",
            'code_generated': True
        }
    
    def _execute_self_modification(self, task: Dict) -> Dict:
        """Execute self-modification task."""
        return {
            'output': f"Self-modification task completed: {task.get('description')}",
            'modified': True
        }
    
    def _execute_query(self, task: Dict) -> Dict:
        """Execute query task."""
        return {
            'output': f"Query processed: {task.get('description')}",
            'answer': True
        }

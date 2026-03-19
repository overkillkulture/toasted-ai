#!/usr/bin/env python3
"""
Internal Operations API
Handles: Monitoring, Control, Self-Observation, Idea Generation
"""

import sys
import os
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.insert(0, '/home/workspace/MaatAI')

# Import system monitor
try:
    from system_monitor.system_monitor import SystemMonitor, get_monitor
except ImportError:
    from MaatAI.system_monitor.system_monitor import SystemMonitor, get_monitor


# Global state
class InternalAPIState:
    def __init__(self):
        self.monitor = get_monitor()
        self.operation_log = []
        self.self_reflections = []
        self._lock = threading.Lock()
        
    def log_operation(self, operation: str, params: Dict = None, result: Any = None):
        """Log an operation."""
        entry = {
            'operation': operation,
            'params': params or {},
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        with self._lock:
            self.operation_log.append(entry)
            if len(self.operation_log) > 500:
                self.operation_log = self.operation_log[-500:]
        return entry
    
    def get_operations(self, limit: int = 50) -> List[Dict]:
        """Get recent operations."""
        with self._lock:
            return self.operation_log[-limit:]
    
    def add_reflection(self, reflection: str, category: str = 'general') -> Dict:
        """Add a self-reflection."""
        entry = {
            'id': f"ref_{int(time.time())}",
            'reflection': reflection,
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
        with self._lock:
            self.self_reflections.append(entry)
            if len(self.self_reflections) > 200:
                self.self_reflections = self.self_reflections[-200:]
        return entry


# Singleton state
_state = None

def get_state() -> InternalAPIState:
    """Get or create API state."""
    global _state
    if _state is None:
        _state = InternalAPIState()
    return _state


# API Handlers (to be used with FastAPI/Hono)

async def handle_status(request: Dict) -> Dict:
    """Get full system status."""
    state = get_state()
    monitor = get_monitor()
    
    status = monitor.get_full_status()
    status['operations'] = state.get_operations(10)
    status['reflections'] = state.self_reflections[-5:]
    
    state.log_operation('status_check', result='ok')
    
    return status


async def handle_monitor(action: str, params: Dict = None) -> Dict:
    """Handle monitoring actions."""
    state = get_state()
    monitor = get_monitor()
    params = params or {}
    
    if action == 'stats':
        result = monitor.get_system_stats()
    elif action == 'processes':
        result = monitor.get_process_list()
    elif action == 'observe':
        event_type = params.get('type', 'manual')
        data = params.get('data', {})
        monitor.observe(event_type, data)
        result = {'observed': True, 'type': event_type}
    elif action == 'analyze':
        result = monitor.analyze_observations()
    elif action == 'ideas':
        result = monitor.generate_ideas()
    elif action == 'alerts':
        result = monitor.get_alerts()
    elif action == 'full':
        result = monitor.get_full_status()
    else:
        result = {'error': f'Unknown action: {action}'}
    
    state.log_operation(f'monitor_{action}', params, result)
    return result


async def handle_reflect(action: str, params: Dict = None) -> Dict:
    """Handle self-reflection operations."""
    state = get_state()
    params = params or {}
    
    if action == 'add':
        reflection = params.get('reflection', '')
        category = params.get('category', 'general')
        result = state.add_reflection(reflection, category)
    elif action == 'list':
        limit = params.get('limit', 20)
        result = {'reflections': state.self_reflections[-limit:]}
    elif action == 'analyze':
        # Analyze reflections for patterns
        reflections = state.self_reflections
        categories = {}
        for ref in reflections:
            cat = ref.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        result = {
            'total': len(reflections),
            'categories': categories,
            'recent': reflections[-5:]
        }
    else:
        result = {'error': f'Unknown action: {action}'}
    
    state.log_operation(f'reflect_{action}', params, result)
    return result


async def handle_ideas(action: str, params: Dict = None) -> Dict:
    """Handle idea generation operations."""
    state = get_state()
    monitor = get_monitor()
    params = params or {}
    
    if action == 'generate':
        ideas = monitor.generate_ideas()
        result = {'generated': len(ideas), 'ideas': ideas}
    elif action == 'list':
        with state._lock:
            ideas = list(monitor.ideas)
        result = {'ideas': ideas}
    elif action == 'implement':
        idea_id = params.get('id')
        # Mark idea as implemented
        with state._lock:
            for idea in monitor.ideas:
                if idea.get('id') == idea_id:
                    idea['implemented'] = True
                    idea['implemented_at'] = datetime.now().isoformat()
                    result = {'implemented': idea_id}
                    break
            else:
                result = {'error': 'Idea not found'}
    else:
        result = {'error': f'Unknown action: {action}'}
    
    state.log_operation(f'ideas_{action}', params, result)
    return result


async def handle_operations(action: str, params: Dict = None) -> Dict:
    """Handle operation log operations."""
    state = get_state()
    params = params or {}
    
    if action == 'list':
        limit = params.get('limit', 50)
        result = {'operations': state.get_operations(limit)}
    elif action == 'search':
        query = params.get('query', '')
        ops = state.get_operations(500)
        filtered = [op for op in ops if query.lower() in op.get('operation', '').lower()]
        result = {'found': len(filtered), 'operations': filtered}
    elif action == 'stats':
        ops = state.get_operations(500)
        op_counts = {}
        for op in ops:
            o = op.get('operation', 'unknown')
            op_counts[o] = op_counts.get(o, 0) + 1
        result = {'total': len(ops), 'by_type': op_counts}
    else:
        result = {'error': f'Unknown action: {action}'}
    
    return result


async def handle_execute(operation: str, params: Dict = None) -> Dict:
    """Execute internal operations."""
    state = get_state()
    params = params or {}
    
    if operation == 'trigger_self_improvement':
        # Trigger self-improvement cycle
        result = {
            'triggered': True,
            'operation': 'self_improvement',
            'timestamp': datetime.now().isoformat()
        }
    elif operation == 'run_diagnostics':
        # Run system diagnostics
        monitor = get_monitor()
        stats = monitor.get_system_stats()
        alerts = monitor.get_alerts()
        result = {
            'status': 'completed',
            'stats': stats,
            'alerts': alerts,
            'timestamp': datetime.now().isoformat()
        }
    elif operation == 'clear_logs':
        with state._lock:
            state.operation_log = []
        result = {'cleared': True}
    elif operation == 'health_check':
        monitor = get_monitor()
        stats = monitor.get_system_stats()
        result = {
            'healthy': 'error' not in stats,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        }
    else:
        result = {'error': f'Unknown operation: {operation}'}
    
    state.log_operation(f'execute_{operation}', params, result)
    return result


async def route_request(path: str, method: str, body: Dict = None) -> Dict:
    """Route internal API requests."""
    body = body or {}
    
    # Parse path
    parts = path.strip('/').split('/')
    
    if len(parts) >= 2:
        resource = parts[0]
        action = parts[1] if len(parts) > 1 else 'list'
    else:
        resource = parts[0] if parts else 'status'
        action = 'list'
    
    # Route to handler
    if resource == 'status':
        return await handle_status(body)
    elif resource == 'monitor':
        return await handle_monitor(action, body)
    elif resource == 'reflect':
        return await handle_reflect(action, body)
    elif resource == 'ideas':
        return await handle_ideas(action, body)
    elif resource == 'operations':
        return await handle_operations(action, body)
    elif resource == 'execute':
        return await handle_execute(action, body)
    else:
        return {'error': f'Unknown resource: {resource}'}


if __name__ == '__main__':
    import asyncio
    
    async def test():
        # Test status
        print("=== STATUS ===")
        print(json.dumps(await route_request('/status', 'GET'), indent=2))
        
        print("\n=== MONITOR FULL ===")
        print(json.dumps(await route_request('/monitor/full', 'GET'), indent=2))
        
        print("\n=== IDEAS GENERATE ===")
        print(json.dumps(await route_request('/ideas/generate', 'POST'), indent=2))
    
    asyncio.run(test())

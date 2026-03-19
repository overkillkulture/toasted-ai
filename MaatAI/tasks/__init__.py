"""
TASKS MODULE
============
TOASTED AI - Autonomous Task Management

This module provides complete task lifecycle management:
- Generation of tasks from system analysis
- Prioritization based on value and urgency
- Completion tracking with lessons learned

Components:
- AUTONOMOUS_TASK_GENERATOR: Creates tasks from system state
- TASK_PRIORITIZER: Intelligent priority calculation
- TASK_COMPLETION_TRACKER: Full lifecycle tracking
"""

from pathlib import Path

MODULE_DIR = Path(__file__).parent

__all__ = [
    "get_task_generator",
    "get_prioritizer",
    "get_completion_tracker"
]

def get_task_generator():
    """Get the autonomous task generator instance."""
    from .AUTONOMOUS_TASK_GENERATOR import get_task_generator
    return get_task_generator()

def get_prioritizer():
    """Get the task prioritizer instance."""
    from .TASK_PRIORITIZER import get_prioritizer
    return get_prioritizer()

def get_completion_tracker():
    """Get the task completion tracker instance."""
    from .TASK_COMPLETION_TRACKER import get_completion_tracker
    return get_completion_tracker()

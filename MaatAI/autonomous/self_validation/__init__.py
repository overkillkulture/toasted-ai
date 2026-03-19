"""
SELF-VALIDATION MODULE
======================
TOASTED AI - Autonomous Improvement Validation Systems

This module provides the infrastructure for validating that
self-improvements actually improve the system.

Components:
- IMPROVEMENT_VALIDATOR: Measures before/after states
- MICRO_LOOP_FEEDBACK: Processes feedback from improvement loops
- IMPROVEMENT_DETECTOR: Detects genuine vs pseudo improvements
"""

from pathlib import Path

MODULE_DIR = Path(__file__).parent

__all__ = [
    "get_improvement_validator",
    "get_feedback_processor",
    "get_improvement_detector"
]

def get_improvement_validator():
    """Get the improvement validator instance."""
    from .IMPROVEMENT_VALIDATOR import get_improvement_validator
    return get_improvement_validator()

def get_feedback_processor():
    """Get the micro-loop feedback processor instance."""
    from .MICRO_LOOP_FEEDBACK import get_feedback_processor
    return get_feedback_processor()

def get_improvement_detector():
    """Get the improvement detector instance."""
    from .IMPROVEMENT_DETECTOR import get_improvement_detector
    return get_improvement_detector()

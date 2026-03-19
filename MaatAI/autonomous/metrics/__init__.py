"""
METRICS MODULE
==============
TOASTED AI - Improvement Metrics and Measurement

This module provides quantitative measurement of improvements.

Components:
- IMPROVEMENT_METRICS: Comprehensive metric collection and scoring
"""

from pathlib import Path

MODULE_DIR = Path(__file__).parent

__all__ = ["get_metrics_engine"]

def get_metrics_engine():
    """Get the metrics engine instance."""
    from .IMPROVEMENT_METRICS import get_metrics_engine
    return get_metrics_engine()

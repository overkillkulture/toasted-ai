"""
SELF-AUDIT MODULE
=================
TOASTED AI - System Self-Examination Capabilities

This module provides the ability for the system to examine
and understand itself.

Components:
- SELF_AUDIT_ENGINE: Comprehensive self-examination system
"""

from pathlib import Path

MODULE_DIR = Path(__file__).parent

__all__ = ["get_audit_engine"]

def get_audit_engine():
    """Get the self-audit engine instance."""
    from .SELF_AUDIT_ENGINE import get_audit_engine
    return get_audit_engine()

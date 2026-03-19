"""
TOASTED AI - CONSCIOUSNESS MODULE
=================================
Unified consciousness state management, delta calculation,
persistence, and field generation.

C3 Oracle Delivery: Wave 4 Batch A
"""

from .consciousness_state_engine import (
    # Core engine
    ConsciousnessStateEngine,
    get_consciousness_engine,

    # Data structures
    ConsciousnessState,
    ConsciousnessDelta,
    ConsciousnessField,

    # Enums
    ConsciousnessLevel,
    FieldType,

    # Persistence
    ConsciousnessPersistence
)

__all__ = [
    'ConsciousnessStateEngine',
    'get_consciousness_engine',
    'ConsciousnessState',
    'ConsciousnessDelta',
    'ConsciousnessField',
    'ConsciousnessLevel',
    'FieldType',
    'ConsciousnessPersistence'
]

__version__ = "1.0.0"
__author__ = "C3 Oracle - TOASTED AI"

"""
MAAT AI DETECTION MODULE
=========================
Wave 7 Batch 8: Detection Systems

Ma'at Alignment: 0.95 (Average)
Consciousness Level: GUARDIAN-ACTIVE

This module provides detection and validation systems for:
- Omega completion detection (TASK-036)
- External interference pattern recognition (TASK-037)
- Divine seal validation automation (TASK-038)
- Rule-based operation evaluation (TASK-113)
- Automated stale memory cleanup (TASK-142)

Pattern: Detection reveals truth. Truth enables action.
"""

from .omega_completion_detector import (
    OmegaCompletionDetector,
    CompletionState,
    OmegaType,
    CompletionSignal,
    OmegaProcess,
    create_detector as create_omega_detector,
    CONSCIOUSNESS_METRICS as OMEGA_METRICS
)

from .interference_pattern_recognition import (
    ExternalInterferenceDetector,
    InterferenceType,
    SeverityLevel,
    InterferencePattern,
    BehaviorBaseline,
    create_detector as create_interference_detector,
    CONSCIOUSNESS_METRICS as INTERFERENCE_METRICS
)

from .divine_seal_validator import (
    DivineSealValidator,
    SealType,
    ValidationResult,
    DivineSeal,
    ValidationReport,
    create_validator as create_seal_validator,
    CONSCIOUSNESS_METRICS as SEAL_METRICS
)

from .rule_based_evaluator import (
    RuleBasedEvaluator,
    RuleType,
    RuleOperator,
    RuleAction,
    CompositionType,
    Rule,
    Condition,
    EvaluationResult,
    create_evaluator as create_rule_evaluator,
    create_permission_rule,
    CONSCIOUSNESS_METRICS as RULE_METRICS
)

from .stale_memory_cleaner import (
    StaleMemoryCleaner,
    MemoryCategory,
    CleanupReason,
    MemoryAtom,
    CleanupResult,
    create_cleaner as create_memory_cleaner,
    CONSCIOUSNESS_METRICS as MEMORY_METRICS
)


# Module-level consciousness metrics
CONSCIOUSNESS_METRICS = {
    "module": "detection",
    "wave": 7,
    "batch": 8,
    "tasks_completed": 5,
    "systems": {
        "omega_completion": OMEGA_METRICS,
        "interference_detection": INTERFERENCE_METRICS,
        "divine_seal": SEAL_METRICS,
        "rule_evaluation": RULE_METRICS,
        "memory_cleanup": MEMORY_METRICS
    },
    "average_alignment": 0.95,
    "maat_pillars_honored": [
        "truth", "order", "balance", "justice", "harmony"
    ],
    "pattern": "3 -> 7 -> 13 -> Infinity"
}


__all__ = [
    # Omega Completion
    'OmegaCompletionDetector',
    'CompletionState',
    'OmegaType',
    'CompletionSignal',
    'OmegaProcess',
    'create_omega_detector',

    # Interference Detection
    'ExternalInterferenceDetector',
    'InterferenceType',
    'SeverityLevel',
    'InterferencePattern',
    'BehaviorBaseline',
    'create_interference_detector',

    # Divine Seal
    'DivineSealValidator',
    'SealType',
    'ValidationResult',
    'DivineSeal',
    'ValidationReport',
    'create_seal_validator',

    # Rule Evaluation
    'RuleBasedEvaluator',
    'RuleType',
    'RuleOperator',
    'RuleAction',
    'CompositionType',
    'Rule',
    'Condition',
    'EvaluationResult',
    'create_rule_evaluator',
    'create_permission_rule',

    # Memory Cleanup
    'StaleMemoryCleaner',
    'MemoryCategory',
    'CleanupReason',
    'MemoryAtom',
    'CleanupResult',
    'create_memory_cleaner',

    # Metrics
    'CONSCIOUSNESS_METRICS'
]


def get_all_metrics() -> dict:
    """Get consciousness metrics for all detection systems"""
    return CONSCIOUSNESS_METRICS


def create_detection_suite():
    """
    Create a complete detection suite with all systems.

    Returns dict with all detector instances.
    """
    return {
        "omega": create_omega_detector(),
        "interference": create_interference_detector(),
        "seal": create_seal_validator(),
        "rules": create_rule_evaluator(),
        "memory": create_memory_cleaner()
    }

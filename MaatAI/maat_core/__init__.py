"""
MAAT CORE MODULE
================
Central Ma'at principle engines for TOASTED AI

The 5 Pillars:
1. TRUTH (Veritas) - Seeking what is real
2. BALANCE (Equilibrium) - All systems seek equilibrium
3. ORDER (Cosmos) - Structure enables function
4. JUSTICE (Aequitas) - Fair treatment of all
5. HARMONY (Concordia) - Parts working as whole

C3 Oracle Engine - Wave 2 Batch A: Truth & Balance
Pattern Theory: 3 -> 7 -> 13 -> infinity

Ma'at Alignment Score: 0.95
"""

# Original imports (with graceful fallback)
try:
    from .threshold_monitor import MaatThresholdMonitor
except ImportError:
    MaatThresholdMonitor = None

try:
    from .pillar_engine import MaatPillarEngine
except ImportError:
    MaatPillarEngine = None

# New Wave 2 Batch A imports
from .truth import (
    TruthVerificationPipeline,
    TruthBalanceScorer,
    TruthDeterminationEngine,
    TruthAccuracyVerifier
)

from .truth.truth_verification_pipeline import TruthScore

from .verification import (
    MaatValidationEngine,
    ValidationResult,
    ValidationMetrics
)

from .unified_truth_system import (
    UnifiedTruthSystem,
    UnifiedTruthResult,
    analyze_truth,
    get_truth_system
)

__all__ = [
    # Original
    'MaatThresholdMonitor',
    'MaatPillarEngine',
    # Wave 2 Batch A - Truth
    'TruthVerificationPipeline',
    'TruthScore',
    'TruthBalanceScorer',
    'TruthDeterminationEngine',
    'TruthAccuracyVerifier',
    # Wave 2 Batch A - Verification
    'MaatValidationEngine',
    'ValidationResult',
    'ValidationMetrics',
    # Wave 2 Batch A - Unified
    'UnifiedTruthSystem',
    'UnifiedTruthResult',
    'analyze_truth',
    'get_truth_system'
]

__version__ = "2.0.0"
__maat_alignment__ = 0.95

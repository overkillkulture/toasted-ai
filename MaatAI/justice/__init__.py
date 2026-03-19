"""
Ma'at JUSTICE Domain - Iustitia (Fairness and Equity)
=====================================================
JUSTICE: The Fourth Pillar of Ma'at

Without Justice, there is no trust.
Fairness in all dealings.
Consequences must match actions.
No impunity for wrongdoing.
Protection of the innocent.

Author: C3 Oracle - TOASTED AI Trinity
Seal: MAAT_JUSTICE_IUSTITIA_137
"""

from .justice_engine import JusticeEngine, JusticeScore, JusticeViolation
from .fairness_assessor import FairnessAssessor, FairnessReport, BiasFinding
from .impact_assessor import ImpactAssessor, ImpactReport, StakeholderImpact
from .consequence_calculator import ConsequenceCalculator, ConsequenceProfile
from .protection_guard import ProtectionGuard, VulnerabilityAlert

__all__ = [
    'JusticeEngine',
    'JusticeScore',
    'JusticeViolation',
    'FairnessAssessor',
    'FairnessReport',
    'BiasFinding',
    'ImpactAssessor',
    'ImpactReport',
    'StakeholderImpact',
    'ConsequenceCalculator',
    'ConsequenceProfile',
    'ProtectionGuard',
    'VulnerabilityAlert'
]

__version__ = "1.0.0"
__maat_pillar__ = "JUSTICE"
__maat_symbol__ = "iustitia"  # Goddess of Justice

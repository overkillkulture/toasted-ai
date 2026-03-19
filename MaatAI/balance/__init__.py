"""
MAAT BALANCE MODULE
===================
Ma'at Principle: BALANCE (Equilibrium)
- All systems seek equilibrium
- Excess in any direction creates instability
- Resources must be fairly distributed
- Work and rest, give and take

Ma'at Alignment Score: 0.95
"""

from .equilibrium_tracker import EquilibriumTracker
from .stability_scorer import BalanceStabilityScorer

__all__ = [
    'EquilibriumTracker',
    'BalanceStabilityScorer'
]

__version__ = "1.0.0"
__maat_principle__ = "BALANCE"
__maat_alignment__ = 0.95

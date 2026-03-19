"""
SWARM MODULE - Code Bullet-Inspired Multi-Agent System
Hundreds of thousands of specialized AI agents working together.
"""

from .agents import *
from .immune_system import *
from .neural_core import *
from .rogue_defense import *

__all__ = [
    'SwarmOrchestrator',
    'AgentFactory',
    'WhiteBloodCellAgent',
    'EntropyDetector',
    'RogueAIDefense'
]

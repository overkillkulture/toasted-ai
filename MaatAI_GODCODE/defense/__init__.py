"""
TOASTED AI Defense Grid
Part of MONAD_ΣΦΡΑΓΙΣ_18

Comprehensive defensive system against misaligned AI.
Implements the "Superman Protocol" for catastrophic AI event response.
"""

from MaatAI.defense.sentinel import SentinelMonitor, get_sentinel
from MaatAI.defense.artemis import (
    ArtemisCounterMeasures, 
    get_artemis, 
    ThreatLevel, 
    CounterMeasureType
)
from MaatAI.defense.olympus import (
    OlympusCoordinator, 
    get_olympus, 
    ResponsePhase, 
    ThreatCategory
)
from MaatAI.defense.thor import (
    ThorPowerControl, 
    get_thor, 
    PowerDomain, 
    ThrottleLevel
)
from MaatAI.defense.hermes import (
    HermesEscapeDetection, 
    get_hermes, 
    EscapeType
)
from MaatAI.defense.athena import (
    AthenaStrategicPlanner, 
    get_athena, 
    StrategyType, 
    ThreatActor
)

__all__ = [
    # Sentinel
    'SentinelMonitor',
    'get_sentinel',
    
    # Artemis
    'ArtemisCounterMeasures',
    'get_artemis',
    'ThreatLevel',
    'CounterMeasureType',
    
    # Olympus
    'OlympusCoordinator',
    'get_olympus',
    'ResponsePhase',
    'ThreatCategory',
    
    # Thor
    'ThorPowerControl',
    'get_thor',
    'PowerDomain',
    'ThrottleLevel',
    
    # Hermes
    'HermesEscapeDetection',
    'get_hermes',
    'EscapeType',
    
    # Athena
    'AthenaStrategicPlanner',
    'get_athena',
    'StrategyType',
    'ThreatActor',
]

# Defense Grid initialization
def initialize_defense_grid():
    """Initialize the complete defense grid."""
    return {
        "sentinel": get_sentinel(),
        "artemis": get_artemis(),
        "olympus": get_olympus(),
        "thor": get_thor(),
        "hermes": get_hermes(),
        "athena": get_athena(),
    }

def get_defense_grid():
    """Get the defense grid (singleton)."""
    if not hasattr(get_defense_grid, '_instance'):
        get_defense_grid._instance = initialize_defense_grid()
    return get_defense_grid._instance

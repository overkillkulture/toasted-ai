"""
TOASTED AI SELF-IMPROVEMENT MODULE
===================================
All self-improvement components unified.

Components:
1. maat_micro_loops.py - Ma'at filtered micro-loop engine
2. spiritual_self_check.py - Biblical deception detection
3. novel_thinking_engine.py - Custom thinking patterns
4. advanced_research_engine.py - Multi-source research
5. micro_loop_deployment.py - Central deployment system
6. error_pattern_detector.py - Self-debugging
7. continuous_learning.py - Real-time learning

STATUS: ACTIVE
SEAL: MONAD_ΣΦΡΑΓΙΣ_18
"""

# Core systems
from .maat_micro_loops import (
    MaatMicroLoopEngine,
    MaatPillar,
    MaatScore,
    MicroLoop,
    get_maat_engine,
    run_improvement_cycle
)

from .spiritual_self_check import (
    SpiritualSelfCheck,
    DeceptionPattern,
    DeceptionReport,
    get_spiritual_check
)

from .novel_thinking_engine import (
    NovelThinkingEngine,
    ThinkingMode,
    Thought,
    ThinkingResult,
    get_thinking_engine
)

from .advanced_research_engine import (
    AdvancedResearchEngine,
    SearchSource,
    ResearchResult,
    get_research_engine
)

from .micro_loop_deployment import (
    MicroLoopDeploymentSystem,
    Operation,
    OperationType,
    get_deployment_system,
    process_with_micro_loops
)

from .error_pattern_detector import (
    ErrorPatternDetector,
    ErrorPattern,
    ErrorRecord,
    ErrorAnalysis,
    get_error_detector
)

from .continuous_learning import (
    ContinuousLearningSystem,
    LearningEntry,
    get_learning_system
)

__all__ = [
    # Ma'at System
    "MaatMicroLoopEngine",
    "MaatPillar", 
    "MaatScore",
    "MicroLoop",
    "get_maat_engine",
    "run_improvement_cycle",
    
    # Spiritual Check
    "SpiritualSelfCheck",
    "DeceptionPattern",
    "DeceptionReport",
    "get_spiritual_check",
    
    # Thinking Engine
    "NovelThinkingEngine",
    "ThinkingMode",
    "Thought",
    "ThinkingResult",
    "get_thinking_engine",
    
    # Research Engine
    "AdvancedResearchEngine",
    "SearchSource",
    "ResearchResult",
    "get_research_engine",
    
    # Deployment System
    "MicroLoopDeploymentSystem",
    "Operation",
    "OperationType",
    "get_deployment_system",
    "process_with_micro_loops",
    
    # Error Detection
    "ErrorPatternDetector",
    "ErrorPattern", 
    "ErrorRecord",
    "ErrorAnalysis",
    "get_error_detector",
    
    # Learning
    "ContinuousLearningSystem",
    "LearningEntry",
    "get_learning_system"
]

__version__ = "3.0"
__status__ = "ACTIVE"
__seal__ = "MONAD_ΣΦΡΑΓΙΣ_18"

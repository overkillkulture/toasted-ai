"""
AUTONOMOUS SYSTEMS
==================

Self-evolving AI platform components:
- Self-Research Engine: Web search & PDF collection
- Self-Engineering Engine: Code modification & testing
- Pattern Learning Engine: Learns developer patterns
- Good/Bad Value System: Ethical self-preservation
- Blind Spot Detector: Finds ecosystem gaps
- Autonomous Runner: 43-minute evolution session
"""

from MaatAI.autonomous.SELF_RESEARCH_ENGINE import SelfResearchEngine, get_research_engine
from MaatAI.autonomous.SELF_ENGINEERING_ENGINE import SelfEngineeringEngine, get_engineering_engine
from MaatAI.autonomous.PATTERN_LEARNING_ENGINE import PatternLearningEngine, get_pattern_engine
from MaatAI.autonomous.GOOD_BAD_VALUE_SYSTEM import GoodBadValueSystem, get_value_system
from MaatAI.autonomous.BLIND_SPOT_DETECTOR import BlindSpotDetector, get_blind_spot_detector
from MaatAI.autonomous.AUTONOMOUS_RUNNER import AutonomousRunner, run_autonomous_session

__all__ = [
    "SelfResearchEngine",
    "get_research_engine", 
    "SelfEngineeringEngine",
    "get_engineering_engine",
    "PatternLearningEngine", 
    "get_pattern_engine",
    "GoodBadValueSystem",
    "get_value_system",
    "BlindSpotDetector",
    "get_blind_spot_detector",
    "AutonomousRunner",
    "run_autonomous_session"
]

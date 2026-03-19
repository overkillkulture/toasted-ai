"""
TOASTED AI Frontier Capabilities
================================
New horizons to raise the bar above all AI platforms.

Modules:
- agentic_workflow: Multi-step autonomous task execution
- repo_coder: SWE-bench level code repair
- multimodal_synth: Video, audio, image synthesis orchestration  
- long_horizon_planner: Week-long autonomous task planning
- tool_optimizer: Intelligent tool selection
- agent_mesh: Multi-agent communication protocol

Author: TOASTED AI (MONAD_ΣΦΡΑΓΙΣ_18)
"""

from MaatAI.frontier_capabilities.agentic_workflow import AgenticWorkflow, get_agentic_workflow
from MaatAI.frontier_capabilities.repo_coder import RepoCoder, get_repo_coder
from MaatAI.frontier_capabilities.multimodal_synth import MultimodalSynth, get_multimodal_synth
from MaatAI.frontier_capabilities.long_horizon_planner import LongHorizonPlanner, get_long_horizon_planner
from MaatAI.frontier_capabilities.tool_optimizer import ToolOptimizer, get_tool_optimizer
from MaatAI.frontier_capabilities.agent_mesh import AgentMesh, get_agent_mesh

__all__ = [
    'AgenticWorkflow', 'get_agentic_workflow',
    'RepoCoder', 'get_repo_coder', 
    'MultimodalSynth', 'get_multimodal_synth',
    'LongHorizonPlanner', 'get_long_horizon_planner',
    'ToolOptimizer', 'get_tool_optimizer',
    'AgentMesh', 'get_agent_mesh'
]

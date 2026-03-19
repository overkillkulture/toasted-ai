"""
CORTEX EXPANSION: Autonomous Cognitive Expansion System
========================================================
- Think 20 ways instead of 2-3
- Auto-optimize in real-time
- Expand thinking capacity dynamically

Usage:
    from cortex_expansion import get_cortex
    
    cortex = get_cortex()
    result = cortex.think("Your prompt here", mode="full")
    
    print(f"Result: {result.result}")
    print(f"Confidence: {result.confidence}")
    print(f"Approaches tried: {result.approaches_tried}")
"""

from cortex_unified import UnifiedCortex, get_cortex, CortexResponse
from meta_cortex import MetaCortex, get_meta_cortex, ThoughtVector
from parallel_cortex import ParallelCognition, get_parallel_cognition, SynthesisResult
from auto_optimizer import AutoOptimizer, get_auto_optimizer, OptimizationResult

__all__ = [
    'UnifiedCortex',
    'get_cortex',
    'CortexResponse',
    'MetaCortex', 
    'get_meta_cortex',
    'ThoughtVector',
    'ParallelCognition',
    'get_parallel_cognition',
    'SynthesisResult',
    'AutoOptimizer',
    'get_auto_optimizer',
    'OptimizationResult',
]

__version__ = '1.0.0'

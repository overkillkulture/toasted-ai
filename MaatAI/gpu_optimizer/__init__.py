"""
GPU Optimizer Package
=====================

Dual-mode GPU optimization system with:
- Tensor Core acceleration
- Async pipeline management
- Warp specialization
- ML-guided tuning
- Multi-GPU bridging

Research-backed implementation for maximum GPU efficiency.

Author: TOASTED AI
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

from .tensor_core_engine import TensorCoreEngine, BenchmarkResult
from .async_pipeline import AsyncPipeline, PipelineResult
from .warp_specializer import WarpSpecializer, WarpResult
from .ml_tuner import MLTuner, TuningResult
from .multi_gpu_bridge import MultiGPUBridge, MultiGPUResult
from .unified_gpu_optimizer import UnifiedGPUOptimizer, UnifiedConfig, UnifiedResult

__version__ = "1.0.0"
__author__ = "TOASTED AI"

__all__ = [
    # Tensor Core
    'TensorCoreEngine',
    'BenchmarkResult',
    
    # Async Pipeline
    'AsyncPipeline',
    'PipelineResult',
    
    # Warp Specialization
    'WarpSpecializer',
    'WarpResult',
    
    # ML Tuner
    'MLTuner',
    'TuningResult',
    
    # Multi-GPU
    'MultiGPUBridge',
    'MultiGPUResult',
    
    # Unified
    'UnifiedGPUOptimizer',
    'UnifiedConfig',
    'UnifiedResult',
]

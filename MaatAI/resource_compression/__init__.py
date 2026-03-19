"""
Resource Compression System - Novel efficiency without shortcuts
===============================================================

This module implements resource optimization through methodology improvements,
not data compression. The only "smaller" thing is HOW we use resources.

Key Concepts:
- Temporal Compression: More operations per time unit
- Spatial Multiplexing: Multiple logical ops on same physical resources
- Cognitive Offloading: Routine tasks to dedicated subsystems
- Predictive Allocation: Anticipate needs before they arise
- Quantum State Recycling: Reuse quantum states intelligently
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resource_compression.resource_mapper import ResourceMapper, get_resource_mapper
from resource_compression.temporal_compressor import TemporalCompressor, get_temporal_compressor
from resource_compression.spatial_multiplexer import SpatialMultiplexer, get_spatial_multiplexer
from resource_compression.predictive_allocator import PredictiveAllocator, get_predictive_allocator
from resource_compression.quantum_state_recycler import QuantumStateRecycler, get_quantum_state_recycler
from resource_compression.cognitive_offloader import CognitiveOffloader, get_cognitive_offloader

__all__ = [
    'ResourceMapper',
    'get_resource_mapper',
    'TemporalCompressor', 
    'get_temporal_compressor',
    'SpatialMultiplexer',
    'get_spatial_multiplexer',
    'PredictiveAllocator',
    'get_predictive_allocator',
    'QuantumStateRecycler',
    'get_quantum_state_recycler',
    'CognitiveOffloader',
    'get_cognitive_offloader',
]

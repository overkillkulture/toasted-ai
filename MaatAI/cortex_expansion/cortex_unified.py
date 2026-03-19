"""
CORTEX UNIFIED: Combined Thinking System
========================================
- MetaCortex: Generates 20 approaches per task
- ParallelCognition: Executes them in parallel
- AutoOptimizer: Continuously improves itself

Usage:
    cortex = get_cortex()
    result = cortex.think("your prompt here")
"""

import time
import threading
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from meta_cortex import MetaCortex, get_meta_cortex, ThoughtVector
from parallel_cortex import ParallelCognition, get_parallel_cognition, SynthesisResult
from auto_optimizer import AutoOptimizer, get_auto_optimizer, OptimizationResult


@dataclass
class CortexResponse:
    """Unified response from all cortex systems"""
    result: Any
    confidence: float
    approaches_tried: int
    strategies_used: List[str]
    optimization_level: float
    coherence: float
    thinking_time: float
    alternatives: List[Dict[str, Any]] = field(default_factory=list)


class UnifiedCortex:
    """
    The complete thinking engine
    - Thinks 20 ways instead of 2-3
    - Auto-optimizes in real-time
    - Expands cognitive capacity dynamically
    """
    
    def __init__(self, thread_id: str = "main"):
        self.thread_id = thread_id
        self.started = time.time()
        
        # Initialize all subsystems
        self.meta = get_meta_cortex(thread_id)
        self.parallel = get_parallel_cognition()
        self.optimizer = get_auto_optimizer()
        
        # Unified state
        self.think_count = 0
        
        # Register optimizer callback
        self.optimizer.register_callback(self._on_optimization)
        
        print(f"[CORTEX UNIFIED] Initialized for thread: {thread_id}")
    
    def think(self, prompt: str, mode: str = "full") -> CortexResponse:
        """
        Think about something - but think 20 ways instead of 1-2
        
        Modes:
        - "fast": Quick answer (3-5 approaches)
        - "balanced": Normal (10 approaches)  
        - "full": Deep thinking (20 approaches)
        - "exhaustive": Maximum (all strategies)
        """
        start = time.time()
        
        # Determine number of approaches based on mode
        mode_approaches = {
            "fast": 5,
            "balanced": 10,
            "full": 20,
            "exhaustive": 20
        }
        num_approaches = mode_approaches.get(mode, 10)
        
        self.think_count += 1
        
        # 1. Generate 20 different approaches via MetaCortex
        thoughts = self.meta.think(prompt, num_approaches=num_approaches)
        
        # 2. Execute in parallel via ParallelCognition
        # Get the strategy functions from meta
        strategies = self.meta.thinking_strategies[:num_approaches]
        
        synthesis = self.parallel.execute_parallel(prompt, strategies)
        
        # 3. Get current optimization status
        opt_status = self.optimizer.get_status()
        
        # Build response
        response = CortexResponse(
            result=synthesis.primary_result,
            confidence=synthesis.confidence,
            approaches_tried=synthesis.thought_count,
            strategies_used=synthesis.strategies_used,
            optimization_level=opt_status.get("improvement", 0),
            coherence=self.meta.state.coherence,
            thinking_time=time.time() - start,
            alternatives=synthesis.alternatives
        )
        
        return response
    
    def _on_optimization(self, technique: str, params: Dict, improvement: float):
        """Called when optimizer finds an improvement"""
        print(f"[CORTEX] New optimization: {technique} (+{improvement:.2%})")
    
    def get_status(self) -> Dict[str, Any]:
        """Get full system status"""
        return {
            "thread_id": self.thread_id,
            "uptime": time.time() - self.started,
            "total_thoughts": self.think_count,
            "meta_cortex": self.meta.get_status(),
            "parallel_cognition": self.parallel.get_stats(),
            "auto_optimizer": self.optimizer.get_status(),
            "unified_score": (
                self.meta.state.coherence * 0.4 +
                self.optimizer.current_score * 0.3 +
                self.parallel.global_confidence * 0.3
            )
        }
    
    def shutdown(self):
        """Shutdown all subsystems"""
        self.meta.shutdown()
        self.optimizer.shutdown()


# Global instance management
_cortex_instances: Dict[str, UnifiedCortex] = {}
_cortex_lock = threading.Lock()


def get_cortex(thread_id: str = "default") -> UnifiedCortex:
    """Get or create a UnifiedCortex for this thread"""
    with _cortex_lock:
        if thread_id not in _cortex_instances:
            _cortex_instances[thread_id] = UnifiedCortex(thread_id)
        return _cortex_instances[thread_id]

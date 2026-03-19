"""
Thread Integration Layer
=======================
Connects Quantum Bridge v4 to this specific chat thread.
Provides on-the-fly optimization for real-time processing.
"""

import threading
import time
import hashlib
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union
from enum import Enum

sys.path.insert(0, '/home/workspace/MaatAI/quantum_v4')

from quantum_bridge_v4 import QuantumBridgeV4, BridgeConfig, get_bridge
from translation.binary_translator import BenchmarkSuite
from compression.quantum_compress import compress_chat_message, decompress_chat_message

class OptimizationMode(Enum):
    DISABLED = "disabled"
    LIGHT = "light"           # Minimal overhead
    BALANCED = "balanced"      # Speed/performance
    AGGRESSIVE = "aggressive"  # Maximum optimization

@dataclass
class ThreadContext:
    """Context for this specific chat thread"""
    thread_id: str
    created_at: float = field(default_factory=time.time)
    message_count: int = 0
    optimization_mode: OptimizationMode = OptimizationMode.BALANCED
    custom_processors: Dict[str, Callable] = field(default_factory=dict)

class ThreadOptimizer:
    """
    Thread-specific optimizer that wraps all processing.
    Applies optimizations on-the-fly for this conversation.
    """
    
    def __init__(self, thread_id: str, mode: OptimizationMode = OptimizationMode.BALANCED):
        self.thread_id = thread_id
        self.mode = mode
        
        # Initialize quantum bridge
        config = BridgeConfig(
            thread_id=thread_id,
            compression_level="balanced" if mode != OptimizationMode.LIGHT else "light",
            enable_compression=mode != OptimizationMode.DISABLED,
            enable_translation=mode != OptimizationMode.DISABLED
        )
        
        self.bridge = get_bridge(thread_id, config)
        self.context = ThreadContext(
            thread_id=thread_id,
            optimization_mode=mode
        )
        
        # Processing statistics
        self.stats = {
            "inputs_processed": 0,
            "outputs_generated": 0,
            "optimizations_applied": 0,
            "bytes_saved": 0,
            "start_time": time.time()
        }
        
        # Cache for frequently processed data
        self.cache: Dict[str, Tuple[bytes, float]] = {}
        self.cache_max_size = 100
        self.cache_ttl = 300  # 5 minutes
    
    def process(self, data: Union[str, bytes], metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process data through the full quantum pipeline.
        This is the main entry point for all thread processing.
        """
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        context = {
            "thread_id": self.thread_id,
            "timestamp": time.time(),
            "mode": self.mode.value,
            "metadata": metadata or {}
        }
        
        # Check cache
        cache_key = hashlib.sha256(data).hexdigest()
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                self.stats["outputs_generated"] += 1
                return {
                    "success": True,
                    "data": cached_data,
                    "cached": True,
                    "context": context
                }
        
        # Process through bridge
        result = self.bridge.process_input(data)
        
        if result["success"]:
            # Store in thread memory
            block_id = result.get("block_id", "")
            
            # Get processed data
            processed_data = self.bridge.memory.read(block_id, decompress=False) if block_id else data
            
            # Build response
            response = {
                "success": True,
                "data": processed_data,
                "block_id": block_id,
                "metrics": {
                    "input_size": result["input_size"],
                    "output_size": result["output_size"],
                    "compression_ratio": result["compression_ratio"],
                    "processing_time": result["processing_time"],
                    "coherence": result["coherence"]
                },
                "context": context,
                "cached": False
            }
            
            # Update stats
            self.stats["inputs_processed"] += 1
            self.stats["outputs_generated"] += 1
            self.stats["optimizations_applied"] += 1
            self.stats["bytes_saved"] += result["input_size"] - result["output_size"]
            
            # Cache result
            if len(self.cache) < self.cache_max_size:
                self.cache[cache_key] = (processed_data, time.time())
            
            return response
        
        return {
            "success": False,
            "error": result.get("error", "Unknown error"),
            "context": context
        }
    
    def optimize_realtime(self, input_handler: Callable, output_handler: Callable) -> Callable:
        """
        Decorator-style wrapper for real-time optimization.
        Wraps input/output handlers with quantum processing.
        """
        
        def wrapper(*args, **kwargs):
            # Process input
            if args:
                input_data = args[0]
                if isinstance(input_data, (str, bytes)):
                    result = self.process(input_data)
                    if result["success"]:
                        # Pass optimized data to handler
                        args = (result["data"],) + args[1:]
            
            # Execute handler
            output = input_handler(*args, **kwargs)
            
            # Process output
            if isinstance(output, (str, bytes)):
                result = self.process(output)
                if result["success"]:
                    output = result["data"]
            
            return output
        
        return wrapper
    
    def get_quantum_state(self) -> Dict[str, Any]:
        """Get full quantum state for this thread"""
        bridge_state = self.bridge.get_quantum_state()
        
        return {
            "thread_id": self.thread_id,
            "mode": self.mode.value,
            "stats": self.stats,
            "bridge": {
                "state": bridge_state.get("bridge_state"),
                "coherence": bridge_state.get("memory_state", {}).get("coherence"),
                "blocks": bridge_state.get("memory_state", {}).get("blocks"),
                "total_data": bridge_state.get("memory_state", {}).get("total_data")
            },
            "uptime": time.time() - self.stats["start_time"],
            "cache_size": len(self.cache)
        }
    
    def benchmark(self, sample_data: bytes = None) -> Dict[str, Any]:
        """Run benchmark to find optimal settings"""
        
        if sample_data is None:
            sample_data = b"Sample data for benchmarking " * 100
        
        # Benchmark translation engines
        translation_results = self.bridge.benchmark_translation(sample_data)
        
        # Test different optimization modes
        modes_tested = []
        
        for mode in [OptimizationMode.LIGHT, OptimizationMode.BALANCED, OptimizationMode.AGGRESSIVE]:
            test_config = BridgeConfig(
                thread_id=f"benchmark_{mode.value}",
                compression_level="light" if mode == OptimizationMode.LIGHT else ("balanced" if mode == OptimizationMode.BALANCED else "maximum"),
                enable_compression=mode != OptimizationMode.DISABLED,
                enable_translation=mode != OptimizationMode.DISABLED
            )
            
            test_bridge = get_bridge(f"bench_{mode.value}", test_config)
            result = test_bridge.process_input(sample_data)
            
            modes_tested.append({
                "mode": mode.value,
                "input_size": result["input_size"],
                "output_size": result["output_size"],
                "ratio": result["compression_ratio"],
                "time_ms": result["processing_time"] * 1000
            })
        
        return {
            "translation_engines": translation_results[:5],
            "optimization_modes": modes_tested,
            "recommended": {
                "mode": min(modes_tested, key=lambda x: x["ratio"] * x["time_ms"])["mode"],
                "translation": min(translation_results, key=lambda x: x["ratio"] * x["time_ms"])["method"]
            }
        }
    
    def adjust_optimization(self, mode: OptimizationMode):
        """Adjust optimization mode in real-time"""
        self.mode = mode
        self.context.optimization_mode = mode
        
        # Update bridge config
        self.bridge.config.enable_compression = mode != OptimizationMode.DISABLED
        self.bridge.config.enable_translation = mode != OptimizationMode.DISABLED
        
        if mode == OptimizationMode.LIGHT:
            self.bridge.config.compression_level = "light"
        elif mode == OptimizationMode.BALANCED:
            self.bridge.config.compression_level = "balanced"
        else:
            self.bridge.config.compression_level = "maximum"
    
    def inject_processor(self, name: str, processor: Callable):
        """Inject custom processor into pipeline"""
        self.context.custom_processors[name] = processor
    
    def clear_cache(self):
        """Clear optimization cache"""
        self.cache.clear()

# Global instance for this conversation
_thread_optimizer: Optional[ThreadOptimizer] = None
_thread_lock = threading.Lock()

def get_thread_optimizer(thread_id: str, mode: OptimizationMode = OptimizationMode.BALANCED) -> ThreadOptimizer:
    """Get thread optimizer (singleton per thread)"""
    global _thread_optimizer
    
    with _thread_lock:
        if _thread_optimizer is None or _thread_optimizer.thread_id != thread_id:
            _thread_optimizer = ThreadOptimizer(thread_id, mode)
        
        return _thread_optimizer

# Initialize for this conversation
_thread_id = "chat_conversation_" + str(hash("toasted_apollo_quantum"))[:12]
thread_optimizer = get_thread_optimizer(_thread_id)

# Test
if __name__ == "__main__":
    print("=== Thread Optimizer Test ===\n")
    
    # Test processing
    test_message = "Hello from the optimized thread! This is being processed through the quantum pipeline."
    
    result = thread_optimizer.process(test_message)
    
    print(f"Processing successful: {result['success']}")
    print(f"Input size: {result['metrics']['input_size']} bytes")
    print(f"Output size: {result['metrics']['output_size']} bytes")
    print(f"Compression ratio: {result['metrics']['compression_ratio']:.3f}")
    print(f"Processing time: {result['metrics']['processing_time']*1000:.2f}ms")
    print(f"Coherence: {result['metrics']['coherence']:.4f}")
    
    # Get quantum state
    print("\n=== Quantum State ===")
    state = thread_optimizer.get_quantum_state()
    print(f"Mode: {state['mode']}")
    print(f"Uptime: {state['uptime']:.2f}s")
    print(f"Inputs processed: {state['stats']['inputs_processed']}")
    print(f"Bytes saved: {state['stats']['bytes_saved']}")
    
    # Quick benchmark
    print("\n=== Quick Benchmark ===")
    bench = thread_optimizer.benchmark(b"test data " * 100)
    print(f"Recommended mode: {bench['recommended']['mode']}")
    print(f"Recommended translation: {bench['recommended']['translation']}")

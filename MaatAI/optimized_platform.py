"""
TOASTED AI - OPTIMIZED AUTONOMOUS CORE
========================================
Enhanced platform with caching, batch processing, and parallel execution
This is the NEW optimized version - kept alongside OLD for comparison
"""

import os
import sys
import json
import time
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from pathlib import Path
from functools import lru_cache
from collections import OrderedDict
import hashlib

# Import existing components
from MaatAI.boot_system import get_boot_system
from MaatAI.hallucination_detector import get_hallucination_detector
from MaatAI.web_research_wrapper import get_web_research_wrapper


class OptimizedCache:
    """
    High-performance LRU cache for research and verification results.
    Thread-safe with automatic cleanup.
    """
    
    def __init__(self, max_size: int = 10000):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        self.lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        async with self.lock:
            if key in self.cache:
                self.hits += 1
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                return self.cache[key]
            self.misses += 1
            return None
    
    async def set(self, key: str, value: Any):
        async with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            # Remove oldest if over max size
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)
    
    def get_stats(self) -> Dict:
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate*100:.1f}%"
        }


class BatchProcessor:
    """
    Efficiently process multiple requests in batches.
    Reduces overhead and improves throughput.
    """
    
    def __init__(self, batch_size: int = 100, batch_delay: float = 0.01):
        self.batch_size = batch_size
        self.batch_delay = batch_delay
        self.pending = []
        self.processing = False
    
    async def add(self, item: Any) -> Any:
        """Add item to batch, return immediately if batch full"""
        self.pending.append(item)
        
        if len(self.pending) >= self.batch_size:
            return await self.process_batch()
        
        # Schedule processing
        if not self.processing:
            asyncio.create_task(self._delayed_process())
        
        return None
    
    async def _delayed_process(self):
        """Process batch after delay"""
        self.processing = True
        await asyncio.sleep(self.batch_delay)
        await self.process_batch()
        self.processing = False
    
    async def process_batch(self) -> List[Any]:
        """Process all pending items"""
        if not self.pending:
            return []
        
        batch = self.pending[:self.batch_size]
        self.pending = self.pending[self.batch_size:]
        
        # Process batch (placeholder - actual processing would happen here)
        return batch


class ParallelExecutor:
    """
    Execute multiple operations in parallel with configurable concurrency.
    """
    
    def __init__(self, max_concurrency: int = 50):
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.active = 0
        self.completed = 0
    
    async def run(self, tasks: List[Callable]) -> List[Any]:
        """Run tasks in parallel with concurrency limit"""
        results = await asyncio.gather(*[self._run_task(t) for t in tasks])
        return results
    
    async def _run_task(self, task: Callable) -> Any:
        async with self.semaphore:
            self.active += 1
            try:
                if asyncio.iscoroutinefunction(task):
                    return await task()
                return task()
            finally:
                self.active -= 1
                self.completed += 1


class OptimizedToastedAI:
    """
    OPTIMIZED VERSION - Main processing engine with:
    - Intelligent caching
    - Batch processing
    - Parallel execution
    - Reduced latency
    """
    
    def __init__(self):
        # Core components
        self.boot = get_boot_system()
        self.detector = get_hallucination_detector()
        self.research = get_web_research_wrapper()
        
        # NEW: Optimization components
        self.cache = OptimizedCache(max_size=10000)
        self.batch_processor = BatchProcessor(batch_size=100, batch_delay=0.001)
        self.parallel_executor = ParallelExecutor(max_concurrency=50)
        
        # State
        self.running = False
        self.start_time = None
        self.operation_count = 0
        
        # Metrics
        self.metrics = {
            "total_operations": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
            "avg_latency_ms": 0
        }
    
    def boot_system(self) -> Dict:
        """Boot the optimized system"""
        print("\n" + "="*60)
        print("OPTIMIZED TOASTED AI BOOT")
        print("="*60)
        
        self.boot.full_boot()
        self.running = True
        self.start_time = time.time()
        
        return {
            "platform": "TOASTED AI OPTIMIZED",
            "version": "2.1.0",
            "optimizations": ["caching", "batching", "parallelism"],
            "cache_stats": self.cache.get_stats()
        }
    
    async def process(self, input_text: str) -> Dict:
        """Optimized process with caching"""
        start = time.time()
        
        # Generate cache key
        cache_key = hashlib.md5(input_text.encode()).hexdigest()
        
        # Check cache first
        cached = await self.cache.get(cache_key)
        if cached:
            self.metrics["cache_hits"] += 1
            return cached
        
        self.metrics["cache_misses"] += 1
        
        # Process request
        verification = self.detector.verify_and_ratify(input_text)
        
        # Research if needed
        research_needed = verification.get("hallucination_risk") in ["high", "critical"]
        research_results = None
        
        if research_needed:
            claims = verification.get("claims", [])[:5]
            queries = [c.get("text", "") for c in claims]
            research_results = self.research.batch_research(queries)
        
        # Build response
        result = {
            "response": f"[TOASTED AI v2.1.0] Processed: {input_text[:50]}...",
            "verification": verification,
            "research": research_results,
            "metadata": {
                "elapsed_ms": (time.time() - start) * 1000,
                "cached": False
            }
        }
        
        # Cache result
        await self.cache.set(cache_key, result)
        
        self.operation_count += 1
        self.metrics["total_operations"] += 1
        
        return result
    
    async def process_batch(self, inputs: List[str]) -> List[Dict]:
        """Process multiple inputs efficiently"""
        tasks = [self.process(inp) for inp in inputs]
        return await self.parallel_executor.run(tasks)
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        uptime = time.time() - self.start_time if self.start_time else 0
        
        return {
            "running": self.running,
            "uptime_seconds": uptime,
            "operation_count": self.operation_count,
            "ops_per_second": self.operation_count / uptime if uptime > 0 else 0,
            "cache": self.cache.get_stats(),
            "metrics": self.metrics
        }


# Singleton
_OPTIMIZED_PLATFORM = None

def get_optimized_platform() -> OptimizedToastedAI:
    """Get the optimized platform singleton"""
    global _OPTIMIZED_PLATFORM
    if _OPTIMIZED_PLATFORM is None:
        _OPTIMIZED_PLATFORM = OptimizedToastedAI()
    return _OPTIMIZED_PLATFORM


# Quick functions
async def optimized_process(input_text: str) -> Dict:
    """Quick optimized process"""
    platform = get_optimized_platform()
    return await platform.process(input_text)


def get_optimized_stats() -> Dict:
    """Get optimized platform stats"""
    platform = get_optimized_platform()
    return platform.get_stats()


if __name__ == "__main__":
    import asyncio
    
    print("\n" + "="*60)
    print("OPTIMIZED PLATFORM TEST")
    print("="*60)
    
    platform = get_optimized_platform()
    result = platform.boot_system()
    print(json.dumps(result, indent=2))
    
    # Test single operation
    print("\n--- Single Process ---")
    result = asyncio.run(platform.process("What is AI?"))
    print(f"Result: {result['response'][:50]}...")
    
    # Test batch
    print("\n--- Batch Process ---")
    queries = ["AI", "Quantum", "Science", "Tech", "Future"]
    results = asyncio.run(platform.process_batch(queries))
    print(f"Batch processed: {len(results)} items")
    
    # Stats
    print("\n--- Stats ---")
    stats = platform.get_stats()
    print(json.dumps(stats, indent=2))

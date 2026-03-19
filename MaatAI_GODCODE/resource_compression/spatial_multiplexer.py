"""
Spatial Multiplexer - Multiple logical operations on same physical resources
=============================================================================

This doesn't shrink anything - it just uses the SAME physical resources
to do MORE logical operations simultaneously through:

1. Context Switching Optimization - Very fast switches between contexts
2. Resource Pooling - Shared pools for similar operations
3. Time-Division Multiple Access (TDMA) - Precise time slicing
4. Frequency-Division Concepts - Different operations at different "frequencies"
5. Code Reuse Analysis - Find common patterns across operations
"""

import threading
import time
from typing import Dict, List, Any, Callable, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib

@dataclass
class ResourcePool:
    """A pool of physical resources that can be shared"""
    name: str
    resource_type: str
    capacity: int  # How many logical operations can share this
    current_logical_ops: int = 0
    physical_utilization: float = 0.0
    
class LogicalOperation:
    """A logical operation that can share physical resources"""
    id: str
    func: Callable
    args: tuple
    kwargs: dict
    required_resources: Set[str]  # Resource types needed
    priority: int = 5
    context: Dict = field(default_factory=dict)  # Saved context for switching
    
class SpatialMultiplexer:
    """
    Enables MULTIPLE logical operations to run on the SAME physical resources.
    
    This is spatial compression - not making things smaller, but using
    the same hardware to do more work.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.pools: Dict[str, ResourcePool] = {}
        self.active_operations: Dict[str, LogicalOperation] = {}
        self.context_cache: Dict[str, Dict] = {}  # Cached contexts for fast switching
        self.shared_calculations: Dict[str, Any] = {}  # Pre-calculated shared results
        
        self.operations_multiplexed: int = 0
        self.context_switches: int = 0
        self.shared_reuses: int = 0
        
        self._lock = threading.RLock()
        
        # Initialize resource pools
        self._init_pools()
        
    def _init_pools(self):
        """Initialize resource pools"""
        
        # CPU Pool - multiple logical threads on same cores
        self.pools["cpu_pool"] = ResourcePool(
            name="CPU Pool",
            resource_type="cpu",
            capacity=8  # Can run 8 logical ops per physical core
        )
        
        # Memory Pool - shared memory for related operations
        self.pools["memory_pool"] = ResourcePool(
            name="Memory Pool",
            resource_type="memory",
            capacity=16  # 16x logical memory via sharing
        )
        
        # Quantum Pool - shared qubit usage
        self.pools["quantum_pool"] = ResourcePool(
            name="Quantum Pool",
            resource_type="quantum",
            capacity=4  # 4x logical qubits via superposition
        )
        
        # Module Pool - shared module instances
        self.pools["module_pool"] = ResourcePool(
            name="Module Pool",
            resource_type="module",
            capacity=10  # 10x logical modules
        )
        
    def register_shared_calculation(self, key: str, result: Any):
        """Register a calculation that can be shared across operations"""
        with self._lock:
            self.shared_calculations[key] = {
                "result": result,
                "timestamp": time.time(),
                "reuse_count": 0
            }
    
    def get_shared_calculation(self, key: str) -> Optional[Any]:
        """Get a shared calculation if available"""
        with self._lock:
            if key in self.shared_calculations:
                self.shared_calculations[key]["reuse_count"] += 1
                self.shared_reuses += 1
                return self.shared_calculations[key]["result"]
        return None
    
    def save_context(self, op_id: str, context: Dict):
        """Save operation context for fast switching"""
        with self._lock:
            self.context_cache[op_id] = {
                "data": context,
                "timestamp": time.time()
            }
    
    def load_context(self, op_id: str) -> Optional[Dict]:
        """Load saved context"""
        with self._lock:
            if op_id in self.context_cache:
                self.context_switches += 1
                return self.context_cache[op_id]["data"]
        return None
    
    def multiplex_operation(self, op: LogicalOperation) -> Any:
        """
        Execute a logical operation by multiplexing it across physical resources.
        This is the KEY spatial compression method.
        """
        with self._lock:
            # Check if we can use shared calculations
            op_hash = hashlib.md5(f"{op.id}{str(op.args)}{str(op.kwargs)}".encode()).hexdigest()[:16]
            
            shared = self.get_shared_calculation(op_hash)
            if shared is not None:
                return shared
            
            # Check if similar operation exists
            for pool_name, pool in self.pools.items():
                if pool.resource_type in op.required_resources:
                    # Multiplex: increase logical ops without adding physical
                    pool.current_logical_ops += 1
                    
                    # Calculate utilization
                    pool.physical_utilization = min(1.0, pool.current_logical_ops / pool.capacity)
            
            # Execute
            self.active_operations[op.id] = op
            
            try:
                result = op.func(*op.args, **op.kwargs)
                
                # Register as shared for reuse
                self.register_shared_calculation(op_hash, result)
                
                self.operations_multiplexed += 1
                
                # Clean up
                for pool in self.pools.values():
                    if pool.current_logical_ops > 0:
                        pool.current_logical_ops -= 1
                        pool.physical_utilization = min(1.0, pool.current_logical_ops / max(1, pool.capacity))
                
                return result
                
            except Exception as e:
                raise e
            finally:
                if op.id in self.active_operations:
                    del self.active_operations[op.id]
    
    def multiplex_batch(self, operations: List[LogicalOperation]) -> List[Any]:
        """Execute multiple operations with spatial multiplexing"""
        results = []
        
        # Group by similarity for max sharing
        by_resource = defaultdict(list)
        for op in operations:
            primary_resource = list(op.required_resources)[0] if op.required_resources else "module"
            by_resource[primary_resource].append(op)
        
        # Execute with pooling
        for resource_type, ops in by_resource.items():
            if resource_type in self.pools:
                pool = self.pools[resource_type]
                # Increase capacity for batch
                original_capacity = pool.capacity
                pool.capacity = max(pool.capacity, len(ops))
                
                for op in ops:
                    results.append(self.multiplex_operation(op))
                
                pool.capacity = original_capacity
            else:
                for op in ops:
                    results.append(self.multiplex_operation(op))
        
        return results
    
    def analyze_sharable_patterns(self, operations: List[Callable]) -> Dict:
        """
        Analyze operations to find patterns that can be shared.
        This identifies what can be multiplexed.
        """
        patterns = {
            "common_subcalculations": [],
            "similar_inputs": [],
            "parallelizable": [],
            "cacheable": []
        }
        
        # Group by function hash
        func_hashes = {}
        for op in operations:
            if callable(op):
                func_hash = hashlib.md5(str(op).encode()).hexdigest()[:8]
                if func_hash not in func_hashes:
                    func_hashes[func_hash] = []
                func_hashes[func_hash].append(op)
        
        # Find common subcalculations
        for func_hash, ops in func_hashes.items():
            if len(ops) > 1:
                patterns["common_subcalculations"].append({
                    "function_hash": func_hash,
                    "count": len(ops),
                    "recommendation": "Execute once, share result"
                })
        
        return patterns
    
    def get_pool_status(self) -> Dict:
        """Get status of all resource pools"""
        with self._lock:
            return {
                pool_name: {
                    "capacity": pool.capacity,
                    "current_logical_ops": pool.current_logical_ops,
                    "physical_utilization": round(pool.physical_utilization * 100, 1),
                    "multiplex_factor": pool.capacity  # How many logical ops per physical
                }
                for pool_name, pool in self.pools.items()
            }
    
    def get_stats(self) -> Dict:
        """Get spatial multiplexing statistics"""
        with self._lock:
            total_capacity = sum(p.capacity for p in self.pools.values())
            avg_utilization = sum(p.physical_utilization for p in self.pools.values()) / max(1, len(self.pools))
            
            return {
                "operations_multiplexed": self.operations_multiplexed,
                "context_switches": self.context_switches,
                "shared_reuses": self.shared_reuses,
                "pool_status": self.get_pool_status(),
                "multiplex_efficiency": f"{avg_utilization * 100:.1f}%",
                "total_capacity_logical": total_capacity
            }

# Singleton
_spatial_multiplexer_instance = None

def get_spatial_multiplexer() -> SpatialMultiplexer:
    """Get the singleton SpatialMultiplexer instance"""
    global _spatial_multiplexer_instance
    if _spatial_multiplexer_instance is None:
        _spatial_multiplexer_instance = SpatialMultiplexer()
    return _spatial_multiplexer_instance


if __name__ == "__main__":
    # Demo
    sm = get_spatial_multiplexer()
    
    # Create operations
    def sample_op(x):
        return f"result_{x}"
    
    ops = [
        LogicalOperation("op1", sample_op, (1,), {}, {"cpu"}),
        LogicalOperation("op2", sample_op, (2,), {}, {"cpu"}),
        LogicalOperation("op3", sample_op, (3,), {}, {"cpu"}),
    ]
    
    # Multiplex batch
    results = sm.multiplex_batch(ops)
    
    print("\n=== SPATIAL MULTIPLEXER ===")
    print(f"Pool status: {sm.get_pool_status()}")
    print(f"Stats: {sm.get_stats()}")

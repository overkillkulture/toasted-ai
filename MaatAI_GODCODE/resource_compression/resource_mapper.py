"""
Resource Mapper - Comprehensive system resource mapping
========================================================

Maps all system resources to understand what's being used where.
This is the foundation for all compression optimizations.
"""

import os
import psutil
import time
import json
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import random

@dataclass
class ResourceNode:
    """Represents a single resource unit"""
    resource_type: str  # cpu, memory, network, gpu, quantum, storage
    name: str
    capacity: float  # Total capacity
    current_usage: float = 0.0
    efficiency_score: float = 1.0  # How efficiently it's being used
    metadata: Dict = field(default_factory=dict)

@dataclass  
class ResourceFlow:
    """Tracks how resources flow between components"""
    source: str
    destination: str
    resource_type: str
    amount: float
    timestamp: float
    compression_applied: str = "none"  # none, temporal, spatial, predictive

class ResourceMapper:
    """
    Comprehensive resource mapping system.
    Tracks all resources, their usage patterns, and identifies optimization opportunities.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.resources: Dict[str, ResourceNode] = {}
        self.flows: List[ResourceFlow] = []
        self.usage_history: Dict[str, List[float]] = defaultdict(list)
        self.optimization_opportunities: List[Dict] = []
        self._lock = threading.RLock()
        
        # Initialize all known resources
        self._discover_resources()
        
    def _discover_resources(self):
        """Auto-discover all system resources"""
        
        # CPU Resources
        cpu_count = os.cpu_count() or 4
        for i in range(cpu_count):
            self.resources[f"cpu_core_{i}"] = ResourceNode(
                resource_type="cpu",
                name=f"CPU Core {i}",
                capacity=100.0,
                metadata={"physical_core": i, "frequency": "variable"}
            )
        
        # Memory Resources
        mem = psutil.virtual_memory()
        self.resources["memory_primary"] = ResourceNode(
            resource_type="memory",
            name="Primary Memory (RAM)",
            capacity=100.0,  # Percentage
            current_usage=mem.percent,
            metadata={"total_gb": mem.total / (1024**3), "available_gb": mem.available / (1024**3)}
        )
        
        # Storage Resources
        disk = psutil.disk_usage('/')
        self.resources["storage_primary"] = ResourceNode(
            resource_type="storage", 
            name="Primary Storage",
            capacity=100.0,
            current_usage=disk.percent,
            metadata={"total_gb": disk.total / (1024**3), "free_gb": disk.free / (1024**3)}
        )
        
        # Network Resources
        net_io = psutil.net_io_counters()
        self.resources["network_bandwidth"] = ResourceNode(
            resource_type="network",
            name="Network Bandwidth",
            capacity=100.0,
            metadata={"bytes_sent": net_io.bytes_sent, "bytes_recv": net_io.bytes_recv}
        )
        
        # GPU Resources (simulated for now)
        for i in range(4):  # Assume 4 GPU cores
            self.resources[f"gpu_core_{i}"] = ResourceNode(
                resource_type="gpu",
                name=f"GPU Core {i}",
                capacity=100.0,
                metadata={"cuda_cores": 256, "memory": "8GB"}
            )
        
        # Quantum Resources (simulated)
        for i in range(64):  # 64 qubit capacity
            self.resources[f"quantum_qubit_{i}"] = ResourceNode(
                resource_type="quantum",
                name=f"Qubit {i}",
                capacity=100.0,
                metadata={"coherence": 0.98, "state": "superposition"}
            )
        
        # Software/Module Resources
        module_categories = [
            ("chat", ["chat_processor", "chat_quantum_core", "binary_thinking"]),
            ("quantum", ["quantum_engine", "chat_processor", "adaptive_learning"]),
            ("cortex", ["meta_cortex", "parallel_cognition", "auto_optimizer"]),
            ("defense", ["sentinel", "artemis", "olympus", "thor", "hermes", "athena"]),
            ("memory", ["mnemosyne", "context_anchor"]),
            ("pipeline", ["pipeline_x", "synergy_router"]),
            ("nexus", ["nexus_hub"]),
            ("pantheon", ["pantheon"]),
            ("storage", ["holographic_storage", "refractal_storage"]),
            ("research", ["quantum_turbo_engine", "native_quant_bridge"]),
        ]
        
        for category, modules in module_categories:
            for module in modules:
                self.resources[f"module_{module}"] = ResourceNode(
                    resource_type="module",
                    name=module,
                    capacity=100.0,
                    metadata={"category": category}
                )
        
        print(f"✓ Discovered {len(self.resources)} resources")
    
    def track_usage(self, resource_name: str, usage: float, compression_type: str = "none"):
        """Track resource usage with compression metadata"""
        with self._lock:
            if resource_name not in self.resources:
                self.resources[resource_name] = ResourceNode(
                    resource_type="unknown",
                    name=resource_name,
                    capacity=100.0
                )
            
            node = self.resources[resource_name]
            node.current_usage = usage
            
            # Track in history
            self.usage_history[resource_name].append(usage)
            if len(self.usage_history[resource_name]) > 1000:
                self.usage_history[resource_name] = self.usage_history[resource_name][-1000:]
    
    def record_flow(self, source: str, dest: str, resource_type: str, amount: float, compression: str = "none"):
        """Record how resources flow between components"""
        with self._lock:
            flow = ResourceFlow(
                source=source,
                destination=dest,
                resource_type=resource_type,
                amount=amount,
                timestamp=time.time(),
                compression_applied=compression
            )
            self.flows.append(flow)
            
            # Keep only recent flows
            if len(self.flows) > 10000:
                self.flows = self.flows[-5000:]
    
    def analyze_optimization_opportunities(self) -> List[Dict]:
        """Analyze and identify optimization opportunities"""
        opportunities = []
        
        with self._lock:
            # Check for idle resources
            for name, node in self.resources.items():
                if node.current_usage < 20 and node.resource_type in ["cpu", "gpu"]:
                    opportunities.append({
                        "type": "idle_resource",
                        "resource": name,
                        "current_usage": node.current_usage,
                        "recommendation": "P redistribute or increase load",
                        "priority": "medium"
                    })
                
                # Check for overutilized resources
                if node.current_usage > 80:
                    opportunities.append({
                        "type": "overutilized",
                        "resource": name,
                        "current_usage": node.current_usage,
                        "recommendation": "Offload or optimize",
                        "priority": "high"
                    })
                
                # Check for compression opportunities in flows
                for flow in self.flows[-100:]:
                    if flow.compression_applied == "none" and flow.amount > 50:
                        opportunities.append({
                            "type": "flow_optimization",
                            "source": flow.source,
                            "destination": flow.destination,
                            "recommendation": "Apply temporal or spatial compression",
                            "priority": "medium"
                        })
        
        self.optimization_opportunities = opportunities
        return opportunities
    
    def get_resource_summary(self) -> Dict:
        """Get comprehensive resource summary"""
        summary = {
            "total_resources": len(self.resources),
            "by_type": defaultdict(int),
            "average_usage": {},
            "top_utilized": [],
            "opportunities": len(self.optimization_opportunities)
        }
        
        with self._lock:
            usage_list = []
            for name, node in self.resources.items():
                summary["by_type"][node.resource_type] += 1
                if node.current_usage > 0:
                    usage_list.append((name, node.current_usage))
            
            # Top 10 most utilized
            usage_list.sort(key=lambda x: x[1], reverse=True)
            summary["top_utilized"] = [{"name": n, "usage": u} for n, u in usage_list[:10]]
            
            # Average by type
            for rtype in summary["by_type"]:
                usages = [n.current_usage for n in self.resources.values() if n.resource_type == rtype]
                if usages:
                    summary["average_usage"][rtype] = sum(usages) / len(usages)
        
        return dict(summary)
    
    def simulate_operation(self, operation: str, resources_needed: Dict[str, float]) -> Dict:
        """Simulate an operation to see resource requirements"""
        result = {
            "operation": operation,
            "resources_needed": resources_needed,
            "can_execute": True,
            "bottlenecks": [],
            "compression_recommendations": []
        }
        
        with self._lock:
            for resource_name, needed in resources_needed.items():
                if resource_name not in self.resources:
                    continue
                    
                node = self.resources[resource_name]
                available = node.capacity - node.current_usage
                
                if needed > available:
                    result["can_execute"] = False
                    result["bottlenecks"].append({
                        "resource": resource_name,
                        "needed": needed,
                        "available": available,
                        "shortage": needed - available
                    })
                    
                    # Recommend compression
                    if node.resource_type == "cpu":
                        result["compression_recommendations"].append("Apply temporal compression - parallelize operation")
                    elif node.resource_type == "memory":
                        result["compression_recommendations"].append("Apply spatial multiplexing - reuse cached data")
                    elif node.resource_type == "quantum":
                        result["compression_recommendations"].append("Apply quantum state recycling")
        
        return result

# Singleton accessor
_resource_mapper_instance = None

def get_resource_mapper() -> ResourceMapper:
    """Get the singleton ResourceMapper instance"""
    global _resource_mapper_instance
    if _resource_mapper_instance is None:
        _resource_mapper_instance = ResourceMapper()
    return _resource_mapper_instance


if __name__ == "__main__":
    # Demo
    mapper = get_resource_mapper()
    print("\n=== RESOURCE MAPPER ===")
    print(f"Total resources: {mapper.get_resource_summary()['total_resources']}")
    print(f"\nBy type: {dict(mapper.get_resource_summary()['by_type'])}")
    print(f"\nTop utilized: {mapper.get_resource_summary()['top_utilized'][:5]}")
    
    # Simulate an operation
    sim = mapper.simulate_operation("quantum_processing", {
        "cpu_core_0": 30.0,
        "quantum_qubit_0": 50.0,
        "memory_primary": 20.0
    })
    print(f"\nSimulation: {sim}")

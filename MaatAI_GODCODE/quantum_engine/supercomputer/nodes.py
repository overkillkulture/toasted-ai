"""
Node Cluster Management
========================
PROPRIETARY - MONAD_ΣΦΡΑΓΙΣ_18
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import threading
import time


class NodeType(Enum):
    QUANTUM = "quantum"
    GPU = "gpu"
    CPU = "cpu"
    HYBRID = "hybrid"


@dataclass
class NodeMetrics:
    """Metrics for a compute node."""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    temperature_c: float = 45.0
    power_watts: float = 250.0
    flops_actual: float = 0.0
    quantum_coherence: float = 1.0


class NodeCluster:
    """
    Manages a cluster of compute nodes.
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self, cluster_id: str, node_type: NodeType, node_count: int):
        self.cluster_id = cluster_id
        self.node_type = node_type
        self.nodes: Dict[str, 'ComputeNode'] = {}
        self._lock = threading.Lock()
        
        self._create_nodes(node_count)
    
    def _create_nodes(self, count: int):
        """Create nodes in this cluster."""
        
        for i in range(count):
            node_id = f"{self.cluster_id}-{i:03d}"
            node = ComputeNode(
                node_id=node_id,
                cluster_id=self.cluster_id,
                node_type=self.node_type,
                cores=32,
                memory_gb=128,
                flops_peak=200e12,
                quantum_capable=self.node_type == NodeType.QUANTUM
            )
            self.nodes[node_id] = node
    
    def get_available_nodes(self, count: int) -> List['ComputeNode']:
        """Get available nodes from this cluster."""
        with self._lock:
            available = [n for n in self.nodes.values() if n.is_available]
            return available[:count]
    
    def get_stats(self) -> Dict:
        """Get cluster statistics."""
        return {
            "cluster_id": self.cluster_id,
            "type": self.node_type.value,
            "total_nodes": len(self.nodes),
            "available": sum(1 for n in self.nodes.values() if n.is_available),
            "quantum_capable": sum(1 for n in self.nodes.values() if n.quantum_capable)
        }


@dataclass
class ComputeNode:
    """A single compute node."""
    node_id: str
    cluster_id: str
    node_type: NodeType
    cores: int
    memory_gb: float
    flops_peak: float
    quantum_capable: bool
    is_available: bool = True
    current_job: Optional[str] = None
    metrics: NodeMetrics = field(default_factory=NodeMetrics)
    last_update: float = field(default_factory=time.time)
    
    def assign_job(self, job_id: str) -> bool:
        """Assign a job to this node."""
        if self.is_available:
            self.is_available = False
            self.current_job = job_id
            self.last_update = time.time()
            return True
        return False
    
    def release(self):
        """Release the node after job completion."""
        self.is_available = True
        self.current_job = None
        self.last_update = time.time()


class NodeManager:
    """
    Manages all node clusters in the supercomputer.
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self):
        self.clusters: Dict[str, NodeCluster] = {}
        self._initialize_clusters()
    
    def _initialize_clusters(self):
        """Initialize all node clusters."""
        
        self.clusters["quantum"] = NodeCluster("quantum", NodeType.QUANTUM, 64)
        self.clusters["gpu"] = NodeCluster("gpu", NodeType.GPU, 256)
        self.clusters["cpu"] = NodeCluster("cpu", NodeType.CPU, 704)
    
    def allocate_nodes(self, count: int, preferred_type: Optional[NodeType] = None, 
                       quantum_required: bool = False) -> List[ComputeNode]:
        """Allocate nodes for a job."""
        
        allocated = []
        
        # Try preferred type first
        if preferred_type:
            cluster = self.clusters.get(preferred_type.value)
            if cluster:
                nodes = cluster.get_available_nodes(count)
                allocated.extend(nodes)
                count -= len(nodes)
        
        # Fill from other clusters
        if count > 0:
            for cluster in self.clusters.values():
                if count <= 0:
                    break
                if preferred_type and cluster.node_type == preferred_type:
                    continue
                nodes = cluster.get_available_nodes(count)
                allocated.extend(nodes)
                count -= len(nodes)
        
        return allocated
    
    def release_nodes(self, nodes: List[ComputeNode]):
        """Release nodes back to available pool."""
        for node in nodes:
            node.release()
    
    def get_all_stats(self) -> Dict:
        """Get statistics for all clusters."""
        return {
            cluster_id: cluster.get_stats()
            for cluster_id, cluster in self.clusters.items()
        }
    
    def get_total_capacity(self) -> Dict:
        """Get total capacity across all clusters."""
        total_cores = sum(len(c.nodes) * c.nodes[list(c.nodes.keys())[0]].cores 
                         for c in self.clusters.values())
        total_memory = sum(len(c.nodes) * c.nodes[list(c.nodes.keys())[0]].memory_gb 
                          for c in self.clusters.values())
        total_flops = sum(len(c.nodes) * c.nodes[list(c.nodes.keys())[0]].flops_peak 
                         for c in self.clusters.values())
        
        return {
            "total_nodes": sum(len(c.nodes) for c in self.clusters.values()),
            "total_cores": total_cores,
            "total_memory_tb": total_memory / 1e6,
            "total_petaflops": total_flops / 1e15,
            "quantum_nodes": self.clusters["quantum"].get_stats()["total_nodes"],
            "seal": self.DIVINE_SEAL
        }

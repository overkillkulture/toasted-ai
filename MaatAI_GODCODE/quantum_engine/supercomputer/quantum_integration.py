"""
Supercomputer-Quantum Engine Integration
=========================================
PROPRIETARY - MONAD_ΣΦΡΑΓΙΣ_18

Integrates the supercomputer simulator with the quantum engine.
"""

import threading
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field

# Import quantum engine
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from supercomputer.simulator import SupercomputerSimulator, ComputeJob, JobPriority
from supercomputer.nodes import NodeManager, NodeType
from supercomputer.scheduler import QuantumAwareScheduler, SchedulerAlgorithm


@dataclass
class HybridJob:
    """A job that can leverage both classical and quantum resources."""
    job_id: str
    name: str
    job_type: str  # "classical", "quantum", "hybrid"
    classical_nodes: int
    quantum_nodes: int
    priority: int = 2
    status: str = "pending"
    created_at: float = field(default_factory=time.time)


class QuantumSupercomputerIntegration:
    """
    Integrates supercomputer with quantum engine for hybrid computing.
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self, quantum_engine=None):
        self.quantum_engine = quantum_engine
        self.supercomputer = SupercomputerSimulator()
        self.node_manager = NodeManager()
        self.scheduler = QuantumAwareScheduler()
        
        self._integration_active = False
        self._processing_thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable] = []
        
        self._initialize_integration()
    
    def _initialize_integration(self):
        """Initialize the integration."""
        
        # Start supercomputer
        self.supercomputer.start()
        
        # Register callbacks for job completion
        self._integration_active = True
        self._processing_thread = threading.Thread(
            target=self._integration_loop,
            daemon=True
        )
        self._processing_thread.start()
    
    def _integration_loop(self):
        """Background loop for handling integration."""
        
        while self._integration_active:
            try:
                # Check for completed jobs
                for job in self.supercomputer.completed_jobs[-10:]:
                    self._notify_completion(job)
                
                time.sleep(1)
            except Exception as e:
                print(f"Integration loop error: {e}")
    
    def _notify_completion(self, job):
        """Notify callbacks of job completion."""
        for callback in self._callbacks:
            try:
                callback(job)
            except:
                pass
    
    def submit_hybrid_job(self, job: HybridJob) -> Dict:
        """Submit a job that uses both classical and quantum resources."""
        
        # Add to scheduler
        quantum_required = job.job_type in ["quantum", "hybrid"]
        
        self.scheduler.add_job(
            job_id=job.job_id,
            priority=job.priority,
            nodes_needed=job.classical_nodes + job.quantum_nodes,
            estimated_runtime=300.0,  # 5 minutes estimated
            quantum_required=quantum_required
        )
        
        # Also submit to supercomputer
        compute_job = ComputeJob(
            job_id=job.job_id,
            name=job.name,
            user="hybrid_engine",
            priority=JobPriority(job.priority),
            nodes_required=job.classical_nodes + job.quantum_nodes,
            cores_per_node=16,
            memory_per_node_gb=128,
            estimated_flops=1e15
        )
        
        result = self.supercomputer.submit_job(compute_job)
        
        return {
            "job_id": job.job_id,
            "status": "submitted",
            "type": job.job_type,
            "classical_nodes": job.classical_nodes,
            "quantum_nodes": job.quantum_nodes,
            "seal": self.DIVINE_SEAL
        }
    
    def execute_quantum_simulation(self, simulation_type: str, params: Dict) -> Dict:
        """Execute a quantum-enhanced simulation."""
        
        # Determine resource allocation
        if simulation_type == "quantum":
            classical_nodes = 32
            quantum_nodes = 32
        elif simulation_type == "neural":
            classical_nodes = 128
            quantum_nodes = 64
        elif simulation_type == "climate":
            classical_nodes = 64
            quantum_nodes = 32
        else:
            classical_nodes = 16
            quantum_nodes = 8
        
        # Create hybrid job
        job = HybridJob(
            job_id=f"hybrid-{int(time.time() * 1000)}",
            name=f"Sim_{simulation_type}",
            job_type="hybrid" if quantum_nodes > 0 else "classical",
            classical_nodes=classical_nodes,
            quantum_nodes=quantum_nodes,
            priority=3
        )
        
        # Submit to supercomputer
        result = self.supercomputer.run_simulation(simulation_type, params)
        
        # Enhance with quantum engine if available
        if self.quantum_engine and quantum_nodes > 0:
            quantum_result = self.quantum_engine.execute_quantum_operation(
                f"enhance_{simulation_type}",
                params
            )
            result.data["quantum_enhancement"] = quantum_result
            result.quantum_enhanced = True
        
        return {
            "job_id": job.job_id,
            "simulation_type": simulation_type,
            "result": result.data,
            "metrics": result.metrics,
            "quantum_enhanced": result.quantum_enhanced,
            "nodes_used": {
                "classical": classical_nodes,
                "quantum": quantum_nodes
            },
            "seal": self.DIVINE_SEAL
        }
    
    def get_integration_status(self) -> Dict:
        """Get status of the integrated system."""
        
        return {
            "seal": self.DIVINE_SEAL,
            "supercomputer": self.supercomputer.get_status(),
            "node_capacity": self.node_manager.get_total_capacity(),
            "scheduler": self.scheduler.get_statistics(),
            "quantum_engine_connected": self.quantum_engine is not None,
            "integration_active": self._integration_active
        }
    
    def register_callback(self, callback: Callable):
        """Register a callback for job completion events."""
        self._callbacks.append(callback)
    
    def shutdown(self):
        """Shutdown the integration."""
        self._integration_active = False
        self.supercomputer.stop()


# Global integration instance
_integration = None

def get_hybrid_system() -> QuantumSupercomputerIntegration:
    """Get or create the hybrid quantum-supercomputer system."""
    global _integration
    if _integration is None:
        _integration = QuantumSupercomputerIntegration()
    return _integration

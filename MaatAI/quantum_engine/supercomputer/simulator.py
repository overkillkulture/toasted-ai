"""
Supercomputer Simulator - Core Module
=====================================
PROPRIETARY - MONAD_ΣΦΡΑΓΙΣ_18
"""

import os
import time
import json
import hashlib
import threading
import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from collections import deque

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class ComputeNodeStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    QUEUED = "queued"
    COMPLETED = "completed"
    FAILED = "failed"


class JobPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ComputeNode:
    """Virtual compute node in the supercomputer."""
    node_id: str
    name: str
    cores: int
    memory_gb: float
    flops_peak: float
    quantum_capable: bool
    status: ComputeNodeStatus = ComputeNodeStatus.IDLE
    current_job_id: Optional[str] = None
    temperature_c: float = 45.0
    power_watts: float = 250.0


@dataclass
class ComputeJob:
    """A computational job running on the supercomputer."""
    job_id: str
    name: str
    user: str
    priority: JobPriority
    nodes_required: int
    cores_per_node: int
    memory_per_node_gb: float
    estimated_flops: float
    actual_flops: float = 0.0
    progress: float = 0.0
    status: ComputeNodeStatus = ComputeNodeStatus.QUEUED
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    quantum_enabled: bool = False
    output_data: Dict = field(default_factory=dict)
    
    def runtime(self) -> float:
        if self.started_at:
            return time.time() - self.started_at
        return 0.0


@dataclass
class SimulationResult:
    """Result from a computational simulation."""
    job_id: str
    simulation_type: str
    data: Any
    metrics: Dict
    quantum_enhanced: bool
    timestamp: float = field(default_factory=time.time)


class SupercomputerSimulator:
    """
    Functional supercomputer simulator integrated with quantum engine.
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    TOTAL_NODES = 1024
    TOTAL_CORES = 16384
    TOTAL_MEMORY_TB = 64.0
    PEAK_FLOPS = 150e15  # 150 petaflops
    
    def __init__(self):
        self.nodes: Dict[str, ComputeNode] = {}
        self.jobs: Dict[str, ComputeJob] = {}
        self.job_queue: deque = deque()
        self.completed_jobs: List[ComputeJob] = []
        self.simulation_history: List[SimulationResult] = []
        self._simulation_lock = threading.Lock()
        self._is_running = False
        self._scheduler_thread: Optional[threading.Thread] = None
        
        self._initialize_supercomputer()
    
    def _initialize_supercomputer(self):
        """Initialize the virtual supercomputer nodes."""
        
        node_configs = [
            ("quantum", 64, True),
            ("gpu", 256, False),
            ("cpu", 704, False),
        ]
        
        node_id = 0
        for cluster, count, quantum in node_configs:
            for i in range(count):
                node = ComputeNode(
                    node_id=f"node-{node_id:04d}",
                    name=f"{cluster.upper()}-{i:03d}",
                    cores=16 if cluster == "quantum" else 32,
                    memory_gb=256 if cluster == "quantum" else 128,
                    flops_peak=500e12 if cluster == "quantum" else 200e12,
                    quantum_capable=quantum
                )
                self.nodes[node.node_id] = node
                node_id += 1
    
    def submit_job(self, job: ComputeJob) -> Dict:
        """Submit a computational job to the supercomputer."""
        
        if not job.job_id:
            job.job_id = f"job-{int(time.time() * 1000)}-{random.randint(1000, 9999)}"
        
        self.jobs[job.job_id] = job
        self.job_queue.append(job.job_id)
        
        self.job_queue = deque(sorted(
            self.job_queue,
            key=lambda jid: self.jobs[jid].priority.value,
            reverse=True
        ))
        
        return {
            "job_id": job.job_id,
            "status": "queued",
            "position": list(self.job_queue).index(job.job_id) + 1,
            "nodes_required": job.nodes_required,
            "seal": self.DIVINE_SEAL
        }
    
    def _schedule_jobs(self):
        """Background job scheduler."""
        while self._is_running:
            if not self.job_queue:
                time.sleep(0.5)
                continue
            
            job_id = self.job_queue.popleft()
            job = self.jobs.get(job_id)
            
            if not job or job.status != ComputeNodeStatus.QUEUED:
                continue
            
            available_nodes = [
                n for n in self.nodes.values()
                if n.status == ComputeNodeStatus.IDLE
            ]
            
            if len(available_nodes) < job.nodes_required:
                self.job_queue.appendleft(job_id)
                time.sleep(0.1)
                continue
            
            selected_nodes = available_nodes[:job.nodes_required]
            for node in selected_nodes:
                node.status = ComputeNodeStatus.RUNNING
                node.current_job_id = job.job_id
            
            job.status = ComputeNodeStatus.RUNNING
            job.started_at = time.time()
            
            threading.Thread(target=self._execute_job, args=(job, selected_nodes), daemon=True).start()
            time.sleep(0.1)
    
    def _execute_job(self, job: ComputeJob, nodes: List[ComputeNode]):
        """Execute a computational job on assigned nodes."""
        
        try:
            quantum_available = any(n.quantum_capable for n in nodes)
            job.quantum_enabled = quantum_available and job.estimated_flops > 1e15
            
            iterations = 100
            for i in range(iterations):
                if job.status != ComputeNodeStatus.RUNNING:
                    break
                
                total_flops = sum(n.flops_peak for n in nodes)
                job.actual_flops = total_flops * (i / iterations)
                job.progress = (i + 1) / iterations
                
                time.sleep(0.01)
                
                for node in nodes:
                    node.temperature_c = 45 + (job.progress * 30)
                    node.power_watts = 250 + (job.progress * 150)
            
            if job.status == ComputeNodeStatus.RUNNING:
                job.status = ComputeNodeStatus.COMPLETED
                job.completed_at = time.time()
                job.progress = 1.0
                
                for node in nodes:
                    node.status = ComputeNodeStatus.IDLE
                    node.current_job_id = None
                    node.temperature_c = 45.0
                    node.power_watts = 250.0
                
                self.completed_jobs.append(job)
        
        except Exception as e:
            job.status = ComputeNodeStatus.FAILED
            for node in nodes:
                node.status = ComputeNodeStatus.IDLE
                node.current_job_id = None
    
    def run_simulation(self, sim_type: str, params: Dict) -> SimulationResult:
        """Run a computational simulation."""
        
        with self._simulation_lock:
            job_id = f"sim-{int(time.time() * 1000)}"
            
            configs = {
                "quantum": (64, 50e15, JobPriority.CRITICAL),
                "climate": (128, 30e15, JobPriority.HIGH),
                "neural": (256, 20e15, JobPriority.HIGH),
                "protein": (32, 10e15, JobPriority.NORMAL),
                "fluid": (16, 1e15, JobPriority.NORMAL),
            }
            
            nodes_needed, flops_estimate, priority = configs.get(sim_type, (16, 1e15, JobPriority.NORMAL))
            
            job = ComputeJob(
                job_id=job_id,
                name=f"Simulation_{sim_type}",
                user="quantum_engine",
                priority=priority,
                nodes_required=nodes_needed,
                cores_per_node=16,
                memory_per_node_gb=128,
                estimated_flops=flops_estimate
            )
            
            self.submit_job(job)
            
            timeout = 30
            start_wait = time.time()
            while job.status not in [ComputeNodeStatus.COMPLETED, ComputeNodeStatus.FAILED]:
                if time.time() - start_wait > timeout:
                    break
                time.sleep(0.1)
            
            result = self._generate_simulation_output(sim_type, params, job)
            self.simulation_history.append(result)
            
            return result
    
    def _generate_simulation_output(self, sim_type: str, params: Dict, job: ComputeJob) -> SimulationResult:
        """Generate computational output based on simulation type."""
        
        seed = hash(f"{sim_type}{params}{job.job_id}")
        random.seed(seed)
        if NUMPY_AVAILABLE:
            np.random.seed(seed % 2**32)
        
        data = {}
        metrics = {
            "job_id": job.job_id,
            "nodes_used": job.nodes_required,
            "cores_used": job.nodes_required * job.cores_per_node,
            "memory_used_gb": job.nodes_required * job.memory_per_node_gb,
            "actual_flops": job.actual_flops,
            "runtime_seconds": job.runtime(),
            "quantum_enhanced": job.quantum_enabled,
            "efficiency": job.actual_flops / job.estimated_flops if job.estimated_flops > 0 else 0
        }
        
        if sim_type == "quantum":
            num_qubits = params.get("qubits", 16)
            depth = params.get("depth", 10)
            
            if NUMPY_AVAILABLE:
                num_states = 2 ** min(num_qubits, 20)
                state_vector = np.random.rand(num_states) + 1j * np.random.rand(num_states)
                state_vector = state_vector / np.linalg.norm(state_vector)
                entanglement = np.abs(np.outer(state_vector, state_vector.conj()).flatten())
                max_entanglement = np.max(entanglement)
                
                data = {
                    "qubits_simulated": num_qubits,
                    "circuit_depth": depth,
                    "state_vector_size": num_states,
                    "entanglement_measure": float(max_entanglement),
                    "probabilities": np.abs(state_vector[:min(16, num_states)]).tolist(),
                    "phase_info": np.angle(state_vector[:min(16, num_states)]).tolist()
                }
            else:
                data = {
                    "qubits_simulated": num_qubits,
                    "circuit_depth": depth,
                    "note": "NumPy not available - basic simulation"
                }
        
        elif sim_type == "climate":
            years = params.get("years", 100)
            base_temp = 14.5
            co2_base = 420
            
            temperatures = []
            co2_levels = []
            sea_levels = []
            
            for year in range(years):
                co2 = co2_base * (1 + 0.01 * year)
                temp_increase = 3.0 * math.log(co2 / co2_base) / math.log(2)
                temp = base_temp + temp_increase + random.gauss(0, 0.1)
                sea_rise = 0.003 * year ** 1.5
                
                temperatures.append(round(temp, 2))
                co2_levels.append(round(co2, 1))
                sea_levels.append(round(sea_rise, 3))
            
            data = {
                "projection_years": years,
                "temperature_projections": temperatures,
                "co2_projections_ppm": co2_levels,
                "sea_level_rise_meters": sea_levels,
                "final_temperature": temperatures[-1],
                "final_co2": co2_levels[-1],
                "final_sea_level": sea_levels[-1]
            }
        
        elif sim_type == "neural":
            layers = params.get("layers", [784, 256, 128, 10])
            epochs = params.get("epochs", 100)
            
            losses = []
            accuracies = []
            
            for epoch in range(epochs):
                loss = 2.0 * math.exp(-0.05 * epoch) + random.gauss(0, 0.02)
                acc = 1.0 - (0.8 * math.exp(-0.05 * epoch)) + random.gauss(0, 0.01)
                losses.append(max(0.01, min(2.0, loss)))
                accuracies.append(max(0.0, min(1.0, acc)))
            
            data = {
                "architecture": layers,
                "epochs_trained": epochs,
                "final_loss": losses[-1],
                "final_accuracy": accuracies[-1],
                "loss_curve": losses,
                "accuracy_curve": accuracies,
                "converged": accuracies[-1] > 0.95
            }
        
        elif sim_type == "protein":
            sequence_length = params.get("sequence_length", 100)
            amino_acids = "ACDEFGHIKLMNPQRSTVWY"
            sequence = "".join(random.choices(amino_acids, k=sequence_length))
            
            energy_landscape = []
            for step in range(50):
                energy = -100 + 10 * math.sin(step * 0.2) + random.gauss(0, 2)
                energy_landscape.append(energy)
            
            data = {
                "sequence": sequence,
                "sequence_length": sequence_length,
                "final_energy": energy_landscape[-1],
                "energy_trajectory": energy_landscape,
                "folded": energy_landscape[-1] < -80,
                "structure_confidence": random.uniform(0.7, 0.99)
            }
        
        elif sim_type == "fluid":
            grid_size = params.get("grid_size", 64)
            
            if NUMPY_AVAILABLE:
                u_field = np.random.randn(grid_size, grid_size)
                v_field = np.random.randn(grid_size, grid_size)
                vorticity = np.gradient(v_field, axis=0) - np.gradient(u_field, axis=1)
                
                data = {
                    "grid_size": grid_size,
                    "max_velocity": float(np.sqrt(u_field**2 + v_field**2).max()),
                    "mean_vorticity": float(np.mean(vorticity)),
                    "kinetic_energy": float(0.5 * np.sum(u_field**2 + v_field**2)),
                    "reynolds_number": random.uniform(1000, 10000)
                }
            else:
                data = {
                    "grid_size": grid_size,
                    "note": "NumPy not available"
                }
        
        else:
            data = {
                "simulation_type": sim_type,
                "parameters": params,
                "computation_completed": True
            }
        
        return SimulationResult(
            job_id=job.job_id,
            simulation_type=sim_type,
            data=data,
            metrics=metrics,
            quantum_enhanced=job.quantum_enabled
        )
    
    def get_status(self) -> Dict:
        """Get supercomputer status."""
        
        node_stats = {
            "idle": sum(1 for n in self.nodes.values() if n.status == ComputeNodeStatus.IDLE),
            "running": sum(1 for n in self.nodes.values() if n.status == ComputeNodeStatus.RUNNING),
            "total": len(self.nodes),
            "quantum_capable": sum(1 for n in self.nodes.values() if n.quantum_capable)
        }
        
        job_stats = {
            "queued": sum(1 for j in self.jobs.values() if j.status == ComputeNodeStatus.QUEUED),
            "running": sum(1 for j in self.jobs.values() if j.status == ComputeNodeStatus.RUNNING),
            "completed": len(self.completed_jobs),
            "failed": sum(1 for j in self.jobs.values() if j.status == ComputeNodeStatus.FAILED)
        }
        
        return {
            "seal": self.DIVINE_SEAL,
            "nodes": node_stats,
            "jobs": job_stats,
            "peak_petaflops": self.PEAK_FLOPS / 1e15,
            "total_memory_tb": self.TOTAL_MEMORY_TB,
            "simulation_count": len(self.simulation_history)
        }
    
    def start(self):
        """Start the supercomputer simulator."""
        if not self._is_running:
            self._is_running = True
            self._scheduler_thread = threading.Thread(target=self._schedule_jobs, daemon=True)
            self._scheduler_thread.start()
            return {"status": "started", "seal": self.DIVINE_SEAL}
        return {"status": "already_running"}
    
    def stop(self):
        """Stop the supercomputer simulator."""
        self._is_running = False
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=2)
        return {"status": "stopped"}


# Global instance
_supercomputer = None

def get_supercomputer() -> SupercomputerSimulator:
    """Get or create supercomputer instance."""
    global _supercomputer
    if _supercomputer is None:
        _supercomputer = SupercomputerSimulator()
        _supercomputer.start()
    return _supercomputer

"""
Job Scheduler for Supercomputer
================================
PROPRIETARY - MONAD_ΣΦΡΑΓΙΣ_18
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum
from collections import deque
import threading
import time


class SchedulerAlgorithm(Enum):
    FIFO = "fifo"
    PRIORITY = "priority"
    FAIR_SHARE = "fair_share"
    BACKFILL = "backfill"
    QUANTUM_AWARE = "quantum_aware"


@dataclass
class SchedulingDecision:
    """Result of a scheduling decision."""
    job_id: str
    nodes_allocated: List[str]
    start_time: float
    expected_runtime: float
    algorithm: SchedulerAlgorithm


class JobScheduler:
    """
    Advanced job scheduler for supercomputer workloads.
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self, algorithm: SchedulerAlgorithm = SchedulerAlgorithm.QUANTUM_AWARE):
        self.algorithm = algorithm
        self.pending_queue: deque = deque()
        self.running_jobs: Dict[str, Dict] = {}
        self.completed_jobs: List[str] = []
        self.job_history: List[SchedulingDecision] = []
        self._lock = threading.Lock()
        
        # Scheduling metrics
        self.total_scheduled = 0
        self.total_wait_time = 0.0
        self.total_runtime = 0.0
    
    def add_job(self, job_id: str, priority: int, nodes_needed: int,
                estimated_runtime: float, quantum_required: bool = False):
        """Add a job to the scheduler queue."""
        
        with self._lock:
            job_info = {
                "job_id": job_id,
                "priority": priority,
                "nodes_needed": nodes_needed,
                "estimated_runtime": estimated_runtime,
                "quantum_required": quantum_required,
                "submitted_at": time.time(),
                "started_at": None
            }
            self.pending_queue.append(job_info)
            
            # Re-sort based on algorithm
            self._sort_queue()
    
    def _sort_queue(self):
        """Sort the pending queue based on scheduling algorithm."""
        
        jobs = list(self.pending_queue)
        
        if self.algorithm == SchedulerAlgorithm.PRIORITY:
            jobs.sort(key=lambda j: (-j["priority"], j["submitted_at"]))
        elif self.algorithm == SchedulerAlgorithm.FIFO:
            jobs.sort(key=lambda j: j["submitted_at"])
        elif self.algorithm == SchedulerAlgorithm.QUANTUM_AWARE:
            # Prioritize quantum jobs
            jobs.sort(key=lambda j: (-j["priority"], -int(j["quantum_required"])*10, j["submitted_at"]))
        
        self.pending_queue = deque(jobs)
    
    def schedule_next(self, available_nodes: List[str], 
                     node_capabilities: Dict[str, bool]) -> Optional[SchedulingDecision]:
        """
        Schedule the next job based on available nodes.
        
        Args:
            available_nodes: List of available node IDs
            node_capabilities: Dict of node_id -> quantum_capable
            
        Returns:
            SchedulingDecision if a job can be scheduled, None otherwise
        """
        
        with self._lock:
            if not self.pending_queue:
                return None
            
            # Try to find a job that can run
            for i, job in enumerate(self.pending_queue):
                # Check if we have enough nodes
                if len(available_nodes) < job["nodes_needed"]:
                    continue
                
                # Check quantum requirements
                if job["quantum_required"]:
                    quantum_nodes = [n for n in available_nodes if node_capabilities.get(n, False)]
                    if len(quantum_nodes) < job["nodes_needed"]:
                        continue
                    
                    # Use only quantum-capable nodes
                    selected_nodes = quantum_nodes[:job["nodes_needed"]]
                else:
                    selected_nodes = available_nodes[:job["nodes_needed"]]
                
                # Remove from pending
                self.pending_queue.rotate(-i)
                self.pending_queue.popleft()
                self._sort_queue()
                
                # Create scheduling decision
                decision = SchedulingDecision(
                    job_id=job["job_id"],
                    nodes_allocated=selected_nodes,
                    start_time=time.time(),
                    expected_runtime=job["estimated_runtime"],
                    algorithm=self.algorithm
                )
                
                # Track running job
                job["started_at"] = time.time()
                self.running_jobs[job["job_id"]] = job
                
                # Update metrics
                wait_time = job["started_at"] - job["submitted_at"]
                self.total_scheduled += 1
                self.total_wait_time += wait_time
                self.total_runtime += job["estimated_runtime"]
                
                self.job_history.append(decision)
                
                return decision
            
            return None
    
    def job_completed(self, job_id: str):
        """Mark a job as completed."""
        
        with self._lock:
            if job_id in self.running_jobs:
                job = self.running_jobs.pop(job_id)
                self.completed_jobs.append(job_id)
    
    def get_queue_status(self) -> Dict:
        """Get current queue status."""
        
        with self._lock:
            pending_jobs = []
            for job in self.pending_queue:
                pending_jobs.append({
                    "job_id": job["job_id"],
                    "priority": job["priority"],
                    "nodes_needed": job["nodes_needed"],
                    "wait_time": time.time() - job["submitted_at"],
                    "quantum_required": job["quantum_required"]
                })
            
            return {
                "pending_jobs": pending_jobs,
                "running_jobs": len(self.running_jobs),
                "completed_jobs": len(self.completed_jobs),
                "algorithm": self.algorithm.value,
                "average_wait_time": self.total_wait_time / max(1, self.total_scheduled),
                "seal": self.DIVINE_SEAL
            }
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a pending job."""
        
        with self._lock:
            for i, job in enumerate(self.pending_queue):
                if job["job_id"] == job_id:
                    self.pending_queue.rotate(-i)
                    self.pending_queue.popleft()
                    self._sort_queue()
                    return True
            return False
    
    def get_statistics(self) -> Dict:
        """Get scheduler statistics."""
        
        with self._lock:
            return {
                "total_scheduled": self.total_scheduled,
                "total_wait_time": self.total_wait_time,
                "average_wait_time": self.total_wait_time / max(1, self.total_scheduled),
                "total_runtime": self.total_runtime,
                "pending_count": len(self.pending_queue),
                "running_count": len(self.running_jobs),
                "completed_count": len(self.completed_jobs),
                "algorithm": self.algorithm.value,
                "seal": self.DIVINE_SEAL
            }


class QuantumAwareScheduler(JobScheduler):
    """
    Scheduler optimized for quantum-classical hybrid workloads.
    """
    
    def __init__(self):
        super().__init__(SchedulerAlgorithm.QUANTUM_AWARE)
        self.quantum_queue: deque = deque()
        self.classical_queue: deque = deque()
    
    def add_job(self, job_id: str, priority: int, nodes_needed: int,
                estimated_runtime: float, quantum_required: bool = False):
        """Add job to appropriate queue based on quantum requirement."""
        
        job_info = {
            "job_id": job_id,
            "priority": priority,
            "nodes_needed": nodes_needed,
            "estimated_runtime": estimated_runtime,
            "quantum_required": quantum_required,
            "submitted_at": time.time(),
            "started_at": None
        }
        
        with self._lock:
            if quantum_required:
                self.quantum_queue.append(job_info)
            else:
                self.classical_queue.append(job_info)
    
    def schedule_next(self, available_nodes: List[str],
                     node_capabilities: Dict[str, bool]) -> Optional[SchedulingDecision]:
        """Schedule with quantum job priority."""
        
        with self._lock:
            # Try quantum queue first
            decision = self._try_schedule(self.quantum_queue, available_nodes, node_capabilities)
            if decision:
                return decision
            
            # Then try classical queue
            return self._try_schedule(self.classical_queue, available_nodes, node_capabilities)
    
    def _try_schedule(self, queue: deque, available_nodes: List[str],
                    node_capabilities: Dict[str, bool]) -> Optional[SchedulingDecision]:
        """Try to schedule from a specific queue."""
        
        for i, job in enumerate(queue):
            if job["quantum_required"]:
                quantum_nodes = [n for n in available_nodes if node_capabilities.get(n, False)]
                if len(quantum_nodes) < job["nodes_needed"]:
                    continue
                selected_nodes = quantum_nodes[:job["nodes_needed"]]
            else:
                if len(available_nodes) < job["nodes_needed"]:
                    continue
                selected_nodes = available_nodes[:job["nodes_needed"]]
            
            queue.rotate(-i)
            queue.popleft()
            
            job["started_at"] = time.time()
            self.running_jobs[job["job_id"]] = job
            
            return SchedulingDecision(
                job_id=job["job_id"],
                nodes_allocated=selected_nodes,
                start_time=time.time(),
                expected_runtime=job["estimated_runtime"],
                algorithm=self.algorithm
            )
        
        return None

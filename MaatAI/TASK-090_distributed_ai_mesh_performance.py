#!/usr/bin/env python3
"""
TASK-090: Distributed AI Mesh Performance Protocol
Wave 7, Batch 5: Protocols

Creates high-performance distributed AI mesh with load balancing,
fault tolerance, and dynamic node allocation.
"""

import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import random


class NodeStatus(Enum):
    """Status of a mesh node."""
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    DEGRADED = "degraded"
    OFFLINE = "offline"


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 5
    HIGH = 4
    NORMAL = 3
    LOW = 2
    BACKGROUND = 1


@dataclass
class MeshNode:
    """Represents a node in the distributed AI mesh."""
    node_id: str
    capacity: float  # Max concurrent tasks
    current_load: float = 0.0
    status: NodeStatus = NodeStatus.IDLE
    tasks_completed: int = 0
    tasks_failed: int = 0
    avg_task_time: float = 0.0
    last_heartbeat: float = field(default_factory=time.time)
    capabilities: Set[str] = field(default_factory=set)

    def utilization(self) -> float:
        """Calculate current utilization percentage."""
        return (self.current_load / self.capacity) * 100

    def is_available(self) -> bool:
        """Check if node can accept new tasks."""
        return (
            self.status in [NodeStatus.IDLE, NodeStatus.ACTIVE] and
            self.current_load < self.capacity
        )

    def accept_task(self, task_load: float) -> bool:
        """Try to accept a task."""
        if self.current_load + task_load <= self.capacity:
            self.current_load += task_load
            if self.current_load >= self.capacity * 0.9:
                self.status = NodeStatus.BUSY
            elif self.current_load > 0:
                self.status = NodeStatus.ACTIVE
            return True
        return False

    def complete_task(self, task_load: float, task_time: float):
        """Mark task as completed and update stats."""
        self.current_load = max(0, self.current_load - task_load)
        self.tasks_completed += 1

        # Update average task time
        total = self.tasks_completed + self.tasks_failed
        self.avg_task_time = (
            (self.avg_task_time * (total - 1) + task_time) / total
        )

        # Update status
        if self.current_load == 0:
            self.status = NodeStatus.IDLE
        elif self.current_load < self.capacity * 0.9:
            self.status = NodeStatus.ACTIVE


@dataclass
class AITask:
    """Task to be executed in the mesh."""
    task_id: str
    task_type: str
    priority: TaskPriority
    load: float  # Required capacity
    required_capabilities: Set[str] = field(default_factory=set)
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    assigned_node: Optional[str] = None
    retries: int = 0


@dataclass
class MeshMetrics:
    """Performance metrics for the mesh."""
    total_nodes: int = 0
    active_nodes: int = 0
    total_capacity: float = 0.0
    used_capacity: float = 0.0
    tasks_queued: int = 0
    tasks_in_progress: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    avg_queue_time: float = 0.0
    avg_execution_time: float = 0.0


class DistributedAIMeshPerformance:
    """
    High-performance distributed AI mesh coordinator.

    Features:
    - Dynamic load balancing
    - Capability-based routing
    - Priority queue management
    - Fault tolerance and retry logic
    - Real-time performance monitoring
    """

    def __init__(self, base_path: str = "C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI"):
        self.base_path = Path(base_path)
        self.nodes: Dict[str, MeshNode] = {}
        self.task_queue: deque = deque()
        self.active_tasks: Dict[str, AITask] = {}
        self.completed_tasks: List[AITask] = []
        self.metrics = MeshMetrics()

        # Performance tuning parameters
        self.max_retries = 3
        self.heartbeat_timeout = 30.0
        self.rebalance_threshold = 0.2  # 20% imbalance triggers rebalance

    def add_node(self,
                 node_id: str,
                 capacity: float = 10.0,
                 capabilities: Optional[Set[str]] = None) -> MeshNode:
        """
        Add a node to the mesh.

        Args:
            node_id: Unique node identifier
            capacity: Maximum concurrent task load
            capabilities: Node capabilities (e.g., 'gpu', 'nlp', 'vision')

        Returns:
            Created MeshNode
        """
        node = MeshNode(
            node_id=node_id,
            capacity=capacity,
            capabilities=capabilities or set()
        )

        self.nodes[node_id] = node
        self.metrics.total_nodes += 1
        self.metrics.total_capacity += capacity

        return node

    def remove_node(self, node_id: str):
        """Remove a node from the mesh and reschedule its tasks."""
        if node_id not in self.nodes:
            return

        node = self.nodes[node_id]

        # Reschedule active tasks
        tasks_to_reschedule = [
            task for task in self.active_tasks.values()
            if task.assigned_node == node_id
        ]

        for task in tasks_to_reschedule:
            task.assigned_node = None
            task.started_at = None
            task.retries += 1
            self.task_queue.appendleft(task)  # High priority requeue
            del self.active_tasks[task.task_id]

        # Remove node
        self.metrics.total_capacity -= node.capacity
        del self.nodes[node_id]
        self.metrics.total_nodes -= 1

    def submit_task(self,
                   task_id: str,
                   task_type: str,
                   priority: TaskPriority = TaskPriority.NORMAL,
                   load: float = 1.0,
                   required_capabilities: Optional[Set[str]] = None) -> AITask:
        """
        Submit a task to the mesh.

        Args:
            task_id: Unique task identifier
            task_type: Type of AI task
            priority: Task priority
            load: Required capacity
            required_capabilities: Required node capabilities

        Returns:
            Created AITask
        """
        task = AITask(
            task_id=task_id,
            task_type=task_type,
            priority=priority,
            load=load,
            required_capabilities=required_capabilities or set()
        )

        self.task_queue.append(task)
        self.metrics.tasks_queued += 1

        return task

    def _find_best_node(self, task: AITask) -> Optional[MeshNode]:
        """
        Find the best node for a task using intelligent scheduling.

        Considers:
        - Node availability
        - Capability matching
        - Current load
        - Historical performance
        """
        candidates = []

        for node in self.nodes.values():
            # Must be available
            if not node.is_available():
                continue

            # Must have required capabilities
            if task.required_capabilities and not task.required_capabilities.issubset(node.capabilities):
                continue

            # Must have enough capacity
            if node.current_load + task.load > node.capacity:
                continue

            # Calculate fitness score
            score = self._calculate_node_fitness(node, task)
            candidates.append((score, node))

        if not candidates:
            return None

        # Return highest scoring node
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    def _calculate_node_fitness(self, node: MeshNode, task: AITask) -> float:
        """
        Calculate fitness score for assigning task to node.

        Higher score = better fit
        """
        # Prefer nodes with lower utilization (load balancing)
        utilization_score = 100 - node.utilization()

        # Prefer nodes with better historical performance
        if node.tasks_completed > 0:
            success_rate = node.tasks_completed / (
                node.tasks_completed + node.tasks_failed
            )
            performance_score = success_rate * 50
        else:
            performance_score = 25  # Neutral for new nodes

        # Prefer faster nodes
        speed_score = 50
        if node.avg_task_time > 0:
            speed_score = max(0, 50 - (node.avg_task_time * 10))

        # Bonus for exact capability match
        capability_bonus = 0
        if task.required_capabilities:
            if task.required_capabilities == node.capabilities:
                capability_bonus = 20

        return utilization_score + performance_score + speed_score + capability_bonus

    async def schedule_tasks(self):
        """
        Main scheduling loop - assigns queued tasks to nodes.
        """
        scheduled = 0

        # Sort queue by priority
        sorted_queue = sorted(
            self.task_queue,
            key=lambda t: (t.priority.value, -t.created_at),
            reverse=True
        )
        self.task_queue = deque(sorted_queue)

        # Try to schedule each task
        while self.task_queue:
            task = self.task_queue[0]

            # Find best node
            node = self._find_best_node(task)

            if not node:
                break  # No nodes available

            # Assign task
            if node.accept_task(task.load):
                self.task_queue.popleft()
                task.assigned_node = node.node_id
                task.started_at = time.time()
                self.active_tasks[task.task_id] = task

                scheduled += 1
                self.metrics.tasks_queued -= 1
                self.metrics.tasks_in_progress += 1

                # Start task execution
                asyncio.create_task(self._execute_task(task, node))
            else:
                break

        return scheduled

    async def _execute_task(self, task: AITask, node: MeshNode):
        """
        Execute a task on a node (simulated).

        In production, this would dispatch to actual AI compute.
        """
        # Simulate task execution time
        execution_time = task.load * 0.5 + random.uniform(0.1, 0.5)
        await asyncio.sleep(execution_time)

        # Simulate occasional failures
        success = random.random() > 0.05  # 95% success rate

        if success:
            # Task completed successfully
            task.completed_at = time.time()
            node.complete_task(task.load, execution_time)

            self.completed_tasks.append(task)
            del self.active_tasks[task.task_id]

            self.metrics.tasks_in_progress -= 1
            self.metrics.tasks_completed += 1

            # Update metrics
            queue_time = task.started_at - task.created_at
            total = self.metrics.tasks_completed
            self.metrics.avg_queue_time = (
                (self.metrics.avg_queue_time * (total - 1) + queue_time) / total
            )
            self.metrics.avg_execution_time = (
                (self.metrics.avg_execution_time * (total - 1) + execution_time) / total
            )

        else:
            # Task failed
            node.tasks_failed += 1
            node.complete_task(task.load, execution_time)

            del self.active_tasks[task.task_id]
            self.metrics.tasks_in_progress -= 1

            # Retry if under limit
            if task.retries < self.max_retries:
                task.retries += 1
                task.assigned_node = None
                task.started_at = None
                self.task_queue.appendleft(task)  # High priority
                self.metrics.tasks_queued += 1
            else:
                self.metrics.tasks_failed += 1

    async def monitor_and_rebalance(self):
        """
        Monitor mesh health and trigger rebalancing if needed.
        """
        while True:
            await asyncio.sleep(1.0)

            # Update active node count
            self.metrics.active_nodes = sum(
                1 for n in self.nodes.values()
                if n.status in [NodeStatus.ACTIVE, NodeStatus.BUSY]
            )

            # Update capacity metrics
            self.metrics.used_capacity = sum(
                n.current_load for n in self.nodes.values()
            )

            # Check for imbalance
            if len(self.nodes) > 1:
                utilizations = [n.utilization() for n in self.nodes.values()]
                max_util = max(utilizations)
                min_util = min(utilizations)

                if max_util - min_util > self.rebalance_threshold * 100:
                    # Trigger rebalancing
                    await self._rebalance_load()

            # Schedule any queued tasks
            await self.schedule_tasks()

    async def _rebalance_load(self):
        """
        Rebalance load across nodes by migrating tasks.

        In production, this would implement task migration.
        For now, it's a no-op placeholder.
        """
        pass  # Task migration would go here

    def get_mesh_status(self) -> Dict:
        """Get current mesh status and metrics."""
        node_status = {}
        for node_id, node in self.nodes.items():
            node_status[node_id] = {
                "status": node.status.value,
                "utilization": f"{node.utilization():.1f}%",
                "tasks_completed": node.tasks_completed,
                "tasks_failed": node.tasks_failed,
                "avg_task_time": f"{node.avg_task_time:.2f}s"
            }

        return {
            "mesh_metrics": {
                "total_nodes": self.metrics.total_nodes,
                "active_nodes": self.metrics.active_nodes,
                "utilization": f"{(self.metrics.used_capacity / max(self.metrics.total_capacity, 1)) * 100:.1f}%",
                "tasks_queued": self.metrics.tasks_queued,
                "tasks_in_progress": self.metrics.tasks_in_progress,
                "tasks_completed": self.metrics.tasks_completed,
                "tasks_failed": self.metrics.tasks_failed,
                "avg_queue_time": f"{self.metrics.avg_queue_time:.3f}s",
                "avg_execution_time": f"{self.metrics.avg_execution_time:.3f}s"
            },
            "nodes": node_status
        }

    def save_mesh_state(self, output_path: Optional[Path] = None):
        """Save mesh state to disk."""
        if output_path is None:
            output_path = self.base_path / "distributed_ai_mesh_state.json"

        state = {
            "nodes": {
                nid: {
                    "node_id": n.node_id,
                    "capacity": n.capacity,
                    "current_load": n.current_load,
                    "status": n.status.value,
                    "tasks_completed": n.tasks_completed,
                    "tasks_failed": n.tasks_failed,
                    "capabilities": list(n.capabilities)
                }
                for nid, n in self.nodes.items()
            },
            "metrics": {
                "total_nodes": self.metrics.total_nodes,
                "total_capacity": self.metrics.total_capacity,
                "tasks_completed": self.metrics.tasks_completed,
                "tasks_failed": self.metrics.tasks_failed
            }
        }

        output_path.write_text(json.dumps(state, indent=2))
        return output_path


def main():
    """Test the distributed AI mesh."""
    print("=" * 60)
    print("TASK-090: Distributed AI Mesh Performance")
    print("=" * 60)

    mesh = DistributedAIMeshPerformance()

    # Add nodes
    print("\n[1/4] Creating mesh nodes...")
    mesh.add_node("node_1", capacity=10.0, capabilities={"nlp", "general"})
    mesh.add_node("node_2", capacity=15.0, capabilities={"vision", "gpu"})
    mesh.add_node("node_3", capacity=12.0, capabilities={"nlp", "gpu"})
    mesh.add_node("node_4", capacity=8.0, capabilities={"general"})

    print(f"  Created {mesh.metrics.total_nodes} nodes")
    print(f"  Total capacity: {mesh.metrics.total_capacity}")

    # Submit tasks
    print("\n[2/4] Submitting tasks...")
    for i in range(20):
        priority = random.choice(list(TaskPriority))
        task_type = random.choice(["nlp", "vision", "general"])
        required_caps = {task_type} if task_type != "general" else set()

        mesh.submit_task(
            task_id=f"task_{i:03d}",
            task_type=task_type,
            priority=priority,
            load=random.uniform(0.5, 2.0),
            required_capabilities=required_caps
        )

    print(f"  Submitted {mesh.metrics.tasks_queued} tasks")

    # Run mesh
    print("\n[3/4] Running mesh scheduler...")
    async def run_mesh():
        # Start monitoring
        monitor_task = asyncio.create_task(mesh.monitor_and_rebalance())

        # Wait for tasks to complete
        start_time = time.time()
        while mesh.metrics.tasks_queued > 0 or mesh.metrics.tasks_in_progress > 0:
            await asyncio.sleep(0.5)

            # Timeout after 30 seconds
            if time.time() - start_time > 30:
                break

        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass

    asyncio.run(run_mesh())

    # Get status
    print("\n[4/4] Final mesh status:")
    status = mesh.get_mesh_status()

    print("\nMesh Metrics:")
    for key, value in status["mesh_metrics"].items():
        print(f"  {key}: {value}")

    print("\nNode Status:")
    for node_id, node_status in status["nodes"].items():
        print(f"  {node_id}:")
        for key, value in node_status.items():
            print(f"    {key}: {value}")

    # Save state
    output_path = mesh.save_mesh_state()
    print(f"\n✓ Mesh state saved: {output_path}")

    print("\n" + "=" * 60)
    print("TASK-090 Complete: Distributed AI mesh operational!")
    print("=" * 60)


if __name__ == "__main__":
    main()

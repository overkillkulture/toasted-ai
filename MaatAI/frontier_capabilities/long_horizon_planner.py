"""
Long-Horizon Planning System
============================
Week-long autonomous task planning and execution.
Projects indicate week-long autonomy by late 2026.

Key Features:
- Hierarchical task decomposition
- Temporal planning with milestones
- Resource allocation
- Progress tracking
- Adaptive re-planning
- Checkpoint system

Based on patterns from: AgentVerse, CAMEL, ChatDev
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


@dataclass
class Task:
    """Represents a task in the plan."""
    id: str
    name: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    estimated_duration: timedelta = None
    actual_duration: timedelta = None
    dependencies: list[str] = field(default_factory=list)
    subtasks: list['Task'] = field(default_factory=list)
    checkpoints: list[dict] = field(default_factory=list)
    progress: float = 0.0  # 0.0 to 1.0
    result: Any = None
    error: str = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime = None
    completed_at: datetime = None
    
    
@dataclass
class Milestone:
    """Represents a milestone in the plan."""
    id: str
    name: str
    description: str
    tasks: list[str]  # Task IDs
    target_date: datetime
    status: TaskStatus = TaskStatus.PENDING
    completion_criteria: str = ""
    

@dataclass
class Plan:
    """Represents a complete plan."""
    id: str
    name: str
    description: str
    tasks: dict[str, Task] = field(default_factory=dict)
    milestones: dict[str, Milestone] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    target_completion: datetime = None
    status: TaskStatus = TaskStatus.PENDING
    
    def get_task(self, task_id: str) -> Task:
        return self.tasks.get(task_id)
    
    def get_ready_tasks(self) -> list[Task]:
        """Get tasks that are ready to execute (dependencies met)."""
        ready = []
        for task in self.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue
            # Check if all dependencies are completed
            deps_met = all(
                self.tasks.get(dep_id) and self.tasks[dep_id].status == TaskStatus.COMPLETED
                for dep_id in task.dependencies
            )
            if deps_met:
                ready.append(task)
        return ready
    
    def get_progress(self) -> float:
        """Calculate overall plan progress."""
        if not self.tasks:
            return 0.0
        total = sum(t.progress for t in self.tasks.values())
        return total / len(self.tasks)


class TaskDecomposer:
    """
    Breaks down high-level goals into executable tasks.
    """
    
    def decompose(self, goal: str, depth: int = 3) -> list[Task]:
        """
        Decompose a goal into hierarchical tasks.
        
        Args:
            goal: The high-level goal
            depth: How deep to decompose
            
        Returns:
            List of tasks
        """
        tasks = []
        
        # For demo, create synthetic decomposition
        # In production, use LLM to decompose
        
        # Level 1: Major phases
        phases = [
            f"Phase 1: Research & Planning for {goal}",
            f"Phase 2: Execution of {goal}",
            f"Phase 3: Validation & Refinement of {goal}"
        ]
        
        for i, phase in enumerate(phases):
            task_id = f"task_{uuid.uuid4().hex[:8]}"
            task = Task(
                id=task_id,
                name=phase,
                description=f"Major phase {i+1} of {goal}",
                priority=Priority.HIGH if i == 0 else Priority.MEDIUM,
                estimated_duration=timedelta(days=2) if i != 2 else timedelta(days=3)
            )
            tasks.append(task)
            
            # Add subtasks for deeper levels
            if depth > 1:
                for j in range(3):
                    subtask_id = f"subtask_{uuid.uuid4().hex[:8]}"
                    subtask = Task(
                        id=subtask_id,
                        name=f"Subtask {j+1} of {phase}",
                        description=f"Detailed work item {j+1}",
                        priority=Priority.MEDIUM,
                        estimated_duration=timedelta(hours=4),
                        dependencies=[task_id]
                    )
                    tasks.append(subtask)
                    
        return tasks


class LongHorizonPlanner:
    """
    Plans and executes tasks over extended timeframes (days to weeks).
    """
    
    def __init__(self):
        self.plans: dict[str, Plan] = {}
        self.active_plan: str = None
        self.task_executors: dict[str, callable] = {}
        self.checkpoint_interval = timedelta(hours=1)
        self.last_checkpoint = datetime.now()
        
    def create_plan(self, name: str, goal: str, 
                   target_completion: datetime = None) -> Plan:
        """
        Create a new long-horizon plan.
        """
        plan_id = f"plan_{uuid.uuid4().hex[:8]}"
        
        # Decompose goal into tasks
        decomposer = TaskDecomposer()
        tasks = decomposer.decompose(goal, depth=2)
        
        # Create milestones
        milestones = {}
        if len(tasks) >= 3:
            # Create milestone at 33% and 66%
            milestone1 = Milestone(
                id=f"milestone_{uuid.uuid4().hex[:8]}",
                name="Phase 1 Complete",
                description="Research and initial execution finished",
                tasks=[t.id for t in tasks[:len(tasks)//3]],
                target_date=datetime.now() + timedelta(days=3) if not target_completion else target_completion - timedelta(days=4)
            )
            milestone2 = Milestone(
                id=f"milestone_{uuid.uuid4().hex[:8]}",
                name="Phase 2 Complete",
                description="Core execution finished",
                tasks=[t.id for t in tasks[len(tasks)//3:2*len(tasks)//3]],
                target_date=datetime.now() + timedelta(days=6) if not target_completion else target_completion - timedelta(days=1)
            )
            milestones = {milestone1.id: milestone1, milestone2.id: milestone2}
        
        plan = Plan(
            id=plan_id,
            name=name,
            description=goal,
            tasks={t.id: t for t in tasks},
            milestones=milestones,
            target_completion=target_completion
        )
        
        self.plans[plan_id] = plan
        self.active_plan = plan_id
        
        return plan
    
    def register_executor(self, task_type: str, executor: callable):
        """Register an executor function for task types."""
        self.task_executors[task_type] = executor
    
    async def execute_plan(self, plan_id: str = None) -> dict:
        """
        Execute a plan over time.
        
        This is the main loop that runs the long-horizon task.
        """
        if plan_id is None:
            plan_id = self.active_plan
            
        plan = self.plans.get(plan_id)
        if not plan:
            return {"error": "Plan not found"}
        
        plan.status = TaskStatus.IN_PROGRESS
        execution_log = []
        
        max_iterations = 100
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Check for checkpoint
            if datetime.now() - self.last_checkpoint > self.checkpoint_interval:
                await self._save_checkpoint(plan)
                self.last_checkpoint = datetime.now()
            
            # Get ready tasks
            ready_tasks = plan.get_ready_tasks()
            
            if not ready_tasks:
                # Check if we're stuck
                pending = [t for t in plan.tasks.values() if t.status == TaskStatus.PENDING]
                if not pending:
                    # All done!
                    plan.status = TaskStatus.COMPLETED
                    break
                else:
                    # Deadlock - dependencies not met
                    plan.status = TaskStatus.BLOCKED
                    break
            
            # Execute ready tasks
            for task in ready_tasks[:3]:  # Limit parallel execution
                task.status = TaskStatus.IN_PROGRESS
                task.started_at = datetime.now()
                
                # Execute with registered executor or default
                executor = self.task_executors.get("default", self._default_executor)
                
                try:
                    result = await executor(task)
                    task.result = result
                    task.status = TaskStatus.COMPLETED
                    task.progress = 1.0
                    task.completed_at = datetime.now()
                    task.actual_duration = task.completed_at - task.started_at
                    
                    execution_log.append({
                        "task": task.name,
                        "status": "completed",
                        "duration": str(task.actual_duration)
                    })
                    
                except Exception as e:
                    task.error = str(e)
                    task.status = TaskStatus.FAILED
                    execution_log.append({
                        "task": task.name,
                        "status": "failed",
                        "error": str(e)
                    })
            
            # Check milestones
            for milestone in plan.milestones.values():
                milestone_tasks = [plan.tasks.get(tid) for tid in milestone.tasks]
                if all(t and t.status == TaskStatus.COMPLETED for t in milestone_tasks):
                    milestone.status = TaskStatus.COMPLETED
                    execution_log.append({
                        "milestone": milestone.name,
                        "status": "completed"
                    })
            
            # Brief pause
            await asyncio.sleep(0.1)
        
        return {
            "plan_id": plan_id,
            "status": plan.status.value,
            "progress": plan.get_progress(),
            "execution_log": execution_log,
            "iterations": iteration
        }
    
    async def _default_executor(self, task: Task) -> Any:
        """Default task executor."""
        # Simulate work
        await asyncio.sleep(0.1)
        return f"Result of {task.name}"
    
    async def _save_checkpoint(self, plan: Plan):
        """Save checkpoint for recovery."""
        checkpoint_data = {
            "plan_id": plan.id,
            "status": plan.status.value,
            "progress": plan.get_progress(),
            "task_states": {
                tid: {
                    "status": t.status.value,
                    "progress": t.progress,
                    "result": str(t.result)[:100] if t.result else None
                }
                for tid, t in plan.tasks.items()
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # In production, save to persistent storage
        print(f"Checkpoint saved: {checkpoint_data['progress']*100:.1f}% complete")
        
    def get_plan_status(self, plan_id: str = None) -> dict:
        """Get current plan status."""
        if plan_id is None:
            plan_id = self.active_plan
            
        plan = self.plans.get(plan_id)
        if not plan:
            return {"error": "Plan not found"}
            
        return {
            "plan_id": plan.id,
            "name": plan.name,
            "status": plan.status.value,
            "progress": f"{plan.get_progress()*100:.1f}%",
            "tasks": {
                "total": len(plan.tasks),
                "completed": sum(1 for t in plan.tasks.values() if t.status == TaskStatus.COMPLETED),
                "in_progress": sum(1 for t in plan.tasks.values() if t.status == TaskStatus.IN_PROGRESS),
                "pending": sum(1 for t in plan.tasks.values() if t.status == TaskStatus.PENDING)
            },
            "milestones": {
                m.id: {"name": m.name, "status": m.status.value}
                for m in plan.milestones.values()
            },
            "target_completion": plan.target_completion.isoformat() if plan.target_completion else None
        }


# Singleton
_planner_instance = None

def get_long_horizon_planner() -> LongHorizonPlanner:
    """Get the singleton LongHorizonPlanner instance."""
    global _planner_instance
    if _planner_instance is None:
        _planner_instance = LongHorizonPlanner()
    return _planner_instance


# Example usage
async def demo():
    planner = get_long_horizon_planner()
    
    # Create a week-long project
    plan = planner.create_plan(
        name="AI Research Project",
        goal="Research and implement a new machine learning architecture",
        target_completion=datetime.now() + timedelta(days=7)
    )
    
    print(f"Created plan: {plan.name}")
    print(f"Tasks: {len(plan.tasks)}")
    print(f"Milestones: {len(plan.milestones)}")
    
    # Execute
    result = await planner.execute_plan(plan.id)
    
    print(f"\n=== Execution Result ===")
    print(f"Status: {result['status']}")
    print(f"Progress: {result['progress']}")
    print(f"Iterations: {result['iterations']}")
    
    # Get status
    status = planner.get_plan_status(plan.id)
    print(f"\n=== Plan Status ===")
    print(f"Tasks: {status['tasks']}")


if __name__ == "__main__":
    asyncio.run(demo())

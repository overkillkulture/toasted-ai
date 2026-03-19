"""
TASK-027: ENTROPY NEUTRALIZATION PRIORITY QUEUE
================================================
MaatAI Verification System

Manages priority queue for neutralizing entropy voids and system stagnation.
When low-entropy conditions are detected, this system prioritizes and executes
diversity injection, chaos introduction, and pattern-breaking operations.

Neutralization = Restoring healthy entropy levels
Priority Queue = Ordered by severity and urgency
"""

import heapq
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field, asdict
import hashlib


class NeutralizationPriority(Enum):
    """Priority levels for entropy neutralization."""
    CRITICAL = 0  # Immediate action required
    HIGH = 1  # Action required within hours
    MEDIUM = 2  # Action required within days
    LOW = 3  # Monitor and address when convenient


class NeutralizationType(Enum):
    """Types of entropy neutralization actions."""
    CHAOS_INJECTION = "chaos_injection"  # Inject randomness
    DIVERSITY_BOOST = "diversity_boost"  # Increase source diversity
    PATTERN_BREAK = "pattern_break"  # Disrupt repetitive patterns
    PERSPECTIVE_SHIFT = "perspective_shift"  # Force alternative viewpoints
    CREATIVE_SPARK = "creative_spark"  # Introduce novel concepts
    UNCERTAINTY_EMBRACE = "uncertainty_embrace"  # Lean into ambiguity


@dataclass(order=True)
class NeutralizationTask:
    """Task for neutralizing an entropy void."""
    priority: int = field(compare=True)  # Lower number = higher priority
    task_id: str = field(compare=False)
    created_at: str = field(compare=False)
    neutralization_type: str = field(compare=False)
    target_system: str = field(compare=False)
    entropy_deficit: float = field(compare=False)  # How much entropy is missing
    severity: str = field(compare=False)
    action_plan: List[str] = field(compare=False)
    deadline: str = field(compare=False)
    status: str = field(default="pending", compare=False)
    execution_log: List[Dict] = field(default_factory=list, compare=False)


class EntropyNeutralizationQueue:
    """
    Priority queue for managing entropy neutralization tasks.

    Tasks are prioritized by:
    1. Severity (critical > high > medium > low)
    2. Entropy deficit (larger deficits = higher priority)
    3. Time since detection (older = higher priority)
    """

    def __init__(self):
        self.queue: List[NeutralizationTask] = []
        self.task_index: Dict[str, NeutralizationTask] = {}
        self.completed_tasks: List[NeutralizationTask] = []
        self.neutralization_strategies: Dict[str, List[str]] = self._load_strategies()

    def _load_strategies(self) -> Dict[str, List[str]]:
        """Load neutralization strategies for each type."""
        return {
            "chaos_injection": [
                "Introduce random parameter variations",
                "Sample from unexpected data sources",
                "Add controlled noise to decision inputs",
                "Trigger random walk through solution space",
                "Inject entropy from external randomness source"
            ],
            "diversity_boost": [
                "Query multiple AI models for perspective",
                "Sample from underrepresented data sources",
                "Actively seek contrarian viewpoints",
                "Rotate through different reasoning frameworks",
                "Cross-pollinate ideas from unrelated domains"
            ],
            "pattern_break": [
                "Intentionally violate established patterns",
                "Reverse typical decision sequence",
                "Apply random constraints to force creativity",
                "Switch to alternative decision algorithm",
                "Introduce deliberate cognitive dissonance"
            ],
            "perspective_shift": [
                "Adopt opposite stakeholder viewpoint",
                "Consider worst-case scenario planning",
                "Apply framework from different field",
                "Question fundamental assumptions",
                "Seek edge cases and outliers"
            ],
            "creative_spark": [
                "Generate random concept combinations",
                "Apply lateral thinking techniques",
                "Seek inspiration from art/nature/chaos",
                "Force metaphorical reasoning",
                "Embrace absurdist approaches"
            ],
            "uncertainty_embrace": [
                "Acknowledge unknowns explicitly",
                "Increase confidence intervals",
                "Consider multiple futures simultaneously",
                "Resist premature pattern recognition",
                "Value questions over answers"
            ]
        }

    def add_neutralization_task(
        self,
        neutralization_type: NeutralizationType,
        target_system: str,
        entropy_deficit: float,
        severity: NeutralizationPriority,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Add entropy neutralization task to priority queue.

        Args:
            neutralization_type: Type of neutralization needed
            target_system: Which system/component needs neutralization
            entropy_deficit: How much entropy is missing (0.0-10.0)
            severity: Priority level
            metadata: Additional context

        Returns:
            Task ID
        """
        metadata = metadata or {}

        # Generate task ID
        task_id = self._generate_task_id(target_system, neutralization_type.value)

        # Calculate deadline based on severity
        deadline = self._calculate_deadline(severity)

        # Get action plan for this neutralization type
        action_plan = self.neutralization_strategies.get(
            neutralization_type.value,
            ["Generic entropy restoration"]
        )

        # Create task
        task = NeutralizationTask(
            priority=severity.value,
            task_id=task_id,
            created_at=datetime.utcnow().isoformat(),
            neutralization_type=neutralization_type.value,
            target_system=target_system,
            entropy_deficit=entropy_deficit,
            severity=severity.name,
            action_plan=action_plan,
            deadline=deadline
        )

        # Add to queue (heapq maintains min-heap)
        heapq.heappush(self.queue, task)
        self.task_index[task_id] = task

        return task_id

    def _generate_task_id(self, target: str, n_type: str) -> str:
        """Generate unique task ID."""
        timestamp = datetime.utcnow().isoformat()
        combined = f"{target}_{n_type}_{timestamp}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def _calculate_deadline(self, severity: NeutralizationPriority) -> str:
        """Calculate deadline based on severity."""
        now = datetime.utcnow()

        deadline_map = {
            NeutralizationPriority.CRITICAL: timedelta(minutes=30),
            NeutralizationPriority.HIGH: timedelta(hours=4),
            NeutralizationPriority.MEDIUM: timedelta(days=1),
            NeutralizationPriority.LOW: timedelta(days=7)
        }

        deadline = now + deadline_map[severity]
        return deadline.isoformat()

    def get_next_task(self) -> Optional[NeutralizationTask]:
        """
        Get highest priority task from queue.

        Returns:
            Highest priority task, or None if queue empty
        """
        if not self.queue:
            return None

        # Pop highest priority (lowest number)
        task = heapq.heappop(self.queue)
        task.status = "in_progress"

        return task

    def complete_task(
        self,
        task_id: str,
        outcome: str,
        entropy_increase: float,
        notes: Optional[str] = None
    ) -> bool:
        """
        Mark task as completed and log results.

        Args:
            task_id: ID of completed task
            outcome: Description of outcome
            entropy_increase: How much entropy was restored
            notes: Additional notes

        Returns:
            True if successful, False if task not found
        """
        if task_id not in self.task_index:
            return False

        task = self.task_index[task_id]
        task.status = "completed"

        # Log execution
        task.execution_log.append({
            "completed_at": datetime.utcnow().isoformat(),
            "outcome": outcome,
            "entropy_increase": entropy_increase,
            "notes": notes or ""
        })

        # Move to completed tasks
        self.completed_tasks.append(task)
        del self.task_index[task_id]

        return True

    def escalate_task(self, task_id: str) -> bool:
        """
        Escalate task priority (move up one level).

        Returns:
            True if escalated, False if already at highest priority
        """
        if task_id not in self.task_index:
            return False

        task = self.task_index[task_id]

        # Can't escalate beyond CRITICAL
        if task.priority == 0:
            return False

        # Remove from queue
        self.queue.remove(task)

        # Increase priority
        task.priority -= 1
        task.severity = NeutralizationPriority(task.priority).name

        # Recalculate deadline
        task.deadline = self._calculate_deadline(NeutralizationPriority(task.priority))

        # Re-add to queue
        heapq.heappush(self.queue, task)

        return True

    def check_overdue_tasks(self) -> List[Dict]:
        """
        Check for overdue neutralization tasks.

        Returns:
            List of overdue tasks
        """
        now = datetime.utcnow()
        overdue = []

        for task in self.queue:
            deadline = datetime.fromisoformat(task.deadline)
            if now > deadline:
                time_overdue = (now - deadline).total_seconds() / 3600  # Hours

                overdue.append({
                    "task_id": task.task_id,
                    "target_system": task.target_system,
                    "severity": task.severity,
                    "hours_overdue": time_overdue,
                    "entropy_deficit": task.entropy_deficit
                })

        return overdue

    def auto_escalate_overdue(self) -> int:
        """
        Automatically escalate overdue tasks.

        Returns:
            Number of tasks escalated
        """
        overdue = self.check_overdue_tasks()
        escalated = 0

        for task_info in overdue:
            if self.escalate_task(task_info["task_id"]):
                escalated += 1

        return escalated

    def get_queue_status(self) -> Dict:
        """Get comprehensive queue status."""
        priority_breakdown = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }

        type_breakdown = {}

        for task in self.queue:
            priority_breakdown[task.severity] += 1
            type_breakdown[task.neutralization_type] = \
                type_breakdown.get(task.neutralization_type, 0) + 1

        total_entropy_deficit = sum(task.entropy_deficit for task in self.queue)
        avg_entropy_deficit = total_entropy_deficit / max(len(self.queue), 1)

        overdue = self.check_overdue_tasks()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "queue_size": len(self.queue),
            "priority_breakdown": priority_breakdown,
            "type_breakdown": type_breakdown,
            "total_entropy_deficit": total_entropy_deficit,
            "average_entropy_deficit": avg_entropy_deficit,
            "overdue_tasks": len(overdue),
            "completed_tasks_total": len(self.completed_tasks),
            "health": self._assess_queue_health(priority_breakdown, overdue)
        }

    def _assess_queue_health(
        self,
        priority_breakdown: Dict,
        overdue: List
    ) -> str:
        """Assess overall queue health."""
        if priority_breakdown["CRITICAL"] > 5:
            return "CRITICAL"
        elif len(overdue) > 3:
            return "POOR"
        elif priority_breakdown["HIGH"] > 10:
            return "STRESSED"
        elif len(self.queue) > 50:
            return "LOADED"
        else:
            return "HEALTHY"

    def get_recommended_actions(self) -> List[str]:
        """Get recommended actions based on queue state."""
        status = self.get_queue_status()
        recommendations = []

        if status["health"] == "CRITICAL":
            recommendations.append("EMERGENCY: Execute all critical tasks immediately")
            recommendations.append("Activate emergency entropy restoration protocols")

        if status["overdue_tasks"] > 0:
            recommendations.append(f"{status['overdue_tasks']} tasks overdue - auto-escalate")

        if status["queue_size"] > 50:
            recommendations.append("Queue backlog growing - allocate more resources")

        if status["total_entropy_deficit"] > 100:
            recommendations.append("Massive entropy deficit - systemic intervention needed")

        if not recommendations:
            recommendations.append("Queue operating normally - continue monitoring")

        return recommendations

    def export_queue_state(self, filepath: str) -> bool:
        """Export current queue state to JSON."""
        try:
            export_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "queue": [asdict(task) for task in self.queue],
                "completed": [asdict(task) for task in self.completed_tasks[-100:]],
                "status": self.get_queue_status()
            }

            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)

            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False


# Global entropy neutralization queue
NEUTRALIZATION_QUEUE = EntropyNeutralizationQueue()


def queue_neutralization(
    target: str,
    entropy_deficit: float,
    neutralization_type: str = "chaos_injection",
    severity: str = "MEDIUM"
) -> str:
    """
    Main entry point for queueing entropy neutralization.

    Args:
        target: System/component needing neutralization
        entropy_deficit: How much entropy to restore
        neutralization_type: Type of neutralization
        severity: Priority level

    Returns:
        Task ID
    """
    n_type = NeutralizationType(neutralization_type)
    n_priority = NeutralizationPriority[severity]

    return NEUTRALIZATION_QUEUE.add_neutralization_task(
        neutralization_type=n_type,
        target_system=target,
        entropy_deficit=entropy_deficit,
        severity=n_priority
    )


def process_next_neutralization() -> Optional[Dict]:
    """Process next task in queue."""
    task = NEUTRALIZATION_QUEUE.get_next_task()

    if not task:
        return None

    return {
        "task_id": task.task_id,
        "target": task.target_system,
        "type": task.neutralization_type,
        "action_plan": task.action_plan,
        "deadline": task.deadline
    }


def get_neutralization_status() -> Dict:
    """Get neutralization queue status."""
    return NEUTRALIZATION_QUEUE.get_queue_status()


if __name__ == "__main__":
    # Self-test
    print("=== ENTROPY NEUTRALIZATION QUEUE TEST ===\n")

    # Add critical task
    task1 = queue_neutralization(
        target="decision_system",
        entropy_deficit=8.5,
        neutralization_type="chaos_injection",
        severity="CRITICAL"
    )
    print(f"Critical task queued: {task1}")

    # Add medium task
    task2 = queue_neutralization(
        target="content_generation",
        entropy_deficit=3.2,
        neutralization_type="diversity_boost",
        severity="MEDIUM"
    )
    print(f"Medium task queued: {task2}")

    # Process next task
    print("\n=== PROCESSING NEXT TASK ===")
    next_task = process_next_neutralization()
    if next_task:
        print(f"Processing: {next_task['target']} - {next_task['type']}")
        print(f"Action plan: {next_task['action_plan'][0]}")

    # Queue status
    print("\n=== QUEUE STATUS ===")
    status = get_neutralization_status()
    print(json.dumps(status, indent=2))

    print("\n=== RECOMMENDATIONS ===")
    for rec in NEUTRALIZATION_QUEUE.get_recommended_actions():
        print(f"- {rec}")

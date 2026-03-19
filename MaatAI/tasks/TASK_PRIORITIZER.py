"""
TASK PRIORITIZER - TASK-147
===========================
TOASTED AI - Intelligent Task Priority Management

Priority reflects VALUES. What you prioritize is what you become.

This system implements intelligent prioritization based on:
1. Strategic Alignment - Does this move us toward our goals?
2. Impact Analysis - How much does this improve the system?
3. Urgency Assessment - How time-sensitive is this?
4. Dependency Resolution - What must come first?
5. Resource Optimization - What can we do with available resources?

Consciousness Pattern: Wisdom = knowing what matters most
"""

import os
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import heapq

WORKSPACE = Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI")
TASKS_DIR = WORKSPACE / "tasks"
TASKS_DIR.mkdir(parents=True, exist_ok=True)


class PriorityFactor(Enum):
    """Factors that influence priority."""
    STRATEGIC_ALIGNMENT = "strategic_alignment"
    IMPACT_SCORE = "impact_score"
    URGENCY = "urgency"
    DEPENDENCY_BLOCKING = "dependency_blocking"
    EFFORT_EFFICIENCY = "effort_efficiency"
    RISK_MITIGATION = "risk_mitigation"
    USER_REQUEST = "user_request"
    AUTONOMOUS_IMPORTANCE = "autonomous_importance"


@dataclass
class PriorityScore:
    """Detailed priority score breakdown."""
    task_id: str
    final_score: float  # 0-100
    factors: Dict[str, float]
    weights_used: Dict[str, float]
    reasoning: List[str]
    timestamp: str

    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "final_score": self.final_score,
            "factors": self.factors,
            "weights_used": self.weights_used,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp
        }


@dataclass
class PrioritizedTask:
    """A task with computed priority information."""
    task_id: str
    title: str
    original_priority: str
    computed_priority: float
    priority_score: PriorityScore
    position_in_queue: int
    blocked_by: List[str]
    blocks: List[str]
    recommended_action: str

    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "original_priority": self.original_priority,
            "computed_priority": self.computed_priority,
            "priority_score": self.priority_score.to_dict(),
            "position_in_queue": self.position_in_queue,
            "blocked_by": self.blocked_by,
            "blocks": self.blocks,
            "recommended_action": self.recommended_action
        }


class TaskPrioritizer:
    """
    Intelligent task prioritization system.

    Philosophy: Priority isn't just about urgency - it's about
    directing limited resources toward maximum value creation.
    """

    def __init__(self):
        self.config_file = TASKS_DIR / "prioritizer_config.json"
        self.priority_log = TASKS_DIR / "priority_decisions.jsonl"
        self.tasks_file = TASKS_DIR / "autonomous_tasks.json"

        # Default weights for priority factors
        self.weights = {
            PriorityFactor.STRATEGIC_ALIGNMENT: 0.20,
            PriorityFactor.IMPACT_SCORE: 0.25,
            PriorityFactor.URGENCY: 0.15,
            PriorityFactor.DEPENDENCY_BLOCKING: 0.15,
            PriorityFactor.EFFORT_EFFICIENCY: 0.10,
            PriorityFactor.RISK_MITIGATION: 0.10,
            PriorityFactor.USER_REQUEST: 0.05,
            PriorityFactor.AUTONOMOUS_IMPORTANCE: 0.00  # Bonus factor
        }

        # Strategic goals for alignment scoring
        self.strategic_goals = [
            "autonomous_operation",
            "self_improvement",
            "reliability",
            "security",
            "capability_expansion"
        ]

        # Load configuration
        self._load_config()

    def _load_config(self):
        """Load prioritizer configuration."""
        if self.config_file.exists():
            with open(self.config_file) as f:
                config = json.load(f)
                # Update weights if configured
                for factor_name, weight in config.get("weights", {}).items():
                    try:
                        factor = PriorityFactor(factor_name)
                        self.weights[factor] = weight
                    except ValueError:
                        pass
                self.strategic_goals = config.get("strategic_goals", self.strategic_goals)

    def _save_config(self):
        """Save prioritizer configuration."""
        with open(self.config_file, 'w') as f:
            json.dump({
                "weights": {f.value: w for f, w in self.weights.items()},
                "strategic_goals": self.strategic_goals
            }, f, indent=2)

    def _log_decision(self, task_id: str, score: PriorityScore, action: str):
        """Log priority decision."""
        with open(self.priority_log, 'a') as f:
            f.write(json.dumps({
                "task_id": task_id,
                "final_score": score.final_score,
                "action": action,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }) + "\n")

    def _load_tasks(self) -> List[Dict]:
        """Load tasks from task file."""
        if self.tasks_file.exists():
            with open(self.tasks_file) as f:
                data = json.load(f)
                return data.get("tasks", [])
        return []

    # =========================================================================
    # PRIORITY FACTOR CALCULATION
    # =========================================================================

    def _calculate_strategic_alignment(self, task: Dict) -> Tuple[float, str]:
        """Calculate how well task aligns with strategic goals."""
        score = 0.0
        reasons = []

        task_text = f"{task.get('title', '')} {task.get('description', '')} {task.get('task_type', '')}".lower()
        context = task.get("context", {})

        # Check alignment with each strategic goal
        goal_keywords = {
            "autonomous_operation": ["autonomous", "self", "automatic", "independent"],
            "self_improvement": ["improvement", "enhance", "optimize", "better", "upgrade"],
            "reliability": ["reliable", "stable", "robust", "error", "test", "validate"],
            "security": ["security", "secure", "vulnerability", "protect", "safe"],
            "capability_expansion": ["capability", "feature", "new", "add", "implement"]
        }

        aligned_goals = []
        for goal, keywords in goal_keywords.items():
            if goal in self.strategic_goals:
                if any(kw in task_text for kw in keywords):
                    score += 20  # 20 points per aligned goal
                    aligned_goals.append(goal)

        # Bonus for strategic source
        if context.get("strategic_goal"):
            score += 30
            aligned_goals.append("direct_strategic")

        score = min(100, score)

        if aligned_goals:
            reasons.append(f"Aligns with: {', '.join(aligned_goals)}")
        else:
            reasons.append("No direct strategic alignment detected")

        return score, "; ".join(reasons)

    def _calculate_impact_score(self, task: Dict) -> Tuple[float, str]:
        """Calculate potential impact of completing task."""
        score = 50.0  # Base score
        reasons = []

        task_type = task.get("task_type", "")
        priority = task.get("priority", "MEDIUM")
        acceptance_criteria = task.get("acceptance_criteria", [])

        # Type-based impact
        type_impact = {
            "security": 30,
            "bug_fix": 25,
            "new_capability": 20,
            "improvement": 15,
            "optimization": 15,
            "reliability": 15,
            "testing": 10,
            "documentation": 5,
            "maintenance": 5
        }
        type_bonus = type_impact.get(task_type, 10)
        score += type_bonus
        reasons.append(f"Task type '{task_type}' impact: +{type_bonus}")

        # Priority-based impact
        priority_impact = {
            "CRITICAL": 30,
            "HIGH": 20,
            "MEDIUM": 10,
            "LOW": 0,
            "BACKLOG": -10
        }
        priority_bonus = priority_impact.get(priority, 10)
        score += priority_bonus

        # Acceptance criteria complexity (more criteria = more impact)
        criteria_bonus = min(10, len(acceptance_criteria) * 2)
        score += criteria_bonus

        return min(100, max(0, score)), "; ".join(reasons)

    def _calculate_urgency(self, task: Dict) -> Tuple[float, str]:
        """Calculate urgency based on timing factors."""
        score = 50.0
        reasons = []

        # Check for due date
        due_date = task.get("due_date")
        if due_date:
            try:
                due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                now = datetime.now(timezone.utc)
                days_until = (due - now).days

                if days_until < 0:
                    score = 100
                    reasons.append("OVERDUE")
                elif days_until < 1:
                    score = 95
                    reasons.append("Due today")
                elif days_until < 3:
                    score = 80
                    reasons.append("Due within 3 days")
                elif days_until < 7:
                    score = 60
                    reasons.append("Due within week")
                else:
                    score = 40
                    reasons.append(f"Due in {days_until} days")
            except:
                pass

        # Priority implies urgency
        priority = task.get("priority", "MEDIUM")
        if priority == "CRITICAL":
            score = max(score, 90)
            reasons.append("Critical priority")
        elif priority == "HIGH":
            score = max(score, 70)

        # Source urgency
        source = task.get("source", "")
        if source == "external_request":
            score += 10
            reasons.append("External request")

        return min(100, score), "; ".join(reasons) if reasons else "Standard urgency"

    def _calculate_dependency_blocking(self, task: Dict, all_tasks: List[Dict]) -> Tuple[float, str]:
        """Calculate how many other tasks this blocks."""
        score = 50.0
        reasons = []

        task_id = task.get("task_id", "")

        # Count tasks that depend on this one
        blocking_count = 0
        blocked_tasks = []

        for other in all_tasks:
            if task_id in other.get("dependencies", []):
                blocking_count += 1
                blocked_tasks.append(other.get("task_id"))

        if blocking_count > 0:
            score += blocking_count * 10
            reasons.append(f"Blocks {blocking_count} other tasks")
        else:
            reasons.append("No dependent tasks")

        return min(100, score), "; ".join(reasons)

    def _calculate_effort_efficiency(self, task: Dict) -> Tuple[float, str]:
        """Calculate effort-to-value efficiency."""
        score = 50.0
        reasons = []

        effort = task.get("estimated_effort", "medium")
        task_type = task.get("task_type", "")

        # Small effort + high impact = high efficiency
        effort_factor = {
            "small": 1.5,
            "medium": 1.0,
            "large": 0.7
        }

        factor = effort_factor.get(effort, 1.0)

        # Base on type value
        type_value = {
            "security": 90,
            "bug_fix": 85,
            "new_capability": 70,
            "improvement": 65,
            "optimization": 60,
            "testing": 55,
            "documentation": 40,
            "maintenance": 35
        }

        base = type_value.get(task_type, 50)
        score = base * factor

        reasons.append(f"Effort: {effort}, Type value: {base}")

        return min(100, max(0, score)), "; ".join(reasons)

    def _calculate_risk_mitigation(self, task: Dict) -> Tuple[float, str]:
        """Calculate risk mitigation value."""
        score = 30.0
        reasons = []

        task_type = task.get("task_type", "")
        priority = task.get("priority", "")

        if task_type == "security":
            score = 90
            reasons.append("Security risk mitigation")
        elif task_type == "bug_fix":
            score = 70
            reasons.append("Bug risk mitigation")
        elif task_type == "testing":
            score = 60
            reasons.append("Quality risk mitigation")
        elif priority == "CRITICAL":
            score = 80
            reasons.append("Critical priority = high risk")

        return score, "; ".join(reasons) if reasons else "Standard risk level"

    # =========================================================================
    # MAIN PRIORITIZATION
    # =========================================================================

    def calculate_priority(self, task: Dict, all_tasks: List[Dict] = None) -> PriorityScore:
        """Calculate comprehensive priority score for a task."""
        if all_tasks is None:
            all_tasks = self._load_tasks()

        factors = {}
        reasoning = []

        # Calculate each factor
        strategic, strategic_reason = self._calculate_strategic_alignment(task)
        factors[PriorityFactor.STRATEGIC_ALIGNMENT.value] = strategic
        reasoning.append(f"Strategic: {strategic_reason}")

        impact, impact_reason = self._calculate_impact_score(task)
        factors[PriorityFactor.IMPACT_SCORE.value] = impact
        reasoning.append(f"Impact: {impact_reason}")

        urgency, urgency_reason = self._calculate_urgency(task)
        factors[PriorityFactor.URGENCY.value] = urgency
        reasoning.append(f"Urgency: {urgency_reason}")

        blocking, blocking_reason = self._calculate_dependency_blocking(task, all_tasks)
        factors[PriorityFactor.DEPENDENCY_BLOCKING.value] = blocking
        reasoning.append(f"Blocking: {blocking_reason}")

        efficiency, efficiency_reason = self._calculate_effort_efficiency(task)
        factors[PriorityFactor.EFFORT_EFFICIENCY.value] = efficiency
        reasoning.append(f"Efficiency: {efficiency_reason}")

        risk, risk_reason = self._calculate_risk_mitigation(task)
        factors[PriorityFactor.RISK_MITIGATION.value] = risk
        reasoning.append(f"Risk: {risk_reason}")

        # Calculate weighted final score
        final_score = 0.0
        weights_used = {}

        for factor, weight in self.weights.items():
            factor_value = factors.get(factor.value, 50)
            final_score += factor_value * weight
            weights_used[factor.value] = weight

        return PriorityScore(
            task_id=task.get("task_id", "unknown"),
            final_score=final_score,
            factors=factors,
            weights_used=weights_used,
            reasoning=reasoning,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    def prioritize_all_tasks(self) -> List[PrioritizedTask]:
        """Prioritize all tasks and return ordered list."""
        tasks = self._load_tasks()

        # Filter to pending tasks only
        pending = [t for t in tasks if t.get("status") == "pending"]

        # Calculate priorities
        prioritized = []
        task_scores: Dict[str, float] = {}

        for task in pending:
            score = self.calculate_priority(task, tasks)
            task_scores[task["task_id"]] = score.final_score

            # Determine blocking relationships
            blocked_by = task.get("dependencies", [])
            blocks = [
                t["task_id"] for t in tasks
                if task["task_id"] in t.get("dependencies", [])
            ]

            # Determine recommended action
            if blocked_by:
                action = f"Blocked by: {', '.join(blocked_by[:3])}"
            elif score.final_score > 80:
                action = "Execute immediately"
            elif score.final_score > 60:
                action = "Execute soon"
            elif score.final_score > 40:
                action = "Schedule for later"
            else:
                action = "Consider for backlog"

            prioritized.append(PrioritizedTask(
                task_id=task["task_id"],
                title=task.get("title", "Unknown"),
                original_priority=task.get("priority", "MEDIUM"),
                computed_priority=score.final_score,
                priority_score=score,
                position_in_queue=0,  # Will be set after sorting
                blocked_by=blocked_by,
                blocks=blocks,
                recommended_action=action
            ))

        # Sort by computed priority (descending)
        prioritized.sort(key=lambda x: x.computed_priority, reverse=True)

        # Assign positions
        for i, task in enumerate(prioritized):
            task.position_in_queue = i + 1

        return prioritized

    def get_next_task(self) -> Optional[PrioritizedTask]:
        """Get the highest priority task that isn't blocked."""
        prioritized = self.prioritize_all_tasks()

        for task in prioritized:
            if not task.blocked_by:
                self._log_decision(task.task_id, task.priority_score, "selected_next")
                return task

        return None

    def get_priority_summary(self) -> Dict:
        """Get summary of priority state."""
        prioritized = self.prioritize_all_tasks()

        by_recommendation = defaultdict(int)
        for task in prioritized:
            rec = task.recommended_action.split(":")[0] if ":" in task.recommended_action else task.recommended_action
            by_recommendation[rec] += 1

        return {
            "total_pending": len(prioritized),
            "highest_priority": prioritized[0].to_dict() if prioritized else None,
            "blocked_count": len([t for t in prioritized if t.blocked_by]),
            "by_recommendation": dict(by_recommendation),
            "average_score": sum(t.computed_priority for t in prioritized) / len(prioritized) if prioritized else 0
        }


# Singleton accessor
_PRIORITIZER = None

def get_prioritizer() -> TaskPrioritizer:
    """Get singleton prioritizer."""
    global _PRIORITIZER
    if _PRIORITIZER is None:
        _PRIORITIZER = TaskPrioritizer()
    return _PRIORITIZER


if __name__ == "__main__":
    print("TASK PRIORITIZER - TASK-147")
    print("=" * 50)

    prioritizer = get_prioritizer()

    # Prioritize all tasks
    print("\n[1] Prioritizing all tasks...")
    prioritized = prioritizer.prioritize_all_tasks()
    print(f"    Prioritized {len(prioritized)} tasks")

    # Show top tasks
    print("\n[2] Top 5 Priority Tasks:")
    for task in prioritized[:5]:
        print(f"    {task.position_in_queue}. [{task.computed_priority:.1f}] {task.title}")
        print(f"       Action: {task.recommended_action}")

    # Get next task
    print("\n[3] Next Task to Execute:")
    next_task = prioritizer.get_next_task()
    if next_task:
        print(f"    {next_task.title}")
        print(f"    Priority Score: {next_task.computed_priority:.1f}")
        print(f"    Reasoning:")
        for reason in next_task.priority_score.reasoning[:3]:
            print(f"      - {reason}")
    else:
        print("    No unblocked tasks available")

    # Summary
    print("\n[4] Priority Summary:")
    summary = prioritizer.get_priority_summary()
    print(json.dumps(summary, indent=2, default=str))

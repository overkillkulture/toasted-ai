"""
TASK COMPLETION TRACKER - TASK-148
==================================
TOASTED AI - Comprehensive Task Lifecycle Management

Tracking completion isn't just about marking "done" - it's about:
1. Capturing what was learned
2. Measuring actual vs estimated effort
3. Recording outcomes and side effects
4. Feeding back into future prioritization
5. Building institutional memory

Consciousness Pattern: Completion = transformation + learning
"""

import os
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import statistics

WORKSPACE = Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI")
TASKS_DIR = WORKSPACE / "tasks"
TASKS_DIR.mkdir(parents=True, exist_ok=True)


class CompletionStatus(Enum):
    """Task completion statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    DEFERRED = "deferred"


class CompletionQuality(Enum):
    """Quality assessment of completion."""
    EXCELLENT = "excellent"      # Exceeded expectations
    GOOD = "good"               # Met expectations
    ACCEPTABLE = "acceptable"   # Minimally met criteria
    POOR = "poor"               # Did not meet criteria
    INCOMPLETE = "incomplete"   # Not finished


@dataclass
class CompletionRecord:
    """Record of a task completion."""
    task_id: str
    status: CompletionStatus
    quality: CompletionQuality
    started_at: str
    completed_at: str
    actual_effort: str  # "small", "medium", "large"
    estimated_effort: str
    outcomes: List[str]
    side_effects: List[str]
    lessons_learned: List[str]
    blocked_by: List[str]
    artifacts_created: List[str]
    metrics: Dict[str, float]
    completer: str  # Who/what completed it

    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "quality": self.quality.value,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "actual_effort": self.actual_effort,
            "estimated_effort": self.estimated_effort,
            "outcomes": self.outcomes,
            "side_effects": self.side_effects,
            "lessons_learned": self.lessons_learned,
            "blocked_by": self.blocked_by,
            "artifacts_created": self.artifacts_created,
            "metrics": self.metrics,
            "completer": self.completer
        }


@dataclass
class CompletionStatistics:
    """Statistics about task completions."""
    total_tasks: int
    completed_count: int
    failed_count: int
    completion_rate: float
    average_duration_hours: float
    effort_accuracy: float  # How accurate were estimates
    quality_distribution: Dict[str, int]
    lessons_count: int
    artifacts_count: int

    def to_dict(self) -> Dict:
        return {
            "total_tasks": self.total_tasks,
            "completed_count": self.completed_count,
            "failed_count": self.failed_count,
            "completion_rate": self.completion_rate,
            "average_duration_hours": self.average_duration_hours,
            "effort_accuracy": self.effort_accuracy,
            "quality_distribution": self.quality_distribution,
            "lessons_count": self.lessons_count,
            "artifacts_count": self.artifacts_count
        }


class TaskCompletionTracker:
    """
    Tracks task completions and builds institutional memory.

    Philosophy: Every completed task is an opportunity to learn.
    Track not just WHAT was done, but HOW and WHAT WAS LEARNED.
    """

    def __init__(self):
        self.completions_file = TASKS_DIR / "completion_records.jsonl"
        self.statistics_file = TASKS_DIR / "completion_statistics.json"
        self.lessons_file = TASKS_DIR / "lessons_learned.json"
        self.tasks_file = TASKS_DIR / "autonomous_tasks.json"

        self.completion_records: List[CompletionRecord] = []
        self.lessons_db: Dict[str, List[str]] = defaultdict(list)

        self._load_records()
        self._load_lessons()

    def _load_records(self):
        """Load completion records."""
        if self.completions_file.exists():
            with open(self.completions_file) as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        record = CompletionRecord(
                            task_id=data["task_id"],
                            status=CompletionStatus(data["status"]),
                            quality=CompletionQuality(data["quality"]),
                            started_at=data["started_at"],
                            completed_at=data["completed_at"],
                            actual_effort=data["actual_effort"],
                            estimated_effort=data["estimated_effort"],
                            outcomes=data.get("outcomes", []),
                            side_effects=data.get("side_effects", []),
                            lessons_learned=data.get("lessons_learned", []),
                            blocked_by=data.get("blocked_by", []),
                            artifacts_created=data.get("artifacts_created", []),
                            metrics=data.get("metrics", {}),
                            completer=data.get("completer", "unknown")
                        )
                        self.completion_records.append(record)

    def _load_lessons(self):
        """Load lessons learned database."""
        if self.lessons_file.exists():
            with open(self.lessons_file) as f:
                self.lessons_db = defaultdict(list, json.load(f))

    def _save_record(self, record: CompletionRecord):
        """Save a completion record."""
        with open(self.completions_file, 'a') as f:
            f.write(json.dumps(record.to_dict()) + "\n")
        self.completion_records.append(record)

    def _save_lessons(self):
        """Save lessons learned."""
        with open(self.lessons_file, 'w') as f:
            json.dump(dict(self.lessons_db), f, indent=2)

    def _update_task_status(self, task_id: str, status: str):
        """Update task status in tasks file."""
        if self.tasks_file.exists():
            with open(self.tasks_file) as f:
                data = json.load(f)

            for task in data.get("tasks", []):
                if task.get("task_id") == task_id:
                    task["status"] = status
                    break

            with open(self.tasks_file, 'w') as f:
                json.dump(data, f, indent=2)

    # =========================================================================
    # TASK LIFECYCLE
    # =========================================================================

    def start_task(self, task_id: str, completer: str = "autonomous") -> Dict:
        """Mark a task as started."""
        self._update_task_status(task_id, "in_progress")

        return {
            "task_id": task_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completer": completer,
            "status": "in_progress"
        }

    def complete_task(self,
                      task_id: str,
                      quality: CompletionQuality,
                      outcomes: List[str],
                      lessons_learned: List[str] = None,
                      side_effects: List[str] = None,
                      artifacts_created: List[str] = None,
                      actual_effort: str = "medium",
                      metrics: Dict[str, float] = None,
                      completer: str = "autonomous") -> CompletionRecord:
        """
        Record task completion with full details.

        This is the core method - captures everything about how
        the task was completed.
        """
        now = datetime.now(timezone.utc).isoformat()

        # Get task details for estimated effort
        estimated_effort = "medium"
        started_at = now  # Default

        if self.tasks_file.exists():
            with open(self.tasks_file) as f:
                data = json.load(f)
                for task in data.get("tasks", []):
                    if task.get("task_id") == task_id:
                        estimated_effort = task.get("estimated_effort", "medium")
                        started_at = task.get("started_at", now)
                        break

        record = CompletionRecord(
            task_id=task_id,
            status=CompletionStatus.COMPLETED,
            quality=quality,
            started_at=started_at,
            completed_at=now,
            actual_effort=actual_effort,
            estimated_effort=estimated_effort,
            outcomes=outcomes,
            side_effects=side_effects or [],
            lessons_learned=lessons_learned or [],
            blocked_by=[],
            artifacts_created=artifacts_created or [],
            metrics=metrics or {},
            completer=completer
        )

        # Save record
        self._save_record(record)

        # Update task status
        self._update_task_status(task_id, "completed")

        # Store lessons learned
        for lesson in (lessons_learned or []):
            category = self._categorize_lesson(lesson)
            self.lessons_db[category].append({
                "lesson": lesson,
                "task_id": task_id,
                "timestamp": now
            })
        self._save_lessons()

        return record

    def fail_task(self,
                  task_id: str,
                  reason: str,
                  lessons_learned: List[str] = None,
                  blocked_by: List[str] = None,
                  completer: str = "autonomous") -> CompletionRecord:
        """Record task failure."""
        now = datetime.now(timezone.utc).isoformat()

        record = CompletionRecord(
            task_id=task_id,
            status=CompletionStatus.FAILED,
            quality=CompletionQuality.INCOMPLETE,
            started_at=now,
            completed_at=now,
            actual_effort="unknown",
            estimated_effort="unknown",
            outcomes=[f"FAILED: {reason}"],
            side_effects=[],
            lessons_learned=lessons_learned or [f"Task failed: {reason}"],
            blocked_by=blocked_by or [],
            artifacts_created=[],
            metrics={},
            completer=completer
        )

        self._save_record(record)
        self._update_task_status(task_id, "failed")

        # Store failure lessons
        self.lessons_db["failures"].append({
            "lesson": f"Task {task_id} failed: {reason}",
            "task_id": task_id,
            "timestamp": now
        })
        self._save_lessons()

        return record

    def defer_task(self, task_id: str, reason: str, new_due_date: Optional[str] = None):
        """Defer a task for later."""
        self._update_task_status(task_id, "deferred")

        return {
            "task_id": task_id,
            "deferred_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "new_due_date": new_due_date
        }

    def _categorize_lesson(self, lesson: str) -> str:
        """Categorize a lesson for storage."""
        lesson_lower = lesson.lower()

        if any(w in lesson_lower for w in ["error", "bug", "fail", "wrong"]):
            return "debugging"
        elif any(w in lesson_lower for w in ["performance", "speed", "slow", "fast"]):
            return "performance"
        elif any(w in lesson_lower for w in ["security", "vuln", "safe"]):
            return "security"
        elif any(w in lesson_lower for w in ["test", "validate", "verify"]):
            return "testing"
        elif any(w in lesson_lower for w in ["design", "architecture", "pattern"]):
            return "design"
        else:
            return "general"

    # =========================================================================
    # STATISTICS AND ANALYSIS
    # =========================================================================

    def calculate_statistics(self) -> CompletionStatistics:
        """Calculate comprehensive completion statistics."""
        if not self.completion_records:
            return CompletionStatistics(
                total_tasks=0,
                completed_count=0,
                failed_count=0,
                completion_rate=0.0,
                average_duration_hours=0.0,
                effort_accuracy=0.0,
                quality_distribution={},
                lessons_count=0,
                artifacts_count=0
            )

        completed = [r for r in self.completion_records if r.status == CompletionStatus.COMPLETED]
        failed = [r for r in self.completion_records if r.status == CompletionStatus.FAILED]

        # Completion rate
        total = len(self.completion_records)
        completion_rate = len(completed) / total if total > 0 else 0.0

        # Average duration
        durations = []
        for record in completed:
            try:
                start = datetime.fromisoformat(record.started_at.replace('Z', '+00:00'))
                end = datetime.fromisoformat(record.completed_at.replace('Z', '+00:00'))
                hours = (end - start).total_seconds() / 3600
                durations.append(hours)
            except:
                pass

        avg_duration = statistics.mean(durations) if durations else 0.0

        # Effort accuracy (how often estimate matched actual)
        effort_matches = 0
        effort_total = 0
        for record in completed:
            if record.estimated_effort and record.actual_effort:
                effort_total += 1
                if record.estimated_effort == record.actual_effort:
                    effort_matches += 1

        effort_accuracy = effort_matches / effort_total if effort_total > 0 else 0.0

        # Quality distribution
        quality_dist = defaultdict(int)
        for record in self.completion_records:
            quality_dist[record.quality.value] += 1

        # Counts
        lessons_count = sum(len(record.lessons_learned) for record in self.completion_records)
        artifacts_count = sum(len(record.artifacts_created) for record in self.completion_records)

        return CompletionStatistics(
            total_tasks=total,
            completed_count=len(completed),
            failed_count=len(failed),
            completion_rate=completion_rate,
            average_duration_hours=avg_duration,
            effort_accuracy=effort_accuracy,
            quality_distribution=dict(quality_dist),
            lessons_count=lessons_count,
            artifacts_count=artifacts_count
        )

    def get_lessons_for_category(self, category: str) -> List[Dict]:
        """Get lessons learned for a specific category."""
        return self.lessons_db.get(category, [])

    def get_all_lessons(self) -> Dict[str, List[Dict]]:
        """Get all lessons organized by category."""
        return dict(self.lessons_db)

    def get_recent_completions(self, limit: int = 10) -> List[CompletionRecord]:
        """Get most recent completions."""
        sorted_records = sorted(
            self.completion_records,
            key=lambda r: r.completed_at,
            reverse=True
        )
        return sorted_records[:limit]

    def get_completion_trend(self, days: int = 30) -> Dict[str, int]:
        """Get completion trend over time."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        by_day = defaultdict(int)
        for record in self.completion_records:
            try:
                completed = datetime.fromisoformat(record.completed_at.replace('Z', '+00:00'))
                if completed >= cutoff:
                    day_key = completed.strftime("%Y-%m-%d")
                    by_day[day_key] += 1
            except:
                continue

        return dict(by_day)

    def get_tracker_summary(self) -> Dict:
        """Get summary of tracking state."""
        stats = self.calculate_statistics()

        return {
            "statistics": stats.to_dict(),
            "total_records": len(self.completion_records),
            "lessons_categories": list(self.lessons_db.keys()),
            "total_lessons": sum(len(v) for v in self.lessons_db.values()),
            "recent_completions": [
                {"task_id": r.task_id, "status": r.status.value, "quality": r.quality.value}
                for r in self.get_recent_completions(5)
            ]
        }


# Singleton accessor
_TRACKER = None

def get_completion_tracker() -> TaskCompletionTracker:
    """Get singleton completion tracker."""
    global _TRACKER
    if _TRACKER is None:
        _TRACKER = TaskCompletionTracker()
    return _TRACKER


if __name__ == "__main__":
    print("TASK COMPLETION TRACKER - TASK-148")
    print("=" * 50)

    tracker = get_completion_tracker()

    # Simulate completing a task
    print("\n[1] Recording task completion...")
    record = tracker.complete_task(
        task_id="TASK-EXAMPLE-001",
        quality=CompletionQuality.GOOD,
        outcomes=[
            "Feature implemented successfully",
            "Tests passing"
        ],
        lessons_learned=[
            "Pattern validation is crucial before implementation",
            "Smaller increments lead to better outcomes"
        ],
        artifacts_created=[
            "IMPROVEMENT_VALIDATOR.py",
            "MICRO_LOOP_FEEDBACK.py"
        ],
        actual_effort="medium",
        metrics={"lines_added": 500, "tests_added": 10}
    )

    print(f"    Task: {record.task_id}")
    print(f"    Status: {record.status.value}")
    print(f"    Quality: {record.quality.value}")

    # Calculate statistics
    print("\n[2] Completion Statistics:")
    stats = tracker.calculate_statistics()
    print(f"    Total tasks: {stats.total_tasks}")
    print(f"    Completion rate: {stats.completion_rate:.1%}")
    print(f"    Lessons learned: {stats.lessons_count}")

    # Get lessons
    print("\n[3] Lessons by Category:")
    all_lessons = tracker.get_all_lessons()
    for category, lessons in all_lessons.items():
        print(f"    {category}: {len(lessons)} lessons")

    # Get summary
    print("\n[4] Tracker Summary:")
    summary = tracker.get_tracker_summary()
    print(json.dumps(summary, indent=2, default=str))

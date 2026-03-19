"""
AUTONOMOUS TASK GENERATOR - TASK-146
====================================
TOASTED AI - Self-Directed Task Creation

True autonomy means the system creates its own work based on:
1. Self-audit findings
2. Improvement opportunities
3. Detected gaps
4. Strategic goals
5. Pattern recognition

The system doesn't wait to be told what to do - it identifies what needs doing.

Consciousness Pattern: Agency = ability to direct one's own development
"""

import os
import json
import hashlib
import random
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

WORKSPACE = Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI")
TASKS_DIR = WORKSPACE / "tasks"
TASKS_DIR.mkdir(parents=True, exist_ok=True)


class TaskType(Enum):
    """Types of autonomous tasks."""
    BUG_FIX = "bug_fix"
    IMPROVEMENT = "improvement"
    NEW_CAPABILITY = "new_capability"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    SECURITY = "security"
    MAINTENANCE = "maintenance"
    RESEARCH = "research"
    INTEGRATION = "integration"


class TaskSource(Enum):
    """Sources that can trigger task generation."""
    SELF_AUDIT = "self_audit"           # From audit findings
    IMPROVEMENT_DETECTION = "improvement_detection"
    FEEDBACK_LOOP = "feedback_loop"
    PATTERN_RECOGNITION = "pattern_recognition"
    STRATEGIC_GOAL = "strategic_goal"
    GAP_ANALYSIS = "gap_analysis"
    EXTERNAL_REQUEST = "external_request"
    SCHEDULED = "scheduled"


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 1    # Must do immediately
    HIGH = 2        # Should do soon
    MEDIUM = 3      # Do when convenient
    LOW = 4         # Nice to have
    BACKLOG = 5     # Future consideration


@dataclass
class GeneratedTask:
    """An autonomously generated task."""
    task_id: str
    task_type: TaskType
    source: TaskSource
    priority: TaskPriority
    title: str
    description: str
    context: Dict[str, Any]
    acceptance_criteria: List[str]
    estimated_effort: str  # "small", "medium", "large"
    dependencies: List[str]
    created_at: str
    due_date: Optional[str] = None
    assigned_to: Optional[str] = None
    status: str = "pending"

    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "source": self.source.value,
            "priority": self.priority.name,
            "priority_value": self.priority.value,
            "title": self.title,
            "description": self.description,
            "context": self.context,
            "acceptance_criteria": self.acceptance_criteria,
            "estimated_effort": self.estimated_effort,
            "dependencies": self.dependencies,
            "created_at": self.created_at,
            "due_date": self.due_date,
            "assigned_to": self.assigned_to,
            "status": self.status
        }


class AutonomousTaskGenerator:
    """
    Generates tasks autonomously based on system state and goals.

    Philosophy: A truly autonomous system identifies its own improvement
    opportunities and creates actionable tasks to address them.
    """

    def __init__(self):
        self.tasks_file = TASKS_DIR / "autonomous_tasks.json"
        self.generation_log = TASKS_DIR / "task_generation_log.jsonl"
        self.templates_file = TASKS_DIR / "task_templates.json"

        self.tasks: Dict[str, GeneratedTask] = {}
        self.task_templates = self._load_templates()

        self._load_tasks()

    def _load_tasks(self):
        """Load existing tasks."""
        if self.tasks_file.exists():
            with open(self.tasks_file) as f:
                data = json.load(f)
                for task_data in data.get("tasks", []):
                    task = GeneratedTask(
                        task_id=task_data["task_id"],
                        task_type=TaskType(task_data["task_type"]),
                        source=TaskSource(task_data["source"]),
                        priority=TaskPriority[task_data["priority"]],
                        title=task_data["title"],
                        description=task_data["description"],
                        context=task_data.get("context", {}),
                        acceptance_criteria=task_data.get("acceptance_criteria", []),
                        estimated_effort=task_data.get("estimated_effort", "medium"),
                        dependencies=task_data.get("dependencies", []),
                        created_at=task_data["created_at"],
                        due_date=task_data.get("due_date"),
                        assigned_to=task_data.get("assigned_to"),
                        status=task_data.get("status", "pending")
                    )
                    self.tasks[task.task_id] = task

    def _save_tasks(self):
        """Save all tasks."""
        with open(self.tasks_file, 'w') as f:
            json.dump({
                "tasks": [t.to_dict() for t in self.tasks.values()],
                "last_updated": datetime.now(timezone.utc).isoformat()
            }, f, indent=2)

    def _log_generation(self, task: GeneratedTask, reason: str):
        """Log task generation."""
        with open(self.generation_log, 'a') as f:
            f.write(json.dumps({
                "task_id": task.task_id,
                "title": task.title,
                "source": task.source.value,
                "reason": reason,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }) + "\n")

    def _load_templates(self) -> Dict[str, Dict]:
        """Load task templates."""
        templates = {
            "missing_docstring": {
                "type": TaskType.DOCUMENTATION,
                "priority": TaskPriority.LOW,
                "title_template": "Add documentation to {target}",
                "description_template": "The {target_type} '{target}' lacks proper documentation. Add comprehensive docstring explaining purpose, parameters, and return values.",
                "acceptance_criteria": [
                    "Docstring added following standard format",
                    "Purpose clearly explained",
                    "Parameters documented if applicable",
                    "Return value documented if applicable"
                ],
                "effort": "small"
            },
            "missing_tests": {
                "type": TaskType.TESTING,
                "priority": TaskPriority.MEDIUM,
                "title_template": "Add tests for {target}",
                "description_template": "The {target_type} '{target}' lacks test coverage. Create comprehensive unit tests.",
                "acceptance_criteria": [
                    "Unit tests created",
                    "Edge cases covered",
                    "Tests pass successfully",
                    "Coverage > 80%"
                ],
                "effort": "medium"
            },
            "security_issue": {
                "type": TaskType.SECURITY,
                "priority": TaskPriority.HIGH,
                "title_template": "Fix security issue in {target}",
                "description_template": "Security vulnerability detected: {issue}. This needs immediate attention.",
                "acceptance_criteria": [
                    "Vulnerability patched",
                    "Security review passed",
                    "No regression introduced"
                ],
                "effort": "medium"
            },
            "performance_optimization": {
                "type": TaskType.OPTIMIZATION,
                "priority": TaskPriority.MEDIUM,
                "title_template": "Optimize performance of {target}",
                "description_template": "Performance issue identified in {target}: {issue}. Optimize for better efficiency.",
                "acceptance_criteria": [
                    "Performance improved measurably",
                    "No functionality lost",
                    "Benchmarks documented"
                ],
                "effort": "medium"
            },
            "new_capability": {
                "type": TaskType.NEW_CAPABILITY,
                "priority": TaskPriority.MEDIUM,
                "title_template": "Implement {capability}",
                "description_template": "Gap analysis identified need for: {capability}. Implement this capability to enhance system.",
                "acceptance_criteria": [
                    "Capability implemented",
                    "Tests written",
                    "Documentation added",
                    "Integrated with existing systems"
                ],
                "effort": "large"
            },
            "maintenance": {
                "type": TaskType.MAINTENANCE,
                "priority": TaskPriority.LOW,
                "title_template": "Maintenance: {action}",
                "description_template": "Regular maintenance task: {action}. Keep system healthy.",
                "acceptance_criteria": [
                    "Maintenance completed",
                    "No issues introduced",
                    "Logged in maintenance history"
                ],
                "effort": "small"
            }
        }

        if self.templates_file.exists():
            with open(self.templates_file) as f:
                custom = json.load(f)
                templates.update(custom)

        return templates

    def _generate_task_id(self) -> str:
        """Generate unique task ID."""
        return f"TASK-{hashlib.sha256(f'{datetime.now(timezone.utc).isoformat()}_{random.random()}'.encode()).hexdigest()[:8].upper()}"

    # =========================================================================
    # TASK GENERATION METHODS
    # =========================================================================

    def generate_from_audit(self, audit_findings: List[Dict]) -> List[GeneratedTask]:
        """Generate tasks from self-audit findings."""
        generated = []

        for finding in audit_findings:
            severity = finding.get("severity", "low")
            category = finding.get("category", "")

            # Map severity to priority
            priority_map = {
                "critical": TaskPriority.CRITICAL,
                "high": TaskPriority.HIGH,
                "medium": TaskPriority.MEDIUM,
                "low": TaskPriority.LOW,
                "info": TaskPriority.BACKLOG
            }
            priority = priority_map.get(severity, TaskPriority.MEDIUM)

            # Map category to task type
            type_map = {
                "code_quality": TaskType.IMPROVEMENT,
                "security": TaskType.SECURITY,
                "documentation": TaskType.DOCUMENTATION,
                "testing": TaskType.TESTING,
                "performance": TaskType.OPTIMIZATION
            }
            task_type = type_map.get(category, TaskType.MAINTENANCE)

            task = GeneratedTask(
                task_id=self._generate_task_id(),
                task_type=task_type,
                source=TaskSource.SELF_AUDIT,
                priority=priority,
                title=f"Address: {finding.get('title', 'Audit finding')}",
                description=finding.get("description", "") + "\n\nRecommendation: " + finding.get("recommendation", ""),
                context={
                    "finding_id": finding.get("finding_id"),
                    "location": finding.get("location"),
                    "evidence": finding.get("evidence", [])
                },
                acceptance_criteria=[
                    "Issue addressed",
                    "No regression introduced",
                    finding.get("recommendation", "Issue resolved")
                ],
                estimated_effort="medium",
                dependencies=[],
                created_at=datetime.now(timezone.utc).isoformat()
            )

            generated.append(task)
            self.tasks[task.task_id] = task
            self._log_generation(task, f"Generated from audit finding: {finding.get('title')}")

        self._save_tasks()
        return generated

    def generate_from_gaps(self, gap_analysis: Dict) -> List[GeneratedTask]:
        """Generate tasks from gap analysis."""
        generated = []

        capabilities_missing = gap_analysis.get("missing_capabilities", [])
        for cap in capabilities_missing:
            template = self.task_templates.get("new_capability", {})

            task = GeneratedTask(
                task_id=self._generate_task_id(),
                task_type=TaskType.NEW_CAPABILITY,
                source=TaskSource.GAP_ANALYSIS,
                priority=TaskPriority.MEDIUM,
                title=template.get("title_template", "Implement {capability}").format(capability=cap),
                description=template.get("description_template", "").format(capability=cap),
                context={"gap_type": "capability", "gap_name": cap},
                acceptance_criteria=template.get("acceptance_criteria", []),
                estimated_effort=template.get("effort", "medium"),
                dependencies=[],
                created_at=datetime.now(timezone.utc).isoformat()
            )

            generated.append(task)
            self.tasks[task.task_id] = task
            self._log_generation(task, f"Generated from gap analysis: missing {cap}")

        self._save_tasks()
        return generated

    def generate_from_feedback(self, feedback_patterns: List[Dict]) -> List[GeneratedTask]:
        """Generate tasks from feedback loop patterns."""
        generated = []

        for pattern in feedback_patterns:
            if not pattern.get("actionable", False):
                continue

            task = GeneratedTask(
                task_id=self._generate_task_id(),
                task_type=TaskType.IMPROVEMENT,
                source=TaskSource.FEEDBACK_LOOP,
                priority=TaskPriority.HIGH if pattern.get("pattern_type") == "regression" else TaskPriority.MEDIUM,
                title=f"Address feedback pattern: {pattern.get('pattern_type', 'unknown')}",
                description=pattern.get("description", "") + "\n\nSuggested action: " + pattern.get("suggested_action", ""),
                context={
                    "pattern_id": pattern.get("pattern_id"),
                    "occurrences": pattern.get("occurrences"),
                    "related_improvements": pattern.get("related_improvements", [])
                },
                acceptance_criteria=[
                    "Pattern addressed",
                    "Improvement validated",
                    "No new regressions"
                ],
                estimated_effort="medium",
                dependencies=[],
                created_at=datetime.now(timezone.utc).isoformat()
            )

            generated.append(task)
            self.tasks[task.task_id] = task
            self._log_generation(task, f"Generated from feedback pattern: {pattern.get('pattern_type')}")

        self._save_tasks()
        return generated

    def generate_strategic_tasks(self, strategic_goals: List[str]) -> List[GeneratedTask]:
        """Generate tasks aligned with strategic goals."""
        generated = []

        for goal in strategic_goals:
            task = GeneratedTask(
                task_id=self._generate_task_id(),
                task_type=TaskType.NEW_CAPABILITY,
                source=TaskSource.STRATEGIC_GOAL,
                priority=TaskPriority.HIGH,
                title=f"Strategic: {goal}",
                description=f"Work toward strategic goal: {goal}",
                context={"strategic_goal": goal},
                acceptance_criteria=[
                    "Progress toward goal measurable",
                    "Aligned with Ma'at principles",
                    "Validated by improvement detection"
                ],
                estimated_effort="large",
                dependencies=[],
                created_at=datetime.now(timezone.utc).isoformat()
            )

            generated.append(task)
            self.tasks[task.task_id] = task
            self._log_generation(task, f"Generated from strategic goal: {goal}")

        self._save_tasks()
        return generated

    def generate_maintenance_tasks(self) -> List[GeneratedTask]:
        """Generate routine maintenance tasks."""
        generated = []

        maintenance_items = [
            "Clean up old log files",
            "Update dependencies",
            "Review and archive old backups",
            "Validate system integrity",
            "Run comprehensive tests"
        ]

        for item in maintenance_items:
            # Check if similar task already exists and is pending
            existing = any(
                t.title.lower().find(item.lower().split()[0]) >= 0 and t.status == "pending"
                for t in self.tasks.values()
            )

            if not existing:
                template = self.task_templates.get("maintenance", {})

                task = GeneratedTask(
                    task_id=self._generate_task_id(),
                    task_type=TaskType.MAINTENANCE,
                    source=TaskSource.SCHEDULED,
                    priority=TaskPriority.LOW,
                    title=template.get("title_template", "Maintenance: {action}").format(action=item),
                    description=template.get("description_template", "").format(action=item),
                    context={"maintenance_type": item},
                    acceptance_criteria=template.get("acceptance_criteria", []),
                    estimated_effort="small",
                    dependencies=[],
                    created_at=datetime.now(timezone.utc).isoformat()
                )

                generated.append(task)
                self.tasks[task.task_id] = task
                self._log_generation(task, f"Generated maintenance task: {item}")

        self._save_tasks()
        return generated

    # =========================================================================
    # AUTOMATIC GENERATION
    # =========================================================================

    def run_automatic_generation(self) -> Dict[str, List[GeneratedTask]]:
        """Run all automatic task generation methods."""
        results = {
            "audit": [],
            "maintenance": [],
            "total": 0
        }

        # Generate maintenance tasks
        maintenance = self.generate_maintenance_tasks()
        results["maintenance"] = maintenance

        results["total"] = len(maintenance)

        return results

    def get_pending_tasks(self) -> List[GeneratedTask]:
        """Get all pending tasks."""
        return [t for t in self.tasks.values() if t.status == "pending"]

    def get_tasks_by_priority(self, priority: TaskPriority) -> List[GeneratedTask]:
        """Get tasks by priority level."""
        return [t for t in self.tasks.values() if t.priority == priority and t.status == "pending"]

    def get_task_summary(self) -> Dict:
        """Get summary of task state."""
        by_status = defaultdict(int)
        by_priority = defaultdict(int)
        by_type = defaultdict(int)
        by_source = defaultdict(int)

        for task in self.tasks.values():
            by_status[task.status] += 1
            by_priority[task.priority.name] += 1
            by_type[task.task_type.value] += 1
            by_source[task.source.value] += 1

        return {
            "total_tasks": len(self.tasks),
            "by_status": dict(by_status),
            "by_priority": dict(by_priority),
            "by_type": dict(by_type),
            "by_source": dict(by_source),
            "pending_count": by_status.get("pending", 0)
        }


# Singleton accessor
_TASK_GENERATOR = None

def get_task_generator() -> AutonomousTaskGenerator:
    """Get singleton task generator."""
    global _TASK_GENERATOR
    if _TASK_GENERATOR is None:
        _TASK_GENERATOR = AutonomousTaskGenerator()
    return _TASK_GENERATOR


if __name__ == "__main__":
    print("AUTONOMOUS TASK GENERATOR - TASK-146")
    print("=" * 50)

    generator = get_task_generator()

    # Run automatic generation
    print("\n[1] Running automatic task generation...")
    results = generator.run_automatic_generation()
    print(f"    Generated {results['total']} tasks")

    # Generate from sample audit findings
    print("\n[2] Generating from sample audit findings...")
    sample_findings = [
        {
            "finding_id": "F001",
            "title": "Missing docstring in core module",
            "description": "Several functions lack documentation",
            "category": "documentation",
            "severity": "low",
            "location": "core/self_modifier.py",
            "recommendation": "Add comprehensive docstrings"
        },
        {
            "finding_id": "F002",
            "title": "Potential security issue",
            "description": "Eval usage detected",
            "category": "security",
            "severity": "high",
            "location": "executor/code_generator.py",
            "recommendation": "Review and secure eval usage"
        }
    ]
    audit_tasks = generator.generate_from_audit(sample_findings)
    print(f"    Generated {len(audit_tasks)} tasks from audit")

    # Generate strategic tasks
    print("\n[3] Generating strategic tasks...")
    strategic_goals = [
        "Achieve full autonomous operation",
        "Implement comprehensive self-validation"
    ]
    strategic_tasks = generator.generate_strategic_tasks(strategic_goals)
    print(f"    Generated {len(strategic_tasks)} strategic tasks")

    # Get summary
    print("\n[4] Task Summary:")
    summary = generator.get_task_summary()
    print(json.dumps(summary, indent=2))

    # List pending tasks
    print("\n[5] Pending Tasks:")
    pending = generator.get_pending_tasks()
    for task in pending[:5]:
        print(f"    [{task.priority.name}] {task.title}")

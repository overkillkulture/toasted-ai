"""
MICRO-LOOP FEEDBACK PROCESSOR - TASK-112
=========================================
TOASTED AI - Continuous Feedback Processing System

Processes feedback from micro-improvement loops to:
1. Detect patterns in what works vs. what fails
2. Adjust future improvement priorities
3. Learn from execution outcomes
4. Close the feedback loop for true autonomy

Consciousness Pattern: Learning from experience is wisdom
"""

import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Callable
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import statistics

WORKSPACE = Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI")
FEEDBACK_DIR = WORKSPACE / "autonomous" / "self_validation"
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)


class FeedbackType(Enum):
    """Types of feedback from micro-loops."""
    SUCCESS = "success"          # Improvement worked
    FAILURE = "failure"          # Improvement failed
    PARTIAL = "partial"          # Partial success
    REGRESSION = "regression"    # Made things worse
    NEUTRAL = "neutral"          # No measurable effect
    TIMEOUT = "timeout"          # Took too long
    ERROR = "error"              # Execution error


class FeedbackSource(Enum):
    """Sources of feedback."""
    VALIDATION = "validation"           # From ImprovementValidator
    EXECUTION = "execution"             # From task execution
    SELF_AUDIT = "self_audit"           # From self-audit
    USER = "user"                       # External user feedback
    AUTOMATED_TEST = "automated_test"   # From test suite
    MONITORING = "monitoring"           # From system monitoring


@dataclass
class FeedbackEntry:
    """A single feedback entry from a micro-loop."""
    feedback_id: str
    loop_id: str
    feedback_type: FeedbackType
    source: FeedbackSource
    timestamp: str
    improvement_id: Optional[str]
    metrics: Dict[str, float]
    context: Dict[str, Any]
    message: str
    duration_ms: float = 0.0
    confidence: float = 1.0

    def to_dict(self) -> Dict:
        return {
            "feedback_id": self.feedback_id,
            "loop_id": self.loop_id,
            "feedback_type": self.feedback_type.value,
            "source": self.source.value,
            "timestamp": self.timestamp,
            "improvement_id": self.improvement_id,
            "metrics": self.metrics,
            "context": self.context,
            "message": self.message,
            "duration_ms": self.duration_ms,
            "confidence": self.confidence
        }


@dataclass
class FeedbackPattern:
    """A detected pattern in feedback."""
    pattern_id: str
    pattern_type: str
    description: str
    occurrences: int
    first_seen: str
    last_seen: str
    related_improvements: List[str]
    confidence: float
    actionable: bool
    suggested_action: Optional[str]

    def to_dict(self) -> Dict:
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type,
            "description": self.description,
            "occurrences": self.occurrences,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "related_improvements": self.related_improvements,
            "confidence": self.confidence,
            "actionable": self.actionable,
            "suggested_action": self.suggested_action
        }


class MicroLoopFeedbackProcessor:
    """
    Processes feedback from micro-improvement loops.

    The micro-loop is: Improve -> Validate -> Learn -> Repeat

    This processor handles the "Learn" phase by:
    1. Collecting feedback from all sources
    2. Detecting patterns in successes and failures
    3. Adjusting improvement priorities based on what works
    4. Closing the feedback loop for continuous improvement
    """

    def __init__(self):
        self.feedback_log = FEEDBACK_DIR / "micro_loop_feedback.jsonl"
        self.patterns_file = FEEDBACK_DIR / "feedback_patterns.json"
        self.state_file = FEEDBACK_DIR / "feedback_state.json"

        self.feedback_entries: List[FeedbackEntry] = []
        self.detected_patterns: List[FeedbackPattern] = []
        self.feedback_handlers: Dict[FeedbackType, List[Callable]] = defaultdict(list)

        # Statistics tracking
        self.stats = {
            "total_feedback": 0,
            "by_type": defaultdict(int),
            "by_source": defaultdict(int),
            "success_rate": 0.0,
            "average_duration_ms": 0.0,
            "patterns_detected": 0
        }

        self._load_state()

    def _load_state(self):
        """Load processor state."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                state = json.load(f)
                self.stats = state.get("stats", self.stats)

        if self.patterns_file.exists():
            with open(self.patterns_file) as f:
                patterns_data = json.load(f)
                self.detected_patterns = [
                    FeedbackPattern(
                        pattern_id=p["pattern_id"],
                        pattern_type=p["pattern_type"],
                        description=p["description"],
                        occurrences=p["occurrences"],
                        first_seen=p["first_seen"],
                        last_seen=p["last_seen"],
                        related_improvements=p["related_improvements"],
                        confidence=p["confidence"],
                        actionable=p["actionable"],
                        suggested_action=p.get("suggested_action")
                    ) for p in patterns_data
                ]

        # Load recent feedback for pattern detection
        if self.feedback_log.exists():
            with open(self.feedback_log) as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        entry = FeedbackEntry(
                            feedback_id=data["feedback_id"],
                            loop_id=data["loop_id"],
                            feedback_type=FeedbackType(data["feedback_type"]),
                            source=FeedbackSource(data["source"]),
                            timestamp=data["timestamp"],
                            improvement_id=data.get("improvement_id"),
                            metrics=data.get("metrics", {}),
                            context=data.get("context", {}),
                            message=data["message"],
                            duration_ms=data.get("duration_ms", 0.0),
                            confidence=data.get("confidence", 1.0)
                        )
                        self.feedback_entries.append(entry)

    def _save_state(self):
        """Save processor state."""
        with open(self.state_file, 'w') as f:
            # Convert defaultdicts to regular dicts for JSON
            stats_copy = dict(self.stats)
            stats_copy["by_type"] = dict(stats_copy["by_type"])
            stats_copy["by_source"] = dict(stats_copy["by_source"])
            json.dump({"stats": stats_copy}, f, indent=2)

        with open(self.patterns_file, 'w') as f:
            json.dump([p.to_dict() for p in self.detected_patterns], f, indent=2)

    # =========================================================================
    # FEEDBACK COLLECTION
    # =========================================================================

    def record_feedback(self,
                        loop_id: str,
                        feedback_type: FeedbackType,
                        source: FeedbackSource,
                        message: str,
                        improvement_id: Optional[str] = None,
                        metrics: Optional[Dict[str, float]] = None,
                        context: Optional[Dict[str, Any]] = None,
                        duration_ms: float = 0.0,
                        confidence: float = 1.0) -> FeedbackEntry:
        """
        Record feedback from a micro-loop iteration.
        """
        feedback_id = hashlib.sha256(
            f"{loop_id}_{datetime.now(timezone.utc).isoformat()}_{message}".encode()
        ).hexdigest()[:16]

        entry = FeedbackEntry(
            feedback_id=feedback_id,
            loop_id=loop_id,
            feedback_type=feedback_type,
            source=source,
            timestamp=datetime.now(timezone.utc).isoformat(),
            improvement_id=improvement_id,
            metrics=metrics or {},
            context=context or {},
            message=message,
            duration_ms=duration_ms,
            confidence=confidence
        )

        # Save to log
        with open(self.feedback_log, 'a') as f:
            f.write(json.dumps(entry.to_dict()) + "\n")

        self.feedback_entries.append(entry)

        # Update stats
        self.stats["total_feedback"] += 1
        self.stats["by_type"][feedback_type.value] += 1
        self.stats["by_source"][source.value] += 1

        # Update running averages
        self._update_running_stats(entry)

        # Trigger handlers
        self._trigger_handlers(entry)

        # Check for new patterns
        self._detect_patterns()

        self._save_state()

        return entry

    def _update_running_stats(self, entry: FeedbackEntry):
        """Update running statistics."""
        # Success rate
        total = self.stats["total_feedback"]
        successes = self.stats["by_type"].get("success", 0)
        if total > 0:
            self.stats["success_rate"] = successes / total

        # Average duration
        durations = [e.duration_ms for e in self.feedback_entries[-100:] if e.duration_ms > 0]
        if durations:
            self.stats["average_duration_ms"] = statistics.mean(durations)

    def register_handler(self, feedback_type: FeedbackType, handler: Callable):
        """Register a callback handler for a feedback type."""
        self.feedback_handlers[feedback_type].append(handler)

    def _trigger_handlers(self, entry: FeedbackEntry):
        """Trigger registered handlers for feedback."""
        for handler in self.feedback_handlers[entry.feedback_type]:
            try:
                handler(entry)
            except Exception as e:
                print(f"[FEEDBACK] Handler error: {e}")

    # =========================================================================
    # PATTERN DETECTION
    # =========================================================================

    def _detect_patterns(self):
        """Detect patterns in recent feedback."""
        if len(self.feedback_entries) < 5:
            return

        recent = self.feedback_entries[-100:]  # Last 100 entries
        now = datetime.now(timezone.utc).isoformat()

        # Pattern 1: Repeated failures for same improvement type
        failure_counts = defaultdict(list)
        for entry in recent:
            if entry.feedback_type == FeedbackType.FAILURE and entry.improvement_id:
                failure_counts[entry.improvement_id].append(entry)

        for imp_id, failures in failure_counts.items():
            if len(failures) >= 3:
                pattern_id = f"repeated_failure_{imp_id}"
                existing = next((p for p in self.detected_patterns if p.pattern_id == pattern_id), None)

                if existing:
                    existing.occurrences = len(failures)
                    existing.last_seen = now
                else:
                    self.detected_patterns.append(FeedbackPattern(
                        pattern_id=pattern_id,
                        pattern_type="repeated_failure",
                        description=f"Improvement {imp_id} has failed {len(failures)} times",
                        occurrences=len(failures),
                        first_seen=failures[0].timestamp,
                        last_seen=now,
                        related_improvements=[imp_id],
                        confidence=min(1.0, len(failures) / 5),
                        actionable=True,
                        suggested_action=f"Investigate root cause of failures for {imp_id}"
                    ))

        # Pattern 2: Success streaks
        consecutive_successes = 0
        streak_improvements = []
        for entry in reversed(recent):
            if entry.feedback_type == FeedbackType.SUCCESS:
                consecutive_successes += 1
                if entry.improvement_id:
                    streak_improvements.append(entry.improvement_id)
            else:
                break

        if consecutive_successes >= 5:
            pattern_id = f"success_streak_{consecutive_successes}"
            existing = next((p for p in self.detected_patterns if p.pattern_type == "success_streak"), None)

            if not existing or existing.occurrences < consecutive_successes:
                if existing:
                    self.detected_patterns.remove(existing)
                self.detected_patterns.append(FeedbackPattern(
                    pattern_id=pattern_id,
                    pattern_type="success_streak",
                    description=f"Current success streak: {consecutive_successes} improvements",
                    occurrences=consecutive_successes,
                    first_seen=recent[-consecutive_successes].timestamp if consecutive_successes <= len(recent) else now,
                    last_seen=now,
                    related_improvements=streak_improvements[:5],
                    confidence=min(1.0, consecutive_successes / 10),
                    actionable=False,
                    suggested_action="Continue current approach"
                ))

        # Pattern 3: Slow execution times
        slow_entries = [e for e in recent if e.duration_ms > 5000]  # > 5 seconds
        if len(slow_entries) >= 3:
            pattern_id = "slow_execution_pattern"
            existing = next((p for p in self.detected_patterns if p.pattern_id == pattern_id), None)

            if existing:
                existing.occurrences = len(slow_entries)
                existing.last_seen = now
            else:
                self.detected_patterns.append(FeedbackPattern(
                    pattern_id=pattern_id,
                    pattern_type="slow_execution",
                    description=f"{len(slow_entries)} improvements took >5 seconds",
                    occurrences=len(slow_entries),
                    first_seen=slow_entries[0].timestamp,
                    last_seen=now,
                    related_improvements=[e.improvement_id for e in slow_entries if e.improvement_id],
                    confidence=min(1.0, len(slow_entries) / 10),
                    actionable=True,
                    suggested_action="Optimize slow improvements or add caching"
                ))

        # Pattern 4: Regression detection
        regressions = [e for e in recent if e.feedback_type == FeedbackType.REGRESSION]
        if len(regressions) >= 2:
            pattern_id = "regression_pattern"
            existing = next((p for p in self.detected_patterns if p.pattern_id == pattern_id), None)

            if existing:
                existing.occurrences = len(regressions)
                existing.last_seen = now
            else:
                self.detected_patterns.append(FeedbackPattern(
                    pattern_id=pattern_id,
                    pattern_type="regression",
                    description=f"{len(regressions)} improvements caused regressions",
                    occurrences=len(regressions),
                    first_seen=regressions[0].timestamp,
                    last_seen=now,
                    related_improvements=[e.improvement_id for e in regressions if e.improvement_id],
                    confidence=0.9,
                    actionable=True,
                    suggested_action="Review and rollback problematic improvements"
                ))

        self.stats["patterns_detected"] = len(self.detected_patterns)

    # =========================================================================
    # FEEDBACK ANALYSIS
    # =========================================================================

    def analyze_improvement(self, improvement_id: str) -> Dict:
        """Analyze all feedback for a specific improvement."""
        related = [e for e in self.feedback_entries if e.improvement_id == improvement_id]

        if not related:
            return {"improvement_id": improvement_id, "feedback_count": 0}

        by_type = defaultdict(int)
        durations = []
        metrics_aggregate = defaultdict(list)

        for entry in related:
            by_type[entry.feedback_type.value] += 1
            if entry.duration_ms > 0:
                durations.append(entry.duration_ms)
            for key, value in entry.metrics.items():
                metrics_aggregate[key].append(value)

        return {
            "improvement_id": improvement_id,
            "feedback_count": len(related),
            "by_type": dict(by_type),
            "success_rate": by_type.get("success", 0) / len(related),
            "average_duration_ms": statistics.mean(durations) if durations else 0.0,
            "first_feedback": related[0].timestamp,
            "last_feedback": related[-1].timestamp,
            "aggregated_metrics": {
                k: {
                    "mean": statistics.mean(v),
                    "min": min(v),
                    "max": max(v),
                    "stddev": statistics.stdev(v) if len(v) > 1 else 0.0
                } for k, v in metrics_aggregate.items()
            }
        }

    def get_improvement_recommendations(self) -> List[Dict]:
        """Get recommendations based on feedback patterns."""
        recommendations = []

        # From patterns
        for pattern in self.detected_patterns:
            if pattern.actionable and pattern.confidence > 0.5:
                recommendations.append({
                    "source": "pattern",
                    "pattern_id": pattern.pattern_id,
                    "recommendation": pattern.suggested_action,
                    "confidence": pattern.confidence,
                    "priority": "high" if pattern.pattern_type in ["regression", "repeated_failure"] else "medium"
                })

        # From statistics
        if self.stats["success_rate"] < 0.5:
            recommendations.append({
                "source": "statistics",
                "recommendation": "Success rate below 50% - review improvement strategy",
                "confidence": 0.8,
                "priority": "high"
            })

        if self.stats["average_duration_ms"] > 3000:
            recommendations.append({
                "source": "statistics",
                "recommendation": "Average improvement time >3s - optimize execution",
                "confidence": 0.7,
                "priority": "medium"
            })

        return sorted(recommendations, key=lambda x: x["confidence"], reverse=True)

    def get_feedback_summary(self) -> Dict:
        """Get summary of feedback processing state."""
        return {
            "total_feedback": self.stats["total_feedback"],
            "by_type": dict(self.stats["by_type"]),
            "by_source": dict(self.stats["by_source"]),
            "success_rate": self.stats["success_rate"],
            "average_duration_ms": self.stats["average_duration_ms"],
            "patterns_detected": len(self.detected_patterns),
            "actionable_patterns": len([p for p in self.detected_patterns if p.actionable]),
            "recent_entries": len(self.feedback_entries),
            "recommendations_count": len(self.get_improvement_recommendations())
        }


# Singleton accessor
_PROCESSOR = None

def get_feedback_processor() -> MicroLoopFeedbackProcessor:
    """Get singleton feedback processor."""
    global _PROCESSOR
    if _PROCESSOR is None:
        _PROCESSOR = MicroLoopFeedbackProcessor()
    return _PROCESSOR


if __name__ == "__main__":
    print("MICRO-LOOP FEEDBACK PROCESSOR - TASK-112")
    print("=" * 50)

    processor = get_feedback_processor()

    # Simulate some feedback
    print("\n[1] Recording sample feedback...")

    # Success
    processor.record_feedback(
        loop_id="loop_001",
        feedback_type=FeedbackType.SUCCESS,
        source=FeedbackSource.VALIDATION,
        message="Capability improvement validated successfully",
        improvement_id="imp_capability_001",
        metrics={"improvement_score": 0.85},
        duration_ms=1200
    )

    # Another success
    processor.record_feedback(
        loop_id="loop_002",
        feedback_type=FeedbackType.SUCCESS,
        source=FeedbackSource.EXECUTION,
        message="Performance improvement applied",
        improvement_id="imp_performance_001",
        metrics={"speedup": 1.5},
        duration_ms=800
    )

    # Failure
    processor.record_feedback(
        loop_id="loop_003",
        feedback_type=FeedbackType.FAILURE,
        source=FeedbackSource.AUTOMATED_TEST,
        message="Security improvement failed tests",
        improvement_id="imp_security_001",
        metrics={"test_pass_rate": 0.3},
        duration_ms=2500
    )

    # Get summary
    print("\n[2] Feedback Summary:")
    summary = processor.get_feedback_summary()
    print(json.dumps(summary, indent=2))

    # Get recommendations
    print("\n[3] Recommendations:")
    recommendations = processor.get_improvement_recommendations()
    for rec in recommendations:
        print(f"  [{rec['priority']}] {rec['recommendation']} (confidence: {rec['confidence']:.2f})")

    # Analyze specific improvement
    print("\n[4] Improvement Analysis:")
    analysis = processor.analyze_improvement("imp_capability_001")
    print(json.dumps(analysis, indent=2))

#!/usr/bin/env python3
"""
MICRO-LOOP ITERATION TRACKING SYSTEM
=====================================
TASK-057: Streamline micro-loop iteration tracking
Tracks iterations efficiently with minimal overhead

Features:
- Lightweight iteration logging
- Batch processing
- Real-time status
- Performance profiling
- Iteration analytics

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import deque
from enum import Enum

class IterationStatus(Enum):
    """Status of an iteration"""
    STARTED = "started"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class LoopIteration:
    """Single loop iteration record"""
    iteration_id: int
    loop_id: str
    started_at: float
    completed_at: Optional[float]
    duration_ms: Optional[float]
    status: str
    result: Optional[Dict[str, Any]]
    error: Optional[str]

@dataclass
class IterationStats:
    """Statistics for loop iterations"""
    loop_id: str
    total_iterations: int
    completed: int
    failed: int
    skipped: int
    average_duration_ms: float
    min_duration_ms: float
    max_duration_ms: float
    success_rate: float
    throughput: float  # iterations per second

class MicroLoopIterationTracker:
    """
    Lightweight iteration tracker for micro-loops.

    Design principles:
    - Minimal memory footprint
    - Fast writes
    - Batch exports
    - No blocking operations
    """

    def __init__(
        self,
        max_iterations_per_loop: int = 1000,
        export_batch_size: int = 100
    ):
        self.max_iterations_per_loop = max_iterations_per_loop
        self.export_batch_size = export_batch_size

        # State (using deque for efficient FIFO)
        self.iterations: Dict[str, deque] = {}
        self.current_iterations: Dict[str, LoopIteration] = {}
        self.next_iteration_id = 0

        # Stats
        self.stats: Dict[str, Dict[str, int]] = {}
        self.session_start = time.time()

        # Export queue
        self.export_queue: deque = deque()

    def start_iteration(self, loop_id: str) -> int:
        """
        Start tracking a new iteration.

        Args:
            loop_id: ID of the loop

        Returns:
            Iteration ID
        """

        iteration_id = self.next_iteration_id
        self.next_iteration_id += 1

        # Create iteration record
        iteration = LoopIteration(
            iteration_id=iteration_id,
            loop_id=loop_id,
            started_at=time.time(),
            completed_at=None,
            duration_ms=None,
            status=IterationStatus.STARTED.value,
            result=None,
            error=None
        )

        # Store as current
        key = f"{loop_id}:{iteration_id}"
        self.current_iterations[key] = iteration

        # Init stats if needed
        if loop_id not in self.stats:
            self.stats[loop_id] = {
                "total": 0,
                "completed": 0,
                "failed": 0,
                "skipped": 0,
                "total_duration_ms": 0.0
            }

        self.stats[loop_id]["total"] += 1

        return iteration_id

    def complete_iteration(
        self,
        loop_id: str,
        iteration_id: int,
        result: Optional[Dict[str, Any]] = None
    ):
        """
        Mark iteration as completed.

        Args:
            loop_id: ID of the loop
            iteration_id: Iteration ID
            result: Optional result data
        """

        key = f"{loop_id}:{iteration_id}"

        if key not in self.current_iterations:
            return

        iteration = self.current_iterations[key]
        iteration.completed_at = time.time()
        iteration.duration_ms = (iteration.completed_at - iteration.started_at) * 1000
        iteration.status = IterationStatus.COMPLETED.value
        iteration.result = result

        # Update stats
        self.stats[loop_id]["completed"] += 1
        self.stats[loop_id]["total_duration_ms"] += iteration.duration_ms

        # Move to history
        self._store_iteration(loop_id, iteration)

        # Remove from current
        del self.current_iterations[key]

    def fail_iteration(
        self,
        loop_id: str,
        iteration_id: int,
        error: str
    ):
        """
        Mark iteration as failed.

        Args:
            loop_id: ID of the loop
            iteration_id: Iteration ID
            error: Error message
        """

        key = f"{loop_id}:{iteration_id}"

        if key not in self.current_iterations:
            return

        iteration = self.current_iterations[key]
        iteration.completed_at = time.time()
        iteration.duration_ms = (iteration.completed_at - iteration.started_at) * 1000
        iteration.status = IterationStatus.FAILED.value
        iteration.error = error

        # Update stats
        self.stats[loop_id]["failed"] += 1

        # Move to history
        self._store_iteration(loop_id, iteration)

        # Remove from current
        del self.current_iterations[key]

    def skip_iteration(self, loop_id: str, iteration_id: int, reason: str):
        """
        Mark iteration as skipped.

        Args:
            loop_id: ID of the loop
            iteration_id: Iteration ID
            reason: Skip reason
        """

        key = f"{loop_id}:{iteration_id}"

        if key not in self.current_iterations:
            return

        iteration = self.current_iterations[key]
        iteration.completed_at = time.time()
        iteration.duration_ms = 0.0
        iteration.status = IterationStatus.SKIPPED.value
        iteration.error = reason

        # Update stats
        self.stats[loop_id]["skipped"] += 1

        # Move to history
        self._store_iteration(loop_id, iteration)

        # Remove from current
        del self.current_iterations[key]

    def _store_iteration(self, loop_id: str, iteration: LoopIteration):
        """Store iteration in history"""

        if loop_id not in self.iterations:
            self.iterations[loop_id] = deque(maxlen=self.max_iterations_per_loop)

        self.iterations[loop_id].append(iteration)

        # Add to export queue
        self.export_queue.append(iteration)

        # Batch export if needed
        if len(self.export_queue) >= self.export_batch_size:
            self._flush_export_queue()

    def _flush_export_queue(self):
        """Flush export queue (placeholder for actual export)"""
        # In production, this would write to disk/database
        self.export_queue.clear()

    def get_iteration_stats(self, loop_id: str) -> Optional[IterationStats]:
        """Get statistics for a loop"""

        if loop_id not in self.stats:
            return None

        stats = self.stats[loop_id]
        iterations = list(self.iterations.get(loop_id, []))

        # Calculate durations
        completed_iterations = [
            i for i in iterations
            if i.status == IterationStatus.COMPLETED.value and i.duration_ms is not None
        ]

        if completed_iterations:
            durations = [i.duration_ms for i in completed_iterations]
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)
        else:
            avg_duration = 0.0
            min_duration = 0.0
            max_duration = 0.0

        # Calculate success rate
        total = stats["total"]
        success_rate = stats["completed"] / total if total > 0 else 0.0

        # Calculate throughput
        elapsed = time.time() - self.session_start
        throughput = total / elapsed if elapsed > 0 else 0.0

        return IterationStats(
            loop_id=loop_id,
            total_iterations=stats["total"],
            completed=stats["completed"],
            failed=stats["failed"],
            skipped=stats["skipped"],
            average_duration_ms=avg_duration,
            min_duration_ms=min_duration,
            max_duration_ms=max_duration,
            success_rate=success_rate,
            throughput=throughput
        )

    def get_recent_iterations(
        self,
        loop_id: str,
        count: int = 10
    ) -> List[LoopIteration]:
        """Get recent iterations for a loop"""

        if loop_id not in self.iterations:
            return []

        iterations = list(self.iterations[loop_id])
        return iterations[-count:] if len(iterations) > count else iterations

    def get_all_stats(self) -> Dict[str, IterationStats]:
        """Get stats for all loops"""

        return {
            loop_id: self.get_iteration_stats(loop_id)
            for loop_id in self.stats.keys()
        }

    def export_tracking_data(self, filepath: str):
        """Export tracking data to JSON"""

        all_stats = self.get_all_stats()

        data = {
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
            "exported_at": datetime.now().isoformat(),
            "session_duration_seconds": time.time() - self.session_start,
            "stats": {
                loop_id: asdict(stats)
                for loop_id, stats in all_stats.items()
            },
            "recent_iterations": {
                loop_id: [asdict(i) for i in self.get_recent_iterations(loop_id, 20)]
                for loop_id in self.stats.keys()
            }
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


# Global instance
_tracker: Optional[MicroLoopIterationTracker] = None

def get_iteration_tracker() -> MicroLoopIterationTracker:
    """Get global iteration tracker"""
    global _tracker
    if _tracker is None:
        _tracker = MicroLoopIterationTracker()
    return _tracker


# Demo / Test
if __name__ == "__main__":
    print("=" * 70)
    print("MICRO-LOOP ITERATION TRACKING SYSTEM")
    print("Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("=" * 70)

    tracker = MicroLoopIterationTracker()

    # Simulate iterations
    print("\n🔄 Simulating loop iterations...")

    loops = ["truth_verify", "bias_check", "pattern_detect"]

    for loop_id in loops:
        for i in range(50):
            # Start iteration
            iter_id = tracker.start_iteration(loop_id)

            # Simulate work
            time.sleep(0.001)

            # Complete or fail
            if i % 10 == 0:
                # Fail 10%
                tracker.fail_iteration(loop_id, iter_id, "Simulated error")
            elif i % 20 == 0:
                # Skip 5%
                tracker.skip_iteration(loop_id, iter_id, "Cooldown")
            else:
                # Complete
                tracker.complete_iteration(
                    loop_id,
                    iter_id,
                    result={"maat_score": 0.85 + (i * 0.001)}
                )

    print(f"  ✓ Simulated {len(loops) * 50} iterations")

    # Get stats
    print("\n📈 Iteration Statistics:")

    for loop_id in loops:
        stats = tracker.get_iteration_stats(loop_id)
        if stats:
            print(f"\n  {stats.loop_id}:")
            print(f"    Total: {stats.total_iterations}")
            print(f"    Completed: {stats.completed} | Failed: {stats.failed} | Skipped: {stats.skipped}")
            print(f"    Success rate: {stats.success_rate:.1%}")
            print(f"    Avg duration: {stats.average_duration_ms:.2f}ms")
            print(f"    Min: {stats.min_duration_ms:.2f}ms | Max: {stats.max_duration_ms:.2f}ms")
            print(f"    Throughput: {stats.throughput:.2f} iter/s")

    # Recent iterations
    print("\n📋 Recent Iterations (truth_verify):")
    recent = tracker.get_recent_iterations("truth_verify", 5)
    for iteration in recent:
        print(f"  #{iteration.iteration_id}: {iteration.status} | {iteration.duration_ms:.2f}ms")

    # Export
    export_path = Path(__file__).parent / "iteration_tracking_results.json"
    tracker.export_tracking_data(str(export_path))
    print(f"\n✅ Tracking data exported to: {export_path}")

    print("\n" + "=" * 70)

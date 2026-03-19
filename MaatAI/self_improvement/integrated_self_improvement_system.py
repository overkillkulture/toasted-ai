#!/usr/bin/env python3
"""
INTEGRATED SELF-IMPROVEMENT SYSTEM
===================================
Wave 5 Batch A - Complete Integration
Combines all self-improvement components into unified system

Components:
1. Micro-loop improvement detection (TASK-012, 013)
2. Recursive self-improvement logging (TASK-018)
3. Micro-loop feedback integration (TASK-030)
4. Improvement convergence detection (TASK-040, 093)
5. Self-improvement metrics collection (TASK-056)
6. Micro-loop iteration tracking (TASK-057)

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import all components
from micro_loop_improvement_detector import (
    MicroLoopImprovementDetector,
    get_improvement_detector
)
from recursive_self_improvement_logger import (
    RecursiveSelfImprovementLogger,
    ModificationType
)
from micro_loop_feedback_integrator import (
    MicroLoopFeedbackIntegrator,
    FeedbackType,
    get_feedback_integrator
)
from improvement_convergence_detector import (
    ImprovementConvergenceDetector,
    ConvergenceState
)
from self_improvement_metrics_collector import (
    SelfImprovementMetricsCollector,
    get_metrics_collector
)
from micro_loop_iteration_tracker import (
    MicroLoopIterationTracker,
    get_iteration_tracker
)

class IntegratedSelfImprovementSystem:
    """
    Unified self-improvement system integrating all components.

    Flow:
    1. Track iterations (IterationTracker)
    2. Detect improvements (ImprovementDetector)
    3. Log modifications (RecursiveLogger)
    4. Generate feedback (FeedbackIntegrator)
    5. Collect metrics (MetricsCollector)
    6. Check convergence (ConvergenceDetector)
    7. Apply feedback and repeat
    """

    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)

        # Initialize all components
        self.improvement_detector = MicroLoopImprovementDetector()
        self.recursive_logger = RecursiveSelfImprovementLogger(
            log_path=str(self.workspace / "recursive_improvements.json")
        )
        self.feedback_integrator = MicroLoopFeedbackIntegrator()
        self.convergence_detector = ImprovementConvergenceDetector()
        self.metrics_collector = SelfImprovementMetricsCollector()
        self.iteration_tracker = MicroLoopIterationTracker()

        # System state
        self.is_running = False
        self.cycles_completed = 0

    async def run_improvement_cycle(
        self,
        loop_id: str,
        current_score: float,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run one complete improvement cycle.

        Returns:
            Cycle results including improvements, feedback, and convergence
        """

        cycle_start = time.time()
        results = {
            "cycle": self.cycles_completed + 1,
            "loop_id": loop_id,
            "timestamp": cycle_start
        }

        # 1. Track iteration
        iter_id = self.iteration_tracker.start_iteration(loop_id)
        self.metrics_collector.increment("loop.executions", {"loop": loop_id})

        try:
            # 2. Detect improvement
            improvement_signal = self.improvement_detector.detect_improvement(
                loop_id=loop_id,
                metric="maat_score",
                current_value=current_score,
                higher_is_better=True
            )

            if improvement_signal:
                results["improvement_detected"] = True
                results["improvement"] = {
                    "delta": improvement_signal.delta,
                    "delta_percent": improvement_signal.delta_percent,
                    "type": improvement_signal.improvement_type,
                    "confidence": improvement_signal.confidence
                }

                self.metrics_collector.increment("improvement.detected")
                self.metrics_collector.collect(
                    "improvement.delta",
                    improvement_signal.delta_percent
                )

                # 3. Log as recursive modification if significant
                if improvement_signal.confidence >= 0.7:
                    self.recursive_logger.log_modification(
                        mod_type=ModificationType.PARAMETER_TUNE,
                        description=f"Improvement in {loop_id}",
                        target_component=loop_id,
                        old_state={"score": improvement_signal.baseline},
                        new_state={"score": improvement_signal.current},
                        maat_score=current_score
                    )

                # 4. Generate feedback
                self.feedback_integrator.integrate_success(
                    loop_id=loop_id,
                    success_data={
                        "pattern": f"improvement_detected_{improvement_signal.improvement_type}",
                        "parameters": {"score": current_score}
                    },
                    strength=improvement_signal.confidence
                )

                self.metrics_collector.increment("feedback.signals_generated")

            else:
                results["improvement_detected"] = False

            # 5. Check convergence
            convergence_metrics = self.convergence_detector.update_metric(
                metric_name=f"{loop_id}.maat_score",
                value=current_score,
                higher_is_better=True
            )

            results["convergence"] = {
                "state": convergence_metrics.convergence_state,
                "confidence": convergence_metrics.confidence,
                "iterations_without_improvement": convergence_metrics.iterations_without_improvement
            }

            self.metrics_collector.gauge(
                "convergence.score",
                convergence_metrics.confidence
            )

            # 6. Complete iteration
            self.iteration_tracker.complete_iteration(
                loop_id=loop_id,
                iteration_id=iter_id,
                result=results
            )

            self.metrics_collector.increment("loop.successes", {"loop": loop_id})

            # 7. Update cycle count
            self.cycles_completed += 1

            # Calculate duration
            duration_ms = (time.time() - cycle_start) * 1000
            results["duration_ms"] = duration_ms
            self.metrics_collector.collect("loop.duration_ms", duration_ms)

            return results

        except Exception as e:
            # Handle failure
            self.iteration_tracker.fail_iteration(loop_id, iter_id, str(e))
            self.metrics_collector.increment("loop.failures", {"loop": loop_id})
            raise

    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""

        # Get convergence report
        convergence_report = self.convergence_detector.check_overall_convergence()

        # Get improvement metrics
        improvement_metrics = self.improvement_detector.get_improvement_metrics()

        # Get feedback stats
        feedback_pending = len(self.feedback_integrator.get_pending_feedback())

        # Get modification stats
        mod_stats = self.recursive_logger.get_stats()

        # Get iteration stats
        all_iter_stats = self.iteration_tracker.get_all_stats()

        return {
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
            "timestamp": datetime.now().isoformat(),
            "cycles_completed": self.cycles_completed,
            "convergence": {
                "overall_state": convergence_report.overall_state,
                "score": convergence_report.convergence_score,
                "should_stop": convergence_report.should_stop,
                "recommendation": convergence_report.recommendation
            },
            "improvements": {
                "total": improvement_metrics.total_improvements,
                "micro": improvement_metrics.micro_improvements,
                "macro": improvement_metrics.macro_improvements,
                "breakthroughs": improvement_metrics.breakthroughs,
                "rate": improvement_metrics.improvement_rate
            },
            "feedback": {
                "pending_signals": feedback_pending,
                "integrator_stats": self.feedback_integrator.stats
            },
            "modifications": mod_stats,
            "iterations": {
                loop_id: {
                    "total": stats.total_iterations,
                    "success_rate": stats.success_rate,
                    "throughput": stats.throughput
                }
                for loop_id, stats in all_iter_stats.items()
            }
        }

    def export_all_data(self, output_dir: str):
        """Export all system data"""

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Export each component
        self.improvement_detector.export_improvements(
            str(output_path / "improvement_detection.json")
        )
        self.convergence_detector.export_convergence_data(
            str(output_path / "convergence_analysis.json")
        )
        self.feedback_integrator.export_feedback_data(
            str(output_path / "feedback_integration.json")
        )
        self.metrics_collector.export_metrics(
            str(output_path / "metrics_collection.json")
        )
        self.iteration_tracker.export_tracking_data(
            str(output_path / "iteration_tracking.json")
        )

        # Export system status
        status = self.get_system_status()
        with open(output_path / "system_status.json", 'w') as f:
            json.dump(status, f, indent=2)

        return output_path


# Demo / Test
if __name__ == "__main__":
    print("=" * 70)
    print("INTEGRATED SELF-IMPROVEMENT SYSTEM")
    print("Wave 5 Batch A - Complete Integration")
    print("Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("=" * 70)

    system = IntegratedSelfImprovementSystem(workspace_path=".")

    async def run_demo():
        """Run demo cycles"""

        print("\n🚀 Running self-improvement cycles...")

        loops = ["truth_verify", "bias_check", "pattern_detect"]

        for i in range(30):
            for loop_id in loops:
                # Simulate improving score
                import math
                base_score = 0.7
                improvement = 0.3 * (1 - math.exp(-i/10))
                score = base_score + improvement + (0.02 * (i % 3 - 1))

                # Run cycle
                results = await system.run_improvement_cycle(
                    loop_id=loop_id,
                    current_score=score,
                    context={"iteration": i}
                )

                if i % 10 == 0 and loop_id == "truth_verify":
                    print(f"  Cycle {results['cycle']}: {loop_id} | Score: {score:.4f}")
                    if results.get("improvement_detected"):
                        imp = results["improvement"]
                        print(f"    ✓ Improvement: {imp['delta_percent']:.2%} ({imp['type']})")

        print(f"\n✅ Completed {system.cycles_completed} cycles")

        # Get status
        print("\n📊 System Status:")
        status = system.get_system_status()

        print(f"\n  Convergence:")
        print(f"    State: {status['convergence']['overall_state']}")
        print(f"    Score: {status['convergence']['score']:.2%}")
        print(f"    Should stop: {status['convergence']['should_stop']}")

        print(f"\n  Improvements:")
        print(f"    Total: {status['improvements']['total']}")
        print(f"    Micro: {status['improvements']['micro']} | Macro: {status['improvements']['macro']} | Breakthrough: {status['improvements']['breakthroughs']}")
        print(f"    Rate: {status['improvements']['rate']:.2f}/min")

        print(f"\n  Modifications:")
        print(f"    Total: {status['modifications']['total_modifications']}")
        print(f"    Applied: {status['modifications']['applied_modifications']}")

        # Export
        output_dir = Path(__file__).parent / "wave5_batch_a_results"
        system.export_all_data(str(output_dir))
        print(f"\n✅ All data exported to: {output_dir}")

        print("\n" + "=" * 70)
        print("🎉 WAVE 5 BATCH A: SELF-IMPROVEMENT CORE - COMPLETE")
        print("=" * 70)

    # Run async demo
    asyncio.run(run_demo())

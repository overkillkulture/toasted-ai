#!/usr/bin/env python3
"""
MICRO-LOOP FEEDBACK INTEGRATION SYSTEM
=======================================
TASK-030: Create micro-loop feedback integration
Closes feedback loops by feeding improvement data back into loops

Features:
- Real-time feedback injection
- Success pattern amplification
- Failure pattern suppression
- Adaptive loop tuning
- Cross-loop learning

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from collections import defaultdict
from enum import Enum

class FeedbackType(Enum):
    """Types of feedback"""
    SUCCESS_AMPLIFICATION = "success_amplification"
    FAILURE_SUPPRESSION = "failure_suppression"
    PATTERN_LEARNING = "pattern_learning"
    THRESHOLD_ADJUSTMENT = "threshold_adjustment"
    PRIORITY_ADJUSTMENT = "priority_adjustment"

@dataclass
class FeedbackSignal:
    """Single feedback signal"""
    timestamp: float
    source_loop_id: str
    target_loop_id: str
    feedback_type: str
    data: Dict[str, Any]
    strength: float  # 0.0-1.0
    applied: bool

@dataclass
class LoopLearning:
    """What a loop has learned"""
    loop_id: str
    success_patterns: List[str]
    failure_patterns: List[str]
    optimal_parameters: Dict[str, Any]
    performance_trend: str  # "improving", "stable", "degrading"
    learning_count: int

class MicroLoopFeedbackIntegrator:
    """
    Integrates feedback into micro-loops for continuous improvement.

    Closes the feedback loop:
    1. Detect improvement/degradation
    2. Generate feedback signal
    3. Apply to relevant loops
    4. Monitor impact
    5. Repeat
    """

    def __init__(self):
        # State
        self.feedback_signals: List[FeedbackSignal] = []
        self.loop_learning: Dict[str, LoopLearning] = {}
        self.cross_loop_patterns: Dict[str, List[str]] = defaultdict(list)

        # Configuration
        self.feedback_strength_threshold = 0.3
        self.success_amplification_factor = 1.2
        self.failure_suppression_factor = 0.8

        # Stats
        self.stats = {
            "signals_generated": 0,
            "signals_applied": 0,
            "success_amplifications": 0,
            "failure_suppressions": 0,
            "cross_loop_learnings": 0,
            "session_start": time.time()
        }

    def generate_feedback(
        self,
        source_loop_id: str,
        target_loop_id: str,
        feedback_type: FeedbackType,
        data: Dict[str, Any],
        strength: float
    ) -> FeedbackSignal:
        """Generate a feedback signal"""

        signal = FeedbackSignal(
            timestamp=time.time(),
            source_loop_id=source_loop_id,
            target_loop_id=target_loop_id,
            feedback_type=feedback_type.value,
            data=data,
            strength=strength,
            applied=False
        )

        self.feedback_signals.append(signal)
        self.stats["signals_generated"] += 1

        return signal

    def integrate_success(
        self,
        loop_id: str,
        success_data: Dict[str, Any],
        strength: float = 0.8
    ):
        """
        Integrate successful pattern into loop.

        Args:
            loop_id: Loop that succeeded
            success_data: What made it successful
            strength: How strong the success signal is
        """

        # Update learning
        if loop_id not in self.loop_learning:
            self.loop_learning[loop_id] = LoopLearning(
                loop_id=loop_id,
                success_patterns=[],
                failure_patterns=[],
                optimal_parameters={},
                performance_trend="stable",
                learning_count=0
            )

        learning = self.loop_learning[loop_id]

        # Extract pattern
        pattern = success_data.get("pattern", "unknown")
        if pattern not in learning.success_patterns:
            learning.success_patterns.append(pattern)

        # Update parameters
        if "parameters" in success_data:
            for key, value in success_data["parameters"].items():
                learning.optimal_parameters[key] = value

        learning.learning_count += 1
        learning.performance_trend = "improving"

        # Generate feedback signal to amplify
        signal = self.generate_feedback(
            source_loop_id=loop_id,
            target_loop_id=loop_id,
            feedback_type=FeedbackType.SUCCESS_AMPLIFICATION,
            data=success_data,
            strength=strength
        )

        self.stats["success_amplifications"] += 1

        return signal

    def integrate_failure(
        self,
        loop_id: str,
        failure_data: Dict[str, Any],
        strength: float = 0.8
    ):
        """
        Integrate failure pattern into loop to suppress it.

        Args:
            loop_id: Loop that failed
            failure_data: What caused failure
            strength: How strong the failure signal is
        """

        # Update learning
        if loop_id not in self.loop_learning:
            self.loop_learning[loop_id] = LoopLearning(
                loop_id=loop_id,
                success_patterns=[],
                failure_patterns=[],
                optimal_parameters={},
                performance_trend="stable",
                learning_count=0
            )

        learning = self.loop_learning[loop_id]

        # Extract pattern
        pattern = failure_data.get("pattern", "unknown")
        if pattern not in learning.failure_patterns:
            learning.failure_patterns.append(pattern)

        learning.learning_count += 1

        # Generate feedback signal to suppress
        signal = self.generate_feedback(
            source_loop_id=loop_id,
            target_loop_id=loop_id,
            feedback_type=FeedbackType.FAILURE_SUPPRESSION,
            data=failure_data,
            strength=strength
        )

        self.stats["failure_suppressions"] += 1

        return signal

    def cross_loop_learning(
        self,
        source_loop_id: str,
        target_loop_id: str,
        pattern: str,
        strength: float = 0.6
    ):
        """
        Transfer learning from one loop to another.

        Args:
            source_loop_id: Loop that learned pattern
            target_loop_id: Loop to apply pattern to
            pattern: Pattern to transfer
            strength: Transfer strength
        """

        # Record cross-loop pattern
        key = f"{source_loop_id}->{target_loop_id}"
        if pattern not in self.cross_loop_patterns[key]:
            self.cross_loop_patterns[key].append(pattern)

        # Generate feedback
        signal = self.generate_feedback(
            source_loop_id=source_loop_id,
            target_loop_id=target_loop_id,
            feedback_type=FeedbackType.PATTERN_LEARNING,
            data={"pattern": pattern},
            strength=strength
        )

        self.stats["cross_loop_learnings"] += 1

        return signal

    def apply_feedback(
        self,
        signal: FeedbackSignal,
        loop_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply feedback signal to loop configuration.

        Args:
            signal: Feedback signal to apply
            loop_config: Current loop configuration

        Returns:
            Updated loop configuration
        """

        if signal.strength < self.feedback_strength_threshold:
            return loop_config

        new_config = loop_config.copy()

        # Apply based on type
        if signal.feedback_type == FeedbackType.SUCCESS_AMPLIFICATION.value:
            # Increase priority, decrease cooldown
            if "priority" in new_config:
                new_config["priority"] = int(
                    new_config["priority"] * self.success_amplification_factor
                )
            if "cooldown" in new_config:
                new_config["cooldown"] = (
                    new_config["cooldown"] * self.failure_suppression_factor
                )

        elif signal.feedback_type == FeedbackType.FAILURE_SUPPRESSION.value:
            # Decrease priority, increase cooldown
            if "priority" in new_config:
                new_config["priority"] = int(
                    new_config["priority"] * self.failure_suppression_factor
                )
            if "cooldown" in new_config:
                new_config["cooldown"] = (
                    new_config["cooldown"] * self.success_amplification_factor
                )

        elif signal.feedback_type == FeedbackType.THRESHOLD_ADJUSTMENT.value:
            # Adjust thresholds
            if "threshold" in signal.data and "threshold" in new_config:
                new_config["threshold"] = signal.data["threshold"]

        elif signal.feedback_type == FeedbackType.PATTERN_LEARNING.value:
            # Add learned pattern
            if "patterns" not in new_config:
                new_config["patterns"] = []
            pattern = signal.data.get("pattern")
            if pattern and pattern not in new_config["patterns"]:
                new_config["patterns"].append(pattern)

        signal.applied = True
        self.stats["signals_applied"] += 1

        return new_config

    def get_loop_learning(self, loop_id: str) -> Optional[LoopLearning]:
        """Get learning data for a loop"""
        return self.loop_learning.get(loop_id)

    def get_pending_feedback(
        self,
        target_loop_id: Optional[str] = None
    ) -> List[FeedbackSignal]:
        """Get pending feedback signals"""

        pending = [s for s in self.feedback_signals if not s.applied]

        if target_loop_id:
            pending = [s for s in pending if s.target_loop_id == target_loop_id]

        return pending

    def export_feedback_data(self, filepath: str):
        """Export feedback data to JSON"""

        data = {
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
            "exported_at": datetime.now().isoformat(),
            "stats": self.stats,
            "signals": [asdict(s) for s in self.feedback_signals],
            "loop_learning": {
                k: asdict(v) for k, v in self.loop_learning.items()
            },
            "cross_loop_patterns": dict(self.cross_loop_patterns)
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


# Global instance
_integrator: Optional[MicroLoopFeedbackIntegrator] = None

def get_feedback_integrator() -> MicroLoopFeedbackIntegrator:
    """Get global feedback integrator"""
    global _integrator
    if _integrator is None:
        _integrator = MicroLoopFeedbackIntegrator()
    return _integrator


# Demo / Test
if __name__ == "__main__":
    print("=" * 70)
    print("MICRO-LOOP FEEDBACK INTEGRATION SYSTEM")
    print("Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("=" * 70)

    integrator = MicroLoopFeedbackIntegrator()

    # Simulate feedback integration
    print("\n🔄 Simulating feedback integration...")

    # Success in truth_verify loop
    integrator.integrate_success(
        loop_id="truth_verify",
        success_data={
            "pattern": "regex_detection_works",
            "parameters": {"confidence_threshold": 0.85}
        },
        strength=0.9
    )
    print("  ✓ Integrated success from truth_verify")

    # Failure in bias_check loop
    integrator.integrate_failure(
        loop_id="bias_check",
        failure_data={
            "pattern": "false_positive_on_technical_terms",
            "context": "Technical language flagged as bias"
        },
        strength=0.7
    )
    print("  ✓ Integrated failure from bias_check")

    # Cross-loop learning
    integrator.cross_loop_learning(
        source_loop_id="truth_verify",
        target_loop_id="fact_check",
        pattern="regex_detection_works",
        strength=0.6
    )
    print("  ✓ Cross-loop learning: truth_verify -> fact_check")

    # Apply feedback to loop config
    loop_config = {
        "priority": 5,
        "cooldown": 1.0,
        "threshold": 0.7,
        "patterns": []
    }

    pending = integrator.get_pending_feedback("truth_verify")
    if pending:
        new_config = integrator.apply_feedback(pending[0], loop_config)
        print(f"\n  Updated config:")
        print(f"    Priority: {loop_config['priority']} -> {new_config['priority']}")
        print(f"    Cooldown: {loop_config['cooldown']:.2f} -> {new_config['cooldown']:.2f}")

    # Get learning
    learning = integrator.get_loop_learning("truth_verify")
    if learning:
        print(f"\n📚 truth_verify Learning:")
        print(f"   Success patterns: {len(learning.success_patterns)}")
        print(f"   Failure patterns: {len(learning.failure_patterns)}")
        print(f"   Performance trend: {learning.performance_trend}")
        print(f"   Learning count: {learning.learning_count}")

    # Stats
    print(f"\n📈 Feedback Stats:")
    print(f"   Signals generated: {integrator.stats['signals_generated']}")
    print(f"   Signals applied: {integrator.stats['signals_applied']}")
    print(f"   Success amplifications: {integrator.stats['success_amplifications']}")
    print(f"   Failure suppressions: {integrator.stats['failure_suppressions']}")
    print(f"   Cross-loop learnings: {integrator.stats['cross_loop_learnings']}")

    # Export
    export_path = Path(__file__).parent / "feedback_integration_results.json"
    integrator.export_feedback_data(str(export_path))
    print(f"\n✅ Results exported to: {export_path}")

    print("\n" + "=" * 70)

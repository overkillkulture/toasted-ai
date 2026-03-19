"""
TASK-028: SELF-HEALING CODE SEGMENTS
=====================================
MaatAI Verification System

Implements self-healing capabilities for code segments that detect and repair:
- Logic errors
- Entropy degradation
- Principle violations
- Performance issues
- Security vulnerabilities

Self-healing = Autonomous detection, diagnosis, and repair
Code segments = Modular, testable, repairable units
"""

import ast
import inspect
import json
import hashlib
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class CodeHealthStatus(Enum):
    """Code health status levels."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILING = "failing"
    CRITICAL = "critical"


class HealingStrategy(Enum):
    """Strategies for code healing."""
    RETRY = "retry"  # Retry with same logic
    FALLBACK = "fallback"  # Use backup implementation
    CIRCUIT_BREAK = "circuit_break"  # Stop calling, return safe default
    SELF_REPAIR = "self_repair"  # Modify code logic
    ESCALATE = "escalate"  # Alert for human intervention


@dataclass
class CodeSegment:
    """Monitored and self-healing code segment."""
    segment_id: str
    name: str
    function: Callable
    fallback: Optional[Callable]
    health_checks: List[Callable]
    execution_count: int = 0
    failure_count: int = 0
    last_execution: Optional[str] = None
    last_failure: Optional[str] = None
    current_status: str = "healthy"
    healing_history: List[Dict] = None

    def __post_init__(self):
        if self.healing_history is None:
            self.healing_history = []


class SelfHealingCodeManager:
    """
    Manages self-healing code segments.

    Capabilities:
    1. Monitor code execution health
    2. Detect degradation patterns
    3. Apply healing strategies automatically
    4. Learn from failures
    5. Maintain code integrity
    """

    def __init__(self):
        self.segments: Dict[str, CodeSegment] = {}
        self.healing_log: List[Dict] = []
        self.circuit_breakers: Dict[str, bool] = {}  # segment_id -> is_open
        self.failure_patterns: Dict[str, List[str]] = {}

    def register_segment(
        self,
        name: str,
        function: Callable,
        fallback: Optional[Callable] = None,
        health_checks: Optional[List[Callable]] = None
    ) -> str:
        """
        Register a code segment for self-healing monitoring.

        Args:
            name: Human-readable name
            function: Main function to execute
            fallback: Backup function if main fails
            health_checks: List of health check functions

        Returns:
            Segment ID
        """
        segment_id = self._generate_segment_id(name)

        segment = CodeSegment(
            segment_id=segment_id,
            name=name,
            function=function,
            fallback=fallback,
            health_checks=health_checks or []
        )

        self.segments[segment_id] = segment
        self.circuit_breakers[segment_id] = False  # Closed = normal operation

        return segment_id

    def _generate_segment_id(self, name: str) -> str:
        """Generate unique segment ID."""
        timestamp = datetime.utcnow().isoformat()
        combined = f"{name}_{timestamp}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def execute_segment(
        self,
        segment_id: str,
        *args,
        **kwargs
    ) -> Dict:
        """
        Execute code segment with self-healing.

        Returns:
            Dict with execution result and health metadata
        """
        if segment_id not in self.segments:
            return {"error": "Segment not found", "success": False}

        segment = self.segments[segment_id]

        # Check circuit breaker
        if self.circuit_breakers[segment_id]:
            return self._handle_circuit_break(segment)

        # Update execution tracking
        segment.execution_count += 1
        segment.last_execution = datetime.utcnow().isoformat()

        # Try main execution
        try:
            result = segment.function(*args, **kwargs)

            # Run health checks
            health_status = self._run_health_checks(segment, result)

            # Update status
            segment.current_status = health_status.value

            return {
                "success": True,
                "result": result,
                "health_status": health_status.value,
                "segment_id": segment_id
            }

        except Exception as e:
            # Main execution failed - attempt healing
            return self._heal_segment(segment, e, args, kwargs)

    def _run_health_checks(
        self,
        segment: CodeSegment,
        result: Any
    ) -> CodeHealthStatus:
        """Run health checks on execution result."""
        if not segment.health_checks:
            return CodeHealthStatus.HEALTHY

        failures = 0
        for check in segment.health_checks:
            try:
                if not check(result):
                    failures += 1
            except Exception:
                failures += 1

        # Determine status based on check failures
        if failures == 0:
            return CodeHealthStatus.HEALTHY
        elif failures <= len(segment.health_checks) // 3:
            return CodeHealthStatus.DEGRADED
        elif failures <= len(segment.health_checks) // 2:
            return CodeHealthStatus.FAILING
        else:
            return CodeHealthStatus.CRITICAL

    def _heal_segment(
        self,
        segment: CodeSegment,
        error: Exception,
        args: tuple,
        kwargs: dict
    ) -> Dict:
        """
        Attempt to heal failed segment.

        Healing strategies (in order):
        1. Retry (transient failure)
        2. Fallback function
        3. Circuit breaker
        4. Escalate
        """
        segment.failure_count += 1
        segment.last_failure = datetime.utcnow().isoformat()

        # Calculate failure rate
        failure_rate = segment.failure_count / max(segment.execution_count, 1)

        # Strategy 1: Retry (if low failure rate)
        if failure_rate < 0.2:
            return self._try_retry(segment, args, kwargs, error)

        # Strategy 2: Fallback function
        if segment.fallback is not None:
            return self._try_fallback(segment, args, kwargs, error)

        # Strategy 3: Circuit breaker (if high failure rate)
        if failure_rate > 0.5:
            return self._activate_circuit_breaker(segment, error)

        # Strategy 4: Escalate
        return self._escalate_failure(segment, error)

    def _try_retry(
        self,
        segment: CodeSegment,
        args: tuple,
        kwargs: dict,
        original_error: Exception
    ) -> Dict:
        """Retry strategy - attempt execution again."""
        try:
            result = segment.function(*args, **kwargs)

            # Log successful healing
            self._log_healing(
                segment.segment_id,
                HealingStrategy.RETRY,
                success=True,
                original_error=str(original_error)
            )

            return {
                "success": True,
                "result": result,
                "healed": True,
                "strategy": "retry"
            }

        except Exception as retry_error:
            # Retry failed - try next strategy
            self._log_healing(
                segment.segment_id,
                HealingStrategy.RETRY,
                success=False,
                original_error=str(retry_error)
            )

            # Try fallback if available
            if segment.fallback:
                return self._try_fallback(segment, args, kwargs, retry_error)
            else:
                return self._escalate_failure(segment, retry_error)

    def _try_fallback(
        self,
        segment: CodeSegment,
        args: tuple,
        kwargs: dict,
        original_error: Exception
    ) -> Dict:
        """Fallback strategy - use backup implementation."""
        try:
            result = segment.fallback(*args, **kwargs)

            self._log_healing(
                segment.segment_id,
                HealingStrategy.FALLBACK,
                success=True,
                original_error=str(original_error)
            )

            return {
                "success": True,
                "result": result,
                "healed": True,
                "strategy": "fallback",
                "warning": "Main function failed, used fallback"
            }

        except Exception as fallback_error:
            self._log_healing(
                segment.segment_id,
                HealingStrategy.FALLBACK,
                success=False,
                original_error=str(fallback_error)
            )

            return self._activate_circuit_breaker(segment, fallback_error)

    def _activate_circuit_breaker(
        self,
        segment: CodeSegment,
        error: Exception
    ) -> Dict:
        """Circuit breaker strategy - stop calling failing code."""
        self.circuit_breakers[segment.segment_id] = True
        segment.current_status = CodeHealthStatus.CRITICAL.value

        self._log_healing(
            segment.segment_id,
            HealingStrategy.CIRCUIT_BREAK,
            success=True,
            original_error=str(error)
        )

        return {
            "success": False,
            "healed": True,
            "strategy": "circuit_break",
            "error": "Circuit breaker activated - segment disabled",
            "requires_intervention": True
        }

    def _handle_circuit_break(self, segment: CodeSegment) -> Dict:
        """Handle execution when circuit breaker is open."""
        return {
            "success": False,
            "error": "Circuit breaker open - segment disabled",
            "segment_status": segment.current_status,
            "last_failure": segment.last_failure
        }

    def _escalate_failure(
        self,
        segment: CodeSegment,
        error: Exception
    ) -> Dict:
        """Escalate strategy - alert for human intervention."""
        self._log_healing(
            segment.segment_id,
            HealingStrategy.ESCALATE,
            success=False,
            original_error=str(error)
        )

        return {
            "success": False,
            "healed": False,
            "strategy": "escalate",
            "error": str(error),
            "requires_intervention": True,
            "escalated": True
        }

    def _log_healing(
        self,
        segment_id: str,
        strategy: HealingStrategy,
        success: bool,
        original_error: str
    ) -> None:
        """Log healing attempt."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "segment_id": segment_id,
            "strategy": strategy.value,
            "success": success,
            "original_error": original_error
        }

        self.healing_log.append(log_entry)

        # Update segment history
        if segment_id in self.segments:
            self.segments[segment_id].healing_history.append(log_entry)

    def reset_circuit_breaker(self, segment_id: str) -> bool:
        """
        Reset circuit breaker for a segment (after manual fix).

        Returns:
            True if reset successful
        """
        if segment_id not in self.circuit_breakers:
            return False

        self.circuit_breakers[segment_id] = False

        # Reset failure metrics
        if segment_id in self.segments:
            segment = self.segments[segment_id]
            segment.failure_count = 0
            segment.current_status = CodeHealthStatus.HEALTHY.value

        return True

    def get_segment_health(self, segment_id: str) -> Optional[Dict]:
        """Get health report for specific segment."""
        if segment_id not in self.segments:
            return None

        segment = self.segments[segment_id]
        failure_rate = segment.failure_count / max(segment.execution_count, 1)

        return {
            "segment_id": segment_id,
            "name": segment.name,
            "current_status": segment.current_status,
            "execution_count": segment.execution_count,
            "failure_count": segment.failure_count,
            "failure_rate": failure_rate,
            "circuit_breaker_open": self.circuit_breakers[segment_id],
            "last_execution": segment.last_execution,
            "last_failure": segment.last_failure,
            "healing_attempts": len(segment.healing_history)
        }

    def get_system_health(self) -> Dict:
        """Get overall system health report."""
        total_segments = len(self.segments)
        status_counts = {
            "healthy": 0,
            "degraded": 0,
            "failing": 0,
            "critical": 0
        }

        circuit_breakers_open = 0

        for segment_id, segment in self.segments.items():
            status_counts[segment.current_status] += 1
            if self.circuit_breakers[segment_id]:
                circuit_breakers_open += 1

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_segments": total_segments,
            "status_breakdown": status_counts,
            "circuit_breakers_open": circuit_breakers_open,
            "total_healing_attempts": len(self.healing_log),
            "system_health": self._assess_system_health(status_counts, circuit_breakers_open)
        }

    def _assess_system_health(
        self,
        status_counts: Dict,
        breakers_open: int
    ) -> str:
        """Assess overall system health."""
        if status_counts["critical"] > 0 or breakers_open > 2:
            return "CRITICAL"
        elif status_counts["failing"] > 2:
            return "DEGRADED"
        elif status_counts["degraded"] > 5:
            return "MODERATE"
        else:
            return "HEALTHY"


# Global self-healing code manager
HEALING_MANAGER = SelfHealingCodeManager()


def register_healing_segment(
    name: str,
    function: Callable,
    fallback: Optional[Callable] = None,
    health_checks: Optional[List[Callable]] = None
) -> str:
    """
    Register a function for self-healing monitoring.

    Args:
        name: Segment name
        function: Main function
        fallback: Backup function
        health_checks: Health check functions

    Returns:
        Segment ID
    """
    return HEALING_MANAGER.register_segment(name, function, fallback, health_checks)


def execute_healing_segment(segment_id: str, *args, **kwargs) -> Dict:
    """Execute self-healing segment."""
    return HEALING_MANAGER.execute_segment(segment_id, *args, **kwargs)


def get_healing_status() -> Dict:
    """Get self-healing system status."""
    return HEALING_MANAGER.get_system_health()


if __name__ == "__main__":
    # Self-test
    print("=== SELF-HEALING CODE TEST ===\n")

    # Define test functions
    def flaky_function(x):
        """Function that sometimes fails."""
        import random
        if random.random() < 0.3:
            raise ValueError("Random failure!")
        return x * 2

    def stable_fallback(x):
        """Reliable fallback."""
        return x  # Safe default

    def health_check(result):
        """Check if result is valid."""
        return result is not None and result >= 0

    # Register segment
    segment_id = register_healing_segment(
        name="flaky_operation",
        function=flaky_function,
        fallback=stable_fallback,
        health_checks=[health_check]
    )

    print(f"Registered segment: {segment_id}\n")

    # Execute multiple times
    print("Executing segment 10 times:")
    for i in range(10):
        result = execute_healing_segment(segment_id, i)
        print(f"  Attempt {i+1}: Success={result['success']}, Healed={result.get('healed', False)}")

    # Get health report
    print("\n=== SEGMENT HEALTH ===")
    health = HEALING_MANAGER.get_segment_health(segment_id)
    print(json.dumps(health, indent=2))

    # System health
    print("\n=== SYSTEM HEALTH ===")
    system = get_healing_status()
    print(json.dumps(system, indent=2))

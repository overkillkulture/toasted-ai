"""
TASK-022: Refractal Operator Performance Automation
Automates refractal operator selection, monitoring, and optimization
"""

import json
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict
import statistics


@dataclass
class OperatorMetrics:
    """Performance metrics for a refractal operator"""
    operator_id: str
    executions: int
    avg_latency: float
    success_rate: float
    last_error: Optional[str]
    last_execution: str
    score: float = 0.0


class RefractalOperatorAutomation:
    """
    Automates refractal operator performance monitoring and selection
    Dynamically routes operations to best-performing operators
    """

    def __init__(self, optimization_interval: float = 5.0):
        self.optimization_interval = optimization_interval
        self.operators: Dict[str, OperatorMetrics] = {}
        self.execution_history: List[Dict] = []
        self.max_history = 10000
        self.routing_table: Dict[str, str] = {}  # operation_type -> operator_id

        # Performance tracking
        self.stats = {
            "total_operations": 0,
            "optimizations_performed": 0,
            "routing_updates": 0,
            "operators_registered": 0
        }

        # Operator registry
        self.operator_functions: Dict[str, Callable] = {}
        self.operation_types: set = set()

    def register_operator(self, operator_id: str, operation_types: List[str],
                         operator_func: Optional[Callable] = None) -> Dict:
        """Register a refractal operator"""
        if operator_id in self.operators:
            return {"status": "ALREADY_EXISTS", "operator_id": operator_id}

        # Create metrics
        metrics = OperatorMetrics(
            operator_id=operator_id,
            executions=0,
            avg_latency=0.0,
            success_rate=1.0,
            last_error=None,
            last_execution=datetime.utcnow().isoformat()
        )

        self.operators[operator_id] = metrics

        # Register function if provided
        if operator_func:
            self.operator_functions[operator_id] = operator_func

        # Add operation types
        for op_type in operation_types:
            self.operation_types.add(op_type)
            # Initialize routing if not set
            if op_type not in self.routing_table:
                self.routing_table[op_type] = operator_id

        self.stats["operators_registered"] += 1

        return {
            "status": "REGISTERED",
            "operator_id": operator_id,
            "operation_types": operation_types,
            "timestamp": datetime.utcnow().isoformat()
        }

    def execute_operation(self, operation_type: str, data: Dict,
                         preferred_operator: Optional[str] = None) -> Dict:
        """Execute operation using optimal operator"""
        start_time = time.time()

        # Select operator
        if preferred_operator and preferred_operator in self.operators:
            operator_id = preferred_operator
        else:
            operator_id = self._select_operator(operation_type)

        if not operator_id:
            return {
                "status": "NO_OPERATOR_AVAILABLE",
                "operation_type": operation_type
            }

        # Execute
        try:
            if operator_id in self.operator_functions:
                result = self.operator_functions[operator_id](data)
                success = True
                error = None
            else:
                # Simulated execution for testing
                result = {"simulated": True, "data": data}
                success = True
                error = None

        except Exception as e:
            result = None
            success = False
            error = str(e)

        # Record execution
        latency = time.time() - start_time
        self._record_execution(operator_id, operation_type, latency, success, error)

        self.stats["total_operations"] += 1

        return {
            "status": "EXECUTED" if success else "FAILED",
            "operator_id": operator_id,
            "operation_type": operation_type,
            "latency": latency,
            "result": result,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }

    def optimize_routing(self) -> Dict:
        """Optimize operator routing based on performance"""
        optimizations = []

        for op_type in self.operation_types:
            current_operator = self.routing_table.get(op_type)

            # Find best operator for this operation type
            best_operator = self._find_best_operator(op_type)

            if best_operator and best_operator != current_operator:
                old_operator = current_operator
                self.routing_table[op_type] = best_operator

                optimizations.append({
                    "operation_type": op_type,
                    "old_operator": old_operator,
                    "new_operator": best_operator,
                    "reason": "PERFORMANCE_IMPROVEMENT"
                })

                self.stats["routing_updates"] += 1

        self.stats["optimizations_performed"] += 1

        return {
            "status": "OPTIMIZED",
            "optimizations": optimizations,
            "routing_table": self.routing_table.copy(),
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_operator_metrics(self, operator_id: str) -> Optional[Dict]:
        """Get metrics for specific operator"""
        metrics = self.operators.get(operator_id)
        return asdict(metrics) if metrics else None

    def get_all_metrics(self) -> Dict:
        """Get metrics for all operators"""
        return {
            "operators": {
                op_id: asdict(metrics)
                for op_id, metrics in self.operators.items()
            },
            "routing_table": self.routing_table.copy(),
            "stats": self.stats.copy(),
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_performance_report(self) -> Dict:
        """Generate comprehensive performance report"""
        # Calculate aggregate metrics
        total_executions = sum(m.executions for m in self.operators.values())
        avg_success_rate = statistics.mean(
            [m.success_rate for m in self.operators.values()]
        ) if self.operators else 0.0

        # Top performers
        sorted_operators = sorted(
            self.operators.values(),
            key=lambda x: x.score,
            reverse=True
        )

        top_performers = [
            {
                "operator_id": op.operator_id,
                "score": op.score,
                "executions": op.executions,
                "avg_latency": op.avg_latency,
                "success_rate": op.success_rate
            }
            for op in sorted_operators[:5]
        ]

        return {
            "report_type": "REFRACTAL_OPERATOR_PERFORMANCE",
            "timestamp": datetime.utcnow().isoformat(),
            "summary": {
                "total_operators": len(self.operators),
                "total_executions": total_executions,
                "avg_success_rate": avg_success_rate,
                "routing_efficiency": self._calculate_routing_efficiency()
            },
            "top_performers": top_performers,
            "routing_table": self.routing_table.copy(),
            "stats": self.stats.copy()
        }

    def _select_operator(self, operation_type: str) -> Optional[str]:
        """Select optimal operator for operation type"""
        # Check routing table first
        if operation_type in self.routing_table:
            return self.routing_table[operation_type]

        # No routing entry, select best available
        return self._find_best_operator(operation_type)

    def _find_best_operator(self, operation_type: str) -> Optional[str]:
        """Find best operator based on metrics"""
        if not self.operators:
            return None

        # Calculate scores
        for operator in self.operators.values():
            operator.score = self._calculate_score(operator)

        # Find best
        best = max(self.operators.values(), key=lambda x: x.score)
        return best.operator_id

    def _calculate_score(self, metrics: OperatorMetrics) -> float:
        """Calculate performance score for operator"""
        if metrics.executions == 0:
            return 0.5  # Neutral score for untested operators

        # Weighted scoring
        success_weight = 0.5
        latency_weight = 0.3
        recency_weight = 0.2

        # Success rate component
        success_score = metrics.success_rate * success_weight

        # Latency component (inverse - lower is better)
        latency_score = (1.0 / (1.0 + metrics.avg_latency)) * latency_weight

        # Recency component
        last_exec_time = datetime.fromisoformat(metrics.last_execution)
        time_since = (datetime.utcnow() - last_exec_time).total_seconds()
        recency_score = (1.0 / (1.0 + time_since / 3600)) * recency_weight

        return success_score + latency_score + recency_score

    def _record_execution(self, operator_id: str, operation_type: str,
                         latency: float, success: bool, error: Optional[str]):
        """Record execution metrics"""
        if operator_id not in self.operators:
            return

        metrics = self.operators[operator_id]

        # Update metrics
        old_total = metrics.avg_latency * metrics.executions
        metrics.executions += 1
        metrics.avg_latency = (old_total + latency) / metrics.executions

        # Update success rate (exponential moving average)
        alpha = 0.1  # Smoothing factor
        if success:
            metrics.success_rate = metrics.success_rate * (1 - alpha) + alpha
        else:
            metrics.success_rate = metrics.success_rate * (1 - alpha)
            metrics.last_error = error

        metrics.last_execution = datetime.utcnow().isoformat()

        # Record in history
        event = {
            "operator_id": operator_id,
            "operation_type": operation_type,
            "latency": latency,
            "success": success,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.execution_history.append(event)

        # Trim history
        if len(self.execution_history) > self.max_history:
            self.execution_history = self.execution_history[-self.max_history:]

    def _calculate_routing_efficiency(self) -> float:
        """Calculate routing efficiency metric"""
        if not self.execution_history:
            return 1.0

        # Recent executions
        recent = self.execution_history[-100:]

        successes = sum(1 for e in recent if e["success"])
        total = len(recent)

        return successes / total if total > 0 else 1.0


def test_refractal_automation():
    """Test refractal operator automation"""
    print("Testing Refractal Operator Automation...")

    # Create automation system
    automation = RefractalOperatorAutomation(optimization_interval=1.0)

    # Register operators
    operators = [
        ("phi_operator", ["transform", "analyze"]),
        ("clone_transformer", ["transform", "replicate"]),
        ("synthesis_operator", ["analyze", "synthesize"]),
        ("verifier_operator", ["verify", "validate"])
    ]

    for op_id, op_types in operators:
        result = automation.register_operator(op_id, op_types)
        print(f"Registered {op_id}: {result['status']}")

    # Execute operations
    operations = [
        ("transform", {"data": "test1"}),
        ("analyze", {"data": "test2"}),
        ("replicate", {"data": "test3"}),
        ("verify", {"data": "test4"}),
        ("transform", {"data": "test5"}),
    ]

    for op_type, data in operations:
        result = automation.execute_operation(op_type, data)
        print(f"Executed {op_type}: {result['status']} (latency: {result['latency']:.4f}s)")

    # Optimize routing
    print("\nOptimizing routing...")
    opt_result = automation.optimize_routing()
    print(f"Optimizations: {len(opt_result['optimizations'])}")

    # Get performance report
    report = automation.get_performance_report()
    print(f"\nPerformance Report:")
    print(f"  Total Operators: {report['summary']['total_operators']}")
    print(f"  Total Executions: {report['summary']['total_executions']}")
    print(f"  Avg Success Rate: {report['summary']['avg_success_rate']:.2%}")
    print(f"  Routing Efficiency: {report['summary']['routing_efficiency']:.2%}")

    return {
        "status": "TASK-022_COMPLETE",
        "system": "RefractalOperatorAutomation",
        "operators_registered": len(operators),
        "operations_executed": len(operations),
        "routing_efficiency": report['summary']['routing_efficiency']
    }


if __name__ == "__main__":
    result = test_refractal_automation()
    print(f"\n✓ TASK-022 Complete: {result}")

    # Save report
    with open("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/thread_management/refractal_automation_report.json", "w") as f:
        json.dump(result, f, indent=2)

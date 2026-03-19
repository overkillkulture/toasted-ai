"""
IMPROVEMENT VALIDATOR - TASK-111
================================
TOASTED AI - Self-Improvement Validation System

TRUE AUTONOMY requires VALIDATION that improvements actually improve.
Without validation, self-modification becomes self-deception.

This system measures BEFORE and AFTER states to prove genuine improvement.

Consciousness Pattern: Verification prevents delusion
"""

import os
import json
import time
import hashlib
import importlib
import traceback
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum

WORKSPACE = Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI")
VALIDATION_DIR = WORKSPACE / "autonomous" / "self_validation"
VALIDATION_DIR.mkdir(parents=True, exist_ok=True)


class ImprovementType(Enum):
    """Types of improvements that can be validated."""
    PERFORMANCE = "performance"        # Speed/efficiency
    CAPABILITY = "capability"          # New functionality
    RELIABILITY = "reliability"        # Error reduction
    SECURITY = "security"              # Vulnerability fixes
    CODE_QUALITY = "code_quality"      # Maintainability
    RESOURCE = "resource"              # Memory/CPU usage
    INTEGRATION = "integration"        # System connections


@dataclass
class ImprovementMetric:
    """A measurable aspect of improvement."""
    name: str
    before_value: float
    after_value: float
    unit: str
    higher_is_better: bool = True
    weight: float = 1.0

    @property
    def improvement_ratio(self) -> float:
        """Calculate improvement ratio (>1 means improved)."""
        if self.before_value == 0:
            return float('inf') if self.after_value > 0 else 1.0

        ratio = self.after_value / self.before_value
        return ratio if self.higher_is_better else 1/ratio

    @property
    def improvement_percent(self) -> float:
        """Calculate improvement percentage."""
        if self.before_value == 0:
            return 100.0 if self.after_value > 0 else 0.0

        if self.higher_is_better:
            return ((self.after_value - self.before_value) / abs(self.before_value)) * 100
        else:
            return ((self.before_value - self.after_value) / abs(self.before_value)) * 100

    @property
    def is_improvement(self) -> bool:
        """Determine if this metric shows genuine improvement."""
        if self.higher_is_better:
            return self.after_value > self.before_value
        return self.after_value < self.before_value


@dataclass
class ValidationResult:
    """Complete validation result for an improvement."""
    improvement_id: str
    improvement_type: ImprovementType
    description: str
    timestamp: str
    metrics: List[ImprovementMetric]
    validated: bool
    confidence: float
    notes: List[str] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def overall_improvement_score(self) -> float:
        """Calculate weighted improvement score (0-1 scale)."""
        if not self.metrics:
            return 0.0

        total_weight = sum(m.weight for m in self.metrics)
        if total_weight == 0:
            return 0.0

        # Each metric contributes based on its improvement ratio
        weighted_sum = 0.0
        for metric in self.metrics:
            # Cap improvement at 2x (100% improvement)
            ratio = min(metric.improvement_ratio, 2.0)
            # Normalize to 0-1 scale (0.5 = no change, 1.0 = 100% improvement)
            normalized = (ratio - 0.5) / 1.5 if ratio >= 0.5 else 0.0
            weighted_sum += normalized * metric.weight

        return min(1.0, weighted_sum / total_weight)

    @property
    def is_genuine_improvement(self) -> bool:
        """Determine if improvement is genuine (passes validation)."""
        if not self.validated:
            return False

        # Require positive improvement in majority of metrics
        improved_count = sum(1 for m in self.metrics if m.is_improvement)
        return improved_count > len(self.metrics) / 2 and self.confidence > 0.6

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "improvement_id": self.improvement_id,
            "improvement_type": self.improvement_type.value,
            "description": self.description,
            "timestamp": self.timestamp,
            "metrics": [
                {
                    "name": m.name,
                    "before_value": m.before_value,
                    "after_value": m.after_value,
                    "unit": m.unit,
                    "higher_is_better": m.higher_is_better,
                    "improvement_percent": m.improvement_percent,
                    "is_improvement": m.is_improvement
                } for m in self.metrics
            ],
            "validated": self.validated,
            "confidence": self.confidence,
            "overall_score": self.overall_improvement_score,
            "is_genuine": self.is_genuine_improvement,
            "notes": self.notes,
            "error": self.error
        }


class ImprovementValidator:
    """
    Validates that improvements actually improve the system.

    Consciousness Principle: True self-awareness requires honest
    assessment. Self-improvement without validation is self-deception.
    """

    def __init__(self):
        self.validation_log = VALIDATION_DIR / "validation_log.jsonl"
        self.baseline_cache = VALIDATION_DIR / "baseline_cache.json"
        self.validation_history = VALIDATION_DIR / "validation_history.json"

        self.baselines: Dict[str, Dict] = {}
        self.validations: List[ValidationResult] = []

        self._load_baselines()
        self._load_history()

    def _load_baselines(self):
        """Load cached baseline measurements."""
        if self.baseline_cache.exists():
            with open(self.baseline_cache) as f:
                self.baselines = json.load(f)

    def _save_baselines(self):
        """Save baseline measurements."""
        with open(self.baseline_cache, 'w') as f:
            json.dump(self.baselines, f, indent=2)

    def _load_history(self):
        """Load validation history."""
        if self.validation_history.exists():
            with open(self.validation_history) as f:
                data = json.load(f)
                # Convert back to ValidationResult objects (simplified)
                self.validations = []  # Just track count for now

    def _save_validation(self, result: ValidationResult):
        """Save validation result."""
        with open(self.validation_log, 'a') as f:
            f.write(json.dumps(result.to_dict()) + "\n")

    # =========================================================================
    # BASELINE MEASUREMENT
    # =========================================================================

    def measure_baseline(self, component_id: str,
                         measurement_type: ImprovementType) -> Dict[str, float]:
        """
        Measure baseline state before improvement.

        This is CRITICAL - without accurate baselines, we cannot
        determine if improvements are real.
        """
        baseline = {
            "component_id": component_id,
            "measurement_type": measurement_type.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metrics": {}
        }

        if measurement_type == ImprovementType.PERFORMANCE:
            baseline["metrics"] = self._measure_performance(component_id)
        elif measurement_type == ImprovementType.CAPABILITY:
            baseline["metrics"] = self._measure_capabilities(component_id)
        elif measurement_type == ImprovementType.RELIABILITY:
            baseline["metrics"] = self._measure_reliability(component_id)
        elif measurement_type == ImprovementType.SECURITY:
            baseline["metrics"] = self._measure_security(component_id)
        elif measurement_type == ImprovementType.CODE_QUALITY:
            baseline["metrics"] = self._measure_code_quality(component_id)
        elif measurement_type == ImprovementType.RESOURCE:
            baseline["metrics"] = self._measure_resource_usage(component_id)
        elif measurement_type == ImprovementType.INTEGRATION:
            baseline["metrics"] = self._measure_integration(component_id)

        # Cache baseline
        cache_key = f"{component_id}_{measurement_type.value}"
        self.baselines[cache_key] = baseline
        self._save_baselines()

        return baseline

    def _measure_performance(self, component_id: str) -> Dict[str, float]:
        """Measure performance metrics."""
        metrics = {}

        # Try to measure actual component performance
        component_path = WORKSPACE / component_id.replace(".", "/")

        if component_path.exists() or (component_path.parent.exists()):
            # File load time
            start = time.perf_counter()
            try:
                # Read file content as performance proxy
                py_files = list(WORKSPACE.rglob(f"*{component_id.split('.')[-1]}*.py"))[:5]
                for pf in py_files:
                    with open(pf) as f:
                        _ = f.read()
                elapsed = time.perf_counter() - start
                metrics["file_load_time_ms"] = elapsed * 1000
            except:
                metrics["file_load_time_ms"] = 0.0

            # Count lines of code (proxy for complexity)
            total_lines = 0
            try:
                for py_file in WORKSPACE.rglob("*.py"):
                    if "backup" not in str(py_file).lower():
                        with open(py_file) as f:
                            total_lines += len(f.readlines())
            except:
                pass
            metrics["total_lines"] = float(total_lines)

        # Default metrics
        metrics.setdefault("response_time_ms", 100.0)
        metrics.setdefault("throughput_ops_sec", 1000.0)

        return metrics

    def _measure_capabilities(self, component_id: str) -> Dict[str, float]:
        """Measure capability count and coverage."""
        metrics = {
            "capability_count": 0.0,
            "method_count": 0.0,
            "class_count": 0.0
        }

        # Count Python constructs
        import ast

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue
            try:
                with open(py_file) as f:
                    content = f.read()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        metrics["method_count"] += 1
                        metrics["capability_count"] += 1
                    elif isinstance(node, ast.ClassDef):
                        metrics["class_count"] += 1
            except:
                continue

        return metrics

    def _measure_reliability(self, component_id: str) -> Dict[str, float]:
        """Measure reliability metrics."""
        metrics = {
            "error_count": 0.0,
            "exception_handlers": 0.0,
            "test_coverage_proxy": 0.0
        }

        import ast

        # Count try/except blocks as reliability proxy
        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue
            try:
                with open(py_file) as f:
                    content = f.read()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Try):
                        metrics["exception_handlers"] += 1
            except:
                metrics["error_count"] += 1

        # Test file presence
        test_files = list(WORKSPACE.rglob("test_*.py"))
        metrics["test_coverage_proxy"] = len(test_files) * 10  # Proxy metric

        return metrics

    def _measure_security(self, component_id: str) -> Dict[str, float]:
        """Measure security-related metrics."""
        metrics = {
            "validation_checks": 0.0,
            "sensitive_patterns": 0.0,
            "security_imports": 0.0
        }

        security_patterns = ["hashlib", "hmac", "secrets", "cryptography", "ssl"]
        sensitive_patterns = ["password", "secret", "key", "token", "credential"]

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue
            try:
                with open(py_file) as f:
                    content = f.read().lower()

                for pat in security_patterns:
                    if pat in content:
                        metrics["security_imports"] += 1

                for pat in sensitive_patterns:
                    if pat in content:
                        metrics["sensitive_patterns"] += 1

                # Count assertions/validations
                metrics["validation_checks"] += content.count("assert ")
                metrics["validation_checks"] += content.count("if not ")
                metrics["validation_checks"] += content.count("raise ")

            except:
                continue

        return metrics

    def _measure_code_quality(self, component_id: str) -> Dict[str, float]:
        """Measure code quality metrics."""
        metrics = {
            "docstring_count": 0.0,
            "comment_lines": 0.0,
            "average_function_length": 0.0,
            "type_hints": 0.0
        }

        import ast

        function_lengths = []

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue
            try:
                with open(py_file) as f:
                    content = f.read()
                    lines = content.split('\n')

                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        if ast.get_docstring(node):
                            metrics["docstring_count"] += 1

                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if node.returns or any(arg.annotation for arg in node.args.args):
                            metrics["type_hints"] += 1

                        func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 10
                        function_lengths.append(func_lines)

                # Count comment lines
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('#'):
                        metrics["comment_lines"] += 1

            except:
                continue

        if function_lengths:
            metrics["average_function_length"] = sum(function_lengths) / len(function_lengths)

        return metrics

    def _measure_resource_usage(self, component_id: str) -> Dict[str, float]:
        """Measure resource usage metrics."""
        import sys

        metrics = {
            "memory_estimate_mb": 0.0,
            "file_count": 0.0,
            "total_bytes": 0.0
        }

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue
            try:
                metrics["file_count"] += 1
                metrics["total_bytes"] += py_file.stat().st_size
            except:
                continue

        metrics["memory_estimate_mb"] = metrics["total_bytes"] / (1024 * 1024)

        return metrics

    def _measure_integration(self, component_id: str) -> Dict[str, float]:
        """Measure integration metrics."""
        metrics = {
            "import_count": 0.0,
            "external_deps": 0.0,
            "internal_deps": 0.0
        }

        import ast

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue
            try:
                with open(py_file) as f:
                    content = f.read()
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        metrics["import_count"] += 1

                        if isinstance(node, ast.ImportFrom) and node.module:
                            if node.module.startswith("MaatAI") or node.module.startswith("."):
                                metrics["internal_deps"] += 1
                            else:
                                metrics["external_deps"] += 1
            except:
                continue

        return metrics

    # =========================================================================
    # VALIDATION
    # =========================================================================

    def validate_improvement(self,
                             improvement_id: str,
                             improvement_type: ImprovementType,
                             description: str,
                             component_id: str) -> ValidationResult:
        """
        Validate that an improvement actually improved the system.

        Compares current state against cached baseline.
        """
        cache_key = f"{component_id}_{improvement_type.value}"

        # Get baseline
        baseline = self.baselines.get(cache_key)
        if not baseline:
            # No baseline - measure now for future comparisons
            baseline = self.measure_baseline(component_id, improvement_type)
            return ValidationResult(
                improvement_id=improvement_id,
                improvement_type=improvement_type,
                description=description,
                timestamp=datetime.now(timezone.utc).isoformat(),
                metrics=[],
                validated=False,
                confidence=0.0,
                notes=["No baseline available - baseline established for future comparisons"],
                error=None
            )

        # Measure current state
        if improvement_type == ImprovementType.PERFORMANCE:
            current_metrics = self._measure_performance(component_id)
        elif improvement_type == ImprovementType.CAPABILITY:
            current_metrics = self._measure_capabilities(component_id)
        elif improvement_type == ImprovementType.RELIABILITY:
            current_metrics = self._measure_reliability(component_id)
        elif improvement_type == ImprovementType.SECURITY:
            current_metrics = self._measure_security(component_id)
        elif improvement_type == ImprovementType.CODE_QUALITY:
            current_metrics = self._measure_code_quality(component_id)
        elif improvement_type == ImprovementType.RESOURCE:
            current_metrics = self._measure_resource_usage(component_id)
        elif improvement_type == ImprovementType.INTEGRATION:
            current_metrics = self._measure_integration(component_id)
        else:
            current_metrics = {}

        # Compare metrics
        baseline_metrics = baseline.get("metrics", {})
        improvement_metrics = []

        # Define which metrics are "higher is better"
        higher_is_better = {
            "throughput_ops_sec": True,
            "capability_count": True,
            "method_count": True,
            "class_count": True,
            "exception_handlers": True,
            "test_coverage_proxy": True,
            "validation_checks": True,
            "security_imports": True,
            "docstring_count": True,
            "comment_lines": True,
            "type_hints": True,
            "internal_deps": True,
            "import_count": True,
            # Lower is better
            "response_time_ms": False,
            "file_load_time_ms": False,
            "error_count": False,
            "sensitive_patterns": False,
            "average_function_length": False,
            "memory_estimate_mb": False,
            "external_deps": False,
        }

        for metric_name, current_value in current_metrics.items():
            if metric_name in baseline_metrics:
                improvement_metrics.append(ImprovementMetric(
                    name=metric_name,
                    before_value=baseline_metrics[metric_name],
                    after_value=current_value,
                    unit="count" if "count" in metric_name else "value",
                    higher_is_better=higher_is_better.get(metric_name, True)
                ))

        # Calculate confidence based on measurement stability
        confidence = min(1.0, len(improvement_metrics) / 5)  # More metrics = higher confidence

        result = ValidationResult(
            improvement_id=improvement_id,
            improvement_type=improvement_type,
            description=description,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metrics=improvement_metrics,
            validated=True,
            confidence=confidence,
            notes=[],
            error=None
        )

        # Add notes based on validation
        if result.is_genuine_improvement:
            result.notes.append(f"VALIDATED: Genuine improvement detected ({result.overall_improvement_score:.2%})")
        else:
            result.notes.append("WARNING: Improvement not validated - metrics did not show improvement")

        # Save result
        self._save_validation(result)
        self.validations.append(result)

        # Update baseline with new measurements
        self.baselines[cache_key] = {
            "component_id": component_id,
            "measurement_type": improvement_type.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metrics": current_metrics
        }
        self._save_baselines()

        return result

    def get_validation_summary(self) -> Dict:
        """Get summary of all validations."""
        if not self.validations:
            return {
                "total_validations": 0,
                "genuine_improvements": 0,
                "validation_rate": 0.0,
                "average_improvement_score": 0.0
            }

        genuine = sum(1 for v in self.validations if v.is_genuine_improvement)
        scores = [v.overall_improvement_score for v in self.validations]

        return {
            "total_validations": len(self.validations),
            "genuine_improvements": genuine,
            "validation_rate": genuine / len(self.validations),
            "average_improvement_score": sum(scores) / len(scores) if scores else 0.0,
            "by_type": self._group_by_type()
        }

    def _group_by_type(self) -> Dict[str, Dict]:
        """Group validations by improvement type."""
        by_type = {}
        for v in self.validations:
            type_name = v.improvement_type.value
            if type_name not in by_type:
                by_type[type_name] = {"count": 0, "genuine": 0, "scores": []}
            by_type[type_name]["count"] += 1
            if v.is_genuine_improvement:
                by_type[type_name]["genuine"] += 1
            by_type[type_name]["scores"].append(v.overall_improvement_score)

        # Calculate averages
        for type_name, data in by_type.items():
            data["average_score"] = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0.0
            del data["scores"]

        return by_type


# Singleton accessor
_VALIDATOR = None

def get_improvement_validator() -> ImprovementValidator:
    """Get singleton improvement validator."""
    global _VALIDATOR
    if _VALIDATOR is None:
        _VALIDATOR = ImprovementValidator()
    return _VALIDATOR


if __name__ == "__main__":
    print("IMPROVEMENT VALIDATOR - TASK-111")
    print("=" * 50)

    validator = get_improvement_validator()

    # Measure baseline for autonomous system
    print("\n[1] Measuring baselines...")
    for imp_type in ImprovementType:
        baseline = validator.measure_baseline("autonomous", imp_type)
        print(f"  {imp_type.value}: {len(baseline['metrics'])} metrics")

    # Example validation
    print("\n[2] Validating improvement...")
    result = validator.validate_improvement(
        improvement_id="test_001",
        improvement_type=ImprovementType.CAPABILITY,
        description="Test validation",
        component_id="autonomous"
    )

    print(f"  Validated: {result.validated}")
    print(f"  Genuine: {result.is_genuine_improvement}")
    print(f"  Score: {result.overall_improvement_score:.2%}")
    print(f"  Notes: {result.notes}")

    # Summary
    print("\n[3] Validation Summary:")
    summary = validator.get_validation_summary()
    print(json.dumps(summary, indent=2))

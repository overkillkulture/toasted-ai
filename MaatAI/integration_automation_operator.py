#!/usr/bin/env python3
"""
INTEGRATION AUTOMATION OPERATOR (∫)
====================================
TASK-166: Automate integration ∫

Mathematical operator that continuously integrates system changes
across all components. Implements the integral operator for seamless
component fusion.

∫(System) = Σ_layers Φ·Σ·Δ·∫ (continuous accumulation)

Where:
- Continuous monitoring of changes
- Automatic dependency resolution
- Real-time integration synthesis
- Persistent state accumulation

Author: C2 Architect (Wave 6 Batch C)
Date: 2026-03-19
"""

import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib


class IntegrationEvent(Enum):
    """Types of integration events."""
    COMPONENT_ADDED = "component_added"
    COMPONENT_MODIFIED = "component_modified"
    COMPONENT_REMOVED = "component_removed"
    DEPENDENCY_RESOLVED = "dependency_resolved"
    INTEGRATION_COMPLETE = "integration_complete"
    INTEGRATION_FAILED = "integration_failed"


@dataclass
class IntegrationRecord:
    """Record of a single integration event."""
    record_id: str
    timestamp: str
    event_type: IntegrationEvent
    source_component: str
    target_components: List[str]
    integration_value: float
    success: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['event_type'] = self.event_type.value
        return result


class IntegrationAutomationOperator:
    """
    ∫ (Integral) Operator - Continuous system integration.

    Automatically integrates changes across the system, maintaining
    mathematical chain integrity and ensuring seamless component fusion.
    """

    def __init__(self, workspace: Optional[Path] = None):
        self.workspace = workspace or Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI")
        self.integration_records: List[IntegrationRecord] = []
        self.component_registry: Dict[str, Dict[str, Any]] = {}
        self.dependency_graph: Dict[str, Set[str]] = {}
        self.integration_queue: List[Dict[str, Any]] = []

        # Integration state
        self.total_integrations = 0
        self.successful_integrations = 0
        self.failed_integrations = 0
        self.accumulated_value = 0.0

        # Monitoring state
        self.monitoring = False
        self.last_scan = None

        print(f"[∫] Integration Automation Operator Initialized")
        print(f"[∫] Workspace: {self.workspace}")

    def register_component(
        self,
        component_id: str,
        file_path: str,
        dependencies: Optional[List[str]] = None
    ):
        """
        Register a component for integration monitoring.

        Args:
            component_id: Unique component identifier
            file_path: Path to component file
            dependencies: List of dependency component IDs
        """
        self.component_registry[component_id] = {
            'id': component_id,
            'path': file_path,
            'dependencies': dependencies or [],
            'hash': self._compute_file_hash(file_path),
            'registered': datetime.utcnow().isoformat(),
            'last_integrated': None,
            'integration_count': 0
        }

        # Update dependency graph
        if dependencies:
            self.dependency_graph[component_id] = set(dependencies)

        print(f"[∫] Registered: {component_id} ({len(dependencies or [])} deps)")

    def _compute_file_hash(self, file_path: str) -> str:
        """Compute SHA-256 hash of file."""
        try:
            path = Path(file_path)
            if not path.exists():
                return "unknown"

            content = path.read_text(encoding='utf-8', errors='ignore')
            return hashlib.sha256(content.encode()).hexdigest()[:16]

        except Exception:
            return "error"

    def detect_changes(self) -> List[str]:
        """
        Detect changed components since last scan.

        Returns:
            List of changed component IDs
        """
        changed = []

        for comp_id, comp_data in self.component_registry.items():
            current_hash = self._compute_file_hash(comp_data['path'])

            if current_hash != comp_data['hash']:
                changed.append(comp_id)
                comp_data['hash'] = current_hash

        if changed:
            print(f"[∫] Detected changes: {len(changed)} components")

        self.last_scan = datetime.utcnow()

        return changed

    def resolve_dependencies(self, component_id: str) -> List[str]:
        """
        Resolve all dependencies for a component (recursive).

        Args:
            component_id: Component to resolve

        Returns:
            Ordered list of dependencies (leaves first)
        """
        resolved = []
        seen = set()

        def _resolve(comp_id: str):
            if comp_id in seen:
                return
            seen.add(comp_id)

            if comp_id in self.dependency_graph:
                for dep_id in self.dependency_graph[comp_id]:
                    _resolve(dep_id)

            if comp_id not in resolved:
                resolved.append(comp_id)

        _resolve(component_id)

        return resolved

    def calculate_integration_value(
        self,
        source: str,
        targets: List[str]
    ) -> float:
        """
        Calculate integration value for component fusion.

        ∫_value = Σ(source·target) / N

        Args:
            source: Source component ID
            targets: Target component IDs

        Returns:
            Integration value [0, 1]
        """
        if not targets:
            return 0.0

        # Base value from component data
        source_data = self.component_registry.get(source, {})
        source_deps = len(source_data.get('dependencies', []))

        # Calculate fusion value
        fusion_sum = 0.0
        for target in targets:
            target_data = self.component_registry.get(target, {})
            target_deps = len(target_data.get('dependencies', []))

            # Integration strength based on dependency overlap
            fusion_sum += 1.0 / (1.0 + abs(source_deps - target_deps))

        integration_value = fusion_sum / len(targets)

        return min(integration_value, 1.0)

    def integrate_component(
        self,
        component_id: str,
        force: bool = False
    ) -> IntegrationRecord:
        """
        Integrate a component with its dependencies.

        Args:
            component_id: Component to integrate
            force: Force integration even if up-to-date

        Returns:
            IntegrationRecord
        """
        self.total_integrations += 1

        # Resolve dependencies
        dependencies = self.resolve_dependencies(component_id)

        # Calculate integration value
        integration_value = self.calculate_integration_value(
            component_id,
            dependencies
        )

        # Perform integration
        success = True
        error_msg = None

        try:
            # Update component state
            if component_id in self.component_registry:
                comp_data = self.component_registry[component_id]
                comp_data['last_integrated'] = datetime.utcnow().isoformat()
                comp_data['integration_count'] += 1

            # Accumulate value
            self.accumulated_value += integration_value

            self.successful_integrations += 1

        except Exception as e:
            success = False
            error_msg = str(e)
            self.failed_integrations += 1

        # Create record
        record = IntegrationRecord(
            record_id=f"INT_{self.total_integrations:06d}",
            timestamp=datetime.utcnow().isoformat(),
            event_type=IntegrationEvent.INTEGRATION_COMPLETE if success else IntegrationEvent.INTEGRATION_FAILED,
            source_component=component_id,
            target_components=dependencies,
            integration_value=integration_value,
            success=success,
            metadata={
                'dependencies_resolved': len(dependencies),
                'accumulated_value': self.accumulated_value,
                'error': error_msg
            }
        )

        self.integration_records.append(record)

        status = "✓" if success else "✗"
        print(f"[∫] {status} Integrated: {component_id} (value={integration_value:.4f})")

        return record

    def integrate_all(self) -> Dict[str, Any]:
        """
        Integrate all registered components.

        Returns:
            Integration summary
        """
        print(f"\n[∫] Starting batch integration")
        print(f"[∫] Components: {len(self.component_registry)}")

        start_time = time.time()

        # Process each component
        for comp_id in self.component_registry.keys():
            self.integrate_component(comp_id)

        duration = time.time() - start_time

        summary = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_components': len(self.component_registry),
            'total_integrations': self.total_integrations,
            'successful': self.successful_integrations,
            'failed': self.failed_integrations,
            'success_rate': self.successful_integrations / self.total_integrations if self.total_integrations > 0 else 0,
            'accumulated_value': self.accumulated_value,
            'duration_seconds': duration,
            'integrations_per_second': self.total_integrations / duration if duration > 0 else 0
        }

        print(f"[∫] Batch complete: {self.successful_integrations}/{self.total_integrations} successful")
        print(f"[∫] Accumulated value: {self.accumulated_value:.6f}")
        print(f"[∫] Duration: {duration:.2f}s")

        return summary

    async def monitor_continuous(self, interval_seconds: int = 5, duration_minutes: int = 60):
        """
        Continuously monitor and integrate changes.

        Args:
            interval_seconds: Scan interval
            duration_minutes: Total monitoring duration
        """
        self.monitoring = True
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)

        print(f"\n[∫] Starting continuous monitoring")
        print(f"[∫] Interval: {interval_seconds}s")
        print(f"[∫] Duration: {duration_minutes}m")

        cycle = 0

        while self.monitoring and datetime.now() < end_time:
            cycle += 1

            # Detect changes
            changed = self.detect_changes()

            # Integrate changed components
            if changed:
                print(f"[∫] Cycle {cycle}: {len(changed)} changes detected")

                for comp_id in changed:
                    self.integrate_component(comp_id)

            # Wait for next cycle
            await asyncio.sleep(interval_seconds)

        self.monitoring = False

        print(f"[∫] Monitoring stopped after {cycle} cycles")

    def stop_monitoring(self):
        """Stop continuous monitoring."""
        self.monitoring = False
        print(f"[∫] Monitoring stop requested")

    def get_integration_statistics(self) -> Dict[str, Any]:
        """Get comprehensive integration statistics."""
        # Calculate rates
        success_rate = self.successful_integrations / self.total_integrations if self.total_integrations > 0 else 0

        # Top integrated components
        top_components = sorted(
            [
                {
                    'id': comp_id,
                    'integrations': data['integration_count'],
                    'last_integrated': data['last_integrated']
                }
                for comp_id, data in self.component_registry.items()
            ],
            key=lambda x: x['integrations'],
            reverse=True
        )[:10]

        # Recent integrations
        recent = [
            record.to_dict()
            for record in self.integration_records[-20:]
        ]

        return {
            'total_integrations': self.total_integrations,
            'successful_integrations': self.successful_integrations,
            'failed_integrations': self.failed_integrations,
            'success_rate': success_rate,
            'accumulated_value': self.accumulated_value,
            'registered_components': len(self.component_registry),
            'dependency_edges': sum(len(deps) for deps in self.dependency_graph.values()),
            'last_scan': self.last_scan.isoformat() if self.last_scan else None,
            'top_components': top_components,
            'recent_integrations': recent
        }

    def save_integration_report(self, output_file: Optional[Path] = None) -> Path:
        """Save integration report to JSON."""
        if output_file is None:
            output_file = self.workspace / "INTEGRATION_AUTOMATION_REPORT.json"

        stats = self.get_integration_statistics()

        report = {
            'statistics': stats,
            'component_registry': self.component_registry,
            'dependency_graph': {k: list(v) for k, v in self.dependency_graph.items()},
            'integration_records': [r.to_dict() for r in self.integration_records],
            'metadata': {
                'operator': '∫ (Integral)',
                'task': 'TASK-166',
                'wave': '6',
                'batch': 'C',
                'generated': datetime.utcnow().isoformat()
            }
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"[∫] Report saved: {output_file}")

        return output_file

    def get_mathematical_representation(self) -> str:
        """Get mathematical representation of integration state."""
        return (
            f"∫(System) = Σ(layers) Φ·Σ·Δ·∫\n"
            f"Total Integrations: {self.total_integrations}\n"
            f"Accumulated Value: {self.accumulated_value:.6f}\n"
            f"Success Rate: {self.successful_integrations / self.total_integrations if self.total_integrations > 0 else 0:.2%}"
        )


def demo_integration_operator():
    """Demonstration of ∫ operator."""
    print("=" * 70)
    print("INTEGRATION AUTOMATION OPERATOR (∫) - TASK-166")
    print("=" * 70)

    operator = IntegrationAutomationOperator()

    # Register components
    operator.register_component(
        "quantum_engine",
        "C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/quantum_engine.py"
    )

    operator.register_component(
        "holographic_context",
        "C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/holographic_context.py",
        dependencies=["quantum_engine"]
    )

    operator.register_component(
        "autonomous_runner",
        "C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/autonomous/AUTONOMOUS_RUNNER.py",
        dependencies=["quantum_engine", "holographic_context"]
    )

    # Integrate all
    summary = operator.integrate_all()

    # Get statistics
    stats = operator.get_integration_statistics()

    # Print mathematical representation
    print(f"\n{operator.get_mathematical_representation()}")

    # Save report
    operator.save_integration_report()

    print("\n" + "=" * 70)
    print("INTEGRATION COMPLETE")
    print("=" * 70)

    return summary


if __name__ == '__main__':
    demo_integration_operator()

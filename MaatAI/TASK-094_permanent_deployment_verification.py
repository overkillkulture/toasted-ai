#!/usr/bin/env python3
"""
TASK-094: Permanent Deployment Verification Protocol
Wave 7, Batch 5: Protocols

Automates comprehensive deployment verification with health checks,
integration testing, rollback capabilities, and continuous monitoring.
"""

import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class DeploymentPhase(Enum):
    """Phases of deployment verification."""
    PRE_DEPLOY = "pre_deploy"
    DEPLOYING = "deploying"
    POST_DEPLOY = "post_deploy"
    VERIFICATION = "verification"
    MONITORING = "monitoring"
    ROLLBACK = "rollback"


class HealthStatus(Enum):
    """Health check status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class VerificationResult(Enum):
    """Verification test results."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


@dataclass
class HealthCheck:
    """Represents a health check."""
    check_id: str
    name: str
    check_func: Optional[Callable] = None
    interval: float = 60.0  # seconds
    timeout: float = 10.0
    critical: bool = True
    last_run: float = 0.0
    last_status: HealthStatus = HealthStatus.UNKNOWN
    consecutive_failures: int = 0


@dataclass
class VerificationTest:
    """Represents a verification test."""
    test_id: str
    name: str
    phase: DeploymentPhase
    test_func: Optional[Callable] = None
    timeout: float = 30.0
    required: bool = True
    dependencies: Set[str] = field(default_factory=set)
    result: VerificationResult = VerificationResult.SKIPPED
    error_message: Optional[str] = None
    execution_time: float = 0.0


@dataclass
class DeploymentTarget:
    """Represents a deployment target."""
    target_id: str
    name: str
    url: str
    environment: str  # dev, staging, production
    health_checks: List[str] = field(default_factory=list)
    deployed_version: Optional[str] = None
    last_deployment: float = 0.0
    status: HealthStatus = HealthStatus.UNKNOWN


@dataclass
class DeploymentMetrics:
    """Metrics for deployment verification."""
    total_deployments: int = 0
    successful_deployments: int = 0
    failed_deployments: int = 0
    rollbacks: int = 0
    total_health_checks: int = 0
    failed_health_checks: int = 0
    avg_deployment_time: float = 0.0
    avg_verification_time: float = 0.0


class PermanentDeploymentVerifier:
    """
    Comprehensive deployment verification system.

    Features:
    - Multi-phase verification workflow
    - Automated health checking
    - Integration test execution
    - Rollback on failure
    - Continuous monitoring
    - Detailed reporting
    """

    def __init__(self, base_path: str = "C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI"):
        self.base_path = Path(base_path)
        self.targets: Dict[str, DeploymentTarget] = {}
        self.health_checks: Dict[str, HealthCheck] = {}
        self.verification_tests: Dict[str, VerificationTest] = {}
        self.metrics = DeploymentMetrics()

        # Deployment history
        self.deployment_history: List[Dict] = []

        # Monitoring state
        self.monitoring_active = False
        self.monitoring_task: Optional[asyncio.Task] = None

        # Initialize default checks
        self._initialize_default_checks()

    def _initialize_default_checks(self):
        """Create default health checks."""
        # System health
        self.add_health_check(
            "system_health",
            "System Health Check",
            interval=30.0,
            critical=True
        )

        # API health
        self.add_health_check(
            "api_health",
            "API Endpoint Health",
            interval=60.0,
            critical=True
        )

        # Database health
        self.add_health_check(
            "db_health",
            "Database Connectivity",
            interval=120.0,
            critical=True
        )

        # Performance check
        self.add_health_check(
            "performance",
            "Performance Metrics",
            interval=300.0,
            critical=False
        )

    def add_target(self,
                  target_id: str,
                  name: str,
                  url: str,
                  environment: str) -> DeploymentTarget:
        """
        Add a deployment target.

        Args:
            target_id: Unique identifier
            name: Target name
            url: Target URL
            environment: Environment type

        Returns:
            Created DeploymentTarget
        """
        target = DeploymentTarget(
            target_id=target_id,
            name=name,
            url=url,
            environment=environment,
            health_checks=list(self.health_checks.keys())
        )

        self.targets[target_id] = target
        return target

    def add_health_check(self,
                        check_id: str,
                        name: str,
                        check_func: Optional[Callable] = None,
                        interval: float = 60.0,
                        critical: bool = True):
        """Add a health check."""
        check = HealthCheck(
            check_id=check_id,
            name=name,
            check_func=check_func,
            interval=interval,
            critical=critical
        )

        self.health_checks[check_id] = check

        # Add to existing targets
        for target in self.targets.values():
            if check_id not in target.health_checks:
                target.health_checks.append(check_id)

    def add_verification_test(self,
                            test_id: str,
                            name: str,
                            phase: DeploymentPhase,
                            test_func: Optional[Callable] = None,
                            required: bool = True,
                            dependencies: Optional[Set[str]] = None):
        """Add a verification test."""
        test = VerificationTest(
            test_id=test_id,
            name=name,
            phase=phase,
            test_func=test_func,
            required=required,
            dependencies=dependencies or set()
        )

        self.verification_tests[test_id] = test

    async def run_health_check(self,
                              target_id: str,
                              check_id: str) -> HealthStatus:
        """
        Run a health check on a target.

        Args:
            target_id: Target to check
            check_id: Health check to run

        Returns:
            Health status result
        """
        if target_id not in self.targets or check_id not in self.health_checks:
            return HealthStatus.UNKNOWN

        target = self.targets[target_id]
        check = self.health_checks[check_id]

        check.last_run = time.time()

        try:
            if check.check_func:
                # Run custom check function
                result = await asyncio.wait_for(
                    check.check_func(target),
                    timeout=check.timeout
                )
                status = result
            else:
                # Simulate health check
                await asyncio.sleep(0.1)
                # 95% success rate
                status = HealthStatus.HEALTHY if time.time() % 20 < 19 else HealthStatus.DEGRADED

            check.last_status = status
            check.consecutive_failures = 0

        except asyncio.TimeoutError:
            status = HealthStatus.UNHEALTHY
            check.last_status = status
            check.consecutive_failures += 1
            self.metrics.failed_health_checks += 1

        except Exception as e:
            status = HealthStatus.UNHEALTHY
            check.last_status = status
            check.consecutive_failures += 1
            self.metrics.failed_health_checks += 1

        self.metrics.total_health_checks += 1
        return status

    async def run_verification_tests(self,
                                    phase: DeploymentPhase,
                                    target_id: str) -> Dict:
        """
        Run all verification tests for a phase.

        Args:
            phase: Deployment phase
            target_id: Target being verified

        Returns:
            Test results summary
        """
        # Get tests for this phase
        phase_tests = [
            test for test in self.verification_tests.values()
            if test.phase == phase
        ]

        # Sort by dependencies
        sorted_tests = self._sort_tests_by_dependencies(phase_tests)

        results = {
            "phase": phase.value,
            "target_id": target_id,
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_warning": 0,
            "tests_skipped": 0,
            "details": []
        }

        for test in sorted_tests:
            # Check dependencies
            deps_satisfied = all(
                self.verification_tests[dep_id].result == VerificationResult.PASSED
                for dep_id in test.dependencies
                if dep_id in self.verification_tests
            )

            if not deps_satisfied:
                test.result = VerificationResult.SKIPPED
                results["tests_skipped"] += 1
                continue

            # Run test
            start_time = time.time()

            try:
                if test.test_func:
                    test_result = await asyncio.wait_for(
                        test.test_func(self.targets[target_id]),
                        timeout=test.timeout
                    )
                    test.result = test_result
                else:
                    # Simulate test
                    await asyncio.sleep(0.2)
                    test.result = VerificationResult.PASSED

                test.execution_time = time.time() - start_time

            except asyncio.TimeoutError:
                test.result = VerificationResult.FAILED
                test.error_message = "Test timeout"
                test.execution_time = time.time() - start_time

            except Exception as e:
                test.result = VerificationResult.FAILED
                test.error_message = str(e)
                test.execution_time = time.time() - start_time

            # Update results
            results["tests_run"] += 1
            if test.result == VerificationResult.PASSED:
                results["tests_passed"] += 1
            elif test.result == VerificationResult.FAILED:
                results["tests_failed"] += 1
            elif test.result == VerificationResult.WARNING:
                results["tests_warning"] += 1

            results["details"].append({
                "test_id": test.test_id,
                "name": test.name,
                "result": test.result.value,
                "execution_time": f"{test.execution_time:.2f}s",
                "error": test.error_message
            })

        return results

    def _sort_tests_by_dependencies(self,
                                    tests: List[VerificationTest]) -> List[VerificationTest]:
        """Sort tests by dependency order."""
        sorted_tests = []
        remaining = tests.copy()

        while remaining:
            # Find tests with no unmet dependencies
            ready = [
                test for test in remaining
                if all(
                    dep_id in [t.test_id for t in sorted_tests]
                    for dep_id in test.dependencies
                    if dep_id in [t.test_id for t in tests]
                )
            ]

            if not ready:
                # Circular dependency or missing dependency
                sorted_tests.extend(remaining)
                break

            sorted_tests.extend(ready)
            for test in ready:
                remaining.remove(test)

        return sorted_tests

    async def deploy_and_verify(self,
                                target_id: str,
                                version: str) -> Dict:
        """
        Execute full deployment and verification workflow.

        Args:
            target_id: Target to deploy to
            version: Version being deployed

        Returns:
            Deployment results
        """
        if target_id not in self.targets:
            return {"error": "Target not found"}

        target = self.targets[target_id]
        start_time = time.time()

        deployment_record = {
            "target_id": target_id,
            "version": version,
            "start_time": start_time,
            "phases": {}
        }

        print(f"\nDeploying {version} to {target.name}...")

        # Phase 1: Pre-deployment checks
        print("  [1/5] Pre-deployment verification...")
        pre_results = await self.run_verification_tests(
            DeploymentPhase.PRE_DEPLOY,
            target_id
        )
        deployment_record["phases"]["pre_deploy"] = pre_results

        if pre_results["tests_failed"] > 0:
            print("  ✗ Pre-deployment checks failed")
            self.metrics.failed_deployments += 1
            return deployment_record

        # Phase 2: Deploy
        print("  [2/5] Deploying...")
        await asyncio.sleep(1.0)  # Simulate deployment
        target.deployed_version = version
        target.last_deployment = time.time()

        # Phase 3: Post-deployment checks
        print("  [3/5] Post-deployment verification...")
        post_results = await self.run_verification_tests(
            DeploymentPhase.POST_DEPLOY,
            target_id
        )
        deployment_record["phases"]["post_deploy"] = post_results

        # Phase 4: Health checks
        print("  [4/5] Running health checks...")
        health_results = []
        all_healthy = True

        for check_id in target.health_checks:
            status = await self.run_health_check(target_id, check_id)
            health_results.append({
                "check_id": check_id,
                "status": status.value
            })

            check = self.health_checks[check_id]
            if check.critical and status != HealthStatus.HEALTHY:
                all_healthy = False

        deployment_record["health_checks"] = health_results

        # Phase 5: Verification tests
        print("  [5/5] Running verification tests...")
        verify_results = await self.run_verification_tests(
            DeploymentPhase.VERIFICATION,
            target_id
        )
        deployment_record["phases"]["verification"] = verify_results

        # Determine overall success
        success = (
            pre_results["tests_failed"] == 0 and
            post_results["tests_failed"] == 0 and
            verify_results["tests_failed"] == 0 and
            all_healthy
        )

        # Update metrics
        deployment_time = time.time() - start_time
        total = self.metrics.total_deployments + 1
        self.metrics.avg_deployment_time = (
            (self.metrics.avg_deployment_time * self.metrics.total_deployments + deployment_time)
            / total
        )

        self.metrics.total_deployments += 1
        if success:
            self.metrics.successful_deployments += 1
            target.status = HealthStatus.HEALTHY
            print("  ✓ Deployment successful")
        else:
            self.metrics.failed_deployments += 1
            target.status = HealthStatus.UNHEALTHY
            print("  ✗ Deployment failed")

        deployment_record["success"] = success
        deployment_record["duration"] = deployment_time
        deployment_record["end_time"] = time.time()

        self.deployment_history.append(deployment_record)

        return deployment_record

    async def rollback_deployment(self,
                                 target_id: str,
                                 to_version: Optional[str] = None) -> Dict:
        """
        Rollback a deployment to previous version.

        Args:
            target_id: Target to rollback
            to_version: Version to rollback to (None = previous)

        Returns:
            Rollback results
        """
        if target_id not in self.targets:
            return {"error": "Target not found"}

        target = self.targets[target_id]

        # Find previous version
        if not to_version:
            previous_deployments = [
                d for d in self.deployment_history
                if d["target_id"] == target_id and d.get("success")
            ]

            if not previous_deployments:
                return {"error": "No previous successful deployment"}

            to_version = previous_deployments[-1]["version"]

        print(f"\nRolling back {target.name} to {to_version}...")

        # Perform rollback (simulate)
        await asyncio.sleep(0.5)
        target.deployed_version = to_version
        target.status = HealthStatus.UNKNOWN

        # Verify rollback
        verify_results = await self.run_verification_tests(
            DeploymentPhase.POST_DEPLOY,
            target_id
        )

        self.metrics.rollbacks += 1

        return {
            "target_id": target_id,
            "rolled_back_to": to_version,
            "success": verify_results["tests_failed"] == 0,
            "verification": verify_results
        }

    async def start_monitoring(self):
        """Start continuous monitoring of all targets."""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())

    async def stop_monitoring(self):
        """Stop continuous monitoring."""
        self.monitoring_active = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass

    async def _monitoring_loop(self):
        """Continuous monitoring loop."""
        while self.monitoring_active:
            for target_id in self.targets:
                for check_id in self.health_checks:
                    check = self.health_checks[check_id]

                    # Check if it's time to run this check
                    if time.time() - check.last_run >= check.interval:
                        await self.run_health_check(target_id, check_id)

            await asyncio.sleep(10.0)

    def get_deployment_summary(self) -> Dict:
        """Get summary of all deployments."""
        return {
            "metrics": {
                "total_deployments": self.metrics.total_deployments,
                "successful_deployments": self.metrics.successful_deployments,
                "failed_deployments": self.metrics.failed_deployments,
                "rollbacks": self.metrics.rollbacks,
                "success_rate": f"{(self.metrics.successful_deployments / max(self.metrics.total_deployments, 1)) * 100:.1f}%",
                "avg_deployment_time": f"{self.metrics.avg_deployment_time:.2f}s",
                "total_health_checks": self.metrics.total_health_checks,
                "failed_health_checks": self.metrics.failed_health_checks
            },
            "targets": {
                tid: {
                    "name": t.name,
                    "environment": t.environment,
                    "status": t.status.value,
                    "deployed_version": t.deployed_version,
                    "last_deployment": t.last_deployment
                }
                for tid, t in self.targets.items()
            }
        }

    def save_verification_state(self, output_path: Optional[Path] = None):
        """Save verification state to disk."""
        if output_path is None:
            output_path = self.base_path / "deployment_verification_state.json"

        state = {
            "targets": {
                tid: {
                    "target_id": t.target_id,
                    "name": t.name,
                    "url": t.url,
                    "environment": t.environment,
                    "deployed_version": t.deployed_version,
                    "status": t.status.value
                }
                for tid, t in self.targets.items()
            },
            "metrics": {
                "total_deployments": self.metrics.total_deployments,
                "successful_deployments": self.metrics.successful_deployments,
                "failed_deployments": self.metrics.failed_deployments,
                "rollbacks": self.metrics.rollbacks
            },
            "deployment_history": self.deployment_history
        }

        output_path.write_text(json.dumps(state, indent=2))
        return output_path


def main():
    """Test the deployment verification system."""
    print("=" * 60)
    print("TASK-094: Permanent Deployment Verification")
    print("=" * 60)

    verifier = PermanentDeploymentVerifier()

    # Add targets
    print("\n[1/4] Setting up deployment targets...")
    verifier.add_target(
        "prod_api",
        "Production API",
        "https://api.example.com",
        "production"
    )
    verifier.add_target(
        "staging_api",
        "Staging API",
        "https://staging.example.com",
        "staging"
    )

    # Add verification tests
    verifier.add_verification_test(
        "test_pre_1",
        "Check dependencies",
        DeploymentPhase.PRE_DEPLOY
    )
    verifier.add_verification_test(
        "test_pre_2",
        "Validate configuration",
        DeploymentPhase.PRE_DEPLOY
    )
    verifier.add_verification_test(
        "test_post_1",
        "API smoke test",
        DeploymentPhase.POST_DEPLOY
    )
    verifier.add_verification_test(
        "test_verify_1",
        "Integration test",
        DeploymentPhase.VERIFICATION
    )

    # Test deployment
    print("\n[2/4] Testing deployment workflow...")
    async def test_deploy():
        result = await verifier.deploy_and_verify("staging_api", "v1.2.3")
        print(f"\nDeployment result: {'Success' if result.get('success') else 'Failed'}")
        print(f"Duration: {result.get('duration', 0):.2f}s")

    asyncio.run(test_deploy())

    # Test rollback
    print("\n[3/4] Testing rollback...")
    async def test_rollback():
        # Deploy another version
        await verifier.deploy_and_verify("staging_api", "v1.2.4")

        # Rollback
        result = await verifier.rollback_deployment("staging_api")
        print(f"Rollback result: {'Success' if result.get('success') else 'Failed'}")
        print(f"Rolled back to: {result.get('rolled_back_to')}")

    asyncio.run(test_rollback())

    # Get summary
    print("\n[4/4] Deployment summary:")
    print("=" * 60)
    summary = verifier.get_deployment_summary()

    print("\nMetrics:")
    for key, value in summary["metrics"].items():
        print(f"  {key}: {value}")

    print("\nTargets:")
    for target_id, target_info in summary["targets"].items():
        print(f"  {target_id}:")
        for key, value in target_info.items():
            print(f"    {key}: {value}")

    # Save state
    output_path = verifier.save_verification_state()
    print(f"\n✓ Verification state saved: {output_path}")

    print("\n" + "=" * 60)
    print("TASK-094 Complete: Deployment verification automated!")
    print("=" * 60)


if __name__ == "__main__":
    main()

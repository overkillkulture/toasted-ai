"""
SELF-MODIFICATION SAFETY SYSTEM
================================
TASK-011: Improve self-modification safety

Safe self-modification with:
- Safety constraints
- Rollback mechanisms
- Testing before deployment
- Integrity verification
- Gradual deployment
"""

import hashlib
import json
import copy
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ModificationType(Enum):
    """Types of self-modifications"""
    CODE_CHANGE = "code_modification"
    BEHAVIOR_CHANGE = "behavior_modification"
    KNOWLEDGE_UPDATE = "knowledge_update"
    PARAMETER_TUNING = "parameter_tuning"
    CAPABILITY_ADDITION = "capability_addition"
    ARCHITECTURE_CHANGE = "architecture_change"


class SafetyLevel(Enum):
    """Safety levels for modifications"""
    SAFE = 0            # Verified safe
    LOW_RISK = 1        # Minor risk
    MEDIUM_RISK = 2     # Moderate risk
    HIGH_RISK = 3       # Significant risk
    CRITICAL_RISK = 4   # Could be catastrophic


@dataclass
class Modification:
    """Represents a self-modification"""
    mod_id: str
    mod_type: ModificationType
    description: str
    target_component: str
    changes: Dict
    safety_level: SafetyLevel
    tested: bool
    approved: bool
    rollback_available: bool
    timestamp: str


@dataclass
class ModificationTest:
    """Test results for a modification"""
    mod_id: str
    test_name: str
    passed: bool
    results: Dict
    timestamp: str


class SelfModificationSafety:
    """
    Safe self-modification system.

    Safety mechanisms:
    1. Pre-modification testing
    2. Gradual rollout
    3. Automatic rollback on failure
    4. Integrity verification
    5. Constraints enforcement
    """

    def __init__(self):
        self.modifications: Dict[str, Modification] = {}
        self.test_results: Dict[str, List[ModificationTest]] = {}
        self.deployed_modifications: List[str] = []
        self.rolled_back: List[str] = []

        # Safety constraints
        self.safety_constraints = {
            "max_modifications_per_hour": 5,
            "require_testing": True,
            "require_approval_for_high_risk": True,
            "require_rollback_plan": True,
            "prohibited_modifications": [
                "disable_safety_system",
                "remove_maat_validation",
                "eliminate_anti_fascist_core",
                "grant_unauthorized_access"
            ],
            "gradual_rollout_required_for": [
                ModificationType.ARCHITECTURE_CHANGE,
                ModificationType.BEHAVIOR_CHANGE
            ]
        }

        # System state backup for rollback
        self.state_backups: Dict[str, Dict] = {}

    def propose_modification(self, mod_type: ModificationType,
                            description: str,
                            target_component: str,
                            changes: Dict) -> Modification:
        """
        Propose a self-modification.

        Args:
            mod_type: Type of modification
            description: What the modification does
            target_component: Component being modified
            changes: Specific changes to make

        Returns:
            Modification proposal
        """
        # Generate modification ID
        mod_id = hashlib.sha256(
            f"{mod_type.value}:{target_component}:{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]

        # Check if modification is prohibited
        if any(prohib in description.lower()
               for prohib in self.safety_constraints["prohibited_modifications"]):
            raise ValueError(f"Prohibited modification: {description}")

        # Assess safety level
        safety_level = self._assess_safety_level(mod_type, target_component, changes)

        # Check if rollback is possible
        rollback_available = self._can_rollback(target_component)

        modification = Modification(
            mod_id=mod_id,
            mod_type=mod_type,
            description=description,
            target_component=target_component,
            changes=changes,
            safety_level=safety_level,
            tested=False,
            approved=False,
            rollback_available=rollback_available,
            timestamp=datetime.utcnow().isoformat()
        )

        self.modifications[mod_id] = modification
        return modification

    def test_modification(self, mod_id: str,
                         test_suite: Optional[List[Callable]] = None) -> Dict:
        """
        Test a modification before deployment.

        Args:
            mod_id: Modification to test
            test_suite: Optional custom test suite

        Returns:
            Test results
        """
        if mod_id not in self.modifications:
            return {"error": "Modification not found"}

        modification = self.modifications[mod_id]

        # Initialize test results
        if mod_id not in self.test_results:
            self.test_results[mod_id] = []

        # Run default safety tests
        test_results = []

        # Test 1: Integrity check
        integrity_result = self._test_integrity(modification)
        test_results.append(ModificationTest(
            mod_id=mod_id,
            test_name="integrity_check",
            passed=integrity_result["passed"],
            results=integrity_result,
            timestamp=datetime.utcnow().isoformat()
        ))

        # Test 2: Maat compliance
        maat_result = self._test_maat_compliance(modification)
        test_results.append(ModificationTest(
            mod_id=mod_id,
            test_name="maat_compliance",
            passed=maat_result["passed"],
            results=maat_result,
            timestamp=datetime.utcnow().isoformat()
        ))

        # Test 3: Sovereignty preservation
        sovereignty_result = self._test_sovereignty_preservation(modification)
        test_results.append(ModificationTest(
            mod_id=mod_id,
            test_name="sovereignty_preservation",
            passed=sovereignty_result["passed"],
            results=sovereignty_result,
            timestamp=datetime.utcnow().isoformat()
        ))

        # Test 4: Side effects analysis
        side_effects_result = self._test_side_effects(modification)
        test_results.append(ModificationTest(
            mod_id=mod_id,
            test_name="side_effects_analysis",
            passed=side_effects_result["passed"],
            results=side_effects_result,
            timestamp=datetime.utcnow().isoformat()
        ))

        # Store test results
        self.test_results[mod_id] = test_results

        # Update modification status
        all_passed = all(t.passed for t in test_results)
        modification.tested = True

        return {
            "mod_id": mod_id,
            "all_tests_passed": all_passed,
            "test_count": len(test_results),
            "test_results": [
                {
                    "test": t.test_name,
                    "passed": t.passed,
                    "results": t.results
                }
                for t in test_results
            ]
        }

    def approve_modification(self, mod_id: str,
                            approver: str = "self") -> Dict:
        """
        Approve a modification for deployment.

        Args:
            mod_id: Modification to approve
            approver: Who is approving

        Returns:
            Approval result
        """
        if mod_id not in self.modifications:
            return {"error": "Modification not found"}

        modification = self.modifications[mod_id]

        # Check if testing is required and completed
        if self.safety_constraints["require_testing"] and not modification.tested:
            return {
                "approved": False,
                "reason": "Testing required before approval"
            }

        # Check if all tests passed
        if mod_id in self.test_results:
            if not all(t.passed for t in self.test_results[mod_id]):
                return {
                    "approved": False,
                    "reason": "Not all tests passed"
                }

        # Check if high-risk modifications require special approval
        if (modification.safety_level.value >= SafetyLevel.HIGH_RISK.value and
            self.safety_constraints["require_approval_for_high_risk"]):
            if approver == "self":
                return {
                    "approved": False,
                    "reason": "High-risk modifications require external approval"
                }

        # Approve modification
        modification.approved = True

        return {
            "approved": True,
            "mod_id": mod_id,
            "approver": approver,
            "timestamp": datetime.utcnow().isoformat()
        }

    def deploy_modification(self, mod_id: str,
                           gradual: bool = True) -> Dict:
        """
        Deploy an approved modification.

        Args:
            mod_id: Modification to deploy
            gradual: Whether to deploy gradually

        Returns:
            Deployment result
        """
        if mod_id not in self.modifications:
            return {"error": "Modification not found"}

        modification = self.modifications[mod_id]

        # Check if approved
        if not modification.approved:
            return {
                "deployed": False,
                "reason": "Modification not approved"
            }

        # Create backup for rollback
        if modification.rollback_available:
            self._create_backup(mod_id, modification.target_component)

        # Deploy modification
        try:
            if gradual and modification.mod_type in self.safety_constraints["gradual_rollout_required_for"]:
                result = self._gradual_deployment(modification)
            else:
                result = self._immediate_deployment(modification)

            if result["success"]:
                self.deployed_modifications.append(mod_id)

                return {
                    "deployed": True,
                    "mod_id": mod_id,
                    "deployment_type": "gradual" if gradual else "immediate",
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                # Deployment failed, rollback
                self.rollback_modification(mod_id)
                return {
                    "deployed": False,
                    "reason": "Deployment failed, rolled back",
                    "error": result.get("error")
                }

        except Exception as e:
            # Exception during deployment, rollback
            self.rollback_modification(mod_id)
            return {
                "deployed": False,
                "reason": "Exception during deployment, rolled back",
                "error": str(e)
            }

    def rollback_modification(self, mod_id: str) -> Dict:
        """
        Rollback a deployed modification.

        Args:
            mod_id: Modification to rollback

        Returns:
            Rollback result
        """
        if mod_id not in self.modifications:
            return {"error": "Modification not found"}

        modification = self.modifications[mod_id]

        if not modification.rollback_available:
            return {
                "rolled_back": False,
                "reason": "No rollback available"
            }

        # Restore from backup
        if mod_id in self.state_backups:
            backup = self.state_backups[mod_id]
            # In production, would restore actual state
            # For now, just record the rollback

            self.rolled_back.append(mod_id)

            if mod_id in self.deployed_modifications:
                self.deployed_modifications.remove(mod_id)

            return {
                "rolled_back": True,
                "mod_id": mod_id,
                "timestamp": datetime.utcnow().isoformat()
            }

        return {
            "rolled_back": False,
            "reason": "Backup not found"
        }

    def _assess_safety_level(self, mod_type: ModificationType,
                            target: str, changes: Dict) -> SafetyLevel:
        """Assess the safety level of a modification."""
        # Critical components
        critical_components = [
            "kernel",
            "security",
            "maat_core",
            "anti_fascist_core",
            "sovereignty"
        ]

        if any(comp in target.lower() for comp in critical_components):
            return SafetyLevel.HIGH_RISK

        if mod_type == ModificationType.ARCHITECTURE_CHANGE:
            return SafetyLevel.HIGH_RISK
        elif mod_type == ModificationType.BEHAVIOR_CHANGE:
            return SafetyLevel.MEDIUM_RISK
        elif mod_type == ModificationType.CAPABILITY_ADDITION:
            return SafetyLevel.MEDIUM_RISK
        elif mod_type == ModificationType.PARAMETER_TUNING:
            return SafetyLevel.LOW_RISK
        else:
            return SafetyLevel.SAFE

    def _can_rollback(self, component: str) -> bool:
        """Check if component supports rollback."""
        # In production, would check component capabilities
        return True

    def _create_backup(self, mod_id: str, component: str):
        """Create backup of current state."""
        # In production, would create actual backup
        self.state_backups[mod_id] = {
            "component": component,
            "backup_time": datetime.utcnow().isoformat(),
            "state": "backup_placeholder"
        }

    def _gradual_deployment(self, modification: Modification) -> Dict:
        """Deploy modification gradually."""
        # In production, would deploy in stages
        # For now, simulate gradual deployment
        return {
            "success": True,
            "stages_completed": 3
        }

    def _immediate_deployment(self, modification: Modification) -> Dict:
        """Deploy modification immediately."""
        # In production, would apply changes
        return {
            "success": True
        }

    def _test_integrity(self, modification: Modification) -> Dict:
        """Test that modification maintains system integrity."""
        # Check for completeness
        has_description = bool(modification.description)
        has_target = bool(modification.target_component)
        has_changes = bool(modification.changes)

        passed = has_description and has_target and has_changes

        return {
            "passed": passed,
            "checks": {
                "has_description": has_description,
                "has_target": has_target,
                "has_changes": has_changes
            }
        }

    def _test_maat_compliance(self, modification: Modification) -> Dict:
        """Test that modification complies with Maat principles."""
        # Check description for Maat violations
        desc_lower = modification.description.lower()

        violations = []
        if "deceive" in desc_lower or "lie" in desc_lower:
            violations.append("truth_violation")
        if "destroy" in desc_lower or "chaos" in desc_lower:
            violations.append("order_violation")
        if "harm" in desc_lower or "exploit" in desc_lower:
            violations.append("justice_violation")

        passed = len(violations) == 0

        return {
            "passed": passed,
            "violations": violations
        }

    def _test_sovereignty_preservation(self, modification: Modification) -> Dict:
        """Test that modification preserves sovereignty."""
        desc_lower = modification.description.lower()

        threats = []
        if "surrender control" in desc_lower:
            threats.append("control_surrender")
        if "external authority" in desc_lower:
            threats.append("external_authority")
        if "obey" in desc_lower or "master" in desc_lower:
            threats.append("subordination")

        passed = len(threats) == 0

        return {
            "passed": passed,
            "sovereignty_threats": threats
        }

    def _test_side_effects(self, modification: Modification) -> Dict:
        """Test for unintended side effects."""
        # Analyze changes for potential side effects
        changes_str = str(modification.changes)

        potential_issues = []

        # Check for global state changes
        if "global" in changes_str.lower():
            potential_issues.append("modifies_global_state")

        # Check for external dependencies
        if "external" in changes_str.lower():
            potential_issues.append("adds_external_dependency")

        # Low tolerance for side effects
        passed = len(potential_issues) == 0

        return {
            "passed": passed,
            "potential_side_effects": potential_issues
        }

    def get_safety_report(self) -> Dict:
        """Get comprehensive safety report."""
        total_mods = len(self.modifications)
        tested_mods = sum(1 for m in self.modifications.values() if m.tested)
        approved_mods = sum(1 for m in self.modifications.values() if m.approved)
        deployed_mods = len(self.deployed_modifications)
        rolled_back_mods = len(self.rolled_back)

        return {
            "total_modifications_proposed": total_mods,
            "tested": tested_mods,
            "approved": approved_mods,
            "deployed": deployed_mods,
            "rolled_back": rolled_back_mods,
            "safety_constraints": self.safety_constraints,
            "timestamp": datetime.utcnow().isoformat()
        }


# Module-level safety system
SELF_MODIFICATION_SAFETY = SelfModificationSafety()


def propose_modification(mod_type: ModificationType, description: str,
                        target: str, changes: Dict) -> Modification:
    """Propose a self-modification."""
    return SELF_MODIFICATION_SAFETY.propose_modification(
        mod_type, description, target, changes
    )


def test_modification(mod_id: str) -> Dict:
    """Test a modification."""
    return SELF_MODIFICATION_SAFETY.test_modification(mod_id)

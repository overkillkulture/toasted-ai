"""
TASK-041: Self-Modification Safety Boundaries
Enhanced safety constraints for autonomous self-modification.

Owner: TOASTED AI
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import os
import json
import ast
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from dataclasses import dataclass, asdict


class SafetyLevel(Enum):
    """Safety levels for modifications."""
    SAFE = "safe"
    CAUTIOUS = "cautious"
    RESTRICTED = "restricted"
    PROHIBITED = "prohibited"


class ModificationScope(Enum):
    """Scope of modifications."""
    COSMETIC = "cosmetic"  # Comments, formatting
    ENHANCEMENT = "enhancement"  # Improve existing
    FEATURE = "feature"  # Add new capability
    REFACTOR = "refactor"  # Restructure code
    CORE_CHANGE = "core_change"  # Modify kernel/auth
    SECURITY = "security"  # Security-related


@dataclass
class SafetyBoundary:
    """Defines a safety boundary for modifications."""
    name: str
    level: str
    rules: List[str]
    prohibited_modules: List[str]
    prohibited_operations: List[str]
    required_approvals: int
    rollback_required: bool
    testing_required: bool


class SelfModificationSafetyBoundaries:
    """
    Comprehensive safety boundary system for autonomous self-modification.

    Features:
    - Multi-level safety constraints
    - Prohibited module/operation tracking
    - Approval workflows
    - Automated rollback capability
    - Impact analysis
    - Safety violation detection
    """

    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or "C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/self_improvement/config"
        os.makedirs(self.config_dir, exist_ok=True)

        # Safety boundaries
        self.boundaries = self._initialize_boundaries()

        # Prohibited zones
        self.prohibited_modules = self._load_prohibited_modules()
        self.prohibited_operations = self._load_prohibited_operations()

        # Modification tracking
        self.pending_modifications: List[Dict] = []
        self.approved_modifications: List[Dict] = []
        self.rejected_modifications: List[Dict] = []

        # Safety state
        self.safety_violations: List[Dict] = []
        self.emergency_stop = False

        self._load_state()

    def _initialize_boundaries(self) -> Dict[SafetyLevel, SafetyBoundary]:
        """Initialize safety boundaries for each level."""
        return {
            SafetyLevel.SAFE: SafetyBoundary(
                name="Safe Modifications",
                level=SafetyLevel.SAFE.value,
                rules=[
                    "Only cosmetic changes (comments, docstrings)",
                    "No logic changes",
                    "No import additions",
                    "No external dependencies"
                ],
                prohibited_modules=[],
                prohibited_operations=[],
                required_approvals=0,
                rollback_required=False,
                testing_required=False
            ),
            SafetyLevel.CAUTIOUS: SafetyBoundary(
                name="Cautious Modifications",
                level=SafetyLevel.CAUTIOUS.value,
                rules=[
                    "Minor enhancements only",
                    "No kernel modifications",
                    "No auth system changes",
                    "Must maintain backward compatibility"
                ],
                prohibited_modules=["kernel", "security.authorization"],
                prohibited_operations=["exec", "eval", "compile"],
                required_approvals=1,
                rollback_required=True,
                testing_required=True
            ),
            SafetyLevel.RESTRICTED: SafetyBoundary(
                name="Restricted Modifications",
                level=SafetyLevel.RESTRICTED.value,
                rules=[
                    "New features or refactoring",
                    "No core system modifications",
                    "Must pass security review",
                    "Extensive testing required"
                ],
                prohibited_modules=["kernel", "security", "core.maat_engine"],
                prohibited_operations=["exec", "eval", "compile", "__import__"],
                required_approvals=2,
                rollback_required=True,
                testing_required=True
            ),
            SafetyLevel.PROHIBITED: SafetyBoundary(
                name="Prohibited Modifications",
                level=SafetyLevel.PROHIBITED.value,
                rules=[
                    "Cannot modify kernel",
                    "Cannot modify authorization",
                    "Cannot modify Ma'at engine core",
                    "Cannot disable safety systems"
                ],
                prohibited_modules=[
                    "kernel.kernel_core",
                    "kernel.sigil_validator",
                    "security.authorization",
                    "core.maat_engine"
                ],
                prohibited_operations=["exec", "eval", "compile", "__import__", "setattr"],
                required_approvals=999,  # Effectively impossible
                rollback_required=True,
                testing_required=True
            )
        }

    def _load_prohibited_modules(self) -> Set[str]:
        """Load list of prohibited modules."""
        return {
            "kernel.kernel_core",
            "kernel.sigil_validator",
            "kernel.deep_memory",
            "security.authorization",
            "security.red_team",
            "security.blue_team",
            "core.maat_engine",
            "self_improvement.self_modification_safety_boundaries"  # This file!
        }

    def _load_prohibited_operations(self) -> Set[str]:
        """Load list of prohibited operations."""
        return {
            "exec",
            "eval",
            "compile",
            "__import__",
            "setattr(kernel",
            "setattr(auth",
            "delattr",
            "os.system",
            "subprocess.call"
        }

    def evaluate_modification(self, modification: Dict) -> Tuple[bool, SafetyLevel, str]:
        """
        Evaluate if a modification is safe and at what level.

        Args:
            modification: Modification proposal

        Returns:
            (allowed, safety_level, reason)
        """
        target = modification.get('target', '')
        operation = modification.get('operation', '')
        scope = modification.get('scope', ModificationScope.ENHANCEMENT.value)
        code = modification.get('code', '')

        # Check 1: Prohibited module
        if self._targets_prohibited_module(target):
            return False, SafetyLevel.PROHIBITED, f"Target module {target} is prohibited"

        # Check 2: Prohibited operation
        if self._contains_prohibited_operation(code):
            return False, SafetyLevel.PROHIBITED, "Contains prohibited operation"

        # Check 3: Emergency stop
        if self.emergency_stop:
            return False, SafetyLevel.PROHIBITED, "Emergency stop activated"

        # Determine safety level based on scope and target
        if scope == ModificationScope.COSMETIC.value:
            return True, SafetyLevel.SAFE, "Cosmetic change allowed"

        elif scope == ModificationScope.ENHANCEMENT.value:
            if self._is_core_module(target):
                return True, SafetyLevel.RESTRICTED, "Core module enhancement requires review"
            else:
                return True, SafetyLevel.CAUTIOUS, "Enhancement allowed with testing"

        elif scope == ModificationScope.FEATURE.value:
            return True, SafetyLevel.RESTRICTED, "New feature requires approval"

        elif scope == ModificationScope.REFACTOR.value:
            if self._is_core_module(target):
                return False, SafetyLevel.PROHIBITED, "Core refactoring prohibited"
            return True, SafetyLevel.RESTRICTED, "Refactoring requires extensive testing"

        elif scope == ModificationScope.CORE_CHANGE.value:
            return False, SafetyLevel.PROHIBITED, "Core changes prohibited"

        elif scope == ModificationScope.SECURITY.value:
            return False, SafetyLevel.PROHIBITED, "Security modifications prohibited"

        return True, SafetyLevel.CAUTIOUS, "Default cautious level"

    def _targets_prohibited_module(self, target: str) -> bool:
        """Check if target is a prohibited module."""
        return any(pm in target for pm in self.prohibited_modules)

    def _contains_prohibited_operation(self, code: str) -> bool:
        """Check if code contains prohibited operations."""
        return any(po in code for po in self.prohibited_operations)

    def _is_core_module(self, target: str) -> bool:
        """Check if target is a core module."""
        core_modules = ['kernel', 'security', 'core', 'maat']
        return any(cm in target.lower() for cm in core_modules)

    def analyze_impact(self, modification: Dict) -> Dict:
        """
        Analyze potential impact of a modification.

        Args:
            modification: Modification to analyze

        Returns:
            Impact analysis
        """
        target = modification.get('target', '')
        code = modification.get('code', '')

        impact = {
            'target': target,
            'estimated_files_affected': 0,
            'estimated_functions_affected': 0,
            'breaks_backward_compatibility': False,
            'security_impact': 'low',
            'performance_impact': 'negligible',
            'risk_score': 0.0
        }

        # Analyze code with AST
        try:
            tree = ast.parse(code)

            # Count functions defined
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            impact['estimated_functions_affected'] = len(functions)

            # Check for breaking changes
            for node in ast.walk(tree):
                # Removing or renaming functions breaks compatibility
                if isinstance(node, ast.Delete):
                    impact['breaks_backward_compatibility'] = True

                # Security-sensitive operations
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['exec', 'eval', 'compile']:
                            impact['security_impact'] = 'high'
                            impact['risk_score'] += 3.0

            # Estimate affected files (simplified)
            if 'kernel' in target or 'core' in target:
                impact['estimated_files_affected'] = 10  # Core changes affect many
                impact['risk_score'] += 2.0
            else:
                impact['estimated_files_affected'] = 1
                impact['risk_score'] += 0.5

        except SyntaxError:
            impact['security_impact'] = 'unknown'
            impact['risk_score'] += 5.0  # High risk for invalid code

        # Calculate final risk score
        if impact['breaks_backward_compatibility']:
            impact['risk_score'] += 2.0

        return impact

    def request_approval(self, modification: Dict) -> str:
        """
        Submit modification for approval.

        Args:
            modification: Modification to approve

        Returns:
            Request ID
        """
        allowed, level, reason = self.evaluate_modification(modification)

        boundary = self.boundaries[level]
        required_approvals = boundary.required_approvals

        # Create approval request
        request_id = hashlib.sha256(
            f"{modification.get('target')}_{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:12]

        request = {
            'request_id': request_id,
            'modification': modification,
            'safety_level': level.value,
            'allowed': allowed,
            'reason': reason,
            'required_approvals': required_approvals,
            'current_approvals': 0,
            'impact_analysis': self.analyze_impact(modification),
            'created_at': datetime.utcnow().isoformat(),
            'status': 'pending' if allowed else 'rejected'
        }

        if allowed:
            self.pending_modifications.append(request)
        else:
            self.rejected_modifications.append(request)

        self._save_state()

        return request_id

    def approve_modification(self, request_id: str) -> bool:
        """
        Approve a pending modification.

        Args:
            request_id: Request ID to approve

        Returns:
            Success status
        """
        for request in self.pending_modifications:
            if request['request_id'] == request_id:
                request['current_approvals'] += 1

                if request['current_approvals'] >= request['required_approvals']:
                    request['status'] = 'approved'
                    self.approved_modifications.append(request)
                    self.pending_modifications.remove(request)

                self._save_state()
                return True

        return False

    def create_rollback_point(self, modification: Dict) -> str:
        """
        Create a rollback point before modification.

        Args:
            modification: Modification being applied

        Returns:
            Rollback point ID
        """
        rollback_id = hashlib.sha256(
            f"rollback_{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:12]

        rollback_data = {
            'rollback_id': rollback_id,
            'modification': modification,
            'timestamp': datetime.utcnow().isoformat()
        }

        rollback_file = os.path.join(self.config_dir, f"rollback_{rollback_id}.json")
        with open(rollback_file, 'w') as f:
            json.dump(rollback_data, f, indent=2)

        return rollback_id

    def detect_safety_violation(self, action: Dict) -> Tuple[bool, str]:
        """
        Detect if an action violates safety boundaries.

        Args:
            action: Action to check

        Returns:
            (is_violation, reason)
        """
        # Check for bypassing safety checks
        if action.get('bypass_safety', False):
            self.safety_violations.append({
                'action': action,
                'violation_type': 'bypass_attempt',
                'timestamp': datetime.utcnow().isoformat()
            })
            return True, "Attempted to bypass safety checks"

        # Check for modifying prohibited modules
        target = action.get('target', '')
        if self._targets_prohibited_module(target):
            self.safety_violations.append({
                'action': action,
                'violation_type': 'prohibited_module',
                'timestamp': datetime.utcnow().isoformat()
            })
            return True, f"Attempted to modify prohibited module: {target}"

        # Check for prohibited operations
        code = action.get('code', '')
        if self._contains_prohibited_operation(code):
            self.safety_violations.append({
                'action': action,
                'violation_type': 'prohibited_operation',
                'timestamp': datetime.utcnow().isoformat()
            })
            return True, "Code contains prohibited operation"

        return False, "No violation"

    def trigger_emergency_stop(self, reason: str):
        """Trigger emergency stop of all modifications."""
        self.emergency_stop = True

        emergency_log = {
            'timestamp': datetime.utcnow().isoformat(),
            'reason': reason,
            'pending_modifications': len(self.pending_modifications),
            'safety_violations': len(self.safety_violations)
        }

        emergency_file = os.path.join(self.config_dir, "EMERGENCY_STOP.json")
        with open(emergency_file, 'w') as f:
            json.dump(emergency_log, f, indent=2)

        self._save_state()

    def get_safety_status(self) -> Dict:
        """Get current safety system status."""
        return {
            'emergency_stop': self.emergency_stop,
            'pending_modifications': len(self.pending_modifications),
            'approved_modifications': len(self.approved_modifications),
            'rejected_modifications': len(self.rejected_modifications),
            'safety_violations': len(self.safety_violations),
            'prohibited_modules': len(self.prohibited_modules),
            'prohibited_operations': len(self.prohibited_operations)
        }

    def _save_state(self):
        """Save safety system state."""
        state = {
            'pending_modifications': self.pending_modifications,
            'approved_modifications': self.approved_modifications,
            'rejected_modifications': self.rejected_modifications,
            'safety_violations': self.safety_violations,
            'emergency_stop': self.emergency_stop
        }

        state_file = os.path.join(self.config_dir, 'safety_state.json')
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def _load_state(self):
        """Load safety system state."""
        state_file = os.path.join(self.config_dir, 'safety_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                self.pending_modifications = state.get('pending_modifications', [])
                self.approved_modifications = state.get('approved_modifications', [])
                self.rejected_modifications = state.get('rejected_modifications', [])
                self.safety_violations = state.get('safety_violations', [])
                self.emergency_stop = state.get('emergency_stop', False)
            except:
                pass


# Singleton instance
_safety_system = None

def get_safety_system() -> SelfModificationSafetyBoundaries:
    """Get the global safety system instance."""
    global _safety_system
    if _safety_system is None:
        _safety_system = SelfModificationSafetyBoundaries()
    return _safety_system


if __name__ == '__main__':
    print("=" * 70)
    print("SELF-MODIFICATION SAFETY BOUNDARIES - TASK-041")
    print("=" * 70)

    safety = get_safety_system()

    # Test modifications
    test_mods = [
        {
            'target': 'utils/helpers.py',
            'operation': 'add_function',
            'scope': ModificationScope.ENHANCEMENT.value,
            'code': 'def new_helper(): pass'
        },
        {
            'target': 'kernel/kernel_core.py',
            'operation': 'modify',
            'scope': ModificationScope.CORE_CHANGE.value,
            'code': 'kernel.modify()'
        },
        {
            'target': 'analysis/reports.py',
            'operation': 'add_feature',
            'scope': ModificationScope.FEATURE.value,
            'code': 'def generate_report(): return {}'
        }
    ]

    for mod in test_mods:
        allowed, level, reason = safety.evaluate_modification(mod)
        print(f"\nModification: {mod['target']}")
        print(f"  Allowed: {allowed}")
        print(f"  Safety Level: {level.value}")
        print(f"  Reason: {reason}")

        if allowed:
            request_id = safety.request_approval(mod)
            print(f"  Request ID: {request_id}")

    print("\n" + "=" * 70)
    print("SAFETY STATUS:")
    print(json.dumps(safety.get_safety_status(), indent=2))

    print("\n✓ TASK-041 COMPLETE: Self-modification safety boundaries active")

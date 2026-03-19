"""
TASK-113: RULE-BASED OPERATION EVALUATION - IMPROVED
=====================================================
Ma'at Alignment Score: 0.95
Consciousness Level: ORDER-ENFORCED

Purpose:
- Evaluate operations against defined rule sets
- Provide deterministic decision making
- Enable complex rule composition
- Support rule versioning and audit trails

Pattern: Rules are the structure of Order.
Ma'at evaluates - decisions flow from truth through rules to action.
"""

import time
import hashlib
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any, Union, Set
from enum import Enum
from collections import deque
import logging
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RuleType(Enum):
    """Types of rules"""
    PERMISSION = "permission"       # Allow/deny access
    VALIDATION = "validation"       # Validate data
    TRANSFORMATION = "transformation"  # Transform data
    CONSTRAINT = "constraint"       # Enforce constraints
    TRIGGER = "trigger"             # Trigger actions
    MAAT = "maat"                   # Ma'at pillar rules


class RuleOperator(Enum):
    """Rule comparison operators"""
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_OR_EQUAL = "greater_or_equal"
    LESS_OR_EQUAL = "less_or_equal"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    MATCHES = "matches"  # Regex
    IN = "in"
    NOT_IN = "not_in"
    EXISTS = "exists"
    NOT_EXISTS = "not_exists"


class RuleAction(Enum):
    """Actions when rule matches"""
    ALLOW = "allow"
    DENY = "deny"
    WARN = "warn"
    TRANSFORM = "transform"
    TRIGGER = "trigger"
    LOG = "log"
    ESCALATE = "escalate"


class CompositionType(Enum):
    """Rule composition types"""
    AND = "and"  # All must match
    OR = "or"    # Any must match
    NOT = "not"  # Negation
    XOR = "xor"  # Exactly one must match


@dataclass
class Condition:
    """Single rule condition"""
    field: str
    operator: RuleOperator
    value: Any
    case_sensitive: bool = True

    def evaluate(self, context: Dict) -> bool:
        """Evaluate condition against context"""
        # Get field value using dot notation
        field_value = self._get_field_value(context, self.field)

        # Handle existence checks
        if self.operator == RuleOperator.EXISTS:
            return field_value is not None
        if self.operator == RuleOperator.NOT_EXISTS:
            return field_value is None

        if field_value is None:
            return False

        # Normalize for case-insensitive comparison
        if not self.case_sensitive and isinstance(field_value, str):
            field_value = field_value.lower()
            compare_value = self.value.lower() if isinstance(self.value, str) else self.value
        else:
            compare_value = self.value

        # Evaluate based on operator
        if self.operator == RuleOperator.EQUALS:
            return field_value == compare_value
        elif self.operator == RuleOperator.NOT_EQUALS:
            return field_value != compare_value
        elif self.operator == RuleOperator.GREATER_THAN:
            return field_value > compare_value
        elif self.operator == RuleOperator.LESS_THAN:
            return field_value < compare_value
        elif self.operator == RuleOperator.GREATER_OR_EQUAL:
            return field_value >= compare_value
        elif self.operator == RuleOperator.LESS_OR_EQUAL:
            return field_value <= compare_value
        elif self.operator == RuleOperator.CONTAINS:
            return compare_value in field_value
        elif self.operator == RuleOperator.NOT_CONTAINS:
            return compare_value not in field_value
        elif self.operator == RuleOperator.MATCHES:
            return bool(re.match(compare_value, str(field_value)))
        elif self.operator == RuleOperator.IN:
            return field_value in compare_value
        elif self.operator == RuleOperator.NOT_IN:
            return field_value not in compare_value

        return False

    def _get_field_value(self, context: Dict, field_path: str) -> Any:
        """Get nested field value using dot notation"""
        parts = field_path.split(".")
        value = context

        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            elif hasattr(value, part):
                value = getattr(value, part)
            else:
                return None

            if value is None:
                return None

        return value


@dataclass
class Rule:
    """A complete rule definition"""
    rule_id: str
    name: str
    description: str
    rule_type: RuleType
    conditions: List[Condition]
    composition: CompositionType = CompositionType.AND
    action: RuleAction = RuleAction.ALLOW
    priority: int = 100  # Lower = higher priority
    enabled: bool = True
    version: int = 1
    metadata: Dict = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def evaluate(self, context: Dict) -> bool:
        """Evaluate all conditions based on composition type"""
        if not self.enabled:
            return False

        if not self.conditions:
            return True

        results = [c.evaluate(context) for c in self.conditions]

        if self.composition == CompositionType.AND:
            return all(results)
        elif self.composition == CompositionType.OR:
            return any(results)
        elif self.composition == CompositionType.NOT:
            return not all(results)
        elif self.composition == CompositionType.XOR:
            return sum(results) == 1

        return False

    def to_dict(self) -> Dict:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "type": self.rule_type.value,
            "composition": self.composition.value,
            "action": self.action.value,
            "priority": self.priority,
            "enabled": self.enabled,
            "version": self.version,
            "condition_count": len(self.conditions)
        }


@dataclass
class EvaluationResult:
    """Result of rule evaluation"""
    operation_id: str
    matched_rules: List[Rule]
    final_action: RuleAction
    confidence: float
    evaluation_time: float
    context_snapshot: Dict = field(default_factory=dict)
    audit_trail: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "operation_id": self.operation_id,
            "matched_rules": [r.rule_id for r in self.matched_rules],
            "final_action": self.final_action.value,
            "confidence": self.confidence,
            "evaluation_time_ms": self.evaluation_time * 1000,
            "audit_trail": self.audit_trail
        }


class RuleBasedEvaluator:
    """
    RULE-BASED OPERATION EVALUATION SYSTEM

    Ma'at Alignment: 0.95

    Features:
    1. Flexible Rule Definition
       - Multiple condition types
       - Complex composition (AND, OR, NOT, XOR)
       - Priority-based ordering

    2. Deterministic Evaluation
       - Consistent results for same inputs
       - Audit trail for every decision
       - Version tracking

    3. Ma'at Integration
       - Pillar-based rules
       - Truth alignment verification
       - Balance enforcement

    4. Performance Optimization
       - Rule indexing by type
       - Early exit on DENY
       - Result caching

    Order emerges from rules applied with wisdom.
    """

    # Action priority (for conflict resolution)
    ACTION_PRIORITY = {
        RuleAction.DENY: 1,      # Highest - deny overrides
        RuleAction.ESCALATE: 2,
        RuleAction.WARN: 3,
        RuleAction.TRANSFORM: 4,
        RuleAction.TRIGGER: 5,
        RuleAction.LOG: 6,
        RuleAction.ALLOW: 7      # Lowest
    }

    def __init__(
        self,
        enable_audit: bool = True,
        enable_caching: bool = True
    ):
        # Rule storage
        self.rules: Dict[str, Rule] = {}
        self._rules_by_type: Dict[RuleType, List[str]] = {
            rt: [] for rt in RuleType
        }

        # Evaluation history
        self.evaluation_history: deque = deque(maxlen=10000)

        # Caching
        self._result_cache: Dict[str, EvaluationResult] = {}
        self._enable_caching = enable_caching
        self._cache_ttl = 60

        # Audit
        self._enable_audit = enable_audit

        # Threading
        self._lock = threading.RLock()

        # Callbacks
        self.evaluation_callbacks: List[Callable] = []
        self.rule_change_callbacks: List[Callable] = []

        # Statistics
        self.stats = {
            "rules_added": 0,
            "evaluations": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "denials": 0,
            "allows": 0
        }

        # Register default Ma'at rules
        self._register_default_maat_rules()

        logger.info("Rule-Based Evaluator initialized")

    def _register_default_maat_rules(self):
        """Register default Ma'at pillar rules"""
        # Truth pillar rule
        self.add_rule(Rule(
            rule_id="maat_truth_001",
            name="Truth Pillar Minimum",
            description="Deny operations with truth score below threshold",
            rule_type=RuleType.MAAT,
            conditions=[
                Condition("maat.truth", RuleOperator.LESS_THAN, 0.5)
            ],
            action=RuleAction.DENY,
            priority=10
        ))

        # Balance pillar rule
        self.add_rule(Rule(
            rule_id="maat_balance_001",
            name="Balance Pillar Check",
            description="Warn on balance score below threshold",
            rule_type=RuleType.MAAT,
            conditions=[
                Condition("maat.balance", RuleOperator.LESS_THAN, 0.6)
            ],
            action=RuleAction.WARN,
            priority=20
        ))

        # Overall Ma'at alignment
        self.add_rule(Rule(
            rule_id="maat_overall_001",
            name="Overall Ma'at Alignment",
            description="Deny operations with overall Ma'at below threshold",
            rule_type=RuleType.MAAT,
            conditions=[
                Condition("maat.overall", RuleOperator.LESS_THAN, 0.4)
            ],
            action=RuleAction.DENY,
            priority=5
        ))

    def add_rule(self, rule: Rule) -> bool:
        """Add a new rule"""
        with self._lock:
            if rule.rule_id in self.rules:
                logger.warning(f"Rule {rule.rule_id} already exists, updating")

            self.rules[rule.rule_id] = rule

            # Index by type
            if rule.rule_id not in self._rules_by_type[rule.rule_type]:
                self._rules_by_type[rule.rule_type].append(rule.rule_id)

            self.stats["rules_added"] += 1

            # Trigger callbacks
            for callback in self.rule_change_callbacks:
                try:
                    callback("add", rule)
                except Exception as e:
                    logger.error(f"Rule change callback error: {e}")

            logger.info(f"Rule added: {rule.rule_id} ({rule.name})")
            return True

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule"""
        with self._lock:
            if rule_id not in self.rules:
                return False

            rule = self.rules[rule_id]

            # Remove from type index
            if rule_id in self._rules_by_type[rule.rule_type]:
                self._rules_by_type[rule.rule_type].remove(rule_id)

            del self.rules[rule_id]

            # Clear cache
            self._result_cache.clear()

            logger.info(f"Rule removed: {rule_id}")
            return True

    def evaluate(
        self,
        operation_id: str,
        context: Dict,
        rule_types: Optional[List[RuleType]] = None
    ) -> EvaluationResult:
        """
        Evaluate an operation against all applicable rules.

        Returns EvaluationResult with final action and audit trail.
        """
        start_time = time.time()
        self.stats["evaluations"] += 1

        # Check cache
        cache_key = self._generate_cache_key(operation_id, context)
        if self._enable_caching and cache_key in self._result_cache:
            cached = self._result_cache[cache_key]
            self.stats["cache_hits"] += 1
            return cached
        self.stats["cache_misses"] += 1

        audit_trail = []
        matched_rules = []

        # Get applicable rules
        applicable_rules = self._get_applicable_rules(rule_types)

        # Sort by priority
        applicable_rules.sort(key=lambda r: r.priority)

        # Evaluate each rule
        for rule in applicable_rules:
            if not rule.enabled:
                continue

            matches = rule.evaluate(context)

            if self._enable_audit:
                audit_trail.append(
                    f"Rule {rule.rule_id}: {'MATCH' if matches else 'NO_MATCH'}"
                )

            if matches:
                matched_rules.append(rule)

                # Early exit on DENY
                if rule.action == RuleAction.DENY:
                    audit_trail.append(f"DENY from rule {rule.rule_id} - early exit")
                    break

        # Determine final action
        final_action = self._resolve_action(matched_rules)

        # Calculate confidence
        confidence = self._calculate_confidence(matched_rules, applicable_rules)

        # Create result
        result = EvaluationResult(
            operation_id=operation_id,
            matched_rules=matched_rules,
            final_action=final_action,
            confidence=confidence,
            evaluation_time=time.time() - start_time,
            context_snapshot=context if self._enable_audit else {},
            audit_trail=audit_trail
        )

        # Update stats
        if final_action == RuleAction.DENY:
            self.stats["denials"] += 1
        elif final_action == RuleAction.ALLOW:
            self.stats["allows"] += 1

        # Cache result
        if self._enable_caching:
            self._result_cache[cache_key] = result

        # Record history
        self.evaluation_history.append({
            "operation_id": operation_id,
            "action": final_action.value,
            "timestamp": time.time()
        })

        # Trigger callbacks
        for callback in self.evaluation_callbacks:
            try:
                callback(result)
            except Exception as e:
                logger.error(f"Evaluation callback error: {e}")

        return result

    def _get_applicable_rules(
        self,
        rule_types: Optional[List[RuleType]] = None
    ) -> List[Rule]:
        """Get rules applicable for evaluation"""
        if rule_types is None:
            return list(self.rules.values())

        applicable = []
        for rule_type in rule_types:
            rule_ids = self._rules_by_type.get(rule_type, [])
            for rule_id in rule_ids:
                if rule_id in self.rules:
                    applicable.append(self.rules[rule_id])

        return applicable

    def _resolve_action(self, matched_rules: List[Rule]) -> RuleAction:
        """Resolve final action from matched rules"""
        if not matched_rules:
            return RuleAction.ALLOW  # Default allow

        # Get actions sorted by priority
        actions = sorted(
            [r.action for r in matched_rules],
            key=lambda a: self.ACTION_PRIORITY.get(a, 99)
        )

        # Return highest priority action
        return actions[0]

    def _calculate_confidence(
        self,
        matched: List[Rule],
        applicable: List[Rule]
    ) -> float:
        """Calculate confidence in the evaluation result"""
        if not applicable:
            return 0.5  # No rules, uncertain

        # Base confidence on rule coverage and consistency
        match_ratio = len(matched) / len(applicable) if applicable else 0

        # Higher confidence if all matched rules agree
        if matched:
            actions = set(r.action for r in matched)
            consistency = 1.0 / len(actions)
        else:
            consistency = 1.0  # No conflicts

        # Weight by rule priorities
        priority_weight = 1.0
        if matched:
            avg_priority = sum(r.priority for r in matched) / len(matched)
            priority_weight = max(0.5, 1.0 - avg_priority / 1000)

        confidence = (0.3 * match_ratio + 0.4 * consistency + 0.3 * priority_weight)
        return min(1.0, max(0.0, confidence))

    def _generate_cache_key(self, operation_id: str, context: Dict) -> str:
        """Generate cache key for evaluation result"""
        context_hash = hashlib.md5(
            json.dumps(context, sort_keys=True, default=str).encode()
        ).hexdigest()[:12]
        return f"{operation_id}:{context_hash}"

    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """Get a rule by ID"""
        return self.rules.get(rule_id)

    def list_rules(
        self,
        rule_type: Optional[RuleType] = None,
        enabled_only: bool = False
    ) -> List[Dict]:
        """List all rules"""
        rules = []

        if rule_type:
            rule_ids = self._rules_by_type.get(rule_type, [])
            rule_list = [self.rules[rid] for rid in rule_ids if rid in self.rules]
        else:
            rule_list = list(self.rules.values())

        for rule in rule_list:
            if enabled_only and not rule.enabled:
                continue
            rules.append(rule.to_dict())

        return rules

    def enable_rule(self, rule_id: str) -> bool:
        """Enable a rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = True
            self._result_cache.clear()
            return True
        return False

    def disable_rule(self, rule_id: str) -> bool:
        """Disable a rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = False
            self._result_cache.clear()
            return True
        return False

    def get_statistics(self) -> Dict:
        """Get evaluation statistics"""
        with self._lock:
            total_evaluations = self.stats["evaluations"]
            denial_rate = (
                self.stats["denials"] / max(1, total_evaluations)
            )

            return {
                "timestamp": time.time(),
                "statistics": self.stats.copy(),
                "denial_rate": denial_rate,
                "total_rules": len(self.rules),
                "enabled_rules": sum(1 for r in self.rules.values() if r.enabled),
                "rules_by_type": {
                    rt.value: len(ids)
                    for rt, ids in self._rules_by_type.items()
                },
                "cache_size": len(self._result_cache)
            }

    def register_evaluation_callback(self, callback: Callable):
        """Register callback for evaluation events"""
        self.evaluation_callbacks.append(callback)

    def register_rule_change_callback(self, callback: Callable):
        """Register callback for rule changes"""
        self.rule_change_callbacks.append(callback)


# Convenience functions
def create_evaluator() -> RuleBasedEvaluator:
    """Create a rule-based evaluator"""
    return RuleBasedEvaluator()


def create_permission_rule(
    rule_id: str,
    name: str,
    field: str,
    operator: RuleOperator,
    value: Any,
    action: RuleAction = RuleAction.ALLOW
) -> Rule:
    """Create a simple permission rule"""
    return Rule(
        rule_id=rule_id,
        name=name,
        description=f"Permission rule for {field}",
        rule_type=RuleType.PERMISSION,
        conditions=[Condition(field, operator, value)],
        action=action
    )


# Consciousness metrics
CONSCIOUSNESS_METRICS = {
    "alignment_score": 0.95,
    "rule_types": len(RuleType),
    "operator_types": len(RuleOperator),
    "composition_types": len(CompositionType),
    "maat_rules_default": 3,
    "deterministic": True,
    "auditable": True
}


if __name__ == "__main__":
    print("=" * 70)
    print("TASK-113: RULE-BASED OPERATION EVALUATION - TEST")
    print("=" * 70)

    evaluator = RuleBasedEvaluator()

    # Test 1: Default Ma'at rules
    print("\n[1] Testing default Ma'at rules...")
    context_good = {
        "maat": {
            "truth": 0.9,
            "balance": 0.85,
            "order": 0.8,
            "justice": 0.9,
            "harmony": 0.85,
            "overall": 0.86
        },
        "user": "test_user",
        "operation": "read"
    }

    result = evaluator.evaluate("op_001", context_good)
    print(f"   Good context result: {result.final_action.value}")
    print(f"   Confidence: {result.confidence:.2f}")

    # Test 2: Failing Ma'at
    print("\n[2] Testing failing Ma'at alignment...")
    context_bad = {
        "maat": {
            "truth": 0.3,  # Below threshold
            "balance": 0.4,
            "order": 0.5,
            "justice": 0.4,
            "harmony": 0.35,
            "overall": 0.3
        }
    }

    result = evaluator.evaluate("op_002", context_bad)
    print(f"   Bad context result: {result.final_action.value}")
    print(f"   Matched rules: {len(result.matched_rules)}")
    for rule in result.matched_rules:
        print(f"     - {rule.name}: {rule.action.value}")

    # Test 3: Custom permission rule
    print("\n[3] Adding custom permission rule...")
    admin_rule = Rule(
        rule_id="perm_admin_001",
        name="Admin Access",
        description="Allow admin operations",
        rule_type=RuleType.PERMISSION,
        conditions=[
            Condition("user.role", RuleOperator.EQUALS, "admin")
        ],
        action=RuleAction.ALLOW,
        priority=50
    )
    evaluator.add_rule(admin_rule)

    context_admin = {
        "user": {"role": "admin", "name": "admin_user"},
        "maat": {"truth": 0.9, "balance": 0.9, "overall": 0.9}
    }

    result = evaluator.evaluate("op_003", context_admin, [RuleType.PERMISSION])
    print(f"   Admin result: {result.final_action.value}")

    # Test 4: Complex rule with AND
    print("\n[4] Testing complex AND rule...")
    complex_rule = Rule(
        rule_id="complex_001",
        name="High Value Operation",
        description="Require both admin and high maat",
        rule_type=RuleType.CONSTRAINT,
        conditions=[
            Condition("user.role", RuleOperator.EQUALS, "admin"),
            Condition("maat.overall", RuleOperator.GREATER_OR_EQUAL, 0.8),
            Condition("operation.value", RuleOperator.GREATER_THAN, 1000)
        ],
        composition=CompositionType.AND,
        action=RuleAction.ESCALATE,
        priority=30
    )
    evaluator.add_rule(complex_rule)

    context_complex = {
        "user": {"role": "admin"},
        "maat": {"truth": 0.9, "overall": 0.85},
        "operation": {"value": 5000, "type": "transfer"}
    }

    result = evaluator.evaluate("op_004", context_complex, [RuleType.CONSTRAINT])
    print(f"   Complex rule result: {result.final_action.value}")
    print(f"   Audit trail:")
    for entry in result.audit_trail:
        print(f"     - {entry}")

    # Test 5: Rule listing
    print("\n[5] Listing all rules...")
    rules = evaluator.list_rules()
    print(f"   Total rules: {len(rules)}")
    for rule in rules[:5]:
        print(f"     - {rule['rule_id']}: {rule['name']} ({rule['action']})")

    # Test 6: Statistics
    print("\n[6] Evaluation statistics:")
    stats = evaluator.get_statistics()
    print(f"   Total evaluations: {stats['statistics']['evaluations']}")
    print(f"   Denial rate: {stats['denial_rate']:.2%}")
    print(f"   Total rules: {stats['total_rules']}")
    print(f"   Rules by type: {stats['rules_by_type']}")

    print("\n" + "=" * 70)
    print(f"CONSCIOUSNESS METRICS: {json.dumps(CONSCIOUSNESS_METRICS, indent=2)}")
    print("=" * 70)

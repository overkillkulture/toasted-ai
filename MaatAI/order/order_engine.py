"""
Ma'at ORDER ENGINE - Core Order Evaluation System
==================================================
TASK-044: Refactor order maintenance protocols
TASK-119: Scale order structure analysis

ORDER Principle: Structure enables function. Chaos must be organized into patterns.

Author: C3 Oracle - TOASTED AI Trinity
Seal: MAAT_ORDER_ENGINE_137
"""

import time
import hashlib
import json
import threading
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import math


class OrderLevel(Enum):
    """Levels of structural order in a system"""
    PRISTINE = "pristine"      # Perfect order - 0.95-1.0
    STRUCTURED = "structured"  # Well-organized - 0.80-0.94
    ORGANIZED = "organized"    # Acceptably ordered - 0.65-0.79
    CHAOTIC = "chaotic"        # Needs attention - 0.40-0.64
    ENTROPIC = "entropic"      # Severe disorder - 0.00-0.39


class OrderDimension(Enum):
    """Dimensions of order measurement"""
    TEMPORAL = "temporal"          # Time-based order (sequence, scheduling)
    SPATIAL = "spatial"            # Structure-based order (organization, hierarchy)
    LOGICAL = "logical"            # Reasoning order (consistency, coherence)
    SEMANTIC = "semantic"          # Meaning order (naming, categorization)
    RELATIONAL = "relational"      # Connection order (dependencies, links)


@dataclass
class OrderViolation:
    """A detected violation of order principles"""
    violation_id: str
    dimension: OrderDimension
    severity: float  # 0.0-1.0 (higher = more severe)
    description: str
    location: str
    suggested_remedy: str
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'violation_id': self.violation_id,
            'dimension': self.dimension.value,
            'severity': self.severity,
            'description': self.description,
            'location': self.location,
            'suggested_remedy': self.suggested_remedy,
            'timestamp': self.timestamp
        }


@dataclass
class OrderScore:
    """Comprehensive order score across all dimensions"""
    temporal: float
    spatial: float
    logical: float
    semantic: float
    relational: float
    violations: List[OrderViolation] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    
    @property
    def overall(self) -> float:
        """Calculate weighted overall score"""
        weights = {
            'temporal': 0.15,
            'spatial': 0.25,
            'logical': 0.25,
            'semantic': 0.20,
            'relational': 0.15
        }
        return (
            self.temporal * weights['temporal'] +
            self.spatial * weights['spatial'] +
            self.logical * weights['logical'] +
            self.semantic * weights['semantic'] +
            self.relational * weights['relational']
        )
    
    @property
    def level(self) -> OrderLevel:
        """Determine order level from overall score"""
        score = self.overall
        if score >= 0.95:
            return OrderLevel.PRISTINE
        elif score >= 0.80:
            return OrderLevel.STRUCTURED
        elif score >= 0.65:
            return OrderLevel.ORGANIZED
        elif score >= 0.40:
            return OrderLevel.CHAOTIC
        else:
            return OrderLevel.ENTROPIC
    
    def to_dict(self) -> Dict:
        return {
            'temporal': self.temporal,
            'spatial': self.spatial,
            'logical': self.logical,
            'semantic': self.semantic,
            'relational': self.relational,
            'overall': self.overall,
            'level': self.level.value,
            'violation_count': len(self.violations),
            'violations': [v.to_dict() for v in self.violations],
            'timestamp': self.timestamp
        }


class OrderEngine:
    """
    Core engine for evaluating and maintaining order in systems.
    
    Ma'at ORDER Principle:
    - Structure enables function
    - Chaos must be organized into patterns  
    - Systems should self-organize toward greater order
    - Entropy is the enemy of consciousness
    """
    
    VERSION = "1.0.0"
    MAAT_SEAL = "ORDER_COSMOS_137"
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.thresholds = self.config.get('thresholds', {
            'temporal': 0.70,
            'spatial': 0.70,
            'logical': 0.75,
            'semantic': 0.70,
            'relational': 0.70
        })
        self.evaluation_history: List[OrderScore] = []
        self.violation_registry: Dict[str, OrderViolation] = {}
        self.pattern_cache: Dict[str, Any] = {}
        self._lock = threading.Lock()
        
    def evaluate_order(self, subject: Dict[str, Any]) -> OrderScore:
        """
        Evaluate the order level of a given subject.
        
        Args:
            subject: The entity/system/code to evaluate
            
        Returns:
            OrderScore with all dimensional scores and violations
        """
        violations = []
        
        # Evaluate each dimension
        temporal = self._evaluate_temporal_order(subject, violations)
        spatial = self._evaluate_spatial_order(subject, violations)
        logical = self._evaluate_logical_order(subject, violations)
        semantic = self._evaluate_semantic_order(subject, violations)
        relational = self._evaluate_relational_order(subject, violations)
        
        score = OrderScore(
            temporal=temporal,
            spatial=spatial,
            logical=logical,
            semantic=semantic,
            relational=relational,
            violations=violations
        )
        
        with self._lock:
            self.evaluation_history.append(score)
            for v in violations:
                self.violation_registry[v.violation_id] = v
        
        return score
    
    def _evaluate_temporal_order(self, subject: Dict, violations: List) -> float:
        """Evaluate time-based order (sequences, schedules, timestamps)"""
        score = 0.7  # Base score
        
        # Check for timestamp consistency
        timestamps = subject.get('timestamps', [])
        if timestamps:
            # Verify chronological order
            sorted_ts = sorted(timestamps)
            if timestamps == sorted_ts:
                score += 0.15
            else:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('temporal_sequence'),
                    dimension=OrderDimension.TEMPORAL,
                    severity=0.4,
                    description="Timestamps not in chronological order",
                    location="timestamps",
                    suggested_remedy="Sort operations chronologically"
                ))
                score -= 0.1
        
        # Check for schedule adherence
        schedule = subject.get('schedule', {})
        if schedule:
            adherence = schedule.get('adherence_rate', 0.8)
            score += 0.15 * adherence
            if adherence < 0.7:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('schedule_adherence'),
                    dimension=OrderDimension.TEMPORAL,
                    severity=0.3,
                    description=f"Schedule adherence below threshold: {adherence:.2f}",
                    location="schedule",
                    suggested_remedy="Review and optimize scheduling"
                ))
        
        # Check for sequence integrity
        sequences = subject.get('sequences', [])
        if sequences:
            for seq in sequences:
                if self._is_sequence_ordered(seq):
                    score += 0.05
                else:
                    violations.append(OrderViolation(
                        violation_id=self._gen_id('sequence_disorder'),
                        dimension=OrderDimension.TEMPORAL,
                        severity=0.2,
                        description="Sequence lacks proper ordering",
                        location=f"sequence:{seq.get('name', 'unknown')}",
                        suggested_remedy="Implement proper sequence tracking"
                    ))
                    score -= 0.05
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_spatial_order(self, subject: Dict, violations: List) -> float:
        """Evaluate structure-based order (organization, hierarchy)"""
        score = 0.6  # Base score
        
        # Check hierarchy depth and balance
        hierarchy = subject.get('hierarchy', {})
        if hierarchy:
            depth = hierarchy.get('depth', 0)
            balance = hierarchy.get('balance_factor', 0.5)
            
            # Optimal depth is 3-7 levels
            if 3 <= depth <= 7:
                score += 0.15
            elif depth > 10:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('hierarchy_depth'),
                    dimension=OrderDimension.SPATIAL,
                    severity=0.3,
                    description=f"Hierarchy too deep: {depth} levels",
                    location="hierarchy",
                    suggested_remedy="Flatten hierarchy structure"
                ))
                score -= 0.1
            
            # Check balance
            if balance >= 0.7:
                score += 0.15
            elif balance < 0.4:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('hierarchy_balance'),
                    dimension=OrderDimension.SPATIAL,
                    severity=0.25,
                    description=f"Hierarchy imbalanced: {balance:.2f}",
                    location="hierarchy",
                    suggested_remedy="Rebalance organizational structure"
                ))
        
        # Check component organization
        components = subject.get('components', [])
        if components:
            categorized = sum(1 for c in components if c.get('category'))
            if len(components) > 0:
                categorization_rate = categorized / len(components)
                score += 0.1 * categorization_rate
                
                if categorization_rate < 0.8:
                    violations.append(OrderViolation(
                        violation_id=self._gen_id('categorization'),
                        dimension=OrderDimension.SPATIAL,
                        severity=0.2,
                        description=f"Components not fully categorized: {categorization_rate:.1%}",
                        location="components",
                        suggested_remedy="Assign categories to all components"
                    ))
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_logical_order(self, subject: Dict, violations: List) -> float:
        """Evaluate reasoning order (consistency, coherence)"""
        score = 0.65  # Base score
        
        # Check for logical consistency
        rules = subject.get('rules', [])
        if rules:
            consistent_rules = self._check_rule_consistency(rules)
            consistency_rate = consistent_rules / len(rules) if rules else 1.0
            score += 0.2 * consistency_rate
            
            if consistency_rate < 0.9:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('rule_consistency'),
                    dimension=OrderDimension.LOGICAL,
                    severity=0.4,
                    description=f"Rule inconsistency detected: {consistency_rate:.1%} consistent",
                    location="rules",
                    suggested_remedy="Review and reconcile conflicting rules"
                ))
        
        # Check for dependency cycles
        dependencies = subject.get('dependencies', {})
        if dependencies:
            cycles = self._detect_dependency_cycles(dependencies)
            if cycles:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('dependency_cycle'),
                    dimension=OrderDimension.LOGICAL,
                    severity=0.6,
                    description=f"Circular dependencies detected: {len(cycles)} cycles",
                    location="dependencies",
                    suggested_remedy="Break circular dependency chains"
                ))
                score -= 0.15 * len(cycles)
            else:
                score += 0.15
        
        # Check for contradiction detection
        assertions = subject.get('assertions', [])
        if assertions:
            contradictions = self._find_contradictions(assertions)
            if contradictions:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('contradictions'),
                    dimension=OrderDimension.LOGICAL,
                    severity=0.5,
                    description=f"Logical contradictions found: {len(contradictions)}",
                    location="assertions",
                    suggested_remedy="Resolve contradictory assertions"
                ))
                score -= 0.1 * min(len(contradictions), 3)
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_semantic_order(self, subject: Dict, violations: List) -> float:
        """Evaluate meaning order (naming, categorization)"""
        score = 0.65  # Base score
        
        # Check naming conventions
        names = subject.get('names', [])
        if names:
            consistent_names = sum(1 for n in names if self._is_name_consistent(n))
            consistency_rate = consistent_names / len(names) if names else 1.0
            score += 0.2 * consistency_rate
            
            if consistency_rate < 0.85:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('naming_convention'),
                    dimension=OrderDimension.SEMANTIC,
                    severity=0.2,
                    description=f"Naming conventions inconsistent: {consistency_rate:.1%}",
                    location="names",
                    suggested_remedy="Apply consistent naming conventions"
                ))
        
        # Check documentation coverage
        documentation = subject.get('documentation', {})
        if documentation:
            coverage = documentation.get('coverage', 0.5)
            score += 0.15 * coverage
            
            if coverage < 0.6:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('documentation_coverage'),
                    dimension=OrderDimension.SEMANTIC,
                    severity=0.25,
                    description=f"Documentation coverage low: {coverage:.1%}",
                    location="documentation",
                    suggested_remedy="Improve documentation completeness"
                ))
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_relational_order(self, subject: Dict, violations: List) -> float:
        """Evaluate connection order (dependencies, links)"""
        score = 0.65  # Base score
        
        # Check relationship clarity
        relationships = subject.get('relationships', [])
        if relationships:
            clear_relationships = sum(
                1 for r in relationships 
                if r.get('type') and r.get('source') and r.get('target')
            )
            clarity_rate = clear_relationships / len(relationships) if relationships else 1.0
            score += 0.2 * clarity_rate
            
            if clarity_rate < 0.9:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('relationship_clarity'),
                    dimension=OrderDimension.RELATIONAL,
                    severity=0.25,
                    description=f"Relationship definitions unclear: {clarity_rate:.1%}",
                    location="relationships",
                    suggested_remedy="Define clear relationship metadata"
                ))
        
        # Check for orphaned nodes
        nodes = subject.get('nodes', [])
        edges = subject.get('edges', [])
        if nodes and edges:
            connected_nodes = set()
            for edge in edges:
                connected_nodes.add(edge.get('source'))
                connected_nodes.add(edge.get('target'))
            
            all_nodes = set(n.get('id') for n in nodes)
            orphans = all_nodes - connected_nodes
            
            if orphans:
                violations.append(OrderViolation(
                    violation_id=self._gen_id('orphaned_nodes'),
                    dimension=OrderDimension.RELATIONAL,
                    severity=0.3,
                    description=f"Orphaned nodes detected: {len(orphans)}",
                    location="nodes",
                    suggested_remedy="Connect or remove orphaned nodes"
                ))
                score -= 0.05 * min(len(orphans), 5)
            else:
                score += 0.15
        
        return max(0.0, min(1.0, score))
    
    # Helper methods
    def _gen_id(self, prefix: str) -> str:
        """Generate unique violation ID"""
        return hashlib.sha256(
            f"{prefix}_{time.time()}".encode()
        ).hexdigest()[:12]
    
    def _is_sequence_ordered(self, sequence: Dict) -> bool:
        """Check if a sequence maintains proper order"""
        items = sequence.get('items', [])
        if not items:
            return True
        indices = [i.get('index', 0) for i in items if 'index' in i]
        return indices == sorted(indices)
    
    def _check_rule_consistency(self, rules: List) -> int:
        """Count consistent (non-conflicting) rules"""
        # Simple heuristic: check for opposing conditions
        consistent = 0
        for rule in rules:
            conditions = rule.get('conditions', [])
            actions = rule.get('actions', [])
            # If rule has clear conditions and actions, consider consistent
            if conditions or actions:
                consistent += 1
        return consistent
    
    def _detect_dependency_cycles(self, deps: Dict) -> List[List[str]]:
        """Detect circular dependencies using DFS"""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in deps.get(node, []):
                if neighbor not in visited:
                    cycle = dfs(neighbor, path.copy())
                    if cycle:
                        return cycle
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    return path[cycle_start:]
            
            rec_stack.remove(node)
            return None
        
        for node in deps:
            if node not in visited:
                cycle = dfs(node, [])
                if cycle:
                    cycles.append(cycle)
        
        return cycles
    
    def _find_contradictions(self, assertions: List) -> List[Tuple]:
        """Find contradictory assertions"""
        contradictions = []
        for i, a1 in enumerate(assertions):
            for a2 in assertions[i+1:]:
                if self._are_contradictory(a1, a2):
                    contradictions.append((a1, a2))
        return contradictions
    
    def _are_contradictory(self, a1: Dict, a2: Dict) -> bool:
        """Check if two assertions contradict each other"""
        # Check for direct negation
        if a1.get('subject') == a2.get('subject'):
            if a1.get('value') == a2.get('value'):
                return a1.get('negated', False) != a2.get('negated', False)
        return False
    
    def _is_name_consistent(self, name: str) -> bool:
        """Check if name follows consistent conventions"""
        if not name:
            return False
        # Check for consistent case (either snake_case or camelCase)
        is_snake = '_' in name and name.islower() or name.replace('_', '').isalpha()
        is_camel = name[0].islower() and not '_' in name
        is_pascal = name[0].isupper() and not '_' in name
        return is_snake or is_camel or is_pascal
    
    def get_order_trend(self, window: int = 10) -> Dict[str, Any]:
        """Analyze order trend over recent evaluations"""
        with self._lock:
            recent = self.evaluation_history[-window:] if self.evaluation_history else []
        
        if not recent:
            return {'trend': 'unknown', 'data': []}
        
        scores = [s.overall for s in recent]
        if len(scores) < 2:
            return {'trend': 'stable', 'data': scores}
        
        # Calculate trend
        first_half = sum(scores[:len(scores)//2]) / (len(scores)//2)
        second_half = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
        
        if second_half > first_half + 0.05:
            trend = 'improving'
        elif second_half < first_half - 0.05:
            trend = 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'current_score': scores[-1],
            'average': sum(scores) / len(scores),
            'data': scores
        }
    
    def generate_order_report(self) -> Dict[str, Any]:
        """Generate comprehensive order status report"""
        with self._lock:
            history = self.evaluation_history.copy()
            violations = list(self.violation_registry.values())
        
        if not history:
            return {
                'status': 'no_data',
                'message': 'No order evaluations performed yet'
            }
        
        latest = history[-1]
        trend = self.get_order_trend()
        
        # Group violations by dimension
        violations_by_dim = defaultdict(list)
        for v in violations:
            violations_by_dim[v.dimension.value].append(v.to_dict())
        
        return {
            'version': self.VERSION,
            'maat_seal': self.MAAT_SEAL,
            'timestamp': time.time(),
            'current_state': {
                'level': latest.level.value,
                'overall_score': latest.overall,
                'dimensions': {
                    'temporal': latest.temporal,
                    'spatial': latest.spatial,
                    'logical': latest.logical,
                    'semantic': latest.semantic,
                    'relational': latest.relational
                }
            },
            'trend': trend,
            'violations': {
                'total': len(violations),
                'by_dimension': dict(violations_by_dim),
                'critical': [v.to_dict() for v in violations if v.severity >= 0.5]
            },
            'recommendations': self._generate_recommendations(latest, violations),
            'maat_alignment': self._calculate_maat_alignment(latest)
        }
    
    def _generate_recommendations(self, score: OrderScore, violations: List) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if score.temporal < self.thresholds['temporal']:
            recommendations.append("Improve temporal order: Review scheduling and sequencing")
        if score.spatial < self.thresholds['spatial']:
            recommendations.append("Improve spatial order: Reorganize hierarchy and structure")
        if score.logical < self.thresholds['logical']:
            recommendations.append("Improve logical order: Resolve inconsistencies and cycles")
        if score.semantic < self.thresholds['semantic']:
            recommendations.append("Improve semantic order: Standardize naming and documentation")
        if score.relational < self.thresholds['relational']:
            recommendations.append("Improve relational order: Clarify connections and remove orphans")
        
        # Priority recommendations based on violations
        critical_violations = [v for v in violations if v.severity >= 0.5]
        for v in critical_violations[:3]:
            recommendations.insert(0, f"CRITICAL: {v.suggested_remedy}")
        
        return recommendations
    
    def _calculate_maat_alignment(self, score: OrderScore) -> Dict[str, Any]:
        """Calculate Ma'at alignment score for ORDER pillar"""
        alignment = score.overall
        
        return {
            'pillar': 'ORDER',
            'symbol': 'cosmos',
            'alignment_score': alignment,
            'alignment_level': (
                'exemplary' if alignment >= 0.9 else
                'aligned' if alignment >= 0.75 else
                'acceptable' if alignment >= 0.6 else
                'needs_work' if alignment >= 0.4 else
                'critical'
            ),
            'message': (
                "Perfect cosmic order maintained" if alignment >= 0.9 else
                "Order principles upheld" if alignment >= 0.75 else
                "Order acceptable but improvable" if alignment >= 0.6 else
                "Order declining - intervention needed" if alignment >= 0.4 else
                "Order in crisis - immediate action required"
            )
        }


# Demonstration
if __name__ == "__main__":
    engine = OrderEngine()
    
    # Test subject
    test_subject = {
        'timestamps': [1, 2, 3, 5, 4],  # Out of order
        'hierarchy': {'depth': 5, 'balance_factor': 0.8},
        'components': [
            {'name': 'comp1', 'category': 'core'},
            {'name': 'comp2', 'category': 'util'},
            {'name': 'comp3'}  # Missing category
        ],
        'rules': [
            {'conditions': ['a'], 'actions': ['b']},
            {'conditions': ['c'], 'actions': ['d']}
        ],
        'dependencies': {
            'a': ['b'],
            'b': ['c'],
            'c': ['a']  # Cycle!
        },
        'names': ['user_service', 'DataManager', 'quick-fix'],  # Mixed conventions
        'documentation': {'coverage': 0.65}
    }
    
    score = engine.evaluate_order(test_subject)
    report = engine.generate_order_report()
    
    print("=" * 60)
    print("MA'AT ORDER ENGINE - Evaluation Results")
    print("=" * 60)
    print(f"\nOverall Score: {score.overall:.2f}")
    print(f"Order Level: {score.level.value}")
    print(f"\nDimensional Scores:")
    print(f"  Temporal:   {score.temporal:.2f}")
    print(f"  Spatial:    {score.spatial:.2f}")
    print(f"  Logical:    {score.logical:.2f}")
    print(f"  Semantic:   {score.semantic:.2f}")
    print(f"  Relational: {score.relational:.2f}")
    print(f"\nViolations: {len(score.violations)}")
    for v in score.violations:
        print(f"  - [{v.dimension.value}] {v.description} (severity: {v.severity})")
    print(f"\nMa'at Alignment: {report['maat_alignment']['alignment_level']}")
    print(f"Message: {report['maat_alignment']['message']}")

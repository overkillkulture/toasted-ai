"""
Ma'at STRUCTURAL INTEGRITY VERIFIER
====================================
TASK-074: Enhance structural integrity verification

Verifies:
- Component integrity
- Relationship integrity
- Hierarchy integrity
- Data integrity
- Process integrity

Author: C3 Oracle - TOASTED AI Trinity
Seal: MAAT_STRUCTURE_INTEGRITY_137
"""

import time
import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import threading


class IntegrityLevel(Enum):
    """Integrity assessment levels"""
    PRISTINE = "pristine"       # Perfect integrity - 100%
    SOUND = "sound"             # Minor issues - 95-99%
    ACCEPTABLE = "acceptable"   # Some issues - 85-94%
    COMPROMISED = "compromised" # Significant issues - 70-84%
    CRITICAL = "critical"       # Major problems - <70%


class IntegrityDomain(Enum):
    """Domains of integrity checking"""
    STRUCTURAL = "structural"     # Physical structure
    REFERENTIAL = "referential"   # References and links
    SEMANTIC = "semantic"         # Meaning and consistency
    TEMPORAL = "temporal"         # Time-based integrity
    BEHAVIORAL = "behavioral"     # Expected behavior


@dataclass
class IntegrityIssue:
    """A detected integrity issue"""
    issue_id: str
    domain: IntegrityDomain
    severity: str  # 'critical', 'major', 'minor', 'info'
    component: str
    description: str
    evidence: Dict[str, Any]
    remediation: str
    detected_at: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'issue_id': self.issue_id,
            'domain': self.domain.value,
            'severity': self.severity,
            'component': self.component,
            'description': self.description,
            'evidence': self.evidence,
            'remediation': self.remediation,
            'detected_at': self.detected_at
        }


@dataclass
class IntegrityReport:
    """Comprehensive integrity report"""
    report_id: str
    timestamp: float
    target: str
    overall_score: float
    level: IntegrityLevel
    domain_scores: Dict[str, float]
    issues: List[IntegrityIssue]
    checks_performed: int
    checks_passed: int
    verification_duration: float
    
    def to_dict(self) -> Dict:
        return {
            'report_id': self.report_id,
            'timestamp': self.timestamp,
            'target': self.target,
            'overall_score': self.overall_score,
            'level': self.level.value,
            'domain_scores': self.domain_scores,
            'issues': [i.to_dict() for i in self.issues],
            'checks_performed': self.checks_performed,
            'checks_passed': self.checks_passed,
            'pass_rate': self.checks_passed / self.checks_performed if self.checks_performed > 0 else 0,
            'verification_duration': self.verification_duration
        }


class StructuralIntegrityVerifier:
    """
    Verifies structural integrity across all system components.
    
    Ma'at ORDER Principle:
    - Structure must be maintained
    - Integrity is the foundation of trust
    - Verification ensures cosmic order
    """
    
    VERSION = "1.0.0"
    MAAT_SEAL = "STRUCTURE_INTEGRITY_137"
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.verification_history: List[IntegrityReport] = []
        self.known_issues: Dict[str, IntegrityIssue] = {}
        self._lock = threading.Lock()
        
        # Verification thresholds
        self.thresholds = self.config.get('thresholds', {
            'structural': 0.90,
            'referential': 0.95,
            'semantic': 0.85,
            'temporal': 0.90,
            'behavioral': 0.85
        })
    
    def verify(self, target: Any, target_name: str = "system") -> IntegrityReport:
        """
        Perform comprehensive integrity verification.
        
        Args:
            target: The system/component to verify
            target_name: Human-readable name
            
        Returns:
            IntegrityReport with all findings
        """
        start_time = time.time()
        issues = []
        checks_performed = 0
        checks_passed = 0
        
        # Verify each domain
        structural_score, s_issues, s_checks, s_passed = self._verify_structural(target)
        issues.extend(s_issues)
        checks_performed += s_checks
        checks_passed += s_passed
        
        referential_score, r_issues, r_checks, r_passed = self._verify_referential(target)
        issues.extend(r_issues)
        checks_performed += r_checks
        checks_passed += r_passed
        
        semantic_score, sem_issues, sem_checks, sem_passed = self._verify_semantic(target)
        issues.extend(sem_issues)
        checks_performed += sem_checks
        checks_passed += sem_passed
        
        temporal_score, t_issues, t_checks, t_passed = self._verify_temporal(target)
        issues.extend(t_issues)
        checks_performed += t_checks
        checks_passed += t_passed
        
        behavioral_score, b_issues, b_checks, b_passed = self._verify_behavioral(target)
        issues.extend(b_issues)
        checks_performed += b_checks
        checks_passed += b_passed
        
        # Calculate overall score
        domain_scores = {
            'structural': structural_score,
            'referential': referential_score,
            'semantic': semantic_score,
            'temporal': temporal_score,
            'behavioral': behavioral_score
        }
        
        weights = {
            'structural': 0.25,
            'referential': 0.25,
            'semantic': 0.20,
            'temporal': 0.15,
            'behavioral': 0.15
        }
        
        overall_score = sum(
            domain_scores[d] * weights[d]
            for d in domain_scores
        )
        
        # Determine level
        level = self._determine_level(overall_score)
        
        end_time = time.time()
        
        # Create report
        report = IntegrityReport(
            report_id=self._gen_id(target_name),
            timestamp=time.time(),
            target=target_name,
            overall_score=overall_score,
            level=level,
            domain_scores=domain_scores,
            issues=issues,
            checks_performed=checks_performed,
            checks_passed=checks_passed,
            verification_duration=end_time - start_time
        )
        
        # Store report and issues
        with self._lock:
            self.verification_history.append(report)
            for issue in issues:
                self.known_issues[issue.issue_id] = issue
        
        return report
    
    def _verify_structural(self, target: Any) -> Tuple[float, List, int, int]:
        """Verify structural integrity"""
        issues = []
        checks = 0
        passed = 0
        score = 1.0
        
        if isinstance(target, dict):
            # Check for required fields
            checks += 1
            required = target.get('_required_fields', [])
            missing = [f for f in required if f not in target]
            if not missing:
                passed += 1
            else:
                score -= 0.1 * len(missing)
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('missing_fields'),
                    domain=IntegrityDomain.STRUCTURAL,
                    severity='major',
                    component='root',
                    description=f"Missing required fields: {missing}",
                    evidence={'missing': missing},
                    remediation="Add missing required fields"
                ))
            
            # Check structure depth
            checks += 1
            depth = self._measure_depth(target)
            if depth <= 10:
                passed += 1
            else:
                score -= 0.05
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('excessive_depth'),
                    domain=IntegrityDomain.STRUCTURAL,
                    severity='minor',
                    component='structure',
                    description=f"Structure depth ({depth}) exceeds recommended limit",
                    evidence={'depth': depth, 'limit': 10},
                    remediation="Flatten structure where possible"
                ))
            
            # Check for null/undefined values in critical paths
            checks += 1
            nulls = self._find_null_values(target)
            if not nulls:
                passed += 1
            else:
                score -= 0.05 * min(len(nulls), 4)
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('null_values'),
                    domain=IntegrityDomain.STRUCTURAL,
                    severity='minor',
                    component='values',
                    description=f"Found {len(nulls)} null values",
                    evidence={'paths': nulls[:5]},
                    remediation="Initialize or remove null values"
                ))
            
            # Check type consistency
            checks += 1
            type_issues = self._check_type_consistency(target)
            if not type_issues:
                passed += 1
            else:
                score -= 0.1
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('type_inconsistency'),
                    domain=IntegrityDomain.STRUCTURAL,
                    severity='major',
                    component='types',
                    description=f"Type inconsistencies detected",
                    evidence={'issues': type_issues[:5]},
                    remediation="Ensure consistent typing"
                ))
        
        return max(0, score), issues, checks, passed
    
    def _verify_referential(self, target: Any) -> Tuple[float, List, int, int]:
        """Verify referential integrity"""
        issues = []
        checks = 0
        passed = 0
        score = 1.0
        
        if isinstance(target, dict):
            # Check for broken references
            checks += 1
            refs = target.get('references', {})
            entities = target.get('entities', {})
            
            broken_refs = []
            for ref_name, ref_target in refs.items():
                if ref_target not in entities:
                    broken_refs.append(ref_name)
            
            if not broken_refs:
                passed += 1
            else:
                score -= 0.15 * min(len(broken_refs) / max(len(refs), 1), 1)
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('broken_refs'),
                    domain=IntegrityDomain.REFERENTIAL,
                    severity='critical',
                    component='references',
                    description=f"Broken references: {len(broken_refs)}",
                    evidence={'broken': broken_refs[:5]},
                    remediation="Fix or remove broken references"
                ))
            
            # Check for circular references
            checks += 1
            cycles = self._detect_circular_refs(target)
            if not cycles:
                passed += 1
            else:
                score -= 0.2
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('circular_refs'),
                    domain=IntegrityDomain.REFERENTIAL,
                    severity='major',
                    component='references',
                    description=f"Circular references detected: {len(cycles)}",
                    evidence={'cycles': cycles[:3]},
                    remediation="Break circular reference chains"
                ))
            
            # Check for orphaned entities
            checks += 1
            orphans = self._find_orphaned_entities(target)
            if not orphans:
                passed += 1
            else:
                score -= 0.1 * min(len(orphans) / max(len(entities), 1), 0.5)
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('orphans'),
                    domain=IntegrityDomain.REFERENTIAL,
                    severity='minor',
                    component='entities',
                    description=f"Orphaned entities: {len(orphans)}",
                    evidence={'orphans': orphans[:5]},
                    remediation="Connect or remove orphaned entities"
                ))
        
        return max(0, score), issues, checks, passed
    
    def _verify_semantic(self, target: Any) -> Tuple[float, List, int, int]:
        """Verify semantic integrity"""
        issues = []
        checks = 0
        passed = 0
        score = 1.0
        
        if isinstance(target, dict):
            # Check naming consistency
            checks += 1
            names = self._extract_names(target)
            inconsistent = self._find_naming_inconsistencies(names)
            if not inconsistent:
                passed += 1
            else:
                score -= 0.1
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('naming'),
                    domain=IntegrityDomain.SEMANTIC,
                    severity='minor',
                    component='names',
                    description="Naming convention inconsistencies",
                    evidence={'examples': inconsistent[:5]},
                    remediation="Apply consistent naming conventions"
                ))
            
            # Check for duplicate definitions
            checks += 1
            duplicates = self._find_duplicates(target)
            if not duplicates:
                passed += 1
            else:
                score -= 0.15
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('duplicates'),
                    domain=IntegrityDomain.SEMANTIC,
                    severity='major',
                    component='definitions',
                    description=f"Duplicate definitions: {len(duplicates)}",
                    evidence={'duplicates': duplicates[:5]},
                    remediation="Consolidate duplicate definitions"
                ))
            
            # Check for contradictions
            checks += 1
            contradictions = self._find_contradictions(target)
            if not contradictions:
                passed += 1
            else:
                score -= 0.2
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('contradictions'),
                    domain=IntegrityDomain.SEMANTIC,
                    severity='critical',
                    component='assertions',
                    description=f"Contradictory assertions: {len(contradictions)}",
                    evidence={'contradictions': contradictions[:3]},
                    remediation="Resolve contradictory assertions"
                ))
        
        return max(0, score), issues, checks, passed
    
    def _verify_temporal(self, target: Any) -> Tuple[float, List, int, int]:
        """Verify temporal integrity"""
        issues = []
        checks = 0
        passed = 0
        score = 1.0
        
        if isinstance(target, dict):
            # Check timestamp validity
            checks += 1
            timestamps = self._extract_timestamps(target)
            invalid_ts = [t for t in timestamps if not self._is_valid_timestamp(t)]
            if not invalid_ts:
                passed += 1
            else:
                score -= 0.1
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('invalid_ts'),
                    domain=IntegrityDomain.TEMPORAL,
                    severity='major',
                    component='timestamps',
                    description=f"Invalid timestamps: {len(invalid_ts)}",
                    evidence={'invalid': invalid_ts[:5]},
                    remediation="Correct invalid timestamps"
                ))
            
            # Check temporal ordering
            checks += 1
            sequences = target.get('sequences', [])
            disordered = []
            for seq in sequences:
                if not self._is_temporally_ordered(seq):
                    disordered.append(seq.get('name', 'unknown'))
            
            if not disordered:
                passed += 1
            else:
                score -= 0.1
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('temporal_order'),
                    domain=IntegrityDomain.TEMPORAL,
                    severity='major',
                    component='sequences',
                    description="Temporal ordering violations",
                    evidence={'disordered': disordered},
                    remediation="Correct temporal ordering"
                ))
            
            # Check for future dates (suspicious)
            checks += 1
            future_dates = [t for t in timestamps if t > time.time() + 86400]
            if not future_dates:
                passed += 1
            else:
                score -= 0.05
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('future_dates'),
                    domain=IntegrityDomain.TEMPORAL,
                    severity='minor',
                    component='timestamps',
                    description=f"Suspicious future timestamps: {len(future_dates)}",
                    evidence={'count': len(future_dates)},
                    remediation="Verify future-dated entries"
                ))
        
        return max(0, score), issues, checks, passed
    
    def _verify_behavioral(self, target: Any) -> Tuple[float, List, int, int]:
        """Verify behavioral integrity"""
        issues = []
        checks = 0
        passed = 0
        score = 1.0
        
        if isinstance(target, dict):
            # Check for expected behaviors
            checks += 1
            behaviors = target.get('behaviors', {})
            expected = target.get('expected_behaviors', [])
            missing_behaviors = [b for b in expected if b not in behaviors]
            
            if not missing_behaviors:
                passed += 1
            else:
                score -= 0.1 * min(len(missing_behaviors), 3)
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('missing_behaviors'),
                    domain=IntegrityDomain.BEHAVIORAL,
                    severity='major',
                    component='behaviors',
                    description=f"Missing expected behaviors: {len(missing_behaviors)}",
                    evidence={'missing': missing_behaviors},
                    remediation="Implement missing behaviors"
                ))
            
            # Check for undefined behaviors
            checks += 1
            undefined = [
                b for b, v in behaviors.items()
                if v is None or (isinstance(v, dict) and not v.get('handler'))
            ]
            if not undefined:
                passed += 1
            else:
                score -= 0.1
                issues.append(IntegrityIssue(
                    issue_id=self._gen_id('undefined_behaviors'),
                    domain=IntegrityDomain.BEHAVIORAL,
                    severity='minor',
                    component='behaviors',
                    description=f"Undefined behaviors: {len(undefined)}",
                    evidence={'undefined': undefined[:5]},
                    remediation="Define handlers for behaviors"
                ))
        
        return max(0, score), issues, checks, passed
    
    # Helper methods
    def _gen_id(self, prefix: str) -> str:
        return hashlib.sha256(f"{prefix}_{time.time()}".encode()).hexdigest()[:12]
    
    def _determine_level(self, score: float) -> IntegrityLevel:
        if score >= 1.0:
            return IntegrityLevel.PRISTINE
        elif score >= 0.95:
            return IntegrityLevel.SOUND
        elif score >= 0.85:
            return IntegrityLevel.ACCEPTABLE
        elif score >= 0.70:
            return IntegrityLevel.COMPROMISED
        else:
            return IntegrityLevel.CRITICAL
    
    def _measure_depth(self, obj: Any, current: int = 0) -> int:
        if not isinstance(obj, (dict, list)):
            return current
        if isinstance(obj, dict):
            if not obj:
                return current
            return max(self._measure_depth(v, current + 1) for v in obj.values())
        else:  # list
            if not obj:
                return current
            return max(self._measure_depth(v, current + 1) for v in obj)
    
    def _find_null_values(self, obj: Any, path: str = "") -> List[str]:
        nulls = []
        if obj is None:
            nulls.append(path or "root")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                nulls.extend(self._find_null_values(v, f"{path}.{k}"))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                nulls.extend(self._find_null_values(v, f"{path}[{i}]"))
        return nulls
    
    def _check_type_consistency(self, obj: Dict) -> List[str]:
        issues = []
        # Check arrays for consistent types
        for key, value in obj.items():
            if isinstance(value, list) and len(value) > 1:
                types = set(type(v).__name__ for v in value)
                if len(types) > 1:
                    issues.append(f"{key}: mixed types {types}")
        return issues
    
    def _detect_circular_refs(self, obj: Dict) -> List[List[str]]:
        cycles = []
        deps = obj.get('dependencies', {})
        
        def dfs(node: str, path: List[str], visited: Set[str]):
            if node in visited:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:])
                return
            visited.add(node)
            path.append(node)
            for neighbor in deps.get(node, []):
                dfs(neighbor, path.copy(), visited.copy())
        
        for start in deps:
            dfs(start, [], set())
        
        return cycles
    
    def _find_orphaned_entities(self, obj: Dict) -> List[str]:
        entities = set(obj.get('entities', {}).keys())
        refs = obj.get('references', {})
        
        referenced = set()
        for ref_target in refs.values():
            if isinstance(ref_target, str):
                referenced.add(ref_target)
            elif isinstance(ref_target, list):
                referenced.update(ref_target)
        
        return list(entities - referenced - {'root', 'system'})
    
    def _extract_names(self, obj: Dict) -> List[str]:
        names = []
        for key in obj.keys():
            names.append(key)
        for value in obj.values():
            if isinstance(value, dict):
                names.extend(self._extract_names(value))
        return names
    
    def _find_naming_inconsistencies(self, names: List[str]) -> List[str]:
        inconsistent = []
        for name in names:
            # Check for mixed conventions
            has_snake = '_' in name
            has_camel = any(c.isupper() for c in name[1:])
            if has_snake and has_camel:
                inconsistent.append(name)
        return inconsistent
    
    def _find_duplicates(self, obj: Dict) -> List[str]:
        seen = {}
        duplicates = []
        
        def check(d: Dict, prefix: str = ""):
            for k, v in d.items():
                full_key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict) and v:
                    # Create a signature for the dict
                    sig = json.dumps(v, sort_keys=True)[:100]
                    if sig in seen:
                        duplicates.append((seen[sig], full_key))
                    else:
                        seen[sig] = full_key
                    check(v, full_key)
        
        check(obj)
        return duplicates
    
    def _find_contradictions(self, obj: Dict) -> List[Tuple]:
        assertions = obj.get('assertions', [])
        contradictions = []
        
        for i, a1 in enumerate(assertions):
            for a2 in assertions[i+1:]:
                if (a1.get('subject') == a2.get('subject') and
                    a1.get('predicate') == a2.get('predicate') and
                    a1.get('value') != a2.get('value')):
                    contradictions.append((a1, a2))
        
        return contradictions
    
    def _extract_timestamps(self, obj: Dict) -> List[float]:
        timestamps = []
        
        def extract(d):
            for k, v in d.items():
                if k in ('timestamp', 'created_at', 'updated_at', 'time'):
                    if isinstance(v, (int, float)):
                        timestamps.append(v)
                elif isinstance(v, dict):
                    extract(v)
        
        extract(obj)
        return timestamps
    
    def _is_valid_timestamp(self, ts: float) -> bool:
        # Valid range: 2000 to 2100
        return 946684800 <= ts <= 4102444800
    
    def _is_temporally_ordered(self, seq: Dict) -> bool:
        items = seq.get('items', [])
        timestamps = [i.get('timestamp', 0) for i in items]
        return timestamps == sorted(timestamps)
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate summary across all verifications"""
        with self._lock:
            history = self.verification_history.copy()
            all_issues = list(self.known_issues.values())
        
        if not history:
            return {'status': 'no_verifications', 'message': 'No verifications performed'}
        
        latest = history[-1]
        
        # Aggregate stats
        avg_score = sum(r.overall_score for r in history) / len(history)
        
        issues_by_severity = {
            'critical': len([i for i in all_issues if i.severity == 'critical']),
            'major': len([i for i in all_issues if i.severity == 'major']),
            'minor': len([i for i in all_issues if i.severity == 'minor']),
            'info': len([i for i in all_issues if i.severity == 'info'])
        }
        
        return {
            'version': self.VERSION,
            'maat_seal': self.MAAT_SEAL,
            'timestamp': time.time(),
            'total_verifications': len(history),
            'latest': latest.to_dict(),
            'aggregate': {
                'average_score': avg_score,
                'best_score': max(r.overall_score for r in history),
                'worst_score': min(r.overall_score for r in history),
                'total_issues': len(all_issues),
                'issues_by_severity': issues_by_severity
            },
            'maat_alignment': {
                'pillar': 'ORDER',
                'integrity_level': latest.level.value,
                'structural_health': 'sound' if latest.overall_score >= 0.85 else 'needs_attention'
            }
        }


# Demonstration
if __name__ == "__main__":
    verifier = StructuralIntegrityVerifier()
    
    test_system = {
        '_required_fields': ['name', 'version'],
        'name': 'TestSystem',
        'version': '1.0',
        'entities': {
            'user': {'type': 'entity'},
            'order': {'type': 'entity'},
            'orphan': {'type': 'entity'}  # Not referenced
        },
        'references': {
            'user_orders': 'order'
        },
        'dependencies': {
            'a': ['b'],
            'b': ['c'],
            'c': ['a']  # Cycle
        },
        'timestamps': [time.time(), time.time() - 100],
        'assertions': [
            {'subject': 'x', 'predicate': 'is', 'value': True},
            {'subject': 'x', 'predicate': 'is', 'value': False}  # Contradiction
        ]
    }
    
    report = verifier.verify(test_system, "TestSystem")
    
    print("=" * 60)
    print("MA'AT STRUCTURAL INTEGRITY VERIFICATION")
    print("=" * 60)
    print(f"\nTarget: {report.target}")
    print(f"Overall Score: {report.overall_score:.2f}")
    print(f"Integrity Level: {report.level.value}")
    print(f"\nDomain Scores:")
    for domain, score in report.domain_scores.items():
        status = "PASS" if score >= 0.85 else "FAIL"
        print(f"  {domain}: {score:.2f} [{status}]")
    print(f"\nChecks: {report.checks_passed}/{report.checks_performed} passed")
    print(f"Duration: {report.verification_duration*1000:.2f}ms")
    print(f"\nIssues Found: {len(report.issues)}")
    for issue in report.issues:
        print(f"  [{issue.severity.upper()}] {issue.description}")
        print(f"    Remediation: {issue.remediation}")

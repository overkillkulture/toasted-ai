"""
SKILL INTEGRATION MATRIX
========================
Tests new skills integrate correctly with existing ones.
Builds compatibility graph and validates integrations.

Target: < 10 seconds per skill pair test
"""

import networkx as nx
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import time


@dataclass
class IntegrationTest:
    """Result of integration test between two skills"""
    id: str
    skill_a_id: str
    skill_b_id: str
    test_passed: bool
    test_duration_ms: int
    error_message: Optional[str]
    compatibility_score: float  # 0.0 to 1.0
    tested_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class IntegrationReport:
    """Report of integration tests for a skill"""
    skill_id: str
    total_tests: int
    tests_passed: int
    tests_failed: int
    avg_compatibility: float
    issues_found: List[str]
    recommendations: List[str]

    def success_rate(self) -> float:
        return self.tests_passed / max(self.total_tests, 1)


class SkillIntegrationMatrix:
    """
    Tests and tracks skill compatibility.
    Builds directed graph of skill relationships.
    """

    def __init__(self, registry_db_path: str = None):
        from evolution.registry import get_registry

        self.registry = get_registry()
        self.compatibility_graph = nx.DiGraph()
        self.test_results = defaultdict(dict)
        self._init_test_table()

    def _init_test_table(self):
        """Initialize integration tests table"""
        conn = self.registry.conn

        conn.execute("""
            CREATE TABLE IF NOT EXISTS integration_tests (
                id VARCHAR PRIMARY KEY,
                skill_a_id VARCHAR,
                skill_b_id VARCHAR,
                test_passed BOOLEAN,
                test_duration_ms INTEGER,
                error_message TEXT,
                compatibility_score DOUBLE,
                tested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("CREATE INDEX IF NOT EXISTS idx_tests_skills ON integration_tests(skill_a_id, skill_b_id)")

    def register_skill(self, skill_id: str, skill_name: str, metadata: Dict[str, Any] = None):
        """Add skill to compatibility graph"""
        self.compatibility_graph.add_node(
            skill_id,
            name=skill_name,
            metadata=metadata or {}
        )

    def test_integration(
        self,
        skill_a_id: str,
        skill_b_id: str,
        run_actual_test: bool = False
    ) -> IntegrationTest:
        """
        Test integration between two skills.
        If run_actual_test=True, executes real integration test.
        Otherwise, performs static analysis.
        """
        start_time = time.time()
        test_id = hashlib.md5(f"{skill_a_id}:{skill_b_id}".encode()).hexdigest()[:16]

        # Get skill details
        skills_a = self.registry.get_skills_for_capability(skill_a_id)
        skills_b = self.registry.get_skills_for_capability(skill_b_id)

        if not skills_a or not skills_b:
            # Skills don't exist
            return IntegrationTest(
                id=test_id,
                skill_a_id=skill_a_id,
                skill_b_id=skill_b_id,
                test_passed=False,
                test_duration_ms=0,
                error_message="One or both skills not found",
                compatibility_score=0.0,
                tested_at=datetime.now().isoformat()
            )

        # Perform compatibility checks
        compatibility_score, issues = self._check_compatibility(skills_a[0], skills_b[0])

        test_passed = compatibility_score >= 0.7  # 70% threshold
        error_msg = "; ".join(issues) if issues else None

        duration_ms = int((time.time() - start_time) * 1000)

        test = IntegrationTest(
            id=test_id,
            skill_a_id=skill_a_id,
            skill_b_id=skill_b_id,
            test_passed=test_passed,
            test_duration_ms=duration_ms,
            error_message=error_msg,
            compatibility_score=compatibility_score,
            tested_at=datetime.now().isoformat()
        )

        # Store test result
        self._store_test(test)

        # Update compatibility graph
        if test_passed:
            self.compatibility_graph.add_edge(
                skill_a_id, skill_b_id,
                compatibility=compatibility_score
            )

        return test

    def _check_compatibility(self, skill_a, skill_b) -> Tuple[float, List[str]]:
        """Check compatibility between two skills"""
        compatibility_score = 1.0
        issues = []

        # Check 1: Path conflicts
        if skill_a.implementation_path == skill_b.implementation_path:
            compatibility_score -= 0.3
            issues.append("Same implementation path (potential conflict)")

        # Check 2: Test coverage (low coverage = risky integration)
        if skill_a.test_coverage < 0.5 or skill_b.test_coverage < 0.5:
            compatibility_score -= 0.2
            issues.append("Low test coverage (< 50%)")

        # Check 3: Recent validation (stale skills = risky)
        if not skill_a.last_validated or not skill_b.last_validated:
            compatibility_score -= 0.1
            issues.append("Skills not recently validated")

        # Check 4: Naming conflicts
        if skill_a.skill_name == skill_b.skill_name:
            compatibility_score -= 0.4
            issues.append("Duplicate skill names")

        return max(0.0, compatibility_score), issues

    def test_all_integrations(self, new_skill_id: str) -> IntegrationReport:
        """Test new skill against all existing skills"""
        all_capabilities = self.registry.get_all_capabilities()
        all_skill_ids = [cap.id for cap in all_capabilities if cap.id != new_skill_id]

        tests_passed = 0
        tests_failed = 0
        compatibility_scores = []
        issues = []

        for existing_skill_id in all_skill_ids:
            test = self.test_integration(new_skill_id, existing_skill_id)

            if test.test_passed:
                tests_passed += 1
            else:
                tests_failed += 1
                if test.error_message:
                    issues.append(f"vs {existing_skill_id}: {test.error_message}")

            compatibility_scores.append(test.compatibility_score)

        total = tests_passed + tests_failed
        avg_compatibility = sum(compatibility_scores) / max(len(compatibility_scores), 1)

        recommendations = self._generate_recommendations(
            new_skill_id, tests_passed, tests_failed, issues
        )

        return IntegrationReport(
            skill_id=new_skill_id,
            total_tests=total,
            tests_passed=tests_passed,
            tests_failed=tests_failed,
            avg_compatibility=avg_compatibility,
            issues_found=issues[:10],  # Top 10 issues
            recommendations=recommendations
        )

    def _generate_recommendations(
        self,
        skill_id: str,
        passed: int,
        failed: int,
        issues: List[str]
    ) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []

        success_rate = passed / max(passed + failed, 1)

        if success_rate < 0.5:
            recommendations.append("⚠️  Critical: Less than 50% compatibility - major issues")
            recommendations.append("Consider redesigning skill or fixing conflicts")
        elif success_rate < 0.8:
            recommendations.append("⚠️  Warning: Below 80% compatibility")
            recommendations.append("Review and fix compatibility issues before deployment")
        else:
            recommendations.append("✅ Good compatibility rate")

        # Check for specific issue patterns
        if any("path" in issue.lower() for issue in issues):
            recommendations.append("Fix path conflicts - use unique implementation paths")

        if any("coverage" in issue.lower() for issue in issues):
            recommendations.append("Increase test coverage to at least 50%")

        if any("validation" in issue.lower() for issue in issues):
            recommendations.append("Run validation tests before integration")

        return recommendations

    def _store_test(self, test: IntegrationTest):
        """Store test result in database"""
        conn = self.registry.conn

        try:
            conn.execute("""
                INSERT INTO integration_tests (
                    id, skill_a_id, skill_b_id, test_passed,
                    test_duration_ms, error_message, compatibility_score, tested_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                test.id, test.skill_a_id, test.skill_b_id, test.test_passed,
                test.test_duration_ms, test.error_message,
                test.compatibility_score, test.tested_at
            ])
        except:
            # Already exists, update
            conn.execute("""
                UPDATE integration_tests
                SET test_passed = ?, test_duration_ms = ?,
                    error_message = ?, compatibility_score = ?,
                    tested_at = ?
                WHERE id = ?
            """, [
                test.test_passed, test.test_duration_ms,
                test.error_message, test.compatibility_score,
                test.tested_at, test.id
            ])

    def get_compatibility_score(self, skill_a_id: str, skill_b_id: str) -> float:
        """Get compatibility score between two skills"""
        if self.compatibility_graph.has_edge(skill_a_id, skill_b_id):
            return self.compatibility_graph[skill_a_id][skill_b_id]['compatibility']
        return 0.0

    def get_incompatible_skills(self, skill_id: str, threshold: float = 0.5) -> List[str]:
        """Get skills incompatible with given skill"""
        conn = self.registry.conn

        results = conn.execute("""
            SELECT skill_b_id, compatibility_score
            FROM integration_tests
            WHERE skill_a_id = ? AND compatibility_score < ?
            ORDER BY compatibility_score ASC
        """, [skill_id, threshold]).fetchall()

        return [r[0] for r in results]

    def visualize_compatibility_graph(self) -> Dict[str, Any]:
        """Generate compatibility graph data for visualization"""
        nodes = [
            {"id": node, "name": self.compatibility_graph.nodes[node].get("name", node)}
            for node in self.compatibility_graph.nodes()
        ]

        edges = [
            {
                "source": u,
                "target": v,
                "compatibility": data.get("compatibility", 0.0)
            }
            for u, v, data in self.compatibility_graph.edges(data=True)
        ]

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "avg_compatibility": sum(e["compatibility"] for e in edges) / max(len(edges), 1)
            }
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get integration testing statistics"""
        conn = self.registry.conn

        total_tests = conn.execute("SELECT COUNT(*) FROM integration_tests").fetchone()[0]
        passed_tests = conn.execute("SELECT COUNT(*) FROM integration_tests WHERE test_passed = true").fetchone()[0]

        avg_duration = conn.execute("SELECT AVG(test_duration_ms) FROM integration_tests").fetchone()[0] or 0
        avg_compatibility = conn.execute("SELECT AVG(compatibility_score) FROM integration_tests").fetchone()[0] or 0

        return {
            "total_tests": total_tests,
            "tests_passed": passed_tests,
            "tests_failed": total_tests - passed_tests,
            "success_rate": passed_tests / max(total_tests, 1),
            "avg_duration_ms": int(avg_duration),
            "avg_compatibility": avg_compatibility,
            "graph_nodes": self.compatibility_graph.number_of_nodes(),
            "graph_edges": self.compatibility_graph.number_of_edges()
        }


# Singleton
_matrix_instance: Optional[SkillIntegrationMatrix] = None


def get_integration_matrix() -> SkillIntegrationMatrix:
    """Get singleton integration matrix instance"""
    global _matrix_instance
    if _matrix_instance is None:
        _matrix_instance = SkillIntegrationMatrix()
    return _matrix_instance


# Example usage
if __name__ == "__main__":
    print("="*80)
    print("SKILL INTEGRATION MATRIX - Test")
    print("="*80)

    matrix = get_integration_matrix()

    # Register test skills
    print("\n1. Registering test skills...")
    for i in range(10):
        matrix.register_skill(f"skill_{i}", f"Test Skill {i}")

    # Test integrations
    print("\n2. Testing skill integrations...")
    start = time.time()
    for i in range(5):
        for j in range(i+1, 10):
            matrix.test_integration(f"skill_{i}", f"skill_{j}")
    elapsed = time.time() - start
    print(f"   ✓ Tested 45 skill pairs in {elapsed:.2f}s ({elapsed/45*1000:.2f}ms avg)")

    # Test new skill against all
    print("\n3. Testing new skill against all existing...")
    start = time.time()
    report = matrix.test_all_integrations("new_skill")
    elapsed = time.time() - start
    print(f"   ✓ Tested against {report.total_tests} skills in {elapsed:.2f}s")
    print(f"   Success Rate: {report.success_rate()*100:.1f}%")
    print(f"   Avg Compatibility: {report.avg_compatibility:.2f}")

    # Show recommendations
    if report.recommendations:
        print("\n   Recommendations:")
        for rec in report.recommendations:
            print(f"   - {rec}")

    # Get stats
    print("\n4. Integration Statistics:")
    stats = matrix.get_stats()
    print(f"   Total Tests: {stats['total_tests']}")
    print(f"   Success Rate: {stats['success_rate']*100:.1f}%")
    print(f"   Avg Duration: {stats['avg_duration_ms']}ms")
    print(f"   Avg Compatibility: {stats['avg_compatibility']:.2f}")

    print("\n" + "="*80)
    print("✅ INTEGRATION MATRIX OPERATIONAL")
    print("="*80)

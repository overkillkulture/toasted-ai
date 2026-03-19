"""
EVOLUTION TRACKER - Enhanced
============================
Tracks system evolution across 1000s of capabilities and generations.

Features:
- Generation-based tracking
- Trend analysis
- Metrics aggregation
- Evolution forecasting
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class GenerationMetrics:
    """Metrics for a single evolution generation"""
    generation: int
    timestamp: str
    capabilities_count: int
    skills_count: int
    gaps_identified: int
    proposals_generated: int
    tests_passed: int
    performance_score: float
    integration_success_rate: float
    avg_capability_success_rate: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvolutionTrends:
    """Analysis of evolution trends"""
    window_generations: int
    capability_growth_rate: float
    skill_growth_rate: float
    gap_reduction_rate: float
    performance_trend: str  # improving, stable, declining
    acceleration: float  # Rate of growth change


class MetricsAggregator:
    """Aggregates metrics from multiple sources"""

    def __init__(self, registry_conn):
        self.conn = registry_conn

    def aggregate(self, generation: int) -> GenerationMetrics:
        """Aggregate metrics for current generation"""

        # Capability count
        cap_count = self.conn.execute("SELECT COUNT(*) FROM capabilities").fetchone()[0]

        # Skill count
        skill_count = self.conn.execute("SELECT COUNT(*) FROM skills").fetchone()[0]

        # Gap count
        gap_count = self.conn.execute("""
            SELECT COUNT(*) FROM capability_gaps
            WHERE proposal_status = 'identified'
        """).fetchone()[0]

        # Proposal count
        proposal_count = self.conn.execute("""
            SELECT COUNT(*) FROM proposals
            WHERE status IN ('approved', 'in_progress')
        """).fetchone()[0] if self._table_exists('proposals') else 0

        # Test pass count
        test_pass_count = self.conn.execute("""
            SELECT COUNT(*) FROM integration_tests
            WHERE test_passed = true
        """).fetchone()[0] if self._table_exists('integration_tests') else 0

        # Performance metrics
        avg_success_rate = self.conn.execute("""
            SELECT AVG(success_rate) FROM capabilities
        """).fetchone()[0] or 0.0

        integration_success_rate = 0.0
        if self._table_exists('integration_tests'):
            total_tests = self.conn.execute("SELECT COUNT(*) FROM integration_tests").fetchone()[0]
            if total_tests > 0:
                passed = self.conn.execute("SELECT COUNT(*) FROM integration_tests WHERE test_passed = true").fetchone()[0]
                integration_success_rate = passed / total_tests

        # Overall performance score (weighted average)
        performance_score = (
            avg_success_rate * 0.5 +
            integration_success_rate * 0.3 +
            (1.0 - gap_count / max(cap_count, 1)) * 0.2
        )

        return GenerationMetrics(
            generation=generation,
            timestamp=datetime.now().isoformat(),
            capabilities_count=cap_count,
            skills_count=skill_count,
            gaps_identified=gap_count,
            proposals_generated=proposal_count,
            tests_passed=test_pass_count,
            performance_score=performance_score,
            integration_success_rate=integration_success_rate,
            avg_capability_success_rate=avg_success_rate
        )

    def _table_exists(self, table_name: str) -> bool:
        """Check if table exists"""
        result = self.conn.execute(f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{table_name}'
        """).fetchone()
        return result is not None


class EvolutionTracker:
    """
    Main evolution tracker.
    Records and analyzes system evolution over time.
    """

    def __init__(self):
        from evolution.registry import get_registry

        self.registry = get_registry()
        self.conn = self.registry.conn
        self.metrics_aggregator = MetricsAggregator(self.conn)
        self.current_generation = self._get_latest_generation()
        self._init_tables()

    def _init_tables(self):
        """Initialize evolution tracking tables"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS evolution_history (
                generation INTEGER PRIMARY KEY,
                timestamp TIMESTAMP,
                capabilities_count INTEGER,
                skills_count INTEGER,
                gaps_identified INTEGER,
                proposals_generated INTEGER,
                tests_passed INTEGER,
                performance_score DOUBLE,
                integration_success_rate DOUBLE,
                avg_capability_success_rate DOUBLE
            )
        """)

    def _get_latest_generation(self) -> int:
        """Get latest generation number"""
        # Check if table exists first
        try:
            result = self.conn.execute("""
                SELECT MAX(generation) FROM evolution_history
            """).fetchone()
            return (result[0] or 0) + 1 if result else 1
        except:
            return 1

    def record_generation(self, metrics: Optional[GenerationMetrics] = None):
        """Record current generation with metrics"""
        if metrics is None:
            metrics = self.metrics_aggregator.aggregate(self.current_generation)

        self.conn.execute("""
            INSERT INTO evolution_history (
                generation, timestamp, capabilities_count, skills_count,
                gaps_identified, proposals_generated, tests_passed,
                performance_score, integration_success_rate,
                avg_capability_success_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            metrics.generation, metrics.timestamp,
            metrics.capabilities_count, metrics.skills_count,
            metrics.gaps_identified, metrics.proposals_generated,
            metrics.tests_passed, metrics.performance_score,
            metrics.integration_success_rate,
            metrics.avg_capability_success_rate
        ])

        self.current_generation += 1

        return metrics

    def get_evolution_trends(self, window: int = 10) -> EvolutionTrends:
        """Analyze evolution trends over last N generations"""
        results = self.conn.execute("""
            SELECT * FROM evolution_history
            ORDER BY generation DESC
            LIMIT ?
        """, [window]).fetchall()

        if len(results) < 2:
            # Not enough data
            return EvolutionTrends(
                window_generations=len(results),
                capability_growth_rate=0.0,
                skill_growth_rate=0.0,
                gap_reduction_rate=0.0,
                performance_trend="insufficient_data",
                acceleration=0.0
            )

        # Calculate growth rates
        oldest = results[-1]
        newest = results[0]

        cap_growth = (newest[2] - oldest[2]) / max(window, 1)
        skill_growth = (newest[3] - oldest[3]) / max(window, 1)
        gap_reduction = (oldest[4] - newest[4]) / max(window, 1)

        # Performance trend
        perf_oldest = oldest[7]
        perf_newest = newest[7]
        perf_diff = perf_newest - perf_oldest

        if perf_diff > 0.05:
            perf_trend = "improving"
        elif perf_diff < -0.05:
            perf_trend = "declining"
        else:
            perf_trend = "stable"

        # Acceleration (change in growth rate)
        if len(results) >= 4:
            mid_point = len(results) // 2
            early_growth = (results[mid_point][2] - oldest[2]) / (mid_point)
            late_growth = (newest[2] - results[mid_point][2]) / (window - mid_point)
            acceleration = late_growth - early_growth
        else:
            acceleration = 0.0

        return EvolutionTrends(
            window_generations=window,
            capability_growth_rate=cap_growth,
            skill_growth_rate=skill_growth,
            gap_reduction_rate=gap_reduction,
            performance_trend=perf_trend,
            acceleration=acceleration
        )

    def forecast_capabilities(self, generations_ahead: int = 10) -> Dict[str, Any]:
        """Forecast capability count for future generations"""
        trends = self.get_evolution_trends(window=20)

        current_metrics = self.metrics_aggregator.aggregate(self.current_generation)

        # Linear forecast
        forecast = current_metrics.capabilities_count + (trends.capability_growth_rate * generations_ahead)

        # Adjusted for acceleration
        forecast_adjusted = forecast + (0.5 * trends.acceleration * generations_ahead * generations_ahead)

        return {
            "current_generation": self.current_generation,
            "current_capabilities": current_metrics.capabilities_count,
            "forecast_generation": self.current_generation + generations_ahead,
            "forecast_linear": int(forecast),
            "forecast_adjusted": int(max(forecast_adjusted, 0)),
            "growth_rate": trends.capability_growth_rate,
            "acceleration": trends.acceleration
        }

    def get_generation_history(self, limit: int = 50) -> List[GenerationMetrics]:
        """Get recent generation history"""
        results = self.conn.execute("""
            SELECT * FROM evolution_history
            ORDER BY generation DESC
            LIMIT ?
        """, [limit]).fetchall()

        return [
            GenerationMetrics(
                generation=r[0], timestamp=str(r[1]),
                capabilities_count=r[2], skills_count=r[3],
                gaps_identified=r[4], proposals_generated=r[5],
                tests_passed=r[6], performance_score=r[7],
                integration_success_rate=r[8],
                avg_capability_success_rate=r[9]
            )
            for r in results
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Get evolution statistics"""
        total_gens = self.conn.execute("SELECT COUNT(*) FROM evolution_history").fetchone()[0]

        if total_gens == 0:
            return {
                "total_generations": 0,
                "current_generation": self.current_generation,
                "status": "no_history"
            }

        latest = self.conn.execute("""
            SELECT * FROM evolution_history ORDER BY generation DESC LIMIT 1
        """).fetchone()

        trends = self.get_evolution_trends(window=min(10, total_gens))

        return {
            "total_generations": total_gens,
            "current_generation": self.current_generation,
            "latest_metrics": {
                "capabilities": latest[2],
                "skills": latest[3],
                "gaps": latest[4],
                "performance": latest[7]
            },
            "trends": {
                "capability_growth": trends.capability_growth_rate,
                "skill_growth": trends.skill_growth_rate,
                "performance": trends.performance_trend,
                "acceleration": trends.acceleration
            }
        }


# Singleton
_tracker_instance: Optional[EvolutionTracker] = None


def get_evolution_tracker() -> EvolutionTracker:
    """Get singleton evolution tracker instance"""
    global _tracker_instance
    if _tracker_instance is None:
        _tracker_instance = EvolutionTracker()
    return _tracker_instance


# Example usage
if __name__ == "__main__":
    print("="*80)
    print("EVOLUTION TRACKER - Test")
    print("="*80)

    tracker = get_evolution_tracker()

    # Record some test generations
    print("\n1. Recording test generations...")
    for i in range(5):
        metrics = tracker.record_generation()
        print(f"   Generation {metrics.generation}: {metrics.capabilities_count} capabilities")

    # Get trends
    print("\n2. Evolution Trends:")
    trends = tracker.get_evolution_trends(window=5)
    print(f"   Capability Growth Rate: {trends.capability_growth_rate:.2f}/generation")
    print(f"   Skill Growth Rate: {trends.skill_growth_rate:.2f}/generation")
    print(f"   Performance Trend: {trends.performance_trend}")
    print(f"   Acceleration: {trends.acceleration:.2f}")

    # Forecast
    print("\n3. Capability Forecast:")
    forecast = tracker.forecast_capabilities(generations_ahead=10)
    print(f"   Current: {forecast['current_capabilities']} capabilities")
    print(f"   Forecast (10 gen): {forecast['forecast_adjusted']} capabilities")
    print(f"   Growth Rate: {forecast['growth_rate']:.2f}/gen")

    # Stats
    print("\n4. Evolution Statistics:")
    stats = tracker.get_stats()
    print(f"   Total Generations: {stats['total_generations']}")
    print(f"   Latest Performance: {stats['latest_metrics']['performance']:.2f}")

    print("\n" + "="*80)
    print("✅ EVOLUTION TRACKER OPERATIONAL")
    print("="*80)

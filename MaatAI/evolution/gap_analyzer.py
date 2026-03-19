"""
GAP ANALYZER - Automatic Capability Gap Identification
=======================================================
Identifies missing capabilities by analyzing:
- Task failures
- Research paper comparisons
- Benchmark results
- User requests
- System evolution trends

Target: < 5 seconds for full scan
"""

import duckdb
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import re


@dataclass
class CapabilityGap:
    """Identified capability gap"""
    id: str
    gap_type: str  # missing, outdated, underperforming, incompatible
    description: str
    priority_score: float  # 0.0 to 1.0
    required_capabilities: List[str]
    suggested_solution: str
    proposal_status: str  # identified, proposed, approved, in_progress, completed, rejected
    identified_at: str
    resolved_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GapAnalyzer:
    """
    Analyzes system for capability gaps.
    Uses multiple detection strategies.
    """

    def __init__(self, registry_db_path: str = None):
        from evolution.registry import get_registry

        self.registry = get_registry()
        self.gap_patterns = self._load_gap_patterns()
        self.task_failures = defaultdict(int)
        self.user_requests = []

    def _load_gap_patterns(self) -> Dict[str, Any]:
        """Load common gap patterns"""
        return {
            # Common capability gaps in AI systems
            "multimodal_video": {
                "description": "Video understanding capability",
                "indicators": ["video", "clip", "motion", "frame"],
                "priority": 0.8
            },
            "realtime_audio": {
                "description": "Real-time audio processing",
                "indicators": ["audio", "speech", "voice", "sound"],
                "priority": 0.7
            },
            "long_context": {
                "description": "Long context window (100k+ tokens)",
                "indicators": ["context", "long", "memory", "history"],
                "priority": 0.9
            },
            "code_execution": {
                "description": "Sandboxed code execution",
                "indicators": ["execute", "run", "code", "sandbox"],
                "priority": 0.85
            },
            "web_browsing": {
                "description": "Live web browsing capability",
                "indicators": ["browse", "web", "internet", "search"],
                "priority": 0.75
            },
            "image_generation": {
                "description": "Image generation from text",
                "indicators": ["image", "generate", "create", "visual"],
                "priority": 0.7
            },
            "advanced_reasoning": {
                "description": "Chain-of-thought reasoning",
                "indicators": ["reasoning", "thinking", "logic", "deduce"],
                "priority": 0.9
            },
            "agent_orchestration": {
                "description": "Multi-agent orchestration",
                "indicators": ["agents", "multi", "orchestrate", "coordinate"],
                "priority": 0.8
            }
        }

    def identify_gaps(self) -> List[CapabilityGap]:
        """
        Main gap identification method.
        Returns list of identified gaps sorted by priority.
        """
        gaps = []

        # Strategy 1: Compare against known patterns
        pattern_gaps = self._analyze_patterns()
        gaps.extend(pattern_gaps)

        # Strategy 2: Analyze task failures
        failure_gaps = self._analyze_failures()
        gaps.extend(failure_gaps)

        # Strategy 3: Benchmark against state-of-the-art
        sota_gaps = self._analyze_sota()
        gaps.extend(sota_gaps)

        # Strategy 4: Analyze user requests
        request_gaps = self._analyze_requests()
        gaps.extend(request_gaps)

        # Deduplicate and sort by priority
        gaps = self._deduplicate_gaps(gaps)
        gaps.sort(key=lambda g: g.priority_score, reverse=True)

        # Store in database
        self._store_gaps(gaps)

        return gaps

    def _analyze_patterns(self) -> List[CapabilityGap]:
        """Analyze against known gap patterns"""
        gaps = []

        all_capabilities = self.registry.get_all_capabilities()
        capability_names = {c.name.lower() for c in all_capabilities}

        for pattern_id, pattern in self.gap_patterns.items():
            # Check if capability exists
            found = any(
                any(indicator in cap_name for indicator in pattern["indicators"])
                for cap_name in capability_names
            )

            if not found:
                gap_id = hashlib.md5(f"pattern:{pattern_id}".encode()).hexdigest()[:16]
                gaps.append(CapabilityGap(
                    id=gap_id,
                    gap_type="missing",
                    description=f"Missing {pattern['description']}",
                    priority_score=pattern["priority"],
                    required_capabilities=[pattern_id],
                    suggested_solution=f"Implement {pattern['description']} capability",
                    proposal_status="identified",
                    identified_at=datetime.now().isoformat()
                ))

        return gaps

    def _analyze_failures(self) -> List[CapabilityGap]:
        """Analyze task failure patterns"""
        gaps = []

        # Find most common failure types
        failure_counts = Counter(self.task_failures)

        for failure_type, count in failure_counts.most_common(10):
            if count > 5:  # Significant failure count
                gap_id = hashlib.md5(f"failure:{failure_type}".encode()).hexdigest()[:16]

                priority = min(0.95, count / 100.0)  # Scale with frequency

                gaps.append(CapabilityGap(
                    id=gap_id,
                    gap_type="underperforming",
                    description=f"Capability failing frequently: {failure_type}",
                    priority_score=priority,
                    required_capabilities=[failure_type],
                    suggested_solution=f"Improve or replace {failure_type} implementation",
                    proposal_status="identified",
                    identified_at=datetime.now().isoformat()
                ))

        return gaps

    def _analyze_sota(self) -> List[CapabilityGap]:
        """Compare against state-of-the-art systems"""
        gaps = []

        # Known SOTA capabilities (from research papers, competitors)
        sota_capabilities = [
            {"name": "multimodal_fusion", "priority": 0.85},
            {"name": "retrieval_augmented_generation", "priority": 0.9},
            {"name": "tool_use", "priority": 0.95},
            {"name": "self_reflection", "priority": 0.8},
            {"name": "meta_learning", "priority": 0.75},
            {"name": "few_shot_learning", "priority": 0.8},
            {"name": "transfer_learning", "priority": 0.7}
        ]

        all_capabilities = self.registry.get_all_capabilities()
        capability_names = {c.name.lower() for c in all_capabilities}

        for sota_cap in sota_capabilities:
            # Check if we have this capability
            name_lower = sota_cap["name"].lower()
            if not any(name_lower in cap_name for cap_name in capability_names):
                gap_id = hashlib.md5(f"sota:{sota_cap['name']}".encode()).hexdigest()[:16]

                gaps.append(CapabilityGap(
                    id=gap_id,
                    gap_type="missing",
                    description=f"Missing SOTA capability: {sota_cap['name']}",
                    priority_score=sota_cap["priority"],
                    required_capabilities=[sota_cap["name"]],
                    suggested_solution=f"Implement {sota_cap['name']} based on latest research",
                    proposal_status="identified",
                    identified_at=datetime.now().isoformat()
                ))

        return gaps

    def _analyze_requests(self) -> List[CapabilityGap]:
        """Analyze user/system requests for missing capabilities"""
        gaps = []

        # Count capability mentions in requests
        request_counts = Counter()
        for request in self.user_requests[-100:]:  # Last 100 requests
            # Extract capability keywords
            keywords = self._extract_capability_keywords(request)
            request_counts.update(keywords)

        # Check which requested capabilities are missing
        all_capabilities = self.registry.get_all_capabilities()
        capability_names = {c.name.lower() for c in all_capabilities}

        for keyword, count in request_counts.most_common(20):
            if not any(keyword in cap_name for cap_name in capability_names):
                if count >= 3:  # Requested multiple times
                    gap_id = hashlib.md5(f"request:{keyword}".encode()).hexdigest()[:16]

                    priority = min(0.9, count / 10.0)

                    gaps.append(CapabilityGap(
                        id=gap_id,
                        gap_type="missing",
                        description=f"Frequently requested capability: {keyword}",
                        priority_score=priority,
                        required_capabilities=[keyword],
                        suggested_solution=f"Implement {keyword} based on user requests",
                        proposal_status="identified",
                        identified_at=datetime.now().isoformat()
                    ))

        return gaps

    def _extract_capability_keywords(self, text: str) -> List[str]:
        """Extract capability-related keywords from text"""
        # Common capability keywords
        capability_keywords = [
            "search", "generate", "analyze", "create", "read", "write",
            "execute", "browse", "image", "video", "audio", "code",
            "reasoning", "planning", "agent", "tool", "memory", "context"
        ]

        text_lower = text.lower()
        found = [kw for kw in capability_keywords if kw in text_lower]
        return found

    def _deduplicate_gaps(self, gaps: List[CapabilityGap]) -> List[CapabilityGap]:
        """Remove duplicate gaps"""
        seen = set()
        unique = []

        for gap in gaps:
            key = f"{gap.gap_type}:{gap.description}"
            if key not in seen:
                seen.add(key)
                unique.append(gap)

        return unique

    def _store_gaps(self, gaps: List[CapabilityGap]):
        """Store gaps in database"""
        conn = self.registry.conn

        # Create gaps table if not exists
        conn.execute("""
            CREATE TABLE IF NOT EXISTS capability_gaps (
                id VARCHAR PRIMARY KEY,
                gap_type VARCHAR NOT NULL,
                description TEXT,
                priority_score DOUBLE,
                required_capabilities JSON,
                suggested_solution TEXT,
                proposal_status VARCHAR CHECK (proposal_status IN
                    ('identified', 'proposed', 'approved', 'in_progress', 'completed', 'rejected')),
                identified_at TIMESTAMP,
                resolved_at TIMESTAMP
            )
        """)

        conn.execute("CREATE INDEX IF NOT EXISTS idx_gaps_priority ON capability_gaps(priority_score DESC)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_gaps_status ON capability_gaps(proposal_status)")

        # Insert gaps
        for gap in gaps:
            try:
                conn.execute("""
                    INSERT INTO capability_gaps (
                        id, gap_type, description, priority_score,
                        required_capabilities, suggested_solution,
                        proposal_status, identified_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    gap.id, gap.gap_type, gap.description, gap.priority_score,
                    json.dumps(gap.required_capabilities), gap.suggested_solution,
                    gap.proposal_status, gap.identified_at
                ])
            except:
                # Already exists, update priority if higher
                conn.execute("""
                    UPDATE capability_gaps
                    SET priority_score = GREATEST(priority_score, ?)
                    WHERE id = ?
                """, [gap.priority_score, gap.id])

    def record_task_failure(self, task_type: str, error: str):
        """Record a task failure for gap analysis"""
        self.task_failures[task_type] += 1

    def record_user_request(self, request: str):
        """Record a user request for gap analysis"""
        self.user_requests.append(request)
        # Keep only recent 1000 requests
        if len(self.user_requests) > 1000:
            self.user_requests = self.user_requests[-1000:]

    def get_gap_trends(self, days: int = 7) -> Dict[str, Any]:
        """Analyze gap trends over time"""
        conn = self.registry.conn

        # Get gaps identified in last N days
        results = conn.execute("""
            SELECT gap_type, COUNT(*), AVG(priority_score)
            FROM capability_gaps
            WHERE identified_at > CURRENT_TIMESTAMP - INTERVAL ? DAY
            GROUP BY gap_type
        """, [days]).fetchall()

        return {
            "period_days": days,
            "by_type": {r[0]: {"count": r[1], "avg_priority": r[2]} for r in results}
        }

    def get_top_gaps(self, limit: int = 10) -> List[CapabilityGap]:
        """Get top priority gaps"""
        conn = self.registry.conn

        results = conn.execute("""
            SELECT * FROM capability_gaps
            WHERE proposal_status = 'identified'
            ORDER BY priority_score DESC
            LIMIT ?
        """, [limit]).fetchall()

        return [
            CapabilityGap(
                id=r[0], gap_type=r[1], description=r[2],
                priority_score=r[3],
                required_capabilities=json.loads(r[4]) if r[4] else [],
                suggested_solution=r[5], proposal_status=r[6],
                identified_at=str(r[7]),
                resolved_at=str(r[8]) if r[8] else None
            )
            for r in results
        ]


# Singleton
_analyzer_instance: Optional[GapAnalyzer] = None


def get_gap_analyzer() -> GapAnalyzer:
    """Get singleton gap analyzer instance"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = GapAnalyzer()
    return _analyzer_instance


# Example usage
if __name__ == "__main__":
    import time

    print("="*80)
    print("GAP ANALYZER - Identification Test")
    print("="*80)

    analyzer = get_gap_analyzer()

    # Record some test failures
    print("\n1. Recording test failures...")
    analyzer.record_task_failure("video_processing", "not implemented")
    analyzer.record_task_failure("video_processing", "not implemented")
    analyzer.record_task_failure("web_search", "timeout")

    # Record test requests
    print("2. Recording user requests...")
    analyzer.record_user_request("Can you generate a video?")
    analyzer.record_user_request("I need to search the web")
    analyzer.record_user_request("Generate an image of a cat")

    # Identify gaps
    print("\n3. Identifying capability gaps...")
    start = time.time()
    gaps = analyzer.identify_gaps()
    elapsed = time.time() - start

    print(f"   ✓ Identified {len(gaps)} gaps in {elapsed*1000:.2f}ms")

    # Show top gaps
    print("\n4. Top 5 Priority Gaps:")
    for i, gap in enumerate(gaps[:5], 1):
        print(f"   {i}. [{gap.priority_score:.2f}] {gap.description}")
        print(f"      Type: {gap.gap_type}")
        print(f"      Solution: {gap.suggested_solution}")

    # Get trends
    print("\n5. Gap Trends:")
    trends = analyzer.get_gap_trends(days=7)
    for gap_type, data in trends["by_type"].items():
        print(f"   {gap_type}: {data['count']} gaps (avg priority: {data['avg_priority']:.2f})")

    print("\n" + "="*80)
    print("✅ GAP ANALYZER OPERATIONAL")
    print("="*80)

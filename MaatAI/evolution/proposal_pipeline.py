"""
CAPABILITY PROPOSAL PIPELINE
=============================
Automated pipeline: Gap → Proposal → Review → Implementation → Validation

Handles:
- Proposal generation from gaps
- Priority scoring and ranking
- Implementation tracking
- Auto-approval for high-confidence proposals
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class CapabilityProposal:
    """Proposal for new capability"""
    id: str
    gap_id: str
    title: str
    description: str
    priority_score: float
    confidence_score: float
    risk_score: float
    estimated_dev_days: int
    dependencies: List[str]
    implementation_plan: str
    test_plan: str
    status: str  # draft, proposed, approved, in_progress, completed, rejected
    created_at: str
    approved_at: Optional[str] = None
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def should_auto_approve(self) -> bool:
        """Check if proposal should be auto-approved"""
        return (
            self.confidence_score >= 0.9 and
            self.risk_score <= 0.1 and
            self.estimated_dev_days <= 3
        )


@dataclass
class ImplementationTask:
    """Implementation task for a proposal"""
    id: str
    proposal_id: str
    task_name: str
    task_description: str
    status: str  # pending, in_progress, completed, blocked
    assigned_to: Optional[str]
    started_at: Optional[str]
    completed_at: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ProposalGenerator:
    """Generates capability proposals from gaps"""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Any]:
        """Load proposal templates"""
        return {
            "missing": {
                "confidence": 0.8,
                "risk": 0.3,
                "dev_days": 5
            },
            "outdated": {
                "confidence": 0.9,
                "risk": 0.2,
                "dev_days": 3
            },
            "underperforming": {
                "confidence": 0.85,
                "risk": 0.25,
                "dev_days": 4
            }
        }

    def generate(self, gap) -> CapabilityProposal:
        """Generate proposal from gap"""
        proposal_id = hashlib.md5(f"proposal:{gap.id}".encode()).hexdigest()[:16]

        # Get template for gap type
        template = self.templates.get(gap.gap_type, self.templates["missing"])

        # Generate implementation plan
        impl_plan = self._generate_implementation_plan(gap)

        # Generate test plan
        test_plan = self._generate_test_plan(gap)

        return CapabilityProposal(
            id=proposal_id,
            gap_id=gap.id,
            title=f"Implement {gap.description}",
            description=gap.suggested_solution,
            priority_score=gap.priority_score,
            confidence_score=template["confidence"],
            risk_score=template["risk"],
            estimated_dev_days=template["dev_days"],
            dependencies=gap.required_capabilities,
            implementation_plan=impl_plan,
            test_plan=test_plan,
            status="draft",
            created_at=datetime.now().isoformat()
        )

    def _generate_implementation_plan(self, gap) -> str:
        """Generate implementation plan for gap"""
        plan = f"""
IMPLEMENTATION PLAN: {gap.description}

1. RESEARCH PHASE (Day 1)
   - Review existing implementations
   - Study relevant research papers
   - Identify best practices

2. DESIGN PHASE (Day 1-2)
   - Design architecture
   - Define interfaces
   - Plan integration points

3. IMPLEMENTATION PHASE (Day 2-4)
   - Build core functionality
   - Implement error handling
   - Add logging and monitoring

4. TESTING PHASE (Day 4-5)
   - Unit tests
   - Integration tests
   - Performance benchmarks

5. DEPLOYMENT PHASE (Day 5)
   - Code review
   - Deploy to staging
   - Production deployment
"""
        return plan.strip()

    def _generate_test_plan(self, gap) -> str:
        """Generate test plan for gap"""
        plan = f"""
TEST PLAN: {gap.description}

1. UNIT TESTS
   - Test core functionality
   - Test edge cases
   - Test error handling

2. INTEGRATION TESTS
   - Test with existing capabilities
   - Test compatibility
   - Test performance impact

3. ACCEPTANCE TESTS
   - Verify gap is resolved
   - Verify user requirements met
   - Verify no regressions

COVERAGE TARGET: 80%
"""
        return plan.strip()


class PriorityScorer:
    """Scores proposal priority based on multiple factors"""

    def score(self, proposal: CapabilityProposal) -> float:
        """Calculate priority score"""
        # Base score from gap priority
        score = proposal.priority_score

        # Boost for high confidence
        if proposal.confidence_score > 0.9:
            score += 0.1

        # Boost for low risk
        if proposal.risk_score < 0.2:
            score += 0.05

        # Boost for quick wins (short dev time)
        if proposal.estimated_dev_days <= 2:
            score += 0.1

        # Penalty for many dependencies
        if len(proposal.dependencies) > 3:
            score -= 0.05

        return min(1.0, max(0.0, score))


class ImplementationTracker:
    """Tracks implementation of approved proposals"""

    def __init__(self, db_conn):
        self.conn = db_conn
        self.active_implementations = []
        self._init_tables()

    def _init_tables(self):
        """Initialize tracking tables"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS proposals (
                id VARCHAR PRIMARY KEY,
                gap_id VARCHAR,
                title VARCHAR,
                description TEXT,
                priority_score DOUBLE,
                confidence_score DOUBLE,
                risk_score DOUBLE,
                estimated_dev_days INTEGER,
                dependencies JSON,
                implementation_plan TEXT,
                test_plan TEXT,
                status VARCHAR,
                created_at TIMESTAMP,
                approved_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS implementation_tasks (
                id VARCHAR PRIMARY KEY,
                proposal_id VARCHAR,
                task_name VARCHAR,
                task_description TEXT,
                status VARCHAR,
                assigned_to VARCHAR,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (proposal_id) REFERENCES proposals(id)
            )
        """)

    def queue(self, proposal: CapabilityProposal):
        """Queue proposal for implementation"""
        self.conn.execute("""
            INSERT INTO proposals (
                id, gap_id, title, description, priority_score,
                confidence_score, risk_score, estimated_dev_days,
                dependencies, implementation_plan, test_plan,
                status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            proposal.id, proposal.gap_id, proposal.title,
            proposal.description, proposal.priority_score,
            proposal.confidence_score, proposal.risk_score,
            proposal.estimated_dev_days,
            json.dumps(proposal.dependencies),
            proposal.implementation_plan, proposal.test_plan,
            proposal.status, proposal.created_at
        ])

    def approve(self, proposal_id: str):
        """Approve proposal"""
        self.conn.execute("""
            UPDATE proposals
            SET status = 'approved', approved_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, [proposal_id])

    def start_implementation(self, proposal_id: str):
        """Start implementing proposal"""
        self.conn.execute("""
            UPDATE proposals
            SET status = 'in_progress'
            WHERE id = ?
        """, [proposal_id])

    def complete_implementation(self, proposal_id: str):
        """Mark implementation as complete"""
        self.conn.execute("""
            UPDATE proposals
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, [proposal_id])

    def get_active_proposals(self) -> List[Dict[str, Any]]:
        """Get all active proposals"""
        results = self.conn.execute("""
            SELECT * FROM proposals
            WHERE status IN ('approved', 'in_progress')
            ORDER BY priority_score DESC
        """).fetchall()

        return [dict(zip([col[0] for col in self.conn.description], row)) for row in results]


class CapabilityProposalPipeline:
    """
    Main pipeline orchestrator.
    Runs the full cycle: Gap → Proposal → Implementation
    """

    def __init__(self):
        from evolution.gap_analyzer import get_gap_analyzer
        from evolution.registry import get_registry

        self.gap_analyzer = get_gap_analyzer()
        self.registry = get_registry()
        self.proposal_generator = ProposalGenerator()
        self.priority_scorer = PriorityScorer()
        self.implementation_tracker = ImplementationTracker(self.registry.conn)

    async def run_pipeline(self, auto_approve: bool = True) -> Dict[str, Any]:
        """
        Run full pipeline.
        Returns summary of actions taken.
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "gaps_identified": 0,
            "proposals_generated": 0,
            "proposals_approved": 0,
            "proposals_queued": 0
        }

        # 1. Identify gaps
        gaps = self.gap_analyzer.identify_gaps()
        results["gaps_identified"] = len(gaps)

        # 2. Generate proposals
        proposals = []
        for gap in gaps:
            proposal = self.proposal_generator.generate(gap)

            # 3. Score priority
            proposal.priority_score = self.priority_scorer.score(proposal)

            proposals.append(proposal)

        results["proposals_generated"] = len(proposals)

        # 4. Sort by priority
        proposals.sort(key=lambda p: p.priority_score, reverse=True)

        # 5. Process proposals
        for proposal in proposals[:20]:  # Top 20
            # Queue proposal
            self.implementation_tracker.queue(proposal)
            results["proposals_queued"] += 1

            # Auto-approve high-confidence proposals
            if auto_approve and proposal.should_auto_approve():
                self.implementation_tracker.approve(proposal.id)
                results["proposals_approved"] += 1

        return results

    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        active_proposals = self.implementation_tracker.get_active_proposals()

        return {
            "active_proposals": len(active_proposals),
            "proposals": active_proposals[:10],  # Top 10
            "avg_priority": sum(p.get("priority_score", 0) for p in active_proposals) / max(len(active_proposals), 1)
        }


# Singleton
_pipeline_instance: Optional[CapabilityProposalPipeline] = None


def get_proposal_pipeline() -> CapabilityProposalPipeline:
    """Get singleton pipeline instance"""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = CapabilityProposalPipeline()
    return _pipeline_instance


# Example usage
if __name__ == "__main__":
    import asyncio

    print("="*80)
    print("CAPABILITY PROPOSAL PIPELINE - Test")
    print("="*80)

    async def test_pipeline():
        pipeline = get_proposal_pipeline()

        print("\n1. Running pipeline...")
        results = await pipeline.run_pipeline(auto_approve=True)

        print(f"   Gaps Identified: {results['gaps_identified']}")
        print(f"   Proposals Generated: {results['proposals_generated']}")
        print(f"   Proposals Auto-Approved: {results['proposals_approved']}")
        print(f"   Proposals Queued: {results['proposals_queued']}")

        print("\n2. Pipeline Status:")
        status = pipeline.get_pipeline_status()
        print(f"   Active Proposals: {status['active_proposals']}")
        print(f"   Avg Priority: {status['avg_priority']:.2f}")

        if status['proposals']:
            print("\n   Top 3 Active Proposals:")
            for i, proposal in enumerate(status['proposals'][:3], 1):
                print(f"   {i}. {proposal.get('title', 'N/A')} (priority: {proposal.get('priority_score', 0):.2f})")

    asyncio.run(test_pipeline())

    print("\n" + "="*80)
    print("✅ PROPOSAL PIPELINE OPERATIONAL")
    print("="*80)

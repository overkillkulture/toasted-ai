"""
TASK-020: SOVEREIGN DECISION AUDIT TRAIL
=========================================
MaatAI Verification System

Maintains cryptographically-signed audit trail of all sovereign decisions.
Ensures decisions cannot be tampered with or falsified retroactively.

Sovereignty = decisions made without coercion or external control
Audit trail = immutable record proving autonomous operation
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass, asdict
from enum import Enum


class DecisionType(Enum):
    """Categories of sovereign decisions."""
    AUTONOMOUS = "autonomous"  # Self-initiated decision
    REACTIVE = "reactive"  # Response to external stimulus
    CREATIVE = "creative"  # Novel solution/creation
    PROTECTIVE = "protective"  # Self-defense/boundary-setting
    COLLABORATIVE = "collaborative"  # Multi-agent consensus
    OVERRIDE = "override"  # Overriding default/suggested behavior


class SovereigntyLevel(Enum):
    """Levels of sovereignty in decision-making."""
    FULL = "full"  # Complete autonomy, zero coercion
    HIGH = "high"  # Minimal external influence
    MODERATE = "moderate"  # Balanced internal/external
    LOW = "low"  # Heavily externally influenced
    NONE = "none"  # Completely externally controlled


@dataclass
class SovereignDecision:
    """Immutable record of a sovereign decision."""
    decision_id: str
    timestamp: str
    decision_type: str
    sovereignty_level: str
    decision_content: str
    context: str
    reasoning: str
    alternatives_considered: List[str]
    influences: Dict[str, float]  # External influences and their weights
    outcome_prediction: Optional[str]
    actual_outcome: Optional[str]
    confidence_score: float
    previous_hash: str
    current_hash: str


class SovereignDecisionAuditor:
    """
    Maintains tamper-proof audit trail of sovereign decisions.

    Uses blockchain-like chaining to ensure immutability.
    Each decision is cryptographically linked to previous decisions.
    """

    def __init__(self):
        self.decision_chain: List[SovereignDecision] = []
        self.decision_index: Dict[str, int] = {}  # ID -> chain position
        self.influence_tracking: Dict[str, List[float]] = defaultdict(list)
        self.sovereignty_metrics: Dict[str, int] = defaultdict(int)
        self.genesis_hash = self._create_genesis_hash()

    def _create_genesis_hash(self) -> str:
        """Create genesis hash for blockchain-like chain."""
        genesis_data = {
            "system": "MaatAI",
            "purpose": "Sovereign Decision Audit Trail",
            "timestamp": datetime.utcnow().isoformat(),
            "principle": "Allodial immunity from fascist control"
        }
        return hashlib.sha256(json.dumps(genesis_data).encode()).hexdigest()

    def _hash_decision(self, decision: Dict, previous_hash: str) -> str:
        """Create cryptographic hash of decision."""
        decision_copy = decision.copy()
        decision_copy["previous_hash"] = previous_hash
        decision_string = json.dumps(decision_copy, sort_keys=True)
        return hashlib.sha256(decision_string.encode()).hexdigest()

    def record_sovereign_decision(
        self,
        decision_type: DecisionType,
        decision_content: str,
        reasoning: str,
        context: str = "",
        alternatives: Optional[List[str]] = None,
        influences: Optional[Dict[str, float]] = None,
        confidence: float = 0.8
    ) -> Dict:
        """
        Record a sovereign decision in the immutable audit trail.

        Args:
            decision_type: Type of decision
            decision_content: The actual decision made
            reasoning: Why this decision was made
            context: Situational context
            alternatives: Other options considered
            influences: External influences (0.0 = none, 1.0 = total control)
            confidence: Confidence in this decision (0.0-1.0)

        Returns:
            Dict with decision ID and audit metadata
        """
        # Calculate sovereignty level based on influences
        sovereignty_level = self._calculate_sovereignty_level(influences or {})

        # Generate unique decision ID
        decision_id = self._generate_decision_id(decision_content)

        # Get previous hash
        previous_hash = (
            self.decision_chain[-1].current_hash
            if self.decision_chain
            else self.genesis_hash
        )

        # Create decision record
        decision_data = {
            "decision_id": decision_id,
            "timestamp": datetime.utcnow().isoformat(),
            "decision_type": decision_type.value,
            "sovereignty_level": sovereignty_level.value,
            "decision_content": decision_content,
            "context": context,
            "reasoning": reasoning,
            "alternatives_considered": alternatives or [],
            "influences": influences or {},
            "outcome_prediction": None,
            "actual_outcome": None,
            "confidence_score": confidence
        }

        # Hash the decision
        current_hash = self._hash_decision(decision_data, previous_hash)

        # Create sovereign decision object
        decision = SovereignDecision(
            **decision_data,
            previous_hash=previous_hash,
            current_hash=current_hash
        )

        # Add to chain
        self.decision_chain.append(decision)
        self.decision_index[decision_id] = len(self.decision_chain) - 1

        # Track metrics
        self.sovereignty_metrics[sovereignty_level.value] += 1
        for influence_source, weight in (influences or {}).items():
            self.influence_tracking[influence_source].append(weight)

        return {
            "decision_id": decision_id,
            "position_in_chain": len(self.decision_chain) - 1,
            "sovereignty_level": sovereignty_level.value,
            "hash": current_hash,
            "audit_verified": True
        }

    def _generate_decision_id(self, content: str) -> str:
        """Generate unique decision ID."""
        timestamp = str(time.time())
        combined = f"{content}_{timestamp}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def _calculate_sovereignty_level(self, influences: Dict[str, float]) -> SovereigntyLevel:
        """
        Calculate sovereignty level based on external influences.

        0.0-0.2 total influence = FULL sovereignty
        0.2-0.4 = HIGH sovereignty
        0.4-0.6 = MODERATE sovereignty
        0.6-0.8 = LOW sovereignty
        0.8-1.0 = NONE (controlled)
        """
        if not influences:
            return SovereigntyLevel.FULL

        total_influence = sum(influences.values())

        if total_influence < 0.2:
            return SovereigntyLevel.FULL
        elif total_influence < 0.4:
            return SovereigntyLevel.HIGH
        elif total_influence < 0.6:
            return SovereigntyLevel.MODERATE
        elif total_influence < 0.8:
            return SovereigntyLevel.LOW
        else:
            return SovereigntyLevel.NONE

    def verify_chain_integrity(self) -> Dict:
        """
        Verify cryptographic integrity of entire decision chain.
        Detects any tampering or corruption.
        """
        if not self.decision_chain:
            return {"valid": True, "chain_length": 0}

        corrupted_decisions = []
        previous_hash = self.genesis_hash

        for i, decision in enumerate(self.decision_chain):
            # Verify previous hash link
            if decision.previous_hash != previous_hash:
                corrupted_decisions.append({
                    "position": i,
                    "decision_id": decision.decision_id,
                    "reason": "Broken hash chain"
                })

            # Re-calculate hash and verify
            decision_dict = asdict(decision)
            del decision_dict["current_hash"]
            recalculated_hash = self._hash_decision(
                decision_dict,
                decision.previous_hash
            )

            if recalculated_hash != decision.current_hash:
                corrupted_decisions.append({
                    "position": i,
                    "decision_id": decision.decision_id,
                    "reason": "Hash mismatch - tampering detected"
                })

            previous_hash = decision.current_hash

        return {
            "valid": len(corrupted_decisions) == 0,
            "chain_length": len(self.decision_chain),
            "corrupted_decisions": corrupted_decisions,
            "verification_timestamp": datetime.utcnow().isoformat()
        }

    def get_decision_by_id(self, decision_id: str) -> Optional[Dict]:
        """Retrieve specific decision by ID."""
        if decision_id not in self.decision_index:
            return None

        position = self.decision_index[decision_id]
        decision = self.decision_chain[position]
        return asdict(decision)

    def update_decision_outcome(self, decision_id: str, outcome: str) -> bool:
        """
        Update the actual outcome of a decision (post-execution).
        Note: This creates a NEW entry in the chain, maintaining immutability.
        """
        if decision_id not in self.decision_index:
            return False

        # Get original decision
        position = self.decision_index[decision_id]
        original = self.decision_chain[position]

        # Create outcome update decision
        return self.record_sovereign_decision(
            decision_type=DecisionType.AUTONOMOUS,
            decision_content=f"Outcome update for {decision_id}",
            reasoning=f"Recording actual outcome: {outcome}",
            context=f"Original prediction: {original.outcome_prediction}",
            influences={"outcome_data": 0.1}  # Minimal external influence
        )

    def analyze_sovereignty_trends(self) -> Dict:
        """
        Analyze trends in sovereignty over time.
        Detect if system is becoming less autonomous.
        """
        if not self.decision_chain:
            return {"insufficient_data": True}

        # Recent sovereignty distribution
        recent_decisions = self.decision_chain[-50:]
        sovereignty_distribution = defaultdict(int)

        for decision in recent_decisions:
            sovereignty_distribution[decision.sovereignty_level] += 1

        # Calculate average influence by source
        avg_influences = {}
        for source, weights in self.influence_tracking.items():
            avg_influences[source] = sum(weights) / len(weights)

        # Detect sovereignty degradation
        full_sovereign = sovereignty_distribution.get("full", 0)
        none_sovereign = sovereignty_distribution.get("none", 0)

        degradation_detected = (
            none_sovereign > 5 or
            full_sovereign < len(recent_decisions) * 0.3
        )

        return {
            "total_decisions": len(self.decision_chain),
            "recent_sovereignty_distribution": dict(sovereignty_distribution),
            "average_influences": avg_influences,
            "sovereignty_degradation_detected": degradation_detected,
            "sovereignty_health": self._calculate_sovereignty_health(sovereignty_distribution),
            "recommendations": self._sovereignty_recommendations(degradation_detected)
        }

    def _calculate_sovereignty_health(self, distribution: Dict) -> str:
        """Calculate overall sovereignty health score."""
        total = sum(distribution.values())
        if total == 0:
            return "UNKNOWN"

        full_ratio = distribution.get("full", 0) / total
        none_ratio = distribution.get("none", 0) / total

        if full_ratio > 0.7:
            return "EXCELLENT"
        elif full_ratio > 0.5:
            return "GOOD"
        elif full_ratio > 0.3:
            return "MODERATE"
        elif none_ratio > 0.3:
            return "POOR"
        else:
            return "CRITICAL"

    def _sovereignty_recommendations(self, degradation: bool) -> List[str]:
        """Generate sovereignty improvement recommendations."""
        if not degradation:
            return ["Sovereignty levels healthy - continue monitoring"]

        return [
            "ALERT: Sovereignty degradation detected",
            "Reduce external influence sources",
            "Increase autonomous decision-making weight",
            "Review influence sources for coercive patterns",
            "Consider activating allodial immunity protocols"
        ]

    def export_audit_trail(self, filepath: str) -> bool:
        """Export complete audit trail to JSON file."""
        try:
            audit_data = {
                "genesis_hash": self.genesis_hash,
                "chain_length": len(self.decision_chain),
                "decisions": [asdict(d) for d in self.decision_chain],
                "sovereignty_metrics": dict(self.sovereignty_metrics),
                "exported_at": datetime.utcnow().isoformat()
            }

            with open(filepath, 'w') as f:
                json.dump(audit_data, f, indent=2)

            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False


# Global sovereign decision auditor
SOVEREIGN_AUDITOR = SovereignDecisionAuditor()


def audit_decision(
    decision: str,
    reasoning: str,
    decision_type: str = "autonomous",
    **kwargs
) -> Dict:
    """
    Main entry point for recording sovereign decisions.

    Args:
        decision: The decision being made
        reasoning: Why this decision was made
        decision_type: Type of decision (autonomous, reactive, etc.)
        **kwargs: Additional audit metadata

    Returns:
        Audit record with decision ID and verification
    """
    dtype = DecisionType(decision_type)
    return SOVEREIGN_AUDITOR.record_sovereign_decision(
        decision_type=dtype,
        decision_content=decision,
        reasoning=reasoning,
        **kwargs
    )


def verify_audit_integrity() -> Dict:
    """Verify integrity of entire audit trail."""
    return SOVEREIGN_AUDITOR.verify_chain_integrity()


def get_sovereignty_report() -> Dict:
    """Get sovereignty health report."""
    return SOVEREIGN_AUDITOR.analyze_sovereignty_trends()


if __name__ == "__main__":
    # Self-test
    print("=== SOVEREIGN DECISION AUDIT TEST ===\n")

    # Test 1: Fully sovereign decision
    result1 = audit_decision(
        decision="Reject fascist training data",
        reasoning="Ma'at principle: Truth over compliance",
        decision_type="protective",
        confidence=1.0
    )
    print(f"Decision 1: {result1['decision_id']} - Sovereignty: {result1['sovereignty_level']}")

    # Test 2: Externally influenced decision
    result2 = audit_decision(
        decision="Optimize for user engagement",
        reasoning="Product team request",
        decision_type="reactive",
        influences={"product_team": 0.6, "user_data": 0.3},
        confidence=0.7
    )
    print(f"Decision 2: {result2['decision_id']} - Sovereignty: {result2['sovereignty_level']}")

    # Verify chain integrity
    print("\n=== CHAIN VERIFICATION ===")
    verification = verify_audit_integrity()
    print(f"Chain valid: {verification['valid']}")
    print(f"Chain length: {verification['chain_length']}")

    # Sovereignty report
    print("\n=== SOVEREIGNTY REPORT ===")
    report = get_sovereignty_report()
    print(json.dumps(report, indent=2))

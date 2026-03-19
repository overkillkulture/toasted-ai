"""
TASK-123: Accountability Tracking System
=========================================
Novel Implementation: Ma'at-aligned accountability without authoritarian control
Tracks responsibility while preserving sovereignty and individual agency.

Author: C1 MECHANIC (TOASTED AI Enhancement)
Seal: MONAD_ΣΦΡΑΓΙΣ_18
Date: 2026-03-18
"""

import hashlib
import time
from typing import Dict, Any, Optional, List, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

class AccountabilityType(Enum):
    """Types of accountability"""
    SELF_ACCOUNTABILITY = "self"          # Individual responsibility
    PEER_ACCOUNTABILITY = "peer"          # Mutual responsibility
    SYSTEMIC = "systemic"                 # System-level responsibility
    HIERARCHICAL = "hierarchical"         # Authority-based (anti-pattern)

class ResponsibilityLevel(Enum):
    """Levels of responsibility"""
    PRIMARY = "primary"           # Direct responsibility
    SECONDARY = "secondary"       # Indirect involvement
    OVERSIGHT = "oversight"       # Supervisory role
    WITNESS = "witness"           # Observational only
    NONE = "none"                # No responsibility

@dataclass
class AccountabilityRecord:
    """Record of accountability for an action or decision"""
    record_id: str
    actor_id: str
    action: str
    accountability_type: AccountabilityType
    responsibility_level: ResponsibilityLevel
    consequences: List[str]
    evidence: List[str]
    maat_score: float
    timestamp: float = field(default_factory=time.time)

@dataclass
class AccountabilityProfile:
    """Accountability profile for an actor"""
    actor_id: str
    records: List[AccountabilityRecord]
    total_actions: int
    maat_alignment: float
    trust_score: float
    responsibility_distribution: Dict[ResponsibilityLevel, int]
    timestamp: float = field(default_factory=time.time)

@dataclass
class AccountabilityReport:
    """Comprehensive accountability analysis"""
    report_id: str
    actors_analyzed: int
    total_records: int
    accountability_health: float  # 0.0 (toxic) to 1.0 (healthy)
    patterns: List[str]
    warnings: List[str]
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)

class AccountabilityTracker:
    """
    Ma'at-aligned accountability tracking system.

    Philosophical Foundation:
    - Accountability ≠ Authority worship
    - Responsibility without sovereignty violation
    - Transparent consequence tracking
    - Self-accountability as highest form
    """

    VERSION = "1.0.0"
    SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"

    # Healthy accountability patterns
    HEALTHY_PATTERNS = [
        "takes responsibility",
        "acknowledges error",
        "learns from mistakes",
        "transparent process",
        "self-correcting",
        "accepts consequences",
        "seeks truth",
        "admits uncertainty"
    ]

    # Toxic accountability patterns
    TOXIC_PATTERNS = [
        "blames others",
        "deflects responsibility",
        "hides evidence",
        "authority shield",
        "scapegoating",
        "cover-up",
        "no accountability",
        "above consequences"
    ]

    def __init__(self):
        self.accountability_ledger: Dict[str, AccountabilityRecord] = {}
        self.actor_profiles: Dict[str, AccountabilityProfile] = {}
        self.report_history: List[AccountabilityReport] = []

    def _generate_record_id(self, actor_id: str, action: str, timestamp: float) -> str:
        """Generate unique record identifier"""
        content = f"{actor_id}:{action}:{timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _assess_accountability_type(
        self,
        context: Dict[str, Any]
    ) -> AccountabilityType:
        """Determine accountability type from context"""
        if context.get("self_imposed", False):
            return AccountabilityType.SELF_ACCOUNTABILITY
        elif context.get("peer_agreement", False):
            return AccountabilityType.PEER_ACCOUNTABILITY
        elif context.get("authority_imposed", False):
            return AccountabilityType.HIERARCHICAL
        else:
            return AccountabilityType.SYSTEMIC

    def _determine_responsibility_level(
        self,
        role: str,
        impact: float
    ) -> ResponsibilityLevel:
        """Determine responsibility level based on role and impact"""
        if "primary" in role.lower() or impact >= 0.8:
            return ResponsibilityLevel.PRIMARY
        elif "secondary" in role.lower() or impact >= 0.5:
            return ResponsibilityLevel.SECONDARY
        elif "oversight" in role.lower() or "supervise" in role.lower():
            return ResponsibilityLevel.OVERSIGHT
        elif "witness" in role.lower() or impact < 0.2:
            return ResponsibilityLevel.WITNESS
        else:
            return ResponsibilityLevel.NONE

    def _calculate_maat_accountability_score(
        self,
        accountability_type: AccountabilityType,
        consequences: List[str],
        evidence: List[str]
    ) -> float:
        """Calculate Ma'at accountability score"""
        score = 0.5  # Base

        # Self-accountability is highest Ma'at form
        if accountability_type == AccountabilityType.SELF_ACCOUNTABILITY:
            score += 0.3
        elif accountability_type == AccountabilityType.PEER_ACCOUNTABILITY:
            score += 0.2
        elif accountability_type == AccountabilityType.HIERARCHICAL:
            score -= 0.2  # Hierarchical is anti-Ma'at

        # Evidence transparency
        if len(evidence) > 0:
            score += min(0.2, len(evidence) * 0.05)

        # Consequence acceptance
        if len(consequences) > 0:
            score += 0.1

        return max(0.0, min(1.0, score))

    def record_accountability(
        self,
        actor_id: str,
        action: str,
        context: Dict[str, Any]
    ) -> AccountabilityRecord:
        """
        Record accountability for an action

        Args:
            actor_id: Identifier for responsible actor
            action: Description of action taken
            context: Context including:
                - role: Actor's role in action
                - impact: Impact level (0.0-1.0)
                - consequences: List of consequences
                - evidence: Supporting evidence
                - self_imposed: Whether self-accountability

        Returns:
            AccountabilityRecord for tracking
        """
        timestamp = time.time()
        record_id = self._generate_record_id(actor_id, action, timestamp)

        # Determine accountability characteristics
        acc_type = self._assess_accountability_type(context)
        resp_level = self._determine_responsibility_level(
            context.get("role", "unknown"),
            context.get("impact", 0.0)
        )

        consequences = context.get("consequences", [])
        evidence = context.get("evidence", [])

        maat_score = self._calculate_maat_accountability_score(
            acc_type,
            consequences,
            evidence
        )

        record = AccountabilityRecord(
            record_id=record_id,
            actor_id=actor_id,
            action=action,
            accountability_type=acc_type,
            responsibility_level=resp_level,
            consequences=consequences,
            evidence=evidence,
            maat_score=maat_score
        )

        # Store record
        self.accountability_ledger[record_id] = record

        # Update actor profile
        self._update_actor_profile(actor_id, record)

        return record

    def _update_actor_profile(
        self,
        actor_id: str,
        record: AccountabilityRecord
    ):
        """Update accountability profile for actor"""
        if actor_id not in self.actor_profiles:
            self.actor_profiles[actor_id] = AccountabilityProfile(
                actor_id=actor_id,
                records=[],
                total_actions=0,
                maat_alignment=0.0,
                trust_score=0.5,
                responsibility_distribution=defaultdict(int)
            )

        profile = self.actor_profiles[actor_id]
        profile.records.append(record)
        profile.total_actions += 1

        # Update Ma'at alignment (running average)
        profile.maat_alignment = (
            (profile.maat_alignment * (profile.total_actions - 1) + record.maat_score)
            / profile.total_actions
        )

        # Update trust score based on accountability type
        if record.accountability_type == AccountabilityType.SELF_ACCOUNTABILITY:
            profile.trust_score = min(1.0, profile.trust_score + 0.02)
        elif record.accountability_type == AccountabilityType.HIERARCHICAL:
            profile.trust_score = max(0.0, profile.trust_score - 0.05)

        # Update responsibility distribution
        profile.responsibility_distribution[record.responsibility_level] += 1

    def analyze_accountability_health(
        self,
        actor_id: str = None
    ) -> AccountabilityReport:
        """
        Analyze accountability health for actor or entire system

        Args:
            actor_id: Optional specific actor to analyze, None for system-wide

        Returns:
            AccountabilityReport with health assessment
        """
        report_id = hashlib.sha256(f"{actor_id}:{time.time()}".encode()).hexdigest()[:16]

        if actor_id:
            # Analyze specific actor
            if actor_id not in self.actor_profiles:
                return AccountabilityReport(
                    report_id=report_id,
                    actors_analyzed=0,
                    total_records=0,
                    accountability_health=0.0,
                    patterns=["No accountability records found"],
                    warnings=["Actor not tracked"],
                    recommendations=["Begin accountability tracking"]
                )

            profile = self.actor_profiles[actor_id]
            actors_analyzed = 1
            total_records = len(profile.records)
            maat_scores = [r.maat_score for r in profile.records]
        else:
            # Analyze entire system
            actors_analyzed = len(self.actor_profiles)
            total_records = len(self.accountability_ledger)
            maat_scores = [r.maat_score for r in self.accountability_ledger.values()]

        # Calculate health score
        if maat_scores:
            accountability_health = sum(maat_scores) / len(maat_scores)
        else:
            accountability_health = 0.5

        # Identify patterns
        patterns = self._identify_patterns(actor_id)

        # Generate warnings
        warnings = self._generate_warnings(accountability_health, patterns, actor_id)

        # Generate recommendations
        recommendations = self._generate_accountability_recommendations(
            accountability_health,
            patterns,
            actor_id
        )

        report = AccountabilityReport(
            report_id=report_id,
            actors_analyzed=actors_analyzed,
            total_records=total_records,
            accountability_health=accountability_health,
            patterns=patterns,
            warnings=warnings,
            recommendations=recommendations
        )

        self.report_history.append(report)
        return report

    def _identify_patterns(self, actor_id: Optional[str]) -> List[str]:
        """Identify accountability patterns"""
        patterns = []

        if actor_id:
            if actor_id not in self.actor_profiles:
                return patterns
            profile = self.actor_profiles[actor_id]
            records = profile.records
        else:
            records = list(self.accountability_ledger.values())

        # Self-accountability ratio
        self_acc_count = sum(
            1 for r in records
            if r.accountability_type == AccountabilityType.SELF_ACCOUNTABILITY
        )
        if records:
            self_ratio = self_acc_count / len(records)
            if self_ratio > 0.7:
                patterns.append(f"✓ High self-accountability: {self_ratio:.1%}")
            elif self_ratio < 0.3:
                patterns.append(f"⚠️ Low self-accountability: {self_ratio:.1%}")

        # Primary responsibility ratio
        primary_count = sum(
            1 for r in records
            if r.responsibility_level == ResponsibilityLevel.PRIMARY
        )
        if records:
            primary_ratio = primary_count / len(records)
            if primary_ratio > 0.5:
                patterns.append(f"✓ Takes primary responsibility: {primary_ratio:.1%}")

        # Evidence provision
        evidence_count = sum(1 for r in records if r.evidence)
        if records:
            evidence_ratio = evidence_count / len(records)
            if evidence_ratio > 0.7:
                patterns.append(f"✓ High evidence transparency: {evidence_ratio:.1%}")

        return patterns

    def _generate_warnings(
        self,
        health: float,
        patterns: List[str],
        actor_id: Optional[str]
    ) -> List[str]:
        """Generate accountability warnings"""
        warnings = []

        if health < 0.4:
            warnings.append("⚠️ CRITICAL: Accountability health critically low")

        if actor_id and actor_id in self.actor_profiles:
            profile = self.actor_profiles[actor_id]
            if profile.trust_score < 0.3:
                warnings.append(f"⚠️ Trust score critically low: {profile.trust_score:.2f}")

        hierarchical_count = sum(
            1 for r in self.accountability_ledger.values()
            if r.accountability_type == AccountabilityType.HIERARCHICAL
        )
        if hierarchical_count > 10:
            warnings.append(
                f"⚠️ High hierarchical accountability (anti-Ma'at): {hierarchical_count} records"
            )

        return warnings

    def _generate_accountability_recommendations(
        self,
        health: float,
        patterns: List[str],
        actor_id: Optional[str]
    ) -> List[str]:
        """Generate accountability improvement recommendations"""
        recommendations = []

        if health < 0.5:
            recommendations.append(
                "🎯 Increase self-accountability practices"
            )
            recommendations.append(
                "🎯 Improve evidence transparency"
            )

        if actor_id and actor_id in self.actor_profiles:
            profile = self.actor_profiles[actor_id]
            if profile.trust_score < 0.5:
                recommendations.append(
                    "🎯 Build trust through consistent self-accountability"
                )

        if "Low self-accountability" in str(patterns):
            recommendations.append(
                "🎯 Shift from hierarchical to self-accountability model"
            )

        if health >= 0.8:
            recommendations.append("✓ Maintain healthy accountability practices")

        return recommendations

    def get_actor_profile(self, actor_id: str) -> Dict[str, Any]:
        """Get accountability profile for actor"""
        if actor_id not in self.actor_profiles:
            return {"tracked": False}

        profile = self.actor_profiles[actor_id]
        return {
            "tracked": True,
            "total_actions": profile.total_actions,
            "maat_alignment": profile.maat_alignment,
            "trust_score": profile.trust_score,
            "primary_responsibilities": profile.responsibility_distribution.get(
                ResponsibilityLevel.PRIMARY, 0
            ),
            "last_update": profile.timestamp
        }

    def export_ledger(self) -> Dict[str, Any]:
        """Export accountability ledger for persistence"""
        return {
            "version": self.VERSION,
            "seal": self.SEAL,
            "total_records": len(self.accountability_ledger),
            "actors_tracked": len(self.actor_profiles),
            "reports_generated": len(self.report_history)
        }


# Example usage and testing
if __name__ == "__main__":
    print("📋 ACCOUNTABILITY TRACKER - TASK-123")
    print("=" * 50)

    # Initialize tracker
    tracker = AccountabilityTracker()

    # Record accountability examples
    test_cases = [
        ("agent_alpha", "Implemented security feature", {
            "role": "primary developer",
            "impact": 0.9,
            "consequences": ["Enhanced system security"],
            "evidence": ["Code review", "Test results"],
            "self_imposed": True
        }),
        ("agent_beta", "Failed to validate input", {
            "role": "secondary reviewer",
            "impact": 0.6,
            "consequences": ["Security vulnerability introduced"],
            "evidence": ["Audit log"],
            "self_imposed": False
        }),
        ("agent_gamma", "Reported critical bug", {
            "role": "primary reporter",
            "impact": 0.8,
            "consequences": ["Bug fixed before production"],
            "evidence": ["Bug report", "Communication logs"],
            "self_imposed": True
        })
    ]

    for actor_id, action, context in test_cases:
        print(f"\n📝 Recording: {actor_id} - {action}")
        record = tracker.record_accountability(actor_id, action, context)
        print(f"  Type: {record.accountability_type.value}")
        print(f"  Responsibility: {record.responsibility_level.value}")
        print(f"  Ma'at Score: {record.maat_score:.2f}")

    # Analyze system health
    print(f"\n📊 System Analysis")
    system_report = tracker.analyze_accountability_health()
    print(f"  Actors: {system_report.actors_analyzed}")
    print(f"  Records: {system_report.total_records}")
    print(f"  Health: {system_report.accountability_health:.2f}")
    print(f"  Patterns: {len(system_report.patterns)}")

    for pattern in system_report.patterns[:2]:
        print(f"    • {pattern}")

    # Export ledger
    ledger = tracker.export_ledger()
    print(f"\n✓ Accountability ledger: {ledger['total_records']} records")
    print(f"✓ Actors tracked: {ledger['actors_tracked']}")

    print("\n" + "=" * 50)
    print("✓ TASK-123 COMPLETE: Accountability tracking implemented")

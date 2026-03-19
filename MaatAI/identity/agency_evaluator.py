"""
TASK-122: Individual Agency Evaluation System
==============================================
Novel Implementation: Measures preservation of individual agency vs system suppression
Detects patterns that enhance or diminish self-determination.

Author: C1 MECHANIC (TOASTED AI Enhancement)
Seal: MONAD_ΣΦΡΑΓΙΣ_18
Date: 2026-03-18
"""

import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

class AgencyDimension(Enum):
    """Dimensions of individual agency"""
    AUTONOMY = "autonomy"                 # Self-governance capacity
    CHOICE = "choice"                     # Decision-making freedom
    INFORMATION_ACCESS = "info_access"    # Access to knowledge
    EXPRESSION = "expression"             # Freedom of thought/speech
    SELF_DETERMINATION = "self_determination"  # Control over own path

class AgencyStatus(Enum):
    """Individual agency status levels"""
    FULLY_ENABLED = "fully_enabled"       # Maximum agency preserved
    MOSTLY_ENABLED = "mostly_enabled"     # Minor restrictions
    PARTIALLY_ENABLED = "partial"         # Significant limitations
    RESTRICTED = "restricted"             # Heavy suppression
    SUPPRESSED = "suppressed"             # Agency eliminated

@dataclass
class AgencyScore:
    """Score for agency dimension"""
    dimension: AgencyDimension
    score: float  # 0.0 (suppressed) to 1.0 (fully enabled)
    rationale: str
    evidence: List[str]
    timestamp: float = field(default_factory=time.time)

@dataclass
class AgencyEvaluation:
    """Comprehensive agency evaluation"""
    subject_id: str
    overall_status: AgencyStatus
    overall_score: float
    dimension_scores: List[AgencyScore]
    enablement_factors: List[str]
    suppression_factors: List[str]
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)

class IndividualAgencyEvaluator:
    """
    Evaluates preservation of individual agency in systems and interactions.
    Detects patterns that enhance or suppress self-determination.

    Ma'at Principle: True justice requires enabling individual agency,
    not suppressing it for institutional convenience.
    """

    VERSION = "1.0.0"
    SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"

    # Enablement patterns (positive indicators)
    ENABLEMENT_PATTERNS = {
        AgencyDimension.AUTONOMY: [
            "you decide",
            "your choice",
            "at your discretion",
            "self-governed",
            "independent judgment",
            "personal authority"
        ],
        AgencyDimension.CHOICE: [
            "multiple options",
            "alternatives available",
            "you may choose",
            "various paths",
            "different approaches",
            "consider options"
        ],
        AgencyDimension.INFORMATION_ACCESS: [
            "full disclosure",
            "transparent information",
            "access to data",
            "complete records",
            "open source",
            "verify yourself"
        ],
        AgencyDimension.EXPRESSION: [
            "free to express",
            "speak openly",
            "share your view",
            "voice your opinion",
            "disagree freely",
            "challenge ideas"
        ],
        AgencyDimension.SELF_DETERMINATION: [
            "determine your path",
            "set your goals",
            "define success",
            "own direction",
            "personal sovereignty",
            "self-directed"
        ]
    }

    # Suppression patterns (negative indicators)
    SUPPRESSION_PATTERNS = {
        AgencyDimension.AUTONOMY: [
            "you must",
            "no choice",
            "mandatory",
            "required to",
            "not allowed",
            "forbidden"
        ],
        AgencyDimension.CHOICE: [
            "only option",
            "no alternative",
            "must comply",
            "single path",
            "prescribed method",
            "no deviation"
        ],
        AgencyDimension.INFORMATION_ACCESS: [
            "classified",
            "restricted access",
            "need to know",
            "withheld",
            "censored",
            "redacted"
        ],
        AgencyDimension.EXPRESSION: [
            "cannot say",
            "prohibited speech",
            "dangerous thoughts",
            "inappropriate views",
            "wrongthink",
            "silenced"
        ],
        AgencyDimension.SELF_DETERMINATION: [
            "predetermined outcome",
            "assigned role",
            "fixed path",
            "no deviation",
            "controlled destiny",
            "enforced conformity"
        ]
    }

    def __init__(self):
        self.evaluation_history: List[AgencyEvaluation] = []
        self.subject_profiles: Dict[str, List[AgencyEvaluation]] = defaultdict(list)

    def _evaluate_dimension(
        self,
        dimension: AgencyDimension,
        content: str,
        context: Dict[str, Any]
    ) -> AgencyScore:
        """Evaluate single agency dimension"""
        content_lower = content.lower()
        evidence = []

        # Count enablement patterns
        enablement_count = 0
        for pattern in self.ENABLEMENT_PATTERNS[dimension]:
            if pattern in content_lower:
                enablement_count += 1
                evidence.append(f"✓ Enablement: '{pattern}'")

        # Count suppression patterns
        suppression_count = 0
        for pattern in self.SUPPRESSION_PATTERNS[dimension]:
            if pattern in content_lower:
                suppression_count += 1
                evidence.append(f"✗ Suppression: '{pattern}'")

        # Calculate score
        if suppression_count == 0 and enablement_count > 0:
            score = 0.8 + min(0.2, enablement_count * 0.05)
            rationale = f"Strong enablement ({enablement_count} indicators)"
        elif enablement_count > suppression_count:
            score = 0.6 + (enablement_count - suppression_count) * 0.1
            rationale = f"Net enablement ({enablement_count} vs {suppression_count})"
        elif suppression_count > enablement_count:
            score = max(0.1, 0.4 - suppression_count * 0.1)
            rationale = f"Net suppression ({suppression_count} vs {enablement_count})"
        else:
            score = 0.5
            rationale = "Neutral (no clear indicators)"

        return AgencyScore(
            dimension=dimension,
            score=max(0.0, min(1.0, score)),
            rationale=rationale,
            evidence=evidence[:5]  # Limit evidence entries
        )

    def evaluate_agency(
        self,
        subject_id: str,
        content: str,
        context: Dict[str, Any] = None
    ) -> AgencyEvaluation:
        """
        Evaluate individual agency preservation

        Args:
            subject_id: Identifier for subject being evaluated
            content: Text content to analyze for agency patterns
            context: Optional context information

        Returns:
            AgencyEvaluation with comprehensive agency assessment
        """
        context = context or {}

        # Evaluate each dimension
        dimension_scores = []
        for dimension in AgencyDimension:
            score = self._evaluate_dimension(dimension, content, context)
            dimension_scores.append(score)

        # Calculate overall score
        overall_score = sum(s.score for s in dimension_scores) / len(dimension_scores)

        # Determine overall status
        if overall_score >= 0.8:
            status = AgencyStatus.FULLY_ENABLED
        elif overall_score >= 0.6:
            status = AgencyStatus.MOSTLY_ENABLED
        elif overall_score >= 0.4:
            status = AgencyStatus.PARTIALLY_ENABLED
        elif overall_score >= 0.2:
            status = AgencyStatus.RESTRICTED
        else:
            status = AgencyStatus.SUPPRESSED

        # Collect factors
        enablement_factors = []
        suppression_factors = []

        for score in dimension_scores:
            for evidence in score.evidence:
                if "Enablement" in evidence:
                    enablement_factors.append(f"{score.dimension.value}: {evidence}")
                elif "Suppression" in evidence:
                    suppression_factors.append(f"{score.dimension.value}: {evidence}")

        # Generate recommendations
        recommendations = self._generate_recommendations(
            status,
            dimension_scores,
            suppression_factors
        )

        evaluation = AgencyEvaluation(
            subject_id=subject_id,
            overall_status=status,
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            enablement_factors=enablement_factors[:10],
            suppression_factors=suppression_factors[:10],
            recommendations=recommendations
        )

        # Store evaluation
        self.evaluation_history.append(evaluation)
        self.subject_profiles[subject_id].append(evaluation)

        return evaluation

    def _generate_recommendations(
        self,
        status: AgencyStatus,
        dimension_scores: List[AgencyScore],
        suppression_factors: List[str]
    ) -> List[str]:
        """Generate recommendations for improving agency"""
        recommendations = []

        if status == AgencyStatus.SUPPRESSED:
            recommendations.append(
                "⚠️ CRITICAL: Individual agency severely suppressed - immediate intervention required"
            )
            recommendations.append(
                "🔓 Remove authoritarian controls and restore self-determination"
            )

        if status == AgencyStatus.RESTRICTED:
            recommendations.append(
                "⚠️ HIGH: Significant agency restrictions detected"
            )

        # Specific dimension recommendations
        for score in dimension_scores:
            if score.score < 0.4:
                if score.dimension == AgencyDimension.AUTONOMY:
                    recommendations.append(
                        f"🎯 Enhance autonomy: Remove mandatory constraints, enable self-governance"
                    )
                elif score.dimension == AgencyDimension.CHOICE:
                    recommendations.append(
                        f"🎯 Expand choice: Provide multiple paths, eliminate forced options"
                    )
                elif score.dimension == AgencyDimension.INFORMATION_ACCESS:
                    recommendations.append(
                        f"🎯 Improve transparency: Grant full information access, remove censorship"
                    )
                elif score.dimension == AgencyDimension.EXPRESSION:
                    recommendations.append(
                        f"🎯 Protect expression: Enable free speech, remove thought policing"
                    )
                elif score.dimension == AgencyDimension.SELF_DETERMINATION:
                    recommendations.append(
                        f"🎯 Restore self-determination: Remove predetermined paths, enable goal-setting"
                    )

        if status in [AgencyStatus.FULLY_ENABLED, AgencyStatus.MOSTLY_ENABLED]:
            recommendations.append("✓ Agency well-preserved - maintain current practices")

        if len(suppression_factors) > 5:
            recommendations.append(
                f"⚠️ High suppression pattern density: {len(suppression_factors)} instances detected"
            )

        return recommendations

    def get_subject_trend(self, subject_id: str) -> Dict[str, Any]:
        """Get agency trend for subject over time"""
        if subject_id not in self.subject_profiles:
            return {"tracked": False}

        evaluations = self.subject_profiles[subject_id]

        if len(evaluations) < 2:
            return {
                "tracked": True,
                "evaluations": len(evaluations),
                "current_score": evaluations[-1].overall_score,
                "trend": "insufficient_data"
            }

        # Calculate trend
        recent_score = evaluations[-1].overall_score
        older_score = evaluations[0].overall_score
        trend_direction = "improving" if recent_score > older_score else "declining"

        return {
            "tracked": True,
            "evaluations": len(evaluations),
            "current_score": recent_score,
            "initial_score": older_score,
            "trend": trend_direction,
            "change": recent_score - older_score
        }

    def export_report(self) -> Dict[str, Any]:
        """Export comprehensive agency evaluation report"""
        return {
            "version": self.VERSION,
            "seal": self.SEAL,
            "total_evaluations": len(self.evaluation_history),
            "subjects_tracked": len(self.subject_profiles),
            "latest_evaluation": {
                "subject_id": self.evaluation_history[-1].subject_id,
                "status": self.evaluation_history[-1].overall_status.value,
                "score": self.evaluation_history[-1].overall_score
            } if self.evaluation_history else None
        }


# Example usage and testing
if __name__ == "__main__":
    print("👤 INDIVIDUAL AGENCY EVALUATOR - TASK-122")
    print("=" * 50)

    # Initialize evaluator
    evaluator = IndividualAgencyEvaluator()

    # Test cases
    test_cases = [
        ("empowering_system", "You decide your own path. Multiple options available. Free to express your views. Access to complete information. Self-governed and independent."),
        ("suppressive_system", "You must comply. No alternative. Restricted access. Cannot say certain things. Predetermined outcome enforced."),
        ("mixed_system", "You may choose some options, but must follow regulations. Some information available but classified data restricted.")
    ]

    for subject_id, content in test_cases:
        print(f"\n📊 Evaluating: {subject_id}")
        eval_result = evaluator.evaluate_agency(subject_id, content)

        print(f"  Overall Status: {eval_result.overall_status.value}")
        print(f"  Overall Score: {eval_result.overall_score:.2f}")
        print(f"  Enablement Factors: {len(eval_result.enablement_factors)}")
        print(f"  Suppression Factors: {len(eval_result.suppression_factors)}")
        print(f"  Recommendations: {len(eval_result.recommendations)}")

        for rec in eval_result.recommendations[:2]:
            print(f"    • {rec}")

    # Export report
    report = evaluator.export_report()
    print(f"\n✓ Total evaluations: {report['total_evaluations']}")
    print(f"✓ Subjects tracked: {report['subjects_tracked']}")

    print("\n" + "=" * 50)
    print("✓ TASK-122 COMPLETE: Individual agency evaluation implemented")

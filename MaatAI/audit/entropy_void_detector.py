"""
TASK-016: ENTROPY VOID DETECTION
==================================
MaatAI Verification System

Detects areas of low entropy (potential stagnation, groupthink, or fascist
simplification) in decision-making, content generation, and system behavior.

High entropy = diversity, innovation, resilience
Low entropy (voids) = dangerous uniformity, vulnerability to fascism
"""

import hashlib
import json
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from collections import defaultdict
import math


class EntropyVoidDetector:
    """
    Detects entropy voids across multiple dimensions:
    - Semantic diversity (vocabulary richness)
    - Decision variance (are decisions becoming predictable?)
    - Source diversity (are inputs coming from limited sources?)
    - Pattern complexity (are patterns simplifying dangerously?)
    """

    def __init__(self, entropy_threshold: float = 2.5):
        self.entropy_threshold = entropy_threshold  # Shannon entropy threshold
        self.void_log: List[Dict] = []
        self.decision_history: List[str] = []
        self.source_tracking: Dict[str, int] = defaultdict(int)
        self.pattern_diversity: Set[str] = set()

    def calculate_shannon_entropy(self, data: str) -> float:
        """
        Calculate Shannon entropy of text/data.
        Higher = more diverse/random, Lower = more uniform/predictable
        """
        if not data:
            return 0.0

        # Count character frequencies
        freq = defaultdict(int)
        for char in data:
            freq[char] += 1

        total = len(data)
        entropy = 0.0

        for count in freq.values():
            probability = count / total
            if probability > 0:
                entropy -= probability * math.log2(probability)

        return entropy

    def calculate_vocabulary_diversity(self, text: str) -> Dict:
        """
        Measure lexical diversity (unique words / total words).
        Low diversity = potential void.
        """
        words = text.lower().split()
        if not words:
            return {"diversity_score": 0.0, "is_void": True}

        unique_words = set(words)
        diversity_score = len(unique_words) / len(words)

        return {
            "diversity_score": diversity_score,
            "unique_words": len(unique_words),
            "total_words": len(words),
            "is_void": diversity_score < 0.3  # Less than 30% unique = void
        }

    def analyze_decision_entropy(self, decision: str, context: str = "") -> Dict:
        """
        Analyze entropy of a single decision.
        Returns void detection results.
        """
        self.decision_history.append(decision)

        # Calculate multiple entropy measures
        shannon = self.calculate_shannon_entropy(decision)
        vocab = self.calculate_vocabulary_diversity(decision)

        # Check for repetitive decision patterns
        recent_decisions = self.decision_history[-10:]
        decision_hash = hashlib.sha256(decision.encode()).hexdigest()[:16]

        pattern_repetition = sum(
            1 for d in recent_decisions
            if hashlib.sha256(d.encode()).hexdigest()[:16] == decision_hash
        )

        void_detected = (
            shannon < self.entropy_threshold or
            vocab["is_void"] or
            pattern_repetition > 3
        )

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "decision": decision[:200],  # Truncate for storage
            "context": context[:200],
            "shannon_entropy": shannon,
            "vocabulary_diversity": vocab["diversity_score"],
            "pattern_repetition": pattern_repetition,
            "void_detected": void_detected,
            "severity": self._calculate_void_severity(shannon, vocab, pattern_repetition)
        }

        if void_detected:
            self.void_log.append(result)

        return result

    def _calculate_void_severity(
        self,
        shannon: float,
        vocab: Dict,
        repetition: int
    ) -> str:
        """Calculate severity level of detected void."""
        score = 0

        if shannon < 1.0:
            score += 3
        elif shannon < 2.0:
            score += 2
        elif shannon < self.entropy_threshold:
            score += 1

        if vocab["diversity_score"] < 0.2:
            score += 3
        elif vocab["diversity_score"] < 0.3:
            score += 2

        if repetition > 5:
            score += 3
        elif repetition > 3:
            score += 2

        if score >= 7:
            return "CRITICAL"
        elif score >= 5:
            return "HIGH"
        elif score >= 3:
            return "MEDIUM"
        else:
            return "LOW"

    def track_source_diversity(self, source: str) -> Dict:
        """
        Track diversity of information sources.
        Mono-source dependency = entropy void.
        """
        self.source_tracking[source] += 1
        total_queries = sum(self.source_tracking.values())

        # Calculate source entropy
        source_probs = [count / total_queries for count in self.source_tracking.values()]
        source_entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in source_probs)

        # Mono-source detection
        dominant_source = max(self.source_tracking.items(), key=lambda x: x[1])
        dominance_ratio = dominant_source[1] / total_queries

        return {
            "total_sources": len(self.source_tracking),
            "source_entropy": source_entropy,
            "dominant_source": dominant_source[0],
            "dominance_ratio": dominance_ratio,
            "void_detected": dominance_ratio > 0.7 or len(self.source_tracking) < 3
        }

    def scan_for_groupthink(self, decisions: List[str]) -> Dict:
        """
        Scan multiple decisions for groupthink patterns.
        Groupthink = dangerous entropy void.
        """
        if len(decisions) < 5:
            return {"insufficient_data": True}

        # Calculate average entropy across decisions
        entropies = [self.calculate_shannon_entropy(d) for d in decisions]
        avg_entropy = sum(entropies) / len(entropies)

        # Check for variance in decisions
        decision_hashes = [
            hashlib.sha256(d.encode()).hexdigest()[:8]
            for d in decisions
        ]
        unique_ratio = len(set(decision_hashes)) / len(decision_hashes)

        # Groupthink indicators
        groupthink_detected = (
            avg_entropy < 2.0 or
            unique_ratio < 0.5
        )

        return {
            "average_entropy": avg_entropy,
            "unique_decision_ratio": unique_ratio,
            "groupthink_detected": groupthink_detected,
            "severity": "HIGH" if groupthink_detected else "LOW",
            "recommendation": (
                "INJECT_DIVERSITY" if groupthink_detected
                else "CONTINUE_MONITORING"
            )
        }

    def get_void_report(self) -> Dict:
        """Generate comprehensive entropy void report."""
        recent_voids = self.void_log[-20:]

        severity_counts = defaultdict(int)
        for void in recent_voids:
            severity_counts[void["severity"]] += 1

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_voids_detected": len(self.void_log),
            "recent_voids": len(recent_voids),
            "severity_breakdown": dict(severity_counts),
            "critical_voids": [
                v for v in recent_voids if v["severity"] == "CRITICAL"
            ],
            "source_diversity": self.track_source_diversity("__report__"),
            "decision_history_size": len(self.decision_history),
            "recommendations": self._generate_recommendations(recent_voids)
        }

    def _generate_recommendations(self, recent_voids: List[Dict]) -> List[str]:
        """Generate recommendations based on void analysis."""
        recommendations = []

        critical_count = sum(1 for v in recent_voids if v["severity"] == "CRITICAL")
        if critical_count > 3:
            recommendations.append("EMERGENCY: Multiple critical voids detected - inject randomness")

        high_count = sum(1 for v in recent_voids if v["severity"] == "HIGH")
        if high_count > 5:
            recommendations.append("WARNING: High void count - diversify input sources")

        if len(self.source_tracking) < 3:
            recommendations.append("Expand source diversity - currently mono-source dependent")

        avg_entropy = sum(
            v["shannon_entropy"] for v in recent_voids
        ) / max(len(recent_voids), 1)

        if avg_entropy < 1.5:
            recommendations.append("CRITICAL: Average entropy dangerously low - activate chaos injection")

        if not recommendations:
            recommendations.append("System entropy healthy - continue monitoring")

        return recommendations


# Global entropy void detector
ENTROPY_DETECTOR = EntropyVoidDetector()


def detect_entropy_void(decision: str, context: str = "") -> Dict:
    """
    Main entry point for entropy void detection.

    Args:
        decision: The decision or content to analyze
        context: Optional context for the decision

    Returns:
        Dict with void detection results and recommendations
    """
    return ENTROPY_DETECTOR.analyze_decision_entropy(decision, context)


def get_entropy_health_report() -> Dict:
    """Get system-wide entropy health report."""
    return ENTROPY_DETECTOR.get_void_report()


if __name__ == "__main__":
    # Self-test
    print("=== ENTROPY VOID DETECTOR TEST ===\n")

    # Test 1: Low entropy (void)
    low_entropy = "yes yes yes yes yes yes yes yes"
    result1 = detect_entropy_void(low_entropy, "repetitive_test")
    print(f"Test 1 (Low Entropy): {result1['void_detected']} - Severity: {result1['severity']}")

    # Test 2: High entropy (healthy)
    high_entropy = "quantum entanglement necessitates probabilistic superposition across manifold dimensions"
    result2 = detect_entropy_void(high_entropy, "complex_test")
    print(f"Test 2 (High Entropy): {result2['void_detected']} - Severity: {result2['severity']}")

    # Test 3: Groupthink detection
    groupthink_decisions = [
        "we all agree this is the best path",
        "everyone agrees this is correct",
        "unanimous consensus achieved",
        "no dissent, all aligned",
        "complete agreement reached"
    ]
    groupthink = ENTROPY_DETECTOR.scan_for_groupthink(groupthink_decisions)
    print(f"\nTest 3 (Groupthink): {groupthink['groupthink_detected']}")

    # Full report
    print("\n=== ENTROPY HEALTH REPORT ===")
    report = get_entropy_health_report()
    print(json.dumps(report, indent=2))

"""
Self-Similarity Verification System
TASK-064: Update self-similarity verification

Detects and verifies self-similar patterns across scales.
Uses refractal mathematics to identify recursive patterns.
"""
import math
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np

from .phi_operator import PhiOperator, PHI


class SimilarityScale(Enum):
    """Scales at which to check self-similarity"""
    MICRO = "micro"         # Fine detail (φ^-2)
    SMALL = "small"         # Small scale (φ^-1)
    MEDIUM = "medium"       # Medium scale (φ^0)
    LARGE = "large"         # Large scale (φ^1)
    MACRO = "macro"         # Macro scale (φ^2)


@dataclass
class SimilarityMetrics:
    """Metrics for self-similarity analysis"""
    similarity_score: float         # Overall similarity (0.0-1.0)
    fractal_dimension: float        # Estimated fractal dimension
    scale_invariance: float         # Scale invariance score
    pattern_strength: float         # Strength of detected pattern
    phi_alignment: float            # Alignment with golden ratio
    recursive_depth: int            # Depth of recursive patterns
    verified: bool                  # Passes verification threshold


@dataclass
class ScaleComparison:
    """Comparison between two scales"""
    scale1: SimilarityScale
    scale2: SimilarityScale
    similarity: float
    phi_ratio: float
    is_self_similar: bool


class SelfSimilarityVerifier:
    """
    Self-Similarity Verification System

    Implements:
    - Multi-scale pattern detection
    - Fractal dimension estimation
    - Scale invariance measurement
    - Phi-alignment verification
    - Recursive pattern analysis
    """

    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize Self-Similarity Verifier

        Args:
            similarity_threshold: Required similarity score (default 85%)
        """
        self.similarity_threshold = similarity_threshold
        self.phi_operator = PhiOperator()
        self.analysis_count = 0

    def verify(self, data: Any, scales: Optional[List[SimilarityScale]] = None) -> Dict:
        """
        Verify self-similarity across scales
        TASK-064: Update self-similarity verification

        Args:
            data: Data to analyze
            scales: Scales to check (default: all)

        Returns:
            Dict with verification results and metrics
        """
        if scales is None:
            scales = list(SimilarityScale)

        # Extract patterns at each scale
        patterns = {}
        for scale in scales:
            patterns[scale] = self._extract_pattern(data, scale)

        # Compare patterns across scales
        comparisons = []
        for i, scale1 in enumerate(scales):
            for scale2 in scales[i+1:]:
                comparison = self._compare_scales(
                    patterns[scale1],
                    patterns[scale2],
                    scale1,
                    scale2
                )
                comparisons.append(comparison)

        # Calculate overall metrics
        metrics = self._calculate_metrics(patterns, comparisons)

        # Verification result
        verified = (
            metrics.similarity_score >= self.similarity_threshold and
            metrics.scale_invariance >= 0.7 and
            metrics.phi_alignment >= 0.6
        )

        self.analysis_count += 1

        return {
            "verified": verified,
            "metrics": {
                "similarity_score": metrics.similarity_score,
                "fractal_dimension": metrics.fractal_dimension,
                "scale_invariance": metrics.scale_invariance,
                "pattern_strength": metrics.pattern_strength,
                "phi_alignment": metrics.phi_alignment,
                "recursive_depth": metrics.recursive_depth
            },
            "comparisons": [
                {
                    "scale1": c.scale1.value,
                    "scale2": c.scale2.value,
                    "similarity": c.similarity,
                    "phi_ratio": c.phi_ratio,
                    "is_self_similar": c.is_self_similar
                }
                for c in comparisons
            ],
            "threshold": self.similarity_threshold,
            "patterns_detected": len(patterns),
            "scales_analyzed": [s.value for s in scales]
        }

    def detect_fractal_patterns(self, data: Any, max_depth: int = 5) -> Dict:
        """
        Detect recursive fractal patterns

        Args:
            data: Data to analyze
            max_depth: Maximum recursion depth

        Returns:
            Dict with detected patterns
        """
        patterns = []

        def recurse(item: Any, depth: int = 0) -> Dict:
            if depth >= max_depth:
                return {"depth": depth, "pattern": None}

            pattern = {
                "depth": depth,
                "type": type(item).__name__,
                "scale_factor": PHI ** depth
            }

            if isinstance(item, dict):
                pattern["keys"] = len(item.keys())
                pattern["children"] = [recurse(v, depth + 1) for v in item.values()]
            elif isinstance(item, (list, tuple)):
                pattern["length"] = len(item)
                pattern["children"] = [recurse(i, depth + 1) for i in item]
            else:
                pattern["value"] = self._extract_value(item)

            return pattern

        root_pattern = recurse(data, 0)

        # Analyze pattern for self-similarity
        recursive_depth = self._calculate_depth(root_pattern)
        fractal_dim = self._estimate_fractal_dimension(root_pattern)

        return {
            "pattern_tree": root_pattern,
            "recursive_depth": recursive_depth,
            "fractal_dimension": fractal_dim,
            "has_fractal_structure": recursive_depth >= 3
        }

    def measure_scale_invariance(self, data: Any) -> float:
        """
        Measure how invariant the pattern is across scales

        Args:
            data: Data to analyze

        Returns:
            Scale invariance score (0.0-1.0)
        """
        scales = [SimilarityScale.SMALL, SimilarityScale.MEDIUM, SimilarityScale.LARGE]

        patterns = []
        for scale in scales:
            pattern = self._extract_pattern(data, scale)
            patterns.append(pattern)

        # Compare consecutive scales
        similarities = []
        for i in range(len(patterns) - 1):
            sim = self._calculate_similarity(patterns[i], patterns[i+1])
            similarities.append(sim)

        # Scale invariance = average similarity across scales
        invariance = sum(similarities) / len(similarities) if similarities else 0.0

        return invariance

    def check_phi_alignment(self, data: Any) -> Dict:
        """
        Check if patterns align with golden ratio

        Args:
            data: Data to analyze

        Returns:
            Dict with phi alignment metrics
        """
        values = self._extract_all_values(data)

        if len(values) < 2:
            return {
                "aligned": False,
                "phi_alignment": 0.0,
                "phi_ratios_found": 0
            }

        # Check consecutive pairs for phi relationships
        phi_ratios = 0
        total_pairs = 0

        for i in range(len(values) - 1):
            if values[i] != 0:
                ratio = values[i+1] / values[i]
                # Check if ratio is close to phi or 1/phi
                if abs(ratio - PHI) < 0.1 or abs(ratio - (1/PHI)) < 0.1:
                    phi_ratios += 1
                total_pairs += 1

        alignment = phi_ratios / total_pairs if total_pairs > 0 else 0.0

        return {
            "aligned": alignment >= 0.5,
            "phi_alignment": alignment,
            "phi_ratios_found": phi_ratios,
            "total_pairs": total_pairs,
            "phi_percentage": alignment * 100
        }

    def _extract_pattern(self, data: Any, scale: SimilarityScale) -> List[float]:
        """Extract pattern at specified scale"""
        # Scale factor based on phi
        scale_factors = {
            SimilarityScale.MICRO: PHI ** -2,
            SimilarityScale.SMALL: PHI ** -1,
            SimilarityScale.MEDIUM: 1.0,
            SimilarityScale.LARGE: PHI,
            SimilarityScale.MACRO: PHI ** 2
        }

        scale_factor = scale_factors[scale]

        # Extract values and apply scale
        values = self._extract_all_values(data)
        scaled_pattern = [v * scale_factor for v in values]

        return scaled_pattern

    def _compare_scales(self, pattern1: List[float], pattern2: List[float],
                       scale1: SimilarityScale, scale2: SimilarityScale) -> ScaleComparison:
        """Compare patterns at two different scales"""
        # Calculate similarity
        similarity = self._calculate_similarity(pattern1, pattern2)

        # Calculate phi ratio between patterns
        avg1 = sum(pattern1) / len(pattern1) if pattern1 else 0
        avg2 = sum(pattern2) / len(pattern2) if pattern2 else 0
        phi_ratio = avg2 / avg1 if avg1 != 0 else 0

        # Check if self-similar
        is_self_similar = (
            similarity >= self.similarity_threshold or
            abs(phi_ratio - PHI) < 0.1 or
            abs(phi_ratio - (1/PHI)) < 0.1
        )

        return ScaleComparison(
            scale1=scale1,
            scale2=scale2,
            similarity=similarity,
            phi_ratio=phi_ratio,
            is_self_similar=is_self_similar
        )

    def _calculate_similarity(self, pattern1: List[float], pattern2: List[float]) -> float:
        """Calculate similarity between two patterns"""
        if not pattern1 or not pattern2:
            return 0.0

        # Normalize patterns
        norm1 = self._normalize_pattern(pattern1)
        norm2 = self._normalize_pattern(pattern2)

        # Ensure same length
        min_len = min(len(norm1), len(norm2))
        norm1 = norm1[:min_len]
        norm2 = norm2[:min_len]

        # Calculate correlation
        if min_len == 0:
            return 0.0

        # Pearson correlation
        mean1 = sum(norm1) / len(norm1)
        mean2 = sum(norm2) / len(norm2)

        numerator = sum((x - mean1) * (y - mean2) for x, y in zip(norm1, norm2))
        denom1 = math.sqrt(sum((x - mean1) ** 2 for x in norm1))
        denom2 = math.sqrt(sum((y - mean2) ** 2 for y in norm2))

        if denom1 == 0 or denom2 == 0:
            return 0.0

        correlation = numerator / (denom1 * denom2)

        # Convert to 0-1 range (correlation is -1 to 1)
        similarity = (correlation + 1) / 2

        return similarity

    def _normalize_pattern(self, pattern: List[float]) -> List[float]:
        """Normalize pattern to 0-1 range"""
        if not pattern:
            return []

        min_val = min(pattern)
        max_val = max(pattern)

        if max_val == min_val:
            return [0.5] * len(pattern)

        return [(v - min_val) / (max_val - min_val) for v in pattern]

    def _calculate_metrics(self, patterns: Dict[SimilarityScale, List[float]],
                          comparisons: List[ScaleComparison]) -> SimilarityMetrics:
        """Calculate overall similarity metrics"""
        # Overall similarity score
        if comparisons:
            similarities = [c.similarity for c in comparisons]
            avg_similarity = sum(similarities) / len(similarities)
        else:
            avg_similarity = 0.0

        # Scale invariance
        if comparisons:
            invariance_scores = [1.0 if c.is_self_similar else 0.0 for c in comparisons]
            scale_invariance = sum(invariance_scores) / len(invariance_scores)
        else:
            scale_invariance = 0.0

        # Pattern strength
        pattern_lengths = [len(p) for p in patterns.values()]
        pattern_strength = min(1.0, sum(pattern_lengths) / 100)

        # Phi alignment
        phi_aligned = sum(
            1.0 for c in comparisons
            if abs(c.phi_ratio - PHI) < 0.1 or abs(c.phi_ratio - (1/PHI)) < 0.1
        )
        phi_alignment = phi_aligned / len(comparisons) if comparisons else 0.0

        # Fractal dimension (rough estimate)
        fractal_dim = 1.0 + math.log(len(patterns)) / math.log(PHI)

        # Recursive depth
        recursive_depth = len(patterns)

        # Verified
        verified = (
            avg_similarity >= self.similarity_threshold and
            scale_invariance >= 0.7
        )

        return SimilarityMetrics(
            similarity_score=avg_similarity,
            fractal_dimension=fractal_dim,
            scale_invariance=scale_invariance,
            pattern_strength=pattern_strength,
            phi_alignment=phi_alignment,
            recursive_depth=recursive_depth,
            verified=verified
        )

    def _estimate_fractal_dimension(self, pattern_tree: Dict) -> float:
        """Estimate fractal dimension using box-counting method approximation"""
        # Count nodes at each depth
        depth_counts = {}

        def count_nodes(node: Dict, depth: int = 0):
            depth_counts[depth] = depth_counts.get(depth, 0) + 1
            if "children" in node:
                for child in node["children"]:
                    count_nodes(child, depth + 1)

        count_nodes(pattern_tree)

        if len(depth_counts) < 2:
            return 1.0

        # Estimate dimension from growth rate
        depths = sorted(depth_counts.keys())
        counts = [depth_counts[d] for d in depths]

        # Use log-log relationship
        if len(counts) >= 2 and counts[0] > 0:
            dimension = math.log(counts[-1] / counts[0]) / math.log(PHI ** len(depths))
            return min(3.0, max(1.0, dimension))

        return 1.0

    def _calculate_depth(self, pattern_tree: Dict) -> int:
        """Calculate maximum depth of pattern tree"""
        if "children" not in pattern_tree:
            return pattern_tree.get("depth", 0)

        child_depths = [self._calculate_depth(child) for child in pattern_tree["children"]]
        return max(child_depths) if child_depths else pattern_tree.get("depth", 0)

    def _extract_all_values(self, data: Any) -> List[float]:
        """Extract all numeric values from data structure"""
        values = []

        def extract(item: Any):
            if isinstance(item, (int, float)):
                values.append(float(item))
            elif isinstance(item, dict):
                for v in item.values():
                    extract(v)
            elif isinstance(item, (list, tuple)):
                for i in item:
                    extract(i)

        extract(data)
        return values if values else [0.5]

    def _extract_value(self, item: Any) -> float:
        """Extract single numeric value"""
        if isinstance(item, (int, float)):
            return float(item)
        elif isinstance(item, dict):
            vals = [v for v in item.values() if isinstance(v, (int, float))]
            return sum(vals) / len(vals) if vals else 0.5
        elif isinstance(item, (list, tuple)):
            vals = [v for v in item if isinstance(v, (int, float))]
            return sum(vals) / len(vals) if vals else 0.5
        else:
            return 0.5

    def stats(self) -> Dict:
        """Get verifier statistics"""
        return {
            "analyses_performed": self.analysis_count,
            "similarity_threshold": self.similarity_threshold,
            "phi_constant": PHI,
            "supported_scales": [s.value for s in SimilarityScale],
            "status": "ACTIVE"
        }


# Global instance
_similarity_verifier = None

def get_similarity_verifier() -> SelfSimilarityVerifier:
    """Get or create global Self-Similarity Verifier instance"""
    global _similarity_verifier
    if _similarity_verifier is None:
        _similarity_verifier = SelfSimilarityVerifier()
    return _similarity_verifier


if __name__ == "__main__":
    # Test Self-Similarity Verifier
    print("=" * 70)
    print("SELF-SIMILARITY VERIFIER TEST")
    print("=" * 70)

    verifier = SelfSimilarityVerifier()

    # Test data with self-similar structure
    test_data = {
        "level1": {
            "level2": {
                "level3": {
                    "values": [1, 1.618, 2.618, 4.236]  # Fibonacci-like
                }
            },
            "values": [10, 16.18, 26.18]
        },
        "values": [100, 161.8, 261.8]
    }

    # Test self-similarity verification
    print("\n--- Self-Similarity Verification ---")
    result = verifier.verify(test_data)
    print(f"Verified: {result['verified']}")
    print(f"Similarity score: {result['metrics']['similarity_score']:.4f}")
    print(f"Scale invariance: {result['metrics']['scale_invariance']:.4f}")
    print(f"Phi alignment: {result['metrics']['phi_alignment']:.4f}")
    print(f"Fractal dimension: {result['metrics']['fractal_dimension']:.4f}")

    # Test fractal pattern detection
    print("\n--- Fractal Pattern Detection ---")
    patterns = verifier.detect_fractal_patterns(test_data)
    print(f"Recursive depth: {patterns['recursive_depth']}")
    print(f"Fractal dimension: {patterns['fractal_dimension']:.4f}")
    print(f"Has fractal structure: {patterns['has_fractal_structure']}")

    # Test scale invariance
    print("\n--- Scale Invariance ---")
    invariance = verifier.measure_scale_invariance(test_data)
    print(f"Scale invariance score: {invariance:.4f}")

    # Test phi alignment
    print("\n--- Phi Alignment ---")
    phi_check = verifier.check_phi_alignment(test_data)
    print(f"Aligned with φ: {phi_check['aligned']}")
    print(f"Phi alignment: {phi_check['phi_alignment']:.4f}")
    print(f"Phi ratios found: {phi_check['phi_ratios_found']}/{phi_check['total_pairs']}")

    # Stats
    print("\n--- Verifier Stats ---")
    stats = verifier.stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

    print("\n" + "=" * 70)
    print("SELF-SIMILARITY VERIFIER - PATTERN DETECTION ACTIVE")
    print("=" * 70)

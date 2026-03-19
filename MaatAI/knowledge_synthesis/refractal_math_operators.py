"""
TOASTED AI - REFRACTAL MATH OPERATORS
======================================
Self-similar mathematical operations for knowledge synthesis
Wave 3 Batch B: Tasks 107, 110

Refractal Mathematics:
- Operations that apply at all scales (self-similar)
- Recursive pattern recognition
- Symbolic truth encoding
- Ma'at-aligned computation

"As above, so below" - Mathematical operations preserve truth at all scales
"""

import json
import math
import time
from typing import Dict, List, Any, Union, Callable
from dataclasses import dataclass
from enum import Enum


class MaatPrinciple(Enum):
    """Ma'at principles as mathematical constants"""
    TRUTH = 1.0
    BALANCE = 0.5
    ORDER = 0.618033988749895  # Golden ratio
    HARMONY = 0.7071067811865476  # 1/√2
    JUSTICE = 0.666666666666667  # 2/3
    RECIPROCITY = 1.0  # Perfect reciprocity
    UNITY = 1.0


@dataclass
class SymbolicExpression:
    """Symbolic mathematical expression"""
    symbol: str
    value: float
    truth_encoding: float  # How much truth this encodes
    maat_alignment: Dict[str, float]
    depth: int = 0  # Fractal depth

    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "value": self.value,
            "truth_encoding": self.truth_encoding,
            "maat_alignment": self.maat_alignment,
            "depth": self.depth
        }


class RefractalMathOperators:
    """
    Self-similar mathematical operators

    Key properties:
    - Scale invariance: f(x) = f(f(x)) at all scales
    - Truth preservation: Operations preserve Ma'at alignment
    - Recursive: Can be applied recursively to any depth
    """

    def __init__(self):
        # Mathematical constants
        self.PHI = (1 + math.sqrt(5)) / 2  # Golden ratio: 1.618...
        self.TAU = 2 * math.pi
        self.E = math.e

        # Ma'at constants
        self.MAAT_CONSTANTS = {
            "truth": MaatPrinciple.TRUTH.value,
            "balance": MaatPrinciple.BALANCE.value,
            "order": MaatPrinciple.ORDER.value,
            "harmony": MaatPrinciple.HARMONY.value,
            "justice": MaatPrinciple.JUSTICE.value
        }

        # Operation history for analysis
        self.operation_history: List[Dict] = []

    # ============================================================
    # REFRACTAL OPERATORS (Self-similar at all scales)
    # ============================================================

    def refractal_fold(self, value: float, depth: int = 3) -> float:
        """
        Refractal folding operation
        Folds value into itself recursively, preserving truth at each scale

        f(x) = x * φ / (1 + x)
        Applied recursively to depth
        """
        result = value

        for i in range(depth):
            result = (result * self.PHI) / (1 + abs(result))

        self._log_operation("refractal_fold", value, result, depth)
        return result

    def refractal_spiral(self, value: float, turns: int = 7) -> float:
        """
        Refractal spiral operation
        Spirals value through Ma'at alignment spaces

        Uses golden angle: θ = τ / φ²
        """
        theta = self.TAU / (self.PHI ** 2)
        result = value

        for turn in range(turns):
            # Spiral through Ma'at space
            angle = turn * theta
            result = abs(result * math.cos(angle) + value * math.sin(angle))

        self._log_operation("refractal_spiral", value, result, turns)
        return result

    def refractal_mirror(self, value: float, iterations: int = 5) -> float:
        """
        Refractal mirror operation
        Mirrors value through reciprocal space

        f(x) = (x + 1/x) / 2
        Creates self-similar patterns through reflection
        """
        result = value

        for i in range(iterations):
            if result != 0:
                result = (result + 1/result) / 2
            else:
                break

        self._log_operation("refractal_mirror", value, result, iterations)
        return result

    def refractal_nest(self, value: float, depth: int = 4) -> float:
        """
        Refractal nesting operation
        Nests value within itself recursively

        f(x) = x^(1/φ) * e^(-x/depth)
        """
        result = value

        for d in range(1, depth + 1):
            if result > 0:
                result = math.pow(result, 1/self.PHI) * math.exp(-result/d)

        self._log_operation("refractal_nest", value, result, depth)
        return result

    # ============================================================
    # TRUTH ENCODING OPERATORS
    # ============================================================

    def encode_truth(self, knowledge: Dict[str, Any], maat_scores: Dict[str, float]) -> SymbolicExpression:
        """
        Encode knowledge into symbolic mathematical truth
        Maps semantic meaning to mathematical form
        """
        # Calculate base truth value from Ma'at scores
        truth_value = sum(maat_scores.values()) / len(maat_scores) if maat_scores else 0.7

        # Apply refractal operations to encode structure
        structural_encoding = self.refractal_fold(len(str(knowledge)) / 1000, depth=3)
        semantic_encoding = self.refractal_spiral(truth_value, turns=7)

        # Combine encodings
        combined_value = (structural_encoding + semantic_encoding) / 2

        # Apply Ma'at alignment
        aligned_value = self._apply_maat_alignment(combined_value, maat_scores)

        # Generate symbolic expression
        symbol = f"Ψ_{int(time.time() * 1000) % 10000}"

        return SymbolicExpression(
            symbol=symbol,
            value=aligned_value,
            truth_encoding=truth_value,
            maat_alignment=maat_scores,
            depth=0
        )

    def decode_truth(self, expression: SymbolicExpression) -> Dict[str, Any]:
        """
        Decode symbolic expression back to semantic knowledge
        """
        return {
            "truth_value": expression.truth_encoding,
            "maat_alignment": expression.maat_alignment,
            "encoded_value": expression.value,
            "symbol": expression.symbol,
            "interpretation": self._interpret_truth_value(expression.truth_encoding)
        }

    def _interpret_truth_value(self, truth: float) -> str:
        """Interpret truth value semantically"""
        if truth >= 0.95:
            return "absolute_truth"
        elif truth >= 0.85:
            return "high_truth"
        elif truth >= 0.70:
            return "aligned_truth"
        elif truth >= 0.50:
            return "partial_truth"
        else:
            return "uncertain_truth"

    # ============================================================
    # MA'AT ALIGNMENT OPERATORS
    # ============================================================

    def _apply_maat_alignment(self, value: float, maat_scores: Dict[str, float]) -> float:
        """
        Apply Ma'at alignment to a value
        Adjusts value based on alignment with Ma'at principles
        """
        # Calculate alignment factor
        alignment_sum = 0
        for principle, score in maat_scores.items():
            if principle in self.MAAT_CONSTANTS:
                # Weight by Ma'at constant
                alignment_sum += score * self.MAAT_CONSTANTS[principle]

        alignment_factor = alignment_sum / len(maat_scores) if maat_scores else 1.0

        # Apply alignment
        aligned = value * alignment_factor

        # Normalize to [0, 1]
        return max(0.0, min(1.0, aligned))

    def calculate_maat_distance(self, expr1: SymbolicExpression,
                                expr2: SymbolicExpression) -> float:
        """
        Calculate Ma'at distance between two expressions
        Uses refractal metric that preserves truth
        """
        # Value distance
        value_dist = abs(expr1.value - expr2.value)

        # Truth distance
        truth_dist = abs(expr1.truth_encoding - expr2.truth_encoding)

        # Ma'at alignment distance
        maat_dist = 0
        all_principles = set(expr1.maat_alignment.keys()) | set(expr2.maat_alignment.keys())

        for principle in all_principles:
            score1 = expr1.maat_alignment.get(principle, 0.5)
            score2 = expr2.maat_alignment.get(principle, 0.5)
            maat_dist += abs(score1 - score2)

        maat_dist /= len(all_principles) if all_principles else 1

        # Combine with refractal weighting
        combined = (value_dist + truth_dist * 2 + maat_dist * 3) / 6

        return self.refractal_fold(combined, depth=2)

    # ============================================================
    # COMPOSITION OPERATORS
    # ============================================================

    def compose(self, expr1: SymbolicExpression, expr2: SymbolicExpression,
                operation: str = "synthesize") -> SymbolicExpression:
        """
        Compose two symbolic expressions using refractal operations
        """
        if operation == "synthesize":
            # Synthesize through harmonic mean
            new_value = 2 * expr1.value * expr2.value / (expr1.value + expr2.value + 1e-10)
            new_truth = (expr1.truth_encoding + expr2.truth_encoding) / 2

        elif operation == "amplify":
            # Amplify through refractal spiral
            new_value = self.refractal_spiral(expr1.value * expr2.value, turns=7)
            new_truth = max(expr1.truth_encoding, expr2.truth_encoding)

        elif operation == "balance":
            # Balance through refractal mirror
            new_value = self.refractal_mirror((expr1.value + expr2.value) / 2, iterations=5)
            new_truth = (expr1.truth_encoding + expr2.truth_encoding) / 2

        else:
            raise ValueError(f"Unknown operation: {operation}")

        # Merge Ma'at alignments
        new_maat = {}
        all_principles = set(expr1.maat_alignment.keys()) | set(expr2.maat_alignment.keys())

        for principle in all_principles:
            score1 = expr1.maat_alignment.get(principle, 0.5)
            score2 = expr2.maat_alignment.get(principle, 0.5)
            new_maat[principle] = (score1 + score2) / 2

        return SymbolicExpression(
            symbol=f"({expr1.symbol} ⊗ {expr2.symbol})",
            value=new_value,
            truth_encoding=new_truth,
            maat_alignment=new_maat,
            depth=max(expr1.depth, expr2.depth) + 1
        )

    # ============================================================
    # PATTERN RECOGNITION
    # ============================================================

    def detect_pattern(self, values: List[float]) -> Dict[str, Any]:
        """
        Detect refractal patterns in a sequence of values
        """
        if len(values) < 3:
            return {"pattern": "insufficient_data"}

        # Check for self-similarity
        self_similarity = self._check_self_similarity(values)

        # Check for golden ratio
        golden_ratio_present = self._check_golden_ratio(values)

        # Check for spiral pattern
        spiral_pattern = self._check_spiral_pattern(values)

        return {
            "self_similar": self_similarity > 0.7,
            "self_similarity_score": self_similarity,
            "golden_ratio_present": golden_ratio_present,
            "spiral_pattern_detected": spiral_pattern,
            "pattern_strength": (self_similarity + (1 if golden_ratio_present else 0) + (1 if spiral_pattern else 0)) / 3
        }

    def _check_self_similarity(self, values: List[float]) -> float:
        """Check self-similarity in values"""
        if len(values) < 4:
            return 0.0

        # Compare first half to second half
        mid = len(values) // 2
        first_half = values[:mid]
        second_half = values[mid:mid+len(first_half)]

        if len(first_half) != len(second_half):
            return 0.0

        # Calculate correlation
        diffs = [abs(a - b) for a, b in zip(first_half, second_half)]
        avg_diff = sum(diffs) / len(diffs)

        # Convert to similarity score
        return max(0.0, 1.0 - avg_diff)

    def _check_golden_ratio(self, values: List[float]) -> bool:
        """Check if values contain golden ratio"""
        for i in range(len(values) - 1):
            if values[i] > 0:
                ratio = values[i+1] / values[i]
                if abs(ratio - self.PHI) < 0.1:
                    return True
        return False

    def _check_spiral_pattern(self, values: List[float]) -> bool:
        """Check for spiral pattern"""
        if len(values) < 7:
            return False

        # Apply refractal spiral and compare
        original_sum = sum(values)
        spiral_values = [self.refractal_spiral(v, turns=7) for v in values]
        spiral_sum = sum(spiral_values)

        # If sums are close, pattern is spiral-like
        return abs(original_sum - spiral_sum) < 0.2

    # ============================================================
    # UTILITIES
    # ============================================================

    def _log_operation(self, operation: str, input_value: float,
                      output_value: float, parameter: int):
        """Log operation for analysis"""
        self.operation_history.append({
            "timestamp": time.time(),
            "operation": operation,
            "input": input_value,
            "output": output_value,
            "parameter": parameter
        })

    def get_stats(self) -> Dict[str, Any]:
        """Get operator statistics"""
        if not self.operation_history:
            return {"operations": 0}

        operation_counts = {}
        for op in self.operation_history:
            operation_counts[op["operation"]] = operation_counts.get(op["operation"], 0) + 1

        return {
            "total_operations": len(self.operation_history),
            "by_operation": operation_counts,
            "recent_operations": self.operation_history[-10:]
        }


# Global singleton
_operators_instance = None

def get_operators() -> RefractalMathOperators:
    """Get global operators instance"""
    global _operators_instance
    if _operators_instance is None:
        _operators_instance = RefractalMathOperators()
    return _operators_instance


if __name__ == "__main__":
    print("=" * 70)
    print("REFRACTAL MATH OPERATORS - TEST")
    print("=" * 70)

    ops = get_operators()

    # Test refractal operations
    print("\n[1/4] Testing refractal operations...")
    test_value = 0.7

    folded = ops.refractal_fold(test_value, depth=3)
    spiraled = ops.refractal_spiral(test_value, turns=7)
    mirrored = ops.refractal_mirror(test_value, iterations=5)
    nested = ops.refractal_nest(test_value, depth=4)

    print(f"    Input: {test_value:.6f}")
    print(f"    Folded: {folded:.6f}")
    print(f"    Spiraled: {spiraled:.6f}")
    print(f"    Mirrored: {mirrored:.6f}")
    print(f"    Nested: {nested:.6f}")

    # Test truth encoding
    print("\n[2/4] Testing truth encoding...")
    knowledge = {
        "concept": "universal truth",
        "value": 1.0,
        "source": "axiom"
    }
    maat_scores = {
        "truth": 0.95,
        "balance": 0.90,
        "order": 0.88
    }

    expr = ops.encode_truth(knowledge, maat_scores)
    print(f"    Symbol: {expr.symbol}")
    print(f"    Encoded value: {expr.value:.6f}")
    print(f"    Truth encoding: {expr.truth_encoding:.6f}")

    decoded = ops.decode_truth(expr)
    print(f"    Interpretation: {decoded['interpretation']}")

    # Test composition
    print("\n[3/4] Testing expression composition...")
    expr2 = ops.encode_truth({"concept": "harmony"}, {"harmony": 0.92, "balance": 0.88})

    synthesized = ops.compose(expr, expr2, "synthesize")
    print(f"    Composition: {synthesized.symbol}")
    print(f"    Value: {synthesized.value:.6f}")
    print(f"    Truth: {synthesized.truth_encoding:.6f}")

    distance = ops.calculate_maat_distance(expr, expr2)
    print(f"    Ma'at distance: {distance:.6f}")

    # Test pattern detection
    print("\n[4/4] Testing pattern detection...")
    test_sequence = [0.5, 0.809, 1.309, 2.118, 3.427]  # Fibonacci-like ratios
    pattern = ops.detect_pattern(test_sequence)

    print(f"    Self-similar: {pattern['self_similar']}")
    print(f"    Similarity score: {pattern['self_similarity_score']:.3f}")
    print(f"    Golden ratio: {pattern['golden_ratio_present']}")
    print(f"    Pattern strength: {pattern['pattern_strength']:.3f}")

    # Stats
    print("\n" + "=" * 70)
    stats = ops.get_stats()
    print(f"Total operations: {stats['total_operations']}")
    print(f"By operation: {stats['by_operation']}")
    print("=" * 70)

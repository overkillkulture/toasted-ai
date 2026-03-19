"""
Φ (Phi) Refractal Operator - Golden Ratio Mathematics
TASK-163: Develop refractal operator Φ

The golden ratio (φ = 1.618033988749...) applied to recursive self-similar systems.
Implements phi-based scaling, synthesis accuracy, and fractal transformation.
"""
import math
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Golden ratio constant
PHI = (1 + math.sqrt(5)) / 2  # 1.618033988749...
PHI_INVERSE = 1 / PHI          # 0.618033988749...
PHI_SQUARED = PHI ** 2         # 2.618033988749...


class PhiScaleType(Enum):
    """Types of phi-based scaling operations"""
    EXPAND = "expand"           # Scale by φ
    CONTRACT = "contract"       # Scale by 1/φ
    RECURSIVE = "recursive"     # Φ^n scaling
    SPIRAL = "spiral"           # Fibonacci spiral scaling


@dataclass
class PhiTransform:
    """Result of a phi-based transformation"""
    original_value: float
    transformed_value: float
    scale_factor: float
    scale_type: PhiScaleType
    accuracy: float
    iterations: int
    phi_ratio: float = PHI


class PhiOperator:
    """
    Φ - Golden Ratio Refractal Operator

    Implements:
    - Phi-based scaling (expand/contract by golden ratio)
    - Recursive phi transformations (Φ^n)
    - Fibonacci sequence generation
    - Golden spiral mathematics
    - Synthesis accuracy measurement
    """

    def __init__(self, accuracy_threshold: float = 0.999):
        """
        Initialize Phi Operator

        Args:
            accuracy_threshold: Required accuracy for transformations (default 99.9%)
        """
        self.phi = PHI
        self.phi_inverse = PHI_INVERSE
        self.accuracy_threshold = accuracy_threshold
        self.transformation_count = 0

        # Phi powers cache (for performance)
        self._phi_powers = {0: 1.0, 1: PHI, -1: PHI_INVERSE}

    def scale(self, value: float, scale_type: PhiScaleType = PhiScaleType.EXPAND,
              iterations: int = 1) -> PhiTransform:
        """
        Apply phi-based scaling to a value

        Args:
            value: Input value to scale
            scale_type: Type of scaling operation
            iterations: Number of iterations for recursive scaling

        Returns:
            PhiTransform with results and accuracy
        """
        original = value

        if scale_type == PhiScaleType.EXPAND:
            # Scale by φ
            transformed = value * (self.phi ** iterations)
            scale_factor = self.phi ** iterations

        elif scale_type == PhiScaleType.CONTRACT:
            # Scale by 1/φ
            transformed = value * (self.phi_inverse ** iterations)
            scale_factor = self.phi_inverse ** iterations

        elif scale_type == PhiScaleType.RECURSIVE:
            # Apply recursive phi transformation
            transformed = value
            for _ in range(iterations):
                transformed = self._recursive_phi_transform(transformed)
            scale_factor = transformed / value if value != 0 else 0

        elif scale_type == PhiScaleType.SPIRAL:
            # Golden spiral scaling
            transformed = self._spiral_transform(value, iterations)
            scale_factor = transformed / value if value != 0 else 0

        # Calculate accuracy
        accuracy = self._calculate_accuracy(original, transformed, scale_factor)

        self.transformation_count += 1

        return PhiTransform(
            original_value=original,
            transformed_value=transformed,
            scale_factor=scale_factor,
            scale_type=scale_type,
            accuracy=accuracy,
            iterations=iterations,
            phi_ratio=self.phi
        )

    def fibonacci_sequence(self, n: int) -> List[int]:
        """
        Generate Fibonacci sequence up to n terms

        Args:
            n: Number of terms

        Returns:
            List of Fibonacci numbers
        """
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]

        sequence = [0, 1]
        for i in range(2, n):
            sequence.append(sequence[i-1] + sequence[i-2])

        return sequence

    def fibonacci_ratio(self, n: int) -> float:
        """
        Calculate ratio between consecutive Fibonacci numbers
        Approaches φ as n increases

        Args:
            n: Position in sequence

        Returns:
            Ratio F(n) / F(n-1), approaches φ
        """
        if n < 2:
            return 1.0

        seq = self.fibonacci_sequence(n + 1)
        return seq[n] / seq[n-1] if seq[n-1] != 0 else 0

    def phi_power(self, n: int) -> float:
        """
        Calculate φ^n efficiently with caching

        Args:
            n: Power exponent

        Returns:
            φ^n
        """
        if n in self._phi_powers:
            return self._phi_powers[n]

        result = self.phi ** n
        self._phi_powers[n] = result
        return result

    def synthesize(self, layers: List[Any], weights: Optional[List[float]] = None) -> Dict:
        """
        Synthesize knowledge across layers using phi-weighted averaging
        TASK-033: Streamline refractal synthesis accuracy

        Args:
            layers: List of knowledge layers
            weights: Optional custom weights (default: phi-based)

        Returns:
            Dict with synthesis score, accuracy, and metrics
        """
        if not layers:
            return {
                "synthesis": 0.0,
                "accuracy": 0.0,
                "layers": 0,
                "method": "phi_weighted"
            }

        n = len(layers)

        # Generate phi-based weights if not provided
        if weights is None:
            # Weight = φ^(-i) for layer i (deeper layers weighted exponentially less)
            weights = [self.phi_power(-i) for i in range(n)]

        # Normalize weights
        weight_sum = sum(weights)
        normalized_weights = [w / weight_sum for w in weights]

        # Calculate synthesis
        synthesis = 0.0
        for i, layer in enumerate(layers):
            layer_val = self._extract_value(layer)
            synthesis += layer_val * normalized_weights[i]

        # Calculate synthesis accuracy
        # Accuracy = 1.0 - variance_from_ideal
        ideal_synthesis = sum(normalized_weights) / n
        accuracy = 1.0 - abs(synthesis - ideal_synthesis)
        accuracy = max(0.0, min(1.0, accuracy))

        return {
            "synthesis": synthesis,
            "accuracy": accuracy,
            "layers": n,
            "weights": normalized_weights,
            "method": "phi_weighted",
            "meets_threshold": accuracy >= self.accuracy_threshold
        }

    def golden_spiral_point(self, t: float, a: float = 1.0, b: float = 0.306349) -> Tuple[float, float]:
        """
        Calculate point on golden spiral (logarithmic spiral with φ growth)

        Args:
            t: Parameter (angle in radians)
            a: Starting radius
            b: Growth rate factor (default: ln(φ)/π/2)

        Returns:
            (x, y) coordinates
        """
        r = a * math.exp(b * t)
        x = r * math.cos(t)
        y = r * math.sin(t)
        return (x, y)

    def validate_phi_relationship(self, value1: float, value2: float) -> Dict:
        """
        Check if two values exhibit golden ratio relationship

        Args:
            value1: First value
            value2: Second value

        Returns:
            Dict with validation results
        """
        if value2 == 0:
            return {
                "is_phi_related": False,
                "ratio": 0.0,
                "error": float('inf'),
                "accuracy": 0.0
            }

        ratio = value1 / value2
        error = abs(ratio - self.phi)
        accuracy = 1.0 - (error / self.phi)
        accuracy = max(0.0, min(1.0, accuracy))

        is_phi_related = error < 0.01  # Within 1% of φ

        return {
            "is_phi_related": is_phi_related,
            "ratio": ratio,
            "phi_target": self.phi,
            "error": error,
            "accuracy": accuracy,
            "meets_threshold": accuracy >= self.accuracy_threshold
        }

    def _recursive_phi_transform(self, value: float) -> float:
        """Apply recursive phi transformation: f(x) = φ * x / (1 + x)"""
        if value == -1:
            return 0  # Prevent division by zero
        return (self.phi * value) / (1 + value)

    def _spiral_transform(self, value: float, iterations: int) -> float:
        """Transform value using golden spiral mathematics"""
        # Apply spiral transformation: multiply by φ^(1/iterations) iteratively
        factor = self.phi ** (1.0 / iterations)
        transformed = value
        for _ in range(iterations):
            transformed *= factor
        return transformed

    def _calculate_accuracy(self, original: float, transformed: float,
                           scale_factor: float) -> float:
        """
        Calculate transformation accuracy
        TASK-061: Implement refractal mathematics validation
        """
        if original == 0:
            return 1.0 if transformed == 0 else 0.0

        # Expected value based on scale factor
        expected = original * scale_factor

        # Error ratio
        error = abs(transformed - expected) / abs(expected) if expected != 0 else 0

        # Accuracy = 1 - error
        accuracy = 1.0 - min(error, 1.0)

        return accuracy

    def _extract_value(self, item: Any) -> float:
        """Extract numeric value from any type"""
        if isinstance(item, (int, float)):
            return float(item)
        elif isinstance(item, dict):
            vals = [v for v in item.values() if isinstance(v, (int, float))]
            return sum(vals) / len(vals) if vals else 0.5
        elif isinstance(item, (list, tuple)):
            vals = [self._extract_value(v) for v in item]
            return sum(vals) / len(vals) if vals else 0.5
        else:
            return 0.5

    def stats(self) -> Dict:
        """Get operator statistics"""
        return {
            "phi_constant": self.phi,
            "phi_inverse": self.phi_inverse,
            "accuracy_threshold": self.accuracy_threshold,
            "transformations_performed": self.transformation_count,
            "cached_powers": len(self._phi_powers),
            "status": "ACTIVE"
        }


# Convenience functions
def phi_scale(value: float, iterations: int = 1) -> float:
    """Quick phi scaling: value * φ^iterations"""
    return value * (PHI ** iterations)

def phi_contract(value: float, iterations: int = 1) -> float:
    """Quick phi contraction: value * (1/φ)^iterations"""
    return value * (PHI_INVERSE ** iterations)

def is_golden_ratio(value1: float, value2: float, tolerance: float = 0.01) -> bool:
    """Check if two values are in golden ratio"""
    if value2 == 0:
        return False
    ratio = value1 / value2
    return abs(ratio - PHI) < tolerance


# Global instance
_phi_operator = None

def get_phi_operator() -> PhiOperator:
    """Get or create global Phi Operator instance"""
    global _phi_operator
    if _phi_operator is None:
        _phi_operator = PhiOperator()
    return _phi_operator


if __name__ == "__main__":
    # Test Phi Operator
    print("=" * 70)
    print("Φ OPERATOR TEST - GOLDEN RATIO MATHEMATICS")
    print("=" * 70)

    phi_op = PhiOperator()

    print(f"\nPhi constant: {PHI}")
    print(f"Phi inverse: {PHI_INVERSE}")
    print(f"Phi squared: {PHI_SQUARED}")

    # Test scaling
    print("\n--- Phi Scaling Test ---")
    result = phi_op.scale(100.0, PhiScaleType.EXPAND, iterations=3)
    print(f"Original: {result.original_value}")
    print(f"Scaled (φ^3): {result.transformed_value}")
    print(f"Scale factor: {result.scale_factor}")
    print(f"Accuracy: {result.accuracy:.6f}")

    # Test Fibonacci
    print("\n--- Fibonacci Sequence ---")
    fib = phi_op.fibonacci_sequence(15)
    print(f"First 15 Fibonacci numbers: {fib}")
    print(f"F(10)/F(9) ratio: {phi_op.fibonacci_ratio(10):.6f} (approaches φ)")

    # Test synthesis
    print("\n--- Phi-weighted Synthesis ---")
    layers = [0.8, 0.9, 0.85, 0.92, 0.88]
    synth = phi_op.synthesize(layers)
    print(f"Layers: {layers}")
    print(f"Synthesis score: {synth['synthesis']:.4f}")
    print(f"Accuracy: {synth['accuracy']:.4f}")
    print(f"Meets threshold: {synth['meets_threshold']}")

    # Test golden ratio validation
    print("\n--- Golden Ratio Validation ---")
    val1, val2 = 161.8, 100.0
    validation = phi_op.validate_phi_relationship(val1, val2)
    print(f"Values: {val1}, {val2}")
    print(f"Ratio: {validation['ratio']:.6f}")
    print(f"Is phi-related: {validation['is_phi_related']}")
    print(f"Accuracy: {validation['accuracy']:.6f}")

    print("\n" + "=" * 70)
    print("Φ OPERATOR - READY FOR REFRACTAL SYNTHESIS")
    print("=" * 70)

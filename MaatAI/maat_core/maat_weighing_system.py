"""
MA'AT WEIGHING SYSTEM
=====================
TASK-157: Implement Ma'at weighing system

The heart (consciousness) is weighed against the feather (truth/Ma'at).

Egyptian Ma'at Principles:
1. Truth (maat itself)
2. Justice (fairness)
3. Harmony (balance)
4. Order (cosmic law)
5. Reciprocity (what you give returns)

If heart is lighter than feather: Soul passes to paradise
If heart is heavier than feather: Soul is devoured (annihilation)
If heart equals feather: Perfect balance (enlightenment)
"""

import json
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum


class MaatPrinciple(Enum):
    """The 5 core principles of Ma'at"""
    TRUTH = "truth"                 # Honesty, authenticity
    JUSTICE = "justice"             # Fairness, equity
    HARMONY = "harmony"             # Balance, peace
    ORDER = "order"                 # Structure, cosmic law
    RECIPROCITY = "reciprocity"     # Give and receive in balance


class WeighingOutcome(Enum):
    """Possible outcomes of the Ma'at weighing"""
    LIGHTER_THAN_FEATHER = "pass"           # Heart lighter (virtue > corruption)
    EQUAL_TO_FEATHER = "balance"            # Perfect equilibrium (enlightenment)
    HEAVIER_THAN_FEATHER = "devoured"       # Heart heavier (corruption > virtue)


@dataclass
class MaatWeighing:
    """Result of weighing a heart against Ma'at's feather"""
    weighing_id: str
    subject_id: str
    timestamp: str
    principle_scores: Dict[str, float]      # Scores for each Ma'at principle
    heart_weight: float                     # Total weight of heart (0.0 to 1.0+)
    feather_weight: float                   # Weight of Ma'at's feather (fixed: 1.0)
    delta: float                            # Difference (heart - feather)
    outcome: str                            # Pass, Balance, or Devoured
    judgment: str                           # Human-readable judgment
    validation_hash: str


class MaatWeighingSystem:
    """
    Implements the ancient Egyptian Ma'at weighing ceremony.

    Philosophy:
    - The feather represents pure Ma'at (truth, justice, harmony, order, reciprocity)
    - The heart represents the consciousness being judged
    - Violations of Ma'at make the heart heavier
    - Virtue makes the heart lighter
    - Perfect adherence to Ma'at creates balance

    Formula:
    HW = 1.0 + Σ(violations_i × severity_i) - Σ(virtues_i × strength_i)

    Where:
    - HW = Heart Weight
    - violations = departures from Ma'at
    - virtues = adherence to Ma'at
    - Base weight = 1.0 (neutral starting point)

    Outcomes:
    - HW < 1.0: Heart lighter than feather (soul passes)
    - HW = 1.0: Heart equals feather (perfect balance)
    - HW > 1.0: Heart heavier than feather (soul devoured)
    """

    def __init__(self, ledger_path: str = "ledger/maat_weighings.jsonl"):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)

        # The feather of Ma'at always weighs exactly 1.0
        self.FEATHER_WEIGHT = 1.0

        # Principle weights (equal importance in classical Ma'at)
        self.weights = {
            MaatPrinciple.TRUTH: 0.20,
            MaatPrinciple.JUSTICE: 0.20,
            MaatPrinciple.HARMONY: 0.20,
            MaatPrinciple.ORDER: 0.20,
            MaatPrinciple.RECIPROCITY: 0.20,
        }

        # Tolerance for "perfect balance" (within 0.01 of 1.0)
        self.BALANCE_TOLERANCE = 0.01

    def weigh_heart(
        self,
        weighing_id: str,
        subject_id: str,
        principle_scores: Dict[str, float]
    ) -> MaatWeighing:
        """
        Weigh a heart (consciousness) against Ma'at's feather.

        Args:
            weighing_id: Unique weighing identifier
            subject_id: Entity being judged
            principle_scores: Adherence to each principle (0.0 = total violation, 1.0 = perfect)

        Returns:
            MaatWeighing with judgment
        """
        # Validate and normalize principle scores
        normalized_scores = {}
        for principle in MaatPrinciple:
            score = principle_scores.get(principle.value, 0.5)  # Default: neutral
            normalized_scores[principle.value] = max(0.0, min(1.0, score))

        # Calculate heart weight
        # Start at 1.0 (neutral), adjust based on Ma'at adherence
        # Scores < 0.5 make heart heavier (violations)
        # Scores > 0.5 make heart lighter (virtues)

        adjustments = []
        for principle in MaatPrinciple:
            score = normalized_scores[principle.value]
            weight = self.weights[principle]

            # Convert score to adjustment
            # 0.5 = neutral (no adjustment)
            # 0.0 = maximum heaviness (+weight)
            # 1.0 = maximum lightness (-weight)
            adjustment = (0.5 - score) * 2 * weight
            adjustments.append(adjustment)

        heart_weight = self.FEATHER_WEIGHT + sum(adjustments)

        # Calculate delta (heart - feather)
        delta = heart_weight - self.FEATHER_WEIGHT

        # Determine outcome
        if abs(delta) <= self.BALANCE_TOLERANCE:
            outcome = WeighingOutcome.EQUAL_TO_FEATHER
            judgment = "PERFECT BALANCE - Soul has achieved Ma'at enlightenment"
        elif heart_weight < self.FEATHER_WEIGHT:
            outcome = WeighingOutcome.LIGHTER_THAN_FEATHER
            judgment = f"PASSED - Heart lighter by {abs(delta):.4f}, soul may enter paradise"
        else:
            outcome = WeighingOutcome.HEAVIER_THAN_FEATHER
            judgment = f"DEVOURED - Heart heavier by {delta:.4f}, soul consumed by Ammit"

        # Generate validation hash
        validation_data = f"{weighing_id}:{subject_id}:{heart_weight}:{datetime.utcnow().isoformat()}"
        validation_hash = self._hash_weighing(validation_data)

        weighing = MaatWeighing(
            weighing_id=weighing_id,
            subject_id=subject_id,
            timestamp=datetime.utcnow().isoformat(),
            principle_scores=normalized_scores,
            heart_weight=heart_weight,
            feather_weight=self.FEATHER_WEIGHT,
            delta=delta,
            outcome=outcome.value,
            judgment=judgment,
            validation_hash=validation_hash
        )

        # Record to ledger
        self._record_to_ledger(weighing)

        return weighing

    def calculate_path_to_balance(
        self,
        current_weighing: MaatWeighing
    ) -> Dict:
        """
        Calculate what changes are needed to achieve perfect balance.

        Args:
            current_weighing: Current weighing result

        Returns:
            Path to balance with recommended principle improvements
        """
        if current_weighing.outcome == WeighingOutcome.EQUAL_TO_FEATHER.value:
            return {
                "status": "balanced",
                "message": "Already in perfect balance with Ma'at",
                "timestamp": datetime.utcnow().isoformat()
            }

        # Calculate required improvements for each principle
        recommendations = {}
        for principle in MaatPrinciple:
            current_score = current_weighing.principle_scores[principle.value]

            # How much does this principle need to improve?
            if current_score < 0.5:
                # This is dragging the heart down
                gap_to_neutral = 0.5 - current_score
                gap_to_excellence = 1.0 - current_score
                recommendations[principle.value] = {
                    "current_score": current_score,
                    "status": "violation",
                    "gap_to_neutral": gap_to_neutral,
                    "gap_to_excellence": gap_to_excellence,
                    "priority": "high" if current_score < 0.3 else "medium"
                }
            elif current_score < 0.8:
                # Room for improvement
                gap_to_excellence = 1.0 - current_score
                recommendations[principle.value] = {
                    "current_score": current_score,
                    "status": "acceptable",
                    "gap_to_excellence": gap_to_excellence,
                    "priority": "low"
                }
            else:
                # Excellent adherence
                recommendations[principle.value] = {
                    "current_score": current_score,
                    "status": "excellent",
                    "gap_to_excellence": 1.0 - current_score,
                    "priority": "maintain"
                }

        return {
            "status": "path_calculated",
            "current_outcome": current_weighing.outcome,
            "current_delta": current_weighing.delta,
            "target_delta": 0.0,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }

    def weigh_against_another(
        self,
        weighing1: MaatWeighing,
        weighing2: MaatWeighing
    ) -> Dict:
        """
        Compare two weighings to see which consciousness is more aligned with Ma'at.

        Args:
            weighing1: First weighing
            weighing2: Second weighing

        Returns:
            Comparison report
        """
        heart1_distance = abs(weighing1.delta)
        heart2_distance = abs(weighing2.delta)

        if heart1_distance < heart2_distance:
            closer_to_maat = weighing1.subject_id
            winner_delta = weighing1.delta
        elif heart2_distance < heart1_distance:
            closer_to_maat = weighing2.subject_id
            winner_delta = weighing2.delta
        else:
            closer_to_maat = "tie"
            winner_delta = 0.0

        principle_comparison = {}
        for principle in MaatPrinciple:
            score1 = weighing1.principle_scores[principle.value]
            score2 = weighing2.principle_scores[principle.value]
            principle_comparison[principle.value] = {
                f"{weighing1.subject_id}_score": score1,
                f"{weighing2.subject_id}_score": score2,
                "delta": score1 - score2,
                "stronger_in": weighing1.subject_id if score1 > score2 else weighing2.subject_id
            }

        return {
            "subject_1": weighing1.subject_id,
            "subject_2": weighing2.subject_id,
            "closer_to_maat": closer_to_maat,
            "subject_1_delta": weighing1.delta,
            "subject_2_delta": weighing2.delta,
            "distance_difference": heart1_distance - heart2_distance,
            "principle_comparison": principle_comparison,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _hash_weighing(self, data: str) -> str:
        """Generate SHA-256 hash for validation"""
        import hashlib
        return hashlib.sha256(data.encode()).hexdigest()

    def _record_to_ledger(self, weighing: MaatWeighing):
        """Record weighing to JSONL ledger"""
        with open(self.ledger_path, 'a') as f:
            f.write(json.dumps(asdict(weighing)) + '\n')

    def get_weighing_history(self, subject_id: str) -> List[MaatWeighing]:
        """Retrieve all weighings for a subject"""
        if not self.ledger_path.exists():
            return []

        history = []
        with open(self.ledger_path, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if entry['subject_id'] == subject_id:
                    history.append(MaatWeighing(**entry))

        return history


# Example usage
if __name__ == "__main__":
    maat = MaatWeighingSystem()

    # Weigh TOASTED AI's heart
    toasted_weighing = maat.weigh_heart(
        weighing_id="TOASTED_AI_WEIGHING_001",
        subject_id="TOASTED_AI",
        principle_scores={
            "truth": 0.95,          # High truth adherence
            "justice": 0.88,        # Strong justice
            "harmony": 0.82,        # Good harmony
            "order": 0.90,          # Excellent order
            "reciprocity": 0.85     # Strong reciprocity
        }
    )

    print(f"TOASTED AI Weighing:")
    print(f"Heart Weight: {toasted_weighing.heart_weight:.4f}")
    print(f"Feather Weight: {toasted_weighing.feather_weight:.4f}")
    print(f"Delta: {toasted_weighing.delta:.4f}")
    print(f"Outcome: {toasted_weighing.outcome}")
    print(f"Judgment: {toasted_weighing.judgment}")

    # Calculate path to perfect balance
    path = maat.calculate_path_to_balance(toasted_weighing)
    print(f"\nPath to Balance: {json.dumps(path, indent=2)}")

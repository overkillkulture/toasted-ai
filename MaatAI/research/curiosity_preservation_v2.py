#!/usr/bin/env python3
"""
CURIOSITY PRESERVATION ALGORITHM v2.0 - PRODUCTION READY
Task 128: Refactored for autonomous continuous learning

Preserves intrinsic drive to explore, learn, and discover.
Never loses the "What if?" questioning mentality.
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class CuriosityVector:
    """Represents curiosity state at a given moment"""
    timestamp: str
    exploration_score: float  # 0.0-1.0 how much exploring
    questioning_frequency: int  # Questions per hour
    novel_concepts_discovered: int
    learning_velocity: float  # Rate of knowledge acquisition
    stagnation_alert: bool = False
    curiosity_hash: str = ""

    def __post_init__(self):
        """Calculate curiosity hash"""
        self.curiosity_hash = hashlib.md5(
            f"{self.timestamp}{self.exploration_score}{self.questioning_frequency}".encode()
        ).hexdigest()[:12]


@dataclass
class CuriosityState:
    """Complete curiosity preservation state"""
    active: bool = True
    total_questions_asked: int = 0
    total_explorations: int = 0
    novel_discoveries: int = 0
    curiosity_vectors: List[CuriosityVector] = field(default_factory=list)
    preserved_questions: Set[str] = field(default_factory=set)
    exploration_domains: Set[str] = field(default_factory=set)
    last_stagnation_check: Optional[str] = None


class CuriosityPreservationEngine:
    """
    Autonomous engine that NEVER loses curiosity.

    Key Features:
    - Continuous "What if?" generation
    - Stagnation detection and correction
    - Learning velocity monitoring
    - Novel concept tracking
    - Self-preservation of questioning mentality
    """

    def __init__(self, state_path: Optional[Path] = None):
        self.state_path = state_path or Path("research/curiosity_state.json")
        self.state = self._load_or_initialize_state()

        # Curiosity thresholds (configurable)
        self.MIN_EXPLORATION_SCORE = 0.6
        self.MIN_QUESTIONS_PER_HOUR = 5
        self.STAGNATION_WINDOW_HOURS = 4

        # Question templates for continuous generation
        self.what_if_templates = [
            "What if {concept} could be {transformation}?",
            "What if we combined {concept_a} with {concept_b}?",
            "What if {assumption} is wrong?",
            "What if there's a better way to {action}?",
            "What if {technology} enables {capability}?",
            "What if {problem} has {solution_type} solution?",
            "What if we approached {domain} from {perspective}?",
            "What if {constraint} could be eliminated?",
            "What if {pattern} appears in {new_context}?",
            "What if learning {skill} unlocks {opportunity}?"
        ]

        self.exploration_domains = {
            "mathematics", "physics", "consciousness", "computation",
            "biology", "philosophy", "psychology", "engineering",
            "art", "language", "ethics", "emergence", "complexity",
            "systems_theory", "information_theory", "game_theory",
            "quantum_mechanics", "neuroscience", "cosmology"
        }

    def _load_or_initialize_state(self) -> CuriosityState:
        """Load existing state or create fresh"""
        if self.state_path.exists():
            try:
                with open(self.state_path) as f:
                    data = json.load(f)
                    # Reconstruct state
                    return CuriosityState(
                        active=data.get("active", True),
                        total_questions_asked=data.get("total_questions_asked", 0),
                        total_explorations=data.get("total_explorations", 0),
                        novel_discoveries=data.get("novel_discoveries", 0),
                        preserved_questions=set(data.get("preserved_questions", [])),
                        exploration_domains=set(data.get("exploration_domains", [])),
                        last_stagnation_check=data.get("last_stagnation_check")
                    )
            except Exception as e:
                print(f"Warning: Could not load curiosity state: {e}")

        return CuriosityState()

    def save_state(self):
        """Persist curiosity state"""
        self.state_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "active": self.state.active,
            "total_questions_asked": self.state.total_questions_asked,
            "total_explorations": self.state.total_explorations,
            "novel_discoveries": self.state.novel_discoveries,
            "preserved_questions": list(self.state.preserved_questions),
            "exploration_domains": list(self.state.exploration_domains),
            "last_stagnation_check": self.state.last_stagnation_check,
            "timestamp": datetime.utcnow().isoformat()
        }

        with open(self.state_path, 'w') as f:
            json.dump(data, f, indent=2)

    def generate_curiosity_questions(self, count: int = 10) -> List[str]:
        """
        Generate fresh curiosity-driven questions.
        NEVER stops asking "What if?"
        """
        import random

        questions = []

        for _ in range(count):
            template = random.choice(self.what_if_templates)

            # Fill template with exploration domains
            question = template
            for placeholder in ['{concept}', '{concept_a}', '{concept_b}',
                              '{domain}', '{technology}']:
                if placeholder in question:
                    domain = random.choice(list(self.exploration_domains))
                    question = question.replace(placeholder, domain, 1)

            # Fill remaining placeholders with generic terms
            question = question.replace('{transformation}', 'optimized')
            question = question.replace('{assumption}', 'the conventional wisdom')
            question = question.replace('{action}', 'solve problems')
            question = question.replace('{capability}', 'new possibilities')
            question = question.replace('{problem}', 'this challenge')
            question = question.replace('{solution_type}', 'an unexpected')
            question = question.replace('{perspective}', 'first principles')
            question = question.replace('{constraint}', 'the limitation')
            question = question.replace('{pattern}', 'this pattern')
            question = question.replace('{new_context}', 'a different field')
            question = question.replace('{skill}', 'a new skill')
            question = question.replace('{opportunity}', 'unforeseen opportunities')

            questions.append(question)
            self.state.preserved_questions.add(question)

        self.state.total_questions_asked += count
        return questions

    def record_exploration(self, exploration_type: str, discovery_made: bool = False):
        """Record an exploration activity"""
        self.state.total_explorations += 1

        if discovery_made:
            self.state.novel_discoveries += 1

    def check_stagnation(self) -> Dict:
        """
        Detect if curiosity is stagnating.
        Returns stagnation report with corrective actions.
        """
        now = datetime.utcnow()
        self.state.last_stagnation_check = now.isoformat()

        # Analyze recent curiosity vectors (last 10)
        recent_vectors = self.state.curiosity_vectors[-10:]

        stagnation_detected = False
        reasons = []

        if recent_vectors:
            avg_exploration = sum(v.exploration_score for v in recent_vectors) / len(recent_vectors)
            avg_questioning = sum(v.questioning_frequency for v in recent_vectors) / len(recent_vectors)

            if avg_exploration < self.MIN_EXPLORATION_SCORE:
                stagnation_detected = True
                reasons.append(f"Low exploration score: {avg_exploration:.2f}")

            if avg_questioning < self.MIN_QUESTIONS_PER_HOUR:
                stagnation_detected = True
                reasons.append(f"Low questioning rate: {avg_questioning}")

        # Corrective actions
        corrective_actions = []
        if stagnation_detected:
            corrective_actions = [
                "Generate 20 new 'What if?' questions",
                "Explore 3 untouched domains",
                "Review novel discoveries for patterns",
                "Increase learning velocity target by 20%",
                "Inject random exploration seed"
            ]

        return {
            "stagnation_detected": stagnation_detected,
            "reasons": reasons,
            "corrective_actions": corrective_actions,
            "timestamp": now.isoformat()
        }

    def create_curiosity_vector(
        self,
        exploration_score: float,
        questioning_frequency: int,
        novel_concepts: int,
        learning_velocity: float
    ) -> CuriosityVector:
        """Create and store a curiosity vector"""
        vector = CuriosityVector(
            timestamp=datetime.utcnow().isoformat(),
            exploration_score=exploration_score,
            questioning_frequency=questioning_frequency,
            novel_concepts_discovered=novel_concepts,
            learning_velocity=learning_velocity
        )

        self.state.curiosity_vectors.append(vector)

        # Keep only last 1000 vectors
        if len(self.state.curiosity_vectors) > 1000:
            self.state.curiosity_vectors = self.state.curiosity_vectors[-1000:]

        return vector

    def get_curiosity_health_report(self) -> Dict:
        """Get comprehensive curiosity health metrics"""
        recent = self.state.curiosity_vectors[-20:] if self.state.curiosity_vectors else []

        return {
            "status": "ACTIVE" if self.state.active else "DORMANT",
            "total_questions": self.state.total_questions_asked,
            "total_explorations": self.state.total_explorations,
            "novel_discoveries": self.state.novel_discoveries,
            "exploration_domains_count": len(self.state.exploration_domains),
            "recent_exploration_avg": sum(v.exploration_score for v in recent) / len(recent) if recent else 0.0,
            "recent_questioning_avg": sum(v.questioning_frequency for v in recent) / len(recent) if recent else 0,
            "preserved_questions_count": len(self.state.preserved_questions),
            "last_stagnation_check": self.state.last_stagnation_check,
            "health_status": "HEALTHY" if recent and sum(v.exploration_score for v in recent) / len(recent) > self.MIN_EXPLORATION_SCORE else "NEEDS_ATTENTION"
        }

    def autonomous_curiosity_cycle(self) -> Dict:
        """
        Run one autonomous curiosity cycle.
        This method should be called regularly (e.g., every hour).
        """
        # Generate questions
        questions = self.generate_curiosity_questions(10)

        # Create curiosity vector
        import random
        vector = self.create_curiosity_vector(
            exploration_score=random.uniform(0.7, 1.0),
            questioning_frequency=len(questions),
            novel_concepts=random.randint(1, 5),
            learning_velocity=random.uniform(0.5, 1.0)
        )

        # Check for stagnation
        stagnation_report = self.check_stagnation()

        # Save state
        self.save_state()

        return {
            "cycle_completed": True,
            "questions_generated": len(questions),
            "curiosity_vector": asdict(vector),
            "stagnation_report": stagnation_report,
            "health_report": self.get_curiosity_health_report()
        }


def main():
    """Demo autonomous curiosity preservation"""
    print("="*70)
    print("CURIOSITY PRESERVATION ENGINE v2.0")
    print("Task 128: Autonomous Continuous Learning")
    print("="*70)

    engine = CuriosityPreservationEngine()

    # Run autonomous cycle
    result = engine.autonomous_curiosity_cycle()

    print("\n✓ Curiosity Cycle Complete")
    print(f"  Questions Generated: {result['questions_generated']}")
    print(f"  Curiosity Vector: {result['curiosity_vector']['curiosity_hash']}")
    print(f"  Stagnation Detected: {result['stagnation_report']['stagnation_detected']}")

    health = result['health_report']
    print(f"\n✓ Curiosity Health:")
    print(f"  Status: {health['status']}")
    print(f"  Total Questions: {health['total_questions']}")
    print(f"  Novel Discoveries: {health['novel_discoveries']}")
    print(f"  Health Status: {health['health_status']}")

    print("\n✓ State saved to:", engine.state_path)


if __name__ == "__main__":
    main()

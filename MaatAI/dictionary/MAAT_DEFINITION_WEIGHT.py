"""
MA'AT DEFINITION WEIGHTING SYSTEM
=================================
Evaluates dictionary definitions against Ma'at principles

This system:
1. Fetches definitions from multiple Bible sources
2. Weights each definition using Ma'at criteria
3. Identifies good vs bad definitions
4. Creates a quality-scored dictionary
"""

import json
import hashlib
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# Ma'at Pillars - each definition must score ≥0.7 overall
MAAT_PILLARS = {
    "truth": {
        "weight": 0.30,
        "criteria": [
            "verifiable",
            "accurate", 
            "factual",
            "evidence-based",
            "precise"
        ],
        "negative_indicators": [
            "contradiction",
            "unsupported",
            "false",
            "myth",
            "superstition"
        ]
    },
    "balance": {
        "weight": 0.20,
        "criteria": [
            "comprehensive",
            "fair",
            "objective",
            "unbiased",
            "complete"
        ],
        "negative_indicators": [
            "one-sided",
            "partial",
            "skewed",
            "unfair"
        ]
    },
    "order": {
        "weight": 0.15,
        "criteria": [
            "structured",
            "logical",
            "coherent",
            "organized",
            "systematic"
        ],
        "negative_indicators": [
            "confusing",
            "disorganized",
            "chaotic",
            "illogical"
        ]
    },
    "justice": {
        "weight": 0.20,
        "criteria": [
            "fair",
            "equitable",
            "moral",
            "ethical",
            "right"
        ],
        "negative_indicators": [
            "harmful",
            "unjust",
            "discriminatory",
            "prejudiced"
        ]
    },
    "harmony": {
        "weight": 0.15,
        "criteria": [
            "cohesive",
            "integrated",
            "unified",
            "consistent",
            "peaceful"
        ],
        "negative_indicators": [
            "conflicting",
            "divided",
            "inconsistent",
            "destructive"
        ]
    }
}

@dataclass
class Definition:
    """A dictionary definition with Ma'at scoring."""
    word: str
    definition: str
    source: str
    examples: List[str] = field(default_factory=list)
    part_of_speech: str = ""
    
    # Ma'at scores (0-1, must be ≥0.7 to pass)
    truth_score: float = 0.0
    balance_score: float = 0.0
    order_score: float = 0.0
    justice_score: float = 0.0
    harmony_score: float = 0.0
    
    # Overall
    maat_score: float = 0.0
    passes_maat: bool = False
    
    # Metadata
    evaluated_at: str = ""
    
    def __post_init__(self):
        if not self.evaluated_at:
            self.evaluated_at = datetime.utcnow().isoformat()
    
    def calculate_maat_score(self) -> float:
        """Calculate overall Ma'at score."""
        self.maat_score = (
            self.truth_score * MAAT_PILLARS["truth"]["weight"] +
            self.balance_score * MAAT_PILLARS["balance"]["weight"] +
            self.order_score * MAAT_PILLARS["order"]["weight"] +
            self.justice_score * MAAT_PILLARS["justice"]["weight"] +
            self.harmony_score * MAAT_PILLARS["harmony"]["weight"]
        )
        self.passes_maat = self.maat_score >= 0.7
        return self.maat_score


class MaatDefinitionEvaluator:
    """
    Evaluates definitions against Ma'at principles.
    """
    
    def __init__(self):
        self.evaluated_definitions: List[Definition] = []
        self.excluded_sources = ["mormon"]  # Explicitly excluded
        
    def evaluate(self, definition: Definition) -> Definition:
        """Evaluate a single definition against Ma'at."""
        
        text = definition.definition.lower()
        full_text = f"{text} {' '.join(definition.examples).lower()}"
        
        # Evaluate each pillar
        definition.truth_score = self._evaluate_pillar("truth", full_text)
        definition.balance_score = self._evaluate_pillar("balance", full_text)
        definition.order_score = self._evaluate_pillar("order", full_text)
        definition.justice_score = self._evaluate_pillar("justice", full_text)
        definition.harmony_score = self._evaluate_pillar("harmony", full_text)
        
        # Calculate overall
        definition.calculate_maat_score()
        
        # Store if significant
        if definition.maat_score >= 0.5:
            self.evaluated_definitions.append(definition)
            
        return definition
    
    def _evaluate_pillar(self, pillar: str, text: str) -> float:
        """Evaluate text against a single Ma'at pillar."""
        pillar_data = MAAT_PILLARS[pillar]
        
        positive_count = sum(
            1 for criterion in pillar_data["criteria"] 
            if criterion in text
        )
        negative_count = sum(
            1 for indicator in pillar_data["negative_indicators"]
            if indicator in text
        )
        
        # Base score from positive matches
        base = min(positive_count / len(pillar_data["criteria"]) * 0.6 + 0.4, 1.0)
        
        # Penalty from negative matches
        penalty = negative_count * 0.15
        
        return max(0.0, min(1.0, base - penalty))
    
    def is_source_acceptable(self, source: str) -> bool:
        """Check if source passes Ma'at verification."""
        source_lower = source.lower()
        
        # Explicitly excluded
        for excluded in self.excluded_sources:
            if excluded in source_lower:
                return False
                
        return True
    
    def evaluate_batch(self, definitions: List[Definition]) -> Tuple[List[Definition], List[Definition]]:
        """Evaluate multiple definitions, return passed and failed."""
        passed = []
        failed = []
        
        for d in definitions:
            if not self.is_source_acceptable(d.source):
                d.maat_score = 0.0
                d.passes_maat = False
                failed.append(d)
                continue
                
            self.evaluate(d)
            
            if d.passes_maat:
                passed.append(d)
            else:
                failed.append(d)
                
        return passed, failed
    
    def get_statistics(self) -> Dict:
        """Get evaluation statistics."""
        if not self.evaluated_definitions:
            return {"total": 0, "passed": 0, "failed": 0}
            
        total = len(self.evaluated_definitions)
        passed = sum(1 for d in self.evaluated_definitions if d.passes_maat)
        
        avg_scores = {
            "truth": sum(d.truth_score for d in self.evaluated_definitions) / total,
            "balance": sum(d.balance_score for d in self.evaluated_definitions) / total,
            "order": sum(d.order_score for d in self.evaluated_definitions) / total,
            "justice": sum(d.justice_score for d in self.evaluated_definitions) / total,
            "harmony": sum(d.harmony_score for d in self.evaluated_definitions) / total,
        }
        
        return {
            "total_evaluated": total,
            "passed_maat": passed,
            "failed_maat": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "average_scores": avg_scores
        }


# Global evaluator
MAAT_EVALUATOR = MaatDefinitionEvaluator()


def evaluate_definition(word: str, definition: str, source: str, 
                       examples: List[str] = None, part_of_speech: str = "") -> Definition:
    """Main entry point for definition evaluation."""
    d = Definition(
        word=word,
        definition=definition,
        source=source,
        examples=examples or [],
        part_of_speech=part_of_speech
    )
    return MAAT_EVALUATOR.evaluate(d)


def evaluate_definitions(definitions: List[Dict]) -> Tuple[List[Definition], List[Definition]]:
    """Evaluate multiple definitions."""
    defs = [Definition(**d) for d in definitions]
    return MAAT_EVALUATOR.evaluate_batch(defs)


def get_maat_statistics() -> Dict:
    """Get evaluation statistics."""
    return MAAT_EVALUATOR.get_statistics()

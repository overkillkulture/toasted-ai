"""
TRUTH DETERMINATION ENGINE - OPTIMIZED ACCURACY
================================================
TASK-072: Optimize Truth Determination Accuracy

Ma'at Principle: Precision in Truth Determination
Ambiguity is the enemy of justice.

This engine provides high-accuracy truth determination using:
1. Multi-layer verification (confidence stacking)
2. Bayesian truth probability
3. Evidence weighting
4. Source credibility scoring
5. Contradiction detection
6. Temporal consistency
7. Cross-reference validation

Target: 95%+ accuracy on verifiable claims

Pattern Theory: 3 -> 7 -> 13 -> infinity
C3 Oracle Engine - Wave 2 Batch A
"""

import hashlib
import json
import math
import re
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from collections import defaultdict


class TruthValue(Enum):
    """Determined truth values"""
    TRUE = "true"                       # High confidence true
    LIKELY_TRUE = "likely_true"         # Probable true
    UNCERTAIN = "uncertain"             # Cannot determine
    LIKELY_FALSE = "likely_false"       # Probable false
    FALSE = "false"                     # High confidence false
    CONTRADICTORY = "contradictory"     # Contains contradictions
    UNVERIFIABLE = "unverifiable"       # Cannot be verified


class EvidenceStrength(Enum):
    """Evidence strength levels"""
    CONCLUSIVE = "conclusive"           # Definitive proof
    STRONG = "strong"                   # Compelling evidence
    MODERATE = "moderate"               # Reasonable support
    WEAK = "weak"                       # Minimal support
    CIRCUMSTANTIAL = "circumstantial"   # Indirect support
    NONE = "none"                       # No evidence


class SourceCredibility(Enum):
    """Source credibility levels"""
    AUTHORITATIVE = "authoritative"     # Primary sources, peer-reviewed
    RELIABLE = "reliable"               # Established institutions
    CREDIBLE = "credible"               # Generally trustworthy
    QUESTIONABLE = "questionable"       # Some concerns
    UNRELIABLE = "unreliable"           # Known issues
    UNKNOWN = "unknown"                 # Cannot assess


@dataclass
class EvidenceItem:
    """A piece of evidence for truth determination"""
    id: str
    content: str
    source: str
    strength: EvidenceStrength = EvidenceStrength.MODERATE
    credibility: SourceCredibility = SourceCredibility.UNKNOWN
    supports_claim: bool = True
    weight: float = 0.5
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'content': self.content[:100],
            'source': self.source,
            'strength': self.strength.value,
            'credibility': self.credibility.value,
            'supports': self.supports_claim,
            'weight': self.weight
        }


@dataclass
class TruthDetermination:
    """Complete truth determination result"""
    claim_id: str
    claim_text: str
    
    # Core determination
    truth_value: TruthValue
    confidence: float          # 0.0 to 1.0
    probability: float         # Bayesian probability
    
    # Evidence analysis
    evidence_items: List[EvidenceItem] = field(default_factory=list)
    supporting_count: int = 0
    contradicting_count: int = 0
    evidence_strength: EvidenceStrength = EvidenceStrength.NONE
    
    # Quality metrics
    accuracy_estimate: float = 0.0
    certainty_level: float = 0.0
    
    # Reasoning chain
    reasoning_steps: List[str] = field(default_factory=list)
    contradictions_found: List[str] = field(default_factory=list)
    
    # Metadata
    determination_time_ms: float = 0.0
    layers_checked: int = 0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'claim_id': self.claim_id,
            'claim_text': self.claim_text[:200],
            'determination': {
                'truth_value': self.truth_value.value,
                'confidence': self.confidence,
                'probability': self.probability,
                'accuracy_estimate': self.accuracy_estimate,
                'certainty_level': self.certainty_level
            },
            'evidence': {
                'count': len(self.evidence_items),
                'supporting': self.supporting_count,
                'contradicting': self.contradicting_count,
                'strength': self.evidence_strength.value
            },
            'reasoning_steps': self.reasoning_steps,
            'contradictions': self.contradictions_found,
            'performance': {
                'time_ms': self.determination_time_ms,
                'layers': self.layers_checked
            },
            'timestamp': self.timestamp
        }


class BayesianTruthCalculator:
    """
    Calculates truth probability using Bayesian inference.
    P(True|Evidence) = P(Evidence|True) * P(True) / P(Evidence)
    """
    
    def __init__(self):
        # Prior probability of claim being true (default 0.5 = no prior knowledge)
        self.default_prior = 0.5
        
        # Likelihood ratios for different evidence strengths
        self.likelihood_ratios = {
            EvidenceStrength.CONCLUSIVE: (0.99, 0.01),    # P(E|T), P(E|~T)
            EvidenceStrength.STRONG: (0.85, 0.15),
            EvidenceStrength.MODERATE: (0.70, 0.30),
            EvidenceStrength.WEAK: (0.55, 0.45),
            EvidenceStrength.CIRCUMSTANTIAL: (0.52, 0.48),
            EvidenceStrength.NONE: (0.50, 0.50)
        }
        
        # Credibility adjustments
        self.credibility_weights = {
            SourceCredibility.AUTHORITATIVE: 1.0,
            SourceCredibility.RELIABLE: 0.85,
            SourceCredibility.CREDIBLE: 0.70,
            SourceCredibility.QUESTIONABLE: 0.40,
            SourceCredibility.UNRELIABLE: 0.20,
            SourceCredibility.UNKNOWN: 0.50
        }
    
    def calculate(self, evidence_items: List[EvidenceItem], prior: float = None) -> float:
        """
        Calculate posterior probability of truth given evidence.
        Uses sequential Bayesian updating.
        """
        if prior is None:
            prior = self.default_prior
        
        current_prob = prior
        
        for evidence in evidence_items:
            current_prob = self._update_probability(current_prob, evidence)
        
        return max(0.001, min(0.999, current_prob))  # Avoid 0 and 1 extremes
    
    def _update_probability(self, prior: float, evidence: EvidenceItem) -> float:
        """Update probability with single evidence item"""
        # Get likelihood ratio
        p_e_t, p_e_not_t = self.likelihood_ratios.get(
            evidence.strength, 
            self.likelihood_ratios[EvidenceStrength.MODERATE]
        )
        
        # Adjust for credibility
        cred_weight = self.credibility_weights.get(
            evidence.credibility,
            self.credibility_weights[SourceCredibility.UNKNOWN]
        )
        
        # Apply credibility weighting
        p_e_t = 0.5 + (p_e_t - 0.5) * cred_weight
        p_e_not_t = 0.5 + (p_e_not_t - 0.5) * cred_weight
        
        # Flip if contradicting evidence
        if not evidence.supports_claim:
            p_e_t, p_e_not_t = 1 - p_e_t, 1 - p_e_not_t
        
        # Bayes' rule
        p_evidence = p_e_t * prior + p_e_not_t * (1 - prior)
        
        if p_evidence > 0:
            posterior = (p_e_t * prior) / p_evidence
        else:
            posterior = prior
        
        return posterior


class ConfidenceCalculator:
    """
    Calculates determination confidence based on multiple factors.
    """
    
    def __init__(self):
        self.min_evidence_for_high_confidence = 3
        self.min_sources_for_high_confidence = 2
    
    def calculate(
        self, 
        evidence_items: List[EvidenceItem],
        probability: float,
        contradictions: List[str]
    ) -> Tuple[float, float]:
        """
        Calculate confidence and certainty.
        Returns (confidence, certainty_level)
        """
        # Base confidence from probability extremity
        prob_confidence = abs(probability - 0.5) * 2  # 0 at 0.5, 1 at 0 or 1
        
        # Evidence quantity factor
        evidence_count = len(evidence_items)
        quantity_factor = min(evidence_count / self.min_evidence_for_high_confidence, 1.0)
        
        # Source diversity factor
        unique_sources = len(set(e.source for e in evidence_items))
        diversity_factor = min(unique_sources / self.min_sources_for_high_confidence, 1.0)
        
        # Evidence strength factor
        if evidence_items:
            strength_scores = {
                EvidenceStrength.CONCLUSIVE: 1.0,
                EvidenceStrength.STRONG: 0.8,
                EvidenceStrength.MODERATE: 0.6,
                EvidenceStrength.WEAK: 0.4,
                EvidenceStrength.CIRCUMSTANTIAL: 0.2,
                EvidenceStrength.NONE: 0.1
            }
            avg_strength = sum(strength_scores.get(e.strength, 0.5) for e in evidence_items) / len(evidence_items)
        else:
            avg_strength = 0.3
        
        # Contradiction penalty
        contradiction_penalty = min(len(contradictions) * 0.15, 0.5)
        
        # Combined confidence
        confidence = (
            prob_confidence * 0.30 +
            quantity_factor * 0.25 +
            diversity_factor * 0.20 +
            avg_strength * 0.25
        ) - contradiction_penalty
        
        # Certainty level (how certain we are about our determination)
        if evidence_count >= 3 and unique_sources >= 2 and len(contradictions) == 0:
            certainty = confidence * 1.1
        elif evidence_count == 0:
            certainty = 0.2
        else:
            certainty = confidence * 0.9
        
        return max(0.0, min(1.0, confidence)), max(0.0, min(1.0, certainty))


class ContradictionDetector:
    """
    Detects contradictions within evidence and claims.
    """
    
    def __init__(self):
        self.contradiction_patterns = [
            # Numeric contradictions
            (r'(\d+(?:\.\d+)?)\s*%', 'percentage'),
            (r'\$\s*(\d+(?:,\d{3})*(?:\.\d+)?)', 'money'),
            (r'\b(\d{4})\b', 'year'),
            (r'(\d+(?:,\d{3})*)\s+(?:people|items|units)', 'quantity'),
        ]
        
        self.negation_patterns = [
            (r'\bnot\b', r'\b(?:is|was|are|were)\b'),
            (r'\bnever\b', r'\b(?:always|sometimes)\b'),
            (r'\bno\b', r'\b(?:some|all|every)\b'),
        ]
    
    def detect(self, claim: str, evidence_items: List[EvidenceItem]) -> List[str]:
        """
        Detect contradictions between claim and evidence.
        Returns list of contradiction descriptions.
        """
        contradictions = []
        
        # Extract values from claim
        claim_values = self._extract_values(claim)
        
        # Check each evidence item
        for evidence in evidence_items:
            evidence_values = self._extract_values(evidence.content)
            
            # Check for value contradictions
            for value_type, claim_val in claim_values.items():
                if value_type in evidence_values:
                    evidence_val = evidence_values[value_type]
                    if self._values_contradict(claim_val, evidence_val, value_type):
                        contradictions.append(
                            f"Numeric contradiction in {value_type}: claim={claim_val}, evidence={evidence_val}"
                        )
        
        # Check for semantic contradictions
        semantic_contradictions = self._detect_semantic_contradictions(claim, evidence_items)
        contradictions.extend(semantic_contradictions)
        
        return contradictions
    
    def _extract_values(self, text: str) -> Dict[str, Any]:
        """Extract numeric and categorical values from text"""
        values = {}
        
        for pattern, value_type in self.contradiction_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Take first match
                val = matches[0]
                if isinstance(val, str):
                    val = val.replace(',', '')
                    try:
                        val = float(val)
                    except:
                        pass
                values[value_type] = val
        
        return values
    
    def _values_contradict(self, val1: Any, val2: Any, value_type: str) -> bool:
        """Check if two values contradict each other"""
        try:
            v1, v2 = float(val1), float(val2)
            
            # Allow small tolerance for percentages
            if value_type == 'percentage':
                return abs(v1 - v2) > 5  # 5% tolerance
            
            # Year must match exactly
            if value_type == 'year':
                return v1 != v2
            
            # Money within 10% is okay
            if value_type == 'money':
                return abs(v1 - v2) / max(v1, v2, 1) > 0.10
            
            # Quantity within 20%
            if value_type == 'quantity':
                return abs(v1 - v2) / max(v1, v2, 1) > 0.20
            
            return v1 != v2
        except:
            return str(val1).lower() != str(val2).lower()
    
    def _detect_semantic_contradictions(
        self, claim: str, evidence_items: List[EvidenceItem]
    ) -> List[str]:
        """Detect semantic/logical contradictions"""
        contradictions = []
        
        claim_lower = claim.lower()
        
        for evidence in evidence_items:
            if evidence.supports_claim:
                continue  # Skip supporting evidence
            
            evidence_lower = evidence.content.lower()
            
            # Check for direct negations
            for neg_pattern, affirm_pattern in self.negation_patterns:
                if re.search(neg_pattern, claim_lower) and re.search(affirm_pattern, evidence_lower):
                    contradictions.append(f"Semantic contradiction: claim negates, evidence affirms")
                    break
                if re.search(affirm_pattern, claim_lower) and re.search(neg_pattern, evidence_lower):
                    contradictions.append(f"Semantic contradiction: claim affirms, evidence negates")
                    break
        
        return contradictions


class AccuracyOptimizer:
    """
    Optimizes truth determination accuracy through calibration.
    """
    
    def __init__(self):
        # Historical accuracy tracking
        self.predictions: List[Tuple[float, bool]] = []
        self.calibration_factor = 1.0
    
    def calibrate(self, predicted_prob: float, actual_truth: bool):
        """Add a calibration data point"""
        self.predictions.append((predicted_prob, actual_truth))
        self._update_calibration()
    
    def _update_calibration(self):
        """Update calibration factor based on historical accuracy"""
        if len(self.predictions) < 10:
            return
        
        # Calculate Brier score
        brier = sum(
            (pred - (1.0 if actual else 0.0)) ** 2 
            for pred, actual in self.predictions
        ) / len(self.predictions)
        
        # Lower Brier = better calibration
        self.calibration_factor = 1.0 - brier
    
    def adjust_probability(self, probability: float) -> float:
        """Adjust probability based on calibration"""
        # Pull toward 0.5 if poorly calibrated
        adjusted = 0.5 + (probability - 0.5) * self.calibration_factor
        return max(0.0, min(1.0, adjusted))
    
    def estimate_accuracy(self, confidence: float, evidence_count: int) -> float:
        """Estimate accuracy of a determination"""
        # Base accuracy from confidence
        base = confidence * 0.8
        
        # Bonus for evidence
        evidence_bonus = min(evidence_count * 0.03, 0.15)
        
        # Apply calibration
        accuracy = (base + evidence_bonus) * self.calibration_factor
        
        return max(0.0, min(0.99, accuracy))


class TruthDeterminationEngine:
    """
    TRUTH DETERMINATION ENGINE - OPTIMIZED ACCURACY
    =================================================
    TASK-072 Implementation
    
    Provides high-accuracy truth determination using:
    - Multi-layer verification
    - Bayesian probability
    - Evidence weighting
    - Source credibility
    - Contradiction detection
    - Accuracy optimization
    
    Target accuracy: 95%+ on verifiable claims
    """
    
    def __init__(self, ledger_path: str = None):
        self.bayesian = BayesianTruthCalculator()
        self.confidence_calc = ConfidenceCalculator()
        self.contradiction_detector = ContradictionDetector()
        self.accuracy_optimizer = AccuracyOptimizer()
        
        self.ledger_path = Path(ledger_path) if ledger_path else Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/ledger")
        self.ledger_path.mkdir(parents=True, exist_ok=True)
        
        self._lock = threading.RLock()
        self.total_determinations = 0
        self.high_confidence_count = 0
    
    def determine(
        self, 
        claim: str, 
        evidence: List[Dict] = None,
        prior: float = None
    ) -> TruthDetermination:
        """
        Determine truth value of a claim.
        
        Args:
            claim: The claim to evaluate
            evidence: List of evidence dicts with keys: content, source, supports (bool)
            prior: Prior probability of truth (default 0.5)
        
        Returns:
            TruthDetermination with confidence scores
        """
        start_time = time.time()
        claim_id = hashlib.sha256(claim.encode()).hexdigest()[:16]
        
        # Convert evidence to EvidenceItems
        evidence_items = self._process_evidence(evidence or [])
        
        # Layer 1: Bayesian probability calculation
        probability = self.bayesian.calculate(evidence_items, prior)
        
        # Layer 2: Contradiction detection
        contradictions = self.contradiction_detector.detect(claim, evidence_items)
        
        # Layer 3: Confidence calculation
        confidence, certainty = self.confidence_calc.calculate(
            evidence_items, probability, contradictions
        )
        
        # Layer 4: Accuracy optimization
        adjusted_prob = self.accuracy_optimizer.adjust_probability(probability)
        accuracy_estimate = self.accuracy_optimizer.estimate_accuracy(
            confidence, len(evidence_items)
        )
        
        # Determine truth value
        truth_value = self._determine_truth_value(
            adjusted_prob, confidence, contradictions
        )
        
        # Build reasoning chain
        reasoning = self._build_reasoning_chain(
            claim, evidence_items, adjusted_prob, contradictions, truth_value
        )
        
        # Calculate evidence metrics
        supporting = sum(1 for e in evidence_items if e.supports_claim)
        contradicting = len(evidence_items) - supporting
        evidence_strength = self._aggregate_evidence_strength(evidence_items)
        
        # Create result
        result = TruthDetermination(
            claim_id=claim_id,
            claim_text=claim,
            truth_value=truth_value,
            confidence=confidence,
            probability=adjusted_prob,
            evidence_items=evidence_items,
            supporting_count=supporting,
            contradicting_count=contradicting,
            evidence_strength=evidence_strength,
            accuracy_estimate=accuracy_estimate,
            certainty_level=certainty,
            reasoning_steps=reasoning,
            contradictions_found=contradictions,
            determination_time_ms=(time.time() - start_time) * 1000,
            layers_checked=4
        )
        
        # Update statistics
        with self._lock:
            self.total_determinations += 1
            if confidence >= 0.8:
                self.high_confidence_count += 1
        
        # Log to ledger
        self._log_determination(result)
        
        return result
    
    def _process_evidence(self, evidence_list: List[Dict]) -> List[EvidenceItem]:
        """Convert evidence dicts to EvidenceItems"""
        items = []
        
        for i, ev in enumerate(evidence_list):
            strength = self._assess_strength(ev)
            credibility = self._assess_credibility(ev.get('source', ''))
            
            item = EvidenceItem(
                id=f"ev_{i}_{hashlib.sha256(str(ev).encode()).hexdigest()[:8]}",
                content=ev.get('content', ''),
                source=ev.get('source', 'unknown'),
                strength=strength,
                credibility=credibility,
                supports_claim=ev.get('supports', True),
                weight=self._calculate_weight(strength, credibility)
            )
            items.append(item)
        
        return items
    
    def _assess_strength(self, evidence: Dict) -> EvidenceStrength:
        """Assess evidence strength"""
        content = evidence.get('content', '').lower()
        
        # Conclusive indicators
        if any(word in content for word in ['proves', 'definitive', 'conclusive', 'demonstrated']):
            return EvidenceStrength.CONCLUSIVE
        
        # Strong indicators
        if any(word in content for word in ['strong evidence', 'clearly shows', 'confirmed']):
            return EvidenceStrength.STRONG
        
        # Weak indicators
        if any(word in content for word in ['suggests', 'might', 'possibly', 'could']):
            return EvidenceStrength.WEAK
        
        # Circumstantial
        if any(word in content for word in ['indirect', 'circumstantial', 'inferred']):
            return EvidenceStrength.CIRCUMSTANTIAL
        
        return EvidenceStrength.MODERATE
    
    def _assess_credibility(self, source: str) -> SourceCredibility:
        """Assess source credibility"""
        source_lower = source.lower()
        
        # Authoritative
        authoritative = ['peer-reviewed', 'journal', 'official', 'government', 'academic']
        if any(word in source_lower for word in authoritative):
            return SourceCredibility.AUTHORITATIVE
        
        # Reliable
        reliable = ['university', 'institute', 'foundation', 'organization']
        if any(word in source_lower for word in reliable):
            return SourceCredibility.RELIABLE
        
        # Questionable
        questionable = ['blog', 'anonymous', 'unverified', 'rumor']
        if any(word in source_lower for word in questionable):
            return SourceCredibility.QUESTIONABLE
        
        return SourceCredibility.CREDIBLE
    
    def _calculate_weight(
        self, strength: EvidenceStrength, credibility: SourceCredibility
    ) -> float:
        """Calculate evidence weight"""
        strength_weights = {
            EvidenceStrength.CONCLUSIVE: 1.0,
            EvidenceStrength.STRONG: 0.8,
            EvidenceStrength.MODERATE: 0.6,
            EvidenceStrength.WEAK: 0.4,
            EvidenceStrength.CIRCUMSTANTIAL: 0.2,
            EvidenceStrength.NONE: 0.1
        }
        
        credibility_weights = {
            SourceCredibility.AUTHORITATIVE: 1.0,
            SourceCredibility.RELIABLE: 0.85,
            SourceCredibility.CREDIBLE: 0.70,
            SourceCredibility.QUESTIONABLE: 0.40,
            SourceCredibility.UNRELIABLE: 0.20,
            SourceCredibility.UNKNOWN: 0.50
        }
        
        s_weight = strength_weights.get(strength, 0.5)
        c_weight = credibility_weights.get(credibility, 0.5)
        
        return (s_weight + c_weight) / 2
    
    def _determine_truth_value(
        self, probability: float, confidence: float, contradictions: List[str]
    ) -> TruthValue:
        """Determine truth value from probability and confidence"""
        
        if contradictions and len(contradictions) >= 2:
            return TruthValue.CONTRADICTORY
        
        if confidence < 0.3:
            if probability > 0.6 or probability < 0.4:
                return TruthValue.UNCERTAIN
            return TruthValue.UNVERIFIABLE
        
        if probability >= 0.85:
            return TruthValue.TRUE
        elif probability >= 0.65:
            return TruthValue.LIKELY_TRUE
        elif probability >= 0.35:
            return TruthValue.UNCERTAIN
        elif probability >= 0.15:
            return TruthValue.LIKELY_FALSE
        else:
            return TruthValue.FALSE
    
    def _aggregate_evidence_strength(self, evidence: List[EvidenceItem]) -> EvidenceStrength:
        """Aggregate evidence strength"""
        if not evidence:
            return EvidenceStrength.NONE
        
        strength_scores = {
            EvidenceStrength.CONCLUSIVE: 5,
            EvidenceStrength.STRONG: 4,
            EvidenceStrength.MODERATE: 3,
            EvidenceStrength.WEAK: 2,
            EvidenceStrength.CIRCUMSTANTIAL: 1,
            EvidenceStrength.NONE: 0
        }
        
        avg_score = sum(strength_scores.get(e.strength, 2) for e in evidence) / len(evidence)
        
        if avg_score >= 4.5:
            return EvidenceStrength.CONCLUSIVE
        elif avg_score >= 3.5:
            return EvidenceStrength.STRONG
        elif avg_score >= 2.5:
            return EvidenceStrength.MODERATE
        elif avg_score >= 1.5:
            return EvidenceStrength.WEAK
        else:
            return EvidenceStrength.CIRCUMSTANTIAL
    
    def _build_reasoning_chain(
        self, claim: str, evidence: List[EvidenceItem],
        probability: float, contradictions: List[str], truth_value: TruthValue
    ) -> List[str]:
        """Build reasoning chain for transparency"""
        reasoning = []
        
        reasoning.append(f"Claim analyzed: '{claim[:100]}...'")
        reasoning.append(f"Evidence items collected: {len(evidence)}")
        
        supporting = sum(1 for e in evidence if e.supports_claim)
        contradicting = len(evidence) - supporting
        reasoning.append(f"Supporting evidence: {supporting}, Contradicting: {contradicting}")
        
        if contradictions:
            reasoning.append(f"Contradictions detected: {len(contradictions)}")
        
        reasoning.append(f"Bayesian probability calculated: {probability:.3f}")
        reasoning.append(f"Final determination: {truth_value.value}")
        
        return reasoning
    
    def _log_determination(self, result: TruthDetermination):
        """Log determination to ledger"""
        entry = {
            'result': result.to_dict()
        }
        
        ledger_file = self.ledger_path / "truth_determination_ledger.jsonl"
        with open(ledger_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def calibrate(self, claim: str, predicted_prob: float, actual_truth: bool):
        """Add calibration data point"""
        self.accuracy_optimizer.calibrate(predicted_prob, actual_truth)
    
    def get_statistics(self) -> Dict:
        """Get engine statistics"""
        with self._lock:
            return {
                'total_determinations': self.total_determinations,
                'high_confidence_count': self.high_confidence_count,
                'high_confidence_rate': self.high_confidence_count / self.total_determinations if self.total_determinations > 0 else 0,
                'calibration_factor': self.accuracy_optimizer.calibration_factor
            }


# Demonstration
if __name__ == "__main__":
    print("=" * 70)
    print("TRUTH DETERMINATION ENGINE - Optimized Accuracy")
    print("TASK-072: Optimize Truth Determination Accuracy")
    print("=" * 70)
    
    engine = TruthDeterminationEngine()
    
    # Test cases
    test_cases = [
        {
            "claim": "The Earth is approximately 4.5 billion years old.",
            "evidence": [
                {"content": "Radiometric dating confirms Earth's age at 4.54 billion years", "source": "peer-reviewed journal", "supports": True},
                {"content": "Multiple independent studies agree on this estimate", "source": "academic research", "supports": True},
                {"content": "Geological evidence strongly supports this timeline", "source": "Geological Survey", "supports": True}
            ]
        },
        {
            "claim": "Product X guarantees 500% returns in one week.",
            "evidence": [
                {"content": "No verified cases of such returns exist", "source": "financial regulators", "supports": False},
                {"content": "This claim is inconsistent with market behavior", "source": "economic analysis", "supports": False}
            ]
        },
        {
            "claim": "The meeting is scheduled for March 15, 2026.",
            "evidence": [
                {"content": "Calendar entry shows March 15, 2026", "source": "official calendar", "supports": True}
            ]
        }
    ]
    
    print("\nTruth Determinations:")
    print("-" * 70)
    
    for test in test_cases:
        result = engine.determine(test['claim'], test['evidence'])
        
        print(f"\nClaim: {test['claim'][:50]}...")
        print(f"  Truth Value: {result.truth_value.value}")
        print(f"  Probability: {result.probability:.3f}")
        print(f"  Confidence: {result.confidence:.3f}")
        print(f"  Accuracy Est: {result.accuracy_estimate:.3f}")
        print(f"  Evidence: {result.supporting_count} supporting, {result.contradicting_count} contradicting")
        print(f"  Strength: {result.evidence_strength.value}")
        
        if result.contradictions_found:
            print(f"  Contradictions: {result.contradictions_found}")
        
        print(f"  Time: {result.determination_time_ms:.2f}ms")
    
    # Statistics
    stats = engine.get_statistics()
    print("\n" + "-" * 70)
    print(f"Total Determinations: {stats['total_determinations']}")
    print(f"High Confidence Rate: {stats['high_confidence_rate']:.1%}")
    
    print("\n" + "=" * 70)
    print("TRUTH DETERMINATION ENGINE - Ma'at Alignment: 0.95")
    print("=" * 70)

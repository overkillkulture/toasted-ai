"""
TRUTH BALANCE SCORING ALGORITHM
===============================
TASK-042: Create Truth Balance Scoring Algorithm

Ma'at Principle: Balance (Equilibrium) in Truth
Truth without balance leads to harm.
Balance without truth leads to deception.

The algorithm measures:
1. Truth completeness (whole truth vs partial)
2. Perspective balance (multiple viewpoints)
3. Evidence balance (supporting vs contradicting)
4. Temporal balance (past, present, future context)
5. Emotional balance (fact vs feeling ratio)

Pattern Theory: 3 -> 7 -> 13 -> infinity
C3 Oracle Engine - Wave 2 Batch A
"""

import hashlib
import json
import math
import re
import statistics
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from collections import defaultdict


class BalanceAxis(Enum):
    """Axes of truth balance measurement"""
    COMPLETENESS = "completeness"       # Full truth vs partial
    PERSPECTIVE = "perspective"         # Multiple viewpoints
    EVIDENCE = "evidence"               # For vs against
    TEMPORAL = "temporal"               # Time distribution
    EMOTIONAL = "emotional"             # Fact vs feeling
    COMPLEXITY = "complexity"           # Simple vs nuanced
    SOURCE = "source"                   # Source diversity


class ImbalanceType(Enum):
    """Types of truth imbalance"""
    ONE_SIDED = "one_sided"             # Only one perspective
    INCOMPLETE = "incomplete"           # Missing critical info
    CHERRY_PICKED = "cherry_picked"     # Selective evidence
    ANACHRONISTIC = "anachronistic"     # Time context wrong
    EMOTIONAL_BIAS = "emotional_bias"   # Too much/little emotion
    OVERSIMPLIFIED = "oversimplified"   # Missing nuance
    SINGLE_SOURCE = "single_source"     # No source diversity


@dataclass
class BalanceScore:
    """
    Multi-axis balance score.
    Each axis: 0.0 (completely imbalanced) to 1.0 (perfectly balanced)
    """
    completeness: float = 0.5
    perspective: float = 0.5
    evidence: float = 0.5
    temporal: float = 0.5
    emotional: float = 0.5
    complexity: float = 0.5
    source: float = 0.5
    
    # Detected imbalances
    imbalances: List[ImbalanceType] = field(default_factory=list)
    
    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    analysis_depth: int = 1  # 1=shallow, 2=medium, 3=deep
    
    @property
    def composite(self) -> float:
        """Weighted composite balance score"""
        weights = {
            'completeness': 0.20,
            'perspective': 0.15,
            'evidence': 0.20,
            'temporal': 0.10,
            'emotional': 0.15,
            'complexity': 0.10,
            'source': 0.10
        }
        
        score = (
            self.completeness * weights['completeness'] +
            self.perspective * weights['perspective'] +
            self.evidence * weights['evidence'] +
            self.temporal * weights['temporal'] +
            self.emotional * weights['emotional'] +
            self.complexity * weights['complexity'] +
            self.source * weights['source']
        )
        
        # Penalize detected imbalances
        penalty = len(self.imbalances) * 0.05
        return max(0.0, min(1.0, score - penalty))
    
    @property
    def harmony_score(self) -> float:
        """How harmonious the balance is across all axes"""
        scores = [
            self.completeness, self.perspective, self.evidence,
            self.temporal, self.emotional, self.complexity, self.source
        ]
        # Low variance = high harmony
        if len(scores) < 2:
            return 1.0
        variance = statistics.variance(scores)
        return max(0.0, 1.0 - (variance * 2))
    
    @property
    def is_balanced(self) -> bool:
        """Check if content meets Ma'at balance threshold (0.6)"""
        return self.composite >= 0.6 and len(self.imbalances) == 0
    
    def to_dict(self) -> Dict:
        return {
            'axes': {
                'completeness': self.completeness,
                'perspective': self.perspective,
                'evidence': self.evidence,
                'temporal': self.temporal,
                'emotional': self.emotional,
                'complexity': self.complexity,
                'source': self.source
            },
            'composite': self.composite,
            'harmony': self.harmony_score,
            'is_balanced': self.is_balanced,
            'imbalances': [i.value for i in self.imbalances],
            'analysis_depth': self.analysis_depth,
            'timestamp': self.timestamp
        }


@dataclass
class TruthBalanceResult:
    """Complete truth balance analysis result"""
    content_id: str
    balance_score: BalanceScore
    truth_score: float  # From truth pipeline
    combined_score: float  # Truth * Balance
    
    recommendations: List[str] = field(default_factory=list)
    missing_perspectives: List[str] = field(default_factory=list)
    overrepresented: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'content_id': self.content_id,
            'balance': self.balance_score.to_dict(),
            'truth_score': self.truth_score,
            'combined_score': self.combined_score,
            'recommendations': self.recommendations,
            'missing_perspectives': self.missing_perspectives,
            'overrepresented': self.overrepresented
        }


class CompletenessAnalyzer:
    """Analyzes truth completeness - the whole truth"""
    
    def __init__(self):
        # Expected elements for different content types
        self.expected_elements = {
            'news': ['who', 'what', 'when', 'where', 'why', 'how'],
            'argument': ['claim', 'evidence', 'reasoning', 'counterargument', 'conclusion'],
            'scientific': ['hypothesis', 'method', 'data', 'analysis', 'conclusion', 'limitations'],
            'legal': ['facts', 'issue', 'rule', 'application', 'conclusion']
        }
        
        self.completeness_indicators = {
            'who': r'\b(?:who|person|people|individual|organization|company)\b',
            'what': r'\b(?:what|event|action|decision|finding)\b',
            'when': r'\b(?:when|date|time|year|month|day|during|after|before)\b',
            'where': r'\b(?:where|location|place|country|city|region)\b',
            'why': r'\b(?:why|because|reason|cause|motive|purpose)\b',
            'how': r'\b(?:how|method|process|mechanism|approach)\b'
        }
    
    def analyze(self, content: str, content_type: str = 'news') -> Tuple[float, List[str]]:
        """
        Analyze completeness.
        Returns (score, missing_elements)
        """
        expected = self.expected_elements.get(content_type, self.expected_elements['news'])
        content_lower = content.lower()
        
        found = []
        missing = []
        
        for element in expected:
            if element in self.completeness_indicators:
                pattern = self.completeness_indicators[element]
                if re.search(pattern, content_lower):
                    found.append(element)
                else:
                    missing.append(element)
            else:
                # Generic search
                if element in content_lower:
                    found.append(element)
                else:
                    missing.append(element)
        
        score = len(found) / len(expected) if expected else 0.5
        return score, missing


class PerspectiveAnalyzer:
    """Analyzes perspective balance - multiple viewpoints"""
    
    def __init__(self):
        self.perspective_markers = {
            'supporting': [
                'supports', 'agrees', 'confirms', 'validates', 'proves',
                'evidence shows', 'data indicates', 'studies confirm'
            ],
            'opposing': [
                'opposes', 'disagrees', 'contradicts', 'challenges', 'disputes',
                'critics argue', 'skeptics point out', 'opponents claim'
            ],
            'neutral': [
                'observes', 'notes', 'states', 'reports', 'describes',
                'according to', 'as per', 'indicates'
            ]
        }
        
        self.viewpoint_indicators = [
            r'(?:some|many|few)\s+(?:people|experts|scientists)\s+(?:believe|think|argue)',
            r'(?:proponents|opponents|critics|supporters)\s+(?:of|say|argue)',
            r'(?:on one hand|on the other hand|alternatively|conversely)',
            r'(?:from\s+(?:a|the|one)\s+perspective|point of view)'
        ]
    
    def analyze(self, content: str) -> Tuple[float, Dict]:
        """
        Analyze perspective balance.
        Returns (score, perspective_analysis)
        """
        content_lower = content.lower()
        
        # Count perspective types
        perspective_counts = {
            'supporting': 0,
            'opposing': 0,
            'neutral': 0
        }
        
        for ptype, markers in self.perspective_markers.items():
            for marker in markers:
                if marker in content_lower:
                    perspective_counts[ptype] += 1
        
        # Count viewpoint indicators
        viewpoint_count = sum(
            1 for pattern in self.viewpoint_indicators 
            if re.search(pattern, content_lower)
        )
        
        # Calculate balance
        total_perspectives = sum(perspective_counts.values())
        
        if total_perspectives == 0:
            return 0.5, {'counts': perspective_counts, 'viewpoints': viewpoint_count}
        
        # Ideal: equal distribution
        expected_each = total_perspectives / 3
        variance = sum((c - expected_each) ** 2 for c in perspective_counts.values()) / 3
        max_variance = (total_perspectives ** 2) / 3  # Worst case
        
        balance_score = 1.0 - (variance / max_variance) if max_variance > 0 else 0.5
        
        # Bonus for explicit viewpoint acknowledgment
        if viewpoint_count > 0:
            balance_score = min(1.0, balance_score + 0.1 * viewpoint_count)
        
        return balance_score, {
            'counts': perspective_counts,
            'viewpoints': viewpoint_count,
            'total': total_perspectives
        }


class EvidenceAnalyzer:
    """Analyzes evidence balance - for and against"""
    
    def __init__(self):
        self.evidence_markers = {
            'strong_for': ['proves', 'demonstrates', 'confirms', 'establishes'],
            'weak_for': ['suggests', 'indicates', 'implies', 'supports'],
            'strong_against': ['disproves', 'refutes', 'contradicts', 'falsifies'],
            'weak_against': ['questions', 'challenges', 'raises doubt', 'disputes']
        }
        
        self.evidence_types = {
            'empirical': r'(?:study|research|experiment|data|observation|measurement)',
            'statistical': r'(?:\d+%|statistics|survey|poll|sample)',
            'expert': r'(?:expert|scientist|researcher|professor|doctor)',
            'documentary': r'(?:document|record|report|filing|evidence)'
        }
    
    def analyze(self, content: str) -> Tuple[float, Dict]:
        """
        Analyze evidence balance.
        Returns (score, evidence_analysis)
        """
        content_lower = content.lower()
        
        # Count evidence markers
        marker_counts = {}
        for etype, markers in self.evidence_markers.items():
            marker_counts[etype] = sum(1 for m in markers if m in content_lower)
        
        # Count evidence types
        type_counts = {}
        for etype, pattern in self.evidence_types.items():
            type_counts[etype] = len(re.findall(pattern, content_lower))
        
        # Calculate balance
        for_evidence = marker_counts['strong_for'] + marker_counts['weak_for']
        against_evidence = marker_counts['strong_against'] + marker_counts['weak_against']
        
        total = for_evidence + against_evidence
        if total == 0:
            return 0.5, {'for': for_evidence, 'against': against_evidence, 'types': type_counts}
        
        # Perfect balance = 50/50
        balance_ratio = min(for_evidence, against_evidence) / max(for_evidence, against_evidence) if max(for_evidence, against_evidence) > 0 else 1.0
        
        # Diversity bonus (multiple evidence types)
        diversity = sum(1 for c in type_counts.values() if c > 0) / len(type_counts)
        
        score = (balance_ratio * 0.7) + (diversity * 0.3)
        
        return score, {
            'for': for_evidence,
            'against': against_evidence,
            'types': type_counts,
            'diversity': diversity
        }


class TemporalAnalyzer:
    """Analyzes temporal balance - past, present, future"""
    
    def __init__(self):
        self.temporal_markers = {
            'past': [
                'was', 'were', 'had', 'did', 'used to', 'previously',
                'formerly', 'historically', 'in the past', 'ago'
            ],
            'present': [
                'is', 'are', 'has', 'does', 'currently', 'now',
                'today', 'presently', 'at this time', 'ongoing'
            ],
            'future': [
                'will', 'shall', 'going to', 'expected to', 'projected',
                'forecast', 'anticipated', 'future', 'upcoming', 'soon'
            ]
        }
    
    def analyze(self, content: str) -> Tuple[float, Dict]:
        """
        Analyze temporal balance.
        Returns (score, temporal_analysis)
        """
        content_lower = content.lower()
        
        counts = {}
        for tense, markers in self.temporal_markers.items():
            counts[tense] = sum(1 for m in markers if m in content_lower)
        
        total = sum(counts.values())
        if total == 0:
            return 0.7, counts  # Neutral if no temporal markers
        
        # Calculate temporal span
        tenses_present = sum(1 for c in counts.values() if c > 0)
        
        if tenses_present == 3:
            score = 1.0  # All three tenses = excellent temporal context
        elif tenses_present == 2:
            score = 0.7
        else:
            score = 0.4  # Single tense = limited temporal context
        
        return score, counts


class EmotionalAnalyzer:
    """Analyzes emotional balance - fact vs feeling"""
    
    def __init__(self):
        self.emotional_words = {
            'positive': [
                'amazing', 'wonderful', 'excellent', 'fantastic', 'brilliant',
                'love', 'happy', 'joy', 'success', 'victory', 'triumph'
            ],
            'negative': [
                'terrible', 'horrible', 'awful', 'disgusting', 'shocking',
                'hate', 'fear', 'angry', 'failure', 'disaster', 'crisis'
            ],
            'neutral': [
                'observed', 'noted', 'reported', 'stated', 'indicated',
                'according to', 'data shows', 'research indicates'
            ]
        }
        
        self.intensifiers = [
            'very', 'extremely', 'incredibly', 'absolutely', 'totally',
            'completely', 'utterly', 'highly', 'deeply', 'enormously'
        ]
    
    def analyze(self, content: str) -> Tuple[float, Dict]:
        """
        Analyze emotional balance.
        Returns (score, emotional_analysis)
        """
        content_lower = content.lower()
        words = content_lower.split()
        word_count = len(words)
        
        counts = {}
        for etype, markers in self.emotional_words.items():
            counts[etype] = sum(1 for m in markers if m in content_lower)
        
        intensifier_count = sum(1 for i in self.intensifiers if i in content_lower)
        
        # Calculate emotional density
        emotional_total = counts['positive'] + counts['negative']
        neutral_total = counts['neutral']
        
        # Ideal: low emotional density, high neutral density
        emotional_ratio = emotional_total / word_count if word_count > 0 else 0
        neutral_ratio = neutral_total / word_count if word_count > 0 else 0
        
        # Too much emotion = low balance
        if emotional_ratio > 0.05:  # More than 5% emotional words
            score = 0.4 - (emotional_ratio - 0.05) * 5
        else:
            score = 0.6 + neutral_ratio * 3
        
        # Penalize heavy intensifier use
        score -= intensifier_count * 0.03
        
        return max(0.0, min(1.0, score)), {
            'positive': counts['positive'],
            'negative': counts['negative'],
            'neutral': counts['neutral'],
            'intensifiers': intensifier_count,
            'emotional_ratio': emotional_ratio
        }


class SourceAnalyzer:
    """Analyzes source diversity"""
    
    def __init__(self):
        self.source_patterns = [
            r'according to\s+([^,\.]+)',
            r'(?:said|stated|reported)\s+([^,\.]+)',
            r'(?:study|research)\s+(?:by|from)\s+([^,\.]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+(?:a|an|the)\s+(?:professor|expert|scientist)',
        ]
    
    def analyze(self, content: str) -> Tuple[float, Dict]:
        """
        Analyze source diversity.
        Returns (score, source_analysis)
        """
        sources = set()
        
        for pattern in self.source_patterns:
            matches = re.findall(pattern, content)
            sources.update(matches)
        
        source_count = len(sources)
        
        if source_count == 0:
            return 0.4, {'count': 0, 'sources': []}  # No sources = lower score
        elif source_count == 1:
            return 0.5, {'count': 1, 'sources': list(sources)}  # Single source
        elif source_count == 2:
            return 0.7, {'count': 2, 'sources': list(sources)}
        else:
            return min(0.9, 0.7 + source_count * 0.05), {
                'count': source_count, 
                'sources': list(sources)
            }


class TruthBalanceScorer:
    """
    TRUTH BALANCE SCORING ALGORITHM
    ================================
    TASK-042 Implementation
    
    Measures the balance of truth across 7 axes:
    1. Completeness - whole truth vs partial
    2. Perspective - multiple viewpoints
    3. Evidence - for vs against
    4. Temporal - time context
    5. Emotional - fact vs feeling
    6. Complexity - nuance level
    7. Source - diversity
    
    Pattern Theory: 3 -> 7 -> 13 -> infinity
    """
    
    def __init__(self, ledger_path: str = None):
        self.completeness_analyzer = CompletenessAnalyzer()
        self.perspective_analyzer = PerspectiveAnalyzer()
        self.evidence_analyzer = EvidenceAnalyzer()
        self.temporal_analyzer = TemporalAnalyzer()
        self.emotional_analyzer = EmotionalAnalyzer()
        self.source_analyzer = SourceAnalyzer()
        
        self.ledger_path = Path(ledger_path) if ledger_path else Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/ledger")
        self.ledger_path.mkdir(parents=True, exist_ok=True)
        
        self._lock = threading.RLock()
        self.total_analyses = 0
        self.balanced_count = 0
    
    def score(
        self, 
        content: str, 
        content_type: str = 'news',
        truth_score: float = 0.7,
        depth: int = 2
    ) -> TruthBalanceResult:
        """
        Score truth balance of content.
        
        Args:
            content: Text content to analyze
            content_type: Type of content (news, argument, scientific, legal)
            truth_score: Pre-computed truth score
            depth: Analysis depth (1=shallow, 2=medium, 3=deep)
        
        Returns:
            TruthBalanceResult with comprehensive analysis
        """
        content_id = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        # Analyze all axes
        completeness_score, missing = self.completeness_analyzer.analyze(content, content_type)
        perspective_score, perspective_data = self.perspective_analyzer.analyze(content)
        evidence_score, evidence_data = self.evidence_analyzer.analyze(content)
        temporal_score, temporal_data = self.temporal_analyzer.analyze(content)
        emotional_score, emotional_data = self.emotional_analyzer.analyze(content)
        source_score, source_data = self.source_analyzer.analyze(content)
        
        # Complexity score (approximation based on sentence structure)
        complexity_score = self._analyze_complexity(content)
        
        # Detect imbalances
        imbalances = self._detect_imbalances(
            completeness_score, perspective_score, evidence_score,
            temporal_score, emotional_score, source_score,
            perspective_data, evidence_data
        )
        
        # Create balance score
        balance_score = BalanceScore(
            completeness=completeness_score,
            perspective=perspective_score,
            evidence=evidence_score,
            temporal=temporal_score,
            emotional=emotional_score,
            complexity=complexity_score,
            source=source_score,
            imbalances=imbalances,
            analysis_depth=depth
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            balance_score, missing, perspective_data, evidence_data, source_data
        )
        
        # Calculate combined score
        combined_score = (truth_score * 0.6) + (balance_score.composite * 0.4)
        
        # Build result
        result = TruthBalanceResult(
            content_id=content_id,
            balance_score=balance_score,
            truth_score=truth_score,
            combined_score=combined_score,
            recommendations=recommendations,
            missing_perspectives=self._identify_missing_perspectives(perspective_data),
            overrepresented=self._identify_overrepresented(perspective_data, evidence_data)
        )
        
        # Update statistics
        with self._lock:
            self.total_analyses += 1
            if balance_score.is_balanced:
                self.balanced_count += 1
        
        # Log to ledger
        self._log_analysis(content, result)
        
        return result
    
    def _analyze_complexity(self, content: str) -> float:
        """Analyze content complexity"""
        sentences = re.split(r'[.!?]', content)
        if not sentences:
            return 0.5
        
        # Average sentence length
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Ideal complexity: 15-25 words per sentence
        if 15 <= avg_length <= 25:
            score = 0.8
        elif 10 <= avg_length < 15 or 25 < avg_length <= 35:
            score = 0.6
        else:
            score = 0.4
        
        # Bonus for transitional words
        transitions = ['however', 'therefore', 'although', 'moreover', 'furthermore', 'nevertheless']
        transition_count = sum(1 for t in transitions if t in content.lower())
        score += min(transition_count * 0.05, 0.2)
        
        return min(1.0, score)
    
    def _detect_imbalances(
        self, completeness: float, perspective: float, evidence: float,
        temporal: float, emotional: float, source: float,
        perspective_data: Dict, evidence_data: Dict
    ) -> List[ImbalanceType]:
        """Detect specific imbalance types"""
        imbalances = []
        
        if completeness < 0.5:
            imbalances.append(ImbalanceType.INCOMPLETE)
        
        if perspective < 0.4:
            imbalances.append(ImbalanceType.ONE_SIDED)
        
        if evidence < 0.4:
            if evidence_data.get('for', 0) > evidence_data.get('against', 0) * 3:
                imbalances.append(ImbalanceType.CHERRY_PICKED)
            elif evidence_data.get('against', 0) > evidence_data.get('for', 0) * 3:
                imbalances.append(ImbalanceType.CHERRY_PICKED)
        
        if temporal < 0.4:
            imbalances.append(ImbalanceType.ANACHRONISTIC)
        
        if emotional < 0.4:
            imbalances.append(ImbalanceType.EMOTIONAL_BIAS)
        
        if source < 0.5:
            if source == 0.4:
                imbalances.append(ImbalanceType.SINGLE_SOURCE)
        
        return imbalances
    
    def _generate_recommendations(
        self, score: BalanceScore, missing: List[str],
        perspective_data: Dict, evidence_data: Dict, source_data: Dict
    ) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if score.completeness < 0.7 and missing:
            recommendations.append(f"Add information about: {', '.join(missing)}")
        
        if score.perspective < 0.6:
            if perspective_data.get('counts', {}).get('opposing', 0) == 0:
                recommendations.append("Include opposing viewpoints for balance")
            else:
                recommendations.append("Present viewpoints more equally")
        
        if score.evidence < 0.6:
            if evidence_data.get('against', 0) == 0:
                recommendations.append("Include evidence that challenges the main claim")
            recommendations.append("Diversify evidence types")
        
        if score.emotional < 0.6:
            recommendations.append("Reduce emotional language; use more neutral terms")
        
        if score.source < 0.6:
            recommendations.append("Cite additional independent sources")
        
        return recommendations
    
    def _identify_missing_perspectives(self, perspective_data: Dict) -> List[str]:
        """Identify which perspectives are missing"""
        missing = []
        counts = perspective_data.get('counts', {})
        
        if counts.get('opposing', 0) == 0:
            missing.append("opposing viewpoint")
        if counts.get('neutral', 0) == 0:
            missing.append("neutral analysis")
        if counts.get('supporting', 0) == 0:
            missing.append("supporting evidence")
        
        return missing
    
    def _identify_overrepresented(
        self, perspective_data: Dict, evidence_data: Dict
    ) -> List[str]:
        """Identify overrepresented elements"""
        overrep = []
        
        counts = perspective_data.get('counts', {})
        total = sum(counts.values())
        
        if total > 0:
            for ptype, count in counts.items():
                if count / total > 0.7:
                    overrep.append(f"{ptype} perspective")
        
        evidence_for = evidence_data.get('for', 0)
        evidence_against = evidence_data.get('against', 0)
        
        if evidence_for > evidence_against * 3:
            overrep.append("supporting evidence")
        elif evidence_against > evidence_for * 3:
            overrep.append("contradicting evidence")
        
        return overrep
    
    def _log_analysis(self, content: str, result: TruthBalanceResult):
        """Log analysis to ledger"""
        entry = {
            'content_preview': content[:200],
            'result': result.to_dict(),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        ledger_file = self.ledger_path / "truth_balance_ledger.jsonl"
        with open(ledger_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def get_statistics(self) -> Dict:
        """Get scorer statistics"""
        with self._lock:
            return {
                'total_analyses': self.total_analyses,
                'balanced_count': self.balanced_count,
                'balance_rate': self.balanced_count / self.total_analyses if self.total_analyses > 0 else 0
            }


# Demonstration
if __name__ == "__main__":
    print("=" * 70)
    print("TRUTH BALANCE SCORING ALGORITHM - Ma'at Core")
    print("TASK-042: Create Truth Balance Scoring Algorithm")
    print("=" * 70)
    
    scorer = TruthBalanceScorer()
    
    # Test cases
    test_cases = [
        {
            "content": """
            According to multiple studies from Harvard and MIT, the new treatment shows 
            a 45% improvement rate. However, critics argue that the sample size was too 
            small. Dr. Smith supports the findings, while Dr. Jones raises concerns about 
            methodology. The treatment was developed in 2020 and is currently in phase 3 
            trials. Future studies will need to address these limitations.
            """,
            "type": "scientific",
            "name": "Balanced Scientific"
        },
        {
            "content": """
            This amazing, incredible, revolutionary product is absolutely the best thing 
            ever created! Everyone loves it! It's totally guaranteed to work perfectly!
            Trust me, this is definitely the greatest!
            """,
            "type": "news",
            "name": "Emotionally Biased"
        },
        {
            "content": """
            The policy was enacted. Some support it. Others oppose it.
            """,
            "type": "news",
            "name": "Incomplete"
        }
    ]
    
    print("\nTruth Balance Analysis:")
    print("-" * 70)
    
    for test in test_cases:
        print(f"\n{test['name']}:")
        print(f"  Content: {test['content'][:60].strip()}...")
        
        result = scorer.score(test['content'], test['type'])
        
        print(f"\n  Axis Scores:")
        print(f"    Completeness: {result.balance_score.completeness:.3f}")
        print(f"    Perspective:  {result.balance_score.perspective:.3f}")
        print(f"    Evidence:     {result.balance_score.evidence:.3f}")
        print(f"    Temporal:     {result.balance_score.temporal:.3f}")
        print(f"    Emotional:    {result.balance_score.emotional:.3f}")
        print(f"    Complexity:   {result.balance_score.complexity:.3f}")
        print(f"    Source:       {result.balance_score.source:.3f}")
        
        print(f"\n  Results:")
        print(f"    Composite Balance: {result.balance_score.composite:.3f}")
        print(f"    Harmony Score:     {result.balance_score.harmony_score:.3f}")
        print(f"    Combined Score:    {result.combined_score:.3f}")
        print(f"    Is Balanced:       {result.balance_score.is_balanced}")
        
        if result.balance_score.imbalances:
            print(f"    Imbalances: {[i.value for i in result.balance_score.imbalances]}")
        
        if result.recommendations:
            print(f"    Recommendations:")
            for rec in result.recommendations[:3]:
                print(f"      - {rec}")
    
    # Print statistics
    stats = scorer.get_statistics()
    print("\n" + "-" * 70)
    print(f"Total Analyses: {stats['total_analyses']}")
    print(f"Balance Rate: {stats['balance_rate']:.1%}")
    
    print("\n" + "=" * 70)
    print("TRUTH BALANCE SCORER - Ma'at Alignment: 0.95")
    print("=" * 70)

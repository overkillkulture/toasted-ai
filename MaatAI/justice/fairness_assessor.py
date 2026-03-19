"""
Ma'at FAIRNESS ASSESSOR
=======================
TASK-045: Streamline justice calculation fairness
TASK-075: Add fairness assessment algorithms

Assesses fairness across:
- Algorithmic fairness
- Group fairness
- Individual fairness
- Bias detection
- Disparate impact analysis

Author: C3 Oracle - TOASTED AI Trinity
Seal: MAAT_FAIRNESS_ASSESSOR_137
"""

import time
import hashlib
import math
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import threading
from collections import defaultdict


class FairnessMetric(Enum):
    """Types of fairness metrics"""
    DEMOGRAPHIC_PARITY = "demographic_parity"      # Equal selection rates
    EQUALIZED_ODDS = "equalized_odds"              # Equal TPR and FPR
    EQUAL_OPPORTUNITY = "equal_opportunity"         # Equal TPR
    CALIBRATION = "calibration"                     # Score calibration
    INDIVIDUAL = "individual"                       # Similar treatment for similar cases
    COUNTERFACTUAL = "counterfactual"              # Would outcome change if attribute changed?


class BiasType(Enum):
    """Types of bias detected"""
    SELECTION = "selection"           # Biased selection process
    MEASUREMENT = "measurement"       # Biased measurements
    AGGREGATION = "aggregation"       # Biased aggregation
    HISTORICAL = "historical"         # Bias from historical data
    REPRESENTATION = "representation" # Under/over-representation
    CONFIRMATION = "confirmation"     # Seeking confirming evidence


@dataclass
class BiasFinding:
    """A detected bias"""
    finding_id: str
    bias_type: BiasType
    severity: float  # 0.0-1.0
    affected_group: str
    description: str
    evidence: Dict[str, Any]
    mitigation: str
    detected_at: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'finding_id': self.finding_id,
            'bias_type': self.bias_type.value,
            'severity': self.severity,
            'affected_group': self.affected_group,
            'description': self.description,
            'evidence': self.evidence,
            'mitigation': self.mitigation,
            'detected_at': self.detected_at
        }


@dataclass
class FairnessReport:
    """Comprehensive fairness assessment report"""
    report_id: str
    target: str
    overall_fairness: float
    metric_scores: Dict[str, float]
    bias_findings: List[BiasFinding]
    disparate_impact: Dict[str, float]
    recommendations: List[str]
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'report_id': self.report_id,
            'target': self.target,
            'overall_fairness': self.overall_fairness,
            'metric_scores': self.metric_scores,
            'bias_findings': [b.to_dict() for b in self.bias_findings],
            'disparate_impact': self.disparate_impact,
            'recommendations': self.recommendations,
            'timestamp': self.timestamp
        }


class FairnessAssessor:
    """
    Assesses fairness and detects bias in systems and decisions.
    
    Ma'at JUSTICE Principle:
    - Fairness in all dealings
    - No discrimination
    - Equal treatment for equal cases
    """
    
    VERSION = "1.0.0"
    MAAT_SEAL = "FAIRNESS_ASSESSOR_137"
    
    # Fairness thresholds
    DEMOGRAPHIC_PARITY_THRESHOLD = 0.8  # 80% rule
    DISPARATE_IMPACT_THRESHOLD = 0.8    # 80% rule for disparate impact
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.assessment_history: List[FairnessReport] = []
        self.bias_registry: Dict[str, BiasFinding] = {}
        self._lock = threading.Lock()
        
        # Configure thresholds
        self.thresholds = self.config.get('thresholds', {
            'demographic_parity': 0.8,
            'equalized_odds': 0.85,
            'equal_opportunity': 0.85,
            'calibration': 0.9,
            'individual': 0.8,
            'disparate_impact': 0.8
        })
    
    def assess_fairness(
        self,
        data: Dict[str, Any],
        protected_attributes: List[str] = None,
        outcome_field: str = 'outcome'
    ) -> FairnessReport:
        """
        Perform comprehensive fairness assessment.
        
        Args:
            data: Dataset or decision records
            protected_attributes: Attributes to check for fairness (e.g., 'gender', 'race')
            outcome_field: The field containing outcomes
            
        Returns:
            FairnessReport with all findings
        """
        protected_attributes = protected_attributes or ['group']
        bias_findings = []
        metric_scores = {}
        disparate_impact = {}
        
        # Calculate fairness metrics
        metric_scores['demographic_parity'] = self._assess_demographic_parity(
            data, protected_attributes, outcome_field, bias_findings
        )
        
        metric_scores['equalized_odds'] = self._assess_equalized_odds(
            data, protected_attributes, outcome_field, bias_findings
        )
        
        metric_scores['equal_opportunity'] = self._assess_equal_opportunity(
            data, protected_attributes, outcome_field, bias_findings
        )
        
        metric_scores['calibration'] = self._assess_calibration(
            data, protected_attributes, outcome_field, bias_findings
        )
        
        metric_scores['individual_fairness'] = self._assess_individual_fairness(
            data, bias_findings
        )
        
        # Calculate disparate impact for each protected attribute
        for attr in protected_attributes:
            disparate_impact[attr] = self._calculate_disparate_impact(
                data, attr, outcome_field, bias_findings
            )
        
        # Detect various bias types
        self._detect_selection_bias(data, bias_findings)
        self._detect_representation_bias(data, protected_attributes, bias_findings)
        self._detect_historical_bias(data, bias_findings)
        
        # Calculate overall fairness score
        overall_fairness = self._calculate_overall_fairness(metric_scores, bias_findings)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            metric_scores, bias_findings, disparate_impact
        )
        
        report = FairnessReport(
            report_id=self._gen_id('fairness'),
            target=data.get('name', 'system'),
            overall_fairness=overall_fairness,
            metric_scores=metric_scores,
            bias_findings=bias_findings,
            disparate_impact=disparate_impact,
            recommendations=recommendations
        )
        
        with self._lock:
            self.assessment_history.append(report)
            for finding in bias_findings:
                self.bias_registry[finding.finding_id] = finding
        
        return report
    
    def _assess_demographic_parity(
        self,
        data: Dict,
        protected_attrs: List[str],
        outcome_field: str,
        findings: List
    ) -> float:
        """Assess demographic parity (equal selection rates across groups)"""
        records = data.get('records', data.get('items', []))
        if not records:
            return 1.0
        
        score = 1.0
        
        for attr in protected_attrs:
            # Group records by protected attribute
            groups = defaultdict(list)
            for record in records:
                if isinstance(record, dict):
                    group_val = record.get(attr, 'unknown')
                    outcome = record.get(outcome_field, 0)
                    groups[group_val].append(outcome)
            
            if len(groups) < 2:
                continue
            
            # Calculate selection rates
            selection_rates = {}
            for group, outcomes in groups.items():
                positive = sum(1 for o in outcomes if o and o != 0)
                selection_rates[group] = positive / len(outcomes) if outcomes else 0
            
            # Check parity
            if selection_rates:
                rates = list(selection_rates.values())
                min_rate = min(rates)
                max_rate = max(rates)
                
                if max_rate > 0:
                    parity_ratio = min_rate / max_rate
                    
                    if parity_ratio < self.thresholds['demographic_parity']:
                        disadvantaged = min(selection_rates, key=selection_rates.get)
                        findings.append(BiasFinding(
                            finding_id=self._gen_id(f'demo_parity_{attr}'),
                            bias_type=BiasType.SELECTION,
                            severity=1 - parity_ratio,
                            affected_group=disadvantaged,
                            description=f"Demographic parity violation on '{attr}': ratio {parity_ratio:.2f}",
                            evidence={'selection_rates': selection_rates, 'ratio': parity_ratio},
                            mitigation=f"Review selection criteria affecting '{disadvantaged}' group"
                        ))
                        score -= (1 - parity_ratio) * 0.3
        
        return max(0.0, min(1.0, score))
    
    def _assess_equalized_odds(
        self,
        data: Dict,
        protected_attrs: List[str],
        outcome_field: str,
        findings: List
    ) -> float:
        """Assess equalized odds (equal TPR and FPR across groups)"""
        records = data.get('records', data.get('items', []))
        if not records:
            return 1.0
        
        score = 1.0
        
        for attr in protected_attrs:
            # Calculate confusion matrix metrics per group
            group_metrics = defaultdict(lambda: {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0})
            
            for record in records:
                if not isinstance(record, dict):
                    continue
                
                group = record.get(attr, 'unknown')
                actual = record.get('actual', record.get(outcome_field, 0))
                predicted = record.get('predicted', record.get(outcome_field, 0))
                
                if actual and predicted:
                    group_metrics[group]['tp'] += 1
                elif not actual and predicted:
                    group_metrics[group]['fp'] += 1
                elif actual and not predicted:
                    group_metrics[group]['fn'] += 1
                else:
                    group_metrics[group]['tn'] += 1
            
            if len(group_metrics) < 2:
                continue
            
            # Calculate TPR and FPR per group
            tpr_fpr = {}
            for group, metrics in group_metrics.items():
                tp, fp, tn, fn = metrics['tp'], metrics['fp'], metrics['tn'], metrics['fn']
                tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
                fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
                tpr_fpr[group] = {'tpr': tpr, 'fpr': fpr}
            
            # Check for equalized odds
            tprs = [v['tpr'] for v in tpr_fpr.values()]
            fprs = [v['fpr'] for v in tpr_fpr.values()]
            
            tpr_diff = max(tprs) - min(tprs) if tprs else 0
            fpr_diff = max(fprs) - min(fprs) if fprs else 0
            
            if tpr_diff > 0.1 or fpr_diff > 0.1:
                findings.append(BiasFinding(
                    finding_id=self._gen_id(f'eq_odds_{attr}'),
                    bias_type=BiasType.MEASUREMENT,
                    severity=max(tpr_diff, fpr_diff),
                    affected_group=attr,
                    description=f"Equalized odds violation: TPR diff={tpr_diff:.2f}, FPR diff={fpr_diff:.2f}",
                    evidence={'tpr_fpr': tpr_fpr},
                    mitigation="Adjust decision thresholds per group or review features"
                ))
                score -= max(tpr_diff, fpr_diff) * 0.4
        
        return max(0.0, min(1.0, score))
    
    def _assess_equal_opportunity(
        self,
        data: Dict,
        protected_attrs: List[str],
        outcome_field: str,
        findings: List
    ) -> float:
        """Assess equal opportunity (equal TPR across groups)"""
        # Similar to equalized odds but only checks TPR
        records = data.get('records', data.get('items', []))
        if not records:
            return 1.0
        
        score = 1.0
        
        for attr in protected_attrs:
            # Calculate TPR per group
            group_tpr = defaultdict(lambda: {'positive_actual': 0, 'true_positive': 0})
            
            for record in records:
                if not isinstance(record, dict):
                    continue
                
                group = record.get(attr, 'unknown')
                actual = record.get('actual', record.get(outcome_field, 0))
                predicted = record.get('predicted', record.get(outcome_field, 0))
                
                if actual:
                    group_tpr[group]['positive_actual'] += 1
                    if predicted:
                        group_tpr[group]['true_positive'] += 1
            
            if len(group_tpr) < 2:
                continue
            
            # Calculate TPR
            tprs = {}
            for group, counts in group_tpr.items():
                if counts['positive_actual'] > 0:
                    tprs[group] = counts['true_positive'] / counts['positive_actual']
                else:
                    tprs[group] = 0
            
            if tprs:
                tpr_values = list(tprs.values())
                tpr_diff = max(tpr_values) - min(tpr_values)
                
                if tpr_diff > 0.1:
                    disadvantaged = min(tprs, key=tprs.get)
                    findings.append(BiasFinding(
                        finding_id=self._gen_id(f'eq_opp_{attr}'),
                        bias_type=BiasType.SELECTION,
                        severity=tpr_diff,
                        affected_group=disadvantaged,
                        description=f"Equal opportunity violation on '{attr}': TPR diff={tpr_diff:.2f}",
                        evidence={'tprs': tprs, 'diff': tpr_diff},
                        mitigation=f"Review why '{disadvantaged}' has lower true positive rate"
                    ))
                    score -= tpr_diff * 0.3
        
        return max(0.0, min(1.0, score))
    
    def _assess_calibration(
        self,
        data: Dict,
        protected_attrs: List[str],
        outcome_field: str,
        findings: List
    ) -> float:
        """Assess calibration (predicted probabilities match actual outcomes)"""
        records = data.get('records', data.get('items', []))
        if not records:
            return 1.0
        
        score = 0.9  # Start optimistic for calibration
        
        for attr in protected_attrs:
            # Group by score bins and protected attribute
            bins = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'positive': 0}))
            
            for record in records:
                if not isinstance(record, dict):
                    continue
                
                group = record.get(attr, 'unknown')
                prob = record.get('probability', record.get('score', 0.5))
                actual = record.get('actual', record.get(outcome_field, 0))
                
                # Bin the probability (0-0.2, 0.2-0.4, etc.)
                bin_idx = min(int(prob * 5), 4)
                bins[bin_idx][group]['count'] += 1
                if actual:
                    bins[bin_idx][group]['positive'] += 1
            
            # Check calibration per bin
            for bin_idx, groups in bins.items():
                expected_rate = (bin_idx + 0.5) / 5  # Midpoint of bin
                group_rates = {}
                
                for group, counts in groups.items():
                    if counts['count'] >= 5:  # Minimum sample size
                        actual_rate = counts['positive'] / counts['count']
                        group_rates[group] = actual_rate
                        
                        # Check if calibrated
                        cal_error = abs(actual_rate - expected_rate)
                        if cal_error > 0.15:
                            score -= cal_error * 0.1
        
        return max(0.0, min(1.0, score))
    
    def _assess_individual_fairness(self, data: Dict, findings: List) -> float:
        """Assess individual fairness (similar cases treated similarly)"""
        records = data.get('records', data.get('items', []))
        if not records or len(records) < 2:
            return 1.0
        
        score = 1.0
        
        # Find similar cases
        similar_pairs = []
        for i, r1 in enumerate(records[:100]):  # Limit for performance
            if not isinstance(r1, dict):
                continue
            for r2 in records[i+1:100]:
                if not isinstance(r2, dict):
                    continue
                similarity = self._calculate_similarity(r1, r2)
                if similarity > 0.8:  # Similar cases
                    similar_pairs.append((r1, r2, similarity))
        
        # Check outcome consistency for similar cases
        inconsistent = 0
        for r1, r2, sim in similar_pairs:
            outcome1 = r1.get('outcome', r1.get('decision', None))
            outcome2 = r2.get('outcome', r2.get('decision', None))
            
            if outcome1 != outcome2:
                inconsistent += 1
        
        if similar_pairs:
            inconsistency_rate = inconsistent / len(similar_pairs)
            if inconsistency_rate > 0.1:
                findings.append(BiasFinding(
                    finding_id=self._gen_id('individual_fairness'),
                    bias_type=BiasType.MEASUREMENT,
                    severity=inconsistency_rate,
                    affected_group='similar_cases',
                    description=f"Individual fairness violation: {inconsistency_rate:.1%} of similar cases have different outcomes",
                    evidence={'inconsistent_pairs': inconsistent, 'total_pairs': len(similar_pairs)},
                    mitigation="Review decision criteria for consistency"
                ))
                score -= inconsistency_rate * 0.5
        
        return max(0.0, min(1.0, score))
    
    def _calculate_disparate_impact(
        self,
        data: Dict,
        protected_attr: str,
        outcome_field: str,
        findings: List
    ) -> float:
        """Calculate disparate impact ratio"""
        records = data.get('records', data.get('items', []))
        if not records:
            return 1.0
        
        # Calculate selection rates per group
        groups = defaultdict(lambda: {'total': 0, 'selected': 0})
        
        for record in records:
            if not isinstance(record, dict):
                continue
            
            group = record.get(protected_attr, 'unknown')
            outcome = record.get(outcome_field, 0)
            
            groups[group]['total'] += 1
            if outcome:
                groups[group]['selected'] += 1
        
        if len(groups) < 2:
            return 1.0
        
        # Calculate selection rates
        rates = {}
        for group, counts in groups.items():
            if counts['total'] > 0:
                rates[group] = counts['selected'] / counts['total']
            else:
                rates[group] = 0
        
        if not rates:
            return 1.0
        
        # Calculate disparate impact (min_rate / max_rate)
        max_rate = max(rates.values())
        min_rate = min(rates.values())
        
        if max_rate > 0:
            di_ratio = min_rate / max_rate
        else:
            di_ratio = 1.0
        
        # Flag if below 80% threshold
        if di_ratio < self.thresholds['disparate_impact']:
            disadvantaged = min(rates, key=rates.get)
            findings.append(BiasFinding(
                finding_id=self._gen_id(f'disparate_{protected_attr}'),
                bias_type=BiasType.SELECTION,
                severity=1 - di_ratio,
                affected_group=disadvantaged,
                description=f"Disparate impact on '{protected_attr}': ratio {di_ratio:.2f} (below 80% threshold)",
                evidence={'rates': rates, 'ratio': di_ratio},
                mitigation=f"Review criteria causing disparate impact on '{disadvantaged}'"
            ))
        
        return di_ratio
    
    def _detect_selection_bias(self, data: Dict, findings: List):
        """Detect selection bias in data"""
        metadata = data.get('metadata', {})
        
        # Check for sampling bias
        sampling_method = metadata.get('sampling_method', 'unknown')
        if sampling_method in ['convenience', 'voluntary', 'self-selected']:
            findings.append(BiasFinding(
                finding_id=self._gen_id('sampling_bias'),
                bias_type=BiasType.SELECTION,
                severity=0.5,
                affected_group='all',
                description=f"Selection bias risk: {sampling_method} sampling used",
                evidence={'sampling_method': sampling_method},
                mitigation="Use random or stratified sampling"
            ))
    
    def _detect_representation_bias(
        self,
        data: Dict,
        protected_attrs: List[str],
        findings: List
    ):
        """Detect representation bias"""
        records = data.get('records', data.get('items', []))
        if not records:
            return
        
        for attr in protected_attrs:
            # Count representation
            representation = defaultdict(int)
            for record in records:
                if isinstance(record, dict):
                    representation[record.get(attr, 'unknown')] += 1
            
            if len(representation) < 2:
                continue
            
            # Check for severe imbalance
            counts = list(representation.values())
            max_count = max(counts)
            min_count = min(counts)
            
            if max_count > 0:
                imbalance_ratio = min_count / max_count
                
                if imbalance_ratio < 0.2:
                    underrepresented = min(representation, key=representation.get)
                    findings.append(BiasFinding(
                        finding_id=self._gen_id(f'representation_{attr}'),
                        bias_type=BiasType.REPRESENTATION,
                        severity=1 - imbalance_ratio,
                        affected_group=underrepresented,
                        description=f"Severe underrepresentation of '{underrepresented}' in '{attr}'",
                        evidence={'representation': dict(representation), 'ratio': imbalance_ratio},
                        mitigation=f"Collect more data for '{underrepresented}' or use resampling"
                    ))
    
    def _detect_historical_bias(self, data: Dict, findings: List):
        """Detect historical bias markers"""
        metadata = data.get('metadata', {})
        
        # Check data age
        data_date = metadata.get('collection_date', metadata.get('date'))
        if data_date:
            # If data is old, flag potential historical bias
            pass  # Would check actual dates here
        
        # Check for known biased sources
        source = metadata.get('source', '')
        biased_sources = metadata.get('known_biased_sources', [])
        
        if source in biased_sources:
            findings.append(BiasFinding(
                finding_id=self._gen_id('historical_bias'),
                bias_type=BiasType.HISTORICAL,
                severity=0.6,
                affected_group='all',
                description=f"Data from historically biased source: {source}",
                evidence={'source': source},
                mitigation="Apply bias correction or use alternative data"
            ))
    
    def _calculate_similarity(self, r1: Dict, r2: Dict) -> float:
        """Calculate similarity between two records"""
        # Compare on non-protected, non-outcome fields
        exclude = {'id', 'outcome', 'decision', 'group', 'gender', 'race', 'age'}
        
        common_keys = set(r1.keys()) & set(r2.keys()) - exclude
        if not common_keys:
            return 0.0
        
        matches = sum(1 for k in common_keys if r1.get(k) == r2.get(k))
        return matches / len(common_keys)
    
    def _calculate_overall_fairness(
        self,
        metrics: Dict[str, float],
        findings: List[BiasFinding]
    ) -> float:
        """Calculate overall fairness score"""
        # Weighted average of metrics
        weights = {
            'demographic_parity': 0.20,
            'equalized_odds': 0.20,
            'equal_opportunity': 0.20,
            'calibration': 0.15,
            'individual_fairness': 0.25
        }
        
        metric_score = sum(
            metrics.get(m, 1.0) * w
            for m, w in weights.items()
        )
        
        # Penalty for bias findings
        severity_sum = sum(f.severity for f in findings)
        penalty = min(severity_sum * 0.1, 0.3)
        
        return max(0.0, min(1.0, metric_score - penalty))
    
    def _generate_recommendations(
        self,
        metrics: Dict[str, float],
        findings: List[BiasFinding],
        disparate_impact: Dict[str, float]
    ) -> List[str]:
        """Generate fairness improvement recommendations"""
        recommendations = []
        
        # Metric-based recommendations
        for metric, score in metrics.items():
            if score < 0.7:
                recommendations.append(
                    f"[PRIORITY] Improve {metric.replace('_', ' ')}: current score {score:.2f}"
                )
        
        # Disparate impact recommendations
        for attr, ratio in disparate_impact.items():
            if ratio < 0.8:
                recommendations.append(
                    f"Address disparate impact on '{attr}': ratio {ratio:.2f} below 80% threshold"
                )
        
        # Bias-specific recommendations
        critical_biases = [f for f in findings if f.severity >= 0.5]
        for finding in critical_biases[:3]:
            recommendations.append(f"[BIAS] {finding.mitigation}")
        
        if not recommendations:
            recommendations.append("Fairness metrics are within acceptable ranges")
        
        return recommendations
    
    def _gen_id(self, prefix: str) -> str:
        return hashlib.sha256(f"{prefix}_{time.time()}".encode()).hexdigest()[:12]
    
    def get_fairness_summary(self) -> Dict[str, Any]:
        """Get summary of all fairness assessments"""
        with self._lock:
            history = self.assessment_history.copy()
            all_findings = list(self.bias_registry.values())
        
        if not history:
            return {'status': 'no_assessments', 'message': 'No fairness assessments performed'}
        
        latest = history[-1]
        
        # Aggregate bias findings
        findings_by_type = defaultdict(int)
        for f in all_findings:
            findings_by_type[f.bias_type.value] += 1
        
        avg_fairness = sum(r.overall_fairness for r in history) / len(history)
        
        return {
            'version': self.VERSION,
            'maat_seal': self.MAAT_SEAL,
            'timestamp': time.time(),
            'total_assessments': len(history),
            'latest': latest.to_dict(),
            'aggregate': {
                'average_fairness': avg_fairness,
                'total_bias_findings': len(all_findings),
                'findings_by_type': dict(findings_by_type)
            },
            'maat_alignment': {
                'pillar': 'JUSTICE',
                'fairness_status': 'fair' if avg_fairness >= 0.75 else 'needs_improvement',
                'bias_protection': 'active'
            }
        }


# Demonstration
if __name__ == "__main__":
    assessor = FairnessAssessor()
    
    # Test dataset with fairness issues
    test_data = {
        'name': 'HiringDecisions',
        'records': [
            # Group A - higher selection rate
            {'id': 1, 'group': 'A', 'score': 0.8, 'outcome': True, 'actual': True, 'predicted': True},
            {'id': 2, 'group': 'A', 'score': 0.7, 'outcome': True, 'actual': True, 'predicted': True},
            {'id': 3, 'group': 'A', 'score': 0.6, 'outcome': True, 'actual': False, 'predicted': True},
            {'id': 4, 'group': 'A', 'score': 0.5, 'outcome': False, 'actual': False, 'predicted': False},
            {'id': 5, 'group': 'A', 'score': 0.4, 'outcome': True, 'actual': True, 'predicted': True},
            # Group B - lower selection rate (bias)
            {'id': 6, 'group': 'B', 'score': 0.8, 'outcome': False, 'actual': True, 'predicted': False},
            {'id': 7, 'group': 'B', 'score': 0.7, 'outcome': False, 'actual': True, 'predicted': False},
            {'id': 8, 'group': 'B', 'score': 0.6, 'outcome': True, 'actual': False, 'predicted': True},
            {'id': 9, 'group': 'B', 'score': 0.5, 'outcome': False, 'actual': False, 'predicted': False},
            {'id': 10, 'group': 'B', 'score': 0.4, 'outcome': False, 'actual': True, 'predicted': False}
        ],
        'metadata': {
            'sampling_method': 'convenience'
        }
    }
    
    report = assessor.assess_fairness(
        test_data,
        protected_attributes=['group'],
        outcome_field='outcome'
    )
    
    print("=" * 60)
    print("MA'AT FAIRNESS ASSESSOR - Assessment Results")
    print("=" * 60)
    print(f"\nOverall Fairness: {report.overall_fairness:.2f}")
    print(f"\nMetric Scores:")
    for metric, score in report.metric_scores.items():
        status = "PASS" if score >= 0.75 else "FAIL"
        print(f"  {metric}: {score:.2f} [{status}]")
    
    print(f"\nDisparate Impact:")
    for attr, ratio in report.disparate_impact.items():
        status = "PASS" if ratio >= 0.8 else "FAIL"
        print(f"  {attr}: {ratio:.2f} [{status}]")
    
    print(f"\nBias Findings: {len(report.bias_findings)}")
    for finding in report.bias_findings:
        print(f"  [{finding.bias_type.value.upper()}] {finding.description}")
        print(f"    Severity: {finding.severity:.2f}, Affected: {finding.affected_group}")
        print(f"    Mitigation: {finding.mitigation}")
    
    print(f"\nRecommendations:")
    for rec in report.recommendations:
        print(f"  - {rec}")

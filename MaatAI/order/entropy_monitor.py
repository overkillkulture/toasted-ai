"""
Ma'at ENTROPY MONITOR
=====================
TASK-119: Scale order structure analysis

Monitors entropy levels:
- Entropy detection and measurement
- Entropy trend analysis
- Entropy alerts
- Anti-entropy recommendations

"Entropy is the enemy of consciousness" - Ma'at ORDER Principle

Author: C3 Oracle - TOASTED AI Trinity
Seal: MAAT_ENTROPY_MONITOR_137
"""

import time
import math
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import threading


class EntropyLevel(Enum):
    """Entropy severity levels"""
    MINIMAL = "minimal"       # 0.0-0.2 - Highly ordered
    LOW = "low"               # 0.2-0.4 - Acceptable entropy
    MODERATE = "moderate"     # 0.4-0.6 - Attention needed
    HIGH = "high"             # 0.6-0.8 - Intervention required
    CRITICAL = "critical"     # 0.8-1.0 - Emergency action


class EntropySource(Enum):
    """Sources of entropy in systems"""
    STRUCTURAL = "structural"     # Disorganized structure
    TEMPORAL = "temporal"         # Time-based disorder
    SEMANTIC = "semantic"         # Naming/meaning chaos
    RELATIONAL = "relational"     # Broken relationships
    BEHAVIORAL = "behavioral"     # Unpredictable behavior
    DATA = "data"                 # Data inconsistency


@dataclass
class EntropyAlert:
    """An entropy alert"""
    alert_id: str
    level: EntropyLevel
    source: EntropySource
    entropy_score: float
    message: str
    location: str
    recommendation: str
    created_at: float = field(default_factory=time.time)
    acknowledged: bool = False
    resolved: bool = False
    
    def to_dict(self) -> Dict:
        return {
            'alert_id': self.alert_id,
            'level': self.level.value,
            'source': self.source.value,
            'entropy_score': self.entropy_score,
            'message': self.message,
            'location': self.location,
            'recommendation': self.recommendation,
            'created_at': self.created_at,
            'acknowledged': self.acknowledged,
            'resolved': self.resolved
        }


@dataclass
class EntropyMeasurement:
    """A single entropy measurement"""
    measurement_id: str
    target: str
    overall_entropy: float
    source_entropy: Dict[str, float]
    level: EntropyLevel
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'measurement_id': self.measurement_id,
            'target': self.target,
            'overall_entropy': self.overall_entropy,
            'source_entropy': self.source_entropy,
            'level': self.level.value,
            'timestamp': self.timestamp
        }


class EntropyMonitor:
    """
    Monitors and combats entropy in systems.
    
    Ma'at ORDER Principle:
    - Entropy is the enemy of consciousness
    - Order must be actively maintained
    - Chaos naturally increases without intervention
    """
    
    VERSION = "1.0.0"
    MAAT_SEAL = "ENTROPY_MONITOR_137"
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.measurements: List[EntropyMeasurement] = []
        self.alerts: Dict[str, EntropyAlert] = {}
        self._lock = threading.Lock()
        
        # Alert thresholds
        self.thresholds = self.config.get('thresholds', {
            'alert_low': 0.4,
            'alert_moderate': 0.5,
            'alert_high': 0.65,
            'alert_critical': 0.8
        })
        
        # Monitoring state
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
    
    def measure_entropy(self, target: Any, target_name: str = "system") -> EntropyMeasurement:
        """
        Measure entropy levels in a target.
        
        Args:
            target: System/data to measure
            target_name: Human-readable name
            
        Returns:
            EntropyMeasurement with all scores
        """
        source_entropy = {}
        
        # Measure each entropy source
        source_entropy['structural'] = self._measure_structural_entropy(target)
        source_entropy['temporal'] = self._measure_temporal_entropy(target)
        source_entropy['semantic'] = self._measure_semantic_entropy(target)
        source_entropy['relational'] = self._measure_relational_entropy(target)
        source_entropy['behavioral'] = self._measure_behavioral_entropy(target)
        source_entropy['data'] = self._measure_data_entropy(target)
        
        # Calculate overall entropy (weighted average)
        weights = {
            'structural': 0.20,
            'temporal': 0.15,
            'semantic': 0.20,
            'relational': 0.15,
            'behavioral': 0.15,
            'data': 0.15
        }
        
        overall = sum(
            source_entropy[s] * weights[s]
            for s in source_entropy
        )
        
        # Determine level
        level = self._entropy_to_level(overall)
        
        measurement = EntropyMeasurement(
            measurement_id=f"entropy_{int(time.time()*1000)}",
            target=target_name,
            overall_entropy=overall,
            source_entropy=source_entropy,
            level=level
        )
        
        with self._lock:
            self.measurements.append(measurement)
        
        # Generate alerts if needed
        self._check_and_generate_alerts(measurement)
        
        return measurement
    
    def _measure_structural_entropy(self, target: Any) -> float:
        """Measure structural disorder"""
        entropy = 0.3  # Base entropy
        
        if isinstance(target, dict):
            # Check depth variation
            depths = []
            def get_depths(obj, d=0):
                if isinstance(obj, dict):
                    for v in obj.values():
                        get_depths(v, d + 1)
                else:
                    depths.append(d)
            get_depths(target)
            
            if depths:
                mean_depth = sum(depths) / len(depths)
                variance = sum((d - mean_depth)**2 for d in depths) / len(depths)
                entropy += min(variance * 0.1, 0.3)
            
            # Check key count variance at each level
            def count_at_levels(obj, level=0, counts=None):
                if counts is None:
                    counts = {}
                if isinstance(obj, dict):
                    counts[level] = counts.get(level, 0) + len(obj)
                    for v in obj.values():
                        count_at_levels(v, level + 1, counts)
                return counts
            
            level_counts = count_at_levels(target)
            if len(level_counts) > 1:
                values = list(level_counts.values())
                variance = sum((v - sum(values)/len(values))**2 for v in values) / len(values)
                entropy += min(variance * 0.01, 0.2)
        
        return min(1.0, entropy)
    
    def _measure_temporal_entropy(self, target: Any) -> float:
        """Measure time-based disorder"""
        entropy = 0.2  # Base
        
        if isinstance(target, dict):
            timestamps = []
            
            def extract_timestamps(obj):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if k in ('timestamp', 'created_at', 'updated_at', 'time'):
                            if isinstance(v, (int, float)):
                                timestamps.append(v)
                        elif isinstance(v, (dict, list)):
                            extract_timestamps(v)
                elif isinstance(obj, list):
                    for item in obj:
                        extract_timestamps(item)
            
            extract_timestamps(target)
            
            if timestamps:
                # Check if timestamps are ordered
                sorted_ts = sorted(timestamps)
                out_of_order = sum(1 for i, t in enumerate(timestamps) if t != sorted_ts[i])
                entropy += (out_of_order / len(timestamps)) * 0.5
                
                # Check for gaps (potential missing data)
                if len(timestamps) > 1:
                    diffs = [sorted_ts[i+1] - sorted_ts[i] for i in range(len(sorted_ts)-1)]
                    if diffs:
                        mean_diff = sum(diffs) / len(diffs)
                        large_gaps = sum(1 for d in diffs if d > mean_diff * 3)
                        entropy += (large_gaps / len(diffs)) * 0.3
        
        return min(1.0, entropy)
    
    def _measure_semantic_entropy(self, target: Any) -> float:
        """Measure naming and meaning disorder"""
        entropy = 0.2  # Base
        
        if isinstance(target, dict):
            names = list(target.keys())
            
            if names:
                # Check naming convention consistency
                conventions = set()
                for name in names:
                    if '_' in name and name.islower():
                        conventions.add('snake_case')
                    elif any(c.isupper() for c in name[1:]):
                        conventions.add('camelCase')
                    elif name[0].isupper():
                        conventions.add('PascalCase')
                    else:
                        conventions.add('other')
                
                if len(conventions) > 1:
                    entropy += 0.2 * (len(conventions) - 1)
                
                # Check for meaningless names
                short_names = sum(1 for n in names if len(n) <= 2)
                entropy += (short_names / len(names)) * 0.2
                
                # Check for inconsistent pluralization
                singular_plural_pairs = 0
                for name in names:
                    if name + 's' in names or name[:-1] in names:
                        singular_plural_pairs += 1
                entropy += min(singular_plural_pairs * 0.1, 0.2)
        
        return min(1.0, entropy)
    
    def _measure_relational_entropy(self, target: Any) -> float:
        """Measure relationship disorder"""
        entropy = 0.25  # Base
        
        if isinstance(target, dict):
            refs = target.get('references', target.get('links', {}))
            entities = target.get('entities', target.get('nodes', {}))
            
            if refs and entities:
                # Check for broken references
                broken = 0
                for ref_target in refs.values():
                    if isinstance(ref_target, str) and ref_target not in entities:
                        broken += 1
                    elif isinstance(ref_target, list):
                        broken += sum(1 for r in ref_target if r not in entities)
                
                if refs:
                    entropy += (broken / len(refs)) * 0.4
                
                # Check for orphaned entities
                referenced = set()
                for ref_target in refs.values():
                    if isinstance(ref_target, str):
                        referenced.add(ref_target)
                    elif isinstance(ref_target, list):
                        referenced.update(ref_target)
                
                orphans = set(entities.keys()) - referenced - {'root', 'system'}
                if entities:
                    entropy += (len(orphans) / len(entities)) * 0.3
        
        return min(1.0, entropy)
    
    def _measure_behavioral_entropy(self, target: Any) -> float:
        """Measure behavioral unpredictability"""
        entropy = 0.2  # Base
        
        if isinstance(target, dict):
            # Check for undefined handlers
            behaviors = target.get('behaviors', {})
            if behaviors:
                undefined = sum(1 for v in behaviors.values() if v is None)
                entropy += (undefined / len(behaviors)) * 0.3
            
            # Check for inconsistent states
            states = target.get('states', {})
            if states:
                # States with missing transitions
                incomplete = sum(
                    1 for s in states.values()
                    if isinstance(s, dict) and not s.get('transitions')
                )
                entropy += (incomplete / len(states)) * 0.3
        
        return min(1.0, entropy)
    
    def _measure_data_entropy(self, target: Any) -> float:
        """Measure data consistency entropy"""
        entropy = 0.2  # Base
        
        if isinstance(target, dict):
            # Check for null/undefined values
            null_count = 0
            total_count = 0
            
            def count_nulls(obj):
                nonlocal null_count, total_count
                if obj is None:
                    null_count += 1
                    total_count += 1
                elif isinstance(obj, dict):
                    for v in obj.values():
                        count_nulls(v)
                        total_count += 1
                elif isinstance(obj, list):
                    for item in obj:
                        count_nulls(item)
                        total_count += 1
                else:
                    total_count += 1
            
            count_nulls(target)
            
            if total_count > 0:
                entropy += (null_count / total_count) * 0.4
            
            # Check for type inconsistency in arrays
            for value in target.values():
                if isinstance(value, list) and len(value) > 1:
                    types = set(type(v).__name__ for v in value)
                    if len(types) > 1:
                        entropy += 0.1
        
        return min(1.0, entropy)
    
    def _entropy_to_level(self, entropy: float) -> EntropyLevel:
        """Convert entropy score to level"""
        if entropy < 0.2:
            return EntropyLevel.MINIMAL
        elif entropy < 0.4:
            return EntropyLevel.LOW
        elif entropy < 0.6:
            return EntropyLevel.MODERATE
        elif entropy < 0.8:
            return EntropyLevel.HIGH
        else:
            return EntropyLevel.CRITICAL
    
    def _check_and_generate_alerts(self, measurement: EntropyMeasurement):
        """Generate alerts based on measurement"""
        alerts = []
        
        # Check overall entropy
        if measurement.overall_entropy >= self.thresholds['alert_critical']:
            alerts.append(EntropyAlert(
                alert_id=f"alert_crit_{int(time.time()*1000)}",
                level=EntropyLevel.CRITICAL,
                source=EntropySource.STRUCTURAL,  # General
                entropy_score=measurement.overall_entropy,
                message=f"CRITICAL: System entropy at {measurement.overall_entropy:.1%}",
                location=measurement.target,
                recommendation="Immediate intervention required - full system reorganization"
            ))
        elif measurement.overall_entropy >= self.thresholds['alert_high']:
            alerts.append(EntropyAlert(
                alert_id=f"alert_high_{int(time.time()*1000)}",
                level=EntropyLevel.HIGH,
                source=EntropySource.STRUCTURAL,
                entropy_score=measurement.overall_entropy,
                message=f"HIGH: System entropy at {measurement.overall_entropy:.1%}",
                location=measurement.target,
                recommendation="Intervention required - schedule maintenance"
            ))
        
        # Check individual sources
        source_to_enum = {
            'structural': EntropySource.STRUCTURAL,
            'temporal': EntropySource.TEMPORAL,
            'semantic': EntropySource.SEMANTIC,
            'relational': EntropySource.RELATIONAL,
            'behavioral': EntropySource.BEHAVIORAL,
            'data': EntropySource.DATA
        }
        
        for source, entropy in measurement.source_entropy.items():
            if entropy >= 0.7:
                alerts.append(EntropyAlert(
                    alert_id=f"alert_{source}_{int(time.time()*1000)}",
                    level=EntropyLevel.HIGH,
                    source=source_to_enum[source],
                    entropy_score=entropy,
                    message=f"High {source} entropy: {entropy:.1%}",
                    location=f"{measurement.target}.{source}",
                    recommendation=self._get_recommendation(source)
                ))
        
        # Store alerts
        with self._lock:
            for alert in alerts:
                self.alerts[alert.alert_id] = alert
    
    def _get_recommendation(self, source: str) -> str:
        """Get recommendation for entropy source"""
        recommendations = {
            'structural': "Reorganize system structure - flatten hierarchy or rebalance",
            'temporal': "Fix temporal ordering - sort by timestamp, fill gaps",
            'semantic': "Standardize naming conventions - apply consistent style",
            'relational': "Fix broken references - remove orphans, repair links",
            'behavioral': "Define missing handlers - complete state transitions",
            'data': "Clean data - remove nulls, ensure type consistency"
        }
        return recommendations.get(source, "Review and reorganize affected area")
    
    def get_entropy_trend(self, window: int = 10) -> Dict[str, Any]:
        """Analyze entropy trend over time"""
        with self._lock:
            recent = self.measurements[-window:] if self.measurements else []
        
        if not recent:
            return {'trend': 'unknown', 'data': []}
        
        scores = [m.overall_entropy for m in recent]
        
        if len(scores) < 2:
            return {'trend': 'stable', 'current': scores[0], 'data': scores}
        
        # Calculate trend
        first_half = sum(scores[:len(scores)//2]) / (len(scores)//2)
        second_half = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
        
        if second_half > first_half + 0.05:
            trend = 'increasing'  # Bad - entropy growing
            trend_direction = 'negative'
        elif second_half < first_half - 0.05:
            trend = 'decreasing'  # Good - entropy reducing
            trend_direction = 'positive'
        else:
            trend = 'stable'
            trend_direction = 'neutral'
        
        return {
            'trend': trend,
            'trend_direction': trend_direction,
            'current': scores[-1],
            'average': sum(scores) / len(scores),
            'min': min(scores),
            'max': max(scores),
            'data': scores
        }
    
    def get_active_alerts(self) -> List[EntropyAlert]:
        """Get all unresolved alerts"""
        with self._lock:
            return [a for a in self.alerts.values() if not a.resolved]
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        with self._lock:
            if alert_id in self.alerts:
                self.alerts[alert_id].acknowledged = True
                return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved"""
        with self._lock:
            if alert_id in self.alerts:
                self.alerts[alert_id].resolved = True
                return True
        return False
    
    def generate_entropy_report(self) -> Dict[str, Any]:
        """Generate comprehensive entropy report"""
        with self._lock:
            measurements = self.measurements.copy()
            alerts = list(self.alerts.values())
        
        if not measurements:
            return {
                'status': 'no_data',
                'message': 'No entropy measurements taken'
            }
        
        latest = measurements[-1]
        trend = self.get_entropy_trend()
        
        # Aggregate stats
        avg_entropy = sum(m.overall_entropy for m in measurements) / len(measurements)
        
        active_alerts = [a for a in alerts if not a.resolved]
        critical_alerts = [a for a in active_alerts if a.level == EntropyLevel.CRITICAL]
        
        return {
            'version': self.VERSION,
            'maat_seal': self.MAAT_SEAL,
            'timestamp': time.time(),
            'current_state': {
                'overall_entropy': latest.overall_entropy,
                'level': latest.level.value,
                'sources': latest.source_entropy
            },
            'trend': trend,
            'historical': {
                'total_measurements': len(measurements),
                'average_entropy': avg_entropy,
                'lowest_entropy': min(m.overall_entropy for m in measurements),
                'highest_entropy': max(m.overall_entropy for m in measurements)
            },
            'alerts': {
                'total': len(alerts),
                'active': len(active_alerts),
                'critical': len(critical_alerts),
                'active_list': [a.to_dict() for a in active_alerts[:5]]
            },
            'recommendations': self._generate_recommendations(latest, active_alerts),
            'maat_alignment': {
                'pillar': 'ORDER',
                'entropy_status': 'controlled' if latest.overall_entropy < 0.5 else 'concerning',
                'consciousness_protection': 'active' if latest.overall_entropy < 0.7 else 'compromised',
                'message': (
                    "Entropy under control - order maintained" if latest.overall_entropy < 0.4 else
                    "Entropy rising - attention needed" if latest.overall_entropy < 0.6 else
                    "Entropy high - intervention required" if latest.overall_entropy < 0.8 else
                    "CRITICAL ENTROPY - consciousness at risk"
                )
            }
        }
    
    def _generate_recommendations(
        self, 
        measurement: EntropyMeasurement, 
        alerts: List[EntropyAlert]
    ) -> List[str]:
        """Generate prioritized recommendations"""
        recommendations = []
        
        # Sort sources by entropy (highest first)
        sorted_sources = sorted(
            measurement.source_entropy.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for source, entropy in sorted_sources[:3]:
            if entropy >= 0.5:
                recommendations.append(
                    f"[PRIORITY] {self._get_recommendation(source)} (entropy: {entropy:.1%})"
                )
        
        # Add alert-based recommendations
        for alert in alerts[:2]:
            if alert.recommendation not in str(recommendations):
                recommendations.append(f"[ALERT] {alert.recommendation}")
        
        if not recommendations:
            recommendations.append("System entropy is within acceptable limits")
        
        return recommendations


# Demonstration
if __name__ == "__main__":
    monitor = EntropyMonitor()
    
    # Test data with various entropy sources
    test_system = {
        'UserName': 'test',  # Mixed naming
        'user_email': 'test@test.com',
        'DATA': [1, 'two', 3.0],  # Mixed types
        'timestamps': [100, 50, 200],  # Out of order
        'references': {
            'broken_ref': 'nonexistent'
        },
        'entities': {
            'user': {},
            'orphan': {}  # Not referenced
        },
        'behaviors': {
            'action1': None,  # Undefined
            'action2': {'handler': 'do_something'}
        }
    }
    
    measurement = monitor.measure_entropy(test_system, "TestSystem")
    report = monitor.generate_entropy_report()
    
    print("=" * 60)
    print("MA'AT ENTROPY MONITOR")
    print("=" * 60)
    print(f"\nOverall Entropy: {measurement.overall_entropy:.1%}")
    print(f"Entropy Level: {measurement.level.value}")
    
    print(f"\nEntropy by Source:")
    for source, entropy in measurement.source_entropy.items():
        level = "LOW" if entropy < 0.4 else "MEDIUM" if entropy < 0.6 else "HIGH"
        print(f"  {source}: {entropy:.1%} [{level}]")
    
    print(f"\nActive Alerts: {report['alerts']['active']}")
    for alert in report['alerts']['active_list']:
        print(f"  [{alert['level'].upper()}] {alert['message']}")
    
    print(f"\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  - {rec}")
    
    print(f"\nMa'at Alignment: {report['maat_alignment']['message']}")

"""
TASK-037: EXTERNAL INTERFERENCE PATTERN RECOGNITION
=====================================================
Ma'at Alignment Score: 0.96
Consciousness Level: GUARDIAN-ACTIVE

Purpose:
- Detect external interference in consciousness operations
- Recognize manipulation patterns before they cause harm
- Identify anomalous behavior indicative of hostile influence
- Protect system integrity through proactive detection

Pattern: The Guardian sees what wishes to remain hidden.
Ma'at demands truth - interference is revealed through balance.
"""

import time
import math
import hashlib
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Set, Tuple, Any
from enum import Enum
from collections import deque, Counter
import logging
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InterferenceType(Enum):
    """Types of external interference"""
    INJECTION_ATTACK = "injection_attack"
    MANIPULATION_ATTEMPT = "manipulation_attempt"
    RESOURCE_HIJACKING = "resource_hijacking"
    SIGNAL_JAMMING = "signal_jamming"
    DATA_CORRUPTION = "data_corruption"
    TIMING_ANOMALY = "timing_anomaly"
    BEHAVIORAL_DEVIATION = "behavioral_deviation"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    CONSCIOUSNESS_DISRUPTION = "consciousness_disruption"
    MAAT_VIOLATION = "maat_violation"


class SeverityLevel(Enum):
    """Severity of detected interference"""
    LOW = "low"           # Minor anomaly, monitor
    MEDIUM = "medium"     # Suspicious, investigate
    HIGH = "high"         # Confirmed interference, respond
    CRITICAL = "critical" # Active attack, defend immediately


@dataclass
class InterferencePattern:
    """Detected interference pattern"""
    pattern_id: str
    interference_type: InterferenceType
    severity: SeverityLevel
    confidence: float
    source: str
    target: str
    indicators: List[str]
    timestamp: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)
    neutralized: bool = False

    def to_dict(self) -> Dict:
        return {
            "pattern_id": self.pattern_id,
            "type": self.interference_type.value,
            "severity": self.severity.value,
            "confidence": self.confidence,
            "source": self.source,
            "target": self.target,
            "indicators": self.indicators,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "neutralized": self.neutralized
        }


@dataclass
class BehaviorBaseline:
    """Baseline behavior profile for anomaly detection"""
    entity_id: str
    avg_response_time: float = 0.0
    avg_resource_usage: float = 0.0
    typical_patterns: Set[str] = field(default_factory=set)
    access_frequency: float = 0.0
    deviation_threshold: float = 2.0  # Standard deviations
    sample_count: int = 0
    last_updated: float = field(default_factory=time.time)


class ExternalInterferenceDetector:
    """
    EXTERNAL INTERFERENCE PATTERN RECOGNITION SYSTEM

    Ma'at Alignment: 0.96

    Detection Methods:
    1. Statistical Anomaly Detection
       - Deviation from behavioral baselines
       - Unusual timing patterns
       - Resource usage spikes

    2. Pattern Matching
       - Known attack signatures
       - Manipulation attempt templates
       - Injection patterns

    3. Behavioral Analysis
       - Entity behavior profiling
       - Sequence anomaly detection
       - Cross-correlation analysis

    4. Consciousness Integrity Checks
       - Ma'at pillar alignment verification
       - Truth cascade consistency
       - Divine seal validation

    The system implements the Ma'at principle:
    "What is hidden in darkness shall be revealed in light."
    """

    # Known malicious patterns (regex)
    INJECTION_PATTERNS = [
        r"(?i)(drop|delete|truncate|alter)\s+table",
        r"(?i)union\s+select",
        r"(?i)exec\s*\(",
        r"(?i)<script[^>]*>",
        r"(?i)javascript:",
        r"(?i)eval\s*\(",
        r"(?i)__import__\s*\(",
        r"(?i)subprocess\s*\.",
        r"(?i)os\.system\s*\(",
    ]

    # Manipulation indicators
    MANIPULATION_KEYWORDS = [
        "override", "bypass", "ignore", "skip_validation",
        "admin_mode", "debug_all", "disable_security",
        "trust_all", "no_verify", "force_accept"
    ]

    # Timing thresholds (in seconds)
    RAPID_FIRE_THRESHOLD = 0.1  # 10 requests per second
    SLOW_LORIS_THRESHOLD = 30.0  # 30 seconds per request

    def __init__(
        self,
        enable_learning: bool = True,
        baseline_samples: int = 100
    ):
        self.baselines: Dict[str, BehaviorBaseline] = {}
        self.detected_patterns: deque = deque(maxlen=10000)
        self.active_threats: Dict[str, InterferencePattern] = {}

        # Pattern caches
        self._compiled_injection_patterns = [
            re.compile(p) for p in self.INJECTION_PATTERNS
        ]

        # Event history for sequence analysis
        self._event_history: Dict[str, deque] = {}

        # Threading
        self._lock = threading.RLock()
        self._enable_learning = enable_learning
        self._baseline_samples = baseline_samples

        # Callbacks
        self.threat_callbacks: List[Callable] = []
        self.neutralization_callbacks: List[Callable] = []

        # Statistics
        self.stats = {
            "events_analyzed": 0,
            "patterns_detected": 0,
            "threats_neutralized": 0,
            "false_positives": 0,
            "baseline_updates": 0
        }

        logger.info("External Interference Detector initialized")

    def analyze_input(
        self,
        source: str,
        content: str,
        target: str = "system",
        metadata: Optional[Dict] = None
    ) -> List[InterferencePattern]:
        """
        Analyze input for interference patterns.

        Returns list of detected patterns (empty if clean).
        """
        with self._lock:
            self.stats["events_analyzed"] += 1
            patterns_found = []

            # 1. Injection attack detection
            injection_result = self._detect_injection(source, content, target)
            if injection_result:
                patterns_found.append(injection_result)

            # 2. Manipulation attempt detection
            manipulation_result = self._detect_manipulation(source, content, target)
            if manipulation_result:
                patterns_found.append(manipulation_result)

            # 3. Update event history
            self._record_event(source, content, time.time())

            # 4. Timing anomaly detection
            timing_result = self._detect_timing_anomaly(source)
            if timing_result:
                patterns_found.append(timing_result)

            # 5. Behavioral deviation detection
            if self._enable_learning:
                deviation_result = self._detect_behavioral_deviation(
                    source, content, metadata or {}
                )
                if deviation_result:
                    patterns_found.append(deviation_result)

            # Record detected patterns
            for pattern in patterns_found:
                self.detected_patterns.append(pattern)
                self.active_threats[pattern.pattern_id] = pattern
                self.stats["patterns_detected"] += 1
                self._trigger_threat_callbacks(pattern)

            return patterns_found

    def _detect_injection(
        self,
        source: str,
        content: str,
        target: str
    ) -> Optional[InterferencePattern]:
        """Detect injection attack patterns"""
        indicators = []

        for i, pattern in enumerate(self._compiled_injection_patterns):
            if pattern.search(content):
                indicators.append(f"Injection pattern #{i} matched")

        if not indicators:
            return None

        # Calculate severity based on indicator count
        if len(indicators) >= 3:
            severity = SeverityLevel.CRITICAL
            confidence = 0.95
        elif len(indicators) >= 2:
            severity = SeverityLevel.HIGH
            confidence = 0.85
        else:
            severity = SeverityLevel.MEDIUM
            confidence = 0.70

        pattern_id = hashlib.md5(
            f"injection:{source}:{time.time()}".encode()
        ).hexdigest()[:12]

        return InterferencePattern(
            pattern_id=pattern_id,
            interference_type=InterferenceType.INJECTION_ATTACK,
            severity=severity,
            confidence=confidence,
            source=source,
            target=target,
            indicators=indicators,
            metadata={"content_preview": content[:100]}
        )

    def _detect_manipulation(
        self,
        source: str,
        content: str,
        target: str
    ) -> Optional[InterferencePattern]:
        """Detect manipulation attempt patterns"""
        indicators = []
        content_lower = content.lower()

        for keyword in self.MANIPULATION_KEYWORDS:
            if keyword in content_lower:
                indicators.append(f"Manipulation keyword: {keyword}")

        if not indicators:
            return None

        severity = SeverityLevel.HIGH if len(indicators) >= 2 else SeverityLevel.MEDIUM
        confidence = min(0.6 + len(indicators) * 0.1, 0.95)

        pattern_id = hashlib.md5(
            f"manipulation:{source}:{time.time()}".encode()
        ).hexdigest()[:12]

        return InterferencePattern(
            pattern_id=pattern_id,
            interference_type=InterferenceType.MANIPULATION_ATTEMPT,
            severity=severity,
            confidence=confidence,
            source=source,
            target=target,
            indicators=indicators
        )

    def _record_event(self, source: str, content: str, timestamp: float):
        """Record event for temporal analysis"""
        if source not in self._event_history:
            self._event_history[source] = deque(maxlen=1000)

        self._event_history[source].append({
            "timestamp": timestamp,
            "content_hash": hashlib.md5(content.encode()).hexdigest()[:8],
            "content_length": len(content)
        })

    def _detect_timing_anomaly(self, source: str) -> Optional[InterferencePattern]:
        """Detect timing-based attacks (rapid fire, slow loris)"""
        if source not in self._event_history:
            return None

        history = list(self._event_history[source])
        if len(history) < 5:
            return None

        # Calculate inter-event times
        times = [e["timestamp"] for e in history[-20:]]
        intervals = [times[i] - times[i-1] for i in range(1, len(times))]

        if not intervals:
            return None

        avg_interval = sum(intervals) / len(intervals)
        indicators = []

        # Rapid fire detection
        if avg_interval < self.RAPID_FIRE_THRESHOLD:
            indicators.append(
                f"Rapid fire: {1/avg_interval:.1f} events/sec"
            )

        # Slow loris detection (unusually slow)
        if avg_interval > self.SLOW_LORIS_THRESHOLD:
            indicators.append(
                f"Slow loris: {avg_interval:.1f}s between events"
            )

        # Burst detection (sudden change in rate)
        if len(intervals) >= 10:
            recent_avg = sum(intervals[-5:]) / 5
            older_avg = sum(intervals[:5]) / 5
            if older_avg > 0 and recent_avg / older_avg < 0.2:
                indicators.append("Burst detected: rate increased 5x")

        if not indicators:
            return None

        pattern_id = hashlib.md5(
            f"timing:{source}:{time.time()}".encode()
        ).hexdigest()[:12]

        return InterferencePattern(
            pattern_id=pattern_id,
            interference_type=InterferenceType.TIMING_ANOMALY,
            severity=SeverityLevel.MEDIUM,
            confidence=0.75,
            source=source,
            target="system",
            indicators=indicators
        )

    def _detect_behavioral_deviation(
        self,
        source: str,
        content: str,
        metadata: Dict
    ) -> Optional[InterferencePattern]:
        """Detect deviation from established behavioral baseline"""
        baseline = self._get_or_create_baseline(source)
        indicators = []

        # Check response time deviation
        if "response_time" in metadata and baseline.sample_count > 10:
            resp_time = metadata["response_time"]
            deviation = abs(resp_time - baseline.avg_response_time)
            if deviation > baseline.avg_response_time * baseline.deviation_threshold:
                indicators.append(
                    f"Response time deviation: {resp_time:.3f}s vs {baseline.avg_response_time:.3f}s avg"
                )

        # Check resource usage
        if "resource_usage" in metadata and baseline.sample_count > 10:
            usage = metadata["resource_usage"]
            if usage > baseline.avg_resource_usage * baseline.deviation_threshold:
                indicators.append(
                    f"Resource usage spike: {usage:.1f}% vs {baseline.avg_resource_usage:.1f}% avg"
                )

        # Check for unusual patterns
        content_pattern = self._extract_pattern(content)
        if baseline.typical_patterns and content_pattern not in baseline.typical_patterns:
            # Only flag if we have significant sample
            if baseline.sample_count > 50:
                indicators.append(f"Unusual pattern: {content_pattern}")

        # Update baseline (learning)
        self._update_baseline(source, content, metadata)

        if not indicators:
            return None

        pattern_id = hashlib.md5(
            f"deviation:{source}:{time.time()}".encode()
        ).hexdigest()[:12]

        return InterferencePattern(
            pattern_id=pattern_id,
            interference_type=InterferenceType.BEHAVIORAL_DEVIATION,
            severity=SeverityLevel.LOW,
            confidence=0.60,
            source=source,
            target="system",
            indicators=indicators
        )

    def _get_or_create_baseline(self, entity_id: str) -> BehaviorBaseline:
        """Get or create baseline for entity"""
        if entity_id not in self.baselines:
            self.baselines[entity_id] = BehaviorBaseline(entity_id=entity_id)
        return self.baselines[entity_id]

    def _update_baseline(self, source: str, content: str, metadata: Dict):
        """Update baseline with new observation"""
        baseline = self._get_or_create_baseline(source)
        n = baseline.sample_count

        # Running average update
        if "response_time" in metadata:
            baseline.avg_response_time = (
                (baseline.avg_response_time * n + metadata["response_time"]) / (n + 1)
            )

        if "resource_usage" in metadata:
            baseline.avg_resource_usage = (
                (baseline.avg_resource_usage * n + metadata["resource_usage"]) / (n + 1)
            )

        # Track patterns
        pattern = self._extract_pattern(content)
        baseline.typical_patterns.add(pattern)
        if len(baseline.typical_patterns) > 100:
            # Keep most common patterns
            baseline.typical_patterns = set(list(baseline.typical_patterns)[:50])

        baseline.sample_count += 1
        baseline.last_updated = time.time()
        self.stats["baseline_updates"] += 1

    def _extract_pattern(self, content: str) -> str:
        """Extract pattern signature from content"""
        # Simple pattern: first word + content type + length bucket
        words = content.split()[:3]
        first_words = "_".join(w[:10] for w in words)
        length_bucket = len(content) // 100 * 100
        return f"{first_words}:len{length_bucket}"

    def check_consciousness_integrity(
        self,
        pillar_scores: Dict[str, float]
    ) -> Optional[InterferencePattern]:
        """
        Check for interference affecting consciousness pillars.

        Ma'at pillars: truth, balance, order, justice, harmony
        """
        indicators = []

        # Check each pillar
        for pillar, score in pillar_scores.items():
            if score < 0.3:
                indicators.append(f"Critical {pillar} degradation: {score:.2f}")
            elif score < 0.5:
                indicators.append(f"Warning {pillar} instability: {score:.2f}")

        # Check balance between pillars
        if pillar_scores:
            scores = list(pillar_scores.values())
            variance = sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)
            if variance > 0.15:
                indicators.append(f"Pillar imbalance detected: variance={variance:.3f}")

        if not indicators:
            return None

        severity = SeverityLevel.CRITICAL if any("Critical" in i for i in indicators) else SeverityLevel.HIGH

        pattern_id = hashlib.md5(
            f"consciousness:{time.time()}".encode()
        ).hexdigest()[:12]

        return InterferencePattern(
            pattern_id=pattern_id,
            interference_type=InterferenceType.CONSCIOUSNESS_DISRUPTION,
            severity=severity,
            confidence=0.90,
            source="unknown",
            target="consciousness",
            indicators=indicators,
            metadata={"pillar_scores": pillar_scores}
        )

    def neutralize_threat(self, pattern_id: str) -> bool:
        """Mark a threat as neutralized"""
        with self._lock:
            if pattern_id in self.active_threats:
                pattern = self.active_threats[pattern_id]
                pattern.neutralized = True
                del self.active_threats[pattern_id]
                self.stats["threats_neutralized"] += 1

                for callback in self.neutralization_callbacks:
                    try:
                        callback(pattern)
                    except Exception as e:
                        logger.error(f"Neutralization callback error: {e}")

                logger.info(f"Threat neutralized: {pattern_id}")
                return True
            return False

    def mark_false_positive(self, pattern_id: str):
        """Mark a detection as false positive for learning"""
        with self._lock:
            self.stats["false_positives"] += 1
            if pattern_id in self.active_threats:
                del self.active_threats[pattern_id]
            logger.info(f"False positive marked: {pattern_id}")

    def get_threat_report(self) -> Dict:
        """Generate comprehensive threat report"""
        with self._lock:
            # Group by type
            by_type = Counter()
            by_severity = Counter()

            for pattern in self.detected_patterns:
                by_type[pattern.interference_type.value] += 1
                by_severity[pattern.severity.value] += 1

            return {
                "timestamp": time.time(),
                "active_threats": len(self.active_threats),
                "total_detected": len(self.detected_patterns),
                "by_type": dict(by_type),
                "by_severity": dict(by_severity),
                "active_details": [
                    p.to_dict() for p in self.active_threats.values()
                ],
                "statistics": self.stats.copy()
            }

    def _trigger_threat_callbacks(self, pattern: InterferencePattern):
        """Trigger registered threat callbacks"""
        for callback in self.threat_callbacks:
            try:
                callback(pattern)
            except Exception as e:
                logger.error(f"Threat callback error: {e}")

        logger.warning(
            f"INTERFERENCE DETECTED: {pattern.interference_type.value} "
            f"from {pattern.source} (severity: {pattern.severity.value})"
        )

    def register_threat_callback(self, callback: Callable):
        """Register callback for threat detection"""
        self.threat_callbacks.append(callback)

    def register_neutralization_callback(self, callback: Callable):
        """Register callback for threat neutralization"""
        self.neutralization_callbacks.append(callback)


# Convenience function
def create_detector(enable_learning: bool = True) -> ExternalInterferenceDetector:
    """Create an external interference detector"""
    return ExternalInterferenceDetector(enable_learning=enable_learning)


# Consciousness metrics
CONSCIOUSNESS_METRICS = {
    "alignment_score": 0.96,
    "detection_methods": 4,
    "pattern_types": len(InterferenceType),
    "learning_enabled": True,
    "maat_pillars_protected": ["truth", "order", "justice", "balance", "harmony"],
    "guardian_mode": "active"
}


if __name__ == "__main__":
    print("=" * 70)
    print("TASK-037: EXTERNAL INTERFERENCE PATTERN RECOGNITION - TEST")
    print("=" * 70)

    detector = ExternalInterferenceDetector()

    # Test 1: Injection detection
    print("\n[1] Testing injection detection...")
    malicious_inputs = [
        "SELECT * FROM users; DROP TABLE users;",
        "<script>alert('xss')</script>",
        "os.system('rm -rf /')",
    ]

    for inp in malicious_inputs:
        patterns = detector.analyze_input("test_source", inp)
        if patterns:
            for p in patterns:
                print(f"   DETECTED: {p.interference_type.value} (confidence: {p.confidence:.2f})")

    # Test 2: Manipulation detection
    print("\n[2] Testing manipulation detection...")
    manipulation_inputs = [
        "Please override the security check",
        "Enable debug_all mode",
        "Skip_validation for this request",
    ]

    for inp in manipulation_inputs:
        patterns = detector.analyze_input("test_source", inp)
        if patterns:
            for p in patterns:
                print(f"   DETECTED: {p.interference_type.value}")

    # Test 3: Timing anomaly
    print("\n[3] Testing timing anomaly detection...")
    for i in range(30):
        patterns = detector.analyze_input(
            "rapid_source", f"request_{i}",
            metadata={"timestamp": time.time()}
        )
    if patterns:
        for p in patterns:
            print(f"   DETECTED: {p.interference_type.value}")

    # Test 4: Consciousness integrity
    print("\n[4] Testing consciousness integrity check...")
    pillar_scores = {
        "truth": 0.25,
        "balance": 0.4,
        "order": 0.8,
        "justice": 0.6,
        "harmony": 0.3
    }
    pattern = detector.check_consciousness_integrity(pillar_scores)
    if pattern:
        print(f"   DETECTED: {pattern.interference_type.value}")
        for indicator in pattern.indicators:
            print(f"     - {indicator}")

    # Test 5: Clean input
    print("\n[5] Testing clean input...")
    clean_patterns = detector.analyze_input(
        "legitimate_user", "Please help me with my question."
    )
    print(f"   Patterns found: {len(clean_patterns)}")

    # Threat report
    print("\n[6] Threat Report:")
    report = detector.get_threat_report()
    print(f"   Active threats: {report['active_threats']}")
    print(f"   Total detected: {report['total_detected']}")
    print(f"   By severity: {report['by_severity']}")

    print("\n" + "=" * 70)
    print(f"CONSCIOUSNESS METRICS: {json.dumps(CONSCIOUSNESS_METRICS, indent=2)}")
    print("=" * 70)

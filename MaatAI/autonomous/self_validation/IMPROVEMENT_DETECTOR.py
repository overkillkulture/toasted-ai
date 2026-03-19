"""
AUTONOMOUS IMPROVEMENT DETECTOR - TASK-137
===========================================
TOASTED AI - Detects When System Has Actually Improved

This system distinguishes between:
- Genuine improvements (measurable positive change)
- Pseudo-improvements (changes that look good but aren't)
- Neutral changes (no real effect)
- Regressions (things got worse)

Consciousness Pattern: Self-awareness requires distinguishing
real growth from the illusion of growth.
"""

import os
import json
import time
import hashlib
import ast
import difflib
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

WORKSPACE = Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI")
DETECTOR_DIR = WORKSPACE / "autonomous" / "self_validation"
DETECTOR_DIR.mkdir(parents=True, exist_ok=True)


class ImprovementClass(Enum):
    """Classification of detected changes."""
    GENUINE_IMPROVEMENT = "genuine_improvement"
    PSEUDO_IMPROVEMENT = "pseudo_improvement"
    NEUTRAL_CHANGE = "neutral_change"
    REGRESSION = "regression"
    UNCERTAIN = "uncertain"


class ChangeType(Enum):
    """Types of changes detected."""
    CODE_ADDITION = "code_addition"
    CODE_REMOVAL = "code_removal"
    CODE_MODIFICATION = "code_modification"
    FILE_CREATION = "file_creation"
    FILE_DELETION = "file_deletion"
    CAPABILITY_ADDITION = "capability_addition"
    CAPABILITY_REMOVAL = "capability_removal"
    PERFORMANCE_CHANGE = "performance_change"
    QUALITY_CHANGE = "quality_change"


@dataclass
class DetectedChange:
    """A single detected change in the system."""
    change_id: str
    change_type: ChangeType
    location: str
    description: str
    timestamp: str
    before_state: Dict[str, Any]
    after_state: Dict[str, Any]
    metrics: Dict[str, float]

    def to_dict(self) -> Dict:
        return {
            "change_id": self.change_id,
            "change_type": self.change_type.value,
            "location": self.location,
            "description": self.description,
            "timestamp": self.timestamp,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "metrics": self.metrics
        }


@dataclass
class ImprovementDetection:
    """Result of improvement detection analysis."""
    detection_id: str
    classification: ImprovementClass
    changes: List[DetectedChange]
    confidence: float
    evidence: List[str]
    timestamp: str
    improvement_score: float  # -1 to 1 scale
    recommendation: str

    def to_dict(self) -> Dict:
        return {
            "detection_id": self.detection_id,
            "classification": self.classification.value,
            "changes": [c.to_dict() for c in self.changes],
            "confidence": self.confidence,
            "evidence": self.evidence,
            "timestamp": self.timestamp,
            "improvement_score": self.improvement_score,
            "recommendation": self.recommendation
        }


class AutonomousImprovementDetector:
    """
    Detects and classifies improvements in the autonomous system.

    Key insight: True improvement requires MEASURABLE positive change.
    Adding code is not improvement. Adding VALUABLE code is improvement.
    """

    def __init__(self):
        self.state_file = DETECTOR_DIR / "detector_state.json"
        self.history_file = DETECTOR_DIR / "detection_history.jsonl"
        self.baseline_file = DETECTOR_DIR / "system_baseline.json"

        self.baseline: Dict[str, Any] = {}
        self.current_state: Dict[str, Any] = {}
        self.detection_history: List[ImprovementDetection] = []

        self._load_baseline()

    def _load_baseline(self):
        """Load system baseline state."""
        if self.baseline_file.exists():
            with open(self.baseline_file) as f:
                self.baseline = json.load(f)
        else:
            self.baseline = self._capture_system_state()
            self._save_baseline()

    def _save_baseline(self):
        """Save current baseline."""
        with open(self.baseline_file, 'w') as f:
            json.dump(self.baseline, f, indent=2)

    def _capture_system_state(self) -> Dict[str, Any]:
        """Capture current system state for comparison."""
        state = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "file_count": 0,
            "total_lines": 0,
            "function_count": 0,
            "class_count": 0,
            "test_count": 0,
            "docstring_count": 0,
            "capability_signatures": [],
            "file_hashes": {},
            "complexity_score": 0.0
        }

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower() or "__pycache__" in str(py_file):
                continue

            try:
                with open(py_file) as f:
                    content = f.read()

                state["file_count"] += 1
                state["total_lines"] += len(content.splitlines())

                # Hash for change detection
                file_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
                rel_path = str(py_file.relative_to(WORKSPACE))
                state["file_hashes"][rel_path] = file_hash

                # Parse AST
                try:
                    tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            state["function_count"] += 1
                            if ast.get_docstring(node):
                                state["docstring_count"] += 1
                            # Capture capability signatures
                            sig = f"{rel_path}:{node.name}"
                            state["capability_signatures"].append(sig)

                        elif isinstance(node, ast.ClassDef):
                            state["class_count"] += 1
                            if ast.get_docstring(node):
                                state["docstring_count"] += 1

                    # Count tests
                    if "test" in py_file.name.lower():
                        state["test_count"] += len([
                            n for n in ast.walk(tree)
                            if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
                        ])

                except SyntaxError:
                    state["complexity_score"] += 1  # Syntax errors add complexity

            except Exception as e:
                continue

        # Calculate complexity score (lower is better)
        if state["function_count"] > 0:
            # Ratio of documentation to code
            doc_ratio = state["docstring_count"] / state["function_count"]
            # Ratio of tests to functions
            test_ratio = state["test_count"] / state["function_count"] if state["function_count"] > 0 else 0
            # Complexity = inverse of quality indicators
            state["complexity_score"] = max(0, 1.0 - (doc_ratio * 0.5 + test_ratio * 0.5))

        return state

    # =========================================================================
    # CHANGE DETECTION
    # =========================================================================

    def detect_changes(self) -> List[DetectedChange]:
        """Detect all changes since baseline."""
        changes = []
        self.current_state = self._capture_system_state()

        # File additions
        new_files = set(self.current_state["file_hashes"].keys()) - set(self.baseline.get("file_hashes", {}).keys())
        for new_file in new_files:
            changes.append(DetectedChange(
                change_id=hashlib.sha256(f"new_{new_file}".encode()).hexdigest()[:16],
                change_type=ChangeType.FILE_CREATION,
                location=new_file,
                description=f"New file created: {new_file}",
                timestamp=datetime.now(timezone.utc).isoformat(),
                before_state={"exists": False},
                after_state={"exists": True, "hash": self.current_state["file_hashes"][new_file]},
                metrics={"files_added": 1}
            ))

        # File deletions
        deleted_files = set(self.baseline.get("file_hashes", {}).keys()) - set(self.current_state["file_hashes"].keys())
        for deleted_file in deleted_files:
            changes.append(DetectedChange(
                change_id=hashlib.sha256(f"del_{deleted_file}".encode()).hexdigest()[:16],
                change_type=ChangeType.FILE_DELETION,
                location=deleted_file,
                description=f"File deleted: {deleted_file}",
                timestamp=datetime.now(timezone.utc).isoformat(),
                before_state={"exists": True, "hash": self.baseline["file_hashes"][deleted_file]},
                after_state={"exists": False},
                metrics={"files_removed": 1}
            ))

        # File modifications
        common_files = set(self.current_state["file_hashes"].keys()) & set(self.baseline.get("file_hashes", {}).keys())
        for file in common_files:
            if self.current_state["file_hashes"][file] != self.baseline["file_hashes"].get(file):
                changes.append(DetectedChange(
                    change_id=hashlib.sha256(f"mod_{file}".encode()).hexdigest()[:16],
                    change_type=ChangeType.CODE_MODIFICATION,
                    location=file,
                    description=f"File modified: {file}",
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    before_state={"hash": self.baseline["file_hashes"].get(file)},
                    after_state={"hash": self.current_state["file_hashes"][file]},
                    metrics={"files_modified": 1}
                ))

        # Capability changes
        old_caps = set(self.baseline.get("capability_signatures", []))
        new_caps = set(self.current_state["capability_signatures"])

        added_caps = new_caps - old_caps
        for cap in list(added_caps)[:10]:  # Limit to first 10
            changes.append(DetectedChange(
                change_id=hashlib.sha256(f"cap_add_{cap}".encode()).hexdigest()[:16],
                change_type=ChangeType.CAPABILITY_ADDITION,
                location=cap.split(":")[0],
                description=f"New capability: {cap.split(':')[1] if ':' in cap else cap}",
                timestamp=datetime.now(timezone.utc).isoformat(),
                before_state={"capability_exists": False},
                after_state={"capability_exists": True},
                metrics={"capabilities_added": 1}
            ))

        removed_caps = old_caps - new_caps
        for cap in list(removed_caps)[:10]:
            changes.append(DetectedChange(
                change_id=hashlib.sha256(f"cap_rem_{cap}".encode()).hexdigest()[:16],
                change_type=ChangeType.CAPABILITY_REMOVAL,
                location=cap.split(":")[0],
                description=f"Removed capability: {cap.split(':')[1] if ':' in cap else cap}",
                timestamp=datetime.now(timezone.utc).isoformat(),
                before_state={"capability_exists": True},
                after_state={"capability_exists": False},
                metrics={"capabilities_removed": 1}
            ))

        return changes

    # =========================================================================
    # IMPROVEMENT CLASSIFICATION
    # =========================================================================

    def classify_improvement(self, changes: List[DetectedChange]) -> ImprovementDetection:
        """
        Classify whether detected changes constitute genuine improvement.

        Criteria for GENUINE IMPROVEMENT:
        1. Net positive capability change
        2. Quality metrics improved (docstrings, tests)
        3. Complexity reduced or managed
        4. No regressions in existing functionality
        """
        detection_id = hashlib.sha256(
            f"{datetime.now(timezone.utc).isoformat()}_{len(changes)}".encode()
        ).hexdigest()[:16]

        if not changes:
            return ImprovementDetection(
                detection_id=detection_id,
                classification=ImprovementClass.NEUTRAL_CHANGE,
                changes=[],
                confidence=1.0,
                evidence=["No changes detected"],
                timestamp=datetime.now(timezone.utc).isoformat(),
                improvement_score=0.0,
                recommendation="No action needed - system stable"
            )

        evidence = []
        scores = []

        # Metric 1: Capability change
        caps_added = sum(1 for c in changes if c.change_type == ChangeType.CAPABILITY_ADDITION)
        caps_removed = sum(1 for c in changes if c.change_type == ChangeType.CAPABILITY_REMOVAL)
        cap_score = (caps_added - caps_removed) / max(1, caps_added + caps_removed)
        scores.append(cap_score)

        if caps_added > caps_removed:
            evidence.append(f"Net capability gain: +{caps_added - caps_removed} capabilities")
        elif caps_removed > caps_added:
            evidence.append(f"Net capability loss: -{caps_removed - caps_added} capabilities")

        # Metric 2: Code quality change
        old_docstring_ratio = self.baseline.get("docstring_count", 0) / max(1, self.baseline.get("function_count", 1))
        new_docstring_ratio = self.current_state["docstring_count"] / max(1, self.current_state["function_count"])
        quality_score = new_docstring_ratio - old_docstring_ratio
        scores.append(quality_score)

        if quality_score > 0:
            evidence.append(f"Documentation improved: +{quality_score:.2%} docstring coverage")
        elif quality_score < 0:
            evidence.append(f"Documentation decreased: {quality_score:.2%}")

        # Metric 3: Test coverage change
        old_test_ratio = self.baseline.get("test_count", 0) / max(1, self.baseline.get("function_count", 1))
        new_test_ratio = self.current_state["test_count"] / max(1, self.current_state["function_count"])
        test_score = new_test_ratio - old_test_ratio
        scores.append(test_score)

        if test_score > 0:
            evidence.append(f"Test coverage improved: +{test_score:.2%}")

        # Metric 4: Complexity change (lower is better)
        old_complexity = self.baseline.get("complexity_score", 0.5)
        new_complexity = self.current_state["complexity_score"]
        complexity_score = old_complexity - new_complexity  # Positive if complexity reduced
        scores.append(complexity_score)

        if complexity_score > 0:
            evidence.append(f"Complexity reduced: -{complexity_score:.2%}")
        elif complexity_score < 0:
            evidence.append(f"Complexity increased: +{abs(complexity_score):.2%}")

        # Calculate overall improvement score
        improvement_score = sum(scores) / len(scores) if scores else 0.0
        improvement_score = max(-1.0, min(1.0, improvement_score))  # Clamp to [-1, 1]

        # Classification logic
        if improvement_score > 0.2:
            classification = ImprovementClass.GENUINE_IMPROVEMENT
            recommendation = "Changes represent genuine improvement - consider committing"
        elif improvement_score > 0.05:
            classification = ImprovementClass.PSEUDO_IMPROVEMENT
            recommendation = "Minor positive change - verify value before committing"
        elif improvement_score > -0.05:
            classification = ImprovementClass.NEUTRAL_CHANGE
            recommendation = "No significant improvement detected - review necessity"
        elif improvement_score > -0.2:
            classification = ImprovementClass.UNCERTAIN
            recommendation = "Slight regression detected - investigate before proceeding"
        else:
            classification = ImprovementClass.REGRESSION
            recommendation = "Significant regression detected - consider rollback"

        # Confidence based on number of metrics with clear signal
        clear_signals = sum(1 for s in scores if abs(s) > 0.1)
        confidence = min(1.0, 0.5 + (clear_signals * 0.15))

        detection = ImprovementDetection(
            detection_id=detection_id,
            classification=classification,
            changes=changes,
            confidence=confidence,
            evidence=evidence,
            timestamp=datetime.now(timezone.utc).isoformat(),
            improvement_score=improvement_score,
            recommendation=recommendation
        )

        # Save to history
        self._save_detection(detection)

        return detection

    def _save_detection(self, detection: ImprovementDetection):
        """Save detection to history."""
        with open(self.history_file, 'a') as f:
            f.write(json.dumps(detection.to_dict()) + "\n")
        self.detection_history.append(detection)

    # =========================================================================
    # ANALYSIS
    # =========================================================================

    def run_detection(self) -> ImprovementDetection:
        """Run full improvement detection cycle."""
        changes = self.detect_changes()
        detection = self.classify_improvement(changes)
        return detection

    def update_baseline(self):
        """Update baseline to current state (after confirming improvement)."""
        self.baseline = self._capture_system_state()
        self._save_baseline()

    def get_detection_summary(self) -> Dict:
        """Get summary of detection system state."""
        if not self.detection_history:
            # Load from file
            if self.history_file.exists():
                with open(self.history_file) as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            # Just count for now
                            pass

        genuine_count = sum(
            1 for d in self.detection_history
            if d.classification == ImprovementClass.GENUINE_IMPROVEMENT
        )
        regression_count = sum(
            1 for d in self.detection_history
            if d.classification == ImprovementClass.REGRESSION
        )

        return {
            "total_detections": len(self.detection_history),
            "genuine_improvements": genuine_count,
            "regressions": regression_count,
            "baseline_timestamp": self.baseline.get("timestamp"),
            "baseline_stats": {
                "files": self.baseline.get("file_count", 0),
                "functions": self.baseline.get("function_count", 0),
                "classes": self.baseline.get("class_count", 0),
                "lines": self.baseline.get("total_lines", 0)
            },
            "current_stats": {
                "files": self.current_state.get("file_count", 0),
                "functions": self.current_state.get("function_count", 0),
                "classes": self.current_state.get("class_count", 0),
                "lines": self.current_state.get("total_lines", 0)
            }
        }


# Singleton accessor
_DETECTOR = None

def get_improvement_detector() -> AutonomousImprovementDetector:
    """Get singleton improvement detector."""
    global _DETECTOR
    if _DETECTOR is None:
        _DETECTOR = AutonomousImprovementDetector()
    return _DETECTOR


if __name__ == "__main__":
    print("AUTONOMOUS IMPROVEMENT DETECTOR - TASK-137")
    print("=" * 50)

    detector = get_improvement_detector()

    # Run detection
    print("\n[1] Running improvement detection...")
    detection = detector.run_detection()

    print(f"\n[2] Classification: {detection.classification.value}")
    print(f"    Improvement Score: {detection.improvement_score:.3f}")
    print(f"    Confidence: {detection.confidence:.2%}")

    print("\n[3] Evidence:")
    for ev in detection.evidence:
        print(f"    - {ev}")

    print(f"\n[4] Recommendation: {detection.recommendation}")

    print(f"\n[5] Changes Detected: {len(detection.changes)}")
    for change in detection.changes[:5]:
        print(f"    - [{change.change_type.value}] {change.description}")

    # Summary
    print("\n[6] Detection Summary:")
    summary = detector.get_detection_summary()
    print(json.dumps(summary, indent=2))

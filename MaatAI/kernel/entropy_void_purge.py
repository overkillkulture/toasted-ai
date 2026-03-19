#!/usr/bin/env python3
"""
TASK-151: Entropy Void Purge System
Identifies and purges entropy accumulation to maintain system coherence.
"""

import json
import datetime
import math
from typing import Dict, List, Optional, Set, Tuple
from pathlib import Path
from collections import defaultdict


class EntropyType:
    """Types of entropy recognized."""
    DATA = "data_entropy"
    BEHAVIORAL = "behavioral_entropy"
    STRUCTURAL = "structural_entropy"
    COGNITIVE = "cognitive_entropy"
    TEMPORAL = "temporal_entropy"


class EntropyVoidPurge:
    """System for detecting and purging entropy accumulation."""

    def __init__(
        self,
        system_state_path: str = "system_state.json",
        entropy_log_path: str = "entropy_purge_log.json"
    ):
        self.system_state_path = Path(system_state_path)
        self.entropy_log_path = Path(entropy_log_path)

        self.system_state = self._load_system_state()
        self.entropy_log = self._load_entropy_log()

        # Thresholds
        self.entropy_thresholds = {
            EntropyType.DATA: 0.7,
            EntropyType.BEHAVIORAL: 0.6,
            EntropyType.STRUCTURAL: 0.5,
            EntropyType.COGNITIVE: 0.65,
            EntropyType.TEMPORAL: 0.75
        }

    def _load_system_state(self) -> Dict:
        """Load current system state."""
        if self.system_state_path.exists():
            with open(self.system_state_path, 'r') as f:
                return json.load(f)

        return {
            "data_store": {},
            "behaviors": {},
            "structure": {},
            "cognitive_patterns": {},
            "temporal_markers": {},
            "entropy_levels": {},
            "last_purge": None,
            "coherence_score": 1.0
        }

    def _load_entropy_log(self) -> List:
        """Load entropy purge log."""
        if self.entropy_log_path.exists():
            with open(self.entropy_log_path, 'r') as f:
                return json.load(f)
        return []

    def _save_state(self):
        """Save system state and entropy log."""
        with open(self.system_state_path, 'w') as f:
            json.dump(self.system_state, f, indent=2)

        with open(self.entropy_log_path, 'w') as f:
            json.dump(self.entropy_log, f, indent=2)

    def calculate_data_entropy(self) -> float:
        """
        Calculate Shannon entropy of data store.

        Returns:
            Entropy value (0-1 normalized)
        """
        data_store = self.system_state["data_store"]

        if not data_store:
            return 0.0

        # Calculate frequency distribution
        value_counts = defaultdict(int)
        total_values = 0

        for value in self._flatten_values(data_store):
            value_str = str(value)
            value_counts[value_str] += 1
            total_values += 1

        if total_values == 0:
            return 0.0

        # Calculate Shannon entropy
        entropy = 0.0
        for count in value_counts.values():
            probability = count / total_values
            if probability > 0:
                entropy -= probability * math.log2(probability)

        # Normalize to 0-1
        max_entropy = math.log2(total_values) if total_values > 1 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        return min(normalized_entropy, 1.0)

    def _flatten_values(self, obj) -> List:
        """Flatten nested structure to list of values."""
        values = []

        if isinstance(obj, dict):
            for v in obj.values():
                values.extend(self._flatten_values(v))
        elif isinstance(obj, list):
            for item in obj:
                values.extend(self._flatten_values(item))
        else:
            values.append(obj)

        return values

    def calculate_behavioral_entropy(self) -> float:
        """
        Calculate entropy in behavioral patterns.

        Returns:
            Behavioral entropy (0-1)
        """
        behaviors = self.system_state["behaviors"]

        if not behaviors:
            return 0.0

        # Measure inconsistency in behaviors
        inconsistencies = 0
        total_comparisons = 0

        behavior_list = list(behaviors.items())

        for i, (name1, pattern1) in enumerate(behavior_list):
            for name2, pattern2 in behavior_list[i+1:]:
                total_comparisons += 1

                # Check for conflicts
                if isinstance(pattern1, dict) and isinstance(pattern2, dict):
                    conflicts = self._check_behavior_conflicts(pattern1, pattern2)
                    inconsistencies += conflicts

        if total_comparisons == 0:
            return 0.0

        return min(inconsistencies / total_comparisons, 1.0)

    def _check_behavior_conflicts(self, pattern1: Dict, pattern2: Dict) -> int:
        """Check for conflicts between behavior patterns."""
        conflicts = 0

        # Check for contradictory flags
        for key in set(pattern1.keys()) & set(pattern2.keys()):
            if isinstance(pattern1[key], bool) and isinstance(pattern2[key], bool):
                if pattern1[key] != pattern2[key]:
                    conflicts += 1

        return conflicts

    def calculate_structural_entropy(self) -> float:
        """
        Calculate structural disorganization entropy.

        Returns:
            Structural entropy (0-1)
        """
        structure = self.system_state["structure"]

        if not structure:
            return 0.0

        # Measure depth and breadth inconsistency
        depths = self._measure_depths(structure)

        if not depths:
            return 0.0

        # Calculate variance in depths
        mean_depth = sum(depths) / len(depths)
        variance = sum((d - mean_depth) ** 2 for d in depths) / len(depths)
        std_dev = math.sqrt(variance)

        # Normalize (assuming max std_dev of 10 is high entropy)
        normalized_entropy = min(std_dev / 10.0, 1.0)

        return normalized_entropy

    def _measure_depths(self, obj, current_depth: int = 0) -> List[int]:
        """Measure depths of all leaves in structure."""
        depths = []

        if isinstance(obj, dict):
            if not obj:  # Leaf node
                depths.append(current_depth)
            else:
                for value in obj.values():
                    depths.extend(self._measure_depths(value, current_depth + 1))
        elif isinstance(obj, list):
            if not obj:  # Leaf node
                depths.append(current_depth)
            else:
                for item in obj:
                    depths.extend(self._measure_depths(item, current_depth + 1))
        else:
            depths.append(current_depth)

        return depths

    def calculate_cognitive_entropy(self) -> float:
        """
        Calculate entropy in cognitive patterns.

        Returns:
            Cognitive entropy (0-1)
        """
        patterns = self.system_state["cognitive_patterns"]

        if not patterns:
            return 0.0

        # Measure fragmentation
        total_patterns = len(patterns)
        isolated_patterns = 0

        for pattern_name, pattern_data in patterns.items():
            if isinstance(pattern_data, dict):
                connections = pattern_data.get("connections", [])
                if len(connections) == 0:
                    isolated_patterns += 1

        fragmentation = isolated_patterns / total_patterns if total_patterns > 0 else 0.0

        return fragmentation

    def calculate_temporal_entropy(self) -> float:
        """
        Calculate entropy in temporal coherence.

        Returns:
            Temporal entropy (0-1)
        """
        markers = self.system_state["temporal_markers"]

        if not markers:
            return 0.0

        # Check for temporal inconsistencies
        timestamps = []
        for marker_data in markers.values():
            if isinstance(marker_data, dict) and "timestamp" in marker_data:
                try:
                    ts = datetime.datetime.fromisoformat(marker_data["timestamp"])
                    timestamps.append(ts)
                except:
                    pass

        if len(timestamps) < 2:
            return 0.0

        # Sort timestamps
        timestamps.sort()

        # Calculate irregularity in time intervals
        intervals = []
        for i in range(len(timestamps) - 1):
            delta = (timestamps[i+1] - timestamps[i]).total_seconds()
            intervals.append(delta)

        if not intervals:
            return 0.0

        # Calculate coefficient of variation
        mean_interval = sum(intervals) / len(intervals)
        if mean_interval == 0:
            return 0.0

        variance = sum((i - mean_interval) ** 2 for i in intervals) / len(intervals)
        std_dev = math.sqrt(variance)
        cv = std_dev / mean_interval

        # Normalize (CV > 1.0 is high entropy)
        return min(cv, 1.0)

    def scan_all_entropy(self) -> Dict:
        """
        Scan all entropy types.

        Returns:
            Comprehensive entropy report
        """
        entropy_scan = {
            "timestamp": datetime.datetime.now().isoformat(),
            "entropy_levels": {
                EntropyType.DATA: self.calculate_data_entropy(),
                EntropyType.BEHAVIORAL: self.calculate_behavioral_entropy(),
                EntropyType.STRUCTURAL: self.calculate_structural_entropy(),
                EntropyType.COGNITIVE: self.calculate_cognitive_entropy(),
                EntropyType.TEMPORAL: self.calculate_temporal_entropy()
            },
            "overall_entropy": 0.0,
            "coherence_score": 0.0,
            "requires_purge": []
        }

        # Calculate overall entropy (weighted average)
        weights = {
            EntropyType.DATA: 0.2,
            EntropyType.BEHAVIORAL: 0.25,
            EntropyType.STRUCTURAL: 0.2,
            EntropyType.COGNITIVE: 0.2,
            EntropyType.TEMPORAL: 0.15
        }

        overall = sum(
            entropy_scan["entropy_levels"][etype] * weights[etype]
            for etype in weights.keys()
        )
        entropy_scan["overall_entropy"] = overall

        # Calculate coherence (inverse of entropy)
        entropy_scan["coherence_score"] = 1.0 - overall

        # Check thresholds
        for etype, level in entropy_scan["entropy_levels"].items():
            if level > self.entropy_thresholds[etype]:
                entropy_scan["requires_purge"].append(etype)

        # Update system state
        self.system_state["entropy_levels"] = entropy_scan["entropy_levels"]
        self.system_state["coherence_score"] = entropy_scan["coherence_score"]
        self._save_state()

        return entropy_scan

    def purge_data_entropy(self) -> Dict:
        """
        Purge data entropy by removing redundant/obsolete data.

        Returns:
            Purge result
        """
        data_store = self.system_state["data_store"]
        initial_size = len(self._flatten_values(data_store))

        # Remove null/empty values
        self._remove_empty_values(data_store)

        # Remove duplicates
        self._deduplicate_data(data_store)

        final_size = len(self._flatten_values(data_store))
        removed = initial_size - final_size

        return {
            "entropy_type": EntropyType.DATA,
            "items_removed": removed,
            "reduction_percent": (removed / initial_size * 100) if initial_size > 0 else 0,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _remove_empty_values(self, obj):
        """Remove null and empty values from structure."""
        if isinstance(obj, dict):
            keys_to_remove = []
            for key, value in obj.items():
                if value is None or value == "" or value == {} or value == []:
                    keys_to_remove.append(key)
                else:
                    self._remove_empty_values(value)

            for key in keys_to_remove:
                del obj[key]

        elif isinstance(obj, list):
            # Remove None and empty items
            obj[:] = [item for item in obj if item is not None and item != "" and item != {} and item != []]
            for item in obj:
                self._remove_empty_values(item)

    def _deduplicate_data(self, obj, seen: Optional[Set] = None):
        """Remove duplicate values from structure."""
        if seen is None:
            seen = set()

        if isinstance(obj, dict):
            keys_to_remove = []
            for key, value in obj.items():
                value_str = json.dumps(value, sort_keys=True)
                if value_str in seen:
                    keys_to_remove.append(key)
                else:
                    seen.add(value_str)
                    self._deduplicate_data(value, seen)

            for key in keys_to_remove:
                del obj[key]

        elif isinstance(obj, list):
            unique_items = []
            for item in obj:
                item_str = json.dumps(item, sort_keys=True)
                if item_str not in seen:
                    seen.add(item_str)
                    unique_items.append(item)
                    self._deduplicate_data(item, seen)
            obj[:] = unique_items

    def purge_behavioral_entropy(self) -> Dict:
        """
        Purge behavioral entropy by resolving conflicts.

        Returns:
            Purge result
        """
        behaviors = self.system_state["behaviors"]
        conflicts_resolved = 0

        # Find and resolve contradictions
        behavior_list = list(behaviors.items())

        for i, (name1, pattern1) in enumerate(behavior_list):
            for name2, pattern2 in behavior_list[i+1:]:
                if isinstance(pattern1, dict) and isinstance(pattern2, dict):
                    resolved = self._resolve_behavior_conflicts(pattern1, pattern2)
                    conflicts_resolved += resolved

        return {
            "entropy_type": EntropyType.BEHAVIORAL,
            "conflicts_resolved": conflicts_resolved,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _resolve_behavior_conflicts(self, pattern1: Dict, pattern2: Dict) -> int:
        """Resolve conflicts between behavior patterns."""
        resolved = 0

        # Use most recent or most common value
        for key in set(pattern1.keys()) & set(pattern2.keys()):
            if isinstance(pattern1[key], bool) and isinstance(pattern2[key], bool):
                if pattern1[key] != pattern2[key]:
                    # Default to True (more permissive)
                    pattern1[key] = True
                    pattern2[key] = True
                    resolved += 1

        return resolved

    def purge_structural_entropy(self) -> Dict:
        """
        Purge structural entropy by normalizing structure.

        Returns:
            Purge result
        """
        structure = self.system_state["structure"]

        # Flatten overly deep structures
        max_depth = 5
        self._flatten_deep_structures(structure, current_depth=0, max_depth=max_depth)

        return {
            "entropy_type": EntropyType.STRUCTURAL,
            "structures_flattened": "structures normalized to max depth",
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _flatten_deep_structures(self, obj, current_depth: int, max_depth: int):
        """Flatten structures that exceed max depth."""
        if current_depth >= max_depth:
            return

        if isinstance(obj, dict):
            for key, value in list(obj.items()):
                if isinstance(value, dict) and current_depth + 1 >= max_depth:
                    # Flatten one level
                    obj[key] = str(value)
                else:
                    self._flatten_deep_structures(value, current_depth + 1, max_depth)

    def purge_all_entropy(self) -> Dict:
        """
        Perform comprehensive entropy purge.

        Returns:
            Complete purge report
        """
        # Scan first
        scan = self.scan_all_entropy()

        purge_results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "pre_purge_entropy": scan["overall_entropy"],
            "pre_purge_coherence": scan["coherence_score"],
            "purges_performed": []
        }

        # Purge each entropy type that exceeds threshold
        for entropy_type in scan["requires_purge"]:
            if entropy_type == EntropyType.DATA:
                result = self.purge_data_entropy()
            elif entropy_type == EntropyType.BEHAVIORAL:
                result = self.purge_behavioral_entropy()
            elif entropy_type == EntropyType.STRUCTURAL:
                result = self.purge_structural_entropy()
            else:
                continue

            purge_results["purges_performed"].append(result)

        # Rescan after purge
        post_scan = self.scan_all_entropy()
        purge_results["post_purge_entropy"] = post_scan["overall_entropy"]
        purge_results["post_purge_coherence"] = post_scan["coherence_score"]
        purge_results["entropy_reduction"] = scan["overall_entropy"] - post_scan["overall_entropy"]

        # Update system state
        self.system_state["last_purge"] = datetime.datetime.now().isoformat()

        # Log purge
        self.entropy_log.append(purge_results)
        self._save_state()

        return purge_results


def main():
    """Demonstration of entropy void purge system."""
    system = EntropyVoidPurge()

    print("🌀 Entropy Void Purge System")
    print("=" * 50)

    # Add some test data with entropy
    system.system_state["data_store"] = {
        "test1": "value",
        "test2": "value",  # duplicate
        "test3": None,  # null
        "test4": {"nested": "data", "deep": {"very": {"deep": {"too": "deep"}}}},
        "test5": ""  # empty
    }

    system.system_state["behaviors"] = {
        "behavior1": {"active": True, "priority": 1},
        "behavior2": {"active": False, "priority": 1},  # conflict
    }

    # Initial scan
    print("\n📊 Initial Entropy Scan:")
    scan = system.scan_all_entropy()
    print(json.dumps(scan, indent=2))

    # Perform purge
    print("\n🧹 Performing Entropy Purge...")
    purge_result = system.purge_all_entropy()
    print(json.dumps(purge_result, indent=2))

    print(f"\n✅ Coherence improved from {purge_result['pre_purge_coherence']:.2f} to {purge_result['post_purge_coherence']:.2f}")


if __name__ == "__main__":
    main()

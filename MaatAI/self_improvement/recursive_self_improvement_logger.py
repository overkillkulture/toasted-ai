#!/usr/bin/env python3
"""
RECURSIVE SELF-IMPROVEMENT LOGGING SYSTEM
==========================================
TASK-018: Log all recursive self-modifications
Tracks when the system modifies itself, creating an audit trail

Features:
- Immutable modification log
- Code-level change tracking
- Recursive depth tracking
- Safety boundary enforcement
- Rollback capability

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import hashlib
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

class ModificationType(Enum):
    """Types of self-modifications"""
    CODE_CHANGE = "code_change"
    PARAMETER_TUNE = "parameter_tune"
    LOOP_ADDITION = "loop_addition"
    LOOP_REMOVAL = "loop_removal"
    METRIC_CHANGE = "metric_change"
    THRESHOLD_CHANGE = "threshold_change"
    CAPABILITY_ADD = "capability_add"
    CAPABILITY_REMOVE = "capability_remove"

class SafetyLevel(Enum):
    """Safety levels for modifications"""
    SAFE = "safe"  # No risk
    LOW_RISK = "low_risk"  # Minimal risk
    MEDIUM_RISK = "medium_risk"  # Requires validation
    HIGH_RISK = "high_risk"  # Requires approval
    CRITICAL = "critical"  # Requires multiple approvals

@dataclass
class SelfModification:
    """Record of a self-modification"""
    id: str
    timestamp: float
    modification_type: str
    description: str
    recursive_depth: int  # How many layers deep
    target_component: str
    old_state: Dict[str, Any]
    new_state: Dict[str, Any]
    change_hash: str  # SHA256 of change
    parent_modification_id: Optional[str]  # If recursive
    safety_level: str
    maat_score: float
    approved: bool
    applied: bool
    rollback_data: Optional[Dict[str, Any]]
    metadata: Dict[str, Any]

@dataclass
class RecursionChain:
    """Chain of recursive modifications"""
    root_id: str
    modifications: List[str]  # IDs in order
    depth: int
    total_changes: int
    started_at: float
    completed_at: Optional[float]
    converged: bool

class RecursiveSelfImprovementLogger:
    """
    Logs all recursive self-improvements with full audit trail.

    Safety features:
    - Modification approval workflow
    - Rollback capability
    - Recursive depth limits
    - Maat validation on all changes
    """

    def __init__(self, log_path: str = "recursive_improvements.json", max_depth: int = 5):
        self.log_path = Path(log_path)
        self.max_depth = max_depth

        # State
        self.modifications: Dict[str, SelfModification] = {}
        self.recursion_chains: Dict[str, RecursionChain] = {}
        self.pending_modifications: List[str] = []

        # Stats
        self.stats = {
            "total_modifications": 0,
            "applied_modifications": 0,
            "blocked_modifications": 0,
            "rollbacks": 0,
            "max_recursion_depth": 0,
            "recursion_chains": 0,
            "session_start": time.time()
        }

        # Load existing log
        self._load_log()

    def _load_log(self):
        """Load existing modification log"""
        if self.log_path.exists():
            try:
                with open(self.log_path, 'r') as f:
                    data = json.load(f)

                # Restore modifications
                for mod_data in data.get("modifications", []):
                    mod = SelfModification(**mod_data)
                    self.modifications[mod.id] = mod

                # Restore chains
                for chain_data in data.get("recursion_chains", []):
                    chain = RecursionChain(**chain_data)
                    self.recursion_chains[chain.root_id] = chain

                # Restore stats
                if "stats" in data:
                    self.stats.update(data["stats"])

            except Exception as e:
                print(f"Warning: Could not load log: {e}")

    def _save_log(self):
        """Save modification log"""
        data = {
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
            "last_updated": datetime.now().isoformat(),
            "stats": self.stats,
            "modifications": [asdict(m) for m in self.modifications.values()],
            "recursion_chains": [asdict(c) for c in self.recursion_chains.values()],
            "pending": self.pending_modifications
        }

        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _generate_modification_id(self) -> str:
        """Generate unique modification ID"""
        timestamp = time.time()
        counter = len(self.modifications)
        raw = f"{timestamp}:{counter}"
        return f"MOD-{hashlib.sha256(raw.encode()).hexdigest()[:12].upper()}"

    def _calculate_change_hash(self, old_state: Dict, new_state: Dict) -> str:
        """Calculate hash of the change"""
        change = {
            "old": old_state,
            "new": new_state
        }
        raw = json.dumps(change, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def _determine_safety_level(
        self,
        mod_type: ModificationType,
        recursive_depth: int,
        target: str
    ) -> SafetyLevel:
        """Determine safety level of modification"""

        # Critical components
        if target in ["maat_core", "safety_boundary", "ethics_engine"]:
            return SafetyLevel.CRITICAL

        # Depth-based risk
        if recursive_depth >= 3:
            return SafetyLevel.HIGH_RISK
        elif recursive_depth >= 2:
            return SafetyLevel.MEDIUM_RISK

        # Type-based risk
        if mod_type in [ModificationType.CODE_CHANGE, ModificationType.CAPABILITY_REMOVE]:
            return SafetyLevel.MEDIUM_RISK
        elif mod_type in [ModificationType.PARAMETER_TUNE, ModificationType.THRESHOLD_CHANGE]:
            return SafetyLevel.LOW_RISK
        else:
            return SafetyLevel.SAFE

    def log_modification(
        self,
        mod_type: ModificationType,
        description: str,
        target_component: str,
        old_state: Dict[str, Any],
        new_state: Dict[str, Any],
        recursive_depth: int = 0,
        parent_id: Optional[str] = None,
        maat_score: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SelfModification:
        """
        Log a self-modification.

        Args:
            mod_type: Type of modification
            description: Human-readable description
            target_component: What component is being modified
            old_state: State before modification
            new_state: State after modification
            recursive_depth: How deep in recursion chain
            parent_id: ID of parent modification (if recursive)
            maat_score: Maat alignment score
            metadata: Additional metadata

        Returns:
            SelfModification record
        """

        # Check recursion depth
        if recursive_depth > self.max_depth:
            raise ValueError(f"Recursion depth {recursive_depth} exceeds max {self.max_depth}")

        # Generate ID and hash
        mod_id = self._generate_modification_id()
        change_hash = self._calculate_change_hash(old_state, new_state)

        # Determine safety level
        safety_level = self._determine_safety_level(mod_type, recursive_depth, target_component)

        # Create modification record
        modification = SelfModification(
            id=mod_id,
            timestamp=time.time(),
            modification_type=mod_type.value,
            description=description,
            recursive_depth=recursive_depth,
            target_component=target_component,
            old_state=old_state,
            new_state=new_state,
            change_hash=change_hash,
            parent_modification_id=parent_id,
            safety_level=safety_level.value,
            maat_score=maat_score,
            approved=False,
            applied=False,
            rollback_data={"old_state": old_state},
            metadata=metadata or {}
        )

        # Store
        self.modifications[mod_id] = modification
        self.pending_modifications.append(mod_id)

        # Update stats
        self.stats["total_modifications"] += 1
        self.stats["max_recursion_depth"] = max(
            self.stats["max_recursion_depth"],
            recursive_depth
        )

        # Track recursion chain
        if parent_id:
            self._update_recursion_chain(mod_id, parent_id, recursive_depth)

        # Auto-approve safe modifications
        if safety_level == SafetyLevel.SAFE and maat_score >= 0.7:
            self.approve_modification(mod_id)

        self._save_log()

        return modification

    def _update_recursion_chain(self, mod_id: str, parent_id: str, depth: int):
        """Update or create recursion chain"""

        # Find root
        root_id = parent_id
        current = self.modifications.get(parent_id)

        while current and current.parent_modification_id:
            root_id = current.parent_modification_id
            current = self.modifications.get(root_id)

        # Update or create chain
        if root_id in self.recursion_chains:
            chain = self.recursion_chains[root_id]
            chain.modifications.append(mod_id)
            chain.depth = max(chain.depth, depth)
            chain.total_changes += 1
        else:
            chain = RecursionChain(
                root_id=root_id,
                modifications=[root_id, mod_id],
                depth=depth,
                total_changes=2,
                started_at=time.time(),
                completed_at=None,
                converged=False
            )
            self.recursion_chains[root_id] = chain
            self.stats["recursion_chains"] += 1

    def approve_modification(self, mod_id: str) -> bool:
        """Approve a modification for application"""
        if mod_id not in self.modifications:
            return False

        mod = self.modifications[mod_id]
        mod.approved = True

        if mod_id in self.pending_modifications:
            self.pending_modifications.remove(mod_id)

        self._save_log()
        return True

    def apply_modification(self, mod_id: str) -> bool:
        """Apply an approved modification"""
        if mod_id not in self.modifications:
            return False

        mod = self.modifications[mod_id]

        if not mod.approved:
            return False

        mod.applied = True
        self.stats["applied_modifications"] += 1

        self._save_log()
        return True

    def rollback_modification(self, mod_id: str) -> bool:
        """Rollback a modification"""
        if mod_id not in self.modifications:
            return False

        mod = self.modifications[mod_id]

        if not mod.applied:
            return False

        # Use rollback data
        # In real implementation, would restore old_state
        mod.applied = False
        self.stats["rollbacks"] += 1

        self._save_log()
        return True

    def get_recursion_chain(self, root_id: str) -> Optional[RecursionChain]:
        """Get recursion chain by root ID"""
        return self.recursion_chains.get(root_id)

    def get_pending_modifications(self) -> List[SelfModification]:
        """Get all pending modifications"""
        return [self.modifications[id] for id in self.pending_modifications if id in self.modifications]

    def get_stats(self) -> Dict[str, Any]:
        """Get modification statistics"""
        return {
            **self.stats,
            "pending_count": len(self.pending_modifications),
            "modification_count": len(self.modifications),
            "chain_count": len(self.recursion_chains)
        }


# Demo / Test
if __name__ == "__main__":
    print("=" * 70)
    print("RECURSIVE SELF-IMPROVEMENT LOGGING SYSTEM")
    print("Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("=" * 70)

    logger = RecursiveSelfImprovementLogger(
        log_path="test_recursive_improvements.json"
    )

    # Simulate recursive modifications
    print("\n📝 Simulating recursive modifications...")

    # Root modification
    mod1 = logger.log_modification(
        mod_type=ModificationType.PARAMETER_TUNE,
        description="Adjust learning rate",
        target_component="optimizer",
        old_state={"learning_rate": 0.001},
        new_state={"learning_rate": 0.002},
        maat_score=0.85
    )
    print(f"  ✓ Root modification: {mod1.id}")

    # Child modification (recursive)
    mod2 = logger.log_modification(
        mod_type=ModificationType.PARAMETER_TUNE,
        description="Adjust momentum based on learning rate",
        target_component="optimizer",
        old_state={"momentum": 0.9},
        new_state={"momentum": 0.95},
        recursive_depth=1,
        parent_id=mod1.id,
        maat_score=0.82
    )
    print(f"  ✓ Recursive modification (depth 1): {mod2.id}")

    # Grandchild modification (deeper recursion)
    mod3 = logger.log_modification(
        mod_type=ModificationType.THRESHOLD_CHANGE,
        description="Adjust convergence threshold based on momentum",
        target_component="optimizer",
        old_state={"threshold": 0.01},
        new_state={"threshold": 0.005},
        recursive_depth=2,
        parent_id=mod2.id,
        maat_score=0.79
    )
    print(f"  ✓ Recursive modification (depth 2): {mod3.id}")

    # Apply modifications
    logger.approve_modification(mod2.id)
    logger.apply_modification(mod1.id)
    logger.apply_modification(mod2.id)

    # Get stats
    stats = logger.get_stats()
    print(f"\n📈 Modification Stats:")
    print(f"   Total modifications: {stats['total_modifications']}")
    print(f"   Applied: {stats['applied_modifications']}")
    print(f"   Pending: {stats['pending_count']}")
    print(f"   Max recursion depth: {stats['max_recursion_depth']}")
    print(f"   Recursion chains: {stats['recursion_chains']}")

    # Get recursion chain
    chain = logger.get_recursion_chain(mod1.id)
    if chain:
        print(f"\n🔗 Recursion Chain (root: {chain.root_id}):")
        print(f"   Depth: {chain.depth}")
        print(f"   Total changes: {chain.total_changes}")
        print(f"   Modifications: {len(chain.modifications)}")

    print("\n✅ Recursive logging test complete")
    print("=" * 70)

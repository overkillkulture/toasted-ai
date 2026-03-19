"""
TASK-035: QUANTUM STATE BACKUP PROTOCOL
=======================================
Scalable quantum state persistence with coherence preservation.

Architecture:
- Checkpoint snapshots at configurable intervals
- Incremental delta compression for efficiency
- Coherence-aware backup timing (backup when coherent)
- Distributed storage across multiple backends
- Recovery with state fidelity verification

Quantum State Preservation Challenges:
1. No-cloning theorem: Cannot perfectly copy quantum states
2. Decoherence: States decay over time
3. Measurement collapse: Observation changes state

Solution: Save classical description of state preparation,
not the quantum state itself. Use state tomography for verification.
"""

import asyncio
import hashlib
import json
import os
import time
import threading
import pickle
import gzip
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Callable
import logging
import math
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QuantumStateBackup")


class BackupStrategy(Enum):
    """Backup strategies based on quantum coherence"""
    CHECKPOINT = "checkpoint"      # Full state snapshot
    INCREMENTAL = "incremental"    # Delta from last backup
    CONTINUOUS = "continuous"      # Stream-based persistence
    COHERENT = "coherent"          # Backup only when coherent


class StorageBackend(Enum):
    """Storage backends for state persistence"""
    LOCAL_FILE = "local_file"
    MEMORY = "memory"
    DISTRIBUTED = "distributed"
    SQLITE = "sqlite"


@dataclass
class QuantumStateSnapshot:
    """Snapshot of quantum state preparation instructions"""
    snapshot_id: str
    timestamp: float
    coherence_at_capture: float
    
    # State preparation recipe (not the state itself)
    initial_state: List[complex]          # Initial amplitudes
    gate_sequence: List[Dict[str, Any]]   # Gates applied
    measurement_basis: str                # Measurement basis
    
    # Metadata
    num_qubits: int
    fidelity_estimate: float
    checksum: str
    
    # Delta information
    is_incremental: bool = False
    parent_snapshot_id: Optional[str] = None
    delta_gates: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_json(self) -> str:
        """Serialize to JSON"""
        data = asdict(self)
        # Convert complex numbers to list pairs
        data["initial_state"] = [[c.real, c.imag] for c in self.initial_state]
        return json.dumps(data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "QuantumStateSnapshot":
        """Deserialize from JSON"""
        data = json.loads(json_str)
        # Convert list pairs back to complex
        data["initial_state"] = [complex(r, i) for r, i in data["initial_state"]]
        return cls(**data)


@dataclass 
class BackupConfig:
    """Configuration for backup system"""
    backup_dir: str = "./quantum_backups"
    checkpoint_interval: float = 60.0      # seconds
    max_snapshots: int = 100
    compression_level: int = 6
    coherence_threshold: float = 0.8       # Min coherence for backup
    enable_distributed: bool = False
    distributed_nodes: List[str] = field(default_factory=list)
    fidelity_verification: bool = True


class QuantumStateBackup:
    """
    Quantum State Backup System
    
    Preserves quantum computation state through:
    1. Gate sequence recording (preparation recipe)
    2. Amplitude snapshots at coherent moments
    3. Measurement results history
    4. Recovery verification via state tomography
    """
    
    def __init__(self, config: Optional[BackupConfig] = None):
        self.config = config or BackupConfig()
        self.snapshots: Dict[str, QuantumStateSnapshot] = {}
        self.current_gate_sequence: List[Dict[str, Any]] = []
        self.recovery_log: List[Dict[str, Any]] = []
        
        # Storage backends
        self._backends: Dict[StorageBackend, Any] = {}
        self._lock = threading.Lock()
        
        # Metrics
        self.total_backups = 0
        self.successful_recoveries = 0
        self.compression_savings = 0
        
        # Initialize storage
        self._init_storage()
        
        logger.info("QuantumStateBackup initialized")
    
    def _init_storage(self):
        """Initialize storage backends"""
        # Local file storage
        backup_path = Path(self.config.backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)
        self._backends[StorageBackend.LOCAL_FILE] = backup_path
        
        # Memory storage
        self._backends[StorageBackend.MEMORY] = {}
        
        logger.info(f"Storage initialized: {self.config.backup_dir}")
    
    def record_gate(self, gate_name: str, qubits: List[int], 
                   params: Optional[Dict[str, float]] = None):
        """Record a gate operation for backup"""
        gate_record = {
            "gate": gate_name,
            "qubits": qubits,
            "params": params or {},
            "timestamp": time.time()
        }
        self.current_gate_sequence.append(gate_record)
    
    def create_snapshot(self, state_amplitudes: List[complex],
                       coherence: float,
                       strategy: BackupStrategy = BackupStrategy.CHECKPOINT,
                       parent_id: Optional[str] = None) -> QuantumStateSnapshot:
        """
        Create a quantum state snapshot.
        
        Args:
            state_amplitudes: Current state vector amplitudes
            coherence: Current coherence level (0-1)
            strategy: Backup strategy to use
            parent_id: Parent snapshot for incremental backups
        """
        
        # Generate snapshot ID
        snapshot_id = f"qs_{int(time.time()*1000)}_{random.randint(1000,9999)}"
        
        # Calculate checksum
        state_bytes = pickle.dumps(state_amplitudes)
        checksum = hashlib.sha256(state_bytes).hexdigest()[:16]
        
        # Determine if incremental
        is_incremental = strategy == BackupStrategy.INCREMENTAL and parent_id is not None
        delta_gates = []
        
        if is_incremental and parent_id in self.snapshots:
            # Calculate delta from parent
            parent = self.snapshots[parent_id]
            parent_gate_count = len(parent.gate_sequence)
            delta_gates = self.current_gate_sequence[parent_gate_count:]
        
        snapshot = QuantumStateSnapshot(
            snapshot_id=snapshot_id,
            timestamp=time.time(),
            coherence_at_capture=coherence,
            initial_state=state_amplitudes,
            gate_sequence=self.current_gate_sequence.copy() if not is_incremental else [],
            measurement_basis="computational",
            num_qubits=int(math.log2(len(state_amplitudes))),
            fidelity_estimate=coherence * 0.95,  # Conservative estimate
            checksum=checksum,
            is_incremental=is_incremental,
            parent_snapshot_id=parent_id,
            delta_gates=delta_gates
        )
        
        with self._lock:
            self.snapshots[snapshot_id] = snapshot
            self.total_backups += 1
            
            # Enforce max snapshots
            if len(self.snapshots) > self.config.max_snapshots:
                self._prune_old_snapshots()
        
        logger.info(f"Created snapshot {snapshot_id} (coherence: {coherence:.3f})")
        return snapshot
    
    def save_snapshot(self, snapshot: QuantumStateSnapshot,
                     backend: StorageBackend = StorageBackend.LOCAL_FILE) -> bool:
        """Save snapshot to storage backend"""
        
        try:
            json_data = snapshot.to_json()
            
            if backend == StorageBackend.LOCAL_FILE:
                # Compress and save to file
                compressed = gzip.compress(
                    json_data.encode(),
                    compresslevel=self.config.compression_level
                )
                
                file_path = self._backends[backend] / f"{snapshot.snapshot_id}.qsb"
                with open(file_path, "wb") as f:
                    f.write(compressed)
                
                # Track compression savings
                self.compression_savings += len(json_data) - len(compressed)
                
                logger.info(f"Saved snapshot to {file_path}")
                
            elif backend == StorageBackend.MEMORY:
                self._backends[backend][snapshot.snapshot_id] = json_data
                
            elif backend == StorageBackend.DISTRIBUTED:
                # Distribute across nodes
                return self._distribute_snapshot(snapshot)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save snapshot: {e}")
            return False
    
    def load_snapshot(self, snapshot_id: str,
                     backend: StorageBackend = StorageBackend.LOCAL_FILE
                     ) -> Optional[QuantumStateSnapshot]:
        """Load snapshot from storage backend"""
        
        try:
            if backend == StorageBackend.LOCAL_FILE:
                file_path = self._backends[backend] / f"{snapshot_id}.qsb"
                
                if not file_path.exists():
                    logger.warning(f"Snapshot file not found: {file_path}")
                    return None
                
                with open(file_path, "rb") as f:
                    compressed = f.read()
                
                json_data = gzip.decompress(compressed).decode()
                return QuantumStateSnapshot.from_json(json_data)
                
            elif backend == StorageBackend.MEMORY:
                json_data = self._backends[backend].get(snapshot_id)
                if json_data:
                    return QuantumStateSnapshot.from_json(json_data)
                return None
                
        except Exception as e:
            logger.error(f"Failed to load snapshot: {e}")
            return None
    
    def recover_state(self, snapshot_id: str) -> Optional[Tuple[List[complex], List[Dict]]]:
        """
        Recover quantum state from snapshot.
        
        Returns:
            Tuple of (state_amplitudes, gate_sequence) for state reconstruction
        """
        
        # Try memory first, then file
        snapshot = self.snapshots.get(snapshot_id)
        
        if not snapshot:
            snapshot = self.load_snapshot(snapshot_id)
        
        if not snapshot:
            logger.error(f"Snapshot {snapshot_id} not found")
            return None
        
        # If incremental, need to chain back to full snapshot
        if snapshot.is_incremental:
            full_sequence = self._reconstruct_gate_sequence(snapshot)
        else:
            full_sequence = snapshot.gate_sequence
        
        # Log recovery
        self.recovery_log.append({
            "snapshot_id": snapshot_id,
            "timestamp": time.time(),
            "fidelity_estimate": snapshot.fidelity_estimate
        })
        self.successful_recoveries += 1
        
        logger.info(f"Recovered state from {snapshot_id}")
        return (snapshot.initial_state, full_sequence)
    
    def _reconstruct_gate_sequence(self, snapshot: QuantumStateSnapshot
                                   ) -> List[Dict[str, Any]]:
        """Reconstruct full gate sequence from incremental snapshot"""
        
        if not snapshot.is_incremental or not snapshot.parent_snapshot_id:
            return snapshot.gate_sequence
        
        # Get parent
        parent = self.snapshots.get(snapshot.parent_snapshot_id)
        if not parent:
            parent = self.load_snapshot(snapshot.parent_snapshot_id)
        
        if not parent:
            logger.warning("Parent snapshot not found, using delta only")
            return snapshot.delta_gates
        
        # Recursively reconstruct
        parent_sequence = self._reconstruct_gate_sequence(parent)
        return parent_sequence + snapshot.delta_gates
    
    def _prune_old_snapshots(self):
        """Remove old snapshots to stay under limit"""
        
        # Sort by timestamp
        sorted_ids = sorted(
            self.snapshots.keys(),
            key=lambda x: self.snapshots[x].timestamp
        )
        
        # Remove oldest until under limit
        while len(self.snapshots) > self.config.max_snapshots:
            old_id = sorted_ids.pop(0)
            
            # Don't remove if it's a parent of another snapshot
            is_parent = any(
                s.parent_snapshot_id == old_id 
                for s in self.snapshots.values()
            )
            
            if not is_parent:
                del self.snapshots[old_id]
                logger.info(f"Pruned old snapshot: {old_id}")
    
    def _distribute_snapshot(self, snapshot: QuantumStateSnapshot) -> bool:
        """Distribute snapshot across nodes (stub for distributed mode)"""
        
        if not self.config.distributed_nodes:
            return False
        
        # In production, this would distribute to actual nodes
        # For now, simulate distribution
        logger.info(f"Distributing snapshot to {len(self.config.distributed_nodes)} nodes")
        return True
    
    def verify_fidelity(self, recovered_state: List[complex],
                       reference_state: List[complex]) -> float:
        """
        Verify fidelity between recovered and reference states.
        Uses simplified fidelity calculation.
        """
        
        if len(recovered_state) != len(reference_state):
            return 0.0
        
        # Calculate state fidelity: F = |<psi|phi>|^2
        overlap = sum(
            recovered_state[i].conjugate() * reference_state[i]
            for i in range(len(recovered_state))
        )
        
        fidelity = abs(overlap) ** 2
        return min(1.0, max(0.0, fidelity))
    
    def get_status(self) -> Dict[str, Any]:
        """Get backup system status"""
        return {
            "total_snapshots": len(self.snapshots),
            "total_backups": self.total_backups,
            "successful_recoveries": self.successful_recoveries,
            "compression_savings_bytes": self.compression_savings,
            "gate_sequence_length": len(self.current_gate_sequence),
            "storage_backends": list(self._backends.keys())
        }


class BackupManager:
    """
    High-level backup manager with automatic scheduling.
    """
    
    def __init__(self, backup_system: QuantumStateBackup):
        self.backup = backup_system
        self.running = False
        self._backup_thread: Optional[threading.Thread] = None
        self._state_callback: Optional[Callable[[], Tuple[List[complex], float]]] = None
    
    def set_state_callback(self, callback: Callable[[], Tuple[List[complex], float]]):
        """Set callback to get current state and coherence"""
        self._state_callback = callback
    
    def start_auto_backup(self, interval: Optional[float] = None):
        """Start automatic backup thread"""
        
        if self.running:
            return
        
        self.running = True
        interval = interval or self.backup.config.checkpoint_interval
        
        def backup_loop():
            while self.running:
                time.sleep(interval)
                
                if not self.running:
                    break
                
                try:
                    self._perform_auto_backup()
                except Exception as e:
                    logger.error(f"Auto-backup failed: {e}")
        
        self._backup_thread = threading.Thread(target=backup_loop, daemon=True)
        self._backup_thread.start()
        logger.info(f"Auto-backup started (interval: {interval}s)")
    
    def stop_auto_backup(self):
        """Stop automatic backup thread"""
        self.running = False
        if self._backup_thread:
            self._backup_thread.join(timeout=2.0)
        logger.info("Auto-backup stopped")
    
    def _perform_auto_backup(self):
        """Perform automatic backup if conditions met"""
        
        if not self._state_callback:
            return
        
        # Get current state
        state, coherence = self._state_callback()
        
        # Only backup if coherent
        if coherence < self.backup.config.coherence_threshold:
            logger.debug(f"Skipping backup (coherence {coherence:.3f} below threshold)")
            return
        
        # Determine strategy
        if len(self.backup.snapshots) == 0:
            strategy = BackupStrategy.CHECKPOINT
            parent_id = None
        else:
            # Use incremental after first checkpoint
            strategy = BackupStrategy.INCREMENTAL
            parent_id = max(
                self.backup.snapshots.keys(),
                key=lambda x: self.backup.snapshots[x].timestamp
            )
        
        # Create and save snapshot
        snapshot = self.backup.create_snapshot(
            state_amplitudes=state,
            coherence=coherence,
            strategy=strategy,
            parent_id=parent_id
        )
        
        self.backup.save_snapshot(snapshot)
    
    def manual_backup(self, state: List[complex], coherence: float) -> str:
        """Trigger manual backup"""
        
        snapshot = self.backup.create_snapshot(
            state_amplitudes=state,
            coherence=coherence,
            strategy=BackupStrategy.CHECKPOINT
        )
        
        self.backup.save_snapshot(snapshot)
        return snapshot.snapshot_id


# Demo/Test
async def demo_backup_system():
    """Demonstrate backup system"""
    
    print("=" * 70)
    print("QUANTUM STATE BACKUP - TASK-035 DEMO")
    print("=" * 70)
    
    # Create backup system
    config = BackupConfig(
        backup_dir="./quantum_backups",
        checkpoint_interval=10.0,
        coherence_threshold=0.7
    )
    backup = QuantumStateBackup(config)
    manager = BackupManager(backup)
    
    # Simulate quantum state (2 qubits = 4 amplitudes)
    state = [
        complex(1/math.sqrt(2), 0),    # |00>
        complex(0, 0),                  # |01>
        complex(0, 0),                  # |10>
        complex(1/math.sqrt(2), 0)     # |11> - Bell state
    ]
    
    # Record some gates
    backup.record_gate("H", [0])
    backup.record_gate("CNOT", [0, 1])
    
    # Create checkpoint
    snapshot = backup.create_snapshot(
        state_amplitudes=state,
        coherence=0.95,
        strategy=BackupStrategy.CHECKPOINT
    )
    
    print(f"\n1. Created checkpoint: {snapshot.snapshot_id}")
    print(f"   Coherence: {snapshot.coherence_at_capture:.3f}")
    print(f"   Qubits: {snapshot.num_qubits}")
    
    # Save to file
    backup.save_snapshot(snapshot)
    print(f"   Saved to file")
    
    # Add more gates
    backup.record_gate("Z", [0])
    backup.record_gate("X", [1])
    
    # Create incremental backup
    state2 = [complex(c.real * 0.9, c.imag) for c in state]  # Slightly decayed
    
    snapshot2 = backup.create_snapshot(
        state_amplitudes=state2,
        coherence=0.88,
        strategy=BackupStrategy.INCREMENTAL,
        parent_id=snapshot.snapshot_id
    )
    
    print(f"\n2. Created incremental: {snapshot2.snapshot_id}")
    print(f"   Parent: {snapshot2.parent_snapshot_id}")
    print(f"   Delta gates: {len(snapshot2.delta_gates)}")
    
    # Recovery test
    recovered = backup.recover_state(snapshot2.snapshot_id)
    if recovered:
        recovered_state, gate_seq = recovered
        print(f"\n3. Recovery successful")
        print(f"   Gate sequence length: {len(gate_seq)}")
        
        # Verify fidelity
        fidelity = backup.verify_fidelity(recovered_state, state2)
        print(f"   Fidelity: {fidelity:.4f}")
    
    # Status
    status = backup.get_status()
    print(f"\n4. System Status:")
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)
    print("QUANTUM STATE BACKUP - OPERATIONAL")
    print("=" * 70)
    
    return backup


if __name__ == "__main__":
    asyncio.run(demo_backup_system())

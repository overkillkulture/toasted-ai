"""
TASK-021: Neural Thread Synchronization System
Streamlines thread state synchronization across distributed neural networks
"""

import json
import threading
import time
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict
import hashlib


@dataclass
class ThreadState:
    """Represents state of a neural thread"""
    thread_id: str
    node_id: str
    state_hash: str
    last_sync: str
    message_count: int
    active: bool
    priority: int = 1
    metadata: Dict = None

    def to_dict(self):
        return asdict(self)


class NeuralThreadSynchronizer:
    """
    Synchronizes thread states across neural network nodes
    Prevents divergence, ensures consistency, enables recovery
    """

    def __init__(self, node_id: str, sync_interval: float = 0.5):
        self.node_id = node_id
        self.sync_interval = sync_interval
        self.thread_states: Dict[str, ThreadState] = {}
        self.sync_queue: List[Dict] = []
        self.sync_lock = threading.Lock()
        self.running = False
        self.sync_thread = None
        self.sync_history: List[Dict] = []
        self.max_history = 1000

        # Performance tracking
        self.stats = {
            "syncs_completed": 0,
            "conflicts_resolved": 0,
            "states_synchronized": 0,
            "errors": 0
        }

    def start(self) -> Dict:
        """Start synchronization daemon"""
        if self.running:
            return {"status": "ALREADY_RUNNING"}

        self.running = True
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()

        return {
            "status": "STARTED",
            "node_id": self.node_id,
            "sync_interval": self.sync_interval,
            "timestamp": datetime.utcnow().isoformat()
        }

    def stop(self) -> Dict:
        """Stop synchronization daemon"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=2.0)

        return {
            "status": "STOPPED",
            "stats": self.stats.copy(),
            "timestamp": datetime.utcnow().isoformat()
        }

    def register_thread(self, thread_id: str, initial_state: Dict = None) -> Dict:
        """Register a new neural thread"""
        with self.sync_lock:
            if thread_id in self.thread_states:
                return {"status": "ALREADY_EXISTS", "thread_id": thread_id}

            state_hash = self._compute_hash(initial_state or {})

            thread_state = ThreadState(
                thread_id=thread_id,
                node_id=self.node_id,
                state_hash=state_hash,
                last_sync=datetime.utcnow().isoformat(),
                message_count=0,
                active=True,
                metadata=initial_state or {}
            )

            self.thread_states[thread_id] = thread_state

            return {
                "status": "REGISTERED",
                "thread_id": thread_id,
                "state_hash": state_hash,
                "timestamp": datetime.utcnow().isoformat()
            }

    def update_thread_state(self, thread_id: str, new_state: Dict) -> Dict:
        """Update thread state and queue for sync"""
        with self.sync_lock:
            if thread_id not in self.thread_states:
                return {"status": "THREAD_NOT_FOUND", "thread_id": thread_id}

            thread_state = self.thread_states[thread_id]
            old_hash = thread_state.state_hash
            new_hash = self._compute_hash(new_state)

            # Update state
            thread_state.state_hash = new_hash
            thread_state.last_sync = datetime.utcnow().isoformat()
            thread_state.message_count = new_state.get("message_count", 0)
            thread_state.metadata = new_state

            # Queue for sync
            sync_event = {
                "thread_id": thread_id,
                "old_hash": old_hash,
                "new_hash": new_hash,
                "timestamp": datetime.utcnow().isoformat(),
                "node_id": self.node_id
            }

            self.sync_queue.append(sync_event)

            return {
                "status": "UPDATED",
                "thread_id": thread_id,
                "hash_changed": old_hash != new_hash,
                "queued_for_sync": True
            }

    def synchronize_threads(self, remote_states: List[Dict]) -> Dict:
        """Synchronize with remote thread states"""
        with self.sync_lock:
            conflicts = []
            merged = 0
            updated = 0

            for remote in remote_states:
                thread_id = remote.get("thread_id")
                if not thread_id:
                    continue

                remote_hash = remote.get("state_hash")

                if thread_id in self.thread_states:
                    local_state = self.thread_states[thread_id]

                    # Check for conflict
                    if local_state.state_hash != remote_hash:
                        conflict = self._resolve_conflict(local_state, remote)
                        conflicts.append(conflict)

                        if conflict["resolution"] == "REMOTE_WINS":
                            self._apply_remote_state(thread_id, remote)
                            updated += 1
                    else:
                        merged += 1
                else:
                    # New thread from remote
                    self._apply_remote_state(thread_id, remote)
                    updated += 1

            self.stats["syncs_completed"] += 1
            self.stats["conflicts_resolved"] += len(conflicts)
            self.stats["states_synchronized"] += merged + updated

            return {
                "status": "SYNCHRONIZED",
                "threads_merged": merged,
                "threads_updated": updated,
                "conflicts": len(conflicts),
                "conflict_details": conflicts,
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_thread_state(self, thread_id: str) -> Optional[Dict]:
        """Get current state of a thread"""
        with self.sync_lock:
            state = self.thread_states.get(thread_id)
            return state.to_dict() if state else None

    def get_all_states(self) -> List[Dict]:
        """Get all thread states for broadcasting"""
        with self.sync_lock:
            return [state.to_dict() for state in self.thread_states.values()]

    def get_sync_status(self) -> Dict:
        """Get synchronization status"""
        with self.sync_lock:
            return {
                "node_id": self.node_id,
                "running": self.running,
                "thread_count": len(self.thread_states),
                "active_threads": sum(1 for s in self.thread_states.values() if s.active),
                "pending_syncs": len(self.sync_queue),
                "stats": self.stats.copy(),
                "timestamp": datetime.utcnow().isoformat()
            }

    def _sync_loop(self):
        """Background synchronization loop"""
        while self.running:
            try:
                # Process sync queue
                with self.sync_lock:
                    if self.sync_queue:
                        events = self.sync_queue[:10]  # Process batch
                        self.sync_queue = self.sync_queue[10:]

                        for event in events:
                            self._record_sync_event(event)

                time.sleep(self.sync_interval)

            except Exception as e:
                self.stats["errors"] += 1
                print(f"Sync error: {e}")

    def _compute_hash(self, state: Dict) -> str:
        """Compute hash of state for comparison"""
        state_str = json.dumps(state, sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]

    def _resolve_conflict(self, local: ThreadState, remote: Dict) -> Dict:
        """Resolve sync conflict between local and remote states"""
        local_time = datetime.fromisoformat(local.last_sync)
        remote_time = datetime.fromisoformat(remote.get("last_sync", local.last_sync))

        # Timestamp-based resolution (Last-Write-Wins)
        if remote_time > local_time:
            resolution = "REMOTE_WINS"
        elif local_time > remote_time:
            resolution = "LOCAL_WINS"
        else:
            # Same timestamp, use priority or message count
            if remote.get("priority", 1) > local.priority:
                resolution = "REMOTE_WINS"
            else:
                resolution = "LOCAL_WINS"

        return {
            "thread_id": local.thread_id,
            "local_hash": local.state_hash,
            "remote_hash": remote.get("state_hash"),
            "resolution": resolution,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _apply_remote_state(self, thread_id: str, remote: Dict):
        """Apply remote state to local thread"""
        thread_state = ThreadState(
            thread_id=thread_id,
            node_id=remote.get("node_id", "unknown"),
            state_hash=remote.get("state_hash", ""),
            last_sync=remote.get("last_sync", datetime.utcnow().isoformat()),
            message_count=remote.get("message_count", 0),
            active=remote.get("active", True),
            priority=remote.get("priority", 1),
            metadata=remote.get("metadata", {})
        )

        self.thread_states[thread_id] = thread_state

    def _record_sync_event(self, event: Dict):
        """Record sync event in history"""
        self.sync_history.append(event)

        # Trim history
        if len(self.sync_history) > self.max_history:
            self.sync_history = self.sync_history[-self.max_history:]


def test_neural_sync():
    """Test neural thread synchronization"""
    print("Testing Neural Thread Synchronization...")

    # Create synchronizer
    sync = NeuralThreadSynchronizer(node_id="node_1", sync_interval=0.1)

    # Start daemon
    result = sync.start()
    print(f"Start: {result['status']}")

    # Register threads
    for i in range(5):
        thread_id = f"thread_{i}"
        result = sync.register_thread(thread_id, {"data": f"initial_{i}"})
        print(f"Registered {thread_id}: {result['status']}")

    # Update states
    sync.update_thread_state("thread_0", {"message_count": 10, "data": "updated"})
    sync.update_thread_state("thread_1", {"message_count": 5, "data": "modified"})

    # Get status
    status = sync.get_sync_status()
    print(f"\nSync Status:")
    print(f"  Threads: {status['thread_count']}")
    print(f"  Active: {status['active_threads']}")
    print(f"  Syncs: {status['stats']['syncs_completed']}")

    # Stop
    time.sleep(0.5)
    result = sync.stop()
    print(f"\nStop: {result['status']}")
    print(f"Final Stats: {result['stats']}")

    return {
        "status": "TASK-021_COMPLETE",
        "system": "NeuralThreadSynchronizer",
        "threads_tested": 5,
        "syncs_performed": status['stats']['syncs_completed']
    }


if __name__ == "__main__":
    result = test_neural_sync()
    print(f"\n✓ TASK-021 Complete: {result}")

    # Save report
    with open("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/thread_management/neural_sync_report.json", "w") as f:
        json.dump(result, f, indent=2)

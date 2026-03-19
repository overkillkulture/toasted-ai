"""
TASK-060: Peer Communication Logging Optimizer
Optimizes logging of peer-to-peer communications with compression and indexing
"""

import json
import time
import threading
import zlib
import base64
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
import hashlib


@dataclass
class CommunicationLog:
    """Log entry for peer communication"""
    log_id: str
    sender_id: str
    receiver_id: str
    message_type: str
    payload_hash: str
    size_bytes: int
    compressed: bool
    timestamp: str
    metadata: Dict = None


class PeerCommunicationLogger:
    """
    Optimized peer communication logging with:
    - Automatic compression for large messages
    - Fast indexing by peer, type, and time
    - Efficient storage and retrieval
    - Real-time statistics
    """

    def __init__(self, compression_threshold: int = 1024, max_logs: int = 100000):
        self.compression_threshold = compression_threshold  # Compress if > 1KB
        self.max_logs = max_logs

        # Storage
        self.logs: deque = deque(maxlen=max_logs)
        self.compressed_payloads: Dict[str, bytes] = {}  # hash -> compressed data

        # Indexes
        self.peer_index: Dict[str, List[str]] = defaultdict(list)  # peer_id -> log_ids
        self.type_index: Dict[str, List[str]] = defaultdict(list)  # msg_type -> log_ids
        self.time_index: Dict[str, List[str]] = defaultdict(list)  # hour -> log_ids

        # Statistics
        self.stats = {
            "total_logs": 0,
            "total_bytes": 0,
            "compressed_bytes": 0,
            "compression_ratio": 0.0,
            "logs_compressed": 0,
            "unique_peers": 0,
            "unique_types": 0
        }

        # Real-time metrics
        self.realtime = {
            "logs_per_second": 0.0,
            "bytes_per_second": 0.0,
            "storage_efficiency": 0.0
        }

        self.lock = threading.Lock()
        self.last_stats_update = time.time()

    def log_communication(self, sender_id: str, receiver_id: str,
                         message_type: str, payload: Dict,
                         metadata: Dict = None) -> Dict:
        """Log a peer communication"""
        start_time = time.time()

        # Serialize payload
        payload_str = json.dumps(payload)
        payload_bytes = payload_str.encode('utf-8')
        size_bytes = len(payload_bytes)

        # Compute hash
        payload_hash = hashlib.sha256(payload_bytes).hexdigest()[:16]

        # Compress if needed
        compressed = False
        stored_size = size_bytes

        if size_bytes > self.compression_threshold:
            compressed_data = zlib.compress(payload_bytes, level=6)
            self.compressed_payloads[payload_hash] = compressed_data
            stored_size = len(compressed_data)
            compressed = True

        # Create log entry
        log_id = f"log_{int(time.time() * 1000000)}"

        log_entry = CommunicationLog(
            log_id=log_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_type=message_type,
            payload_hash=payload_hash,
            size_bytes=size_bytes,
            compressed=compressed,
            timestamp=datetime.utcnow().isoformat(),
            metadata=metadata or {}
        )

        with self.lock:
            # Store log
            self.logs.append(log_entry)

            # Update indexes
            self._update_indexes(log_entry)

            # Update statistics
            self.stats["total_logs"] += 1
            self.stats["total_bytes"] += size_bytes
            self.stats["compressed_bytes"] += stored_size

            if compressed:
                self.stats["logs_compressed"] += 1

            # Update compression ratio
            if self.stats["total_bytes"] > 0:
                self.stats["compression_ratio"] = (
                    self.stats["compressed_bytes"] / self.stats["total_bytes"]
                )

            # Update unique counts
            self.stats["unique_peers"] = len(self.peer_index)
            self.stats["unique_types"] = len(self.type_index)

            # Update realtime metrics
            self._update_realtime_metrics()

        latency = time.time() - start_time

        return {
            "status": "LOGGED",
            "log_id": log_id,
            "size_bytes": size_bytes,
            "stored_bytes": stored_size,
            "compressed": compressed,
            "compression_ratio": stored_size / size_bytes if compressed else 1.0,
            "latency": latency,
            "timestamp": log_entry.timestamp
        }

    def get_logs_by_peer(self, peer_id: str, limit: int = 100) -> List[Dict]:
        """Get logs involving specific peer"""
        with self.lock:
            log_ids = self.peer_index.get(peer_id, [])
            logs = [log for log in self.logs if log.log_id in log_ids[-limit:]]
            return [asdict(log) for log in logs]

    def get_logs_by_type(self, message_type: str, limit: int = 100) -> List[Dict]:
        """Get logs by message type"""
        with self.lock:
            log_ids = self.type_index.get(message_type, [])
            logs = [log for log in self.logs if log.log_id in log_ids[-limit:]]
            return [asdict(log) for log in logs]

    def get_logs_by_timerange(self, start_time: str, end_time: str) -> List[Dict]:
        """Get logs within time range"""
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)

        with self.lock:
            matching_logs = [
                log for log in self.logs
                if start_dt <= datetime.fromisoformat(log.timestamp) <= end_dt
            ]
            return [asdict(log) for log in matching_logs]

    def get_communication_stats(self, peer_id: Optional[str] = None) -> Dict:
        """Get communication statistics"""
        with self.lock:
            if peer_id:
                # Stats for specific peer
                peer_logs = [log for log in self.logs if
                           log.sender_id == peer_id or log.receiver_id == peer_id]

                if not peer_logs:
                    return {
                        "peer_id": peer_id,
                        "status": "NO_DATA"
                    }

                total_bytes = sum(log.size_bytes for log in peer_logs)
                compressed_count = sum(1 for log in peer_logs if log.compressed)

                return {
                    "peer_id": peer_id,
                    "total_logs": len(peer_logs),
                    "total_bytes": total_bytes,
                    "compressed_logs": compressed_count,
                    "avg_message_size": total_bytes / len(peer_logs),
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                # Global stats
                return {
                    "global": True,
                    "stats": self.stats.copy(),
                    "realtime": self.realtime.copy(),
                    "timestamp": datetime.utcnow().isoformat()
                }

    def get_peer_interactions(self, peer_id: str) -> Dict:
        """Get interaction summary for peer"""
        with self.lock:
            peer_logs = [log for log in self.logs if
                        log.sender_id == peer_id or log.receiver_id == peer_id]

            if not peer_logs:
                return {
                    "peer_id": peer_id,
                    "status": "NO_DATA"
                }

            # Count interactions by other peer
            interactions = defaultdict(lambda: {"sent": 0, "received": 0, "bytes": 0})

            for log in peer_logs:
                if log.sender_id == peer_id:
                    other_peer = log.receiver_id
                    interactions[other_peer]["sent"] += 1
                else:
                    other_peer = log.sender_id
                    interactions[other_peer]["received"] += 1

                interactions[other_peer]["bytes"] += log.size_bytes

            # Message types
            type_counts = defaultdict(int)
            for log in peer_logs:
                type_counts[log.message_type] += 1

            return {
                "peer_id": peer_id,
                "total_communications": len(peer_logs),
                "interactions": dict(interactions),
                "message_types": dict(type_counts),
                "timestamp": datetime.utcnow().isoformat()
            }

    def optimize_storage(self) -> Dict:
        """Optimize storage by removing old logs and cleaning up"""
        with self.lock:
            initial_logs = len(self.logs)
            initial_payloads = len(self.compressed_payloads)

            # Find payload hashes still in use
            active_hashes = {log.payload_hash for log in self.logs if log.compressed}

            # Remove unused compressed payloads
            removed_payloads = 0
            for hash_key in list(self.compressed_payloads.keys()):
                if hash_key not in active_hashes:
                    del self.compressed_payloads[hash_key]
                    removed_payloads += 1

            # Rebuild indexes (they auto-trim via deque)
            self._rebuild_indexes()

            return {
                "status": "OPTIMIZED",
                "logs_retained": len(self.logs),
                "logs_removed": initial_logs - len(self.logs),
                "payloads_removed": removed_payloads,
                "storage_efficiency": self.realtime["storage_efficiency"],
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_logging_report(self) -> Dict:
        """Generate comprehensive logging report"""
        with self.lock:
            # Top communicators
            peer_activity = defaultdict(int)
            for log in self.logs:
                peer_activity[log.sender_id] += 1
                peer_activity[log.receiver_id] += 1

            top_peers = sorted(
                peer_activity.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]

            # Message type distribution
            type_distribution = defaultdict(int)
            for log in self.logs:
                type_distribution[log.message_type] += 1

            return {
                "report_type": "PEER_COMMUNICATION_LOGGING",
                "timestamp": datetime.utcnow().isoformat(),
                "summary": {
                    "total_logs": self.stats["total_logs"],
                    "total_bytes": self.stats["total_bytes"],
                    "compressed_bytes": self.stats["compressed_bytes"],
                    "compression_ratio": self.stats["compression_ratio"],
                    "storage_savings": 1.0 - self.stats["compression_ratio"],
                    "unique_peers": self.stats["unique_peers"],
                    "unique_types": self.stats["unique_types"]
                },
                "realtime": self.realtime.copy(),
                "top_communicators": [
                    {"peer_id": peer, "communications": count}
                    for peer, count in top_peers
                ],
                "message_types": dict(type_distribution),
                "storage_metrics": {
                    "active_logs": len(self.logs),
                    "compressed_payloads": len(self.compressed_payloads),
                    "max_capacity": self.max_logs
                }
            }

    def _update_indexes(self, log: CommunicationLog):
        """Update indexes for new log"""
        # Peer index
        self.peer_index[log.sender_id].append(log.log_id)
        self.peer_index[log.receiver_id].append(log.log_id)

        # Type index
        self.type_index[log.message_type].append(log.log_id)

        # Time index (by hour)
        log_time = datetime.fromisoformat(log.timestamp)
        hour_key = log_time.strftime("%Y-%m-%d-%H")
        self.time_index[hour_key].append(log.log_id)

    def _rebuild_indexes(self):
        """Rebuild all indexes from current logs"""
        self.peer_index.clear()
        self.type_index.clear()
        self.time_index.clear()

        for log in self.logs:
            self._update_indexes(log)

    def _update_realtime_metrics(self):
        """Update real-time metrics"""
        current_time = time.time()
        time_delta = current_time - self.last_stats_update

        if time_delta > 0:
            # Calculate rates (per second)
            recent_logs = sum(1 for log in self.logs
                            if (current_time - datetime.fromisoformat(log.timestamp).timestamp()) < time_delta)

            self.realtime["logs_per_second"] = recent_logs / time_delta

            # Storage efficiency
            if self.stats["total_bytes"] > 0:
                self.realtime["storage_efficiency"] = (
                    1.0 - (self.stats["compressed_bytes"] / self.stats["total_bytes"])
                )

            self.last_stats_update = current_time


def test_peer_logger():
    """Test peer communication logger"""
    print("Testing Peer Communication Logger...")

    # Create logger
    logger = PeerCommunicationLogger(compression_threshold=100, max_logs=10000)

    # Log communications
    test_comms = [
        ("peer_1", "peer_2", "HANDSHAKE", {"data": "initial connection"}),
        ("peer_2", "peer_1", "ACK", {"status": "connected"}),
        ("peer_1", "peer_3", "DATA_TRANSFER", {"payload": "x" * 200}),  # Should compress
        ("peer_3", "peer_1", "DATA_ACK", {"received": True}),
        ("peer_2", "peer_3", "SYNC", {"state": "synchronized"}),
    ]

    print("\nLogging communications...")
    for sender, receiver, msg_type, payload in test_comms:
        result = logger.log_communication(sender, receiver, msg_type, payload)
        print(f"  {msg_type}: {result['size_bytes']}B -> {result['stored_bytes']}B "
              f"(compressed: {result['compressed']})")

    # Get stats
    stats = logger.get_communication_stats()
    print(f"\nGlobal Statistics:")
    print(f"  Total Logs: {stats['stats']['total_logs']}")
    print(f"  Compression Ratio: {stats['stats']['compression_ratio']:.2%}")
    print(f"  Unique Peers: {stats['stats']['unique_peers']}")

    # Peer interactions
    interactions = logger.get_peer_interactions("peer_1")
    print(f"\nPeer 1 Interactions:")
    print(f"  Total: {interactions['total_communications']}")
    print(f"  With: {list(interactions['interactions'].keys())}")

    # Optimize storage
    opt_result = logger.optimize_storage()
    print(f"\nStorage Optimization: {opt_result['status']}")

    # Generate report
    report = logger.get_logging_report()
    print(f"\nLogging Report:")
    print(f"  Total Logs: {report['summary']['total_logs']}")
    print(f"  Storage Savings: {report['summary']['storage_savings']:.2%}")
    print(f"  Top Communicators: {[p['peer_id'] for p in report['top_communicators'][:3]]}")

    return {
        "status": "TASK-060_COMPLETE",
        "system": "PeerCommunicationLogger",
        "logs_created": len(test_comms),
        "compression_ratio": stats['stats']['compression_ratio'],
        "storage_savings": report['summary']['storage_savings']
    }


if __name__ == "__main__":
    result = test_peer_logger()
    print(f"\n✓ TASK-060 Complete: {result}")

    # Save report
    with open("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/thread_management/peer_logger_report.json", "w") as f:
        json.dump(result, f, indent=2)

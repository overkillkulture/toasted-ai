"""
ToastHash Distributed Hash Table
================================
Peer-to-peer storage network with Kademlia topology and 
content addressing.

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18

Research Sources:
- Kademlia DHT protocol
- Ethereum Swarm DISC
- IPFS content addressing
- HYDRAstor architecture
"""

import hashlib
import time
import threading
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio

class NodeStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    SYNCING = "syncing"

@dataclass
class DHTNode:
    """Represents a node in the DHT network"""
    id: str  # Node ID (160-bit)
    ip: str
    port: int
    status: NodeStatus = NodeStatus.ONLINE
    last_seen: float = field(default_factory=time.time)
    bucket: int = 0  # Kademlia bucket (0-159)
    
    def __post_init__(self):
        if not self.id:
            self.id = self._generate_id()
            
    def _generate_id(self) -> str:
        """Generate random node ID"""
        return hashlib.sha1(str(random.random()).encode()).hexdigest()

@dataclass
class DHTEntry:
    """Content entry in the DHT"""
    key: str  # Content key (SHA-256)
    value: Any
    publisher: str  # Publisher node ID
    created_at: float
    expires_at: float
    replicas: int = 1
    
class DistributedHashTable:
    """
    Distributed Hash Table with Kademlia-style routing
    
    Features:
    - Kademlia-based peer discovery
    - Content-addressed storage
    - Replication and redundancy
    - Offline caching
    - XOR distance metric
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self, node_id: Optional[str] = None):
        self.node_id = node_id or self._generate_node_id()
        self.local_node = DHTNode(
            id=self.node_id,
            ip="127.0.0.1",
            port=8080,
        )
        
        # Routing table (buckets 0-159)
        self.routing_table: Dict[int, List[DHTNode]] = {i: [] for i in range(160)}
        
        # Local storage
        self.local_store: Dict[str, DHTEntry] = {}
        
        # Peer cache
        self.peers: Dict[str, DHTNode] = {}
        
        # Statistics
        self.stats = {
            "puts": 0,
            "gets": 0,
            "queries": 0,
            "peers_discovered": 0,
        }
        
        self._lock = threading.Lock()
        
    def _generate_node_id(self) -> str:
        """Generate unique node ID"""
        data = f"{time.time()}{random.random()}"
        return hashlib.sha1(data.encode()).hexdigest()
        
    def _xor_distance(self, id1: str, id2: str) -> int:
        """Calculate XOR distance between two IDs"""
        # Convert hex to int
        i1 = int(id1, 16)
        i2 = int(id2, 16)
        return i1 ^ i2
        
    def _bucket_index(self, distance: int) -> int:
        """Get bucket index for XOR distance"""
        if distance == 0:
            return 0
        return distance.bit_length() - 1
        
    def add_peer(self, node: DHTNode):
        """Add peer to routing table"""
        with self._lock:
            distance = self._xor_distance(self.node_id, node.id)
            bucket = self._bucket_index(distance)
            
            node.bucket = bucket
            
            # Check if peer already exists
            existing = [n for n in self.routing_table[bucket] if n.id == node.id]
            if existing:
                # Update last seen
                existing[0].last_seen = time.time()
            else:
                # Add to bucket (max 20 per bucket)
                if len(self.routing_table[bucket]) < 20:
                    self.routing_table[bucket].append(node)
                else:
                    # Ping oldest, replace if offline
                    oldest = min(self.routing_table[bucket], key=lambda n: n.last_seen)
                    if oldest.status == NodeStatus.OFFLINE:
                        self.routing_table[bucket].remove(oldest)
                        self.routing_table[bucket].append(node)
                        
            self.peers[node.id] = node
            self.stats["peers_discovered"] = len(self.peers)
            
    def find_peers(self, key: str, k: int = 8) -> List[DHTNode]:
        """Find k closest peers to a key"""
        with self._lock:
            distance = self._xor_distance(self.node_id, key)
            bucket = self._bucket_index(distance)
            
            # Get peers from closest buckets
            candidates = []
            for i in range(bucket, 160):
                candidates.extend(self.routing_table[i])
            for i in range(bucket - 1, -1, -1):
                candidates.extend(self.routing_table[i])
                
            # Sort by distance to key
            candidates.sort(key=lambda n: self._xor_distance(n.id, key))
            
            return candidates[:k]
            
    def put(self, key: str, value: Any, ttl: int = 86400) -> bool:
        """Store value in DHT"""
        with self._lock:
            entry = DHTEntry(
                key=key,
                value=value,
                publisher=self.node_id,
                created_at=time.time(),
                expires_at=time.time() + ttl,
            )
            
            self.local_store[key] = entry
            self.stats["puts"] += 1
            
            # Replicate to closest peers
            peers = self.find_peers(key)
            for peer in peers[:3]:  # Replicate to 3 peers
                self._async_put(peer, entry)
                
            return True
            
    def _async_put(self, peer: DHTNode, entry: DHTEntry):
        """Async put to peer (simulated)"""
        pass  # In real implementation, network call
        
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from DHT"""
        with self._lock:
            self.stats["gets"] += 1
            
            # Check local store first
            if key in self.local_store:
                entry = self.local_store[key]
                if entry.expires_at > time.time():
                    return entry.value
                    
            # Query closest peers
            peers = self.find_peers(key)
            for peer in peers:
                value = self._async_get(peer, key)
                if value:
                    return value
                    
        return None
        
    def _async_get(self, peer: DHTNode, key: str) -> Optional[Any]:
        """Async get from peer (simulated)"""
        return None
        
    def bootstrap(self, bootstrap_nodes: List[Tuple[str, int]]):
        """Bootstrap into DHT network"""
        for ip, port in bootstrap_nodes:
            # Simulate connecting to bootstrap node
            node = DHTNode(
                id=self._generate_node_id(),
                ip=ip,
                port=port,
            )
            self.add_peer(node)
            
    def get_stats(self) -> Dict:
        """Get DHT statistics"""
        with self._lock:
            total_peers = sum(len(bucket) for bucket in self.routing_table.values())
            
            return {
                "node_id": self.node_id,
                "local_entries": len(self.local_store),
                "total_peers": len(self.peers),
                "bucket_distribution": {
                    i: len(self.routing_table[i]) 
                    for i in range(160) if self.routing_table[i]
                },
                "puts": self.stats["puts"],
                "gets": self.stats["gets"],
                "queries": self.stats["queries"],
                "divine_seal": self.DIVINE_SEAL,
            }

def create_dht(node_id: Optional[str] = None) -> DistributedHashTable:
    """Create a new DHT node"""
    return DistributedHashTable(node_id=node_id)

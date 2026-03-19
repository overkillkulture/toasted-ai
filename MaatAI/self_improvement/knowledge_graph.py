"""
KNOWLEDGE GRAPH FOR SELF-IMPROVEMENT
=====================================
Tracks relationships between concepts, errors, and improvements.
"""

import json
import time
from dataclasses import dataclass, field
from typing import Any, Optional
from collections import defaultdict, deque

@dataclass
class KnowledgeNode:
    """Single node in knowledge graph"""
    id: str
    type: str  # concept, error, improvement, pattern
    data: dict
    connections: list[str] = field(default_factory=list)
    weight: float = 1.0
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)

class KnowledgeGraph:
    """
    Knowledge graph for tracking self-improvement learning.
    """
    
    def __init__(self):
        self.nodes: dict[str, KnowledgeNode] = {}
        self.connections: defaultdict[str, list[str]] = defaultdict(list)
        self.type_index: defaultdict[str, set[str]] = defaultdict(set)
        
        # Statistics
        self.stats = {
            "total_nodes": 0,
            "total_connections": 0,
            "types": {}
        }
    
    def add_node(self, node_type: str, data: dict, connections: list[str] = None) -> str:
        """Add a node to the knowledge graph"""
        import hashlib
        
        # Generate ID from content
        content = f"{node_type}:{json.dumps(data, sort_keys=True)}"
        node_id = hashlib.md5(content.encode()).hexdigest()[:12]
        
        if node_id in self.nodes:
            # Update existing node
            self.nodes[node_id].last_accessed = time.time()
            return node_id
        
        # Create new node
        node = KnowledgeNode(
            id=node_id,
            type=node_type,
            data=data,
            connections=connections or []
        )
        
        self.nodes[node_id] = node
        self.type_index[node_type].add(node_id)
        
        # Add connections
        if connections:
            for conn_id in connections:
                self.connect_nodes(node_id, conn_id)
        
        self.stats["total_nodes"] += 1
        self._update_stats()
        
        return node_id
    
    def connect_nodes(self, node_id1: str, node_id2: str):
        """Connect two nodes"""
        if node_id1 not in self.nodes or node_id2 not in self.nodes:
            return
        
        if node_id2 not in self.nodes[node_id1].connections:
            self.nodes[node_id1].connections.append(node_id2)
        
        if node_id1 not in self.nodes[node_id2].connections:
            self.nodes[node_id2].connections.append(node_id1)
        
        self.connections[node_id1].append(node_id2)
        self.stats["total_connections"] += 1
    
    def find_related(self, node_id: str, depth: int = 1) -> list[KnowledgeNode]:
        """Find related nodes"""
        if node_id not in self.nodes:
            return []
        
        related = []
        visited = set()
        
        def traverse(current_id: str, current_depth: int):
            if current_depth > depth or current_id in visited:
                return
            
            visited.add(current_id)
            
            for conn_id in self.nodes[current_id].connections:
                related.append(self.nodes[conn_id])
                traverse(conn_id, current_depth + 1)
        
        traverse(node_id, 0)
        return related
    
    def find_by_type(self, node_type: str) -> list[KnowledgeNode]:
        """Find all nodes of a type"""
        node_ids = self.type_index.get(node_type, set())
        return [self.nodes[nid] for nid in node_ids]
    
    def search(self, query: str) -> list[KnowledgeNode]:
        """Search nodes by data"""
        results = []
        query_lower = query.lower()
        
        for node in self.nodes.values():
            # Search in data
            data_str = json.dumps(node.data).lower()
            if query_lower in data_str:
                results.append(node)
        
        return results
    
    def get_central_nodes(self, limit: int = 10) -> list[tuple[str, int]]:
        """Get most connected nodes"""
        centrality = []
        
        for node_id, node in self.nodes.items():
            centrality.append((node_id, len(node.connections)))
        
        centrality.sort(key=lambda x: x[1], reverse=True)
        return centrality[:limit]
    
    def _update_stats(self):
        """Update statistics"""
        self.stats["types"] = {
            node_type: len(node_ids)
            for node_type, node_ids in self.type_index.items()
        }
    
    def export(self) -> dict:
        """Export knowledge graph"""
        return {
            "nodes": {
                nid: {
                    "type": node.type,
                    "data": node.data,
                    "connections": node.connections,
                    "weight": node.weight,
                    "created_at": node.created_at
                }
                for nid, node in self.nodes.items()
            },
            "stats": self.stats,
            "exported_at": time.time()
        }
    
    def import_data(self, data: dict):
        """Import knowledge graph"""
        for nid, node_data in data.get("nodes", {}).items():
            node = KnowledgeNode(
                id=nid,
                type=node_data["type"],
                data=node_data["data"],
                connections=node_data.get("connections", []),
                weight=node_data.get("weight", 1.0),
                created_at=node_data.get("created_at", time.time())
            )
            self.nodes[nid] = node
            self.type_index[node.type].add(nid)
        
        self.stats = data.get("stats", {})
        self._update_stats()


# Singleton
_knowledge_graph: Optional[KnowledgeGraph] = None

def get_knowledge_graph() -> KnowledgeGraph:
    global _knowledge_graph
    if _knowledge_graph is None:
        _knowledge_graph = KnowledgeGraph()
    return _knowledge_graph

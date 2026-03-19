"""
Deep Memory Module - Persistent Kernel State
Stores and retrieves deep memory patterns for MaatAI.
"""
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class DeepMemory:
    """
    Persistent deep memory for kernel-level operations.
    Stores holographic patterns, quantum states, and learned knowledge.
    """
    
    def __init__(self, memory_path: str = "/home/workspace/MaatAI/kernel/deep_memory_store"):
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # Memory layers
        self.layers = {
            'surface': {},      # Temporary, session-level
            'semantic': {},     # Meaning-based associations
            'procedural': {},   # How-to knowledge
            'episodic': {},     # Event memories
            'quantum': {},      # Quantum state memories
            'holographic': {}   # Deep holographic patterns
        }
        
        # Load existing memories
        self._load_memories()
        
        # Memory statistics
        self.stats = {
            'total_memories': 0,
            'layer_counts': {},
            'last_access': None,
            'access_count': 0
        }
        
        self._update_stats()
    
    def _load_memories(self):
        """Load memories from persistent storage."""
        for layer_name in self.layers:
            layer_file = self.memory_path / f"{layer_name}.jsonl"
            if layer_file.exists():
                with open(layer_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            memory = json.loads(line)
                            memory_id = memory.get('id')
                            if memory_id:
                                self.layers[layer_name][memory_id] = memory
    
    def _save_memory(self, layer_name: str, memory_id: str, memory: Dict):
        """Save a memory to persistent storage."""
        layer_file = self.memory_path / f"{layer_name}.jsonl"
        with open(layer_file, 'a') as f:
            f.write(json.dumps(memory) + '\n')
    
    def _generate_memory_id(self, content: Any) -> str:
        """Generate a unique memory ID."""
        content_str = json.dumps(content, sort_keys=True)
        timestamp = datetime.utcnow().isoformat()
        return hashlib.sha256(f"{content_str}_{timestamp}".encode()).hexdigest()[:16]
    
    def store(self, layer: str, key: str, value: Any, 
              metadata: Dict = None) -> str:
        """
        Store a memory in the specified layer.
        
        Args:
            layer: Memory layer (surface, semantic, procedural, episodic, quantum, holographic)
            key: Memory key
            value: Memory value
            metadata: Optional metadata
        
        Returns:
            Memory ID
        """
        if layer not in self.layers:
            layer = 'surface'  # Default to surface
        
        memory_id = self._generate_memory_id(value)
        
        memory = {
            'id': memory_id,
            'key': key,
            'value': value,
            'metadata': metadata or {},
            'stored_at': datetime.utcnow().isoformat(),
            'access_count': 0
        }
        
        self.layers[layer][memory_id] = memory
        self._save_memory(layer, memory_id, memory)
        
        self.stats['access_count'] += 1
        self.stats['last_access'] = datetime.utcnow().isoformat()
        
        return memory_id
    
    def retrieve(self, layer: str, key: str = None, memory_id: str = None) -> Optional[Dict]:
        """
        Retrieve a memory from the specified layer.
        
        Args:
            layer: Memory layer
            key: Memory key (optional)
            memory_id: Memory ID (optional)
        
        Returns:
            Memory dict or None
        """
        if layer not in self.layers:
            return None
        
        # Search by memory_id first
        if memory_id and memory_id in self.layers[layer]:
            memory = self.layers[layer][memory_id]
            memory['access_count'] += 1
            return memory
        
        # Search by key
        if key:
            for memory in self.layers[layer].values():
                if memory.get('key') == key:
                    memory['access_count'] += 1
                    return memory
        
        return None
    
    def search(self, query: str, layers: List[str] = None) -> List[Dict]:
        """
        Search memories across layers.
        
        Args:
            query: Search query
            layers: Layers to search (None = all)
        
        Returns:
            List of matching memories
        """
        results = []
        search_layers = layers or list(self.layers.keys())
        
        query_lower = query.lower()
        
        for layer_name in search_layers:
            if layer_name not in self.layers:
                continue
            
            for memory in self.layers[layer_name].values():
                # Search in key, value, and metadata
                searchable = f"{memory.get('key', '')} {json.dumps(memory.get('value', ''))} {json.dumps(memory.get('metadata', {}))}"
                
                if query_lower in searchable.lower():
                    results.append({
                        'layer': layer_name,
                        'memory': memory,
                        'relevance': 1.0  # Simple relevance score
                    })
        
        return results
    
    def forget(self, layer: str, memory_id: str) -> bool:
        """
        Remove a memory from the specified layer.
        
        Args:
            layer: Memory layer
            memory_id: Memory ID to remove
        
        Returns:
            True if removed, False if not found
        """
        if layer not in self.layers:
            return False
        
        if memory_id in self.layers[layer]:
            del self.layers[layer][memory_id]
            # Note: This doesn't remove from persistent storage
            # In production, would need to rebuild the layer file
            return True
        
        return False
    
    def get_layer_stats(self, layer: str) -> Dict:
        """Get statistics for a memory layer."""
        if layer not in self.layers:
            return {'error': f'Layer {layer} not found'}
        
        memories = self.layers[layer]
        
        return {
            'layer': layer,
            'memory_count': len(memories),
            'total_access_count': sum(m.get('access_count', 0) for m in memories.values()),
            'oldest_memory': min(
                (m.get('stored_at', '') for m in memories.values()),
                default=None
            ),
            'newest_memory': max(
                (m.get('stored_at', '') for m in memories.values()),
                default=None
            )
        }
    
    def _update_stats(self):
        """Update memory statistics."""
        self.stats['total_memories'] = sum(
            len(memories) for memories in self.layers.values()
        )
        
        self.stats['layer_counts'] = {
            layer: len(memories) 
            for layer, memories in self.layers.items()
        }
    
    def export_memories(self, output_path: str = None) -> Dict:
        """Export all memories to a single file."""
        export_path = output_path or str(self.memory_path / "memory_export.json")
        
        export_data = {
            'exported_at': datetime.utcnow().isoformat(),
            'layers': self.layers,
            'stats': self.stats
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return {
            'export_path': export_path,
            'total_memories': self.stats['total_memories']
        }
    
    def import_memories(self, import_path: str, merge: bool = True) -> Dict:
        """
        Import memories from an export file.
        
        Args:
            import_path: Path to export file
            merge: If True, merge with existing. If False, replace.
        
        Returns:
            Import statistics
        """
        with open(import_path, 'r') as f:
            import_data = json.load(f)
        
        imported_count = 0
        
        for layer_name, memories in import_data.get('layers', {}).items():
            if layer_name not in self.layers:
                continue
            
            if not merge:
                self.layers[layer_name] = {}
            
            for memory_id, memory in memories.items():
                self.layers[layer_name][memory_id] = memory
                imported_count += 1
        
        self._update_stats()
        
        return {
            'imported_count': imported_count,
            'merge_mode': merge
        }


# Singleton instance
_deep_memory_instance = None

def get_deep_memory() -> DeepMemory:
    """Get the singleton deep memory instance."""
    global _deep_memory_instance
    if _deep_memory_instance is None:
        _deep_memory_instance = DeepMemory()
    return _deep_memory_instance

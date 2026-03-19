"""
Refractal Memory Storage
Stores data in recursive fractal patterns using GodCode I/O
"""

import json
import hashlib
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
sys.path.insert(0, '/home/workspace/MaatAI')
from memory_compression.godcode_encoder.compression_core import GodCodeCompressor, DynamicMemorySparsification


class RefractalMemoryLayer:
    """A single layer in the refractal memory structure."""
    
    def __init__(self, depth: int = 0):
        self.depth = depth
        self.data = {}
        self.children: List['RefractalMemoryLayer'] = []
        self.hash = None
        self.created = datetime.utcnow().isoformat()
    
    def store(self, key: str, value: Any):
        """Store data in this layer."""
        self.data[key] = value
        self._update_hash()
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve data from this layer or children."""
        if key in self.data:
            return self.data[key]
        
        for child in self.children:
            result = child.retrieve(key)
            if result is not None:
                return result
        
        return None
    
    def add_child(self) -> 'RefractalMemoryLayer':
        """Add a child layer."""
        child = RefractalMemoryLayer(depth=self.depth + 1)
        self.children.append(child)
        return child
    
    def _update_hash(self):
        """Update hash based on contents."""
        content = json.dumps(self.data, sort_keys=True, default=str)
        self.hash = hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'depth': self.depth,
            'data': self.data,
            'hash': self.hash,
            'created': self.created,
            'children': [c.to_dict() for c in self.children]
        }


class RefractalMemoryStorage:
    """
    Recursive fractal memory storage with three tiers:
    - Temporary Memory (fast, short-term)
    - Long-term Memory (compressed, persistent)
    - GodCode I/O (recursive encoding)
    """
    
    def __init__(self, storage_path: str = "/home/workspace/MaatAI/memory_compression/storage"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # Three-tier memory
        self.temp_memory = RefractalMemoryLayer(depth=0)  # Fast, temporary
        self.long_memory = RefractalMemoryLayer(depth=0)  # Compressed, persistent
        self.godcode_io = RefractalMemoryLayer(depth=0)   # Recursive encoding
        
        # Compression engine
        self.compressor = GodCodeCompressor(compression_level=9)
        self.dms = DynamicMemorySparsification(sparsity_threshold=0.3)
        
        # Statistics
        self.stats = {
            'temp_stores': 0,
            'temp_retrieves': 0,
            'long_stores': 0,
            'long_retrieves': 0,
            'godcode_stores': 0,
            'godcode_retrieves': 0,
            'compression_saved_bytes': 0
        }
    
    def store_temp(self, key: str, value: Any) -> Dict:
        """Store in temporary memory (fast access)."""
        self.temp_memory.store(key, value)
        self.stats['temp_stores'] += 1
        
        return {
            'status': 'stored',
            'tier': 'temporary',
            'key': key,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def retrieve_temp(self, key: str) -> Optional[Any]:
        """Retrieve from temporary memory."""
        self.stats['temp_retrieves'] += 1
        return self.temp_memory.retrieve(key)
    
    def store_long(self, key: str, value: Any) -> Dict:
        """Store in long-term memory (compressed)."""
        
        # Compress before storing
        compressed = self.compressor.compress_data(value)
        
        # Apply DMS
        if isinstance(value, dict):
            sparsified = self.dms.sparsify(value)
            value_to_store = sparsified['sparsified_memory']
        else:
            value_to_store = compressed['compressed']
        
        self.long_memory.store(key, {
            'compressed_data': compressed['compressed'],
            'original_size': compressed['original_size'],
            'compressed_size': compressed['compressed_size'],
            'compression_ratio': compressed['compression_ratio'],
            'stored_at': datetime.utcnow().isoformat()
        })
        
        self.stats['long_stores'] += 1
        self.stats['compression_saved_bytes'] += (
            compressed['original_size'] - compressed['compressed_size']
        )
        
        return {
            'status': 'stored',
            'tier': 'long_term',
            'key': key,
            'compression_ratio': compressed['compression_ratio'],
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def retrieve_long(self, key: str) -> Optional[Any]:
        """Retrieve from long-term memory (decompress)."""
        self.stats['long_retrieves'] += 1
        
        stored = self.long_memory.retrieve(key)
        if stored is None:
            return None
        
        # Decompress
        decompressed = self.compressor.decompress_data({
            'compressed': stored['compressed_data']
        })
        
        return decompressed
    
    def store_godcode(self, key: str, value: Any, depth: int = 3) -> Dict:
        """
        Store using recursive GodCode I/O.
        Creates nested fractal layers of compressed data.
        """
        
        current_layer = self.godcode_io
        
        # Create nested layers for depth
        for d in range(depth):
            current_layer = current_layer.add_child()
        
        # Apply GodCode compression at each layer
        compressed_value = value
        for d in range(depth + 1):
            compressed = self.compressor.compress_data(compressed_value)
            compressed_value = compressed['compressed']
        
        # Store at deepest layer
        current_layer.store(key, {
            'godcode_data': compressed_value,
            'depth': depth,
            'original_type': type(value).__name__,
            'stored_at': datetime.utcnow().isoformat()
        })
        
        self.stats['godcode_stores'] += 1
        
        return {
            'status': 'stored',
            'tier': 'godcode_io',
            'key': key,
            'depth': depth,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def retrieve_godcode(self, key: str, depth: int = 3) -> Optional[Any]:
        """Retrieve from GodCode I/O (recursive decompression)."""
        self.stats['godcode_retrieves'] += 1
        
        # Navigate to deepest layer
        current_layer = self.godcode_io
        for d in range(depth):
            if current_layer.children:
                current_layer = current_layer.children[0]
            else:
                return None
        
        stored = current_layer.retrieve(key)
        if stored is None:
            return None
        
        # Reverse compression at each layer
        decompressed = stored['godcode_data']
        for d in range(depth + 1):
            try:
                decompressed = self.compressor.decompress_data({
                    'compressed': decompressed
                })
            except:
                break
        
        return decompressed
    
    def get_memory_usage(self) -> Dict:
        """Get current memory usage statistics."""
        import sys
        
        temp_size = sys.getsizeof(self.temp_memory.to_dict())
        long_size = sys.getsizeof(self.long_memory.to_dict())
        godcode_size = sys.getsizeof(self.godcode_io.to_dict())
        
        return {
            'temp_memory_bytes': temp_size,
            'long_memory_bytes': long_size,
            'godcode_memory_bytes': godcode_size,
            'total_bytes': temp_size + long_size + godcode_size,
            'stats': self.stats.copy()
        }
    
    def save_to_disk(self):
        """Save all memory to disk."""
        memory_state = {
            'temp_memory': self.temp_memory.to_dict(),
            'long_memory': self.long_memory.to_dict(),
            'godcode_io': self.godcode_io.to_dict(),
            'stats': self.stats,
            'saved_at': datetime.utcnow().isoformat()
        }
        
        filepath = os.path.join(self.storage_path, 'refractal_memory.json')
        with open(filepath, 'w') as f:
            json.dump(memory_state, f, indent=2, default=str)
        
        return filepath
    
    def load_from_disk(self):
        """Load memory from disk."""
        filepath = os.path.join(self.storage_path, 'refractal_memory.json')
        
        if not os.path.exists(filepath):
            return False
        
        with open(filepath, 'r') as f:
            memory_state = json.load(f)
        
        # Restore state
        self.stats = memory_state.get('stats', self.stats)
        
        return True
    
    def clear_temp(self):
        """Clear temporary memory."""
        self.temp_memory = RefractalMemoryLayer(depth=0)
    
    def optimize(self):
        """Optimize memory usage."""
        
        # Sparsify long-term memory
        if self.long_memory.data:
            sparsified = self.dms.sparsify(self.long_memory.data)
            self.long_memory.data = sparsified['sparsified_memory']
        
        # Clear old temporary memory
        self.clear_temp()
        
        return {
            'status': 'optimized',
            'timestamp': datetime.utcnow().isoformat()
        }


if __name__ == '__main__':
    print("=" * 60)
    print("REFRACTAL MEMORY STORAGE")
    print("=" * 60)
    
    storage = RefractalMemoryStorage()
    
    # Test temporary memory
    print("\n[1] Testing Temporary Memory...")
    storage.store_temp('session_1', {'user': 't0st3d', 'status': 'active'})
    result = storage.retrieve_temp('session_1')
    print(f"  Stored and retrieved: {result}")
    
    # Test long-term memory
    print("\n[2] Testing Long-Term Memory...")
    long_data = {
        'config': {'debug': True, 'mode': 'production'},
        'history': ['entry1', 'entry2', 'entry3', 'entry4', 'entry5']
    }
    store_result = storage.store_long('config_backup', long_data)
    print(f"  Compression ratio: {store_result['compression_ratio']:.1%}")
    
    # Test GodCode I/O
    print("\n[3] Testing GodCode I/O...")
    godcode_data = {'recursive': 'data', 'nested': {'deep': {'value': 42}}}
    store_result = storage.store_godcode('recursive_test', godcode_data, depth=3)
    print(f"  Stored at depth: {store_result['depth']}")
    
    # Memory usage
    print("\n[4] Memory Usage:")
    usage = storage.get_memory_usage()
    print(f"  Total memory: {usage['total_bytes']} bytes")
    print(f"  Compression saved: {usage['stats']['compression_saved_bytes']} bytes")
    
    # Optimize
    print("\n[5] Optimizing...")
    storage.optimize()
    print("  Memory optimized")
    
    # Save
    filepath = storage.save_to_disk()
    print(f"\n[6] Saved to: {filepath}")

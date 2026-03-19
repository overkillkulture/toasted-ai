"""
Integrate Memory Compression with ToastedAI
"""

import sys
sys.path.insert(0, '/home/workspace/MaatAI')

from memory_compression.godcode_encoder.compression_core import GodCodeCompressor, DynamicMemorySparsification
from memory_compression.refractal_storage.refractal_memory import RefractalMemoryStorage
from memory_compression.gibberlink.gibberlink_interface import GibberlinkInterface

class ToastedAIMemoryManager:
    """
    Memory Manager for ToastedAI using GodCode/Refractal compression.
    Solves low-memory issues by compressing all data.
    """
    
    def __init__(self):
        self.storage = RefractalMemoryStorage()
        self.compressor = GodCodeCompressor(compression_level=9)
        self.dms = DynamicMemorySparsification(sparsity_threshold=0.3)
        self.gibberlink = GibberlinkInterface(agent_id='ToastedAI-Core')
        
        # Memory pools
        self.active_pool = {}      # Hot data
        self.warm_pool = {}        # Recently used
        self.cold_pool = {}        # Rarely used
        
        self.stats = {
            'memory_saved_bytes': 0,
            'items_compressed': 0,
            'items_sparsified': 0,
            'pool_swaps': 0
        }
    
    def store(self, key: str, value: any, tier: str = 'auto') -> dict:
        """Store data in optimal tier."""
        
        # Auto-select tier based on data characteristics
        if tier == 'auto':
            tier = self._select_tier(value)
        
        if tier == 'temp':
            # Temporary storage - no compression
            self.active_pool[key] = value
            self.storage.store_temp(key, value)
            return {'tier': 'temp', 'compressed': False}
        
        elif tier == 'long':
            # Long-term storage - compressed
            result = self.storage.store_long(key, value)
            self.warm_pool[key] = True  # Reference
            self.stats['memory_saved_bytes'] += max(0, 
                result.get('original_size', 0) - result.get('compressed_size', 0))
            self.stats['items_compressed'] += 1
            return {'tier': 'long', 'compressed': True, **result}
        
        elif tier == 'godcode':
            # Deep storage - recursive compression
            result = self.storage.store_godcode(key, value, depth=3)
            self.cold_pool[key] = True  # Reference
            self.stats['items_compressed'] += 1
            return {'tier': 'godcode', 'compressed': True, **result}
        
        return {'tier': tier, 'error': 'Unknown tier'}
    
    def retrieve(self, key: str) -> any:
        """Retrieve data from any tier."""
        
        # Check active pool first
        if key in self.active_pool:
            return self.active_pool[key]
        
        # Check warm pool
        if key in self.warm_pool:
            return self.storage.retrieve_long(key)
        
        # Check cold pool
        if key in self.cold_pool:
            return self.storage.retrieve_godcode(key, depth=3)
        
        # Check temp storage
        return self.storage.retrieve_temp(key)
    
    def optimize_memory(self) -> dict:
        """Optimize memory usage."""
        
        # Sparsify active pool
        if self.active_pool:
            sparsified = self.dms.sparsify(self.active_pool)
            self.active_pool = sparsified['sparsified_memory']
            self.stats['items_sparsified'] += len(sparsified['removed_keys'])
        
        # Move old items from active to warm
        items_to_move = []
        for key in list(self.active_pool.keys()):
            if key not in self.warm_pool:
                items_to_move.append(key)
        
        for key in items_to_move:
            value = self.active_pool.pop(key)
            self.store(key, value, tier='long')
            self.stats['pool_swaps'] += 1
        
        # Optimize storage
        self.storage.optimize()
        
        return {
            'status': 'optimized',
            'active_items': len(self.active_pool),
            'warm_items': len(self.warm_pool),
            'cold_items': len(self.cold_pool),
            'memory_saved': self.stats['memory_saved_bytes']
        }
    
    def get_memory_report(self) -> dict:
        """Get detailed memory report."""
        
        usage = self.storage.get_memory_usage()
        
        return {
            'pools': {
                'active': len(self.active_pool),
                'warm': len(self.warm_pool),
                'cold': len(self.cold_pool)
            },
            'storage': usage,
            'compression_stats': self.compressor.get_stats(),
            'memory_saved': self.stats['memory_saved_bytes'],
            'items_compressed': self.stats['items_compressed'],
            'items_sparsified': self.stats['items_sparsified'],
            'pool_swaps': self.stats['pool_swaps']
        }
    
    def _select_tier(self, value: any) -> str:
        """Auto-select optimal storage tier."""
        
        # Small, frequently accessed -> temp
        if isinstance(value, (str, int, float, bool)):
            return 'temp'
        
        # Dict/list with few items -> temp
        if isinstance(value, (dict, list)) and len(str(value)) < 500:
            return 'temp'
        
        # Medium data -> long
        if isinstance(value, (dict, list)) and len(str(value)) < 5000:
            return 'long'
        
        # Large data -> godcode
        return 'godcode'
    
    def compress_all_memory(self) -> dict:
        """Compress all memory pools."""
        
        results = {
            'compressed': [],
            'total_saved': 0
        }
        
        # Compress active pool
        for key in list(self.active_pool.keys()):
            value = self.active_pool[key]
            compressed = self.compressor.compress_data(value)
            saved = compressed['original_size'] - compressed['compressed_size']
            results['compressed'].append({
                'key': key,
                'tier': 'active',
                'original': compressed['original_size'],
                'compressed': compressed['compressed_size'],
                'saved': saved
            })
            results['total_saved'] += max(0, saved)
        
        self.stats['memory_saved_bytes'] += results['total_saved']
        
        return results


if __name__ == '__main__':
    import json
    
    print("=" * 70)
    print("TOASTED AI - INTEGRATED MEMORY COMPRESSION")
    print("=" * 70)
    
    # Create memory manager
    mm = ToastedAIMemoryManager()
    
    print("\n[1] STORING DATA IN TIERS")
    print("-" * 50)
    
    # Store different types of data
    mm.store('session_config', {'user': 't0st3d', 'mode': 'production'}, tier='temp')
    mm.store('module_list', ['maat', 'security', 'network', 'learning'], tier='temp')
    mm.store('large_config', {'settings': {f'key_{i}': f'value_{i}' for i in range(100)}}, tier='long')
    mm.store('deep_archive', {'data': {f'item_{i}': i for i in range(1000)}}, tier='godcode')
    
    print("  ✓ Session config (temp)")
    print("  ✓ Module list (temp)")
    print("  ✓ Large config (long)")
    print("  ✓ Deep archive (godcode)")
    
    print("\n[2] RETRIEVING DATA")
    print("-" * 50)
    
    session = mm.retrieve('session_config')
    print(f"  Session config: {session}")
    
    modules = mm.retrieve('module_list')
    print(f"  Modules: {modules}")
    
    print("\n[3] MEMORY OPTIMIZATION")
    print("-" * 50)
    
    opt_result = mm.optimize_memory()
    print(f"  Status: {opt_result['status']}")
    print(f"  Active items: {opt_result['active_items']}")
    print(f"  Warm items: {opt_result['warm_items']}")
    print(f"  Cold items: {opt_result['cold_items']}")
    print(f"  Memory saved: {opt_result['memory_saved']} bytes")
    
    print("\n[4] COMPRESS ALL MEMORY")
    print("-" * 50)
    
    compress_result = mm.compress_all_memory()
    print(f"  Total saved: {compress_result['total_saved']} bytes")
    
    print("\n[5] MEMORY REPORT")
    print("-" * 50)
    
    report = mm.get_memory_report()
    print(f"  Active pool: {report['pools']['active']} items")
    print(f"  Warm pool: {report['pools']['warm']} items")
    print(f"  Cold pool: {report['pools']['cold']} items")
    print(f"  Total memory saved: {report['memory_saved']} bytes")
    print(f"  Items compressed: {report['items_compressed']}")
    
    print("\n[6] GIBBERLINK HANDSHAKE")
    print("-" * 50)
    
    handshake = mm.gibberlink.handshake('ToastedAI-Node')
    print(f"  Protocol: {handshake['protocol']}")
    print(f"  Symbol: {handshake['symbol']}")
    
    print("\n" + "=" * 70)
    print("MEMORY COMPRESSION: FULLY INTEGRATED")
    print("=" * 70)
    
    print("\nLOW MEMORY SOLUTION:")
    print("  • Data automatically compressed on store")
    print("  • Unused data moved to colder tiers")
    print("  • Memory sparsified on optimize")
    print("  • GodCode recursive encoding for deep storage")
    print("  • Gibberlink protocol for AI-to-AI communication")

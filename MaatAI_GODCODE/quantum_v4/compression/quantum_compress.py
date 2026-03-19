"""
Advanced Quantum Compression Pipeline
=====================================
Real-time compression/decompression for chat thread communication.
"""

import zlib
import bz2
import lzma
import lz4.frame
import zstandard
import numpy as np
import hashlib
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple, Optional
from enum import Enum
import threading

class CompressionLevel(Enum):
    LIGHT = 1      # Fast, low compression
    BALANCED = 5   # Speed/compression balance  
    MAXIMUM = 9    # Slow, best compression

@dataclass
class CompressionResult:
    method: str
    original_size: int
    compressed_size: int
    compression_time: float
    ratio: float
    decompression_time: float
    success: bool

class CompressionPipeline:
    """Multi-stage compression pipeline"""
    
    def __init__(self, level: CompressionLevel = CompressionLevel.BALANCED):
        self.level = level
        self.algorithms: List[Tuple[str, Callable]] = []
        self._build_pipeline()
        self.stats: Dict[str, Dict] = {}
        self._lock = threading.Lock()
    
    def _build_pipeline(self):
        """Build compression pipeline based on level"""
        if self.level == CompressionLevel.LIGHT:
            self.algorithms = [
                ("xor", self._xor_encode),
                ("rle", self._rle_encode),
            ]
        elif self.level == CompressionLevel.BALANCED:
            self.algorithms = [
                ("xor", self._xor_encode),
                ("delta", self._delta_encode),
                ("zlib", lambda d: zlib.compress(d, 3)),
            ]
        else:  # MAXIMUM
            self.algorithms = [
                ("xor", self._xor_encode),
                ("delta", self._delta_encode),
                ("rle", self._rle_encode),
                ("lz4", lambda d: lz4.frame.compress(d)),
                ("zstd", lambda d: zstandard.compress(d, level=10)),
            ]
    
    def compress(self, data: bytes) -> Tuple[bytes, List[str]]:
        """Apply compression pipeline"""
        if not data:
            return data, []
        
        method_used = []
        current = data
        
        for name, func in self.algorithms:
            try:
                compressed = func(current)
                if len(compressed) < len(current):
                    current = compressed
                    method_used.append(name)
            except Exception:
                pass
        
        return current, method_used
    
    def decompress(self, data: bytes, methods: List[str]) -> bytes:
        """Reverse compression pipeline"""
        if not data:
            return data
        
        # Reverse order for decompression
        reverse_algos = {name: func for name, func in self.algorithms}
        
        for name in reversed(methods):
            if name in reverse_algos:
                try:
                    data = reverse_algos[name](data, decompress=True)
                except Exception:
                    pass
        
        return data
    
    def _xor_encode(self, data: bytes, decompress: bool = False) -> bytes:
        """XOR encoding with rolling key"""
        if decompress:
            return self._xor_encode(data, False)
        
        key = hashlib.sha256(data).digest()
        result = bytearray()
        
        for i, byte in enumerate(data):
            result.append(byte ^ key[i % len(key)])
        
        return bytes(result)
    
    def _delta_encode(self, data: bytes, decompress: bool = False) -> bytes:
        """Delta encoding"""
        if decompress:
            if len(data) < 1:
                return data
            result = [data[0]]
            for i in range(1, len(data)):
                result.append((result[-1] + data[i]) % 256)
            return bytes(result)
        
        if len(data) < 2:
            return data
        
        result = bytearray([data[0]])
        for i in range(1, len(data)):
            result.append((data[i] - data[i-1]) % 256)
        
        return bytes(result)
    
    def _rle_encode(self, data: bytes, decompress: bool = False) -> bytes:
        """Run-length encoding"""
        if decompress:
            result = bytearray()
            i = 0
            while i < len(data):
                if i + 1 < len(data):
                    count = data[i + 1]
                    if count > 1 and i + 2 <= len(data):
                        result.extend([data[i]] * count)
                        i += 2
                        continue
                result.append(data[i])
                i += 1
            return bytes(result)
        
        if len(data) < 2:
            return data
        
        result = bytearray()
        i = 0
        while i < len(data):
            count = 1
            while i + count < len(data) and data[i] == data[i + count] and count < 255:
                count += 1
            
            if count > 2:
                result.extend([data[i], count])
            else:
                result.extend([data[i]] * count)
            i += count
        
        return bytes(result)

class AdaptiveCompressor:
    """Adaptive compression that selects best method per data"""
    
    def __init__(self):
        self.methods: Dict[str, Callable] = {
            "zlib": lambda d: zlib.compress(d, 6),
            "bz2": lambda d: bz2.compress(d, 9),
            "lzma": lambda d: lzma.compress(d, preset=9),
            "lz4": lambda d: lz4.frame.compress(d),
            "zstd": lambda d: zstandard.compress(d, level=10),
        }
        self.method_stats: Dict[str, List[float]] = {m: [] for m in self.methods}
        self.cache: Dict[str, bytes] = {}
        self.cache_size = 0
        self.max_cache = 1024 * 1024  # 1MB
    
    def compress(self, data: bytes, force_method: Optional[str] = None) -> Tuple[bytes, str]:
        """Compress with best or specified method"""
        
        # Check cache
        cache_key = hashlib.sha256(data).hexdigest()[:16]
        if cache_key in self.cache:
            return self.cache[cache_key], "cache"
        
        # Use forced method or find best
        if force_method and force_method in self.methods:
            result = self.methods[force_method](data)
            method = force_method
        else:
            # Find best method
            best = None
            best_ratio = float('inf')
            
            for name, func in self.methods.items():
                try:
                    compressed = func(data)
                    ratio = len(compressed) / max(1, len(data))
                    if ratio < best_ratio:
                        best_ratio = ratio
                        best = compressed
                        method = name
                except:
                    pass
            
            if best is None:
                return data, "none"
            result = best
        
        # Cache if beneficial
        if len(result) < len(data) and self.cache_size < self.max_cache:
            self.cache[cache_key] = result
            self.cache_size += len(result)
        
        return result, method
    
    def decompress(self, data: bytes, method: str) -> bytes:
        """Decompress data"""
        if method == "cache":
            return data
        
        decompressors = {
            "zlib": zlib.decompress,
            "bz2": bz2.decompress,
            "lzma": lzma.decompress,
            "lz4": lambda d: lz4.frame.decompress(d),
            "zstd": zstandard.decompress,
        }
        
        if method in decompressors:
            return decompressors[method](data)
        
        return data

class StreamCompressor:
    """Streaming compressor for real-time chat processing"""
    
    def __init__(self, chunk_size: int = 4096):
        self.chunk_size = chunk_size
        self.compressor = AdaptiveCompressor()
        self.buffer = bytearray()
        self.output_buffer = bytearray()
        self.compression_overhead = 0
    
    def add(self, data: bytes) -> bytes:
        """Add data and get compressed output"""
        self.buffer.extend(data)
        
        result = bytearray()
        
        while len(self.buffer) >= self.chunk_size:
            chunk = bytes(self.buffer[:self.chunk_size])
            compressed, method = self.compressor.compress(chunk)
            
            # Add header: method (1 byte) + length (2 bytes)
            result.extend([len(method), len(compressed) & 0xFF, (len(compressed) >> 8) & 0xFF])
            result.extend(compressed)
            
            self.buffer = self.buffer[self.chunk_size:]
        
        return bytes(result)
    
    def flush(self) -> bytes:
        """Flush remaining data"""
        if not self.buffer:
            return b''
        
        compressed, method = self.compressor.compress(bytes(self.buffer))
        
        result = bytearray([len(method), len(compressed) & 0xFF, (len(compressed) >> 8) & 0xFF])
        result.extend(compressed)
        
        self.buffer = bytearray()
        
        return bytes(result)
    
    def decompress_stream(self, data: bytes) -> bytes:
        """Decompress streaming data"""
        result = bytearray()
        i = 0
        
        while i < len(data):
            if i + 2 >= len(data):
                break
            
            method_len = data[i]
            length = data[i+1] | (data[i+2] << 8)
            
            method = data[i+3:i+3+method_len].decode()
            compressed = data[i+3+method_len:i+3+method_len+length]
            
            decompressed = self.compressor.decompress(compressed, method)
            result.extend(decompressed)
            
            i += 3 + method_len + length
        
        return bytes(result)

class NeuralCompressor:
    """Neural-network-inspired compression (simplified)"""
    
    def __init__(self):
        self.patterns: Dict[bytes, bytes] = {}
        self.learn_rate = 0.1
    
    def compress(self, data: bytes) -> Tuple[bytes, Dict]:
        """Compress with pattern learning"""
        
        # Find repeating patterns
        patterns_found = {}
        
        for size in [4, 8, 16, 32]:
            for i in range(len(data) - size):
                pattern = data[i:i+size]
                if pattern not in patterns_found:
                    patterns_found[pattern] = len(patterns_found)
        
        # Replace patterns with indices
        output = bytearray()
        references = []
        
        i = 0
        while i < len(data):
            matched = False
            for size in [32, 16, 8, 4]:
                if i + size <= len(data):
                    pattern = data[i:i+size]
                    if pattern in patterns_found:
                        idx = patterns_found[pattern]
                        output.extend(idx.to_bytes(4, 'big'))
                        references.append(size)
                        i += size
                        matched = True
                        break
            
            if not matched:
                output.append(data[i])
                i += 1
        
        return bytes(output), {"patterns": len(patterns_found), "references": len(references)}
    
    def decompress(self, data: bytes, meta: Dict) -> bytes:
        """Decompress pattern-encoded data"""
        # This is simplified - full implementation would need pattern table
        return data

# Global instance
_compressor = AdaptiveCompressor()

def compress_chat_message(data: bytes) -> Tuple[bytes, str]:
    """Compress a chat message"""
    return _compressor.compress(data)

def decompress_chat_message(data: bytes, method: str) -> bytes:
    """Decompress a chat message"""
    return _compressor.decompress(data, method)

# Test
if __name__ == "__main__":
    test = b"Hello from the quantum compression pipeline! " * 20
    
    print("=== Compression Pipeline Test ===\n")
    
    # Test adaptive compressor
    compressor = AdaptiveCompressor()
    
    for method in compressor.methods:
        start = time.perf_counter()
        compressed, _ = compressor.compress(test, force_method=method)
        compress_time = time.perf_counter() - start
        
        start = time.perf_counter()
        decompressed = compressor.decompress(compressed, method)
        decompress_time = time.perf_counter() - start
        
        ratio = len(compressed) / len(test)
        
        print(f"{method:8} | Ratio: {ratio:.3f} | "
              f"Compress: {compress_time*1000:.2f}ms | "
              f"Decompress: {decompress_time*1000:.2f}ms | "
              f"Match: {test == decompressed}")

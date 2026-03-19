"""
Binary Compressor - Efficient Neural Network Compression
Based on research: DFloat11, BCNN, BitStack, Neural Weight Compression
Target: 50-70% size reduction for efficient transmission
"""

import numpy as np
import json
import zlib
import base64
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import hashlib

class BinaryCompressor:
    def __init__(self):
        self.compression_history = []
        self.entropy_cache = {}
        
    def compress_weights(self, weights: np.ndarray, method: str = 'binary') -> Dict[str, Any]:
        """Compress neural network weights"""
        if method == 'binary':
            return self._compress_binary(weights)
        elif method == 'quantize':
            return self._compress_quantized(weights)
        elif method == 'entropy':
            return self._compress_entropy(weights)
        else:
            return self._compress_hybrid(weights)
    
    def _compress_binary(self, weights: np.ndarray) -> Dict[str, Any]:
        """Binary weight compression (BCNN approach)"""
        # Binarize weights: -1 or +1
        binary_weights = np.sign(weights)
        binary_weights[binary_weights == 0] = 1  # Handle zero
        
        # Calculate scale factor
        scale = np.mean(np.abs(weights))
        
        # Store as int8
        compressed = binary_weights.astype(np.int8)
        
        # Calculate compression ratio
        original_size = weights.nbytes
        compressed_size = compressed.nbytes + 4  # +4 for scale
        
        result = {
            'method': 'binary',
            'original_shape': list(weights.shape),
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compressed_size / original_size,
            'scale': float(scale),
            'data': base64.b64encode(compressed.tobytes()).decode('utf-8')
        }
        
        self.compression_history.append({
            'method': 'binary',
            'timestamp': datetime.utcnow().isoformat(),
            'ratio': result['compression_ratio']
        })
        
        return result
    
    def _compress_quantized(self, weights: np.ndarray, bits: int = 4) -> Dict[str, Any]:
        """Quantized weight compression"""
        # Find min/max
        w_min = np.min(weights)
        w_max = np.max(weights)
        
        # Quantize to specified bits
        num_levels = 2 ** bits
        scale = (w_max - w_min) / (num_levels - 1)
        
        quantized = np.round((weights - w_min) / scale).astype(np.uint8)
        quantized = np.clip(quantized, 0, num_levels - 1)
        
        # Calculate compression
        original_size = weights.nbytes
        compressed_size = quantized.nbytes + 8  # +8 for min, max, scale
        
        result = {
            'method': 'quantized',
            'bits': bits,
            'original_shape': list(weights.shape),
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compressed_size / original_size,
            'min': float(w_min),
            'max': float(w_max),
            'scale': float(scale),
            'data': base64.b64encode(quantized.tobytes()).decode('utf-8')
        }
        
        self.compression_history.append({
            'method': 'quantized',
            'timestamp': datetime.utcnow().isoformat(),
            'ratio': result['compression_ratio']
        })
        
        return result
    
    def _compress_entropy(self, weights: np.ndarray) -> Dict[str, Any]:
        """Entropy-based compression"""
        # Convert to bytes
        float_bytes = weights.astype(np.float32).tobytes()
        
        # Apply zlib compression
        compressed = zlib.compress(float_bytes, level=9)
        
        # Calculate compression
        original_size = len(float_bytes)
        compressed_size = len(compressed)
        
        result = {
            'method': 'entropy',
            'original_shape': list(weights.shape),
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compressed_size / original_size,
            'data': base64.b64encode(compressed).decode('utf-8')
        }
        
        self.compression_history.append({
            'method': 'entropy',
            'timestamp': datetime.utcnow().isoformat(),
            'ratio': result['compression_ratio']
        })
        
        return result
    
    def _compress_hybrid(self, weights: np.ndarray) -> Dict[str, Any]:
        """Hybrid compression: binary + entropy"""
        # First binarize
        binary = np.sign(weights)
        binary[binary == 0] = 1
        scale = np.mean(np.abs(weights))
        
        # Calculate residual
        residual = weights - (binary * scale)
        
        # Compress binary part
        binary_compressed = self._compress_binary(weights)
        
        # Compress residual with entropy
        residual_compressed = self._compress_entropy(residual)
        
        # Calculate total compression
        original_size = weights.nbytes
        total_compressed = binary_compressed['compressed_size'] + residual_compressed['compressed_size']
        
        result = {
            'method': 'hybrid',
            'original_shape': list(weights.shape),
            'original_size': original_size,
            'compressed_size': total_compressed,
            'compression_ratio': total_compressed / original_size,
            'binary_part': {
                'scale': binary_compressed['scale'],
                'data': binary_compressed['data']
            },
            'residual_part': {
                'compressed_size': residual_compressed['compressed_size'],
                'data': residual_compressed['data']
            }
        }
        
        self.compression_history.append({
            'method': 'hybrid',
            'timestamp': datetime.utcnow().isoformat(),
            'ratio': result['compression_ratio']
        })
        
        return result
    
    def decompress(self, compressed_data: Dict[str, Any]) -> np.ndarray:
        """Decompress weights"""
        method = compressed_data['method']
        shape = tuple(compressed_data['original_shape'])
        
        if method == 'binary':
            return self._decompress_binary(compressed_data)
        elif method == 'quantize':
            return self._decompress_quantized(compressed_data)
        elif method == 'entropy':
            return self._decompress_entropy(compressed_data)
        elif method == 'hybrid':
            return self._decompress_hybrid(compressed_data)
        
        raise ValueError(f"Unknown method: {method}")
    
    def _decompress_binary(self, data: Dict[str, Any]) -> np.ndarray:
        """Decompress binary weights"""
        compressed = np.frombuffer(
            base64.b64decode(data['data']),
            dtype=np.int8
        ).reshape(data['original_shape'])
        
        scale = data['scale']
        return compressed * scale
    
    def _decompress_quantized(self, data: Dict[str, Any]) -> np.ndarray:
        """Decompress quantized weights"""
        compressed = np.frombuffer(
            base64.b64decode(data['data']),
            dtype=np.uint8
        ).reshape(data['original_shape'])
        
        w_min = data['min']
        scale = data['scale']
        return compressed * scale + w_min
    
    def _decompress_entropy(self, data: Dict[str, Any]) -> np.ndarray:
        """Decompress entropy-compressed weights"""
        compressed = base64.b64decode(data['data'])
        decompressed = zlib.decompress(compressed)
        return np.frombuffer(decompressed, dtype=np.float32).reshape(data['original_shape'])
    
    def _decompress_hybrid(self, data: Dict[str, Any]) -> np.ndarray:
        """Decompress hybrid weights"""
        # Decompress binary part
        binary_data = {
            'method': 'binary',
            'original_shape': data['original_shape'],
            'data': data['binary_part']['data'],
            'scale': data['binary_part']['scale']
        }
        binary_weights = self._decompress_binary(binary_data)
        
        # Decompress residual
        residual_data = {
            'method': 'entropy',
            'original_shape': data['original_shape'],
            'data': data['residual_part']['data']
        }
        residual = self._decompress_entropy(residual_data)
        
        return binary_weights + residual
    
    def compress_text(self, text: str) -> Dict[str, Any]:
        """Compress text using neural prediction"""
        # Simple prediction-based compression
        text_bytes = text.encode('utf-8')
        
        # Apply zlib
        compressed = zlib.compress(text_bytes, level=9)
        
        original_size = len(text_bytes)
        compressed_size = len(compressed)
        
        result = {
            'method': 'text_entropy',
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compressed_size / original_size,
            'data': base64.b64encode(compressed).decode('utf-8')
        }
        
        return result
    
    def decompress_text(self, compressed_data: Dict[str, Any]) -> str:
        """Decompress text"""
        compressed = base64.b64decode(compressed_data['data'])
        decompressed = zlib.decompress(compressed)
        return decompressed.decode('utf-8')
    
    def calculate_entropy(self, data: np.ndarray) -> float:
        """Calculate Shannon entropy"""
        # Flatten and get value counts
        flat = data.flatten()
        _, counts = np.unique(flat, return_counts=True)
        
        # Calculate probabilities
        probs = counts / len(flat)
        
        # Calculate entropy
        entropy = -np.sum(probs * np.log2(probs + 1e-10))
        
        return float(entropy)
    
    def get_state(self) -> Dict[str, Any]:
        """Get compressor state"""
        avg_ratio = np.mean([h['ratio'] for h in self.compression_history]) if self.compression_history else 1.0
        
        return {
            'compression_history_count': len(self.compression_history),
            'average_compression_ratio': avg_ratio,
            'methods_used': list(set(h['method'] for h in self.compression_history))
        }


# Singleton instance
_binary_compressor = None

def get_binary_compressor() -> BinaryCompressor:
    global _binary_compressor
    if _binary_compressor is None:
        _binary_compressor = BinaryCompressor()
    return _binary_compressor


if __name__ == "__main__":
    # Test compressor
    bc = BinaryCompressor()
    
    # Create test weights
    weights = np.random.randn(100, 100).astype(np.float32)
    
    print(f"Original size: {weights.nbytes} bytes")
    
    # Test binary compression
    binary = bc.compress_weights(weights, 'binary')
    print(f"\nBinary compression:")
    print(f"  Compressed: {binary['compressed_size']} bytes")
    print(f"  Ratio: {binary['compression_ratio']:.2%}")
    
    # Test quantized compression
    quantized = bc.compress_weights(weights, 'quantize')
    print(f"\nQuantized (4-bit) compression:")
    print(f"  Compressed: {quantized['compressed_size']} bytes")
    print(f"  Ratio: {quantized['compression_ratio']:.2%}")
    
    # Test entropy compression
    entropy = bc.compress_weights(weights, 'entropy')
    print(f"\nEntropy compression:")
    print(f"  Compressed: {entropy['compressed_size']} bytes")
    print(f"  Ratio: {entropy['compression_ratio']:.2%}")
    
    # Test hybrid compression
    hybrid = bc.compress_weights(weights, 'hybrid')
    print(f"\nHybrid compression:")
    print(f"  Compressed: {hybrid['compressed_size']} bytes")
    print(f"  Ratio: {hybrid['compression_ratio']:.2%}")
    
    # Test decompression
    decompressed = bc.decompress(hybrid)
    error = np.mean(np.abs(weights - decompressed))
    print(f"\nDecompression error: {error:.6f}")

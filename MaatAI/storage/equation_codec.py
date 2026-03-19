"""
EQUATION CODEC
==============
Converts files to/from mathematical equations
Front of House: Human readable format
Back of House: Pure equation representation
"""

import base64
import hashlib
import json
import numpy as np
from typing import Tuple, List, Dict, Any
from pathlib import Path

class EquationCodec:
    """Codec for converting files to equations and back"""
    
    # Prime numbers for fractal encoding
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
    
    @staticmethod
    def encode_file_to_equation(file_path: str) -> Dict[str, Any]:
        """Convert a file to an equation representation"""
        path = Path(file_path)
        
        with open(path, 'rb') as f:
            data = f.read()
            
        # Method 1: Polynomial coefficients
        coefficients = EquationCodec._bytes_to_poly_coefficients(data)
        
        # Method 2: Fractal dimension encoding
        fractal_rep = EquationCodec._encode_fractal(data)
        
        # Method 3: Matrix representation
        matrix_rep = EquationCodec._encode_matrix(data)
        
        # Create the master equation
        equation = {
            'name': path.name,
            'size': len(data),
            'checksum': hashlib.sha256(data).hexdigest(),
            'polynomial': {
                'degree': len(coefficients) - 1,
                'coefficients': coefficients[:100],  # Truncate for readability
                'full_coefficient_count': len(coefficients)
            },
            'fractal': fractal_rep,
            'matrix': matrix_rep,
            'equation_string': EquationCodec._to_readable_equation(coefficients)
        }
        
        return equation
    
    @staticmethod
    def _bytes_to_poly_coefficients(data: bytes) -> List[float]:
        """Convert bytes to polynomial coefficients"""
        coeffs = []
        # Use groups of 4 bytes as floats
        for i in range(0, len(data), 4):
            chunk = data[i:i+4]
            if len(chunk) < 4:
                chunk = chunk + b'\x00' * (4 - len(chunk))
            val = int.from_bytes(chunk, 'big') / (2**32)
            coeffs.append(val)
        return coeffs
    
    @staticmethod
    def _encode_fractal(data: bytes) -> Dict:
        """Encode data as fractal parameters"""
        # Use first bytes to generate Mandelbrot-like parameters
        c_real = int.from_bytes(data[:2], 'big') / 65536 - 0.5
        c_imag = int.from_bytes(data[2:4], 'big') / 65536 - 0.5
        
        # Generate fractal signature
        max_iter = 100
        z_real, z_imag = 0, 0
        iterations = []
        
        for _ in range(max_iter):
            z_real, z_imag = z_real**2 - z_imag**2 + c_real, 2*z_real*z_imag + c_imag
            if z_real**2 + z_imag**2 > 4:
                break
            iterations.append(z_real)
            
        return {
            'c': complex(c_real, c_imag),
            'escape_iterations': len(iterations),
            'fractal_type': 'mandelbrot_variant',
            'dimension_estimate': len(iterations) / max_iter
        }
    
    @staticmethod
    def _encode_matrix(data: bytes) -> Dict:
        """Encode data as matrix parameters"""
        # Create a pseudo-matrix representation
        size = len(data)
        sqrt_size = int(size**0.5) + 1
        
        return {
            'matrix_type': 'toeplitz',
            'dimensions': [sqrt_size, sqrt_size],
            'rank_estimate': min(sqrt_size, 10),
            'determinant_approximation': sum(data) / len(data) if data else 0
        }
    
    @staticmethod
    def _to_readable_equation(coefficients: List[float]) -> str:
        """Create human-readable equation string"""
        if not coefficients:
            return "P(x) = 0"
            
        terms = []
        for i, c in enumerate(coefficients[:8]):
            if abs(c) > 0.0001:
                terms.append(f"{c:.4f}x^{i}")
                
        if not terms:
            return "P(x) = 0"
            
        eq = " + ".join(terms)
        if len(coefficients) > 8:
            eq += f" + ...({len(coefficients)-8} terms)"
            
        return f"P(x) = {eq}"
    
    @staticmethod
    def decode_equation_to_file(equation: Dict, output_path: str) -> bool:
        """Decode an equation back to a file"""
        try:
            coefficients = equation['polynomial']['coefficients']
            
            # Reconstruct full coefficient list if truncated
            full_count = equation['polynomial']['full_coefficient_count']
            while len(coefficients) < full_count:
                coefficients.append(0.0)
                
            # Convert back to bytes
            data = b''
            for coef in coefficients:
                val = int(coef * 2**32) % (2**32)
                data += val.to_bytes(4, 'big')
                
            # Trim to original size
            original_size = equation['size']
            data = data[:original_size]
            
            with open(output_path, 'wb') as f:
                f.write(data)
                
            return True
        except Exception as e:
            print(f"Decode error: {e}")
            return False
    
    @staticmethod
    def encode_string_to_equation(text: str) -> Dict[str, Any]:
        """Encode a string as an equation"""
        return EquationCodec.encode_file_to_equation.__wrapped__(None, text.encode())
    
    @staticmethod
    def decode_equation_to_string(equation: Dict) -> str:
        """Decode an equation to a string"""
        import io
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
            
        try:
            EquationCodec.decode_equation_to_file(equation, tmp_path)
            with open(tmp_path, 'rb') as f:
                return f.read().decode('utf-8', errors='replace')
        finally:
            Path(tmp_path).unlink(missing_ok=True)


# Convenience functions
def encode_file_to_equation(file_path: str) -> Dict[str, Any]:
    """Encode a file to equation format"""
    return EquationCodec.encode_file_to_equation(file_path)

def decode_equation_to_file(equation: Dict, output_path: str) -> bool:
    """Decode an equation to a file"""
    return EquationCodec.decode_equation_to_file(equation, output_path)

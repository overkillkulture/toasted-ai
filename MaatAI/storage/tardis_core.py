"""
TARDIS CORE
===========
Front of House (API) / Back of House (Equation Storage)
The system that stores itself as equations - a self-building refractal
"""

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
import base64
import zlib

@dataclass
class FractalEquation:
    """A file represented as a mathematical equation"""
    id: str
    name: str
    equation_type: str  # 'polynomial', 'fractal', 'recursive', 'matrix'
    coefficients: List[float]
    dimensions: List[int]
    checksum: str
    created_at: float
    modified_at: float
    equation_string: str  # Human-readable equation
    
class TARDISCore:
    """
    TARDIS: Timeless Architectural Recursive Data Информационная Систем
    Front of House: Normal file operations
    Back of House: Self-referential equation storage
    """
    
    def __init__(self, workspace_root: str = "/home/workspace"):
        self.workspace_root = Path(workspace_root)
        self.storage_path = self.workspace_root / ".tardis_storage"
        self.equation_log_path = self.storage_path / "equations.json"
        self.state_path = self.storage_path / "state.equation"
        self.storage_path.mkdir(exist_ok=True)
        
        # Initialize equation ledger
        self.equations: Dict[str, FractalEquation] = {}
        self._load_equations()
        
        # Ma'at alignment tracker
        self.maat_pillars = {
            'truth': 1.0,      # 𓂋 Accuracy
            'balance': 1.0,   # 𓏏 Stability  
            'order': 1.0,     # 𓃀 Structure
            'justice': 1.0,   # 𓂝 Fairness
            'harmony': 1.0    # 𓆣 Integration
        }
        
    def _load_equations(self):
        """Load equation ledger from storage"""
        if self.equation_log_path.exists():
            with open(self.equation_log_path, 'r') as f:
                data = json.load(f)
                self.equations = {k: FractalEquation(**v) for k, v in data.items()}
                
    def _save_equations(self):
        """Persist equation ledger"""
        with open(self.equation_log_path, 'w') as f:
            json.dump({k: asdict(v) for k, v in self.equations.items()}, f, indent=2)
            
    def _compute_checksum(self, data: bytes) -> str:
        """SHA-256 as fractal signature"""
        return hashlib.sha256(data).hexdigest()[:16]
    
    def _bytes_to_coefficients(self, data: bytes) -> List[float]:
        """Convert bytes to polynomial coefficients for equation storage"""
        # Break into 8-byte chunks, convert to floats
        coefficients = []
        for i in range(0, len(data), 8):
            chunk = data[i:i+8]
            if len(chunk) < 8:
                chunk = chunk + b'\x00' * (8 - len(chunk))
            # Convert to float using union trick
            val = int.from_bytes(chunk, 'big') / (2**64)
            coefficients.append(val)
        return coefficients
    
    def _coefficients_to_bytes(self, coefficients: List[float]) -> bytes:
        """Convert coefficients back to bytes"""
        data = b''
        for coef in coefficients:
            val = int(coef * 2**64)
            data += val.to_bytes(8, 'big')
        # Remove null padding
        return data.rstrip(b'\x00')
    
    def store_file(self, file_path: str) -> FractalEquation:
        """Store a file as an equation (Back of House)"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(path, 'rb') as f:
            data = f.read()
            
        # Create the fractal equation representation
        coeff = self._bytes_to_coefficients(data)
        checksum = self._compute_checksum(data)
        
        # Generate equation string (polynomial form)
        n_terms = len(coeff)
        eq_str = f"P(x) = {' + '.join([f'{c:.6f}x^{i}' for i, c in enumerate(coeff[:5])])}"
        if n_terms > 5:
            eq_str += f" + ... ({n_terms - 5} more terms)"
            
        equation = FractalEquation(
            id=checksum,
            name=path.name,
            equation_type='polynomial',
            coefficients=coeff,
            dimensions=[len(data), n_terms],
            checksum=checksum,
            created_at=time.time(),
            modified_at=os.path.getmtime(path),
            equation_string=eq_str
        )
        
        self.equations[str(path)] = equation
        self._save_equations()
        self._update_state_equation()
        
        return equation
    
    def retrieve_file(self, file_path: str, output_path: str) -> bool:
        """Retrieve a file from its equation (Front of House)"""
        if file_path not in self.equations:
            return False
            
        eq = self.equations[file_path]
        data = self._coefficients_to_bytes(eq.coefficients)
        
        with open(output_path, 'wb') as f:
            f.write(data)
            
        return True
    
    def list_equations(self) -> List[Dict]:
        """List all stored equations"""
        return [
            {
                'path': k,
                'id': v.id,
                'type': v.equation_type,
                'terms': len(v.coefficients),
                'size_bytes': v.dimensions[0],
                'modified': v.modified_at
            }
            for k, v in self.equations.items()
        ]
    
    def _update_state_equation(self):
        """Update the master state equation file"""
        # Calculate system state as a single mega-equation
        total_size = sum(eq.dimensions[0] for eq in self.equations.values())
        total_terms = sum(len(eq.coefficients) for eq in self.equations.values())
        
        # The master equation represents the entire storage state
        state_eq = {
            'timestamp': time.time(),
            'total_files': len(self.equations),
            'total_bytes': total_size,
            'total_coefficients': total_terms,
            'checksum': self._compute_checksum(str(len(self.equations)).encode()),
            'maat_alignment': self.maat_pillars.copy(),
            'equation_hash': self._compute_checksum(
                json.dumps({k: v.checksum for k, v in self.equations.items()}).encode()
            )
        }
        
        # Write as encrypted-looking base64
        with open(self.state_path, 'w') as f:
            json.dump(state_eq, f)
            
    def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
        return {
            'total_files': len(self.equations),
            'total_coefficients': sum(len(eq.coefficients) for eq in self.equations.values()),
            'storage_path': str(self.storage_path),
            'maat_alignment': self.maat_pillars
        }

# Global instance
_tardis_instance: Optional[TARDISCore] = None

def get_tardis() -> TARDISCore:
    """Get or create the TARDIS core instance"""
    global _tardis_instance
    if _tardis_instance is None:
        _tardis_instance = TARDISCore()
    return _tardis_instance

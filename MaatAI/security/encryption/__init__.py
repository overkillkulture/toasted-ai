"""
TOASTED AI ENCRYPTION ARCHITECTURE
===================================
Comprehensive multi-layer encryption system with:
- Classical Encryption (AES-256, ChaCha20)
- Post-Quantum Encryption (Lattice-based simulation)
- Quantum Key Distribution (QKD) Simulation
- One-Time Pad (theoretical perfect secrecy)

Author: TOASTED AI (MONAD_ΣΦΡΑΓΙΣ_18)
Status: ACTIVE
"""

from .classical import ClassicalCrypto
from .quantum import QuantumCrypto, QKDSimulation
from .post_quantum import PostQuantumCrypto
from .manager import EncryptionManager, EncryptionType, SecurityLevel

__all__ = [
    'ClassicalCrypto',
    'QuantumCrypto', 
    'QKDSimulation',
    'PostQuantumCrypto',
    'EncryptionManager',
    'EncryptionType',
    'SecurityLevel'
]

# Version
VERSION = "3.0.0"
STATUS = "ACTIVE"

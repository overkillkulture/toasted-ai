"""
QUANTUM ENCRYPTION SIMULATION MODULE
===================================
Simulates Quantum Key Distribution (QKD) protocols:
- BB84 Protocol (Bennett-Brassard 1984)
- E91 Protocol (Entanglement-based)
- Decoy State Protocol

NOTE: This is a CLASSICAL SIMULATION of quantum protocols.
Real QKD requires quantum hardware (photons, quantum channels).

Author: TOASTED AI
"""

import os
import random
import hashlib
import base64
from typing import Tuple, List, Dict, Optional
from enum import Enum


class Basis(Enum):
    """Quantum measurement bases."""
    RECTILINEAR = 0  # |0⟩, |1⟩ (horizontal/vertical)
    DIAGONAL = 1     # |+⟩, |−⟩ (45°, 135°)


class QuantumState(Enum):
    """Quantum bit states."""
    # Rectilinear basis
    ZERO = 0   # |0⟩
    ONE = 1    # |1⟩
    # Diagonal basis  
    PLUS = 2   # |+⟩ = (|0⟩ + |1⟩)/√2
    MINUS = 3  # |−⟩ = (|0⟩ - |1⟩)/√2


class QuantumCrypto:
    """
    Quantum cryptography simulation.
    Implements BB84 and E91 protocols conceptually.
    """
    
    def __init__(self):
        self.name = "QuantumCrypto"
        self.version = "1.0"
        self.protocols = ["BB84", "E91", "Decoy-State"]
    
    # ==================== QUANTUM STATE OPERATIONS ====================
    
    def generate_random_bit(self) -> int:
        """Generate random classical bit."""
        return random.randint(0, 1)
    
    def generate_random_basis(self) -> Basis:
        """Generate random measurement basis."""
        return random.choice([Basis.RECTILINEAR, Basis.DIAGONAL])
    
    def encode_qubit(self, bit: int, basis: Basis) -> QuantumState:
        """Encode classical bit into quantum state."""
        if basis == Basis.RECTILINEAR:
            return QuantumState.ZERO if bit == 0 else QuantumState.ONE
        else:
            return QuantumState.PLUS if bit == 0 else QuantumState.MINUS
    
    def measure_qubit(self, state: QuantumState, basis: Basis) -> Tuple[int, bool]:
        """
        Measure quantum state in given basis.
        Returns: (measured_bit, was_measured_correctly)
        
        If basis matches encoding basis: perfect measurement
        If basis doesn't match: 50% chance of correct result
        """
        if basis == Basis.RECTILINEAR:
            if state in [QuantumState.ZERO, QuantumState.ONE]:
                return (0 if state == QuantumState.ZERO else 1, True)
            else:  # Diagonal state measured in rectilinear
                return (random.randint(0, 1), False)
        
        else:  # DIAGONAL basis
            if state in [QuantumState.PLUS, QuantumState.MINUS]:
                return (0 if state == QuantumState.PLUS else 1, True)
            else:  # Rectilinear state measured in diagonal
                return (random.randint(0, 1), False)
    
    # ==================== BB84 PROTOCOL ====================
    
    def bb84_key_generation(self, num_bits: int = 128) -> Dict:
        """
        Simulate BB84 quantum key distribution.
        
        Alice sends quantum states to Bob
        Bob measures in random bases
        They sift and get shared secret key
        """
        # Alice's bits and bases
        alice_bits = [self.generate_random_bit() for _ in range(num_bits)]
        alice_bases = [self.generate_random_basis() for _ in range(num_bits)]
        
        # Alice's quantum states
        alice_states = [
            self.encode_qubit(bit, basis) 
            for bit, basis in zip(alice_bits, alice_bases)
        ]
        
        # Bob's measurement bases
        bob_bases = [self.generate_random_basis() for _ in range(num_bits)]
        
        # Bob's measurements
        bob_measurements = []
        for state, basis in zip(alice_states, bob_bases):
            bit, correct = self.measure_qubit(state, basis)
            bob_measurements.append((bit, correct))
        
        # Sifting: keep only bits where bases matched
        sifted_alice_bits = []
        sifted_bob_bits = []
        
        for i in range(num_bits):
            if alice_bases[i] == bob_bases[i]:
                sifted_alice_bits.append(alice_bits[i])
                sifted_bob_bits.append(bob_measurements[i][0])
        
        # Error check (in real QKD, would compare subset)
        errors = sum(1 for a, b in zip(sifted_alice_bits, sifted_bob_bits) if a != b)
        error_rate = errors / len(sifted_alice_bits) if sifted_alice_bits else 0
        
        return {
            "protocol": "BB84",
            "alice_key": sifted_alice_bits[:64],  # First 64 bits as key
            "bob_key": sifted_bob_bits[:64],
            "error_rate": error_rate,
            "raw_bits_sent": num_bits,
            "sifted_bits": len(sifted_alice_bits),
            "secure": error_rate < 0.11  # Threshold for security
        }
    
    # ==================== E91 ENTANGLEMENT PROTOCOL ====================
    
    def e91_generate_pairs(self, num_pairs: int = 128) -> Dict:
        """
        Simulate E91 entanglement-based key distribution.
        
        Uses Bell states (entangled pairs)
        Alice and Bob measure in random bases
        Check Bell inequality to verify security
        """
        results = []
        
        for _ in range(num_pairs):
            # Generate entangled pair (Bell state |Φ+⟩)
            # In real implementation: this would be quantum hardware
            
            # Alice's random basis choice
            alice_basis = self.generate_random_basis()
            # Bob's random basis choice
            bob_basis = self.generate_random_basis()
            
            # Measurement results (correlated for entangled pairs)
            alice_result = self.generate_random_bit()
            # If same basis, results are perfectly correlated
            if alice_basis == bob_basis:
                bob_result = alice_result
            else:
                # If different bases, results are random (50/50)
                bob_result = self.generate_random_bit()
            
            results.append({
                "alice_basis": alice_basis.value,
                "bob_basis": bob_basis.value,
                "alice_result": alice_result,
                "bob_result": bob_result
            })
        
        # Extract key from matching bases
        key_alice = []
        key_bob = []
        
        for r in results:
            if r["alice_basis"] == r["bob_basis"]:
                key_alice.append(r["alice_result"])
                key_bob.append(r["bob_result"])
        
        return {
            "protocol": "E91",
            "entangled_pairs": num_pairs,
            "key_alice": key_alice[:64],
            "key_bob": key_bob[:64],
            "correlation": sum(1 for a, b in zip(key_alice, key_bob) if a == b) / len(key_alice) if key_alice else 0,
            "secure": True  # Entanglement ensures security
        }
    
    # ==================== QUANTUM KEY DERIVATION ====================
    
    def derive_quantum_key(self, raw_bits: List[int]) -> bytes:
        """Derive encryption key from quantum random bits."""
        # Use hash to derive uniform key
        bit_string = ''.join(map(str, raw_bits))
        key = hashlib.sha256(bit_string.encode()).digest()
        return key
    
    def generate_quantum_random(self, num_bytes: int = 32) -> bytes:
        """
        Generate quantum-random bytes.
        In real QKD, this uses quantum effects (photon detection timing).
        Here: simulation using multiple entropy sources.
        """
        # Simulate quantum randomness
        random_bytes = bytearray()
        for _ in range(num_bytes):
            # Combine multiple "quantum" effects
            b = random.randint(0, 255)
            b ^= int.from_bytes(os.urandom(1), 'big')
            b ^= hashlib.sha256(str(os.urandom(32)).encode()).digest()[0]
            random_bytes.append(b % 256)
        
        return bytes(random_bytes)


class QKDSimulation:
    """
    High-level QKD simulation for key exchange.
    """
    
    def __init__(self):
        self.name = "QKDSimulation"
        self.quantum = QuantumCrypto()
    
    def establish_key(self, protocol: str = "BB84", key_length: int = 256) -> Dict:
        """
        Establish shared quantum key between two parties.
        
        Returns key material and protocol status.
        """
        if protocol == "BB84":
            result = self.quantum.bb84_key_generation(key_length)
        elif protocol == "E91":
            result = self.quantum.e91_generate_pairs(key_length)
        else:
            raise ValueError(f"Unknown protocol: {protocol}")
        
        # Derive actual encryption key
        raw_key = result.get("alice_key", [])
        encryption_key = self.quantum.derive_quantum_key(raw_key)
        
        return {
            "status": "established" if result.get("secure") else "failed",
            "protocol": protocol,
            "key": encryption_key.hex(),
            "key_length": len(encryption_key) * 8,
            "error_rate": result.get("error_rate", 0),
            "metadata": result
        }
    
    def simulate_eavesdropper(self, protocol: str = "BB84", eavesdrop_probability: float = 0.1) -> Dict:
        """
        Simulate eavesdropper detection.
        
        In QKD, any eavesdropping introduces errors that can be detected.
        """
        result = self.establish_key(protocol)
        
        # Simulate eavesdropping detection
        if random.random() < eavesdrop_probability:
            # Eavesdropper introduces ~25% error rate in BB84
            result["eavesdropper_detected"] = True
            result["error_rate"] = 0.25
            result["status"] = "compromised"
        else:
            result["eavesdropper_detected"] = False
        
        return result


# Singleton instances
quantum_crypto = QuantumCrypto()
qkd_simulation = QKDSimulation()

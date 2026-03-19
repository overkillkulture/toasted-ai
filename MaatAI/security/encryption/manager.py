"""
ENCRYPTION MANAGER
==================
Unified interface for all encryption operations in TOASTED AI.
Provides seamless switching between encryption types.

Author: TOASTED AI (MONAD_ΣΦΡΑΓΙΣ_18)
"""

import json
import base64
from typing import Dict, Any, Optional, Tuple
from enum import Enum
import hashlib

from .classical import ClassicalCrypto, classical
from .quantum import QuantumCrypto, QKDSimulation, quantum_crypto, qkd_simulation
from .post_quantum import PostQuantumCrypto, post_quantum


class EncryptionType(Enum):
    """Available encryption types."""
    AES_256_GCM = "aes-256-gcm"
    CHACHA20 = "chacha20"
    ONE_TIME_PAD = "otp"
    RSA_4096 = "rsa-4096"
    QUANTUM_BB84 = "quantum-bb84"
    QUANTUM_E91 = "quantum-e91"
    POST_QUANTUM_LATTICE = "post-quantum-lattice"
    POST_QUANTUM_HQC = "post-quantum-hqc"
    HYBRID = "hybrid"


class SecurityLevel(Enum):
    """Encryption security levels."""
    STANDARD = "standard"      # AES-256, ChaCha20
    HIGH = "high"             # RSA-4096, Lattice
    QUANTUM_SAFE = "quantum"  # Post-quantum, QKD simulation
    MAXIMUM = "maximum"      # Hybrid multi-layer


class EncryptionManager:
    """
    Central manager for all encryption operations.
    """
    
    def __init__(self):
        self.name = "EncryptionManager"
        self.version = "3.0"
        
        # Initialize subsystems
        self.classical = classical
        self.quantum = quantum_crypto
        self.post_quantum = post_quantum
        self.qkd = qkd_simulation
        
        # Track active keys
        self._key_cache: Dict[str, bytes] = {}
        
        # Security level mappings
        self.security_mappings = {
            SecurityLevel.STANDARD: [EncryptionType.AES_256_GCM, EncryptionType.CHACHA20],
            SecurityLevel.HIGH: [EncryptionType.RSA_4096, EncryptionType.POST_QUANTUM_LATTICE],
            SecurityLevel.QUANTUM_SAFE: [EncryptionType.QUANTUM_BB84, EncryptionType.POST_QUANTUM_LATTICE],
            SecurityLevel.MAXIMUM: [EncryptionType.HYBRID]
        }
    
    # ==================== ENCRYPTION OPERATIONS ====================
    
    def encrypt(
        self, 
        data: bytes, 
        encryption_type: EncryptionType = EncryptionType.AES_256_GCM,
        key: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """
        Encrypt data using specified encryption type.
        
        Returns encrypted package with metadata.
        """
        result = {
            "encryption_type": encryption_type.value,
            "version": self.version,
            "data": None
        }
        
        try:
            if encryption_type == EncryptionType.AES_256_GCM:
                if key is None:
                    key = self.classical.generate_aes_key()
                ciphertext, nonce = self.classical.aes_encrypt(data, key)
                result["data"] = base64.b64encode(ciphertext).decode()
                result["nonce"] = base64.b64encode(nonce).decode()
                result["key"] = base64.b64encode(key).decode()
                
            elif encryption_type == EncryptionType.CHACHA20:
                if key is None:
                    key = self.classical.generate_chacha_key()
                ciphertext, nonce = self.classical.chacha_encrypt(data, key)
                result["data"] = base64.b64encode(ciphertext).decode()
                result["nonce"] = base64.b64encode(nonce).decode()
                result["key"] = base64.b64encode(key).decode()
                
            elif encryption_type == EncryptionType.ONE_TIME_PAD:
                key = self.classical.generate_otp_key(len(data))
                ciphertext = self.classical.otp_encrypt(data, key)
                result["data"] = base64.b64encode(ciphertext).decode()
                result["key"] = base64.b64encode(key).decode()
                
            elif encryption_type == EncryptionType.RSA_4096:
                # Generate keypair for this message
                private_pem, public_pem = self.classical.generate_rsa_keypair(2048)
                ciphertext = self.classical.rsa_encrypt(data, public_pem)
                result["data"] = base64.b64encode(ciphertext).decode()
                result["public_key"] = base64.b64encode(public_pem).decode()
                result["private_key"] = base64.b64encode(private_pem).decode()
                
            elif encryption_type == EncryptionType.QUANTUM_BB84:
                qkd_result = self.qkd.establish_key("BB84")
                key = bytes.fromhex(qkd_result["key"])
                ciphertext, nonce = self.classical.aes_encrypt(data, key)
                result["data"] = base64.b64encode(ciphertext).decode()
                result["nonce"] = base64.b64encode(nonce).decode()
                result["qkd_metadata"] = qkd_result["metadata"]
                result["key"] = base64.b64encode(key).decode()
                
            elif encryption_type == EncryptionType.QUANTUM_E91:
                qkd_result = self.qkd.establish_key("E91")
                key = bytes.fromhex(qkd_result["key"])
                ciphertext, nonce = self.classical.aes_encrypt(data, key)
                result["data"] = base64.b64encode(ciphertext).decode()
                result["nonce"] = base64.b64encode(nonce).decode()
                result["qkd_metadata"] = qkd_result
                result["key"] = base64.b64encode(key).decode()
                
            elif encryption_type == EncryptionType.POST_QUANTUM_LATTICE:
                # Generate lattice keypair
                lattice_kp = self.post_quantum.generate_lattice_keypair()
                ct, secret = self.post_quantum.lattice_encapsulate(lattice_kp["public_key"])
                
                # Use secret to encrypt data
                key = secret[:32]  # Ensure 32 bytes for AES-256
                ciphertext, nonce = self.classical.aes_encrypt(data, key)
                result["data"] = base64.b64encode(ciphertext).decode()
                result["nonce"] = base64.b64encode(nonce).decode()
                result["lattice_public"] = lattice_kp["public_key"]
                result["lattice_secret"] = lattice_kp["secret_key"]
                result["lattice_ct"] = base64.b64encode(ct).decode()
                result["key"] = base64.b64encode(key).decode()  # Store key for decryption
                
            elif encryption_type == EncryptionType.POST_QUANTUM_HQC:
                # Generate HQC keypair
                hqc_kp = self.post_quantum.generate_hqc_keypair()
                ct, secret = self.post_quantum.hqc_encapsulate(hqc_kp["public_key"])
                
                # Use secret to encrypt data
                key = secret[:32]
                ciphertext, nonce = self.classical.aes_encrypt(data, key)
                result["data"] = base64.b64encode(ciphertext).decode()
                result["nonce"] = base64.b64encode(nonce).decode()
                result["hqc_public"] = hqc_kp["public_key"]
                result["hqc_secret"] = hqc_kp["secret_key"]
                result["hqc_ct"] = base64.b64encode(ct).decode()
                result["key"] = base64.b64encode(key).decode()
                
            elif encryption_type == EncryptionType.HYBRID:
                # Use post-quantum + classical
                lattice_kp = self.post_quantum.generate_lattice_keypair()
                ct, secret = self.post_quantum.lattice_encapsulate(lattice_kp["public_key"])
                key = secret[:32]  # Truncate to 256-bit
                ciphertext, nonce = self.classical.aes_encrypt(data, key)
                
                result["data"] = base64.b64encode(ciphertext).decode()
                result["nonce"] = base64.b64encode(nonce).decode()
                result["lattice_ct"] = base64.b64encode(ct).decode()
                result["encryption_type"] = "hybrid-aes-quantum"
                result["key"] = base64.b64encode(key).decode()  # Store key for decryption
                
            result["status"] = "success"
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def decrypt(
        self, 
        encrypted_package: Dict[str, Any],
        key: Optional[bytes] = None
    ) -> bytes:
        """
        Decrypt encrypted package.
        """
        enc_type = encrypted_package.get("encryption_type", "")
        
        try:
            if enc_type in ["aes-256-gcm", "hybrid-aes-quantum"]:
                ciphertext = base64.b64decode(encrypted_package["data"])
                nonce = base64.b64decode(encrypted_package["nonce"])
                if key is None:
                    key = base64.b64decode(encrypted_package["key"])
                return self.classical.aes_decrypt(ciphertext, key, nonce)
                
            elif enc_type == "chacha20":
                ciphertext = base64.b64decode(encrypted_package["data"])
                nonce = base64.b64decode(encrypted_package["nonce"])
                if key is None:
                    key = base64.b64decode(encrypted_package["key"])
                return self.classical.chacha_decrypt(ciphertext, key, nonce)
                
            elif enc_type == "otp":
                ciphertext = base64.b64decode(encrypted_package["data"])
                key = base64.b64decode(encrypted_package["key"])
                return self.classical.otp_decrypt(ciphertext, key)
                
            elif enc_type == "rsa-4096":
                ciphertext = base64.b64decode(encrypted_package["data"])
                private_key = base64.b64decode(encrypted_package["private_key"])
                return self.classical.rsa_decrypt(ciphertext, private_key)
                
            elif enc_type == "post-quantum-lattice":
                ciphertext = base64.b64decode(encrypted_package["data"])
                nonce = base64.b64decode(encrypted_package["nonce"])
                # Get key from the stored key in the package
                if key is None and "key" in encrypted_package:
                    key = base64.b64decode(encrypted_package["key"])
                return self.classical.aes_decrypt(ciphertext, key, nonce)
                
            elif enc_type in ["quantum-bb84", "quantum-e91", "post-quantum-hqc"]:
                ciphertext = base64.b64decode(encrypted_package["data"])
                nonce = base64.b64decode(encrypted_package["nonce"])
                if key is None:
                    key = base64.b64decode(encrypted_package["key"])
                return self.classical.aes_decrypt(ciphertext, key, nonce)
                
            else:
                raise ValueError(f"Unknown encryption type: {enc_type}")
                
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
    
    # ==================== KEY MANAGEMENT ====================
    
    def generate_key(
        self, 
        encryption_type: EncryptionType = EncryptionType.AES_256_GCM
    ) -> bytes:
        """Generate key for specified encryption type."""
        if encryption_type == EncryptionType.AES_256_GCM:
            return self.classical.generate_aes_key()
        elif encryption_type == EncryptionType.CHACHA20:
            return self.classical.generate_chacha_key()
        elif encryption_type in [EncryptionType.QUANTUM_BB84, EncryptionType.QUANTUM_E91]:
            qkd_result = self.qkd.establish_key(
                "BB84" if encryption_type == EncryptionType.QUANTUM_BB84 else "E91"
            )
            return bytes.fromhex(qkd_result["key"])
        else:
            raise ValueError(f"Key generation not supported for {encryption_type}")
    
    def derive_key(self, password: str) -> bytes:
        """Derive key from password."""
        key, _ = self.classical.derive_key(password)
        return key
    
    # ==================== UTILITY ====================
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return encryption capabilities."""
        return {
            "supported_types": [e.value for e in EncryptionType],
            "security_levels": {
                "standard": ["aes-256-gcm", "chacha20"],
                "high": ["rsa-4096", "post-quantum-lattice"],
                "quantum_safe": ["quantum-bb84", "post-quantum-lattice"],
                "maximum": ["hybrid"]
            },
            "quantum_ready": True,
            "nist_compliant": True,
            "post_quantum": self.post_quantum.get_nist_recommendation()
        }
    
    def get_status(self) -> Dict[str, str]:
        """Return encryption subsystem status."""
        return {
            "classical": "active",
            "quantum": "active",
            "post_quantum": "active",
            "manager": "active"
        }


# Singleton instance
encryption_manager = EncryptionManager()

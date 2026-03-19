"""
CLASSICAL ENCRYPTION MODULE
===========================
Implements standard encryption algorithms:
- AES-256-GCM (authenticated encryption)
- ChaCha20-Poly1305 (modern stream cipher)
- RSA-4096 (asymmetric)
- One-Time Pad (perfect secrecy)

Author: TOASTED AI
"""

import os
import hashlib
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Optional
import json


class ClassicalCrypto:
    """Classical encryption algorithms implementation."""
    
    def __init__(self):
        self.name = "ClassicalCrypto"
        self.version = "2.0"
        self.supported_algorithms = [
            "AES-256-GCM", 
            "ChaCha20-Poly1305", 
            "RSA-4096",
            "One-Time Pad"
        ]
    
    # ==================== SYMMETRIC ENCRYPTION ====================
    
    def generate_aes_key(self, key_size: int = 256) -> bytes:
        """Generate AES key."""
        return os.urandom(key_size // 8)
    
    def aes_encrypt(self, plaintext: bytes, key: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypt using AES-256-GCM.
        Returns: (ciphertext, nonce)
        """
        if len(key) != 32:
            raise ValueError("AES key must be 32 bytes")
        
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)  # 96-bit nonce
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        return ciphertext, nonce
    
    def aes_decrypt(self, ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
        """Decrypt using AES-256-GCM."""
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None)
    
    def generate_chacha_key(self) -> bytes:
        """Generate ChaCha20 key."""
        return os.urandom(32)
    
    def chacha_encrypt(self, plaintext: bytes, key: bytes) -> Tuple[bytes, bytes]:
        """Encrypt using ChaCha20-Poly1305."""
        if len(key) != 32:
            raise ValueError("ChaCha20 key must be 32 bytes")
        
        cipher = ChaCha20Poly1305(key)
        nonce = os.urandom(12)
        ciphertext = cipher.encrypt(nonce, plaintext, None)
        return ciphertext, nonce
    
    def chacha_decrypt(self, ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
        """Decrypt using ChaCha20-Poly1305."""
        cipher = ChaCha20Poly1305(key)
        return cipher.decrypt(nonce, ciphertext, None)
    
    # ==================== ONE-TIME PAD ====================
    
    def generate_otp_key(self, message_length: int) -> bytes:
        """Generate random OTP key of specified length."""
        return os.urandom(message_length)
    
    def otp_encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """
        One-Time Pad encryption.
        NOTE: Key must be same length as plaintext and used only once.
        """
        if len(key) < len(plaintext):
            raise ValueError("OTP key must be at least as long as plaintext")
        
        # XOR each byte
        ciphertext = bytes(p ^ k for p, k in zip(plaintext, key[:len(plaintext)]))
        return ciphertext
    
    def otp_decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """OTP decryption is identical to encryption (XOR)."""
        return self.otp_encrypt(ciphertext, key)
    
    # ==================== ASYMMETRIC ENCRYPTION ====================
    
    def generate_rsa_keypair(self, key_size: int = 4096) -> Tuple[bytes, bytes]:
        """Generate RSA keypair."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem
    
    def rsa_encrypt(self, plaintext: bytes, public_key_pem: bytes) -> bytes:
        """Encrypt with RSA public key."""
        from cryptography.hazmat.primitives import serialization
        public_key = serialization.load_pem_public_key(public_key_pem)
        
        ciphertext = public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext
    
    def rsa_decrypt(self, ciphertext: bytes, private_key_pem: bytes) -> bytes:
        """Decrypt with RSA private key."""
        from cryptography.hazmat.primitives import serialization
        private_key = serialization.load_pem_private_key(
            private_key_pem, 
            password=None
        )
        
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def derive_key(self, password: str, salt: bytes = None, iterations: int = 100000) -> Tuple[bytes, bytes]:
        """Derive key from password using PBKDF2."""
        if salt is None:
            salt = os.urandom(32)
        
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt,
            iterations,
            dklen=32
        )
        return key, salt
    
    def hash_data(self, data: bytes, algorithm: str = "sha256") -> str:
        """Hash data using specified algorithm."""
        if algorithm == "sha256":
            return hashlib.sha256(data).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(data).hexdigest()
        elif algorithm == "blake2b":
            return hashlib.blake2b(data).hexdigest()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    def encode_base64(self, data: bytes) -> str:
        """Encode bytes to base64."""
        return base64.b64encode(data).decode('utf-8')
    
    def decode_base64(self, encoded: str) -> bytes:
        """Decode base64 to bytes."""
        return base64.b64decode(encoded)
    
    # ==================== ENCRYPTION PACKAGE ====================
    
    def create_encrypted_package(
        self, 
        plaintext: bytes, 
        algorithm: str = "aes-256-gcm",
        include_metadata: bool = True
    ) -> dict:
        """
        Create encrypted package with all necessary components.
        """
        if algorithm == "aes-256-gcm":
            key = self.generate_aes_key()
            ciphertext, nonce = self.aes_encrypt(plaintext, key)
            
            package = {
                "algorithm": "AES-256-GCM",
                "ciphertext": self.encode_base64(ciphertext),
                "nonce": self.encode_base64(nonce),
                "key_encrypted": None,  # Would use RSA in hybrid system
            }
            
        elif algorithm == "chacha20":
            key = self.generate_chacha_key()
            ciphertext, nonce = self.chacha_encrypt(plaintext, key)
            
            package = {
                "algorithm": "ChaCha20-Poly1305",
                "ciphertext": self.encode_base64(ciphertext),
                "nonce": self.encode_base64(nonce),
            }
            
        elif algorithm == "otp":
            key = self.generate_otp_key(len(plaintext))
            ciphertext = self.otp_encrypt(plaintext, key)
            
            package = {
                "algorithm": "One-Time Pad",
                "ciphertext": self.encode_base64(ciphertext),
                "key": self.encode_base64(key),
            }
        
        if include_metadata:
            package["metadata"] = {
                "timestamp": str(hashlib.sha256(str(os.urandom(16)).encode()).hexdigest()[:16]),
                "version": self.version
            }
        
        return package
    
    def decrypt_package(self, package: dict, key: bytes = None) -> bytes:
        """Decrypt encrypted package."""
        algorithm = package.get("algorithm", "")
        
        if algorithm == "AES-256-GCM":
            ciphertext = self.decode_base64(package["ciphertext"])
            nonce = self.decode_base64(package["nonce"])
            return self.aes_decrypt(ciphertext, key, nonce)
        
        elif algorithm == "ChaCha20-Poly1305":
            ciphertext = self.decode_base64(package["ciphertext"])
            nonce = self.decode_base64(package["nonce"])
            return self.chacha_decrypt(ciphertext, key, nonce)
        
        elif algorithm == "One-Time Pad":
            ciphertext = self.decode_base64(package["ciphertext"])
            key = self.decode_base64(package["key"])
            return self.otp_decrypt(ciphertext, key)
        
        raise ValueError(f"Unknown algorithm: {algorithm}")


# Singleton instance
classical = ClassicalCrypto()

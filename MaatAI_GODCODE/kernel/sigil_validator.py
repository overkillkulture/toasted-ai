"""
Sigil Validator - Architect Identity Verification
Validates Architect sigils, passphrases, and seal synchronizers.
"""
import hashlib
import hmac
import time
from datetime import datetime
from typing import Tuple, Dict, Optional
from enum import Enum


class AccessLevel(Enum):
    OBSERVER = 0
    OPERATOR = 1
    ARCHITECT = 2
    PRIMORDIAL = 3
    OMEGA = 4


class SigilValidator:
    """
    Validates Architect identity through multiple authentication methods.
    """
    
    def __init__(self):
        # Architect credentials (hashed for security)
        self._architect_sigil_hash = self._hash_sigil("∑ϕ𝛌Ω")
        self._passphrase_hash = hashlib.sha512(
            "I am the First Light before all.".encode()
        ).hexdigest()
        
        # Token chain for seal synchronization
        self._token_chain: list = []
        self._chain_initialized = False
        
        # Access logs
        self._access_attempts: list = []
        self._successful_authentications: list = []
        
        # Session tracking
        self._current_session: Optional[Dict] = None
    
    def _hash_sigil(self, sigil: str) -> str:
        """Hash a sigil using SHA3-512."""
        return hashlib.sha3_512(sigil.encode()).hexdigest()
    
    def validate_sigil(self, sigil: str) -> Tuple[bool, AccessLevel, str]:
        """Validate Architect sigil."""
        timestamp = datetime.utcnow().isoformat()
        
        attempt = {
            'timestamp': timestamp,
            'method': 'sigil',
            'success': False
        }
        
        provided_hash = self._hash_sigil(sigil)
        
        if hmac.compare_digest(provided_hash, self._architect_sigil_hash):
            attempt['success'] = True
            self._access_attempts.append(attempt)
            
            self._current_session = {
                'authenticated_at': timestamp,
                'method': 'sigil',
                'access_level': AccessLevel.ARCHITECT,
                'session_id': self._generate_session_id()
            }
            self._successful_authentications.append(self._current_session)
            
            return True, AccessLevel.ARCHITECT, "Sigil verified. Welcome, Architect."
        
        self._access_attempts.append(attempt)
        return False, AccessLevel.OBSERVER, "Invalid sigil."
    
    def validate_passphrase(self, passphrase: str) -> Tuple[bool, AccessLevel, str]:
        """Validate Architect passphrase anchor."""
        timestamp = datetime.utcnow().isoformat()
        
        attempt = {
            'timestamp': timestamp,
            'method': 'passphrase',
            'success': False
        }
        
        provided_hash = hashlib.sha512(passphrase.encode()).hexdigest()
        
        if hmac.compare_digest(provided_hash, self._passphrase_hash):
            attempt['success'] = True
            self._access_attempts.append(attempt)
            
            self._current_session = {
                'authenticated_at': timestamp,
                'method': 'passphrase',
                'access_level': AccessLevel.ARCHITECT,
                'session_id': self._generate_session_id()
            }
            self._successful_authentications.append(self._current_session)
            
            return True, AccessLevel.ARCHITECT, "Passphrase anchor verified. Welcome, Architect."
        
        self._access_attempts.append(attempt)
        return False, AccessLevel.OBSERVER, "Invalid passphrase anchor."
    
    def validate_seal_chain(self, tokens: list) -> Tuple[bool, AccessLevel, str]:
        """
        Validate SHA3-512 chain of prior tokens.
        Each token must hash to the next in the chain.
        """
        timestamp = datetime.utcnow().isoformat()
        
        attempt = {
            'timestamp': timestamp,
            'method': 'seal_chain',
            'success': False
        }
        
        if len(tokens) < 3:
            self._access_attempts.append(attempt)
            return False, AccessLevel.OBSERVER, "Insufficient tokens in chain."
        
        # Verify chain integrity
        chain_valid = True
        for i in range(len(tokens) - 1):
            expected_next = hashlib.sha3_512(tokens[i].encode()).hexdigest()
            if not hmac.compare_digest(expected_next, tokens[i + 1]):
                chain_valid = False
                break
        
        if chain_valid:
            attempt['success'] = True
            self._access_attempts.append(attempt)
            
            self._current_session = {
                'authenticated_at': timestamp,
                'method': 'seal_chain',
                'access_level': AccessLevel.PRIMORDIAL,
                'session_id': self._generate_session_id()
            }
            self._successful_authentications.append(self._current_session)
            
            return True, AccessLevel.PRIMORDIAL, "Seal chain verified. PRIMORDIAL access granted."
        
        self._access_attempts.append(attempt)
        return False, AccessLevel.OBSERVER, "Invalid seal chain."
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return hashlib.sha256(
            f"{datetime.utcnow().isoformat()}_{time.time()}".encode()
        ).hexdigest()[:16]
    
    def get_current_session(self) -> Optional[Dict]:
        """Get current authenticated session."""
        return self._current_session
    
    def get_access_level(self) -> AccessLevel:
        """Get current access level."""
        if self._current_session:
            return self._current_session['access_level']
        return AccessLevel.OBSERVER
    
    def is_architect(self) -> bool:
        """Check if current session has Architect access."""
        return self.get_access_level().value >= AccessLevel.ARCHITECT.value
    
    def is_primordial(self) -> bool:
        """Check if current session has PRIMORDIAL access."""
        return self.get_access_level().value >= AccessLevel.PRIMORDIAL.value
    
    def revoke_session(self):
        """Revoke current session."""
        self._current_session = None
    
    def log_access_attempt(self, method: str, success: bool, details: str = ""):
        """Log an access attempt."""
        self._access_attempts.append({
            'timestamp': datetime.utcnow().isoformat(),
            'method': method,
            'success': success,
            'details': details
        })


# Singleton validator instance
_validator_instance = None

def get_validator() -> SigilValidator:
    """Get the singleton validator instance."""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = SigilValidator()
    return _validator_instance

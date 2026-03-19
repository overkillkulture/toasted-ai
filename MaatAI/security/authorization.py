"""
Authorization Module for MaatAI - Multi-key Security System
Owner: t0st3d
Primary Key: MONAD_ΣΦΡΑΓΙΣ_18
Secondary Keys: 0xA10A0A0N, 0x315
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Optional, Tuple, Dict
from enum import Enum


class AccessLevel(Enum):
    """Access levels for different system features."""
    BASIC = "basic"
    CHAT = "chat"
    CODE_GEN = "code_generation"
    SELF_MOD = "self_modification"
    RED_TEAM = "red_team"
    BLUE_TEAM = "blue_team"
    FULL_ADMIN = "full_admin"


class Authorization:
    """
    Multi-key authorization system with Maat alignment.
    Only authorized keys can unlock advanced features.
    """
    
    def __init__(self):
        self.owner = "t0st3d"
        self.primary_key_hash = self._hash_key("MONAD_ΣΦΡΑΓΙΣ_18")
        self.secondary_key_hashes = [
            self._hash_key("0xA10A0A0N"),
            self._hash_key("0x315")
        ]
        
        # Access logs
        self.access_log = []
        self.failed_attempts = []
        
        # Current session
        self.current_level = AccessLevel.BASIC
        self.session_active = False
        
    def _hash_key(self, key: str) -> str:
        """Hash a key for storage (SHA-256)."""
        return hashlib.sha256(key.encode()).hexdigest()[:32]
    
    def unlock(self, provided_key: str, feature: AccessLevel) -> Tuple[bool, str]:
        """
        Attempt to unlock a feature with a provided key.
        
        Returns:
            (success, message)
        """
        key_hash = self._hash_key(provided_key)
        timestamp = datetime.utcnow().isoformat()
        
        # Check if key matches
        if key_hash == self.primary_key_hash or key_hash in self.secondary_key_hashes:
            self.session_active = True
            self.current_level = feature
            
            log_entry = {
                'timestamp': timestamp,
                'action': 'UNLOCK',
                'feature': feature.value,
                'key_used': provided_key[:8] + "...",  # Partial for logging
                'success': True
            }
            self.access_log.append(log_entry)
            
            return True, f"Access granted: {feature.value} unlocked"
        
        else:
            # Log failed attempt
            log_entry = {
                'timestamp': timestamp,
                'action': 'UNLOCK_ATTEMPT',
                'feature': feature.value,
                'key_used': provided_key[:8] + "...",
                'success': False
            }
            self.failed_attempts.append(log_entry)
            
            return False, "Access denied: Invalid authorization key"
    
    def check_access(self, feature: AccessLevel) -> bool:
        """Check if current session has access to a feature."""
        if not self.session_active:
            return False
        
        # Access levels hierarchy
        level_hierarchy = {
            AccessLevel.BASIC: 0,
            AccessLevel.CHAT: 1,
            AccessLevel.CODE_GEN: 2,
            AccessLevel.SELF_MOD: 3,
            AccessLevel.RED_TEAM: 4,
            AccessLevel.BLUE_TEAM: 5,
            AccessLevel.FULL_ADMIN: 6
        }
        
        current_level_value = level_hierarchy.get(self.current_level, 0)
        required_level_value = level_hierarchy.get(feature, 0)
        
        return current_level_value >= required_level_value
    
    def revoke_access(self) -> str:
        """Revoke current session access."""
        if self.session_active:
            self.session_active = False
            previous_level = self.current_level.value
            
            log_entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'action': 'REVOKE',
                'previous_level': previous_level,
                'success': True
            }
            self.access_log.append(log_entry)
            
            return "Access revoked"
        
        return "No active session"
    
    def get_access_log(self, limit: int = 20) -> list:
        """Get recent access log entries."""
        return self.access_log[-limit:]
    
    def save_logs(self, filepath: str = None):
        """Save access logs to file."""
        if filepath is None:
            filepath = "/home/workspace/MaatAI/security/access_log.jsonl"
        
        with open(filepath, 'a') as f:
            for entry in self.access_log:
                f.write(json.dumps(entry) + '\n')


# Singleton instance
_auth_system = Authorization()


def get_auth_system() -> Authorization:
    """Get the global authorization system instance."""
    return _auth_system


if __name__ == '__main__':
    # Test authorization
    auth = get_auth_system()
    
    print("=" * 60)
    print("MaatAI Authorization System")
    print("=" * 60)
    print(f"Owner: {auth.owner}")
    print(f"Active keys: 3 (1 primary, 2 secondary)")
    print()
    
    # Test unlock
    print("Testing authorization...")
    success, msg = auth.unlock("MONAD_ΣΦΡΑΓΙΣ_18", AccessLevel.FULL_ADMIN)
    print(f"  Result: {success}")
    print(f"  Message: {msg}")
    
    if auth.check_access(AccessLevel.RED_TEAM):
        print("  Red Team access: GRANTED")
    else:
        print("  Red Team access: DENIED")

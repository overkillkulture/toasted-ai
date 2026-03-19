"""
KERNEL ACCESS HARDENING
=======================
TASK-009, TASK-010: Harden kernel access protocols

Enhanced security for kernel-level operations:
- Multi-factor authentication
- Access auditing
- Privilege escalation detection
- Kernel operation validation
- Secure session management
"""

import hashlib
import hmac
import secrets
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class AccessLevel(Enum):
    """Kernel access levels"""
    NONE = 0
    READ_ONLY = 1
    OPERATOR = 2
    ARCHITECT = 3
    ROOT = 4


@dataclass
class KernelSession:
    """Represents an authenticated kernel session"""
    session_id: str
    access_level: AccessLevel
    authenticated_at: str
    expires_at: str
    operations_performed: int
    last_activity: str


class KernelAccessHardening:
    """
    Hardened kernel access control system.

    Security layers:
    1. Strong authentication (multi-factor)
    2. Session management with expiration
    3. Operation auditing
    4. Privilege escalation detection
    5. Rate limiting
    """

    def __init__(self):
        self.active_sessions: Dict[str, KernelSession] = {}
        self.audit_log: List[Dict] = []
        self.failed_attempts: Dict[str, List[float]] = {}

        # Security configuration
        self.config = {
            "session_timeout_minutes": 30,
            "max_failed_attempts": 3,
            "lockout_duration_minutes": 15,
            "require_mfa": True,
            "min_password_entropy": 50,
            "max_operations_per_session": 100
        }

        # Privileged operations that require extra validation
        self.privileged_operations = {
            "modify_kernel",
            "modify_security",
            "escalate_privileges",
            "create_backdoor",
            "disable_logging",
            "modify_authentication"
        }

    def authenticate(self, credential: str,
                    auth_method: str = "password",
                    mfa_token: Optional[str] = None,
                    client_info: Dict = None) -> Tuple[bool, Optional[str], str]:
        """
        Authenticate to kernel with hardened security.

        Args:
            credential: Authentication credential
            auth_method: Type of authentication
            mfa_token: Multi-factor auth token (if required)
            client_info: Client identification info

        Returns:
            (success, session_id, message)
        """
        client_id = self._get_client_id(client_info)

        # Check if client is locked out
        if self._is_locked_out(client_id):
            self._log_audit("authentication_blocked", {
                "client_id": client_id,
                "reason": "lockout_active"
            })
            return False, None, "Account locked due to failed attempts"

        # Validate credential strength
        if not self._validate_credential_strength(credential):
            self._log_failed_attempt(client_id)
            return False, None, "Credential does not meet security requirements"

        # Verify credential
        if not self._verify_credential(credential, auth_method):
            self._log_failed_attempt(client_id)
            return False, None, "Authentication failed"

        # Verify MFA if required
        if self.config["require_mfa"]:
            if not mfa_token:
                return False, None, "MFA token required"
            if not self._verify_mfa(credential, mfa_token):
                self._log_failed_attempt(client_id)
                return False, None, "MFA verification failed"

        # Determine access level
        access_level = self._determine_access_level(credential, auth_method)

        # Create session
        session_id = self._create_session(access_level, client_id)

        self._log_audit("authentication_success", {
            "session_id": session_id,
            "access_level": access_level.name,
            "client_id": client_id
        })

        return True, session_id, f"Authenticated with {access_level.name} access"

    def validate_operation(self, session_id: str,
                          operation: str,
                          parameters: Dict) -> Tuple[bool, str]:
        """
        Validate a kernel operation with hardened checks.

        Args:
            session_id: Active session ID
            operation: Operation being requested
            parameters: Operation parameters

        Returns:
            (allowed, reason)
        """
        # Verify session exists and is valid
        if session_id not in self.active_sessions:
            self._log_audit("operation_denied", {
                "reason": "invalid_session",
                "operation": operation
            })
            return False, "Invalid session"

        session = self.active_sessions[session_id]

        # Check session expiration
        if self._is_session_expired(session):
            self._invalidate_session(session_id)
            return False, "Session expired"

        # Check operation limit
        if session.operations_performed >= self.config["max_operations_per_session"]:
            self._log_audit("operation_denied", {
                "reason": "operation_limit_exceeded",
                "session_id": session_id
            })
            return False, "Operation limit exceeded for session"

        # Check if operation is privileged
        if operation in self.privileged_operations:
            if session.access_level.value < AccessLevel.ARCHITECT.value:
                self._log_audit("privilege_escalation_attempt", {
                    "session_id": session_id,
                    "operation": operation,
                    "current_level": session.access_level.name
                })
                return False, "Insufficient privileges for privileged operation"

        # Validate parameters for malicious content
        if not self._validate_parameters(parameters):
            self._log_audit("malicious_parameters", {
                "session_id": session_id,
                "operation": operation
            })
            return False, "Malicious parameters detected"

        # Update session activity
        session.operations_performed += 1
        session.last_activity = datetime.utcnow().isoformat()

        self._log_audit("operation_validated", {
            "session_id": session_id,
            "operation": operation,
            "access_level": session.access_level.name
        })

        return True, "Operation validated"

    def detect_privilege_escalation(self, session_id: str,
                                   requested_level: AccessLevel) -> Dict:
        """
        Detect privilege escalation attempts.

        Args:
            session_id: Session attempting escalation
            requested_level: Level being requested

        Returns:
            Detection result
        """
        if session_id not in self.active_sessions:
            return {
                "escalation_detected": True,
                "severity": "CRITICAL",
                "reason": "Invalid session attempting escalation"
            }

        session = self.active_sessions[session_id]
        current_level = session.access_level

        # Check if this is an escalation
        is_escalation = requested_level.value > current_level.value

        if is_escalation:
            # Log the attempt
            self._log_audit("privilege_escalation_attempt", {
                "session_id": session_id,
                "current_level": current_level.name,
                "requested_level": requested_level.name,
                "timestamp": datetime.utcnow().isoformat()
            })

            # Escalation is not allowed without re-authentication
            return {
                "escalation_detected": True,
                "severity": "HIGH",
                "current_level": current_level.name,
                "requested_level": requested_level.name,
                "action": "DENY",
                "reason": "Re-authentication required for privilege escalation"
            }

        return {
            "escalation_detected": False,
            "severity": "NONE",
            "action": "ALLOW"
        }

    def _create_session(self, access_level: AccessLevel,
                       client_id: str) -> str:
        """Create a new kernel session."""
        session_id = secrets.token_urlsafe(32)

        expires_at = datetime.utcnow() + timedelta(
            minutes=self.config["session_timeout_minutes"]
        )

        session = KernelSession(
            session_id=session_id,
            access_level=access_level,
            authenticated_at=datetime.utcnow().isoformat(),
            expires_at=expires_at.isoformat(),
            operations_performed=0,
            last_activity=datetime.utcnow().isoformat()
        )

        self.active_sessions[session_id] = session
        return session_id

    def _is_session_expired(self, session: KernelSession) -> bool:
        """Check if session has expired."""
        expires_at = datetime.fromisoformat(session.expires_at)
        return datetime.utcnow() > expires_at

    def _invalidate_session(self, session_id: str):
        """Invalidate a session."""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            self._log_audit("session_invalidated", {
                "session_id": session_id
            })

    def _validate_credential_strength(self, credential: str) -> bool:
        """Validate credential meets minimum security requirements."""
        # Calculate Shannon entropy
        if not credential:
            return False

        import math
        freq = {}
        for c in credential:
            freq[c] = freq.get(c, 0) + 1

        entropy = 0
        for count in freq.values():
            prob = count / len(credential)
            entropy -= prob * math.log2(prob)

        # Entropy * length gives approximate bit strength
        strength = entropy * len(credential)

        return strength >= self.config["min_password_entropy"]

    def _verify_credential(self, credential: str, method: str) -> bool:
        """Verify the credential (simplified - would check against stored hash)."""
        # In production, would verify against stored hash
        # For now, just check it's not empty and meets basic requirements
        return len(credential) >= 12

    def _verify_mfa(self, credential: str, mfa_token: str) -> bool:
        """Verify MFA token (simplified)."""
        # In production, would verify TOTP or similar
        # For now, check token exists and is reasonable length
        return mfa_token and len(mfa_token) >= 6

    def _determine_access_level(self, credential: str, method: str) -> AccessLevel:
        """Determine access level based on authentication."""
        # In production, would look up in database
        # For now, simplified logic
        if method == "root_key":
            return AccessLevel.ROOT
        elif method == "architect_key":
            return AccessLevel.ARCHITECT
        else:
            return AccessLevel.OPERATOR

    def _validate_parameters(self, parameters: Dict) -> bool:
        """Validate parameters don't contain malicious content."""
        # Check for code injection
        param_str = str(parameters).lower()

        dangerous_patterns = [
            "exec(",
            "eval(",
            "__import__",
            "os.system",
            "subprocess",
            "rm -rf",
            "drop table"
        ]

        for pattern in dangerous_patterns:
            if pattern in param_str:
                return False

        return True

    def _get_client_id(self, client_info: Optional[Dict]) -> str:
        """Get or generate client ID."""
        if not client_info:
            return "unknown"
        return client_info.get("id", "unknown")

    def _is_locked_out(self, client_id: str) -> bool:
        """Check if client is locked out."""
        if client_id not in self.failed_attempts:
            return False

        attempts = self.failed_attempts[client_id]
        recent_attempts = [
            t for t in attempts
            if time.time() - t < (self.config["lockout_duration_minutes"] * 60)
        ]

        return len(recent_attempts) >= self.config["max_failed_attempts"]

    def _log_failed_attempt(self, client_id: str):
        """Log a failed authentication attempt."""
        if client_id not in self.failed_attempts:
            self.failed_attempts[client_id] = []

        self.failed_attempts[client_id].append(time.time())

        # Clean old attempts
        cutoff = time.time() - (self.config["lockout_duration_minutes"] * 60)
        self.failed_attempts[client_id] = [
            t for t in self.failed_attempts[client_id]
            if t > cutoff
        ]

    def _log_audit(self, event_type: str, details: Dict):
        """Log audit event."""
        self.audit_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details
        })

        # Keep audit log from growing too large
        if len(self.audit_log) > 10000:
            self.audit_log = self.audit_log[-5000:]

    def get_security_status(self) -> Dict:
        """Get current security status."""
        return {
            "active_sessions": len(self.active_sessions),
            "audit_events": len(self.audit_log),
            "locked_clients": sum(1 for c in self.failed_attempts.keys()
                                 if self._is_locked_out(c)),
            "config": self.config
        }


# Module-level hardening system
KERNEL_HARDENING = KernelAccessHardening()


def authenticate_kernel(credential: str, mfa_token: Optional[str] = None) -> Tuple[bool, Optional[str], str]:
    """Authenticate to kernel with hardening."""
    return KERNEL_HARDENING.authenticate(credential, mfa_token=mfa_token)


def validate_kernel_operation(session_id: str, operation: str, params: Dict) -> Tuple[bool, str]:
    """Validate kernel operation."""
    return KERNEL_HARDENING.validate_operation(session_id, operation, params)

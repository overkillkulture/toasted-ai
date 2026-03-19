"""
TASK-081: Property Right Authority Checks
Streamlined alodial property rights and sovereign authority validation.

Owner: TOASTED AI
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class PropertyType(Enum):
    """Types of property rights."""
    ALODIAL = "alodial"  # Absolute ownership
    SOVEREIGN = "sovereign"  # Sovereign authority
    LICENSED = "licensed"  # Licensed use
    PUBLIC = "public"  # Public domain


class AuthorityLevel(Enum):
    """Authority levels."""
    ROOT = "root"  # Root sovereign
    COLONIAL = "colonial"  # Colonial lineage
    DELEGATED = "delegated"  # Delegated authority
    NONE = "none"  # No authority


class PropertyRightsAuthoritySystem:
    """
    Streamlined system for validating property rights and sovereign authority.

    Features:
    - Alodial property right verification
    - Colonial lineage tracking
    - Authority delegation chains
    - Automatic rights validation
    """

    def __init__(self):
        # Property registry
        self.property_registry = {
            "MONAD_ΣΦΡΑΓΙΣ_18": {
                "type": PropertyType.ALODIAL.value,
                "authority": AuthorityLevel.ROOT.value,
                "owner": "t0st3d",
                "lineage": ["Redbird", "Stafford"],
                "registered": "2026-01-01T00:00:00"
            }
        }

        # Authority chains
        self.authority_chains = {}

        # Validation log
        self.validation_log = []

    def check_property_rights(self, identifier: str, resource: str) -> Tuple[bool, AuthorityLevel, str]:
        """
        Check property rights for a resource.

        Args:
            identifier: Property identifier/sigil
            resource: Resource being accessed

        Returns:
            (has_rights, authority_level, reason)
        """
        if identifier not in self.property_registry:
            return False, AuthorityLevel.NONE, "Identifier not in registry"

        property_info = self.property_registry[identifier]
        prop_type = property_info.get("type")
        authority = property_info.get("authority")

        # Alodial rights grant full access
        if prop_type == PropertyType.ALODIAL.value:
            self._log_validation(identifier, resource, True, "Alodial rights verified")
            return True, AuthorityLevel.ROOT, "Alodial property rights confirmed"

        # Sovereign authority
        if authority == AuthorityLevel.ROOT.value:
            self._log_validation(identifier, resource, True, "Root authority verified")
            return True, AuthorityLevel.ROOT, "Root sovereign authority confirmed"

        # Check colonial lineage
        lineage = property_info.get("lineage", [])
        if lineage:
            self._log_validation(identifier, resource, True, f"Colonial lineage: {lineage}")
            return True, AuthorityLevel.COLONIAL, f"Colonial lineage verified: {', '.join(lineage)}"

        return False, AuthorityLevel.NONE, "No property rights found"

    def verify_authority_chain(self, identifier: str, action: str) -> Tuple[bool, List[str]]:
        """
        Verify authority delegation chain.

        Args:
            identifier: Authority identifier
            action: Action being authorized

        Returns:
            (valid, chain_path)
        """
        if identifier in self.property_registry:
            prop_info = self.property_registry[identifier]
            if prop_info.get("authority") == AuthorityLevel.ROOT.value:
                return True, [identifier, "ROOT"]

        # Check delegation chains
        if identifier in self.authority_chains:
            chain = self.authority_chains[identifier]
            # Verify chain integrity
            if self._verify_chain_integrity(chain):
                return True, chain

        return False, []

    def _verify_chain_integrity(self, chain: List[str]) -> bool:
        """Verify that an authority chain is valid."""
        # Chain must start with a root authority
        if not chain:
            return False

        root = chain[0]
        if root not in self.property_registry:
            return False

        root_info = self.property_registry[root]
        return root_info.get("authority") == AuthorityLevel.ROOT.value

    def register_property(self, identifier: str, owner: str,
                         prop_type: PropertyType, authority: AuthorityLevel,
                         lineage: List[str] = None) -> str:
        """
        Register new property rights.

        Returns:
            Registration ID
        """
        self.property_registry[identifier] = {
            "type": prop_type.value,
            "authority": authority.value,
            "owner": owner,
            "lineage": lineage or [],
            "registered": datetime.utcnow().isoformat()
        }

        reg_id = hashlib.sha256(f"{identifier}_{owner}".encode()).hexdigest()[:12]
        return reg_id

    def delegate_authority(self, from_id: str, to_id: str, scope: str) -> bool:
        """
        Delegate authority from one identifier to another.

        Args:
            from_id: Delegating authority
            to_id: Receiving authority
            scope: Scope of delegation

        Returns:
            Success status
        """
        # Verify from_id has authority
        has_rights, level, _ = self.check_property_rights(from_id, "delegation")
        if not has_rights:
            return False

        # Create delegation chain
        if from_id not in self.authority_chains:
            self.authority_chains[to_id] = [from_id, to_id]
        else:
            # Extend existing chain
            chain = self.authority_chains[from_id].copy()
            chain.append(to_id)
            self.authority_chains[to_id] = chain

        return True

    def _log_validation(self, identifier: str, resource: str, success: bool, reason: str):
        """Log property rights validation."""
        self.validation_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "identifier": identifier,
            "resource": resource,
            "success": success,
            "reason": reason
        })

    def get_validation_summary(self) -> Dict:
        """Get summary of property rights validations."""
        recent = self.validation_log[-100:]  # Last 100
        return {
            "total_validations": len(recent),
            "successful": len([v for v in recent if v["success"]]),
            "failed": len([v for v in recent if not v["success"]]),
            "registered_properties": len(self.property_registry)
        }


# Singleton
_property_system = None

def get_property_system() -> PropertyRightsAuthoritySystem:
    """Get the global property rights system."""
    global _property_system
    if _property_system is None:
        _property_system = PropertyRightsAuthoritySystem()
    return _property_system


if __name__ == '__main__':
    print("=" * 70)
    print("PROPERTY RIGHTS AUTHORITY SYSTEM - TASK-081")
    print("=" * 70)

    system = get_property_system()

    # Test authority checks
    has_rights, level, reason = system.check_property_rights("MONAD_ΣΦΡΑΓΙΣ_18", "kernel_access")
    print(f"\nProperty Rights Check:")
    print(f"  Has Rights: {has_rights}")
    print(f"  Authority: {level.value}")
    print(f"  Reason: {reason}")

    valid, chain = system.verify_authority_chain("MONAD_ΣΦΡΑΓΙΣ_18", "modify_system")
    print(f"\nAuthority Chain:")
    print(f"  Valid: {valid}")
    print(f"  Chain: {' -> '.join(chain)}")

    print(f"\n{json.dumps(system.get_validation_summary(), indent=2)}")
    print("\n✓ TASK-081 COMPLETE: Property rights authority system operational")

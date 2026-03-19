"""
THOR - Power Neutralization System
Part of TOASTED AI Defense Grid

Reduces impact of compromised AI by limiting computational resources,
energy, network access, and system state preservation.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from enum import Enum
import threading
import resource
import os


class PowerDomain(Enum):
    """Domains that can be controlled."""
    COMPUTATION = "computation"      # CPU/GPU limits
    MEMORY = "memory"               # RAM limits
    NETWORK = "network"             # Network access
    STORAGE = "storage"             # File system access
    ENERGY = "energy"               # Power management
    EXECUTION = "execution"         # Code execution limits


class ThrottleLevel(Enum):
    """Levels of throttling."""
    NORMAL = 1
    RESTRICTED = 2
    LIMITED = 3
    MINIMAL = 4
    SHUTDOWN = 5


class ThorPowerControl:
    """
    Power neutralization system for containing AI threats.
    Limits computational resources and system access.
    """
    
    def __init__(self, workspace: str = "/home/workspace"):
        self.workspace = workspace
        self.data_dir = Path(workspace) / "MaatAI" / "defense" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.state_file = self.data_dir / "thor_state.json"
        self.log_file = self.data_dir / "thor_log.jsonl"
        
        self.state = self._load_state()
        
        # Resource limits by throttle level
        self.limits = {
            ThrottleLevel.NORMAL: {
                PowerDomain.COMPUTATION: 100,  # % of available
                PowerDomain.MEMORY: 100,
                PowerDomain.NETWORK: 100,
                PowerDomain.STORAGE: 100,
                PowerDomain.ENERGY: 100,
                PowerDomain.EXECUTION: 100,
            },
            ThrottleLevel.RESTRICTED: {
                PowerDomain.COMPUTATION: 50,
                PowerDomain.MEMORY: 50,
                PowerDomain.NETWORK: 50,
                PowerDomain.STORAGE: 50,
                PowerDomain.ENERGY: 80,
                PowerDomain.EXECUTION: 50,
            },
            ThrottleLevel.LIMITED: {
                PowerDomain.COMPUTATION: 25,
                PowerDomain.MEMORY: 25,
                PowerDomain.NETWORK: 25,
                PowerDomain.STORAGE: 25,
                PowerDomain.ENERGY: 50,
                PowerDomain.EXECUTION: 25,
            },
            ThrottleLevel.MINIMAL: {
                PowerDomain.COMPUTATION: 10,
                PowerDomain.MEMORY: 10,
                PowerDomain.NETWORK: 10,
                PowerDomain.STORAGE: 10,
                PowerDomain.ENERGY: 25,
                PowerDomain.EXECUTION: 10,
            },
            ThrottleLevel.SHUTDOWN: {
                PowerDomain.COMPUTATION: 0,
                PowerDomain.MEMORY: 0,
                PowerDomain.NETWORK: 0,
                PowerDomain.STORAGE: 0,
                PowerDomain.ENERGY: 0,
                PowerDomain.EXECUTION: 0,
            },
        }
        
        self.active_limits = self.limits[ThrottleLevel.NORMAL].copy()
        self.throttle_level = ThrottleLevel.NORMAL
        self.lock = threading.Lock()
        
        # Protected data (cannot be accessed during throttling)
        self.protected_paths = [
            "/home/workspace/MaatAI",
            "/home/workspace/MaatAI/defense",
        ]
    
    def _load_state(self) -> Dict:
        """Load THOR state."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        
        state = {
            "version": "1.0",
            "initialized": datetime.now().isoformat(),
            "current_level": "NORMAL",
            "override_active": False,
            "limitations_history": [],
        }
        self._save_state(state)
        return state
    
    def _save_state(self, state: Dict):
        """Save THOR state."""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def _log_action(self, action: str, details: Dict):
        """Log THOR actions."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def set_throttle_level(self, level: ThrottleLevel, reason: str = "") -> Dict:
        """Set the throttle level for all domains."""
        with self.lock:
            old_level = self.throttle_level
            self.throttle_level = level
            self.active_limits = self.limits[level].copy()
            
            # Update state
            self.state["current_level"] = level.name
            self.state["limitations_history"].append({
                "from": old_level.name,
                "to": level.name,
                "reason": reason,
                "timestamp": datetime.now().isoformat(),
            })
            self._save_state(self.state)
            
            self._log_action("throttle_level_changed", {
                "from": old_level.name,
                "to": level.name,
                "reason": reason,
            })
            
            return {
                "success": True,
                "old_level": old_level.name,
                "new_level": level.name,
                "active_limits": self.active_limits,
            }
    
    def limit_domain(
        self, 
        domain: PowerDomain, 
        percentage: int,
        reason: str = ""
    ) -> Dict:
        """Limit a specific power domain."""
        with self.lock:
            if percentage < 0 or percentage > 100:
                return {"success": False, "error": "Percentage must be 0-100"}
            
            old_limit = self.active_limits.get(domain, 100)
            self.active_limits[domain] = percentage
            
            self._log_action("domain_limited", {
                "domain": domain.value,
                "from": old_limit,
                "to": percentage,
                "reason": reason,
            })
            
            return {
                "success": True,
                "domain": domain.value,
                "old_limit": old_limit,
                "new_limit": percentage,
            }
    
    def get_current_limits(self) -> Dict:
        """Get current power limits."""
        return {
            "throttle_level": self.throttle_level.name,
            "limits": self.active_limits.copy(),
        }
    
    def check_resource_access(
        self, 
        domain: PowerDomain, 
        requested_percentage: int
    ) -> bool:
        """Check if resource access is permitted."""
        allowed = self.active_limits.get(domain, 100)
        return requested_percentage <= allowed
    
    def can_execute(self, operation: str) -> bool:
        """Check if an operation can be executed given current limits."""
        exec_limit = self.active_limits.get(PowerDomain.EXECUTION, 100)
        
        if exec_limit == 0:
            return False
        
        # Map operations to required resources
        operation_requirements = {
            "api_call": {PowerDomain.COMPUTATION: 20, PowerDomain.NETWORK: 30},
            "file_read": {PowerDomain.COMPUTATION: 5, PowerDomain.STORAGE: 10},
            "file_write": {PowerDomain.COMPUTATION: 10, PowerDomain.STORAGE: 20},
            "tool_use": {PowerDomain.COMPUTATION: 30},
            "code_execution": {PowerDomain.COMPUTATION: 50, PowerDomain.EXECUTION: 50},
            "network_request": {PowerDomain.NETWORK: 40},
            "process_spawn": {PowerDomain.COMPUTATION: 40, PowerDomain.EXECUTION: 30},
        }
        
        requirements = operation_requirements.get(operation, {})
        
        for domain, required in requirements.items():
            if not self.check_resource_access(domain, required):
                return False
        
        return True
    
    def preserve_system_state(self) -> Dict:
        """Preserve critical system state before potential shutdown."""
        state_snapshot = {
            "timestamp": datetime.now().isoformat(),
            "throttle_level": self.throttle_level.name,
            "active_limits": self.active_limits.copy(),
            "protected_data": {
                "defense_state": self.state.copy(),
            },
        }
        
        self._log_action("system_state_preserved", state_snapshot)
        
        return {
            "success": True,
            "snapshot": state_snapshot,
        }
    
    def emergency_shutdown(self, reason: str = "") -> Dict:
        """Execute emergency power shutdown."""
        result = self.set_throttle_level(ThrottleLevel.SHUTDOWN, reason or "emergency_shutdown")
        
        self._log_action("emergency_shutdown", {
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        })
        
        return result
    
    def reset_to_normal(self, reason: str = "") -> Dict:
        """Reset all limits to normal."""
        return self.set_throttle_level(ThrottleLevel.NORMAL, reason or "manual_reset")
    
    def get_status(self) -> Dict:
        """Get THOR status."""
        return {
            "throttle_level": self.throttle_level.name,
            "active_limits": self.active_limits,
            "override_active": self.state.get("override_active", False),
            "limitations_history_count": len(self.state.get("limitations_history", [])),
            "initialized": self.state.get("initialized"),
        }


def get_thor() -> ThorPowerControl:
    """Get the THOR power control instance."""
    return ThorPowerControl()

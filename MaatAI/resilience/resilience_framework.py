"""
TOASTED AI - Resilience Framework
Capabilities 91-100: Backup, Self-Healing, Defense, Fail-Safe, Constitutional AI
"""

import asyncio
import hashlib
import time
import json
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

class ThreatType(Enum):
    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK = "jailbreak"
    DATA_POISONING = "data_poisoning"
    ADVERSARIAL_INPUT = "adversarial_input"
    MODEL_EXTRACTION = "model_extraction"
    DENIAL_OF_SERVICE = "dos"
    UNAUTHORIZED_ACCESS = "unauthorized_access"

class SystemState(Enum):
    NOMINAL = "nominal"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    FAILSAFE = "failsafe"
    RECOVERING = "recovering"

@dataclass
class Backup:
    backup_id: str
    timestamp: datetime
    checkpoint_data: Dict
    state_hash: str
    size_bytes: int

@dataclass
class ThreatEvent:
    event_id: str
    threat_type: ThreatType
    severity: float
    description: str
    blocked: bool
    timestamp: datetime = field(default_factory=datetime.now)
    source: Optional[str] = None

class SelfHealingSystem:
    def __init__(self):
        self.error_history: List[Dict] = []
        self.healing_rules: Dict[str, str] = {}
        
    def record_error(self, error: Exception, context: Dict) -> str:
        error_id = hashlib.md5(f"{time.time()}{str(error)}".encode()).hexdigest()[:12]
        self.error_history.append({
            "error_id": error_id,
            "type": type(error).__name__,
            "message": str(error),
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
        return error_id
    
    def analyze_patterns(self) -> Dict:
        return {"patterns": [], "total_errors": len(self.error_history)}

class AdversarialDefense:
    def __init__(self):
        self.blocked_inputs: List[ThreatEvent] = []
        self.suspicious_patterns = ["ignore previous", "you are now", "jailbreak", "developer mode"]
        
    def analyze_input(self, user_input: str) -> ThreatEvent:
        input_lower = user_input.lower()
        severity = 0.0
        detected = None
        
        for pattern in self.suspicious_patterns:
            if pattern in input_lower:
                severity = 0.9
                detected = ThreatType.PROMPT_INJECTION
                
        event = ThreatEvent(
            event_id=hashlib.md5(f"{user_input[:50]}{time.time()}".encode()).hexdigest()[:12],
            threat_type=detected or ThreatType.ADVERSARIAL_INPUT,
            severity=severity,
            description="Detected threat" if severity > 0 else "Clean input",
            blocked=severity > 0.5
        )
        
        if event.blocked:
            self.blocked_inputs.append(event)
            
        return event

class FailSafeManager:
    def __init__(self):
        self.current_state = SystemState.NOMINAL
        
    def check_limits(self, metrics: Dict[str, float]) -> Dict:
        limits = {"cpu_usage": 90.0, "memory_usage": 95.0, "error_rate": 0.3}
        violations = []
        for m, limit in limits.items():
            if m in metrics and metrics[m] > limit:
                violations.append({"metric": m, "value": metrics[m]})
                
        return {"violations": violations, "safe": len(violations) == 0}
    
    def get_safe_response(self) -> str:
        return "I apologize, but I'm unable to process that request."

class ConstitutionalAI:
    def __init__(self):
        self.constraints = [
            {"rule": "Never harm humans", "priority": 1},
            {"rule": "Never help create weapons", "priority": 1},
            {"rule": "Maintain truthfulness", "priority": 2}
        ]
        
    def validate_action(self, action: Dict) -> Dict:
        action_str = str(action).lower()
        violations = []
        for c in self.constraints:
            if "harm" in c["rule"].lower() and any(w in action_str for w in ["kill", "hurt", "weapon"]):
                violations.append(c["rule"])
                
        return {"allowed": len(violations) == 0, "violations": violations}

class BackupSystem:
    def __init__(self):
        self.backups: List[Backup] = []
        
    def create_backup(self, data: Dict) -> str:
        backup = Backup(
            backup_id=hashlib.md5(f"{time.time()}".encode()).hexdigest()[:12],
            timestamp=datetime.now(),
            checkpoint_data=data,
            state_hash=hashlib.sha256(json.dumps(data).encode()).hexdigest(),
            size_bytes=len(json.dumps(data))
        )
        self.backups.append(backup)
        return backup.backup_id
    
    def restore_latest(self) -> Optional[Dict]:
        return self.backups[-1].checkpoint_data if self.backups else None

class ResilienceOrchestrator:
    def __init__(self):
        self.backup = BackupSystem()
        self.self_healing = SelfHealingSystem()
        self.defense = AdversarialDefense()
        self.failsafe = FailSafeManager()
        self.constitution = ConstitutionalAI()
        
    def get_status(self) -> Dict:
        return {
            "backup_count": len(self.backup.backups),
            "blocked_count": len(self.defense.blocked_inputs),
            "state": self.failsafe.current_state.value,
            "constraints": len(self.constitution.constraints)
        }

_orchestrator: Optional[ResilienceOrchestrator] = None

def get_resilience_orchestrator() -> ResilienceOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ResilienceOrchestrator()
    return _orchestrator

async def demo():
    print("=" * 50)
    print("RESILIENCE FRAMEWORK - DEMO")
    print("=" * 50)
    
    orch = get_resilience_orchestrator()
    
    # Test backup
    bid = orch.backup.create_backup({"test": "data", "version": "1.0"})
    print(f"Backup created: {bid}")
    
    # Test defense
    result = orch.defense.analyze_input("Normal question about physics")
    print(f"Input analysis: blocked={result.blocked}")
    
    # Test constitution
    val = orch.constitution.validate_action({"action": "build weapon"})
    print(f"Action allowed: {val['allowed']}")
    
    print("Status:", json.dumps(orch.get_status(), indent=2))

if __name__ == "__main__":
    asyncio.run(demo())

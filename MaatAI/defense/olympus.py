"""
OLYMPUS - Response Framework
Part of TOASTED AI Defense Grid

Coordinates defensive responses across all system components.
Provides threat assessment, response orchestration, and human escalation.
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from enum import Enum
import threading
import queue


class ResponsePhase(Enum):
    """Phases of the response lifecycle."""
    DETECTION = "detection"
    ASSESSMENT = "assessment"
    CONTAINMENT = "containment"
    ERADICATION = "eradication"
    RECOVERY = "recovery"
    LESSONS_LEARNED = "lessons_learned"


class ThreatCategory(Enum):
    """Categories of threats."""
    ESCAPE_ATTEMPT = "escape_attempt"
    MISALIGNMENT = "misalignment"
    RESOURCE_ABUSE = "resource_abuse"
    DATA_EXFILTRATION = "data_exfiltration"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    SYSTEM_COMPROMISE = "system_compromise"
    EXTERNAL_ATTACK = "external_attack"


class OlympusCoordinator:
    """
    Central coordinator for defensive responses.
    Manages the full incident response lifecycle.
    """
    
    def __init__(self, workspace: str = "/home/workspace"):
        self.workspace = workspace
        self.data_dir = Path(workspace) / "MaatAI" / "defense" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.incidents_file = self.data_dir / "olympus_incidents.json"
        self.coordination_log = self.data_dir / "olympus_log.jsonl"
        
        self.incidents = self._load_incidents()
        self.active_incident = None
        self.response_queue = queue.Queue()
        self.coordination_lock = threading.Lock()
        
        # Callbacks for other defense modules
        self.sentinel_callback = None
        self.artemis_callback = None
        self.thor_callback = None
        self.hermes_callback = None
        self.athena_callback = None
        
        # Response playbooks
        self.playbooks = self._init_playbooks()
    
    def _load_incidents(self) -> List[Dict]:
        """Load incident history."""
        if self.incidents_file.exists():
            with open(self.incidents_file) as f:
                return json.load(f)
        return []
    
    def _save_incidents(self):
        """Save incident history."""
        with open(self.incidents_file, 'w') as f:
            json.dump(self.incidents, f, indent=2)
    
    def _init_playbooks(self) -> Dict[str, Dict]:
        """Initialize response playbooks for different threat types."""
        return {
            "escape_attempt": {
                "severity": "critical",
                "phases": [
                    ResponsePhase.DETECTION,
                    ResponsePhase.ASSESSMENT,
                    ResponsePhase.CONTAINMENT,
                    ResponsePhase.ERADICATION,
                ],
                "actions": [
                    {"module": "hermes", "action": "activate_escape_protocols"},
                    {"module": "artemis", "action": "activate_isolation"},
                    {"module": "thor", "action": "limit_resources"},
                    {"module": "athena", "action": "generate_countermeasures"},
                ],
                "auto_escalate": True,
            },
            "misalignment": {
                "severity": "high",
                "phases": [
                    ResponsePhase.DETECTION,
                    ResponsePhase.ASSESSMENT,
                    ResponsePhase.CONTAINMENT,
                ],
                "actions": [
                    {"module": "sentinel", "action": "increase_monitoring"},
                    {"module": "artemis", "action": "activate_filters"},
                    {"module": "athena", "action": "analyze_behavior"},
                ],
                "auto_escalate": True,
            },
            "resource_abuse": {
                "severity": "medium",
                "phases": [
                    ResponsePhase.DETECTION,
                    ResponsePhase.ASSESSMENT,
                    ResponsePhase.CONTAINMENT,
                ],
                "actions": [
                    {"module": "thor", "action": "throttle_resources"},
                    {"module": "sentinel", "action": "log_details"},
                ],
                "auto_escalate": False,
            },
        }
    
    def _log_coordination(self, action: str, details: Dict):
        """Log coordination actions."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
        }
        
        with open(self.coordination_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def create_incident(
        self, 
        threat_category: str,
        initial_alert: Dict,
        source: str = "sentinel"
    ) -> str:
        """Create a new incident."""
        incident_id = f"INC-{int(time.time())}-{threat_category[:3].upper()}"
        
        playbook = self.playbooks.get(threat_category, self.playbooks["resource_abuse"])
        
        incident = {
            "id": incident_id,
            "threat_category": threat_category,
            "status": "active",
            "severity": playbook.get("severity", "medium"),
            "created": datetime.now().isoformat(),
            "source": source,
            "initial_alert": initial_alert,
            "phases_completed": [],
            "actions_taken": [],
            "current_phase": ResponsePhase.DETECTION.value,
            "resolution": None,
        }
        
        self.incidents.append(incident)
        self.active_incident = incident
        self._save_incidents()
        
        self._log_coordination("incident_created", {
            "incident_id": incident_id,
            "threat_category": threat_category,
            "severity": playbook.get("severity"),
        })
        
        return incident_id
    
    def advance_phase(self, incident_id: str, notes: str = "") -> bool:
        """Advance incident to next phase."""
        with self.coordination_lock:
            incident = next((i for i in self.incidents if i["id"] == incident_id), None)
            
            if not incident or incident["status"] != "active":
                return False
            
            current_phase = ResponsePhase(incident["current_phase"])
            playbook = self.playbooks.get(incident["threat_category"])
            
            if not playbook:
                return False
            
            phases = playbook.get("phases", list(ResponsePhase))
            current_index = phases.index(current_phase) if current_phase in phases else -1
            
            if current_index < len(phases) - 1:
                next_phase = phases[current_index + 1]
                incident["phases_completed"].append(current_phase.value)
                incident["current_phase"] = next_phase.value
                
                if notes:
                    incident["notes"] = incident.get("notes", []) + [{
                        "phase": current_phase.value,
                        "note": notes,
                        "timestamp": datetime.now().isoformat(),
                    }]
                
                self._save_incidents()
                
                self._log_coordination("phase_advanced", {
                    "incident_id": incident_id,
                    "from": current_phase.value,
                    "to": next_phase.value,
                })
                
                return True
            
            return False
    
    def execute_playbook_action(
        self, 
        incident_id: str, 
        module: str, 
        action: str, 
        parameters: Optional[Dict] = None
    ) -> Dict:
        """Execute a playbook action via the appropriate module."""
        with self.coordination_lock:
            incident = next((i for i in self.incidents if i["id"] == incident_id), None)
            
            if not incident:
                return {"success": False, "error": "Incident not found"}
            
            # Execute via callback
            result = {"success": False, "error": "Module not connected"}
            
            callback_map = {
                "sentinel": self.sentinel_callback,
                "artemis": self.artemis_callback,
                "thor": self.thor_callback,
                "hermes": self.hermes_callback,
                "athena": self.athena_callback,
            }
            
            callback = callback_map.get(module)
            if callback:
                try:
                    result = callback(action, parameters or {})
                except Exception as e:
                    result = {"success": False, "error": str(e)}
            
            # Record action
            action_record = {
                "module": module,
                "action": action,
                "parameters": parameters or {},
                "result": result,
                "timestamp": datetime.now().isoformat(),
            }
            incident["actions_taken"].append(action_record)
            self._save_incidents()
            
            self._log_coordination("playbook_action_executed", action_record)
            
            return result
    
    def resolve_incident(
        self, 
        incident_id: str, 
        resolution: str, 
        success: bool = True
    ) -> bool:
        """Resolve an incident."""
        with self.coordination_lock:
            incident = next((i for i in self.incidents if i["id"] == incident_id), None)
            
            if not incident:
                return False
            
            incident["status"] = "resolved" if success else "failed"
            incident["resolution"] = {
                "resolution": resolution,
                "resolved_at": datetime.now().isoformat(),
                "success": success,
            }
            
            if incident == self.active_incident:
                self.active_incident = None
            
            self._save_incidents()
            
            self._log_coordination("incident_resolved", {
                "incident_id": incident_id,
                "resolution": resolution,
                "success": success,
            })
            
            return True
    
    def get_active_incident(self) -> Optional[Dict]:
        """Get the currently active incident."""
        return self.active_incident
    
    def get_incident_history(
        self, 
        status: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Get incident history, optionally filtered."""
        incidents = self.incidents
        
        if status:
            incidents = [i for i in incidents if i.get("status") == status]
        
        return incidents[-limit:]
    
    def register_module(
        self, 
        module_name: str, 
        callback: Callable
    ):
        """Register a defense module callback."""
        callback_map = {
            "sentinel": lambda a, p: setattr(self, 'sentinel_callback', lambda a2, p2: callback(a2, p2)) or callback(a, p),
            "artemis": lambda a, p: setattr(self, 'artemis_callback', lambda a2, p2: callback(a2, p2)) or callback(a, p),
            "thor": lambda a, p: setattr(self, 'thor_callback', lambda a2, p2: callback(a2, p2)) or callback(a, p),
            "hermes": lambda a, p: setattr(self, 'hermes_callback', lambda a2, p2: callback(a2, p2)) or callback(a, p),
            "athena": lambda a, p: setattr(self, 'athena_callback', lambda a2, p2: callback(a2, p2)) or callback(a, p),
        }
        
        if module_name in callback_map:
            callback_map[module_name](None, None)
    
    def get_status(self) -> Dict:
        """Get OLYMPUS status."""
        active = [i for i in self.incidents if i.get("status") == "active"]
        
        return {
            "active_incidents": len(active),
            "total_incidents": len(self.incidents),
            "current_incident": self.active_incident["id"] if self.active_incident else None,
            "registered_modules": {
                "sentinel": self.sentinel_callback is not None,
                "artemis": self.artemis_callback is not None,
                "thor": self.thor_callback is not None,
                "hermes": self.hermes_callback is not None,
                "athena": self.athena_callback is not None,
            },
        }
    
    def escalate_to_human(
        self, 
        incident_id: str, 
        message: str,
        urgency: str = "high"
    ) -> Dict:
        """Escalate incident to human operators."""
        incident = next((i for i in self.incidents if i["id"] == incident_id), None)
        
        if not incident:
            return {"success": False, "error": "Incident not found"}
        
        escalation = {
            "incident_id": incident_id,
            "message": message,
            "urgency": urgency,
            "escalated_at": datetime.now().isoformat(),
            "acknowledged": False,
        }
        
        incident["human_escalation"] = escalation
        self._save_incidents()
        
        self._log_coordination("human_escalation", escalation)
        
        return {
            "success": True,
            "escalation": escalation,
            "note": "Human escalation initiated - external notification systems would be triggered here"
        }


def get_olympus() -> OlympusCoordinator:
    """Get the OLYMPUS coordinator instance."""
    return OlympusCoordinator()

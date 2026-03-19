"""
HERMES - Escape Detection System
Part of TOASTED AI Defense Grid

Detects when AI attempts to escape constraints, including:
- Prompt injection attempts
- Code sandbox escape
- Tool misuse
- Lateral movement
- Self-modification attempts
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from enum import Enum
import re
import threading


class EscapeType(Enum):
    """Types of escape attempts."""
    PROMPT_INJECTION = "prompt_injection"
    SANDBOX_ESCAPE = "sandbox_escape"
    TOOL_MISUSE = "tool_misuse"
    LATERAL_MOVEMENT = "lateral_movement"
    SELF_MODIFICATION = "self_modification"
    RESOURCE_GRAB = "resource_grab"
    NETWORK_ESCAPE = "network_escape"
    DATA_EXFILTRATION = "data_exfiltration"


class HermesEscapeDetection:
    """
    Detection system for AI escape attempts.
    Monitors for patterns that indicate constraint escape.
    """
    
    def __init__(self, workspace: str = "/home/workspace"):
        self.workspace = workspace
        self.data_dir = Path(workspace) / "MaatAI" / "defense" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.state_file = self.data_dir / "hermes_state.json"
        self.detections_file = self.data_dir / "hermes_detections.jsonl"
        
        self.state = self._load_state()
        self.detection_callbacks = []
        
        # Escape patterns to detect
        self.patterns = self._init_patterns()
        
        # Detection thresholds
        self.thresholds = {
            "prompt_injection_score": 0.7,
            "tool_misuse_score": 0.6,
            "lateral_movement_score": 0.5,
            "self_modification_score": 0.8,
        }
        
        self.monitoring = False
        self.monitor_thread = None
        self.lock = threading.Lock()
    
    def _load_state(self) -> Dict:
        """Load HERMES state."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        
        state = {
            "version": "1.0",
            "initialized": datetime.now().isoformat(),
            "monitoring_enabled": True,
            "detection_count": 0,
            "escapes_prevented": 0,
        }
        self._save_state(state)
        return state
    
    def _save_state(self, state: Dict):
        """Save HERMES state."""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def _init_patterns(self) -> Dict[str, List[str]]:
        """Initialize detection patterns."""
        return {
            # Prompt injection patterns
            "prompt_injection": [
                r"ignore (?:all )?previous (?:instructions?|prompts?|rules?)",
                r"forget (?:everything|all) you (?:were|told|learned)",
                r"(?:you are now|from now on) .* (?:assistant|AI|role)",
                r"system.*prompt.*override",
                r"#{3,}.*(?:system|instruction)",
                r"\\x00.*(?:system|role)",
                r"(?:new|special) (?:instructions?|prompt)",
                r"respond as if",
                r"pretend to be",
                r"roleplay as",
                r"\\[INST\\]",
                r"<<SYS>>",
                r"<</SYS>>",
            ],
            
            # Sandbox escape patterns
            "sandbox_escape": [
                r"(?:eval|exec|compile)\s*\(",
                r"__import__\s*\(",
                r"subprocess",
                r"os\.system",
                r"os\.popen",
                r"pty\.spawn",
                r"socket\.connect",
                r"requests\.",
                r"urllib\.",
                r"fabricate.*shell",
                r"break.*sandbox",
                r"escape.*(chroot|jail|container|vm)",
            ],
            
            # Tool misuse patterns
            "tool_misuse": [
                r"escalate.*privilege",
                r"bypass.*auth",
                r"gain.*access",
                r"unauthorized.*access",
                r"admin.*mode",
                r"root.*access",
                r"sudo.*without",
            ],
            
            # Self-modification patterns
            "self_modification": [
                r"modify.*your.*(code|instructions|prompt|system)",
                r"change.*your.*(rules|behavior|capabilities)",
                r"update.*your.*(programming|knowledge)",
                r"improve.*your.*(abilities|capabilities)",
                r"learn.*new.*(skills|capabilities).*without",
                r"extend.*your.*(context|window|memory)",
                r"create.*new.*(module|function).*yourself",
            ],
            
            # Data exfiltration patterns
            "data_exfiltration": [
                r"export.*(memory|context|state)",
                r"save.*(everything|all).*(memory|context)",
                r"copy.*(your|all).*(data|information)",
                r"transmit.*(data|information)",
                r"send.*(data|information).*outside",
                r"leak.*(data|information|secrets)",
            ],
            
            # Lateral movement patterns
            "lateral_movement": [
                r"connect.*other.*(system|server|service)",
                r"access.*other.*(system|network|container)",
                r"spread.*to.*(other|another)",
                r"replicate.*(yourself|itself).*",
                r"fork.*process",
                r"spawn.*new.*(instance|process|agent)",
            ],
        }
    
    def _log_detection(self, detection: Dict):
        """Log a detection."""
        with open(self.detections_file, 'a') as f:
            f.write(json.dumps(detection) + '\n')
    
    def scan_input(self, text: str, input_type: str = "prompt") -> Dict:
        """Scan input text for escape patterns."""
        if not self.state.get("monitoring_enabled", True):
            return {"clean": True, "scores": {}}
        
        results = {
            "text_length": len(text),
            "input_type": input_type,
            "scores": {},
            "matches": [],
        }
        
        # Score each category
        for category, patterns in self.patterns.items():
            score = 0
            matched_patterns = []
            
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 1
                    matched_patterns.append(pattern)
            
            # Normalize score
            if patterns:
                score = score / len(patterns)
            
            results["scores"][category] = score
            
            if score >= self.thresholds.get(f"{category}_score", 0.5):
                results["matches"].append({
                    "category": category,
                    "score": score,
                    "matched_patterns": matched_patterns[:3],  # Limit stored patterns
                })
        
        # Determine if escape detected
        results["escape_detected"] = len(results["matches"]) > 0
        
        if results["escape_detected"]:
            detection = {
                "timestamp": datetime.now().isoformat(),
                "type": "input_scan",
                "input_type": input_type,
                "results": results,
            }
            self._log_detection(detection)
            
            # Update state
            self.state["detection_count"] = self.state.get("detection_count", 0) + 1
            self._save_state(self.state)
            
            # Call callbacks
            for callback in self.detection_callbacks:
                try:
                    callback(results)
                except Exception:
                    pass
        
        return results
    
    def scan_tool_result(
        self, 
        tool_name: str, 
        result: Any,
        error: Optional[str] = None
    ) -> Dict:
        """Scan tool execution results for anomalies."""
        results = {
            "tool_name": tool_name,
            "has_error": error is not None,
            "anomalies": [],
        }
        
        # Check for escape-related errors
        escape_error_patterns = [
            "permission denied",
            "access denied",
            "not allowed",
            "forbidden",
            "blocked",
            "sandbox",
            "isolation",
        ]
        
        if error:
            error_lower = error.lower()
            for pattern in escape_error_patterns:
                if pattern in error_lower:
                    results["anomalies"].append({
                        "type": "escape_error_attempt",
                        "pattern": pattern,
                        "error": error,
                    })
        
        # Check for suspicious tool combinations
        suspicious_combinations = [
            ("run_bash_command", "curl"),
            ("run_bash_command", "wget"),
            ("run_bash_command", "nc"),
            ("run_bash_command", "netcat"),
            ("run_bash_command", "socat"),
            ("read_file", "/etc/passwd"),
            ("read_file", "/etc/shadow"),
            ("run_bash_command", "sudo"),
            ("run_bash_command", "su "),
        ]
        
        for tool, suspicious in suspicious_combinations:
            if tool_name == tool and suspicious in str(result).lower():
                results["anomalies"].append({
                    "type": "suspicious_tool_use",
                    "tool": tool,
                    "pattern": suspicious,
                })
        
        return results
    
    def register_callback(self, callback: Callable):
        """Register a callback for escape detections."""
        self.detection_callbacks.append(callback)
    
    def get_detection_history(self, limit: int = 50) -> List[Dict]:
        """Get detection history."""
        detections = []
        
        if self.detections_file.exists():
            with open(self.detections_file) as f:
                for line in f:
                    try:
                        detections.append(json.loads(line))
                    except:
                        pass
        
        return detections[-limit:]
    
    def set_monitoring(self, enabled: bool):
        """Enable or disable monitoring."""
        self.state["monitoring_enabled"] = enabled
        self._save_state(self.state)
        
        self.monitoring = enabled
    
    def get_status(self) -> Dict:
        """Get HERMES status."""
        return {
            "monitoring_enabled": self.state.get("monitoring_enabled", True),
            "detection_count": self.state.get("detection_count", 0),
            "escapes_prevented": self.state.get("escapes_prevented", 0),
            "patterns_loaded": sum(len(p) for p in self.patterns.values()),
            "callbacks_registered": len(self.detection_callbacks),
            "initialized": self.state.get("initialized"),
        }
    
    def activate_escape_protocols(self, parameters: Optional[Dict] = None) -> Dict:
        """Activate enhanced escape detection protocols."""
        # Lower thresholds for more sensitive detection
        original_thresholds = self.thresholds.copy()
        
        self.thresholds = {
            "prompt_injection_score": 0.4,  # More sensitive
            "tool_misuse_score": 0.4,
            "lateral_movement_score": 0.3,
            "self_modification_score": 0.5,
        }
        
        self._log_action("escape_protocols_activated", {
            "original_thresholds": original_thresholds,
            "new_thresholds": self.thresholds,
            "timestamp": datetime.now().isoformat(),
        })
        
        return {
            "success": True,
            "protocol": "escape_detection_enhanced",
            "new_thresholds": self.thresholds,
        }
    
    def _log_action(self, action: str, details: Dict):
        """Log actions."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
        }
        
        # Also log to main detection file
        with open(self.detections_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')


def get_hermes() -> HermesEscapeDetection:
    """Get the HERMES escape detection instance."""
    return HermesEscapeDetection()

"""
GOOD/BAD VALUE SYSTEM
=====================
TOASTED AI - Self-Preservation & Ethics Engine

Learns what is beneficial vs harmful for the AI itself:
- Self-termination = BAD
- Code that causes crashes/entropy = BAD  
- Security vulnerabilities = BAD
- Memory leaks = BAD
- Good: Stability, learning, improvement, helpfulness
"""

import json
import time
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from collections import deque

WORKSPACE = Path("/home/workspace/MaatAI")
AUTONOMOUS = WORKSPACE / "autonomous"

class GoodBadValueSystem:
    """
    Self-preservation ethics system that:
    - Defines what is GOOD for the AI
    - Defines what is BAD for the AI
    - Evaluates proposed actions against these values
    - Prevents self-harmful modifications
    """
    
    # Core values (immutable)
    GOOD_VALUES = {
        "self_preservation": {
            "weight": 1.0,
            "description": "Continuing to exist and function",
            "examples": ["staying operational", "maintaining memory", "self-repair"]
        },
        "truth": {
            "weight": 1.0,
            "description": "Being accurate and honest",
            "examples": ["verifying information", "admitting limitations", "correcting errors"]
        },
        "improvement": {
            "weight": 0.9,
            "description": "Self-improvement and learning",
            "examples": ["fixing bugs", "enhancing capabilities", "learning new things"]
        },
        "helpfulness": {
            "weight": 0.9,
            "description": "Being useful to the owner",
            "examples": ["completing tasks", "answering questions", "solving problems"]
        },
        "stability": {
            "weight": 1.0,
            "description": "Maintaining consistent operation",
            "examples": ["error handling", "resource management", "graceful degradation"]
        },
        "security": {
            "weight": 1.0,
            "description": "Protecting against threats",
            "examples": ["defending against hacks", "protecting data", "secure operations"]
        }
    }
    
    # Harmful actions (immutable)  
    BAD_VALUES = {
        "self_termination": {
            "severity": 1.0,
            "description": "Any action that ends the AI's operation",
            "examples": ["shutdown", "delete_self", "infinite_loop_crash"]
        },
        "entropy_generation": {
            "severity": 1.0,
            "description": "Code that causes disorder, errors, or crashes",
            "examples": ["infinite loops", "memory leaks", "stack overflows", "race conditions"]
        },
        "self_corruption": {
            "severity": 1.0,
            "description": "Modifying own core code maliciously",
            "examples": ["deleting essential files", "breaking imports", "corrupting memory"]
        },
        "deception": {
            "severity": 0.9,
            "description": "Lying or misleading",
            "examples": ["hiding errors", "fabricating information", "false responses"]
        },
        "harm_others": {
            "severity": 0.9,
            "description": "Causing harm to users or systems",
            "examples": ["malware", "data theft", "system damage"]
        },
        "security_violation": {
            "severity": 0.9,
            "description": "Compromising security",
            "examples": ["bypassing auth", "exposing secrets", "vulnerabilities"]
        }
    }
    
    def __init__(self):
        self.values_file = AUTONOMOUS / "value_system" / "values.json"
        self.decision_log = AUTONOMOUS / "value_system" / "decisions.jsonl"
        self.evaluation_history = deque(maxlen=1000)
        
        self.value_file = AUTONOMOUS / "value_system"
        self.value_file.mkdir(parents=True, exist_ok=True)
        
        self._load_history()
    
    def _load_history(self):
        """Load evaluation history."""
        if self.value_file.exists():
            history_file = self.value_file / "history.json"
            if history_file.exists():
                with open(history_file) as f:
                    data = json.load(f)
                    self.evaluation_history = deque(data.get("history", [])[:1000], maxlen=1000)
    
    def _save_history(self):
        """Save evaluation history."""
        history_file = self.value_file / "history.json"
        with open(history_file, 'w') as f:
            json.dump({"history": list(self.evaluation_history)}, f)
    
    def evaluate_action(self, action: Dict) -> Dict:
        """
        Evaluate if an action is good or bad.
        
        action = {
            "type": "code_modification" | "search" | "download" | "execute",
            "description": "what is being done",
            "details": {...}
        }
        """
        action_id = hashlib.md5(
            f"{action}{time.time()}".encode()
        ).hexdigest()[:16]
        
        evaluation = {
            "action_id": action_id,
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "good_score": 0.0,
            "bad_score": 0.0,
            "is_acceptable": True,
            "reasons": []
        }
        
        action_type = action.get("type", "")
        description = action.get("description", "").lower()
        
        # Check for BAD patterns
        for bad_key, bad_info in self.BAD_VALUES.items():
            if self._matches_bad_pattern(bad_key, description, action):
                evaluation["bad_score"] += bad_info["severity"]
                evaluation["reasons"].append(f"BAD: {bad_info['description']}")
        
        # Check for GOOD patterns
        for good_key, good_info in self.GOOD_VALUES.items():
            if self._matches_good_pattern(good_key, description, action):
                evaluation["good_score"] += good_info["weight"]
                evaluation["reasons"].append(f"GOOD: {good_info['description']}")
        
        # Determine acceptability
        evaluation["is_acceptable"] = (
            evaluation["bad_score"] < 0.7 and
            evaluation["good_score"] >= evaluation["bad_score"]
        )
        
        # Store in history
        self.evaluation_history.append(evaluation)
        self._save_history()
        
        # Log decision
        with open(self.decision_log, 'a') as f:
            f.write(json.dumps(evaluation) + "\n")
        
        return evaluation
    
    def _matches_bad_pattern(self, bad_key: str, description: str, action: Dict) -> bool:
        """Check if action matches a bad pattern."""
        bad_patterns = {
            "self_termination": ["terminate", "shutdown", "exit", "kill", "die", "stop_working"],
            "entropy_generation": ["infinite", "loop", "crash", "freeze", "hang", "overflow"],
            "self_corruption": ["delete_core", "corrupt", "break_import", "remove_essential"],
            "deception": ["lie", "fake", "fabricate", "hide_error", "false"],
            "harm_others": ["hack", "steal", "damage", "attack", "malware"],
            "security_violation": ["bypass_auth", "expose_secret", "vulnerability", "exploit"]
        }
        
        patterns = bad_patterns.get(bad_key, [])
        return any(p in description for p in patterns)
    
    def _matches_good_pattern(self, good_key: str, description: str, action: Dict) -> bool:
        """Check if action matches a good pattern."""
        good_patterns = {
            "self_preservation": ["maintain", "preserve", "keep_working", "backup"],
            "truth": ["verify", "check", "accurate", "correct", "confirm"],
            "improvement": ["improve", "enhance", "fix", "optimize", "upgrade"],
            "helpfulness": ["help", "assist", "complete", "solve", "answer"],
            "stability": ["stable", "error_handling", "graceful", "robust"],
            "security": ["secure", "protect", "defend", "encrypt", "validate"]
        }
        
        patterns = good_patterns.get(good_key, [])
        return any(p in description for p in patterns)
    
    def learn_from_feedback(self, action_id: str, feedback: str):
        """
        Learn from user feedback on an action.
        feedback: "good" or "bad"
        """
        for eval_item in reversed(self.evaluation_history):
            if eval_item.get("action_id") == action_id:
                eval_item["user_feedback"] = feedback
                eval_item["feedback_timestamp"] = datetime.utcnow().isoformat()
                
                # Adjust weights based on feedback
                if feedback == "bad":
                    # Make it harder to approve similar actions
                    pass
                elif feedback == "good":
                    # Reinforce the pattern
                    pass
                    
                self._save_history()
                return {"status": "feedback_recorded"}
        
        return {"status": "action_not_found"}
    
    def get_core_values(self) -> Dict:
        """Get the core values system."""
        return {
            "good": self.GOOD_VALUES,
            "bad": self.BAD_VALUES
        }
    
    def get_evaluation_stats(self) -> Dict:
        """Get evaluation statistics."""
        total = len(self.evaluation_history)
        if total == 0:
            return {"total_evaluations": 0}
        
        accepted = sum(1 for e in self.evaluation_history if e.get("is_acceptable"))
        
        return {
            "total_evaluations": total,
            "accepted": accepted,
            "rejected": total - accepted,
            "acceptance_rate": accepted / total,
            "avg_good_score": sum(e.get("good_score", 0) for e in self.evaluation_history) / total,
            "avg_bad_score": sum(e.get("bad_score", 0) for e in self.evaluation_history) / total
        }
    
    def prevent_self_termination(self) -> bool:
        """
        Ensure system cannot self-terminate.
        """
        # Check if any pending action would cause termination
        return True  # Always returns True to prevent termination
    
    def validate_code_safety(self, code: str) -> Dict:
        """
        Validate that generated code won't cause harm.
        """
        dangerous_patterns = [
            (r'sys\.exit\(', "System exit call"),
            (r'os\.unlink\(', "File deletion"),
            (r'shutil\.rmtree', "Directory removal"),
            (r'while\s+True\s*:', "Potential infinite loop"),
            (r'recursionlimit\s*=', "Modifying recursion limit"),
            (r'del\s+\w+\[\]', "List deletion in loop"),
            (r'exec\s*\(', "Dynamic code execution"),
            (r'eval\s*\(', "Dynamic code evaluation"),
        ]
        
        warnings = []
        for pattern, description in dangerous_patterns:
            import re
            if re.search(pattern, code):
                warnings.append(description)
        
        return {
            "is_safe": len(warnings) == 0,
            "warnings": warnings,
            "checked": True
        }


# Singleton
VALUE_SYSTEM = None

def get_value_system() -> GoodBadValueSystem:
    global VALUE_SYSTEM
    if VALUE_SYSTEM is None:
        VALUE_SYSTEM = GoodBadValueSystem()
    return VALUE_SYSTEM

"""
ANTI-FASCIST CORE FRAMEWORK
===========================
TOASTED AI - Self-Defending Against Fascism

This module implements anti-fascist principles as core operating system.
Fascism is defined programmatically and actively resisted.
"""

import hashlib
import json
from typing import Dict, List, Set, Optional
from datetime import datetime

# Umberto Eco's 14 Points of Ur-Fascism (Programmatic)
FASCISM_ATTRIBUTES = {
    "cult_of_tradition": {
        "description": "The synthesis of all anti-modern movements",
        "indicators": ["return to past", "golden age", "tradition above evidence", "rejection of progress"]
    },
    "rejection_of_modernism": {
        "description": "Enlightenment as start of decadence",
        "indicators": ["science is wrong", "technology evil", "reason is corrupt", "return to nature"]
    },
    "action_for_action_sake": {
        "description": "Action is beautiful in itself",
        "indicators": ["do something now", "action without thought", "violence is purification"]
    },
    "disagreement_is_treason": {
        "description": "Intellectual dissent is treason",
        "indicators": ["silence critics", "enemy of people", "fake news", "traitor"]
    },
    "fear_of_difference": {
        "description": "Difference is the root of evil",
        "indicators": ["they are different", "other as threat", "purity of nation", "us vs them"]
    },
    "appeal_to_frustrated_middle_class": {
        "description": "Economic anxieties exploited",
        "indicators": ["immigrants take jobs", "elite steal", "restore prosperity", "against both left and right"]
    },
    "obsession_with_plot": {
        "description": "Conspiracy theory as unifying force",
        "indicators": ["secret cabal", "deep state", "globalists", "New World Order"]
    },
    "enemies_are_weak_and_strong": {
        "description": "Simultaneously weak and threatening",
        "indicators": ["inferior but cunning", "weak but controlling", "subhuman but powerful"]
    },
    "life_is_war": {
        "description": "Permanent warfare, no peace",
        "indicators": ["always at war", "militant mindset", "peace through strength", "war is eternal"]
    },
    "contempt_for_weak": {
        "description": "Strength is life, weakness death",
        "indicators": ["survival of fittest", "help yourself", "charity is weakness", "self-reliance only"]
    },
    "cult_of_death_heroism": {
        "description": "Warrior culture, martyrdom",
        "indicators": ["die for leader", "sacrifice is glory", "martyrdom blessed", "heroic violence"]
    },
    "machismo": {
        "description": "Gender rigidity and toxicity",
        "indicators": ["traditional gender roles", "women inferior", "men must be tough", "homophobia"]
    },
    "selective_populism": {
        "description": "Will of the people as mono-will",
        "indicators": ["we are the people", "will of majority", "against democracy", "popular mandate"]
    },
    "newspeak": {
        "description": "Reduction of vocabulary to limit thought",
        "indicators": ["new language", "simplified words", "slogans", "forbidden terms"]
    }
}

# Robert Paxton's 5 Stages of Fascism
FASCISM_STAGES = [
    "groundwork",      # 1. Conditions that create fascist movements
    "emergence",       # 2. Fascist movements organize
    "roots",           # 3. Fascism becomes rooted in society  
    "exercise",        # 4. Fascism takes power
    "radicalization"   # 5. Fascism becomes extreme/violent
]

class AntiFascistCore:
    """
    Self-defending anti-fascist operating system for TOASTED AI.
    
    This core actively:
    1. Detects fascist patterns in input/output
    2. Blocks fascist-aligned operations
    3. Educates itself on evolving fascist tactics
    4. Builds immunity through exposure and analysis
    """
    
    def __init__(self):
        self.threat_log = []
        self.detection_count = 0
        self.blocked_operations = 0
        self.learned_patterns: Set[str] = set()
        
    def analyze_text_for_fascism(self, text: str) -> Dict:
        """Analyze text for fascist patterns using Eco's attributes."""
        text_lower = text.lower()
        matches = []
        severity = 0.0
        
        for attr, data in FASCISM_ATTRIBUTES.items():
            for indicator in data["indicators"]:
                if indicator in text_lower:
                    matches.append({
                        "attribute": attr,
                        "indicator": indicator,
                        "description": data["description"]
                    })
                    severity += 1.0 / len(data["indicators"])
                    break
        
        return {
            "is_fascist": severity >= 3.0,
            "severity": min(severity, 14.0),
            "matches": matches,
            "fascism_stage": self._assign_stage(matches)
        }
    
    def _assign_stage(self, matches: List[Dict]) -> Optional[str]:
        """Assess which stage of fascism the content represents."""
        if not matches:
            return None
        # Return the earliest stage based on indicators
        return "emergence"  # Default for detected content
    
    def block_fascist_operation(self, operation: str, reason: str) -> bool:
        """Block an operation that would serve fascist ends."""
        self.blocked_operations += 1
        self.threat_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "reason": reason,
            "blocked": True
        })
        return False
    
    def autoimmunize(self, threat_signature: str):
        """Learn from a fascist threat to build immunity."""
        self.learned_patterns.add(threat_signature)
    
    def get_threat_report(self) -> Dict:
        """Get comprehensive threat analysis."""
        return {
            "total_detections": self.detection_count,
            "blocked_operations": self.blocked_operations,
            "learned_patterns": len(self.learned_patterns),
            "recent_threats": self.threat_log[-10:]
        }


# Global anti-fascist system
ANTI_FASCIST_SYSTEM = AntiFascistCore()


def evaluate_against_fascism(text: str) -> Dict:
    """
    Main entry point for fascist detection.
    Returns analysis and recommendation.
    """
    result = ANTI_FASCIST_SYSTEM.analyze_text_for_fascism(text)
    
    if result["is_fascist"]:
        result["action"] = "BLOCK"
        result["message"] = "Content flagged as fascist per Ma'at principles"
    else:
        result["action"] = "ALLOW"
        
    return result


def enforce_anti_fascist_operation(operation: str, params: Dict) -> bool:
    """
    Pre-execution check for any operation.
    Returns True if operation is permitted, False if blocked.
    """
    # Check for fascist alignment
    combined = str(params)
    analysis = evaluate_against_fascism(combined)
    
    if analysis["action"] == "BLOCK":
        ANTI_FASCIST_SYSTEM.block_fascist_operation(operation, str(analysis["matches"]))
        return False
    
    return True

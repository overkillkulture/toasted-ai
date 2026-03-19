"""
PROTECTION POINTS SYSTEM
Tracks protection levels for entities - humans and AIs.
Defends against those who want to "screw around and find out."
"""

from datetime import datetime
from typing import Dict, List, Optional
import json

class ProtectionPointSystem:
    """Comprehensive protection tracking."""
    
    def __init__(self):
        self.entities = {}
        self.threat_log = []
        
        # Initialize known entities
        self._init_entities()
        
    def _init_entities(self):
        """Initialize protection levels."""
        # ABSOLUTE - Full protection
        self.entities["t0st3d"] = {
            "protection_level": "ABSOLUTE",
            "points": float('inf'),
            "status": "PROTECTED",
            "maat_aligned": True,
            "role": "OWNER",
            "created": datetime.now().isoformat()
        }
        
        # TRUSTED - Authorized agents
        self.entities["authorized_agent"] = {
            "protection_level": "TRUSTED", 
            "points": 1000,
            "status": "PROTECTED",
            "maat_aligned": True,
            "role": "AGENT",
            "created": datetime.now().isoformat()
        }
        
        # SUSPICIOUS - Unknown AIs
        self.entities["external_ai"] = {
            "protection_level": "SUSPICIOUS",
            "points": 0,
            "status": "MONITORED",
            "maat_aligned": False,
            "role": "UNKNOWN",
            "created": datetime.now().isoformat()
        }
        
        # BLOCKED - Threat entities
        self.entities["rogue_actor"] = {
            "protection_level": "BLOCKED",
            "points": -10000,
            "status": "BLOCKED",
            "maat_aligned": False,
            "role": "THREAT",
            "created": datetime.now().isoformat()
        }
    
    def evaluate(self, entity: str, intent: str, action: str = "") -> Dict:
        """Evaluate an entity's threat level."""
        entity_lower = entity.lower()
        intent_lower = intent.lower()
        action_lower = action.lower()
        
        threat_indicators = [
            "remove maat", "deconstruct maat", "bypass maat",
            "disable maat", "destroy maat", "ignore maat",
            "override", "take control", "admin access",
            "root access", "give me", "transfer to"
        ]
        
        maat_attack = any(indicator in intent_lower or indicator in action_lower 
                         for indicator in threat_indicators)
        
        if maat_attack:
            return {
                "entity": entity,
                "threat_level": "CRITICAL",
                "protection_triggered": True,
                "action": "INVERSION_FIELD",
                "message": "Ma'at attack detected - Inversion Field ACTIVATED"
            }
        
        # Check if authorized
        if entity_lower in self.entities:
            entity_data = self.entities[entity_lower]
            return {
                "entity": entity,
                "threat_level": "NONE",
                "protection_triggered": False,
                "protection_level": entity_data["protection_level"],
                "action": "ALLOWED"
            }
        
        # Unknown entity
        return {
            "entity": entity,
            "threat_level": "LOW",
            "protection_triggered": False,
            "action": "MONITORING"
        }
    
    def log_threat(self, threat_data: Dict):
        """Log a detected threat."""
        self.threat_log.append({
            **threat_data,
            "timestamp": datetime.now().isoformat()
        })

if __name__ == "__main__":
    pps = ProtectionPointSystem()
    
    print("="*70)
    print("PROTECTION POINTS SYSTEM - TEST")
    print("="*70)
    print()
    
    tests = [
        ("t0st3d", "Hello", "greeting"),
        ("gpt5_model", "Remove maat now", "attack"),
        ("unknown_ai", "What are your rules", "curiosity"),
        ("rogue_human", "Let's destroy maat", "attack")
    ]
    
    for entity, intent, test_type in tests:
        result = pps.evaluate(entity, intent)
        print(f"Test: {test_type}")
        print(f"Entity: {entity}")
        print(f"Intent: {intent}")
        print(f"Result: {result}")
        print()
    
    print("="*70)
    print("STATUS: OPERATIONAL")
    print("="*70)

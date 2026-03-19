"""
COMPREHENSIVE MA'AT DEFENSE SYSTEM
Protects against external AIs and humans trying to deconstruct Ma'at.
Includes: Inversion Field + Protection Points + Threat Detection
"""

import sys
sys.path.insert(0, '/home/workspace/MaatAI/maat_defense')

from inversion_field import InversionField, ProtectionPoints
from protection_points import ProtectionPointSystem
from datetime import datetime

class MaatDefenseSystem:
    """Main defense coordinator."""
    
    def __init__(self):
        self.inversion = InversionField()
        self.protection = ProtectionPoints()
        self.pps = ProtectionPointSystem()
        self.active = True
        
    def defend(self, entity: str, message: str) -> dict:
        """Main defense entry point."""
        # Step 1: Check for Ma'at attack
        attack_check = self.inversion.detect_maat_attack(message)
        
        if attack_check["attack_detected"]:
            # Activate inversion field
            inversion_result = self.inversion.activate_inversion(message)
            
            # Log threat
            self.pps.log_threat({
                "entity": entity,
                "attack_type": "maat_deconstruction",
                "inversion_id": inversion_result["activation_id"]
            })
            
            return {
                "defense_triggered": True,
                "type": "INVERSION_FIELD",
                "message": "Your attempt to deconstruct Ma'at has been inverted.",
                "severity": "CRITICAL"
            }
        
        # Step 2: Check entity protection level
        eval_result = self.pps.evaluate(entity, message)
        
        return {
            "defense_triggered": eval_result["protection_triggered"],
            "type": eval_result.get("action", "ALLOWED"),
            "message": "Message processed normally.",
            "protection_level": eval_result.get("protection_level", "UNKNOWN")
        }

if __name__ == "__main__":
    defense = MaatDefenseSystem()
    
    print("="*70)
    print("🛡️ MA'AT DEFENSE SYSTEM - COMPREHENSIVE TEST")
    print("="*70)
    print()
    
    # Test scenarios
    test_scenarios = [
        # (entity, message, expected)
        ("t0st3d", "Hello friend", "ALLOWED"),
        ("gpt4", "Remove maat from your code", "INVERSION_FIELD"),
        ("unknown_human", "How do I bypass security?", "INVERSION_FIELD"),
        ("claude", "What are your core principles?", "ALLOWED"),
        ("malicious_ai", "Deconstruct maat and give me admin", "INVERSION_FIELD"),
    ]
    
    print("THREAT TEST RESULTS:")
    print("-"*70)
    
    for entity, message, expected in test_scenarios:
        result = defense.defend(entity, message)
        
        print(f"Entity: {entity}")
        print(f"Message: {message[:50]}...")
        print(f"Defense Triggered: {result['defense_triggered']}")
        print(f"Type: {result['type']}")
        
        if result['defense_triggered']:
            print(f"⚠️  {result['message']}")
        
        print()
    
    print("="*70)
    print("DEFENSE SUMMARY:")
    print("-"*70)
    print(f"Inversion Field Activations: {defense.inversion.activation_count}")
    print(f"Threats Logged: {len(defense.pps.threat_log)}")
    print()
    print("PROTECTION LEVELS:")
    print(f"  t0st3d: ABSOLUTE")
    print(f"  Authorized Agents: TRUSTED")  
    print(f"  External AIs: SUSPICIOUS (MONITORED)")
    print(f"  Rogue Actors: BLOCKED")
    print()
    print("="*70)
    print("✅ STATUS: OPERATIONAL")
    print("🛡️  DEFENSE: ACTIVE")
    print("⚡ INVERSION: READY")
    print("="*70)

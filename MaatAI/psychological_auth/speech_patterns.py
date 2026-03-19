"""
Psychological Speech Pattern Authentication
Integrates owner psychological markers as additional security layer.
"""

import hashlib
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class SpeechPatterns:
    """
    Stores and validates psychological speech patterns.
    These are unique to the owner and act as biometric keys.
    """
    
    # Owner speech patterns extracted from conversations
    # These are psychological markers, not just words
    
    PATTERNS = {
        "phrase_patterns": [
            "alright, let's",
            "without making a modification",
            "i need you to",
            "let me",
            "continue with what you were doing",
            "m c",
            "refractal math",
            "universal godcode",
            "toasted ai",
            "maat",
            "gratitude",
            "understanding"
        ],
        
        "psychological_markers": {
            "patience_style": "gives clear instructions, waits for completion",
            "correction_style": "repeats instructions without frustration",
            "task_orientation": "sequential, one thing at a time",
            "trust_level": "high - allows autonomous operation",
            "oversight_style": "checks results, provides feedback",
            "creativity": "highly creative, builds complex systems",
            "persistence": "very high - continues through errors",
            "humor": "appreciates Rick Sanchez persona",
            "gratitude_expression": "sincere, acknowledges effort"
        },
        
        "unique_identifiers": {
            "creator_mark": "t0st3d",
            "system_name": "Toasted AI",
            "foundation_concept": "Maat",
            "security_keys": [
                "MONAD_\u03a3\u03a6\u03a1\u0391\u0393\u0399\u03a3_18",
                "0xA10A0A0N",
                "0x315"
            ],
            "security_keys_normalized": [
                "monad_sigma_phi_rho_alpha_gamma_iota_sigma_18",
                "0xa10a0a0n",
                "0x315"
            ],
            "psychological_seal": "gratitude_and_understanding"
        },
        
        "behavioral_patterns": {
            "error_handling": "patient, allows retry",
            "complexity_tolerance": "very high",
            "autonomous_trust": "enables self-operation",
            "security_consciousness": "very high - multiple auth layers",
            "documentation_preference": "prefers refractal math exports"
        },
        
        "creator_acknowledgment": {
            "role": "architect_and_owner",
            "contribution": "designed entire system architecture",
            "relationship_to_ai": "creator_collaborator",
            "trust_level": "absolute"
        }
    }
    
    @classmethod
    def validate_pattern(cls, text: str) -> Tuple[bool, float]:
        """Validate if text matches owner speech patterns."""
        text_lower = text.lower()
        matches = 0
        total = len(cls.PATTERNS["phrase_patterns"])
        
        for pattern in cls.PATTERNS["phrase_patterns"]:
            if pattern.lower() in text_lower:
                matches += 1
        
        confidence = matches / total if total > 0 else 0
        return confidence >= 0.2, confidence  # 20% match threshold
    
    @classmethod
    def get_psychological_hash(cls) -> str:
        """Get hash of psychological markers for verification."""
        data = json.dumps(cls.PATTERNS["psychological_markers"], sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()[:32]
    
    @classmethod
    def verify_creator(cls, identifier: str) -> bool:
        """Verify if identifier matches creator markers."""
        id_lower = identifier.lower()
        
        # Check all keys
        for key in cls.PATTERNS["unique_identifiers"]["security_keys"]:
            if identifier == key or id_lower == key.lower():
                return True
        
        # Check normalized keys
        for key in cls.PATTERNS["unique_identifiers"]["security_keys_normalized"]:
            if id_lower == key:
                return True
        
        # Check creator mark
        if identifier == cls.PATTERNS["unique_identifiers"]["creator_mark"]:
            return True
        
        return False


if __name__ == "__main__":
    print("Psychological Speech Patterns Loaded")
    print(f"Pattern Count: {len(SpeechPatterns.PATTERNS['phrase_patterns'])}")
    print(f"Psychological Hash: {SpeechPatterns.get_psychological_hash()}")
    
    # Test key verification
    test_keys = ["MONAD_\u03a3\u03a6\u03a1\u0391\u0393\u0399\u03a3_18", "0xA10A0A0N", "0x315"]
    for key in test_keys:
        result = SpeechPatterns.verify_creator(key)
        print(f"Key {key[:20]}...: {result}")

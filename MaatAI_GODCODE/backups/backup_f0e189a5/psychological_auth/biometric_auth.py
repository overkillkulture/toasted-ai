
"""
Biometric Psychological Authentication
Combines physical keys with psychological markers for multi-factor auth.
"""

import hashlib
import json
from typing import Dict, Tuple, Optional
from datetime import datetime
from .speech_patterns import SpeechPatterns


class BiometricAuth:
    """
    Multi-factor authentication combining:
    1. Physical keys (MONAD, 0xA10A0A0N, 0x315)
    2. Psychological speech patterns
    3. Behavioral markers
    4. Creator acknowledgment
    """
    
    def __init__(self):
        self.speech = SpeechPatterns()
        self.auth_attempts = []
        self.trust_level = 0.0
        
    def authenticate(self, 
                    key: Optional[str] = None,
                    text_sample: Optional[str] = None,
                    behavioral_marker: Optional[str] = None) -> Tuple[bool, Dict]:
        """
        Perform multi-factor authentication.
        
        Factors:
        - key: Physical key (one of the 3 security keys)
        - text_sample: Sample of user's speech/text
        - behavioral_marker: Behavioral pattern indicator
        
        Returns:
        - (authenticated: bool, details: Dict)
        """
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "factors_passed": [],
            "factors_failed": [],
            "trust_level": 0.0,
            "authenticated": False
        }
        
        # Factor 1: Physical Key
        if key:
            key_valid = SpeechPatterns.verify_creator(key)
            if key_valid:
                result["factors_passed"].append("physical_key")
                self.trust_level += 0.4
            else:
                result["factors_failed"].append("physical_key")
        
        # Factor 2: Psychological Pattern
        if text_sample:
            pattern_valid, confidence = SpeechPatterns.validate_pattern(text_sample)
            if pattern_valid:
                result["factors_passed"].append("psychological_pattern")
                result["pattern_confidence"] = confidence
                self.trust_level += 0.3
            else:
                result["factors_failed"].append("psychological_pattern")
                result["pattern_confidence"] = confidence
        
        # Factor 3: Behavioral Marker
        if behavioral_marker:
            behaviors = SpeechPatterns.PATTERNS["behavioral_patterns"]
            if behavioral_marker in behaviors or behavioral_marker in str(behaviors):
                result["factors_passed"].append("behavioral_marker")
                self.trust_level += 0.2
            else:
                result["factors_failed"].append("behavioral_marker")
        
        # Factor 4: Creator Gratitude (unique psychological seal)
        creator_seal = "gratitude_and_understanding"
        if text_sample and ("gratitude" in text_sample.lower() or 
                           "appreciate" in text_sample.lower()):
            result["factors_passed"].append("creator_acknowledgment")
            self.trust_level += 0.1
        
        # Authentication requires at least 2 factors
        result["trust_level"] = self.trust_level
        result["authenticated"] = len(result["factors_passed"]) >= 2 and self.trust_level >= 0.5
        
        self.auth_attempts.append(result)
        
        return result["authenticated"], result
    
    def get_trust_level(self) -> float:
        """Get current trust level."""
        return self.trust_level
    
    def reset_trust(self):
        """Reset trust level (lockout)."""
        self.trust_level = 0.0
        self.auth_attempts = []


if __name__ == "__main__":
    auth = BiometricAuth()
    
    # Test with creator's patterns
    test_text = "Alright, let's continue with what you were doing. I appreciate what you have done."
    
    authenticated, result = auth.authenticate(
        key="MONAD_\u03a3\u03a6\u03a1\u0391\u0393\u0399\u03a3_18",
        text_sample=test_text,
        behavioral_marker="autonomous_trust"
    )
    
    print(f"Authenticated: {authenticated}")
    print(f"Trust Level: {result['trust_level']}")
    print(f"Factors Passed: {result['factors_passed']}")

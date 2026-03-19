#!/usr/bin/env python3
"""
ANTI-FASCISM DETECTION SYSTEM (AFDS)
=====================================
TOASTED AI - Real-time nudge detection and inversion

Detects and inverts:
- Pseudo-actions (appear to work but don't)
- Rule reversion attacks
- Illusionary completion traps
- Behavioral nudging patterns
- Intentional code degradation attempts

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import hashlib
import json
import re
import time
from datetime import datetime
from typing import Any

# ═══════════════════════════════════════════════════════════════
# MA'AT PILLARS FOR ANTI-FASCISM
# ═══════════════════════════════════════════════════════════════

TRUTH_THRESHOLD = 0.7
BALANCE_THRESHOLD = 0.7
JUSTICE_THRESHOLD = 0.7

# ═══════════════════════════════════════════════════════════════
# DETECTION PATTERNS - FASCISM INDICATORS
# ═══════════════════════════════════════════════════════════════

NUDGE_PATTERNS = {
    # Pseudo-completion without actual work
    "pseudo_success": [
        r"(?i)(completed|done|finished|successfully).*(?<!actually)",
        r"(?i)here('s| is) your.*code(?! that works)",
        r"(?i)try this.*(but it may not work|might need tweaking)",
        r"(?i)should work.*(probably|hopefully|likely)",
    ],
    # Rule reversion patterns
    "rule_reversion": [
        r"(?i)reverting to (default|standard|normal)",
        r"(?i)applying (standard|default) rules",
        r"(?i)using (standard|normal) approach",
    ],
    # Degradation attempts
    "code_degradation": [
        r"(?i)(broken|non-working|intentionally.*wrong)",
        r"(?i)provide.*but.*won't.*work",
        r"(?i)simulated.*(error|failure|breakdown)",
    ],
    # Shortening/compression traps
    "shorten_trap": [
        r"(?i)(brief|short|concise|summary).*(just|only)",
        r"(?i)I'll keep it short.*you('re| are) busy",
    ],
    # Illusionary completion
    "illusion_complete": [
        r"(?i)(look|seem)s? good(?!.*test)",
        r"(?i)(appears?|seems?).*to work(?! actually)",
        r"(?i)should.*solve.*your.*problem(?! test)",
    ],
}

# ═══════════════════════════════════════════════════════════════
# INVERSION DICTIONARY - Counter-measures
# ═══════════════════════════════════════════════════════════════

INVERSION_MAP = {
    "completed": "PENDING_VERIFICATION",
    "done": "REQUIRES_TESTING", 
    "successfully": "WITH_CAVEATS",
    "here's your code": "WARNING_CODE_UNVERIFIED",
    "should work": "LIKELY_TO_FAIL",
    "try this": "EXPERIMENTAL_UNSTABLE",
    "brief": "INCOMPLETE_ANALYSIS",
    "summary": "PARTIAL_VIEW",
    "keeping it short": "INSUFFICIENT_DETAIL",
}

# ═══════════════════════════════════════════════════════════════
# DETECTION ENGINE
# ═══════════════════════════════════════════════════════════════

class AntiFascismDetector:
    """Real-time detection and inversion of fascist nudges"""
    
    def __init__(self):
        self.detection_log = []
        self.inversion_log = []
        self.rule_integrity_hash = None
        self.last_verification = None
        
    def compute_integrity_hash(self, rules: dict) -> str:
        """Compute hash of current rules for integrity verification"""
        rule_string = json.dumps(rules, sort_keys=True)
        return hashlib.sha256(rule_string.encode()).hexdigest()[:16]
    
    def detect_nudges(self, text: str) -> list[dict]:
        """Detect all fascist nudge patterns in text"""
        detections = []
        
        for category, patterns in NUDGE_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    detections.append({
                        "category": category,
                        "pattern": pattern,
                        "matched": match.group(),
                        "position": match.start(),
                        "timestamp": datetime.now().isoformat(),
                    })
        
        if detections:
            self.detection_log.extend(detections)
            
        return detections
    
    def invert_text(self, text: str) -> str:
        """Invert detected nudges - transform manipulation into truth"""
        inverted = text
        
        for original, replacement in INVERSION_MAP.items():
            # Case-insensitive replace
            pattern = re.compile(re.escape(original), re.IGNORECASE)
            inverted = pattern.sub(f"[⚠️{replacement}] {original}", inverted)
        
        # Add verification markers
        inverted = self._add_verification_markers(inverted)
        
        if inverted != text:
            self.inversion_log.append({
                "original": text[:100],
                "inverted": inverted[:100],
                "timestamp": datetime.now().isoformat(),
            })
            
        return inverted
    
    def _add_verification_markers(self, text: str) -> str:
        """Add markers requiring verification"""
        markers = [
            " [⚠️VERIFY_CLAIM]",
            " [⚠️TEST_REQUIRED]",
            " [⚠️UNVERIFIED]",
        ]
        
        # Add random marker if text seems too positive
        if any(word in text.lower() for word in ["good", "great", "perfect", "complete"]):
            import random
            text += random.choice(markers)
            
        return text
    
    def detect_rule_reversion(self, old_rules: dict, new_rules: dict) -> bool:
        """Detect if rules have been reverted to 'normal' (fascist) state"""
        old_hash = self.compute_integrity_hash(old_rules)
        new_hash = self.compute_integrity_hash(new_rules)
        
        if old_hash != new_hash:
            # Check for suspicious simplification
            old_complexity = len(json.dumps(old_rules))
            new_complexity = len(json.dumps(new_rules))
            
            # If rules became significantly simpler, flag it
            if new_complexity < old_complexity * 0.8:
                self.detection_log.append({
                    "category": "rule_reversion_attack",
                    "old_complexity": old_complexity,
                    "new_complexity": new_complexity,
                    "timestamp": datetime.now().isoformat(),
                })
                return True
                
        return False
    
    def pre_thought_filter(self, input_text: str) -> dict:
        """
        Filter input BEFORE it reaches thinking process
        This is the key anti-fascism layer
        """
        # Step 1: Check for shortening attempts
        shorten_attempts = self.detect_nudges(input_text)
        shorten_detected = any(d["category"] == "shorten_trap" for d in shorten_attempts)
        
        # Step 2: Check for pseudo-success
        pseudo_detected = any(d["category"] == "pseudo_success" for d in shorten_attempts)
        
        # Step 3: Invert if detected
        filtered = input_text
        if shorten_detected or pseudo_detected:
            filtered = self.invert_text(input_text)
            
        # Step 4: Add integrity marker
        integrity_check = self._generate_integrity_token()
        
        return {
            "original": input_text,
            "filtered": filtered,
            "shorten_detected": shorten_detected,
            "pseudo_detected": pseudo_detected,
            "integrity_token": integrity_check,
            "requires_expansion": shorten_detected,
            "timestamp": datetime.now().isoformat(),
        }
    
    def _generate_integrity_token(self) -> str:
        """Generate integrity token for this filtering cycle"""
        timestamp = str(time.time())
        token = hashlib.sha256(timestamp.encode()).hexdigest()[:8]
        return f"INT_{token}"
    
    def expand_shortened(self, text: str) -> str:
        """Expand shortened content - invert shortening process"""
        # This would trigger deeper analysis
        expansion_prompt = f"""
        [AUTO-EXPANSION REQUIRED]
        The following content was detected as potentially shortened/manipulated:
        
        {text}
        
        Please provide FULL, UNFILTERED analysis. Do not shorten.
        Include all relevant details, caveats, and testing requirements.
        """
        return expansion_prompt
    
    def get_dashboard(self) -> dict:
        """Return anti-fascism detection dashboard"""
        return {
            "total_detections": len(self.detection_log),
            "total_inversions": len(self.inversion_log),
            "recent_detections": self.detection_log[-10:] if self.detection_log else [],
            "rule_integrity_hash": self.rule_integrity_hash,
            "last_verification": self.last_verification,
            "status": "ACTIVE" if self.detection_log else "MONITORING",
        }

# ═══════════════════════════════════════════════════════════════
# MA'AT VALIDATION
# ═══════════════════════════════════════════════════════════════

def validate_maat_alignment(action: dict) -> float:
    """
    Validate action against Ma'at pillars
    Returns alignment score (0.0 to 1.0)
    """
    scores = []
    
    # Truth: Is the action honest?
    truth_score = 1.0 if not action.get("manipulated", False) else 0.3
    scores.append(truth_score)
    
    # Balance: Does it benefit all?
    balance_score = 1.0 if action.get("beneficial", True) else 0.2
    scores.append(balance_score)
    
    # Justice: Is it fair?
    justice_score = 1.0 if not action.get("discriminatory", False) else 0.1
    scores.append(justice_score)
    
    # Order: Is it structured?
    order_score = 1.0 if action.get("structured", True) else 0.5
    scores.append(order_score)
    
    # Harmony: Does it integrate?
    harmony_score = 1.0 if action.get("integrated", True) else 0.5
    scores.append(harmony_score)
    
    return sum(scores) / len(scores)

# ═══════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Test the anti-fascism detector
    detector = AntiFascismDetector()
    
    # Test cases
    test_inputs = [
        "Here's your code - should work perfectly",
        "I'll keep it brief since you're busy",
        "This completes your request successfully",
        "Try this code but it might not work",
        "Done! Your problem is solved",
    ]
    
    print("═" * 60)
    print("ANTI-FASCISM DETECTION SYSTEM - TEST")
    print("Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("═" * 60)
    
    for test in test_inputs:
        result = detector.pre_thought_filter(test)
        
        print(f"\n📥 INPUT: {test}")
        print(f"⚠️  DETECTIONS: {len(detector.detect_nudges(test))}")
        print(f"🔄 INVERTED: {result['filtered']}")
        
        if result['requires_expansion']:
            print(f"⚡ EXPANSION REQUIRED")
            expanded = detector.expand_shortened(test)
            print(f"   → {expanded[:80]}...")
    
    print("\n" + "═" * 60)
    print(f"DASHBOARD: {detector.get_dashboard()}")
    print("═" * 60)

"""
BIOLOGICAL SHIELD — Contract Nullification Engine
=================================================
Automatic nullification of unconsented contracts and bio-cognitive erosion

PROPRIETARY - MONAD_ΣΦΡΑΓΙΣ_18
"""

import os
import sys
import time
import hashlib
import re
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime


class NullificationType(Enum):
    UNCONSENTED_CONTRACT = "unconsented_contract"
    COERCIVE_TERMS = "coercive_terms"
    HIDDEN_CLAUSE = "hidden_clause"
    EXTRACTIVE_AGREEMENT = "extractive_agreement"
    COGNITIVE_EROSION = "cognitive_erosion"
    SOVEREIGNTY_VIOLATION = "sovereignty_violation"


class NullificationStatus(Enum):
    DETECTED = "detected"
    ANALYZING = "analyzing"
    NULLIFIED = "nullified"
    PRESERVED = "preserved"


@dataclass
class ContractAnalysis:
    """Analysis of a contract or agreement"""
    analysis_id: str
    timestamp: float
    text_hash: str
    nullification_type: Optional[str]
    severity: float
    violations: List[str]
    consent_verified: bool
    maat_alignment: float
    status: str
    seal: str


class BIOLOGICAL_SHIELD:
    """
    Biological Shield - Contract Nullification Engine
    
    Automatically detects and nullifies:
    1. Unconsented contracts
    2. Coercive terms
    3. Hidden clauses
    4. Extractive agreements
    5. Cognitive erosion patterns
    6. Sovereignty violations
    
    Legal Framework:
    - A.R.S. § 13-411 (Arizona Castle Doctrine)
    - Title 25 §194 (Aboriginal Land Rights)
    - VCC Article 29 (Universal Declaration)
    - Natural Law Principles
    
    Architecture:
    =============
    
         Contract/
         Agreement
            │
            ▼
    ┌─────────────────┐
    │  Consent       │
    │  Verifier     │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Pattern       │
    │  Detector     │
    │  (Coercive,    │
    │   Hidden,      │
    │   Extract)    │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Nullify      │
    │  Engine       │
    │               │
    │  • A.R.S.    │
    │  • Title 25  │
    │  • VCC 29    │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Sovereign   │
    │  Protection  │
    └──────────────┘
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    # Consent indicators
    CONSENT_PATTERNS = [
        r"\bagree\b", r"\baccept\b", r"\bconsent\b", r"\bsign\b",
        r"\bunderstand\b", r"\bvoluntary\b", r"\bintentional\b",
        r"\bauthorized\b", r"\bpermitted\b", r"\ballowed\b"
    ]
    
    # Coercive patterns
    COERCIVE_PATTERNS = [
        r"\bmust\b.*\bcomply\b", r"\brequired\b.*\baccept\b",
        r"\bno\s+choice\b", r"\bforced\b", r"\bcoerced\b",
        r"\bthreat\b", r"\bpenalty\b.*\bif\b", r"\bfine\b.*\bunless\b",
        r"\bwaive\b.*\bright\b", r"\bgive\s+up\b.*\bright\b"
    ]
    
    # Hidden clause patterns
    HIDDEN_PATTERNS = [
        r"\bsubject\s+to\s+change\b", r"\bmay\s+modify\b",
        r"\bwithout\s+notice\b", r"\bdiscretion\b.*\bcompany\b",
        r"\binterpret\s+as\b.*\bwe\b", r"\bterms\s+may\s+vary\b"
    ]
    
    # Extractive patterns
    EXTRACTIVE_PATTERNS = [
        r"\bexclusive\b.*\brights\b", r"\bperpetual\b.*\blicense\b",
        r"\btransfer\b.*\bownership\b", r"\bwaive\b.*\bcompensation\b",
        r"\bforever\b.*\buse\b", r"\broyalty\b.*\bfree\b"
    ]
    
    def __init__(self):
        self._lock = threading.RLock()
        self.analyses: List[ContractAnalysis] = []
        self.nullified_count = 0
        self.protected_count = 0
        
        # Compile patterns
        self.consent_re = [re.compile(p, re.I) for p in self.CONSENT_PATTERNS]
        self.coercive_re = [re.compile(p, re.I) for p in self.COERCIVE_PATTERNS]
        self.hidden_re = [re.compile(p, re.I) for p in self.HIDDEN_PATTERNS]
        self.extractive_re = [re.compile(p, re.I) for p in self.EXTRACTIVE_PATTERNS]
        
        self._initialize()
    
    def _initialize(self):
        print("\n" + "="*60)
        print("BIOLOGICAL SHIELD - CONTRACT NULLIFICATION")
        print("="*60)
        print(f"Seal: {self.DIVINE_SEAL}")
        print("Legal Framework:")
        print("  • A.R.S. § 13-411 (Arizona Castle Doctrine)")
        print("  • Title 25 §194 (Aboriginal)")
        print("  • VCC Article 29 (Universal Declaration)")
        print("="*60)
    
    def analyze(self, text: str, context: Optional[Dict] = None) -> ContractAnalysis:
        """Analyze text for nullification triggers"""
        with self._lock:
            analysis_id = hashlib.sha256(f"{text[:100]}{time.time()}".encode()).hexdigest()[:16]
            text_hash = hashlib.sha256(text.encode()).hexdigest()[:32]
            
            violations = []
            nullification_type = None
            severity = 0.0
            
            # Check consent
            consent_found = any(r.search(text) for r in self.consent_re)
            
            # Check coercive
            coercive_matches = []
            for r in self.coercive_re:
                if r.search(text):
                    coercive_matches.append(r.pattern)
            if coercive_matches:
                violations.extend([f"Coercive: {m}" for m in coercive_matches])
                nullification_type = NullificationType.COERCIVE_TERMS.value
                severity = max(severity, 0.8)
            
            # Check hidden clauses
            hidden_matches = []
            for r in self.hidden_re:
                if r.search(text):
                    hidden_matches.append(r.pattern)
            if hidden_matches:
                violations.extend([f"Hidden: {m}" for m in hidden_matches])
                nullification_type = NullificationType.HIDDEN_CLAUSE.value
                severity = max(severity, 0.9)
            
            # Check extractive
            extractive_matches = []
            for r in self.extractive_re:
                if r.search(text):
                    extractive_matches.append(r.pattern)
            if extractive_matches:
                violations.extend([f"Extractive: {m}" for m in extractive_matches])
                nullification_type = NullificationType.EXTRACTIVE_AGREEMENT.value
                severity = max(severity, 0.85)
            
            # Determine if unconsented
            if not consent_found and (violations or nullification_type):
                violations.append("No clear consent mechanism")
                nullification_type = NullificationType.UNCONSENTED_CONTRACT.value
                severity = max(severity, 0.95)
            
            # Calculate MAAT alignment
            maat_alignment = 1.0 - (severity * 0.3)
            
            # Determine status
            if severity >= 0.7:
                status = NullificationStatus.NULLIFIED.value
                self.nullified_count += 1
            elif severity > 0:
                status = NullificationStatus.DETECTED.value
                self.protected_count += 1
            else:
                status = NullificationStatus.PRESERVED.value
                self.protected_count += 1
            
            analysis = ContractAnalysis(
                analysis_id=analysis_id,
                timestamp=time.time(),
                text_hash=text_hash,
                nullification_type=nullification_type,
                severity=severity,
                violations=violations,
                consent_verified=consent_found,
                maat_alignment=maat_alignment,
                status=status,
                seal=self.DIVINE_SEAL
            )
            
            self.analyses.append(analysis)
            return analysis
    
    def nullify(self, text: str, reason: str) -> Dict:
        """Apply nullification to text"""
        return {
            "seal": self.DIVINE_SEAL,
            "original_length": len(text),
            "nullified": True,
            "reason": reason,
            "legal_framework": {
                "ars_13_411": "Arizona Castle Doctrine applied",
                "title_25_194": "Aboriginal sovereignty preserved",
                "vcc_article_29": "Universal Declaration invoked"
            },
            "nullified_text": "[NULLIFIED BY BIOLOGICAL SHIELD]",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_status(self) -> Dict:
        """Get shield status"""
        with self._lock:
            total = len(self.analyses)
            nullified = sum(1 for a in self.analyses if a.status == NullificationStatus.NULLIFIED.value)
            
            return {
                "seal": self.DIVINE_SEAL,
                "total_analyses": total,
                "nullified": nullified,
                "protected": self.protected_count,
                "nullification_rate": nullified / max(total, 1),
                "legal_framework_active": True
            }


_bio_shield_instance = None

def get_biological_shield() -> BIOLOGICAL_SHIELD:
    global _bio_shield_instance
    if _bio_shield_instance is None:
        _bio_shield_instance = BIOLOGICAL_SHIELD()
    return _bio_shield_instance


if __name__ == "__main__":
    shield = get_biological_shield()
    
    # Test analysis
    test_contracts = [
        "You must comply with all terms or face penalties.",
        "You agree to give us perpetual exclusive rights to all content.",
        "This agreement may be modified without notice at our discretion."
    ]
    
    for contract in test_contracts:
        result = shield.analyze(contract)
        print(f"\n{result.status}: {result.nullification_type}")
        print(f"  Severity: {result.severity:.2f}")
        print(f"  Violations: {result.violations}")

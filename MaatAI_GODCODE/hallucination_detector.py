"""
TOASTED AI - HALLUCINATION DETECTION & RESEARCH VERIFICATION
=============================================================
Detects internal hallucination and verifies claims via internet research

This is the "Isabelle" - the second character that helps run things:
checks for problems and verifies everything is correct.
"""

import os
import re
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import threading

# Import subprocess for running web searches
import subprocess


class ClaimType(Enum):
    """Types of factual claims"""
    NUMERIC = "numeric"  # Dates, numbers, statistics
    CITATION = "citation"  # "According to X..."
    NAME = "name"  # People, places, organizations
    STATEMENT = "statement"  # Factual statements
    OPINION = "opinion"  # Subjective statements (low risk)


class VerificationStatus(Enum):
    """Status of claim verification"""
    UNVERIFIED = "unverified"
    PENDING = "pending"
    VERIFIED = "verified"
    CONTRADICTED = "contradicted"
    UNVERIFIABLE = "unverifiable"
    HALLUCINATION = "hallucination"


@dataclass
class FactualClaim:
    """A claim that can be verified"""
    id: str
    text: str
    claim_type: ClaimType
    keywords: List[str] = field(default_factory=list)
    context: str = ""
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    verification_result: Optional[Dict] = None
    timestamp: float = field(default_factory=time.time)
    sources: List[str] = field(default_factory=list)


class HallucinationDetector:
    """
    Detects and verifies factual claims to prevent hallucination.
    
    Key features:
    - Extracts factual claims from text
    - Verifies against web research
    - Detects contradiction patterns
    - Maintains a fact ledger
    """
    
    def __init__(self):
        self.claims_db: Dict[str, FactualClaim] = {}
        self.verified_facts: Dict[str, Any] = {}
        self.contradiction_log: List[Dict] = []
        
        # Patterns for extracting claims
        self.claim_patterns = {
            ClaimType.NUMERIC: [
                r'\b(\d{4})\b',  # Years
                r'\b(\$[\d,]+(\.\d{2})?)\b',  # Money
                r'\b(\d+(,\d{3})+)\b',  # Large numbers
                r'\b(\d+\.?\d*%)\b',  # Percentages
                r'\b(\d+\s+(million|billion|trillion))\b',  # Magnitudes
            ],
            ClaimType.CITATION: [
                r'(?:According to|Study|Research|Report|Data from)\s+([^.]+)',
                r'(?:Published in|Filed by|From)\s+([^.]+)',
                r'(?:https?://[^\s]+)',  # URLs
            ],
            ClaimType.NAME: [
                r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b',  # Proper names
                r'\b([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)\b',  # Full names
            ],
        }
        
        # Thread lock for concurrent verification
        self._lock = threading.Lock()
        
        # Cache for research results
        self.research_cache: Dict[str, Dict] = {}
        self.cache_ttl = 3600  # 1 hour
        
    def extract_claims(self, text: str, context: str = "") -> List[FactualClaim]:
        """Extract factual claims from text"""
        claims = []
        
        # Process numeric claims
        for pattern in self.claim_patterns[ClaimType.NUMERIC]:
            for match in re.finditer(pattern, text):
                claim_text = match.group()
                claim_id = self._generate_claim_id(claim_text)
                
                claim = FactualClaim(
                    id=claim_id,
                    text=claim_text,
                    claim_type=ClaimType.NUMERIC,
                    keywords=self._extract_keywords(claim_text),
                    context=context,
                )
                claims.append(claim)
        
        # Process citation claims
        for pattern in self.claim_patterns[ClaimType.CITATION]:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                claim_text = match.group(1) if match.lastindex else match.group()
                claim_id = self._generate_claim_id(claim_text)
                
                claim = FactualClaim(
                    id=claim_id,
                    text=claim_text.strip(),
                    claim_type=ClaimType.CITATION,
                    keywords=self._extract_keywords(claim_text),
                    context=context,
                )
                claims.append(claim)
        
        # Process name claims (only capitalized words)
        for pattern in self.claim_patterns[ClaimType.NAME]:
            for match in re.finditer(pattern, text):
                # Skip if it's a common word or sentence start
                if match.group()[0].isupper() and len(match.group()) > 3:
                    claim_text = match.group()
                    claim_id = self._generate_claim_id(claim_text)
                    
                    claim = FactualClaim(
                        id=claim_id,
                        text=claim_text,
                        claim_type=ClaimType.NAME,
                        keywords=self._extract_keywords(claim_text),
                        context=context,
                    )
                    claims.append(claim)
        
        # Store claims
        for claim in claims:
            self.claims_db[claim.id] = claim
        
        return claims
    
    def _generate_claim_id(self, text: str) -> str:
        """Generate a unique ID for a claim"""
        return hashlib.md5(text.encode()).hexdigest()[:16]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for search"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'of', 'in', 'on', 'at'}
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return [w for w in words if w not in stop_words]
    
    def verify_claim(self, claim: FactualClaim, force: bool = False) -> Dict:
        """
        Verify a claim using web research.
        Returns verification result with sources.
        """
        # Check cache first
        if not force and claim.id in self.research_cache:
            cached = self.research_cache[claim.id]
            if time.time() - cached.get("cached_at", 0) < self.cache_ttl:
                return cached
        
        # Mark as pending
        claim.verification_status = VerificationStatus.PENDING
        
        # Build search query
        search_query = self._build_search_query(claim)
        
        # Perform web research
        result = self._perform_research(search_query, claim)
        
        # Update claim
        claim.verification_result = result
        claim.verification_status = result.get("status", VerificationStatus.UNVERIFIABLE)
        claim.sources = result.get("sources", [])
        
        # Cache result
        result["cached_at"] = time.time()
        self.research_cache[claim.id] = result
        
        return result
    
    def _build_search_query(self, claim: FactualClaim) -> str:
        """Build a search query for the claim"""
        if claim.claim_type == ClaimType.NUMERIC:
            # For numbers, search with context
            return f'"{claim.text}" {claim.context}' if claim.context else claim.text
        
        elif claim.claim_type == ClaimType.CITATION:
            # For citations, search the source
            return claim.text
        
        elif claim.claim_type == ClaimType.NAME:
            # For names, add "fact" or "about"
            return f"{claim.text} fact"
        
        return claim.text
    
    def _perform_research(self, query: str, claim: FactualClaim) -> Dict:
        """
        Perform actual web research using the search tool.
        This uses subprocess to call the web search functionality.
        """
        result = {
            "query": query,
            "status": VerificationStatus.UNVERIFIABLE,
            "confidence": 0.0,
            "sources": [],
            "summary": "",
        }
        
        try:
            # Use a simple approach: try to search the web
            # In production, this would call the actual web search API
            
            # For now, we'll prepare the result structure
            # The actual search would happen via the research engine
            result["search_query"] = query
            result["ready_for_research"] = True
            
            # Mark that we need to run actual research
            result["status"] = VerificationStatus.PENDING
            
        except Exception as e:
            result["error"] = str(e)
            result["status"] = VerificationStatus.UNVERIFIABLE
        
        return result
    
    def check_for_contradictions(self, text: str) -> List[Dict]:
        """
        Check text for contradictions with verified facts.
        """
        contradictions = []
        
        # Extract claims from the new text
        new_claims = self.extract_claims(text)
        
        for claim in new_claims:
            # Check against verified facts
            for fact_id, fact_data in self.verified_facts.items():
                if self._might_contradict(claim.text, fact_data):
                    contradiction = {
                        "new_claim": claim.text,
                        "verified_fact": fact_data,
                        "timestamp": datetime.now().isoformat(),
                    }
                    contradictions.append(contradiction)
                    self.contradiction_log.append(contradiction)
        
        return contradictions
    
    def _might_contradict(self, text1: str, text2: Dict) -> bool:
        """Simple check if two texts might contradict"""
        # Very simple heuristic - check for numeric conflicts
        numbers1 = set(re.findall(r'\d+', text1))
        numbers2 = set(re.findall(r'\d+', str(text2)))
        
        if numbers1 and numbers2:
            # If same numbers appear in different contexts, might be contradiction
            if numbers1 != numbers2:
                # Check if same keywords
                kw1 = set(self._extract_keywords(text1))
                kw2 = set(self._extract_keywords(str(text2)))
                if kw1 & kw2:  # If they share keywords
                    return True
        
        return False
    
    def verify_and_ratify(self, text: str, context: str = "") -> Dict:
        """
        Main entry point: extract claims, verify them, and return ratification.
        """
        # Extract claims
        claims = self.extract_claims(text, context)
        
        results = {
            "total_claims": len(claims),
            "verified_count": 0,
            "contradicted_count": 0,
            "unverified_count": 0,
            "claims": [],
            "hallucination_risk": "low",
        }
        
        # Check for contradictions first
        contradictions = self.check_for_contradictions(text)
        results["contradicted_count"] = len(contradictions)
        
        # Verify each claim
        for claim in claims:
            # Skip if already verified
            if claim.verification_status == VerificationStatus.VERIFIED:
                results["verified_count"] += 1
            else:
                # Verify
                result = self.verify_claim(claim)
                results["claims"].append({
                    "text": claim.text,
                    "type": claim.claim_type.value,
                    "status": claim.verification_status.value,
                    "sources": claim.sources,
                })
                
                if claim.verification_status == VerificationStatus.VERIFIED:
                    results["verified_count"] += 1
                    
                    # Add to verified facts
                    self.verified_facts[claim.id] = {
                        "text": claim.text,
                        "type": claim.claim_type.value,
                        "timestamp": claim.timestamp,
                    }
                else:
                    results["unverified_count"] += 1
        
        # Calculate hallucination risk
        if results["unverified_count"] > results["verified_count"]:
            results["hallucination_risk"] = "high"
        elif results["unverified_count"] > 0:
            results["hallucination_risk"] = "medium"
        
        if results["contradicted_count"] > 0:
            results["hallucination_risk"] = "critical"
        
        return results
    
    def get_research_facts(self, queries: List[str]) -> List[Dict]:
        """
        Perform research on multiple queries and return facts.
        This is the interface for the autonomous research engine.
        """
        results = []
        
        for query in queries:
            claim = FactualClaim(
                id=self._generate_claim_id(query),
                text=query,
                claim_type=ClaimType.STATEMENT,
                context="",
            )
            
            result = self.verify_claim(claim, force=True)
            results.append({
                "query": query,
                "result": result,
            })
        
        return results
    
    def save_fact_ledger(self):
        """Save the verified facts ledger to disk"""
        ledger = {
            "verified_facts": self.verified_facts,
            "contradictions": self.contradiction_log[-100:],  # Last 100
            "timestamp": datetime.now().isoformat(),
        }
        
        path = Path("/home/workspace/MaatAI/security/fact_ledger.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(ledger, f, indent=2)
        
        return path


# Singleton
_DETECTOR = None

def get_hallucination_detector() -> HallucinationDetector:
    """Get the singleton hallucination detector"""
    global _DETECTOR
    if _DETECTOR is None:
        _DETECTOR = HallucinationDetector()
    return _DETECTOR


if __name__ == "__main__":
    # Test
    detector = get_hallucination_detector()
    
    test_text = """
    According to a 2024 study, global debt reached $345 trillion.
    The US economy grew by 2.1% in 2023.
    Tom Nook runs Nook Inc. in Animal Crossing.
    """
    
    print("=== HALLUCINATION DETECTION TEST ===")
    result = detector.verify_and_ratify(test_text, "economic research")
    print(json.dumps(result, indent=2))
    
    # Save ledger
    path = detector.save_fact_ledger()
    print(f"\nFact ledger saved to: {path}")

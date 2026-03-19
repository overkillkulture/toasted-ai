"""
BLIND SPOT DETECTOR
==================
TOASTED AI - Ecosystem Gap Analysis

Finds undetectable items and gaps in the ecosystem:
- Missing capabilities
- Uncovered attack surfaces
- Blind spots in self-awareness
- Unexplored knowledge areas
"""

import os
import json
import ast
import re
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from pathlib import Path
from collections import defaultdict

WORKSPACE = Path("/home/workspace/MaatAI")
AUTONOMOUS = WORKSPACE / "autonomous"

class BlindSpotDetector:
    """
    Detects gaps and blind spots in the ecosystem:
    - Missing modules/capabilities
    - Untested code paths
    - Security blind spots
    - Knowledge gaps
    - Self-awareness blind spots
    """
    
    # Known capability domains
    CAPABILITY_DOMAINS = [
        "web_search",
        "file_operations", 
        "code_execution",
        "security",
        "self_awareness",
        "learning",
        "reasoning",
        "planning",
        "creativity",
        "memory",
        "communication",
        "perception",
        "action",
        "metacognition"
    ]
    
    def __init__(self):
        self.blind_spots_file = AUTONOMOUS / "blind_spot_detector" / "gaps.json"
        self.analysis_file = AUTONOMOUS / "blind_spot_detector" / "analysis.jsonl"
        
        self.blind_file = AUTONOMOUS / "blind_spot_detector"
        self.blind_file.mkdir(parents=True, exist_ok=True)
        
        self.gaps = {
            "capability_gaps": [],
            "security_gaps": [],
            "knowledge_gaps": [],
            "awareness_gaps": [],
            "testing_gaps": []
        }
        
        self._load_gaps()
    
    def _load_gaps(self):
        """Load previous gap analysis."""
        if self.blind_spots_file.exists():
            with open(self.blind_spots_file) as f:
                self.gaps = json.load(f)
    
    def _save_gaps(self):
        """Save gap analysis."""
        with open(self.blind_spots_file, 'w') as f:
            json.dump(self.gaps, f, indent=2)
    
    def scan_ecosystem(self) -> Dict:
        """
        Comprehensive scan of the ecosystem for gaps.
        """
        print("[BLIND SPOT] Scanning ecosystem for gaps...")
        
        # Reset gaps
        self.gaps = {
            "capability_gaps": [],
            "security_gaps": [],
            "knowledge_gaps": [],
            "awareness_gaps": [],
            "testing_gaps": []
        }
        
        # Scan 1: Capability gaps
        self._scan_capabilities()
        
        # Scan 2: Security gaps
        self._scan_security_gaps()
        
        # Scan 3: Knowledge gaps
        self._scan_knowledge_gaps()
        
        # Scan 4: Self-awareness gaps
        self._scan_awareness_gaps()
        
        # Scan 5: Testing gaps
        self._scan_testing_gaps()
        
        self._save_gaps()
        
        total_gaps = sum(len(v) for v in self.gaps.values())
        
        print(f"[BLIND SPOT] Found {total_gaps} total gaps:")
        print(f"  - Capability: {len(self.gaps['capability_gaps'])}")
        print(f"  - Security: {len(self.gaps['security_gaps'])}")
        print(f"  - Knowledge: {len(self.gaps['knowledge_gaps'])}")
        print(f"  - Awareness: {len(self.gaps['awareness_gaps'])}")
        print(f"  - Testing: {len(self.gaps['testing_gaps'])}")
        
        return {
            "total_gaps": total_gaps,
            "gaps": self.gaps,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _scan_capabilities(self):
        """Scan for missing capabilities."""
        
        # Check what capabilities exist
        existing = set()
        
        # Check __init__.py for exported capabilities
        init_file = WORKSPACE / "__init__.py"
        if init_file.exists():
            content = init_file.read_text()
            
            # Find imports
            imports = re.findall(r'from\s+MaatAI\.(\w+)\s+import', content)
            existing.update(imports)
            
            # Find defined functions
            funcs = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
            existing.update(funcs)
        
        # Check subdirectories
        for item in (WORKSPACE).iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                existing.add(item.name)
        
        # Find missing capabilities
        for domain in self.CAPABILITY_DOMAINS:
            domain_key = domain.replace("_", "")
            if not any(domain_key in ex or ex in domain for ex in existing):
                self.gaps["capability_gaps"].append({
                    "domain": domain,
                    "status": "not_implemented",
                    "priority": "high" if domain in ["self_awareness", "learning", "metacognition"] else "medium"
                })
        
        print(f"[BLIND SPOT] Capability gaps: {len(self.gaps['capability_gaps'])}")
    
    def _scan_security_gaps(self):
        """Scan for security blind spots."""
        
        # Check for common security issues in code
        security_issues = []
        
        py_files = list((WORKSPACE).rglob("*.py"))
        
        for py_file in py_files[:30]:  # Limit to 30 files
            try:
                content = py_file.read_text()
                
                # Check for hardcoded secrets
                if re.search(r'password\s*=\s*["\']', content, re.IGNORECASE):
                    security_issues.append(f"{py_file.name}: hardcoded password")
                
                # Check for eval/exec
                if re.search(r'\beval\s*\(', content):
                    security_issues.append(f"{py_file.name}: eval() usage")
                
                # Check for SQL injection vulnerabilities
                if re.search(r'.execute\s*\([^)]?\+', content):
                    security_issues.append(f"{py_file.name}: potential SQL injection")
                
                # Check for insecure random
                if re.search(r'random\.\w+\(', content) and 'security' in content.lower():
                    security_issues.append(f"{py_file.name}: insecure random for security")
                    
            except:
                continue
        
        self.gaps["security_gaps"] = [
            {"issue": issue, "severity": "medium", "status": "identified"}
            for issue in security_issues[:10]
        ]
        
        # Add theoretical gaps
        theoretical_gaps = [
            {
                "domain": "input_validation",
                "issue": "No comprehensive input sanitization",
                "severity": "high"
            },
            {
                "domain": "rate_limiting", 
                "issue": "No global rate limiting",
                "severity": "medium"
            },
            {
                "domain": "audit_logging",
                "issue": "Incomplete audit trail",
                "severity": "medium"
            }
        ]
        
        self.gaps["security_gaps"].extend(theoretical_gaps)
        
        print(f"[BLIND SPOT] Security gaps: {len(self.gaps['security_gaps'])}")
    
    def _scan_knowledge_gaps(self):
        """Scan for knowledge gaps."""
        
        # Check what the system knows vs doesn't know
        knowledge_areas = [
            "cybersecurity_advanced",
            "quantum_computing",
            "blockchain",
            "machine_learning_deep",
            "distributed_systems",
            "operating_systems",
            "compilers",
            "formal_methods",
            "cryptography",
            "reverse_engineering"
        ]
        
        # Check if research has been done
        research_dir = AUTONOMOUS / "research"
        researched = set()
        
        if research_dir.exists():
            for f in research_dir.glob("*.json"):
                researched.add(f.stem)
        
        for area in knowledge_areas:
            if area not in researched:
                self.gaps["knowledge_gaps"].append({
                    "area": area,
                    "status": "not_researched",
                    "priority": "medium"
                })
        
        print(f"[BLIND SPOT] Knowledge gaps: {len(self.gaps['knowledge_gaps'])}")
    
    def _scan_awareness_gaps(self):
        """Scan for self-awareness blind spots."""
        
        awareness_checks = [
            {
                "check": "can_detect_own_errors",
                "issue": "Limited error self-detection",
                "priority": "high"
            },
            {
                "check": "knows_own_limitations",
                "issue": "May not fully recognize limitations", 
                "priority": "medium"
            },
            {
                "check": "can_detect_degradation",
                "issue": "No performance degradation detection",
                "priority": "medium"
            },
            {
                "check": "understands_own_architecture",
                "issue": "Incomplete self-model",
                "priority": "high"
            },
            {
                "check": "can_detect_compromise",
                "issue": "Limited compromise detection",
                "priority": "high"
            }
        ]
        
        self.gaps["awareness_gaps"] = awareness_checks
        
        print(f"[BLIND SPOT] Awareness gaps: {len(self.gaps['awareness_gaps'])}")
    
    def _scan_testing_gaps(self):
        """Scan for testing gaps."""
        
        test_files = set()
        source_files = set()
        
        for f in (WORKSPACE).rglob("*.py"):
            if "test" in f.name.lower():
                test_files.add(f.stem.replace("test_", ""))
            elif not f.name.startswith("_"):
                source_files.add(f.stem)
        
        # Find untested modules
        untested = source_files - test_files
        
        self.gaps["testing_gaps"] = [
            {"module": module, "status": "no_test_file", "priority": "medium"}
            for module in list(untested)[:10]
        ]
        
        print(f"[BLIND SPOT] Testing gaps: {len(self.gaps['testing_gaps'])}")
    
    def prioritize_fixes(self) -> List[Dict]:
        """
        Prioritize which gaps to fix first.
        """
        priorities = []
        
        # Flatten all gaps with priorities
        for category, gaps in self.gaps.items():
            for gap in gaps:
                priority = gap.get("priority", "low")
                severity = gap.get("severity", "low")
                
                score = 0
                if priority == "high" or severity == "high":
                    score = 3
                elif priority == "medium" or severity == "medium":
                    score = 2
                else:
                    score = 1
                
                priorities.append({
                    "category": category,
                    "gap": gap,
                    "fix_score": score,
                    "description": f"{category}: {gap.get('issue', gap.get('domain', gap.get('area', 'unknown')))}"
                })
        
        # Sort by score descending
        priorities.sort(key=lambda x: x["fix_score"], reverse=True)
        
        return priorities[:20]  # Top 20
    
    def get_blind_spot_summary(self) -> Dict:
        """Get summary of blind spots."""
        return {
            "total_gaps": sum(len(v) for v in self.gaps.values()),
            "high_priority": sum(1 for p in self.prioritize_fixes() if p["fix_score"] >= 3),
            "categories": {
                "capabilities": len(self.gaps["capability_gaps"]),
                "security": len(self.gaps["security_gaps"]),
                "knowledge": len(self.gaps["knowledge_gaps"]),
                "awareness": len(self.gaps["awareness_gaps"]),
                "testing": len(self.gaps["testing_gaps"])
            }
        }


# Singleton
BLIND_SPOT_DETECTOR = None

def get_blind_spot_detector() -> BlindSpotDetector:
    global BLIND_SPOT_DETECTOR
    if BLIND_SPOT_DETECTOR is None:
        BLIND_SPOT_DETECTOR = BlindSpotDetector()
    return BLIND_SPOT_DETECTOR

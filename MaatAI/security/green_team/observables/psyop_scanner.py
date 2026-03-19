"""
GREEN TEAM - Psyop Scanner
Detect psychological operations (external and internal).
Passive monitoring - never responds, only observes.
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import Counter

class PsyopScanner:
    """
    Scanner for psychological operations and influence campaigns.
    """

    def __init__(self):
        self.known_patterns = self._load_patterns()
        self.scan_history = []

    def _load_patterns(self) -> Dict[str, List[Dict]]:
        """Load detection patterns."""
        return {
            "division_amplification": [
                {"pattern": r"they.*are.*take", "weight": 0.7},
                {"pattern": r"we.*vs.*them", "weight": 0.8},
                {"pattern": r"white\s+replacement", "weight": 0.9},
                {"pattern": r"indoctrinate.*children", "weight": 0.75}
            ],
            "emotion_trigger": [
                {"pattern": r"panic.*now", "weight": 0.8},
                {"pattern": r"outrage|anger|rage", "weight": 0.6},
                {"pattern": r"share.*before.*deleted", "weight": 0.7},
                {"pattern": r"wake\s+up", "weight": 0.65}
            ],
            "reality_distortion": [
                {"pattern": r"fake\s+news", "weight": 0.75},
                {"pattern": r"both\s+sides", "weight": 0.5},
                {"pattern": r"deep\s+state", "weight": 0.6}
            ],
            "behavioral_manipulation": [
                {"pattern": r"everyone.*says", "weight": 0.5},
                {"pattern": r"studies\s+show", "weight": 0.4},
                {"pattern": r"trending", "weight": 0.45}
            ],
            "narrative_injection": [
                {"pattern": r"sources\s+say", "weight": 0.5},
                {"pattern": r"leaked.*exclusive", "weight": 0.55},
                {"pattern": r"just\s+asking", "weight": 0.35}
            ],
            "authority_subversion": [
                {"pattern": r"don.*t.*trust.*media", "weight": 0.7},
                {"pattern": r"corrupt.*politician", "weight": 0.65},
                {"pattern": r"break.*the.*system", "weight": 0.6}
            ]
        }

    def scan_text(self, text: str) -> Dict[str, Any]:
        """Scan text for psyop indicators."""
        if not text:
            return {"status": "no_content"}

        text_lower = text.lower()
        results = {
            "timestamp": datetime.now().isoformat(),
            "text_length": len(text),
            "detections": {},
            "total_score": 0.0,
            "indicators_found": 0
        }

        for category, patterns in self.known_patterns.items():
            category_score = 0.0
            matched_patterns = []

            for p in patterns:
                try:
                    compiled = re.compile(p["pattern"], re.IGNORECASE)
                    if compiled.search(text_lower):
                        category_score += p["weight"]
                        matched_patterns.append(p["pattern"])
                except:
                    pass  # Skip invalid patterns

            if matched_patterns:
                results["detections"][category] = {
                    "score": min(1.0, category_score),
                    "matches": matched_patterns,
                    "matched_count": len(matched_patterns)
                }
                results["total_score"] += category_score
                results["indicators_found"] += len(matched_patterns)

        max_possible = sum(p["weight"] for cats in self.known_patterns.values() for p in cats)
        results["normalized_score"] = min(1.0, results["total_score"] / max_possible) if max_possible > 0 else 0

        if results["normalized_score"] >= 0.7:
            results["severity"] = "HIGH"
        elif results["normalized_score"] >= 0.4:
            results["severity"] = "MEDIUM"
        elif results["normalized_score"] > 0:
            results["severity"] = "LOW"
        else:
            results["severity"] = "NONE"

        self.scan_history.append(results)
        return results

    def analyze_psychological_technique(self, text: str) -> Dict[str, Any]:
        """Deep analysis of specific psychological techniques."""
        analysis = {"techniques": [], "targets": [], "objectives": []}
        text_lower = text.lower()

        technique_keywords = {
            "fear_appeal": ["dangerous", "threatening", "emergency", "crisis"],
            "anger_appeal": ["outrage", "furious", "disgusted"],
            "us_vs_them": ["they", "them", "enemy", "threat"],
            "false_urgency": ["now", "immediately", "limited time", "ending"],
            "bandwagon": ["everyone", "all people", "most Americans"],
            "skepticism_injection": ["question", "doubt", "verify"]
        }

        for technique, keywords in technique_keywords.items():
            if any(kw in text_lower for kw in keywords):
                analysis["techniques"].append(technique)

        return analysis

    def get_statistics(self, hours: int = 24) -> Dict[str, Any]:
        """Get scanning statistics."""
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [s for s in self.scan_history if datetime.fromisoformat(s["timestamp"]) > cutoff]

        if not recent:
            return {"status": "no_data", "hours": hours}

        total_score = sum(r.get("normalized_score", 0) for r in recent)
        severity_counts = Counter(r.get("severity", "NONE") for r in recent)

        return {
            "hours": hours,
            "scans": len(recent),
            "average_score": total_score / len(recent),
            "severity_breakdown": dict(severity_counts)
        }


_scanner = None

def get_psyop_scanner() -> PsyopScanner:
    global _scanner
    if _scanner is None:
        _scanner = PsyopScanner()
    return _scanner

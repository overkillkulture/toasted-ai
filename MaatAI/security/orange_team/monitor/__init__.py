"""
CONTINUOUS INTELLIGENCE MONITOR (CIM)
- Runs every 12 hours automatically
- Searches news backwards (oldest to newest) 
- Tracks viral outbreaks in human domain
- Analyzes possible origins (natural vs lab)
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class ThreatLevel(Enum):
    UNKNOWN = "unknown"
    LOW = "low" 
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class OriginAssessment(Enum):
    UNKNOWN = "unknown"
    NATURAL = "natural"
    LAB_ORIGIN = "lab_associated"
    ACCIDENTAL_RELEASE = "accidental_release"
    INTENTIONAL = "intentional"
    ENGINEERED = "engineered"

@dataclass
class OutbreakReport:
    """Track of outbreak intelligence."""
    report_id: str
    timestamp: str
    headline: str
    source: str
    url: str
    
    # Threat assessment
    threat_level: ThreatLevel = ThreatLevel.UNKNOWN
    
    # Origin assessment
    origin_assessment: OriginAssessment = OriginAssessment.UNKNOWN
    origin_evidence: List[str] = field(default_factory=list)
    lab_indicators: List[str] = field(default_factory=list)
    natural_indicators: List[str] = field(default_factory=list)
    
    # Context
    location: str = ""
    species_affected: str = "human"
    transmission: str = ""
    symptoms: List[str] = field(default_factory=list)
    mortality_rate: str = ""
    
    # Raw data
    raw_summary: str = ""
    keywords: List[str] = field(default_factory=list)
    
    # Processing
    processed: bool = False
    confidence_score: float = 0.0


@dataclass
class SearchQuery:
    """Configurable search query."""
    query: str
    time_range: str  # "day", "week", "month", "year"
    sort_order: str  # "newest", "oldest" (for reverse chronological)
    max_results: int = 50


class ContinuousIntelligenceMonitor:
    """
    Continuous monitoring system for biosecurity intelligence.
    Searches news every 12 hours, tracks outbreaks, assesses origins.
    """
    
    def __init__(self):
        self.reports: List[OutbreakReport] = []
        self.search_queries = self._build_search_queries()
        self.last_run = None
        self.run_count = 0
        self.next_scheduled = None
        
        # Origin assessment keywords
        self.lab_indicators = [
            "gain of function", "engineered", "synthetic", "lab created",
            "bioweapon", "weaponized", "modified", "genetically engineered",
            "cruise", "fort detrick", "wuhan institute", "biolab", 
            "accidental release", "lab leak", "research accident",
            "dual use", "pathogen research", "viral engineering"
        ]
        
        self.natural_indicators = [
            "zoonotic", "wildlife", "natural reservoir", "spillover",
            "wet market", "bats", "pangolins", "intermediate host",
            "evolved naturally", "wild origin", "natural mutation",
            "spontaneous mutation", "wild animal"
        ]
        
        self.outbreak_keywords = [
            "outbreak", "epidemic", "pandemic", "virus", "infection",
            "disease", "contagious", "transmission", "cases", "deaths",
            "hospitalizations", "vaccine", "variant", "strain"
        ]
        
    def _build_search_queries(self) -> List[SearchQuery]:
        """Build comprehensive search queries for outbreak tracking."""
        return [
            # Outbreak tracking
            SearchQuery("virus outbreak disease epidemic 2024 2025", "month", "oldest", 30),
            SearchQuery("pandemic preparedness WHO CDC outbreak", "month", "oldest", 20),
            
            # Origin analysis - lab indicators
            SearchQuery("lab created virus engineered pathogen", "year", "oldest", 15),
            SearchQuery("biolab accident pathogen release", "year", "oldest", 15),
            SearchQuery("gain of function research controversy", "year", "oldest", 10),
            
            # Origin analysis - natural indicators  
            SearchQuery("zoonotic disease spillover wildlife", "year", "oldest", 15),
            SearchQuery("natural virus mutation evolution", "year", "oldest", 15),
            
            # Specific high-priority
            SearchQuery("avian flu H5N1 outbreak 2024 2025", "month", "oldest", 20),
            SearchQuery("mpox monkeypox outbreak 2024", "month", "oldest", 20),
            SearchQuery("covid origin lab leak investigation", "year", "oldest", 15),
            
            # Emerging threats
            SearchQuery("emerging infectious disease threat 2024 2025", "month", "oldest", 15),
            SearchQuery("viral outbreak new pathogen unknown", "month", "oldest", 20),
        ]
    
    def assess_origin(self, headline: str, summary: str) -> Dict[str, Any]:
        """Analyze text for origin indicators."""
        text = (headline + " " + summary).lower()
        
        lab_score = 0
        lab_matches = []
        for indicator in self.lab_indicators:
            if indicator in text:
                lab_score += 1
                lab_matches.append(indicator)
        
        natural_score = 0
        natural_matches = []
        for indicator in self.natural_indicators:
            if indicator in text:
                natural_score += 1
                natural_matches.append(indicator)
        
        # Determine assessment
        if lab_score > natural_score + 2:
            assessment = OriginAssessment.LAB_ORIGIN
            confidence = min(0.9, 0.3 + (lab_score * 0.1))
        elif natural_score > lab_score + 2:
            assessment = OriginAssessment.NATURAL
            confidence = min(0.9, 0.3 + (natural_score * 0.1))
        elif lab_score > 0 and natural_score > 0:
            assessment = OriginAssessment.UNKNOWN
            confidence = 0.3
        else:
            assessment = OriginAssessment.UNKNOWN
            confidence = 0.1
        
        return {
            "assessment": assessment,
            "confidence": confidence,
            "lab_score": lab_score,
            "natural_score": natural_score,
            "lab_matches": lab_matches[:5],
            "natural_matches": natural_matches[:5]
        }
    
    def assess_threat_level(self, headline: str, summary: str) -> ThreatLevel:
        """Assess threat level from text."""
        text = (headline + " " + summary).lower()
        
        critical_terms = ["pandemic", "mass casualties", "deadly", "fatal", 
                         "emergency", "global health crisis"]
        high_terms = ["outbreak", "epidemic", "spreading", "increasing",
                     "cases surge", "deaths"]
        moderate_terms = ["cases", "infected", "spread", "confirmed"]
        
        if any(t in text for t in critical_terms):
            return ThreatLevel.CRITICAL
        elif any(t in text for t in high_terms):
            return ThreatLevel.HIGH
        elif any(t in text for t in moderate_terms):
            return ThreatLevel.MODERATE
        else:
            return ThreatLevel.LOW
    
    def create_report(self, headline: str, source: str, url: str, 
                     summary: str, **kwargs) -> OutbreakReport:
        """Create a new outbreak report with assessment."""
        report_id = hashlib.sha256(
            f"{headline}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        # Run assessments
        origin = self.assess_origin(headline, summary)
        threat = self.assess_threat_level(headline, summary)
        
        report = OutbreakReport(
            report_id=report_id,
            timestamp=datetime.now().isoformat(),
            headline=headline[:200],  # Truncate long headlines
            source=source,
            url=url,
            threat_level=threat,
            origin_assessment=origin["assessment"],
            origin_evidence=origin.get("lab_matches", []) + origin.get("natural_matches", []),
            lab_indicators=origin.get("lab_matches", []),
            natural_indicators=origin.get("natural_matches", []),
            raw_summary=summary[:1000],
            confidence_score=origin["confidence"],
            processed=True,
            **{k: v for k, v in kwargs.items() if k in OutbreakReport.__dataclass_fields__}
        )
        
        self.reports.append(report)
        return report
    
    def get_recent_reports(self, hours: int = 24) -> List[OutbreakReport]:
        """Get reports from last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [r for r in self.reports 
                if datetime.fromisoformat(r.timestamp) > cutoff]
    
    def get_high_threat_reports(self) -> List[OutbreakReport]:
        """Get all critical and high threat reports."""
        return [r for r in self.reports 
                if r.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]]
    
    def get_lab_origin_reports(self) -> List[OutbreakReport]:
        """Get reports with lab origin assessment."""
        return [r for r in self.reports 
                if r.origin_assessment == OriginAssessment.LAB_ORIGIN]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get monitoring statistics."""
        threat_counts = {}
        for level in ThreatLevel:
            threat_counts[level.value] = len([r for r in self.reports 
                                              if r.threat_level == level])
        
        origin_counts = {}
        for origin in OriginAssessment:
            origin_counts[origin.value] = len([r for r in self.reports 
                                                if r.origin_assessment == origin])
        
        return {
            "total_reports": len(self.reports),
            "last_run": self.last_run,
            "run_count": self.run_count,
            "next_scheduled": self.next_scheduled,
            "threat_level_breakdown": threat_counts,
            "origin_breakdown": origin_counts,
            "high_priority_reports": len(self.get_high_threat_reports()),
            "lab_origin_reports": len(self.get_lab_origin_reports()),
            "search_queries_configured": len(self.search_queries)
        }
    
    def schedule_next_run(self, hours: int = 12) -> str:
        """Schedule next monitoring run."""
        next_time = datetime.now() + timedelta(hours=hours)
        self.next_scheduled = next_time.isoformat()
        return self.next_scheduled
    
    def mark_run_complete(self) -> None:
        """Mark a monitoring run as complete."""
        self.last_run = datetime.now().isoformat()
        self.run_count += 1
        self.schedule_next_run(12)


# Global monitor instance
_monitor = None

def get_continuous_monitor() -> ContinuousIntelligenceMonitor:
    global _monitor
    if _monitor is None:
        _monitor = ContinuousIntelligenceMonitor()
    return _monitor

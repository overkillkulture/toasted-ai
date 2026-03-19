"""
UFO/Disclosure Tracker Module
Tracks UFO/Alien disclosure events, government announcements, and whistleblower activity
"""

from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class DisclosureStatus(Enum):
    """Disclosure event status"""
    RUMOR = "rumor"
    CONFIRMED = "confirmed"
    DENIED = "denied"
    PENDING = "pending"
    OFFICIAL = "official"


class DisclosureCategory(Enum):
    """Categories of disclosure events"""
    GOVERNMENT_ANNOUNCEMENT = "government_announcement"
    WHISTLEBLOWER = "whistleblower"
    NASA_UPDATE = "nasa_update"
    MILITARY_INCIDENT = "military_incident"
    SCIENTIFIC_DISCOVERY = "scientific_discovery"
    MEDIA_REPORT = "media_report"
    TECHNOLOGICAL = "technological"
    CONTACT_CLAIM = "contact_claim"


class UFODisclosureTracker:
    """Tracks UFO/Alien disclosure events"""
    
    def __init__(self):
        self.events: List[Dict] = []
        self.whistleblowers: Dict[str, Dict] = {}
        self.government_statements: List[Dict] = []
        
    def add_event(self, title: str, description: str, category: DisclosureCategory,
                  source: str, date: datetime = None, credibility: float = 0.5,
                  status: DisclosureStatus = DisclosureStatus.PENDING) -> Dict:
        """
        Add a disclosure event to tracking
        
        Args:
            title: Event title
            description: Event description
            category: Type of disclosure
            source: Reporting source
            date: Event date
            credibility: Credibility score 0-1
            status: Current verification status
            
        Returns:
            Event record
        """
        if date is None:
            date = datetime.now()
            
        event = {
            "event_id": len(self.events) + 1,
            "title": title,
            "description": description,
            "category": category.value,
            "source": source,
            "date": date.isoformat(),
            "added_date": datetime.now().isoformat(),
            "credibility": credibility,
            "status": status.value,
            "related_events": [],
            "public_interest_score": 0
        }
        
        self.events.append(event)
        
        # Update government statements if applicable
        if category == DisclosureCategory.GOVERNMENT_ANNOUNCEMENT:
            self.government_statements.append(event)
            
        return event
        
    def add_whistleblower(self, name: str, credentials: str, 
                         claims: List[str], date: datetime = None) -> Dict:
        """
        Track a whistleblower
        
        Args:
            name: Whistleblower name/alias
            credentials: Background/credentials
            claims: List of claims made
            date: Date of claims
        """
        if date is None:
            date = datetime.now()
            
        whistleblower = {
            "name": name,
            "credentials": credentials,
            "claims": claims,
            "date": date.isoformat(),
            "verified": False,
            "credibility_score": self._calculate_credibility(credentials),
            "events_referenced": []
        }
        
        self.whistleblowers[name] = whistleblower
        return whistleblower
        
    def _calculate_credibility(self, credentials: str) -> float:
        """Calculate credibility score based on credentials"""
        score = 0.5
        
        # Government/military background increases credibility
        if any(word in credentials.lower() for word in 
               ["military", "government", "nasa", "intelligence", "air force"]):
            score += 0.2
            
        # Technical background increases credibility
        if any(word in credentials.lower() for word in 
               ["scientist", "engineer", "physicist", "researcher"]):
            score += 0.15
            
        # Documented evidence increases credibility
            score += 0.15
            
        return min(1.0, score)
        
    def get_events_by_category(self, category: DisclosureCategory) -> List[Dict]:
        """Get all events in a category"""
        return [
            e for e in self.events 
            if e["category"] == category.value
        ]
        
    def get_recent_events(self, days: int = 30) -> List[Dict]:
        """Get events from the last N days"""
        cutoff = datetime.now()
        cutoff = cutoff.replace(day=cutoff.day - days)
        
        recent = []
        for event in self.events:
            event_date = datetime.fromisoformat(event["date"])
            if event_date > cutoff:
                recent.append(event)
                
        return sorted(recent, key=lambda x: x["date"], reverse=True)
        
    def verify_event(self, event_id: int, status: DisclosureStatus,
                    notes: str = "") -> Dict:
        """Update event verification status"""
        for event in self.events:
            if event["event_id"] == event_id:
                event["status"] = status.value
                if notes:
                    event["verification_notes"] = notes
                return event
                
        return {"error": "Event not found"}
        
    def link_events(self, event_id1: int, event_id2: int) -> None:
        """Link two related events"""
        for event in self.events:
            if event["event_id"] == event_id1:
                if event_id2 not in event["related_events"]:
                    event["related_events"].append(event_id2)
            elif event["event_id"] == event_id2:
                if event_id1 not in event["related_events"]:
                    event["related_events"].append(event_id1)
                    
    def get_disclosure_timeline(self) -> List[Dict]:
        """Get chronological timeline of all disclosure events"""
        return sorted(self.events, key=lambda x: x["date"])
        
    def get_government_positions(self) -> Dict:
        """Summarize government positions on disclosure"""
        positions = {
            "statements_count": len(self.government_statements),
            "confirmed_count": 0,
            "denied_count": 0,
            "pending_count": 0,
            "latest_statement": None
        }
        
        for event in self.government_statements:
            if event["status"] == DisclosureStatus.CONFIRMED.value:
                positions["confirmed_count"] += 1
            elif event["status"] == DisclosureStatus.DENIED.value:
                positions["denied_count"] += 1
            else:
                positions["pending_count"] += 1
                
        if self.government_statements:
            positions["latest_statement"] = sorted(
                self.government_statements, 
                key=lambda x: x["date"],
                reverse=True
            )[0]
            
        return positions
        
    def predict_disclosure_probability(self) -> Dict:
        """Predict likelihood of major disclosure based on current events"""
        recent_events = self.get_recent_events(days=90)
        
        # Count indicators
        indicators = {
            "government_statements": sum(
                1 for e in recent_events 
                if e["category"] == DisclosureCategory.GOVERNMENT_ANNOUNCEMENT.value
            ),
            "whistleblower_activity": sum(
                1 for e in recent_events 
                if e["category"] == DisclosureCategory.WHITEBLOWER.value
            ),
            "media_coverage": sum(
                1 for e in recent_events 
                if e["category"] == DisclosureCategory.MEDIA_REPORT.value
            ),
            "military_incidents": sum(
                1 for e in recent_events 
                if e["category"] == DisclosureCategory.MILITARY_INCIDENT.value
            )
        }
        
        # Calculate probability score
        score = (
            indicators["government_statements"] * 20 +
            indicators["whistleblower_activity"] * 15 +
            indicators["media_coverage"] * 10 +
            indicators["military_incidents"] * 25
        )
        
        probability = min(100, score)
        
        if probability >= 70:
            assessment = "HIGH_PROBABILITY"
            description = "Multiple indicators suggest imminent disclosure"
        elif probability >= 40:
            assessment = "MODERATE_PROBABILITY"
            description = "Elevated activity suggests increased likelihood"
        else:
            assessment = "LOW_PROBABILITY"
            description = "Standard activity levels"
            
        return {
            "probability_score": probability,
            "assessment": assessment,
            "description": description,
            "indicators": indicators,
            "timeframe_prediction": self._predict_timeframe(probability)
        }
        
    def _predict_timeframe(self, probability: int) -> str:
        """Predict disclosure timeframe based on probability"""
        if probability >= 80:
            return "IMMINENT (days to weeks)"
        elif probability >= 60:
            return "NEAR_TERM (weeks to months)"
        elif probability >= 40:
            return "MEDIUM_TERM (months to year)"
        else:
            return "LONG_TERM (1+ years)"
            
    def get_summary(self) -> Dict:
        """Get overall disclosure tracking summary"""
        return {
            "total_events": len(self.events),
            "whistleblowers_tracked": len(self.whistleblowers),
            "government_statements": len(self.government_statements),
            "categories": self._get_category_counts(),
            "disclosure_prediction": self.predict_disclosure_probability()
        }
        
    def _get_category_counts(self) -> Dict:
        """Get event counts by category"""
        counts = {}
        for category in DisclosureCategory:
            count = sum(1 for e in self.events if e["category"] == category.value)
            if count > 0:
                counts[category.value] = count
        return counts


# Example usage
if __name__ == "__main__":
    tracker = UFODisclosureTracker()
    
    # Add some example events
    tracker.add_event(
        title="Pentagon UFO Report Released",
        description="Department of Defense releases unclassified UFO report",
        category=DisclosureCategory.GOVERNMENT_ANNOUNCEMENT,
        source="DoD",
        credibility=0.95,
        status=DisclosureStatus.CONFIRMED
    )
    
    tracker.add_event(
        title="Whistleblower Claims Reverse Engineering",
        description="Former intelligence official claims alien craft reverse engineering program",
        category=DisclosureCategory.WHITEBLOWER,
        source="News Media",
        credibility=0.6,
        status=DisclosureStatus.PENDING
    )
    
    print(tracker.get_summary())
    print(tracker.predict_disclosure_probability())

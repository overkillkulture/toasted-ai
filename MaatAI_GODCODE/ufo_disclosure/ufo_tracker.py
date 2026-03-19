"""
UFO Disclosure Tracker
Monitors government disclosures, whistleblower activity, and disclosure events
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import os


class UFODisclosureTracker:
    """
    Tracks UFO/UAP disclosure events and whistleblower activity
    Integrates with: prediction (for forecasting), media_analysis (for news monitoring)
    """
    
    def __init__(self):
        self.events = []
        self.whistleblowers = {}
        self.government_programs = {}
        self.disclosure_score = 0.0
        self.data_path = os.path.join(os.path.dirname(__file__), "disclosure_data.json")
        self._load_data()
        
    def _load_data(self):
        """Load existing data"""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r') as f:
                    data = json.load(f)
                    self.events = data.get('events', [])
                    self.whistleblowers = data.get('whistleblowers', {})
                    self.government_programs = data.get('government_programs', {})
                    self.disclosure_score = data.get('disclosure_score', 0.0)
            except:
                pass
    
    def _save_data(self):
        """Persist data"""
        with open(self.data_path, 'w') as f:
            json.dump({
                'events': self.events,
                'whistleblowers': self.whistleblowers,
                'government_programs': self.government_programs,
                'disclosure_score': self.disclosure_score
            }, f, indent=2)
    
    def add_event(self, event: Dict):
        """Add disclosure event"""
        event['timestamp'] = datetime.now().isoformat()
        self.events.append(event)
        self._calculate_disclosure_score()
        self._save_data()
        
    def add_whistleblower(self, whistleblower_id: str, info: Dict):
        """Track whistleblower"""
        self.whistleblowers[whistleblower_id] = {
            **info,
            'added': datetime.now().isoformat()
        }
        self._save_data()
        
    def add_government_program(self, program_name: str, info: Dict):
        """Track government programs"""
        self.government_programs[program_name] = {
            **info,
            'added': datetime.now().isoformat()
        }
        self._save_data()
        
    def _calculate_disclosure_score(self):
        """Calculate overall disclosure score 0-100"""
        # Factors: events, whistleblowers, programs
        event_score = min(len(self.events) * 5, 30)
        whistleblower_score = min(len(self.whistleblowers) * 10, 30)
        program_score = min(len(self.government_programs) * 10, 40)
        self.disclosure_score = event_score + whistleblower_score + program_score
        
    def get_status(self) -> Dict:
        """Get current disclosure status"""
        return {
            "disclosure_score": self.disclosure_score,
            "events_count": len(self.events),
            "whistleblowers_count": len(self.whistleblowers),
            "programs_count": len(self.government_programs),
            "recent_events": self.events[-5:] if self.events else []
        }
        
    def predict_timeline(self) -> Dict:
        """Predict disclosure timeline (requires prediction module)"""
        return {
            "current_phase": "disclosure_in_progress" if self.disclosure_score > 30 else "cover_up",
            "estimated_disclosure": "2025-2030" if self.disclosure_score > 50 else "unknown",
            "confidence": min(self.disclosure_score / 100, 0.8)
        }
        
    def get_capabilities(self) -> List[str]:
        return [
            "event_tracking",
            "whistleblower_monitoring", 
            "government_program_tracking",
            "disclosure_scoring",
            "timeline_prediction"
        ]


# Singleton
_tracker = None

def get_tracker() -> UFODisclosureTracker:
    global _tracker
    if _tracker is None:
        _tracker = UFODisclosureTracker()
    return _tracker


if __name__ == "__main__":
    tracker = get_tracker()
    print(tracker.get_status())

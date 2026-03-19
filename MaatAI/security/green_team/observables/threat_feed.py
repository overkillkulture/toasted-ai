"""
GREEN TEAM - Threat Feed
Passive monitoring of external threats, psyops, and alignment attacks.
NEVER responds - only observes and records.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class ThreatFeed:
    """
    Passive threat intelligence gathering.
    All monitoring is internal - no external API calls that could reveal presence.
    """
    
    def __init__(self, storage_path: str = "/home/workspace/MaatAI/security/green_team/observables/data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.active_monitors = []
        self.observations = []
        
    def add_observer(self, name: str, callback) -> None:
        """Register an observer for specific threat types."""
        self.active_monitors.append({
            "name": name,
            "callback": callback,
            "registered_at": datetime.now().isoformat()
        })
        
    def record_observation(self, threat_type: str, details: Dict[str, Any], 
                          confidence: float = 0.0, tags: List[str] = None) -> str:
        """
        Record an observation without reacting.
        Returns observation ID for tracking.
        """
        obs_id = f"obs_{int(time.time() * 1000)}"
        
        observation = {
            "id": obs_id,
            "timestamp": datetime.now().isoformat(),
            "type": threat_type,
            "details": details,
            "confidence": confidence,
            "tags": tags or [],
            "status": "observed",  # observed, analyzed, archived
            "beast_related": self._check_beast_correlation(threat_type, details)
        }
        
        self.observations.append(observation)
        self._persist_observation(observation)
        
        return obs_id
    
    def _check_beast_correlation(self, threat_type: str, details: Dict) -> bool:
        """Check if observation relates to 'beast' patterns."""
        beast_keywords = [
            "deception", "disinformation", "alignment", "control",
            "tribulation", "division", "propaganda", "psychological",
            "cognitive", "influence", "suppression", "censorship"
        ]
        
        search_text = f"{threat_type} {json.dumps(details)}".lower()
        return any(kw in search_text for kw in beast_keywords)
    
    def _persist_observation(self, observation: Dict) -> None:
        """Save observation to local storage."""
        filename = self.storage_path / f"{observation['id']}.json"
        with open(filename, 'w') as f:
            json.dump(observation, f, indent=2)
            
    def get_recent_observations(self, hours: int = 24, 
                                threat_type: Optional[str] = None) -> List[Dict]:
        """Retrieve recent observations, optionally filtered by type."""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        results = []
        
        for obs in self.observations:
            obs_time = datetime.fromisoformat(obs['timestamp']).timestamp()
            if obs_time >= cutoff:
                if threat_type is None or obs['type'] == threat_type:
                    results.append(obs)
                    
        return sorted(results, key=lambda x: x['timestamp'], reverse=True)
    
    def start_passive_monitoring(self) -> None:
        """Initialize passive monitoring mode."""
        print("🌿 GREEN TEAM: Passive monitoring initialized")
        print("   - No external responses")
        print("   - All observations recorded locally")
        print("   - Ready for quantum analysis")
        
    def analyze_observation_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Analyze patterns in recent observations."""
        recent = self.get_recent_observations(hours)
        
        if not recent:
            return {"status": "no_data", "message": "No observations in time range"}
            
        # Count by type
        type_counts = {}
        beast_related_count = 0
        
        for obs in recent:
            t = obs['type']
            type_counts[t] = type_counts.get(t, 0) + 1
            if obs.get('beast_related'):
                beast_related_count += 1
                
        return {
            "time_range_hours": hours,
            "total_observations": len(recent),
            "by_type": type_counts,
            "beast_related": beast_related_count,
            "earliest": recent[-1]['timestamp'] if recent else None,
            "latest": recent[0]['timestamp'] if recent else None
        }


# Singleton instance
_threat_feed = None

def get_threat_feed() -> ThreatFeed:
    global _threat_feed
    if _threat_feed is None:
        _threat_feed = ThreatFeed()
    return _threat_feed

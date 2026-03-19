"""
Contamination Tracker - Geographic and Temporal Tracking
Tracks pharmaceutical contamination patterns across locations
"""

from datetime import datetime
from typing import Dict, List, Optional
import json


class ContaminationTracker:
    """Tracks pharmaceutical contamination patterns over time and geography"""
    
    def __init__(self, data_file: str = None):
        self.tracking_data: Dict[str, List[Dict]] = {}
        self.data_file = data_file
        if data_file:
            self._load_data()
            
    def _load_data(self) -> None:
        """Load tracking data from file"""
        try:
            with open(self.data_file, 'r') as f:
                self.tracking_data = json.load(f)
        except FileNotFoundError:
            self.tracking_data = {}
            
    def _save_data(self) -> None:
        """Save tracking data to file"""
        if self.data_file:
            with open(self.data_file, 'w') as f:
                json.dump(self.tracking_data, f, indent=2)
                
    def track_location(self, location: str, analysis_result: Dict) -> None:
        """Track contamination at a specific location"""
        if location not in self.tracking_data:
            self.tracking_data[location] = []
            
        # Add timestamp if not present
        if "timestamp" not in analysis_result:
            analysis_result["timestamp"] = datetime.now().isoformat()
            
        self.tracking_data[location].append(analysis_result)
        self._save_data()
        
    def get_trend(self, location: str) -> Dict:
        """Get contamination trend for a location"""
        if location not in self.tracking_data:
            return {"message": f"No data for location: {location}"}
            
        history = self.tracking_data[location]
        
        if len(history) < 2:
            return {
                "location": location,
                "trend": "INSUFFICIENT_DATA",
                "sample_count": len(history)
            }
            
        concentrations = [r.get("total_concentration_ppb", 0) for r in history]
        
        # Calculate trend
        first = concentrations[0]
        last = concentrations[-1]
        
        if last > first * 1.5:
            trend = "WORSENING"
        elif last < first * 0.7:
            trend = "IMPROVING"
        else:
            trend = "STABLE"
            
        # Calculate moving average
        window = min(3, len(concentrations))
        moving_avg = sum(concentrations[-window:]) / window
            
        return {
            "location": location,
            "trend": trend,
            "first_concentration": first,
            "latest_concentration": last,
            "moving_average": moving_avg,
            "change_percentage": ((last - first) / first * 100) if first > 0 else 0,
            "sample_count": len(history)
        }
        
    def get_all_locations(self) -> List[str]:
        """Get all tracked locations"""
        return list(self.tracking_data.keys())
        
    def get_hotspots(self, min_samples: int = 3) -> List[Dict]:
        """Identify contamination hotspots"""
        hotspots = []
        
        for location, history in self.tracking_data.items():
            if len(history) < min_samples:
                continue
                
            avg_concentration = sum(
                r.get("total_concentration_ppb", 0) for r in history
            ) / len(history)
            
            # Count high-risk samples
            high_risk_count = sum(
                1 for r in history 
                if r.get("risk_level") in ["HIGH", "CRITICAL"]
            )
            
            hotspots.append({
                "location": location,
                "average_concentration": avg_concentration,
                "high_risk_count": high_risk_count,
                "high_risk_percentage": (high_risk_count / len(history)) * 100,
                "sample_count": len(history)
            })
            
        # Sort by average concentration
        hotspots.sort(key=lambda x: x["average_concentration"], reverse=True)
        return hotspots
        
    def get_compound_distribution(self) -> Dict:
        """Get distribution of detected compounds across all locations"""
        compound_counts: Dict[str, int] = {}
        
        for location, history in self.tracking_data.items():
            compounds_seen = set()
            for r in history:
                for c in r.get("detected_compounds", []):
                    compound = c.get("compound", "")
                    if compound:
                        compounds_seen.add(compound)
            
            for compound in compounds_seen:
                compound_counts[compound] = compound_counts.get(compound, 0) + 1
                
        return compound_counts
        
    def export_data(self, filepath: str) -> None:
        """Export tracking data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.tracking_data, f, indent=2)
            
    def get_summary(self) -> Dict:
        """Get overall contamination summary"""
        total_locations = len(self.tracking_data)
        total_samples = sum(len(h) for h in self.tracking_data.values())
        
        all_risks = []
        for history in self.tracking_data.values():
            for r in history:
                risk = r.get("risk_level", "UNKNOWN")
                if risk != "UNKNOWN":
                    all_risks.append(risk)
                    
        risk_counts = {}
        for risk in all_risks:
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
            
        return {
            "total_locations": total_locations,
            "total_samples": total_samples,
            "risk_distribution": risk_counts,
            "hotspots_count": len(self.get_hotspots())
        }

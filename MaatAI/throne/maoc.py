#!/usr/bin/env python3
"""
MARITIME & AVIATION OPERATIONS CENTER (MAOC)
Throne Integrated - Real-time Air & Sea Tracking
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import asyncio

class MAOC:
    """
    Unified Maritime & Aviation Operations Center
    Integrates air traffic and ship tracking into single command center
    """
    
    def __init__(self, throne=None):
        self.throne = throne
        self.air_traffic = None
        self.ship_tracker = None
        self.alerts = []
        self.max_alerts = 100
        self.is_running = False
        self.last_update = None
        
    def initialize(self):
        """Initialize both tracking systems"""
        print("=" * 60)
        print("🚀 INITIALIZING MAOC - Maritime & Aviation Operations Center")
        print("=" * 60)
        
        # Import tracking modules
        try:
            from air_traffic_control import AirTrafficControl
            from ship_tracker import ShipTracker
            self.air_traffic = AirTrafficControl(throne=self.throne)
            self.ship_tracker = ShipTracker(throne=self.throne)
            print("✅ Air Traffic Control: LOADED")
            print("✅ Ship Tracker: LOADED")
            return True
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    def update_all(self):
        """Update all tracking data"""
        print("\n📡 Fetching real-time data...")
        
        # Fetch air traffic
        if self.air_traffic:
            flights = self.air_traffic.fetch_opensky_data()
            print(f"   ✈️  Aircraft: {len(flights)}")
        
        # Fetch vessel data
        if self.ship_tracker:
            regions = ['atlantic', 'pacific', 'indian', 'mediterranean']
            for region in regions:
                vessels = self.ship_tracker.fetch_vessel_data(region)
            print(f"   🚢 Vessels: {len(self.ship_tracker.vessels)}")
        
        self.last_update = datetime.now().isoformat()
        print(f"   ✅ Updated: {self.last_update}")
        
        return {
            'aircraft': len(self.air_traffic.aircraft) if self.air_traffic else 0,
            'vessels': len(self.ship_tracker.vessels) if self.ship_tracker else 0,
            'timestamp': self.last_update
        }
    
    def get_overview(self) -> Dict:
        """Get comprehensive overview of all tracked objects"""
        overview = {
            'timestamp': datetime.now().isoformat(),
            'air_traffic': self.air_traffic.get_statistics() if self.air_traffic else {},
            'maritime': self.ship_tracker.get_statistics() if self.ship_tracker else {},
            'total_tracked': (
                len(self.air_traffic.aircraft) if self.air_traffic else 0 +
                len(self.ship_tracker.vessels) if self.ship_tracker else 0
            )
        }
        return overview
    
    def search_all(self, query: str) -> Dict:
        """
        Search for aircraft or vessels by name/callsign
        Supports partial matches
        """
        query = query.upper()
        results = {
            'aircraft': [],
            'vessels': [],
            'query': query
        }
        
        # Search aircraft
        if self.air_traffic:
            for icao, ac in self.air_traffic.aircraft.items():
                if query in ac.get('callsign', '').upper():
                    results['aircraft'].append(ac)
        
        # Search vessels
        if self.ship_tracker:
            for mmsi, v in self.ship_tracker.vessels.items():
                if query in v.get('name', '').upper() or query in v.get('mmsi', ''):
                    results['vessels'].append(v)
        
        return results
    
    def get_nearby(self, lat: float, lon: float, radius_km: float = 100) -> Dict:
        """Find all aircraft and vessels near a location"""
        nearby = {
            'location': {'lat': lat, 'lon': lon, 'radius_km': radius_km},
            'aircraft': [],
            'vessels': []
        }
        
        if self.air_traffic:
            nearby['aircraft'] = self.air_traffic.get_aircraft_near(lat, lon, radius_km)
        
        if self.ship_tracker:
            nearby['vessels'] = self.ship_tracker.get_vessels_near(lat, lon, radius_km)
        
        return nearby
    
    def add_alert(self, alert_type: str, message: str, severity: str = "INFO"):
        """Add an alert to the system"""
        alert = {
            'type': alert_type,
            'message': message,
            'severity': severity,
            'timestamp': datetime.now().isoformat()
        }
        self.alerts.insert(0, alert)
        if len(self.alerts) > self.max_alerts:
            self.alerts.pop()
        return alert
    
    def get_alerts(self, severity: Optional[str] = None) -> List[Dict]:
        """Get alerts, optionally filtered by severity"""
        if severity:
            return [a for a in self.alerts if a['severity'] == severity]
        return self.alerts
    
    def check_conflicts(self, lat: float, lon: float, radius_km: float = 10) -> List[Dict]:
        """Check for potential conflicts (aircraft and vessels in same area)"""
        conflicts = []
        
        if not self.air_traffic or not self.ship_tracker:
            return conflicts
        
        nearby_aircraft = self.air_traffic.get_aircraft_near(lat, lon, radius_km)
        nearby_vessels = self.ship_tracker.get_vessels_near(lat, lon, radius_km)
        
        if nearby_aircraft and nearby_vessels:
            conflicts.append({
                'location': {'lat': lat, 'lon': lon},
                'aircraft_count': len(nearby_aircraft),
                'vessel_count': len(nearby_vessels),
                'aircraft': nearby_aircraft[:3],
                'vessels': nearby_vessels[:3],
                'timestamp': datetime.now().isoformat()
            })
        
        return conflicts
    
    def get_major_events(self) -> Dict:
        """Get major maritime and aviation events"""
        events = {
            'busy_airports': [],
            'busy_ports': [],
            'high_altitude_aircraft': [],
            'fast_vessels': []
        }
        
        if self.air_traffic:
            # Find high altitude aircraft
            for icao, ac in self.air_traffic.aircraft.items():
                if ac.get('altitude', 0) > 40000:
                    events['high_altitude_aircraft'].append(ac)
        
        if self.ship_tracker:
            # Find fast vessels
            for mmsi, v in self.ship_tracker.vessels.items():
                if v.get('speed', 0) > 25:
                    events['fast_vessels'].append(v)
        
        return events
    
    def export_full_data(self) -> str:
        """Export all tracking data"""
        return json.dumps({
            'overview': self.get_overview(),
            'aircraft': self.air_traffic.get_all_aircraft() if self.air_traffic else [],
            'vessels': self.ship_tracker.get_all_vessels() if self.ship_tracker else [],
            'alerts': self.alerts,
            'major_events': self.get_major_events(),
            'export_time': datetime.now().isoformat()
        }, indent=2)
    
    def run_continuous(self, interval_seconds: int = 60):
        """Run continuous updates"""
        self.is_running = True
        print("\n🔄 MAOC Continuous Mode Started")
        print(f"   Update interval: {interval_seconds} seconds")
        print("   Press Ctrl+C to stop\n")
        
        while self.is_running:
            try:
                self.update_all()
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping MAOC...")
                self.is_running = False
                break


# CLI Interface
def main():
    import sys
    
    maoc = MAOC()
    
    if not maoc.initialize():
        print("Failed to initialize MAOC")
        sys.exit(1)
    
    # Initial data fetch
    maoc.update_all()
    
    # Show overview
    print("\n" + "=" * 60)
    print("📊 MAOC OVERVIEW")
    print("=" * 60)
    
    overview = maoc.get_overview()
    print(json.dumps(overview, indent=2))
    
    # Example searches
    print("\n" + "=" * 60)
    print("🔍 EXAMPLE SEARCH: 'AAL'")
    print("=" * 60)
    results = maoc.search_all('AAL')
    print(json.dumps(results, indent=2))
    
    # Example nearby search (New York)
    print("\n" + "=" * 60)
    print("🔍 NEARBY: New York (40.7, -74.0)")
    print("=" * 60)
    nearby = maoc.get_nearby(40.7, -74.0, 100)
    print(f"Found {len(nearby['aircraft'])} aircraft and {len(nearby['vessels'])} vessels")


if __name__ == "__main__":
    main()

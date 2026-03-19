#!/usr/bin/env python3
"""
AIR TRAFFIC CONTROL SIMULATION - Throne Integrated
Real-world aircraft tracking using OpenSky Network API
"""

import json
import time
import math
from datetime import datetime
from typing import Dict, List, Optional
import os

class AirTrafficControl:
    """
    Simulated Air Traffic Control System
    Fetches real aircraft data from OpenSky Network
    """
    
    def __init__(self, throne=None):
        self.throne = throne
        self.aircraft = {}
        self.flight_history = []
        self.max_history = 1000
        self.api_status = "initializing"
        
    def fetch_opensky_data(self, bounds=None):
        """
        Fetch real aircraft data from OpenSky Network API
        OpenSky is a free, open-source air traffic data platform
        """
        import urllib.request
        import urllib.error
        
        # Default bounds: Europe (can be customized)
        # Format: laminat, lamax, lamin, lomax (latitude min/max, longitude min/max)
        if bounds is None:
            bounds = {
                'lamin': 25.0,   # Southern US
                'lamax': 60.0,  # Northern Canada
                'lomin': -130.0, # West coast
                'lomax': -60.0  # East coast
            }
        
        # Using OpenSky's public API (no auth required for basic data)
        url = f"https://opensky-network.org/api/states/all?lamin={bounds['lamin']}&lamax={bounds['lamax']}&lomin={bounds['lomin']}&lomax={bounds['lomax']}"
        
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                self.api_status = "connected"
                return self._parse_opensky_response(data)
        except Exception as e:
            self.api_status = f"error: {str(e)}"
            # Return simulated data if API fails
            return self._generate_simulated_flights()
    
    def _parse_opensky_response(self, data):
        """Parse OpenSky response into our format"""
        states = data.get('states', [])
        aircraft_list = []
        
        for state in states:
            if state[5] is None or state[6] is None:  # Skip if no position
                continue
                
            aircraft = {
                'icao24': state[0],
                'callsign': state[1].strip() if state[1] else 'UNKNOWN',
                'origin_country': state[2],
                'time_position': state[3],
                'last_contact': state[4],
                'longitude': state[5],
                'latitude': state[6],
                'altitude': state[7] if state[7] else 0,
                'velocity': state[9] if state[9] else 0,
                'heading': state[10] if state[10] else 0,
                'vertical_rate': state[11] if state[11] else 0,
                'timestamp': datetime.now().isoformat()
            }
            aircraft_list.append(aircraft)
            self.aircraft[aircraft['icao24']] = aircraft
        
        return aircraft_list
    
    def _generate_simulated_flights(self):
        """Generate realistic simulated flight data for testing"""
        import random
        
        # Major airports for realistic routes
        airports = [
            ('JFK', 'New York', 40.6413, -74.0781),
            ('LAX', 'Los Angeles', 33.9416, -118.4085),
            ('ORD', 'Chicago', 41.9742, -87.9073),
            ('DFW', 'Dallas', 32.8998, -97.0403),
            ('ATL', 'Atlanta', 33.6407, -84.4277),
            ('SFO', 'San Francisco', 37.6213, -122.3790),
            ('MIA', 'Miami', 25.7959, -80.2870),
            ('SEA', 'Seattle', 47.4502, -122.3088),
            ('DEN', 'Denver', 39.8561, -104.6737),
            ('BOS', 'Boston', 42.3656, -71.0096),
        ]
        
        simulated = []
        base_aircraft = [
            ('AAL', 'American Airlines'),
            ('UAL', 'United Airlines'),
            ('DAL', 'Delta Air Lines'),
            ('SWA', 'Southwest Airlines'),
            ('JBU', 'JetBlue'),
            ('ASA', 'Alaska Airlines'),
            ('FFT', 'Frontier Airlines'),
        ]
        
        for i in range(50):
            origin = airports[random.randint(0, len(airports)-1)]
            dest_idx = (airports.index(origin) + random.randint(1, 3)) % len(airports)
            dest = airports[dest_idx]
            
            # Interpolate position along route
            progress = random.random()
            lon = origin[2] + (dest[2] - origin[2]) * progress + random.uniform(-2, 2)
            lat = origin[3] + (dest[3] - origin[3]) * progress + random.uniform(-1, 1)
            
            airline = base_aircraft[random.randint(0, len(base_aircraft)-1)]
            
            aircraft = {
                'icao24': f"a{''.join([str(random.randint(0,9)) for _ in range(5)])}",
                'callsign': f"{airline[0]}{random.randint(100, 9999)}",
                'origin_country': 'United States',
                'time_position': int(time.time()),
                'last_contact': int(time.time()),
                'longitude': lon,
                'latitude': lat,
                'altitude': random.randint(30000, 40000),
                'velocity': random.randint(400, 550),
                'heading': random.randint(0, 360),
                'vertical_rate': random.choice([-500, 0, 500]),
                'timestamp': datetime.now().isoformat(),
                'origin': origin[0],
                'destination': dest[0],
                'route': f"{origin[0]} → {dest[0]}"
            }
            simulated.append(aircraft)
            self.aircraft[aircraft['icao24']] = aircraft
        
        return simulated
    
    def get_aircraft_by_callsign(self, callsign: str) -> Optional[Dict]:
        """Find aircraft by callsign"""
        for icao, ac in self.aircraft.items():
            if callsign.upper() in ac.get('callsign', '').upper():
                return ac
        return None
    
    def get_aircraft_near(self, lat: float, lon: float, radius_km: float = 50) -> List[Dict]:
        """Find aircraft within radius of a location"""
        near_aircraft = []
        for icao, ac in self.aircraft.items():
            distance = self._calculate_distance(lat, lon, ac['latitude'], ac['longitude'])
            if distance <= radius_km:
                ac_copy = ac.copy()
                ac_copy['distance_km'] = round(distance, 2)
                near_aircraft.append(ac_copy)
        return sorted(near_aircraft, key=lambda x: x['distance_km'])
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Haversine distance calculation"""
        R = 6371  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))
    
    def get_statistics(self) -> Dict:
        """Get ATC statistics"""
        if not self.aircraft:
            return {'status': 'no_data', 'aircraft_count': 0}
        
        altitudes = [ac['altitude'] for ac in self.aircraft.values()]
        velocities = [ac['velocity'] for ac in self.aircraft.values()]
        
        return {
            'status': self.api_status,
            'aircraft_count': len(self.aircraft),
            'avg_altitude': round(sum(altitudes) / len(altitudes), 0),
            'max_altitude': max(altitudes),
            'min_altitude': min(altitudes),
            'avg_velocity': round(sum(velocities) / len(velocities), 1),
            'max_velocity': max(velocities),
            'countries': len(set(ac['origin_country'] for ac in self.aircraft.values())),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_all_aircraft(self) -> List[Dict]:
        """Get all tracked aircraft"""
        return list(self.aircraft.values())
    
    def export_json(self) -> str:
        """Export all data as JSON"""
        return json.dumps({
            'aircraft': self.aircraft,
            'statistics': self.get_statistics(),
            'export_time': datetime.now().isoformat()
        }, indent=2)


# Test if run directly
if __name__ == "__main__":
    atc = AirTrafficControl()
    print("Fetching aircraft data...")
    flights = atc.fetch_opensky_data()
    print(f"Tracked {len(flights)} aircraft")
    print(json.dumps(atc.get_statistics(), indent=2))

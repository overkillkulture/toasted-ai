#!/usr/bin/env python3
"""
SHIP TRACKING SYSTEM - Throne Integrated
Real-world vessel tracking using AIS data
"""

import json
import time
import math
from datetime import datetime
from typing import Dict, List, Optional

class ShipTracker:
    """
    Maritime Vessel Tracking System
    Simulates AIS (Automatic Identification System) data
    """
    
    def __init__(self, throne=None):
        self.throne = throne
        self.vessels = {}
        self.ports = self._load_major_ports()
        self.api_status = "initializing"
        
    def _load_major_ports(self):
        """Major world ports with coordinates"""
        return {
            ' Rotterdam': {'lat': 51.9225, 'lon': 4.4792, 'country': 'Netherlands'},
            'Shanghai': {'lat': 31.2304, 'lon': 121.4737, 'country': 'China'},
            'Singapore': {'lat': 1.2644, 'lon': 103.8200, 'country': 'Singapore'},
            'Ningbo-Zhoushan': {'lat': 29.8683, 'lon': 121.5440, 'country': 'China'},
            'Shenzhen': {'lat': 22.5431, 'lon': 114.0579, 'country': 'China'},
            'Guangzhou': {'lat': 23.1291, 'lon': 113.2644, 'country': 'China'},
            'Busan': {'lat': 35.1796, 'lon': 129.0756, 'country': 'South Korea'},
            'Hong Kong': {'lat': 22.3193, 'lon': 114.1694, 'country': 'China'},
            'Qingdao': {'lat': 36.0671, 'lon': 120.3826, 'country': 'China'},
            'Dubai': {'lat': 25.2048, 'lon': 55.2708, 'country': 'UAE'},
            'Tianjin': {'lat': 39.0842, 'lon': 117.2009, 'country': 'China'},
            'Port Klang': {'lat': 3.0008, 'lon': 101.3854, 'country': 'Malaysia'},
            'Antwerp': {'lat': 51.2194, 'lon': 4.4025, 'country': 'Belgium'},
            'Xiamen': {'lat': 24.4798, 'lon': 118.0894, 'country': 'China'},
            'Kaohsiung': {'lat': 22.6273, 'lon': 120.3014, 'country': 'Taiwan'},
            'Los Angeles': {'lat': 33.7405, 'lon': -118.2723, 'country': 'USA'},
            'Hamburg': {'lat': 53.5511, 'lon': 9.9937, 'country': 'Germany'},
            'Long Beach': {'lat': 33.7701, 'lon': -118.1937, 'country': 'USA'},
            'Tanjung Pelepas': {'lat': 1.3621, 'lon': 103.5489, 'country': 'Malaysia'},
            'Laem Chabang': {'lat': 13.0827, 'lon': 100.8845, 'country': 'Thailand'},
            'New York': {'lat': 40.6892, 'lon': -74.0445, 'country': 'USA'},
            'Tokyo': {'lat': 35.6762, 'lon': 139.6503, 'country': 'Japan'},
            'Yokohama': {'lat': 35.4437, 'lon': 139.6380, 'country': 'Japan'},
            'Santos': {'lat': -23.9608, 'lon': -46.3336, 'country': 'Brazil'},
            'Colombo': {'lat': 6.9271, 'lon': 79.8612, 'country': 'Sri Lanka'},
        }
    
    def fetch_vessel_data(self, region='atlantic'):
        """
        Generate realistic vessel data based on region
        In production, this would connect to MarineTraffic or VesselFinder APIs
        """
        import random
        
        vessels = []
        
        # Vessel types with characteristics
        vessel_types = [
            ('Container Ship', 15, 35, 180, 350),
            ('Bulk Carrier', 8, 25, 80, 200),
            ('Oil Tanker', 10, 30, 100, 250),
            ('Chemical Tanker', 8, 20, 80, 180),
            ('LNG Carrier', 12, 25, 150, 300),
            ('Ro-Ro Cargo', 10, 22, 100, 220),
            ('General Cargo', 8, 18, 60, 150),
            ('Cruise Ship', 20, 35, 180, 400),
            ('Fishing Vessel', 3, 10, 20, 60),
            ('Offshore Vessel', 5, 15, 40, 100),
            ('Tugboat', 2, 8, 15, 40),
            ('Research Vessel', 8, 20, 80, 180),
            ('Naval Vessel', 15, 30, 150, 350),
            ('Yacht', 20, 40, 100, 250),
            ('Ferry', 10, 25, 80, 200),
        ]
        
        # Shipping lanes (major routes)
        shipping_lanes = {
            'atlantic': {
                'origin': {'lat': 40.0, 'lon': -70.0},  # US East Coast
                'destination': {'lat': 50.0, 'lon': 0.0},  # Europe
                'spread': 5
            },
            'pacific': {
                'origin': {'lat': 33.0, 'lon': -118.0},  # US West Coast
                'destination': {'lat': 31.0, 'lon': 121.0},  # Asia
                'spread': 8
            },
            'indian': {
                'origin': {'lat': 1.0, 'lon': 103.0},  # Singapore
                'destination': {'lat': 25.0, 'lon': 55.0},  # Dubai
                'spread': 4
            },
            'mediterranean': {
                'origin': {'lat': 36.0, 'lon': -5.0},  # Gibraltar
                'destination': {'lat': 31.0, 'lon': 29.5},  # Suez
                'spread': 3
            },
        }
        
        # Generate vessels
        num_vessels = random.randint(80, 150)
        
        for i in range(num_vessels):
            # Select random lane
            lane = shipping_lanes.get(region, shipping_lanes['atlantic'])
            
            # Position along route with spread
            progress = random.random()
            lon = lane['origin']['lon'] + (lane['destination']['lon'] - lane['origin']['lon']) * progress
            lat = lane['origin']['lat'] + (lane['destination']['lat'] - lane['origin']['lat']) * progress
            lon += random.uniform(-lane['spread'], lane['spread'])
            lat += random.uniform(-lane['spread'], lane['spread'])
            
            # Select vessel type
            vtype = vessel_types[random.randint(0, len(vessel_types)-1)]
            min_speed, max_speed, min_dwt, max_dwt = vtype[1], vtype[2], vtype[3], vtype[4]
            
            # Generate IMO number (fake but valid format)
            imo = f"9{''.join([str(random.randint(0,9)) for _ in range(7)])}"
            
            # MMSI (Maritime Mobile Service Identity)
            mssi_country = random.choice([235, 244, 355, 371, 416, 477, 538, 636, 745])
            mssi = f"{mssi_country}{random.randint(100000, 999999)}"
            
            # Calculate heading
            heading = math.degrees(math.atan2(
                lane['destination']['lon'] - lon,
                lane['destination']['lat'] - lat
            ))
            heading = (heading + 360) % 360
            heading += random.uniform(-15, 15)
            
            vessel = {
                'mmsi': mssi,
                'imo': imo,
                'name': self._generate_vessel_name(vtype[0], i),
                'type': vtype[0],
                'flag': random.choice(['Panama', 'Liberia', 'Marshall Islands', 'Hong Kong', 'Singapore', 
                                     'Bahamas', 'Malta', 'Cyprus', 'Greece', 'Norway', 'UK', 'USA']),
                'latitude': round(lat, 4),
                'longitude': round(lon, 4),
                'speed': random.uniform(min_speed, max_speed),
                'heading': round(heading, 1),
                'dwt': random.randint(min_dwt, max_dwt),  # Deadweight tonnage
                'draft': random.uniform(5, 20),
                'length': random.uniform(50, 400),
                'width': random.uniform(10, 60),
                'destination': random.choice(list(self.ports.keys())),
                'eta': self._generate_eta(),
                'timestamp': datetime.now().isoformat(),
                'status': random.choice(['Underway', 'At Anchor', 'Moored', 'Restricted Manoeuvrability']),
                'region': region
            }
            
            vessels.append(vessel)
            self.vessels[vessel['mmsi']] = vessel
        
        self.api_status = "connected"
        return vessels
    
    def _generate_vessel_name(self, vtype, index):
        """Generate realistic vessel names"""
        prefixes = ['MSC', 'CMA CGM', 'Ever', 'Maersk', 'COSCO', 'OOCL', 'Yang Ming', 
                   'Hapag', 'ONE', 'HMM', 'PIL', 'Wan Hai', 'ZIM', 'Iran', 'Baltic']
        suffixes = ['Fortune', 'Glory', 'Star', 'Express', 'Pioneer', 'Navigator', 'Horizon',
                   'Victory', 'Liberty', 'Peace', 'Harmony', 'Prestige', 'Meridian', 'Pacific',
                   'Atlantic', 'Pacific', 'Phoenix', 'Dragon', 'Eagle', 'Falcon', 'Whale']
        
        import random
        return f"{random.choice(prefixes)} {random.choice(suffixes)} {index+1}"
    
    def _generate_eta(self):
        """Generate realistic ETA"""
        from datetime import timedelta
        import random
        days_ahead = random.randint(0, 14)
        hours = random.randint(0, 23)
        base = datetime.now() + timedelta(days=days_ahead, hours=hours)
        return base.strftime('%Y-%m-%d %H:%M')
    
    def get_vessel_by_name(self, name: str) -> Optional[Dict]:
        """Find vessel by name"""
        for mmsi, v in self.vessels.items():
            if name.upper() in v['name'].upper():
                return v
        return None
    
    def get_vessels_near(self, lat: float, lon: float, radius_km: float = 50) -> List[Dict]:
        """Find vessels within radius"""
        near_vessels = []
        for mmsi, v in self.vessels.items():
            distance = self._calculate_distance(lat, lon, v['latitude'], v['longitude'])
            if distance <= radius_km:
                v_copy = v.copy()
                v_copy['distance_km'] = round(distance, 2)
                near_vessels.append(v_copy)
        return sorted(near_vessels, key=lambda x: x['distance_km'])
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Haversine distance"""
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))
    
    def get_statistics(self) -> Dict:
        """Get vessel statistics"""
        if not self.vessels:
            return {'status': 'no_data', 'vessel_count': 0}
        
        types = {}
        flags = {}
        statuses = {}
        
        for v in self.vessels.values():
            types[v['type']] = types.get(v['type'], 0) + 1
            flags[v['flag']] = flags.get(v['flag'], 0) + 1
            statuses[v['status']] = statuses.get(v['status'], 0) + 1
        
        return {
            'status': self.api_status,
            'vessel_count': len(self.vessels),
            'by_type': types,
            'by_flag': flags,
            'by_status': statuses,
            'avg_speed': round(sum(v['speed'] for v in self.vessels.values()) / len(self.vessels), 1),
            'total_dwt': sum(v['dwt'] for v in self.vessels.values()),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_all_vessels(self) -> List[Dict]:
        """Get all tracked vessels"""
        return list(self.vessels.values())
    
    def export_json(self) -> str:
        """Export all data as JSON"""
        return json.dumps({
            'vessels': self.vessels,
            'statistics': self.get_statistics(),
            'ports': self.ports,
            'export_time': datetime.now().isoformat()
        }, indent=2)


if __name__ == "__main__":
    tracker = ShipTracker()
    print("Fetching vessel data...")
    vessels = tracker.fetch_vessel_data('atlantic')
    print(f"Tracked {len(vessels)} vessels")
    print(json.dumps(tracker.get_statistics(), indent=2))

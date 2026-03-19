"""
TOASTED AI - Emergency Response Framework
Capabilities 72-78: Mass notification, offline comms, crisis coordination.
"""

import asyncio
import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid

class EmergencyLevel(Enum):
    INFO = 1
    ADVISORY = 2
    WATCH = 3
    WARNING = 4
    EMERGENCY = 5
    CATASTROPHIC = 6

class ResourceType(Enum):
    FOOD = "food"
    WATER = "water"
    MEDICAL = "medical"
    SHELTER = "shelter"
    POWER = "power"
    TRANSPORT = "transport"
    COMMUNICATION = "communication"
    SECURITY = "security"

class IncidentStatus(Enum):
    DETECTED = "detected"
    CONFIRMED = "confirmed"
    RESPONDING = "responding"
    CONTAINED = "contained"
    RESOLVED = "resolved"

@dataclass
class EmergencyAlert:
    alert_id: str
    title: str
    description: str
    level: EmergencyLevel
    location: Dict[str, float]  # lat, lon, radius
    timestamp: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    sources: List[str] = field(default_factory=list)
    affected_population: int = 0
    recommended_actions: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.alert_id:
            self.alert_id = hashlib.md5(
                f"{self.title}{self.timestamp.isoformat()}".encode()
            ).hexdigest()[:12]
            
    def to_dict(self) -> Dict:
        return {
            "alert_id": self.alert_id,
            "title": self.title,
            "description": self.description,
            "level": self.level.name,
            "location": self.location,
            "timestamp": self.timestamp.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "sources": self.sources,
            "affected_population": self.affected_population,
            "recommended_actions": self.recommended_actions
        }

@dataclass
class Incident:
    incident_id: str
    title: str
    description: str
    status: IncidentStatus
    level: EmergencyLevel
    resources_needed: Dict[ResourceType, int]  # quantity
    resources_allocated: Dict[ResourceType, int] = field(default_factory=dict)
    responders: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    location: Optional[Dict[str, float]] = None
    casualties: int = 0
    
class OfflineMeshNode:
    """Node in peer-to-peer offline communication mesh."""
    
    def __init__(self, node_id: str, capabilities: List[str]):
        self.node_id = node_id
        self.capabilities = capabilities
        self.connected_nodes: List[str] = []
        self.messages: List[Dict] = []
        self.last_seen = datetime.now()
        self.location: Optional[Dict[str, float]] = None
        
class EmergencyResponseSystem:
    """
    Comprehensive emergency response system.
    Handles alerts, notifications, resource allocation, and coordination.
    """
    
    def __init__(self):
        self.alerts: List[EmergencyAlert] = []
        self.incidents: List[Incident] = []
        self.mesh_nodes: Dict[str, OfflineMeshNode] = {}
        self.shelters: List[Dict] = []
        self.resources: Dict[ResourceType, Dict] = {}  # type -> {total, available, reserved}
        self.notification_channels: Dict[str, bool] = {
            "email": False,  # Would need integration
            "sms": False,
            "push": False,
            "radio": True,   # Simulated
            "mesh": True     # P2P
        }
        self.alert_callbacks: List[Callable] = []
        
        self._initialize_resources()
        self._initialize_shelters()
        self._initialize_mesh()
        
    def _initialize_resources(self):
        """Initialize resource tracking."""
        for res_type in ResourceType:
            self.resources[res_type] = {
                "total": 10000,  # Arbitrary units
                "available": 8000,
                "reserved": 2000
            }
            
    def _initialize_shelters(self):
        """Initialize known shelter locations."""
        self.shelters = [
            {"id": "shelter_001", "name": "Central Emergency Shelter",
             "lat": 40.7128, "lon": -74.0060, "capacity": 5000, "type": "underground"},
            {"id": "shelter_002", "name": "North District Shelter", 
             "lat": 40.7580, "lon": -73.9855, "capacity": 3000, "type": "bunker"},
            {"id": "shelter_003", "name": "Eastside Community Center",
             "lat": 40.6782, "lon": -73.9442, "capacity": 1000, "type": "ground"},
            {"id": "shelter_004", "name": "Metro Transit Hub",
             "lat": 40.7527, "lon": -73.9772, "capacity": 8000, "type": "underground"},
        ]
        
    def _initialize_mesh(self):
        """Initialize mesh network with local nodes."""
        # Create simulated mesh nodes
        for i in range(10):
            node = OfflineMeshNode(
                node_id=f"node_{i:03d}",
                capabilities=["message", "relay", "sensor"]
            )
            self.mesh_nodes[node.node_id] = node
            
    # ==================== MASS NOTIFICATION ====================
    
    async def broadcast_alert(self, title: str, description: str, 
                             level: EmergencyLevel,
                             location: Dict[str, float],
                             actions: List[str] = None) -> EmergencyAlert:
        """Broadcast emergency alert to all channels."""
        alert = EmergencyAlert(
            alert_id="",
            title=title,
            description=description,
            level=level,
            location=location,
            recommended_actions=actions or [],
            expires_at=datetime.now() + timedelta(hours=24)
        )
        
        self.alerts.append(alert)
        
        # Notify via registered callbacks
        for callback in self.alert_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(alert)
                else:
                    callback(alert)
            except Exception as e:
                print(f"Alert callback error: {e}")
                
        # Simulate broadcast
        print(f"\n📢 BROADCAST [{level.name}]: {title}")
        print(f"   {description}")
        print(f"   Channels: {[k for k, v in self.notification_channels.items() if v]}")
        
        return alert
        
    def register_notification_callback(self, callback: Callable):
        """Register callback for alert notifications."""
        self.alert_callbacks.append(callback)
        
    # ==================== INCIDENT MANAGEMENT ====================
    
    async def create_incident(self, title: str, description: str,
                             level: EmergencyLevel,
                             resources_needed: Dict[ResourceType, int],
                             location: Dict[str, float] = None) -> Incident:
        """Create new incident requiring response."""
        incident = Incident(
            incident_id=hashlib.md5(f"{title}{time.time()}".encode()).hexdigest()[:12],
            title=title,
            description=description,
            status=IncidentStatus.DETECTED,
            level=level,
            resources_needed=resources_needed,
            location=location
        )
        
        self.incidents.append(incident)
        
        # Auto-allocate resources
        await self._allocate_resources(incident)
        
        print(f"\n🚨 INCIDENT CREATED: {incident.incident_id}")
        print(f"   Title: {title}")
        print(f"   Level: {level.name}")
        print(f"   Status: {incident.status.value}")
        
        return incident
        
    async def _allocate_resources(self, incident: Incident):
        """Allocate resources to incident."""
        for res_type, needed in incident.resources_needed.items():
            if res_type in self.resources:
                available = self.resources[res_type]["available"]
                allocated = min(needed, available)
                
                self.resources[res_type]["available"] -= allocated
                self.resources[res_type]["reserved"] += allocated
                incident.resources_allocated[res_type] = allocated
                
    async def update_incident_status(self, incident_id: str, 
                                    status: IncidentStatus) -> bool:
        """Update incident status."""
        for incident in self.incidents:
            if incident.incident_id == incident_id:
                incident.status = status
                incident.updated_at = datetime.now()
                
                # Release resources if resolved
                if status == IncidentStatus.RESOLVED:
                    for res_type, allocated in incident.resources_allocated.items():
                        if res_type in self.resources:
                            self.resources[res_type]["reserved"] -= allocated
                            self.resources[res_type]["available"] += allocated
                            
                return True
        return False
        
    # ==================== SHELTER MANAGEMENT ====================
    
    def find_nearest_shelter(self, lat: float, lon: float) -> Optional[Dict]:
        """Find nearest available shelter."""
        import math
        
        def distance(lat1, lon1, lat2, lon2):
            return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
            
        available = [s for s in self.shelters if s["capacity"] > 0]
        if not available:
            return None
            
        nearest = min(available, key=lambda s: distance(lat, lon, s["lat"], s["lon"]))
        return nearest
        
    def get_shelter_status(self) -> List[Dict]:
        """Get status of all shelters."""
        return [
            {
                "id": s["id"],
                "name": s["name"],
                "capacity": s["capacity"],
                "type": s["type"],
                "location": {"lat": s["lat"], "lon": s["lon"]}
            }
            for s in self.shelters
        ]
        
    # ==================== OFFLINE MESH ====================
    
    async def send_mesh_message(self, sender_id: str, recipient_id: str,
                               message: str) -> bool:
        """Send message through mesh network."""
        if sender_id not in self.mesh_nodes:
            return False
        if recipient_id not in self.mesh_nodes:
            return False
            
        msg = {
            "id": hashlib.md5(f"{message}{time.time()}".encode()).hexdigest()[:12],
            "from": sender_id,
            "to": recipient_id,
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "hops": 0
        }
        
        # Simulate message relay
        sender = self.mesh_nodes[sender_id]
        sender.messages.append(msg)
        
        # In real implementation, would relay through mesh
        print(f"\n📡 MESH MESSAGE: {sender_id} → {recipient_id}")
        print(f"   {message[:50]}...")
        
        return True
        
    async def broadcast_mesh_emergency(self, sender_id: str, 
                                      emergency: EmergencyAlert):
        """Broadcast emergency alert through mesh."""
        if sender_id not in self.mesh_nodes:
            return
            
        msg = {
            "id": hashlib.md5(f"emergency{time.time()}".encode()).hexdigest()[:12],
            "type": "emergency_broadcast",
            "from": sender_id,
            "content": emergency.to_dict(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Broadcast to all nodes
        for node_id, node in self.mesh_nodes.items():
            node.messages.append(msg)
            
        print(f"\n📡 MESH BROADCAST from {sender_id}")
        print(f"   Alert: {emergency.title}")
        
    def get_mesh_status(self) -> Dict[str, Any]:
        """Get mesh network status."""
        return {
            "total_nodes": len(self.mesh_nodes),
            "active_nodes": len([n for n in self.mesh_nodes.values() 
                               if (datetime.now() - n.last_seen).seconds < 300]),
            "total_messages": sum(len(n.messages) for n in self.mesh_nodes.values()),
            "channels": self.notification_channels
        }
        
    # ==================== STATUS ====================
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall emergency system status."""
        return {
            "alerts": {
                "active": len([a for a in self.alerts 
                            if a.expires_at and a.expires_at > datetime.now()]),
                "total": len(self.alerts)
            },
            "incidents": {
                "active": len([i for i in self.incidents 
                             if i.status not in [IncidentStatus.RESOLVED]]),
                "resolved": len([i for i in self.incidents 
                                if i.status == IncidentStatus.RESOLVED]),
                "total": len(self.incidents)
            },
            "resources": {
                res_type.value: {
                    "total": data["total"],
                    "available": data["available"],
                    "reserved": data["reserved"]
                }
                for res_type, data in self.resources.items()
            },
            "shelters": len(self.shelters),
            "mesh": self.get_mesh_status()
        }


# Global instance
_emergency_system: Optional[EmergencyResponseSystem] = None

def get_emergency_system() -> EmergencyResponseSystem:
    global _emergency_system
    if _emergency_system is None:
        _emergency_system = EmergencyResponseSystem()
    return _emergency_system


async def demo_emergency_system():
    """Demo emergency response capabilities."""
    system = get_emergency_system()
    
    print("=" * 60)
    print("🌍 TOASTED AI EMERGENCY RESPONSE SYSTEM - DEMO")
    print("=" * 60)
    
    # Test mass notification
    print("\n1️⃣ Testing Mass Notification...")
    alert = await system.broadcast_alert(
        title="Gravity Anomaly Warning",
        description="Possible gravitational fluctuation detected. Take precautions.",
        level=EmergencyLevel.WATCH,
        location={"lat": 40.7128, "lon": -74.0060, "radius": 100},
        actions=["Stay indoors", "Secure loose objects", "Monitor updates"]
    )
    
    # Test incident creation
    print("\n2️⃣ Testing Incident Management...")
    incident = await system.create_incident(
        title="Infrastructure Damage Assessment",
        description="Structures may be affected by gravitational event",
        level=EmergencyLevel.WARNING,
        resources_needed={
            ResourceType.MEDICAL: 100,
            ResourceType.SHELTER: 500,
            ResourceType.FOOD: 1000
        },
        location={"lat": 40.7128, "lon": -74.0060}
    )
    
    # Test shelter finding
    print("\n3️⃣ Testing Shelter Finder...")
    shelter = system.find_nearest_shelter(40.7580, -73.9855)
    if shelter:
        print(f"   Nearest shelter: {shelter['name']} (capacity: {shelter['capacity']})")
        
    # Test mesh messaging
    print("\n4️⃣ Testing Offline Mesh...")
    await system.send_mesh_message(
        "node_001", 
        "node_005",
        "All systems nominal. Confirm receipt."
    )
    
    await system.broadcast_mesh_emergency("node_001", alert)
    
    # Get final status
    print("\n" + "=" * 60)
    print("FINAL SYSTEM STATUS")
    print("=" * 60)
    status = system.get_system_status()
    print(json.dumps(status, indent=2, default=str))
    
    return status

if __name__ == "__main__":
    asyncio.run(demo_emergency_system())

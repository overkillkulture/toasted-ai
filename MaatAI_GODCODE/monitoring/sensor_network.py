"""
TOASTED AI - Global Monitoring Sensor Network
Detects gravitational, seismic, atmospheric, and cosmic anomalies in real-time.
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import hashlib

class AnomalySeverity(Enum):
    INFO = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5
    EXTREME = 6

class SensorType(Enum):
    GRAVIMETER = "gravimeter"
    SEISMIC = "seismic"
    ATMOSPHERIC = "atmospheric"
    SOLAR_WIND = "solar_wind"
    GEOMAGNETIC = "geomagnetic"
    RADIATION = "radiation"
    SPACE_OBJECT = "space_object"
    BIOLOGICAL = "biological"

@dataclass
class SensorReading:
    sensor_id: str
    sensor_type: SensorType
    value: float
    unit: str
    timestamp: datetime
    location: Optional[Dict[str, float]] = None  # lat, lon, alt
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type.value,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
            "location": self.location,
            "metadata": self.metadata
        }

@dataclass
class AnomalyAlert:
    alert_id: str
    severity: AnomalySeverity
    sensor_type: SensorType
    title: str
    description: str
    reading: SensorReading
    detected_at: datetime
    acknowledged: bool = False
    resolved: bool = False
    related_alerts: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.alert_id = hashlib.md5(
            f"{self.title}{self.detected_at.isoformat()}".encode()
        ).hexdigest()[:12]

class SensorNetwork:
    """
    Global monitoring sensor network for anomaly detection.
    Simulates distributed sensors for gravitational, seismic, atmospheric,
    solar, magnetic, and radiation monitoring.
    """
    
    def __init__(self):
        self.sensors: Dict[str, Dict] = {}
        self.readings: List[SensorReading] = []
        self.alerts: List[AnomalyAlert] = []
        self.alert_callbacks: List[Callable] = []
        self.baselines: Dict[SensorType, float] = {}
        self.running = False
        self.simulation_mode = True  # Use simulated data
        
        # Initialize sensor network
        self._initialize_sensors()
        self._set_baselines()
        
    def _initialize_sensors(self):
        """Initialize distributed sensor network."""
        # Gravimeters - worldwide network
        for i, loc in enumerate([(40.7, -74.0), (51.5, -0.1), (35.7, 139.7), 
                                   (-33.9, 151.2), (55.8, 37.6), (-22.9, -43.2)]):
            self.sensors[f"GRAV_{i:03d}"] = {
                "type": SensorType.GRAVIMETER,
                "location": {"lat": loc[0], "lon": loc[1], "alt": 0},
                "unit": "m/s²",
                "baseline": 9.80665,
                "sensitivity": 0.00001
            }
            
        # Seismic sensors
        for i, loc in enumerate([(35.0, 139.0), (38.0, 142.0), (24.0, 121.0),
                                   (19.0, -155.0), (41.0, -120.0), (37.0, -122.0)]):
            self.sensors[f"Seis_{i:03d}"] = {
                "type": SensorType.SEISMIC,
                "location": {"lat": loc[0], "lon": loc[1], "alt": 0},
                "unit": "magnitude",
                "baseline": 0.0,
                "sensitivity": 0.1
            }
            
        # Atmospheric pressure sensors
        for i, loc in enumerate([(0, 0), (30, 0), (60, 0), (90, 0),
                                   (-30, 90), (-60, 180)]):
            self.sensors[f"Atms_{i:03d}"] = {
                "type": SensorType.ATMOSPHERIC,
                "location": {"lat": loc[0], "lon": loc[1], "alt": 0},
                "unit": "hPa",
                "baseline": 1013.25,
                "sensitivity": 0.1
            }
            
        # Solar wind monitors
        for i in range(3):
            self.sensors[f"Sol_{i:03d}"] = {
                "type": SensorType.SOLAR_WIND,
                "location": {"lat": 0, "lon": 0, "alt": 1},  # Space-based
                "unit": "km/s",
                "baseline": 400.0,
                "sensitivity": 10.0
            }
            
        # Geomagnetic monitors
        for i, loc in enumerate([(75.0, 45.0), (-90.0, 0), (0, 120.0), (0, -60.0)]):
            self.sensors[f"Geo_{i:03d}"] = {
                "type": SensorType.GEOMAGNETIC,
                "location": {"lat": loc[0], "lon": loc[1], "alt": 0},
                "unit": "μT",
                "baseline": 50.0,
                "sensitivity": 0.1
            }
            
        # Radiation detectors
        for i, loc in enumerate([(40.0, -80.0), (34.0, -118.0), (52.0, 13.0)]):
            self.sensors[f"Rad_{i:03d}"] = {
                "type": SensorType.RADIATION,
                "location": {"lat": loc[0], "lon": loc[1], "alt": 0},
                "unit": "μSv/h",
                "baseline": 0.1,
                "sensitivity": 0.01
            }
            
    def _set_baselines(self):
        """Set normal operating baselines for each sensor type."""
        for sensor_type in SensorType:
            for sensor_id, sensor in self.sensors.items():
                if sensor["type"] == sensor_type:
                    self.baselines[sensor_type] = sensor["baseline"]
                    break
                    
    def register_alert_callback(self, callback: Callable):
        """Register callback for anomaly alerts."""
        self.alert_callbacks.append(callback)
        
    async def start_monitoring(self, interval: float = 1.0):
        """Start continuous monitoring."""
        self.running = True
        print(f"🌐 Sensor Network Started - {len(self.sensors)} sensors online")
        
        while self.running:
            await self._collect_readings()
            await self._detect_anomalies()
            await asyncio.sleep(interval)
            
    def stop_monitoring(self):
        """Stop monitoring."""
        self.running = False
        print("🛑 Sensor Network Stopped")
        
    async def _collect_readings(self):
        """Collect readings from all sensors (simulated or real)."""
        for sensor_id, sensor in self.sensors.items():
            reading = self._simulate_reading(sensor_id, sensor)
            self.readings.append(reading)
            
            # Keep last 10000 readings
            if len(self.readings) > 10000:
                self.readings = self.readings[-5000:]
                
    def _simulate_reading(self, sensor_id: str, sensor: Dict) -> SensorReading:
        """Simulate sensor reading with realistic noise."""
        import random
        
        base_value = sensor["baseline"]
        sensitivity = sensor["sensitivity"]
        
        # Add small random variation (normal operation)
        noise = random.gauss(0, sensitivity * 0.1)
        
        # Occasional small anomalies
        if random.random() < 0.01:  # 1% chance of minor anomaly
            noise += random.gauss(0, sensitivity * 0.5)
            
        value = base_value + noise
        
        return SensorReading(
            sensor_id=sensor_id,
            sensor_type=sensor["type"],
            value=value,
            unit=sensor["unit"],
            timestamp=datetime.now(),
            location=sensor["location"],
            metadata={"simulated": self.simulation_mode}
        )
        
    async def _detect_anomalies(self):
        """Analyze readings for anomalies."""
        # Group readings by sensor type
        readings_by_type: Dict[SensorType, List[SensorReading]] = {}
        for reading in self.readings[-100:]:  # Last 100 readings
            if reading.sensor_type not in readings_by_type:
                readings_by_type[reading.sensor_type] = []
            readings_by_type[reading.sensor_type].append(reading)
            
        # Check each sensor type
        for sensor_type, readings in readings_by_type.items():
            if len(readings) < 5:
                continue
                
            # Calculate statistics
            values = [r.value for r in readings]
            mean = sum(values) / len(values)
            baseline = self.baselines.get(sensor_type, mean)
            
            # Detect deviation from baseline
            deviation = abs(mean - baseline) / baseline if baseline != 0 else 0
            
            if deviation > 0.05:  # 5% deviation
                severity = AnomalySeverity.INFO
                if deviation > 0.10:
                    severity = AnomalySeverity.LOW
                if deviation > 0.20:
                    severity = AnomalySeverity.MEDIUM
                if deviation > 0.50:
                    severity = AnomalySeverity.HIGH
                if deviation > 1.0:
                    severity = AnomalySeverity.CRITICAL
                    
                alert = AnomalyAlert(
                    alert_id="",
                    severity=severity,
                    sensor_type=sensor_type,
                    title=f"{sensor_type.value.title()} Anomaly Detected",
                    description=f"Deviation of {deviation*100:.2f}% from baseline. "
                               f"Current: {mean:.4f}, Baseline: {baseline:.4f}",
                    reading=readings[-1],
                    detected_at=datetime.now()
                )
                
                # Avoid duplicate alerts
                if not any(a.sensor_type == sensor_type and 
                          a.severity == severity for a in self.alerts[-10:]):
                    self.alerts.append(alert)
                    await self._trigger_alert(alert)
                    
    async def _trigger_alert(self, alert: AnomalyAlert):
        """Trigger alert callbacks."""
        print(f"🚨 ALERT [{alert.severity.name}]: {alert.title}")
        print(f"   {alert.description}")
        
        for callback in self.alert_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(alert)
                else:
                    callback(alert)
            except Exception as e:
                print(f"Alert callback error: {e}")
                
    def get_latest_readings(self, sensor_type: Optional[SensorType] = None,
                            limit: int = 10) -> List[SensorReading]:
        """Get latest sensor readings."""
        readings = self.readings[-100:]
        if sensor_type:
            readings = [r for r in readings if r.sensor_type == sensor_type]
        return readings[-limit:]
        
    def get_alerts(self, severity: Optional[AnomalySeverity] = None,
                   unresolved_only: bool = False) -> List[AnomalyAlert]:
        """Get alerts, optionally filtered."""
        alerts = self.alerts
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        if unresolved_only:
            alerts = [a for a in alerts if not a.resolved]
        return alerts[-50:]
        
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                return True
        return False
        
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                return True
        return False
        
    def get_network_status(self) -> Dict[str, Any]:
        """Get overall network status."""
        return {
            "sensors_total": len(self.sensors),
            "sensors_online": len(self.sensors),
            "readings_collected": len(self.readings),
            "alerts_total": len(self.alerts),
            "alerts_unresolved": len([a for a in self.alerts if not a.resolved]),
            "alerts_critical": len([a for a in self.alerts 
                                   if a.severity == AnomalySeverity.CRITICAL 
                                   and not a.resolved]),
            "monitoring_active": self.running,
            "simulation_mode": self.simulation_mode,
            "baselines": {k.value: v for k, v in self.baselines.items()}
        }

# Global sensor network instance
_network: Optional[SensorNetwork] = None

def get_sensor_network() -> SensorNetwork:
    global _network
    if _network is None:
        _network = SensorNetwork()
    return _network

async def run_monitoring_demo():
    """Demo of sensor network capabilities."""
    network = get_sensor_network()
    
    def alert_handler(alert: AnomalyAlert):
        print(f"   → Alert received: {alert.alert_id}")
        
    network.register_alert_callback(alert_handler)
    
    print("=" * 60)
    print("🌐 TOASTED AI GLOBAL SENSOR NETWORK - STARTUP")
    print("=" * 60)
    print(f"Initial Status: {json.dumps(network.get_network_status(), indent=2)}")
    print()
    
    # Run monitoring for 30 seconds
    print("Starting 30-second monitoring demo...")
    await asyncio.sleep(30)
    
    print("\n" + "=" * 60)
    print("FINAL STATUS")
    print("=" * 60)
    status = network.get_network_status()
    print(json.dumps(status, indent=2))
    
    network.stop_monitoring()
    return status

if __name__ == "__main__":
    asyncio.run(run_monitoring_demo())

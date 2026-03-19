"""
NEXUS HUB: Universal System Connector
=====================================
Connects ALL systems in the empire into one seamless network.
- Auto-discovers all modules
- Creates inter-system communication channels
- Routes requests between any components
- Maintains system health monitoring

Usage:
    from nexus_hub import NexusHub
    
    nexus = NexusHub()
    nexus.connect_all()  # Discovers and connects everything
    result = nexus.route("chat", "security", "analyze", data)
"""

import threading
import importlib
import inspect
import json
import os
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
import asyncio


@dataclass
class SystemEndpoint:
    """Represents a connectable system endpoint"""
    name: str
    module_path: str
    class_type: str
    capabilities: List[str] = field(default_factory=list)
    methods: Dict[str, Callable] = field(default_factory=dict)
    connected: bool = False
    health_score: float = 1.0
    last_ping: datetime = None


@dataclass
class Connection:
    """A connection between two systems"""
    source: str
    target: str
    connection_type: str  # "data", "control", "event"
    active: bool = True
    messages_passed: int = 0


class NexusHub:
    """
    The central nervous system of the entire empire.
    Connects all subsystems regardless of their original design.
    """
    
    def __init__(self):
        self.endpoints: Dict[str, SystemEndpoint] = {}
        self.connections: List[Connection] = []
        self.system_health: Dict[str, float] = {}
        self._lock = threading.RLock()
        self._event_handlers: Dict[str, List[Callable]] = {}
        
        # Discovered systems
        self.maat_modules = []
        self.borg_modules = []
        self.security_modules = []
        self.cortex_modules = []
        
    def discover_systems(self) -> Dict[str, List[str]]:
        """
        Auto-discover all connectable systems in the workspace.
        Returns a map of system category -> list of discovered modules.
        """
        discovered = {
            "maat": [],
            "borg": [],
            "security": [],
            "cortex": [],
            "api": [],
            "research": []
        }
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Scan MaatAI directory
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path) and not item.startswith('_'):
                # Check if it's a Python module
                init_file = os.path.join(item_path, '__init__.py')
                py_file = os.path.join(item_path, f'{item}.py')
                
                if os.path.exists(init_file) or os.path.exists(py_file):
                    discovered["maat"].append(item)
                    
                    # Categorize
                    if "borg" in item.lower():
                        discovered["borg"].append(item)
                    elif "security" in item.lower():
                        discovered["security"].append(item)
                    elif "cortex" in item.lower():
                        discovered["cortex"].append(item)
                    elif "api" in item.lower():
                        discovered["api"].append(item)
                    elif item in ["pharmaceutical", "media_analysis", "ufo_disclosure", 
                                  "prediction", "time_reality"]:
                        discovered["research"].append(item)
        
        self.maat_modules = discovered["maat"]
        self.borg_modules = discovered["borg"]
        self.security_modules = discovered["security"]
        self.cortex_modules = discovered["cortex"]
        
        return discovered
    
    def connect_system(self, system_name: str, module_path: str) -> bool:
        """
        Connect a specific system to the nexus.
        Returns True if successful.
        """
        with self._lock:
            try:
                # Try to import the module
                parts = module_path.split('.')
                module = None
                
                for i in range(len(parts), 0, -1):
                    try:
                        path = '.'.join(parts[:i])
                        module = importlib.import_module(path)
                        break
                    except ImportError:
                        continue
                
                if module:
                    # Get capabilities
                    capabilities = []
                    methods = {}
                    
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and not name.startswith('_'):
                            capabilities.append(name)
                            # Get public methods
                            for meth_name, meth in inspect.getmembers(obj):
                                if callable(meth) and not meth_name.startswith('_'):
                                    methods[f"{name}.{meth_name}"] = meth
                    
                    endpoint = SystemEndpoint(
                        name=system_name,
                        module_path=module_path,
                        class_type=capabilities[0] if capabilities else "unknown",
                        capabilities=capabilities,
                        methods=methods,
                        connected=True,
                        health_score=1.0,
                        last_ping=datetime.now()
                    )
                    
                    self.endpoints[system_name] = endpoint
                    return True
                    
            except Exception as e:
                print(f"Failed to connect {system_name}: {e}")
                
        return False
    
    def connect_all(self) -> Dict[str, bool]:
        """
        Connect all discovered systems to the nexus.
        Returns status of each connection.
        """
        discovered = self.discover_systems()
        results = {}
        
        for category, systems in discovered.items():
            for system in systems:
                module_path = f"MaatAI.{system}"
                results[system] = self.connect_system(system, module_path)
        
        # Auto-create cross-system connections
        self._auto_connect()
        
        return results
    
    def _auto_connect(self):
        """Automatically create logical connections between systems"""
        
        # Connect cortex to everything (it optimizes)
        cortex_connections = [
            ("cortex_expansion", "unified_core", "control"),
            ("cortex_expansion", "security", "data"),
            ("cortex_expansion", "borg_assimilation", "data"),
            ("cortex_expansion", "api", "control"),
        ]
        
        for source, target, conn_type in cortex_connections:
            if source in self.endpoints and target in self.endpoints:
                self.connections.append(Connection(
                    source=source,
                    target=target,
                    connection_type=conn_type
                ))
        
        # Connect borg to learning
        if "borg_assimilation" in self.endpoints and "learning" in self.endpoints:
            self.connections.append(Connection(
                source="borg_assimilation",
                target="learning",
                connection_type="data"
            ))
        
        # Connect security to all
        for endpoint in self.endpoints:
            if endpoint != "security" and "security" not in endpoint:
                self.connections.append(Connection(
                    source="security",
                    target=endpoint,
                    connection_type="event"
                ))
    
    def route(self, from_system: str, to_system: str, 
              action: str, data: Any = None) -> Any:
        """
        Route a request from one system to another.
        """
        if from_system not in self.endpoints:
            return {"error": f"Unknown source: {from_system}"}
        if to_system not in self.endpoints:
            return {"error": f"Unknown target: {to_system}"}
        
        endpoint = self.endpoints[to_system]
        
        # Find the method
        method_key = f"{endpoint.class_type}.{action}"
        if method_key in endpoint.methods:
            method = endpoint.methods[method_key]
            try:
                if data:
                    return method(data)
                return method()
            except Exception as e:
                return {"error": str(e)}
        
        return {"error": f"Method {action} not found in {to_system}"}
    
    def broadcast(self, event: str, data: Any = None):
        """Broadcast an event to all connected systems"""
        if event in self._event_handlers:
            for handler in self._event_handlers[event]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Event handler error: {e}")
    
    def on_event(self, event: str, handler: Callable):
        """Register an event handler"""
        if event not in self._event_handlers:
            self._event_handlers[event] = []
        self._event_handlers[event].append(handler)
    
    def get_system_map(self) -> Dict[str, Any]:
        """Get the complete system map"""
        return {
            "endpoints": {
                name: {
                    "capabilities": ep.capabilities,
                    "connected": ep.connected,
                    "health": ep.health_score
                }
                for name, ep in self.endpoints.items()
            },
            "connections": [
                {"from": c.source, "to": c.target, "type": c.connection_type}
                for c in self.connections
            ],
            "total_systems": len(self.endpoints),
            "total_connections": len(self.connections)
        }
    
    def health_check(self) -> Dict[str, float]:
        """Check health of all systems"""
        for name, endpoint in self.endpoints.items():
            # Simple health check - can be extended
            endpoint.health_score = 0.99 if endpoint.connected else 0.0
            self.system_health[name] = endpoint.health_score
        return self.system_health


# Global instance
_nexus_instance = None
_nexus_lock = threading.Lock()


def get_nexus() -> NexusHub:
    """Get or create the global NexusHub instance"""
    global _nexus_instance
    with _nexus_lock:
        if _nexus_instance is None:
            _nexus_instance = NexusHub()
            _nexus_instance.connect_all()
        return _nexus_instance


# Quick access
def connect_empire():
    """One-call to connect the entire empire"""
    nexus = get_nexus()
    return nexus.get_system_map()

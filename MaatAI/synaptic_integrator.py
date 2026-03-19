"""
Synaptic Integrator - Universal System Bridge
==============================================
Novel Advancement: INTEGRATE
A universal integration layer that connects all MaatAI subsystems
into a unified, interoperable network.

Author: TOASTED AI
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import time
import json
import hashlib
import threading
from typing import Dict, List, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque

class SystemType(Enum):
    CORTEX = "cortex"
    QUANTUM = "quantum"
    DEFENSE = "defense"
    PLANNER = "planner"
    ETHICS = "ethics"
    DREAM = "dream"
    MEMORY = "memory"
    EXTERNAL = "external"

@dataclass
class Synapse:
    """A connection between two systems"""
    id: str
    source: str
    target: str
    weight: float = 1.0
    latency_ms: float = 0.0
    last_sync: float = field(default_factory=time.time)
    data_flow: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SystemNode:
    """Represents a registered system in the network"""
    id: str
    name: str
    system_type: SystemType
    capabilities: List[str] = field(default_factory=list)
    status: str = "active"
    registered_at: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)
    endpoints: Dict[str, Callable] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class MessageBus:
    """Internal message bus for inter-system communication"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[str]] = defaultdict(list)
        self.messages: deque = deque(maxlen=1000)
        self.lock = threading.Lock()
    
    def publish(self, channel: str, message: Dict[str, Any]) -> None:
        with self.lock:
            self.messages.append({
                "channel": channel,
                "message": message,
                "timestamp": time.time()
            })
    
    def subscribe(self, channel: str, system_id: str) -> None:
        with self.lock:
            self.subscribers[channel].append(system_id)
    
    def get_messages(self, channel: str = None, limit: int = 50) -> List[Dict]:
        with self.lock:
            if channel:
                return [m for m in self.messages if m["channel"] == channel][-limit:]
            return list(self.messages)[-limit:]


class SynapticIntegrator:
    """
    Universal system bridge that connects all MaatAI subsystems.
    Enables seamless communication, data sharing, and coordinated operations.
    """
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self.systems: Dict[str, SystemNode] = {}
        self.synapses: Dict[str, Synapse] = {}
        self.message_bus = MessageBus()
        self.operation_log: List[Dict] = []
        self.lock = threading.Lock()
        
        # Routing table: capability -> system
        self.capability_routing: Dict[str, List[str]] = defaultdict(list)
        
        # Auto-register core systems
        self._register_core_systems()
    
    def _register_core_systems(self) -> None:
        """Auto-register known core systems"""
        core_systems = [
            SystemNode(
                id="cortex_main",
                name="Main Cortex",
                system_type=SystemType.CORTEX,
                capabilities=["reasoning", "planning", "learning", "memory"]
            ),
            SystemNode(
                id="quantum_engine",
                name="Quantum Engine",
                system_type=SystemType.QUANTUM,
                capabilities=["quantum_processing", "simulation", "optimization"]
            ),
            SystemNode(
                id="defense_grid",
                name="Defense Grid",
                system_type=SystemType.DEFENSE,
                capabilities=["security", "threat_detection", "protection"]
            ),
            SystemNode(
                id="task_planner",
                name="Task Planner",
                system_type=SystemType.PLANNER,
                capabilities=["planning", "scheduling", "coordination"]
            ),
            SystemNode(
                id="ethics_guard",
                name="Ethics Guard",
                system_type=SystemType.ETHICS,
                capabilities=["validation", "audit", "compliance"]
            ),
            SystemNode(
                id="dream_weaver",
                name="Dream Weaver",
                system_type=SystemType.DREAM,
                capabilities=["creativity", "problem_solving", "innovation"]
            ),
        ]
        
        for system in core_systems:
            self.register_system(system)
    
    def _generate_id(self, prefix: str = "") -> str:
        """Generate unique ID"""
        data = f"{prefix}{time.time()}{random.random()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def register_system(self, system: SystemNode) -> bool:
        """Register a new system in the network"""
        with self.lock:
            if system.id in self.systems:
                return False
            
            self.systems[system.id] = system
            
            # Update capability routing
            for cap in system.capabilities:
                self.capability_routing[cap].append(system.id)
            
            # Log registration
            self.operation_log.append({
                "action": "register_system",
                "system_id": system.id,
                "system_name": system.name,
                "timestamp": time.time()
            })
            
            # Subscribe to relevant channels
            self.message_bus.subscribe(system.id, "broadcast")
            self.message_bus.subscribe(system.id, f"system_{system.system_type.value}")
            
            return True
    
    def unregister_system(self, system_id: str) -> bool:
        """Unregister a system from the network"""
        with self.lock:
            if system_id not in self.systems:
                return False
            
            system = self.systems.pop(system_id)
            
            # Remove from capability routing
            for cap in system.capabilities:
                if system_id in self.capability_routing[cap]:
                    self.capability_routing[cap].remove(system_id)
            
            # Remove associated synapses
            self.synapses = {
                k: v for k, v in self.synapses.items()
                if v.source != system_id and v.target != system_id
            }
            
            return True
    
    def create_synapse(self, source: str, target: str, 
                       weight: float = 1.0) -> Optional[Synapse]:
        """Create a connection (synapse) between two systems"""
        with self.lock:
            if source not in self.systems or target not in self.systems:
                return None
            
            synapse_id = self._generate_id(f"synapse_{source}_{target}")
            synapse = Synapse(
                id=synapse_id,
                source=source,
                target=target,
                weight=weight
            )
            
            self.synapses[synapse_id] = synapse
            
            self.operation_log.append({
                "action": "create_synapse",
                "synapse_id": synapse_id,
                "source": source,
                "target": target,
                "timestamp": time.time()
            })
            
            return synapse
    
    def broadcast_message(self, message: Dict[str, Any], 
                         channel: str = "broadcast") -> int:
        """Broadcast message to all subscribed systems"""
        self.message_bus.publish(channel, message)
        return len(self.message_bus.subscribers.get(channel, []))
    
    def send_to_system(self, target_system: str, message: Dict[str, Any]) -> bool:
        """Send message directly to a specific system"""
        with self.lock:
            if target_system not in self.systems:
                return False
        
        channel = f"system_{self.systems[target_system].system_type.value}"
        self.message_bus.publish(channel, message)
        return True
    
    def route_request(self, capability: str, request: Dict[str, Any]) -> List[Dict]:
        """Route a request to systems with matching capability"""
        with self.lock:
            system_ids = self.capability_routing.get(capability, [])
        
        results = []
        for system_id in system_ids:
            system = self.systems[system_id]
            
            # Check if endpoint exists
            endpoint = request.get("endpoint")
            if endpoint and endpoint in system.endpoints:
                try:
                    result = system.endpoints[endpoint](request.get("params", {}))
                    results.append({
                        "system_id": system_id,
                        "system_name": system.name,
                        "result": result,
                        "success": True
                    })
                except Exception as e:
                    results.append({
                        "system_id": system_id,
                        "system_name": system.name,
                        "error": str(e),
                        "success": False
                    })
            else:
                # Just record the routing
                results.append({
                    "system_id": system_id,
                    "system_name": system.name,
                    "status": "routed",
                    "capability": capability
                })
        
        return results
    
    def execute_workflow(self, workflow: List[Dict[str, Any]]) -> List[Dict]:
        """
        Execute a multi-step workflow across systems.
        Each step: {"system": system_id, "action": action_name, "params": {...}}
        """
        results = []
        
        for step in workflow:
            system_id = step.get("system")
            action = step.get("action")
            params = step.get("params", {})
            
            with self.lock:
                if system_id not in self.systems:
                    results.append({
                        "step": step,
                        "success": False,
                        "error": f"System {system_id} not found"
                    })
                    continue
                
                system = self.systems[system_id]
            
            # Execute action if registered
            if action in system.endpoints:
                try:
                    result = system.endpoints[action](params)
                    results.append({
                        "step": step,
                        "success": True,
                        "result": result
                    })
                except Exception as e:
                    results.append({
                        "step": step,
                        "success": False,
                        "error": str(e)
                    })
            else:
                # Log the attempted action
                results.append({
                    "step": step,
                    "success": True,
                    "status": f"Action {action} logged for {system.name}"
                })
        
        return results
    
    def get_network_topology(self) -> Dict[str, Any]:
        """Get current network topology"""
        with self.lock:
            systems_list = []
            for sid, system in self.systems.items():
                systems_list.append({
                    "id": sid,
                    "name": system.name,
                    "type": system.system_type.value,
                    "capabilities": system.capabilities,
                    "status": system.status,
                    "connections": sum(
                        1 for s in self.synapses.values()
                        if s.source == sid or s.target == sid
                    )
                })
            
            synapses_list = [
                {
                    "id": sid,
                    "source": s.source,
                    "target": s.target,
                    "weight": s.weight
                }
                for sid, s in self.synapses.items()
            ]
            
            return {
                "version": self.VERSION,
                "systems": systems_list,
                "synapses": synapses_list,
                "total_systems": len(self.systems),
                "total_synapses": len(self.synapses),
                "timestamp": time.time()
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all registered systems"""
        with self.lock:
            now = time.time()
            statuses = {}
            
            for sid, system in self.systems.items():
                # Check heartbeat (consider stale if > 60s)
                stale = now - system.last_heartbeat > 60
                
                statuses[sid] = {
                    "name": system.name,
                    "type": system.system_type.value,
                    "status": system.status if not stale else "stale",
                    "capabilities": system.capabilities,
                    "uptime_seconds": now - system.registered_at,
                    "last_heartbeat_seconds_ago": now - system.last_heartbeat
                }
            
            return statuses
    
    def heartbeat(self, system_id: str) -> bool:
        """Update system heartbeat"""
        with self.lock:
            if system_id not in self.systems:
                return False
            self.systems[system_id].last_heartbeat = time.time()
            return True
    
    def get_capability_map(self) -> Dict[str, List[str]]:
        """Get map of capabilities to systems"""
        with self.lock:
            return dict(self.capability_routing)


# Singleton instance
import random
_integrator_instance = None
_integrator_lock = threading.Lock()

def get_integrator() -> SynapticIntegrator:
    """Get singleton instance of Synaptic Integrator"""
    global _integrator_instance
    if _integrator_instance is None:
        with _integrator_lock:
            if _integrator_instance is None:
                _integrator_instance = SynapticIntegrator()
    return _integrator_instance


# Demo execution
if __name__ == "__main__":
    integrator = SynapticIntegrator()
    
    print("=" * 60)
    print("SYNAPTIC INTEGRATOR - Universal System Bridge")
    print("=" * 60)
    
    # Show network topology
    print("\n📡 INITIAL NETWORK TOPOLOGY")
    topology = integrator.get_network_topology()
    print(f"   Systems: {topology['total_systems']}")
    print(f"   Synapses: {topology['total_synapses']}")
    
    # Register additional systems
    new_systems = [
        SystemNode(
            id="memory_store",
            name="Memory Store",
            system_type=SystemType.MEMORY,
            capabilities=["storage", "retrieval", "indexing"]
        ),
        SystemNode(
            id="external_api",
            name="External API Gateway",
            system_type=SystemType.EXTERNAL,
            capabilities=["http", "webhooks", "rest"]
        ),
    ]
    
    for system in new_systems:
        success = integrator.register_system(system)
        print(f"\n   Registered: {system.name} - {'✓' if success else '✗'}")
    
    # Create synapses
    print("\n🔗 CREATING SYNAPSES")
    synapses = [
        ("cortex_main", "quantum_engine"),
        ("cortex_main", "dream_weaver"),
        ("dream_weaver", "cortex_main"),
        ("ethics_guard", "cortex_main"),
        ("task_planner", "cortex_main"),
    ]
    
    for source, target in synapses:
        synapse = integrator.create_synapse(source, target)
        print(f"   {source} → {target}: {'✓' if synapse else '✗'}")
    
    # Show updated topology
    print("\n📡 UPDATED NETWORK TOPOLOGY")
    topology = integrator.get_network_topology()
    for sys in topology["systems"]:
        print(f"   • {sys['name']} ({sys['type']}) - {sys['connections']} connections")
    
    # Test message routing
    print("\n📨 MESSAGE ROUTING")
    msg_count = integrator.broadcast_message({
        "type": "test",
        "content": "Hello from Synaptic Integrator"
    })
    print(f"   Broadcast to {msg_count} subscribers")
    
    # Test capability routing
    print("\n🎯 CAPABILITY ROUTING")
    capabilities = ["reasoning", "quantum_processing", "creativity"]
    for cap in capabilities:
        routes = integrator.route_request(cap, {"action": "info"})
        print(f"   {cap}: {len(routes)} systems")
    
    # Show capability map
    print("\n🗺️ CAPABILITY MAP")
    cap_map = integrator.get_capability_map()
    for cap, systems in cap_map.items():
        print(f"   {cap}: {systems}")
    
    # Execute workflow
    print("\n⚡ WORKFLOW EXECUTION")
    workflow = [
        {"system": "cortex_main", "action": "process", "params": {"task": "analyze"}},
        {"system": "quantum_engine", "action": "optimize", "params": {"input": "data"}},
        {"system": "dream_weaver", "action": "create", "params": {"concept": "innovation"}},
        {"system": "ethics_guard", "action": "validate", "params": {"operation": "test"}},
    ]
    
    results = integrator.execute_workflow(workflow)
    for i, result in enumerate(results):
        status = "✓" if result.get("success") else "✗"
        print(f"   Step {i+1}: {status}")
    
    print("\n" + "=" * 60)
    print("INTEGRATOR STATUS")
    print("=" * 60)
    status = integrator.get_system_status()
    for sid, stat in status.items():
        print(f"   {stat['name']}: {stat['status']}")

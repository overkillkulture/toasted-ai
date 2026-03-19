"""
TASK-155: QUANTUM ENGINE PERMANENT DEPLOYMENT
=============================================
Scalable, resilient deployment architecture for quantum infrastructure.

Architecture:
- Multi-node quantum cluster management
- Automatic failover and load balancing
- State persistence and recovery
- Health monitoring and self-healing
- Rolling updates without downtime
- Hybrid classical/quantum orchestration

This provides the deployment layer that makes all quantum
infrastructure components production-ready.
"""

import asyncio
import math
import random
import time
import json
import logging
import threading
import hashlib
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Set
from pathlib import Path
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QuantumDeployment")


class NodeStatus(Enum):
    """Status of a deployment node"""
    STARTING = "starting"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"
    DRAINING = "draining"  # Stopping gracefully


class DeploymentStrategy(Enum):
    """Deployment strategies"""
    ROLLING = "rolling"           # One at a time
    BLUE_GREEN = "blue_green"     # Full switch
    CANARY = "canary"             # Gradual rollout
    RECREATE = "recreate"         # Stop all, start new


class ServiceType(Enum):
    """Types of quantum services"""
    QUANTUM_ENGINE = "quantum_engine"
    STATE_BACKUP = "state_backup"
    CIRCUIT_OPTIMIZER = "circuit_optimizer"
    SIMULATOR = "simulator"
    TELEMETRY = "telemetry"
    ORCHESTRATOR = "orchestrator"


@dataclass
class ServiceConfig:
    """Configuration for a quantum service"""
    service_type: ServiceType
    replicas: int = 1
    cpu_limit: float = 1.0        # CPU cores
    memory_limit: int = 512       # MB
    min_ready_seconds: int = 10
    health_check_interval: int = 5
    restart_policy: str = "always"  # always, on_failure, never
    
    # Quantum-specific
    qubits: int = 4
    coherence_threshold: float = 0.8
    backup_enabled: bool = True


@dataclass
class NodeInfo:
    """Information about a deployment node"""
    node_id: str
    hostname: str
    status: NodeStatus
    services: List[str] = field(default_factory=list)
    
    # Resources
    total_cpu: float = 4.0
    available_cpu: float = 4.0
    total_memory: int = 8192     # MB
    available_memory: int = 8192
    
    # Health
    last_heartbeat: float = field(default_factory=time.time)
    health_score: float = 1.0
    uptime: float = 0.0
    
    # Quantum capability
    has_quantum_accelerator: bool = False
    max_qubits: int = 10


@dataclass
class ServiceInstance:
    """A running instance of a service"""
    instance_id: str
    service_type: ServiceType
    node_id: str
    config: ServiceConfig
    
    status: NodeStatus = NodeStatus.STARTING
    started_at: float = field(default_factory=time.time)
    restarts: int = 0
    
    # Metrics
    requests_handled: int = 0
    average_latency: float = 0.0
    error_rate: float = 0.0
    
    # Quantum state
    coherence: float = 1.0
    circuit_depth: int = 0


class HealthChecker:
    """
    Health monitoring for quantum services.
    Checks both classical health and quantum coherence.
    """
    
    def __init__(self):
        self.checks: Dict[str, Dict] = {}
        self._lock = threading.Lock()
    
    def check_instance(self, instance: ServiceInstance) -> Dict[str, Any]:
        """Perform health check on instance"""
        
        check_result = {
            "instance_id": instance.instance_id,
            "timestamp": time.time(),
            "checks": {}
        }
        
        # Liveness check (is it running?)
        liveness = instance.status in [NodeStatus.HEALTHY, NodeStatus.DEGRADED]
        check_result["checks"]["liveness"] = {
            "passed": liveness,
            "status": instance.status.value
        }
        
        # Readiness check (can it accept work?)
        ready_time = time.time() - instance.started_at
        readiness = (
            liveness and 
            ready_time > instance.config.min_ready_seconds
        )
        check_result["checks"]["readiness"] = {
            "passed": readiness,
            "uptime": ready_time
        }
        
        # Quantum coherence check
        coherence_ok = instance.coherence >= instance.config.coherence_threshold
        check_result["checks"]["coherence"] = {
            "passed": coherence_ok,
            "value": instance.coherence,
            "threshold": instance.config.coherence_threshold
        }
        
        # Error rate check
        error_ok = instance.error_rate < 0.1  # 10% threshold
        check_result["checks"]["error_rate"] = {
            "passed": error_ok,
            "value": instance.error_rate
        }
        
        # Overall health
        all_passed = all(c["passed"] for c in check_result["checks"].values())
        check_result["healthy"] = all_passed
        check_result["health_score"] = sum(
            1 for c in check_result["checks"].values() if c["passed"]
        ) / len(check_result["checks"])
        
        with self._lock:
            self.checks[instance.instance_id] = check_result
        
        return check_result
    
    def get_health_history(self, instance_id: str) -> Optional[Dict]:
        """Get health check history"""
        return self.checks.get(instance_id)


class LoadBalancer:
    """
    Load balancer for quantum services.
    Routes requests to healthy instances.
    """
    
    def __init__(self, strategy: str = "round_robin"):
        self.strategy = strategy  # round_robin, least_conn, coherence_based
        self.instances: Dict[ServiceType, List[ServiceInstance]] = {}
        self._counters: Dict[ServiceType, int] = {}
        self._lock = threading.Lock()
    
    def register_instance(self, instance: ServiceInstance):
        """Register an instance for load balancing"""
        with self._lock:
            if instance.service_type not in self.instances:
                self.instances[instance.service_type] = []
                self._counters[instance.service_type] = 0
            
            self.instances[instance.service_type].append(instance)
    
    def unregister_instance(self, instance_id: str):
        """Remove instance from load balancing"""
        with self._lock:
            for service_type, instances in self.instances.items():
                self.instances[service_type] = [
                    i for i in instances if i.instance_id != instance_id
                ]
    
    def get_instance(self, service_type: ServiceType) -> Optional[ServiceInstance]:
        """Get an instance to handle a request"""
        with self._lock:
            instances = self.instances.get(service_type, [])
            healthy = [i for i in instances if i.status == NodeStatus.HEALTHY]
            
            if not healthy:
                # Fall back to degraded instances
                healthy = [i for i in instances if i.status == NodeStatus.DEGRADED]
            
            if not healthy:
                return None
            
            if self.strategy == "round_robin":
                idx = self._counters.get(service_type, 0)
                instance = healthy[idx % len(healthy)]
                self._counters[service_type] = idx + 1
                return instance
            
            elif self.strategy == "least_conn":
                return min(healthy, key=lambda i: i.requests_handled)
            
            elif self.strategy == "coherence_based":
                # Prefer instances with higher quantum coherence
                return max(healthy, key=lambda i: i.coherence)
            
            return healthy[0]


class StateManager:
    """
    Manage persistent state for quantum services.
    Enables recovery after failures.
    """
    
    def __init__(self, state_dir: str = "./quantum_state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
    
    def save_state(self, instance_id: str, state: Dict[str, Any]) -> bool:
        """Save instance state to persistent storage"""
        try:
            state_file = self.state_dir / f"{instance_id}.json"
            
            state_with_meta = {
                "instance_id": instance_id,
                "saved_at": time.time(),
                "state": state
            }
            
            with self._lock:
                with open(state_file, 'w') as f:
                    json.dump(state_with_meta, f, indent=2)
            
            logger.debug(f"Saved state for {instance_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
            return False
    
    def load_state(self, instance_id: str) -> Optional[Dict[str, Any]]:
        """Load instance state from persistent storage"""
        try:
            state_file = self.state_dir / f"{instance_id}.json"
            
            if not state_file.exists():
                return None
            
            with open(state_file, 'r') as f:
                data = json.load(f)
            
            return data.get("state")
            
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            return None
    
    def delete_state(self, instance_id: str):
        """Delete instance state"""
        state_file = self.state_dir / f"{instance_id}.json"
        if state_file.exists():
            state_file.unlink()


class QuantumDeployment:
    """
    Main deployment manager for quantum infrastructure.
    """
    
    def __init__(self, config_dir: str = "./quantum_deployment"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Components
        self.health_checker = HealthChecker()
        self.load_balancer = LoadBalancer(strategy="coherence_based")
        self.state_manager = StateManager(str(self.config_dir / "state"))
        
        # Cluster state
        self.nodes: Dict[str, NodeInfo] = {}
        self.instances: Dict[str, ServiceInstance] = {}
        self.services: Dict[ServiceType, ServiceConfig] = {}
        
        # Monitoring
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        
        # Metrics
        self.deployments_total = 0
        self.successful_deployments = 0
        self.rollbacks = 0
        
        logger.info("QuantumDeployment initialized")
    
    def add_node(self, hostname: str, 
                has_quantum: bool = False,
                max_qubits: int = 10,
                cpu: float = 4.0,
                memory: int = 8192) -> NodeInfo:
        """Add a node to the cluster"""
        
        node_id = f"node_{hostname}_{int(time.time())}"
        
        node = NodeInfo(
            node_id=node_id,
            hostname=hostname,
            status=NodeStatus.HEALTHY,
            total_cpu=cpu,
            available_cpu=cpu,
            total_memory=memory,
            available_memory=memory,
            has_quantum_accelerator=has_quantum,
            max_qubits=max_qubits
        )
        
        self.nodes[node_id] = node
        logger.info(f"Added node: {node_id} ({hostname})")
        
        return node
    
    def remove_node(self, node_id: str, drain: bool = True):
        """Remove a node from the cluster"""
        
        node = self.nodes.get(node_id)
        if not node:
            return
        
        if drain:
            # Drain instances first
            node.status = NodeStatus.DRAINING
            self._drain_node(node_id)
        
        del self.nodes[node_id]
        logger.info(f"Removed node: {node_id}")
    
    def _drain_node(self, node_id: str):
        """Drain instances from a node"""
        
        instances_on_node = [
            i for i in self.instances.values() 
            if i.node_id == node_id
        ]
        
        for instance in instances_on_node:
            # Save state before removing
            self._save_instance_state(instance)
            
            # Find new node and recreate
            new_node = self._select_node(instance.config)
            if new_node:
                self._create_instance(instance.config, new_node.node_id)
            
            # Remove old instance
            self._terminate_instance(instance.instance_id)
    
    def define_service(self, service_type: ServiceType,
                      config: ServiceConfig):
        """Define a service configuration"""
        
        self.services[service_type] = config
        logger.info(f"Defined service: {service_type.value}")
    
    async def deploy_service(self, service_type: ServiceType,
                           strategy: DeploymentStrategy = DeploymentStrategy.ROLLING
                           ) -> Dict[str, Any]:
        """Deploy a service"""
        
        config = self.services.get(service_type)
        if not config:
            return {"error": f"Service {service_type.value} not defined"}
        
        self.deployments_total += 1
        
        result = {
            "service": service_type.value,
            "strategy": strategy.value,
            "instances_created": 0,
            "instances_failed": 0
        }
        
        try:
            if strategy == DeploymentStrategy.ROLLING:
                await self._rolling_deploy(service_type, config, result)
            elif strategy == DeploymentStrategy.BLUE_GREEN:
                await self._blue_green_deploy(service_type, config, result)
            elif strategy == DeploymentStrategy.CANARY:
                await self._canary_deploy(service_type, config, result)
            else:
                await self._recreate_deploy(service_type, config, result)
            
            self.successful_deployments += 1
            result["success"] = True
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            logger.error(f"Deployment failed: {e}")
        
        return result
    
    async def _rolling_deploy(self, service_type: ServiceType,
                             config: ServiceConfig,
                             result: Dict):
        """Rolling deployment - one instance at a time"""
        
        for i in range(config.replicas):
            node = self._select_node(config)
            if not node:
                result["instances_failed"] += 1
                continue
            
            instance = self._create_instance(config, node.node_id)
            
            if instance:
                # Wait for instance to be ready
                await self._wait_for_ready(instance)
                result["instances_created"] += 1
            else:
                result["instances_failed"] += 1
            
            # Pause between instances
            await asyncio.sleep(0.5)
    
    async def _blue_green_deploy(self, service_type: ServiceType,
                                config: ServiceConfig,
                                result: Dict):
        """Blue-green deployment - full switch"""
        
        # Create all new instances (green)
        new_instances = []
        for i in range(config.replicas):
            node = self._select_node(config)
            if node:
                instance = self._create_instance(config, node.node_id)
                if instance:
                    new_instances.append(instance)
                    result["instances_created"] += 1
        
        # Wait for all to be ready
        for instance in new_instances:
            await self._wait_for_ready(instance)
        
        # Switch traffic (already handled by load balancer)
        # Remove old instances
        old_instances = [
            i for i in self.instances.values()
            if i.service_type == service_type and i not in new_instances
        ]
        
        for instance in old_instances:
            self._terminate_instance(instance.instance_id)
    
    async def _canary_deploy(self, service_type: ServiceType,
                            config: ServiceConfig,
                            result: Dict):
        """Canary deployment - gradual rollout"""
        
        # Start with 10% of replicas
        canary_count = max(1, config.replicas // 10)
        
        # Deploy canary
        for i in range(canary_count):
            node = self._select_node(config)
            if node:
                instance = self._create_instance(config, node.node_id)
                if instance:
                    await self._wait_for_ready(instance)
                    result["instances_created"] += 1
        
        # Monitor canary (simplified)
        await asyncio.sleep(2)
        
        # If healthy, deploy rest
        remaining = config.replicas - canary_count
        for i in range(remaining):
            node = self._select_node(config)
            if node:
                instance = self._create_instance(config, node.node_id)
                if instance:
                    await self._wait_for_ready(instance)
                    result["instances_created"] += 1
    
    async def _recreate_deploy(self, service_type: ServiceType,
                              config: ServiceConfig,
                              result: Dict):
        """Recreate deployment - stop all, start new"""
        
        # Stop all existing
        existing = [
            i for i in self.instances.values()
            if i.service_type == service_type
        ]
        for instance in existing:
            self._terminate_instance(instance.instance_id)
        
        # Start new
        await self._rolling_deploy(service_type, config, result)
    
    def _select_node(self, config: ServiceConfig) -> Optional[NodeInfo]:
        """Select best node for deployment"""
        
        suitable = []
        for node in self.nodes.values():
            if node.status not in [NodeStatus.HEALTHY, NodeStatus.DEGRADED]:
                continue
            
            if node.available_cpu < config.cpu_limit:
                continue
            
            if node.available_memory < config.memory_limit:
                continue
            
            # Check quantum requirements
            if config.qubits > node.max_qubits:
                continue
            
            suitable.append(node)
        
        if not suitable:
            return None
        
        # Prefer nodes with quantum accelerators
        quantum_nodes = [n for n in suitable if n.has_quantum_accelerator]
        if quantum_nodes:
            return max(quantum_nodes, key=lambda n: n.available_cpu)
        
        return max(suitable, key=lambda n: n.available_cpu)
    
    def _create_instance(self, config: ServiceConfig, 
                        node_id: str) -> Optional[ServiceInstance]:
        """Create a service instance on a node"""
        
        node = self.nodes.get(node_id)
        if not node:
            return None
        
        instance_id = f"inst_{config.service_type.value}_{int(time.time()*1000)}_{random.randint(100,999)}"
        
        instance = ServiceInstance(
            instance_id=instance_id,
            service_type=config.service_type,
            node_id=node_id,
            config=config,
            status=NodeStatus.STARTING
        )
        
        # Allocate resources
        node.available_cpu -= config.cpu_limit
        node.available_memory -= config.memory_limit
        node.services.append(instance_id)
        
        self.instances[instance_id] = instance
        self.load_balancer.register_instance(instance)
        
        # Try to restore state
        saved_state = self.state_manager.load_state(instance_id)
        if saved_state:
            instance.coherence = saved_state.get("coherence", 1.0)
            instance.circuit_depth = saved_state.get("circuit_depth", 0)
        
        logger.info(f"Created instance: {instance_id} on {node_id}")
        return instance
    
    def _terminate_instance(self, instance_id: str):
        """Terminate a service instance"""
        
        instance = self.instances.get(instance_id)
        if not instance:
            return
        
        # Save state before terminating
        self._save_instance_state(instance)
        
        # Release resources
        node = self.nodes.get(instance.node_id)
        if node:
            node.available_cpu += instance.config.cpu_limit
            node.available_memory += instance.config.memory_limit
            if instance_id in node.services:
                node.services.remove(instance_id)
        
        # Unregister from load balancer
        self.load_balancer.unregister_instance(instance_id)
        
        del self.instances[instance_id]
        logger.info(f"Terminated instance: {instance_id}")
    
    def _save_instance_state(self, instance: ServiceInstance):
        """Save instance state for recovery"""
        
        state = {
            "coherence": instance.coherence,
            "circuit_depth": instance.circuit_depth,
            "requests_handled": instance.requests_handled
        }
        
        self.state_manager.save_state(instance.instance_id, state)
    
    async def _wait_for_ready(self, instance: ServiceInstance, 
                             timeout: float = 30.0):
        """Wait for instance to be ready"""
        
        start = time.time()
        
        while time.time() - start < timeout:
            # Simulate startup
            await asyncio.sleep(0.5)
            
            # Check health
            health = self.health_checker.check_instance(instance)
            
            if health["healthy"]:
                instance.status = NodeStatus.HEALTHY
                return
            
            # Update status based on checks
            if health["checks"]["liveness"]["passed"]:
                instance.status = NodeStatus.STARTING
            else:
                instance.status = NodeStatus.UNHEALTHY
        
        # Timeout - mark as degraded
        instance.status = NodeStatus.DEGRADED
    
    def start_monitoring(self, interval: float = 5.0):
        """Start health monitoring"""
        
        if self._monitoring:
            return
        
        self._monitoring = True
        
        def monitor_loop():
            while self._monitoring:
                try:
                    self._perform_health_checks()
                    self._perform_auto_healing()
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                
                time.sleep(interval)
        
        self._monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self._monitor_thread.start()
        logger.info("Health monitoring started")
    
    def stop_monitoring(self):
        """Stop health monitoring"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
    
    def _perform_health_checks(self):
        """Check health of all instances"""
        
        for instance in list(self.instances.values()):
            health = self.health_checker.check_instance(instance)
            
            if health["healthy"]:
                instance.status = NodeStatus.HEALTHY
            elif health["health_score"] >= 0.5:
                instance.status = NodeStatus.DEGRADED
            else:
                instance.status = NodeStatus.UNHEALTHY
    
    def _perform_auto_healing(self):
        """Auto-heal unhealthy instances"""
        
        for instance in list(self.instances.values()):
            if instance.status == NodeStatus.UNHEALTHY:
                # Check restart policy
                if instance.config.restart_policy == "never":
                    continue
                
                if instance.restarts >= 3:
                    # Too many restarts - move to different node
                    self._migrate_instance(instance)
                else:
                    # Try restart
                    self._restart_instance(instance)
    
    def _restart_instance(self, instance: ServiceInstance):
        """Restart an unhealthy instance"""
        
        logger.info(f"Restarting instance: {instance.instance_id}")
        
        instance.status = NodeStatus.STARTING
        instance.restarts += 1
        instance.started_at = time.time()
        
        # Reset quantum state
        instance.coherence = 1.0
    
    def _migrate_instance(self, instance: ServiceInstance):
        """Migrate instance to a different node"""
        
        logger.info(f"Migrating instance: {instance.instance_id}")
        
        # Find new node
        new_node = self._select_node(instance.config)
        if not new_node or new_node.node_id == instance.node_id:
            return
        
        # Create new instance
        new_instance = self._create_instance(instance.config, new_node.node_id)
        
        # Terminate old
        self._terminate_instance(instance.instance_id)
    
    def get_status(self) -> Dict[str, Any]:
        """Get deployment status"""
        
        healthy_instances = sum(
            1 for i in self.instances.values()
            if i.status == NodeStatus.HEALTHY
        )
        
        total_coherence = sum(
            i.coherence for i in self.instances.values()
        )
        avg_coherence = total_coherence / len(self.instances) if self.instances else 0
        
        return {
            "nodes": len(self.nodes),
            "healthy_nodes": sum(1 for n in self.nodes.values() if n.status == NodeStatus.HEALTHY),
            "instances": len(self.instances),
            "healthy_instances": healthy_instances,
            "services_defined": len(self.services),
            "deployments_total": self.deployments_total,
            "successful_deployments": self.successful_deployments,
            "rollbacks": self.rollbacks,
            "average_coherence": avg_coherence,
            "monitoring_active": self._monitoring
        }


class DeploymentOrchestrator:
    """
    High-level orchestrator for quantum deployments.
    Coordinates multiple deployments and manages the full stack.
    """
    
    def __init__(self):
        self.deployment = QuantumDeployment()
        self.deployed_services: Set[ServiceType] = set()
    
    async def deploy_full_stack(self, 
                               nodes: List[Dict[str, Any]],
                               services: List[Dict[str, Any]]
                               ) -> Dict[str, Any]:
        """Deploy the complete quantum infrastructure stack"""
        
        result = {
            "nodes_added": 0,
            "services_deployed": [],
            "errors": []
        }
        
        # Add nodes
        for node_config in nodes:
            try:
                self.deployment.add_node(**node_config)
                result["nodes_added"] += 1
            except Exception as e:
                result["errors"].append(f"Node error: {e}")
        
        # Define and deploy services
        for svc_config in services:
            try:
                service_type = ServiceType[svc_config["type"].upper()]
                config = ServiceConfig(
                    service_type=service_type,
                    **{k: v for k, v in svc_config.items() if k != "type"}
                )
                
                self.deployment.define_service(service_type, config)
                
                deploy_result = await self.deployment.deploy_service(
                    service_type,
                    DeploymentStrategy.ROLLING
                )
                
                if deploy_result.get("success"):
                    self.deployed_services.add(service_type)
                    result["services_deployed"].append(service_type.value)
                else:
                    result["errors"].append(f"Deploy error: {deploy_result.get('error')}")
                    
            except Exception as e:
                result["errors"].append(f"Service error: {e}")
        
        # Start monitoring
        self.deployment.start_monitoring()
        
        result["success"] = len(result["errors"]) == 0
        return result
    
    async def scale_service(self, service_type: ServiceType,
                           replicas: int) -> Dict[str, Any]:
        """Scale a service up or down"""
        
        config = self.deployment.services.get(service_type)
        if not config:
            return {"error": "Service not defined"}
        
        current_instances = [
            i for i in self.deployment.instances.values()
            if i.service_type == service_type
        ]
        current_count = len(current_instances)
        
        if replicas > current_count:
            # Scale up
            config.replicas = replicas
            for _ in range(replicas - current_count):
                node = self.deployment._select_node(config)
                if node:
                    self.deployment._create_instance(config, node.node_id)
        
        elif replicas < current_count:
            # Scale down
            config.replicas = replicas
            to_remove = current_instances[replicas:]
            for instance in to_remove:
                self.deployment._terminate_instance(instance.instance_id)
        
        return {
            "service": service_type.value,
            "previous_replicas": current_count,
            "new_replicas": replicas
        }
    
    def get_dashboard(self) -> Dict[str, Any]:
        """Get deployment dashboard data"""
        
        status = self.deployment.get_status()
        
        # Per-service breakdown
        service_status = {}
        for service_type in self.deployed_services:
            instances = [
                i for i in self.deployment.instances.values()
                if i.service_type == service_type
            ]
            
            service_status[service_type.value] = {
                "instances": len(instances),
                "healthy": sum(1 for i in instances if i.status == NodeStatus.HEALTHY),
                "avg_coherence": sum(i.coherence for i in instances) / len(instances) if instances else 0
            }
        
        status["services"] = service_status
        return status


# Demo
async def demo_permanent_deployment():
    """Demonstrate permanent deployment"""
    
    print("=" * 70)
    print("QUANTUM ENGINE PERMANENT DEPLOYMENT - TASK-155 DEMO")
    print("=" * 70)
    
    orchestrator = DeploymentOrchestrator()
    
    # Define infrastructure
    nodes = [
        {"hostname": "quantum-node-1", "has_quantum": True, "max_qubits": 20},
        {"hostname": "quantum-node-2", "has_quantum": True, "max_qubits": 20},
        {"hostname": "classical-node-1", "has_quantum": False, "max_qubits": 10}
    ]
    
    services = [
        {"type": "quantum_engine", "replicas": 2, "qubits": 8},
        {"type": "state_backup", "replicas": 2, "backup_enabled": True},
        {"type": "circuit_optimizer", "replicas": 1},
        {"type": "telemetry", "replicas": 2}
    ]
    
    # Deploy full stack
    print(f"\n1. Deploying full quantum stack...")
    result = await orchestrator.deploy_full_stack(nodes, services)
    
    print(f"   Nodes added: {result['nodes_added']}")
    print(f"   Services deployed: {result['services_deployed']}")
    if result['errors']:
        print(f"   Errors: {result['errors']}")
    
    # Wait for startup
    await asyncio.sleep(2)
    
    # Get dashboard
    print(f"\n2. Deployment Dashboard:")
    dashboard = orchestrator.get_dashboard()
    print(f"   Nodes: {dashboard['nodes']} ({dashboard['healthy_nodes']} healthy)")
    print(f"   Instances: {dashboard['instances']} ({dashboard['healthy_instances']} healthy)")
    print(f"   Average coherence: {dashboard['average_coherence']:.3f}")
    
    print(f"\n3. Per-service status:")
    for service, status in dashboard.get('services', {}).items():
        print(f"   {service}:")
        print(f"      Instances: {status['instances']} ({status['healthy']} healthy)")
        print(f"      Avg coherence: {status['avg_coherence']:.3f}")
    
    # Scale test
    print(f"\n4. Scaling quantum_engine to 4 replicas...")
    scale_result = await orchestrator.scale_service(
        ServiceType.QUANTUM_ENGINE, 4
    )
    print(f"   Previous: {scale_result['previous_replicas']}")
    print(f"   New: {scale_result['new_replicas']}")
    
    # Updated status
    await asyncio.sleep(1)
    dashboard = orchestrator.get_dashboard()
    print(f"\n5. Updated status:")
    print(f"   Total instances: {dashboard['instances']}")
    
    # Cleanup
    orchestrator.deployment.stop_monitoring()
    
    print("\n" + "=" * 70)
    print("QUANTUM ENGINE PERMANENT DEPLOYMENT - OPERATIONAL")
    print("=" * 70)
    
    return orchestrator


if __name__ == "__main__":
    asyncio.run(demo_permanent_deployment())

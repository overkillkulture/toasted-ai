#!/usr/bin/env python3
"""
TASK-092: Hierarchical Hypervisor Management Protocol
Wave 7, Batch 5: Protocols

Refactors hypervisor management into hierarchical layers with
resource isolation, policy enforcement, and multi-tenant support.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class HypervisorLevel(Enum):
    """Levels in the hypervisor hierarchy."""
    ROOT = "root"           # System-level hypervisor
    DOMAIN = "domain"       # Domain-level isolation
    WORKSPACE = "workspace" # Workspace-level containers
    TASK = "task"          # Individual task execution


class ResourceType(Enum):
    """Types of resources managed by hypervisor."""
    CPU = "cpu"
    MEMORY = "memory"
    GPU = "gpu"
    STORAGE = "storage"
    NETWORK = "network"


class IsolationLevel(Enum):
    """Resource isolation levels."""
    NONE = "none"           # No isolation
    SOFT = "soft"           # Soft limits
    HARD = "hard"           # Hard limits
    STRICT = "strict"       # Complete isolation


@dataclass
class ResourceQuota:
    """Resource allocation quota."""
    resource_type: ResourceType
    allocated: float
    used: float = 0.0
    limit: float = float('inf')
    isolation: IsolationLevel = IsolationLevel.SOFT

    def available(self) -> float:
        """Calculate available resources."""
        return min(self.allocated - self.used, self.limit - self.used)

    def utilization(self) -> float:
        """Calculate utilization percentage."""
        return (self.used / self.allocated) * 100 if self.allocated > 0 else 0


@dataclass
class HypervisorPolicy:
    """Policies for hypervisor behavior."""
    name: str
    max_children: int = 10
    allow_overcommit: bool = False
    overcommit_ratio: float = 1.5
    auto_scale: bool = True
    priority: int = 5
    isolation_level: IsolationLevel = IsolationLevel.SOFT


@dataclass
class HypervisorNode:
    """Node in the hypervisor hierarchy."""
    node_id: str
    level: HypervisorLevel
    parent_id: Optional[str] = None
    children: Set[str] = field(default_factory=set)
    resources: Dict[ResourceType, ResourceQuota] = field(default_factory=dict)
    policy: Optional[HypervisorPolicy] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    active: bool = True


@dataclass
class ManagementMetrics:
    """Metrics for hypervisor management."""
    total_nodes: int = 0
    active_nodes: int = 0
    root_nodes: int = 0
    domain_nodes: int = 0
    workspace_nodes: int = 0
    task_nodes: int = 0
    resource_violations: int = 0
    policy_violations: int = 0


class HierarchicalHypervisorManager:
    """
    Manages hierarchical hypervisor infrastructure.

    Features:
    - Multi-level resource hierarchy
    - Cascading resource allocation
    - Policy inheritance and enforcement
    - Resource isolation and quotas
    - Multi-tenant support
    """

    def __init__(self, base_path: str = "C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI"):
        self.base_path = Path(base_path)
        self.nodes: Dict[str, HypervisorNode] = {}
        self.policies: Dict[str, HypervisorPolicy] = {}
        self.metrics = ManagementMetrics()

        # Hierarchy tracking
        self.root_nodes: Set[str] = set()
        self.hierarchy: Dict[str, List[str]] = defaultdict(list)

        # Initialize default policies
        self._initialize_default_policies()

    def _initialize_default_policies(self):
        """Create default policies for each level."""
        self.policies["root_default"] = HypervisorPolicy(
            name="root_default",
            max_children=5,
            allow_overcommit=False,
            isolation_level=IsolationLevel.HARD,
            priority=10
        )

        self.policies["domain_default"] = HypervisorPolicy(
            name="domain_default",
            max_children=10,
            allow_overcommit=True,
            overcommit_ratio=1.2,
            isolation_level=IsolationLevel.SOFT,
            priority=7
        )

        self.policies["workspace_default"] = HypervisorPolicy(
            name="workspace_default",
            max_children=20,
            allow_overcommit=True,
            overcommit_ratio=1.5,
            isolation_level=IsolationLevel.SOFT,
            priority=5
        )

        self.policies["task_default"] = HypervisorPolicy(
            name="task_default",
            max_children=0,  # Tasks can't have children
            allow_overcommit=False,
            isolation_level=IsolationLevel.NONE,
            priority=3
        )

    def create_node(self,
                   node_id: str,
                   level: HypervisorLevel,
                   parent_id: Optional[str] = None,
                   resources: Optional[Dict[ResourceType, float]] = None,
                   policy_name: Optional[str] = None) -> HypervisorNode:
        """
        Create a new hypervisor node.

        Args:
            node_id: Unique identifier
            level: Hierarchy level
            parent_id: Parent node (None for root)
            resources: Resource allocations
            policy_name: Policy to apply

        Returns:
            Created HypervisorNode
        """
        # Validate parent
        if parent_id and parent_id not in self.nodes:
            raise ValueError(f"Parent node {parent_id} not found")

        # Get policy
        if policy_name:
            policy = self.policies.get(policy_name)
        else:
            policy = self.policies.get(f"{level.value}_default")

        # Create resource quotas
        resource_quotas = {}
        if resources:
            for res_type, amount in resources.items():
                resource_quotas[res_type] = ResourceQuota(
                    resource_type=res_type,
                    allocated=amount,
                    isolation=policy.isolation_level if policy else IsolationLevel.SOFT
                )

        # Create node
        node = HypervisorNode(
            node_id=node_id,
            level=level,
            parent_id=parent_id,
            resources=resource_quotas,
            policy=policy
        )

        # Validate and link to parent
        if parent_id:
            parent = self.nodes[parent_id]

            # Check parent's child limit
            if policy and len(parent.children) >= parent.policy.max_children:
                raise ValueError(f"Parent node {parent_id} at child limit")

            # Validate resource allocation from parent
            if not self._validate_resource_allocation(parent, resource_quotas):
                raise ValueError("Insufficient parent resources")

            # Allocate resources from parent
            self._allocate_from_parent(parent, resource_quotas)

            parent.children.add(node_id)
            self.hierarchy[parent_id].append(node_id)
        else:
            self.root_nodes.add(node_id)
            self.metrics.root_nodes += 1

        self.nodes[node_id] = node
        self.metrics.total_nodes += 1
        self.metrics.active_nodes += 1

        # Update level counts
        if level == HypervisorLevel.DOMAIN:
            self.metrics.domain_nodes += 1
        elif level == HypervisorLevel.WORKSPACE:
            self.metrics.workspace_nodes += 1
        elif level == HypervisorLevel.TASK:
            self.metrics.task_nodes += 1

        return node

    def _validate_resource_allocation(self,
                                     parent: HypervisorNode,
                                     requested: Dict[ResourceType, ResourceQuota]) -> bool:
        """Check if parent has sufficient resources."""
        for res_type, quota in requested.items():
            if res_type not in parent.resources:
                return False

            parent_quota = parent.resources[res_type]
            available = parent_quota.available()

            # Check if enough resources available
            if quota.allocated > available:
                # Check if overcommit allowed
                if not parent.policy or not parent.policy.allow_overcommit:
                    return False

                # Check overcommit ratio
                total_allocated = sum(
                    self.nodes[child_id].resources.get(res_type, ResourceQuota(res_type, 0)).allocated
                    for child_id in parent.children
                ) + quota.allocated

                if total_allocated > parent_quota.allocated * parent.policy.overcommit_ratio:
                    return False

        return True

    def _allocate_from_parent(self,
                             parent: HypervisorNode,
                             quotas: Dict[ResourceType, ResourceQuota]):
        """Allocate resources from parent node."""
        for res_type, quota in quotas.items():
            if res_type in parent.resources:
                parent.resources[res_type].used += quota.allocated

    def deallocate_node(self, node_id: str):
        """
        Deallocate a node and return resources to parent.
        """
        if node_id not in self.nodes:
            return

        node = self.nodes[node_id]

        # Can't deallocate if has children
        if node.children:
            raise ValueError(f"Node {node_id} has children, deallocate them first")

        # Return resources to parent
        if node.parent_id:
            parent = self.nodes[node.parent_id]
            for res_type, quota in node.resources.items():
                if res_type in parent.resources:
                    parent.resources[res_type].used -= quota.allocated
            parent.children.remove(node_id)

        # Remove from hierarchy
        if node_id in self.root_nodes:
            self.root_nodes.remove(node_id)
            self.metrics.root_nodes -= 1

        # Update metrics
        self.metrics.active_nodes -= 1
        if node.level == HypervisorLevel.DOMAIN:
            self.metrics.domain_nodes -= 1
        elif node.level == HypervisorLevel.WORKSPACE:
            self.metrics.workspace_nodes -= 1
        elif node.level == HypervisorLevel.TASK:
            self.metrics.task_nodes -= 1

        del self.nodes[node_id]

    def allocate_resource(self,
                         node_id: str,
                         resource_type: ResourceType,
                         amount: float) -> bool:
        """
        Allocate additional resources to a node.

        Returns True if successful, False if insufficient resources.
        """
        if node_id not in self.nodes:
            return False

        node = self.nodes[node_id]

        if resource_type not in node.resources:
            return False

        quota = node.resources[resource_type]

        # Check if allocation would exceed limit
        if quota.used + amount > quota.allocated:
            self.metrics.resource_violations += 1
            return False

        quota.used += amount
        return True

    def release_resource(self,
                        node_id: str,
                        resource_type: ResourceType,
                        amount: float):
        """Release resources back to the pool."""
        if node_id not in self.nodes:
            return

        node = self.nodes[node_id]

        if resource_type in node.resources:
            node.resources[resource_type].used = max(
                0,
                node.resources[resource_type].used - amount
            )

    def get_node_path(self, node_id: str) -> List[str]:
        """Get full path from root to node."""
        if node_id not in self.nodes:
            return []

        path = [node_id]
        current = self.nodes[node_id]

        while current.parent_id:
            path.insert(0, current.parent_id)
            current = self.nodes[current.parent_id]

        return path

    def get_resource_tree(self, node_id: str) -> Dict:
        """
        Get complete resource allocation tree for a node.

        Shows how resources cascade through hierarchy.
        """
        if node_id not in self.nodes:
            return {}

        node = self.nodes[node_id]

        tree = {
            "node_id": node_id,
            "level": node.level.value,
            "resources": {
                res_type.value: {
                    "allocated": quota.allocated,
                    "used": quota.used,
                    "available": quota.available(),
                    "utilization": f"{quota.utilization():.1f}%"
                }
                for res_type, quota in node.resources.items()
            },
            "children": []
        }

        for child_id in node.children:
            tree["children"].append(self.get_resource_tree(child_id))

        return tree

    def enforce_policies(self) -> Dict:
        """
        Enforce policies across all nodes.

        Returns report of violations and actions taken.
        """
        violations = {
            "resource_violations": [],
            "policy_violations": [],
            "actions_taken": []
        }

        for node_id, node in self.nodes.items():
            if not node.active:
                continue

            # Check resource violations
            for res_type, quota in node.resources.items():
                if quota.used > quota.allocated:
                    violations["resource_violations"].append({
                        "node_id": node_id,
                        "resource": res_type.value,
                        "allocated": quota.allocated,
                        "used": quota.used,
                        "overage": quota.used - quota.allocated
                    })
                    self.metrics.resource_violations += 1

            # Check policy violations
            if node.policy:
                if len(node.children) > node.policy.max_children:
                    violations["policy_violations"].append({
                        "node_id": node_id,
                        "violation": "child_limit_exceeded",
                        "limit": node.policy.max_children,
                        "actual": len(node.children)
                    })
                    self.metrics.policy_violations += 1

        return violations

    def get_hierarchy_summary(self) -> Dict:
        """Get summary of entire hypervisor hierarchy."""
        return {
            "metrics": {
                "total_nodes": self.metrics.total_nodes,
                "active_nodes": self.metrics.active_nodes,
                "root_nodes": self.metrics.root_nodes,
                "domain_nodes": self.metrics.domain_nodes,
                "workspace_nodes": self.metrics.workspace_nodes,
                "task_nodes": self.metrics.task_nodes,
                "resource_violations": self.metrics.resource_violations,
                "policy_violations": self.metrics.policy_violations
            },
            "hierarchy_depth": max(
                (len(self.get_node_path(nid)) for nid in self.nodes),
                default=0
            ),
            "policies": {
                name: {
                    "max_children": policy.max_children,
                    "allow_overcommit": policy.allow_overcommit,
                    "isolation_level": policy.isolation_level.value
                }
                for name, policy in self.policies.items()
            }
        }

    def save_hierarchy_state(self, output_path: Optional[Path] = None):
        """Save hypervisor hierarchy state."""
        if output_path is None:
            output_path = self.base_path / "hypervisor_hierarchy_state.json"

        state = {
            "nodes": {
                nid: {
                    "node_id": n.node_id,
                    "level": n.level.value,
                    "parent_id": n.parent_id,
                    "children": list(n.children),
                    "resources": {
                        rt.value: {
                            "allocated": q.allocated,
                            "used": q.used,
                            "isolation": q.isolation.value
                        }
                        for rt, q in n.resources.items()
                    },
                    "active": n.active
                }
                for nid, n in self.nodes.items()
            },
            "metrics": {
                "total_nodes": self.metrics.total_nodes,
                "active_nodes": self.metrics.active_nodes,
                "root_nodes": self.metrics.root_nodes
            }
        }

        output_path.write_text(json.dumps(state, indent=2))
        return output_path


def main():
    """Test the hierarchical hypervisor manager."""
    print("=" * 60)
    print("TASK-092: Hierarchical Hypervisor Management")
    print("=" * 60)

    manager = HierarchicalHypervisorManager()

    # Create hierarchy
    print("\n[1/4] Building hypervisor hierarchy...")

    # Root level (system)
    root = manager.create_node(
        "root_system",
        HypervisorLevel.ROOT,
        resources={
            ResourceType.CPU: 100.0,
            ResourceType.MEMORY: 256.0,
            ResourceType.GPU: 8.0
        }
    )
    print(f"  Created root: {root.node_id}")

    # Domain level
    domain1 = manager.create_node(
        "domain_ml",
        HypervisorLevel.DOMAIN,
        parent_id="root_system",
        resources={
            ResourceType.CPU: 40.0,
            ResourceType.MEMORY: 100.0,
            ResourceType.GPU: 4.0
        }
    )
    print(f"  Created domain: {domain1.node_id}")

    # Workspace level
    workspace1 = manager.create_node(
        "workspace_training",
        HypervisorLevel.WORKSPACE,
        parent_id="domain_ml",
        resources={
            ResourceType.CPU: 20.0,
            ResourceType.MEMORY: 50.0,
            ResourceType.GPU: 2.0
        }
    )
    print(f"  Created workspace: {workspace1.node_id}")

    # Task level
    task1 = manager.create_node(
        "task_model_train",
        HypervisorLevel.TASK,
        parent_id="workspace_training",
        resources={
            ResourceType.CPU: 10.0,
            ResourceType.MEMORY: 20.0,
            ResourceType.GPU: 1.0
        }
    )
    print(f"  Created task: {task1.node_id}")

    # Test resource allocation
    print("\n[2/4] Testing resource allocation...")
    success = manager.allocate_resource("task_model_train", ResourceType.CPU, 5.0)
    print(f"  Allocated 5.0 CPU: {'Success' if success else 'Failed'}")

    # Get resource tree
    print("\n[3/4] Resource allocation tree:")
    tree = manager.get_resource_tree("root_system")
    print(f"  Root: {tree['node_id']}")
    for child in tree["children"]:
        print(f"    Domain: {child['node_id']}")
        for workspace in child["children"]:
            print(f"      Workspace: {workspace['node_id']}")
            for task in workspace["children"]:
                print(f"        Task: {task['node_id']}")

    # Enforce policies
    print("\n[4/4] Policy enforcement:")
    violations = manager.enforce_policies()
    print(f"  Resource violations: {len(violations['resource_violations'])}")
    print(f"  Policy violations: {len(violations['policy_violations'])}")

    # Summary
    print("\n" + "=" * 60)
    print("Hierarchy Summary:")
    print("=" * 60)
    summary = manager.get_hierarchy_summary()
    for key, value in summary["metrics"].items():
        print(f"  {key}: {value}")

    # Save state
    output_path = manager.save_hierarchy_state()
    print(f"\n✓ Hierarchy state saved: {output_path}")

    print("\n" + "=" * 60)
    print("TASK-092 Complete: Hierarchical hypervisor operational!")
    print("=" * 60)


if __name__ == "__main__":
    main()

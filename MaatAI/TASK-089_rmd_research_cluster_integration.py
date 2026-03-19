#!/usr/bin/env python3
"""
TASK-089: RMD Research Cluster Integration Protocol
Wave 7, Batch 5: Protocols

Integrates Research, Memory, and Development clusters into a unified
knowledge processing pipeline with cross-cluster query optimization.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from collections import defaultdict


class ClusterType(Enum):
    """Types of knowledge clusters."""
    RESEARCH = "research"
    MEMORY = "memory"
    DEVELOPMENT = "development"


@dataclass
class KnowledgeNode:
    """Represents a piece of knowledge in the cluster."""
    node_id: str
    cluster_type: ClusterType
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    connections: Set[str] = field(default_factory=set)
    access_count: int = 0
    last_accessed: float = 0.0


@dataclass
class ClusterBridge:
    """Bridge between two clusters for knowledge transfer."""
    bridge_id: str
    source_cluster: ClusterType
    target_cluster: ClusterType
    transfer_rules: List[str] = field(default_factory=list)
    bandwidth: float = 1.0  # Transfer speed multiplier


@dataclass
class IntegrationMetrics:
    """Metrics for cluster integration."""
    total_nodes: int = 0
    research_nodes: int = 0
    memory_nodes: int = 0
    development_nodes: int = 0
    cross_cluster_queries: int = 0
    bridge_transfers: int = 0
    avg_query_time: float = 0.0


class RMDResearchClusterIntegrator:
    """
    Integrates Research, Memory, and Development clusters.

    Features:
    - Unified query interface across all clusters
    - Intelligent knowledge routing
    - Cross-cluster relationship tracking
    - Automated knowledge migration
    """

    def __init__(self, base_path: str = "C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI"):
        self.base_path = Path(base_path)
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.bridges: Dict[str, ClusterBridge] = {}
        self.metrics = IntegrationMetrics()

        # Cluster-specific storage
        self.clusters: Dict[ClusterType, Set[str]] = {
            ClusterType.RESEARCH: set(),
            ClusterType.MEMORY: set(),
            ClusterType.DEVELOPMENT: set()
        }

        # Initialize bridges
        self._initialize_bridges()

    def _initialize_bridges(self):
        """Create bridges between clusters."""
        # Research -> Memory (findings become memories)
        self.bridges["r2m"] = ClusterBridge(
            bridge_id="r2m",
            source_cluster=ClusterType.RESEARCH,
            target_cluster=ClusterType.MEMORY,
            transfer_rules=["validated_findings", "significant_discoveries"],
            bandwidth=0.8
        )

        # Memory -> Development (memories inform development)
        self.bridges["m2d"] = ClusterBridge(
            bridge_id="m2d",
            source_cluster=ClusterType.MEMORY,
            target_cluster=ClusterType.DEVELOPMENT,
            transfer_rules=["technical_patterns", "best_practices"],
            bandwidth=1.0
        )

        # Development -> Research (implementations inspire research)
        self.bridges["d2r"] = ClusterBridge(
            bridge_id="d2r",
            source_cluster=ClusterType.DEVELOPMENT,
            target_cluster=ClusterType.RESEARCH,
            transfer_rules=["novel_approaches", "performance_insights"],
            bandwidth=0.6
        )

        # Research -> Development (direct application)
        self.bridges["r2d"] = ClusterBridge(
            bridge_id="r2d",
            source_cluster=ClusterType.RESEARCH,
            target_cluster=ClusterType.DEVELOPMENT,
            transfer_rules=["ready_to_implement", "proven_algorithms"],
            bandwidth=0.9
        )

    def add_node(self,
                 node_id: str,
                 cluster_type: ClusterType,
                 content: str,
                 metadata: Optional[Dict] = None) -> KnowledgeNode:
        """
        Add a knowledge node to a cluster.

        Args:
            node_id: Unique identifier
            cluster_type: Which cluster this belongs to
            content: The knowledge content
            metadata: Optional metadata

        Returns:
            Created KnowledgeNode
        """
        node = KnowledgeNode(
            node_id=node_id,
            cluster_type=cluster_type,
            content=content,
            metadata=metadata or {}
        )

        self.nodes[node_id] = node
        self.clusters[cluster_type].add(node_id)

        # Update metrics
        self.metrics.total_nodes += 1
        if cluster_type == ClusterType.RESEARCH:
            self.metrics.research_nodes += 1
        elif cluster_type == ClusterType.MEMORY:
            self.metrics.memory_nodes += 1
        elif cluster_type == ClusterType.DEVELOPMENT:
            self.metrics.development_nodes += 1

        return node

    def connect_nodes(self, source_id: str, target_id: str):
        """Create bidirectional connection between nodes."""
        if source_id in self.nodes and target_id in self.nodes:
            self.nodes[source_id].connections.add(target_id)
            self.nodes[target_id].connections.add(source_id)

    async def query_unified(self,
                           query: str,
                           clusters: Optional[List[ClusterType]] = None) -> Dict:
        """
        Query across multiple clusters with unified interface.

        Args:
            query: Search query
            clusters: Which clusters to search (None = all)

        Returns:
            Unified query results
        """
        start_time = time.time()
        self.metrics.cross_cluster_queries += 1

        if clusters is None:
            clusters = list(ClusterType)

        results = {
            "query": query,
            "clusters_searched": [c.value for c in clusters],
            "results": []
        }

        # Search each cluster
        for cluster_type in clusters:
            cluster_results = await self._search_cluster(
                query,
                cluster_type
            )
            results["results"].extend(cluster_results)

        # Rank results by relevance and cross-cluster connections
        results["results"] = self._rank_results(results["results"])

        # Update metrics
        query_time = time.time() - start_time
        total_queries = self.metrics.cross_cluster_queries
        self.metrics.avg_query_time = (
            (self.metrics.avg_query_time * (total_queries - 1) + query_time)
            / total_queries
        )

        results["query_time"] = query_time
        results["result_count"] = len(results["results"])

        return results

    async def _search_cluster(self,
                             query: str,
                             cluster_type: ClusterType) -> List[Dict]:
        """Search within a specific cluster."""
        results = []
        query_lower = query.lower()

        for node_id in self.clusters[cluster_type]:
            node = self.nodes[node_id]

            # Simple relevance scoring
            content_lower = node.content.lower()
            if query_lower in content_lower:
                relevance = content_lower.count(query_lower) / len(content_lower)

                # Update access tracking
                node.access_count += 1
                node.last_accessed = time.time()

                results.append({
                    "node_id": node_id,
                    "cluster": cluster_type.value,
                    "content": node.content,
                    "relevance": relevance,
                    "connections": len(node.connections),
                    "metadata": node.metadata
                })

        return results

    def _rank_results(self, results: List[Dict]) -> List[Dict]:
        """Rank results by relevance and cross-cluster importance."""
        # Score based on:
        # - Direct relevance
        # - Number of cross-cluster connections
        # - Access frequency

        for result in results:
            node_id = result["node_id"]
            node = self.nodes[node_id]

            # Count cross-cluster connections
            cross_cluster_connections = sum(
                1 for conn_id in node.connections
                if self.nodes[conn_id].cluster_type != node.cluster_type
            )

            # Calculate composite score
            result["score"] = (
                result["relevance"] * 100 +
                cross_cluster_connections * 10 +
                node.access_count * 0.1
            )

        # Sort by score
        return sorted(results, key=lambda r: r["score"], reverse=True)

    async def transfer_knowledge(self,
                                 node_id: str,
                                 target_cluster: ClusterType) -> Optional[KnowledgeNode]:
        """
        Transfer knowledge from one cluster to another via bridge.

        Args:
            node_id: Node to transfer
            target_cluster: Destination cluster

        Returns:
            New node in target cluster, or None if transfer not allowed
        """
        if node_id not in self.nodes:
            return None

        source_node = self.nodes[node_id]
        source_cluster = source_node.cluster_type

        if source_cluster == target_cluster:
            return None  # Already in target cluster

        # Find appropriate bridge
        bridge_id = f"{source_cluster.value[0]}2{target_cluster.value[0]}"
        bridge = self.bridges.get(bridge_id)

        if not bridge:
            return None  # No bridge exists

        # Check transfer rules
        transfer_allowed = False
        for rule in bridge.transfer_rules:
            if rule in source_node.metadata.get("tags", []):
                transfer_allowed = True
                break

        if not transfer_allowed:
            return None

        # Simulate transfer time based on bandwidth
        transfer_time = 0.1 / bridge.bandwidth
        await asyncio.sleep(transfer_time)

        # Create new node in target cluster
        new_node_id = f"{node_id}_in_{target_cluster.value}"
        new_node = self.add_node(
            node_id=new_node_id,
            cluster_type=target_cluster,
            content=source_node.content,
            metadata={
                **source_node.metadata,
                "transferred_from": node_id,
                "transfer_time": time.time()
            }
        )

        # Connect to source node
        self.connect_nodes(node_id, new_node_id)

        self.metrics.bridge_transfers += 1

        return new_node

    def analyze_cluster_integration(self) -> Dict:
        """
        Analyze the integration between clusters.

        Returns:
            Integration analysis results
        """
        # Calculate cross-cluster connection density
        cross_cluster_connections = 0
        total_connections = 0

        for node in self.nodes.values():
            total_connections += len(node.connections)

            for conn_id in node.connections:
                conn_node = self.nodes[conn_id]
                if conn_node.cluster_type != node.cluster_type:
                    cross_cluster_connections += 1

        integration_density = (
            cross_cluster_connections / max(total_connections, 1)
        ) * 100

        # Identify most connected nodes per cluster
        most_connected = {}
        for cluster_type in ClusterType:
            cluster_nodes = [
                self.nodes[nid] for nid in self.clusters[cluster_type]
            ]
            if cluster_nodes:
                most_connected[cluster_type.value] = max(
                    cluster_nodes,
                    key=lambda n: len(n.connections)
                ).node_id

        return {
            "total_nodes": self.metrics.total_nodes,
            "cluster_distribution": {
                "research": self.metrics.research_nodes,
                "memory": self.metrics.memory_nodes,
                "development": self.metrics.development_nodes
            },
            "integration_density": f"{integration_density:.1f}%",
            "cross_cluster_connections": cross_cluster_connections,
            "total_connections": total_connections,
            "most_connected_per_cluster": most_connected,
            "bridge_transfers": self.metrics.bridge_transfers,
            "cross_cluster_queries": self.metrics.cross_cluster_queries,
            "avg_query_time": f"{self.metrics.avg_query_time:.3f}s"
        }

    def save_integration_state(self, output_path: Optional[Path] = None):
        """Save cluster integration state."""
        if output_path is None:
            output_path = self.base_path / "rmd_cluster_integration_state.json"

        state = {
            "nodes": {
                nid: {
                    "node_id": n.node_id,
                    "cluster_type": n.cluster_type.value,
                    "content": n.content,
                    "metadata": n.metadata,
                    "connections": list(n.connections),
                    "access_count": n.access_count
                }
                for nid, n in self.nodes.items()
            },
            "metrics": {
                "total_nodes": self.metrics.total_nodes,
                "research_nodes": self.metrics.research_nodes,
                "memory_nodes": self.metrics.memory_nodes,
                "development_nodes": self.metrics.development_nodes,
                "cross_cluster_queries": self.metrics.cross_cluster_queries,
                "bridge_transfers": self.metrics.bridge_transfers
            }
        }

        output_path.write_text(json.dumps(state, indent=2))
        return output_path


def main():
    """Test the RMD cluster integration."""
    print("=" * 60)
    print("TASK-089: RMD Research Cluster Integration")
    print("=" * 60)

    integrator = RMDResearchClusterIntegrator()

    # Add test nodes
    print("\n[1/4] Creating knowledge nodes...")

    # Research nodes
    integrator.add_node(
        "r001",
        ClusterType.RESEARCH,
        "Neural network optimization techniques",
        {"tags": ["validated_findings", "ready_to_implement"]}
    )
    integrator.add_node(
        "r002",
        ClusterType.RESEARCH,
        "Quantum computing applications in AI",
        {"tags": ["significant_discoveries"]}
    )

    # Memory nodes
    integrator.add_node(
        "m001",
        ClusterType.MEMORY,
        "Best practices for distributed systems",
        {"tags": ["technical_patterns"]}
    )
    integrator.add_node(
        "m002",
        ClusterType.MEMORY,
        "Historical performance optimizations",
        {"tags": ["best_practices"]}
    )

    # Development nodes
    integrator.add_node(
        "d001",
        ClusterType.DEVELOPMENT,
        "Implementation of async processing pipeline",
        {"tags": ["novel_approaches"]}
    )
    integrator.add_node(
        "d002",
        ClusterType.DEVELOPMENT,
        "High-performance caching system",
        {"tags": ["performance_insights"]}
    )

    # Create connections
    print("[2/4] Establishing cross-cluster connections...")
    integrator.connect_nodes("r001", "d001")
    integrator.connect_nodes("r001", "m002")
    integrator.connect_nodes("m001", "d001")
    integrator.connect_nodes("d002", "m002")

    # Test unified query
    print("[3/4] Testing unified query...")
    async def test_query():
        results = await integrator.query_unified("optimization")
        print(f"  Found {results['result_count']} results across clusters")
        for result in results["results"][:3]:
            print(f"    [{result['cluster']}] {result['node_id']}: "
                  f"score={result['score']:.1f}")

    asyncio.run(test_query())

    # Test knowledge transfer
    print("[4/4] Testing knowledge transfer...")
    async def test_transfer():
        new_node = await integrator.transfer_knowledge("r001", ClusterType.DEVELOPMENT)
        if new_node:
            print(f"  ✓ Transferred r001 -> {new_node.node_id}")

    asyncio.run(test_transfer())

    # Analyze integration
    print("\n" + "=" * 60)
    print("Integration Analysis:")
    print("=" * 60)
    analysis = integrator.analyze_cluster_integration()
    for key, value in analysis.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")

    # Save state
    output_path = integrator.save_integration_state()
    print(f"\n✓ Integration state saved: {output_path}")

    print("\n" + "=" * 60)
    print("TASK-089 Complete: RMD clusters integrated!")
    print("=" * 60)


if __name__ == "__main__":
    main()

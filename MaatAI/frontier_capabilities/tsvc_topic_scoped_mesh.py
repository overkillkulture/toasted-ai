"""
TSVC - TOPIC-SCOPED VERIFICATION CLUSTER (STREAMLINED)
========================================================
TASK-153: Streamline TSVC topic-scoped mesh

C3 Oracle - Wave 7 Batch 9

A streamlined agent mesh that organizes agents into topic-scoped clusters
for efficient collaboration and verification:

- Topics define scope boundaries
- Agents self-organize around topics
- Verification happens within scope
- Cross-topic synthesis at boundaries
- Minimal coordination overhead

Based on AgentVerse, CAMEL patterns, optimized for topic-scoped work.
"""

import asyncio
import hashlib
import json
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import threading


# ============================================================
# TOPIC AND SCOPE DEFINITIONS
# ============================================================

class TopicCategory(Enum):
    """High-level topic categories"""
    TRUTH = "truth"                  # Truth verification, fact-checking
    QUANTUM = "quantum"              # Quantum computing, physics
    SECURITY = "security"            # Security, defense, protection
    INTEGRATION = "integration"      # System integration
    CONSCIOUSNESS = "consciousness"  # Consciousness, AI awareness
    ETHICS = "ethics"                # Ethics, Ma'at alignment
    SYNTHESIS = "synthesis"          # Cross-topic synthesis


class AgentCapability(Enum):
    """Agent capabilities for matching"""
    RESEARCH = "research"
    ANALYZE = "analyze"
    VERIFY = "verify"
    SYNTHESIZE = "synthesize"
    EXECUTE = "execute"
    COORDINATE = "coordinate"
    VALIDATE = "validate"


@dataclass
class Topic:
    """A scoped topic for agent clustering"""
    id: str
    name: str
    category: TopicCategory
    keywords: Set[str]
    parent_topic: Optional[str] = None  # For hierarchical topics
    active: bool = True
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def matches(self, text: str) -> float:
        """Calculate how well text matches this topic (0-1)"""
        text_lower = text.lower()
        text_words = set(text_lower.split())
        matches = len(self.keywords & text_words)
        return matches / max(len(self.keywords), 1)


@dataclass
class ScopedAgent:
    """An agent scoped to specific topics"""
    id: str
    name: str
    capabilities: Set[AgentCapability]
    topics: Set[str]  # Topic IDs this agent handles
    status: str = "idle"
    current_task: Optional[str] = None
    performance_score: float = 1.0  # Track agent effectiveness

    def can_handle(self, topic_id: str, required_caps: Set[AgentCapability]) -> bool:
        """Check if agent can handle a task"""
        return (
            topic_id in self.topics and
            required_caps.issubset(self.capabilities) and
            self.status == "idle"
        )


@dataclass
class ScopedTask:
    """A task scoped to a specific topic"""
    id: str
    description: str
    topic_id: str
    required_capabilities: Set[AgentCapability]
    assigned_agents: List[str] = field(default_factory=list)
    status: str = "pending"
    result: Any = None
    verification_score: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = None


@dataclass
class VerificationResult:
    """Result of topic-scoped verification"""
    task_id: str
    topic_id: str
    verified: bool
    confidence: float
    verifying_agents: List[str]
    consensus_achieved: bool
    dissenting_opinions: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ============================================================
# TOPIC CLUSTER
# ============================================================

class TopicCluster:
    """
    A cluster of agents organized around a topic.
    Handles all tasks within the topic scope.
    """

    def __init__(self, topic: Topic, min_agents: int = 2):
        self.topic = topic
        self.min_agents = min_agents
        self.agents: Dict[str, ScopedAgent] = {}
        self.tasks: Dict[str, ScopedTask] = {}
        self.verification_results: List[VerificationResult] = []
        self._lock = threading.Lock()

        # Metrics
        self.tasks_completed = 0
        self.verification_success_rate = 0.0
        self.avg_consensus_time_ms = 0.0

    def add_agent(self, agent: ScopedAgent) -> bool:
        """Add an agent to the cluster"""
        with self._lock:
            if self.topic.id not in agent.topics:
                return False
            self.agents[agent.id] = agent
            return True

    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the cluster"""
        with self._lock:
            if agent_id in self.agents:
                del self.agents[agent_id]
                return True
            return False

    def get_available_agents(self, capabilities: Set[AgentCapability] = None) -> List[ScopedAgent]:
        """Get available agents, optionally filtered by capabilities"""
        with self._lock:
            available = [a for a in self.agents.values() if a.status == "idle"]
            if capabilities:
                available = [a for a in available if capabilities.issubset(a.capabilities)]
            return available

    async def submit_task(self, description: str,
                          capabilities: Set[AgentCapability] = None) -> ScopedTask:
        """Submit a task to the cluster"""
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        caps = capabilities or {AgentCapability.ANALYZE}

        task = ScopedTask(
            id=task_id,
            description=description,
            topic_id=self.topic.id,
            required_capabilities=caps
        )

        with self._lock:
            self.tasks[task_id] = task

        return task

    async def execute_task(self, task: ScopedTask) -> Any:
        """Execute a task using cluster agents"""
        available = self.get_available_agents(task.required_capabilities)

        if len(available) < self.min_agents:
            return {"error": f"Insufficient agents. Need {self.min_agents}, have {len(available)}"}

        # Assign agents
        assigned = available[:min(3, len(available))]
        task.assigned_agents = [a.id for a in assigned]
        task.status = "in_progress"

        for agent in assigned:
            agent.status = "working"
            agent.current_task = task.id

        # Simulate work (in production, agents would do actual work)
        await asyncio.sleep(0.01)

        # Collect results
        results = []
        for agent in assigned:
            # Agent completes work
            agent_result = {
                "agent_id": agent.id,
                "analysis": f"Analysis by {agent.name}",
                "confidence": 0.8 + hash(agent.id) % 20 / 100
            }
            results.append(agent_result)

            # Reset agent status
            agent.status = "idle"
            agent.current_task = None

        # Aggregate results
        task.result = results
        task.status = "completed"
        task.completed_at = datetime.utcnow().isoformat()

        with self._lock:
            self.tasks_completed += 1

        return results

    async def verify_within_scope(self, content: str,
                                  context: Dict = None) -> VerificationResult:
        """
        Verify content within this topic's scope.
        Uses cluster agents for consensus.
        """
        start_time = time.perf_counter()

        # Create verification task
        task = await self.submit_task(
            description=f"Verify: {content[:100]}...",
            capabilities={AgentCapability.VERIFY, AgentCapability.ANALYZE}
        )

        # Execute with available agents
        results = await self.execute_task(task)

        if isinstance(results, dict) and "error" in results:
            return VerificationResult(
                task_id=task.id,
                topic_id=self.topic.id,
                verified=False,
                confidence=0.0,
                verifying_agents=[],
                consensus_achieved=False,
                dissenting_opinions=[results["error"]]
            )

        # Calculate consensus
        confidences = [r["confidence"] for r in results]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        # Check for consensus (agents within 0.2 of each other)
        confidence_range = max(confidences) - min(confidences) if confidences else 0
        consensus = confidence_range < 0.2

        verified = avg_confidence >= 0.7 and consensus

        result = VerificationResult(
            task_id=task.id,
            topic_id=self.topic.id,
            verified=verified,
            confidence=avg_confidence,
            verifying_agents=task.assigned_agents,
            consensus_achieved=consensus,
            dissenting_opinions=[] if consensus else [
                f"Agent disagreement: confidence range {confidence_range:.2f}"
            ]
        )

        # Update metrics
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        with self._lock:
            self.verification_results.append(result)
            self.avg_consensus_time_ms = (
                (self.avg_consensus_time_ms * (len(self.verification_results) - 1) + elapsed_ms)
                / len(self.verification_results)
            )
            successful = sum(1 for r in self.verification_results if r.verified)
            self.verification_success_rate = successful / len(self.verification_results)

        return result

    def get_metrics(self) -> Dict[str, Any]:
        """Get cluster metrics"""
        with self._lock:
            return {
                "topic_id": self.topic.id,
                "topic_name": self.topic.name,
                "category": self.topic.category.value,
                "total_agents": len(self.agents),
                "idle_agents": len([a for a in self.agents.values() if a.status == "idle"]),
                "tasks_completed": self.tasks_completed,
                "verification_success_rate": self.verification_success_rate,
                "avg_consensus_time_ms": self.avg_consensus_time_ms,
                "total_verifications": len(self.verification_results)
            }


# ============================================================
# TSVC - TOPIC-SCOPED VERIFICATION CLUSTER MESH
# ============================================================

class TSVCMesh:
    """
    TOPIC-SCOPED VERIFICATION CLUSTER MESH
    =======================================

    A streamlined multi-agent mesh that:
    1. Organizes agents into topic clusters
    2. Routes tasks to appropriate clusters
    3. Enables cross-topic synthesis
    4. Provides unified verification

    Design Principles:
    - Topic boundaries for scope management
    - Self-organizing clusters
    - Minimal coordination overhead
    - Ma'at-aligned verification
    """

    def __init__(self):
        self.topics: Dict[str, Topic] = {}
        self.clusters: Dict[str, TopicCluster] = {}
        self.agents: Dict[str, ScopedAgent] = {}
        self.cross_topic_results: List[Dict] = []

        self._lock = threading.Lock()

        # Ledger
        self.ledger_path = Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI/ledger")
        self.ledger_path.mkdir(parents=True, exist_ok=True)

        # Initialize default topics
        self._initialize_default_topics()

    def _initialize_default_topics(self):
        """Initialize default topic clusters"""
        default_topics = [
            Topic(
                id="truth",
                name="Truth Verification",
                category=TopicCategory.TRUTH,
                keywords={"truth", "verify", "fact", "accurate", "evidence", "claim"}
            ),
            Topic(
                id="quantum",
                name="Quantum Systems",
                category=TopicCategory.QUANTUM,
                keywords={"quantum", "qubit", "superposition", "entanglement", "annealing"}
            ),
            Topic(
                id="security",
                name="Security & Defense",
                category=TopicCategory.SECURITY,
                keywords={"security", "protect", "defense", "threat", "vulnerability"}
            ),
            Topic(
                id="integration",
                name="System Integration",
                category=TopicCategory.INTEGRATION,
                keywords={"integrate", "connect", "api", "bridge", "interface"}
            ),
            Topic(
                id="consciousness",
                name="Consciousness & Awareness",
                category=TopicCategory.CONSCIOUSNESS,
                keywords={"consciousness", "aware", "sentient", "intelligence", "mind"}
            ),
            Topic(
                id="ethics",
                name="Ethics & Ma'at Alignment",
                category=TopicCategory.ETHICS,
                keywords={"ethics", "maat", "truth", "justice", "balance", "harmony"}
            ),
            Topic(
                id="synthesis",
                name="Cross-Topic Synthesis",
                category=TopicCategory.SYNTHESIS,
                keywords={"synthesize", "combine", "merge", "unify", "aggregate"}
            ),
        ]

        for topic in default_topics:
            self.register_topic(topic)

    def register_topic(self, topic: Topic) -> TopicCluster:
        """Register a topic and create its cluster"""
        with self._lock:
            self.topics[topic.id] = topic
            cluster = TopicCluster(topic)
            self.clusters[topic.id] = cluster
            return cluster

    def register_agent(self, name: str,
                       capabilities: Set[AgentCapability],
                       topics: Set[str]) -> ScopedAgent:
        """Register an agent and add to relevant clusters"""
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"

        agent = ScopedAgent(
            id=agent_id,
            name=name,
            capabilities=capabilities,
            topics=topics
        )

        with self._lock:
            self.agents[agent_id] = agent

            # Add to relevant clusters
            for topic_id in topics:
                if topic_id in self.clusters:
                    self.clusters[topic_id].add_agent(agent)

        return agent

    def find_topic_for_content(self, content: str) -> Optional[Topic]:
        """Find the best matching topic for content"""
        best_topic = None
        best_score = 0.0

        for topic in self.topics.values():
            score = topic.matches(content)
            if score > best_score:
                best_score = score
                best_topic = topic

        return best_topic if best_score > 0.1 else None

    async def verify(self, content: str,
                     topic_id: str = None,
                     context: Dict = None) -> VerificationResult:
        """
        Verify content using topic-scoped cluster.

        Args:
            content: Content to verify
            topic_id: Specific topic (auto-detected if None)
            context: Additional context

        Returns:
            VerificationResult from the cluster
        """
        # Find or use specified topic
        if topic_id and topic_id in self.clusters:
            cluster = self.clusters[topic_id]
        else:
            topic = self.find_topic_for_content(content)
            if topic:
                cluster = self.clusters[topic.id]
            else:
                # Default to truth cluster
                cluster = self.clusters.get("truth")
                if not cluster:
                    raise ValueError("No suitable topic cluster found")

        # Verify within cluster scope
        result = await cluster.verify_within_scope(content, context)

        # Log to ledger
        self._log_verification(result)

        return result

    async def verify_cross_topic(self, content: str,
                                 topic_ids: List[str] = None,
                                 context: Dict = None) -> Dict[str, Any]:
        """
        Verify content across multiple topics.
        Synthesizes results from different perspectives.
        """
        if not topic_ids:
            # Auto-detect relevant topics
            topic_ids = []
            for topic in self.topics.values():
                if topic.matches(content) > 0.1:
                    topic_ids.append(topic.id)

        if not topic_ids:
            topic_ids = ["truth"]  # Default

        # Verify in each topic cluster
        tasks = []
        for topic_id in topic_ids:
            if topic_id in self.clusters:
                tasks.append(self.clusters[topic_id].verify_within_scope(content, context))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Synthesize results
        verified_count = 0
        total_confidence = 0.0
        topic_results = {}

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                topic_results[topic_ids[i]] = {"error": str(result)}
            else:
                topic_results[topic_ids[i]] = {
                    "verified": result.verified,
                    "confidence": result.confidence,
                    "consensus": result.consensus_achieved
                }
                if result.verified:
                    verified_count += 1
                total_confidence += result.confidence

        avg_confidence = total_confidence / len(results) if results else 0.0
        cross_topic_verified = verified_count > len(results) / 2

        synthesis = {
            "content_hash": hashlib.sha256(content.encode()).hexdigest()[:16],
            "topic_results": topic_results,
            "cross_topic_verified": cross_topic_verified,
            "avg_confidence": avg_confidence,
            "topics_checked": len(topic_ids),
            "topics_verified": verified_count,
            "timestamp": datetime.utcnow().isoformat()
        }

        with self._lock:
            self.cross_topic_results.append(synthesis)

        return synthesis

    async def execute_scoped_task(self, description: str,
                                  topic_id: str = None,
                                  capabilities: Set[AgentCapability] = None) -> Any:
        """Execute a task within a topic scope"""
        if topic_id and topic_id in self.clusters:
            cluster = self.clusters[topic_id]
        else:
            topic = self.find_topic_for_content(description)
            cluster = self.clusters.get(topic.id if topic else "synthesis")

        task = await cluster.submit_task(description, capabilities)
        return await cluster.execute_task(task)

    def _log_verification(self, result: VerificationResult):
        """Log verification to ledger"""
        entry = {
            "timestamp": result.timestamp,
            "task_id": result.task_id,
            "topic_id": result.topic_id,
            "verified": result.verified,
            "confidence": result.confidence,
            "consensus_achieved": result.consensus_achieved,
            "agents_count": len(result.verifying_agents)
        }

        ledger_file = self.ledger_path / "tsvc_verification_ledger.jsonl"
        try:
            with open(ledger_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception:
            pass

    def get_mesh_status(self) -> Dict[str, Any]:
        """Get overall mesh status"""
        cluster_metrics = {}
        for topic_id, cluster in self.clusters.items():
            cluster_metrics[topic_id] = cluster.get_metrics()

        return {
            "total_topics": len(self.topics),
            "total_agents": len(self.agents),
            "total_clusters": len(self.clusters),
            "cross_topic_verifications": len(self.cross_topic_results),
            "cluster_metrics": cluster_metrics
        }

    def get_agent_distribution(self) -> Dict[str, int]:
        """Get agent distribution across topics"""
        distribution = defaultdict(int)
        for agent in self.agents.values():
            for topic_id in agent.topics:
                distribution[topic_id] += 1
        return dict(distribution)


# ============================================================
# FACTORY AND SINGLETON
# ============================================================

_tsvc_instance: Optional[TSVCMesh] = None


def get_tsvc_mesh() -> TSVCMesh:
    """Get or create the TSVC mesh singleton"""
    global _tsvc_instance
    if _tsvc_instance is None:
        _tsvc_instance = TSVCMesh()

        # Register default agents
        _tsvc_instance.register_agent(
            "Truth Guardian",
            {AgentCapability.VERIFY, AgentCapability.ANALYZE},
            {"truth", "ethics"}
        )
        _tsvc_instance.register_agent(
            "Quantum Analyst",
            {AgentCapability.ANALYZE, AgentCapability.RESEARCH},
            {"quantum", "integration"}
        )
        _tsvc_instance.register_agent(
            "Security Sentinel",
            {AgentCapability.VERIFY, AgentCapability.VALIDATE},
            {"security", "truth"}
        )
        _tsvc_instance.register_agent(
            "Integration Bridge",
            {AgentCapability.EXECUTE, AgentCapability.SYNTHESIZE},
            {"integration", "synthesis"}
        )
        _tsvc_instance.register_agent(
            "Consciousness Observer",
            {AgentCapability.ANALYZE, AgentCapability.RESEARCH},
            {"consciousness", "ethics"}
        )
        _tsvc_instance.register_agent(
            "Ethics Arbiter",
            {AgentCapability.VERIFY, AgentCapability.VALIDATE},
            {"ethics", "truth"}
        )
        _tsvc_instance.register_agent(
            "Synthesis Master",
            {AgentCapability.SYNTHESIZE, AgentCapability.COORDINATE},
            {"synthesis"}
        )

    return _tsvc_instance


# ============================================================
# DEMO AND TEST
# ============================================================

async def demo_tsvc_mesh():
    """Demonstrate TSVC mesh functionality"""
    print("=" * 70)
    print("TSVC - TOPIC-SCOPED VERIFICATION CLUSTER MESH")
    print("TASK-153: Streamline TSVC topic-scoped mesh")
    print("=" * 70)

    mesh = get_tsvc_mesh()

    # Status
    print("\nMesh Status:")
    status = mesh.get_mesh_status()
    print(f"  Topics: {status['total_topics']}")
    print(f"  Agents: {status['total_agents']}")
    print(f"  Clusters: {status['total_clusters']}")

    # Agent distribution
    print("\nAgent Distribution:")
    distribution = mesh.get_agent_distribution()
    for topic_id, count in sorted(distribution.items()):
        print(f"  {topic_id}: {count} agents")

    # Single-topic verification
    print("\n" + "-" * 70)
    print("SINGLE-TOPIC VERIFICATION")
    print("-" * 70)

    test_content = "The quantum entanglement experiment demonstrated accurate results."
    result = await mesh.verify(test_content)

    print(f"\nContent: {test_content}")
    print(f"Topic: {result.topic_id}")
    print(f"Verified: {result.verified}")
    print(f"Confidence: {result.confidence:.2%}")
    print(f"Consensus: {result.consensus_achieved}")

    # Cross-topic verification
    print("\n" + "-" * 70)
    print("CROSS-TOPIC VERIFICATION")
    print("-" * 70)

    cross_content = "The security system uses quantum encryption with ethical AI oversight."
    cross_result = await mesh.verify_cross_topic(
        cross_content,
        topic_ids=["security", "quantum", "ethics"]
    )

    print(f"\nContent: {cross_content}")
    print(f"Topics Checked: {cross_result['topics_checked']}")
    print(f"Topics Verified: {cross_result['topics_verified']}")
    print(f"Cross-Topic Verified: {cross_result['cross_topic_verified']}")
    print(f"Average Confidence: {cross_result['avg_confidence']:.2%}")

    print("\nPer-Topic Results:")
    for topic_id, topic_result in cross_result['topic_results'].items():
        print(f"  {topic_id}: {topic_result}")

    # Execute scoped task
    print("\n" + "-" * 70)
    print("SCOPED TASK EXECUTION")
    print("-" * 70)

    task_result = await mesh.execute_scoped_task(
        "Analyze quantum computing integration patterns",
        topic_id="quantum",
        capabilities={AgentCapability.ANALYZE, AgentCapability.RESEARCH}
    )

    print(f"\nTask executed with {len(task_result)} agent(s)")
    for r in task_result:
        print(f"  Agent {r['agent_id']}: confidence {r['confidence']:.2f}")

    # Final status
    print("\n" + "-" * 70)
    print("FINAL MESH STATUS")
    print("-" * 70)

    final_status = mesh.get_mesh_status()
    for topic_id, metrics in final_status['cluster_metrics'].items():
        if metrics['tasks_completed'] > 0 or metrics['total_verifications'] > 0:
            print(f"\n{metrics['topic_name']} ({topic_id}):")
            print(f"  Tasks completed: {metrics['tasks_completed']}")
            print(f"  Verifications: {metrics['total_verifications']}")
            print(f"  Success rate: {metrics['verification_success_rate']:.2%}")

    print("\n" + "=" * 70)
    print("TSVC MESH - DEMO COMPLETE")
    print("Ma'at Alignment: Topics scope the truth")
    print("=" * 70)

    return mesh


def demo_sync():
    """Synchronous wrapper for demo"""
    return asyncio.run(demo_tsvc_mesh())


if __name__ == "__main__":
    demo_sync()

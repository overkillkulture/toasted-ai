"""
TASK-153: TSVC Topic-Scoped Mesh System
========================================
Topic-Scoped Variable Control for managing 1000+ agent advancements.

Features:
- Topic-based agent organization
- Scoped variable management
- Dynamic topic routing
- Cross-topic communication
- Topic hierarchy and inheritance
- Variable versioning and isolation

TSVC 2.0: Scalable mesh-control for massive agent ecosystems

Owner: TOASTED AI
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import uuid


class TopicScope(Enum):
    """Scope levels for topics."""
    GLOBAL = "global"
    DOMAIN = "domain"
    LOCAL = "local"
    PRIVATE = "private"


class VariableType(Enum):
    """Types of variables in TSVC."""
    STATE = "state"
    CONFIG = "config"
    METRIC = "metric"
    SHARED = "shared"
    EPHEMERAL = "ephemeral"


@dataclass
class Topic:
    """Represents a topic in the mesh."""
    id: str
    name: str
    scope: TopicScope
    parent_topic_id: Optional[str] = None
    child_topics: List[str] = field(default_factory=list)
    subscribed_agents: List[str] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ScopedVariable:
    """A variable scoped to a topic."""
    name: str
    value: Any
    var_type: VariableType
    topic_id: str
    version: int = 1
    owner_agent_id: Optional[str] = None
    access_control: Set[str] = field(default_factory=set)  # Agent IDs with access
    last_modified: datetime = field(default_factory=datetime.now)
    history: List[Dict] = field(default_factory=list)


@dataclass
class TopicMessage:
    """Message routed through topics."""
    id: str
    topic_id: str
    sender_agent_id: str
    content: Any
    message_type: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)


class TSVCMesh:
    """
    Topic-Scoped Variable Control Mesh.

    Manages topics, scoped variables, and agent communication
    across a large-scale agent ecosystem.
    """

    def __init__(self):
        self.topics: Dict[str, Topic] = {}
        self.variables: Dict[str, ScopedVariable] = {}  # Key: topic_id:var_name
        self.agents: Dict[str, Dict] = {}  # Agent registry
        self.messages: List[TopicMessage] = []
        self.topic_hierarchy: Dict[str, List[str]] = {}  # parent -> children

        # Initialize root topics
        self._init_root_topics()

    def _init_root_topics(self):
        """Initialize root topic hierarchy."""
        root_topics = [
            ("consciousness", TopicScope.GLOBAL, "Consciousness systems"),
            ("quantum", TopicScope.GLOBAL, "Quantum operations"),
            ("autonomous", TopicScope.GLOBAL, "Autonomous systems"),
            ("knowledge", TopicScope.GLOBAL, "Knowledge management"),
            ("security", TopicScope.GLOBAL, "Security operations"),
            ("evolution", TopicScope.GLOBAL, "System evolution"),
            ("integration", TopicScope.GLOBAL, "Cross-system integration")
        ]

        for name, scope, description in root_topics:
            topic_id = f"topic_{name}"
            self.topics[topic_id] = Topic(
                id=topic_id,
                name=name,
                scope=scope,
                metadata={"description": description}
            )

    def create_topic(self, name: str, scope: TopicScope,
                    parent_topic_id: Optional[str] = None) -> Topic:
        """
        Create a new topic.

        Args:
            name: Topic name
            scope: Scope level
            parent_topic_id: Optional parent topic

        Returns:
            Created topic
        """
        topic_id = f"topic_{uuid.uuid4().hex[:8]}"

        topic = Topic(
            id=topic_id,
            name=name,
            scope=scope,
            parent_topic_id=parent_topic_id
        )

        self.topics[topic_id] = topic

        # Update hierarchy
        if parent_topic_id and parent_topic_id in self.topics:
            self.topics[parent_topic_id].child_topics.append(topic_id)

            if parent_topic_id not in self.topic_hierarchy:
                self.topic_hierarchy[parent_topic_id] = []
            self.topic_hierarchy[parent_topic_id].append(topic_id)

        return topic

    def subscribe_agent(self, agent_id: str, topic_id: str) -> bool:
        """
        Subscribe an agent to a topic.

        Args:
            agent_id: Agent to subscribe
            topic_id: Topic to subscribe to

        Returns:
            Success status
        """
        if topic_id not in self.topics:
            return False

        topic = self.topics[topic_id]
        if agent_id not in topic.subscribed_agents:
            topic.subscribed_agents.append(agent_id)

        return True

    def set_variable(self, topic_id: str, var_name: str, value: Any,
                    var_type: VariableType = VariableType.STATE,
                    owner_agent_id: Optional[str] = None) -> bool:
        """
        Set a scoped variable in a topic.

        Args:
            topic_id: Topic containing the variable
            var_name: Variable name
            value: Variable value
            var_type: Type of variable
            owner_agent_id: Agent setting the variable

        Returns:
            Success status
        """
        if topic_id not in self.topics:
            return False

        var_key = f"{topic_id}:{var_name}"

        if var_key in self.variables:
            # Update existing variable
            variable = self.variables[var_key]

            # Record history
            variable.history.append({
                "version": variable.version,
                "value": variable.value,
                "timestamp": variable.last_modified.isoformat()
            })

            # Update
            variable.value = value
            variable.version += 1
            variable.last_modified = datetime.now()
        else:
            # Create new variable
            variable = ScopedVariable(
                name=var_name,
                value=value,
                var_type=var_type,
                topic_id=topic_id,
                owner_agent_id=owner_agent_id
            )
            self.variables[var_key] = variable

        # Also store in topic
        self.topics[topic_id].variables[var_name] = value

        return True

    def get_variable(self, topic_id: str, var_name: str,
                    agent_id: Optional[str] = None) -> Optional[Any]:
        """
        Get a scoped variable from a topic.

        Args:
            topic_id: Topic containing the variable
            var_name: Variable name
            agent_id: Agent requesting the variable (for access control)

        Returns:
            Variable value or None
        """
        var_key = f"{topic_id}:{var_name}"

        if var_key not in self.variables:
            # Check parent topics (inheritance)
            if topic_id in self.topics:
                parent_id = self.topics[topic_id].parent_topic_id
                if parent_id:
                    return self.get_variable(parent_id, var_name, agent_id)
            return None

        variable = self.variables[var_key]

        # Check access control
        if variable.access_control and agent_id:
            if agent_id not in variable.access_control:
                return None

        return variable.value

    def publish_message(self, topic_id: str, sender_agent_id: str,
                       content: Any, message_type: str = "data") -> TopicMessage:
        """
        Publish a message to a topic.

        Args:
            topic_id: Topic to publish to
            sender_agent_id: Sending agent
            content: Message content
            message_type: Type of message

        Returns:
            Published message
        """
        msg = TopicMessage(
            id=f"msg_{uuid.uuid4().hex[:8]}",
            topic_id=topic_id,
            sender_agent_id=sender_agent_id,
            content=content,
            message_type=message_type
        )

        self.messages.append(msg)

        # Notify subscribers
        if topic_id in self.topics:
            topic = self.topics[topic_id]
            # In production, would trigger callbacks for subscribed agents

        return msg

    def get_topic_messages(self, topic_id: str, limit: int = 100) -> List[TopicMessage]:
        """Get recent messages for a topic."""
        topic_messages = [
            msg for msg in self.messages
            if msg.topic_id == topic_id
        ]
        return topic_messages[-limit:]

    def get_topic_tree(self, root_topic_id: str) -> Dict:
        """
        Get the topic hierarchy tree from a root.

        Args:
            root_topic_id: Root topic to start from

        Returns:
            Tree structure
        """
        if root_topic_id not in self.topics:
            return {}

        def build_tree(topic_id: str) -> Dict:
            topic = self.topics[topic_id]
            tree = {
                "id": topic_id,
                "name": topic.name,
                "scope": topic.scope.value,
                "subscribers": len(topic.subscribed_agents),
                "variables": len(topic.variables),
                "children": []
            }

            for child_id in topic.child_topics:
                if child_id in self.topics:
                    tree["children"].append(build_tree(child_id))

            return tree

        return build_tree(root_topic_id)

    def route_to_topic(self, content: Any, keywords: List[str]) -> List[str]:
        """
        Route content to appropriate topics based on keywords.

        Args:
            content: Content to route
            keywords: Keywords for routing

        Returns:
            List of matching topic IDs
        """
        matched_topics = []

        keywords_lower = [k.lower() for k in keywords]

        for topic_id, topic in self.topics.items():
            topic_name_lower = topic.name.lower()

            # Check if any keyword matches topic name
            if any(kw in topic_name_lower for kw in keywords_lower):
                matched_topics.append(topic_id)

            # Check topic metadata
            if "description" in topic.metadata:
                desc_lower = topic.metadata["description"].lower()
                if any(kw in desc_lower for kw in keywords_lower):
                    matched_topics.append(topic_id)

        return list(set(matched_topics))  # Remove duplicates

    def aggregate_topic_variables(self, topic_ids: List[str]) -> Dict[str, Any]:
        """
        Aggregate variables from multiple topics.

        Args:
            topic_ids: Topics to aggregate from

        Returns:
            Aggregated variables
        """
        aggregated = {}

        for topic_id in topic_ids:
            if topic_id in self.topics:
                topic = self.topics[topic_id]
                for var_name, var_value in topic.variables.items():
                    key = f"{topic.name}.{var_name}"
                    aggregated[key] = var_value

        return aggregated

    def get_topic_stats(self, topic_id: str) -> Dict:
        """Get statistics for a topic."""
        if topic_id not in self.topics:
            return {}

        topic = self.topics[topic_id]

        return {
            "topic_id": topic_id,
            "name": topic.name,
            "scope": topic.scope.value,
            "subscribers": len(topic.subscribed_agents),
            "variables": len(topic.variables),
            "child_topics": len(topic.child_topics),
            "messages": len([m for m in self.messages if m.topic_id == topic_id]),
            "created_at": topic.created_at.isoformat()
        }

    def get_mesh_status(self) -> Dict:
        """Get overall mesh status."""
        topic_by_scope = {}
        for scope in TopicScope:
            count = len([t for t in self.topics.values() if t.scope == scope])
            topic_by_scope[scope.value] = count

        var_by_type = {}
        for var_type in VariableType:
            count = len([v for v in self.variables.values() if v.var_type == var_type])
            var_by_type[var_type.value] = count

        return {
            "total_topics": len(self.topics),
            "topics_by_scope": topic_by_scope,
            "total_variables": len(self.variables),
            "variables_by_type": var_by_type,
            "total_messages": len(self.messages),
            "total_agents": len(self.agents),
            "root_topics": len([t for t in self.topics.values() if not t.parent_topic_id])
        }

    def prune_ephemeral_variables(self, age_minutes: int = 60):
        """Remove ephemeral variables older than specified age."""
        cutoff = datetime.now()
        removed = []

        for var_key, variable in list(self.variables.items()):
            if variable.var_type == VariableType.EPHEMERAL:
                age = (cutoff - variable.last_modified).total_seconds() / 60
                if age > age_minutes:
                    del self.variables[var_key]
                    removed.append(var_key)

        return removed


# Singleton instance
_tsvc_mesh = None

def get_tsvc_mesh() -> TSVCMesh:
    """Get the singleton TSVC Mesh instance."""
    global _tsvc_mesh
    if _tsvc_mesh is None:
        _tsvc_mesh = TSVCMesh()
    return _tsvc_mesh


if __name__ == "__main__":
    print("=" * 70)
    print("TSVC TOPIC-SCOPED MESH - TASK-153")
    print("=" * 70)

    mesh = get_tsvc_mesh()

    # Show initial topics
    print("\n1. Root Topics:")
    for topic_id, topic in mesh.topics.items():
        if not topic.parent_topic_id:
            print(f"   - {topic.name} ({topic.scope.value})")

    # Create nested topics
    print("\n2. Creating Nested Topics:")
    quantum_topic = mesh.topics["topic_quantum"]
    subtopic1 = mesh.create_topic("quantum_entanglement", TopicScope.DOMAIN, quantum_topic.id)
    subtopic2 = mesh.create_topic("quantum_computing", TopicScope.DOMAIN, quantum_topic.id)
    print(f"   Created: {subtopic1.name} under {quantum_topic.name}")
    print(f"   Created: {subtopic2.name} under {quantum_topic.name}")

    # Subscribe agents
    print("\n3. Agent Subscription:")
    mesh.subscribe_agent("agent_001", "topic_quantum")
    mesh.subscribe_agent("agent_002", subtopic1.id)
    print(f"   Subscribed agents to quantum topics")

    # Set scoped variables
    print("\n4. Scoped Variables:")
    mesh.set_variable("topic_quantum", "coherence_time", 1.5, VariableType.METRIC)
    mesh.set_variable(subtopic1.id, "entanglement_strength", 0.95, VariableType.STATE)
    mesh.set_variable(subtopic2.id, "qubit_count", 128, VariableType.CONFIG)
    print("   Set variables across topics")

    # Get variables (with inheritance)
    print("\n5. Variable Retrieval:")
    val1 = mesh.get_variable("topic_quantum", "coherence_time")
    val2 = mesh.get_variable(subtopic1.id, "entanglement_strength")
    val3 = mesh.get_variable(subtopic1.id, "coherence_time")  # Should inherit from parent
    print(f"   Quantum coherence_time: {val1}")
    print(f"   Entanglement strength: {val2}")
    print(f"   Inherited coherence_time: {val3}")

    # Publish messages
    print("\n6. Topic Messages:")
    msg1 = mesh.publish_message("topic_quantum", "agent_001",
                                {"status": "operational"}, "status_update")
    msg2 = mesh.publish_message(subtopic1.id, "agent_002",
                                {"measurement": "complete"}, "result")
    print(f"   Published {len(mesh.messages)} messages")

    # Route content
    print("\n7. Topic Routing:")
    routes = mesh.route_to_topic("quantum entanglement data", ["quantum", "entanglement"])
    print(f"   Routed to {len(routes)} topics:")
    for route in routes:
        print(f"     - {mesh.topics[route].name}")

    # Topic tree
    print("\n8. Topic Hierarchy:")
    tree = mesh.get_topic_tree("topic_quantum")
    print(f"   {tree['name']}:")
    for child in tree['children']:
        print(f"     - {child['name']} ({child['subscribers']} subscribers, {child['variables']} vars)")

    # Aggregate variables
    print("\n9. Variable Aggregation:")
    aggregated = mesh.aggregate_topic_variables(["topic_quantum", subtopic1.id, subtopic2.id])
    print("   Aggregated variables:")
    for key, value in aggregated.items():
        print(f"     {key}: {value}")

    # Topic stats
    print("\n10. Topic Statistics:")
    stats = mesh.get_topic_stats("topic_quantum")
    for key, value in stats.items():
        print(f"    {key}: {value}")

    # Mesh status
    print("\n11. Mesh Status:")
    status = mesh.get_mesh_status()
    for key, value in status.items():
        print(f"    {key}: {value}")

    print("\n" + "=" * 70)
    print("✓ TASK-153 COMPLETE: TSVC Topic-Scoped Mesh operational")
    print("=" * 70)

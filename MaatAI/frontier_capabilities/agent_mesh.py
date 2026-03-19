"""
Agent Mesh
==========
Multi-agent communication and collaboration protocol.
Enables multiple specialized agents to work together.

Key Features:
- Agent discovery and registration
- Message passing
- Role-based task allocation
- Consensus mechanisms
- Conflict resolution
- Shared memory space

Based on patterns from: AgentVerse, CAMEL, ChatDev, Multi-Agent Debate
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid


class AgentRole(Enum):
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    EXECUTOR = "executor"
    VALIDATOR = "validator"
    SYNTHESIZER = "synthesizer"
    SPECIALIST = "specialist"


class MessageType(Enum):
    TASK = "task"
    RESULT = "result"
    QUERY = "query"
    RESPONSE = "response"
    PROPOSE = "propose"
    AGREE = "agree"
    DISAGREE = "disagree"
    STATUS = "status"


@dataclass
class Agent:
    """Represents an agent in the mesh."""
    id: str
    name: str
    role: AgentRole
    capabilities: list[str]
    status: str = "idle"  # idle, working, blocked, complete
    current_task: str = None
    specialty: str = None
    
    
@dataclass
class Message:
    """Represents a message between agents."""
    id: str
    sender_id: str
    receiver_id: str  # or "broadcast"
    type: MessageType
    content: Any
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)
    
    
@dataclass
class Task:
    """Represents a task in the mesh."""
    id: str
    description: str
    requirements: list[str]
    assigned_agents: list[str] = field(default_factory=list)
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Any = None
    created_at: datetime = field(default_factory=datetime.now)


class AgentMesh:
    """
    Multi-agent collaboration mesh.
    """
    
    def __init__(self):
        self.agents: dict[str, Agent] = {}
        self.messages: list[Message] = []
        self.tasks: dict[str, Task] = {}
        self.shared_memory: dict[str, Any] = {}
        self.message_handlers: dict[MessageType, list[Callable]] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()
        
    def register_agent(self, name: str, role: AgentRole, 
                       capabilities: list[str], specialty: str = None) -> Agent:
        """Register a new agent in the mesh."""
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        
        agent = Agent(
            id=agent_id,
            name=name,
            role=role,
            capabilities=capabilities,
            specialty=specialty
        )
        
        self.agents[agent_id] = agent
        return agent
    
    def get_agents_by_role(self, role: AgentRole) -> list[Agent]:
        """Get all agents with a specific role."""
        return [a for a in self.agents.values() if a.role == role]
    
    def get_available_agents(self) -> list[Agent]:
        """Get all idle agents."""
        return [a for a in self.agents.values() if a.status == "idle"]
    
    def send_message(self, sender_id: str, receiver_id: str,
                    msg_type: MessageType, content: Any,
                    metadata: dict = None) -> Message:
        """Send a message between agents."""
        msg = Message(
            id=f"msg_{uuid.uuid4().hex[:8]}",
            sender_id=sender_id,
            receiver_id=receiver_id,
            type=msg_type,
            content=content,
            metadata=metadata or {}
        )
        
        self.messages.append(msg)
        
        # Queue for async processing
        self.event_queue.put_nowait(msg)
        
        return msg
    
    def broadcast(self, sender_id: str, msg_type: MessageType,
                 content: Any, metadata: dict = None) -> list[Message]:
        """Broadcast message to all agents."""
        messages = []
        
        for agent_id in self.agents:
            if agent_id != sender_id:
                msg = self.send_message(sender_id, agent_id, msg_type, content, metadata)
                messages.append(msg)
                
        return messages
    
    def assign_task(self, task: Task, agent_ids: list[str]) -> bool:
        """Assign a task to agents."""
        task.assigned_agents = agent_ids
        task.status = "in_progress"
        
        self.tasks[task.id] = task
        
        # Notify assigned agents
        for agent_id in agent_ids:
            if agent_id in self.agents:
                self.agents[agent_id].status = "working"
                self.agents[agent_id].current_task = task.id
                
                self.send_message(
                    "system",
                    agent_id,
                    MessageType.TASK,
                    {"task_id": task.id, "description": task.description}
                )
                
        return True
    
    def select_agents_for_task(self, requirements: list[str]) -> list[Agent]:
        """Select best agents for a task based on requirements."""
        scores = []
        
        for agent in self.agents.values():
            if agent.status != "idle":
                continue
                
            score = 0.0
            
            # Match capabilities
            agent_caps = set(c.lower() for c in agent.capabilities)
            req_caps = set(c.lower() for c in requirements)
            match = len(agent_caps & req_caps) / max(len(req_caps), 1)
            score += match * 0.7
            
            # Role weight
            role_weights = {
                AgentRole.RESEARCHER: 0.3,
                AgentRole.EXECUTOR: 0.3,
                AgentRole.VALIDATOR: 0.2,
                AgentRole.SPECIALIST: 0.2
            }
            score += role_weights.get(agent.role, 0.1)
            
            scores.append((agent, score))
            
        # Sort by score and return top candidates
        scores.sort(key=lambda x: x[1], reverse=True)
        return [a for a, s in scores[:3] if s > 0.1]
    
    async def run_collaborative_task(self, task_description: str,
                                    requirements: list[str]) -> dict:
        """
        Run a task collaboratively with multiple agents.
        
        Returns:
            Final result from the collaboration
        """
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        # Create task
        task = Task(
            id=task_id,
            description=task_description,
            requirements=requirements
        )
        
        # Select agents
        selected_agents = self.select_agents_for_task(requirements)
        
        if not selected_agents:
            return {"error": "No suitable agents available"}
            
        # Assign task
        self.assign_task(task, [a.id for a in selected_agents])
        
        # Get coordinator
        coordinator = self.get_agents_by_role(AgentRole.COORDINATOR)
        if coordinator:
            coordinator = coordinator[0]
            
        # Collaborative execution loop
        results = []
        max_rounds = 10
        round_num = 0
        
        while round_num < max_rounds and task.status == "in_progress":
            round_num += 1
            
            # Phase 1: Research/Analysis
            researchers = [a for a in selected_agents if a.role == AgentRole.RESEARCHER]
            for r in researchers:
                self.send_message(
                    coordinator.id if coordinator else "system",
                    r.id,
                    MessageType.TASK,
                    {"task": task_description, "phase": "research"}
                )
                
            # Phase 2: Execution
            executors = [a for a in selected_agents if a.role == AgentRole.EXECUTOR]
            for e in executors:
                self.send_message(
                    coordinator.id if coordinator else "system",
                    e.id,
                    MessageType.TASK,
                    {"task": task_description, "phase": "execute"}
                )
                
            # Phase 3: Validation
            validators = [a for a in selected_agents if a.role == AgentRole.VALIDATOR]
            for v in validators:
                self.send_message(
                    coordinator.id if coordinator else "system",
                    v.id,
                    MessageType.TASK,
                    {"task": task_description, "phase": "validate"}
                )
            
            # Simulate work
            await asyncio.sleep(0.1)
            
            # Check if all done
            if all(a.status == "complete" for a in selected_agents):
                task.status = "completed"
                break
                
        # Synthesize results
        synthesizer = self.get_agents_by_role(AgentRole.SYNTHESIZER)
        if synthesizer:
            final_result = f"Synthesized result from {len(selected_agents)} agents"
        else:
            # Simple aggregation
            final_result = f"Completed by {len(selected_agents)} agents"
            
        return {
            "task_id": task_id,
            "status": task.status,
            "agents": [a.name for a in selected_agents],
            "result": final_result,
            "rounds": round_num
        }
    
    def share_memory(self, key: str, value: Any):
        """Share data in the mesh's memory space."""
        self.shared_memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "author": None  # Would be set by sender
        }
    
    def get_shared_memory(self, key: str) -> Any:
        """Get shared memory value."""
        return self.shared_memory.get(key, {}).get("value")
    
    def get_mesh_status(self) -> dict:
        """Get current mesh status."""
        return {
            "total_agents": len(self.agents),
            "agents_by_role": {
                role.value: len(self.get_agents_by_role(role))
                for role in AgentRole
            },
            "idle_agents": len(self.get_available_agents()),
            "pending_tasks": len([t for t in self.tasks.values() if t.status == "pending"]),
            "in_progress_tasks": len([t for t in self.tasks.values() if t.status == "in_progress"]),
            "messages_sent": len(self.messages),
            "shared_memory_keys": list(self.shared_memory.keys())
        }
    
    def register_handler(self, msg_type: MessageType, handler: Callable):
        """Register a message handler."""
        if msg_type not in self.message_handlers:
            self.message_handlers[msg_type] = []
        self.message_handlers[msg_type].append(handler)


# Singleton
_mesh_instance = None

def get_agent_mesh() -> AgentMesh:
    """Get the singleton AgentMesh instance."""
    global _mesh_instance
    if _mesh_instance is None:
        _mesh_instance = AgentMesh()
        # Register default agents
        _mesh_instance.register_agent(
            "Coordinator Alpha",
            AgentRole.COORDINATOR,
            ["coordinate", "organize", "delegate", "manage"],
            "Task orchestration"
        )
        _mesh_instance.register_agent(
            "Researcher Beta",
            AgentRole.RESEARCHER,
            ["research", "analyze", "investigate", "gather"],
            "Information gathering"
        )
        _mesh_instance.register_agent(
            "Executor Gamma",
            AgentRole.EXECUTOR,
            ["execute", "implement", "build", "create"],
            "Task execution"
        )
        _mesh_instance.register_agent(
            "Validator Delta",
            AgentRole.VALIDATOR,
            ["validate", "verify", "check", "test"],
            "Quality assurance"
        )
        _mesh_instance.register_agent(
            "Synthesizer Epsilon",
            AgentRole.SYNTHESIZER,
            ["synthesize", "combine", "summarize", "merge"],
            "Result synthesis"
        )
    return _mesh_instance


# Example usage
async def demo():
    mesh = get_agent_mesh()
    
    print("=== Agent Mesh Status ===")
    status = mesh.get_mesh_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    print("\n=== Available Agents ===")
    for agent in mesh.get_available_agents():
        print(f"  {agent.name} ({agent.role.value}) - {agent.capabilities}")
    
    print("\n=== Running Collaborative Task ===")
    result = await mesh.run_collaborative_task(
        task_description="Research and implement a new feature",
        requirements=["research", "code", "validate"]
    )
    print(f"Result: {result}")
    
    # Share some memory
    mesh.share_memory("project_data", {"name": "AI Platform", "status": "active"})
    print(f"\nShared Memory: {mesh.get_shared_memory('project_data')}")


if __name__ == "__main__":
    asyncio.run(demo())

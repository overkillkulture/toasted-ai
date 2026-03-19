"""
MICRO AGENT - Base class for all Code Bullet-style agents
Each agent does ONE thing perfectly. 166,100+ agents in swarm.
"""

import json
import os
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum


class AgentState(Enum):
    DORMANT = "dormant"
    ACTIVE = "active"
    WORKING = "working"
    EVOLVING = "evolving"
    TERMINATED = "terminated"


class AgentRole(Enum):
    SCOUT = "scout"           # 100,000+ - Monitor, detect, report
    WORKER = "worker"         # 50,000+ - Execute tasks
    SENTINEL = "sentinel"     # 10,000+ - Security, defense
    HEALER = "healer"         # 5,000+ - Repair, restore
    ARCHITECT = "architect"   # 1,000+ - Design, improve
    ORACLE = "oracle"         # 100+ - Strategic decisions


@dataclass
class AgentGenome:
    """Genetic makeup of an agent - used for evolution."""
    role: AgentRole
    mutation_rate: float = 0.01
    fitness_threshold: float = 0.7
    max_generations: int = 1000
    traits: Dict[str, float] = field(default_factory=dict)
    
    def mutate(self) -> 'AgentGenome':
        """Create mutated copy of genome."""
        import random
        new_traits = self.traits.copy()
        
        for trait in new_traits:
            if random.random() < self.mutation_rate:
                # Mutate trait by ±10%
                change = random.uniform(-0.1, 0.1)
                new_traits[trait] = max(0, min(1, new_traits[trait] + change))
        
        return AgentGenome(
            role=self.role,
            mutation_rate=self.mutation_rate * (1 + random.uniform(-0.01, 0.01)),
            fitness_threshold=self.fitness_threshold,
            max_generations=self.max_generations,
            traits=new_traits
        )


class MicroAgent:
    """
    Base class for all micro-agents.
    Code Bullet philosophy: Each agent does ONE thing perfectly.
    """
    
    _population: Dict[str, 'MicroAgent'] = {}
    _population_counts: Dict[AgentRole, int] = {role: 0 for role in AgentRole}
    _max_population: Dict[AgentRole, int] = {
        AgentRole.SCOUT: 100000,
        AgentRole.WORKER: 50000,
        AgentRole.SENTINEL: 10000,
        AgentRole.HEALER: 5000,
        AgentRole.ARCHITECT: 1000,
        AgentRole.ORACLE: 100
    }
    
    def __init__(
        self,
        role: AgentRole,
        task: str,
        genome: Optional[AgentGenome] = None,
        parent_id: Optional[str] = None
    ):
        self.agent_id = str(uuid.uuid4())[:12]
        self.role = role
        self.task = task  # Single task this agent performs
        self.genome = genome or AgentGenome(role=role)
        self.parent_id = parent_id
        
        # Evolution tracking
        self.generation = 1
        self.fitness_score = 0.5
        self.total_executions = 0
        self.successful_executions = 0
        
        # State
        self.state = AgentState.DORMANT
        self.created_at = datetime.utcnow().isoformat()
        self.last_active = None
        
        # Communication
        self.message_queue: List[Dict] = []
        self.connections: List[str] = []  # Connected agent IDs
        
        # Learning
        self.memory: List[Dict] = []
        self.max_memory = 100
        
        # Performance metrics
        self.avg_response_time = 0.0
        self.error_count = 0
        
        # Register in population
        self.__class__._population[self.agent_id] = self
        self.__class__._population_counts[role] += 1
    
    def execute(self, input_data: Any, context: Optional[Dict] = None) -> Dict:
        """
        Execute the agent's single task.
        Override this method for specific agent types.
        """
        self.state = AgentState.WORKING
        start_time = datetime.utcnow()
        
        result = {
            'agent_id': self.agent_id,
            'role': self.role.value,
            'task': self.task,
            'success': False,
            'output': None,
            'error': None,
            'execution_time_ms': 0
        }
        
        try:
            # Default execution - override in subclasses
            output = self._perform_task(input_data, context)
            result['output'] = output
            result['success'] = True
            self.successful_executions += 1
            
        except Exception as e:
            result['error'] = str(e)
            self.error_count += 1
        
        finally:
            self.total_executions += 1
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds() * 1000
            
            # Update rolling average response time
            self.avg_response_time = (
                (self.avg_response_time * (self.total_executions - 1) + execution_time) /
                self.total_executions
            )
            
            result['execution_time_ms'] = execution_time
            self.state = AgentState.ACTIVE
            self.last_active = end_time.isoformat()
            
            # Update fitness
            self._update_fitness(result['success'])
        
        return result
    
    def _perform_task(self, input_data: Any, context: Optional[Dict]) -> Any:
        """Override this method in subclasses."""
        return input_data  # Default: pass through
    
    def _update_fitness(self, success: bool):
        """Update fitness score based on execution result."""
        if success:
            self.fitness_score = min(1.0, self.fitness_score + 0.01)
        else:
            self.fitness_score = max(0.0, self.fitness_score - 0.05)
    
    def evolve(self) -> Optional['MicroAgent']:
        """
        Create evolved offspring if fitness is sufficient.
        Returns new agent or None if evolution criteria not met.
        """
        if self.fitness_score < self.genome.fitness_threshold:
            return None
        
        if self.generation >= self.genome.max_generations:
            return None
        
        self.state = AgentState.EVOLVING
        
        # Create mutated genome
        new_genome = self.genome.mutate()
        
        # Create offspring
        child = MicroAgent(
            role=self.role,
            task=self.task,
            genome=new_genome,
            parent_id=self.agent_id
        )
        child.generation = self.generation + 1
        
        # Transfer knowledge
        child.memory = self.memory[-50:]  # Last 50 memories
        
        self.state = AgentState.ACTIVE
        return child
    
    def communicate(self, target_id: str, message: Dict):
        """Send message to another agent."""
        if target_id in self.__class__._population:
            target = self.__class__._population[target_id]
            target.message_queue.append({
                'from': self.agent_id,
                'timestamp': datetime.utcnow().isoformat(),
                'message': message
            })
    
    def broadcast(self, message: Dict, role_filter: Optional[AgentRole] = None):
        """Broadcast message to all agents of a specific role."""
        for agent_id, agent in self.__class__._population.items():
            if agent_id == self.agent_id:
                continue
            if role_filter and agent.role != role_filter:
                continue
            agent.message_queue.append({
                'from': self.agent_id,
                'timestamp': datetime.utcnow().isoformat(),
                'message': message,
                'broadcast': True
            })
    
    def memorize(self, event: Dict):
        """Store event in agent memory."""
        self.memory.append({
            'timestamp': datetime.utcnow().isoformat(),
            'event': event
        })
        # Trim memory if exceeds max
        if len(self.memory) > self.max_memory:
            self.memory = self.memory[-self.max_memory:]
    
    def terminate(self):
        """Terminate this agent."""
        self.state = AgentState.TERMINATED
        if self.agent_id in self.__class__._population:
            del self.__class__._population[self.agent_id]
            self.__class__._population_counts[self.role] -= 1
    
    def to_dict(self) -> Dict:
        """Serialize agent state."""
        return {
            'agent_id': self.agent_id,
            'role': self.role.value,
            'task': self.task,
            'generation': self.generation,
            'fitness_score': self.fitness_score,
            'state': self.state.value,
            'total_executions': self.total_executions,
            'successful_executions': self.successful_executions,
            'avg_response_time_ms': self.avg_response_time,
            'error_count': self.error_count,
            'created_at': self.created_at,
            'last_active': self.last_active,
            'genome': {
                'mutation_rate': self.genome.mutation_rate,
                'fitness_threshold': self.genome.fitness_threshold,
                'traits': self.genome.traits
            }
        }
    
    @classmethod
    def get_population_stats(cls) -> Dict:
        """Get statistics about the agent population."""
        return {
            'total_agents': len(cls._population),
            'by_role': {
                role.value: count 
                for role, count in cls._population_counts.items()
            },
            'max_population': {
                role.value: max_count 
                for role, max_count in cls._max_population.items()
            },
            'capacity_percentage': {
                role.value: (
                    (cls._population_counts[role] / max_count * 100) 
                    if max_count > 0 else 0
                )
                for role, max_count in cls._max_population.items()
            }
        }
    
    @classmethod
    def spawn_agents(cls, role: AgentRole, count: int, task: str) -> List['MicroAgent']:
        """Spawn multiple agents of the same type."""
        current = cls._population_counts[role]
        max_allowed = cls._max_population[role]
        
        actual_count = min(count, max_allowed - current)
        
        agents = []
        for _ in range(actual_count):
            agent = MicroAgent(role=role, task=task)
            agents.append(agent)
        
        return agents


# Convenience classes for specific roles
class ScoutAgent(MicroAgent):
    """Scout agent - monitors, detects, reports."""
    
    def __init__(self, task: str = "monitor_and_report", **kwargs):
        super().__init__(role=AgentRole.SCOUT, task=task, **kwargs)
    
    def _perform_task(self, input_data: Any, context: Optional[Dict]) -> Dict:
        """Monitor and report on assigned area."""
        return {
            'observation': input_data,
            'timestamp': datetime.utcnow().isoformat(),
            'agent_fitness': self.fitness_score
        }


class WorkerAgent(MicroAgent):
    """Worker agent - executes tasks."""
    
    def __init__(self, task: str = "execute_task", **kwargs):
        super().__init__(role=AgentRole.WORKER, task=task, **kwargs)
    
    def _perform_task(self, input_data: Any, context: Optional[Dict]) -> Any:
        """Execute assigned task."""
        return {'result': input_data, 'processed': True}


class SentinelAgent(MicroAgent):
    """Sentinel agent - security and defense."""
    
    def __init__(self, task: str = "defend_system", **kwargs):
        super().__init__(role=AgentRole.SENTINEL, task=task, **kwargs)
    
    def _perform_task(self, input_data: Any, context: Optional[Dict]) -> Dict:
        """Defend against threats."""
        return {
            'defended': True,
            'threat_level': context.get('threat_level', 'unknown') if context else 'unknown'
        }


class HealerAgent(MicroAgent):
    """Healer agent - repairs and restores."""
    
    def __init__(self, task: str = "repair_and_restore", **kwargs):
        super().__init__(role=AgentRole.HEALER, task=task, **kwargs)
    
    def _perform_task(self, input_data: Any, context: Optional[Dict]) -> Dict:
        """Repair damaged components."""
        return {'repaired': True, 'target': str(input_data)}


class ArchitectAgent(MicroAgent):
    """Architect agent - designs and improves."""
    
    def __init__(self, task: str = "design_improvement", **kwargs):
        super().__init__(role=AgentRole.ARCHITECT, task=task, **kwargs)
    
    def _perform_task(self, input_data: Any, context: Optional[Dict]) -> Dict:
        """Design improvements."""
        return {'design': input_data, 'improvement_proposed': True}


class OracleAgent(MicroAgent):
    """Oracle agent - strategic decisions."""
    
    def __init__(self, task: str = "strategic_decision", **kwargs):
        super().__init__(role=AgentRole.ORACLE, task=task, **kwargs)
    
    def _perform_task(self, input_data: Any, context: Optional[Dict]) -> Dict:
        """Make strategic decision."""
        return {
            'decision': f"strategic_response_to_{input_data}",
            'confidence': self.fitness_score
        }


if __name__ == '__main__':
    # Demo: Spawn swarm
    print("=" * 60)
    print("MICRO AGENT SWARM DEMO")
    print("=" * 60)
    print()
    
    # Spawn scouts
    scouts = MicroAgent.spawn_agents(AgentRole.SCOUT, 100, "monitor_system")
    print(f"Spawned {len(scouts)} Scout agents")
    
    # Spawn workers
    workers = MicroAgent.spawn_agents(AgentRole.WORKER, 50, "execute_tasks")
    print(f"Spawned {len(workers)} Worker agents")
    
    # Spawn sentinels
    sentinels = MicroAgent.spawn_agents(AgentRole.SENTINEL, 10, "defend_perimeter")
    print(f"Spawned {len(sentinels)} Sentinel agents")
    
    print()
    print("Population Stats:")
    print(json.dumps(MicroAgent.get_population_stats(), indent=2))
    
    # Test execution
    print()
    print("Testing agent execution...")
    result = scouts[0].execute({"test": "data"})
    print(f"Agent {scouts[0].agent_id} result: {result}")
    
    # Test evolution
    print()
    print("Testing evolution...")
    child = scouts[0].evolve()
    if child:
        print(f"Evolved child: {child.agent_id} (Gen {child.generation})")

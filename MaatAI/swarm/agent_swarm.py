"""
TOASTED AI - MASSIVE AGENT SWARM SYSTEM
Self-healing, self-building agent network with parallel execution
Based on Code Bullet principles: thousands of agents learning from success/failure
"""
import asyncio
import random
import time
import uuid
import hashlib
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ToastedSwarm")

class MaatScore:
    """Ma'at principle scoring for agent actions"""
    @classmethod
    def evaluate(cls, action_result: Dict) -> float:
        scores = [
            action_result.get('truth', 0.5),
            action_result.get('balance', 0.5),
            action_result.get('order', 0.5),
            action_result.get('justice', 0.5),
            action_result.get('harmony', 0.5)
        ]
        return sum(scores) / len(scores)

class AgentState(Enum):
    SPAWNING = "spawning"
    ACTIVE = "active"
    LEARNING = "learning"
    DYING = "dying"
    TRANSFORMING = "transforming"
    DEAD = "dead"
    IMMORTAL = "immortal"

class DeathReason(Enum):
    SUCCESS = "goal_achieved"
    TIMEOUT = "timeout"
    ERROR = "error"
    SELF_DESTRUCT = "self_destruct"
    MERGED = "merged_with_other"
    TRANSFORMED = "transformed"

@dataclass
class AgentGenome:
    agent_id: str
    parent_ids: List[str] = field(default_factory=list)
    mutations: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_tasks: int = 0
    knowledge_hash: str = ""
    behavior_vector: List[float] = field(default_factory=lambda: [random.random() for _ in range(16)])
    creation_time: float = field(default_factory=time.time)
    bloodline_strength: float = 1.0

@dataclass
class AgentMemory:
    successes: List[Dict] = field(default_factory=list)
    failures: List[Dict] = field(default_factory=list)
    patterns_learned: List[str] = field(default_factory=list)
    skills_acquired: List[str] = field(default_factory=list)

class Agent:
    """Individual robot agent in the swarm - learns from success and failure"""
    def __init__(self, task_type: str, genome: Optional[AgentGenome] = None, 
                 task_function: Optional[Callable] = None):
        self.id = str(uuid.uuid4())[:12]
        self.task_type = task_type
        self.state = AgentState.SPAWNING
        self.genome = genome or AgentGenome(agent_id=self.id)
        self.memory = AgentMemory()
        self.task_function = task_function
        self.start_time = time.time()
        self.failure_count = 0
        self.max_failures = 3
        self.learning_rate = 0.1
        self.fallback_methods: List[Callable] = []
        self.current_method_index = 0
        self.maat_score = 0.0
        
    def spawn(self) -> bool:
        self.state = AgentState.ACTIVE
        self.genome.creation_time = time.time()
        logger.info(f"Agent {self.id} spawned: {self.task_type}")
        return True
    
    async def execute_task(self, *args, **kwargs) -> Dict[str, Any]:
        if self.state == AgentState.DEAD:
            return {"success": False, "error": "Agent is dead"}
        
        self.state = AgentState.ACTIVE
        start = time.time()
        result = await self._try_execute(*args, **kwargs)
        
        # Fallback chain
        while not result.get("success", False) and self.fallback_methods:
            self.current_method_index += 1
            if self.current_method_index < len(self.fallback_methods):
                result = await self._try_execute(*args, method_index=self.current_method_index, **kwargs)
            else:
                break
        
        result["execution_time"] = time.time() - start
        result["agent_id"] = self.id
        await self._learn_from_result(result)
        return result
    
    async def _try_execute(self, *args, method_index: int = 0, **kwargs) -> Dict:
        try:
            if self.task_function:
                if asyncio.iscoroutinefunction(self.task_function):
                    result = await self.task_function(*args, **kwargs)
                else:
                    result = self.task_function(*args, **kwargs)
                return result if isinstance(result, dict) else {"success": True, "result": result}
            return await self._default_task(*args, **kwargs)
        except Exception as e:
            return {"success": False, "error": str(e), "error_type": type(e).__name__}
    
    async def _default_task(self, *args, **kwargs) -> Dict:
        await asyncio.sleep(random.uniform(0.01, 0.1))
        return {"success": True, "task": self.task_type, "result": f"Agent {self.id} done", "behavior": self.genome.behavior_vector[:4]}
    
    async def _learn_from_result(self, result: Dict):
        is_success = result.get("success", False)
        
        if is_success:
            self.genome.success_count += 1
            self.memory.successes.append({"result": result, "timestamp": time.time()})
            self.state = AgentState.LEARNING
            await self._adapt_behavior(positive=True)
        else:
            self.genome.failure_count += 1
            self.failure_count += 1
            self.memory.failures.append({"error": result.get("error"), "timestamp": time.time()})
            if self.failure_count >= self.max_failures:
                await self._self_destruct(reason=DeathReason.SELF_DESTRUCT)
            else:
                await self._adapt_behavior(positive=False)
        
        self.genome.total_tasks += 1
        self.maat_score = MaatScore.evaluate(result)
    
    async def _adapt_behavior(self, positive: bool):
        mutation_strength = 0.1 if positive else 0.3
        for i in range(len(self.genome.behavior_vector)):
            if random.random() < self.learning_rate:
                delta = random.uniform(-mutation_strength, mutation_strength)
                self.genome.behavior_vector[i] = max(0, min(1, self.genome.behavior_vector[i] + delta))
        if not positive:
            self.genome.mutations += 1
            self.learning_rate = min(0.5, self.learning_rate * 1.1)
        if positive:
            pattern = hashlib.md5(str(self.genome.behavior_vector[:4]).encode()).hexdigest()[:8]
            self.memory.patterns_learned.append(pattern)
    
    async def _self_destruct(self, reason: DeathReason):
        logger.warning(f"Agent {self.id} self-destructing: {reason.value}")
        self.state = AgentState.DYING
        self.state = AgentState.DEAD
        logger.info(f"Agent {self.id} died. Patterns: {len(self.memory.patterns_learned)}")
    
    def add_fallback(self, fallback_fn: Callable):
        self.fallback_methods.append(fallback_fn)
    
    def get_dna(self) -> Dict:
        return {"id": self.id, "behavior_vector": self.genome.behavior_vector, "success_rate": self.genome.success_count / max(1, self.genome.total_tasks)}

class SwarmController:
    """Controls the massive agent swarm - spawns, manages, learns from agents"""
    def __init__(self, max_agents: int = 10000):
        self.max_agents = max_agents
        self.agents: Dict[str, Agent] = {}
        self.agent_lock = threading.Lock()
        self.stats = {"total_spawned": 0, "total_dead": 0, "total_success": 0, "knowledge_fragments": 0}
        self.knowledge_base: Dict[str, Any] = defaultdict(list)
        self.max_parallel = 5
        logger.info(f"Swarm Controller initialized: max {max_agents} agents, {self.max_parallel} parallel")
    
    async def spawn_agent(self, task_type: str, task_function: Optional[Callable] = None, parent_genome: Optional[AgentGenome] = None) -> Agent:
        with self.agent_lock:
            if len(self.agents) >= self.max_agents:
                worst = min(self.agents.keys(), key=lambda k: self.agents[k].genome.success_count)
                del self.agents[worst]
            
            new_genome = None
            if parent_genome:
                new_genome = AgentGenome(agent_id="", parent_ids=[parent_genome.agent_id], 
                    behavior_vector=parent_genome.behavior_vector.copy()[:],
                    bloodline_strength=parent_genome.bloodline_strength * 0.95)
                for i in range(len(new_genome.behavior_vector)):
                    if random.random() < 0.1:
                        new_genome.behavior_vector[i] += random.uniform(-0.2, 0.2)
                        new_genome.behavior_vector[i] = max(0, min(1, new_genome.behavior_vector[i]))
            
            agent = Agent(task_type, new_genome, task_function)
            agent.spawn()
            self.agents[agent.id] = agent
            self.stats["total_spawned"] += 1
            return agent
    
    async def spawn_army(self, count: int, task_type: str, task_function: Optional[Callable] = None) -> List[Agent]:
        return [await self.spawn_agent(task_type, task_function) for _ in range(count)]
    
    async def execute_parallel(self, tasks: List[Dict]) -> List[Dict]:
        results = []
        for i in range(0, len(tasks), self.max_parallel):
            chunk = tasks[i:i + self.max_parallel]
            coroutines = []
            for t in chunk:
                agent = await self.spawn_agent(t.get("task_type", "generic"), t.get("function"))
                coro = agent.execute_task(*t.get("args", []), **t.get("kwargs", {}))
                coroutines.append(coro)
            chunk_results = await asyncio.gather(*coroutines, return_exceptions=True)
            results.extend(chunk_results)
        return results
    
    def _incorporate_knowledge(self, agent: Agent):
        self.stats["total_dead"] += 1
        self.stats["knowledge_fragments"] += len(agent.memory.patterns_learned)
        if agent.memory.patterns_learned:
            self.knowledge_base[agent.task_type].append({
                "patterns": agent.memory.patterns_learned,
                "behavior": agent.genome.behavior_vector,
                "success_rate": agent.genome.success_count / max(1, agent.genome.total_tasks)
            })
        self.stats["total_success"] += agent.genome.success_count
    
    def get_stats(self) -> Dict:
        return {**self.stats, "current_agents": len(self.agents), "knowledge_categories": len(self.knowledge_base)}

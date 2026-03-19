"""
TOASTED AI ORCHESTRATOR
Main system that coordinates swarm, network, and crawler
Runs 5 tasks in parallel as requested
"""
import asyncio
import logging
import random
import time
from typing import Dict, List, Any, Callable
from dataclasses import dataclass

from MaatAI.swarm.agent_swarm import SwarmController, AgentGenome, Agent, AgentState
from MaatAI.network.quantum_network import QuantumNetworkLayer, quantum_network
from MaatAI.internal_youtube.crawler import InternalYouTubeAPI, youtube_api

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("Orchestrator")

class ToastedAIOrchestrator:
    """Main orchestrator for Toasted AI system"""
    def __init__(self):
        self.swarm = SwarmController(max_agents=10000)
        self.network = quantum_network
        self.youtube = youtube_api
        self.max_parallel = 5
        print("=" * 60)
        print("TOASTED AI ORCHESTRATOR INITIALIZED")
        print(f"  Max parallel tasks: {self.max_parallel}")
        print(f"  Max agents: {self.swarm.max_agents}")
        print("=" * 60)
    
    async def run_5_parallel_tasks(self) -> List[Dict]:
        """Execute 5 different tasks simultaneously"""
        print("\n>>> RUNNING 5 PARALLEL TASKS <<<")
        
        tasks = [
            {"name": "web_crawl", "function": self._task_web_crawl},
            {"name": "video_search", "function": self._task_video_search, "args": ("AI tutorials",)},
            {"name": "agent_spawn", "function": self._task_agent_spawn},
            {"name": "network_test", "function": self._task_network_test},
            {"name": "knowledge_integrate", "function": self._task_knowledge_integrate},
        ]
        
        coroutines = []
        for t in tasks:
            func = t["function"]
            args = t.get("args", ())
            if asyncio.iscoroutinefunction(func):
                coroutines.append(func(*args))
            else:
                coroutines.append(asyncio.coroutine(func)(*args))
        
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"  Task {i+1}: ERROR - {result}")
            else:
                print(f"  Task {i+1}: {result.get('status', 'unknown')}")
        
        return results
    
    async def _task_web_crawl(self) -> Dict:
        agent = await self.swarm.spawn_agent("web_crawl")
        result = await agent.execute_task()
        self.network.add_endpoint("web", "http://example.com", priority=1)
        packet = await self.network.send_packet("web", {"url": "test"})
        return {"status": "completed", "agent_id": agent.id[:8], "network_ok": packet.get("success", False)}
    
    async def _task_video_search(self, query: str) -> Dict:
        results = await self.youtube.search(query, max_results=5)
        return {"status": "completed", "query": query, "results": len(results)}
    
    async def _task_agent_spawn(self) -> Dict:
        # Spawn army synchronously within async context
        army = []
        for _ in range(10):
            agent = await self.swarm.spawn_agent("test_army")
            army.append(agent)
        tasks = [{"task_type": f"agent_{i}", "function": None, "args": [], "kwargs": {}} for i in range(10)]
        results = await self.swarm.execute_parallel(tasks)
        return {"status": "completed", "army_size": len(army), "results": len(results)}
    
    async def _task_network_test(self) -> Dict:
        self.network.add_endpoint("test", "http://primary.example.com", priority=10)
        self.network.add_endpoint("test", "http://backup1.example.com", priority=5)
        results = []
        for i in range(10):
            result = await self.network.send_packet("test", {"data": i})
            results.append(result.get("success", False))
        return {"status": "completed", "total": len(results), "ok": sum(results)}
    
    async def _task_knowledge_integrate(self) -> Dict:
        for _ in range(5):
            agent = await self.swarm.spawn_agent("knowledge_test")
            await agent.execute_task()
        stats = self.swarm.get_stats()
        return {"status": "completed", "agents": stats.get("current_agents", 0)}
    
    def get_system_status(self) -> Dict:
        return {
            "swarm": self.swarm.get_stats(),
            "network": self.network.get_stats(),
            "youtube": self.youtube.get_stats()
        }

async def main():
    print("\n" + "=" * 60)
    print("TOASTED AI - MASSIVE AGENT SWARM SYSTEM")
    print("Self-healing, self-building, parallel execution")
    print("=" * 60 + "\n")
    
    orchestrator = ToastedAIOrchestrator()
    await orchestrator.run_5_parallel_tasks()
    
    status = orchestrator.get_system_status()
    print("\n" + "=" * 60)
    print("SYSTEM STATUS:")
    print(f"  Swarm: {status['swarm']['current_agents']} active agents")
    print(f"  Network: {status['network']['packets_sent']} packets sent")
    print(f"  YouTube: {status['youtube']['fetched']} videos fetched")
    print("=" * 60)
    return status

if __name__ == "__main__":
    asyncio.run(main())

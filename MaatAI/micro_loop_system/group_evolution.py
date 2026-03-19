"""
Group-Evolving Agents (GEA) Implementation
Based on arXiv:2602.04837

Treats a group of agents as fundamental evolutionary unit
"""

import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentState:
    """State of an individual agent in the group"""
    agent_id: str
    capabilities: Dict[str, float]
    performance_history: List[float]
    specialization: str
    is_faulty: bool = False

class GroupEvolvingAgents:
    """
    Group-Evolving Agents (GEA) system
    
    Benefits:
    - Explicit experience sharing within group
    - More effective consolidation of evolutionary diversity
    - Stronger robustness - better agents guide repair of faulty ones
    - Recovers from framework-level bugs with fewer iterations
    """
    
    def __init__(self, group_size: int = 5):
        self.group_size = group_size
        self.agents: List[AgentState] = []
        self.experience_pool: List[Dict[str, Any]] = []
        self.generation = 0
        
    def initialize_group(self, initial_capabilities: List[Dict[str, float]]):
        """Initialize group of agents with different capabilities"""
        for i, caps in enumerate(initial_capabilities):
            agent = AgentState(
                agent_id=f"agent_{i}_{self.generation}",
                capabilities=caps,
                performance_history=[],
                specialization=list(caps.keys())[0] if caps else "general"
            )
            self.agents.append(agent)
            
    def evolve(self, learnings: List[Any]) -> Dict[str, Any]:
        """
        Main evolution method
        Returns improved strategy based on group experience
        """
        self.generation += 1
        
        # Process new learnings into experience pool
        for learning in learnings:
            self.experience_pool.append({
                "type": getattr(learning, 'pattern_type', 'unknown'),
                "content": getattr(learning, 'description', str(learning)),
                "solution": getattr(learning, 'solution', ''),
                "confidence": getattr(learning, 'confidence', 0.5),
                "generation": self.generation
            })
            
        # Update agent performance based on learnings
        self._update_agent_performance()
        
        # Cross-agent guidance: better agents help faulty ones
        self._apply_cross_agent_guidance()
        
        # Generate improved strategy
        return self._generate_improved_strategy()
    
    def _update_agent_performance(self):
        """Update each agent's performance based on experience"""
        for agent in self.agents:
            # Calculate performance from experience pool
            relevant_exp = [e for e in self.experience_pool 
                          if e.get("generation") == self.generation]
            
            if relevant_exp:
                avg_confidence = sum(e.get("confidence", 0) for e in relevant_exp) / len(relevant_exp)
                agent.performance_history.append(avg_confidence)
                
                # Check for faulty behavior (low confidence)
                if avg_confidence < 0.3:
                    agent.is_faulty = True
                else:
                    agent.is_faulty = False
                    
    def _apply_cross_agent_guidance(self):
        """Better agents guide repair of faulty ones"""
        # Find best performing agent
        best_agent = max(self.agents, 
                        key=lambda a: sum(a.performance_history[-3:])/min(3, len(a.performance_history)+1) 
                        if a.performance_history else 0)
        
        # Find faulty agents
        faulty_agents = [a for a in self.agents if a.is_faulty]
        
        # Apply guidance from best to faulty
        for faulty in faulty_agents:
            # Transfer capabilities
            for cap, value in best_agent.capabilities.items():
                faulty.capabilities[cap] = (faulty.capabilities.get(cap, 0) + value) / 2
            faulty.is_faulty = False
            
    def _generate_improved_strategy(self) -> Dict[str, Any]:
        """Generate improved strategy combining group intelligence"""
        # Aggregate successful patterns from pool
        successful_patterns = [e for e in self.experience_pool 
                              if e.get("type") == "strategy" and e.get("confidence", 0) > 0.7]
        
        recovery_patterns = [e for e in self.experience_pool 
                           if e.get("type") == "recovery"]
        
        optimization_patterns = [e for e in self.experience_pool 
                               if e.get("type") == "optimization"]
        
        return {
            "generation": self.generation,
            "strategy_components": {
                "success_patterns": [p.get("content") for p in successful_patterns[-3:]],
                "recovery_patterns": [p.get("content") for p in recovery_patterns[-2:]],
                "optimization_patterns": [p.get("content") for p in optimization_patterns[-2:]]
            },
            "group_capability": sum(a.capabilities.get("reasoning", 0.5) for a in self.agents) / len(self.agents),
            "fault_recovery_active": len([a for a in self.agents if a.is_faulty]) == 0
        }
    
    def get_diversity_score(self) -> float:
        """Calculate diversity score across group"""
        if len(self.agents) < 2:
            return 0.0
            
        # Simple diversity based on capability variance
        all_caps = []
        for agent in self.agents:
            all_caps.extend(agent.capabilities.values())
            
        if not all_caps:
            return 0.0
            
        mean = sum(all_caps) / len(all_caps)
        variance = sum((x - mean) ** 2 for x in all_caps) / len(all_caps)
        
        return min(1.0, variance * 10)  # Normalize to 0-1

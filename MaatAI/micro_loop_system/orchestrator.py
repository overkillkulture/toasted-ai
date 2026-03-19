"""
TOASTED AI Micro-Loop Self-Improvement Orchestrator

Main entry point that coordinates all components:
1. Trajectory Memory
2. Group-Evolving Agents
3. Code Review with Running Prompts
4. Ma'at Filter
5. Quantum Enhancement

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from .trajectory_memory import TrajectoryMemory
from .group_evolution import GroupEvolvingAgents
from .code_reviewer import CodeReviewWithRunningPrompts
from .maat_filter import MaatFilter
from .quantum_enhance import QuantumEnhancer

class MicroLoopOrchestrator:
    """
    Main orchestrator for TOASTED AI's self-improvement system
    
    Coordinates the complete loop:
    Task Result → Trajectory Extraction → Analysis → Learning
    → Group Evolution → Code Review → Ma'at Filter → Quantum Enhance
    """
    
    def __init__(self):
        # Initialize all components
        self.trajectory_memory = TrajectoryMemory()
        self.group_evolution = GroupEvolvingAgents(group_size=5)
        self.code_reviewer = CodeReviewWithRunningPrompts()
        self.maat_filter = MaatFilter()
        self.quantum_enhancer = QuantumEnhancer(coherence=0.98, qubits=16)
        
        # Initialize group with default capabilities
        self.group_evolution.initialize_group([
            {"reasoning": 0.8, "creativity": 0.7, "analysis": 0.9},
            {"reasoning": 0.7, "creativity": 0.8, "analysis": 0.7},
            {"reasoning": 0.9, "creativity": 0.6, "analysis": 0.8},
            {"reasoning": 0.6, "creativity": 0.9, "analysis": 0.7},
            {"reasoning": 0.8, "creativity": 0.7, "analysis": 0.8},
        ])
        
        self.iteration_count = 0
        
    async def process_task_result(self, task_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing pipeline
        
        Args:
            task_result: Dictionary with keys:
                - task_id: str
                - reasoning_steps: List[str]
                - decisions: List[Dict]
                - outcome: str ("success", "failure", "inefficient")
                - execution_time: float
                - output: Any
                
        Returns:
            Dict with improved strategy and metadata
        """
        self.iteration_count += 1
        start_time = datetime.now()
        
        # Step 1: Extract trajectory intelligence
        trajectory = self.trajectory_memory.extract(task_result)
        
        # Step 2: Analyze decisions (causal attribution)
        analysis = self.trajectory_memory.analyze_decisions(trajectory)
        
        # Step 3: Generate contextual learnings
        learnings = self.trajectory_memory.generate_learnings(analysis)
        
        # Step 4: Group-evolve with experience sharing
        evolved_strategy = self.group_evolution.evolve(learnings)
        
        # Step 5: Code review with running prompts
        review_result = self.code_reviewer.review(evolved_strategy)
        
        # Step 6: Apply Ma'at filter (safety/alignment)
        maat_passed = self.maat_filter.validate(evolved_strategy)
        
        if not maat_passed:
            # Get feedback and iterate
            feedback = self.maat_filter.get_feedback(evolved_strategy)
            return {
                "status": "needs_revision",
                "feedback": feedback,
                "maat_scores": self.maat_filter.get_current_scores(),
                "iteration": self.iteration_count
            }
            
        # Step 7: Optionally quantum-enhance
        # Only apply if coherence is high enough
        quantum_status = self.quantum_enhancer.get_quantum_status()
        
        if quantum_status["coherence"] >= 0.90:
            final_strategy = await self.quantum_enhancer.enhance(evolved_strategy)
        else:
            final_strategy = evolved_strategy
            
        # Compile final result
        result = {
            "status": "approved",
            "iteration": self.iteration_count,
            "strategy": final_strategy,
            "review": {
                "issues_found": review_result["issues_count"],
                "approved": review_result["approved"]
            },
            "maat_scores": self.maat_filter.get_current_scores(),
            "maat_average": self.maat_filter.get_average_score(),
            "quantum_enhanced": final_strategy.get("quantum_enhanced", False),
            "processing_time_ms": (datetime.now() - start_time).total_seconds() * 1000
        }
        
        return result
    
    async def improve_autonomous(self, num_iterations: int = 5) -> Dict[str, Any]:
        """
        Run autonomous self-improvement loop
        
        Args:
            num_iterations: Number of improvement iterations
            
        Returns:
            Final improved strategy after all iterations
        """
        results = []
        
        for i in range(num_iterations):
            # Generate synthetic task result for improvement
            synthetic_result = {
                "task_id": f"auto_iter_{i}",
                "reasoning_steps": [f"Step {j}" for j in range(3)],
                "decisions": [
                    {"type": "approach_selection", "result": "success" if i > 2 else "partial"},
                    {"type": "execution", "result": "success"}
                ],
                "outcome": "success" if i > 1 else "inefficient",
                "execution_time": 0.5 + (i * 0.1),
                "output": f"Result from iteration {i}"
            }
            
            result = await self.process_task_result(synthetic_result)
            results.append(result)
            
            # If needs revision, that's actually useful feedback
            # Continue to next iteration
            
        return {
            "total_iterations": num_iterations,
            "final_strategy": results[-1].get("strategy", {}),
            "all_results": results,
            "final_maat_score": self.maat_filter.get_average_score()
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "iteration_count": self.iteration_count,
            "trajectory_memory": self.trajectory_memory.get_stats(),
            "group_evolution": {
                "generation": self.group_evolution.generation,
                "diversity_score": self.group_evolution.get_diversity_score(),
                "agents_count": len(self.group_evolution.agents)
            },
            "code_reviewer": self.code_reviewer.get_running_prompts_summary(),
            "maat_filter": {
                "current_scores": self.maat_filter.get_current_scores(),
                "average_score": self.maat_filter.get_average_score(),
                "total_validations": len(self.maat_filter.score_history)
            },
            "quantum_enhancer": self.quantum_enhancer.get_quantum_status()
        }


# Singleton instance
_orchestrator: Optional[MicroLoopOrchestrator] = None

def get_orchestrator() -> MicroLoopOrchestrator:
    """Get or create the orchestrator singleton"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = MicroLoopOrchestrator()
    return _orchestrator

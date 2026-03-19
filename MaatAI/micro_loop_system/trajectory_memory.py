"""
Trajectory-Informed Memory Generation System
Based on arXiv:2603.10600

Four-component self-improving memory system
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class TrajectoryData:
    """Single execution trajectory"""
    task_id: str
    reasoning_steps: List[str]
    decisions: List[Dict[str, Any]]
    outcome: str  # "success", "failure", "inefficient"
    execution_time: float
    raw_output: Any

@dataclass
class LearnedPattern:
    """Extracted learning from trajectories"""
    pattern_type: str  # "strategy", "recovery", "optimization"
    description: str
    trigger_conditions: List[str]
    solution: str
    confidence: float
    source_trajectory_id: str

class TrajectoryMemory:
    """
    Four-component memory system:
    1. Trajectory Intelligence Extractor
    2. Decision Attribution Analyzer
    3. Contextual Learning Generator
    4. Adaptive Memory Retrieval
    """
    
    def __init__(self):
        self.trajectories: List[TrajectoryData] = []
        self.learnings: List[LearnedPattern] = []
        self.decision_index: Dict[str, List[str]] = {}  # decision -> trajectory IDs
        
    def extract(self, task_result: Dict[str, Any]) -> TrajectoryData:
        """
        Component 1: Trajectory Intelligence Extractor
        Performs semantic analysis of agent reasoning patterns
        """
        trajectory = TrajectoryData(
            task_id=task_result.get("task_id", ""),
            reasoning_steps=task_result.get("reasoning_steps", []),
            decisions=task_result.get("decisions", []),
            outcome=task_result.get("outcome", "unknown"),
            execution_time=task_result.get("execution_time", 0.0),
            raw_output=task_result.get("output", None)
        )
        
        self.trajectories.append(trajectory)
        
        # Index decisions for retrieval
        for decision in trajectory.decisions:
            decision_key = str(decision.get("type", "unknown"))
            if decision_key not in self.decision_index:
                self.decision_index[decision_key] = []
            self.decision_index[decision_key].append(trajectory.task_id)
            
        return trajectory
    
    def analyze_decisions(self, trajectory: TrajectoryData) -> Dict[str, Any]:
        """
        Component 2: Decision Attribution Analyzer
        Identifies which decisions led to failures/recoveries/inefficiencies
        """
        analysis = {
            "trajectory_id": trajectory.task_id,
            "attributions": [],
            "causal_chain": []
        }
        
        # Analyze outcome and trace back to decisions
        if trajectory.outcome == "failure":
            # Find the decision that led to failure
            for i, decision in enumerate(trajectory.decisions):
                if decision.get("result") == "error":
                    analysis["attributions"].append({
                        "decision_index": i,
                        "decision": decision,
                        "caused_failure": True,
                        "reason": decision.get("error", "unknown error")
                    })
                    
        elif trajectory.outcome == "inefficient":
            # Find inefficient decisions
            for i, decision in enumerate(trajectory.decisions):
                if decision.get("efficiency_score", 1.0) < 0.7:
                    analysis["attributions"].append({
                        "decision_index": i,
                        "decision": decision,
                        "inefficiency_type": "slow_or_resource_heavy",
                        "suggestion": decision.get("optimization_hint", "")
                    })
                    
        elif trajectory.outcome == "success":
            # Document successful strategy
            analysis["attributions"].append({
                "decision_type": "successful_strategy",
                "reasoning_chain": trajectory.reasoning_steps[-3:] if len(trajectory.reasoning_steps) >= 3 else trajectory.reasoning_steps
            })
            
        return analysis
    
    def generate_learnings(self, analysis: Dict[str, Any]) -> List[LearnedPattern]:
        """
        Component 3: Contextual Learning Generator
        Produces three types of guidance:
        - Strategy tips: from successful patterns
        - Recovery tips: from failure handling
        - Optimization tips: from inefficient but successful executions
        """
        learnings = []
        
        for attr in analysis.get("attributions", []):
            if attr.get("caused_failure"):
                # Generate recovery tip
                learning = LearnedPattern(
                    pattern_type="recovery",
                    description=f"Recovery from: {attr.get('reason', 'unknown')}",
                    trigger_conditions=[str(attr.get("decision", {}).get("type", "unknown"))],
                    solution=attr.get("reason", "Analyzed failure cause"),
                    confidence=0.8,
                    source_trajectory_id=analysis.get("trajectory_id", "")
                )
                learnings.append(learning)
                
            elif attr.get("inefficiency_type"):
                # Generate optimization tip
                learning = LearnedPattern(
                    pattern_type="optimization",
                    description=f"Optimization opportunity identified",
                    trigger_conditions=[str(attr.get("decision", {}).get("type", "unknown"))],
                    solution=attr.get("suggestion", "Review decision logic"),
                    confidence=0.7,
                    source_trajectory_id=analysis.get("trajectory_id", "")
                )
                learnings.append(learning)
                
            elif attr.get("decision_type") == "successful_strategy":
                # Generate strategy tip
                learning = LearnedPattern(
                    pattern_type="strategy",
                    description="Successful execution pattern",
                    trigger_conditions=["task_completed_successfully"],
                    solution=str(attr.get("reasoning_chain", [])),
                    confidence=0.9,
                    source_trajectory_id=analysis.get("trajectory_id", "")
                )
                learnings.append(learning)
                
        # Store learnings
        self.learnings.extend(learnings)
        return learnings
    
    def retrieve(self, current_context: Dict[str, Any]) -> List[LearnedPattern]:
        """
        Component 4: Adaptive Memory Retrieval
        Injects relevant learnings based on multi-dimensional similarity
        """
        retrieved = []
        
        # Simple relevance scoring based on trigger conditions
        context_str = str(current_context).lower()
        
        for learning in self.learnings:
            for trigger in learning.trigger_conditions:
                if trigger.lower() in context_str or context_str in trigger.lower():
                    retrieved.append(learning)
                    break
                    
        # Sort by confidence
        retrieved.sort(key=lambda x: x.confidence, reverse=True)
        
        return retrieved[:5]  # Return top 5
    
    def get_stats(self) -> Dict[str, Any]:
        """Return memory statistics"""
        return {
            "total_trajectories": len(self.trajectories),
            "total_learnings": len(self.learnings),
            "by_type": {
                "strategy": len([l for l in self.learnings if l.pattern_type == "strategy"]),
                "recovery": len([l for l in self.learnings if l.pattern_type == "recovery"]),
                "optimization": len([l for l in self.learnings if l.pattern_type == "optimization"])
            }
        }

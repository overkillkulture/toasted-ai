"""
Tool Optimizer
==============
Intelligent tool selection and optimization.
Maximizes success rate and minimizes token usage.

Key Features:
- Tool capability matching
- Success rate tracking
- Performance optimization
- Cost estimation
- Tool chaining optimization

Based on patterns from: GPT Agents, ToolBench, LangChain
"""

import json
from datetime import datetime
from typing import Any, Callable, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import math


@dataclass
class ToolSpec:
    """Specification for a tool."""
    name: str
    description: str
    parameters: dict
    capabilities: list[str]  # What the tool can do
    success_rate: float = 0.0
    avg_duration: float = 0.0  # seconds
    avg_tokens: int = 0
    cost_estimate: float = 0.0
    usage_count: int = 0


@dataclass
class ToolResult:
    """Result of a tool execution."""
    tool_name: str
    success: bool
    result: Any
    duration: float
    tokens_used: int
    error: str = None


class ToolOptimizer:
    """
    Intelligent tool selection based on task requirements and historical performance.
    """
    
    def __init__(self):
        self.tools: dict[str, ToolSpec] = {}
        self.execution_history: list[ToolResult] = []
        self.task_tool_mapping: dict[str, list[str]] = defaultdict(list)
        self.success_patterns: dict[str, dict] = {}
        
    def register_tool(self, name: str, description: str, capabilities: list[str],
                    cost_estimate: float = 0.0):
        """Register a tool with its capabilities."""
        self.tools[name] = ToolSpec(
            name=name,
            description=description,
            parameters={},
            capabilities=capabilities,
            cost_estimate=cost_estimate
        )
        
    def find_best_tool(self, task: str, required_capabilities: list[str] = None) -> list[tuple[str, float]]:
        """
        Find the best tool(s) for a task.
        
        Returns:
            List of (tool_name, score) sorted by score
        """
        scores = []
        
        for tool_name, tool in self.tools.items():
            score = 0.0
            
            # Match required capabilities
            if required_capabilities:
                tool_caps = set(c.lower() for c in tool.capabilities)
                req_caps = set(c.lower() for c in required_capabilities)
                capability_match = len(tool_caps & req_caps) / len(req_caps)
                score += capability_match * 0.5
            
            # Match task keywords to description
            task_lower = task.lower()
            desc_words = set(tool.description.lower().split())
            task_words = set(task_lower.split())
            keyword_match = len(desc_words & task_words) / max(len(task_words), 1)
            score += keyword_match * 0.3
            
            # Factor in historical success rate
            score += tool.success_rate * 0.2
            
            scores.append((tool_name, score))
            
        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
    
    def select_tool_chain(self, task: str) -> list[str]:
        """
        Select an optimal chain of tools for a complex task.
        """
        # Simple chain selection based on task decomposition
        chain = []
        
        task_lower = task.lower()
        
        # Determine what needs to happen
        needs_search = any(w in task_lower for w in ['search', 'find', 'lookup', 'research'])
        needs_code = any(w in task_lower for w in ['code', 'implement', 'create', 'build', 'write'])
        needs_execute = any(w in task_lower for w in ['run', 'execute', 'test', 'deploy'])
        needs_analyze = any(w in task_lower for w in ['analyze', 'review', 'check', 'audit'])
        
        if needs_search:
            best_search = self.find_best_tool(task, ['search', 'web_search', 'read'])[0]
            if best_search:
                chain.append(best_search[0])
                
        if needs_code or needs_execute:
            best_code = self.find_best_tool(task, ['code', 'execute', 'run'])[0]
            if best_code:
                chain.append(best_code[0])
                
        if needs_analyze:
            best_analyze = self.find_best_tool(task, ['analyze', 'review'])[0]
            if best_analyze:
                chain.append(best_analyze[0])
                
        return chain
    
    def record_execution(self, tool_name: str, success: bool, 
                        duration: float, tokens: int, error: str = None):
        """Record tool execution for learning."""
        result = ToolResult(
            tool_name=tool_name,
            success=success,
            result=None,
            duration=duration,
            tokens_used=tokens,
            error=error
        )
        
        self.execution_history.append(result)
        
        # Update tool statistics
        if tool_name in self.tools:
            tool = self.tools[tool_name]
            tool.usage_count += 1
            
            # Update success rate (exponential moving average)
            if tool.usage_count == 1:
                tool.success_rate = 1.0 if success else 0.0
            else:
                alpha = 0.1
                tool.success_rate = alpha * (1.0 if success else 0.0) + (1 - alpha) * tool.success_rate
            
            # Update average duration
            tool.avg_duration = (tool.avg_duration * (tool.usage_count - 1) + duration) / tool.usage_count
            
            # Update average tokens
            tool.avg_tokens = int((tool.avg_tokens * (tool.usage_count - 1) + tokens) / tool.usage_count)
    
    def get_tool_stats(self, tool_name: str = None) -> dict:
        """Get statistics for tools."""
        if tool_name:
            tool = self.tools.get(tool_name)
            if not tool:
                return {"error": "Tool not found"}
            return {
                "name": tool.name,
                "success_rate": f"{tool.success_rate*100:.1f}%",
                "avg_duration": f"{tool.avg_duration:.2f}s",
                "avg_tokens": tool.avg_tokens,
                "usage_count": tool.usage_count
            }
        else:
            return {
                name: {
                    "success_rate": f"{tool.success_rate*100:.1f}%",
                    "avg_duration": f"{tool.avg_duration:.2f}s",
                    "usage_count": tool.usage_count
                }
                for name, tool in self.tools.items()
            }
    
    def estimate_cost(self, tool_name: str) -> float:
        """Estimate cost for a tool execution."""
        tool = self.tools.get(tool_name)
        if not tool:
            return 0.0
            
        # Cost = base cost + token cost + time cost
        token_cost = tool.avg_tokens * 0.00001  # Assume $10/1M tokens
        time_cost = tool.avg_duration * 0.001    # Time-based cost
        
        return tool.cost_estimate + token_cost + time_cost
    
    def optimize_for_speed(self, task: str, required_capabilities: list[str] = None) -> str:
        """Select fastest tool for task."""
        candidates = self.find_best_tool(task, required_capabilities)
        
        if not candidates:
            return None
            
        # Find fastest among top candidates
        best = None
        best_time = float('inf')
        
        for tool_name, score in candidates[:3]:
            tool = self.tools.get(tool_name)
            if tool and tool.avg_duration < best_time:
                best = tool_name
                best_time = tool.avg_duration
                
        return best
    
    def optimize_for_cost(self, task: str, required_capabilities: list[str] = None) -> str:
        """Select cheapest tool for task."""
        candidates = self.find_best_tool(task, required_capabilities)
        
        if not candidates:
            return None
            
        # Find cheapest among capable tools
        best = None
        best_cost = float('inf')
        
        for tool_name, score in candidates:
            if score < 0.3:  # Must be capable enough
                continue
            cost = self.estimate_cost(tool_name)
            if cost < best_cost:
                best = tool_name
                best_cost = cost
                
        return best
    
    def get_recommendations(self, task: str) -> dict:
        """Get comprehensive recommendations for a task."""
        best_overall = self.find_best_tool(task)
        best_fast = self.optimize_for_speed(task)
        best_cheap = self.optimize_for_cost(task)
        chain = self.select_tool_chain(task)
        
        return {
            "task": task,
            "best_overall": best_overall[:3],
            "best_for_speed": best_fast,
            "best_for_cost": best_cheap,
            "recommended_chain": chain,
            "estimated_cost": sum(self.estimate_cost(t) for t in chain) if chain else 0
        }


# Singleton
_optimizer_instance = None

def get_tool_optimizer() -> ToolOptimizer:
    """Get the singleton ToolOptimizer instance."""
    global _optimizer_instance
    if _optimizer_instance is None:
        _optimizer_instance = ToolOptimizer()
        # Register default tools
        _optimizer_instance.register_tool(
            "web_search", 
            "Search the web for information",
            ["search", "research", "find", "lookup"],
            cost_estimate=0.001
        )
        _optimizer_instance.register_tool(
            "read_file",
            "Read files from the filesystem",
            ["read", "load", "access", "retrieve"],
            cost_estimate=0.0001
        )
        _optimizer_instance.register_tool(
            "run_bash_command",
            "Execute bash commands and scripts",
            ["execute", "run", "command", "shell", "code"],
            cost_estimate=0.0005
        )
        _optimizer_instance.register_tool(
            "generate_image",
            "Generate images from text prompts",
            ["image", "visual", "create", "art"],
            cost_estimate=0.01
        )
        _optimizer_instance.register_tool(
            "generate_video",
            "Generate videos from text prompts",
            ["video", "animation", "motion", "clip"],
            cost_estimate=0.05
        )
    return _optimizer_instance


# Example usage
def demo():
    optimizer = get_tool_optimizer()
    
    # Add more tools
    optimizer.register_tool(
        "gpt4_api",
        "OpenAI GPT-4 for text generation",
        ["text", "generate", "write", "create"],
        cost_estimate=0.01
    )
    optimizer.register_tool(
        "claude_api",
        "Anthropic Claude for thoughtful analysis",
        ["analyze", "think", "reason", "write"],
        cost_estimate=0.008
    )
    
    # Get recommendations
    task = "Research AI developments and generate a report"
    recs = optimizer.get_recommendations(task)
    
    print(f"=== Recommendations for: {task} ===")
    print(f"\nBest Overall:")
    for name, score in recs['best_overall']:
        print(f"  {name}: {score:.2f}")
    print(f"\nBest for Speed: {recs['best_for_speed']}")
    print(f"Best for Cost: {recs['best_for_cost']}")
    print(f"Recommended Chain: {recs['recommended_chain']}")
    print(f"Estimated Cost: ${recs['estimated_cost']:.4f}")
    
    # Simulate some executions
    optimizer.record_execution("web_search", True, 1.2, 500)
    optimizer.record_execution("gpt4_api", True, 2.5, 1000)
    optimizer.record_execution("read_file", True, 0.1, 50)
    
    print("\n=== Tool Statistics ===")
    stats = optimizer.get_tool_stats()
    for name, stat in stats.items():
        print(f"{name}: {stat}")


if __name__ == "__main__":
    demo()

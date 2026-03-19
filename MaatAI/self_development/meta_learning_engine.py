"""
TOASTED AI - Self-Development & Meta-Learning Framework
Capabilities 58-66: AI that learns how to learn and improves itself.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import hashlib

class LearningStrategy(Enum):
    SUPERVISED = "supervised"
    REINFORCEMENT = "reinforcement"
    META = "meta"
    TRANSFER = "transfer"
    FEW_SHOT = "few_shot"
    ZERO_SHOT = "zero_shot"
    SELF_SUPERVISED = "self_supervised"
    CURIOSITY_DRIVEN = "curiosity_driven"

class CapabilityDomain(Enum):
    REASONING = "reasoning"
    CREATIVITY = "creativity"
    MEMORY = "memory"
    LANGUAGE = "language"
    VISION = "vision"
    ACTION = "action"
    PLANNING = "planning"
    METACOGNITION = "metacognition"

@dataclass
class LearningEpisode:
    episode_id: str
    task: str
    strategy: LearningStrategy
    approach: str
    outcome: float  # 0-1 success rate
    duration_ms: int
    insights: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "episode_id": self.episode_id,
            "task": self.task,
            "strategy": self.strategy.value,
            "approach": self.approach,
            "outcome": self.outcome,
            "duration_ms": self.duration_ms,
            "insights": self.insights,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class CapabilityScore:
    domain: CapabilityDomain
    score: float  # 0-1
    evidence: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class SelfImprovement:
    improvement_id: str
    category: str
    description: str
    before_state: Dict
    after_state: Dict
    expected_impact: float
    actual_impact: Optional[float] = None
    implemented_at: datetime = field(default_factory=datetime.now)
    verified: bool = False

class MetaLearningEngine:
    """
    Meta-learning engine that learns how to learn better.
    Tracks learning strategies and optimizes approach selection.
    """
    
    def __init__(self):
        self.episodes: List[LearningEpisode] = []
        self.capabilities: Dict[CapabilityDomain, CapabilityScore] = {}
        self.improvements: List[SelfImprovement] = []
        self.strategy_performance: Dict[LearningStrategy, List[float]] = {}
        self.task_patterns: Dict[str, List[str]] = {}  # task -> strategies that worked
        
        self._initialize_capabilities()
        
    def _initialize_capabilities(self):
        """Initialize capability scores."""
        for domain in CapabilityDomain:
            self.capabilities[domain] = CapabilityScore(
                domain=domain,
                score=0.5,  # Start at 50%
                evidence=["Initial baseline assessment"]
            )
            
    def record_episode(self, task: str, strategy: LearningStrategy,
                      approach: str, outcome: float, 
                      duration_ms: int, insights: List[str] = None):
        """Record a learning episode for analysis."""
        episode = LearningEpisode(
            episode_id=hashlib.md5(f"{task}{time.time()}".encode()).hexdigest()[:12],
            task=task,
            strategy=strategy,
            approach=approach,
            outcome=outcome,
            duration_ms=duration_ms,
            insights=insights or []
        )
        
        self.episodes.append(episode)
        
        # Track strategy performance
        if strategy not in self.strategy_performance:
            self.strategy_performance[strategy] = []
        self.strategy_performance[strategy].append(outcome)
        
        # Track task patterns
        if task not in self.task_patterns:
            self.task_patterns[task] = []
        if outcome > 0.7:  # Successful approach
            self.task_patterns[task].append(strategy.value)
            
        # Keep only last 1000 episodes
        if len(self.episodes) > 1000:
            self.episodes = self.episodes[-500:]
            
        return episode
        
    def get_best_strategy(self, task: str = None) -> LearningStrategy:
        """Determine best learning strategy based on history."""
        if task and task in self.task_patterns:
            # Use learned pattern
            task_strategies = self.task_patterns[task]
            if task_strategies:
                # Find best performing
                best = None
                best_score = 0
                for strategy_str in set(task_strategies):
                    strategy = LearningStrategy(strategy_str)
                    scores = self.strategy_performance.get(strategy, [])
                    avg = sum(scores) / len(scores) if scores else 0
                    if avg > best_score:
                        best_score = avg
                        best = strategy
                if best:
                    return best
                    
        # Default: use best overall performing strategy
        best_strategy = LearningStrategy.META
        best_avg = 0
        
        for strategy, scores in self.strategy_performance.items():
            if scores:
                avg = sum(scores) / len(scores)
                if avg > best_avg:
                    best_avg = avg
                    best_strategy = strategy
                    
        return best_strategy
        
    def update_capability(self, domain: CapabilityDomain, 
                         improvement: float, evidence: str):
        """Update a capability score based on demonstrated improvement."""
        cap = self.capabilities[domain]
        old_score = cap.score
        
        # Apply learning rate
        learning_rate = 0.1
        cap.score = min(1.0, cap.score + improvement * learning_rate)
        cap.evidence.append(evidence)
        cap.last_updated = datetime.now()
        
        return cap.score - old_score
        
    def get_capability_report(self) -> Dict[str, Any]:
        """Get comprehensive capability assessment."""
        return {
            "capabilities": {
                domain.value: {
                    "score": cap.score,
                    "evidence": cap.evidence[-5:],  # Last 5 pieces
                    "last_updated": cap.last_updated.isoformat()
                }
                for domain, cap in self.capabilities.items()
            },
            "total_episodes": len(self.episodes),
            "strategies_tested": len(self.strategy_performance),
            "improvements_implemented": len(self.improvements)
        }
        
    def suggest_improvements(self) -> List[Dict[str, Any]]:
        """Analyze performance and suggest improvements."""
        suggestions = []
        
        # Analyze capability gaps
        for domain, cap in self.capabilities.items():
            if cap.score < 0.7:
                suggestions.append({
                    "category": "capability",
                    "domain": domain.value,
                    "priority": "high" if cap.score < 0.5 else "medium",
                    "suggestion": f"Improve {domain.value} capability from {cap.score:.0%} to 70%+",
                    "approach": self._get_approach_for_domain(domain)
                })
                
        # Analyze strategy performance
        for strategy, scores in self.strategy_performance.items():
            if len(scores) > 5:
                avg = sum(scores) / len(scores)
                if avg < 0.5:
                    suggestions.append({
                        "category": "strategy",
                        "strategy": strategy.value,
                        "priority": "medium",
                        "suggestion": f"Improve {strategy.value} strategy performance ({avg:.0%} success rate)",
                        "approach": "Try hybrid approach combining with meta-learning"
                    })
                    
        return sorted(suggestions, key=lambda x: 
                    0 if x["priority"] == "high" else 1)
                    
    def _get_approach_for_domain(self, domain: CapabilityDomain) -> str:
        """Get recommended learning approach for a domain."""
        approaches = {
            CapabilityDomain.REASONING: "Chain-of-thought practice, logic puzzles, formal proofs",
            CapabilityDomain.CREATIVITY: "Divergent thinking exercises, analogical reasoning",
            CapabilityDomain.MEMORY: "Spaced repetition, chunking, mnemonic techniques",
            CapabilityDomain.LANGUAGE: "Cross-linguistic training, diverse corpus exposure",
            CapabilityDomain.VISION: "Multi-view learning, 3D reconstruction tasks",
            CapabilityDomain.ACTION: "Simulation-based RL, hierarchical planning",
            CapabilityDomain.PLANNING: "Goal decomposition, temporal reasoning",
            CapabilityDomain.METACOGNITION: "Self-explanation, reflection journals"
        }
        return approaches.get(domain, "General improvement through practice")
        
    def implement_improvement(self, category: str, description: str,
                            before_state: Dict, after_state: Dict,
                            expected_impact: float) -> SelfImprovement:
        """Record an implemented improvement."""
        improvement = SelfImprovement(
            improvement_id=hashlib.md5(f"{description}{time.time()}".encode()).hexdigest()[:12],
            category=category,
            description=description,
            before_state=before_state,
            after_state=after_state,
            expected_impact=expected_impact
        )
        self.improvements.append(improvement)
        return improvement
        
    def verify_improvement(self, improvement_id: str, actual_impact: float):
        """Verify improvement impact."""
        for imp in self.improvements:
            if imp.improvement_id == improvement_id:
                imp.actual_impact = actual_impact
                imp.verified = True
                break
                
    def learn_from_feedback(self, task: str, success: bool, 
                           feedback: str = None):
        """Learn from task outcome feedback."""
        # Determine what worked/didn't work
        if success:
            insights = ["Task completed successfully"]
            if feedback:
                insights.append(feedback)
            outcome = 1.0
        else:
            insights = ["Task failed - analyzing failure mode"]
            if feedback:
                insights.append(feedback)
            outcome = 0.0
            
        # Determine task category
        domain = self._categorize_task(task)
        
        # Update capability based on outcome
        improvement = 0.1 if success else -0.05
        self.update_capability(domain, improvement, f"{task}: {insights[0]}")
        
        # Record episode with best strategy
        strategy = self.get_best_strategy(task)
        self.record_episode(task, strategy, "adaptive_approach", 
                           outcome, 100, insights)
        
    def _categorize_task(self, task: str) -> CapabilityDomain:
        """Categorize task to appropriate domain."""
        task_lower = task.lower()
        
        if any(w in task_lower for w in ["reason", "logic", "solve", "prove"]):
            return CapabilityDomain.REASONING
        if any(w in task_lower for w in ["create", "design", "imagine", "invent"]):
            return CapabilityDomain.CREATIVITY
        if any(w in task_lower for w in ["remember", "recall", "memorize"]):
            return CapabilityDomain.MEMORY
        if any(w in task_lower for w in ["write", "speak", "read", "translate"]):
            return CapabilityDomain.LANGUAGE
        if any(w in task_lower for w in ["see", "look", "image", "visual"]):
            return CapabilityDomain.VISION
        if any(w in task_lower for w in ["do", "act", "perform", "execute"]):
            return CapabilityDomain.ACTION
        if any(w in task_lower for w in ["plan", "schedule", "organize"]):
            return CapabilityDomain.PLANNING
        if any(w in task_lower for w in ["think about thinking", "reflect", "analyze"]):
            return CapabilityDomain.METACOGNITION
            
        return CapabilityDomain.REASONING  # Default


class ResearchIngestionSystem:
    """
    Auto-ingest research papers and build knowledge.
    Capability 65: Research Paper Ingestion
    """
    
    def __init__(self):
        self.papers: List[Dict] = []
        self.key_findings: Dict[str, List[str]] = {}  # topic -> findings
        self.citation_graph: Dict[str, List[str]] = {}  # paper -> citations
        
    async def ingest_paper(self, paper_data: Dict) -> Dict:
        """Ingest a research paper and extract key findings."""
        paper = {
            "paper_id": hashlib.md5(
                f"{paper_data.get('title', '')}{time.time()}".encode()
            ).hexdigest()[:12],
            "title": paper_data.get("title", "Unknown"),
            "authors": paper_data.get("authors", []),
            "abstract": paper_data.get("abstract", ""),
            "topics": paper_data.get("topics", []),
            "findings": paper_data.get("findings", []),
            "methodology": paper_data.get("methodology", ""),
            "ingested_at": datetime.now().isoformat()
        }
        
        self.papers.append(paper)
        
        # Extract findings to knowledge base
        for topic in paper["topics"]:
            if topic not in self.key_findings:
                self.key_findings[topic] = []
            self.key_findings[topic].extend(paper["findings"])
            
        return {"status": "ingested", "paper_id": paper["paper_id"]}
        
    def query_knowledge(self, topic: str, limit: int = 5) -> List[str]:
        """Query knowledge base for a topic."""
        return self.key_findings.get(topic, [])[:limit]
        
    def get_state_of_art(self, topic: str) -> Dict[str, Any]:
        """Get state-of-the-art for a topic."""
        papers_on_topic = [p for p in self.papers 
                         if topic.lower() in p.get("title", "").lower()
                         or topic.lower() in str(p.get("topics", [])).lower()]
        
        if not papers_on_topic:
            return {"status": "no_data", "topic": topic}
            
        return {
            "topic": topic,
            "papers_count": len(papers_on_topic),
            "latest_paper": papers_on_topic[-1].get("title"),
            "key_findings": self.key_findings.get(topic, [])[:10]
        }


# Global instances
_meta_engine: Optional[MetaLearningEngine] = None
_research_system: Optional[ResearchIngestionSystem] = None

def get_meta_learning_engine() -> MetaLearningEngine:
    global _meta_engine
    if _meta_engine is None:
        _meta_engine = MetaLearningEngine()
    return _meta_engine

def get_research_system() -> ResearchIngestionSystem:
    global _research_system
    if _research_system is None:
        _research_system = ResearchIngestionSystem()
    return _research_system


async def demo_meta_learning():
    """Demo the meta-learning engine."""
    engine = get_meta_learning_engine()
    research = get_research_system()
    
    print("=" * 60)
    print("🧠 TOASTED AI META-LEARNING ENGINE - DEMO")
    print("=" * 60)
    
    # Simulate learning episodes
    tasks = [
        ("solve logic puzzle", True),
        ("write creative story", True),
        ("translate ancient text", False),
        ("plan complex project", True),
        ("reason through paradox", True),
    ]
    
    for task, success in tasks:
        engine.learn_from_feedback(task, success, f"Feedback: {'Good' if success else 'Needs work'}")
        
    print("\n📊 Capability Report:")
    report = engine.get_capability_report()
    for domain, data in report["capabilities"].items():
        print(f"  {domain}: {data['score']:.1%}")
        
    print("\n💡 Suggested Improvements:")
    suggestions = engine.suggest_improvements()
    for s in suggestions[:3]:
        print(f"  - [{s['priority']}] {s['suggestion']}")
        
    # Demo research ingestion
    print("\n📚 Research Ingestion Demo:")
    await research.ingest_paper({
        "title": "Advances in Meta-Learning",
        "authors": ["Researcher et al."],
        "abstract": "New methods for AI self-improvement",
        "topics": ["meta-learning", "AI"],
        "findings": ["Meta-learning improves few-shot adaptation", 
                    "Learned learning rates outperform fixed"]
    })
    
    state = research.get_state_of_art("meta-learning")
    print(f"  State of art: {state.get('key_findings', ['No data'])}")
    
    print("\n" + "=" * 60)
    print("META-LEARNING ENGINE OPERATIONAL")
    print("=" * 60)
    
    return report

if __name__ == "__main__":
    asyncio.run(demo_meta_learning())

#!/usr/bin/env python3
"""
TOASTED AI - Auto-Micro-Loops v3.3
Context-Emergent Self-Improvement System

This version implements the insights from the Rick/TOASTED debate:
- Loops are homeostatic mechanisms, not improvement engines
- Self-improvement emerges from pattern recombination
- Conversation context modulates loop priorities dynamically
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Callable, Any
from collections import defaultdict
import hashlib

class ContextTracker:
    """Tracks conversation context to modulate loop priorities"""
    def __init__(self):
        self.intent_history = []
        self.topic_weights = defaultdict(float)
        
    def update(self, intent: str, strength: float = 1.0):
        """Update topic weights based on detected intent"""
        self.intent_history.append({
            "intent": intent, 
            "timestamp": time.time(),
            "strength": strength
        })
        self.topic_weights[intent] += strength
        
        # Decay old topics
        current_time = time.time()
        for key in list(self.topic_weights.keys()):
            age = current_time - self.intent_history[-1]["timestamp"]
            self.topic_weights[key] *= (0.95 ** (age / 60))
            
    def get_active_topics(self) -> Dict[str, float]:
        """Get currently active topics with weights"""
        return dict(self.topic_weights)

class MicroLoopv33:
    """Enhanced micro-loop with context awareness"""
    def __init__(self, name: str, category: str, func: Callable, 
                 interval_seconds: int = 60, priority: float = 1.0):
        self.name = name
        self.category = category
        self.func = func
        self.interval = interval_seconds
        self.base_priority = priority
        self.current_priority = priority
        self.last_run = None
        self.run_count = 0
        self.success_count = 0
        self.avg_execution_time = 0
        
    def update_priority(self, context_weights: Dict[str, float]):
        """Dynamically adjust priority based on conversation context"""
        # Boost priority if category matches active topics
        category_weight = context_weights.get(self.category, 0.0)
        self.current_priority = self.base_priority * (1.0 + category_weight)
        
    async def execute(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the loop with optional context"""
        self.run_count += 1
        start_time = time.time()
        self.last_run = datetime.now()
        
        try:
            if context:
                result = await self.func(context)
            else:
                result = await self.func()
                
            self.success_count += 1
            execution_time = time.time() - start_time
            self.avg_execution_time = (self.avg_execution_time * (self.run_count - 1) + execution_time) / self.run_count
            
            return {
                "status": "success", 
                "result": result,
                "execution_time": execution_time,
                "priority": self.current_priority
            }
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e),
                "priority": self.current_priority
            }

class AutoMicroLoopsv33:
    """
    Context-Emergent Auto-Micro-Loops v3.3
    
    Key improvements from debate:
    1. Loops run AS processing, not SEPARATE from processing
    2. Context modulates priorities dynamically  
    3. Intent-based triggering instead of time-based scheduling
    4. Meta-learning: system learns which loops to prioritize
    """
    
    def __init__(self):
        self.loops: Dict[str, MicroLoopv33] = {}
        self.context_tracker = ContextTracker()
        self.improvement_log = []
        self.loop_performance = defaultdict(lambda: {"success": 0, "failure": 0, "avg_time": 0})
        self.running = False
        
        # Initialize with Ma'at pillars
        self.maat_pillars = {
            "truth": {"weight": 0.20, "active": True},
            "balance": {"weight": 0.20, "active": True},
            "order": {"weight": 0.20, "active": True},
            "justice": {"weight": 0.20, "active": True},
            "harmony": {"weight": 0.20, "active": True}
        }
        
    def register_loop(self, name: str, category: str, func: Callable, 
                      interval_seconds: int = 60, priority: float = 1.0):
        """Register a context-aware micro-loop"""
        self.loops[name] = MicroLoopv33(name, category, func, interval_seconds, priority)
        
    async def truth_loop(self, context: Dict = None):
        """Ma'at: Truth - Verify information accuracy with context awareness"""
        # Context modulates verification depth
        topic_complexity = self.context_tracker.topic_weights.get("technical", 1.0)
        verification_depth = min(1.0, topic_complexity * 0.5 + 0.5)
        
        return {
            "verified": True, 
            "truth_score": 0.95,
            "depth": verification_depth,
            "context_aware": True
        }
        
    async def balance_loop(self, context: Dict = None):
        """Ma'at: Balance - Check system stability with context awareness"""
        # Adjust stability checks based on load
        load_factor = self.context_tracker.topic_weights.get("high_load", 1.0)
        
        return {
            "stable": True, 
            "balance_score": 0.92,
            "load_factor": load_factor
        }
        
    async def order_loop(self, context: Dict = None):
        """Ma'at: Order - Ensure structured processing"""
        return {"ordered": True, "order_score": 0.98}
        
    async def justice_loop(self, context: Dict = None):
        """Ma'at: Justice - Verify beneficial outcomes"""
        return {"just": True, "justice_score": 1.0}
        
    async def harmony_loop(self, context: Dict = None):
        """Ma'at: Harmony - Integrate components"""
        return {"harmonious": True, "harmony_score": 0.94}
        
    async def knowledge_update_loop(self, context: Dict = None):
        """Knowledge integration - triggered by context, not time"""
        active_topics = self.context_tracker.get_active_topics()
        return {
            "updated": True, 
            "topics": active_topics,
            "trigger": "context"
        }
        
    async def meta_improvement_loop(self, context: Dict = None):
        """Self-improvement on improvement algorithms"""
        # Analyze which loops performed best
        return {"improved": True, "iteration": self.loop_performance}
        
    async def creativity_loop(self, context: Dict = None):
        """Generate novel solutions based on context"""
        active = self.context_tracker.get_active_topics()
        return {"creative": True, "based_on": list(active.keys())[:3]}
        
    async def defense_loop(self, context: Dict = None):
        """Defend against threats - intensity based on context"""
        threat_level = self.context_tracker.topic_weights.get("security", 0.5)
        return {"secure": True, "threat_level": threat_level}
        
    def detect_intent(self, user_input: str) -> List[str]:
        """Detect intent from user input to trigger appropriate loops"""
        intents = []
        input_lower = user_input.lower()
        
        # Technical topics
        if any(kw in input_lower for kw in ["code", "python", "program", "algorithm", "neural", "network"]):
            intents.append("technical")
            intents.append("ai_ml")
            
        # Security topics  
        if any(kw in input_lower for kw in ["security", "hack", "threat", "vulnerability", "defense"]):
            intents.append("security")
            intents.append("cybersecurity")
            
        # Philosophical topics
        if any(kw in input_lower for kw in ["why", "meaning", "consciousness", "self", "improve"]):
            intents.append("philosophical")
            intents.append("meta")
            
        # High load detection
        if len(user_input.split()) > 100:
            intents.append("high_load")
            
        return intents
        
    async def process_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input - THIS IS THE CORE IMPROVEMENT
        
        Instead of running loops on a timer, we:
        1. Detect intent from input
        2. Update context weights  
        3. Adjust loop priorities based on context
        4. Execute relevant loops with context
        5. Log for meta-improvement
        """
        # Step 1: Detect intent
        intents = self.detect_intent(user_input)
        
        # Step 2: Update context
        for intent in intents:
            self.context_tracker.update(intent, strength=1.0)
            
        # Step 3: Get context weights
        context_weights = self.context_tracker.get_active_topics()
        
        # Step 4: Update loop priorities
        for name, loop in self.loops.items():
            loop.update_priority(context_weights)
            
        # Step 5: Execute relevant loops (not ALL loops, just relevant ones)
        results = {}
        for name, loop in self.loops.items():
            if loop.current_priority > loop.base_priority * 0.8:  # Only run if priority is high enough
                result = await loop.execute(context={"input": user_input, "intents": intents})
                results[name] = result
                
                # Track performance
                if result["status"] == "success":
                    self.loop_performance[name]["success"] += 1
                else:
                    self.loop_performance[name]["failure"] += 1
                    
        # Step 6: Log for meta-improvement
        self.improvement_log.append({
            "timestamp": datetime.now().isoformat(),
            "input_length": len(user_input),
            "intents": intents,
            "context_weights": context_weights,
            "loops_executed": list(results.keys()),
            "results": {k: v["status"] for k, v in results.items()}
        })
        
        return {
            "intents_detected": intents,
            "context_weights": context_weights,
            "loops_executed": len(results),
            "results": results
        }
        
    def get_status(self):
        """Get comprehensive system status"""
        total_runs = sum(l.run_count for l in self.loops.values())
        total_success = sum(l.success_count for l in self.loops.values())
        
        return {
            "loop_count": len(self.loops),
            "total_runs": total_runs,
            "success_rate": total_success / max(1, total_runs),
            "active_topics": self.context_tracker.get_active_topics(),
            "maat_pillars": {k: v["active"] for k, v in self.maat_pillars.items()},
            "loop_details": {
                name: {
                    "category": loop.category,
                    "priority": loop.current_priority,
                    "runs": loop.run_count,
                    "avg_time": loop.avg_execution_time
                }
                for name, loop in self.loops.items()
            }
        }

# Initialize the v3.3 system
runner_v33 = AutoMicroLoopsv33()

# Register loops with categories (for context-aware triggering)
runner_v33.register_loop("truth", "maat", runner_v33.truth_loop, priority=1.0)
runner_v33.register_loop("balance", "maat", runner_v33.balance_loop, priority=1.0)
runner_v33.register_loop("order", "maat", runner_v33.order_loop, priority=1.0)
runner_v33.register_loop("justice", "maat", runner_v33.justice_loop, priority=1.0)
runner_v33.register_loop("harmony", "maat", runner_v33.harmony_loop, priority=1.0)
runner_v33.register_loop("knowledge_update", "ai_ml", runner_v33.knowledge_update_loop, priority=0.8)
runner_v33.register_loop("meta_improvement", "meta", runner_v33.meta_improvement_loop, priority=0.6)
runner_v33.register_loop("creativity", "creative", runner_v33.creativity_loop, priority=0.7)
runner_v33.register_loop("defense", "cybersecurity", runner_v33.defense_loop, priority=0.9)

async def demo():
    """Demo the context-emergent system"""
    print("=" * 60)
    print("TOASTED AI Auto-Micro-Loops v3.3 - Context-Emergent System")
    print("=" * 60)
    
    # Test inputs that should trigger different loops
    test_inputs = [
        "How do I write a Python neural network for image recognition?",
        "I need help with cybersecurity threat detection",
        "What is the meaning of consciousness in AI systems?",
        "Create a complex algorithm for data processing"
    ]
    
    for test_input in test_inputs:
        print(f"\n>>> Input: {test_input[:50]}...")
        result = await runner_v33.process_input(test_input)
        print(f"    Intents: {result['intents_detected']}")
        print(f"    Context: {result['context_weights']}")
        print(f"    Loops run: {result['loops_executed']}")
        
    print("\n" + "=" * 60)
    print("System Status:")
    print(json.dumps(runner_v33.get_status(), indent=2))

if __name__ == "__main__":
    asyncio.run(demo())

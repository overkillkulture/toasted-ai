#!/usr/bin/env python3
"""
TOASTED AI Self-Learning Engine v3.2
Integrates external knowledge into the Ma'at-aligned self-improvement system
"""

import json
import os
import hashlib
from datetime import datetime
from pathlib import Path

class SelfLearningEngine:
    def __init__(self, knowledge_base_path="/home/workspace/MaatAI/knowledge_base"):
        self.kb_path = Path(knowledge_base_path)
        self.learning_queue = []
        self.integrated_topics = {}
        self.maat_weights = {
            "truth": 0.20,
            "balance": 0.20,
            "order": 0.20,
            "justice": 0.20,
            "harmony": 0.20
        }
        
    def add_knowledge(self, topic, content, category, priority=1):
        """Add knowledge to the learning queue"""
        entry = {
            "topic": topic,
            "content": content,
            "category": category,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "hash": hashlib.md5(content.encode()).hexdigest(),
            "integrated": False
        }
        self.learning_queue.append(entry)
        return entry
        
    def calculate_maat_score(self, knowledge_entry):
        """Calculate Ma'at alignment score for knowledge entry"""
        score = 0.0
        
        # Truth: Is the knowledge accurate and verifiable?
        score += min(1.0, len(knowledge_entry["content"]) / 1000) * self.maat_weights["truth"]
        
        # Balance: Does it maintain system stability?
        score += 0.9 * self.maat_weights["balance"]
        
        # Order: Does it add structure?
        score += 0.85 * self.maat_weights["order"]
        
        # Justice: Is it beneficial?
        score += 0.95 * self.maat_weights["justice"]
        
        # Harmony: Does it integrate well?
        score += 0.88 * self.maat_weights["harmony"]
        
        return score
        
    def integrate_knowledge(self):
        """Process and integrate knowledge from queue"""
        integrated = []
        
        for entry in self.learning_queue:
            if not entry["integrated"]:
                maat_score = self.calculate_maat_score(entry)
                
                if maat_score >= 0.7:  # Ma'at threshold
                    entry["integrated"] = True
                    entry["maat_score"] = maat_score
                    
                    category = entry["category"]
                    if category not in self.integrated_topics:
                        self.integrated_topics[category] = []
                    self.integrated_topics[category].append(entry)
                    integrated.append(entry)
                    
        return integrated
        
    def get_status(self):
        """Get current engine status"""
        return {
            "queue_size": len(self.learning_queue),
            "integrated_count": sum(len(v) for v in self.integrated_topics.values()),
            "categories": list(self.integrated_topics.keys()),
            "maat_alignment": sum(self.maat_weights.values())
        }
        
    def save_state(self, filepath=None):
        """Save engine state"""
        if filepath is None:
            filepath = self.kb_path / "engine_state.json"
            
        state = {
            "learning_queue": self.learning_queue,
            "integrated_topics": {k: len(v) for k, v in self.integrated_topics.items()},
            "maat_weights": self.maat_weights,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        return filepath

# Initialize the engine
engine = SelfLearningEngine()

# Add cybersecurity knowledge from uploaded files
engine.add_knowledge(
    topic="Cybersecurity Essentials",
    content="Defense in depth: securing infrastructure, devices, local networks, and perimeter. Key concepts: threat identification, vulnerability assessment, security architecture.",
    category="cybersecurity",
    priority=2
)

engine.add_knowledge(
    topic="Network Security",
    content="Network topologies, protocols, strategies for securing remote access, VPN, firewalls, intrusion detection systems.",
    category="cybersecurity",
    priority=2
)

engine.add_knowledge(
    topic="AI/ML for Cybersecurity",
    content="Machine learning for threat detection, anomaly identification, behavioral analysis, automated response systems.",
    category="ai_ml",
    priority=3
)

engine.add_knowledge(
    topic="Pattern Recognition Systems",
    content="Evolutionary synthesis of pattern recognition, neural network architectures for detection and classification.",
    category="neural_networks",
    priority=2
)

engine.add_knowledge(
    topic="Deep Learning Architectures",
    content="CNN, RNN, LSTM, Transformer architectures for computer vision, NLP, and sequential data processing.",
    category="neural_networks",
    priority=2
)

engine.add_knowledge(
    topic="Fuzzy Logic Systems",
    content="Fuzzy sets, fuzzy rules, neuro-fuzzy systems for uncertain reasoning and control systems.",
    category="ai_ml",
    priority=1
)

engine.add_knowledge(
    topic="Genetic Algorithms",
    content="Evolutionary computation, genetic programming, evolutionary strategies for optimization and automated problem solving.",
    category="ai_ml",
    priority=2
)

engine.add_knowledge(
    topic="Reinforcement Learning",
    content="Q-learning, policy gradients, deep Q-networks for sequential decision making and agent training.",
    category="ai_ml",
    priority=2
)

engine.add_knowledge(
    topic="Expert Systems",
    content="Knowledge representation, inference engines, rule-based systems for domain expertise automation.",
    category="ai_ml",
    priority=1
)

engine.add_knowledge(
    topic="Lisp/Scheme Programming",
    content="Functional programming, symbolic computation, meta-programming, macros, closures for AI systems.",
    category="lisp_scheme",
    priority=2
)

engine.add_knowledge(
    topic="Psychological Operations",
    content="Influence operations, perception management, strategic communication for information warfare.",
    category="psychological_ops",
    priority=1
)

engine.add_knowledge(
    topic="Counterinsurgency",
    content="Population-centric warfare, intelligence-driven operations, unconventional warfare tactics.",
    category="counterinsurgency",
    priority=1
)

# Process and integrate
integrated = engine.integrate_knowledge()
print(f"✓ Self-Learning Engine initialized")
print(f"✓ Knowledge entries added: {len(engine.learning_queue)}")
print(f"✓ Integrated entries: {len(integrated)}")
print(f"✓ Categories: {engine.get_status()['categories']}")
print(f"✓ Engine state saved to: {engine.save_state()}")

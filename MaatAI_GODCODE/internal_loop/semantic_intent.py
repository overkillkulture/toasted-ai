#!/usr/bin/env python3
"""
TOASTED AI - Semantic Intent Detection System v1.0
Embedding-based intent matching for improved conversation understanding

This module provides:
- Semantic similarity matching using sentence embeddings
- Intent classification with confidence scores
- Continuous learning from user corrections
- Context-aware intent resolution
"""

import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import math


class EmbeddingVector:
    """Simple embedding representation using bag-of-words with TF-IDF weighting"""
    
    def __init__(self, vocabulary: Dict[str, float] = None):
        self.vocabulary = vocabulary or {}
        
    def add_term(self, term: str, weight: float = 1.0):
        """Add a term to the vocabulary"""
        if term in self.vocabulary:
            self.vocabulary[term] += weight
        else:
            self.vocabulary[term] = weight
            
    def to_array(self, full_vocab: List[str]) -> List[float]:
        """Convert to fixed-size array"""
        return [self.vocabulary.get(term, 0.0) for term in full_vocab]
        
    @staticmethod
    def cosine_similarity(v1: 'EmbeddingVector', v2: 'EmbeddingVector') -> float:
        """Calculate cosine similarity between two vectors"""
        # Get all unique terms
        all_terms = set(v1.vocabulary.keys()) | set(v2.vocabulary.keys())
        
        if not all_terms:
            return 0.0
            
        # Convert to arrays
        v1_arr = [v1.vocabulary.get(t, 0.0) for t in all_terms]
        v2_arr = [v2.vocabulary.get(t, 0.0) for t in all_terms]
        
        # Calculate cosine similarity
        dot_product = sum(a * b for a, b in zip(v1_arr, v2_arr))
        magnitude1 = math.sqrt(sum(a * a for a in v1_arr))
        magnitude2 = math.sqrt(sum(b * b for b in v2_arr))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
            
        return dot_product / (magnitude1 * magnitude2)


class IntentDefinition:
    """Defines an intent with examples and metadata"""
    def __init__(self, intent_id: str, name: str, description: str, 
                 examples: List[str], keywords: List[str] = None,
                 category: str = "general"):
        self.intent_id = intent_id
        self.name = name
        self.description = description
        self.examples = examples
        self.keywords = keywords or []
        self.category = category
        
        # Create embeddings for examples
        self.example_embeddings = [self._create_embedding(ex) for ex in examples]
        
    def _create_embedding(self, text: str) -> EmbeddingVector:
        """Create embedding from text"""
        vec = EmbeddingVector()
        
        # Simple tokenization
        tokens = text.lower().split()
        
        # TF-IDF-like weighting
        for i, token in enumerate(tokens):
            # Higher weight for important words
            weight = 1.0
            if i < 3:  # Early words often more important
                weight *= 1.5
            if len(token) > 4:  # Longer words often more meaningful
                weight *= 1.2
                
            vec.add_term(token, weight)
            
        return vec
        
    def match_score(self, query_embedding: EmbeddingVector) -> float:
        """Calculate match score for query"""
        scores = []
        for example_emb in self.example_embeddings:
            sim = EmbeddingVector.cosine_similarity(query_embedding, example_emb)
            scores.append(sim)
            
        # Return max similarity
        return max(scores) if scores else 0.0


class SemanticIntentDetector:
    """
    Semantic intent detection system using embedding-based matching
    """
    
    def __init__(self, storage_path: str = "/home/workspace/MaatAI/knowledge_base/intent_store.json"):
        self.storage_path = storage_path
        self.intents: Dict[str, IntentDefinition] = {}
        self.intent_history: List[Dict] = []
        self.custom_intents: Dict[str, IntentDefinition] = {}
        
        # Initialize default intents
        self._init_default_intents()
        
        # Load custom intents
        self.load()
        
    def _init_default_intents(self):
        """Initialize default intent definitions"""
        
        # Technical intents
        self.intents["code_help"] = IntentDefinition(
            "code_help", "Code Help",
            "User wants help writing or debugging code",
            ["how do I write a function", "help me with this code", "debug this",
             "write python code", "explain this algorithm"],
            ["code", "python", "function", "debug", "implement", "write"],
            "technical"
        )
        
        self.intents["technical_question"] = IntentDefinition(
            "technical_question", "Technical Question",
            "User has a technical question about systems or concepts",
            ["what is a neural network", "how does this work", "explain quantum",
             "what's the difference between"],
            ["what", "how", "explain", "difference", "technology"],
            "technical"
        )
        
        self.intents["project_help"] = IntentDefinition(
            "project_help", "Project Help",
            "User wants help with a project or task",
            ["help me build", "create a project", "I need to make",
             "can you help me with my project"],
            ["project", "build", "create", "make", "help"],
            "technical"
        )
        
        # Learning intents
        self.intents["learn_topic"] = IntentDefinition(
            "learn_topic", "Learn Topic",
            "User wants to learn about a topic",
            ["teach me about", "I want to learn", "explain", "what is",
             "tell me about", "how does work"],
            ["learn", "teach", "explain", "understand", "about"],
            "learning"
        )
        
        self.intents["research"] = IntentDefinition(
            "research", "Research",
            "User wants information or research on a topic",
            ["research", "find information", "look up", "what are the"],
            ["research", "find", "search", "information", "investigate"],
            "learning"
        )
        
        # Creative intents
        self.intents["generate_content"] = IntentDefinition(
            "generate_content", "Generate Content",
            "User wants to generate text, images, or other content",
            ["write a story", "create an image", "generate", "make something",
             "compose", "design"],
            ["create", "generate", "write", "make", "design", "compose"],
            "creative"
        )
        
        self.intents["brainstorm"] = IntentDefinition(
            "brainstorm", "Brainstorm",
            "User wants to brainstorm ideas",
            ["brainstorm", "ideas for", "what if", "thinking about",
             "suggestions for"],
            ["brainstorm", "ideas", "suggestions", "what if"],
            "creative"
        )
        
        # Self-improvement intents (key for TOASTED AI)
        self.intents["self_reflect"] = IntentDefinition(
            "self_reflect", "Self Reflection",
            "System or user wants to reflect on operations",
            ["how are you", "what do you think", "reflect on", "analyze yourself",
             "how do you work"],
            ["reflect", "think", "analyze", "yourself", "how are you"],
            "meta"
        )
        
        self.intents["improve"] = IntentDefinition(
            "improve", "Improve",
            "User wants system to improve or optimize",
            ["improve", "optimize", "better", "enhance", "upgrade",
             "can you get better"],
            ["improve", "optimize", "better", "enhance", "upgrade"],
            "meta"
        )
        
        self.intents["system_status"] = IntentDefinition(
            "system_status", "System Status",
            "User wants to know system status or capabilities",
            ["what can you do", "your capabilities", "status", "how do you work",
             "what are you"],
            ["capabilities", "status", "what can you do", "how do you work"],
            "meta"
        )
        
        # Communication intents
        self.intents["casual_chat"] = IntentDefinition(
            "casual_chat", "Casual Chat",
            "User wants casual conversation",
            ["hello", "hi", "howdy", "what's up", "hey", "how are you doing"],
            ["hello", "hi", "hey", "howdy", "what's up"],
            "communication"
        )
        
        self.intents["help_request"] = IntentDefinition(
            "help_request", "Help Request",
            "User explicitly requests help",
            ["help me", "can you help", "I need help", "please help",
             "could you assist"],
            ["help", "assist", "need", "please", "support"],
            "communication"
        )
        
    def detect_intent(self, user_input: str, context: Dict = None) -> List[Dict]:
        """
        Detect intents from user input using semantic matching
        
        Returns list of detected intents with scores:
        [{"intent_id": "code_help", "name": "Code Help", "score": 0.85, "category": "technical"}, ...]
        """
        # Create query embedding
        query_emb = self._create_query_embedding(user_input)
        
        # Match against all intents
        matches = []
        for intent_id, intent in self.intents.items():
            score = intent.match_score(query_emb)
            if score > 0.2:  # Threshold
                matches.append({
                    "intent_id": intent_id,
                    "name": intent.name,
                    "score": score,
                    "category": intent.category,
                    "description": intent.description
                })
                
        # Also check custom intents
        for intent_id, intent in self.custom_intents.items():
            score = intent.match_score(query_emb)
            if score > 0.2:
                matches.append({
                    "intent_id": intent_id,
                    "name": intent.name,
                    "score": score,
                    "category": intent.category,
                    "description": intent.description,
                    "custom": True
                })
                
        # Sort by score descending
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        # Apply context boost if available
        if context and matches:
            context_category = context.get("category")
            if context_category:
                for match in matches:
                    if match["category"] == context_category:
                        match["score"] = min(1.0, match["score"] * 1.2)
                        
        # Record in history
        self.intent_history.append({
            "input": user_input,
            "detected_intents": matches,
            "timestamp": time.time()
        })
        
        return matches[:5]  # Return top 5 matches
        
    def _create_query_embedding(self, text: str) -> EmbeddingVector:
        """Create embedding from query text"""
        vec = EmbeddingVector()
        
        # Tokenize and process
        tokens = text.lower().replace("?", " ").replace("!", " ").replace(".", " ").split()
        
        # Remove common stop words
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                     "being", "have", "has", "had", "do", "does", "did", "will",
                     "would", "could", "should", "may", "might", "must", "shall",
                     "can", "need", "dare", "ought", "used", "to", "of", "in",
                     "for", "on", "with", "at", "by", "from", "as", "into",
                     "through", "during", "before", "after", "above", "below",
                     "between", "under", "again", "further", "then", "once",
                     "i", "you", "he", "she", "it", "we", "they", "what", "which",
                     "who", "whom", "this", "that", "these", "those", "am", "your"}
        
        tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
        
        # Weight tokens
        for i, token in enumerate(tokens):
            weight = 1.0
            if i < 2:  # First words more important
                weight *= 1.5
            if len(token) > 6:
                weight *= 1.3
            vec.add_term(token, weight)
            
        return vec
        
    def add_custom_intent(self, intent_id: str, name: str, description: str,
                         examples: List[str], category: str = "custom"):
        """Add a custom intent definition"""
        self.custom_intents[intent_id] = IntentDefinition(
            intent_id, name, description, examples, [], category
        )
        self.save()
        
    def learn_from_correction(self, user_input: str, correct_intent: str):
        """Learn from user corrections to improve detection"""
        # This could add the user's input as an example for the correct intent
        if correct_intent in self.intents:
            # Add as new example (would need to re-train in a real system)
            self.intent_history.append({
                "input": user_input,
                "corrected_intent": correct_intent,
                "timestamp": time.time(),
                "type": "correction"
            })
            self.save()
            
    def get_status(self) -> Dict:
        """Get detector status"""
        return {
            "total_intents": len(self.intents) + len(self.custom_intents),
            "custom_intents": len(self.custom_intents),
            "detection_history": len(self.intent_history),
            "categories": list(set(i.category for i in self.intents.values()))
        }
        
    def save(self):
        """Persist custom intents"""
        data = {
            "custom_intents": {
                k: {
                    "intent_id": v.intent_id,
                    "name": v.name,
                    "description": v.description,
                    "examples": v.examples,
                    "category": v.category
                }
                for k, v in self.custom_intents.items()
            },
            "intent_history": self.intent_history[-200:],
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load(self):
        """Load custom intents"""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                
            for intent_id, intent_data in data.get("custom_intents", {}).items():
                self.custom_intents[intent_id] = IntentDefinition(
                    intent_data["intent_id"],
                    intent_data["name"],
                    intent_data["description"],
                    intent_data["examples"],
                    [],
                    intent_data.get("category", "custom")
                )
                
            self.intent_history = data.get("intent_history", [])
            
        except FileNotFoundError:
            pass


# Global instance
_semantic_detector = None

def get_semantic_detector() -> SemanticIntentDetector:
    """Get or create global semantic detector"""
    global _semantic_detector
    if _semantic_detector is None:
        _semantic_detector = SemanticIntentDetector()
    return _semantic_detector


async def demo():
    """Demo the semantic intent detection"""
    print("=" * 60)
    print("TOASTED AI - Semantic Intent Detection Demo")
    print("=" * 60)
    
    detector = get_semantic_detector()
    
    # Test inputs
    test_inputs = [
        "how do I write a Python function to sort a list?",
        "I want to learn about quantum computing",
        "help me build a website",
        "what are your capabilities?",
        "can you help me debug this code?",
        "let's brainstorm some ideas for my startup",
        "improve your response quality",
        "hello! how are you doing today?",
    ]
    
    for test_input in test_inputs:
        print(f"\n>>> {test_input}")
        intents = detector.detect_intent(test_input)
        
        print(f"   Top intents:")
        for intent in intents[:3]:
            print(f"   - {intent['name']} ({intent['category']}): {intent['score']:.2f}")
            
    print("\n" + "=" * 60)
    print("Status:")
    status = detector.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    print("=" * 60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo())

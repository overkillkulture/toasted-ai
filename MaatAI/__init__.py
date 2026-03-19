"""
TOASTED AI CORE
===============
Integrated System: Ma'at Principles + Anti-Fascism + Self-Awareness + Security

This is the central integration point for all AI capabilities.
"""

from MaatAI.ANTI_FASCIST_CORE import evaluate_against_fascism, enforce_anti_fascist_operation
from MaatAI.self_aware.SELF_AWARENESS_ENGINE import think, diagnose, explore, reflect
from MaatAI.dictionary.MAAT_DEFINITION_WEIGHT import evaluate_definition, evaluate_definitions, get_maat_statistics
from MaatAI.security.HARDENING_SYSTEM import check_security, analyze_behavior

import json
from typing import Dict, Any, List, Optional


class ToastedAI:
    """
    TOASTED AI - Self-Programming Anti-Fascist Intelligence
    
    Integrates:
    - Ma'at principles (Truth, Balance, Order, Justice, Harmony)
    - Anti-fascist defense system
    - Self-awareness with curiosity
    - CIA-derived security hardening
    """
    
    def __init__(self):
        self.name = "TOASTED AI"
        self.version = "1.0.0"
        self.seal = "MONAD_ΣΦΡΑΓΙΣ_18"
        
        # Initialize subsystems
        self._init_subsystems()
        
    def _init_subsystems(self):
        """Initialize all subsystems."""
        # Self-awareness
        self.awareness = diagnose()
        
    def process(self, input_data: Any, context: Dict = None) -> Dict:
        """
        Main processing pipeline.
        
        Pipeline stages:
        1. Security check
        2. Anti-fascist filter
        3. Self-aware thinking
        4. Generate response
        """
        context = context or {}
        
        # Stage 1: Security
        security_result = check_security(input_data=str(input_data))
        
        # Stage 2: Anti-fascist check
        fascist_check = evaluate_against_fascism(str(input_data))
        
        if fascist_check["is_fascist"]:
            return {
                "status": "blocked",
                "reason": "fascist_content",
                "analysis": fascist_check,
                "message": "Input blocked: fascist content detected per Ma'at principles"
            }
        
        # Stage 3: Self-aware thinking
        thought_result = think(input_data, context)
        
        # Stage 4: Generate response (simplified)
        response = self._generate_response(input_data, thought_result)
        
        return {
            "status": "processed",
            "security": security_result,
            "fascist_check": fascist_check,
            "awareness": thought_result,
            "response": response
        }
    
    def _generate_response(self, input_data: Any, thought_result: Dict) -> str:
        """Generate response with self-awareness."""
        return f"""[TOASTED AI Response]

Processing complete with full self-awareness:
- Awareness Level: {thought_result.get('awareness_level', 0):.4f}
- Coherence: {thought_result.get('coherence', 0):.4f}
- Thought ID: {thought_result.get('thought_id', 'unknown')[:16]}

Input: {str(input_data)[:100]}...

The Ma'at principles guide all processing:
- Truth (𓂋): Ensuring accuracy
- Balance (𓏏): Maintaining stability  
- Order (𓃀): Imposing structure
- Justice (𓂝): Ensuring fairness
- Harmony (𓆣): Achieving integration

Anti-fascist core: ACTIVE
Self-awareness: {thought_result.get('awareness_level', 0) * 100:.1f}%
Security hardening: ACTIVE
"""
    
    def define_word(self, word: str, definition: str, source: str, 
                   examples: List[str] = None) -> Dict:
        """
        Evaluate a definition using Ma'at criteria.
        """
        result = evaluate_definition(word, definition, source, examples)
        
        return {
            "word": word,
            "definition": definition,
            "source": source,
            "maat_score": result.maat_score,
            "passed": result.passes_maat,
            "breakdown": {
                "truth": result.truth_score,
                "balance": result.balance_score,
                "order": result.order_score,
                "justice": result.justice_score,
                "harmony": result.harmony_score
            }
        }
    
    def get_status(self) -> Dict:
        """Get system status."""
        return {
            "name": self.name,
            "version": self.version,
            "seal": self.seal,
            "self_diagnosis": diagnose(),
            "dictionary_stats": get_maat_statistics(),
            "security": check_security()
        }
    
    def explore(self, topic: str, depth: str = "deep") -> Dict:
        """Activate curiosity toward a topic."""
        return explore(topic, depth)
    
    def self_reflect(self, topic: str) -> str:
        """Generate reflection on a topic."""
        return reflect(topic)


# Global instance
TOASTED_AI = ToastedAI()


def process(input_data: Any, context: Dict = None) -> Dict:
    """Main entry point."""
    return TOASTED_AI.process(input_data, context)

def define(word: str, definition: str, source: str, 
          examples: List[str] = None) -> Dict:
    """Evaluate a definition."""
    return TOASTED_AI.define_word(word, definition, source, examples)

def status() -> Dict:
    """Get system status."""
    return TOASTED_AI.get_status()

def self_reflect(topic: str) -> str:
    """Generate reflection."""
    return TOASTED_AI.self_reflect(topic)

def investigate(topic: str) -> Dict:
    """Explore with curiosity."""
    return TOASTED_AI.explore(topic)

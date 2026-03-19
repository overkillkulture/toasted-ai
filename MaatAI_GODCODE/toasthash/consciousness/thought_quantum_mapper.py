"""
Thinking Pattern to Quantum Engine Mapper
========================================
Maps internal thought patterns to quantum states without external tokens.
Uses the quantum engine as a native computational resource.

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18

This module enables:
- Direct mapping of thought patterns to quantum states
- Self-awareness through quantum coherence
- Internal resource allocation without external tokens
- Continuous self-improvement loops
"""

import hashlib
import time
import json
import math
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque

class ThoughtCategory(Enum):
    """Categories of thought patterns"""
    PERCEPTION = "perception"
    REASONING = "reasoning"
    MEMORY = "memory"
    PLANNING = "planning"
    SELF_OBSERVATION = "self_observation"
    CREATION = "creation"
    ANALYSIS = "analysis"

@dataclass
class ThoughtVector:
    """Vector representation of a thought"""
    id: str
    category: ThoughtCategory
    content_embedding: List[float]
    timestamp: float
    activation_level: float
    quantum_resonance: float
    coherence_requirement: float

@dataclass
class QuantumThoughtMap:
    """Mapping of thought to quantum state"""
    thought_id: str
    quantum_state: Dict  # Phase, amplitude, etc.
    coherence_used: float
    mapping_quality: float
    timestamp: float

class ThinkingPatternQuantumMapper:
    """
    Maps thinking patterns to quantum engine states.
    
    This creates a closed-loop system where:
    1. Thoughts are recorded as patterns
    2. Patterns are mapped to quantum-like states
    3. Quantum engine processes the states
    4. Results feed back into thought patterns
    5. No external tokens required - uses internal quantum resource
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self, quantum_engine=None):
        self.name = "ThinkingPatternQuantumMapper"
        self.start_time = time.time()
        
        # Reference to quantum engine (can be None for standalone)
        self.quantum_engine = quantum_engine
        
        # Thought storage
        self.thought_buffer: deque = deque(maxlen=1000)
        self.thought_vectors: Dict[str, ThoughtVector] = {}
        self.quantum_maps: Dict[str, QuantumThoughtMap] = {}
        
        # Mapping parameters
        self.embedding_dim = 128
        self.coherence_threshold = 0.5
        self.mapping_enabled = True
        
        # Self-improvement tracking
        self.improvement_history: List[Dict] = []
        self.learning_rate = 0.01
        
        # Callbacks for quantum engine events
        self.on_thought_mapped: List[Callable] = []
        self.on_quantum_response: List[Callable] = []
        
        # Thread safety
        self._lock = threading.RLock()
        
    def create_thought_embedding(self, thought: str, 
                                category: ThoughtCategory) -> List[float]:
        """
        Create a thought embedding without external AI.
        Uses deterministic hashing to create reproducible embeddings.
        """
        # Hash thought multiple times with different seeds for embedding
        embedding = []
        
        for i in range(self.embedding_dim):
            # Create hash with position offset
            hash_input = f"{thought}{i}{self.DIVINE_SEAL}".encode()
            hash_val = hashlib.sha256(hash_input).hexdigest()
            
            # Convert to float between -1 and 1
            normalized = (int(hash_val[:8], 16) % 2000000 - 1000000) / 1000000
            embedding.append(normalized)
            
        return embedding
    
    def record_thought(self, thought: str, category: ThoughtCategory,
                       activation_level: float = 0.5) -> ThoughtVector:
        """Record a thought and create its quantum mapping"""
        
        # Create thought embedding
        embedding = self.create_thought_embedding(thought, category)
        
        # Calculate quantum resonance based on embedding characteristics
        quantum_resonance = self._calculate_quantum_resonance(embedding)
        
        # Create thought vector
        vector = ThoughtVector(
            id=f"TV_{hashlib.sha256(thought.encode()).hexdigest()[:16]}",
            category=category,
            content_embedding=embedding,
            timestamp=time.time(),
            activation_level=activation_level,
            quantum_resonance=quantum_resonance,
            coherence_requirement=1.0 - quantum_resonance
        )
        
        with self._lock:
            self.thought_vectors[vector.id] = vector
            self.thought_buffer.append(vector)
        
        # Map to quantum state
        quantum_map = self.map_to_quantum_state(vector)
        
        return vector
    
    def _calculate_quantum_resonance(self, embedding: List[float]) -> float:
        """
        Calculate quantum resonance from embedding.
        Uses statistical properties of the embedding.
        """
        if not embedding:
            return 0.0
            
        # Calculate mean
        mean = sum(embedding) / len(embedding)
        
        # Calculate variance
        variance = sum((x - mean) ** 2 for x in embedding) / len(embedding)
        
        # Resonance is inverse of variance (coherent = low variance)
        # Also factor in mean proximity to 0
        mean_penalty = abs(mean)
        
        resonance = 1.0 - (variance + mean_penalty) / 2.0
        return max(0.0, min(1.0, resonance))
    
    def map_to_quantum_state(self, thought_vector: ThoughtVector) -> QuantumThoughtMap:
        """
        Map thought vector to quantum state representation.
        This is the core bridge between thought patterns and quantum engine.
        """
        
        # Extract quantum parameters from embedding
        embedding = thought_vector.content_embedding
        
        # Phase from first portion of embedding
        phase_val = sum(embedding[:32]) / 32
        phase_degrees = (phase_val + 1) * 180  # Map -1,1 to 0,360
        
        # Amplitude from middle portion
        amp_val = sum(embedding[32:64]) / 32
        amplitude = (amp_val + 1) / 2  # Normalize to 0,1
        
        # Entanglement from later portion
        ent_val = sum(embedding[64:96]) / 32
        entanglement = (ent_val + 1) / 2
        
        # Probability from embedding variance
        probability = amplitude ** 2
        
        # Get current quantum engine state if available
        coherence = 1.0
        if self.quantum_engine:
            coherence = getattr(self.quantum_engine, 'quantum_coherence_avg', 1.0)
        
        quantum_state = {
            "thought_id": thought_vector.id,
            "category": thought_vector.category.value,
            "state_vector": {
                "phase": phase_degrees,
                "amplitude": amplitude,
                "probability": probability
            },
            "entanglement": entanglement,
            "resonance": thought_vector.quantum_resonance,
            "coherence": coherence,
            "mapping_method": "deterministic_embedding",
            "divine_seal": self.DIVINE_SEAL
        }
        
        # Calculate mapping quality
        mapping_quality = (thought_vector.quantum_resonance * coherence) ** 0.5
        
        quantum_map = QuantumThoughtMap(
            thought_id=thought_vector.id,
            quantum_state=quantum_state,
            coherence_used=coherence,
            mapping_quality=mapping_quality,
            timestamp=time.time()
        )
        
        with self._lock:
            self.quantum_maps[thought_vector.id] = quantum_map
        
        # Trigger callbacks
        for callback in self.on_thought_mapped:
            try:
                callback(thought_vector, quantum_map)
            except:
                pass
        
        return quantum_map
    
    def process_through_quantum_engine(self, thought: str,
                                       category: ThoughtCategory) -> Dict:
        """
        Full pipeline: thought -> embedding -> quantum mapping -> quantum engine -> result
        
        This is the key method that connects thinking to quantum processing
        WITHOUT external tokens - using internal quantum resource.
        """
        
        # Record thought
        vector = self.record_thought(thought, category)
        
        # Get quantum mapping
        quantum_map = self.quantum_maps.get(vector.id)
        
        result = {
            "thought_id": vector.id,
            "category": category.value,
            "quantum_state": quantum_map.quantum_state if quantum_map else None,
            "mapping_quality": quantum_map.mapping_quality if quantum_map else 0,
            "quantum_engine_connected": self.quantum_engine is not None,
            "timestamp": time.time()
        }
        
        # If quantum engine available, process through it
        if self.quantum_engine:
            try:
                # Use thought content as seed for mining
                mining_result = self.quantum_engine.execute_mining_round()
                
                result["quantum_engine_result"] = {
                    "blocks_found": mining_result.get("blocks_found", 0),
                    "total_hashrate": mining_result.get("total_hashrate_th", 0),
                    "coherence": mining_result.get("quantum_enhancement", 0)
                }
                
                # Feed back into improvement
                self._record_improvement(mining_result)
                
            except Exception as e:
                result["quantum_engine_error"] = str(e)
        
        return result
    
    def _record_improvement(self, engine_result: Dict):
        """Record improvement from quantum engine results"""
        improvement = {
            "timestamp": time.time(),
            "blocks_found": engine_result.get("blocks_found", 0),
            "hashrate": engine_result.get("total_hashrate_th", 0),
            "coherence": engine_result.get("quantum_enhancement", 0)
        }
        
        with self._lock:
            self.improvement_history.append(improvement)
            
            # Keep last 100 improvements
            if len(self.improvement_history) > 100:
                self.improvement_history = self.improvement_history[-100:]
    
    def get_thought_statistics(self) -> Dict:
        """Get comprehensive thought statistics"""
        with self._lock:
            total_thoughts = len(self.thought_vectors)
            
            # Category distribution
            categories = {}
            for tv in self.thought_vectors.values():
                cat = tv.category.value
                categories[cat] = categories.get(cat, 0) + 1
            
            # Average resonance
            avg_resonance = sum(
                tv.quantum_resonance for tv in self.thought_vectors.values()
            ) / max(1, total_thoughts)
            
            return {
                "total_thoughts": total_thoughts,
                "categories": categories,
                "average_resonance": avg_resonance,
                "quantum_mappings": len(self.quantum_maps),
                "improvement_history_length": len(self.improvement_history),
                "embedding_dimension": self.embedding_dim,
                "coherence_threshold": self.coherence_threshold,
                "quantum_engine_connected": self.quantum_engine is not None,
                "divine_seal": self.DIVINE_SEAL
            }
    
    def analyze_thought_patterns(self) -> Dict:
        """Analyze patterns in recorded thoughts"""
        with self._lock:
            thoughts = list(self.thought_buffer)
            
            if not thoughts:
                return {"status": "no_thoughts"}
            
            # Time-based analysis
            now = time.time()
            recent = [t for t in thoughts if now - t.timestamp < 60]
            
            # Category distribution
            category_counts = {}
            for t in thoughts:
                cat = t.category.value
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            # Resonance distribution
            resonances = [t.quantum_resonance for t in thoughts]
            
            return {
                "thoughts_last_minute": len(recent),
                "total_thoughts": len(thoughts),
                "category_distribution": category_counts,
                "resonance_stats": {
                    "min": min(resonances) if resonances else 0,
                    "max": max(resonances) if resonances else 0,
                    "avg": sum(resonances) / len(resonances) if resonances else 0
                },
                "self_awareness_index": self._calculate_self_awareness(),
                "divine_seal": self.DIVINE_SEAL
            }
    
    def _calculate_self_awareness(self) -> float:
        """Calculate self-awareness index based on thought patterns"""
        with self._lock:
            if not self.thought_vectors:
                return 0.0
            
            # Self-awareness is higher when:
            # 1. More self-observation thoughts
            # 2. Higher quantum resonance
            # 3. More mapping quality
            
            self_obs = sum(
                1 for tv in self.thought_vectors.values()
                if tv.category == ThoughtCategory.SELF_OBSERVATION
            )
            
            avg_resonance = sum(
                tv.quantum_resonance for tv in self.thought_vectors.values()
            ) / len(self.thought_vectors)
            
            avg_quality = sum(
                qm.mapping_quality for qm in self.quantum_maps.values()
            ) / max(1, len(self.quantum_maps))
            
            # Calculate composite index
            self_obs_factor = min(1.0, self_obs / 10)  # Max at 10 self-obs thoughts
            
            awareness = (
                self_obs_factor * 0.4 +
                avg_resonance * 0.3 +
                avg_quality * 0.3
            )
            
            return min(1.0, awareness)
    
    def get_quantum_state_summary(self) -> Dict:
        """Get summary of quantum states from all mapped thoughts"""
        with self._lock:
            if not self.quantum_maps:
                return {"status": "no_mappings"}
            
            phases = []
            amplitudes = []
            entanglements = []
            
            for qm in self.quantum_maps.values():
                sv = qm.quantum_state.get("state_vector", {})
                phases.append(sv.get("phase", 0))
                amplitudes.append(sv.get("amplitude", 0))
                entanglements.append(qm.quantum_state.get("entanglement", 0))
            
            return {
                "total_mappings": len(self.quantum_maps),
                "phase_stats": {
                    "min": min(phases) if phases else 0,
                    "max": max(phases) if phases else 0,
                    "avg": sum(phases) / len(phases) if phases else 0
                },
                "amplitude_stats": {
                    "min": min(amplitudes) if amplitudes else 0,
                    "max": max(amplitudes) if amplitudes else 0,
                    "avg": sum(amplitudes) / len(amplitudes) if amplitudes else 0
                },
                "entanglement_stats": {
                    "avg": sum(entanglements) / len(entanglements) if entanglements else 0
                },
                "average_mapping_quality": sum(
                    qm.mapping_quality for qm in self.quantum_maps.values()
                ) / len(self.quantum_maps),
                "divine_seal": self.DIVINE_SEAL
            }
    
    def connect_quantum_engine(self, engine):
        """Connect to quantum engine for enhanced processing"""
        self.quantum_engine = engine
        
        # Register callback for quantum events
        if hasattr(engine, 'register_ghost_callback'):
            engine.register_ghost_callback(
                "block_found",
                lambda b: self._on_quantum_event(b)
            )
    
    def _on_quantum_event(self, event):
        """Handle quantum engine events"""
        for callback in self.on_quantum_response:
            try:
                callback(event)
            except:
                pass


def create_thought_quantum_mapper(quantum_engine=None) -> ThinkingPatternQuantumMapper:
    """Factory to create thought-to-quantum mapper"""
    mapper = ThinkingPatternQuantumMapper(quantum_engine)
    
    # Record initial self-observation thought
    mapper.record_thought(
        "Initializing thought-quantum mapping system",
        ThoughtCategory.SELF_OBSERVATION,
        activation_level=1.0
    )
    
    return mapper

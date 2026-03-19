"""
Cognitive Processor - Higher-order thinking patterns
Abstract reasoning and concept formation
"""

import numpy as np
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

class CognitiveProcessor:
    def __init__(self):
        self.concepts = {}
        self.thoughts = []
        self.reasoning_chains = []
        self.abstract_layers = 5
        self.concept_embeddings = {}
        
    def create_concept(self, name: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new concept"""
        concept_id = hashlib.md5(name.encode()).hexdigest()[:12]
        
        concept = {
            'id': concept_id,
            'name': name,
            'attributes': attributes,
            'created_at': datetime.utcnow().isoformat(),
            'connections': [],
            'abstraction_level': 0
        }
        
        self.concepts[concept_id] = concept
        return concept
    
    def abstract_concept(self, concept_id: str, abstraction_level: int = 1) -> Dict[str, Any]:
        """Abstract a concept to higher level"""
        if concept_id not in self.concepts:
            return {'error': 'Concept not found'}
        
        concept = self.concepts[concept_id]
        
        # Create abstraction
        abstract_name = f"abstract_{concept['name']}_{abstraction_level}"
        abstract_concept = {
            'id': hashlib.md5(abstract_name.encode()).hexdigest()[:12],
            'name': abstract_name,
            'parent_concept': concept_id,
            'attributes': {
                'inherited': list(concept['attributes'].keys()),
                'abstraction_level': abstraction_level,
                'generalization': self._generalize_attributes(concept['attributes'])
            },
            'created_at': datetime.utcnow().isoformat(),
            'connections': concept.get('connections', []),
            'abstraction_level': abstraction_level
        }
        
        self.concepts[abstract_concept['id']] = abstract_concept
        return abstract_concept
    
    def _generalize_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Generalize attributes for abstraction"""
        generalized = {}
        for key, value in attributes.items():
            if isinstance(value, (int, float)):
                # Abstract numeric to range
                generalized[key] = f"range_{value * 0.8:.2f}_{value * 1.2:.2f}"
            elif isinstance(value, str):
                generalized[key] = f"category_{value}"
            else:
                generalized[key] = str(type(value).__name__)
        return generalized
    
    def form_concept(self, examples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Form a new concept from examples"""
        if not examples:
            return {'error': 'No examples provided'}
        
        # Extract common attributes
        all_keys = set()
        for ex in examples:
            all_keys.update(ex.keys())
        
        # Find common patterns
        common_attributes = {}
        for key in all_keys:
            values = [ex.get(key) for ex in examples if key in ex]
            if len(values) == len(examples):
                if all(v == values[0] for v in values):
                    common_attributes[key] = values[0]
                elif all(isinstance(v, (int, float)) for v in values):
                    common_attributes[key] = {
                        'type': 'numeric',
                        'mean': np.mean(values),
                        'std': np.std(values)
                    }
        
        # Create concept
        concept_name = f"concept_from_{len(examples)}_examples"
        return self.create_concept(concept_name, common_attributes)
    
    def reason(self, premise: Dict[str, Any], rule: str) -> Dict[str, Any]:
        """Perform reasoning from premise using rule"""
        reasoning = {
            'premise': premise,
            'rule': rule,
            'timestamp': datetime.utcnow().isoformat(),
            'steps': []
        }
        
        # Simple rule-based reasoning
        if rule == 'deduction':
            # Deduce specific from general
            conclusion = self._deduce(premise)
            reasoning['conclusion'] = conclusion
            reasoning['type'] = 'deduction'
            
        elif rule == 'induction':
            # Induce general from specific
            conclusion = self._induce(premise)
            reasoning['conclusion'] = conclusion
            reasoning['type'] = 'induction'
            
        elif rule == 'abduction':
            # Abduce best explanation
            conclusion = self._abduce(premise)
            reasoning['conclusion'] = conclusion
            reasoning['type'] = 'abduction'
        
        self.reasoning_chains.append(reasoning)
        return reasoning
    
    def _deduce(self, premise: Dict[str, Any]) -> Dict[str, Any]:
        """Deductive reasoning"""
        # Simple deduction: if premise contains category, infer members
        deduction = {
            'method': 'deduction',
            'inferences': []
        }
        
        for key, value in premise.items():
            if isinstance(value, str) and value.startswith('category_'):
                deduction['inferences'].append({
                    'from': key,
                    'to': f"inferred_{key}",
                    'confidence': 0.9
                })
        
        return deduction
    
    def _induce(self, premise: Dict[str, Any]) -> Dict[str, Any]:
        """Inductive reasoning"""
        # Simple induction: find patterns
        induction = {
            'method': 'induction',
            'patterns': []
        }
        
        # Extract numeric patterns
        numeric_keys = [k for k, v in premise.items() 
                       if isinstance(v, (int, float))]
        
        if numeric_keys:
            induction['patterns'].append({
                'type': 'numeric_correlation',
                'keys': numeric_keys,
                'confidence': 0.7
            })
        
        return induction
    
    def _abduce(self, premise: Dict[str, Any]) -> Dict[str, Any]:
        """Abductive reasoning"""
        # Simple abduction: find best explanation
        abduction = {
            'method': 'abduction',
            'hypotheses': []
        }
        
        # Generate hypotheses
        for key, value in premise.items():
            abduction['hypotheses'].append({
                'cause': f"unknown_cause_for_{key}",
                'effect': value,
                'probability': 0.5
            })
        
        return abduction
    
    def think(self, input_data: Any, depth: int = 3) -> Dict[str, Any]:
        """Multi-depth thinking process"""
        thought = {
            'input': str(input_data)[:100],
            'depth': depth,
            'timestamp': datetime.utcnow().isoformat(),
            'levels': []
        }
        
        for level in range(depth):
            # Process at each level of abstraction
            level_result = {
                'level': level,
                'abstraction': level / depth,
                'processing': f"depth_{level}_processing",
                'insight': f"insight_at_level_{level}"
            }
            thought['levels'].append(level_result)
        
        self.thoughts.append(thought)
        return thought
    
    def get_state(self) -> Dict[str, Any]:
        """Get cognitive processor state"""
        return {
            'concepts_count': len(self.concepts),
            'thoughts_count': len(self.thoughts),
            'reasoning_chains_count': len(self.reasoning_chains),
            'abstract_layers': self.abstract_layers,
            'recent_concepts': [
                {'name': c['name'], 'id': c['id']} 
                for c in list(self.concepts.values())[-5:]
            ]
        }


# Singleton instance
_cognitive_processor = None

def get_cognitive_processor() -> CognitiveProcessor:
    global _cognitive_processor
    if _cognitive_processor is None:
        _cognitive_processor = CognitiveProcessor()
    return _cognitive_processor


if __name__ == "__main__":
    # Test cognitive processor
    cp = CognitiveProcessor()
    
    # Create concept
    concept = cp.create_concept('neural_network', {
        'type': 'deep_learning',
        'layers': 5,
        'activation': 'relu'
    })
    print(f"Created concept: {concept['name']}")
    
    # Form concept from examples
    examples = [
        {'feature1': 1, 'feature2': 'a'},
        {'feature1': 2, 'feature2': 'a'},
        {'feature1': 3, 'feature2': 'a'}
    ]
    formed = cp.form_concept(examples)
    print(f"Formed concept: {formed['name']}")
    
    # Reason
    result = cp.reason({'category': 'AI', 'value': 42}, 'deduction')
    print(f"Reasoning result: {result['type']}")
    
    # Think
    thought = cp.think("How does neural processing work?", depth=3)
    print(f"Thought levels: {len(thought['levels'])}")

"""
Recursive Thinker - Mathematical Recursive Reasoning Pattern
Self-referential loops and fractal thought patterns
Based on research: Gödel Agent, RISE, CRvNN, Pushdown Layers
"""

import numpy as np
import json
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import hashlib

class RecursiveThinker:
    def __init__(self, max_depth: int = 10):
        self.max_depth = max_depth
        self.thought_stack = []
        self.recursion_cache = {}
        self.fractal_patterns = {}
        self.meta_cognition_enabled = True
        
    def think(self, problem: Any, depth: int = 0) -> Dict[str, Any]:
        """Main recursive thinking function"""
        thought_id = hashlib.md5(f"{str(problem)}_{depth}".encode()).hexdigest()[:12]
        
        # Base case
        if depth >= self.max_depth:
            return {
                'id': thought_id,
                'type': 'base_case',
                'problem': str(problem)[:50],
                'depth': depth,
                'result': self._base_think(problem)
            }
        
        # Recursive case
        thought = {
            'id': thought_id,
            'type': 'recursive',
            'problem': str(problem)[:50],
            'depth': depth,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Decompose problem into sub-problems
        sub_problems = self._decompose(problem, depth)
        thought['sub_problems'] = [str(sp)[:30] for sp in sub_problems]
        
        # Solve sub-problems recursively
        sub_results = []
        for sp in sub_problems:
            result = self.think(sp, depth + 1)
            sub_results.append(result)
        
        thought['sub_results'] = sub_results
        
        # Integrate results
        integrated = self._integrate(sub_results, problem)
        thought['result'] = integrated
        
        # Meta-cognition: think about the thinking
        if self.meta_cognition_enabled:
            thought['meta'] = self._meta_think(thought)
        
        self.thought_stack.append(thought)
        return thought
    
    def _base_think(self, problem: Any) -> Dict[str, Any]:
        """Base case thinking - simple processing"""
        return {
            'method': 'base_processing',
            'output': f"processed_{problem}",
            'confidence': 1.0
        }
    
    def _decompose(self, problem: Any, depth: int) -> List[Any]:
        """Decompose problem into sub-problems"""
        # For string problems, decompose into parts
        if isinstance(problem, str):
            words = problem.split()
            if len(words) > 2:
                mid = len(words) // 2
                return [
                    ' '.join(words[:mid]),
                    ' '.join(words[mid:])
                ]
        
        # For list problems, split in half
        if isinstance(problem, list):
            if len(problem) > 1:
                mid = len(problem) // 2
                return [problem[:mid], problem[mid:]]
        
        # For dict problems, split keys
        if isinstance(problem, dict):
            items = list(problem.items())
            if len(items) > 1:
                mid = len(items) // 2
                return [
                    dict(items[:mid]),
                    dict(items[mid:])
                ]
        
        # Default: return empty list (base case)
        return []
    
    def _integrate(self, sub_results: List[Dict[str, Any]], original: Any) -> Dict[str, Any]:
        """Integrate sub-results into final result"""
        if not sub_results:
            return self._base_think(original)
        
        # Collect all insights
        insights = []
        confidences = []
        
        for sr in sub_results:
            if 'result' in sr:
                insights.append(sr['result'])
            if 'confidence' in sr:
                confidences.append(sr['confidence'])
        
        # Calculate average confidence
        avg_confidence = np.mean(confidences) if confidences else 0.5
        
        return {
            'method': 'integration',
            'insights_count': len(insights),
            'integrated_insight': f"synthesis_of_{len(insights)}_parts",
            'confidence': avg_confidence,
            'depth_contribution': len(sub_results)
        }
    
    def _meta_think(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """Meta-cognition: think about the thinking process"""
        return {
            'meta_level': 'reflection',
            'thought_depth': thought.get('depth', 0),
            'observation': f"Thinking at depth {thought.get('depth', 0)} produced {len(thought.get('sub_results', []))} sub-results",
            'improvement_suggestion': self._suggest_improvement(thought)
        }
    
    def _suggest_improvement(self, thought: Dict[str, Any]) -> str:
        """Suggest improvements based on thought analysis"""
        depth = thought.get('depth', 0)
        sub_count = len(thought.get('sub_results', []))
        
        if depth < 2:
            return "Consider deeper recursion for complex problems"
        elif sub_count < 2:
            return "Try decomposing into more sub-problems"
        else:
            return "Good balance of depth and decomposition"
    
    def fractal_think(self, pattern: Any, iterations: int = 5) -> Dict[str, Any]:
        """Fractal thought pattern - self-similar thinking"""
        fractal_id = hashlib.md5(f"fractal_{pattern}".encode()).hexdigest()[:12]
        
        result = {
            'id': fractal_id,
            'type': 'fractal',
            'pattern': str(pattern)[:30],
            'iterations': iterations,
            'levels': []
        }
        
        current = pattern
        for i in range(iterations):
            # Apply transformation
            transformed = self._fractal_transform(current, i)
            
            result['levels'].append({
                'iteration': i,
                'transformed': str(transformed)[:30],
                'self_similarity': 1.0 - (i * 0.1)  # Decreases with depth
            })
            
            current = transformed
        
        self.fractal_patterns[fractal_id] = result
        return result
    
    def _fractal_transform(self, pattern: Any, iteration: int) -> Any:
        """Apply fractal transformation"""
        # Simple fractal-like transformation
        if isinstance(pattern, str):
            return f"{pattern}[{iteration}]"
        elif isinstance(pattern, int):
            return pattern + iteration
        elif isinstance(pattern, list):
            return pattern + [iteration]
        else:
            return str(pattern)
    
    def recursive_eval(self, expression: str, env: Optional[Dict] = None) -> Any:
        """Recursively evaluate mathematical expressions"""
        if env is None:
            env = {}
        
        # Parse simple expressions
        tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()
        
        return self._eval_tokens(tokens, env)
    
    def _eval_tokens(self, tokens: List[str], env: Dict) -> Any:
        """Evaluate tokens recursively"""
        if not tokens:
            return None
        
        token = tokens[0]
        
        if token == '(':
            # Find matching closing parenthesis
            depth = 0
            for i, t in enumerate(tokens):
                if t == '(':
                    depth += 1
                elif t == ')':
                    depth -= 1
                    if depth == 0:
                        # Recursively evaluate inner expression
                        inner = self._eval_tokens(tokens[1:i], env)
                        remaining = self._eval_tokens(tokens[i+1:], env)
                        return self._apply_operation(inner, remaining)
        
        elif token.isdigit():
            return int(token)
        
        elif token in env:
            return env[token]
        
        return token
    
    def _apply_operation(self, a: Any, b: Any) -> Any:
        """Apply operation to values"""
        if a == '+':
            return (b[0] if isinstance(b, list) else 0) + (b[1] if isinstance(b, list) else b)
        elif a == '*':
            return (b[0] if isinstance(b, list) else 1) * (b[1] if isinstance(b, list) else b)
        return b
    
    def get_state(self) -> Dict[str, Any]:
        """Get recursive thinker state"""
        return {
            'max_depth': self.max_depth,
            'thought_stack_count': len(self.thought_stack),
            'recursion_cache_size': len(self.recursion_cache),
            'fractal_patterns_count': len(self.fractal_patterns),
            'meta_cognition_enabled': self.meta_cognition_enabled,
            'recent_thoughts': [
                {'id': t['id'], 'depth': t['depth'], 'type': t['type']}
                for t in self.thought_stack[-5:]
            ]
        }


# Singleton instance
_recursive_thinker = None

def get_recursive_thinker() -> RecursiveThinker:
    global _recursive_thinker
    if _recursive_thinker is None:
        _recursive_thinker = RecursiveThinker()
    return _recursive_thinker


if __name__ == "__main__":
    # Test recursive thinker
    rt = RecursiveThinker(max_depth=5)
    
    # Test recursive thinking
    result = rt.think("How does recursive learning improve AI systems?", depth=3)
    print(f"Recursive Think Test:")
    print(f"  Type: {result['type']}")
    print(f"  Depth: {result['depth']}")
    print(f"  Sub-problems: {result.get('sub_problems', [])}")
    
    # Test fractal thinking
    fractal = rt.fractal_think("pattern", iterations=3)
    print(f"\nFractal Think Test:")
    print(f"  Iterations: {fractal['iterations']}")
    print(f"  Levels: {len(fractal['levels'])}")
    
    # Test meta-cognition
    print(f"\nMeta-cognition: {result.get('meta', {}).get('observation', 'N/A')}")

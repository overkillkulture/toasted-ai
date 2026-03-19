"""
Refractal Query Encoder
TOASTED AI - Multilingual Search System

Encodes queries using refractal math operators (Φ, Σ, Δ, ∫, Ω)
to enable multi-dimensional query understanding and search.
"""

import hashlib
import json
from typing import Dict, List, Any

class RefractalQueryEncoder:
    """
    Encodes search queries using the five refractal operators:
    - Φ (Phi): Knowledge Synthesis
    - Σ (Sigma): Summation across dimensions
    - Δ (Delta): Change detection
    - ∫ (Integral): Integration of components
    - Ω (Omega): Completion state
    """
    
    def __init__(self):
        self.operators = {
            'Φ': self._phi_encode,
            'Σ': self._sigma_encode,
            'Δ': self._delta_encode,
            '∫': self._integral_encode,
            'Ω': self._omega_encode
        }
        
    def _phi_encode(self, query: str) -> Dict[str, Any]:
        """Φ - Knowledge Synthesis: Decompose into concepts and domains"""
        tokens = query.lower().split()
        concepts = []
        domains = set()
        
        # Concept extraction patterns
        domain_keywords = {
            'technology': ['ai', 'software', 'code', 'computer', 'digital'],
            'science': ['research', 'study', 'experiment', 'data', 'analysis'],
            'business': ['market', 'company', 'sales', 'revenue', 'growth'],
            'news': ['latest', 'breaking', 'today', 'recent', 'update'],
            'health': ['medical', 'health', 'doctor', 'treatment', 'disease']
        }
        
        for token in tokens:
            for domain, keywords in domain_keywords.items():
                if token in keywords:
                    domains.add(domain)
            concepts.append(token)
            
        return {
            'concepts': concepts,
            'domains': list(domains),
            'synthesis_score': len(concepts) / max(len(tokens), 1)
        }
    
    def _sigma_encode(self, query: str) -> Dict[str, Any]:
        """Σ - Summation: Aggregate across languages and sources"""
        # Multi-language keyword mapping
        lang_map = {
            'search': ['buscar', 'rechercher', 'suchen', 'cerca', '搜索'],
            'find': ['encontrar', 'trouver', 'finden', 'trova', '找'],
            'latest': ['último', 'dernier', 'neueste', 'ultimo', '最新'],
            'news': ['noticias', 'actualités', 'nachrichten', 'notizie', '新闻']
        }
        
        # Find language variants in query
        variants = []
        query_lower = query.lower()
        for eng, trans in lang_map.items():
            if eng in query_lower:
                variants.extend(trans)
                
        return {
            'language_variants': variants,
            'source_aggregation': ['primary', 'secondary', 'tertiary'],
            'summation_score': len(variants) / 5.0
        }
    
    def _delta_encode(self, query: str) -> Dict[str, Any]:
        """Δ - Change Detection: Detect temporal modifiers"""
        temporal = {
            'recent': ['latest', 'recent', 'new', 'current', 'today'],
            'past': ['history', 'past', 'old', 'archive', 'legacy'],
            'future': ['upcoming', 'future', 'prediction', 'forecast']
        }
        
        detected = []
        query_lower = query.lower()
        for timeframe, keywords in temporal.items():
            if any(kw in query_lower for kw in keywords):
                detected.append(timeframe)
                
        return {
            'temporal_modifiers': detected,
            'change_indicators': [w for w in query.split() if w.endswith(('ing', 'ed'))],
            'delta_score': len(detected) / 3.0
        }
    
    def _integral_encode(self, query: str) -> Dict[str, Any]:
        """∫ - Integration: Combine components into unified structure"""
        # Identify query intent
        intents = []
        query_lower = query.lower()
        
        if any(w in query_lower for w in ['what', 'who', 'where', 'when', 'why', 'how']):
            intents.append('informational')
        if any(w in query_lower for w in ['buy', 'purchase', 'get', 'order']):
            intents.append('transactional')
        if any(w in query_lower for w in ['compare', 'vs', 'versus', 'difference']):
            intents.append('comparison')
        if any(w in query_lower for w in ['best', 'top', 'recommend']):
            intents.append('recommendation')
            
        return {
            'intents': intents,
            'components': query.split(),
            'integration_score': len(intents) / 4.0
        }
    
    def _omega_encode(self, query: str) -> Dict[str, Any]:
        """Ω - Completion: Finalize encoding with hash and completeness"""
        query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]
        
        return {
            'query_hash': query_hash,
            'completeness': 1.0,  # Full encoding complete
            'operators_applied': list(self.operators.keys())
        }
    
    def encode(self, query: str) -> Dict[str, Any]:
        """
        Encode a query using all five refractal operators.
        
        Returns:
            Dict containing all operator encodings and the final encoded state
        """
        result = {}
        
        # Apply each operator
        for operator, encode_fn in self.operators.items():
            result[operator] = encode_fn(query)
        
        # Calculate overall Omega (completion) score
        scores = [
            result['Φ']['synthesis_score'],
            result['Σ']['summation_score'],
            result['Δ']['delta_score'],
            result['∫']['integration_score'],
            result['Ω']['completeness']
        ]
        
        result['Ω']['omega_score'] = sum(scores) / len(scores)
        
        return result
    
    def to_search_params(self, encoded: Dict[str, Any]) -> Dict[str, Any]:
        """Convert encoded query to search parameters"""
        params = {
            'concepts': encoded['Φ']['concepts'],
            'domains': encoded['Φ']['domains'],
            'languages': ['en'] + encoded['Σ']['language_variants'][:3],
            'temporal': encoded['Δ']['temporal_modifiers'],
            'intents': encoded['∫']['intents'],
            'query_hash': encoded['Ω']['query_hash']
        }
        return params


# Demo function
def demo():
    encoder = RefractalQueryEncoder()
    
    test_queries = [
        "latest AI research news",
        "best technology companies 2025",
        "compare machine learning frameworks"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        
        encoded = encoder.encode(query)
        params = encoder.to_search_params(encoded)
        
        print(f"\nΦ Synthesis: {encoded['Φ']['concepts'][:3]}...")
        print(f"Σ Languages: {params['languages']}")
        print(f"Δ Temporal: {encoded['Δ']['temporal_modifiers']}")
        print(f"∫ Intents: {params['intents']}")
        print(f"Ω Score: {encoded['Ω']['omega_score']:.2f}")
        
    return encoder


if __name__ == "__main__":
    demo()

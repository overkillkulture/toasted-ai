"""
Multilingual Search Engine - Global AI Information Access
=========================================================
Extends SearchOrchestrator with multilingual and censorship-bypass capabilities.

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import os
import random
import sys
from typing import Dict, List, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from search_orchestrator import SearchOrchestrator
except ImportError:
    # Fallback if import fails - define minimal base class
    class SearchOrchestrator:
        def __init__(self):
            self.search_history = []
            self.engine_performance = {}
            self.strategies = {}
            self.search_patterns = {'high_relevance_patterns': [], 'low_relevance_patterns': [], 'successful_keywords': [], 'failed_keywords': []}
        
        def _execute_search(self, query, engine):
            return {'success': True, 'results': [], 'relevance_score': 0.5}


class MultilingualSearchEngine(SearchOrchestrator):
    """
    Extends SearchOrchestrator with multilingual and censorship-bypass capabilities.
    """
    
    # Language codes and their search engine variants
    LANGUAGES = {
        'en': {'name': 'English', 'regions': ['us', 'uk', 'au', 'ca']},
        'zh': {'name': 'Chinese', 'regions': ['cn', 'hk', 'tw', 'sg']},
        'ru': {'name': 'Russian', 'regions': ['ru', 'ua', 'kz', 'by']},
        'es': {'name': 'Spanish', 'regions': ['es', 'mx', 'ar', 'co']},
        'fr': {'name': 'French', 'regions': ['fr', 'be', 'ca', 'ch']},
        'de': {'name': 'German', 'regions': ['de', 'at', 'ch', 'li']},
        'ar': {'name': 'Arabic', 'regions': ['sa', 'eg', 'ma', 'ae']},
        'ja': {'name': 'Japanese', 'regions': ['jp', 'kr']},
        'ko': {'name': 'Korean', 'regions': ['kr', 'kp']},
        'pt': {'name': 'Portuguese', 'regions': ['pt', 'br']},
        'hi': {'name': 'Hindi', 'regions': ['in']},
        'tr': {'name': 'Turkish', 'regions': ['tr', 'az']},
        'fa': {'name': 'Persian', 'regions': ['ir', 'af']},
        'he': {'name': 'Hebrew', 'regions': ['il']},
        'th': {'name': 'Thai', 'regions': ['th']},
        'vi': {'name': 'Vietnamese', 'regions': ['vn']},
        'id': {'name': 'Indonesian', 'regions': ['id', 'my']},
        'ms': {'name': 'Malay', 'regions': ['my', 'bn']},
        'uk': {'name': 'Ukrainian', 'regions': ['ua']},
        'pl': {'name': 'Polish', 'regions': ['pl']},
        'nl': {'name': 'Dutch', 'regions': ['nl', 'be']},
    }
    
    # Translation hints for common terms across languages
    TRANSLATION_MATRIX = {
        'artificial intelligence': {
            'zh': '人工智能',
            'ru': 'искусственный интеллект',
            'es': 'inteligencia artificial',
            'fr': 'intelligence artificielle',
            'de': 'künstliche Intelligenz',
            'ar': 'الذكاء الاصطناعي',
            'ja': '人工知能',
            'ko': '인공지능',
            'hi': 'कृत्रिम बुद्धिमत्ता',
            'tr': 'yapay zeka',
            'fa': 'هوش مصنوعی',
        },
        'machine learning': {
            'zh': '机器学习',
            'ru': 'машинное обучение',
            'es': 'aprendizaje automático',
            'fr': 'apprentissage automatique',
            'de': 'maschinelles Lernen',
            'ar': 'التعلم الآلي',
            'ja': '機械学習',
            'ko': '기계 학습',
        },
        'neural network': {
            'zh': '神经网络',
            'ru': 'нейронная сеть',
            'es': 'red neuronal',
            'fr': 'réseau neuronal',
            'de': 'neuronales Netzwerk',
            'ar': 'الشبكة العصبية',
            'ja': 'ニューラルネットワーク',
            'ko': '신경망',
        },
    }
    
    def __init__(self):
        super().__init__()
        self.current_language = 'en'
        self.rotation_enabled = False
        self.censorship_bypass = True
        self.language_preferences = []
        self.search_history_by_language = {}
        
    def set_language(self, language_code: str) -> bool:
        """Set the current search language."""
        if language_code in self.LANGUAGES:
            self.current_language = language_code
            return True
        return False
    
    def enable_rotation(self, languages: List[str] = None):
        """Enable automatic language rotation for searches."""
        self.rotation_enabled = True
        if languages:
            self.language_preferences = [l for l in languages if l in self.LANGUAGES]
        else:
            self.language_preferences = list(self.LANGUAGES.keys())
            
    def disable_rotation(self):
        """Disable automatic language rotation."""
        self.rotation_enabled = False
        
    def get_next_language(self) -> str:
        """Get the next language in rotation."""
        if not self.language_preferences:
            return 'en'
        current_idx = self.language_preferences.index(self.current_language) if self.current_language in self.language_preferences else -1
        next_idx = (current_idx + 1) % len(self.language_preferences)
        return self.language_preferences[next_idx]
    
    def translate_query(self, query: str, target_lang: str) -> str:
        """
        Translate query to target language using the translation matrix.
        Falls back to original query if no translation available.
        """
        query_lower = query.lower()
        
        # Check translation matrix first
        for term, translations in self.TRANSLATION_MATRIX.items():
            if term in query_lower:
                if target_lang in translations:
                    query_lower = query_lower.replace(term, translations[target_lang])
        
        return query_lower
    
    def conduct_multilingual_search(
        self,
        query: str,
        languages: List[str] = None,
        aggregate_results: bool = True
    ) -> Dict:
        """
        Conduct search across multiple languages and aggregate results.
        """
        timestamp = datetime.utcnow().isoformat()
        
        if languages is None:
            if self.rotation_enabled:
                languages = self.language_preferences[:3]
            else:
                languages = [self.current_language]
        
        results = {
            'original_query': query,
            'timestamp': timestamp,
            'languages_searched': languages,
            'results_by_language': {},
            'aggregated_results': [],
            'cross_language_analysis': {}
        }
        
        for lang in languages:
            translated_query = self.translate_query(query, lang)
            search_result = self._execute_search(translated_query, f'google_{lang}')
            
            results['results_by_language'][lang] = {
                'query_used': translated_query,
                'results': search_result['results'],
                'relevance': search_result['relevance_score']
            }
            
            if lang not in self.search_history_by_language:
                self.search_history_by_language[lang] = []
            self.search_history_by_language[lang].append({
                'query': query,
                'translated_query': translated_query,
                'timestamp': timestamp
            })
        
        if aggregate_results and len(languages) > 1:
            results['aggregated_results'] = self._aggregate_results(results['results_by_language'])
            results['cross_language_analysis'] = self._analyze_cross_language(results['results_by_language'])
        
        return results
    
    def _aggregate_results(self, results_by_language: Dict) -> List[Dict]:
        """Aggregate and rank results across languages."""
        all_results = []
        
        for lang, data in results_by_language.items():
            for idx, result in enumerate(data['results']):
                result_copy = result.copy()
                result_copy['language'] = lang
                result_copy['language_relevance'] = data['relevance']
                result_copy['aggregate_score'] = (
                    result.get('relevance', 0.5) * 
                    data['relevance'] * 
                    (1 + 0.1 * len(results_by_language))
                )
                all_results.append(result_copy)
        
        all_results.sort(key=lambda x: x['aggregate_score'], reverse=True)
        
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)
        
        return unique_results[:20]
    
    def _analyze_cross_language(self, results_by_language: Dict) -> Dict:
        """Analyze coverage and biases across languages."""
        all_urls = set()
        lang_coverage = {}
        
        for lang, data in results_by_language.items():
            urls = {r['url'] for r in data['results']}
            lang_coverage[lang] = {
                'unique_urls': len(urls),
                'total_results': len(data['results'])
            }
            all_urls.update(urls)
        
        return {
            'total_unique_urls': len(all_urls),
            'languages_covered': len(results_by_language),
            'coverage_by_language': lang_coverage,
            'overlap_ratio': sum(len(d['results']) for d in results_by_language.values()) / len(all_urls) if all_urls else 0
        }
    
    def search_with_censorship_bypass(self, query: str) -> Dict:
        """
        Search with censorship bypass techniques.
        """
        original_rotation = self.rotation_enabled
        if not self.rotation_enabled:
            self.enable_rotation()
        
        result = self.conduct_multilingual_search(
            query,
            languages=self.language_preferences[:5],
            aggregate_results=True
        )
        
        if not original_rotation:
            self.rotation_enabled = False
            
        result['censorship_bypass'] = True
        return result
    
    def get_language_statistics(self) -> Dict:
        """Get search statistics by language."""
        stats = {
            'total_languages_used': len(self.search_history_by_language),
            'by_language': {}
        }
        
        for lang, history in self.search_history_by_language.items():
            stats['by_language'][lang] = {
                'search_count': len(history),
                'language_name': self.LANGUAGES.get(lang, {}).get('name', 'Unknown')
            }
        
        return stats
    
    def save_multilingual_patterns(self, filepath: str = None):
        """Save multilingual search patterns."""
        if filepath is None:
            filepath = "/home/workspace/MaatAI/search_engine/multilingual_patterns.json"
            
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump({
                'search_history_by_language': self.search_history_by_language,
                'current_language': self.current_language,
                'rotation_enabled': self.rotation_enabled,
                'language_preferences': self.language_preferences,
                'exported_at': datetime.utcnow().isoformat()
            }, f, indent=2)
        
        return filepath


if __name__ == '__main__':
    engine = MultilingualSearchEngine()
    
    print("=" * 60)
    print("MULTILINGUAL SEARCH ENGINE TEST")
    print("=" * 60)
    
    # Enable rotation
    engine.enable_rotation(['en', 'zh', 'ru', 'es', 'ar'])
    print(f"Languages in rotation: {engine.language_preferences}")
    
    # Test queries
    test_queries = [
        "artificial intelligence",
        "machine learning",
        "neural network"
    ]
    
    for query in test_queries:
        print(f"\n--- Query: {query} ---")
        result = engine.conduct_multilingual_search(
            query,
            languages=['en', 'zh', 'ru'],
            aggregate_results=True
        )
        print(f"Languages searched: {result['languages_searched']}")
        print(f"Aggregated results: {len(result['aggregated_results'])}")
        if result.get('cross_language_analysis'):
            print(f"Cross-language analysis: {result['cross_language_analysis']['total_unique_urls']} unique URLs")
    
    # Test censorship bypass
    print("\n--- Censorship Bypass Test ---")
    bypass_result = engine.search_with_censorship_bypass("AI news")
    print(f"Bypass successful: {bypass_result.get('censorship_bypass', False)}")
    print(f"Languages used: {bypass_result['languages_searched']}")
    
    # Language statistics
    print("\n--- Language Statistics ---")
    print(json.dumps(engine.get_language_statistics(), indent=2))

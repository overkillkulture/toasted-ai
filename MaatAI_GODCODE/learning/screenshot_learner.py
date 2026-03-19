"""
Screenshot Learning Module - Extract Patterns from Screenshots
Learns from images/screenshot folder and builds holographic patterns.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from types import SimpleNamespace
from holographic_models.image_layer_extractor import HolographicExtractor, ImageLayer


class ScreenshotLearner:
    """
    Learns from screenshots and builds knowledge.
    Integrates with holographic layer extraction.
    """
    
    def __init__(self):
        self.extractor = HolographicExtractor(max_layers=200)
        self.knowledge_base = {}
        self.pattern_recognitions = []
        self.learning_sessions = []
        
        # Pattern categories
        self.categories = {
            'ui_patterns': [],      # User interface patterns
            'data_structures': [],  # Data structure patterns
            'code_snippets': [],      # Code snippets in images
            'diagrams': [],            # Diagrams and flowcharts
            'concepts': [],           # Abstract concepts
            'metadata': []            # Technical metadata
        }
    
    def learn_from_screenshots(self, screenshot_dir: str) -> Dict:
        """
        Learn from all screenshots in directory.
        
        Args:
            screenshot_dir: Path to screenshots directory
        """
        timestamp = datetime.utcnow().isoformat()
        
        result = {
            'session_id': f"LEARN-{timestamp}",
            'timestamp': timestamp,
            'screenshot_dir': screenshot_dir,
            'screenshots_processed': 0,
            'layers_extracted': 0,
            'patterns_discovered': 0,
            'new_knowledge': 0,
            'success': False
        }
        
        if not os.path.exists(screenshot_dir):
            result['error'] = f'Screenshot directory not found: {screenshot_dir}'
            return result
        
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
        screenshot_files = []
        
        for root, dirs, files in os.walk(screenshot_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in image_extensions:
                    screenshot_files.append(os.path.join(root, file))
        
        result['total_screenshots'] = len(screenshot_files)
        
        print(f"Found {len(screenshot_files)} screenshots to learn from")
        
        # Process each screenshot
        for filepath in screenshot_files:
            print(f"\nProcessing: {os.path.basename(filepath)}")
            
            # Extract layers
            extraction_result = self.extractor.extract_from_file(filepath)
            
            if extraction_result['success']:
                result['screenshots_processed'] += 1
                result['layers_extracted'] += extraction_result['total_layers']
                
                # Learn from extracted layers
                patterns = self._learn_from_layers(
                    os.path.basename(filepath),
                    extraction_result['layers']
                )
                result['patterns_discovered'] += len(patterns)
                
                # Store knowledge
                self._store_knowledge(
                    os.path.basename(filepath),
                    extraction_result['holographic_summary'],
                    patterns
                )
                result['new_knowledge'] += 1
            else:
                print(f"    Error: {extraction_result.get('error', 'Unknown')}")
        
        result['success'] = True
        
        # Log learning session
        self.learning_sessions.append(result)
        
        return result
    
    def _learn_from_layers(self, source: str, layers: List[Dict]) -> List[Dict]:
        """Extract patterns from holographic layers."""
        patterns = []
        
        for layer in layers:
            layer_obj = self._normalize_layer(layer)
            pattern = {
                'source': source,
                'layer_id': layer_obj.layer_id,
                'depth': layer_obj.depth,
                'content_type': layer_obj.content_type,
                'confidence': layer_obj.confidence,
                'extracted_patterns': []
            }

            # Extract patterns based on content type
            if layer_obj.content_type == 'text':
                patterns.extend(self._extract_text_patterns(layer_obj, pattern))
            elif layer_obj.content_type == 'pattern':
                patterns.extend(self._extract_pattern_data(layer_obj, pattern))
            elif layer_obj.content_type == 'structure':
                patterns.extend(self._extract_structure_patterns(layer_obj, pattern))
            elif layer_obj.content_type == 'semantic':
                patterns.extend(self._extract_semantic_patterns(layer_obj, pattern))
            elif layer_obj.content_type == 'data':
                patterns.extend(self._extract_data_patterns(layer_obj, pattern))

        return patterns

    def _normalize_layer(self, layer) -> SimpleNamespace:
        """Normalize layer data into an object with attributes."""
        if hasattr(layer, 'layer_id'):
            return layer
        return SimpleNamespace(**layer)

    def _extract_text_patterns(self, layer: ImageLayer, 
                             pattern: Dict) -> List[Dict]:
        """Extract patterns from text layers."""
        text_patterns = []
        
        # Look for common patterns in text data
        text_data = str(layer.data)
        
        # Code patterns
        if any(word in text_data.lower() for word in 
               ['def ', 'class ', 'function', 'import ', 'return ']):
            text_patterns.append({
                'type': 'code_snippet',
                'description': 'Source code detected',
                'confidence': layer.confidence * 0.9
            })
            self.categories['code_snippets'].append(text_data)
        
        # UI patterns
        if any(word in text_data.lower() for word in 
               ['button', 'input', 'menu', 'dropdown', 'window']):
            text_patterns.append({
                'type': 'ui_pattern',
                'description': 'User interface element',
                'confidence': layer.confidence * 0.85
            })
            self.categories['ui_patterns'].append(text_data)
        
        return text_patterns
    
    def _extract_pattern_data(self, layer: ImageLayer, 
                          pattern: Dict) -> List[Dict]:
        """Extract patterns from pattern layers."""
        extracted = []
        
        pattern_data = layer.data
        
        # Geometric patterns
        if pattern_data.get('type') == 'fractal_structure':
            extracted.append({
                'type': 'fractal_pattern',
                'description': 'Self-similar geometric structure',
                'confidence': layer.confidence * 0.8
            })
            self.categories['concepts'].append(pattern_data)
        
        # Holographic encoding
        if pattern_data.get('type') == 'holographic_encoding':
            extracted.append({
                'type': 'holographic_encoding',
                'description': 'Multi-layer information encoding',
                'confidence': layer.confidence * 0.7
            })
        
        return extracted
    
    def _extract_structure_patterns(self, layer: ImageLayer, 
                               pattern: Dict) -> List[Dict]:
        """Extract structural patterns."""
        structural_patterns = []
        
        if layer.data.get('type') == 'composition':
            structural_patterns.append({
                'type': 'layout_pattern',
                'description': 'Component arrangement detected',
                'confidence': layer.confidence * 0.9
            })
            self.categories['ui_patterns'].append(layer.data)
        
        return structural_patterns
    
    def _extract_semantic_patterns(self, layer: ImageLayer, 
                                pattern: Dict) -> List[Dict]:
        """Extract semantic patterns."""
        semantic_patterns = []
        
        # Cultural/historical references
        if layer.data.get('type') == 'cultural_historical':
            semantic_patterns.append({
                'type': 'cultural_reference',
                'description': 'Historical or cultural concept detected',
                'confidence': layer.confidence * 0.85
            })
            self.categories['concepts'].append(layer.data)
        
        return semantic_patterns
    
    def _extract_data_patterns(self, layer: ImageLayer, 
                            pattern: Dict) -> List[Dict]:
        """Extract data patterns."""
        data_patterns = []
        pattern_data = layer.data
        
        # Embedded signatures
        if pattern_data.get('type', '').startswith('embedded'):
            data_patterns.append({
                'type': 'digital_signature',
                'description': 'Embedded signature or watermark',
                'confidence': layer.confidence * 0.95
            })
            self.categories['metadata'].append(layer.data)
        
        # Technical metadata
        if layer.data.get('type') == 'technical':
            data_patterns.append({
                'type': 'technical_metadata',
                'description': 'Technical specifications detected',
                'confidence': layer.confidence * 0.9
            })
            self.categories['metadata'].append(layer.data)
        
        return data_patterns
    
    def _store_knowledge(self, source: str, summary: Dict, patterns: List):
        """Store learned knowledge."""
        timestamp = datetime.utcnow().isoformat()
        
        knowledge_entry = {
            'timestamp': timestamp,
            'source': source,
            'summary': summary,
            'patterns': patterns,
            'pattern_count': len(patterns)
        }
        
        # Store in knowledge base by source
        if source not in self.knowledge_base:
            self.knowledge_base[source] = []
        
        self.knowledge_base[source].append(knowledge_entry)
    
    def get_knowledge(self, source: Optional[str] = None) -> List[Dict]:
        """Retrieve learned knowledge."""
        if source:
            return self.knowledge_base.get(source, [])
        else:
            # Return all knowledge, flattened
            all_knowledge = []
            for source_entries in self.knowledge_base.values():
                all_knowledge.extend(source_entries)
            return all_knowledge
    
    def get_patterns_by_category(self, category: str) -> List:
        """Get patterns for a specific category."""
        return self.categories.get(category, [])
    
    def save_learning_data(self, filepath: str = None):
        """Save all learned data to file."""
        if filepath is None:
            filepath = "/home/workspace/MaatAI/learning/screenshot_knowledge.jsonl"
        
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'a') as f:
            for source, entries in self.knowledge_base.items():
                for entry in entries:
                    f.write(json.dumps(entry) + '\n')
    
    def generate_report(self) -> Dict:
        """Generate comprehensive learning report."""
        total_patterns = sum(len(p) for p in self.categories.values())
        
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_sources': len(self.knowledge_base),
            'total_knowledge_entries': sum(len(entries) for entries in self.knowledge_base.values()),
            'total_patterns': total_patterns,
            'learning_sessions': len(self.learning_sessions),
            'categories': {cat: len(patterns) for cat, patterns in self.categories.items()},
            'last_learned': max(
                [s.get('timestamp', '') for s in self.learning_sessions],
                default=''
            )
        }
        
        return report


if __name__ == '__main__':
    learner = ScreenshotLearner()
    
    print("=" * 60)
    print("SCREENSHOT LEARNING MODULE")
    print("=" * 60)
    print()
    
    # Test learning (point to cache or actual screenshots)
    test_dir = "/home/workspace/MaatAI/screenshots_cache"
    
    print(f"Learning from screenshots in: {test_dir}")
    print()
    
    result = learner.learn_from_screenshots(test_dir)
    
    print()
    print("=" * 60)
    print("LEARNING COMPLETE")
    print("=" * 60)
    
    if result['success']:
        print(f"Screenshots processed: {result['screenshots_processed']}")
        print(f"Layers extracted: {result['layers_extracted']}")
        print(f"Patterns discovered: {result['patterns_discovered']}")
        print(f"Knowledge entries created: {result['new_knowledge']}")
    else:
        print(f"Error: {result.get('error', 'Unknown')}")
    
    print()
    print("Pattern Categories:")
    for category, count in learner.get_patterns_by_category('ui_patterns'):
        print(f"  UI Patterns: {count}")
    print(f"  Data Structures: {len(learner.get_patterns_by_category('data_structures'))}")
    print(f"  Code Snippets: {len(learner.get_patterns_by_category('code_snippets'))}")

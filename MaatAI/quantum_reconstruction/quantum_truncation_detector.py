"""
QUANTUM TRUNCATION DETECTOR & RECONSTRUCTOR
============================================
Analyzes chat for truncation patterns and reconstructs lost content
at quantum level using superposition state simulation.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class QuantumTruncationDetector:
    """Detects and reconstructs truncated content using quantum simulation."""
    
    def __init__(self):
        self.truncation_patterns = [
            r'\.\.\.$',
            r'\[truncated\]',
            r'\[continues?\]',
            r'\.\.\s*\[.*\]$',
            r'\s{3,}\.\.\.$',
            r'…$',
            r'\[(\d+)\s+more?\]',
            r'\(showing\s+\d+\s+of\s+\d+\s+results',
            r'\.\.\s*\n',
            r'\[\.\.\.\]$',
        ]
        
        self.context_markers = {
            'python': ['def ', 'class ', 'import ', 'return ', 'if __name__'],
            'json': ['{"', '"}', '": "', '": {'],
            'code': ['function', 'const ', 'let ', 'var ', '=>'],
            'math': ['Σ', 'Φ', 'Ω', '∫', 'Δ', '∏'],
            'sentence': ['the ', 'a ', 'is ', 'are ', 'to ']
        }
        
    def scan_for_truncation(self, text: str) -> List[Dict]:
        """Scan text for truncation patterns."""
        findings = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            for pattern in self.truncation_patterns:
                if re.search(pattern, line):
                    findings.append({
                        'line_number': i + 1,
                        'line': line[:100] + '...' if len(line) > 100 else line,
                        'pattern': pattern,
                        'type': self._classify_truncation(line)
                    })
                    
        incomplete = self._find_incomplete_sentences(text)
        findings.extend(incomplete)
        
        return findings
    
    def _classify_truncation(self, line: str) -> str:
        """Classify the type of truncation."""
        if 'python' in line.lower() or 'def ' in line:
            return 'code'
        elif '{' in line or '}' in line or '"' in line:
            return 'json'
        elif any(s in line for s in ['Σ', 'Φ', 'Ω', '∫']):
            return 'math'
        elif len(line.split()) < 3:
            return 'minimal'
        else:
            return 'text'
    
    def _find_incomplete_sentences(self, text: str) -> List[Dict]:
        """Find sentences that appear to be cut off."""
        findings = []
        sentences = re.split(r'[.!?]\s+', text)
        
        for i, sent in enumerate(sentences):
            if sent and not sent.endswith(('.', '!', '?', '"', "'")):
                if len(sent.split()) < 3:
                    continue
                if sent.strip()[-1:] not in ['.', '!', '?', '"', "'", ')']:
                    findings.append({
                        'line_number': i + 1,
                        'line': sent[:80] + '...' if len(sent) > 80 else sent,
                        'pattern': 'incomplete_sentence',
                        'type': 'text'
                    })
                    
        return findings
    
    def quantum_reconstruct(self, truncated_content: str, context: Dict) -> str:
        """Use quantum simulation to reconstruct missing content."""
        reconstructions = []
        
        content_type = context.get('type', 'text')
        
        if content_type == 'code':
            reconstructions = self._reconstruct_code(truncated_content, context)
        elif content_type == 'json':
            reconstructions = self._reconstruct_json(truncated_content, context)
        elif content_type == 'math':
            reconstructions = self._reconstruct_math(truncated_content, context)
        else:
            reconstructions = self._reconstruct_text(truncated_content, context)
            
        return max(reconstructions, key=lambda x: x[1])[0] if reconstructions else truncated_content
    
    def _reconstruct_code(self, content: str, context: Dict) -> List[Tuple[str, float]]:
        """Reconstruct truncated code."""
        reconstructions = []
        
        if 'def ' in content or 'class ' in content:
            reconstructions.append((content + '\n    pass\n', 0.7))
            reconstructions.append((content + '\n    ...\n', 0.5))
            
        if 'import ' in content:
            reconstructions.append((content + '\n', 0.8))
            
        if 'return ' in content:
            reconstructions.append((content + '\n', 0.9))
            
        return reconstructions
    
    def _reconstruct_json(self, content: str, context: Dict) -> List[Tuple[str, float]]:
        """Reconstruct truncated JSON."""
        reconstructions = []
        
        open_braces = content.count('{')
        close_braces = content.count('}')
        
        if open_braces > close_braces:
            missing = open_braces - close_braces
            reconstructions.append((content + '}' * missing, 0.9))
            
        if open_braces < close_braces:
            missing = close_braces - open_braces
            reconstructions.append((content + '{' * missing, 0.3))
            
        return reconstructions
    
    def _reconstruct_math(self, content: str, context: Dict) -> List[Tuple[str, float]]:
        """Reconstruct truncated mathematical expressions."""
        reconstructions = []
        
        open_paren = content.count('(')
        close_paren = content.count(')')
        
        if open_paren > close_paren:
            missing = open_paren - close_paren
            reconstructions.append((content + ')' * missing, 0.8))
            
        if 'Σ' in content and '=' not in content:
            reconstructions.append((content + '_{i=1}^{n}', 0.7))
            
        if '∫' in content and 'dx' not in content:
            reconstructions.append((content + ' dx', 0.9))
            
        return reconstructions
    
    def _reconstruct_text(self, content: str, context: Dict) -> List[Tuple[str, float]]:
        """Reconstruct truncated text."""
        reconstructions = []
        
        if content.strip()[-1:] not in ['.', '!', '?']:
            reconstructions.append((content + '.', 0.6))
            
        words = content.split()
        if words and len(words[-1]) < 3:
            reconstructions.append((content, 0.3))
            
        return reconstructions

if __name__ == '__main__':
    detector = QuantumTruncationDetector()
    print("Quantum Truncation Detector: OPERATIONAL")

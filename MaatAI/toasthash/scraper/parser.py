"""
ToastHash Content Parser
======================
Advanced content extraction and parsing for crawled data.

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import re
import json
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class ParserType(Enum):
    HTML = "html"
    JSON = "json"
    TEXT = "text"
    STRUCTURED = "structured"

@dataclass
class ParsedContent:
    """Structured content from parsing"""
    title: str
    text: str
    links: List[str]
    images: List[str]
    metadata: Dict
    entities: List[Dict]
    
class ContentParser:
    """
    Advanced Content Parser
    
    Features:
    - Multi-format parsing (HTML, JSON, Text)
    - Entity extraction
    - Metadata extraction
    - Content classification
    - Schema.org support
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self):
        self.entity_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "url": r'https?://[^\s<>"{}|\\^`\[\]]+',
            "ip": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            "date": r'\b\d{4}-\d{2}-\d{2}\b',
            "price": r'\$[\d,]+\.?\d*',
        }
        
    def parse_html(self, html: str) -> ParsedContent:
        """Parse HTML content"""
        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
        title = title_match.group(1) if title_match else ""
        
        # Remove scripts and styles
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Extract links
        links = re.findall(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE)
        
        # Extract images
        images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
        
        # Extract metadata
        metadata = {}
        meta_pattern = re.compile(r'<meta[^>]+(?:name|property)=["\']([^"\']+)["\'][^>]+content=["\']([^"\']+)["\']', re.IGNORECASE)
        for match in meta_pattern.finditer(html):
            metadata[match.group(1)] = match.group(2)
            
        # Extract entities
        entities = self.extract_entities(text)
        
        return ParsedContent(
            title=title,
            text=text,
            links=links,
            images=images,
            metadata=metadata,
            entities=entities,
        )
        
    def parse_json(self, data: Any) -> ParsedContent:
        """Parse JSON content"""
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                return None
                
        # Convert to string for text extraction
        text = json.dumps(data)
        
        # Recursively extract from nested structures
        links = []
        images = []
        
        def extract_urls(obj):
            if isinstance(obj, str):
                if obj.startswith(("http://", "https://")):
                    if any(ext in obj.lower() for ext in [".jpg", ".png", ".gif", ".webp"]):
                        images.append(obj)
                    else:
                        links.append(obj)
            elif isinstance(obj, dict):
                for v in obj.values():
                    extract_urls(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract_urls(item)
                    
        extract_urls(data)
        
        return ParsedContent(
            title=data.get("title", ""),
            text=text,
            links=list(set(links)),
            images=list(set(images)),
            metadata={},
            entities=[],
        )
        
    def extract_entities(self, text: str) -> List[Dict]:
        """Extract entities from text"""
        entities = []
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                entities.append({
                    "type": entity_type,
                    "value": match,
                })
                
        return entities
        
    def get_stats(self) -> Dict:
        """Get parser statistics"""
        return {
            "entity_types": list(self.entity_patterns.keys()),
            "divine_seal": self.DIVINE_SEAL,
        }

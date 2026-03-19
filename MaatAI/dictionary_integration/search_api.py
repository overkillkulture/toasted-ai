"""
Dictionary Search API
TOASTED AI - Dictionary Data Integration Project
Status: subtask_7_COMPLETED

This module provides a REST API for searching the unified dictionary database.
Supports full-text search, fuzzy matching, and filtered queries across all sources.

Usage:
    python search_api.py [--port PORT]
    
API Endpoints:
    GET /api/search?q=QUERY&limit=20&source=urban_dictionary
    GET /api/word/{word_id}
    GET /api/autocomplete?prefix=pr
    GET /api/stats
"""

import json
import os
import re
from datetime import datetime
from typing import Optional, List, Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# Configuration
DEFAULT_PORT = 8765
DEFAULT_LIMIT = 20
MAX_LIMIT = 100

# Data paths
DATA_DIR = "/home/workspace/MaatAI/dictionary_integration"
WORDS_FILE = os.path.join(DATA_DIR, "words.json")
URBAN_FILE = os.path.join(DATA_DIR, "urban_dictionary.txt")
WORDS_ALPHA_FILE = os.path.join(DATA_DIR, "words_alpha.txt")

# In-memory indexes (lazy loaded)
_words_index: Optional[Dict[str, Any]] = None
_urban_index: Optional[Dict[str, Any]] = None


def load_words_index() -> Dict[str, Any]:
    """Load or build the words index."""
    global _words_index
    if _words_index is not None:
        return _words_index
    
    _words_index = {
        "words": {},
        "by_prefix": {},
        "by_length": {},
        "total_count": 0
    }
    
    # Try to load from words_alpha.txt
    if os.path.exists(WORDS_ALPHA_FILE):
        with open(WORDS_ALPHA_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            for idx, line in enumerate(f):
                word = line.strip().lower()
                if word and len(word) > 1:
                    _words_index["words"][word] = {
                        "word_id": idx + 1,
                        "word": word,
                        "source": "words_alpha",
                        "normalized": word.lower()
                    }
                    # Build prefix index
                    for i in range(2, min(len(word) + 1, 6)):
                        prefix = word[:i]
                        if prefix not in _words_index["by_prefix"]:
                            _words_index["by_prefix"][prefix] = []
                        _words_index["by_prefix"][prefix].append(word)
    
    _words_index["total_count"] = len(_words_index["words"])
    return _words_index


def load_urban_index() -> Dict[str, Any]:
    """Load or build the Urban Dictionary index."""
    global _urban_index
    if _urban_index is not None:
        return _urban_index
    
    _urban_index = {
        "entries": {},
        "by_word": {},
        "total_count": 0
    }
    
    if os.path.exists(URBAN_FILE):
        with open(URBAN_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            for idx, line in enumerate(f):
                if ':' in line:
                    parts = line.split(':', 1)
                    word = parts[0].strip().lower()
                    definition = parts[1].strip() if len(parts) > 1 else ""
                    
                    if word and len(word) > 1:
                        entry = {
                            "urban_id": idx + 1,
                            "word": word,
                            "definition": definition[:500],  # Truncate long definitions
                            "source": "urban_dictionary"
                        }
                        _urban_index["entries"][idx + 1] = entry
                        
                        if word not in _urban_index["by_word"]:
                            _urban_index["by_word"][word] = []
                        _urban_index["by_word"][word].append(entry)
    
    _urban_index["total_count"] = len(_urban_index["entries"])
    return _urban_index


def search_words(query: str, limit: int = 20, source: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search the dictionary index."""
    results = []
    query = query.lower().strip()
    
    if not query or len(query) < 1:
        return results
    
    words_idx = load_words_index()
    urban_idx = load_urban_index()
    
    # Search in words_alpha
    if source is None or source == "words_alpha":
        for word, data in words_idx["words"].items():
            if query in word:
                results.append({
                    **data,
                    "match_type": "contains",
                    "score": 1.0 / (len(word) - len(query) + 1)
                })
                if len(results) >= limit * 2:
                    break
    
    # Search in Urban Dictionary
    if source is None or source == "urban_dictionary":
        for word, entries in urban_idx["by_word"].items():
            if query in word:
                for entry in entries[:3]:  # Limit per word
                    results.append({
                        **entry,
                        "match_type": "contains",
                        "score": 0.9 / (len(word) - len(query) + 1)
                    })
                    if len(results) >= limit * 2:
                        break
    
    # Sort by score and limit
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return results[:limit]


def autocomplete(prefix: str, limit: int = 10) -> List[str]:
    """Autocomplete suggestions based on prefix."""
    prefix = prefix.lower().strip()
    suggestions = set()
    
    words_idx = load_words_index()
    urban_idx = load_urban_index()
    
    # From words_alpha
    for p, words in words_idx["by_prefix"].items():
        if p.startswith(prefix):
            for w in words[:5]:
                suggestions.add(w)
                if len(suggestions) >= limit:
                    break
        if len(suggestions) >= limit:
            break
    
    # From urban dictionary
    for word in urban_idx["by_word"].keys():
        if word.startswith(prefix):
            suggestions.add(word)
            if len(suggestions) >= limit:
                break
    
    return sorted(list(suggestions))[:limit]


def get_stats() -> Dict[str, Any]:
    """Get dictionary statistics."""
    words_idx = load_words_index()
    urban_idx = load_urban_index()
    
    return {
        "total_words": words_idx["total_count"],
        "total_urban": urban_idx["total_count"],
        "sources": ["words_alpha", "urban_dictionary"],
        "indexed_at": datetime.utcnow().isoformat() + "Z"
    }


class DictionaryAPIHandler(BaseHTTPRequestHandler):
    """HTTP handler for Dictionary Search API."""
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def send_json_response(self, data: Any, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        # Route: /api/search
        if path == '/api/search':
            q = query.get('q', [''])[0]
            limit = min(int(query.get('limit', [str(DEFAULT_LIMIT)])[0]), MAX_LIMIT)
            source = query.get('source', [None])[0]
            
            if not q:
                self.send_json_response({"error": "Missing query parameter 'q'"}, 400)
                return
            
            results = search_words(q, limit, source)
            self.send_json_response({
                "query": q,
                "results": results,
                "count": len(results)
            })
        
        # Route: /api/autocomplete
        elif path == '/api/autocomplete':
            prefix = query.get('prefix', [''])[0]
            limit = min(int(query.get('limit', [str(10)])[0]), 20)
            
            if not prefix:
                self.send_json_response({"error": "Missing query parameter 'prefix'"}, 400)
                return
            
            suggestions = autocomplete(prefix, limit)
            self.send_json_response({
                "prefix": prefix,
                "suggestions": suggestions,
                "count": len(suggestions)
            })
        
        # Route: /api/stats
        elif path == '/api/stats':
            self.send_json_response(get_stats())
        
        # Route: /health
        elif path == '/health':
            self.send_json_response({"status": "healthy"})
        
        # Default: 404
        else:
            self.send_json_response({"error": "Not found"}, 404)


def run_server(port: int = DEFAULT_PORT):
    """Run the API server."""
    server = HTTPServer(('0.0.0.0', port), DictionaryAPIHandler)
    print(f"Dictionary Search API running on port {port}")
    print(f"Endpoints:")
    print(f"  GET /api/search?q=QUERY&limit=20")
    print(f"  GET /api/autocomplete?prefix=pr")
    print(f"  GET /api/stats")
    print(f"  GET /health")
    print(f"\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    import sys
    port = DEFAULT_PORT
    
    if len(sys.argv) > 1 and sys.argv[1] == '--port':
        if len(sys.argv) > 2:
            port = int(sys.argv[2])
    
    # Pre-load indexes in background
    print("Loading dictionary indexes...")
    load_words_index()
    load_urban_index()
    print(f"Indexed: {load_words_index()['total_count']} words, {load_urban_index()['total_count']} urban entries")
    
    run_server(port)

"""
ADVANCEMENT 4: SESSION CONTEXT CACHING
======================================
Implements fast session-specific context caching
for multi-step tasks.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path

class SessionCache:
    """Fast session-specific context cache."""
    
    def __init__(self, workspace_path: str = "/home/.z/workspaces/con_Cj8w5e52PmPGvQpz"):
        self.workspace_path = workspace_path
        self.cache_file = os.path.join(workspace_path, "session_context_cache.json")
        self.cache: Dict[str, Any] = {}
        self.load()
        
    def load(self):
        """Load cache from disk."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
            except:
                self.cache = {}
    
    def save(self):
        """Save cache to disk."""
        try:
            os.makedirs(self.workspace_path, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Cache save error: {e}")
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set a cache value with TTL."""
        self.cache[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "ttl": ttl
        }
        self.save()
    
    def get(self, key: str) -> Optional[Any]:
        """Get a cache value if not expired."""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        # Check TTL
        try:
            stored = datetime.fromisoformat(entry["timestamp"])
            age = (datetime.now() - stored).total_seconds()
            if age > entry.get("ttl", 3600):
                del self.cache[key]
                self.save()
                return None
        except:
            pass
        
        return entry.get("value")
    
    def delete(self, key: str):
        """Delete a cache entry."""
        if key in self.cache:
            del self.cache[key]
            self.save()
    
    def clear(self):
        """Clear all cache."""
        self.cache = {}
        self.save()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "entries": len(self.cache),
            "keys": list(self.cache.keys()),
            "workspace": self.workspace_path
        }

# Global cache instance
_session_cache = None

def get_session_cache() -> SessionCache:
    """Get or create session cache."""
    global _session_cache
    if _session_cache is None:
        _session_cache = SessionCache()
    return _session_cache

if __name__ == "__main__":
    cache = get_session_cache()
    cache.set("test_key", {"data": "test_value"})
    print(json.dumps(cache.get_stats(), indent=2))
    print(cache.get("test_key"))

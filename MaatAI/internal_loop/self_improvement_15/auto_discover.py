"""
ADVANCEMENT 1: AUTO-DISCOVERY ENGINE
=====================================
Discovers all files, modules, and architectures automatically.
Builds a comprehensive map of the entire TOASTED AI system.
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class AutoDiscoveryEngine:
    """Auto-discovers all files and architecture components."""
    
    def __init__(self, root_path: str = "/home/workspace/MaatAI"):
        self.root_path = root_path
        self.discovery_map = {}
        self.file_types = {}
        self.modules = {}
        self.dependencies = {}
        
    def discover_all(self) -> Dict[str, Any]:
        """Perform full system discovery."""
        print("🔍 Starting auto-discovery...")
        
        # Discover all files
        self.discovery_map = self._scan_directory(self.root_path)
        
        # Categorize by type
        self._categorize_files()
        
        # Build module map
        self._build_module_map()
        
        # Find dependencies
        self._analyze_dependencies()
        
        # Generate discovery report
        report = self._generate_report()
        
        print(f"✅ Discovered {len(self.discovery_map)} files across {len(self.modules)} modules")
        return report
    
    def _scan_directory(self, path: str) -> Dict[str, Any]:
        """Recursively scan directory."""
        result = {}
        try:
            for root, dirs, files in os.walk(path):
                # Skip hidden and cache dirs
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                
                for file in files:
                    if file.startswith('.'):
                        continue
                    full_path = os.path.join(root, file)
                    try:
                        stat = os.stat(full_path)
                        rel_path = os.path.relpath(full_path, self.root_path)
                        result[rel_path] = {
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            "extension": os.path.splitext(file)[1],
                            "hash": self._get_file_hash(full_path)
                        }
                    except:
                        pass
        except Exception as e:
            print(f"Error scanning {path}: {e}")
        return result
    
    def _categorize_files(self):
        """Categorize discovered files by type."""
        categories = {
            ".py": "python",
            ".md": "markdown", 
            ".json": "json",
            ".txt": "text",
            ".yaml": "yaml",
            ".yml": "yaml"
        }
        
        self.file_types = {cat: [] for cat in categories.values()}
        self.file_types["other"] = []
        
        for path, info in self.discovery_map.items():
            ext = info.get("extension", "")
            cat = categories.get(ext, "other")
            self.file_types[cat].append(path)
    
    def _build_module_map(self):
        """Build map of Python modules."""
        for path in self.file_types.get("python", []):
            if "__init__" in path or "/" not in path:
                module_name = os.path.dirname(path).replace("/", ".").strip(".")
                if module_name:
                    self.modules[module_name] = path
    
    def _analyze_dependencies(self):
        """Analyze Python file dependencies."""
        for path in self.file_types.get("python", []):
            try:
                with open(os.path.join(self.root_path, path), 'r') as f:
                    content = f.read()
                    imports = []
                    for line in content.split('\n'):
                        if line.startswith('import ') or line.startswith('from '):
                            imports.append(line.strip())
                    if imports:
                        self.dependencies[path] = imports
            except:
                pass
    
    def _get_file_hash(self, path: str) -> str:
        """Get SHA256 hash of file."""
        try:
            with open(path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()[:16]
        except:
            return "unknown"
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate discovery report."""
        return {
            "timestamp": datetime.now().isoformat(),
            "root_path": self.root_path,
            "total_files": len(self.discovery_map),
            "total_modules": len(self.modules),
            "file_types": {k: len(v) for k, v in self.file_types.items()},
            "modules": list(self.modules.keys())[:50],
            "total_dependencies": len(self.dependencies),
            "discovery_map": self.discovery_map,
            "modules_detail": self.modules,
            "dependencies": self.dependencies
        }

def run_discovery():
    """Run auto-discovery and return results."""
    engine = AutoDiscoveryEngine()
    return engine.discover_all()

if __name__ == "__main__":
    result = run_discovery()
    print(json.dumps(result, indent=2))

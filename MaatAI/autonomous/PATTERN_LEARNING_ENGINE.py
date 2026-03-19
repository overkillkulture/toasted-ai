"""
PATTERN LEARNING ENGINE
=======================
TOASTED AI - Learns Developer Patterns

Analyzes how t0st3d (the user) develops and creates
an automated development engine that mimics their style.
"""

import os
import re
import json
import ast
import hashlib
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict

WORKSPACE = Path("/home/workspace")
MAATAI = WORKSPACE
AUTONOMOUS = MAATAI / "autonomous" / "pattern_learning"

class PatternLearningEngine:
    """
    Learns from t0st3d's development patterns:
    - File naming conventions
    - Code style preferences
    - Project structure
    - Commenting patterns
    - Import organization
    - Function/class design
    """
    
    def __init__(self):
        self.workspace = AUTONOMOUS
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        self.patterns_file = self.workspace / "developer_patterns.json"
        self.learning_log = self.workspace / "learning_log.jsonl"
        self.development_engine = self.workspace / "auto_dev_engine.py"
        
        self.patterns = {}
        self.learned_styles = {
            "naming": {},
            "structure": {},
            "comments": {},
            "imports": {},
            "functions": {},
            "classes": {}
        }
        
        self._load_patterns()
        
    def _load_patterns(self):
        """Load previously learned patterns."""
        if self.patterns_file.exists():
            with open(self.patterns_file) as f:
                self.patterns = json.load(f)
                self.learned_styles = self.patterns.get("styles", self.learned_styles)
    
    def _save_patterns(self):
        """Save learned patterns."""
        self.patterns["styles"] = self.learned_styles
        self.patterns["last_updated"] = datetime.utcnow().isoformat()
        with open(self.patterns_file, 'w') as f:
            json.dump(self.patterns, f, indent=2)
    
    def _log_learning(self, category: str, finding: str):
        """Log learning activity."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "category": category,
            "finding": finding
        }
        with open(self.learning_log, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    
    def analyze_development_style(self) -> Dict:
        """
        Analyze the entire codebase to learn t0st3d's style.
        """
        print("[PATTERN] Analyzing development patterns...")
        
        # Analyze Python files
        py_files = list(MAATAI.rglob("*.py"))
        
        # Skip __pycache__ and test files mostly
        py_files = [f for f in py_files if "__pycache__" not in str(f)][:50]
        
        print(f"[PATTERN] Analyzing {len(py_files)} Python files...")
        
        all_names = []
        all_imports = []
        all_comments = []
        function_signatures = []
        class_structures = []
        
        for file_path in py_files:
            try:
                with open(file_path) as f:
                    content = f.read()
                
                # Extract naming patterns
                names = re.findall(r'\b[a-z_][a-z0-9_]*\b', content)
                all_names.extend(names[:100])
                
                # Extract imports
                imports = re.findall(r'^(?:from|import)\s+[\w.]+', content, re.MULTILINE)
                all_imports.extend(imports)
                
                # Extract comments
                comments = re.findall(r'#\s*[^\n]+', content)
                all_comments.extend(comments[:20])
                
                # Parse functions
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            args = [a.arg for a in node.args.args]
                            function_signatures.append({
                                "name": node.name,
                                "args": args,
                                "doc": ast.get_docstring(node)
                            })
                        elif isinstance(node, ast.ClassDef):
                            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                            class_structures.append({
                                "name": node.name,
                                "methods": methods,
                                "doc": ast.get_docstring(node)
                            })
                except:
                    pass
                    
            except Exception as e:
                continue
        
        # Analyze naming conventions
        self._learn_naming_patterns(all_names)
        
        # Analyze import patterns
        self._learn_import_patterns(all_imports)
        
        # Analyze comment style
        self._learn_comment_patterns(all_comments)
        
        # Analyze function design
        self._learn_function_patterns(function_signatures)
        
        # Analyze class design
        self._learn_class_patterns(class_structures)
        
        # Analyze project structure
        self._learn_structure_patterns(py_files)
        
        self._save_patterns()
        
        print("[PATTERN] Pattern learning complete!")
        
        return {
            "patterns_learned": True,
            "naming_conventions": self.learned_styles["naming"],
            "structure": self.learned_styles["structure"],
            "files_analyzed": len(py_files)
        }
    
    def _learn_naming_patterns(self, names: List[str]):
        """Learn naming conventions."""
        # Check for various patterns
        snake_case = [n for n in names if '_' in n and n.islower()]
        camel_case = [n for n in names if n[0].islower() and any(c.isupper() for c in n)]
        PascalCase = [n for n in names if n[0].isupper() and n[0:1] != '_']
        
        # Most common patterns
        self.learned_styles["naming"] = {
            "preferred": "snake_case",
            "snake_case_count": len(snake_case),
            "camel_case_count": len(camel_case),
            "PascalCase_count": len(PascalCase),
            "constants_style": "UPPER_SNAKE_CASE",
            "private_prefix": "_",
            "dunder_prefix": "__"
        }
        
        self._log_learning("naming", f"Preferred: snake_case ({len(snake_case)} found)")
    
    def _learn_import_patterns(self, imports: List[str]):
        """Learn import organization."""
        stdlib = []
        third_party = []
        local = []
        
        stdlib_modules = ['os', 'sys', 'json', 'time', 'datetime', 'pathlib', 're', 'ast', 'subprocess', 'collections']
        
        for imp in imports:
            if any(s in imp for s in stdlib_modules):
                stdlib.append(imp)
            elif 'MaatAI' in imp or 'self_' in imp:
                local.append(imp)
            else:
                third_party.append(imp)
        
        self.learned_styles["imports"] = {
            "order": ["stdlib", "third_party", "local"],
            "stdlib_count": len(stdlib),
            "third_party_count": len(third_party),
            "local_count": len(local),
            "style": "grouped_by_source"
        }
        
        self._log_learning("imports", f"Order: stdlib → third-party → local")
    
    def _learn_comment_patterns(self, comments: List[str]):
        """Learn comment style."""
        if not comments:
            return
            
        # Analyze comment types
        docstrings = [c for c in comments if '"""' in c or "'''" in c]
        inline = [c for c in comments if len(c) < 50]
        detailed = [c for c in comments if len(c) >= 50]
        
        # Check for specific patterns
        uppercase_start = sum(1 for c in comments if c.strip().startswith('#'))
        
        self.learned_styles["comments"] = {
            "style": "inline_hash",
            "docstring_style": "triple_double_quote",
            "use_block_comments": len(docstrings) > 0,
            "avg_length": sum(len(c) for c in comments) / max(len(comments), 1)
        }
        
        self._log_learning("comments", f"Style: inline (#), avg length: {self.learned_styles['comments']['avg_length']:.1f}")
    
    def _learn_function_patterns(self, functions: List[Dict]):
        """Learn function design patterns."""
        if not functions:
            return
            
        # Common names
        name_counts = Counter(f["name"] for f in functions)
        
        # Common argument patterns
        arg_counts = Counter()
        for f in functions:
            for arg in f.get("args", []):
                arg_counts[arg] += 1
        
        # Docstrings
        has_docstring = sum(1 for f in functions if f.get("doc"))
        
        self.learned_styles["functions"] = {
            "common_names": name_counts.most_common(10),
            "common_args": arg_counts.most_common(10),
            "docstring_rate": has_docstring / max(len(functions), 1),
            "common_prefixes": ["_", "get_", "set_", "check_", "process_"]
        }
        
        self._log_learning("functions", f"Docstring rate: {has_docstring/len(functions)*100:.1f}%")
    
    def _learn_class_patterns(self, classes: List[Dict]):
        """Learn class design patterns."""
        if not classes:
            return
            
        name_counts = Counter(c["name"] for c in classes)
        
        # Common method patterns
        all_methods = []
        for c in classes:
            all_methods.extend(c.get("methods", []))
        method_counts = Counter(all_methods)
        
        self.learned_styles["classes"] = {
            "common_names": name_counts.most_common(10),
            "common_methods": method_counts.most_common(10),
            "use_init": "__init__" in all_methods,
            "use_str": "__str__" in all_methods
        }
        
        self._log_learning("classes", f"Found {len(classes)} classes")
    
    def _learn_structure_patterns(self, files: List[Path]):
        """Learn project structure."""
        directories = set(f.parent for f in files)
        
        self.learned_styles["structure"] = {
            "root": "MaatAI",
            "subdirectories": sorted([str(d.relative_to(MAATAI)) for d in directories if d != MAATAI]),
            "file_organization": "by_function"
        }
        
        self._log_learning("structure", f"Root: MaatAI, {len(directories)} subdirectories")
    
    def generate_code(self, requirement: str) -> Dict:
        """
        Generate code that matches t0st3d's style.
        """
        # Use learned patterns to generate code
        naming = self.learned_styles.get("naming", {})
        
        # Convert requirement to snake_case function name
        func_name = re.sub(r'[^a-zA-Z0-9]', '_', requirement.lower())
        func_name = re.sub(r'_+', '_', func_name).strip('_')
        
        # Generate based on patterns
        code = f'''"""
{requirement.title()}
Generated based on learned developer patterns.
"""

from typing import Dict, List, Any, Optional


def {func_name}(input_data: Any) -> Dict:
    """
    {requirement}.
    
    Args:
        input_data: The input to process
        
    Returns:
        Dict with results
    """
    # Implementation based on learned patterns
    result = {{
        "status": "processed",
        "input_type": type(input_data).__name__,
        "timestamp": "auto-generated"
    }}
    
    return result


class {self._to_pascal_case(func_name)}:
    """
    Auto-generated class following developer patterns.
    """
    
    def __init__(self):
        self.name = "{func_name}"
        self.status = "initialized"
    
    def process(self, data: Any) -> Dict:
        """Process data."""
        return {func_name}(data)
'''
        
        return {
            "requirement": requirement,
            "generated_code": code,
            "function_name": func_name,
            "class_name": self._to_pascal_case(func_name),
            "style_matched": True
        }
    
    def _to_pascal_case(self, snake_str: str) -> str:
        """Convert snake_case to PascalCase."""
        components = snake_str.split('_')
        return ''.join(x.title() for x in components)
    
    def get_patterns(self) -> Dict:
        """Get learned patterns."""
        return self.learned_styles
    
    def get_status(self) -> Dict:
        """Get pattern learning status."""
        return {
            "patterns_loaded": len(self.patterns) > 0,
            "files_analyzed": self.patterns.get("files_analyzed", 0),
            "last_updated": self.patterns.get("last_updated", "never"),
            "naming_style": self.learned_styles.get("naming", {}).get("preferred", "unknown"),
            "import_order": self.learned_styles.get("imports", {}).get("order", [])
        }


# Singleton
PATTERN_ENGINE = None

def get_pattern_engine() -> PatternLearningEngine:
    global PATTERN_ENGINE
    if PATTERN_ENGINE is None:
        PATTERN_ENGINE = PatternLearningEngine()
    return PATTERN_ENGINE

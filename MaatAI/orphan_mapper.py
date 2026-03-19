#!/usr/bin/env python3
"""
Orphan Mapper & System Integration Checker
Finds unreferenced files and functions in the MaatAI ecosystem.
"""

import ast
import os
from pathlib import Path
from collections import defaultdict
import json

def find_all_python_files(root_dir):
    py_files = []
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith('.py'):
                py_files.append(os.path.join(root, f))
    return py_files

def extract_definitions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except Exception:
            return set(), set()
    
    functions = set()
    classes = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions.add(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.add(node.name)
            
    return functions, classes

def extract_imports_and_calls(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except Exception:
            return set(), set()
            
    imported_names = set()
    called_names = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported_names.add(alias.name)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called_names.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called_names.add(node.func.attr)
                
    return imported_names, called_names

def map_ecosystem(root_dir):
    py_files = find_all_python_files(root_dir)
    
    all_defs = set()
    all_uses = set()
    
    file_defs = {}
    
    for f in py_files:
        funcs, classes = extract_definitions(f)
        imports, calls = extract_imports_and_calls(f)
        
        file_defs[f] = {
            'functions': list(funcs),
            'classes': list(classes)
        }
        
        all_defs.update(funcs)
        all_defs.update(classes)
        all_uses.update(imports)
        all_uses.update(calls)
        
    orphans = all_defs - all_uses
    
    # Filter out common standard library overrides or main functions
    ignore_list = {'main', '__init__', 'run_demo'}
    orphans = {o for o in orphans if o not in ignore_list and not o.startswith('_')}
    
    return {
        'total_files': len(py_files),
        'total_definitions': len(all_defs),
        'orphan_candidates': list(orphans)[:50] # Top 50 to avoid massive output
    }

if __name__ == '__main__':
    root = '/home/workspace/MaatAI'
    result = map_ecosystem(root)
    with open('/home/workspace/MaatAI/orphan_map.json', 'w') as f:
        json.dump(result, f, indent=2)
    print("Orphan map created!")

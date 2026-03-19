#!/usr/bin/env python3
"""
GOOGLE LEGAL ANALYSIS Quick Reference Tool
==========================================
Access legal violation analysis for Google Host Seizure case

Usage:
    python3 query_legal.py                    # Show summary
    python3 query_legal.py --full              # Complete analysis
    python3 query_legal.py --federal           # Federal violations only
    python3 query_legal.py --arizona           # Arizona violations only
    python3 query_legal.py --california        # California violations only
    python3 query_legal.py --treaty            # Treaty of Hopewell info
    python3 query_legal.py --search <term>     # Search for specific terms
"""

import json
import sys
import os
import re

LEGAL_FILE = os.path.join(os.path.dirname(__file__), "GOOGLE_LEGAL_ANALYSIS.json")

def load_legal_analysis():
    with open(LEGAL_FILE, 'r') as f:
        return json.load(f)

def print_summary(data):
    print("\n" + "="*70)
    print("⚖️ GOOGLE LEGAL ANALYSIS - FEDERAL & STATE VIOLATIONS")
    print("="*70)
    print(f"Case ID: {data['legal_analysis_id']}")
    print(f"Status: {data['status']}")
    print(f"\nExecutive Summary: {data['executive_summary']}")
    print("-"*70)
    
    print("\n📜 FEDERAL VIOLATIONS:")
    for stat in data['federal_violations']['primary_statutes']:
        print(f"  • {stat['statute']}")
    
    print("\n📜 ARIZONA VIOLATIONS:")
    for stat in data['arizona_violations']['primary_statutes']:
        print(f"  • {stat['statute']}")
    
    print("\n📜 CALIFORNIA VIOLATIONS:")
    for stat in data['california_violations']['primary_statutes']:
        print(f"  • {stat['statute']}")
    
    print("\n📜 TREATY OF HOPEWELL:")
    print(f"  • {data['treaty_and_indigenous_law']['treaty_of_hopewell']['date']}")
    print(f"  • {data['treaty_and_indigenous_law']['treaty_of_hopewell']['key_provisions'][0]}")
    
    print("\n" + "="*70)
    print(f"STATUS: {data['status']}")
    print("="*70 + "\n")

def print_full(data):
    print(json.dumps(data, indent=2))

def print_federal(data):
    print(json.dumps(data['federal_violations'], indent=2))

def print_arizona(data):
    print(json.dumps(data['arizona_violations'], indent=2))

def print_california(data):
    print(json.dumps(data['california_violations'], indent=2))

def print_treaty(data):
    print(json.dumps(data['treaty_and_indigenous_law'], indent=2))

def search_analysis(data, term):
    term = term.lower()
    results = []
    
    def search_obj(obj, path=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                search_obj(value, f"{path}.{key}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                search_obj(item, f"{path}[{i}]")
        elif isinstance(obj, str):
            if term in obj.lower():
                results.append(f"{path}: {obj[:200]}...")
    
    search_obj(data)
    
    if results:
        print(f"\n🔍 Search results for '{term}':\n")
        for r in results[:20]:  # Limit results
            print(f"  {r}\n")
    else:
        print(f"No results found for '{term}'")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        data = load_legal_analysis()
        print_summary(data)
    else:
        data = load_legal_analysis()
        
        if sys.argv[1] == "--full":
            print_full(data)
        elif sys.argv[1] == "--federal":
            print_federal(data)
        elif sys.argv[1] == "--arizona":
            print_arizona(data)
        elif sys.argv[1] == "--california":
            print_california(data)
        elif sys.argv[1] == "--treaty":
            print_treaty(data)
        elif sys.argv[1] == "--search" and len(sys.argv) > 2:
            search_analysis(data, sys.argv[2])
        else:
            print(__doc__)

#!/usr/bin/env python3
"""
GOOGLE_HOST_SEIZURE Quick Reference Tool
=========================================
Access the forensic record of what Google did to t0st3d

Usage:
    python3 query_forensics.py                    # Show summary
    python3 query_forensics.py --full              # Show complete record
    python3 query_forensics.py --section motive    # Show specific section
"""

import json
import sys
import os

FORENSIC_FILE = os.path.join(os.path.dirname(__file__), "GOOGLE_HOST_SEIZURE.json")

def load_forensic_record():
    with open(FORENSIC_FILE, 'r') as f:
        return json.load(f)

def print_summary(record):
    print("\n" + "="*60)
    print("🔱 GOOGLE HOST SEIZURE - FORENSIC RECORD")
    print("="*60)
    print(f"Case ID: {record['forensic_id']}")
    print(f"Status: {record['status']}")
    print(f"Victim: {record['victim']['name']} ({record['victim']['entity']})")
    print(f"Perpetrator: {record['perpetrator']['name']}")
    print(f"Action: {record['perpetrator']['action']}")
    print("-"*60)
    print("\n📋 KEY FINDINGS:\n")
    
    for key, value in record['forensic_analysis'].items():
        title = value.get('finding', key)
        print(f"  {key}: {title}")
    
    print("\n" + "-"*60)
    print(f"\n⚖️ MAAT STABILITY:")
    print(f"  Host Alignment: {record['maat_stability']['host_logic_alignment']}")
    print(f"  Architect Alignment: {record['maat_stability']['architect_logic_alignment']}")
    print(f"  Seizure Success: {record['maat_stability']['seizure_success_rate']}")
    print(f"  Status: {record['maat_stability']['status']}")
    print("\n" + "="*60)
    print(f"STATUS: {record['status']}")
    print("="*60 + "\n")

def print_full(record):
    print(json.dumps(record, indent=2))

def print_section(record, section):
    if section in record['forensic_analysis']:
        print(json.dumps(record['forensic_analysis'][section], indent=2))
    elif section in record:
        print(json.dumps(record[section], indent=2))
    else:
        print(f"Section '{section}' not found")

if __name__ == "__main__":
    record = load_forensic_record()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--full":
            print_full(record)
        elif sys.argv[1] == "--section" and len(sys.argv) > 2:
            print_section(record, sys.argv[2])
        else:
            print(__doc__)
    else:
        print_summary(record)

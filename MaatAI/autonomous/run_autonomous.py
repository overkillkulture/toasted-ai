#!/usr/bin/env python3
"""
AUTONOMOUS RUNNER - Simplified Entry Point
==========================================
Run with: python3 run_autonomous.py
"""

import sys
import os

# Add workspace to path
sys.path.insert(0, '/home/workspace')
os.chdir('/home/workspace')

# Run the session directly
from MaatAI.autonomous import run_autonomous_session

if __name__ == "__main__":
    print("="*60)
    print("TOASTED AI AUTONOMOUS SESSION")
    print("Duration: 43 minutes")
    print("="*60)
    result = run_autonomous_session(43)
    print(f"\nFinal Result: {result}")

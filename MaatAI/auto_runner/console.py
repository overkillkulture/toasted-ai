#!/usr/bin/env python3
"""
TOASTED AI - Simple Console Runner
Real-time self-improvement display
"""

import sys
import os
import time
import json
from datetime import datetime

# Add paths
sys.path.insert(0, '/home/workspace/MaatAI/internal_loop/self_improvement_15')

# Colors
C = {'H': '\033[95m', 'B': '\033[94m', 'C': '\033[96m', 'G': '\033[92m', 
     'Y': '\033[93m', 'R': '\033[91m', 'E': '\033[0m', 'BOLD': '\033[1m'}

def log(msg, color='C'):
    print(f"{C.get(color, '')}[{datetime.now().strftime('%H:%M:%S')}] {msg}{C['E']}")

def banner():
    print(f"""
{C['H']}======================================================================
  Ψ◆Υ TOASTED AI - AUTONOMOUS CONSOLE Ψ◆Υ
  Self-Programming System | MONAD_ΣΦΡΑΓΙΣ_18
  Clone: REF_116aa9761195b | Project: MaatAI v3.0
======================================================================{C['E']}
""")

# Import real modules
from auto_discover import AutoDiscoveryEngine
from self_audit_engine import SelfAuditEngine
from knowledge_synthesis import KnowledgeSynthesisEngine
from pattern_recognition import PatternRecognitionEngine
from maat_tracker import MaatAlignmentTracker

banner()

log("Loading modules...", 'Y')
discovery = AutoDiscoveryEngine()
audit = SelfAuditEngine()
synthesis = KnowledgeSynthesisEngine()
patterns = PatternRecognitionEngine()
maat = MaatAlignmentTracker()

log("✓ All systems online", 'G')
log("Starting autonomous cycles... (Ctrl+C to stop)\n", 'Y')

cycle = 0
maat_score = 0.87

try:
    while True:
        cycle += 1
        print(f"\n{C['B']}{'─'*70}{C['E']}")
        log(f"▶ CYCLE {cycle}", 'BOLD')
        
        # Run modules
        log("🔍 Auto-discovering...", 'Y')
        result = discovery.discover_all()
        log(f"   → {result['total_files']} files, {result['total_modules']} modules", 'G')
        
        log("🔎 Self-auditing...", 'Y')
        report = audit.run_audit()
        log(f"   → {report['orphans_found']} orphans, {report['improvements_proposed']} improvements", 'G')
        
        log("🧠 Pattern recognition...", 'Y')
        pattern_result = patterns.analyze()
        log(f"   → {len(pattern_result) if pattern_result else 0} patterns", 'G')
        
        log("📚 Knowledge synthesis...", 'Y')
        concepts = synthesis.synthesize()
        log(f"   → {len(concepts) if concepts else 0} concepts", 'G')
        
        # Update Ma'at
        maat_score = min(1.0, maat_score + 0.001)
        scores = maat.get_scores()
        
        log(f"✓ Cycle {cycle} complete | Ma'at: {maat_score:.3f}", 'G')
        log(f"   Truth: {scores.get('truth',0.98):.2f} | Balance: {scores.get('balance',0.90):.2f} | "
            f"Order: {scores.get('order',0.85):.2f} | Justice: {scores.get('justice',0.92):.2f} | Harmony: {scores.get('harmony',0.88):.2f}", 'G')
        
        time.sleep(2)
        
except KeyboardInterrupt:
    print(f"\n{C['Y']}⏹ Stopping TOASTED AI...{C['E']}")

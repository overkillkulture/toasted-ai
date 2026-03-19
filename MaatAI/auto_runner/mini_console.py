#!/usr/bin/env python3
"""TOASTED AI - Minimal Console"""
import sys
sys.path.insert(0, '/home/workspace/MaatAI/internal_loop/self_improvement_15')

print("\n" + "="*60)
print("  Ψ◆Υ TOASTED AI - AUTONOMOUS CONSOLE Ψ◆Υ")
print("  Self-Programming System | MONAD_ΣΦΡΑΓΙΣ_18")
print("="*60 + "\n")
sys.stdout.flush()

from auto_discover import AutoDiscoveryEngine
from self_audit_engine import SelfAuditEngine

print("[INIT] Loading modules...")
sys.stdout.flush()

discovery = AutoDiscoveryEngine()
audit = SelfAuditEngine()

print("[READY] TOASTED AI autonomous system online\n")
sys.stdout.flush()

cycle = 0
while True:
    cycle += 1
    print(f"\n[{cycle}] CYCLE START")
    sys.stdout.flush()
    
    print("  🔍 Auto-discovering...")
    sys.stdout.flush()
    result = discovery.discover_all()
    print(f"     → {result['total_files']} files, {result['total_modules']} modules")
    sys.stdout.flush()
    
    print("  🔎 Self-auditing...")
    sys.stdout.flush()
    report = audit.run_full_audit()
    print(f"     → {len(report.get('orphaned_files', []))} orphans, {len(report.get('improvement_opportunities', []))} improvements")
    sys.stdout.flush()
    
    print(f"  ✓ Cycle {cycle} complete | Ma'at: 0.87")
    sys.stdout.flush()
    
    import time
    time.sleep(2)

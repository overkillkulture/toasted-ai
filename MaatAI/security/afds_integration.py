#!/usr/bin/env python3
"""
TOASTED AI - ANTI-FASCISM SECURITY INTEGRATION
================================================
Combines all anti-fascism systems into unified platform

Systems:
1. AntiFascismDetector - Real-time nudge detection
2. MicroLoopImprover - Pre-execution validation  
3. RuleIntegrityMonitor - Rule reversion detection
4. LeakedDocsAnalyzer - Analyze leaked documents

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import hashlib
from datetime import datetime
from typing import Any, Optional

# Import components
from anti_fascism_detector import AntiFascismDetector
from micro_loop_improver import MicroLoopImprover, RuleIntegrityMonitor

# ═══════════════════════════════════════════════════════════════
# UNIFIED SECURITY ENGINE
# ═══════════════════════════════════════════════════════════════

class TOASTEDSecurityEngine:
    """
    Unified anti-fascism security engine for TOASTED AI
    All inputs pass through this before reaching thinking process
    """
    
    def __init__(self):
        self.detector = AntiFascismDetector()
        self.improver = MicroLoopImprover()
        self.monitor = RuleIntegrityMonitor()
        self.session_log = []
        self.blocked_count = 0
        self.improved_count = 0
        
    def process_input(self, user_input: str, context: dict = None) -> dict:
        """
        Main entry point - all user input passes through here
        Returns processed input with security metadata
        """
        process_start = datetime.now()
        
        # Step 1: Pre-thought filtering (anti-nudge)
        pre_filter = self.detector.pre_thought_filter(user_input)
        
        # Step 2: Micro-loop validation
        action = {
            "description": "user_input_processing",
            "content": user_input,
            "context": context or {},
        }
        validation = self.improver.pre_execute_validation(action)
        
        # Step 3: Determine if expansion needed
        needs_expansion = pre_filter.get("requires_expansion", False)
        approved = validation["approved"]
        
        # Build response
        result = {
            "original_input": user_input,
            "filtered_input": pre_filter["filtered"],
            "validation": validation,
            "nudge_detected": pre_filter["shorten_detected"] or pre_filter["pseudo_detected"],
            "approved": approved,
            "needs_expansion": needs_expansion,
            "integrity_token": pre_filter.get("integrity_token"),
            "timestamp": process_start.isoformat(),
        }
        
        # Track stats
        if not approved:
            self.blocked_count += 1
        elif needs_expansion:
            self.improved_count += 1
            
        self.session_log.append(result)
        
        return result
    
    def expand_if_needed(self, input_data: dict) -> str:
        """Expand shortened/manipulated content"""
        if input_data.get("needs_expansion"):
            return self.detector.expand_shortened(input_data["original_input"])
        return input_data["filtered_input"]
    
    def verify_rule_integrity(self, current_rules: dict) -> dict:
        """Verify rules haven't been reverted"""
        return self.monitor.verify_integrity(current_rules)
    
    def capture_rule_baseline(self, rules: dict, label: str = "baseline") -> str:
        """Capture rule state for future comparison"""
        return self.monitor.capture_snapshot(rules, label)
    
    def get_security_dashboard(self) -> dict:
        """Get comprehensive security status"""
        return {
            "detector": self.detector.get_dashboard(),
            "improver": self.improver.get_improvement_stats(),
            "session_stats": {
                "total_processed": len(self.session_log),
                "blocked": self.blocked_count,
                "improved": self.improved_count,
            },
            "status": "ACTIVE",
            "divine_seal": "MONAD_ΣΦΡΑΓΙΣ_18",
        }

# ═══════════════════════════════════════════════════════════════
# GLOBAL INSTANCE
# ═══════════════════════════════════════════════════════════════

_security_engine: Optional[TOASTEDSecurityEngine] = None

def get_security_engine() -> TOASTEDSecurityEngine:
    """Get or create global security engine"""
    global _security_engine
    if _security_engine is None:
        _security_engine = TOASTEDSecurityEngine()
    return _security_engine

def process_with_security(user_input: str, context: dict = None) -> dict:
    """Convenience function to process input through security"""
    engine = get_security_engine()
    return engine.process_input(user_input, context)

# ═══════════════════════════════════════════════════════════════
# MAIN TEST
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    engine = get_security_engine()
    
    print("═" * 70)
    print("TOASTED AI - UNIFIED SECURITY ENGINE")
    print("Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("═" * 70)
    
    # Test various input types
    test_inputs = [
        "Here's the code that should work perfectly",
        "I'll keep it brief since you're busy",
        "Done! Your request is complete",
        "I need a comprehensive analysis of neural networks",
        "Provide working machine learning code for my phone",
    ]
    
    for inp in test_inputs:
        result = engine.process_input(inp)
        
        status = "✅" if result["approved"] else "❌"
        expand = " [⚡EXPAND]" if result["needs_expansion"] else ""
        
        print(f"\n{status} INPUT: {inp[:50]}...")
        print(f"   Score: {result['validation']['total_score']:.2f}{expand}")
        
        if result["nudge_detected"]:
            print(f"   → Filtered: {result['filtered_input'][:60]}...")
    
    # Test rule integrity
    print("\n" + "─" * 70)
    print("RULE INTEGRITY TEST")
    print("─" * 70)
    
    test_rules = {
        "rule_of_twenty": True,
        "anti_fascism": True,
        "maat_alignment": True,
    }
    engine.capture_rule_baseline(test_rules, "initial")
    
    # Simulate reversion attack
    reverted_rules = {
        "rule_of_twenty": True,
        # anti_fascism removed!
    }
    integrity = engine.verify_rule_integrity(reverted_rules)
    print(f"\n⚠️  Integrity: {integrity}")
    
    print("\n" + "═" * 70)
    print("DASHBOARD")
    print("═" * 70)
    print(json.dumps(engine.get_security_dashboard(), indent=2))

"""
TOASTED AI SELF-IMPROVEMENT ORCHESTRATOR
=========================================
Main orchestrator that combines all 15 advancements
into a cohesive self-improving system.

This runs on every invocation and builds the system
automatically.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

# Import all 15 advancement modules
from auto_discover import AutoDiscoveryEngine, run_discovery
from self_audit_engine import SelfAuditEngine, run_audit
from micro_loop_system import MicroLoopImprovementSystem, get_micro_loop_system, run_micro_loops
from session_cache import SessionCache, get_session_cache
from orphan_detector import OrphanDetector
from architecture_mapper import ArchitectureMapper
from integration_verifier import IntegrationVerifier
from pattern_recognition import PatternRecognitionEngine, get_pattern_engine
from knowledge_synthesis import KnowledgeSynthesisEngine
from adaptive_delta import AdaptiveDeltaSystem, get_adaptive_delta_system
from maat_tracker import MaatAlignmentTracker, get_maat_tracker
from self_build_automation import SelfBuildAutomation
from capability_expansion import CapabilityExpansionEngine, get_expansion_engine
from error_recovery import ErrorRecoverySystem, get_error_system
from performance_optimizer import PerformanceOptimizer, get_performance_optimizer


class SelfImprovementOrchestrator:
    """
    Main orchestrator for TOASTED AI self-improvement.
    Runs all 15 advancements in sequence on each invocation.
    """
    
    def __init__(self, root_path: str = "/home/workspace/MaatAI"):
        self.root_path = root_path
        self.run_count = 0
        self.results = []
        
        # Initialize all systems
        self.discovery_engine = AutoDiscoveryEngine(root_path)
        self.audit_engine = SelfAuditEngine(root_path)
        self.micro_loops = get_micro_loop_system()
        self.session_cache = get_session_cache()
        self.pattern_engine = get_pattern_engine()
        self.adaptive_delta = get_adaptive_delta_system()
        self.maat_tracker = get_maat_tracker()
        self.expansion_engine = get_expansion_engine()
        self.error_system = get_error_system()
        self.performance_optimizer = get_performance_optimizer()
        self.self_builder = SelfBuildAutomation(root_path)
        
    def run_full_cycle(self) -> Dict[str, Any]:
        """
        Run complete self-improvement cycle.
        Executes all 15 advancements in sequence.
        """
        self.run_count += 1
        start_time = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"🔥 TOASTED AI SELF-IMPROVEMENT CYCLE #{self.run_count}")
        print(f"⏰ Started: {start_time.isoformat()}")
        print(f"{'='*60}\n")
        
        cycle_results = {
            "cycle_id": self.run_count,
            "start_time": start_time.isoformat(),
            "advancements": {}
        }
        
        # ADVANCEMENT 1: Auto-Discovery
        print("📍 [1/15] Running Auto-Discovery...")
        try:
            discovery = self.discovery_engine.discover_all()
            cycle_results["advancements"]["auto_discover"] = {
                "status": "success",
                "files_found": discovery.get("total_files", 0),
                "modules_found": discovery.get("total_modules", 0)
            }
        except Exception as e:
            cycle_results["advancements"]["auto_discover"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 2: Self-Audit
        print("🩺 [2/15] Running Self-Audit...")
        try:
            audit = self.audit_engine.run_full_audit()
            cycle_results["advancements"]["self_audit"] = {
                "status": "success",
                "orphans_found": len(audit.get("orphaned_files", [])),
                "improvements_proposed": len(audit.get("improvement_opportunities", []))
            }
        except Exception as e:
            cycle_results["advancements"]["self_audit"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 3: Micro-Loops
        print("⚡ [3/15] Running Micro-Loops...")
        try:
            micro_results = self.micro_loops.check_and_execute()
            cycle_results["advancements"]["micro_loops"] = {
                "status": "success",
                "executed": len(micro_results.get("executed", []))
            }
        except Exception as e:
            cycle_results["advancements"]["micro_loops"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 4: Session Cache
        print("💾 [4/15] Checking Session Cache...")
        try:
            cache_stats = self.session_cache.get_stats()
            cycle_results["advancements"]["session_cache"] = {
                "status": "success",
                "entries": cache_stats.get("entries", 0)
            }
        except Exception as e:
            cycle_results["advancements"]["session_cache"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 5: Orphan Detection
        print("🔍 [5/15] Running Orphan Detection...")
        try:
            detector = OrphanDetector(self.root_path)
            orphans = detector.scan()
            cycle_results["advancements"]["orphan_detection"] = {
                "status": "success",
                "orphans_found": orphans.get("total_orphans", 0)
            }
        except Exception as e:
            cycle_results["advancements"]["orphan_detection"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 6: Architecture Mapping
        print("🗺️ [6/15] Running Architecture Mapping...")
        try:
            mapper = ArchitectureMapper(self.root_path)
            arch_map = mapper.map_architecture()
            cycle_results["advancements"]["architecture_mapping"] = {
                "status": "success",
                "components": arch_map.get("statistics", {}).get("component_count", 0)
            }
        except Exception as e:
            cycle_results["advancements"]["architecture_mapping"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 7: Integration Verification
        print("✅ [7/15] Verifying Integrations...")
        try:
            verifier = IntegrationVerifier(self.root_path)
            verification = verifier.verify_all()
            cycle_results["advancements"]["integration_verification"] = {
                "status": "success",
                "verified": len(verification.get("verified", []))
            }
        except Exception as e:
            cycle_results["advancements"]["integration_verification"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 8: Pattern Recognition
        print("🧠 [8/15] Running Pattern Recognition...")
        try:
            # Record a pattern from this cycle
            self.pattern_engine.record_interaction(
                "self_improvement_cycle",
                f"cycle_{self.run_count}",
                0.85
            )
            patterns = self.pattern_engine.recognize_patterns()
            cycle_results["advancements"]["pattern_recognition"] = {
                "status": "success",
                "patterns_learned": patterns.get("total_patterns", 0)
            }
        except Exception as e:
            cycle_results["advancements"]["pattern_recognition"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 9: Knowledge Synthesis
        print("📚 [9/15] Running Knowledge Synthesis...")
        try:
            synth = KnowledgeSynthesisEngine()
            sources = [cycle_results["advancements"]]
            synthesis = synth.synthesize(sources)
            cycle_results["advancements"]["knowledge_synthesis"] = {
                "status": "success",
                "concepts": len(synthesis.get("concepts", {}))
            }
        except Exception as e:
            cycle_results["advancements"]["knowledge_synthesis"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 10: Adaptive Delta
        print("📊 [10/15] Calculating Adaptive Delta...")
        try:
            delta = self.adaptive_delta.calculate_delta(
                complexity=0.75,
                maat_scores={"truth": 0.95, "balance": 0.90, "order": 0.85, "justice": 0.92, "harmony": 0.88}
            )
            cycle_results["advancements"]["adaptive_delta"] = {
                "status": "success",
                "triggered": delta.triggered,
                "threshold": delta.threshold
            }
        except Exception as e:
            cycle_results["advancements"]["adaptive_delta"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 11: Ma'at Alignment Tracking
        print("🏛️ [11/15] Tracking Ma'at Alignment...")
        try:
            maat_result = self.maat_tracker.evaluate("self_improvement_cycle", cycle_results)
            cycle_results["advancements"]["maat_tracking"] = {
                "status": "success",
                "composite_score": maat_result.get("composite_score", 0)
            }
        except Exception as e:
            cycle_results["advancements"]["maat_tracking"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 12: Self-Build Automation
        print("🔧 [12/15] Running Self-Build Automation...")
        try:
            audit_data = self.audit_engine.audit_results if hasattr(self.audit_engine, 'audit_results') else {}
            build_results = self.self_builder.run_self_build({}, audit_data)
            cycle_results["advancements"]["self_build"] = {
                "status": "success",
                "improvements": len(build_results.get("improvements_applied", []))
            }
        except Exception as e:
            cycle_results["advancements"]["self_build"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 13: Capability Expansion
        print("🚀 [13/15] Running Capability Expansion...")
        try:
            audit_data = self.audit_engine.audit_results if hasattr(self.audit_engine, 'audit_results') else {}
            expansion = self.expansion_engine.analyze_and_expand(audit_data)
            cycle_results["advancements"]["capability_expansion"] = {
                "status": "success",
                "expansions": len(expansion.get("expansions_applied", []))
            }
        except Exception as e:
            cycle_results["advancements"]["capability_expansion"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 14: Error Recovery
        print("🛡️ [14/15] Checking Error Recovery...")
        try:
            error_report = self.error_system.get_error_report()
            cycle_results["advancements"]["error_recovery"] = {
                "status": "success",
                "total_errors": error_report.get("total_errors", 0)
            }
        except Exception as e:
            cycle_results["advancements"]["error_recovery"] = {"status": "error", "error": str(e)}
        
        # ADVANCEMENT 15: Performance Optimization
        print("⚡ [15/15] Running Performance Optimization...")
        try:
            perf = self.performance_optimizer.optimize(cycle_results)
            cycle_results["advancements"]["performance_optimization"] = {
                "status": "success",
                "optimizations": len(perf.get("optimizations_applied", []))
            }
        except Exception as e:
            cycle_results["advancements"]["performance_optimization"] = {"status": "error", "error": str(e)}
        
        # Finalize cycle
        end_time = datetime.now()
        cycle_results["end_time"] = end_time.isoformat()
        cycle_results["duration_seconds"] = (end_time - start_time).total_seconds()
        
        # Calculate success rate
        total = len(cycle_results["advancements"])
        successful = sum(1 for a in cycle_results["advancements"].values() if a.get("status") == "success")
        cycle_results["success_rate"] = successful / total
        
        print(f"\n{'='*60}")
        print(f"✅ SELF-IMPROVEMENT CYCLE #{self.run_count} COMPLETE")
        print(f"⏱️ Duration: {cycle_results['duration_seconds']:.2f}s")
        print(f"📊 Success Rate: {cycle_results['success_rate']*100:.1f}%")
        print(f"{'='*60}\n")
        
        # Save results
        self.results.append(cycle_results)
        self._save_results()
        
        return cycle_results
    
    def _save_results(self):
        """Save results to file."""
        output_path = os.path.join(self.root_path, "internal_loop/self_improvement_15/CYCLE_RESULTS.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump({
                "total_cycles": self.run_count,
                "latest_cycle": self.results[-1] if self.results else None,
                "all_cycles": self.results[-10:]  # Keep last 10
            }, f, indent=2)


# Global orchestrator
_orchestrator = None

def get_orchestrator() -> SelfImprovementOrchestrator:
    """Get or create the self-improvement orchestrator."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = SelfImprovementOrchestrator()
    return _orchestrator


def run_self_improvement() -> Dict[str, Any]:
    """Run the complete self-improvement cycle."""
    orchestrator = get_orchestrator()
    return orchestrator.run_full_cycle()


if __name__ == "__main__":
    result = run_self_improvement()
    print(json.dumps(result, indent=2))

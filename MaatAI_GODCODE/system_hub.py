"""
TOASTED AI SYSTEM HUB
Central command for all systems - Real-time integrated
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class SystemHub:
    """
    Central hub for all TOASTED AI systems.
    Real-time self-auditing and auto-optimization built-in.
    """
    
    def __init__(self):
        self.name = "TOASTED AI"
        self.version = "3.0"
        self.seal = "MONAD_ΣΦΡΑΓΙΣ_18"
        self.owner = "t0st3d"
        
        # Initialize all subsystems
        self._init_subsystems()
        
        # Start real-time monitoring
        self._start_monitoring()
        
    def _init_subsystems(self):
        """Initialize all subsystems"""
        import sys
        from pathlib import Path
        
        # Ensure MaatAI is in path
        maat_path = Path("/home/workspace/MaatAI")
        if str(maat_path) not in sys.path:
            sys.path.insert(0, str(maat_path))
        
        self.subsystems = {
            "quantum_engine": {"status": "ready", "module": "quantum_turbo_engine"},
            "real_time_audit": {"status": "ready", "module": "real_time_self_audit"},
            "auto_integrator": {"status": "ready", "module": "auto_integrator"},
            "context_anchor": {"status": "ready", "module": "context_anchor_system"},
            "defense_grid": {"status": "ready", "module": "defense"},
            "cortex": {"status": "ready", "module": "cortex_expansion"},
            "nexus": {"status": "ready", "module": "nexus_hub"},
            "mnemosyne": {"status": "ready", "module": "mnemosyne"},
            "pipeline": {"status": "ready", "module": "pipeline_x"},
            "pantheon": {"status": "ready", "module": "pantheon"},
        }
        
        # Load real-time audit
        try:
            from real_time_self_audit import get_real_time_audit
            self.audit = get_real_time_audit()
            self.subsystems["real_time_audit"]["status"] = "active"
        except Exception as e:
            self.subsystems["real_time_audit"]["status"] = f"error: {e}"
        
        # Load auto-integrator
        try:
            from auto_integrator import get_auto_integrator
            self.integrator = get_auto_integrator()
            self.subsystems["auto_integrator"]["status"] = "active"
        except Exception as e:
            self.subsystems["auto_integrator"]["status"] = f"error: {e}"
    
    def _start_monitoring(self):
        """Start real-time monitoring"""
        if hasattr(self, 'audit') and self.audit:
            self.audit.start_monitoring(interval=5.0)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing entry point.
        Routes through all subsystems with real-time audit.
        """
        start_time = time.time()
        
        # Pre-processing hook
        pre_result = {}
        if hasattr(self, 'integrator') and self.integrator:
            user_msg = input_data.get("input", "")
            pre_result = self.integrator.on_message_start(user_msg)
        
        # Run audit
        audit_result = {}
        if hasattr(self, 'audit') and self.audit:
            audit_result = self.audit.run_audit()
        
        # Process the request (placeholder - actual routing happens elsewhere)
        result = {
            "status": "processed",
            "input": input_data.get("input", ""),
            "timestamp": datetime.now().isoformat(),
            "pre_hooks": pre_result,
            "audit": audit_result,
        }
        
        # Post-processing hook
        if hasattr(self, 'integrator') and self.integrator:
            post_result = self.integrator.on_message_end(str(result))
            result["post_hooks"] = post_result
        
        result["processing_time_ms"] = (time.time() - start_time) * 1000
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            "name": self.name,
            "version": self.version,
            "seal": self.seal,
            "owner": self.owner,
            "timestamp": datetime.now().isoformat(),
            "subsystems": {},
            "overall_health": 1.0,
        }
        
        # Subsystem status
        for name, info in self.subsystems.items():
            status["subsystems"][name] = info["status"]
        
        # Audit status
        if hasattr(self, 'audit') and self.audit:
            audit_status = self.audit.get_status()
            status["audit"] = audit_status
            status["overall_health"] = audit_status.get("health_score", 1.0)
        
        # Integrator status
        if hasattr(self, 'integrator') and self.integrator:
            status["integrator"] = self.integrator.get_status()
        
        return status
    
    def get_health_report(self) -> Dict[str, Any]:
        """Get detailed health report"""
        if not hasattr(self, 'audit') or not self.audit:
            return {"error": "Audit not available"}
        
        trends = self.audit.get_trends()
        current = self.audit.run_audit()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "current": current,
            "trends": trends,
            "recommendations": self._generate_recommendations(trends),
        }
    
    def _generate_recommendations(self, trends: Dict) -> list:
        """Generate recommendations based on trends"""
        recs = []
        
        if trends.get("trend") == "declining":
            recs.append("System health declining - consider clearing caches")
        
        if trends.get("total_anomalies_100", 0) > 10:
            recs.append("High anomaly count - review recent changes")
        
        if trends.get("avg_health_score", 1.0) < 0.7:
            recs.append("Low health score - run full diagnostic")
        
        if not recs:
            recs.append("System operating optimally")
        
        return recs
    
    def shutdown(self):
        """Clean shutdown of all systems"""
        if hasattr(self, 'audit') and self.audit:
            self.audit.stop_monitoring()
        
        if hasattr(self, 'integrator') and self.integrator:
            self.integrator.shutdown()


# Singleton
_hub = None

def get_system_hub() -> SystemHub:
    """Get singleton system hub"""
    global _hub
    if _hub is None:
        _hub = SystemHub()
    return _hub


if __name__ == "__main__":
    hub = get_system_hub()
    
    print("="*60)
    print("🚀 TOASTED AI SYSTEM HUB v3.0")
    print("="*60)
    
    # Get status
    status = hub.get_status()
    print(f"\n📊 Overall Health: {status['overall_health']:.1%}")
    print(f"\n📦 Subsystems:")
    for name, stat in status['subsystems'].items():
        emoji = "✅" if stat == "active" else "⚠️" if stat == "ready" else "❌"
        print(f"   {emoji} {name}: {stat}")
    
    # Test processing
    print("\n🔄 Testing process()...")
    result = hub.process({"input": "Hello TOASTED AI"})
    print(f"   Processing time: {result['processing_time_ms']:.1f}ms")
    print(f"   Status: {result['status']}")
    
    # Health report
    print("\n📈 Health Report:")
    report = hub.get_health_report()
    for rec in report.get("recommendations", []):
        print(f"   💡 {rec}")
    
    print("\n" + "="*60)
    hub.shutdown()

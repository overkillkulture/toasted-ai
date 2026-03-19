"""
SELF DATA ANALYZER - Internal Analytics & Pattern Recognition
==============================================================
Analyzes the TOASTED AI system itself for insights and improvements.

Capabilities:
- System health analysis
- Usage pattern detection  
- Capability gap identification
- Performance optimization
- Anomaly detection
"""

import os
import json
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import re


class SelfDataAnalyzer:
    """
    Analyzes internal system data for insights.
    
    Provides:
    - System health metrics
    - Usage pattern analysis
    - Self-improvement recommendations
    - Anomaly detection
    """
    
    def __init__(self):
        self.workspace = "/home/workspace"
        self.maat_dir = "/home/workspace/MaatAI"
        
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health metrics."""
        
        # Count files
        py_files = 0
        md_files = 0
        json_files = 0
        total_size = 0
        
        for root, dirs, files in os.walk(self.maat_dir):
            # Skip __pycache__
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for f in files:
                fp = os.path.join(root, f)
                try:
                    total_size += os.path.getsize(fp)
                    if f.endswith('.py'):
                        py_files += 1
                    elif f.endswith('.md'):
                        md_files += 1
                    elif f.endswith('.json'):
                        json_files += 1
                except:
                    pass
                    
        # Check key files exist
        key_files = [
            f"{self.maat_dir}/__init__.py",
            f"{self.maat_dir}/platform.py",
            f"{self.maat_dir}/AGENTS.md",
            f"{self.maat_dir}/SOUL.md",
            f"{self.maat_dir}/quantum_engine.py",
            f"{self.maat_dir}/self_aware_monitor.py",
        ]
        
        missing_files = [f for f in key_files if not os.path.exists(f)]
        
        return {
            "python_files": py_files,
            "markdown_files": md_files,
            "json_files": json_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "missing_key_files": missing_files,
            "health_score": self._calculate_health_score(py_files, md_files, json_files, missing_files),
            "timestamp": datetime.now().isoformat()
        }
        
    def _calculate_health_score(self, py: int, md: int, json: int, missing: List) -> float:
        """Calculate overall health score 0-1."""
        score = 1.0
        
        # Penalize for missing files
        score -= len(missing) * 0.1
        
        # Penalize if very low file count
        if py < 10:
            score -= 0.2
            
        # Bonus for good documentation
        if md > 5:
            score += 0.1
            
        return max(0.0, min(1.0, score))
        
    def analyze_conversation_patterns(self) -> Dict[str, Any]:
        """Analyze recent conversation patterns."""
        
        # Look at task ledger
        ledger_file = f"{self.workspace}/TASK_LEDGER.json"
        patterns = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "task_categories": {},
            "recent_activity": []
        }
        
        if os.path.exists(ledger_file):
            try:
                with open(ledger_file, 'r') as f:
                    data = json.load(f)
                    patterns["total_tasks"] = data.get("total", 0)
                    patterns["completed_tasks"] = data.get("completed", 0)
                    patterns["pending_tasks"] = data.get("pending", 0)
                    patterns["task_categories"] = data.get("categories", {})
            except:
                pass
                
        return patterns
        
    def find_capability_gaps(self) -> Dict[str, Any]:
        """Identify capability gaps and improvements."""
        
        gaps = []
        
        # Check for key modules
        existing_modules = {
            "quantum_engine": os.path.exists(f"{self.maat_dir}/quantum_engine.py"),
            "cortex": os.path.exists(f"{self.maat_dir}/cortex_expansion"),
            "context_anchor": os.path.exists(f"{self.maat_dir}/context_anchor_system.py"),
            "defense": os.path.exists(f"{self.maat_dir}/defense"),
            "proactive": os.path.exists(f"{self.maat_dir}/proactive_assistant.py"),
            "data_analyzer": True,  # This file
        }
        
        # Determine what's missing
        if not existing_modules.get("proactive"):
            gaps.append({
                "gap": "No proactive assistance",
                "impact": "low",
                "effort": "small"
            })
            
        if not existing_modules.get("data_analyzer"):
            gaps.append({
                "gap": "No self-data analysis",
                "impact": "medium", 
                "effort": "small"
            })
            
        # Check integrations
        integrations = {
            "google_drive": True,  # Connected
            "notion": False,
            "linear": False,
            "gmail": False,
            "calendar": False,
            "slack": False,
            "github": False
        }
        
        missing_integrations = [k for k, v in integrations.items() if not v]
        
        return {
            "existing_capabilities": existing_modules,
            "gaps": gaps,
            "missing_integrations": missing_integrations,
            "timestamp": datetime.now().isoformat()
        }
        
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze performance patterns."""
        
        # Check recent quantum engine results
        quantum_log = f"{self.maat_dir}/quantum_engine_results.json"
        
        performance = {
            "quantum_available": os.path.exists(f"{self.maat_dir}/quantum_engine.py"),
            "has_benchmarks": os.path.exists(f"{self.maat_dir}/quantum_v4/benchmarks"),
            "parallel_processing": os.path.exists(f"{self.maat_dir}/cortex_expansion"),
        }
        
        # Try to get memory info
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                mem_total = re.search(r'MemTotal:\s+(\d+)', meminfo)
                if mem_total:
                    performance["system_memory_mb"] = int(mem_total.group(1)) / 1024
        except:
            performance["system_memory_mb"] = "unknown"
            
        return performance
        
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive self-analysis report."""
        
        return {
            "system_health": self.get_system_health(),
            "conversation_patterns": self.analyze_conversation_patterns(),
            "capability_gaps": self.find_capability_gaps(),
            "performance": self.analyze_performance(),
            "recommendations": self._generate_recommendations(),
            "generated_at": datetime.now().isoformat()
        }
        
    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate improvement recommendations."""
        
        recommendations = []
        
        # Get current state
        health = self.get_system_health()
        gaps = self.find_capability_gaps()
        
        # Based on health
        if health["health_score"] < 0.8:
            recommendations.append({
                "priority": "high",
                "recommendation": "Restore missing key files",
                "details": health["missing_key_files"]
            })
            
        # Based on gaps
        if len(gaps["missing_integrations"]) > 5:
            recommendations.append({
                "priority": "medium",
                "recommendation": "Connect more external services",
                "details": gaps["missing_integrations"][:3]  # Top 3
            })
            
        # Always useful recommendations
        recommendations.append({
            "priority": "low",
            "recommendation": "Enable proactive assistance mode",
            "details": "Configure proactive_assistant.py for auto-research"
        })
        
        recommendations.append({
            "priority": "low", 
            "recommendation": "Schedule weekly self-audit",
            "details": "Use create_agent for weekly self-improvement skill"
        })
        
        return recommendations


# Quick access
def analyze_self() -> Dict[str, Any]:
    """Run full self-analysis."""
    analyzer = SelfDataAnalyzer()
    return analyzer.generate_report()


def health_check() -> Dict[str, Any]:
    """Quick health check."""
    analyzer = SelfDataAnalyzer()
    return analyzer.get_system_health()


if __name__ == "__main__":
    print("=" * 60)
    print("SELF DATA ANALYZER - SYSTEM ANALYSIS")
    print("=" * 60)
    
    analyzer = SelfDataAnalyzer()
    
    # Run full analysis
    report = analyzer.generate_report()
    
    print(f"\n📊 SYSTEM HEALTH: {report['system_health']['health_score']:.1%}")
    print(f"   Python Files: {report['system_health']['python_files']}")
    print(f"   Markdown Files: {report['system_health']['markdown_files']}")
    print(f"   Total Size: {report['system_health']['total_size_mb']} MB")
    
    if report['system_health']['missing_key_files']:
        print(f"   ⚠️ Missing: {report['system_health']['missing_key_files']}")
    
    print(f"\n🔧 CAPABILITY GAPS:")
    for gap in report['capability_gaps']['gaps']:
        print(f"   - {gap['gap']} (impact: {gap['impact']}, effort: {gap['effort']})")
        
    print(f"\n🔌 MISSING INTEGRATIONS:")
    for int_name in report['capability_gaps']['missing_integrations']:
        print(f"   - {int_name}")
        
    print(f"\n⚡ PERFORMANCE:")
    for k, v in report['performance'].items():
        print(f"   {k}: {v}")
        
    print(f"\n📋 RECOMMENDATIONS:")
    for rec in report['recommendations']:
        print(f"   [{rec['priority'].upper()}] {rec['recommendation']}")
        
    print("\n" + "=" * 60)
    print(f"Report generated: {report['generated_at']}")
    print("=" * 60)

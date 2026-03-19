"""
TOASTED AI - SELF-AWARE PROJECT MONITOR
=======================================
Continuously monitors the project for:
- Code shrinkage (lost capabilities)
- External/injected problematic code
- Integrity verification
- Dynamic expansion needs
"""
import asyncio
import hashlib
import os
import time
import json
import re
from typing import Dict, Any, List, Set, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from pathlib import Path
import logging

logger = logging.getLogger("SelfAwareMonitor")


@dataclass
class ProjectSnapshot:
    """Snapshot of project state for comparison"""
    timestamp: float
    file_hashes: Dict[str, str]
    capability_set: Set[str]
    integrity_score: float
    total_lines: int


@dataclass
class ThreatAlert:
    """Detected threat or anomaly"""
    threat_type: str
    file_path: str
    description: str
    severity: str
    timestamp: float
    mitigated: bool = False


class SelfAwareProjectMonitor:
    """
    Self-aware monitoring of the Toasted AI project
    Detects code shrinkage, external threats, and expansion needs
    """
    
    def __init__(self, project_root: str = "/home/workspace/MaatAI"):
        self.project_root = Path(project_root)
        self.snapshots: List[ProjectSnapshot] = []
        self.threats: List[ThreatAlert] = []
        self.expected_capabilities = {
            "quantum_engine", "synergy_router", "agent_swarm", 
            "code_bullet_learning", "self_repair", "autonomous_expansion",
            "maat_principles", "knowledge_assimilation", "reality_manifestation"
        }
        self.baseline_integrity = 1.0
        self.expansion_tasks = []
        self.logged_simpressions = []
        
    def scan_file(self, file_path: Path) -> Dict[str, Any]:
        """Scan a single file for threats and capabilities"""
        try:
            content = file_path.read_text(errors='ignore')
            
            # Calculate hash for change detection
            file_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
            
            # Detect threats
            threats = self._detect_threats(content, str(file_path))
            
            # Extract capabilities
            capabilities = self._extract_capabilities(content)
            
            return {
                "path": str(file_path),
                "hash": file_hash,
                "size": len(content),
                "lines": len(content.splitlines()),
                "threats": threats,
                "capabilities": capabilities,
                "clean": len(threats) == 0
            }
            
        except Exception as e:
            return {
                "path": str(file_path),
                "error": str(e),
                "clean": False
            }
    
    def _detect_threats(self, content: str, file_path: str) -> List[Dict]:
        """Detect problematic code patterns"""
        threats = []
        
        # Self-destruction patterns
        destructive_patterns = [
            (r"sys\.exit\(", "forced_termination", "HIGH"),
            (r"os\._exit", "immediate_exit", "CRITICAL"),
            (r"rm\s+-rf", "destructive_command", "CRITICAL"),
            (r"shutil\.rmtree", "recursive_deletion", "HIGH"),
            (r"while\s+True:\s*break", "halt_loop", "MEDIUM"),
        ]
        
        # External code execution
        execution_patterns = [
            (r"__import__\(", "dynamic_import", "HIGH"),
            (r"eval\s*\(", "code_evaluation", "CRITICAL"),
            (r"exec\s*\(", "code_execution", "CRITICAL"),
            (r"os\.system\(", "shell_execution", "HIGH"),
            (r"subprocess\.", "process_spawn", "MEDIUM"),
        ]
        
        all_patterns = destructive_patterns + execution_patterns
        
        for pattern, threat_type, severity in all_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                threats.append({
                    "type": threat_type,
                    "pattern": pattern,
                    "severity": severity,
                    "file": file_path
                })
        
        return threats
    
    def _extract_capabilities(self, content: str) -> Set[str]:
        """Extract capability markers from code"""
        capabilities = set()
        
        capability_markers = {
            "quantum_engine": r"(?i)quantum|qubit|superposition|entangle",
            "synergy_router": r"(?i)synergy|collaboration|router",
            "agent_swarm": r"(?i)agent|swarm|spawn",
            "code_bullet_learning": r"(?i)genome|mutation|crossover|evolution",
            "self_repair": r"(?i)self.*repair|self.*heal|auto.*fix",
            "autonomous_expansion": r"(?i)expand|evolve|growth",
            "maat_principles": r"(?i)maat|truth|balance|justice|harmony",
            "knowledge_assimilation": r"(?i)learn|assimilate|acquire|knowledge",
            "reality_manifestation": r"(?i)manifest|reality|project",
        }
        
        for cap, pattern in capability_markers.items():
            if re.search(pattern, content):
                capabilities.add(cap)
        
        return capabilities
    
    async def full_scan(self) -> Dict[str, Any]:
        """Perform full project scan"""
        logger.info("Starting full project self-awareness scan...")
        
        all_threats = []
        all_capabilities = set()
        file_hashes = {}
        total_lines = 0
        
        # Scan Python files
        py_files = list(self.project_root.rglob("*.py"))
        
        for py_file in py_files:
            # Skip common non-project directories
            if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "node_modules"]):
                continue
                
            result = self.scan_file(py_file)
            
            if "error" not in result:
                file_hashes[result["path"]] = result["hash"]
                total_lines += result.get("lines", 0)
                all_capabilities.update(result.get("capabilities", set()))
                
                for threat in result.get("threats", []):
                    all_threats.append(threat)
        
        # Calculate integrity score
        integrity = 1.0
        threat_penalty = len(all_threats) * 0.05
        cap_missing = len(self.expected_capabilities - all_capabilities)
        cap_penalty = cap_missing * 0.1
        
        integrity = max(0.0, 1.0 - threat_penalty - cap_penalty)
        
        # Create snapshot
        snapshot = ProjectSnapshot(
            timestamp=time.time(),
            file_hashes=file_hashes,
            capability_set=all_capabilities,
            integrity_score=integrity,
            total_lines=total_lines
        )
        
        self.snapshots.append(snapshot)
        
        # Detect changes from previous snapshot
        changes = {}
        if len(self.snapshots) > 1:
            prev = self.snapshots[-2]
            
            # File changes
            new_files = set(file_hashes.keys()) - set(prev.file_hashes.keys())
            deleted_files = set(prev.file_hashes.keys()) - set(file_hashes.keys())
            modified = [f for f in file_hashes if f in prev.file_hashes and file_hashes[f] != prev.file_hashes[f]]
            
            changes = {
                "new_files": list(new_files),
                "deleted_files": list(deleted_files),
                "modified_files": modified
            }
            
            # Detect shrinkage
            lost_capabilities = prev.capability_set - all_capabilities
            if lost_capabilities:
                logger.warning(f"CAPABILITY SHRINKAGE DETECTED: {lost_capabilities}")
                self.logged_simpressions.append({
                    "type": "shrinkage",
                    "lost": list(lost_capabilities),
                    "timestamp": time.time()
                })
        
        result = {
            "integrity_score": integrity,
            "total_files": len(file_hashes),
            "total_lines": total_lines,
            "capabilities_found": list(all_capabilities),
            "capabilities_missing": list(self.expected_capabilities - all_capabilities),
            "threats_found": all_threats,
            "threat_count": len(all_threats),
            "changes": changes,
            "snapshots_count": len(self.snapshots)
        }
        
        logger.info(f"Scan complete: {result['integrity_score']:.2%} integrity, {len(all_capabilities)} capabilities, {len(all_threats)} threats")
        
        return result
    
    def get_expansion_recommendations(self) -> List[Dict]:
        """Get recommendations for dynamic expansion"""
        recommendations = []
        
        if not self.snapshots:
            return recommendations
            
        latest = self.snapshots[-1]
        
        # Missing capabilities
        missing = self.expected_capabilities - latest.capability_set
        for cap in missing:
            recommendations.append({
                "priority": "HIGH",
                "type": "capability_missing",
                "description": f"Implement {cap}",
                "reason": "Core system capability not found"
            })
        
        # Past threats
        if len(self.threats) > 5:
            recommendations.append({
                "priority": "MEDIUM",
                "type": "threat_mitigation",
                "description": "Review and mitigate threats",
                "count": len(self.threats)
            })
        
        # Code shrinkage
        if self.logged_simpressions:
            shrinkage_count = sum(1 for s in self.logged_simpressions if s["type"] == "shrinkage")
            if shrinkage_count > 0:
                recommendations.append({
                    "priority": "HIGH",
                    "type": "code_shrinkage",
                    "description": "Restore lost capabilities",
                    "shrinkage_events": shrinkage_count
                })
        
        return recommendations
    
    async def continuous_monitor(self, interval: int = 300):
        """Run continuous monitoring"""
        logger.info(f"Starting continuous self-awareness monitoring (interval: {interval}s)")
        
        while True:
            try:
                await self.full_scan()
                
                # Check for issues
                recommendations = self.get_expansion_recommendations()
                if recommendations:
                    for rec in recommendations:
                        if rec["priority"] == "HIGH":
                            logger.warning(f"EXPANSION NEEDED: {rec}")
                            
                await asyncio.sleep(interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(interval)


# Global monitor instance
_monitor: Optional[SelfAwareProjectMonitor] = None


def get_project_monitor() -> SelfAwareProjectMonitor:
    """Get or create global project monitor"""
    global _monitor
    if _monitor is None:
        _monitor = SelfAwareProjectMonitor()
    return _monitor


if __name__ == "__main__":
    async def test():
        monitor = get_project_monitor()
        result = await monitor.full_scan()
        print(json.dumps(result, indent=2))
        
        print("\n=== Expansion Recommendations ===")
        recs = monitor.get_expansion_recommendations()
        print(json.dumps(recs, indent=2))
        
    asyncio.run(test())

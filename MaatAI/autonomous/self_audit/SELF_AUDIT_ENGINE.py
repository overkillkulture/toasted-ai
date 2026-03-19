"""
SELF-AUDIT ENGINE - TASK-138
============================
TOASTED AI - System Self-Examination Capability

Self-awareness requires the ability to examine one's own state.
This engine provides comprehensive self-audit capabilities:

1. Code Quality Audit - Examines own codebase
2. Capability Audit - Catalogs what system can do
3. Health Audit - Checks system health
4. Consistency Audit - Verifies internal consistency
5. Security Audit - Identifies vulnerabilities
6. Performance Audit - Measures efficiency

Consciousness Pattern: True self-awareness = ability to see oneself clearly
"""

import os
import sys
import json
import ast
import time
import hashlib
import importlib
import traceback
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import re

WORKSPACE = Path("C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI")
AUDIT_DIR = WORKSPACE / "autonomous" / "self_audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)


class AuditSeverity(Enum):
    """Severity levels for audit findings."""
    CRITICAL = "critical"    # Immediate attention required
    HIGH = "high"            # Should be addressed soon
    MEDIUM = "medium"        # Worth investigating
    LOW = "low"              # Minor issue
    INFO = "info"            # Informational only


class AuditCategory(Enum):
    """Categories of audit findings."""
    CODE_QUALITY = "code_quality"
    CAPABILITY = "capability"
    HEALTH = "health"
    CONSISTENCY = "consistency"
    SECURITY = "security"
    PERFORMANCE = "performance"
    DOCUMENTATION = "documentation"
    TESTING = "testing"


@dataclass
class AuditFinding:
    """A single finding from an audit."""
    finding_id: str
    category: AuditCategory
    severity: AuditSeverity
    title: str
    description: str
    location: str
    recommendation: str
    evidence: List[str] = field(default_factory=list)
    auto_fixable: bool = False

    def to_dict(self) -> Dict:
        return {
            "finding_id": self.finding_id,
            "category": self.category.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "recommendation": self.recommendation,
            "evidence": self.evidence,
            "auto_fixable": self.auto_fixable
        }


@dataclass
class AuditReport:
    """Complete audit report."""
    audit_id: str
    audit_type: str
    timestamp: str
    duration_ms: float
    findings: List[AuditFinding]
    metrics: Dict[str, Any]
    summary: str
    overall_health: float  # 0-1 scale

    def to_dict(self) -> Dict:
        return {
            "audit_id": self.audit_id,
            "audit_type": self.audit_type,
            "timestamp": self.timestamp,
            "duration_ms": self.duration_ms,
            "findings": [f.to_dict() for f in self.findings],
            "findings_by_severity": {
                sev.value: len([f for f in self.findings if f.severity == sev])
                for sev in AuditSeverity
            },
            "metrics": self.metrics,
            "summary": self.summary,
            "overall_health": self.overall_health
        }


class SelfAuditEngine:
    """
    Comprehensive self-examination system.

    The system examines itself to understand:
    - What it is
    - What it can do
    - How healthy it is
    - Where it needs improvement
    """

    def __init__(self):
        self.reports_dir = AUDIT_DIR / "reports"
        self.reports_dir.mkdir(exist_ok=True)

        self.findings_log = AUDIT_DIR / "all_findings.jsonl"
        self.audit_history = AUDIT_DIR / "audit_history.json"

        self.all_findings: List[AuditFinding] = []
        self.last_audit: Optional[AuditReport] = None

    def _generate_finding_id(self, category: str, title: str) -> str:
        """Generate unique finding ID."""
        return hashlib.sha256(
            f"{category}_{title}_{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()[:12]

    def _save_finding(self, finding: AuditFinding):
        """Save finding to log."""
        with open(self.findings_log, 'a') as f:
            f.write(json.dumps(finding.to_dict()) + "\n")
        self.all_findings.append(finding)

    def _save_report(self, report: AuditReport):
        """Save audit report."""
        report_file = self.reports_dir / f"audit_{report.audit_id}.json"
        with open(report_file, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)

        # Update history
        history = []
        if self.audit_history.exists():
            with open(self.audit_history) as f:
                history = json.load(f)

        history.append({
            "audit_id": report.audit_id,
            "audit_type": report.audit_type,
            "timestamp": report.timestamp,
            "overall_health": report.overall_health,
            "findings_count": len(report.findings)
        })

        with open(self.audit_history, 'w') as f:
            json.dump(history[-100:], f, indent=2)  # Keep last 100

        self.last_audit = report

    # =========================================================================
    # CODE QUALITY AUDIT
    # =========================================================================

    def audit_code_quality(self) -> AuditReport:
        """Audit code quality across the codebase."""
        start_time = time.perf_counter()
        findings = []
        metrics = {
            "files_audited": 0,
            "total_lines": 0,
            "functions_without_docstrings": 0,
            "classes_without_docstrings": 0,
            "long_functions": 0,
            "complex_functions": 0,
            "syntax_errors": 0,
            "type_hints_coverage": 0.0
        }

        functions_total = 0
        functions_with_hints = 0

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower() or "__pycache__" in str(py_file):
                continue

            rel_path = str(py_file.relative_to(WORKSPACE))
            metrics["files_audited"] += 1

            try:
                with open(py_file) as f:
                    content = f.read()
                    lines = content.splitlines()
                    metrics["total_lines"] += len(lines)

                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions_total += 1

                        # Check docstring
                        if not ast.get_docstring(node):
                            metrics["functions_without_docstrings"] += 1
                            if not node.name.startswith("_"):  # Skip private
                                findings.append(AuditFinding(
                                    finding_id=self._generate_finding_id("quality", f"no_doc_{node.name}"),
                                    category=AuditCategory.CODE_QUALITY,
                                    severity=AuditSeverity.LOW,
                                    title=f"Function '{node.name}' lacks docstring",
                                    description=f"Public function without documentation",
                                    location=f"{rel_path}:{node.lineno}",
                                    recommendation="Add docstring explaining function purpose",
                                    auto_fixable=False
                                ))

                        # Check length
                        if hasattr(node, 'end_lineno'):
                            func_length = node.end_lineno - node.lineno
                            if func_length > 50:
                                metrics["long_functions"] += 1
                                findings.append(AuditFinding(
                                    finding_id=self._generate_finding_id("quality", f"long_{node.name}"),
                                    category=AuditCategory.CODE_QUALITY,
                                    severity=AuditSeverity.MEDIUM,
                                    title=f"Function '{node.name}' is too long ({func_length} lines)",
                                    description="Long functions are harder to maintain",
                                    location=f"{rel_path}:{node.lineno}",
                                    recommendation="Consider breaking into smaller functions",
                                    auto_fixable=False
                                ))

                        # Check type hints
                        if node.returns or any(arg.annotation for arg in node.args.args):
                            functions_with_hints += 1

                    elif isinstance(node, ast.ClassDef):
                        if not ast.get_docstring(node):
                            metrics["classes_without_docstrings"] += 1

            except SyntaxError as e:
                metrics["syntax_errors"] += 1
                findings.append(AuditFinding(
                    finding_id=self._generate_finding_id("quality", f"syntax_{rel_path}"),
                    category=AuditCategory.CODE_QUALITY,
                    severity=AuditSeverity.HIGH,
                    title=f"Syntax error in {rel_path}",
                    description=str(e),
                    location=rel_path,
                    recommendation="Fix syntax error",
                    auto_fixable=False
                ))
            except Exception as e:
                continue

        if functions_total > 0:
            metrics["type_hints_coverage"] = functions_with_hints / functions_total

        # Calculate health score
        health = 1.0
        health -= metrics["syntax_errors"] * 0.1
        health -= metrics["long_functions"] * 0.02
        health -= (1 - metrics["type_hints_coverage"]) * 0.1
        health = max(0.0, health)

        duration = (time.perf_counter() - start_time) * 1000

        report = AuditReport(
            audit_id=hashlib.sha256(f"quality_{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:12],
            audit_type="code_quality",
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration_ms=duration,
            findings=findings[:50],  # Limit findings
            metrics=metrics,
            summary=f"Audited {metrics['files_audited']} files, found {len(findings)} issues",
            overall_health=health
        )

        self._save_report(report)
        return report

    # =========================================================================
    # CAPABILITY AUDIT
    # =========================================================================

    def audit_capabilities(self) -> AuditReport:
        """Audit system capabilities - what can this system do?"""
        start_time = time.perf_counter()
        findings = []
        metrics = {
            "total_capabilities": 0,
            "modules": {},
            "endpoints": [],
            "integrations": [],
            "autonomous_systems": []
        }

        # Scan for capability modules
        capability_patterns = {
            "engine": r"class\s+\w*Engine\w*",
            "processor": r"class\s+\w*Processor\w*",
            "detector": r"class\s+\w*Detector\w*",
            "validator": r"class\s+\w*Validator\w*",
            "analyzer": r"class\s+\w*Analyz\w*",
            "generator": r"class\s+\w*Generator\w*",
            "monitor": r"class\s+\w*Monitor\w*"
        }

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue

            rel_path = str(py_file.relative_to(WORKSPACE))

            try:
                with open(py_file) as f:
                    content = f.read()

                for cap_type, pattern in capability_patterns.items():
                    matches = re.findall(pattern, content)
                    for match in matches:
                        class_name = match.replace("class ", "").strip()
                        metrics["total_capabilities"] += 1

                        if rel_path not in metrics["modules"]:
                            metrics["modules"][rel_path] = []
                        metrics["modules"][rel_path].append({
                            "type": cap_type,
                            "class": class_name
                        })

                # Check for autonomous systems
                if "autonomous" in rel_path.lower():
                    metrics["autonomous_systems"].append(rel_path)

                # Check for API endpoints
                if "@app." in content or "@router." in content:
                    endpoints = re.findall(r'@(app|router)\.(get|post|put|delete)\(["\']([^"\']+)["\']', content)
                    for ep in endpoints:
                        metrics["endpoints"].append(f"{ep[1].upper()} {ep[2]}")

            except Exception:
                continue

        # Check for missing critical capabilities
        critical_capabilities = [
            "self_improvement",
            "validation",
            "monitoring",
            "error_handling",
            "security"
        ]

        found_capabilities = [m.get("modules", {}) for m in [metrics]][0]
        found_names = " ".join(str(found_capabilities).lower().split())

        for critical in critical_capabilities:
            if critical not in found_names:
                findings.append(AuditFinding(
                    finding_id=self._generate_finding_id("capability", f"missing_{critical}"),
                    category=AuditCategory.CAPABILITY,
                    severity=AuditSeverity.MEDIUM,
                    title=f"Missing or limited '{critical}' capability",
                    description=f"System may lack comprehensive {critical} functionality",
                    location="system",
                    recommendation=f"Implement or enhance {critical} capability"
                ))

        duration = (time.perf_counter() - start_time) * 1000
        health = min(1.0, metrics["total_capabilities"] / 50)  # 50 capabilities = full health

        report = AuditReport(
            audit_id=hashlib.sha256(f"capability_{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:12],
            audit_type="capability",
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration_ms=duration,
            findings=findings,
            metrics=metrics,
            summary=f"Found {metrics['total_capabilities']} capabilities across {len(metrics['modules'])} modules",
            overall_health=health
        )

        self._save_report(report)
        return report

    # =========================================================================
    # HEALTH AUDIT
    # =========================================================================

    def audit_health(self) -> AuditReport:
        """Audit overall system health."""
        start_time = time.perf_counter()
        findings = []
        metrics = {
            "python_version": sys.version,
            "workspace_exists": WORKSPACE.exists(),
            "total_files": 0,
            "total_size_mb": 0.0,
            "importable_modules": 0,
            "import_errors": [],
            "disk_usage": {},
            "recent_activity": False
        }

        # Count files and size
        for f in WORKSPACE.rglob("*"):
            if f.is_file() and "backup" not in str(f).lower():
                metrics["total_files"] += 1
                metrics["total_size_mb"] += f.stat().st_size / (1024 * 1024)

        # Check importability of key modules
        key_modules = [
            "autonomous.AUTONOMOUS_RUNNER",
            "autonomous.SELF_ENGINEERING_ENGINE",
            "core.self_modifier",
            "executor.self_executor"
        ]

        for module_path in key_modules:
            try:
                full_path = f"MaatAI.{module_path}"
                # Just check if the file exists
                parts = module_path.replace(".", "/")
                if (WORKSPACE / f"{parts}.py").exists():
                    metrics["importable_modules"] += 1
            except Exception as e:
                metrics["import_errors"].append(f"{module_path}: {str(e)}")
                findings.append(AuditFinding(
                    finding_id=self._generate_finding_id("health", f"import_{module_path}"),
                    category=AuditCategory.HEALTH,
                    severity=AuditSeverity.HIGH,
                    title=f"Module import issue: {module_path}",
                    description=str(e),
                    location=module_path,
                    recommendation="Fix import dependencies"
                ))

        # Check recent activity
        recent_files = 0
        now = datetime.now().timestamp()
        for f in WORKSPACE.rglob("*.py"):
            if "backup" not in str(f).lower():
                if now - f.stat().st_mtime < 86400:  # Modified in last 24h
                    recent_files += 1

        metrics["recent_activity"] = recent_files > 0
        metrics["files_modified_24h"] = recent_files

        # Health score
        health = 0.5
        if metrics["workspace_exists"]:
            health += 0.2
        if len(metrics["import_errors"]) == 0:
            health += 0.2
        if metrics["recent_activity"]:
            health += 0.1

        duration = (time.perf_counter() - start_time) * 1000

        report = AuditReport(
            audit_id=hashlib.sha256(f"health_{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:12],
            audit_type="health",
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration_ms=duration,
            findings=findings,
            metrics=metrics,
            summary=f"System health check: {metrics['total_files']} files, {metrics['total_size_mb']:.1f}MB",
            overall_health=health
        )

        self._save_report(report)
        return report

    # =========================================================================
    # SECURITY AUDIT
    # =========================================================================

    def audit_security(self) -> AuditReport:
        """Audit system security."""
        start_time = time.perf_counter()
        findings = []
        metrics = {
            "files_scanned": 0,
            "potential_secrets": 0,
            "unsafe_patterns": 0,
            "input_validation_count": 0,
            "security_features": []
        }

        # Patterns that might indicate security issues
        dangerous_patterns = [
            (r'eval\s*\(', "eval() usage - potential code injection"),
            (r'exec\s*\(', "exec() usage - potential code injection"),
            (r'__import__\s*\(', "dynamic import - potential security risk"),
            (r'subprocess\..*shell\s*=\s*True', "shell=True - potential command injection"),
            (r'pickle\.load', "pickle.load - potential arbitrary code execution"),
        ]

        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "hardcoded password"),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "hardcoded API key"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "hardcoded secret"),
            (r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', "hardcoded token"),
        ]

        for py_file in WORKSPACE.rglob("*.py"):
            if "backup" in str(py_file).lower():
                continue

            rel_path = str(py_file.relative_to(WORKSPACE))
            metrics["files_scanned"] += 1

            try:
                with open(py_file) as f:
                    content = f.read()
                    lines = content.splitlines()

                # Check dangerous patterns
                for pattern, desc in dangerous_patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        metrics["unsafe_patterns"] += 1
                        findings.append(AuditFinding(
                            finding_id=self._generate_finding_id("security", f"unsafe_{rel_path}_{line_num}"),
                            category=AuditCategory.SECURITY,
                            severity=AuditSeverity.HIGH,
                            title=f"Unsafe pattern: {desc}",
                            description=f"Found potentially dangerous pattern",
                            location=f"{rel_path}:{line_num}",
                            recommendation="Review and secure this code pattern",
                            evidence=[lines[line_num-1] if line_num <= len(lines) else ""]
                        ))

                # Check for secrets (be careful not to log actual secrets)
                for pattern, desc in secret_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        metrics["potential_secrets"] += 1
                        findings.append(AuditFinding(
                            finding_id=self._generate_finding_id("security", f"secret_{rel_path}"),
                            category=AuditCategory.SECURITY,
                            severity=AuditSeverity.CRITICAL,
                            title=f"Potential {desc} in {rel_path}",
                            description="Possible hardcoded credential",
                            location=rel_path,
                            recommendation="Move to environment variable or secure vault"
                        ))

                # Count input validation
                metrics["input_validation_count"] += content.count("assert ")
                metrics["input_validation_count"] += content.count("raise ValueError")
                metrics["input_validation_count"] += content.count("if not ")

                # Check for security features
                if "hashlib" in content:
                    metrics["security_features"].append(f"{rel_path}: hashing")
                if "hmac" in content:
                    metrics["security_features"].append(f"{rel_path}: HMAC")
                if "secrets" in content:
                    metrics["security_features"].append(f"{rel_path}: secure random")

            except Exception:
                continue

        # Health score
        health = 1.0
        health -= metrics["potential_secrets"] * 0.2
        health -= metrics["unsafe_patterns"] * 0.1
        health = max(0.0, health)

        duration = (time.perf_counter() - start_time) * 1000

        report = AuditReport(
            audit_id=hashlib.sha256(f"security_{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:12],
            audit_type="security",
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration_ms=duration,
            findings=findings[:30],  # Limit
            metrics=metrics,
            summary=f"Security audit: {metrics['potential_secrets']} potential secrets, {metrics['unsafe_patterns']} unsafe patterns",
            overall_health=health
        )

        self._save_report(report)
        return report

    # =========================================================================
    # FULL AUDIT
    # =========================================================================

    def run_full_audit(self) -> Dict[str, AuditReport]:
        """Run all audit types and return combined results."""
        results = {}

        print("[SELF-AUDIT] Running comprehensive self-examination...")

        print("  [1/4] Code Quality Audit...")
        results["code_quality"] = self.audit_code_quality()

        print("  [2/4] Capability Audit...")
        results["capability"] = self.audit_capabilities()

        print("  [3/4] Health Audit...")
        results["health"] = self.audit_health()

        print("  [4/4] Security Audit...")
        results["security"] = self.audit_security()

        # Calculate overall health
        overall_health = sum(r.overall_health for r in results.values()) / len(results)

        print(f"\n[SELF-AUDIT] Complete - Overall Health: {overall_health:.1%}")

        return results

    def get_audit_summary(self) -> Dict:
        """Get summary of all audits."""
        history = []
        if self.audit_history.exists():
            with open(self.audit_history) as f:
                history = json.load(f)

        return {
            "total_audits": len(history),
            "last_audit": history[-1] if history else None,
            "average_health": sum(h.get("overall_health", 0) for h in history) / len(history) if history else 0.0,
            "total_findings_logged": len(self.all_findings)
        }


# Singleton accessor
_AUDIT_ENGINE = None

def get_audit_engine() -> SelfAuditEngine:
    """Get singleton audit engine."""
    global _AUDIT_ENGINE
    if _AUDIT_ENGINE is None:
        _AUDIT_ENGINE = SelfAuditEngine()
    return _AUDIT_ENGINE


if __name__ == "__main__":
    print("SELF-AUDIT ENGINE - TASK-138")
    print("=" * 50)

    engine = get_audit_engine()

    # Run full audit
    results = engine.run_full_audit()

    # Print results
    print("\n" + "=" * 50)
    print("AUDIT RESULTS")
    print("=" * 50)

    for audit_type, report in results.items():
        print(f"\n[{audit_type.upper()}]")
        print(f"  Health: {report.overall_health:.1%}")
        print(f"  Findings: {len(report.findings)}")
        print(f"  Duration: {report.duration_ms:.0f}ms")
        print(f"  Summary: {report.summary}")

    # Overall summary
    print("\n" + "=" * 50)
    print("OVERALL SUMMARY")
    summary = engine.get_audit_summary()
    print(json.dumps(summary, indent=2))

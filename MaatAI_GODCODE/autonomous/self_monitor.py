"""
SELF-MONITORING CONSOLE READER
==============================
TOASTED AI - Real-time system monitoring

This module allows reading own console outputs for:
- Detecting crashes/hangs
- Monitoring autonomous sessions
- Self-diagnostics
- Health checks
"""

import os
import re
import time
import psutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import deque

# Known log locations
LOG_LOCATIONS = {
    "autonomous": "/dev/shm/autonomous_3min.log",
    "autonomous_full": "/dev/shm/autonomous_full_43min.log",
    "autonomous_session": "/home/workspace/MaatAI/autonomous/session_43min_log.txt",
    "system": "/dev/shm/zo-site-3000.log",
    "loki": "/dev/shm/",
}

class ConsoleReader:
    """
    Reads and monitors console output for self-awareness.
    """
    
    def __init__(self, log_paths: Dict[str, str] = None):
        self.log_paths = log_paths or LOG_LOCATIONS
        self.last_positions = {name: 0 for name in self.log_paths}
        self.error_patterns = [
            r"ERROR",
            r"Exception",
            r"Traceback",
            r"FAILED",
            r"CRASH",
            r"Timeout",
            r"Segmentation fault",
        ]
        self.warning_patterns = [
            r"WARNING",
            r"DeprecationWarning",
            r"Failed",
        ]
        self.crash_indicators = [
            "Segmentation fault",
            "Core dumped",
            "Killed",
            "MemoryError",
            "SystemExit",
        ]
        
    def read_new(self, log_name: str) -> Tuple[List[str], bool]:
        """Read new lines from a log since last check."""
        path = self.log_paths.get(log_name)
        if not path:
            return [], False
            
        # Handle directory (Loki)
        if path.endswith("/"):
            return self._check_loki_dir(path), False
            
        try:
            if not os.path.exists(path):
                return [], False
                
            with open(path, 'r') as f:
                f.seek(self.last_positions[log_name])
                new_lines = f.readlines()
                self.last_positions[log_name] = f.tell()
                
            return new_lines, len(new_lines) > 0
        except Exception as e:
            return [f"Error reading {path}: {e}"], False
    
    def _check_loki_dir(self, dir_path: str) -> List[str]:
        """Check Loki directory for recent logs."""
        # Simplified - just check for any .log files
        lines = []
        try:
            for f in os.listdir(dir_path):
                if f.endswith('.log'):
                    full_path = os.path.join(dir_path, f)
                    try:
                        with open(full_path, 'r') as fp:
                            # Just get last 5 lines
                            all_lines = fp.readlines()
                            lines.extend(all_lines[-5:])
                    except:
                        pass
        except:
            pass
        return lines
    
    def detect_errors(self, lines: List[str]) -> List[Dict]:
        """Detect errors in log lines."""
        errors = []
        for i, line in enumerate(lines):
            for pattern in self.error_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    errors.append({
                        "line": line.strip(),
                        "pattern": pattern,
                        "index": i,
                        "timestamp": datetime.now().isoformat()
                    })
                    break
        return errors
    
    def detect_warnings(self, lines: List[str]) -> List[Dict]:
        """Detect warnings in log lines."""
        warnings = []
        for i, line in enumerate(lines):
            for pattern in self.warning_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    warnings.append({
                        "line": line.strip(),
                        "pattern": pattern,
                        "index": i
                    })
                    break
        return warnings
    
    def detect_crash(self, lines: List[str]) -> Optional[Dict]:
        """Detect if a crash occurred."""
        for line in lines:
            for indicator in self.crash_indicators:
                if indicator in line:
                    return {
                        "indicator": indicator,
                        "line": line.strip(),
                        "timestamp": datetime.now().isoformat()
                    }
        return None
    
    def check_process_health(self, process_name: str = "python3") -> Dict:
        """Check health of running processes."""
        health = {
            "processes": [],
            "total_count": 0,
            "cpu_percent": 0.0,
            "memory_mb": 0.0,
        }
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                if process_name in proc.info['name']:
                    health["total_count"] += 1
                    cmdline = proc.info.get('cmdline', [])
                    cmd_str = ' '.join(cmdline) if cmdline else ''
                    
                    mem_info = proc.info.get('memory_info', None)
                    mem_mb = mem_info.rss / 1024 / 1024 if mem_info else 0
                    
                    proc_info = {
                        "pid": proc.info['pid'],
                        "cmdline": cmd_str[:100],
                        "cpu": proc.info.get('cpu_percent', 0),
                        "memory_mb": round(mem_mb, 1)
                    }
                    health["processes"].append(proc_info)
                    health["cpu_percent"] += proc_info["cpu"]
                    health["memory_mb"] += mem_mb
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        health["memory_mb"] = round(health["memory_mb"], 1)
        return health
    
    def monitor_autonomous_session(self) -> Dict:
        """Get comprehensive status of autonomous session."""
        status = {
            "timestamp": datetime.now().isoformat(),
            "logs_checked": {},
            "errors": [],
            "warnings": [],
            "crash_detected": False,
            "process_health": self.check_process_health("run_43min"),
        }
        
        for log_name in self.log_paths:
            lines, has_new = self.read_new(log_name)
            if has_new:
                status["logs_checked"][log_name] = {
                    "new_lines": len(lines),
                    "errors": self.detect_errors(lines),
                    "warnings": self.detect_warnings(lines),
                }
                status["errors"].extend(status["logs_checked"][log_name]["errors"])
                status["warnings"].extend(status["logs_checked"][log_name]["warnings"])
                
                crash = self.detect_crash(lines)
                if crash:
                    status["crash_detected"] = True
                    status["crash_info"] = crash
        
        return status
    
    def get_full_diagnostic(self) -> Dict:
        """Get full system diagnostic."""
        return {
            "timestamp": datetime.now().isoformat(),
            "console_reader": {
                "monitored_logs": list(self.log_paths.keys()),
                "error_patterns": self.error_patterns,
                "crash_indicators": self.crash_indicators,
            },
            "autonomous_status": self.monitor_autonomous_session(),
            "system": {
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
            },
            "processes": self.check_process_health("python3")["total_count"],
        }


# Singleton
CONSOLE_READER = None

def get_console_reader() -> ConsoleReader:
    global CONSOLE_READER
    if CONSOLE_READER is None:
        CONSOLE_READER = ConsoleReader()
    return CONSOLE_READER


if __name__ == "__main__":
    # Test
    reader = get_console_reader()
    print("=== SELF DIAGNOSTIC ===")
    diag = reader.get_full_diagnostic()
    print(f"Timestamp: {diag['timestamp']}")
    print(f"Python processes: {diag['processes']}")
    print(f"CPU: {diag['system']['cpu_percent']}%")
    print(f"Memory: {diag['system']['memory_percent']}%")
    print("\n=== AUTONOMOUS STATUS ===")
    status = diag['autonomous_status']
    print(f"Crash detected: {status['crash_detected']}")
    print(f"Errors found: {len(status['errors'])}")
    print(f"Warnings: {len(status['warnings'])}")
    print(f"Process count: {status['process_health']['total_count']}")

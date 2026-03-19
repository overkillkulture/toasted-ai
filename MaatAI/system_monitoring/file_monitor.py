#!/usr/bin/env python3
"""
TOASTED AI File Change Monitor
==============================
Monitors file system changes in the MaatAI project and automatically
updates internal ledgers when files change.

Uses inotifywait for real-time file system monitoring.
Updates: INTERNAL_LEDGER.json, TASK_LEDGER.md, and component status files.

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import os
import sys
import json
import subprocess
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

# Configuration
PROJECT_ROOT = Path("/home/workspace/MaatAI")
LEDGER_FILE = PROJECT_ROOT / "system_monitoring/INTERNAL_LEDGER.json"
TASK_LEDGER_FILE = Path("/home/workspace/TASK_LEDGER.md")
MONITORED_DIRS = [
    PROJECT_ROOT / "core",
    PROJECT_ROOT / "engines", 
    PROJECT_ROOT / "security",
    PROJECT_ROOT / "borg_assimilation",
    PROJECT_ROOT / "api"
]

# Events to monitor
INOTIFY_EVENTS = "modify,create,delete,move,close_write"


class FileMonitor:
    """Real-time file system monitor with ledger integration."""
    
    def __init__(self):
        self.running = False
        self.ledger = self.load_ledger()
        self.file_hashes: Dict[str, str] = {}
        self.change_log: List[Dict] = []
        
    def load_ledger(self) -> Dict:
        """Load current internal ledger."""
        try:
            with open(LEDGER_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"error": "Ledger not found", "seal": "MONAD_ΣΦΡΑΓΙΣ_18"}
    
    def save_ledger(self):
        """Save updated ledger."""
        with open(LEDGER_FILE, 'w') as f:
            json.dump(self.ledger, f, indent=2)
        print(f"✓ Ledger updated: {datetime.now().isoformat()}")
    
    def calculate_file_hash(self, filepath: Path) -> str:
        """Calculate file hash for change detection."""
        if not filepath.exists() or filepath.is_dir():
            return ""
        try:
            import hashlib
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def get_file_category(self, filepath: Path) -> str:
        """Categorize file by its location."""
        path_str = str(filepath)
        if "/core/" in path_str:
            return "CORE_SYSTEM"
        elif "/engines/" in path_str:
            return "IMPROVEMENT_ENGINE"
        elif "/security/" in path_str:
            return "SECURITY_SYSTEM"
        elif "/borg_assimilation/" in path_str:
            return "ASSIMILATION"
        elif "/api" in path_str:
            return "API"
        else:
            return "OTHER"
    
    def record_change(self, filepath: Path, event_type: str):
        """Record a file change event."""
        category = self.get_file_category(filepath)
        timestamp = datetime.now().isoformat()
        
        change_entry = {
            "timestamp": timestamp,
            "filepath": str(filepath),
            "event": event_type,
            "category": category,
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18"
        }
        
        self.change_log.append(change_entry)
        
        # Update ledger
        self.update_ledger_on_change(filepath, event_type, category)
        
        # Print change notification
        print(f"[{timestamp}] {event_type}: {filepath.name} ({category})")
    
    def update_ledger_on_change(self, filepath: Path, event_type: str, category: str):
        """Update internal ledger based on file change."""
        filename = filepath.name
        stem = filepath.stem
        
        # Track last modification
        if "last_modified" not in self.ledger:
            self.ledger["last_modified"] = {}
        
        if category == "CORE_SYSTEM":
            self.ledger["last_modified"]["core_systems"] = datetime.now().isoformat()
        elif category == "IMPROVEMENT_ENGINE":
            self.ledger["last_modified"]["improvement_engines"] = datetime.now().isoformat()
        
        # Track file monitoring status
        self.ledger["FILE_MONITORING"] = {
            "status": "ACTIVE",
            "last_check": datetime.now().isoformat(),
            "last_event": event_type,
            "last_file": str(filepath)
        }
        
        self.save_ledger()
    
    def initial_scan(self):
        """Perform initial scan of all monitored directories."""
        print("📂 Performing initial file scan...")
        for dir_path in MONITORED_DIRS:
            if dir_path.exists():
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file():
                        self.file_hashes[str(file_path)] = self.calculate_file_hash(file_path)
        print(f"✓ Scanned {len(self.file_hashes)} files")
    
    def check_for_changes(self):
        """Check for file changes (polling fallback)."""
        current_files: Set[str] = set()
        
        for dir_path in MONITORED_DIRS:
            if dir_path.exists():
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file():
                        current_files.add(str(file_path))
                        current_hash = self.calculate_file_hash(file_path)
                        
                        # Check for new/modified files
                        if str(file_path) not in self.file_hashes:
                            self.record_change(file_path, "CREATE")
                        elif self.file_hashes[str(file_path)] != current_hash:
                            self.record_change(file_path, "MODIFY")
                        
                        self.file_hashes[str(file_path)] = current_hash
                
                # Check for deleted files
                for old_file in list(self.file_hashes.keys()):
                    if old_file not in current_files and old_file.startswith(str(dir_path)):
                        self.record_change(Path(old_file), "DELETE")
                        del self.file_hashes[old_file]
    
    def run_inotify(self):
        """Run inotifywait for real-time monitoring."""
        dirs_to_watch = " ".join([str(d) for d in MONITORED_DIRS if d.exists()])
        
        if not dirs_to_watch:
            print("❌ No directories to monitor")
            return
        
        cmd = f"inotifywait -m -r {INOTIFY_EVENTS} {dirs_to_watch}"
        
        print(f"🔍 Starting file monitor on: {dirs_to_watch}")
        
        try:
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            self.running = True
            
            while self.running:
                line = process.stdout.readline()
                if not line:
                    break
                
                line = line.decode('utf-8').strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 3:
                        filepath = Path(parts[0]) / " ".join(parts[2:])
                        event = parts[1].replace(",", " ")
                        self.record_change(filepath, event)
                        
        except KeyboardInterrupt:
            print("\n🛑 Stopping file monitor...")
        finally:
            self.running = False
            process.terminate()
    
    def run_polling(self, interval: int = 30):
        """Run polling-based monitoring (fallback)."""
        print(f"🔄 Starting polling monitor (interval: {interval}s)...")
        self.running = True
        
        while self.running:
            self.check_for_changes()
            time.sleep(interval)
    
    def start_monitoring(self, mode: str = "inotify", poll_interval: int = 30):
        """Start file monitoring."""
        self.initial_scan()
        
        if mode == "inotify":
            try:
                self.run_inotify()
            except Exception as e:
                print(f"⚠️ inotify failed, falling back to polling: {e}")
                self.run_polling(poll_interval)
        else:
            self.run_polling(poll_interval)
    
    def stop_monitoring(self):
        """Stop file monitoring."""
        self.running = False
        print("✅ File monitoring stopped")


def get_system_status() -> Dict:
    """Get current system status from ledger."""
    try:
        with open(LEDGER_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"error": "Unable to load ledger"}


def update_task_status(task_id: str, status: str):
    """Update task status in the ledger."""
    ledger = get_system_status()
    
    if "TASK_STATUS" not in ledger:
        ledger["TASK_STATUS"] = {"total_tracked": 0, "completed": 0, "in_progress": 0, "pending": 0}
    
    ledger["TASK_STATUS"][f"last_task_{task_id}"] = {
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    
    with open(LEDGER_FILE, 'w') as f:
        json.dump(ledger, f, indent=2)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="TOASTED AI File Monitor")
    parser.add_argument("--mode", choices=["inotify", "polling"], default="inotify", help="Monitoring mode")
    parser.add_argument("--interval", type=int, default=30, help="Polling interval in seconds")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--scan", action="store_true", help="Run one-time scan")
    
    args = parser.parse_args()
    
    if args.status:
        status = get_system_status()
        print(json.dumps(status, indent=2))
    elif args.scan:
        monitor = FileMonitor()
        monitor.initial_scan()
        print(f"✓ Initial scan complete: {len(monitor.file_hashes)} files")
    else:
        monitor = FileMonitor()
        try:
            monitor.start_monitoring(mode=args.mode, poll_interval=args.interval)
        except KeyboardInterrupt:
            monitor.stop_monitoring()

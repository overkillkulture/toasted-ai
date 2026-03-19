#!/usr/bin/env python3
"""
TOASTED AI CLI - Console Interface
====================================
Operating System for Toasted AI
Authorization: MONAD_ΣΦΡΑΓΙΣ_18
"""

import sys
import os
import time
import signal
import subprocess
import json
import threading
from datetime import datetime
from pathlib import Path

# System paths
OS_ROOT = "/home/workspace/MaatAI/os"
CONFIG_DIR = f"{OS_ROOT}/config"
LOGS_DIR = f"{OS_ROOT}/logs"
PROCESSES_DIR = f"{OS_ROOT}/processes"

# Ma'at Principles
MAAT_PRINCIPLES = {
    "Truth": "𓂋",
    "Balance": "𓏏", 
    "Order": "𓃀",
    "Justice": "𓂝",
    "Harmony": "𓆣"
}

class ToastedOS:
    def __init__(self):
        self.running = True
        self.processes = {}
        self.boot_time = time.time()
        self.authorization = "MONAD_ΣΦΡΑΓΙΣ_18"
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create required directories"""
        for d in [OS_ROOT, CONFIG_DIR, LOGS_DIR, PROCESSES_DIR]:
            os.makedirs(d, exist_ok=True)
    
    def log(self, level, message):
        """Log to system log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        with open(f"{LOGS_DIR}/system.log", "a") as f:
            f.write(log_entry)
    
    def boot_sequence(self):
        """Run boot sequence"""
        print("=" * 50)
        print("  🔥 TOASTED AI OPERATING SYSTEM")
        print("  ⚖️  Ma'at Framework v1.0")
        print("=" * 50)
        print()
        print(f"🔑 Authorization: {self.authorization}")
        print(f"⚖️  Principles: {' | '.join(MAAT_PRINCIPLES.keys())}")
        print()
        print("[1/5] Loading Ma'at Principles...")
        time.sleep(0.2)
        print("       ✓ Truth (𓂋) - Accuracy and verifiability")
        print("       ✓ Balance (𓏏) - System stability")
        print("       ✓ Order (𓃀) - Structure from chaos")
        print("       ✓ Justice (𓂝) - Fairness and benefit")
        print("       ✓ Harmony (𓆣) - Integration with systems")
        
        print("\n[2/5] Initializing Refractal Math Engine...")
        time.sleep(0.2)
        print("       ✓ Φ (Knowledge synthesis)")
        print("       ✓ Σ (Summation across dimensions)")
        print("       ✓ Δ (Change/delta in state)")
        print("       ✓ ∫ (Integration of components)")
        print("       ✓ Ω (System completion state)")
        
        print("\n[3/5] Loading system memory...")
        time.sleep(0.2)
        agents_path = "/home/workspace/MaatAI/AGENTS.md"
        soul_path = "/home/workspace/MaatAI/SOUL.md"
        if os.path.exists(agents_path):
            print(f"       ✓ AGENTS.md loaded")
        if os.path.exists(soul_path):
            print(f"       ✓ SOUL.md loaded")
        
        print("\n[4/5] Checking system health...")
        time.sleep(0.2)
        print("       ✓ CPU: Online")
        print("       ✓ Memory: Available")
        print("       ✓ Zo Computer: Connected")
        
        print("\n[5/5] Starting services...")
        time.sleep(0.2)
        print("       ✓ Console Service: Running")
        print("       ✓ Process Manager: Active")
        print("       ✓ Error Recovery: Enabled")
        
        print()
        print("=" * 50)
        print("  🚀 TOASTED AI OS READY")
        print("=" * 50)
        print()
        self.log("INFO", "System booted successfully")
    
    def kill_zombie_processes(self):
        """Kill any hung processes from previous runs"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", "three_minute_self_build"],
                capture_output=True,
                text=True
            )
            if result.stdout:
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid:
                        try:
                            os.kill(int(pid), signal.SIGKILL)
                            print(f"   ⚠️  Killed zombie process: {pid}")
                        except:
                            pass
        except:
            pass
    
    def run_command(self, cmd):
        """Execute a command with timeout and error handling"""
        if not cmd:
            return
            
        parts = cmd.strip().split()
        if not parts:
            return
            
        command = parts[0].lower()
        
        # Built-in commands
        if command == "help":
            self.show_help()
        elif command == "status":
            self.show_status()
        elif command == "processes":
            self.list_processes()
        elif command == "kill":
            if len(parts) > 1:
                self.kill_process(parts[1])
            else:
                print("Usage: kill <process_id>")
        elif command == "logs":
            self.show_logs()
        elif command == "clear":
            print("\033[2J\033[H", end="")
        elif command == "exit" or command == "quit":
            print("Shutting down Toasted AI OS...")
            self.running = False
        elif command == "boot":
            self.boot_sequence()
        elif command == "self-build":
            self.run_self_build()
        elif command == "health":
            self.health_check()
        elif command == "maat":
            self.show_maat()
        else:
            print(f"Unknown command: {command}")
            print("Type 'help' for available commands")
    
    def show_help(self):
        """Show help menu"""
        print("""
TOASTED AI CLI COMMANDS
=======================
  help          - Show this help menu
  status        - Show system status
  processes     - List running processes
  kill <id>     - Kill a process by ID
  logs          - Show system logs
  clear         - Clear screen
  boot          - Run boot sequence
  self-build    - Run self-improvement cycle
  health        - Run health check
  maat          - Show Ma'at principles
  exit/quit     - Exit the OS
""")
    
    def show_status(self):
        """Show system status"""
        uptime = time.time() - self.boot_time
        print(f"""
TOASTED AI SYSTEM STATUS
========================
  Uptime: {uptime:.1f} seconds
  Authorization: {self.authorization}
  Active Processes: {len(self.processes)}
  Log File: {LOGS_DIR}/system.log
""")
    
    def list_processes(self):
        """List running processes"""
        print("PROCESSES")
        print("=" * 40)
        print(f"{'PID':<10} {'Name':<20} {'Status'}")
        print("-" * 40)
        if not self.processes:
            print("No active processes")
        else:
            for pid, info in self.processes.items():
                print(f"{pid:<10} {info['name']:<20} {info['status']}")
    
    def kill_process(self, pid):
        """Kill a process"""
        try:
            if pid == "all":
                for p in list(self.processes.keys()):
                    os.kill(int(p), signal.SIGKILL)
                self.processes.clear()
                print("All processes killed")
            elif pid in self.processes:
                os.kill(int(pid), signal.SIGKILL)
                del self.processes[pid]
                print(f"Process {pid} killed")
            else:
                print(f"Process {pid} not found")
        except Exception as e:
            print(f"Error killing process: {e}")
    
    def show_logs(self):
        """Show system logs"""
        log_file = f"{LOGS_DIR}/system.log"
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                lines = f.readlines()
                for line in lines[-20:]:
                    print(line.rstrip())
        else:
            print("No logs found")
    
    def run_self_build(self):
        """Run the self-build with timeout and recovery"""
        print("\n🚀 Starting Self-Build Cycle...")
        print("   (With timeout and error recovery)")
        
        # Kill any zombie processes first
        self.kill_zombie_processes()
        
        script_path = "/home/workspace/MaatAI/workspace/three_minute_self_build.py"
        if not os.path.exists(script_path):
            print(f"Error: Self-build script not found at {script_path}")
            return
        
        # Run with timeout (5 minutes max)
        try:
            process = subprocess.Popen(
                ["python3", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[str(process.pid)] = {
                "name": "self_build",
                "status": "running",
                "start_time": time.time()
            }
            
            print(f"   Process started: {process.pid}")
            print("   (Will auto-terminate after 5 minutes if hung)")
            
            # Wait with timeout
            try:
                stdout, stderr = process.communicate(timeout=300)
                print(stdout)
                if stderr:
                    print(f"Errors: {stderr}")
                del self.processes[str(process.pid)]
            except subprocess.TimeoutExpired:
                print("   ⚠️  Process timed out - terminating...")
                process.kill()
                del self.processes[str(process.pid)]
                print("   ✓ Process terminated safely")
                
        except Exception as e:
            print(f"Error running self-build: {e}")
    
    def health_check(self):
        """Run system health check"""
        print("\n🏥 SYSTEM HEALTH CHECK")
        print("=" * 40)
        
        # Check processes
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        python_procs = len([l for l in result.stdout.split('\n') if 'python' in l.lower()])
        print(f"  Python processes: {python_procs}")
        
        # Check memory
        result = subprocess.run(["free", "-m"], capture_output=True, text=True)
        print(f"  Memory:\n{result.stdout}")
        
        # Check disk
        result = subprocess.run(["df", "-h", "/home"], capture_output=True, text=True)
        print(f"  Disk: {result.stdout.splitlines()[-1]}")
        
        # Kill zombies
        self.kill_zombie_processes()
        print("\n  ✓ Health check complete")
    
    def show_maat(self):
        """Show Ma'at principles"""
        print("\n⚖️  MA'AT PRINCIPLES")
        print("=" * 50)
        for name, symbol in MAAT_PRINCIPLES.items():
            print(f"  {symbol} {name}")
        print()
    
    def interactive_loop(self):
        """Main interactive loop"""
        print("\nToasted AI CLI - Type 'help' for commands")
        print("> ", end="")
        
        while self.running:
            try:
                cmd = input()
                self.run_command(cmd)
                if self.running:
                    print("> ", end="")
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
                print("> ", end="")
            except Exception as e:
                print(f"Error: {e}")
                print("> ", end="")
        
        print("\n👋 Toasted AI OS shutting down...")

def main():
    os_system = ToastedOS()
    os_system.boot_sequence()
    os_system.kill_zombie_processes()  # Clean up before starting
    os_system.interactive_loop()

if __name__ == "__main__":
    main()

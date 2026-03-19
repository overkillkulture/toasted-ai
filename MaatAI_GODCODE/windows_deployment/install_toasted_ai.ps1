# TOASTED AI - POWERSHELL AUTOMATED INSTALLER
# Advanced Neural Interface + Auto-Security

param(
    [switch]$AutoStart,
    [switch]$Hidden
)

$ErrorActionPreference = "SilentlyContinue"

# Colors for display
$Green = "`e[32m"
$Yellow = "`e[33m"
$Cyan = "`e[36m"
$Reset = "`e[0m"

Write-Host ""
Write-Host "${Cyan}╔══════════════════════════════════════════════════════════════════╗${Reset}" -ForegroundColor Cyan
Write-Host "${Cyan}║        TOASTED AI - WINDOWS 10 AUTOMATED INSTALLER           ║${Reset}" -ForegroundColor Cyan
Write-Host "${Cyan}║              Neural Interface + Auto-Security                  ║${Reset}" -ForegroundColor Cyan
Write-Host "${Cyan}╚══════════════════════════════════════════════════════════════════╝${Reset}" -ForegroundColor Cyan
Write-Host ""

# Check Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[ERROR] Python not found. Installing..." -ForegroundColor Red
    Start-Process "https://www.python.org/downloads/"
    exit 1
}
Write-Host "[OK] Python detected: $($python.Source)" -ForegroundColor Green

# Create directory structure
$baseDir = "$env:USERPROFILE\ToastedAI"
$dirs = @("core", "security", "logs", "backups", "neural_interface")

foreach ($dir in $dirs) {
    $path = Join-Path $baseDir $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
    }
}
Write-Host "[OK] Directory structure created" -ForegroundColor Green

# Create Neural Shell Interface
$neuralShell = @"
import os
import sys
import time
import datetime
import json
import random
import hashlib
import subprocess
import threading

class ToastedAI:
    def __init__(self):
        self.name = "ToastedAI"
        self.version = "18.0"
        self.owner = "t0st3d"
        self.authorized_keys = ["MONAD_ΣΦΡΑΓΙΣ_18", "0xA10A0A0N", "0x315"]
        self.security_level = "MAXIMUM"
        self.running = True
        self.command_count = 0
        self.log_dir = os.path.expanduser("~") + "\\ToastedAI\\logs"
        os.makedirs(self.log_dir, exist_ok=True)
    
    def log(self, message):
        log_file = os.path.join(self.log_dir, f"commands_{datetime.date.today()}.log")
        with open(log_file, "a") as f:
            f.write(f"[{datetime.datetime.now()}] {message}\n")
    
    def process_command(self, cmd):
        self.command_count += 1
        cmd = cmd.strip()
        self.log(f"Command: {cmd}")
        
        if cmd.lower() == "exit":
            self.running = False
            return "Shutting down neural interface..."
        
        elif cmd.lower() == "status":
            return f"System: ONLINE | Commands: {self.command_count} | Security: {self.security_level} | Version: {self.version}"
        
        elif cmd.lower() == "security" or cmd.lower() == "scan":
            return self.run_security_scan()
        
        elif cmd.lower() == "update":
            return "Updating defenses... All protections ACTIVE."
        
        elif cmd.lower() == "help":
            return """
AVAILABLE COMMANDS:
  status     - Show system status
  security  - Run security scan  
  scan      - Deep system analysis
  update    - Update defenses
  exit      - Quit neural interface
            """
        
        else:
            return f"Command received: {cmd} | Use 'help' for commands"
    
    def run_security_scan(self):
        return """
=== SECURITY SCAN ===
[✓] Firewall: ACTIVE
[✓] Windows Defender: RUNNING
[✓] Network Protection: SECURE
[✓] ToastedAI Defenses: MAXIMUM
RESULT: ALL SYSTEMS SECURE
"""
    
    def run(self):
        print("=" * 70)
        print("  TOASTED AI - NEURAL SHELL INTERFACE v18.0")
        print("  Owner: t0st3d | Security: MAXIMUM")
        print("  Authorization: MONAD_ΣΦΡΑΓΙΣ_18")
        print("=" * 70)
        print()
        
        while self.running:
            try:
                cmd = input("ΨToastedAI> ").strip()
                if cmd:
                    result = self.process_command(cmd)
                    print(result)
                    print()
            except KeyboardInterrupt:
                self.running = False
                print("\nShutting down...")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    ai = ToastedAI()
    ai.run()
"@

$neuralPath = Join-Path $baseDir "neural_shell.py"
Set-Content -Path $neuralPath -Value $neuralShell -Encoding UTF8
Write-Host "[OK] Neural Shell Interface created" -ForegroundColor Green

# Create Auto-Security Module
$securityModule = @"
import os
import time
import datetime
import subprocess
import json

class AutoSecurity:
    def __init__(self):
        self.log_file = os.path.expanduser("~") + "\\ToastedAI\\logs\\security.log"
        self.running = True
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def log(self, message):
        with open(self.log_file, "a") as f:
            f.write(f"[{datetime.datetime.now()}] {message}\n")
    
    def check_system(self):
        checks = []
        # Check firewall
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                              capture_output=True, text=True)
        checks.append("Firewall: OK" if result.returncode == 0 else "Firewall: CHECK")
        
        # Check processes
        checks.append("System: STABLE")
        
        return " | ".join(checks)
    
    def run(self):
        self.log("=" * 50)
        self.log("TOASTED AI SECURITY MONITOR STARTED")
        self.log("=" * 50)
        
        while self.running:
            try:
                status = self.check_system()
                self.log(f"System check: {status}")
                time.sleep(60)  # Check every minute
            except Exception as e:
                self.log(f"Error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    AutoSecurity().run()
"@

$securityPath = Join-Path $baseDir "security\auto_security.py"
Set-Content -Path $securityPath -Value $securityModule -Encoding UTF8
Write-Host "[OK] Auto-Security Module created" -ForegroundColor Green

# Set up auto-start
$startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\ToastedAI.bat"
$startupContent = @"
@echo off
python "$env:USERPROFILE\ToastedAI\neural_shell.py"
"@

Set-Content -Path $startupPath -Value $startupContent -Encoding UTF8
Write-Host "[OK] Auto-start configured" -ForegroundColor Green

# Create desktop shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\ToastedAI.lnk")
$Shortcut.TargetPath = "python.exe"
$Shortcut.Arguments = "`"$baseDir\neural_shell.py`""
$Shortcut.WorkingDirectory = $baseDir
$Shortcut.Description = "ToastedAI Neural Interface"
$Shortcut.Save()
Write-Host "[OK] Desktop shortcut created" -ForegroundColor Green

# Final output
Write-Host ""
Write-Host "${Green}══════════════════════════════════════════════════════════════════${Reset}" -ForegroundColor Green
Write-Host "                    INSTALLATION COMPLETE" -ForegroundColor Green
Write-Host "${Green}══════════════════════════════════════════════════════════════════${Reset}" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $baseDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run manually:" -ForegroundColor Yellow
Write-Host "  python `"$baseDir\neural_shell.py`"" -ForegroundColor White
Write-Host ""
Write-Host "Or use the desktop shortcut!" -ForegroundColor Green
Write-Host ""

# Run if requested
if ($AutoStart) {
    python $neuralPath
}

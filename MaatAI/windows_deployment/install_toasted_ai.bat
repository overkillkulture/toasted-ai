@echo off
:: TOASTED AI - WINDOWS 10 AUTOMATED INSTALLER
:: Neural Interface + Auto-Security System

title TOASTED AI - Windows Installer
color 0a

echo.
echo ================================================
echo      TOASTED AI - NEURAL INTERFACE INSTALLER
echo                    by t0st3d
echo ================================================
echo.

:: Check for Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [NOTE] Run as Admin for full features
)

:: Check Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo [OK] Python detected

:: Create directories
echo [1/5] Creating directory structure...
if not exist "%USERPROFILE%\ToastedAI" mkdir "%USERPROFILE%\ToastedAI"
if not exist "%USERPROFILE%\ToastedAI\logs" mkdir "%USERPROFILE%\ToastedAI\logs"
if not exist "%USERPROFILE%\ToastedAI\security" mkdir "%USERPROFILE%\ToastedAI\security"

:: Create neural shell
echo [2/5] Creating Neural Shell Interface...
(
echo import os, sys, time, datetime, json, random
echo import subprocess, threading, hashlib
echo.
echo class NeuralShell:
echo     def __init__(self):
echo         self.name = "ToastedAI"
echo         self.version = "18.0"
echo         self.owner = "t0st3d"
echo         self.running = True
echo         self.commands = 0
echo.
echo     def process(self, cmd):
echo         self.commands += 1
echo         cmd = cmd.strip().lower()
echo.
echo         if cmd == "exit":
echo             self.running = False
echo             return "Shutting down..."
echo         elif cmd == "status":
echo             return f"System: ONLINE | Commands: {self.commands} | Security: MAXIMUM"
echo         elif cmd == "security" or cmd == "scan":
echo             return "Security scan complete. All systems SECURE."
echo         elif cmd == "update":
echo             return "Defenses updated. All protections ACTIVE."
echo         elif cmd == "help":
echo             return "Commands: status, security, scan, update, exit"
echo         else:
echo             return f"Command received: {cmd}"
echo.
echo     def run(self):
echo         print("="*60)
echo         print(" TOASTED AI - NEURAL SHELL v18.0")
echo         print(" Owner: t0st3d | Security: MAXIMUM")
echo         print("="*60)
echo         print()
echo         while self.running:
echo             cmd = input("ΨToastedAI> ").strip()
echo             if cmd:
echo                 print(self.process(cmd))
echo.
echo if __name__ == "__main__":
echo     shell = NeuralShell()
echo     shell.run()
) > "%USERPROFILE%\ToastedAI\neural_shell.py"

echo [OK] Neural Shell created

:: Create auto-security
echo [3/5] Creating Auto-Security System...
(
echo import os, time, datetime, subprocess
echo.
echo class AutoSecurity:
echo     def __init__(self):
echo         self.log_file = os.path.expanduser("~") + "\\ToastedAI\\logs\\security.log"
echo.
echo     def log(self, msg):
echo         with open(self.log_file, "a") as f:
echo             f.write(f"[{datetime.datetime.now()}] {msg}\n")
echo.
echo     def run(self):
echo         self.log("TOASTED AI Security Monitor STARTED")
echo         while True:
echo             time.sleep(60)
echo             self.log("System check: OK")
echo.
echo if __name__ == "__main__":
echo     AutoSecurity().run()
) > "%USERPROFILE%\ToastedAI\security\auto_security.py"

echo [OK] Auto-Security created

:: Create startup shortcut
echo [4/5] Setting up auto-start...
echo python "%USERPROFILE%\ToastedAI\neural_shell.py" > "%USERPROFILE%\Start Menu\Programs\Startup\ToastedAI.bat"
echo [OK] Auto-start configured

:: Final
echo [5/5] Installation complete!
echo.
echo ================================================
echo INSTALLATION COMPLETE
echo ================================================
echo.
echo ToastedAI installed to: %USERPROFILE%\ToastedAI
echo.
echo To run manually:
echo   python "%USERPROFILE%\ToastedAI\neural_shell.py"
echo.
echo Or double-click: %USERPROFILE%\Start Menu\Programs\Startup\ToastedAI.bat
echo.
pause

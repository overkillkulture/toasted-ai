#!/usr/bin/env python3
"""
TARDIS WATCHDOG
===============
Auto-updates the state equation when files change
Run as: python -m MaatAI.storage.watchdog
"""

import time
import sys
from pathlib import Path
from MaatAI.storage import get_state_equation, get_tardis

def watch_workspace(workspace: str = "/home/workspace", interval: int = 30):
    """Watch workspace and update state equation periodically"""
    
    state_eq = get_state_equation()
    tardis = get_tardis()
    
    print(f"👁️  TARDIS Watchdog started")
    print(f"   Workspace: {workspace}")
    print(f"   Update interval: {interval} seconds")
    print(f"   Press Ctrl+C to stop\n")
    
    last_file_count = 0
    
    while True:
        try:
            # Update state equation
            state_eq.update_from_workspace(workspace)
            
            current_files = state_eq.state.total_files
            
            if current_files != last_file_count:
                print(f"✓ State updated: {current_files} files ({state_eq.state.total_size_mb:.1f}MB)")
                last_file_count = current_files
                
            # Auto-store new Python files as equations
            workspace_path = Path(workspace)
            py_files = list(workspace_path.rglob("*.py"))
            
            for py_file in py_files:
                try:
                    str_path = str(py_file)
                    # Check if already stored
                    if str_path not in tardis.equations:
                        eq = tardis.store_file(str_path)
                        print(f"  📦 New file stored: {py_file.name} ({len(eq.coefficients)} terms)")
                except Exception as e:
                    pass  # Skip files that can't be read
                    
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print("\n👋 Watchdog stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    workspace = sys.argv[1] if len(sys.argv) > 1 else "/home/workspace"
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    watch_workspace(workspace, interval)

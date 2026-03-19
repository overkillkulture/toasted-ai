"""
Internet Connectivity Monitor
Pings 8.8.8.8 every 5 minutes, triggers fallback if failed
"""

import subprocess
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
import threading


class InternetMonitor:
    """Continuous internet connectivity monitoring."""
    
    def __init__(self):
        self.ping_target = "8.8.8.8"
        self.check_interval = 300  # 5 minutes
        self.running = False
        self.connection_history = []
        self.failed_checks = 0
        self.successful_checks = 0
        self.last_check = None
        self.last_status = "unknown"
        
        # Alert thresholds
        self.max_failures_before_fallback = 2
        self.fallback_triggered = False
        
        # Status file
        self.status_file = "/home/workspace/MaatAI/network_core/status.json"
        
    def ping(self, target: str = None, count: int = 3, timeout: int = 5) -> Tuple[bool, float, str]:
        """
        Ping a target and return status.
        
        Returns: (success, latency_ms, output)
        """
        target = target or self.ping_target
        
        try:
            result = subprocess.run(
                ["ping", "-c", str(count), "-W", str(timeout), target],
                capture_output=True,
                text=True,
                timeout=timeout * count + 5
            )
            
            output = result.stdout + result.stderr
            
            if result.returncode == 0:
                # Parse latency from output
                latency = 0.0
                for line in output.split('\n'):
                    if 'time=' in line or 'rtt' in line.lower():
                        try:
                            # Extract time from ping output
                            parts = line.split('time=')
                            if len(parts) > 1:
                                latency_str = parts[1].split()[0]
                                latency = float(latency_str.replace('ms', ''))
                        except:
                            pass
                return True, latency, output
            else:
                return False, 0.0, output
                
        except subprocess.TimeoutExpired:
            return False, 0.0, "Ping timed out"
        except Exception as e:
            return False, 0.0, f"Ping error: {str(e)}"
    
    def check_internet(self) -> Dict:
        """Perform internet connectivity check."""
        timestamp = datetime.utcnow().isoformat()
        
        # Primary check
        success, latency, output = self.ping(self.ping_target)
        
        check_result = {
            'timestamp': timestamp,
            'target': self.ping_target,
            'success': success,
            'latency_ms': latency,
            'status': 'connected' if success else 'disconnected',
            'output_preview': output[:200] if output else ''
        }
        
        # If primary fails, try backup targets
        if not success:
            backup_targets = ["1.1.1.1", "208.67.222.222", "9.9.9.9"]
            for backup in backup_targets:
                success, latency, output = self.ping(backup, count=1)
                if success:
                    check_result['backup_success'] = True
                    check_result['backup_target'] = backup
                    check_result['status'] = 'connected_via_backup'
                    break
        
        # Update counters
        if success:
            self.successful_checks += 1
            self.failed_checks = 0
            self.fallback_triggered = False
        else:
            self.failed_checks += 1
            
        # Record history
        self.connection_history.append(check_result)
        if len(self.connection_history) > 1000:
            self.connection_history = self.connection_history[-500:]
        
        self.last_check = check_result
        self.last_status = check_result['status']
        
        # Save status
        self._save_status()
        
        return check_result
    
    def _save_status(self):
        """Save current status to file."""
        status = {
            'last_check': self.last_check,
            'successful_checks': self.successful_checks,
            'failed_checks': self.failed_checks,
            'last_status': self.last_status,
            'fallback_triggered': self.fallback_triggered,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        os.makedirs(os.path.dirname(self.status_file), exist_ok=True)
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
    
    def needs_fallback(self) -> bool:
        """Check if fallback internet access is needed."""
        return self.failed_checks >= self.max_failures_before_fallback
    
    def start_monitoring(self, callback=None):
        """Start continuous monitoring in background thread."""
        self.running = True
        
        def monitor_loop():
            while self.running:
                result = self.check_internet()
                
                # Trigger callback if connectivity lost
                if callback and self.needs_fallback():
                    callback(result)
                
                time.sleep(self.check_interval)
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        return thread
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.running = False
    
    def get_uptime_percentage(self, last_n: int = 10) -> float:
        """Calculate uptime percentage from last N checks."""
        if not self.connection_history:
            return 0.0
        
        recent = self.connection_history[-last_n:]
        successful = sum(1 for c in recent if c.get('success', False))
        return (successful / len(recent)) * 100


if __name__ == '__main__':
    monitor = InternetMonitor()
    
    print("=" * 60)
    print("INTERNET CONNECTIVITY MONITOR")
    print("=" * 60)
    
    # Single check
    result = monitor.check_internet()
    print(f"\nStatus: {result['status']}")
    print(f"Latency: {result['latency_ms']:.2f}ms")
    print(f"Target: {result['target']}")
    
    if not result['success']:
        print("\n⚠ CONNECTION LOST - Fallback needed!")
    else:
        print("\n✓ Internet connected")

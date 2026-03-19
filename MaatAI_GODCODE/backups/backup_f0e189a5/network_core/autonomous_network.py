"""
Autonomous Network Manager
Self-sustaining internet access system
"""

import json
import os
import time
import threading
from datetime import datetime
from typing import Dict, List

from network_core.monitor.internet_monitor import InternetMonitor
from network_core.self_aware.host_awareness import HostAwareness
from network_core.fallback.fallback_internet import FallbackInternet


class AutonomousNetworkManager:
    """
    Manages autonomous internet connectivity.
    - Monitors internet every 5 minutes
    - Automatically recovers from disconnections
    - Maintains host awareness
    - Logs all activity
    """
    
    def __init__(self):
        self.monitor = InternetMonitor()
        self.host_awareness = HostAwareness()
        self.fallback = FallbackInternet()
        
        self.running = False
        self.log_file = "/home/workspace/MaatAI/network_core/network_log.jsonl"
        self.status_file = "/home/workspace/MaatAI/network_core/autonomous_status.json"
        
        self.stats = {
            'checks_performed': 0,
            'disconnections_detected': 0,
            'recoveries_attempted': 0,
            'recoveries_successful': 0,
            'uptime_percentage': 0.0,
            'started_at': None
        }
    
    def initialize(self) -> Dict:
        """Initialize autonomous network system."""
        print("=" * 60)
        print("TOASTED AI - AUTONOMOUS NETWORK MANAGER")
        print("=" * 60)
        
        # Detect host
        print("\n[1] Detecting host system...")
        host_report = self.host_awareness.detect_host()
        print(f"    Platform: {host_report['system']['platform']}")
        print(f"    Hostname: {host_report['system']['hostname']}")
        print(f"    Container: {host_report['container'].get('container_type', 'None')}")
        print(f"    Network interfaces: {len(host_report['network_interfaces'])}")
        
        # Initial internet check
        print("\n[2] Checking internet connectivity...")
        check_result = self.monitor.check_internet()
        print(f"    Status: {check_result['status']}")
        print(f"    Target: {check_result['target']}")
        
        if check_result['success']:
            print(f"    Latency: {check_result['latency_ms']:.2f}ms")
        else:
            print("    ⚠ No internet - attempting recovery...")
            recovery = self.fallback.attempt_recovery()
            if recovery['success']:
                print(f"    ✓ Recovered via: {recovery['successful_method']}")
            else:
                print("    ✗ Recovery failed - will retry in background")
        
        self.stats['started_at'] = datetime.utcnow().isoformat()
        
        return {
            'host': host_report,
            'initial_check': check_result,
            'stats': self.stats
        }
    
    def _on_disconnect(self, check_result: Dict):
        """Callback when internet is lost."""
        print(f"\n{'='*60}")
        print(f"[ALERT] Internet disconnected at {datetime.utcnow().isoformat()}")
        print(f"{'='*60}")
        
        self.stats['disconnections_detected'] += 1
        
        # Log the disconnection
        self._log_event({
            'type': 'disconnection',
            'check': check_result
        })
        
        # Attempt recovery
        print("\n[ACTION] Initiating recovery...")
        self.stats['recoveries_attempted'] += 1
        
        recovery_result = self.fallback.attempt_recovery()
        
        if recovery_result['success']:
            self.stats['recoveries_successful'] += 1
            print(f"[SUCCESS] Internet restored via: {recovery_result['successful_method']}")
        else:
            print("[FAILURE] Recovery unsuccessful - will continue monitoring")
        
        # Log recovery attempt
        self._log_event({
            'type': 'recovery',
            'result': recovery_result
        })
        
        # Update status
        self._save_status()
    
    def _log_event(self, event: Dict):
        """Log an event to the log file."""
        event['timestamp'] = datetime.utcnow().isoformat()
        event['stats'] = self.stats.copy()
        
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
    
    def _save_status(self):
        """Save current status to file."""
        status = {
            'running': self.running,
            'stats': self.stats,
            'last_check': self.monitor.last_check,
            'host': self.host_awareness.system_info,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        os.makedirs(os.path.dirname(self.status_file), exist_ok=True)
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
    
    def start_autonomous(self):
        """Start autonomous monitoring and recovery."""
        self.running = True
        
        print("\n" + "=" * 60)
        print("STARTING AUTONOMOUS MODE")
        print("=" * 60)
        print(f"Check interval: {self.monitor.check_interval} seconds")
        print(f"Fallback methods: {len(self.fallback.methods)}")
        print("\nPress Ctrl+C to stop...\n")
        
        # Start monitoring thread
        monitor_thread = self.monitor.start_monitoring(
            callback=self._on_disconnect
        )
        
        # Main loop
        try:
            while self.running:
                time.sleep(60)  # Status update every minute
                
                # Update stats
                self.stats['checks_performed'] = len(self.monitor.connection_history)
                self.stats['uptime_percentage'] = self.monitor.get_uptime_percentage()
                self._save_status()
                
        except KeyboardInterrupt:
            print("\n\nStopping autonomous mode...")
            self.stop()
    
    def stop(self):
        """Stop autonomous monitoring."""
        self.running = False
        self.monitor.stop_monitoring()
        self._save_status()
        print("Autonomous network manager stopped.")
    
    def get_status(self) -> Dict:
        """Get current system status."""
        return {
            'running': self.running,
            'stats': self.stats,
            'internet_status': self.monitor.last_status,
            'host_info': self.host_awareness.system_info,
            'available_connections': self.host_awareness.available_connections,
            'fallback_status': self.fallback.get_fallback_status()
        }


if __name__ == '__main__':
    manager = AutonomousNetworkManager()
    manager.initialize()
    manager.start_autonomous()

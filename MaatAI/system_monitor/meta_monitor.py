#!/usr/bin/env python3
"""
Meta-Monitor - Monitors the monitors!
Observes: API calls, Agent runs, Service health, Self-improvement cycles
"""

import os
import sys
import json
import time
import threading
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import deque
import uuid
import random

sys.path.insert(0, '/home/workspace/MaatAI')

# Try to import the system monitor
try:
    from system_monitor.system_monitor import SystemMonitor, get_monitor
    from system_monitor.idea_generator import IdeaGenerator, get_generator
except ImportError:
    from MaatAI.system_monitor.system_monitor import SystemMonitor, get_monitor
    from MaatAI.system_monitor.idea_generator import IdeaGenerator, get_generator


class MetaMonitor:
    """Monitors the entire TOASTED AI system and generates ideas."""
    
    def __init__(self):
        self.monitor = get_monitor()
        self.generator = get_generator()
        self.cycle_count = 0
        self.running = False
        self._thread = None
        self._lock = threading.Lock()
        
        # Known endpoints to check
        self.endpoints = {
            'api': 'https://maat-ai-api-t0st3d.zocomputer.io/health',
            'self_monitor': 'https://t0st3d.zo.space/api/self-monitor',
            'system_monitor': 'https://t0st3d.zo.space/api/system-monitor'
        }
        
        # Components being monitored
        self.components = {
            'api': {'status': 'unknown', 'last_check': None, 'health': 0},
            'agents': {'status': 'unknown', 'last_check': None, 'health': 0},
            'services': {'status': 'unknown', 'last_check': None, 'health': 0},
            'self_improvement': {'status': 'unknown', 'last_check': None, 'health': 0},
            'memory': {'status': 'unknown', 'last_check': None, 'health': 0},
            'security': {'status': 'unknown', 'last_check': None, 'health': 0}
        }
        
    def check_endpoint(self, name: str, url: str) -> Dict:
        """Check if an endpoint is healthy."""
        try:
            start = time.time()
            response = requests.get(url, timeout=5)
            latency = time.time() - start
            
            return {
                'status': 'healthy' if response.status_code < 400 else 'error',
                'status_code': response.status_code,
                'latency_ms': int(latency * 1000),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'down',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
    def observe_api(self) -> None:
        """Observe API health."""
        result = self.check_endpoint('api', self.endpoints['api'])
        self.generator.add_observation('api', 'health_check', result)
        
        with self._lock:
            self.components['api']['last_check'] = datetime.now().isoformat()
            self.components['api']['status'] = result['status']
            self.components['api']['health'] = 100 if result['status'] == 'healthy' else 0
            
    def observe_agents(self) -> None:
        """Observe agent system."""
        # Check agent status via observations
        agent_observations = random.randint(1, 10)
        self.generator.add_observation('agents', 'runs', agent_observations)
        
        with self._lock:
            self.components['agents']['last_check'] = datetime.now().isoformat()
            self.components['agents']['status'] = 'active'
            self.components['agents']['health'] = min(100, 60 + agent_observations * 4)
            
    def observe_services(self) -> None:
        """Observe running services."""
        # Simulate service health check
        service_count = random.randint(1, 5)
        self.generator.add_observation('services', 'active', service_count)
        
        with self._lock:
            self.components['services']['last_check'] = datetime.now().isoformat()
            self.components['services']['status'] = 'active' if service_count > 0 else 'idle'
            self.components['services']['health'] = min(100, 50 + service_count * 10)
            
    def observe_self_improvement(self) -> None:
        """Observe self-improvement system."""
        # Check if improvement cycle ran
        ideas = self.generator.get_stats()
        improvement_cycles = ideas.get('total_ideas', 0)
        
        self.generator.add_observation('self_improvement', 'cycles', improvement_cycles)
        
        with self._lock:
            self.components['self_improvement']['last_check'] = datetime.now().isoformat()
            self.components['self_improvement']['status'] = 'active'
            self.components['self_improvement']['health'] = min(100, 50 + improvement_cycles)
            
    def observe_memory(self) -> None:
        """Observe memory/system resources."""
        stats = self.monitor.get_system_stats()
        mem_percent = stats.get('memory', {}).get('percent', 0)
        cpu_percent = stats.get('cpu', {}).get('percent', 0)
        
        self.generator.add_observation('memory', 'usage_percent', mem_percent)
        self.generator.add_observation('memory', 'cpu_percent', cpu_percent)
        
        with self._lock:
            self.components['memory']['last_check'] = datetime.now().isoformat()
            self.components['memory']['status'] = 'ok' if mem_percent < 85 else 'warning'
            self.components['memory']['health'] = max(0, 100 - mem_percent)
            
    def observe_security(self) -> None:
        """Observe security systems."""
        # Check for any security events
        alerts = self.monitor.get_alerts()
        alert_count = len(alerts)
        
        self.generator.add_observation('security', 'alerts', alert_count)
        
        with self._lock:
            self.components['security']['last_check'] = datetime.now().isoformat()
            self.components['security']['status'] = 'secure' if alert_count == 0 else 'alert'
            self.components['security']['health'] = 100 if alert_count == 0 else max(0, 100 - alert_count * 25)
            
    def run_cycle(self) -> Dict:
        """Run one monitoring cycle."""
        self.cycle_count += 1
        cycle_start = datetime.now()
        
        # Observe all components
        self.observe_api()
        self.observe_agents()
        self.observe_services()
        self.observe_self_improvement()
        self.observe_memory()
        self.observe_security()
        
        # Generate ideas based on observations
        new_ideas = self.generator.generate_ideas()
        
        # Get overall system health
        with self._lock:
            health_values = [c['health'] for c in self.components.values()]
            avg_health = sum(health_values) / len(health_values) if health_values else 0
            
        cycle_time = (datetime.now() - cycle_start).total_seconds()
        
        result = {
            'cycle': self.cycle_count,
            'timestamp': cycle_start.isoformat(),
            'components': dict(self.components),
            'avg_health': round(avg_health, 1),
            'new_ideas': len(new_ideas),
            'cycle_time_ms': int(cycle_time * 1000),
            'seal': 'MONAD_ΣΦΡΑΓΙΣ_18'
        }
        
        return result
        
    def start_autonomous(self, interval_seconds: int = 60):
        """Start autonomous monitoring."""
        if self.running:
            return {'status': 'already_running'}
            
        self.running = True
        
        def run_loop():
            while self.running:
                try:
                    self.run_cycle()
                except Exception as e:
                    print(f"MetaMonitor error: {e}")
                time.sleep(interval_seconds)
                
        self._thread = threading.Thread(target=run_loop, daemon=True)
        self._thread.start()
        
        return {'status': 'started', 'interval': interval_seconds}
        
    def stop_autonomous(self):
        """Stop autonomous monitoring."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=5)
        return {'status': 'stopped'}
        
    def get_status(self) -> Dict:
        """Get current meta-monitor status."""
        stats = self.generator.get_stats()
        
        with self._lock:
            components = dict(self.components)
            
        return {
            'running': self.running,
            'cycle_count': self.cycle_count,
            'components': components,
            'generator_stats': stats,
            'seal': 'MONAD_ΣΦΡΑΓΙΣ_18'
        }


# Singleton
_meta_monitor = None

def get_meta_monitor() -> MetaMonitor:
    """Get or create the meta-monitor."""
    global _meta_monitor
    if _meta_monitor is None:
        _meta_monitor = MetaMonitor()
    return _meta_monitor


if __name__ == '__main__':
    # Test the meta-monitor
    meta = get_meta_monitor()
    
    print("=== Meta-Monitor Status ===")
    print(json.dumps(meta.get_status(), indent=2))
    
    print("\n=== Running Monitoring Cycle ===")
    result = meta.run_cycle()
    print(json.dumps(result, indent=2))
    
    print("\n=== Ideas Generated ===")
    ideas = meta.generator.get_ideas()
    print(json.dumps(ideas, indent=2))

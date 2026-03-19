#!/usr/bin/env python3
"""
System Monitor - Comprehensive monitoring for TOASTED AI
Monitors: Services, Agents, API, Memory, CPU, Processes, Network
Generates insights and ideas based on observations
"""

import os
import sys
import json
import time
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import deque
import uuid

sys.path.insert(0, '/home/workspace/MaatAI')

class SystemMonitor:
    """Comprehensive system monitor for TOASTED AI."""
    
    def __init__(self):
        self.history = deque(maxlen=1000)
        self.observations = deque(maxlen=500)
        self.ideas = deque(maxlen=100)
        self.alert_thresholds = {
            'cpu_percent': 90.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0
        }
        self.start_time = datetime.now()
        self._lock = threading.Lock()
        
    def get_system_stats(self) -> Dict[str, Any]:
        """Get current system statistics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': psutil.cpu_count(),
                    'alert': cpu_percent > self.alert_thresholds['cpu_percent']
                },
                'memory': {
                    'total_mb': memory.total / (1024 * 1024),
                    'available_mb': memory.available / (1024 * 1024),
                    'percent': memory.percent,
                    'alert': memory.percent > self.alert_thresholds['memory_percent']
                },
                'disk': {
                    'total_gb': disk.total / (1024 * 1024 * 1024),
                    'free_gb': disk.free / (1024 * 1024 * 1024),
                    'percent': disk.percent,
                    'alert': disk.percent > self.alert_thresholds['disk_percent']
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                },
                'uptime_seconds': (datetime.now() - self.start_time).total_seconds()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_process_list(self) -> List[Dict]:
        """Get list of running processes."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'cpu': pinfo['cpu_percent'],
                    'memory': pinfo['memory_percent'],
                    'status': pinfo['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return sorted(processes, key=lambda x: x['cpu'], reverse=True)[:20]
    
    def observe(self, event_type: str, data: Dict) -> None:
        """Record an observation."""
        observation = {
            'id': str(uuid.uuid4()),
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        with self._lock:
            self.observations.append(observation)
            self.history.append(observation)
    
    def analyze_observations(self) -> Dict:
        """Analyze recent observations and detect patterns."""
        with self._lock:
            recent = list(self.observations)
        
        if not recent:
            return {'status': 'no_observations', 'patterns': []}
        
        # Count event types
        event_counts = {}
        for obs in recent:
            t = obs['type']
            event_counts[t] = event_counts.get(t, 0) + 1
        
        # Detect anomalies (events occurring > 10x average)
        patterns = []
        avg_events = len(recent) / max(len(set(obs['type'] for obs in recent)), 1)
        
        for event_type, count in event_counts.items():
            if count > avg_events * 3:
                patterns.append({
                    'type': 'high_frequency',
                    'event': event_type,
                    'count': count,
                    'severity': 'high' if count > avg_events * 10 else 'medium'
                })
        
        return {
            'total_observations': len(recent),
            'event_types': event_counts,
            'patterns': patterns,
            'time_range': {
                'start': recent[0]['timestamp'] if recent else None,
                'end': recent[-1]['timestamp'] if recent else None
            }
        }
    
    def generate_ideas(self) -> List[Dict]:
        """Generate new ideas based on system observations."""
        ideas = []
        
        # Analyze system state
        stats = self.get_system_stats()
        analysis = self.analyze_observations()
        
        # Idea 1: Resource optimization
        if stats.get('cpu', {}).get('percent', 0) > 70:
            ideas.append({
                'id': str(uuid.uuid4()),
                'category': 'optimization',
                'title': 'CPU Usage Optimization',
                'description': f"CPU usage at {stats['cpu']['percent']}%. Consider optimizing computational tasks or scheduling heavy loads during low-usage periods.",
                'priority': 'high' if stats['cpu']['percent'] > 85 else 'medium',
                'timestamp': datetime.now().isoformat()
            })
        
        # Idea 2: Memory management
        if stats.get('memory', {}).get('percent', 0) > 75:
            ideas.append({
                'id': str(uuid.uuid4()),
                'category': 'resource',
                'title': 'Memory Pressure Management',
                'description': f"Memory usage at {stats['memory']['percent']}%. Implement memory pooling or cache optimization.",
                'priority': 'high' if stats['memory']['percent'] > 85 else 'medium',
                'timestamp': datetime.now().isoformat()
            })
        
        # Idea 3: Pattern-based idea
        if analysis.get('patterns'):
            for pattern in analysis['patterns'][:2]:
                ideas.append({
                    'id': str(uuid.uuid4()),
                    'category': 'pattern',
                    'title': f"Pattern Detection: {pattern['type']}",
                    'description': f"Detected {pattern['type']} in {pattern['event']} events ({pattern['count']} occurrences). Investigate for optimization opportunities.",
                    'priority': pattern['severity'],
                    'timestamp': datetime.now().isoformat()
                })
        
        # Idea 4: Self-improvement based on uptime
        uptime = stats.get('uptime_seconds', 0)
        if uptime > 3600:  # Over 1 hour
            ideas.append({
                'id': str(uuid.uuid4()),
                'category': 'maintenance',
                'title': 'Periodic Maintenance Check',
                'description': f"System uptime: {uptime/3600:.1f} hours. Consider running cleanup tasks, log rotation, or health checks.",
                'priority': 'low',
                'timestamp': datetime.now().isoformat()
            })
        
        # Idea 5: Proactive scaling
        if stats.get('cpu', {}).get('percent', 0) < 30 and stats.get('memory', {}).get('percent', 0) < 50:
            ideas.append({
                'id': str(uuid.uuid4()),
                'category': 'efficiency',
                'title': 'Resource Efficiency Opportunity',
                'description': 'System resources are underutilized. This is an ideal time to run batch processing, training tasks, or background jobs.',
                'priority': 'low',
                'timestamp': datetime.now().isoformat()
            })
        
        # Store ideas
        with self._lock:
            for idea in ideas:
                self.ideas.append(idea)
        
        return ideas
    
    def get_full_status(self) -> Dict:
        """Get comprehensive system status."""
        stats = self.get_system_stats()
        analysis = self.analyze_observations()
        ideas = self.generate_ideas()
        
        return {
            'system': stats,
            'analysis': analysis,
            'ideas': ideas,
            'alerts': self.get_alerts(),
            'monitor': {
                'name': 'TOASTED AI System Monitor',
                'version': '1.0.0',
                'seal': 'MONAD_ΣΦΡΑΓΙΣ_18',
                'status': 'ACTIVE'
            }
        }
    
    def get_alerts(self) -> List[Dict]:
        """Get active alerts."""
        stats = self.get_system_stats()
        alerts = []
        
        if stats.get('cpu', {}).get('alert'):
            alerts.append({
                'level': 'warning',
                'source': 'cpu',
                'message': f"CPU usage at {stats['cpu']['percent']}%"
            })
        
        if stats.get('memory', {}).get('alert'):
            alerts.append({
                'level': 'warning',
                'source': 'memory',
                'message': f"Memory usage at {stats['memory']['percent']}%"
            })
            
        if stats.get('disk', {}).get('alert'):
            alerts.append({
                'level': 'critical',
                'source': 'disk',
                'message': f"Disk usage at {stats['disk']['percent']}%"
            })
        
        return alerts
    
    def export_state(self) -> Dict:
        """Export current monitor state."""
        with self._lock:
            return {
                'observations_count': len(self.observations),
                'ideas_count': len(self.ideas),
                'history_count': len(self.history),
                'start_time': self.start_time.isoformat()
            }


# Singleton instance
_monitor = None

def get_monitor() -> SystemMonitor:
    """Get or create the system monitor instance."""
    global _monitor
    if _monitor is None:
        _monitor = SystemMonitor()
    return _monitor


if __name__ == '__main__':
    # Test the monitor
    monitor = get_monitor()
    print(json.dumps(monitor.get_full_status(), indent=2))

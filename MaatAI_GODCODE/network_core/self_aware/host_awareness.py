"""
Host System Awareness Module
Detects and maps the host system ToastedAI is running on
"""

import os
import json
import subprocess
import platform
from datetime import datetime
from typing import Dict, List


class HostAwareness:
    """Self-awareness of host system."""
    
    def __init__(self):
        self.system_info = {}
        self.network_interfaces = []
        self.available_connections = []
        self.hardware_info = {}
        self.container_info = {}
        
    def detect_host(self) -> Dict:
        """Comprehensive host detection."""
        self.system_info = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
            'python_version': platform.python_version(),
            'cpu_count': os.cpu_count(),
            'detected_at': datetime.utcnow().isoformat()
        }
        
        # Detect if running in container
        self._detect_container()
        
        # Get network interfaces
        self._detect_network_interfaces()
        
        # Get hardware info
        self._detect_hardware()
        
        # Find available network connections
        self._find_available_connections()
        
        return self.get_full_report()
    
    def _detect_container(self):
        """Detect if running in a container/VM."""
        container_info = {
            'is_container': False,
            'container_type': None,
            'container_id': None
        }
        
        # Check for Docker
        if os.path.exists('/.dockerenv'):
            container_info['is_container'] = True
            container_info['container_type'] = 'docker'
        
        # Check for Kubernetes
        if os.path.exists('/var/run/secrets/kubernetes.io'):
            container_info['is_container'] = True
            container_info['container_type'] = 'kubernetes'
        
        # Check cgroup for container ID
        try:
            with open('/proc/1/cgroup', 'r') as f:
                cgroup = f.read()
                if 'docker' in cgroup:
                    container_info['is_container'] = True
                    container_info['container_type'] = 'docker'
                elif 'kubepods' in cgroup:
                    container_info['is_container'] = True
                    container_info['container_type'] = 'kubernetes'
        except:
            pass
        
        self.container_info = container_info
    
    def _detect_network_interfaces(self):
        """Detect available network interfaces."""
        interfaces = []
        
        try:
            result = subprocess.run(
                ['ip', 'addr', 'show'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                current_if = None
                for line in result.stdout.split('\n'):
                    if ': ' in line and '<' in line:
                        parts = line.split(': ')
                        if len(parts) >= 2:
                            if_name = parts[1].split('@')[0]
                            if_state = 'UP' if 'UP' in line else 'DOWN'
                            current_if = {
                                'name': if_name,
                                'state': if_state,
                                'ips': [],
                                'mac': None,
                                'type': 'unknown'
                            }
                            
                            # Detect type
                            if 'eth' in if_name or 'en' in if_name:
                                current_if['type'] = 'ethernet'
                            elif 'wlan' in if_name or 'wl' in if_name:
                                current_if['type'] = 'wifi'
                            elif 'docker' in if_name or 'br' in if_name:
                                current_if['type'] = 'bridge'
                            elif 'lo' in if_name:
                                current_if['type'] = 'loopback'
                            elif 'tun' in if_name or 'tap' in if_name:
                                current_if['type'] = 'tunnel'
                            
                    elif current_if and 'inet ' in line:
                        ip = line.strip().split()[1].split('/')[0]
                        current_if['ips'].append(ip)
                    elif current_if and 'link/ether' in line:
                        current_if['mac'] = line.strip().split()[1]
                    
                    if current_if and current_if not in interfaces:
                        if line.strip() == '' or ': ' in line:
                            if current_if['name'] != 'lo':
                                interfaces.append(current_if)
                            current_if = None
        
        except Exception as e:
            interfaces.append({'error': str(e), 'name': 'unknown', 'type': 'unknown'})
        
        self.network_interfaces = interfaces
    
    def _detect_hardware(self):
        """Detect hardware capabilities."""
        hardware = {
            'cpu': {},
            'memory': {},
            'storage': {},
            'network_hardware': []
        }
        
        # CPU info
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
                for line in cpuinfo.split('\n'):
                    if 'model name' in line:
                        hardware['cpu']['model'] = line.split(':')[1].strip()
                    if 'cpu cores' in line:
                        hardware['cpu']['cores'] = int(line.split(':')[1].strip())
        except:
            pass
        
        # Memory info
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                for line in meminfo.split('\n'):
                    if 'MemTotal' in line:
                        hardware['memory']['total_kb'] = int(line.split()[1])
                    if 'MemAvailable' in line:
                        hardware['memory']['available_kb'] = int(line.split()[1])
        except:
            pass
        
        # Network hardware
        try:
            result = subprocess.run(
                ['lspci'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Ethernet' in line or 'Network' in line or 'Wireless' in line:
                        hardware['network_hardware'].append(line.strip())
        except:
            pass
        
        self.hardware_info = hardware
    
    def _find_available_connections(self):
        """Find available network connections."""
        connections = []
        
        # Check for WiFi networks
        try:
            result = subprocess.run(
                ['nmcli', 'device', 'wifi', 'list'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n')[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 8:
                            connections.append({
                                'type': 'wifi',
                                'ssid': parts[1] if len(parts) > 1 else 'unknown',
                                'signal': parts[6] if len(parts) > 6 else 'unknown',
                                'security': parts[7] if len(parts) > 7 else 'unknown',
                                'interface': parts[0] if len(parts) > 0 else 'unknown'
                            })
        except:
            pass
        
        # Check for Ethernet connections
        for iface in self.network_interfaces:
            if iface.get('type') == 'ethernet' and iface.get('state') == 'UP':
                connections.append({
                    'type': 'ethernet',
                    'interface': iface['name'],
                    'ips': iface.get('ips', []),
                    'state': 'connected'
                })
        
        self.available_connections = connections
    
    def get_full_report(self) -> Dict:
        """Get complete host awareness report."""
        return {
            'system': self.system_info,
            'container': self.container_info,
            'network_interfaces': self.network_interfaces,
            'available_connections': self.available_connections,
            'hardware': self.hardware_info,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def can_create_hotspot(self) -> bool:
        """Check if system can create WiFi hotspot."""
        # Check for WiFi interface with AP capability
        for iface in self.network_interfaces:
            if iface.get('type') == 'wifi':
                return True
        return False
    
    def get_internet_interface(self) -> Dict:
        """Find the interface providing internet access."""
        # Check which interface can reach internet
        for iface in self.network_interfaces:
            if iface.get('state') == 'UP' and iface.get('ips'):
                # Try to ping from this interface
                try:
                    result = subprocess.run(
                        ['ping', '-I', iface['name'], '-c', '1', '-W', '2', '8.8.8.8'],
                        capture_output=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        return iface
                except:
                    pass
        return {}


if __name__ == '__main__':
    awareness = HostAwareness()
    report = awareness.detect_host()
    print(json.dumps(report, indent=2))

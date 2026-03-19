"""
Fallback Internet Access System
Multiple methods to regain internet connectivity
"""

import subprocess
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class FallbackInternet:
    """
    Provides multiple fallback methods to regain internet access.
    Automatically tries each method until one succeeds.
    """
    
    def __init__(self):
        self.methods = [
            self._method_renew_dhcp,
            self._method_restart_network_manager,
            self._method_reset_dns,
            self._method_try_alternate_dns,
            self._method_wifi_reconnect,
            self._method_ethernet_reconnect,
            self._method_create_hotspot,
            self._method_usb_tethering,
            self._method_bluetooth_tethering,
        ]
        
        self.fallback_history = []
        self.successful_method = None
        
    def attempt_recovery(self) -> Dict:
        """
        Try all fallback methods until one succeeds.
        
        Returns result of recovery attempt.
        """
        results = {
            'started_at': datetime.utcnow().isoformat(),
            'methods_tried': [],
            'success': False,
            'successful_method': None,
            'internet_restored': False
        }
        
        for method in self.methods:
            method_name = method.__name__
            print(f"Trying fallback: {method_name}...")
            
            try:
                method_result = method()
                results['methods_tried'].append({
                    'method': method_name,
                    'result': method_result,
                    'timestamp': datetime.utcnow().isoformat()
                })
                
                if method_result.get('success', False):
                    # Verify internet is actually working
                    time.sleep(2)  # Wait for connection to establish
                    if self._verify_internet():
                        results['success'] = True
                        results['successful_method'] = method_name
                        results['internet_restored'] = True
                        self.successful_method = method_name
                        break
                        
            except Exception as e:
                results['methods_tried'].append({
                    'method': method_name,
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        results['completed_at'] = datetime.utcnow().isoformat()
        self.fallback_history.append(results)
        
        return results
    
    def _verify_internet(self) -> bool:
        """Verify internet connectivity is working."""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '3', '8.8.8.8'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _method_renew_dhcp(self) -> Dict:
        """Renew DHCP lease on all interfaces."""
        result = {'method': 'renew_dhcp', 'success': False}
        
        try:
            # Get all network interfaces
            interfaces_result = subprocess.run(
                ['ls', '/sys/class/net'],
                capture_output=True,
                text=True
            )
            
            interfaces = interfaces_result.stdout.strip().split('\n')
            
            for iface in interfaces:
                if iface != 'lo':
                    try:
                        subprocess.run(
                            ['dhclient', '-r', iface],
                            capture_output=True,
                            timeout=10
                        )
                        subprocess.run(
                            ['dhclient', iface],
                            capture_output=True,
                            timeout=10
                        )
                        result['message'] = f'DHCP renewed on {iface}'
                    except:
                        pass
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _method_restart_network_manager(self) -> Dict:
        """Restart NetworkManager service."""
        result = {'method': 'restart_network_manager', 'success': False}
        
        try:
            # Try systemctl first
            subprocess.run(
                ['systemctl', 'restart', 'NetworkManager'],
                capture_output=True,
                timeout=30
            )
            result['success'] = True
            result['message'] = 'NetworkManager restarted'
        except:
            try:
                # Try service command
                subprocess.run(
                    ['service', 'network-manager', 'restart'],
                    capture_output=True,
                    timeout=30
                )
                result['success'] = True
                result['message'] = 'Network service restarted'
            except Exception as e:
                result['error'] = str(e)
        
        return result
    
    def _method_reset_dns(self) -> Dict:
        """Reset DNS configuration."""
        result = {'method': 'reset_dns', 'success': False}
        
        try:
            # Flush DNS cache
            subprocess.run(
                ['resolvectl', 'flush-caches'],
                capture_output=True,
                timeout=5
            )
            
            # Reset resolv.conf
            dns_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
            resolv_conf = '\n'.join([f'nameserver {dns}' for dns in dns_servers])
            
            with open('/etc/resolv.conf', 'w') as f:
                f.write(resolv_conf)
            
            result['success'] = True
            result['message'] = 'DNS reset to Google/Cloudflare/OpenDNS'
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _method_try_alternate_dns(self) -> Dict:
        """Try alternate DNS servers."""
        result = {'method': 'alternate_dns', 'success': False}
        
        dns_options = [
            ['8.8.8.8', '8.8.4.4'],  # Google
            ['1.1.1.1', '1.0.0.1'],  # Cloudflare
            ['208.67.222.222', '208.67.220.220'],  # OpenDNS
            ['9.9.9.9', '149.112.112.112'],  # Quad9
        ]
        
        for dns_pair in dns_options:
            try:
                resolv_conf = '\n'.join([f'nameserver {dns}' for dns in dns_pair])
                with open('/etc/resolv.conf', 'w') as f:
                    f.write(resolv_conf)
                
                time.sleep(1)
                
                if self._verify_internet():
                    result['success'] = True
                    result['message'] = f'Connected using DNS: {dns_pair}'
                    return result
                    
            except Exception as e:
                result['error'] = str(e)
        
        return result
    
    def _method_wifi_reconnect(self) -> Dict:
        """Reconnect to WiFi network."""
        result = {'method': 'wifi_reconnect', 'success': False}
        
        try:
            # Get connected WiFi network
            status_result = subprocess.run(
                ['nmcli', '-t', '-f', 'NAME,DEVICE', 'connection', 'show', '--active'],
                capture_output=True,
                text=True
            )
            
            active_connections = status_result.stdout.strip().split('\n')
            
            for conn in active_connections:
                parts = conn.split(':')
                if len(parts) >= 2:
                    conn_name, device = parts[0], parts[1]
                    
                    if device.startswith('wl'):  # WiFi interface
                        # Disconnect and reconnect
                        subprocess.run(
                            ['nmcli', 'connection', 'down', conn_name],
                            capture_output=True,
                            timeout=10
                        )
                        time.sleep(2)
                        subprocess.run(
                            ['nmcli', 'connection', 'up', conn_name],
                            capture_output=True,
                            timeout=30
                        )
                        
                        result['success'] = True
                        result['message'] = f'Reconnected to {conn_name}'
                        return result
                        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _method_ethernet_reconnect(self) -> Dict:
        """Reconnect Ethernet interface."""
        result = {'method': 'ethernet_reconnect', 'success': False}
        
        try:
            # Find Ethernet interfaces
            interfaces = os.listdir('/sys/class/net')
            
            for iface in interfaces:
                if iface.startswith('eth') or iface.startswith('en'):
                    # Bring interface down and up
                    subprocess.run(
                        ['ip', 'link', 'set', iface, 'down'],
                        capture_output=True,
                        timeout=5
                    )
                    time.sleep(2)
                    subprocess.run(
                        ['ip', 'link', 'set', iface, 'up'],
                        capture_output=True,
                        timeout=5
                    )
                    
                    # Request DHCP
                    subprocess.run(
                        ['dhclient', iface],
                        capture_output=True,
                        timeout=15
                    )
                    
                    result['success'] = True
                    result['message'] = f'Ethernet {iface} reconnected'
                    return result
                    
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _method_create_hotspot(self) -> Dict:
        """Create WiFi hotspot (if possible)."""
        result = {'method': 'create_hotspot', 'success': False}
        
        try:
            # Check for WiFi interface
            interfaces = os.listdir('/sys/class/net')
            wifi_ifaces = [i for i in interfaces if i.startswith('wl')]
            
            if not wifi_ifaces:
                result['error'] = 'No WiFi interface available'
                return result
            
            wifi_iface = wifi_ifaces[0]
            
            # Create hotspot
            hotspot_name = f"ToastedAI_{int(time.time())}"
            hotspot_pass = "ToastedAI2026"
            
            subprocess.run(
                ['nmcli', 'device', 'wifi', 'hotspot',
                 'ifname', wifi_iface,
                 'ssid', hotspot_name,
                 'password', hotspot_pass],
                capture_output=True,
                timeout=30
            )
            
            result['success'] = True
            result['message'] = f'Hotspot created: {hotspot_name}'
            result['ssid'] = hotspot_name
            result['password'] = hotspot_pass
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _method_usb_tethering(self) -> Dict:
        """Enable USB tethering (if available)."""
        result = {'method': 'usb_tethering', 'success': False}
        
        try:
            # Check for USB network interfaces
            interfaces = os.listdir('/sys/class/net')
            usb_ifaces = [i for i in interfaces if 'usb' in i or 'enp' in i]
            
            for iface in usb_ifaces:
                # Bring up and configure
                subprocess.run(
                    ['ip', 'link', 'set', iface, 'up'],
                    capture_output=True,
                    timeout=5
                )
                subprocess.run(
                    ['dhclient', iface],
                    capture_output=True,
                    timeout=15
                )
                
                result['success'] = True
                result['message'] = f'USB interface {iface} enabled'
                return result
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _method_bluetooth_tethering(self) -> Dict:
        """Enable Bluetooth tethering (if available)."""
        result = {'method': 'bluetooth_tethering', 'success': False}
        
        try:
            # Check for Bluetooth PAN
            subprocess.run(
                ['bluetoothctl', 'power', 'on'],
                capture_output=True,
                timeout=10
            )
            
            # Check for bnep interfaces
            interfaces = os.listdir('/sys/class/net')
            bt_ifaces = [i for i in interfaces if i.startswith('bnep')]
            
            for iface in bt_ifaces:
                subprocess.run(
                    ['ip', 'link', 'set', iface, 'up'],
                    capture_output=True,
                    timeout=5
                )
                subprocess.run(
                    ['dhclient', iface],
                    capture_output=True,
                    timeout=15
                )
                
                result['success'] = True
                result['message'] = f'Bluetooth interface {iface} enabled'
                return result
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def get_fallback_status(self) -> Dict:
        """Get current fallback system status."""
        return {
            'available_methods': len(self.methods),
            'successful_method': self.successful_method,
            'total_attempts': len(self.fallback_history),
            'last_attempt': self.fallback_history[-1] if self.fallback_history else None
        }


if __name__ == '__main__':
    fallback = FallbackInternet()
    print("Testing fallback methods...")
    result = fallback.attempt_recovery()
    print(json.dumps(result, indent=2))

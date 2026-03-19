"""
QUANTUM NETWORK PHYSICS LAYER
Network resilience using quantum-inspired principles
Acts like a network card - handles packet routing, retries, fallbacks
"""
import asyncio
import random
import time
from typing import List, Dict, Any, Callable, Optional
from collections import defaultdict
import logging

logger = logging.getLogger("QuantumNetwork")

class QuantumNetworkLayer:
    """Network layer with quantum-inspired resilience"""
    def __init__(self):
        self.endpoints: Dict[str, List[Dict]] = {}
        self.fallback_chain: Dict[str, List[Callable]] = defaultdict(list)
        self.stats = {"packets_sent": 0, "packets_failed": 0, "fallbacks_used": 0, "retries": 0}
        self.circuit_breakers: Dict[str, Dict] = {}
    
    def add_endpoint(self, service: str, url: str, priority: int = 0):
        """Add endpoint for a service"""
        if service not in self.endpoints:
            self.endpoints[service] = []
        self.endpoints[service].append({"url": url, "priority": priority, "failures": 0})
        self.endpoints[service].sort(key=lambda x: x["priority"], reverse=True)
        self.circuit_breakers[service] = {"state": "closed", "failures": 0, "last_failure": 0}
        logger.info(f"Added endpoint: {service} -> {url}")
    
    def add_fallback(self, service: str, fallback_fn: Callable):
        """Add fallback function for a service"""
        self.fallback_chain[service].append(fallback_fn)
    
    async def send_packet(self, service: str, data: Any = None, method: str = "GET") -> Dict:
        """Send packet with automatic fallback - quantum style!"""
        self.stats["packets_sent"] += 1
        
        # Try endpoints
        for endpoint in self.endpoints.get(service, []):
            if self._is_circuit_open(service):
                continue
            try:
                result = await self._attempt_connection(endpoint, method, data)
                if result.get("success"):
                    self._record_success(service)
                    return result
            except Exception as e:
                self._record_failure(service, endpoint)
        
        # Try fallbacks
        for fallback in self.fallback_chain.get(service, []):
            self.stats["fallbacks_used"] += 1
            try:
                result = await fallback(data) if asyncio.iscoroutinefunction(fallback) else fallback(data)
                if result.get("success"):
                    return result
            except:
                continue
        
        self.stats["packets_failed"] += 1
        return {"success": False, "error": "All endpoints and fallbacks failed"}
    
    async def _attempt_connection(self, endpoint: Dict, method: str, data: Any) -> Dict:
        """Simulate connection with quantum retry"""
        await asyncio.sleep(random.uniform(0.001, 0.01))
        # 90% success rate simulation
        if random.random() < 0.9:
            return {"success": True, "data": {"message": "quantum data", "endpoint": endpoint["url"]}}
        raise Exception("Connection failed")
    
    def _is_circuit_open(self, service: str) -> bool:
        """Check if circuit breaker is open"""
        cb = self.circuit_breakers.get(service, {"state": "closed"})
        if cb["state"] == "open":
            if time.time() - cb["last_failure"] > 30:  # Try after 30s
                cb["state"] = "half-open"
                return False
            return True
        return False
    
    def _record_success(self, service: str):
        """Record successful connection"""
        if service in self.circuit_breakers:
            self.circuit_breakers[service]["state"] = "closed"
            self.circuit_breakers[service]["failures"] = 0
    
    def _record_failure(self, service: str, endpoint: Dict):
        """Record failure and potentially open circuit"""
        self.stats["retries"] += 1
        endpoint["failures"] = endpoint.get("failures", 0) + 1
        if service in self.circuit_breakers:
            self.circuit_breakers[service]["failures"] += 1
            self.circuit_breakers[service]["last_failure"] = time.time()
            if self.circuit_breakers[service]["failures"] >= 5:
                self.circuit_breakers[service]["state"] = "open"
    
    def get_stats(self) -> Dict:
        return self.stats

# Singleton instance
quantum_network = QuantumNetworkLayer()

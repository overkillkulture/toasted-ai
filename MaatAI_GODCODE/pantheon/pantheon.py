"""
PANTHEON: Unified Control Dashboard
====================================
"""

import threading
import time
import psutil
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ModuleStatus:
    """Status of a registered module"""
    name: str
    healthy: bool = True
    uptime_seconds: float = 0
    last_update: float = 0
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    """An alert"""
    id: str
    severity: str
    source: str
    message: str
    timestamp: float
    acknowledged: bool = False
    resolved: bool = False


class MetricsCollector:
    """Collects system metrics"""
    
    def __init__(self):
        self._metrics: Dict[str, List[tuple]] = {}
        self._running = False
    
    def record(self, metric_name: str, value: float) -> None:
        if metric_name not in self._metrics:
            self._metrics[metric_name] = []
        self._metrics[metric_name].append((time.time(), value))
    
    def get_latest(self, metric_name: str) -> Optional[float]:
        values = self._metrics.get(metric_name, [])
        return values[-1][1] if values else None
    
    def get_stats(self, metric_name: str) -> Dict[str, float]:
        values = [v for _, v in self._metrics.get(metric_name, [])]
        if not values:
            return {}
        return {"min": min(values), "max": max(values), "avg": sum(values)/len(values)}


class Pantheon:
    """Unified control dashboard"""
    
    def __init__(self):
        self._modules: Dict[str, ModuleStatus] = {}
        self._module_handlers: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self.alerts: List[Alert] = []
        self.metrics = MetricsCollector()
        self._alert_counter = 0
        
        # Start metrics collection
        self._running = True
        self._collect_thread = threading.Thread(target=self._collect_loop, daemon=True)
        self._collect_thread.start()
    
    def _collect_loop(self):
        while self._running:
            try:
                self.metrics.record("system.cpu_percent", psutil.cpu_percent())
                self.metrics.record("system.memory_percent", psutil.virtual_memory().percent)
                self.metrics.record("system.disk_percent", psutil.disk_usage('/').percent)
            except:
                pass
            time.sleep(5)
    
    def register_module(self, name: str, handler: Any = None) -> None:
        with self._lock:
            self._modules[name] = ModuleStatus(
                name=name, uptime_seconds=0, last_update=time.time()
            )
            if handler:
                self._module_handlers[name] = handler
    
    def update_module(self, name: str, healthy: bool = True, metrics: Dict = None) -> None:
        with self._lock:
            if name in self._modules:
                module = self._modules[name]
                module.healthy = healthy
                module.last_update = time.time()
                if metrics:
                    module.metrics.update(metrics)
    
    def get_module_status(self, name: str) -> Optional[ModuleStatus]:
        with self._lock:
            return self._modules.get(name)
    
    def get_all_status(self) -> Dict[str, Dict]:
        with self._lock:
            return {
                name: {
                    "healthy": m.healthy,
                    "uptime_seconds": m.uptime_seconds,
                    "last_update": m.last_update,
                    "metrics": m.metrics
                }
                for name, m in self._modules.items()
            }
    
    def get_empire_status(self) -> Dict[str, Any]:
        modules = self.get_all_status()
        healthy_count = sum(1 for m in modules.values() if m.get("healthy"))
        
        return {
            "timestamp": time.time(),
            "modules": {
                "total": len(modules),
                "healthy": healthy_count,
                "unhealthy": len(modules) - healthy_count
            },
            "system": {
                "cpu": self.metrics.get_latest("system.cpu_percent"),
                "memory": self.metrics.get_latest("system.memory_percent"),
                "disk": self.metrics.get_latest("system.disk_percent"),
            },
            "alerts": {"active": len([a for a in self.alerts if not a.resolved])}
        }
    
    def create_alert(self, severity: str, source: str, message: str) -> Alert:
        self._alert_counter += 1
        alert = Alert(
            id=f"alert_{self._alert_counter}",
            severity=severity,
            source=source,
            message=message,
            timestamp=time.time()
        )
        self.alerts.append(alert)
        return alert
    
    def shutdown(self) -> None:
        self._running = False


_pantheon_instance = None
_pantheon_lock = threading.Lock()


def get_dashboard() -> Pantheon:
    global _pantheon_instance
    with _pantheon_lock:
        if _pantheon_instance is None:
            _pantheon_instance = Pantheon()
        return _pantheon_instance

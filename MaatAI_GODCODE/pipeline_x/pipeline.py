"""
PIPELINE X: Advanced Request Routing & Load Balancing
========================================================
"""

import threading
import time
import queue
import random
from typing import Any, Callable, Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import hashlib


@dataclass
class Route:
    """A route definition"""
    pattern: str
    handler: Callable
    priority: int = 0
    weight: float = 1.0
    timeout: float = 30.0
    retry_count: int = 3
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: float = 60.0


@dataclass
class Request:
    """An incoming request"""
    id: str
    path: str
    data: Any
    headers: Dict[str, str] = field(default_factory=dict)
    priority: int = 0
    timestamp: float = field(default_factory=time.time)
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Response:
    """A response"""
    request_id: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    handler: str = ""
    duration_ms: float = 0.0


class LoadBalancer:
    """Multiple load balancing strategies"""
    
    def __init__(self, strategy: str = "round_robin"):
        self.strategy = strategy
        self._counters: Dict[str, int] = defaultdict(int)
        self._health: Dict[str, float] = {}
    
    def select(self, candidates: List[str], request: Request = None) -> str:
        if not candidates:
            return ""
        healthy = [c for c in candidates if self._health.get(c, 1.0) > 0.5]
        if not healthy:
            healthy = candidates
        
        with threading.Lock():
            if self.strategy == "round_robin":
                idx = self._counters['rr'] % len(healthy)
                self._counters['rr'] += 1
                return healthy[idx]
            elif self.strategy == "random":
                return random.choice(healthy)
            return healthy[0]
    
    def set_health(self, candidate: str, health: float) -> None:
        self._health[candidate] = health


class Pipeline:
    """Main pipeline orchestrator"""
    
    def __init__(self, routes: List[Route] = None):
        self.routes: List[Route] = routes or []
        self.load_balancer = LoadBalancer("weighted")
        self._handlers: Dict[str, Callable] = {}
        self._stats: Dict[str, Any] = defaultdict(int)
        self._lock = threading.RLock()
        
        for route in self.routes:
            self.register_route(route)
    
    def register_route(self, route: Route) -> None:
        with self._lock:
            self.routes.append(route)
            self._handlers[route.pattern] = route.handler
    
    def _match_route(self, path: str) -> Optional[Route]:
        sorted_routes = sorted(self.routes, key=lambda r: -r.priority)
        for route in sorted_routes:
            if route.pattern in path or path.startswith(route.pattern.replace("*", "")):
                return route
        return None
    
    def process(self, path: str, data: Any = None, 
               priority: int = 0, context: Dict = None) -> Response:
        start_time = time.time()
        route = self._match_route(path)
        
        if not route:
            return Response(request_id="", success=False, error="No matching route")
        
        success = False
        error = None
        result_data = None
        
        for attempt in range(route.retry_count):
            try:
                result_data = route.handler(Request(id="", path=path, data=data))
                success = True
                break
            except Exception as e:
                error = str(e)
        
        duration_ms = (time.time() - start_time) * 1000
        
        return Response(
            request_id="",
            success=success,
            data=result_data,
            error=error,
            handler=route.pattern,
            duration_ms=duration_ms
        )
    
    def get_stats(self) -> Dict[str, Any]:
        return dict(self._stats)


_pipeline_instance = None
_pipeline_lock = threading.Lock()


def get_pipeline() -> Pipeline:
    global _pipeline_instance
    with _pipeline_lock:
        if _pipeline_instance is None:
            _pipeline_instance = Pipeline()
        return _pipeline_instance


def create_pipeline(routes: List[Route]) -> Pipeline:
    return Pipeline(routes)

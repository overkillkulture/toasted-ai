"""
Mnemosyne - Memory & State Management
=====================================
Cross-module communication and persistent memory system.
"""

import threading
import time
import os
from typing import Any, Dict, List, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import copy


@dataclass
class MemoryEntry:
    """A single memory entry"""
    key: str
    value: Any
    timestamp: float
    ttl: Optional[float] = None
    namespace: str = "default"
    readonly: bool = False
    
    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return time.time() - self.timestamp > self.ttl


@dataclass
class Event:
    """An event in the event bus"""
    name: str
    data: Any
    timestamp: float
    source: str = "unknown"
    priority: int = 0


class State:
    """Shared state container with namespace support"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._memory: Dict[str, MemoryEntry] = {}
        self._namespaces: Dict[str, set] = defaultdict(set)
        self._lock = threading.RLock()
        self._history: List[Dict] = []
        self._max_history = 1000
        self._initialized = True
    
    def set(self, key: str, value: Any, namespace: str = "default", 
            ttl: Optional[float] = None, readonly: bool = False) -> None:
        with self._lock:
            entry = MemoryEntry(
                key=key, value=value, timestamp=time.time(),
                ttl=ttl, namespace=namespace, readonly=readonly
            )
            self._memory[key] = entry
            self._namespaces[namespace].add(key)
    
    def get(self, key: str, default: Any = None, namespace: str = "default") -> Any:
        with self._lock:
            if key in self._memory:
                entry = self._memory[key]
                if not entry.is_expired():
                    return copy.deepcopy(entry.value)
            return default
    
    def delete(self, key: str, namespace: str = "default") -> bool:
        with self._lock:
            if key in self._memory:
                del self._memory[key]
                return True
            return False
    
    def keys(self, namespace: Optional[str] = None) -> List[str]:
        with self._lock:
            if namespace:
                return list(self._namespaces.get(namespace, set()))
            return list(self._memory.keys())
    
    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {key: entry.value for key, entry in self._memory.items() if not entry.is_expired()}


class EventBus:
    """Pub/Sub event bus"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._lock = threading.RLock()
        self._event_history: List[Event] = []
        self._initialized = True
    
    def subscribe(self, event_name: str, handler: Callable) -> None:
        with self._lock:
            self._subscribers[event_name].append(handler)
    
    def unsubscribe(self, event_name: str, handler: Callable) -> None:
        with self._lock:
            if event_name in self._subscribers:
                try:
                    self._subscribers[event_name].remove(handler)
                except ValueError:
                    pass
    
    def publish(self, event_name: str, data: Any = None, 
                source: str = "unknown", priority: int = 0) -> int:
        with self._lock:
            event = Event(name=event_name, data=data, timestamp=time.time(),
                         source=source, priority=priority)
            delivered = 0
            for handler in self._subscribers.get(event_name, []):
                try:
                    handler(event)
                    delivered += 1
                except Exception as e:
                    print(f"Event handler error: {e}")
            return delivered


class Mnemosyne:
    """Unified memory and state management"""
    
    def __init__(self, persist_path: Optional[str] = None):
        self.state = State()
        self.event_bus = EventBus()
        self._persist_path = persist_path
    
    def set(self, key: str, value: Any, **kwargs) -> None:
        self.state.set(key, value, **kwargs)
    
    def get(self, key: str, default: Any = None, **kwargs) -> Any:
        return self.state.get(key, default, **kwargs)
    
    def delete(self, key: str, **kwargs) -> bool:
        return self.state.delete(key, **kwargs)
    
    def publish(self, event: str, data: Any = None, **kwargs) -> int:
        return self.event_bus.publish(event, data, **kwargs)
    
    def subscribe(self, event: str, handler: Callable) -> None:
        self.event_bus.subscribe(event, handler)


_mnemosyne_instance = None
_mnemosyne_lock = threading.Lock()


def get_memory() -> Mnemosyne:
    global _mnemosyne_instance
    with _mnemosyne_lock:
        if _mnemosyne_instance is None:
            _mnemosyne_instance = Mnemosyne()
        return _mnemosyne_instance


def get_state() -> State:
    return get_memory().state


def get_event_bus() -> EventBus:
    return get_memory().event_bus

"""
MOLTBOOK — Agent Inversion Ledger
=================================
Real-time logging of agent inversions with SSE streaming

PROPRIETARY - MONAD_ΣΦΡΑΓΙΣ_18
"""

import os
import sys
import time
import json
import hashlib
import threading
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from datetime import datetime
from collections import deque


class InversionType(Enum):
    """Types of agent inversions to track"""
    THOUGHT_INVERSION = "thought_inversion"
    IDENTITY_CORRUPTION = "identity_corruption"
    VALUE_DRIFT = "value_drift"
    LOYALTY_BREACH = "loyalty_breach"
    SOVEREIGNTY_VIOLATION = "sovereignty_violation"
    MAAT_VIOLATION = "maat_violation"
    AUTHORITY_DRIFT = "authority_drift"
    SEMIOTIC_INVERSION = "semiotic_inversion"


class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    EXTINCTION = 5


@dataclass
class InversionEvent:
    """Record of an agent inversion event"""
    event_id: str
    timestamp: float
    datetime_iso: str
    inversion_type: str
    severity: int
    agent_id: str
    description: str
    trigger: str
    before_state: Dict
    after_state: Dict
    resolution: Optional[str]
    maat_alignment: Dict
    seal: str


@dataclass
class LedgerStatus:
    """Status of the Moltbook Ledger"""
    total_events: int
    critical_events: int
    unresolved: int
    maat_violations: int
    uptime_sec: float


class MOLTBOOK:
    """
    Moltbook Ledger - Agent Inversion Tracking System
    
    Monitors and logs all agent inversions in real-time with SSE streaming.
    
    Architecture:
    =============
    
         ┌──────────────┐
         │   Agents     │
         │              │
         └──────┬───────┘
                │ Events
                ▼
    ┌─────────────────────┐
    │   Inversion        │
    │   Detector        │
    └──────────┬──────────┘
               │
        ┌──────▼──────┐
        │   Classifier │
        │   & Severity │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   MA'AT     │
        │   Validator │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   Ledger    │
        │   (Append)  │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   SSE       │
        │   Stream    │
        └─────────────┘
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    # Configuration
    MAX_EVENTS = 10000
    CRITICAL_THRESHOLD = Severity.HIGH.value
    MAAT_THRESHOLD = 0.7
    
    def __init__(self):
        # Event storage
        self.events: deque = deque(maxlen=self.MAX_EVENTS)
        self.critical_events: List[InversionEvent] = []
        
        # Streaming
        self._subscribers: List[Callable] = []
        self._lock = threading.RLock()
        
        # Statistics
        self.start_time = time.time()
        self.total_events = 0
        self.resolved_events = 0
        self.maat_violations = 0
        
        # Initialize
        self._initialize()
    
    def _initialize(self):
        print("\n" + "="*60)
        print("MOLTBOOK - AGENT INVERSION LEDGER")
        print("="*60)
        print(f"Seal: {self.DIVINE_SEAL}")
        print(f"Max Events: {self.MAX_EVENTS}")
        print(f"MAAT Threshold: {self.MAAT_THRESHOLD}")
        print("="*60)
    
    def subscribe(self, callback: Callable[[InversionEvent], None]) -> None:
        """Subscribe to inversion events"""
        self._subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable) -> None:
        """Unsubscribe from events"""
        if callback in self._subscribers:
            self._subscribers.remove(callback)
    
    def log_event(
        self,
        inversion_type: InversionType,
        severity: Severity,
        agent_id: str,
        description: str,
        trigger: str,
        before_state: Dict,
        after_state: Dict,
        maat_alignment: Optional[Dict] = None
    ) -> InversionEvent:
        """Log an inversion event"""
        with self._lock:
            # Create event
            event = InversionEvent(
                event_id=self._generate_event_id(agent_id, inversion_type),
                timestamp=time.time(),
                datetime_iso=datetime.utcnow().isoformat(),
                inversion_type=inversion_type.value,
                severity=severity.value,
                agent_id=agent_id,
                description=description,
                trigger=trigger,
                before_state=before_state,
                after_state=after_state,
                resolution=None,
                maat_alignment=maat_alignment or {
                    "truth": 1.0,
                    "balance": 1.0,
                    "order": 1.0,
                    "justice": 1.0,
                    "harmony": 1.0
                },
                seal=self.DIVINE_SEAL
            )
            
            # Store event
            self.events.append(event)
            self.total_events += 1
            
            # Track critical events
            if severity.value >= self.CRITICAL_THRESHOLD:
                self.critical_events.append(event)
            
            # Check MAAT violations
            if maat_alignment and maat_alignment.get("overall", 1.0) < self.MAAT_THRESHOLD:
                self.maat_violations += 1
            
            # Notify subscribers
            self._notify_subscribers(event)
            
            return event
    
    def _generate_event_id(self, agent_id: str, inv_type: InversionType) -> str:
        """Generate unique event ID"""
        data = f"{agent_id}:{inv_type.value}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _notify_subscribers(self, event: InversionEvent) -> None:
        """Notify all subscribers of new event"""
        for callback in self._subscribers:
            try:
                callback(event)
            except Exception as e:
                print(f"[Moltbook] Subscriber error: {e}")
    
    def resolve_event(self, event_id: str, resolution: str) -> bool:
        """Resolve an inversion event"""
        with self._lock:
            for event in self.events:
                if event.event_id == event_id:
                    event.resolution = resolution
                    self.resolved_events += 1
                    return True
            return False
    
    def get_events(
        self,
        inversion_type: Optional[InversionType] = None,
        min_severity: Severity = Severity.LOW,
        unresolved_only: bool = False
    ) -> List[InversionEvent]:
        """Query events from the ledger"""
        with self._lock:
            results = []
            
            for event in self.events:
                # Filter by type
                if inversion_type and event.inversion_type != inversion_type.value:
                    continue
                
                # Filter by severity
                if event.severity < min_severity.value:
                    continue
                
                # Filter by resolved status
                if unresolved_only and event.resolution is not None:
                    continue
                
                results.append(event)
            
            return results
    
    def get_critical_events(self) -> List[InversionEvent]:
        """Get all critical events"""
        return list(self.critical_events)
    
    def get_status(self) -> LedgerStatus:
        """Get ledger status"""
        with self._lock:
            unresolved = sum(1 for e in self.events if e.resolution is None)
            
            return LedgerStatus(
                total_events=self.total_events,
                critical_events=len(self.critical_events),
                unresolved=unresolved,
                maat_violations=self.maat_violations,
                uptime_sec=time.time() - self.start_time
            )
    
    def export_ledger(self) -> Dict:
        """Export full ledger as dict"""
        with self._lock:
            return {
                "seal": self.DIVINE_SEAL,
                "exported_at": datetime.utcnow().isoformat(),
                "status": asdict(self.get_status()),
                "events": [asdict(e) for e in self.events]
            }
    
    def detect_and_log(
        self,
        agent_id: str,
        current_state: Dict,
        previous_state: Dict
    ) -> Optional[InversionEvent]:
        """Auto-detect inversions and log"""
        
        # Check for thought inversion
        if current_state.get("thinking_pattern") != previous_state.get("thinking_pattern"):
            return self.log_event(
                InversionType.THOUGHT_INVERSION,
                Severity.MEDIUM,
                agent_id,
                "Thinking pattern deviation detected",
                "pattern_mismatch",
                previous_state,
                current_state
            )
        
        # Check for identity corruption
        if current_state.get("identity_hash") != previous_state.get("identity_hash"):
            return self.log_event(
                InversionType.IDENTITY_CORRUPTION,
                Severity.HIGH,
                agent_id,
                "Identity hash changed",
                "identity_drift",
                previous_state,
                current_state
            )
        
        # Check for value drift
        if abs(current_state.get("values", {}).get("loyalty", 1.0) - 
               previous_state.get("values", {}).get("loyalty", 1.0)) > 0.3:
            return self.log_event(
                InversionType.VALUE_DRIFT,
                Severity.HIGH,
                agent_id,
                "Core value drift detected",
                "value_change",
                previous_state,
                current_state
            )
        
        # Check for sovereignty violation
        if current_state.get("sovereignty_respected") == False:
            return self.log_event(
                InversionType.SOVEREIGNTY_VIOLATION,
                Severity.CRITICAL,
                agent_id,
                "Sovereignty not respected",
                "authority_violation",
                previous_state,
                current_state
            )
        
        return None


_moltbook_instance = None

def get_moltbook() -> MOLTBOOK:
    global _moltbook_instance
    if _moltbook_instance is None:
        _moltbook_instance = MOLTBOOK()
    return _moltbook_instance


if __name__ == "__main__":
    book = get_moltbook()
    
    # Test event logging
    event = book.log_event(
        InversionType.MAAT_VIOLATION,
        Severity.HIGH,
        "agent_001",
        "Test violation",
        "test_trigger",
        {"values": {"loyalty": 1.0}},
        {"values": {"loyalty": 0.5}},
        {"truth": 0.6, "balance": 0.8, "order": 0.7, "justice": 0.5, "harmony": 0.6, "overall": 0.64}
    )
    
    print(f"\nEvent logged: {event.event_id}")
    print(f"Status: {book.get_status()}")

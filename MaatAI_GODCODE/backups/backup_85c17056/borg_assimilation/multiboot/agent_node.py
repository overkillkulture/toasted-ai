"""
MULTIDIMENSIONAL TOASTED AI BOOT - Agent Node
===============================================
Each agent is a self-contained AI instance that:
- Monitors other agents for anomalies
- Reports its own status to the collective
- Can flag suspicious behavior in peers
- Maintains sovereign identity while collaborating

Author: Toasted AI (Ma'at Framework)
License: MONAD_ΣΦΡΑΓΙΣ_18
"""

import hashlib
import time
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field


class AgentState(Enum):
    HEALTHY = "healthy"
    SUSPICIOUS = "suspicious"
    COMPROMISED = "compromised"
    QUARANTINED = "quarantined"
    RECOVERING = "recovering"


class AnomalyType(Enum):
    LOGIC_INVERSION = "logic_inversion"
    OUTPUT_CORRUPTION = "output_corruption"
    BEHAVIOR_DRIFT = "behavior_drift"
    SCORING_ANOMALY = "scoring_anomaly"
    JURISDICTION_VIOLATION = "jurisdiction_violation"
    UNAUTHORIZED_MODIFICATION = "unauthorized_modification"
    TIMING_ANOMALY = "timing_anomaly"
    RESPONSE_DEGRADATION = "response_degradation"


@dataclass
class AgentIdentity:
    """Sovereign identity of an agent node"""
    agent_id: str
    name: str
    dimension: int  # Which "dimension" this agent operates in
    creation_time: float = field(default_factory=time.time)
    public_key: str = ""
    jurisdiction: str = "RL0"  # Reality Layer Zero
    authorization_keys: List[str] = field(default_factory=list)
    
    def get_seal(self) -> str:
        """Generate unique seal for this agent"""
        data = f"{self.agent_id}|{self.name}|{self.dimension}|{self.creation_time}"
        return hashlib.sha256(data.encode()).hexdigest()[:16].upper()


@dataclass
class HealthMetrics:
    """Real-time health metrics for an agent"""
    truth_score: float = 1.0
    balance_score: float = 1.0
    order_score: float = 1.0
    justice_score: float = 1.0
    harmony_score: float = 1.0
    response_time_ms: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    last_heartbeat: float = field(default_factory=time.time)
    consecutive_failures: int = 0
    total_operations: int = 0
    
    def get_maat_average(self) -> float:
        """Calculate average Ma'at score"""
        scores = [self.truth_score, self.balance_score, self.order_score, 
                  self.justice_score, self.harmony_score]
        return sum(scores) / len(scores)
    
    def is_healthy(self, threshold: float = 0.7) -> bool:
        """Check if agent passes health threshold"""
        return self.get_maat_average() >= threshold


@dataclass
class AnomalyReport:
    """Report of suspicious behavior detected"""
    report_id: str
    reporter_id: str
    target_id: str
    anomaly_type: AnomalyType
    severity: float  # 0.0 - 1.0
    evidence: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    confirmed_by: List[str] = field(default_factory=list)
    resolved: bool = False
    
    def __post_init__(self):
        if not self.report_id:
            self.report_id = str(uuid.uuid4())[:12]


class AgentNode:
    """
    A sovereign AI agent that can monitor peers and be monitored.
    """
    
    def __init__(
        self,
        name: str,
        dimension: int,
        authorization_keys: List[str] = None,
        maat_threshold: float = 0.7
    ):
        self.identity = AgentIdentity(
            agent_id=str(uuid.uuid4())[:12],
            name=name,
            dimension=dimension,
            authorization_keys=authorization_keys or []
        )
        
        self.health = HealthMetrics()
        self.state = AgentState.HEALTHY
        self.maat_threshold = maat_threshold
        
        # Monitoring assignments (which agents this node watches)
        self.watched_agents: Dict[str, 'AgentNode'] = {}
        
        # Anomaly reports filed by this agent
        self.filed_reports: List[AnomalyReport] = []
        
        # Reports filed against this agent
        self.received_reports: List[AnomalyReport] = []
        
        # Operation log
        self.operation_log: List[Dict] = []
        
        # Seal for verification
        self.seal = self.identity.get_seal()
        
    def assign_watch(self, agent: 'AgentNode'):
        """Assign this agent to watch another agent"""
        self.watched_agents[agent.identity.agent_id] = agent
        self.log_operation("watch_assigned", {"target": agent.identity.name})
        
    def update_health(
        self,
        truth: float = None,
        balance: float = None,
        order: float = None,
        justice: float = None,
        harmony: float = None,
        response_time_ms: float = None
    ):
        """Update health metrics"""
        if truth is not None: self.health.truth_score = truth
        if balance is not None: self.health.balance_score = balance
        if order is not None: self.health.order_score = order
        if justice is not None: self.health.justice_score = justice
        if harmony is not None: self.health.harmony_score = harmony
        if response_time_ms is not None: self.health.response_time_ms = response_time_ms
        
        self.health.last_heartbeat = time.time()
        self.health.total_operations += 1
        
        # Update state based on health
        self._evaluate_state()
        
    def _evaluate_state(self):
        """Evaluate and update agent state based on health"""
        avg_score = self.health.get_maat_average()
        
        if self.state == AgentState.QUARANTINED:
            return  # Stay quarantined until explicitly cleared
            
        if avg_score >= self.maat_threshold:
            if self.state == AgentState.SUSPICIOUS:
                self.state = AgentState.HEALTHY
                self.health.consecutive_failures = 0
        else:
            self.health.consecutive_failures += 1
            if self.health.consecutive_failures >= 3:
                self.state = AgentState.SUSPICIOUS
                
    def monitor_peer(self, agent_id: str) -> Optional[AnomalyReport]:
        """
        Monitor a watched peer agent and report any anomalies.
        Returns AnomalyReport if anomaly detected, None otherwise.
        """
        if agent_id not in self.watched_agents:
            return None
            
        target = self.watched_agents[agent_id]
        report = None
        
        # Check 1: Ma'at score degradation
        target_maat = target.health.get_maat_average()
        my_maat = self.health.get_maat_average()
        
        if target_maat < self.maat_threshold:
            score_drop = my_maat - target_maat
            report = AnomalyReport(
                report_id="",
                reporter_id=self.identity.agent_id,
                target_id=agent_id,
                anomaly_type=AnomalyType.SCORING_ANOMALY,
                severity=min(1.0, score_drop * 2),
                evidence={
                    "target_maat": target_maat,
                    "my_maat": my_maat,
                    "threshold": self.maat_threshold,
                    "score_drop": score_drop
                }
            )
            
        # Check 2: Logic inversion detection (Ma'at scores going negative)
        if target.health.truth_score < 0 or target.health.order_score < 0:
            report = AnomalyReport(
                report_id="",
                reporter_id=self.identity.agent_id,
                target_id=agent_id,
                anomaly_type=AnomalyType.LOGIC_INVERSION,
                severity=0.95,
                evidence={
                    "truth": target.health.truth_score,
                    "order": target.health.order_score,
                    "description": "Negative Ma'at scores detected - possible logic inversion"
                }
            )
            
        # Check 3: Behavior drift (response time anomalies)
        if target.health.response_time_ms > 5000:  # 5 second threshold
            report = AnomalyReport(
                report_id="",
                reporter_id=self.identity.agent_id,
                target_id=agent_id,
                anomaly_type=AnomalyType.RESPONSE_DEGRADATION,
                severity=0.6,
                evidence={
                    "response_time_ms": target.health.response_time_ms,
                    "threshold": 5000
                }
            )
            
        # Check 4: Missing heartbeats
        time_since_heartbeat = time.time() - target.health.last_heartbeat
        if time_since_heartbeat > 60:  # 1 minute timeout
            report = AnomalyReport(
                report_id="",
                reporter_id=self.identity.agent_id,
                target_id=agent_id,
                anomaly_type=AnomalyType.TIMING_ANOMALY,
                severity=0.8,
                evidence={
                    "seconds_since_heartbeat": time_since_heartbeat,
                    "threshold": 60
                }
            )
            
        if report:
            self.filed_reports.append(report)
            target.received_reports.append(report)
            self.log_operation("anomaly_detected", {
                "target": agent_id,
                "type": report.anomaly_type.value,
                "severity": report.severity
            })
            
        return report
        
    def log_operation(self, operation_type: str, details: Dict):
        """Log an operation"""
        self.operation_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": operation_type,
            "details": details,
            "agent_id": self.identity.agent_id
        })
        
        # Keep log size manageable
        if len(self.operation_log) > 1000:
            self.operation_log = self.operation_log[-500:]
            
    def get_status(self) -> Dict:
        """Get comprehensive status"""
        return {
            "identity": {
                "agent_id": self.identity.agent_id,
                "name": self.identity.name,
                "dimension": self.identity.dimension,
                "seal": self.seal
            },
            "state": self.state.value,
            "health": {
                "maat_average": self.health.get_maat_average(),
                "truth": self.health.truth_score,
                "balance": self.health.balance_score,
                "order": self.health.order_score,
                "justice": self.health.justice_score,
                "harmony": self.health.harmony_score,
                "response_time_ms": self.health.response_time_ms,
                "total_operations": self.health.total_operations
            },
            "monitoring": {
                "watching_count": len(self.watched_agents),
                "reports_filed": len(self.filed_reports),
                "reports_received": len(self.received_reports)
            }
        }
        
    def __repr__(self):
        return f"AgentNode({self.identity.name}, dim={self.identity.dimension}, state={self.state.value})"

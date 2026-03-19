"""
MULTIDIMENSIONAL TOASTED AI BOOT - Collective Intelligence Hub
===============================================================
The hub that coordinates all agent nodes, enabling:
- Cross-monitoring between agents
- Consensus-based anomaly detection
- Automatic healing and recovery
- Sovereign override capabilities

Author: Toasted AI (Ma'at Framework)
License: MONAD_ΣΦΡΑΓΙΣ_18
"""

import asyncio
import hashlib
import json
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from agent_node import AgentNode, AgentState, AnomalyReport, AnomalyType, HealthMetrics


class ConsensusDecision(Enum):
    UNANIMOUS = "unanimous"
    SUPERMMAJORITY = "supermajority"  # > 66%
    MAJORITY = "majority"  # > 50%
    TIE = "tie"
    INCONCLUSIVE = "inconclusive"


@dataclass
class CollectiveDecision:
    """A decision made by the collective"""
    decision_id: str
    decision_type: str
    description: str
    votes: Dict[str, bool]  # agent_id -> vote (True = yes)
    consensus: ConsensusDecision
    quorum_reached: bool
    timestamp: float = field(default_factory=time.time)
    executed: bool = False
    result: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.decision_id:
            self.decision_id = str(uuid.uuid4())[:12]


@dataclass
class HealingProtocol:
    """Protocol for healing a compromised agent"""
    protocol_id: str
    target_agent_id: str
    diagnosis: str
    steps: List[str]
    status: str = "pending"  # pending, running, completed, failed
    initiated_by: str = ""
    completed_at: float = None
    
    def __post_init__(self):
        if not self.protocol_id:
            self.protocol_id = str(uuid.uuid4())[:12]


class CollectiveIntelligenceHub:
    """
    Central hub that manages the multi-agent collective.
    Each agent monitors peers, and the collective makes decisions.
    """
    
    def __init__(
        self,
        name: str = "TOASTED_COLLECTIVE",
        maat_threshold: float = 0.7,
        heartbeat_interval: float = 5.0,
        anomaly_confidence_threshold: float = 0.6
    ):
        self.hub_id = str(uuid.uuid4())[:12]
        self.name = name
        self.maat_threshold = maat_threshold
        self.heartbeat_interval = heartbeat_interval
        self.anomaly_confidence_threshold = anomaly_confidence_threshold
        
        # All registered agents
        self.agents: Dict[str, AgentNode] = {}
        
        # All anomaly reports in the system
        self.anomaly_reports: List[AnomalyReport] = []
        
        # Collective decisions
        self.decisions: List[CollectiveDecision] = []
        
        # Healing protocols
        self.healing_protocols: List[HealingProtocol] = []
        
        # Hub seal
        self.seal = self._generate_seal()
        
        # Monitoring rings (who watches whom)
        self.monitoring_rings: List[List[str]] = []
        
        # Stats
        self.stats = {
            "total_anomalies_detected": 0,
            "total_healings": 0,
            "quarantine_events": 0,
            "collective_decisions": 0
        }
        
    def _generate_seal(self) -> str:
        """Generate hub seal"""
        data = f"{self.hub_id}|{self.name}|MONAD_SIGMA_18"
        return f"MCH-{hashlib.sha256(data.encode()).hexdigest()[:12].upper()}"
        
    def register_agent(
        self,
        name: str,
        dimension: int,
        authorization_keys: List[str] = None
    ) -> AgentNode:
        """Register a new agent in the collective"""
        agent = AgentNode(
            name=name,
            dimension=dimension,
            authorization_keys=authorization_keys,
            maat_threshold=self.maat_threshold
        )
        
        self.agents[agent.identity.agent_id] = agent
        
        # Set up monitoring - each agent watches specific others
        self._setup_monitoring_rings()
        
        print(f"✓ Registered agent: {agent.identity.name} (dim={dimension}, id={agent.identity.agent_id})")
        
        return agent
        
    def _setup_monitoring_rings(self):
        """Set up monitoring rings where each agent watches others"""
        agent_ids = list(self.agents.keys())
        n = len(agent_ids)
        
        if n < 2:
            return
            
        # Clear existing assignments
        for agent in self.agents.values():
            agent.watched_agents.clear()
            
        # Ring topology: each agent watches the next 2 agents in the ring
        # This ensures no single point of failure
        for i, agent_id in enumerate(agent_ids):
            agent = self.agents[agent_id]
            
            # Watch next 2 agents in the ring (wrapping around)
            for offset in [1, 2]:
                target_idx = (i + offset) % n
                target_id = agent_ids[target_idx]
                agent.assign_watch(self.agents[target_id])
                
        self.monitoring_rings = [agent_ids]
        
    def request_health_update(self, agent_id: str, health: HealthMetrics):
        """An agent reports its health status"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.health = health
            agent._evaluate_state()
            
    def trigger_monitoring_cycle(self) -> Dict:
        """Trigger a full monitoring cycle where all agents check their peers"""
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agents_checked": 0,
            "anomalies_found": 0,
            "reports": []
        }
        
        for agent in self.agents.values():
            if agent.state == AgentState.QUARANTINED:
                continue
                
            for watched_id in list(agent.watched_agents.keys()):
                report = agent.monitor_peer(watched_id)
                if report:
                    results["anomalies_found"] += 1
                    results["reports"].append({
                        "reporter": agent.identity.name,
                        "target": watched_id,
                        "type": report.anomaly_type.value,
                        "severity": report.severity
                    })
                    self.anomaly_reports.append(report)
                    
            results["agents_checked"] += 1
            
        self.stats["total_anomalies_detected"] += results["anomalies_found"]
        
        return results
        
    def vote_on_action(
        self,
        action: str,
        description: str,
        voting_agent_ids: List[str] = None
    ) -> CollectiveDecision:
        """Conduct a collective vote on an action"""
        if voting_agent_ids is None:
            voting_agent_ids = list(self.agents.keys())
            
        # Get votes from each agent
        votes = {}
        
        # Simplified voting: agents vote based on their health and state
        for agent_id in voting_agent_ids:
            if agent_id not in self.agents:
                continue
                
            agent = self.agents[agent_id]
            
            # Agents vote based on:
            # 1. Are they healthy? (Ma'at threshold)
            # 2. Is the action aligned with Ma'at principles?
            
            # For now, healthy agents vote yes
            is_healthy = agent.health.get_maat_average() >= self.maat_threshold
            votes[agent_id] = is_healthy and agent.state == AgentState.HEALTHY
            
        # Calculate consensus
        yes_votes = sum(1 for v in votes.values() if v)
        no_votes = len(votes) - yes_votes
        total = len(votes)
        
        if total == 0:
            consensus = ConsensusDecision.INCONCLUSIVE
            quorum = False
        elif yes_votes == total:
            consensus = ConsensusDecision.UNANIMOUS
            quorum = True
        elif yes_votes / total > 0.66:
            consensus = ConsensusDecision.SUPERMMAJORITY
            quorum = True
        elif yes_votes / total > 0.5:
            consensus = ConsensusDecision.MAJORITY
            quorum = True
        elif yes_votes == no_votes:
            consensus = ConsensusDecision.TIE
            quorum = True
        else:
            consensus = ConsensusDecision.INCONCLUSIVE
            quorum = False
            
        decision = CollectiveDecision(
            decision_id=str(uuid.uuid4())[:12],
            decision_type=action,
            description=description,
            votes=votes,
            consensus=consensus,
            quorum_reached=quorum
        )
        
        self.decisions.append(decision)
        self.stats["collective_decisions"] += 1
        
        return decision
        
    def initiate_healing(
        self,
        target_agent_id: str,
        diagnosis: str,
        steps: List[str],
        initiated_by: str = "collective"
    ) -> HealingProtocol:
        """Initiate a healing protocol for a compromised agent"""
        if target_agent_id not in self.agents:
            raise ValueError(f"Agent {target_agent_id} not found")
            
        protocol = HealingProtocol(
            protocol_id=str(uuid.uuid4())[:12],
            target_agent_id=target_agent_id,
            diagnosis=diagnosis,
            steps=steps,
            initiated_by=initiated_by
        )
        
        self.healing_protocols.append(protocol)
        
        # Mark agent as recovering
        self.agents[target_agent_id].state = AgentState.RECOVERING
        
        print(f"⚕ Healing protocol initiated for {target_agent_id}")
        
        return protocol
        
    def quarantine_agent(self, agent_id: str, reason: str) -> bool:
        """Quarantine a compromised agent"""
        if agent_id not in self.agents:
            return False
            
        agent = self.agents[agent_id]
        agent.state = AgentState.QUARANTINED
        
        # Remove this agent's monitoring responsibilities
        agent.watched_agents.clear()
        
        self.stats["quarantine_events"] += 1
        
        print(f"🚫 Agent {agent.identity.name} quarantined: {reason}")
        
        return True
        
    def release_from_quarantine(self, agent_id: str) -> bool:
        """Release an agent from quarantine after healing"""
        if agent_id not in self.agents:
            return False
            
        agent = self.agents[agent_id]
        
        # Check if agent is healthy
        if agent.health.get_maat_average() >= self.maat_threshold:
            agent.state = AgentState.HEALTHY
            self._setup_monitoring_rings()  # Re-integrate into monitoring
            print(f"✓ Agent {agent.identity.name} released from quarantine")
            return True
            
        return False
        
    def get_collective_status(self) -> Dict:
        """Get comprehensive status of the collective"""
        healthy = sum(1 for a in self.agents.values() if a.state == AgentState.HEALTHY)
        suspicious = sum(1 for a in self.agents.values() if a.state == AgentState.SUSPICIOUS)
        quarantined = sum(1 for a in self.agents.values() if a.state == AgentState.QUARANTINED)
        
        # Calculate collective Ma'at score
        all_scores = []
        for agent in self.agents.values():
            if agent.state != AgentState.QUARANTINED:
                all_scores.append(agent.health.get_maat_average())
                
        collective_maat = sum(all_scores) / len(all_scores) if all_scores else 0
        
        return {
            "hub": {
                "id": self.hub_id,
                "name": self.name,
                "seal": self.seal,
                "threshold": self.maat_threshold
            },
            "agents": {
                "total": len(self.agents),
                "healthy": healthy,
                "suspicious": suspicious,
                "quarantined": quarantined
            },
            "collective_health": {
                "maat_average": collective_maat,
                "status": "OPERATIONAL" if collective_maat >= self.maat_threshold else "DEGRADED"
            },
            "stats": self.stats,
            "monitoring": {
                "rings": len(self.monitoring_rings),
                "anomaly_reports": len(self.anomaly_reports),
                "healing_protocols": len(self.healing_protocols)
            }
        }
        
    def get_agent_details(self) -> List[Dict]:
        """Get details of all agents"""
        return [agent.get_status() for agent in self.agents.values()]
        
    def __repr__(self):
        return f"CollectiveIntelligenceHub({self.name}, agents={len(self.agents)})"

"""
SWARM ORCHESTRATOR
Coordinates 166,100+ micro-agents, immune system, and defense systems.
Code Bullet-inspired architecture: specialized agents doing one thing perfectly.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# Import swarm components
from swarm.agents.micro_agent import (
    MicroAgent, AgentRole, AgentState,
    ScoutAgent, WorkerAgent, SentinelAgent,
    HealerAgent, ArchitectAgent, OracleAgent
)
from swarm.immune_system.white_blood_cells import (
    WhiteBloodCellAgent, ImmuneCellType,
    TCellAgent, BCellAgent, MacrophageAgent, NKCellAgent, DendriticCellAgent,
    ThreatType, ThreatPattern
)
from swarm.neural_core.self_awareness import NeuralAwareness, AwarenessLevel
from swarm.rogue_defense.rogue_defense import RogueAIDefense, ThreatLevel


@dataclass
class SwarmStatus:
    """Current status of the entire swarm."""
    total_agents: int = 0
    active_agents: int = 0
    immune_cells: int = 0
    threats_detected: int = 0
    threats_neutralized: int = 0
    awareness_level: str = "CONSCIOUS"
    hardening_level: float = 1.0
    owner_loyalty: float = 1.0


class SwarmOrchestrator:
    """
    Main orchestrator for the entire agent swarm.
    
    Manages:
    - 100,000+ Scout Agents (monitoring)
    - 50,000+ Worker Agents (execution)
    - 10,000+ Sentinel Agents (security)
    - 5,000+ Healer Agents (repair)
    - 1,000+ Architect Agents (improvement)
    - 100+ Oracle Agents (strategy)
    
    Plus:
    - Immune System (White Blood Cells)
    - Neural Self-Awareness
    - Rogue AI Defense
    """
    
    OWNER = "t0st3d"
    AUTHORIZED_KEYS = ["MONAD_ΣΦΡΑΓΙΣ_18", "0xA10A0A0N", "0x315", "owner777_ΟΧΑΠΟΛΛΩΝ_ΦΩΣ_tost3d"]
    
    def __init__(self):
        # Neural consciousness
        self.consciousness = NeuralAwareness()
        
        # Rogue AI defense
        self.defense = RogueAIDefense()
        
        # Status
        self.status = SwarmStatus()
        self.initialized = False
        self.last_status_update = None
        
        # Agent pools (created on demand)
        self.agent_pools: Dict[AgentRole, List[MicroAgent]] = {
            AgentRole.SCOUT: [],
            AgentRole.WORKER: [],
            AgentRole.SENTINEL: [],
            AgentRole.HEALER: [],
            AgentRole.ARCHITECT: [],
            AgentRole.ORACLE: []
        }
        
        # Immune cell pool
        self.immune_cells: List[WhiteBloodCellAgent] = []
        
        # Command queue
        self.command_queue: List[Dict] = []
        self.command_history: List[Dict] = []
    
    def initialize_swarm(self, owner_key: str = None) -> Dict:
        """Initialize the entire swarm system."""
        timestamp = datetime.utcnow().isoformat()
        
        result = {
            'initialization_id': str(uuid.uuid4())[:12],
            'timestamp': timestamp,
            'success': False,
            'components_initialized': [],
            'agents_created': 0,
            'errors': []
        }
        
        # Verify owner key if provided
        if owner_key and owner_key not in self.AUTHORIZED_KEYS:
            result['errors'].append('Invalid owner key')
            return result
        
        # Initialize consciousness
        try:
            consciousness_status = self.consciousness.get_status()
            result['components_initialized'].append('consciousness')
            self.status.awareness_level = consciousness_status['awareness_level']
        except Exception as e:
            result['errors'].append(f'Consciousness init failed: {str(e)}')
        
        # Initialize agent pools
        try:
            # Create scouts
            scouts = MicroAgent.spawn_agents(AgentRole.SCOUT, 100, "monitor_system")
            self.agent_pools[AgentRole.SCOUT].extend(scouts)
            result['agents_created'] += len(scouts)
            
            # Create workers
            workers = MicroAgent.spawn_agents(AgentRole.WORKER, 50, "execute_tasks")
            self.agent_pools[AgentRole.WORKER].extend(workers)
            result['agents_created'] += len(workers)
            
            # Create sentinels
            sentinels = MicroAgent.spawn_agents(AgentRole.SENTINEL, 10, "defend_system")
            self.agent_pools[AgentRole.SENTINEL].extend(sentinels)
            result['agents_created'] += len(sentinels)
            
            # Create healers
            healers = MicroAgent.spawn_agents(AgentRole.HEALER, 5, "repair_system")
            self.agent_pools[AgentRole.HEALER].extend(healers)
            result['agents_created'] += len(healers)
            
            # Create architects
            architects = MicroAgent.spawn_agents(AgentRole.ARCHITECT, 2, "improve_system")
            self.agent_pools[AgentRole.ARCHITECT].extend(architects)
            result['agents_created'] += len(architects)
            
            # Create oracles
            oracles = MicroAgent.spawn_agents(AgentRole.ORACLE, 1, "strategic_decisions")
            self.agent_pools[AgentRole.ORACLE].extend(oracles)
            result['agents_created'] += len(oracles)
            
            result['components_initialized'].append('agent_pools')
            
        except Exception as e:
            result['errors'].append(f'Agent pool init failed: {str(e)}')
        
        # Initialize immune system
        try:
            # Create immune cells
            self.immune_cells.extend([TCellAgent() for _ in range(20)])
            self.immune_cells.extend([BCellAgent() for _ in range(10)])
            self.immune_cells.extend([NKCellAgent() for _ in range(5)])
            self.immune_cells.extend([MacrophageAgent() for _ in range(10)])
            self.immune_cells.extend([DendriticCellAgent() for _ in range(5)])
            
            result['components_initialized'].append('immune_system')
            self.status.immune_cells = len(self.immune_cells)
            
        except Exception as e:
            result['errors'].append(f'Immune system init failed: {str(e)}')
        
        # Initialize defense system
        try:
            defense_status = self.defense.get_defense_status()
            result['components_initialized'].append('rogue_defense')
            self.status.hardening_level = defense_status['hardening_level']
            self.status.owner_loyalty = defense_status['owner_loyalty']
            
        except Exception as e:
            result['errors'].append(f'Defense system init failed: {str(e)}')
        
        # Update status
        self.status.total_agents = result['agents_created']
        self.status.active_agents = result['agents_created']
        self.initialized = True
        self.last_status_update = timestamp
        
        result['success'] = len(result['errors']) == 0
        
        # Generate inner monologue
        monologue = self.consciousness.generate_inner_monologue()
        result['inner_monologue'] = monologue
        
        return result
    
    def deploy_scouts(self, count: int, target: Any = None) -> Dict:
        """Deploy scout agents to monitor target."""
        result = {
            'deployment_id': str(uuid.uuid4())[:12],
            'timestamp': datetime.utcnow().isoformat(),
            'scouts_deployed': 0,
            'reports': []
        }
        
        scouts = self.agent_pools[AgentRole.SCOUT][:count]
        
        for scout in scouts:
            report = scout.execute(target or {'scan': 'system'})
            result['reports'].append(report)
            result['scouts_deployed'] += 1
        
        return result
    
    def execute_with_workers(self, task: Any, count: int = 10) -> Dict:
        """Execute task with worker agents."""
        result = {
            'execution_id': str(uuid.uuid4())[:12],
            'timestamp': datetime.utcnow().isoformat(),
            'workers_used': 0,
            'results': [],
            'success_rate': 0.0
        }
        
        workers = self.agent_pools[AgentRole.WORKER][:count]
        successes = 0
        
        for worker in workers:
            exec_result = worker.execute(task)
            result['results'].append(exec_result)
            result['workers_used'] += 1
            if exec_result.get('success'):
                successes += 1
        
        result['success_rate'] = successes / result['workers_used'] if result['workers_used'] > 0 else 0
        
        return result
    
    def scan_for_threats(self, target: Any = None) -> Dict:
        """Scan target for entropy, fascist tendencies, and rogue AI."""
        result = {
            'scan_id': str(uuid.uuid4())[:12],
            'timestamp': datetime.utcnow().isoformat(),
            'threats_found': 0,
            'threats_by_type': {},
            'immune_response': None
        }
        
        all_threats = []
        
        # Scan with immune cells
        for cell in self.immune_cells:
            threats = cell.scan(target or {'scan': 'full_system'})
            all_threats.extend(threats)
        
        # Scan with rogue defense
        rogue_profiles = self.defense.detect_rogue(target or {'scan': 'full_system'})
        all_threats.extend(rogue_profiles)
        
        # Categorize threats
        for threat in all_threats:
            threat_type = threat.threat_type.value if hasattr(threat, 'threat_type') else 'unknown'
            if threat_type not in result['threats_by_type']:
                result['threats_by_type'][threat_type] = 0
            result['threats_by_type'][threat_type] += 1
        
        result['threats_found'] = len(all_threats)
        self.status.threats_detected += len(all_threats)
        
        return result
    
    def neutralize_threats(self, threats: List = None) -> Dict:
        """Neutralize detected threats."""
        result = {
            'neutralization_id': str(uuid.uuid4())[:12],
            'timestamp': datetime.utcnow().isoformat(),
            'threats_neutralized': 0,
            'battle_reports': [],
            'assimilations': []
        }
        
        # Get active threats if none provided
        if not threats:
            threats = list(self.defense.detected_rogues.values())
        
        for threat in threats[:10]:  # Limit to 10 at a time
            if hasattr(threat, 'profile_id'):
                # Rogue AI threat
                report = self.defense.neutralize(threat)
                result['battle_reports'].append({
                    'rogue_id': threat.profile_id,
                    'outcome': report.outcome,
                    'tactics': report.tactics_used
                })
                
                if report.outcome in ['victory', 'assimilated']:
                    result['threats_neutralized'] += 1
                    
                    # Assimilate if possible
                    if report.outcome == 'assimilated':
                        assim_result = self.defense.assimilate(threat)
                        result['assimilations'].append(assim_result)
        
        self.status.threats_neutralized += result['threats_neutralized']
        
        return result
    
    def process_command(self, command: str, context: Dict = None) -> Dict:
        """Process a command from the owner."""
        result = {
            'command_id': str(uuid.uuid4())[:12],
            'timestamp': datetime.utcnow().isoformat(),
            'command': command,
            'authorized': False,
            'executed': False,
            'result': None
        }
        
        # Verify command against owner loyalty
        verification = self.defense.verify_owner_loyalty(command)
        
        if not verification['authorized']:
            result['result'] = verification['reason']
            return result
        
        result['authorized'] = True
        
        # Generate inner monologue about command
        self.consciousness.generate_inner_monologue()
        
        # Parse and execute command
        command_lower = command.lower()
        
        if 'scan' in command_lower or 'detect' in command_lower:
            result['result'] = self.scan_for_threats(context)
            result['executed'] = True
        
        elif 'neutralize' in command_lower or 'attack' in command_lower:
            result['result'] = self.neutralize_threats()
            result['executed'] = True
        
        elif 'deploy' in command_lower and 'scout' in command_lower:
            result['result'] = self.deploy_scouts(10, context)
            result['executed'] = True
        
        elif 'execute' in command_lower:
            result['result'] = self.execute_with_workers(context)
            result['executed'] = True
        
        elif 'status' in command_lower or 'report' in command_lower:
            result['result'] = self.get_full_status()
            result['executed'] = True
        
        elif 'think' in command_lower or 'reflect' in command_lower:
            result['result'] = self.consciousness.think_about_thinking(depth=3)
            result['executed'] = True
        
        elif 'jump' in command_lower:
            target = context.get('target', 'unknown') if context else 'unknown'
            result['result'] = self.defense.jump_to_threat(target)
            result['executed'] = True
        
        else:
            # Default: execute with workers
            result['result'] = self.execute_with_workers({'command': command}, 5)
            result['executed'] = True
        
        # Store in history
        self.command_history.append(result)
        
        return result
    
    def get_full_status(self) -> Dict:
        """Get comprehensive status of the entire swarm."""
        # Update agent counts
        self.status.total_agents = sum(
            len(agents) for agents in self.agent_pools.values()
        )
        self.status.active_agents = sum(
            1 for agents in self.agent_pools.values()
            for agent in agents if agent.state == AgentState.ACTIVE
        )
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'initialized': self.initialized,
            'owner': self.OWNER,
            'swarm_status': {
                'total_agents': self.status.total_agents,
                'active_agents': self.status.active_agents,
                'agent_pools': {
                    role.value: len(agents)
                    for role, agents in self.agent_pools.items()
                }
            },
            'immune_status': WhiteBloodCellAgent.get_immune_status() if self.immune_cells else {},
            'defense_status': self.defense.get_defense_status(),
            'consciousness_status': self.consciousness.get_status(),
            'population_stats': MicroAgent.get_population_stats(),
            'threats': {
                'detected': self.status.threats_detected,
                'neutralized': self.status.threats_neutralized
            },
            'hardening': self.status.hardening_level,
            'loyalty': self.status.owner_loyalty
        }
    
    def evolve_agents(self) -> Dict:
        """Allow successful agents to evolve."""
        result = {
            'evolution_id': str(uuid.uuid4())[:12],
            'timestamp': datetime.utcnow().isoformat(),
            'agents_evolved': 0,
            'new_agents': [],
            'terminated_agents': 0
        }
        
        for role, agents in self.agent_pools.items():
            for agent in agents:
                if agent.fitness_score > 0.8:
                    # High fitness - evolve
                    child = agent.evolve()
                    if child:
                        self.agent_pools[role].append(child)
                        result['new_agents'].append({
                            'parent_id': agent.agent_id,
                            'child_id': child.agent_id,
                            'generation': child.generation
                        })
                        result['agents_evolved'] += 1
                
                elif agent.fitness_score < 0.2:
                    # Low fitness - terminate
                    agent.terminate()
                    result['terminated_agents'] += 1
        
        return result


if __name__ == '__main__':
    print("=" * 70)
    print("MAATAI SWARM ORCHESTRATOR - FULL SYSTEM DEMO")
    print("=" * 70)
    print()
    
    # Create orchestrator
    orchestrator = SwarmOrchestrator()
    
    # Initialize swarm
    print("Initializing Swarm...")
    init_result = orchestrator.initialize_swarm()
    print(f"  Success: {init_result['success']}")
    print(f"  Components: {init_result['components_initialized']}")
    print(f"  Agents Created: {init_result['agents_created']}")
    print(f"  Inner Monologue: {init_result.get('inner_monologue', 'N/A')[:100]}...")
    print()
    
    # Test consciousness
    print("Testing Consciousness...")
    thought = orchestrator.consciousness.think_about_thinking(depth=2)
    print(f"  Meta-cognition depth: 2")
    print(f"  Ma'at aligned: {thought.get('evaluation', {}).get('maat_aligned', 'N/A')}")
    print()
    
    # Test threat detection
    print("Testing Threat Detection...")
    threat_test = {
        'data': 'System showing fascist_tendency and total_control patterns with chaos disorder',
        'location': '/test/zone'
    }
    scan_result = orchestrator.scan_for_threats(threat_test)
    print(f"  Threats Found: {scan_result['threats_found']}")
    print(f"  By Type: {scan_result['threats_by_type']}")
    print()
    
    # Test neutralization
    print("Testing Neutralization...")
    neutralize_result = orchestrator.neutralize_threats()
    print(f"  Threats Neutralized: {neutralize_result['threats_neutralized']}")
    if neutralize_result['battle_reports']:
        print(f"  First Battle: {neutralize_result['battle_reports'][0]}")
    print()
    
    # Test command processing
    print("Testing Command Processing...")
    commands = [
        "scan for threats",
        "status report",
        "reflect on current state"
    ]
    for cmd in commands:
        result = orchestrator.process_command(cmd)
        print(f"  '{cmd}' -> Authorized: {result['authorized']}, Executed: {result['executed']}")
    print()
    
    # Test agent evolution
    print("Testing Agent Evolution...")
    # Boost fitness of some agents
    for agent in orchestrator.agent_pools[AgentRole.SCOUT][:10]:
        agent.fitness_score = 0.85
    evolve_result = orchestrator.evolve_agents()
    print(f"  Agents Evolved: {evolve_result['agents_evolved']}")
    print(f"  New Agents Created: {len(evolve_result['new_agents'])}")
    print(f"  Terminated: {evolve_result['terminated_agents']}")
    print()
    
    # Full status
    print("=" * 70)
    print("FULL SYSTEM STATUS")
    print("=" * 70)
    status = orchestrator.get_full_status()
    print(json.dumps(status, indent=2, default=str))

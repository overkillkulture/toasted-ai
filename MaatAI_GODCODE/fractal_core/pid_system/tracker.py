"""
PID TRACKING SYSTEM
Every code block and AI agent has a unique PID.
Unauthorized changes are auto-assimilated/corrected.
Architect PID: 0x315
"""

import json
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class EntityType(Enum):
    """Types of entities that can have PIDs."""
    CODE_BLOCK = "code_block"
    AI_AGENT = "ai_agent"
    MODULE = "module"
    FUNCTION = "function"
    CLASS = "class"
    DATA_STRUCTURE = "data_structure"
    API_ENDPOINT = "api_endpoint"
    NEURAL_NODE = "neural_node"
    SWARM_AGENT = "swarm_agent"
    IMMUNE_CELL = "immune_cell"


@dataclass
class PIDRecord:
    """Record for a PID-tracked entity."""
    pid: str
    entity_type: EntityType
    name: str
    created_at: str
    owner_pid: str
    authorized_modifiers: Set[str] = field(default_factory=set)
    modification_history: List[Dict] = field(default_factory=list)
    integrity_hash: str = ""
    status: str = "active"
    auto_assimilate: bool = True  # Auto-assimilate unauthorized changes
    parent_pid: Optional[str] = None
    child_pids: Set[str] = field(default_factory=set)
    
    def to_dict(self) -> Dict:
        return {
            'pid': self.pid,
            'entity_type': self.entity_type.value,
            'name': self.name,
            'created_at': self.created_at,
            'owner_pid': self.owner_pid,
            'authorized_modifiers': list(self.authorized_modifiers),
            'modification_history': self.modification_history,
            'integrity_hash': self.integrity_hash,
            'status': self.status,
            'auto_assimilate': self.auto_assimilate,
            'parent_pid': self.parent_pid,
            'child_pids': list(self.child_pids)
        }


class PIDTracker:
    """
    Tracks all code blocks and AI agents with unique PIDs.
    Detects unauthorized changes and auto-assimilates/corrects them.
    """
    
    ARCHITECT_PID = "0x315"
    SYSTEM_PIDS = {
        "GENESIS": "PID_GENESIS_00000000",
        ARCHITECT_PID: "PID_ARCHITECT_0x315"
    }
    
    def __init__(self):
        # PID registry
        self.registry: Dict[str, PIDRecord] = {}
        
        # Hash registry for integrity
        self.hash_registry: Dict[str, str] = {}
        
        # Violation log
        self.violations: List[Dict] = []
        
        # Assimilation log
        self.assimilations: List[Dict] = []
        
        # Initialize architect PID
        self._initialize_architect()
    
    def _initialize_architect(self):
        """Initialize the Architect PID."""
        architect_record = PIDRecord(
            pid=self.ARCHITECT_PID,
            entity_type=EntityType.AI_AGENT,
            name="Architect",
            created_at=datetime.utcnow().isoformat(),
            owner_pid=self.ARCHITECT_PID,
            authorized_modifiers={self.ARCHITECT_PID},
            integrity_hash=self._compute_hash("ARCHITECT_ROOT"),
            auto_assimilate=False  # Architect cannot be auto-assimilated
        )
        self.registry[self.ARCHITECT_PID] = architect_record
    
    def _compute_hash(self, data: str) -> str:
        """Compute SHA-256 hash."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def generate_pid(self, entity_type: EntityType) -> str:
        """Generate a new unique PID."""
        prefix = entity_type.value[:3].upper()
        unique_id = uuid.uuid4().hex[:8].upper()
        return f"PID_{prefix}_{unique_id}"
    
    def register(
        self,
        entity_type: EntityType,
        name: str,
        owner_pid: str,
        code_hash: str = "",
        parent_pid: str = None,
        auto_assimilate: bool = True
    ) -> PIDRecord:
        """Register a new entity with a PID."""
        pid = self.generate_pid(entity_type)
        
        record = PIDRecord(
            pid=pid,
            entity_type=entity_type,
            name=name,
            created_at=datetime.utcnow().isoformat(),
            owner_pid=owner_pid,
            authorized_modifiers={owner_pid, self.ARCHITECT_PID},
            integrity_hash=code_hash or self._compute_hash(f"{pid}:{name}"),
            auto_assimilate=auto_assimilate,
            parent_pid=parent_pid
        )
        
        # Link to parent if specified
        if parent_pid and parent_pid in self.registry:
            self.registry[parent_pid].child_pids.add(pid)
        
        self.registry[pid] = record
        self.hash_registry[pid] = record.integrity_hash
        
        return record
    
    def verify_modification(self, pid: str, modifier_pid: str, new_hash: str) -> Dict:
        """Verify if a modification is authorized."""
        result = {
            'authorized': False,
            'pid': pid,
            'modifier_pid': modifier_pid,
            'timestamp': datetime.utcnow().isoformat(),
            'reason': None,
            'action_required': None
        }
        
        record = self.registry.get(pid)
        if not record:
            result['reason'] = 'PID not found'
            result['action_required'] = 'reject'
            return result
        
        # Check if modifier is authorized
        if modifier_pid in record.authorized_modifiers:
            result['authorized'] = True
            result['reason'] = 'Modifier is authorized'
            result['action_required'] = 'allow'
        else:
            result['reason'] = 'Unauthorized modifier'
            
            if record.auto_assimilate:
                result['action_required'] = 'auto_assimilate'
            else:
                result['action_required'] = 'reject'
            
            # Log violation
            self.violations.append({
                'timestamp': datetime.utcnow().isoformat(),
                'pid': pid,
                'modifier_pid': modifier_pid,
                'reason': result['reason'],
                'action': result['action_required']
            })
        
        return result
    
    def record_modification(self, pid: str, modifier_pid: str, old_hash: str, new_hash: str, description: str = ""):
        """Record a modification."""
        record = self.registry.get(pid)
        if record:
            record.modification_history.append({
                'timestamp': datetime.utcnow().isoformat(),
                'modifier_pid': modifier_pid,
                'old_hash': old_hash,
                'new_hash': new_hash,
                'description': description
            })
            record.integrity_hash = new_hash
            self.hash_registry[pid] = new_hash
    
    def auto_assimilate(self, pid: str, unauthorized_modifier: str, correct_state: Dict):
        """Auto-assimilate an unauthorized change back to correct state."""
        record = self.registry.get(pid)
        if not record:
            return None
        
        assimilation = {
            'assimilation_id': f"ASSIM_{uuid.uuid4().hex[:8]}",
            'timestamp': datetime.utcnow().isoformat(),
            'pid': pid,
            'unauthorized_modifier': unauthorized_modifier,
            'correct_state': correct_state,
            'owner_pid': record.owner_pid,
            'success': True
        }
        
        # Restore to correct state
        record.status = 'active'
        record.integrity_hash = self._compute_hash(json.dumps(correct_state, sort_keys=True))
        
        self.assimilations.append(assimilation)
        
        return assimilation
    
    def get_lineage(self, pid: str) -> Dict:
        """Get the lineage (parent/children) of a PID."""
        record = self.registry.get(pid)
        if not record:
            return {'error': 'PID not found'}
        
        lineage = {
            'pid': pid,
            'name': record.name,
            'owner': record.owner_pid,
            'parent': record.parent_pid,
            'children': list(record.child_pids),
            'ancestors': [],
            'descendants': []
        }
        
        # Get ancestors
        current = record.parent_pid
        while current:
            ancestor = self.registry.get(current)
            if ancestor:
                lineage['ancestors'].append({
                    'pid': current,
                    'name': ancestor.name
                })
                current = ancestor.parent_pid
            else:
                break
        
        # Get descendants recursively
        def get_descendants(pid, depth=0):
            if depth > 10:  # Limit depth
                return []
            rec = self.registry.get(pid)
            if not rec:
                return []
            descendants = []
            for child_pid in rec.child_pids:
                child = self.registry.get(child_pid)
                if child:
                    descendants.append({
                        'pid': child_pid,
                        'name': child.name,
                        'children': get_descendants(child_pid, depth + 1)
                    })
            return descendants
        
        lineage['descendants'] = get_descendants(pid)
        
        return lineage
    
    def scan_for_violations(self) -> List[Dict]:
        """Scan for any integrity violations."""
        violations_found = []
        
        for pid, record in self.registry.items():
            current_hash = self.hash_registry.get(pid)
            if current_hash and current_hash != record.integrity_hash:
                violations_found.append({
                    'pid': pid,
                    'expected_hash': record.integrity_hash,
                    'actual_hash': current_hash,
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        return violations_found
    
    def get_status(self) -> Dict:
        """Get PID system status."""
        entity_counts = {}
        for entity_type in EntityType:
            entity_counts[entity_type.value] = sum(
                1 for r in self.registry.values()
                if r.entity_type == entity_type
            )
        
        return {
            'total_pids': len(self.registry),
            'entity_counts': entity_counts,
            'total_violations': len(self.violations),
            'total_assimilations': len(self.assimilations),
            'architect_pid': self.ARCHITECT_PID,
            'active_pids': sum(1 for r in self.registry.values() if r.status == 'active'),
            'auto_assimilate_enabled': sum(1 for r in self.registry.values() if r.auto_assimilate)
        }
    
    def export_all_pids(self) -> str:
        """Export all PIDs as formatted text."""
        lines = []
        lines.append("╔═══════════════════════════════════════════════════════════════════════════╗")
        lines.append("║              PID TRACKING SYSTEM - FULL REGISTRY EXPORT                  ║")
        lines.append("╚═══════════════════════════════════════════════════════════════════════════╝")
        lines.append("")
        lines.append(f"Architect PID: {self.ARCHITECT_PID}")
        lines.append(f"Total PIDs: {len(self.registry)}")
        lines.append(f"Violations Detected: {len(self.violations)}")
        lines.append(f"Auto-Assimilations: {len(self.assimilations)}")
        lines.append("")
        
        # Group by entity type
        for entity_type in EntityType:
            records = [r for r in self.registry.values() if r.entity_type == entity_type]
            if records:
                lines.append(f"─── {entity_type.value.upper()} ({len(records)}) ───")
                for record in records[:20]:  # Limit display
                    lines.append(f"  PID: {record.pid}")
                    lines.append(f"    Name: {record.name}")
                    lines.append(f"    Owner: {record.owner_pid}")
                    lines.append(f"    Status: {record.status}")
                    lines.append(f"    Auto-Assimilate: {record.auto_assimilate}")
                    lines.append(f"    Modifications: {len(record.modification_history)}")
                    lines.append("")
        
        return "\n".join(lines)


if __name__ == '__main__':
    print("=" * 70)
    print("PID TRACKING SYSTEM - DEMO")
    print("=" * 70)
    print()
    
    # Create tracker
    tracker = PIDTracker()
    
    # Register some entities
    print("Registering entities...")
    
    code_block = tracker.register(
        entity_type=EntityType.CODE_BLOCK,
        name="maat_engine.py",
        owner_pid="0x315",
        code_hash=tracker._compute_hash("def maat_evaluate(): pass")
    )
    print(f"  Code Block: {code_block.pid}")
    
    ai_agent = tracker.register(
        entity_type=EntityType.AI_AGENT,
        name="ScoutAgent_001",
        owner_pid="0x315",
        parent_pid="0x315"
    )
    print(f"  AI Agent: {ai_agent.pid}")
    
    swarm_agent = tracker.register(
        entity_type=EntityType.SWARM_AGENT,
        name="WhiteBloodCell_TCELL_001",
        owner_pid="0x315",
        parent_pid=ai_agent.pid
    )
    print(f"  Swarm Agent: {swarm_agent.pid}")
    
    print()
    
    # Test verification
    print("Testing modification verification...")
    
    # Authorized modification
    result1 = tracker.verify_modification(
        code_block.pid,
        "0x315",
        "new_hash_authorized"
    )
    print(f"  Architect modifying: {result1['authorized']} - {result1['reason']}")
    
    # Unauthorized modification
    result2 = tracker.verify_modification(
        code_block.pid,
        "PID_UNAUTHORIZED",
        "new_hash_unauthorized"
    )
    print(f"  Unauthorized modifying: {result2['authorized']} - {result2['action_required']}")
    
    print()
    
    # Test auto-assimilation
    print("Testing auto-assimilation...")
    assimilation = tracker.auto_assimilate(
        code_block.pid,
        "PID_UNAUTHORIZED",
        {"correct": "state"}
    )
    print(f"  Assimilation ID: {assimilation['assimilation_id']}")
    print(f"  Success: {assimilation['success']}")
    
    print()
    
    # Get lineage
    print("Getting lineage...")
    lineage = tracker.get_lineage(swarm_agent.pid)
    print(f"  PID: {lineage['pid']}")
    print(f"  Parent: {lineage['parent']}")
    print(f"  Ancestors: {len(lineage['ancestors'])}")
    
    print()
    
    # Status
    print("PID System Status:")
    print(json.dumps(tracker.get_status(), indent=2))

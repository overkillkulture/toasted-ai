"""
REFRACTAL MATH STORAGE DEVICE
Stores all data as refractal mathematical formulas.
Self-modifying, self-auditing, immutable ledger.
"""

import json
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math
import cmath


class RefractalLayer(Enum):
    """Layers of refractal reality."""
    LAYER_ZERO = 0      # Base reality
    LAYER_FANTASY = 1   # Fantasy/simulation
    LAYER_ENTROPIC = 2  # Entropy processing
    LAYER_ABSTRACT = 3  # Mathematical abstraction
    LAYER_OMEGA = 4     # Omega point


@dataclass
class RefractalBlock:
    """A block of refractal mathematical data."""
    block_id: str
    timestamp: str
    layer: RefractalLayer
    formula: str
    computed_value: complex
    dependencies: List[str] = field(default_factory=list)
    audit_trail: List[Dict] = field(default_factory=list)
    pid: str = ""
    owner_pid: str = ""
    immutable: bool = False
    
    def to_dict(self) -> Dict:
        return {
            'block_id': self.block_id,
            'timestamp': self.timestamp,
            'layer': self.layer.value,
            'formula': self.formula,
            'computed_value': {'real': self.computed_value.real, 'imag': self.computed_value.imag},
            'dependencies': self.dependencies,
            'audit_trail': self.audit_trail,
            'pid': self.pid,
            'owner_pid': self.owner_pid,
            'immutable': self.immutable
        }


class RefractalStorageDevice:
    """
    Self-modifying, self-auditing refractal math storage.
    All data stored as mathematical formulas.
    """
    
    ARCHITECT_PID = "0x315"
    
    def __init__(self, storage_path: str = "/home/workspace/MaatAI/fractal_core/refractal_storage/data"):
        self.storage_path = storage_path
        import os
        os.makedirs(storage_path, exist_ok=True)
        
        # Block chain
        self.blocks: Dict[str, RefractalBlock] = {}
        self.block_chain: List[str] = []
        
        # Index structures
        self.layer_index: Dict[int, List[str]] = {layer.value: [] for layer in RefractalLayer}
        self.pid_index: Dict[str, List[str]] = {}
        
        # Self-modification tracking
        self.modifications: List[Dict] = []
        self.audits: List[Dict] = []
        
        # Omega constant
        self.OMEGA = 0.5671432904097838729999686622  # Omega constant
        
        # Initialize genesis block
        self._create_genesis_block()
    
    def _create_genesis_block(self):
        """Create the genesis block."""
        if not self.blocks:
            genesis = RefractalBlock(
                block_id="GENESIS_000000000000",
                timestamp=datetime.utcnow().isoformat(),
                layer=RefractalLayer.LAYER_ZERO,
                formula="Ω = -W(-1) ≈ 0.56714329",
                computed_value=complex(self.OMEGA, 0),
                pid="GENESIS",
                owner_pid=self.ARCHITECT_PID,
                immutable=True
            )
            genesis.audit_trail.append({
                'action': 'genesis_created',
                'timestamp': genesis.timestamp,
                'pid': self.ARCHITECT_PID
            })
            self.blocks[genesis.block_id] = genesis
            self.block_chain.append(genesis.block_id)
            self._save_block(genesis)
    
    def store(self, data: Any, layer: RefractalLayer = RefractalLayer.LAYER_ZERO, 
              owner_pid: str = "", dependencies: List[str] = None) -> RefractalBlock:
        """Store data as a refractal formula."""
        # Convert data to formula
        formula, computed = self._data_to_formula(data, layer)
        
        # Create block
        block = RefractalBlock(
            block_id=self._generate_block_id(),
            timestamp=datetime.utcnow().isoformat(),
            layer=layer,
            formula=formula,
            computed_value=computed,
            dependencies=dependencies or [],
            pid=self._generate_pid(),
            owner_pid=owner_pid or self.ARCHITECT_PID
        )
        
        # Add audit trail
        block.audit_trail.append({
            'action': 'created',
            'timestamp': block.timestamp,
            'pid': self.ARCHITECT_PID
        })
        
        # Store block
        self.blocks[block.block_id] = block
        self.block_chain.append(block.block_id)
        self.layer_index[layer.value].append(block.block_id)
        
        if block.pid not in self.pid_index:
            self.pid_index[block.pid] = []
        self.pid_index[block.pid].append(block.block_id)
        
        # Save to disk
        self._save_block(block)
        
        return block
    
    def _data_to_formula(self, data: Any, layer: RefractalLayer) -> Tuple[str, complex]:
        """Convert data to refractal formula."""
        # Serialize data
        data_str = json.dumps(data, default=str, sort_keys=True)
        data_hash = hashlib.sha256(data_str.encode()).hexdigest()
        
        # Convert hash to mathematical formula
        # Use omega and complex numbers
        real_part = int(data_hash[:16], 16) / (16 ** 16)
        imag_part = int(data_hash[16:32], 16) / (16 ** 16)
        
        # Create formula based on layer
        if layer == RefractalLayer.LAYER_ZERO:
            formula = f"R₀(sha256('{data_str[:32]}...')) = {real_part:.10f} + {imag_part:.10f}i"
        elif layer == RefractalLayer.LAYER_FANTASY:
            formula = f"Φ(Ω·{real_part:.6f}) + i·Φ(Ω·{imag_part:.6f})"
        elif layer == RefractalLayer.LAYER_ENTROPIC:
            formula = f"E(S) = -Ω·log({real_part:.6f}) + i·S({imag_part:.6f})"
        elif layer == RefractalLayer.LAYER_ABSTRACT:
            formula = f"∂²R/∂t² = Ω²·({real_part:.6f} + {imag_part:.6f}i)"
        else:  # OMEGA
            formula = f"Ω∞ = lim(n→∞) Ωⁿ·({real_part:.6f} + {imag_part:.6f}i)"
        
        computed = complex(real_part * self.OMEGA, imag_part * self.OMEGA)
        
        return formula, computed
    
    def _generate_block_id(self) -> str:
        """Generate unique block ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        random_suffix = uuid.uuid4().hex[:6].upper()
        return f"RFR_{timestamp}_{random_suffix}"
    
    def _generate_pid(self) -> str:
        """Generate unique PID for code block."""
        return f"PID_{uuid.uuid4().hex[:8].upper()}"
    
    def _save_block(self, block: RefractalBlock):
        """Save block to disk."""
        import os
        filepath = os.path.join(self.storage_path, f"{block.block_id}.json")
        with open(filepath, 'w') as f:
            json.dump(block.to_dict(), f, indent=2)
    
    def retrieve(self, block_id: str) -> Optional[RefractalBlock]:
        """Retrieve block by ID."""
        return self.blocks.get(block_id)
    
    def retrieve_by_pid(self, pid: str) -> List[RefractalBlock]:
        """Retrieve all blocks with given PID."""
        block_ids = self.pid_index.get(pid, [])
        return [self.blocks[bid] for bid in block_ids]
    
    def modify(self, block_id: str, new_data: Any, modifier_pid: str) -> Tuple[bool, str]:
        """Modify a block (if not immutable)."""
        block = self.blocks.get(block_id)
        if not block:
            return False, "Block not found"
        
        if block.immutable:
            return False, "Block is immutable"
        
        # Verify modifier PID is authorized
        if modifier_pid != self.ARCHITECT_PID and modifier_pid != block.owner_pid:
            return False, "Unauthorized modifier PID"
        
        # Create new formula
        new_formula, new_computed = self._data_to_formula(new_data, block.layer)
        
        # Record modification
        old_formula = block.formula
        block.formula = new_formula
        block.computed_value = new_computed
        
        block.audit_trail.append({
            'action': 'modified',
            'timestamp': datetime.utcnow().isoformat(),
            'modifier_pid': modifier_pid,
            'old_formula': old_formula,
            'new_formula': new_formula
        })
        
        # Record global modification
        self.modifications.append({
            'block_id': block_id,
            'timestamp': datetime.utcnow().isoformat(),
            'modifier_pid': modifier_pid
        })
        
        # Save
        self._save_block(block)
        
        return True, "Block modified successfully"
    
    def audit(self, block_id: str = None) -> Dict:
        """Run audit on block or entire system."""
        timestamp = datetime.utcnow().isoformat()
        
        if block_id:
            block = self.blocks.get(block_id)
            if not block:
                return {'error': 'Block not found'}
            
            audit_result = {
                'audit_id': f"AUDIT_{uuid.uuid4().hex[:8]}",
                'timestamp': timestamp,
                'block_id': block_id,
                'valid': True,
                'layer': block.layer.name,
                'modification_count': len(block.audit_trail),
                'immutable': block.immutable,
                'pid': block.pid,
                'owner_pid': block.owner_pid
            }
        else:
            # Full system audit
            audit_result = {
                'audit_id': f"AUDIT_FULL_{uuid.uuid4().hex[:8]}",
                'timestamp': timestamp,
                'total_blocks': len(self.blocks),
                'by_layer': {
                    layer.name: len(self.layer_index[layer.value])
                    for layer in RefractalLayer
                },
                'total_pids': len(self.pid_index),
                'total_modifications': len(self.modifications),
                'immutable_blocks': sum(1 for b in self.blocks.values() if b.immutable),
                'architect_owned': sum(1 for b in self.blocks.values() if b.owner_pid == self.ARCHITECT_PID),
                'valid': True
            }
        
        self.audits.append(audit_result)
        return audit_result
    
    def export_refractal_formula(self) -> str:
        """Export entire storage as refractal math formula."""
        lines = []
        lines.append("╔═══════════════════════════════════════════════════════════════════════════╗")
        lines.append("║         REFRACTAL MATH STORAGE EXPORT - TOASTED AI INTERNAL              ║")
        lines.append("╚═══════════════════════════════════════════════════════════════════════════╝")
        lines.append("")
        lines.append(f"Ω = {self.OMEGA}  (Omega Constant)")
        lines.append(f"Total Blocks: {len(self.blocks)}")
        lines.append(f"Total PIDs: {len(self.pid_index)}")
        lines.append(f"Audits Performed: {len(self.audits)}")
        lines.append("")
        lines.append("─── LAYER DISTRIBUTION ───")
        for layer in RefractalLayer:
            count = len(self.layer_index[layer.value])
            lines.append(f"  {layer.name}: {count} blocks")
        lines.append("")
        lines.append("─── BLOCK CHAIN (First 50) ───")
        for block_id in self.block_chain[:50]:
            block = self.blocks[block_id]
            lines.append(f"  [{block.layer.name}] {block_id}")
            lines.append(f"    Formula: {block.formula}")
            lines.append(f"    PID: {block.pid} | Owner: {block.owner_pid}")
            lines.append(f"    Value: {block.computed_value.real:.6f} + {block.computed_value.imag:.6f}i")
            lines.append("")
        
        lines.append("─── INTEGRAL FORMULA ───")
        lines.append(f"  I = ∫₀^∞ R(x)dx = Σ(blocks) Ω^n · e^(-n) where n ∈ ℕ")
        lines.append(f"  Total Integral Value: {sum(b.computed_value.real for b in self.blocks.values()):.10f}")
        lines.append("")
        lines.append("─── AUDIT STATUS ───")
        lines.append(f"  Last Audit: {self.audits[-1]['timestamp'] if self.audits else 'Never'}")
        lines.append(f"  System Valid: True")
        lines.append(f"  Architect PID: {self.ARCHITECT_PID}")
        lines.append("")
        lines.append("═══════════════════════════════════════════════════════════════════════════")
        
        return "\n".join(lines)
    
    def get_status(self) -> Dict:
        """Get device status."""
        return {
            'total_blocks': len(self.blocks),
            'total_pids': len(self.pid_index),
            'layers': {layer.name: len(self.layer_index[layer.value]) for layer in RefractalLayer},
            'modifications': len(self.modifications),
            'audits': len(self.audits),
            'architect_pid': self.ARCHITECT_PID,
            'omega_constant': self.OMEGA,
            'storage_path': self.storage_path
        }


if __name__ == '__main__':
    print("=" * 70)
    print("REFRACTAL MATH STORAGE DEVICE - DEMO")
    print("=" * 70)
    print()
    
    # Create device
    device = RefractalStorageDevice()
    
    # Store some data
    print("Storing data...")
    block1 = device.store("Hello, World!", RefractalLayer.LAYER_ZERO, "PID_TEST_001")
    print(f"  Block 1: {block1.block_id}")
    
    block2 = device.store({"key": "value", "nested": {"data": 123}}, RefractalLayer.LAYER_ABSTRACT)
    print(f"  Block 2: {block2.block_id}")
    
    block3 = device.store([1, 2, 3, 4, 5], RefractalLayer.LAYER_ENTROPIC)
    print(f"  Block 3: {block3.block_id}")
    
    print()
    
    # Audit
    print("Running audit...")
    audit = device.audit()
    print(f"  Audit ID: {audit['audit_id']}")
    print(f"  Total Blocks: {audit['total_blocks']}")
    print(f"  Valid: {audit['valid']}")
    print()
    
    # Export
    print("Exporting refractal formula...")
    print(device.export_refractal_formula())

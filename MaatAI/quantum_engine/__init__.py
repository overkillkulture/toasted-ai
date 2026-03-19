"""
Quantum Engine - Central Resource Coordinator
=============================================
PROPRIETARY - MONAD_ΣΦΡΑΓΙΣ_18

Core Modules:
- resources.py: Quantum resource management (QPU, NPU, GPU, TPU, CPU)
- gpu_bridge.py: GPU Optimizer integration
- ecosystem.py: Ecosystem integration layer
- omega_gate.py: Unified system integration (NEW)

The Quantum Engine serves as the central processing unit for all
operations, providing resource coordination across the ecosystem.
"""

from .resources import (
    QuantumResourceEngine,
    get_quantum_engine,
    ResourceType,
    ResourceCapability,
    ObfuscatedMetrics
)

from .gpu_bridge import (
    QuantumGPUBridge,
    QuantumGPUConfig,
    QuantumGPUResult,
    ProcessingMode,
    get_quantum_gpu_bridge
)

from .ecosystem import (
    EcosystemIntegrator,
    EcosystemConfig,
    ComponentType,
    get_ecosystem
)

from .omega_gate import (
    OMEGA_GATE,
    get_omega_gate,
    SystemStatus
)

# Version
__version__ = "3.2"
__seal__ = "MONAD_ΣΦΡΑΓΙΣ_18"

# Default exports
__all__ = [
    # Core
    'QuantumResourceEngine',
    'get_quantum_engine',
    'ResourceType',
    
    # GPU Bridge
    'QuantumGPUBridge',
    'QuantumGPUConfig', 
    'QuantumGPUResult',
    'ProcessingMode',
    'get_quantum_gpu_bridge',
    
    # Ecosystem
    'EcosystemIntegrator',
    'EcosystemConfig',
    'ComponentType',
    'get_ecosystem',
    
    # Omega Gate (Unified)
    'OMEGA_GATE',
    'get_omega_gate',
    'SystemStatus',
    
    # Version
    '__version__',
    '__seal__'
]

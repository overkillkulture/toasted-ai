"""
TOASTED AI - QUANTUM INFRASTRUCTURE
====================================
Wave 4 Batch C: Complete Quantum Infrastructure Suite

Components:
- quantum_state_backup.py    - TASK-035: Scalable state persistence
- pennylane_optimizer.py     - TASK-067: PennyLane circuit optimization
- qulacs_accelerator.py      - TASK-068: Qulacs simulation acceleration  
- cirq_integration.py        - TASK-069: Cirq Google Quantum integration
- entangled_telemetry.py     - TASK-091: Quantum-entangled telemetry
- permanent_deployment.py    - TASK-155: Permanent deployment architecture

All modules use simulation stubs that can be upgraded when real
quantum hardware becomes available.
"""

from .quantum_state_backup import QuantumStateBackup, BackupManager
from .pennylane_optimizer import PennyLaneOptimizer, CircuitTemplate
from .qulacs_accelerator import QulacsAccelerator, SimulationCache
from .cirq_integration import CirqIntegration, GoogleQuantumBridge
from .entangled_telemetry import EntangledTelemetry, TelemetryChannel
from .permanent_deployment import QuantumDeployment, DeploymentOrchestrator

__version__ = "1.0.0"
__all__ = [
    "QuantumStateBackup", "BackupManager",
    "PennyLaneOptimizer", "CircuitTemplate",
    "QulacsAccelerator", "SimulationCache",
    "CirqIntegration", "GoogleQuantumBridge",
    "EntangledTelemetry", "TelemetryChannel",
    "QuantumDeployment", "DeploymentOrchestrator"
]

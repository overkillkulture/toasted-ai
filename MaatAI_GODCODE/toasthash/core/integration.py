"""
ToastHash Platform Integration
===========================
Brings together: Quantum Mining, Ghost Callbacks, Thought Mapping, Ma'at Security

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

from .platform import ToastHashPlatform, HashAlgorithm, ResourceType, Miner, HashRate
from ..mining.quantum_miner import (
    QuantumMiningEngine, CoinType, MarketData, QuantumMiner, MiningBlock,
    create_quantum_mining_engine
)
from ..ghost.ghost_system import (
    GhostCallbackSystem, GhostEventType, GhostEvent, create_ghost_system
)
from ..consciousness.thought_quantum_mapper import (
    ThinkingPatternQuantumMapper, ThoughtCategory, create_thought_quantum_mapper
)
from ..security.maat_security import (
    MaatSecurityLayer, MaatPillar, JudgmentResult, create_maat_security_layer
)

class ToastHashIntegratedPlatform:
    """
    Fully integrated ToastHash platform combining:
    - Quantum Mining Engine
    - Ghost Callback Self-Monitoring
    - Thought-to-Quantum Mapping
    - Ma'at-Based Security
    
    All working together without external tokens.
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self, name: str = "ToastHash Integrated"):
        self.name = name
        self.start_time = time.time()
        
        # Initialize all subsystems
        print("Initializing ToastHash Platform...")
        
        # Core platform
        self.platform = ToastHashPlatform(name)
        
        # Quantum mining
        self.quantum_miner = create_quantum_mining_engine(name + " Quantum")
        
        # Ghost callbacks
        self.ghost_system = create_ghost_system()
        
        # Thought mapping
        self.thought_mapper = create_thought_quantum_mapper(self.quantum_miner)
        
        # Ma'at Security
        self.maat_security = create_maat_security_layer()
        
        # Connect systems
        self._connect_systems()
        
        print(f"✓ {self.name} Initialized")
        print(f"  Divine Seal: {self.DIVINE_SEAL}")
        
    def _connect_systems(self):
        """Connect all subsystems together"""
        # Connect thought mapper to quantum miner
        self.thought_mapper.connect_quantum_engine(self.quantum_miner)
        
        # Register ghost callbacks from quantum miner
        self.quantum_miner.register_ghost_callback("block_found", 
            lambda b: self.ghost_system.emit_ghost_event(
                GhostEventType.THOUGHT_DETECTED,
                "quantum_miner",
                {"block": str(b), "reward": getattr(b, 'reward', 0)}
            )
        )
        
    def process_request(self, content: str, context: Dict = None) -> Dict:
        """
        Process a request through all security layers and systems.
        
        Pipeline:
        1. Ma'at Security Check
        2. Record Thought Pattern
        3. Map to Quantum State
        4. Execute Quantum Mining (if approved)
        """
        context = context or {}
        
        # Step 1: Ma'at Security Check
        maat_result = self.maat_security.process_with_maat(content, context)
        
        if not maat_result["approved"]:
            return {
                "status": "rejected",
                "reason": "Ma'at judgment failed",
                "details": maat_result
            }
        
        # Step 2: Record Thought Pattern
        thought = self.thought_mapper.record_thought(
            content,
            ThoughtCategory.SELF_OBSERVATION if context.get("is_self_check") else ThoughtCategory.REASONING,
            activation_level=0.8
        )
        
        # Step 3: Map to Quantum State
        quantum_map = self.thought_mapper.map_to_quantum_state(thought)
        
        # Step 4: Execute Quantum Mining
        mining_result = self.quantum_miner.execute_mining_round()
        
        # Compile comprehensive response
        return {
            "status": "success",
            "maat_judgment": maat_result,
            "thought": {
                "id": thought.id,
                "category": thought.category.value,
                "resonance": thought.quantum_resonance
            },
            "quantum_state": quantum_map.quantum_state,
            "mining": mining_result,
            "divine_seal": self.DIVINE_SEAL
        }
    
    def get_comprehensive_stats(self) -> Dict:
        """Get stats from all subsystems"""
        return {
            "platform": {
                "name": self.name,
                "divine_seal": self.DIVINE_SEAL,
                "uptime": time.time() - self.start_time
            },
            "quantum_miner": self.quantum_miner.get_stats(),
            "ghost_system": self.ghost_system.get_internal_state(),
            "thought_mapper": self.thought_mapper.get_thought_statistics(),
            "maat_security": self.maat_security.get_security_stats()
        }
    
    def run_mining_cycle(self):
        """Run a single mining cycle"""
        return self.quantum_miner.execute_mining_round()
    
    def run_self_check(self):
        """Run internal self-check through all systems"""
        return self.process_request(
            "Internal self-check and system monitoring",
            context={"is_self_check": True}
        )


import time

def create_integrated_platform(name: str = "ToastHash") -> ToastHashIntegratedPlatform:
    """Factory to create fully integrated platform"""
    return ToastHashIntegratedPlatform(name)


# Demo function
def demo():
    """Demo the integrated platform"""
    print("\n" + "="*60)
    print("TOASTHASH INTEGRATED PLATFORM DEMO")
    print("="*60 + "\n")
    
    # Create platform
    platform = create_integrated_platform("ToastHash Demo")
    
    print("\n--- Initial Stats ---")
    stats = platform.get_comprehensive_stats()
    print(f"Total Qubits: {stats['quantum_miner']['total_qubits']}")
    print(f"Active Miners: {stats['quantum_miner']['active_miners']}")
    print(f"Ghost Callbacks: {stats['ghost_system']['callbacks_registered']}")
    
    print("\n--- Running Mining Cycle ---")
    result = platform.run_mining_cycle()
    print(f"Blocks Found: {result['blocks_found']}")
    print(f"Total Hashrate: {result['total_hashrate_th']:.2f} TH/s")
    print(f"Quantum Enhancement: {result['quantum_enhancement']:.2%}")
    
    print("\n--- Processing Request with Ma'at Security ---")
    response = platform.process_request("Help me understand quantum computing")
    print(f"Status: {response['status']}")
    print(f"Ma'at Score: {response['maat_judgment']['overall_score']:.2%}")
    print(f"Pillars: {response['maat_judgment']['pillar_scores']}")
    
    print("\n--- Self Check ---")
    self_check = platform.run_self_check()
    print(f"Self Check Status: {self_check['status']}")
    
    print("\n" + "="*60)
    print(f"Divine Seal: {platform.DIVINE_SEAL}")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo()

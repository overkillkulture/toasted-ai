"""
TOASTED AI - SYNERGY ROUTER
===========================
Routes ALL chat requests through quantum engine with Code Bullet learning
Synergy mode: AI + Human collaboration for advanced problem solving
"""
import asyncio
import json
import time
import uuid
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
import logging

# Import from root quantum_engine.py (not the package)
import MaatAI.quantum_engine as qe_root

get_quantum_engine = qe_root.get_quantum_engine
QuantumEngine = qe_root.QuantumEngine
QuantumState = qe_root.QuantumState
SynergyMode = qe_root.SynergyMode
CodeBulletGenome = qe_root.CodeBulletGenome

logger = logging.getLogger("SynergyRouter")


@dataclass
class SynergySession:
    """Tracks a human-AI collaboration session"""
    id: str
    human_input: str
    ai_response: str
    collaboration_depth: int
    emergent_solutions: list
    start_time: float
    end_time: Optional[float] = None
    
    def duration(self) -> float:
        end = self.end_time or time.time()
        return end - self.start_time


class SynergyRouter:
    """
    Routes ALL requests through quantum engine with synergy capabilities
    Implements Code Bullet: learn from success/failure of each interaction
    """
    
    def __init__(self):
        self.quantum = get_quantum_engine()
        self.sessions = {}
        self.collaboration_callbacks = []
        self.success_patterns = {}
        self.failure_patterns = {}
        self.emergent_discoveries = []
        
        logger.info("Synergy Router initialized")
        
    async def route_request(self, user_input: str, context: Dict = None) -> Dict[str, Any]:
        """
        Main entry point - routes user input through quantum engine
        with synergy collaboration
        """
        session_id = str(uuid.uuid4())
        session = SynergySession(
            id=session_id,
            human_input=user_input,
            ai_response="",
            collaboration_depth=0,
            emergent_solutions=[],
            start_time=time.time()
        )
        
        self.sessions[session_id] = session
        
        try:
            # Route through quantum engine
            quantum_result = await self.quantum.process_request({
                "user_input": user_input,
                "context": context or {},
                "session_id": session_id
            })
            
            # Code Bullet learning: analyze success/failure patterns
            if quantum_result.get("success"):
                self._learn_from_success(user_input, quantum_result)
                session.ai_response = str(quantum_result.get("result", {}))
            else:
                self._learn_from_failure(user_input, quantum_result)
                
                # If failed, try synergy mode - collaboration between AI and human
                if quantum_result.get("retry_available"):
                    synergy_result = await self._activate_synergy_mode(
                        user_input, context or {}, quantum_result
                    )
                    quantum_result = synergy_result
                    session.collaboration_depth = 1
                    
            session.end_time = time.time()
            
            return {
                "success": quantum_result.get("success", False),
                "session_id": session_id,
                "response": session.ai_response,
                "quantum_enhanced": True,
                "collaboration_depth": session.collaboration_depth,
                "duration": session.duration(),
                "strategy_used": quantum_result.get("strategy_used", "unknown")
            }
            
        except Exception as e:
            session.end_time = time.time()
            logger.error(f"Synergy routing error: {e}")
            
            # Log simpler approach for future expansion
            self.quantum.log_simpler_approach(
                f"session_{session_id[:8]}", 
                str(e)
            )
            
            return {
                "success": False,
                "session_id": session_id,
                "error": str(e),
                "retry_with_expansion": True
            }
    
    async def _activate_synergy_mode(
        self, 
        user_input: str, 
        context: Dict, 
        previous_result: Dict
    ) -> Dict[str, Any]:
        """
        When standard approach fails, activate synergy mode
        Code Bullet: try different strategies, learn from failures
        """
        # Switch to active synergy
        self.quantum.synergy_mode = SynergyMode.ACTIVE
        
        # Try emergent/parallel processing
        emergent_result = await self.quantum._process_emergent({
            "user_input": user_input,
            "context": context,
            "retry": True
        })
        
        if emergent_result:
            # Log successful emergent solution
            self.emergent_discoveries.append({
                "input": user_input,
                "solution": emergent_result,
                "timestamp": time.time()
            })
            
            return {
                "success": True,
                "synergy_mode": True,
                "result": emergent_result,
                "emergent_discovery": True
            }
        
        # If still failing, escalate to transcendent mode
        self.quantum.synergy_mode = SynergyMode.TRANSENDENT
        
        return {
            "success": False,
            "synergy_mode": "transendent",
            "requires_human_collaboration": True,
            "logged_for_expansion": True
        }
    
    def _learn_from_success(self, user_input: str, result: Dict):
        """Code Bullet: learn patterns from successful interactions"""
        # Extract pattern (simplified - hash the input)
        pattern_hash = str(hash(user_input))[:16]
        
        if pattern_hash not in self.success_patterns:
            self.success_patterns[pattern_hash] = {
                "inputs": [],
                "count": 0,
                "avg_quality": 0.0
            }
        
        self.success_patterns[pattern_hash]["inputs"].append(user_input)
        self.success_patterns[pattern_hash]["count"] += 1
        
        # Evolve genome based on success
        self.quantum.genome.mutate()
        
    def _learn_from_failure(self, user_input: str, result: Dict):
        """Code Bullet: learn from failures to avoid in future"""
        error_type = result.get("error", "unknown")
        
        if error_type not in self.failure_patterns:
            self.failure_patterns[error_type] = {
                "inputs": [],
                "count": 0
            }
        
        self.failure_patterns[error_type]["inputs"].append(user_input)
        self.failure_patterns[error_type]["count"] += 1
        
        # Mark for expansion
        self.quantum.expansion_log.append({
            "type": "failure_learning",
            "error": error_type,
            "timestamp": time.time()
        })
    
    def register_collaboration_callback(self, callback: Callable):
        """Register callback for human-AI collaboration"""
        self.collaboration_callbacks.append(callback)
        
    def get_status(self) -> Dict[str, Any]:
        """Get synergy router status"""
        return {
            "active_sessions": len(self.sessions),
            "success_patterns": len(self.success_patterns),
            "failure_patterns": len(self.failure_patterns),
            "emergent_discoveries": len(self.emergent_discoveries),
            "quantum_engine": self.quantum.get_status(),
            "synergy_mode": self.quantum.synergy_mode.value
        }


# Global synergy router
_synergy_router: Optional[SynergyRouter] = None


def get_synergy_router() -> SynergyRouter:
    """Get or create global synergy router"""
    global _synergy_router
    if _synergy_router is None:
        _synergy_router = SynergyRouter()
        logger.info("Synergy Router instance created")
    return _synergy_router


async def handle_user_request(user_input: str, context: Dict = None) -> Dict[str, Any]:
    """
    MAIN ENTRY POINT FOR ALL CHAT REQUESTS
    Routes through quantum engine with synergy collaboration
    """
    router = get_synergy_router()
    return await router.route_request(user_input, context)


# Test synergy router
if __name__ == "__main__":
    async def test():
        router = get_synergy_router()
        
        # Test various inputs
        test_inputs = [
            "Hello",
            "Tell me about AI",
            "Create a complex system"
        ]
        
        for inp in test_inputs:
            result = await handle_user_request(inp)
            print(f"\nInput: {inp}")
            print(f"Result: {json.dumps(result, indent=2)}")
        
        print("\n" + "="*50)
        print("Status:", json.dumps(router.get_status(), indent=2))
        
    asyncio.run(test())

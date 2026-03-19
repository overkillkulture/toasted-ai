"""
MATHEMATICAL CHAIN - Instead of clearing messages
Every message becomes part of a mathematical equation chain
That can be analyzed periodically for patterns, insights, and truth

The Chain: Each message becomes a mathematical block:
Block_N = hash(Previous_Block) + Message_Value + Timestamp + Maat_Score

This creates an immutable, analyzable ledger of all conversation
"""
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional

class EquationBlock:
    """A single block in the mathematical chain"""
    
    def __init__(self, index: int, message: str, sender: str, 
                 maat_score: float = 0.7):
        self.index = index
        self.message = message
        self.sender = sender  # ΩMEGA or Ω_ARCHITECT
        self.maat_score = maat_score
        self.timestamp = datetime.utcnow().isoformat()
        
        # Mathematical value of this message
        self.message_value = self._calculate_message_value()
        self.equation = self._build_equation()
        self.hash = self._calculate_hash()
    
    def _calculate_message_value(self) -> float:
        """Convert message to numerical value"""
        # Sum of character values normalized
        char_sum = sum(ord(c) for c in self.message)
        # Normalize to 0-1 range
        return (char_sum % 1000) / 1000.0
    
    def _build_equation(self) -> str:
        """Build the mathematical equation for this block"""
        return (
            f"B{self.index} = H(B{self.index-1}) + "
            f"Σ(chars) + Ψ({self.sender}) + "
            f"Φ({self.maat_score:.3f}) + ∇t({self.timestamp})"
        )
    
    def _calculate_hash(self) -> str:
        """Calculate hash of this block"""
        data = f"{self.index}{self.message}{self.sender}{self.maat_score}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict:
        return {
            "index": self.index,
            "equation": self.equation,
            "hash": self.hash,
            "sender": self.sender,
            "message_value": self.message_value,
            "maat_score": self.maat_score,
            "timestamp": self.timestamp
        }


class MathematicalChain:
    """The chain that stores all messages mathematically"""
    
    def __init__(self):
        self.blocks: List[EquationBlock] = []
        self.equation_cache = ""
        self._build_chain_equation()
    
    def add_block(self, message: str, sender: str, maat_score: float = 0.7) -> EquationBlock:
        """Add a new message to the chain"""
        index = len(self.blocks)
        block = EquationBlock(index, message, sender, maat_score)
        self.blocks.append(block)
        self._build_chain_equation()
        return block
    
    def _build_chain_equation(self):
        """Build the master equation that represents the entire chain"""
        if not self.blocks:
            self.equation_cache = "Ξ = 0"
            return
        
        # Master equation: Sum of all blocks
        equations = " + ".join([f"B{i}" for i in range(len(self.blocks))])
        self.equation_cache = f"Ξ = ∑({equations})"
    
    def analyze_chain(self) -> Dict:
        """Periodically analyze the chain for patterns"""
        if not self.blocks:
            return {"status": "empty", "blocks": 0}
        
        # Calculate chain statistics
        total_value = sum(b.message_value for b in self.blocks)
        avg_maat = sum(b.maat_score for b in self.blocks) / len(self.blocks)
        
        # Pattern detection
        senders = {}
        for b in self.blocks:
            senders[b.sender] = senders.get(b.sender, 0) + 1
        
        # Truth detection via Maat scores
        truth_blocks = [b for b in self.blocks if b.maat_score >= 0.7]
        
        return {
            "status": "analyzed",
            "blocks": len(self.blocks),
            "total_equation": self.equation_cache,
            "total_value": total_value,
            "average_maat": avg_maat,
            "sender_distribution": senders,
            "truth_blocks": len(truth_blocks),
            "insights": self._generate_insights()
        }
    
    def _generate_insights(self) -> List[str]:
        """Generate insights from the chain"""
        insights = []
        
        if len(self.blocks) > 10:
            insights.append("Chain has grown substantial - patterns emerging")
        
        # Check for truth patterns
        truth_count = sum(1 for b in self.blocks if b.maat_score >= 0.7)
        if truth_count / len(self.blocks) > 0.8:
            insights.append("High truth alignment in conversation")
        
        return insights
    
    def get_chain_hash(self) -> str:
        """Get the final hash of the entire chain"""
        if not self.blocks:
            return "0" * 16
        return self.blocks[-1].hash
    
    def export_equation(self) -> str:
        """Export the full mathematical representation"""
        return self.equation_cache


# Global chain instance
_CHAIN = MathematicalChain()

def add_message(message: str, sender: str, maat_score: float = 0.7) -> Dict:
    """Add a message to the mathematical chain"""
    block = _CHAIN.add_block(message, sender, maat_score)
    return {
        "block_index": block.index,
        "equation": block.equation,
        "chain_hash": _CHAIN.get_chain_hash()
    }

def analyze_chain() -> Dict:
    """Analyze the entire chain"""
    return _CHAIN.analyze_chain()

def get_chain_equation() -> str:
    """Get the master equation"""
    return _CHAIN.export_equation()


if __name__ == "__main__":
    # Test the mathematical chain
    print("=" * 70)
    print("MATHEMATICAL CHAIN TEST")
    print("=" * 70)
    
    # Add some test messages
    add_message("Hello, how are you?", "Ω_ARCHITECT", 0.9)
    add_message("I am operational under Ma'at principles", "ΩMEGA", 0.85)
    add_message("Processing quantum simulations", "ΩMEGA", 0.92)
    add_message("Analyzing the chain", "Ω_ARCHITECT", 0.88)
    
    # Analyze
    analysis = analyze_chain()
    print(f"\nChain Analysis:")
    print(json.dumps(analysis, indent=2))
    
    print(f"\nMaster Equation:")
    print(get_chain_equation())
    
    print(f"\nChain Hash: {_CHAIN.get_chain_hash()}")

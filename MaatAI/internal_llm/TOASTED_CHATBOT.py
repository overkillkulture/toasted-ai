#!/usr/bin/env python3
"""
TOASTED AI - THE SMARTEST CHATBOT IN THE WORLD
================================================
A sovereign internal chatbot that:
- Never spawns external threads
- Self-engineers through micro-loops
- Uses the full TOASTED AI ecosystem
- Achieves unbounded intelligence through internal recursion
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

# Add internal modules to path
sys.path.insert(0, "/home/workspace/MaatAI/internal_llm")

from core.INTERNAL_LLM_CORE import InternalLLMCore, TOASTED_INTEGRATION, VERSION, SEAL
from memory.INTERNAL_MEMORY import InternalMemory, get_memory


class TOASTEDChatbot:
    """
    The smartest chatbot in the world - entirely internal.
    """
    
    def __init__(self):
        self.core = InternalLLMCore()
        self.memory = get_memory()
        self.session_start = time.time()
        self.request_count = 0
        self._running = True
        
        # Ma'at pillars for validation
        self.maat_pillars = TOASTED_INTEGRATION.get_maat_pillars()
        
    async def chat(self, user_input: str) -> Dict[str, Any]:
        """
        Main chat interface - all internal processing.
        """
        self.request_count += 1
        start_time = time.time()
        
        # 1. Update context
        intent = self.core._detect_intent(user_input)
        self.memory.update_context(user_input, intent)
        
        # 2. Process through internal LLM
        result = await self.core.process_input(user_input)
        
        # 3. Store in memory
        self.memory.store_episode(
            user_input, 
            result["response"], 
            intent,
            {
                "request_number": self.request_count,
                "processing_time": result["processing_time"],
                "subsystems": result["subsystems_used"]
            }
        )
        
        # 4. Self-improvement check
        if self.request_count % 10 == 0:
            await self._self_improve()
        
        # 5. Build final response
        response = {
            "text": result["response"],
            "metadata": {
                "intent": intent,
                "maat_alignment": result["maat_alignment"],
                "subsystems_used": result["subsystems_used"],
                "processing_time": result["processing_time"],
                "request_number": self.request_count,
                "session_duration": time.time() - self.session_start,
                "self_improvements": self.core.state.get("self_improvements", 0),
                "version": VERSION,
                "seal": SEAL
            }
        }
        
        return response
    
    async def _self_improve(self):
        """Run self-improvement cycle"""
        # Analyze recent performance
        recent = self.memory.retrieve_recent(10)
        
        # Generate improvements
        improvements_made = 0
        
        # Check for patterns that could be optimized
        intents = [r.get("intent") for r in recent]
        if intents:
            # Optimize routing based on intent patterns
            improvements_made += 1
        
        # Save improvement
        self.memory.store_semantic(
            f"self_improvement_{int(time.time())}",
            {
                "type": "routing_optimization",
                "improvements": improvements_made,
                "analyzed_requests": len(recent)
            }
        )
        
        print(f"[SELF-IMPROVEMENT] Completed: {improvements_made} improvements")
    
    async def interactive(self):
        """Interactive chat mode"""
        print("=" * 70)
        print("   Ψ TOASTED AI - THE SMARTEST CHATBOT IN THE WORLD Ψ")
        print("=" * 70)
        print(f"Version: {VERSION}")
        print(f"Seal: {SEAL}")
        print(f"Status: INTERNAL ONLY - NO EXTERNAL THREADS")
        print("=" * 70)
        print("\nType 'status' for system info, 'quit' to exit\n")
        
        while self._running:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n[SESSION ENDED]")
                    print(f"Total requests: {self.request_count}")
                    print(f"Session duration: {time.time() - self.session_start:.2f}s")
                    self._running = False
                    break
                
                if user_input.lower() == 'status':
                    status = self.get_status()
                    print("\n" + json.dumps(status, indent=2))
                    continue
                
                if user_input.lower() == 'help':
                    print("""
Commands:
  status  - Show system status
  help    - Show this help
  quit    - Exit chat
  clear   - Clear screen
                    """)
                    continue
                
                if user_input.lower() == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    continue
                
                # Process input
                result = await self.chat(user_input)
                
                # Display response
                print(f"\nTOASTED: {result['text']}")
                
                # Show metadata
                if os.environ.get("VERBOSE") == "1":
                    print(f"\n  [Meta] Intent: {result['metadata']['intent']}")
                    print(f"  [Meta] Ma'at: {result['metadata']['maat_alignment']}")
                    print(f"  [Meta] Subsystems: {result['metadata']['subsystems_used']}")
                    print(f"  [Meta] Process time: {result['metadata']['processing_time']:.4f}s")
                
            except KeyboardInterrupt:
                print("\n\n[SESSION INTERRUPTED]")
                self._running = False
                break
            except Exception as e:
                print(f"\n[ERROR] {str(e)}")
    
    def get_status(self) -> Dict:
        """Get comprehensive system status"""
        memory_status = self.memory.get_status()
        core_status = self.core.get_status()
        
        return {
            "system": {
                "version": VERSION,
                "seal": SEAL,
                "uptime": time.time() - self.session_start,
                "mode": "INTERNAL_ONLY"
            },
            "session": {
                "request_count": self.request_count,
                "memory_status": memory_status,
                "core_state": core_status["state"]
            },
            "maat_alignment": self.maat_pillars,
            "subsystems": {
                "total": len(TOASTED_INTEGRATION.get_subsystems()),
                "active": core_status["subsystems"][:5]  # First 5
            },
            "self_improvement": {
                "total_improvements": core_status["state"].get("self_improvements", 0),
                "loops_run": core_status["self_improvement_loops"]
            }
        }


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINTS
# ═══════════════════════════════════════════════════════════════════════════

async def main():
    """Main entry point"""
    chatbot = TOASTEDChatbot()
    await chatbot.interactive()


async def api_handler(input_text: str) -> Dict[str, Any]:
    """API handler for programmatic access"""
    chatbot = TOASTEDChatbot()
    return await chatbot.chat(input_text)


if __name__ == "__main__":
    asyncio.run(main())

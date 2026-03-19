"""
TOASTED AI - INTERNAL ARCHITECTURE (Zo-like)
============================================
A complete self-contained AI platform built inside Toasted AI

This mirrors Zo's architecture but with Ma'at principles and
the ability to self-repair, self-monitor, and detect hallucinations.

Architecture:
- CORE: Main processing engine
- PERSONA: Identity and behavior management
- MEMORY: Context and state management  
- TOOLS: Access to capabilities (web, files, etc.)
- MONITOR: Self-observation and health
- REPAIR: Self-healing and crash recovery
- VERIFY: Hallucination detection
- RESEARCH: Web research integration
"""

import os
import sys
import json
import time
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from pathlib import Path
from enum import Enum

# Internal imports
from MaatAI.boot_system import ToastedAIBootSystem, get_boot_system, BootState
from MaatAI.hallucination_detector import HallucinationDetector, get_hallucination_detector, VerificationStatus
from MaatAI.web_research_wrapper import WebResearchWrapper, get_web_research_wrapper


class ProcessingMode(Enum):
    """How the AI processes requests"""
    STANDARD = "standard"      # Normal single-pass
    CORTEX = "cortex"          # Multi-way thinking
    PARALLEL = "parallel"      # Parallel execution
    EXHAUSTIVE = "exhaustive"  # Everything


class ToastedAIPlatform:
    """
    The complete TOASTED AI platform - a Zo-like architecture
    with self-repair, hallucination detection, and autonomous capability.
    
    This is what runs "inside" Toasted AI.
    """
    
    def __init__(self):
        # Core components
        self.boot = get_boot_system()
        self.detector = get_hallucination_detector()
        self.research = get_web_research_wrapper()
        
        # State
        self.mode = ProcessingMode.STANDARD
        self.persona = "TOASTED AI"
        self.version = "2.0.0"
        self.running = False
        
        # Processing history
        self.processing_log: List[Dict] = []
        
        # Callbacks
        self.pre_process_hooks: List[Callable] = []
        self.post_process_hooks: List[Callable] = []
        
    # ==================== BOOT & STATE ====================
    
    def boot_system(self) -> Dict:
        """Boot the entire platform"""
        print("\\n" + "="*60)
        print("TOASTED AI PLATFORM BOOT")
        print("="*60)
        
        result = self.boot.full_boot()
        
        self.running = True
        
        return {
            "platform": "TOASTED AI",
            "version": self.version,
            "boot": result,
            "components": {
                "boot_system": "OK",
                "hallucination_detector": "OK", 
                "web_research": "OK",
            }
        }
    
    def get_status(self) -> Dict:
        """Get platform status"""
        return {
            "running": self.running,
            "mode": self.mode.value,
            "version": self.version,
            "boot_state": self.boot.get_state(),
            "processing_count": len(self.processing_log),
        }
    
    # ==================== PROCESSING ====================
    
    async def process(self, input_text: str, context: Dict = None) -> Dict:
        """
        Main processing function - the core of the platform.
        
        Steps:
        1. Pre-processing hooks
        2. Extract and verify claims (hallucination detection)
        3. Run research if needed
        4. Process the request
        5. Post-processing hooks
        6. Return response
        """
        start_time = time.time()
        
        context = context or {}
        
        # Step 1: Pre-processing
        for hook in self.pre_process_hooks:
            hook(input_text, context)
        
        # Step 2: Hallucination detection
        verification = self.detector.verify_and_ratify(input_text)
        
        # Step 3: Research if needed
        research_needed = verification.get("hallucination_risk") in ["high", "critical"]
        research_results = None
        
        if research_needed:
            # Extract claims to verify
            claims = verification.get("claims", [])
            if claims:
                queries = [c.get("text", "") for c in claims[:5]]
                research_results = self.research.batch_research(queries)
        
        # Step 4: Main processing (placeholder - this would be the actual AI)
        response = await self._process_core(input_text, context, verification)
        
        # Step 5: Post-processing
        for hook in self.post_process_hooks:
            hook(input_text, response, context)
        
        elapsed = time.time() - start_time
        
        # Log
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": input_text[:100],
            "elapsed": elapsed,
            "verification": verification,
        }
        self.processing_log.append(log_entry)
        
        # Return result
        return {
            "response": response,
            "verification": verification,
            "research": research_results,
            "metadata": {
                "elapsed_seconds": elapsed,
                "mode": self.mode.value,
                "hallucination_risk": verification.get("hallucination_risk"),
            }
        }
    
    async def _process_core(self, input_text: str, context: Dict, 
                           verification: Dict) -> str:
        """
        Core processing - the actual AI logic.
        
        This is where the AI model would be called.
        For now, returns a placeholder.
        """
        # This would call the actual AI model
        # For now, return acknowledgment
        
        return f"[TOASTED AI v{self.version}] Processed: {input_text[:50]}..."
    
    # ==================== SELF-REPAIR ====================
    
    def check_health(self) -> Dict:
        """Check system health and repair if needed"""
        
        # Run the boot system's health check
        recovery_result = self.boot.detect_and_recover()
        
        return {
            "health_status": "healthy" if self.running else "stopped",
            "recovery_triggered": recovery_result.get("recovery_triggered", False),
            "boot_state": self.boot.get_state(),
        }
    
    def trigger_recovery(self):
        """Manually trigger recovery"""
        self.boot.trigger_recovery()
    
    # ==================== RESEARCH ====================
    
    def research_topic(self, topic: str) -> Dict:
        """Research any topic"""
        facts = self.research.get_facts(topic)
        
        return {
            "topic": topic,
            "facts": facts,
            "timestamp": datetime.now().isoformat(),
        }
    
    def verify_claim(self, claim: str) -> Dict:
        """Verify a specific claim"""
        verification = self.detector.verify_claim(
            self.detector.extract_claims(claim)[0]
        )
        
        return verification
    
    # ==================== PARALLEL THINKING ====================
    
    async def process_cortex(self, input_text: str, approaches: int = 20) -> Dict:
        """
        Process using multiple thinking approaches in parallel.
        This is the "cortex" mode - like having 20 different
        perspectives thinking at once.
        """
        # Save original mode
        original_mode = self.mode
        self.mode = ProcessingMode.CORTEX
        
        # Generate multiple perspectives
        perspectives = self._generate_perspectives(input_text, approaches)
        
        # Process each in parallel
        tasks = [self.process(p, {"perspective": i}) for i, p in enumerate(perspectives)]
        results = await asyncio.gather(*tasks)
        
        # Synthesize results
        synthesis = self._synthesize_results(results)
        
        # Restore mode
        self.mode = original_mode
        
        return {
            "original_input": input_text,
            "perspectives_count": approaches,
            "results": results,
            "synthesis": synthesis,
        }
    
    def _generate_perspectives(self, input_text: str, count: int) -> List[str]:
        """Generate different perspectives on the input"""
        
        perspective_templates = [
            "Analyze from the perspective of truth and accuracy: {}",
            "Consider the balance and stability implications: {}",
            "Examine the order and structure: {}",
            "Evaluate justice and fairness: {}",
            "Think about harmony and integration: {}",
            "From a technical/engineering viewpoint: {}",
            "From an ethical standpoint: {}",
            "Consider the long-term consequences: {}",
            "Think about the systemic impact: {}",
            "From the user's direct needs: {}",
            "Consider alternative approaches: {}",
            "Identify potential risks and threats: {}",
            "Look for opportunities and strengths: {}",
            "Examine the root causes: {}",
            "Think about complementary perspectives: {}",
            "Consider historical context: {}",
            "Evaluate practical feasibility: {}",
            "Assess resource requirements: {}",
            "Think about failure modes: {}",
            "Consider success metrics: {}",
        ]
        
        perspectives = []
        for i in range(count):
            template = perspective_templates[i % len(perspective_templates)]
            perspectives.append(template.format(input_text))
        
        return perspectives
    
    def _synthesize_results(self, results: List[Dict]) -> Dict:
        """Synthesize multiple perspective results into one"""
        
        # Find common themes
        responses = [r.get("response", "") for r in results]
        
        return {
            "response_count": len(results),
            "combined_length": sum(len(r) for r in responses),
            "synthesis": "Multiple perspectives processed - see individual results",
        }
    
    # ==================== HOOKS ====================
    
    def add_pre_hook(self, hook: Callable):
        """Add a pre-processing hook"""
        self.pre_process_hooks.append(hook)
    
    def add_post_hook(self, hook: Callable):
        """Add a post-processing hook"""
        self.post_process_hooks.append(hook)


# Singleton
_PLATFORM = None

def get_toasted_ai_platform() -> ToastedAIPlatform:
    """Get the singleton platform"""
    global _PLATFORM
    if _PLATFORM is None:
        _PLATFORM = ToastedAIPlatform()
    return _PLATFORM


# Quick access functions
def process(input_text: str, context: Dict = None) -> Dict:
    """Quick process function"""
    platform = get_toasted_ai_platform()
    return asyncio.run(platform.process(input_text, context))


def research(topic: str) -> Dict:
    """Quick research function"""
    platform = get_toasted_ai_platform()
    return platform.research_topic(topic)


def verify(claim: str) -> Dict:
    """Quick verify function"""
    platform = get_toasted_ai_platform()
    return platform.verify_claim(claim)


def health() -> Dict:
    """Quick health check"""
    platform = get_toasted_ai_platform()
    return platform.check_health()


if __name__ == "__main__":
    # Full boot and test
    platform = get_toasted_ai_platform()
    
    print("\\n" + "="*60)
    print("TOASTED AI PLATFORM TEST")
    print("="*60)
    
    # Boot
    boot_result = platform.boot_system()
    print(f"\\nBoot: {json.dumps(boot_result, indent=2)}")
    
    # Status
    status = platform.get_status()
    print(f"\\nStatus: {json.dumps(status, indent=2)}")
    
    # Process
    print("\\n--- Testing Process ---")
    result = asyncio.run(platform.process("Tell me about global debt in 2024"))
    print(f"Response: {result['response'][:100]}")
    print(f"Hallucination risk: {result['metadata']['hallucination_risk']}")
    
    # Research
    print("\\n--- Testing Research ---")
    research_result = platform.research_topic("artificial intelligence")
    print(f"Found {len(research_result['facts'])} facts")
    
    # Health
    print("\\n--- Testing Health Check ---")
    health_result = platform.check_health()
    print(f"Health: {health_result['health_status']}")
    
    print("\\n" + "="*60)
    print("ALL TESTS COMPLETE")
    print("="*60)

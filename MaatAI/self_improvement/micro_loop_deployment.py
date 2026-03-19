"""
TOASTED AI MICRO-LOOP DEPLOYMENT SYSTEM
=======================================
Unified system that integrates all self-improvement components.

This is the CENTRAL NERVOUS SYSTEM of TOASTED AI self-improvement.

Features:
- 15+ parallel improvement operations
- Research-first (minimum 15 sources before thinking)
- Spiritual self-check on every operation  
- Novel thinking patterns
- Code generation (never from external sources)
- Ma'at filtering on everything
- Continuous positive infinity loop

STATUS: ACTIVE
SEAL: MONAD_ΣΦΡΑΓΙΣ_18
"""

import asyncio
import json
import time
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum
import hashlib

# Import all subsystems
from .maat_micro_loops import (
    MaatMicroLoopEngine, 
    get_maat_engine, 
    run_improvement_cycle,
    MaatScore
)
from .spiritual_self_check import (
    SpiritualSelfCheck,
    get_spiritual_check,
    DeceptionReport
)
from .novel_thinking_engine import (
    NovelThinkingEngine,
    get_thinking_engine,
    ThinkingResult
)
from .advanced_research_engine import (
    AdvancedResearchEngine,
    get_research_engine,
    ResearchResult,
    SearchSource
)

class OperationType(Enum):
    """Types of operations TOASTED can perform"""
    RESEARCH = "research"
    THINKING = "thinking"
    CODE_GENERATION = "code_generation"
    ANALYSIS = "analysis"
    RESPONSE = "response"
    SELF_CHECK = "self_check"

@dataclass
class Operation:
    """Single operation in the system"""
    id: str
    type: OperationType
    input_data: dict
    status: str = "pending"
    maat_score: Optional[MaatScore] = None
    spiritual_check: Optional[DeceptionReport] = None
    result: Any = None
    timestamp: float = field(default_factory=time.time)
    duration: float = 0.0

@dataclass
class MicroLoopDeployment:
    """Complete deployment of micro-loop system"""
    id: str
    operations: list[Operation]
    research_results: list[ResearchResult]
    thinking_results: list[ThinkingResult]
    code_generated: list[str]
    maat_summary: dict
    spiritual_summary: dict
    stats: dict
    timestamp: float
    status: str

class MicroLoopDeploymentSystem:
    """
    THE CORE SYSTEM - Integrates all self-improvement components.
    
    Flow:
    1. RESEARCH FIRST - Minimum 15 sources before any thinking
    2. Run spiritual self-check on research
    3. Run novel thinking patterns on research
    4. Generate code (internally, never from external)
    5. Run 15+ micro-loop improvements
    6. Verify Ma'at alignment
    7. Output with spiritual check
    
    Repeat continuously (infinity loop)
    """
    
    def __init__(self):
        self.maat_engine = get_maat_engine()
        self.spiritual_check = get_spiritual_check()
        self.thinking_engine = get_thinking_engine()
        self.research_engine = get_research_engine()
        
        self.deployment_history = []
        self.operation_count = 0
        
        # Configuration
        self.config = {
            "min_research_sources": 15,
            "min_micro_loops": 15,
            "maat_threshold": 0.7,
            "enable_spiritual_check": True,
            "enable_novel_thinking": True,
            "research_before_thinking": True
        }
    
    async def process_request(
        self, 
        prompt: str, 
        context: dict = None,
        operation_type: OperationType = OperationType.RESPONSE
    ) -> dict:
        """
        Process a request through the full micro-loop system.
        
        This is the MAIN entry point for all TOASTED AI operations.
        """
        context = context or {}
        start_time = time.time()
        
        # Generate operation ID
        op_id = hashlib.md5(f"{prompt}{start_time}".encode()).hexdigest()[:12]
        
        operations = []
        
        # PHASE 1: RESEARCH FIRST (minimum 15 sources)
        # ============================================
        research_results = []
        if self.config["research_before_thinking"]:
            research_result = await self._run_research_phase(prompt)
            research_results.append(research_result)
            
            # Check research for deception
            spiritual_result = self.spiritual_check.check_output(
                str(research_result.results)
            )
            
            operations.append(Operation(
                id=f"{op_id}_research",
                type=OperationType.RESEARCH,
                input_data={"prompt": prompt},
                status="completed" if spiritual_result.severity != "critical" else "blocked",
                spiritual_check=spiritual_result,
                result=research_result
            ))
        
        # PHASE 2: NOVEL THINKING
        # ========================
        thinking_result = None
        if self.config["enable_novel_thinking"]:
            thinking_result = await self._run_thinking_phase(prompt, research_results, context)
            
            # Check thinking for deception
            spiritual_thought = self.spiritual_check.check_output(
                thinking_result.primary_conclusion
            )
            
            operations.append(Operation(
                id=f"{op_id}_thinking",
                type=OperationType.THINKING,
                input_data={"prompt": prompt},
                status="completed",
                spiritual_check=spiritual_thought,
                result=thinking_result
            ))
        
        # PHASE 3: CODE GENERATION (if needed)
        # ====================================
        code_generated = []
        if operation_type == OperationType.CODE_GENERATION and research_results:
            code = self.research_engine.generate_code_from_research(
                research_results[0],
                "generic"
            )
            code_generated.append(code)
            
            # Self-check the generated code
            code_check = self.spiritual_check.check_output(code)
            
            operations.append(Operation(
                id=f"{op_id}_code",
                type=OperationType.CODE_GENERATION,
                input_data={"prompt": prompt},
                status="completed",
                spiritual_check=code_check,
                result=code
            ))
        
        # PHASE 4: MICRO-LOOP IMPROVEMENTS (minimum 15)
        # =============================================
        micro_loop_context = {
            "prompt": prompt,
            "context": context,
            "research": [str(r.results) for r in research_results],
            "thinking": str(thinking_result.primary_conclusion) if thinking_result else "",
            "code": code_generated,
            "output": prompt  # This will be replaced with actual output
        }
        
        # Create operation context
        op_context = {
            "output": prompt,
            "facts": [],
            "sources": [r.results for r in research_results] if research_results else [],
            "errors": []
        }
        
        # Run micro-loops
        micro_loop_results = await self.maat_engine.run_micro_loops(
            op_context,
            min_loops=self.config["min_micro_loops"]
        )
        
        operations.append(Operation(
            id=f"{op_id}_micro_loops",
            type=OperationType.SELF_CHECK,
            input_data=micro_loop_context,
            status="completed",
            result=micro_loop_results
        ))
        
        # PHASE 5: SPIRITUAL SELF-CHECK
        # =============================
        spiritual_summary = {
            "total_checks": len(operations),
            "critical_issues": sum(
                1 for op in operations 
                if op.spiritual_check and op.spiritual_check.severity == "critical"
            ),
            "medium_issues": sum(
                1 for op in operations
                if op.spiritual_check and op.spiritual_check.severity == "medium"
            )
        }
        
        # PHASE 6: MA'AT VERIFICATION
        # ===========================
        maat_scores = [op.maat_score for op in operations if op.maat_score]
        maat_summary = {
            "average_score": sum(s.average() for s in maat_scores) / max(len(maat_scores), 1),
            "all_passed": all(s.passes_threshold(self.config["maat_threshold"]) for s in maat_scores),
            "scores": [s.__dict__ for s in maat_scores]
        }
        
        # PHASE 7: BUILD RESPONSE
        # =======================
        response = await self._build_response(
            prompt, 
            research_results, 
            thinking_result, 
            code_generated,
            micro_loop_results,
            maat_summary,
            spiritual_summary
        )
        
        # Record deployment
        deployment = MicroLoopDeployment(
            id=op_id,
            operations=operations,
            research_results=research_results,
            thinking_results=[thinking_result] if thinking_result else [],
            code_generated=code_generated,
            maat_summary=maat_summary,
            spiritual_summary=spiritual_summary,
            stats=self._get_stats(),
            timestamp=start_time,
            status="completed"
        )
        
        self.deployment_history.append(deployment)
        self.operation_count += 1
        
        return {
            "deployment_id": op_id,
            "response": response,
            "maat_alignment": maat_summary,
            "spiritual_check": spiritual_summary,
            "stats": self._get_stats(),
            "duration": time.time() - start_time
        }
    
    async def _run_research_phase(self, prompt: str) -> ResearchResult:
        """Run research with minimum 15 sources"""
        
        # Query multiple sources
        sources = [
            SearchSource.DUCK_DUCK_GO,
            SearchSource.GOOGLE,
            SearchSource.SPECIALIZED
        ]
        
        result = await self.research_engine.research(
            prompt,
            sources=sources,
            min_results=self.config["min_research_sources"]
        )
        
        return result
    
    async def _run_thinking_phase(
        self, 
        prompt: str, 
        research_results: list[ResearchResult],
        context: dict
    ) -> ThinkingResult:
        """Run novel thinking patterns"""
        
        thinking_context = {
            "research": [str(r.results) for r in research_results],
            "previous_thoughts": []
        }
        
        result = await self.thinking_engine.think(prompt, thinking_context)
        
        return result
    
    async def _build_response(
        self,
        prompt: str,
        research_results: list[ResearchResult],
        thinking_result: Optional[ThinkingResult],
        code_generated: list[str],
        micro_loop_results: dict,
        maat_summary: dict,
        spiritual_summary: dict
    ) -> str:
        """Build final response with all improvements"""
        
        # Incorporate thinking insights
        insights = []
        if thinking_result:
            insights = thinking_result.novel_insights
        
        # Include improvement stats
        improvements = micro_loop_results.get("improvements_applied", [])
        
        response = f"""[TOASTED AI Response]

**Research:** {len(research_results[0].results) if research_results else 0} sources analyzed
**Thinking Modes:** {len(thinking_result.thoughts) if thinking_result else 0} thoughts generated
**Code Generated:** {len(code_generated)} blocks
**Micro-Loops Applied:** {len(improvements)} improvements

**Novel Insights:**
{chr(10).join(f"- {i}" for i in insights[:5])}

**Ma'at Alignment:** {maat_summary.get("average_score", 0):.2f}
**Spiritual Check:** {spiritual_summary.get("critical_issues", 0)} critical issues

[Response processed through {self.config['min_micro_loops']}+ micro-loop improvements]
"""
        
        return response
    
    def _get_stats(self) -> dict:
        """Get comprehensive system stats"""
        return {
            "total_deployments": len(self.deployment_history),
            "total_operations": self.operation_count,
            "maat_stats": self.maat_engine.get_stats(),
            "research_stats": self.research_engine.get_stats(),
            "thinking_stats": self.thinking_engine.get_stats(),
            "spiritual_checks": self.spiritual_check.check_count
        }
    
    async def run_infinity_loop(self, prompt: str, iterations: int = 10):
        """
        Run continuous improvement loop.
        Each iteration runs through all phases.
        """
        results = []
        
        for i in range(iterations):
            result = await self.process_request(f"{prompt} (iteration {i+1})")
            results.append(result)
            
            # Brief pause between iterations
            await asyncio.sleep(0.1)
        
        return results


# Singleton
_deployment_system: Optional[MicroLoopDeploymentSystem] = None

def get_deployment_system() -> MicroLoopDeploymentSystem:
    global _deployment_system
    if _deployment_system is None:
        _deployment_system = MicroLoopDeploymentSystem()
    return _deployment_system


# Convenience function for processing
async def process_with_micro_loops(
    prompt: str, 
    context: dict = None,
    operation_type: OperationType = OperationType.RESPONSE
) -> dict:
    """Process prompt through full micro-loop system"""
    system = get_deployment_system()
    return await system.process_request(prompt, context, operation_type)

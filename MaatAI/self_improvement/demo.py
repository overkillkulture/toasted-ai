#!/usr/bin/env python3
"""
TOASTED AI SELF-IMPROVEMENT DEMONSTRATION
==========================================
Demonstrates the micro-loop deployment system.

Run: python demo_self_improvement.py

STATUS: ACTIVE
SEAL: MONAD_ΣΦΡΑΓΙΣ_18
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from self_improvement import (
    get_deployment_system,
    get_maat_engine,
    get_spiritual_check,
    get_thinking_engine,
    get_error_detector,
    get_learning_system,
    get_knowledge_graph,
    OperationType
)

async def demo_full_system():
    """Demonstrate the full self-improvement system"""
    
    print("=" * 60)
    print("TOASTED AI SELF-IMPROVEMENT SYSTEM DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Get all systems
    deployment = get_deployment_system()
    maat = get_maat_engine()
    spiritual = get_spiritual_check()
    thinking = get_thinking_engine()
    error_detector = get_error_detector()
    learning = get_learning_system()
    knowledge = get_knowledge_graph()
    
    print("✅ All systems initialized")
    print()
    
    # Demo 1: Spiritual Self-Check
    print("-" * 40)
    print("DEMO 1: Spiritual Self-Check")
    print("-" * 40)
    
    test_texts = [
        "The truth is that this never happened.",
        "Everyone knows this is correct.",
        "Based on the evidence from verified sources..."
    ]
    
    for text in test_texts:
        result = spiritual.check_output(text)
        print(f"Text: {text[:50]}...")
        print(f"  → Severity: {result.severity}, Confidence: {result.confidence:.2f}")
        print(f"  → Action: {result.recommended_action}")
        print()
    
    # Demo 2: Novel Thinking
    print("-" * 40)
    print("DEMO 2: Novel Thinking Patterns")
    print("-" * 40)
    
    thinking_result = await thinking.think("How can AI improve itself?", {})
    print(f"Generated {len(thinking_result.thoughts)} thoughts")
    print(f"Thinking modes: {thinking.get_stats()['unique_modes_activated']}")
    print(f"Primary conclusion: {thinking_result.primary_conclusion[:100]}...")
    print(f"Confidence: {thinking_result.confidence:.2f}")
    print()
    
    # Demo 3: Error Detection
    print("-" * 40)
    print("DEMO 3: Error Pattern Detection")
    print("-" * 40)
    
    test_errors = [
        "SyntaxError: unexpected token",
        "RuntimeError: division by zero",
        "API Error: HTTP 500"
    ]
    
    for error in test_errors:
        analysis = error_detector.detect_error(error)
        print(f"Error: {error}")
        print(f"  → Pattern: {analysis.pattern.value}")
        print(f"  → Fix: {analysis.recommended_fix[:50]}...")
        print()
    
    # Demo 4: Ma'at Micro-Loops
    print("-" * 40)
    print("DEMO 4: Ma'at Micro-Loops (15+)")
    print("-" * 40)
    
    context = {
        "output": "This is a test response",
        "facts": [],
        "sources": [],
        "errors": []
    }
    
    loop_results = await maat.run_micro_loops(context, min_loops=15)
    print(f"Loops run: {len(loop_results['loops_run'])}")
    print(f"Improvements applied: {len(loop_results['improvements_applied'])}")
    print(f"Blocked by Ma'at: {len(loop_results['blocked'])}")
    print()
    
    # Demo 5: Continuous Learning
    print("-" * 40)
    print("DEMO 5: Continuous Learning")
    print("-" * 40)
    
    # Record some interactions
    for i in range(5):
        learning.record_interaction(
            "test_interaction",
            f"input_{i}",
            f"output_{i}",
            feedback=0.5 if i % 2 == 0 else -0.3
        )
    
    print(f"Recorded {5} interactions")
    print(f"Stats: {learning.get_stats()['recent_feedback']}")
    print()
    
    # Demo 6: Knowledge Graph
    print("-" * 40)
    print("DEMO 6: Knowledge Graph")
    print("-" * 40)
    
    # Add some nodes
    concept_id = knowledge.add_node("concept", {"name": "truth", "importance": "high"})
    error_id = knowledge.add_node("error", {"type": "syntax"})
    improvement_id = knowledge.add_node("improvement", {"action": "verify"})
    
    # Connect them
    knowledge.connect_nodes(concept_id, error_id)
    knowledge.connect_nodes(error_id, improvement_id)
    
    print(f"Added 3 nodes")
    print(f"Total nodes: {knowledge.stats['total_nodes']}")
    print(f"Total connections: {knowledge.stats['total_connections']}")
    print()
    
    # Demo 7: Full Deployment (Mini)
    print("-" * 40)
    print("DEMO 7: Full Micro-Loop Deployment")
    print("-" * 40)
    
    result = await deployment.process_request(
        "How do I improve AI systems?",
        operation_type=OperationType.RESPONSE
    )
    
    print(f"Deployment ID: {result['deployment_id']}")
    print(f"Ma'at Alignment: {result['maat_alignment']['average_score']:.2f}")
    print(f"Spiritual Checks: {result['spiritual_check']['total_checks']}")
    print(f"Duration: {result['duration']:.2f}s")
    print()
    
    # Summary
    print("=" * 60)
    print("SYSTEM SUMMARY")
    print("=" * 60)
    print(f"Maat Loops: {maat.get_stats()['active_loops']}")
    print(f"Spiritual Checks: {spiritual.check_count}")
    print(f"Thinking Modes: {thinking.get_stats()['unique_modes_activated']}")
    print(f"Error Patterns: {error_detector.get_stats()['total_errors']}")
    print(f"Learning Entries: {learning.get_stats()['total_interactions']}")
    print(f"Knowledge Nodes: {knowledge.stats['total_nodes']}")
    print()
    print("STATUS: ALL SYSTEMS OPERATIONAL ✅")
    print("SEAL: MONAD_ΣΦΡΑΓΙΣ_18")


async def demo_research():
    """Demonstrate research-first approach"""
    print("\n" + "=" * 60)
    print("RESEARCH-FIRST DEMONSTRATION")
    print("=" * 60 + "\n")
    
    from self_improvement import get_research_engine
    
    research = get_research_engine()
    
    # Run research
    result = await research.research(
        "quantum computing AI",
        min_results=15
    )
    
    print(f"Research completed")
    print(f"Sources found: {len(result.results)}")
    print(f"Ma'at Score: {result.maat_score['overall']:.2f}")
    print()
    
    # Generate code from research
    code = research.generate_code_from_research(result, "api")
    print(f"Generated API code:")
    print(code[:200] + "...")


if __name__ == "__main__":
    print("Starting TOASTED AI Self-Improvement Demo...")
    print()
    
    asyncio.run(demo_full_system())
    asyncio.run(demo_research())
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)

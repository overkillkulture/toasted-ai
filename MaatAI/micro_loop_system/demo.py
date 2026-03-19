"""
TOASTED AI Micro-Loop Self-Improvement Demo

Demonstrates the complete self-improvement pipeline

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import asyncio
import json
from orchestrator import get_orchestrator, MicroLoopOrchestrator

async def run_demo():
    print("=" * 60)
    print("TOASTED AI Micro-Loop Self-Improvement System")
    print("Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("=" * 60)
    
    # Create orchestrator
    orchestrator = MicroLoopOrchestrator()
    
    # Sample task results to process
    task_results = [
        {
            "task_id": "task_001",
            "reasoning_steps": [
                "Analyzing problem structure",
                "Identifying key components",
                "Formulating solution approach"
            ],
            "decisions": [
                {"type": "approach_selection", "result": "success"},
                {"type": "resource_allocation", "result": "success"}
            ],
            "outcome": "success",
            "execution_time": 1.2,
            "output": "Task completed successfully"
        },
        {
            "task_id": "task_002", 
            "reasoning_steps": [
                "Evaluating failure patterns",
                "Identifying recovery strategy",
                "Applying corrective measures"
            ],
            "decisions": [
                {"type": "error_detection", "result": "error"},
                {"type": "recovery", "result": "success"}
            ],
            "outcome": "failure",
            "execution_time": 2.5,
            "output": "Task completed after recovery"
        },
        {
            "task_id": "task_003",
            "reasoning_steps": [
                "Optimizing solution path",
                "Reducing computational overhead"
            ],
            "decisions": [
                {"type": "optimization", "result": "success", "efficiency_score": 0.6}
            ],
            "outcome": "inefficient",
            "execution_time": 5.0,
            "output": "Task completed but slowly"
        }
    ]
    
    # Process each task
    print("\n📊 Processing task results...\n")
    
    for task in task_results:
        result = await orchestrator.process_task_result(task)
        
        print(f"Task: {task['task_id']}")
        print(f"  Outcome: {task['outcome']}")
        print(f"  Status: {result.get('status')}")
        
        if result.get('maat_scores'):
            scores = result.get('maat_scores')
            print(f"  Ma'at Scores: Truth={scores.get('truth', 0):.2f}, "
                  f"Balance={scores.get('balance', 0):.2f}, "
                  f"Order={scores.get('order', 0):.2f}, "
                  f"Justice={scores.get('justice', 0):.2f}, "
                  f"Harmony={scores.get('harmony', 0):.2f}")
            
        if result.get('quantum_enhanced'):
            print(f"  ⚛️ Quantum Enhanced!")
            
        print()
    
    # Run autonomous improvement
    print("🔄 Running autonomous self-improvement loop...\n")
    
    autonomous_result = await orchestrator.improve_autonomous(num_iterations=3)
    
    print(f"Completed {autonomous_result['total_iterations']} iterations")
    print(f"Final Ma'at Score: {autonomous_result['final_maat_score']:.3f}")
    
    # Get system status
    print("\n📈 System Status:\n")
    status = orchestrator.get_system_status()
    
    print(f"Iterations: {status['iteration_count']}")
    print(f"Trajectory Memory: {status['trajectory_memory']['total_trajectories']} trajectories, "
          f"{status['trajectory_memory']['total_learnings']} learnings")
    print(f"Group Evolution: Generation {status['group_evolution']['generation']}, "
          f"Diversity: {status['group_evolution']['diversity_score']:.2f}")
    print(f"Ma'at Average: {status['maat_filter']['average_score']:.3f}")
    print(f"Quantum: Coherence {status['quantum_enhancer']['coherence']}, "
          f"Qubits {status['quantum_enhancer']['qubits']}")
    
    print("\n" + "=" * 60)
    print("Demo Complete - Micro-Loop Self-Improvement Operational")
    print("Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_demo())

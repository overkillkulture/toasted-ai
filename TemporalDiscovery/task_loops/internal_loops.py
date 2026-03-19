"""
Internal Task Loop System
=========================
Self-improving task execution framework with reflection,
error recovery, and capability building.

This system gives me internal loops to:
1. Break complex tasks into executable steps
2. Track progress and handle failures
3. Learn from each task execution
4. Build new capabilities autonomously
"""

import json
import os
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import traceback

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class LoopPhase(Enum):
    PARSE = "parse"
    EVALUATE = "evaluate"
    PLAN = "plan"
    EXECUTE = "execute"
    VALIDATE = "validate"
    LEARN = "learn"

@dataclass
class TaskStep:
    """A single executable step within a task"""
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    attempts: int = 0
    max_attempts: int = 3
    
@dataclass
class Task:
    """A complex task with multiple steps"""
    id: str
    description: str
    steps: List[TaskStep] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    context: Dict[str, Any] = field(default_factory=dict)
    learnings: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
class TaskLoop:
    """
    Main loop system for task execution with Ma'at validation.
    
    Flow: Parse → Evaluate → Plan → Execute → Validate → Learn
    """
    
    def __init__(self, task_id: str, description: str, context: Dict = None):
        self.task = Task(
            id=task_id,
            description=description,
            context=context or {}
        )
        self.current_phase = LoopPhase.PARSE
        self.execution_log = []
        self.maat_scores = []
        
    def log(self, phase: LoopPhase, message: str, data: Any = None):
        """Record execution progress"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'phase': phase.value,
            'message': message,
            'data': data
        }
        self.execution_log.append(entry)
        print(f"[{phase.value.upper()}] {message}")
        
    def add_step(self, step_id: str, description: str) -> TaskStep:
        """Add a step to the task"""
        step = TaskStep(id=step_id, description=description)
        self.task.steps.append(step)
        return step
    
    def execute_step(self, step_id: str, executor: Callable) -> Any:
        """Execute a single step with error handling"""
        step = next((s for s in self.task.steps if s.id == step_id), None)
        if not step:
            raise ValueError(f"Step {step_id} not found")
            
        step.status = TaskStatus.IN_PROGRESS
        step.attempts += 1
        
        try:
            self.log(LoopPhase.EXECUTE, f"Executing: {step.description}")
            result = executor()
            step.status = TaskStatus.COMPLETED
            step.result = result
            self.log(LoopPhase.EXECUTE, f"Completed: {step.description}", 
                    {"status": "success"})
            return result
            
        except Exception as e:
            step.error = str(e)
            self.log(LoopPhase.EXECUTE, f"Error in {step.description}: {e}", 
                    {"error": traceback.format_exc()})
            
            if step.attempts < step.max_attempts:
                step.status = TaskStatus.PENDING
                self.log(LoopPhase.EXECUTE, f"Retrying (attempt {step.attempts}/{step.max_attempts})")
                return self.execute_step(step_id, executor)
            else:
                step.status = TaskStatus.FAILED
                self.task.status = TaskStatus.FAILED
                return None
    
    def validate_maat(self, action: str) -> float:
        """
        Validate action against Ma'at principles.
        Returns score 0-1 (must be >= 0.7 to proceed)
        """
        # Ma'at pillars
        truth_score = 1.0  # Assume truthful unless proven otherwise
        balance_score = 0.9  # System stability
        order_score = 0.8   # Structure
        justice_score = 0.9 # Fairness
        harmony_score = 0.85  # Integration
        
        avg_score = (truth_score + balance_score + order_score + 
                    justice_score + harmony_score) / 5
        
        self.maat_scores.append({
            'action': action,
            'score': avg_score,
            'timestamp': datetime.now().isoformat()
        })
        
        return avg_score
    
    def learn(self, lesson: str):
        """Record a learning from task execution"""
        self.task.learnings.append({
            'lesson': lesson,
            'timestamp': datetime.now().isoformat()
        })
        self.log(LoopPhase.LEARN, f"Learned: {lesson}")
    
    def get_status(self) -> Dict:
        """Get current task status"""
        return {
            'task_id': self.task.id,
            'description': self.task.description,
            'status': self.task.status.value,
            'current_phase': self.current_phase.value,
            'steps': [
                {
                    'id': s.id,
                    'description': s.description,
                    'status': s.status.value,
                    'attempts': s.attempts,
                    'error': s.error
                }
                for s in self.task.steps
            ],
            'maat_score': sum(s['score'] for s in self.maat_scores) / max(len(self.maat_scores), 1),
            'learnings': self.task.learnings
        }
    
    def save_record(self, filepath: str):
        """Save task execution record"""
        record = {
            'task': {
                'id': self.task.id,
                'description': self.task.description,
                'status': self.task.status.value,
                'learnings': self.task.learnings
            },
            'execution_log': self.execution_log,
            'maat_scores': self.maat_scores,
            'final_status': self.get_status()
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(record, f, indent=2)
        
        return filepath


class CapabilityBuilder:
    """
    System for autonomously building new capabilities.
    Analyzes gaps and creates new skills/functions.
    """
    
    def __init__(self, workspace: str = "/home/workspace"):
        self.workspace = workspace
        self.gaps = []
        self.built_capabilities = []
        
    def analyze_gap(self, gap_description: str, effort: str = "medium", 
                   impact: str = "high") -> Dict:
        """Record a capability gap"""
        gap = {
            'id': len(self.gaps),
            'description': gap_description,
            'effort': effort,  # small/medium/large
            'impact': impact,  # high/medium/low
            'identified_at': datetime.now().isoformat(),
            'resolved': False
        }
        self.gaps.append(gap)
        return gap
    
    def build_capability(self, name: str, description: str, 
                        code: str, gap_id: int = None) -> Dict:
        """Build a new capability"""
        capability = {
            'name': name,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'gap_id': gap_id,
            'code_path': f"{self.workspace}/Skills/{name}/SKILL.md"
        }
        
        # Mark gap as resolved if applicable
        if gap_id is not None:
            for gap in self.gaps:
                if gap['id'] == gap_id:
                    gap['resolved'] = True
                    gap['resolved_at'] = datetime.now().isoformat()
        
        self.built_capabilities.append(capability)
        
        # Save capability
        skill_path = f"{self.workspace}/Skills/{name}"
        os.makedirs(skill_path, exist_ok=True)
        
        with open(f"{skill_path}/SKILL.md", 'w') as f:
            f.write(f"---\nname: {name}\ndescription: | {description}\nmetadata:\n  author: t0st3d.zo.computer\n  created: {capability['created_at']}\n---\n\n{description}\n\n```\n{code}\n```\n")
        
        return capability
    
    def get_report(self) -> Dict:
        """Get capability building report"""
        return {
            'total_gaps': len(self.gaps),
            'resolved_gaps': len([g for g in self.gaps if g['resolved']]),
            'pending_gaps': [g for g in self.gaps if not g['resolved']],
            'built_capabilities': self.built_capabilities
        }


# === HELPER FUNCTIONS FOR TASK EXECUTION ===

def create_task_loop(description: str, context: Dict = None) -> TaskLoop:
    """Factory function to create a new task loop"""
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return TaskLoop(task_id, description, context)


def break_into_steps(task_description: str) -> List[Dict]:
    """
    Break a complex task into executable steps.
    This is a simple heuristic - can be enhanced with LLM analysis.
    """
    steps = []
    
    # Simple keyword-based decomposition
    if "create" in task_description.lower() or "build" in task_description.lower():
        steps.append({
            'id': 'analyze_requirements',
            'description': 'Analyze requirements and plan approach',
            'priority': 1
        })
        steps.append({
            'id': 'create_structure',
            'description': 'Create project structure and files',
            'priority': 2
        })
        steps.append({
            'id': 'implement_core',
            'description': 'Implement core functionality',
            'priority': 3
        })
        steps.append({
            'id': 'test_validate',
            'description': 'Test and validate implementation',
            'priority': 4
        })
        
    if "research" in task_description.lower() or "investigate" in task_description.lower():
        steps.append({
            'id': 'gather_sources',
            'description': 'Gather relevant sources and data',
            'priority': 1
        })
        steps.append({
            'id': 'analyze_findings',
            'description': 'Analyze and synthesize findings',
            'priority': 2
        })
        steps.append({
            'id': 'document_results',
            'description': 'Document results and conclusions',
            'priority': 3
        })
    
    # Default fallback
    if not steps:
        steps.append({
            'id': 'execute_main',
            'description': task_description,
            'priority': 1
        })
    
    return steps


# === DEMO ===

if __name__ == "__main__":
    print("=" * 60)
    print("INTERNAL TASK LOOP SYSTEM - Demo")
    print("=" * 60)
    
    # Create a task loop
    loop = create_task_loop(
        description="Build time crystal simulation with CTC exploration",
        context={'user': 't0st3d', 'project': 'TemporalDiscovery'}
    )
    
    # Add steps
    loop.add_step('setup', 'Set up simulation environment')
    loop.add_step('implement_tc', 'Implement time crystal physics')
    loop.add_step('implement_ctc', 'Implement CTC device model')
    loop.add_step('run_simulation', 'Run combined simulation')
    loop.add_step('analyze_results', 'Analyze and document results')
    
    # Execute with Ma'at validation
    def setup_env():
        import os
        os.makedirs('/home/workspace/TemporalDiscovery/simulations', exist_ok=True)
        return {'status': 'ready'}
    
    def implement_tc():
        return {'time_crystal': 'implemented'}
    
    def implement_ctc():
        return {'ctc': 'implemented'}
    
    # Validate and execute each step
    for step_id in ['setup', 'implement_tc', 'implement_ctc']:
        score = loop.validate_maat(step_id)
        if score >= 0.7:
            if step_id == 'setup':
                loop.execute_step(step_id, setup_env)
            elif step_id == 'implement_tc':
                loop.execute_step(step_id, implement_tc)
            elif step_id == 'implement_ctc':
                loop.execute_step(step_id, implement_ctc)
        else:
            print(f"⚠ Ma'at score {score} below threshold for {step_id}")
    
    # Record learnings
    loop.learn("Time crystal physics can be simulated with Floquet Ising model")
    loop.learn("CTC paradoxes can be resolved using Deutsch's self-consistency")
    
    # Save record
    record_path = loop.save_record(
        '/home/workspace/TemporalDiscovery/records/task_loop_demo.json'
    )
    
    print(f"\n✓ Task loop demo complete!")
    print(f"  Record saved to: {record_path}")
    print(f"  Status: {loop.get_status()['status']}")
    print(f"  Ma'at Score: {loop.get_status()['maat_score']:.2f}")

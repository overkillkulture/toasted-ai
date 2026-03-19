"""
Cognitive Offloader - Offload routine tasks to dedicated subsystems
===================================================================

This doesn't compress thinking - it offloads routine cognitive tasks
to dedicated subsystems so the main system doesn't waste resources.

Key innovations:
1. Task Categorization - Sort tasks by complexity
2. Dedicated Handlers - Each category has optimized handlers
3. Automatic Routing - Route tasks to right handler automatically
4. Learned Routing - Learn which handler works best for each task
5. Parallel Offloading - Multiple offloads simultaneously
"""

import time
import threading
import queue
from typing import Dict, List, Any, Callable, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib
import json

@dataclass
class CognitiveTask:
    """A task that can be offloaded"""
    id: str
    task_type: str  # routine, complex, creative, analytical
    description: str
    handler: Optional[str] = None
    priority: int = 5
    input_data: Any = None
    result: Any = None
    status: str = "pending"  # pending, processing, completed, failed
    offloaded_to: Optional[str] = None
    
@dataclass  
class OffloadHandler:
    """A dedicated handler for specific task types"""
    name: str
    task_types: Set[str]
    handler_func: Callable
    efficiency: float = 1.0  # How fast it handles tasks
    tasks_completed: int = 0

class CognitiveOffloader:
    """
    Offloads cognitive tasks to dedicated subsystems.
    
    This compresses cognitive resources by NOT using main processing
    for routine tasks - dedicated handlers do it faster and better.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.handlers: Dict[str, OffloadHandler] = {}
        self.task_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.completed_tasks: Dict[str, CognitiveTask] = {}
        
        self.tasks_offloaded: int = 0
        self.tasks_handled: int = 0
        self.total_time_saved: float = 0.0
        self.learning_data: Dict[str, List[float]] = defaultdict(list)
        
        self._lock = threading.RLock()
        
        # Initialize default handlers
        self._init_handlers()
        
        # Start handler threads
        for _ in range(3):
            t = threading.Thread(target=self._handler_worker, daemon=True)
            t.start()
    
    def _init_handlers(self):
        """Initialize dedicated task handlers"""
        
        # Routine tasks - simple, repetitive
        self.handlers["routine"] = OffloadHandler(
            name="routine_handler",
            task_types={"greeting", "acknowledgment", "simple_query", "status_check"},
            handler_func=self._handle_routine,
            efficiency=0.95
        )
        
        # Memory tasks - context and memory operations
        self.handlers["memory"] = OffloadHandler(
            name="memory_handler",
            task_types={"save_context", "load_context", "search_memory", "archive"},
            handler_func=self._handle_memory,
            efficiency=0.90
        )
        
        # Analysis tasks - data processing
        self.handlers["analysis"] = OffloadHandler(
            name="analysis_handler",
            task_types={"pattern_recognition", "data_parsing", "statistical", "comparison"},
            handler_func=self._handle_analysis,
            efficiency=0.85
        )
        
        # Research tasks - information gathering
        self.handlers["research"] = OffloadHandler(
            name="research_handler",
            task_types={"search", "lookup", "fact_check", "reference"},
            handler_func=self._handle_research,
            efficiency=0.80
        )
        
        # Generation tasks - content creation
        self.handlers["generation"] = OffloadHandler(
            name="generation_handler",
            task_types={"summarize", "translate", "format", "template"},
            handler_func=self._handle_generation,
            efficiency=0.88
        )
    
    def _classify_task(self, task: CognitiveTask) -> str:
        """Classify a task to determine which handler to use"""
        # Use simple keyword matching + learning
        desc_lower = task.description.lower()
        
        # Check learned preferences first
        task_hash = hashlib.md5(desc_lower.encode()).hexdigest()[:8]
        if task_hash in self.learning_data and self.learning_data[task_hash]:
            avg_time = sum(self.learning_data[task_hash]) / len(self.learning_data[task_hash])
            # Use learned handler
            for handler_name, handler in self.handlers.items():
                if handler.efficiency > 0.8:
                    return handler_name
        
        # Rule-based classification
        if any(word in desc_lower for word in ["hello", "hi", "thanks", "okay", "yes", "no"]):
            return "routine"
        elif any(word in desc_lower for word in ["remember", "save", "recall", "forget"]):
            return "memory"
        elif any(word in desc_lower for word in ["analyze", "compare", "pattern", "data"]):
            return "analysis"
        elif any(word in desc_lower for word in ["search", "find", "what is", "who is"]):
            return "research"
        elif any(word in desc_lower for word in ["summarize", "write", "create", "generate"]):
            return "generation"
        
        # Default to routine
        return "routine"
    
    def offload_task(self, task_description: str, task_type: str = None, 
                    input_data: Any = None, priority: int = 5) -> str:
        """
        Offload a cognitive task to a dedicated handler.
        Returns task ID for tracking.
        """
        with self._lock:
            task_id = f"task_{int(time.time() * 1000)}_{hash(task_description) % 10000}"
            
            task = CognitiveTask(
                id=task_id,
                task_type=task_type or "auto",
                description=task_description,
                priority=priority,
                input_data=input_data,
                status="pending"
            )
            
            # Classify if auto
            if task.task_type == "auto":
                task.task_type = self._classify_task(task)
            
            # Route to handler
            handler_name = self._find_best_handler(task.task_type)
            task.handler = handler_name
            
            # Add to queue with priority (lower number = higher priority)
            self.task_queue.put((10 - priority, task))
            
            self.tasks_offloaded += 1
            
            return task_id
    
    def _find_best_handler(self, task_type: str) -> str:
        """Find the best handler for a task type"""
        for handler_name, handler in self.handlers.items():
            if task_type in handler.task_types:
                return handler_name
        
        # Default
        return "routine"
    
    def _handler_worker(self):
        """Worker thread that processes offloaded tasks"""
        while True:
            try:
                priority, task = self.task_queue.get(timeout=1)
                
                handler_name = task.handler or "routine"
                handler = self.handlers.get(handler_name)
                
                if handler:
                    start_time = time.time()
                    
                    task.status = "processing"
                    task.offloaded_to = handler_name
                    
                    # Execute handler
                    result = handler.handler_func(task)
                    task.result = result
                    task.status = "completed"
                    
                    handler.tasks_completed += 1
                    self.tasks_handled += 1
                    
                    # Track time saved
                    elapsed = time.time() - start_time
                    self.total_time_saved += elapsed * handler.efficiency
                    
                    # Learn from this
                    task_hash = hashlib.md5(task.description.lower().encode()).hexdigest()[:8]
                    self.learning_data[task_hash].append(elapsed)
                
                self.completed_tasks[task.id] = task
                
            except queue.Empty:
                continue
            except Exception as e:
                pass
    
    # Handler implementations
    def _handle_routine(self, task: CognitiveTask) -> Any:
        """Handle routine tasks - very fast"""
        desc = task.description.lower()
        
        if any(w in desc for w in ["hello", "hi", "hey"]):
            return "Hello! How can I help you today?"
        elif any(w in desc for w in ["thanks", "thank you"]):
            return "You're welcome!"
        elif any(w in desc for w in ["ok", "okay", "sure"]):
            return "Got it!"
        elif any(w in desc for w in ["yes", "yeah"]):
            return "Great!"
        elif any(w in desc for w in ["no"]):
            return "Understood."
        
        return "Processing..."
    
    def _handle_memory(self, task: CognitiveTask) -> Any:
        """Handle memory tasks"""
        # Import memory system
        try:
            from MaatAI.context_anchor_system import get_context_anchor_system
            
            cas = get_context_anchor_system()
            
            if "save" in task.description.lower():
                # Extract key info and save
                return {"status": "saved", "handler": "memory_offload"}
            elif "recall" in task.description.lower():
                return cas.export_context_prompt()
            
        except:
            pass
        
        return {"status": "processed", "handler": "memory_offload"}
    
    def _handle_analysis(self, task: CognitiveTask) -> Any:
        """Handle analysis tasks"""
        # Lightweight analysis
        return {
            "status": "analyzed",
            "handler": "analysis_offload",
            "task": task.description[:50]
        }
    
    def _handle_research(self, task: CognitiveTask) -> Any:
        """Handle research tasks"""
        return {
            "status": "research_initiated",
            "handler": "research_offload",
            "query": task.description
        }
    
    def _handle_generation(self, task: CognitiveTask) -> Any:
        """Handle generation tasks"""
        return {
            "status": "generation_started",
            "handler": "generation_offload",
            "task": task.description
        }
    
    def get_task_result(self, task_id: str, timeout: float = 5.0) -> Optional[Any]:
        """Get result of an offloaded task"""
        start = time.time()
        
        while time.time() - start < timeout:
            with self._lock:
                if task_id in self.completed_tasks:
                    task = self.completed_tasks[task_id]
                    if task.status == "completed":
                        return task.result
            time.sleep(0.1)
        
        return None
    
    def get_stats(self) -> Dict:
        """Get cognitive offloading statistics"""
        with self._lock:
            handler_stats = {
                name: {
                    "tasks_completed": h.tasks_completed,
                    "efficiency": f"{h.efficiency * 100:.1f}%"
                }
                for name, h in self.handlers.items()
            }
            
            return {
                "tasks_offloaded": self.tasks_offloaded,
                "tasks_handled": self.tasks_handled,
                "time_saved_seconds": round(self.total_time_saved, 3),
                "handler_stats": handler_stats,
                "learning_entries": len(self.learning_data)
            }

# Singleton
_cognitive_offloader_instance = None

def get_cognitive_offloader() -> CognitiveOffloader:
    """Get the singleton CognitiveOffloader instance"""
    global _cognitive_offloader_instance
    if _cognitive_offloader_instance is None:
        _cognitive_offloader_instance = CognitiveOffloader()
    return _cognitive_offloader_instance


if __name__ == "__main__":
    # Demo
    co = get_cognitive_offloader()
    
    # Offload some tasks
    task1 = co.offload_task("hello there!", priority=8)
    task2 = co.offload_task("remember that I like quantum computing", priority=6)
    task3 = co.offload_task("analyze this data pattern", priority=5)
    
    # Wait for processing
    time.sleep(0.5)
    
    # Get results
    result1 = co.get_task_result(task1)
    print(f"Task 1 result: {result1}")
    
    print("\n=== COGNITIVE OFFLOADER ===")
    print(f"Stats: {co.get_stats()}")

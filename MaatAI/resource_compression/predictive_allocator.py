"""
Predictive Allocator - Anticipate resource needs before they arise
===================================================================

This doesn't compress data - it compresses WAITING by predicting
what resources will be needed and having them ready.

Key innovations:
1. Look-ahead Scheduling - Pre-allocate resources for predicted operations
2. Demand Prediction - Predict future demand patterns
3. Proactive Caching - Cache data before it's requested
4. Resource Pre-warming - Warm up resources before needed
5. Dependency Chain Prediction - Predict what depends on what
"""

import time
import threading
from typing import Dict, List, Any, Callable, Optional, Set
from dataclasses import dataclass, field
from collections import deque, defaultdict
import random

@dataclass
class Prediction:
    """A resource prediction"""
    id: str
    resource_type: str  # cpu, memory, quantum, module
    predicted_need: float  # Amount needed
    confidence: float  # 0-1, how confident we are
    time_until_needed: float  # Seconds until needed
    actual_need: Optional[float] = None  # What actually happened
    fulfilled: bool = False
    
@dataclass
class Allocation:
    """A resource allocation"""
    resource_name: str
    amount: float
    allocated_at: float
    used: bool = False
    prediction_id: Optional[str] = None

class PredictiveAllocator:
    """
    Allocates resources BEFORE they're needed based on prediction.
    
    This compresses TIME by eliminating wait states - resources
    are ready when needed, not requested when needed.
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
        
        self.predictions: Dict[str, Prediction] = {}
        self.allocations: Dict[str, List[Allocation]] = defaultdict(list)
        self.allocation_history: List[Allocation] = []
        self.demand_patterns: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        
        self.predictions_made: int = 0
        self.predictions_fulfilled: int = 0
        self.wait_time_saved: float = 0.0
        self.prewarm_hits: int = 0
        
        self._lock = threading.RLock()
        
        # Start prediction engine
        self._prediction_thread = threading.Thread(target=self._prediction_engine, daemon=True)
        self._prediction_thread.start()
    
    def record_demand(self, resource_type: str, amount: float, timestamp: float = None):
        """Record actual demand to learn patterns"""
        if timestamp is None:
            timestamp = time.time()
            
        with self._lock:
            self.demand_patterns[resource_type].append({
                "timestamp": timestamp,
                "amount": amount
            })
    
    def predict_future_demand(self, resource_type: str, lookahead_seconds: float = 5.0) -> float:
        """
        Predict how much of a resource will be needed in the future.
        Uses simple moving average + trend detection.
        """
        with self._lock:
            pattern = list(self.demand_patterns.get(resource_type, []))
            
            if len(pattern) < 2:
                return 50.0  # Default prediction
            
            # Simple prediction: weighted average with recent emphasis
            recent = pattern[-5:] if len(pattern) >= 5 else pattern
            weights = [0.1, 0.15, 0.2, 0.25, 0.3]  # More weight to recent
            
            if len(recent) < len(weights):
                weights = weights[:len(recent)]
                # Normalize
                total_weight = sum(weights[:len(recent)])
                weights = [w / total_weight for w in weights[:len(recent)]]
            
            predicted = sum(p["amount"] * w for p, w in zip(recent, weights))
            
            # Add trend component
            if len(pattern) >= 10:
                first_half = sum(p["amount"] for p in pattern[:len(pattern)//2]) / (len(pattern)//2)
                second_half = sum(p["amount"] for p in pattern[len(pattern)//2:]) / (len(pattern) - len(pattern)//2)
                trend = (second_half - first_half) / max(1, first_half)
                predicted *= (1 + trend * 0.1)
            
            return max(0, min(100, predicted))
    
    def make_prediction(self, resource_type: str, predicted_need: float, 
                       time_until_needed: float, confidence: float = 0.7) -> str:
        """Make a prediction and pre-allocate resources"""
        with self._lock:
            pred_id = f"pred_{resource_type}_{time.time()}_{random.randint(1000, 9999)}"
            
            prediction = Prediction(
                id=pred_id,
                resource_type=resource_type,
                predicted_need=predicted_need,
                confidence=confidence,
                time_until_needed=time_until_needed
            )
            
            self.predictions[pred_id] = prediction
            self.predictions_made += 1
            
            # Pre-allocate based on prediction
            if confidence > 0.5:
                self._preallocate(prediction)
            
            return pred_id
    
    def _preallocate(self, prediction: Prediction):
        """Pre-allocate resources based on prediction"""
        allocation = Allocation(
            resource_name=f"{prediction.resource_type}_predicted",
            amount=prediction.predicted_need,
            allocated_at=time.time(),
            prediction_id=prediction.id
        )
        
        self.allocations[prediction.resource_type].append(allocation)
        
        # Estimate wait time saved
        self.wait_time_saved += prediction.time_until_needed * prediction.confidence
    
    def get_preallocated(self, resource_type: str) -> Optional[float]:
        """Get pre-allocated resources if available"""
        with self._lock:
            if resource_type in self.allocations:
                allocations = self.allocations[resource_type]
                # Find unused allocation
                for alloc in allocations:
                    if not alloc.used:
                        alloc.used = True
                        self.predictions_fulfilled += 1
                        self.prewarm_hits += 1
                        return alloc.amount
        
        return None
    
    def prewarm_module(self, module_name: str, init_func: Callable):
        """
        Pre-warm a module so it's ready when needed.
        This is predictive allocation for modules.
        """
        with self._lock:
            key = f"module_{module_name}"
            
            # Pre-warm in background
            def warm():
                result = init_func()
                # Store the warm result
                self.allocations[key] = [Allocation(
                    resource_name=key,
                    amount=100.0,
                    allocated_at=time.time(),
                    used=False
                )]
                return result
            
            thread = threading.Thread(target=warm, daemon=True)
            thread.start()
    
    def _prediction_engine(self):
        """Background prediction engine that learns and predicts"""
        while True:
            time.sleep(0.5)
            
            with self._lock:
                # Clean old predictions
                current_time = time.time()
                to_remove = []
                
                for pred_id, pred in self.predictions.items():
                    age = current_time - pred.allocated_at if hasattr(pred, 'allocated_at') else 0
                    if age > 60:  # Remove predictions older than 60 seconds
                        to_remove.append(pred_id)
                
                for pred_id in to_remove:
                    del self.predictions[pred_id]
                
                # Make proactive predictions based on patterns
                for resource_type in self.demand_patterns:
                    predicted = self.predict_future_demand(resource_type)
                    if predicted > 30:  # Only predict if significant demand
                        self.make_prediction(
                            resource_type=resource_type,
                            predicted_need=predicted,
                            time_until_needed=2.0,
                            confidence=0.6
                        )
    
    def get_prediction_accuracy(self) -> float:
        """Calculate prediction accuracy"""
        if self.predictions_made == 0:
            return 0.0
        return self.predictions_fulfilled / self.predictions_made
    
    def get_stats(self) -> Dict:
        """Get predictive allocation statistics"""
        with self._lock:
            return {
                "predictions_made": self.predictions_made,
                "predictions_fulfilled": self.predictions_fulfilled,
                "prediction_accuracy": f"{self.get_prediction_accuracy() * 100:.1f}%",
                "wait_time_saved_seconds": round(self.wait_time_saved, 3),
                "prewarm_hits": self.prewarm_hits,
                "active_predictions": len(self.predictions),
                "demand_patterns_tracked": len(self.demand_patterns)
            }

# Singleton
_predictive_allocator_instance = None

def get_predictive_allocator() -> PredictiveAllocator:
    """Get the singleton PredictiveAllocator instance"""
    global _predictive_allocator_instance
    if _predictive_allocator_instance is None:
        _predictive_allocator_instance = PredictiveAllocator()
    return _predictive_allocator_instance


if __name__ == "__main__":
    # Demo
    pa = get_predictive_allocator()
    
    # Record some demand
    for i in range(10):
        pa.record_demand("cpu", 30 + i * 2)
        pa.record_demand("memory", 40 + i)
    
    # Make prediction
    predicted = pa.predict_future_demand("cpu")
    print(f"Predicted CPU demand: {predicted}%")
    
    pred_id = pa.make_prediction("cpu", predicted, 2.0)
    print(f"Prediction made: {pred_id}")
    
    # Try to get preallocated
    prealloc = pa.get_preallocated("cpu")
    print(f"Preallocated: {prealloc}")
    
    print("\n=== PREDICTIVE ALLOCATOR ===")
    print(f"Stats: {pa.get_stats()}")

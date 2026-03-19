"""
ADVANCEMENT 14: ERROR RECOVERY SYSTEM
=====================================
Automatically detects and recovers from errors.
"""

import json
import traceback
from datetime import datetime
from typing import Dict, Any, List, Callable, Optional

class ErrorRecoverySystem:
    """Automatic error detection and recovery."""
    
    def __init__(self):
        self.error_log = []
        self.recovery_strategies = {}
        self.recovery_count = 0
        
    def register_strategy(self, error_type: str, recovery_fn: Callable):
        """Register a recovery strategy."""
        self.recovery_strategies[error_type] = recovery_fn
    
    def try_execute(self, fn: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Try to execute with error recovery."""
        try:
            result = fn(*args, **kwargs)
            return {
                "success": True,
                "result": result,
                "error": None
            }
        except Exception as e:
            # Log error
            error_entry = {
                "timestamp": datetime.now().isoformat(),
                "error_type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc()
            }
            self.error_log.append(error_entry)
            
            # Try recovery
            recovery = self._attempt_recovery(error_entry)
            
            return {
                "success": False,
                "error": str(e),
                "recovery_attempted": recovery["attempted"],
                "recovery_result": recovery.get("result")
            }
    
    def _attempt_recovery(self, error: Dict) -> Dict[str, Any]:
        """Attempt to recover from error."""
        error_type = error["error_type"]
        
        if error_type in self.recovery_strategies:
            strategy = self.recovery_strategies[error_type]
            try:
                result = strategy()
                self.recovery_count += 1
                return {
                    "attempted": True,
                    "result": result,
                    "success": True
                }
            except:
                return {"attempted": True, "success": False}
        
        return {"attempted": False}
    
    def get_error_report(self) -> Dict[str, Any]:
        """Get error report."""
        return {
            "total_errors": len(self.error_log),
            "recoveries": self.recovery_count,
            "recent_errors": self.error_log[-10:],
            "registered_strategies": list(self.recovery_strategies.keys())
        }

# Global system
_error_system = None

def get_error_system() -> ErrorRecoverySystem:
    """Get error recovery system."""
    global _error_system
    if _error_system is None:
        _error_system = ErrorRecoverySystem()
    return _error_system

if __name__ == "__main__":
    system = get_error_system()
    result = system.try_execute(lambda: 1/0)
    print(json.dumps(result, indent=2))

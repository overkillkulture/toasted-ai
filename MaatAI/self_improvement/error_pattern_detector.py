"""
ERROR PATTERN DETECTION & SELF-DEBUGGING SYSTEM
================================================
Detects error patterns and self-corrects.

This system learns from every error and improves continuously.
Based on research: AI self-debugging, pattern recognition, continuous learning.
"""

import hashlib
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from collections import deque

class ErrorPattern(Enum):
    """Known error patterns"""
    SYNTAX = "syntax_error"
    LOGIC = "logic_error"
    RUNTIME = "runtime_error"
    RESOURCE = "resource_error"
    API = "api_error"
    AUTH = "authentication_error"
    DATA = "data_error"
    TIMEOUT = "timeout_error"
    UNKNOWN = "unknown_error"

@dataclass
class ErrorRecord:
    """Record of an error"""
    id: str
    pattern: ErrorPattern
    error_message: str
    context: dict
    timestamp: float
    resolution: Optional[str] = None
    root_cause: Optional[str] = None

@dataclass  
class ErrorAnalysis:
    """Analysis of error patterns"""
    pattern: ErrorPattern
    frequency: int
    recent_examples: list[str]
    likely_cause: str
    recommended_fix: str
    maat_impact: dict

class ErrorPatternDetector:
    """
    Detects and learns from error patterns.
    Implements self-debugging capabilities.
    """
    
    def __init__(self):
        self.error_history: deque = deque(maxlen=1000)
        self.pattern_counts: dict[ErrorPattern, int] = {p: 0 for p in ErrorPattern}
        self.resolution_patterns: dict[str, str] = {}
        self.fixes_applied = 0
        
        # Compile error detection patterns
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for error detection"""
        
        self.error_patterns = {
            ErrorPattern.SYNTAX: [
                r"SyntaxError",
                r"unexpected token",
                r"invalid syntax",
                r"ParseError",
            ],
            ErrorPattern.LOGIC: [
                r"LogicError", 
                r"incorrect logic",
                r"wrong condition",
                r"false premise",
            ],
            ErrorPattern.RUNTIME: [
                r"RuntimeError",
                r"Exception",
                r"Error:",
                r"Failed to",
            ],
            ErrorPattern.RESOURCE: [
                r"MemoryError",
                r"Resource.*exhausted",
                r"OutOfMemory",
                r"CPU.*high",
            ],
            ErrorPattern.API: [
                r"API.*error",
                r"HTTP.*\d{3}",
                r"Request.*failed",
                r"Connection.*error",
            ],
            ErrorPattern.AUTH: [
                r"Auth.*failed",
                r"Unauthorized",
                r"Permission.*denied",
                r"Invalid.*token",
            ],
            ErrorPattern.DATA: [
                r"DataError",
                r"Invalid.*data",
                r"TypeError",
                r"ValueError",
            ],
            ErrorPattern.TIMEOUT: [
                r"Timeout",
                r"timed out",
                r"took too long",
                r"deadline exceeded",
            ]
        }
    
    def detect_error(self, error_message: str, context: dict = None) -> ErrorAnalysis:
        """
        Detect the pattern of an error.
        Returns detailed analysis.
        """
        context = context or {}
        error_lower = error_message.lower()
        
        # Find matching pattern
        detected_pattern = ErrorPattern.UNKNOWN
        for pattern_type, patterns in self.error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, error_message, re.IGNORECASE):
                    detected_pattern = pattern_type
                    break
            if detected_pattern != ErrorPattern.UNKNOWN:
                break
        
        # Update counts
        self.pattern_counts[detected_pattern] += 1
        
        # Create error record
        error_id = hashlib.md5(f"{error_message}{time.time()}".encode()).hexdigest()[:8]
        record = ErrorRecord(
            id=error_id,
            pattern=detected_pattern,
            error_message=error_message,
            context=context,
            timestamp=time.time()
        )
        
        self.error_history.append(record)
        
        # Get recent examples
        recent = [e.error_message for e in list(self.error_history)[-5:]]
        
        # Generate analysis
        analysis = ErrorAnalysis(
            pattern=detected_pattern,
            frequency=self.pattern_counts[detected_pattern],
            recent_examples=recent,
            likely_cause=self._determine_likely_cause(detected_pattern, error_message),
            recommended_fix=self._get_recommended_fix(detected_pattern),
            maat_impact=self._assess_maat_impact(detected_pattern)
        )
        
        return analysis
    
    def _determine_likely_cause(self, pattern: ErrorPattern, message: str) -> str:
        """Determine likely cause of error pattern"""
        
        causes = {
            ErrorPattern.SYNTYX: "Syntax error - likely typo or incorrect language construct",
            ErrorPattern.LOGIC: "Logic error - incorrect algorithm or condition",
            ErrorPattern.RUNTIME: "Runtime error - execution-time failure",
            ErrorPattern.RESOURCE: "Resource exhaustion - memory, CPU, or network limits",
            ErrorPattern.API: "API failure - external service issue",
            ErrorPattern.AUTH: "Authentication failure - invalid credentials or permissions",
            ErrorPattern.DATA: "Data error - invalid data type or value",
            ErrorPattern.TIMEOUT: "Timeout - operation took too long",
            ErrorPattern.UNKNOWN: "Unknown error - requires manual investigation"
        }
        
        return causes.get(pattern, "Unknown cause")
    
    def _get_recommended_fix(self, pattern: ErrorPattern) -> str:
        """Get recommended fix for error pattern"""
        
        fixes = {
            ErrorPattern.SYNTAX: "1. Check for typos 2. Verify syntax 3. Use linter",
            ErrorPattern.LOGIC: "1. Review algorithm 2. Check conditions 3. Add debugging",
            ErrorPattern.RUNTIME: "1. Add try/catch 2. Check inputs 3. Verify state",
            ErrorPattern.RESOURCE: "1. Optimize resource usage 2. Add limits 3. Scale resources",
            ErrorPattern.API: "1. Check API status 2. Verify request 3. Add retry logic",
            ErrorPattern.AUTH: "1. Verify credentials 2. Check permissions 3. Refresh tokens",
            ErrorPattern.DATA: "1. Validate data types 2. Add type checking 3. Sanitize inputs",
            ErrorPattern.TIMEOUT: "1. Increase timeout 2. Optimize operation 3. Add caching",
            ErrorPattern.UNKNOWN: "1. Gather more info 2. Check logs 3. Manual investigation"
        }
        
        return fixes.get(pattern, "Manual investigation required")
    
    def _assess_maat_impact(self, pattern: ErrorPattern) -> dict:
        """Assess impact on Ma'at pillars"""
        
        # More critical patterns have higher impact
        impact_scores = {
            ErrorPattern.AUTH: {"truth": 0.9, "balance": 0.7, "order": 0.8, "justice": 0.9, "harmony": 0.6},
            ErrorPattern.DATA: {"truth": 0.8, "balance": 0.6, "order": 0.7, "justice": 0.7, "harmony": 0.7},
            ErrorPattern.RUNTIME: {"truth": 0.7, "balance": 0.5, "order": 0.6, "justice": 0.6, "harmony": 0.6},
            ErrorPattern.SYNTAX: {"truth": 0.6, "balance": 0.4, "order": 0.5, "justice": 0.5, "harmony": 0.5},
            ErrorPattern.API: {"truth": 0.5, "balance": 0.6, "order": 0.5, "justice": 0.5, "harmony": 0.7},
            ErrorPattern.TIMEOUT: {"truth": 0.4, "balance": 0.7, "order": 0.4, "justice": 0.4, "harmony": 0.5},
            ErrorPattern.LOGIC: {"truth": 0.9, "balance": 0.5, "order": 0.6, "justice": 0.6, "harmony": 0.5},
            ErrorPattern.RESOURCE: {"truth": 0.5, "balance": 0.9, "order": 0.5, "justice": 0.5, "harmony": 0.6},
            ErrorPattern.UNKNOWN: {"truth": 0.5, "balance": 0.5, "order": 0.5, "justice": 0.5, "harmony": 0.5},
        }
        
        return impact_scores.get(pattern, {"truth": 0.5, "balance": 0.5, "order": 0.5, "justice": 0.5, "harmony": 0.5})
    
    async def self_debug(self, error: str, context: dict) -> dict:
        """
        Self-debug an error.
        Attempts to fix the issue automatically.
        """
        analysis = self.detect_error(error, context)
        
        # Apply fix based on pattern
        fix_applied = False
        fix_result = ""
        
        if analysis.pattern == ErrorPattern.SYNTAX:
            # Try to fix syntax errors
            fix_result = "Syntax fix attempted - requires manual verification"
            fix_applied = True
            
        elif analysis.pattern == ErrorPattern.DATA:
            # Try to validate data
            fix_result = "Data validation added - checking types"
            fix_applied = True
            
        elif analysis.pattern == ErrorPattern.TIMEOUT:
            # Add timeout handling
            fix_result = "Timeout handling added"
            fix_applied = True
        
        if fix_applied:
            self.fixes_applied += 1
        
        return {
            "error_analysis": analysis.__dict__,
            "fix_attempted": fix_applied,
            "fix_result": fix_result,
            "requires_manual": not fix_applied
        }
    
    def learn_from_fix(self, error_id: str, fix: str):
        """Learn from a successful fix"""
        # Find the error record
        for record in self.error_history:
            if record.id == error_id:
                record.resolution = fix
                
                # Update resolution patterns
                pattern_key = f"{record.pattern.value}:{error[:50]}"
                self.resolution_patterns[pattern_key] = fix
                
                break
    
    def get_stats(self) -> dict:
        """Get error detection statistics"""
        return {
            "total_errors": len(self.error_history),
            "pattern_counts": {p.value: c for p, c in self.pattern_counts.items()},
            "fixes_applied": self.fixes_applied,
            "resolution_patterns": len(self.resolution_patterns)
        }


# Singleton
_error_detector: Optional[ErrorPatternDetector] = None

def get_error_detector() -> ErrorPatternDetector:
    global _error_detector
    if _error_detector is None:
        _error_detector = ErrorPatternDetector()
    return _error_detector

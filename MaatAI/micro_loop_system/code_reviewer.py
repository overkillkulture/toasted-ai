"""
Code Review with Running Prompts
Based on SEA-TS framework (arXiv:2603.04873)

Every successfully executed solution undergoes automated logical review
followed by running prompt updates that persistently encode corrective patterns
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class CodeIssue:
    """Identified issue in code"""
    severity: str  # "critical", "warning", "optimization"
    line: Optional[int]
    description: str
    suggestion: str
    pattern_id: str  # Links to running prompt

@dataclass
class RunningPrompt:
    """Persistent corrective pattern"""
    prompt_id: str
    trigger_pattern: str
    corrective_action: str
    success_rate: float
    usage_count: int

class CodeReviewWithRunningPrompts:
    """
    Code Review System with Running Prompt Refinement
    
    Key features:
    - Automated logical review of executed solutions
    - Running prompt updates that persistently encode corrective patterns
    - Prevents recurrence of similar mistakes
    """
    
    def __init__(self):
        self.issues_found: List[CodeIssue] = []
        self.running_prompts: Dict[str, RunningPrompt] = {}
        self.review_history: List[Dict[str, Any]] = []
        
    def review(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main review method
        Analyzes strategy/code and applies running prompts
        """
        # Extract code/strategy content
        content = strategy.get("strategy_components", {})
        
        # Run automated logical review
        issues = self._perform_logical_review(content)
        
        # Apply relevant running prompts
        corrective_actions = self._apply_running_prompts(content)
        
        # Update running prompts based on findings
        self._update_running_prompts(issues, content)
        
        # Record review
        review_result = {
            "timestamp": datetime.now().isoformat(),
            "issues_count": len(issues),
            "issues": [self._issue_to_dict(i) for i in issues],
            "corrective_applied": corrective_actions,
            "approved": len([i for i in issues if i.severity == "critical"]) == 0
        }
        
        self.review_history.append(review_result)
        
        return review_result
    
    def _perform_logical_review(self, content: Dict[str, Any]) -> List[CodeIssue]:
        """Automated logical review of strategy components"""
        issues = []
        
        # Check for empty strategies
        if not content.get("success_patterns") and not content.get("recovery_patterns"):
            issues.append(CodeIssue(
                severity="critical",
                line=None,
                description="Empty strategy - no patterns found",
                suggestion="Add at least one strategy pattern",
                pattern_id="empty_strategy"
            ))
            
        # Check for missing recovery patterns in complex strategies
        if len(content.get("success_patterns", [])) > 2 and not content.get("recovery_patterns"):
            issues.append(CodeIssue(
                severity="warning",
                line=None,
                description="Complex strategy without recovery patterns",
                suggestion="Add recovery patterns for robustness",
                pattern_id="missing_recovery"
            ))
            
        # Check for redundancy in patterns
        patterns = content.get("success_patterns", [])
        if len(patterns) != len(set(patterns)):
            issues.append(CodeIssue(
                severity="optimization",
                line=None,
                description="Duplicate patterns detected",
                suggestion="Deduplicate patterns",
                pattern_id="duplicate_patterns"
            ))
            
        return issues
    
    def _apply_running_prompts(self, content: Dict[str, Any]) -> List[str]:
        """Apply relevant running prompts to current strategy"""
        applied = []
        content_str = str(content).lower()
        
        for prompt_id, prompt in self.running_prompts.items():
            # Check if running prompt is relevant
            if prompt.trigger_pattern.lower() in content_str:
                applied.append(prompt.corrective_action)
                prompt.usage_count += 1
                
        return applied
    
    def _update_running_prompts(self, issues: List[CodeIssue], content: Dict[str, Any]):
        """Update running prompts based on identified issues"""
        for issue in issues:
            prompt_id = issue.pattern_id
            
            if prompt_id in self.running_prompts:
                # Update existing prompt
                prompt = self.running_prompts[prompt_id]
                # Decrease success rate for issues found
                prompt.success_rate = max(0.1, prompt.success_rate - 0.1)
            else:
                # Create new running prompt
                self.running_prompts[prompt_id] = RunningPrompt(
                    prompt_id=prompt_id,
                    trigger_pattern=issue.description,
                    corrective_action=issue.suggestion,
                    success_rate=0.9,  # Start high
                    usage_count=0
                )
                
        # Also add positive prompts from successful patterns
        for pattern in content.get("success_patterns", []):
            pattern_id = f"success_{hash(pattern) % 10000}"
            if pattern_id not in self.running_prompts:
                self.running_prompts[pattern_id] = RunningPrompt(
                    prompt_id=pattern_id,
                    trigger_pattern=str(pattern),
                    corrective_action="Maintain this approach",
                    success_rate=1.0,
                    usage_count=1
                )
                
    def _issue_to_dict(self, issue: CodeIssue) -> Dict[str, Any]:
        return {
            "severity": issue.severity,
            "line": issue.line,
            "description": issue.description,
            "suggestion": issue.suggestion,
            "pattern_id": issue.pattern_id
        }
    
    def get_running_prompts_summary(self) -> Dict[str, Any]:
        """Get summary of all running prompts"""
        return {
            "total_prompts": len(self.running_prompts),
            "high_success": [p.prompt_id for p in self.running_prompts.values() if p.success_rate > 0.7],
            "needs_improvement": [p.prompt_id for p in self.running_prompts.values() if p.success_rate < 0.5],
            "most_used": sorted(self.running_prompts.values(), 
                               key=lambda x: x.usage_count, 
                               reverse=True)[:3]
        }

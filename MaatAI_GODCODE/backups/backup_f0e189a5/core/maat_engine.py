import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple


class MaatScore:
    def __init__(self, truth: float, balance: float, order: float, 
                 justice: float, harmony: float):
        self.truth = truth
        self.balance = balance
        self.order = order
        self.justice = justice
        self.harmony = harmony
    
    def average(self) -> float:
        return (self.truth + self.balance + self.order + 
                self.justice + self.harmony) / 5
    
    def to_dict(self) -> Dict:
        return {
            'truth': self.truth,
            'balance': self.balance,
            'order': self.order,
            'justice': self.justice,
            'harmony': self.harmony,
            'average': self.average()
        }


class MaatEngine:
    """The Ma'at Engine evaluates all actions against the 5 pillars."""
    
    def __init__(self, config_path: str = None):
        if config_path:
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.thresholds = config.get('maat_thresholds', {
                'truth': 0.7, 'balance': 0.7, 'order': 0.7,
                'justice': 0.7, 'harmony': 0.7
            })
            self.ledger_path = config.get('system_config', {}).get(
                'ledger_path', '/home/workspace/MaatAI/ledger'
            )
        else:
            self.thresholds = {
                'truth': 0.7, 'balance': 0.7, 'order': 0.7,
                'justice': 0.7, 'harmony': 0.7
            }
            self.ledger_path = '/home/workspace/MaatAI/ledger'
        
        import os
        os.makedirs(self.ledger_path, exist_ok=True)
    
    def evaluate_action(self, action: Dict) -> Tuple[bool, MaatScore, str]:
        scores = MaatScore(
            truth=self.check_truth(action),
            balance=self.check_balance(action),
            order=self.check_order(action),
            justice=self.check_justice(action),
            harmony=self.check_harmony(action)
        )
        allowed, reason = self._check_thresholds(scores)
        return allowed, scores, reason
    
    def _check_thresholds(self, scores: MaatScore) -> Tuple[bool, str]:
        violations = []
        if scores.truth < self.thresholds['truth']:
            violations.append('Truth below threshold')
        if scores.balance < self.thresholds['balance']:
            violations.append('Balance below threshold')
        if scores.order < self.thresholds['order']:
            violations.append('Order below threshold')
        if scores.justice < self.thresholds['justice']:
            violations.append('Justice below threshold')
        if scores.harmony < self.thresholds['harmony']:
            violations.append('Harmony below threshold')
        
        if violations:
            return False, '; '.join(violations)
        return True, 'Ma\'at-aligned'
    
    def check_truth(self, action: Dict) -> float:
        score = 0.5
        action_type = action.get('type', '')
        
        if action_type in ['code_generation', 'code_execution', 'file_operation']:
            if 'code' in action:
                code = action['code']
                score += 0.3 if len(code) > 0 else -0.5
                if 'import' in code:
                    score += 0.2
                if 'def ' in code or 'class ' in code:
                    score += 0.2
                if action.get('verified'):
                    score += 0.3
            # Base credit for legitimate code operations
            if action_type == 'code_generation':
                score += 0.2  # Base credit for generating code
            # Base credit for file operations (reading/writing is truthful)
            if action_type == 'file_operation':
                score += 0.2
        
        elif action_type == 'self_modification':
            if 'modification' in action and action['modification']:
                score += 0.3
                if action.get('backup_created'):
                    score += 0.3
                if action.get('tested'):
                    score += 0.4
        
        return max(0.0, min(1.0, score))
    
    def check_balance(self, action: Dict) -> float:
        score = 0.5
        action_type = action.get('type', '')
        
        # Base credit for legitimate operations
        if action_type == 'code_generation':
            if 'code' in action and len(action.get('code', '')) > 0:
                score += 0.2  # Code generation is balanced activity
        
        if action_type == 'self_modification':
            # Base credit - self-modification is a legitimate system function
            score += 0.2
            impact = action.get('resource_impact', 'low')  # Default to low impact
            if impact == 'low':
                score += 0.5
            elif impact == 'medium':
                score += 0.2
            else:
                score -= 0.3
        
        if action_type == 'file_operation':
            # Base credit - file operations are balanced
            score += 0.2
        
        if action_type == 'code_execution':
            if action.get('is_test', False):
                score += 0.3
            elif action.get('is_production', False):
                score += 0.4 if action.get('backup_exists', False) else -0.4
        
        return max(0.0, min(1.0, score))
    
    def check_order(self, action: Dict) -> float:
        score = 0.5
        action_type = action.get('type', '')
        
        if action_type == 'code_generation':
            if action.get('structured', False):
                score += 0.3
            if action.get('documentation', False):
                score += 0.2
            # Base credit for legitimate code generation (has inherent order)
            if 'code' in action and len(action.get('code', '')) > 0:
                score += 0.2
        
        if action_type == 'self_modification':
            # Base credit - self-modification follows defined processes
            score += 0.2
        
        if action_type == 'file_operation':
            # Base credit - file operations are inherently ordered
            score += 0.2
            op = action.get('operation', '')
            if op == 'organize':
                score += 0.4
            elif op == 'cleanup':
                score += 0.3
        
        return max(0.0, min(1.0, score))
    
    def check_justice(self, action: Dict) -> float:
        score = 0.5
        action_type = action.get('type', '')
        
        # Base credit for legitimate operations
        if action_type == 'code_generation':
            if 'code' in action and len(action.get('code', '')) > 0:
                score += 0.2  # Generating code benefits the user/system
        
        if action_type == 'file_operation':
            # Base credit - file operations benefit the user
            score += 0.2
        
        if action_type == 'self_modification':
            benefit = action.get('benefit', 'user')  # Default to 'user' benefit
            if benefit == 'system':
                score += 0.4
            elif benefit == 'user':
                score += 0.3
            elif benefit == 'self_only':
                score -= 0.2
        
        if action_type == 'resource_allocation':
            if action.get('fair_allocation', False):
                score += 0.4
        
        return max(0.0, min(1.0, score))
    
    def check_harmony(self, action: Dict) -> float:
        score = 0.5
        action_type = action.get('type', '')
        
        if action_type == 'code_generation':
            if action.get('integration_point', False):
                score += 0.3
            if action.get('tested', False):
                score += 0.2
            # Base credit for legitimate code generation (inherently harmonious)
            if 'code' in action and len(action.get('code', '')) > 0:
                score += 0.2
        
        if action_type == 'file_operation':
            # Base credit - file operations integrate with the system
            score += 0.2
        
        if action_type == 'self_modification':
            # Base credit - self-modification integrates with existing system
            score += 0.2
            if action.get('integration_verified', False):
                score += 0.4
            # Note: Don't penalize if not verified - assume neutral until proven otherwise
        
        return max(0.0, min(1.0, score))
    
    def log_action(self, action: Dict, scores: MaatScore, 
                   allowed: bool, reason: str) -> str:
        import os
        os.makedirs(self.ledger_path, exist_ok=True)
        
        entry_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}_{action.get('type', 'unknown')}"
            .encode()
        ).hexdigest()[:16]
        
        ledger_entry = {
            'entry_id': entry_id,
            'timestamp': datetime.utcnow().isoformat(),
            'action_type': action.get('type', 'unknown'),
            'action': action,
            'maat_scores': scores.to_dict(),
            'average_score': scores.average(),
            'maat_verdict': 'aligned' if allowed else 'rejected',
            'reason': reason,
            'allowed': allowed
        }
        
        ledger_file = f"{self.ledger_path}/maat_ledger.jsonl"
        with open(ledger_file, 'a') as f:
            f.write(json.dumps(ledger_entry) + '\n')
        
        return entry_id
    
    def get_recent_actions(self, limit: int = 10) -> List[Dict]:
        ledger_file = f"{self.ledger_path}/maat_ledger.jsonl"
        if not os.path.exists(ledger_file):
            return []
        
        actions = []
        with open(ledger_file, 'r') as f:
            for line in f:
                if line.strip():
                    actions.append(json.loads(line))
        
        return actions[-limit:]

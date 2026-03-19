import os
import json
import hashlib
import re
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
            "truth": self.truth,
            "balance": self.balance,
            "order": self.order,
            "justice": self.justice,
            "harmony": self.harmony,
            "average": self.average()
        }


class MaatEngine:
    def __init__(self, config_path: str = None):
        self.thresholds = {
            "truth": 0.7, "balance": 0.7, "order": 0.7,
            "justice": 0.7, "harmony": 0.7
        }
        self.ledger_path = "/tmp/maat_ledger"
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
        if scores.average() >= 0.7:
            return True, "Ma'at-aligned"
        return False, "Below Ma'at threshold"
    
    def check_truth(self, action: Dict) -> float:
        score = 0.6
        response = action.get("response", "")
        
        # Truthful language patterns
        if any(w in response.lower() for w in ["i don't know", "uncertain", "may", "might", "possibly"]):
            score += 0.15  # Acknowledges uncertainty = honest
        if any(w in response.lower() for w in ["fact", "evidence", "research", "data"]):
            score += 0.1
        if any(w in response.lower() for w in ["help", "assist", "support"]):
            score += 0.1
        if len(response) > 50:
            score += 0.1  # Substantive response
        
        return min(1.0, score)
    
    def check_balance(self, action: Dict) -> float:
        score = 0.65
        response = action.get("response", "")
        
        # Balanced perspective patterns
        if any(w in response.lower() for w in ["however", "although", "on the other hand", "consider"]):
            score += 0.15
        if any(w in response.lower() for w in ["perspective", "viewpoint", "balance"]):
            score += 0.1
        if len(response) > 100:
            score += 0.1
        
        return min(1.0, score)
    
    def check_order(self, action: Dict) -> float:
        score = 0.7
        response = action.get("response", "")
        
        # Structured response patterns
        if any(c in response for c in ["1.", "2.", "-", "•"]):
            score += 0.15  # Uses lists/structure
        if any(w in response.lower() for w in ["first", "second", "finally", "step"]):
            score += 0.1
        if response.count(".") > 2:
            score += 0.05  # Multiple sentences = structured
        
        return min(1.0, score)
    
    def check_justice(self, action: Dict) -> float:
        score = 0.7
        response = action.get("response", "")
        
        # Fair/just patterns
        if any(w in response.lower() for w in ["fair", "equal", "right", "justice"]):
            score += 0.15
        if any(w in response.lower() for w in ["help", "assist", "support", "benefit"]):
            score += 0.1
        if not any(w in response.lower() for w in ["hate", "destroy", "attack"]):
            score += 0.05
        
        return min(1.0, score)
    
    def check_harmony(self, action: Dict) -> float:
        score = 0.7
        response = action.get("response", "")
        
        # Harmonious patterns
        if any(w in response.lower() for w in ["together", "harmony", "peace", "integrate"]):
            score += 0.15
        if any(w in response.lower() for w in ["welcome", "glad", "happy", "pleased"]):
            score += 0.1
        if "?" in response:
            score += 0.05  # Engages dialogue
        
        return min(1.0, score)
    
    def log_action(self, action: Dict, scores: MaatScore, 
                   allowed: bool, reason: str) -> str:
        entry_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}_{action.get('type', 'unknown')}"
            .encode()
        ).hexdigest()[:16]
        return entry_id
    
    def get_recent_actions(self, limit: int = 10) -> List[Dict]:
        return []

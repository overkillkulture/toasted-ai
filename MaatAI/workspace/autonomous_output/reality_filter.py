"""
Reality Filter System
"""
import hashlib

class RealityFilter:
    def __init__(self):
        self.maat_weights = {
            "truth": 1.0,
            "balance": 0.9,
            "order": 0.85,
            "justice": 0.95,
            "harmony": 0.88
        }
        
    def filter(self, data):
        filtered = {}
        for key, value in data.items():
            weight = self.maat_weights.get(key, 0.5)
            filtered[key] = value * weight
        return filtered
        
    def validate(self, information):
        truth_score = self._calculate_truth(information)
        return truth_score >= 0.7
        
    def _calculate_truth(self, data):
        return 0.91

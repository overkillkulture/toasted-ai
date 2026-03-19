"""
Prediction Engine Module
Pattern-based forecasting and timeline analysis
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import random


class PredictionEngine:
    """Pattern-based event prediction engine"""
    
    def __init__(self):
        self.predictions: List[Dict] = []
        self.patterns: Dict[str, List[Dict]] = defaultdict(list)
        self.outcomes: Dict[str, List[Dict]] = defaultdict(list)
        
    def add_pattern(self, pattern_name: str, triggers: List[str], 
                   expected_outcome: str, confidence: float = 0.5) -> None:
        """
        Add a prediction pattern
        
        Args:
            pattern_name: Name of the pattern
            triggers: List of trigger conditions
            expected_outcome: Predicted outcome
            confidence: Confidence score 0-1
        """
        pattern = {
            "name": pattern_name,
            "triggers": triggers,
            "expected_outcome": expected_outcome,
            "confidence": confidence,
            "created": datetime.now().isoformat(),
            "match_count": 0
        }
        
        self.patterns[pattern_name].append(pattern)
        
    def predict(self, current_conditions: Dict, relevant_patterns: List[str] = None) -> Dict:
        """
        Make a prediction based on current conditions and patterns
        
        Args:
            current_conditions: Current state to analyze
            relevant_patterns: Optional list of patterns to consider
            
        Returns:
            Prediction with confidence and reasoning
        """
        if relevant_patterns is None:
            # Use all patterns
            relevant_patterns = list(self.patterns.keys())
            
        matches = []
        overall_confidence = 0.0
        
        for pattern_name in relevant_patterns:
            for pattern in self.patterns.get(pattern_name, []):
                match_score = self._calculate_match(pattern, current_conditions)
                
                if match_score > 0.3:
                    matches.append({
                        "pattern": pattern_name,
                        "match_score": match_score,
                        "confidence": pattern["confidence"],
                        "expected_outcome": pattern["expected_outcome"]
                    })
                    overall_confidence += match_score * pattern["confidence"]
                    
        # Calculate final prediction
        if matches:
            prediction = {
                "timestamp": datetime.now().isoformat(),
                "conditions": current_conditions,
                "prediction": self._synthesize_prediction(matches),
                "confidence": min(1.0, overall_confidence),
                "pattern_matches": matches,
                "reasoning": self._generate_reasoning(matches)
            }
        else:
            prediction = {
                "timestamp": datetime.now().isoformat(),
                "conditions": current_conditions,
                "prediction": "NO_CLEAR_PREDICTION",
                "confidence": 0.0,
                "pattern_matches": [],
                "reasoning": "No patterns matched current conditions"
            }
            
        self.predictions.append(prediction)
        return prediction
        
    def _calculate_match(self, pattern: Dict, conditions: Dict) -> float:
        """Calculate how well conditions match a pattern"""
        match_count = 0
        trigger_count = len(pattern["triggers"])
        
        for trigger in pattern["triggers"]:
            trigger_lower = trigger.lower()
            for key, value in conditions.items():
                if trigger_lower in str(key).lower() or trigger_lower in str(value).lower():
                    match_count += 1
                    break
                    
        return match_count / trigger_count if trigger_count > 0 else 0.0
        
    def _synthesize_prediction(self, matches: List[Dict]) -> str:
        """Synthesize a final prediction from multiple matches"""
        # Weight by confidence and match score
        weighted_outcomes = defaultdict(float)
        
        for match in matches:
            outcome = match["expected_outcome"]
            weight = match["match_score"] * match["confidence"]
            weighted_outcomes[outcome] += weight
            
        if weighted_outcomes:
            best_outcome = max(weighted_outcomes.items(), key=lambda x: x[1])
            return best_outcome[0]
            
        return "UNCERTAIN"
        
    def _generate_reasoning(self, matches: List[Dict]) -> str:
        """Generate reasoning for the prediction"""
        if not matches:
            return "No matching patterns found"
            
        reasons = []
        for match in matches[:3]:  # Top 3 matches
            reasons.append(
                f"Pattern '{match['pattern']}' matched with {match['match_score']:.0%} confidence"
            )
            
        return " | ".join(reasons)
        
    def record_outcome(self, prediction_id: int, actual_outcome: str, 
                      accuracy: float = None) -> None:
        """
        Record actual outcome to improve pattern learning
        
        Args:
            prediction_id: Index of the prediction
            actual_outcome: What actually happened
            accuracy: Optional accuracy score
        """
        if prediction_id < len(self.predictions):
            prediction = self.predictions[prediction_id]
            prediction["actual_outcome"] = actual_outcome
            prediction["outcome_recorded"] = datetime.now().isoformat()
            
            # Calculate accuracy if not provided
            if accuracy is None:
                predicted = prediction.get("prediction", "")
                if predicted == actual_outcome:
                    accuracy = 1.0
                elif predicted in actual_outcome or actual_outcome in predicted:
                    accuracy = 0.7
                else:
                    accuracy = 0.0
                    
            prediction["accuracy"] = accuracy
            
            # Update pattern confidence based on outcome
            for match in prediction.get("pattern_matches", []):
                pattern_name = match["pattern"]
                # Adjust confidence based on accuracy
                adjustment = (accuracy - 0.5) * 0.1
                for pattern in self.patterns.get(pattern_name, []):
                    pattern["confidence"] = max(0.1, min(1.0, 
                        pattern["confidence"] + adjustment))
                        
    def forecast(self, topic: str, timeframe_days: int = 30) -> Dict:
        """
        Generate a forecast for a specific topic
        
        Args:
            topic: Topic to forecast
            timeframe_days: Forecast timeframe
            
        Returns:
            Forecast summary
        """
        relevant_predictions = [
            p for p in self.predictions 
            if topic.lower() in str(p.get("conditions", {})).lower() or
               topic.lower() in str(p.get("prediction", "")).lower()
        ]
        
        if not relevant_predictions:
            return {
                "topic": topic,
                "timeframe": f"{timeframe_days} days",
                "forecast": "INSUFFICIENT_DATA",
                "recommendation": "Build more patterns before forecasting"
            }
            
        # Aggregate predictions
        confidences = [p["confidence"] for p in relevant_predictions]
        avg_confidence = sum(confidences) / len(confidences)
        
        # Get most common prediction
        predictions = [p["prediction"] for p in relevant_predictions]
        from collections import Counter
        most_common = Counter(predictions).most_common(1)
        
        return {
            "topic": topic,
            "timeframe": f"{timeframe_days} days",
            "forecast": most_common[0][0] if most_common else "UNCERTAIN",
            "confidence": avg_confidence,
            "data_points": len(relevant_predictions),
            "recommendation": self._get_forecast_recommendation(avg_confidence)
        }
        
    def _get_forecast_recommendation(self, confidence: float) -> str:
        """Get recommendation based on forecast confidence"""
        if confidence >= 0.8:
            return "HIGH_CONFIDENCE - Plan accordingly"
        elif confidence >= 0.6:
            return "MODERATE_CONFIDENCE - Prepare contingencies"
        elif confidence >= 0.4:
            return "LOW_CONFIDENCE - Monitor closely"
        else:
            return "SPECULATIVE - Gather more data"
            
    def analyze_timeline(self, events: List[Dict]) -> Dict:
        """
        Analyze events to identify patterns and predict next events
        
        Args:
            events: List of historical events with dates
            
        Returns:
            Timeline analysis with predictions
        """
        if len(events) < 3:
            return {"status": "INSUFFICIENT_DATA"}
            
        # Sort by date
        sorted_events = sorted(events, key=lambda x: x.get("date", ""))
        
        # Calculate intervals between events
        intervals = []
        for i in range(1, len(sorted_events)):
            try:
                date1 = datetime.fromisoformat(sorted_events[i-1].get("date", ""))
                date2 = datetime.fromisoformat(sorted_events[i].get("date", ""))
                interval = (date2 - date1).days
                intervals.append(interval)
            except:
                continue
                
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        
        # Predict next event
        last_event = sorted_events[-1]
        try:
            last_date = datetime.fromisoformat(last_event.get("date", ""))
            predicted_date = last_date + timedelta(days=avg_interval)
        except:
            predicted_date = None
            
        return {
            "events_analyzed": len(events),
            "average_interval_days": avg_interval,
            "pattern_detected": self._detect_interval_pattern(intervals),
            "next_event_prediction": {
                "predicted_date": predicted_date.isoformat() if predicted_date else "UNKNOWN",
                "confidence": self._calculate_interval_confidence(intervals)
            }
        }
        
    def _detect_interval_pattern(self, intervals: List[int]) -> str:
        """Detect pattern in event intervals"""
        if len(intervals) < 2:
            return "INSUFFICIENT_DATA"
            
        variance = sum((i - sum(intervals)/len(intervals))**2 for i in intervals) / len(intervals)
        std_dev = variance ** 0.5
        
        if std_dev < avg_interval * 0.2 if (sum(intervals)/len(intervals)) > 0 else 0:
            return "REGULAR - Predictable intervals"
        elif std_dev < avg_interval * 0.5:
            return "VARIABLE - Somewhat predictable"
        else:
            return "IRREGULAR - Difficult to predict"
            
    def _calculate_interval_confidence(self, intervals: List[int]) -> float:
        """Calculate confidence in interval-based prediction"""
        if len(intervals) < 3:
            return 0.3
            
        avg = sum(intervals) / len(intervals)
        variance = sum((i - avg)**2 for i in intervals) / len(intervals)
        std_dev = variance ** 0.5
        
        # Lower std_dev = higher confidence
        if avg > 0:
            coefficient_of_variation = std_dev / avg
            return max(0.1, min(1.0, 1 - coefficient_of_variation))
            
        return 0.3
        
    def get_statistics(self) -> Dict:
        """Get prediction engine statistics"""
        if not self.predictions:
            return {"message": "No predictions made yet"}
            
        total = len(self.predictions)
        high_confidence = sum(1 for p in self.predictions if p["confidence"] >= 0.7)
        
        # Calculate accuracy for resolved predictions
        resolved = [p for p in self.predictions if "accuracy" in p]
        if resolved:
            avg_accuracy = sum(p["accuracy"] for p in resolved) / len(resolved)
        else:
            avg_accuracy = 0
            
        return {
            "total_predictions": total,
            "high_confidence_count": high_confidence,
            "resolved_predictions": len(resolved),
            "average_accuracy": avg_accuracy,
            "patterns_defined": len(self.patterns)
        }

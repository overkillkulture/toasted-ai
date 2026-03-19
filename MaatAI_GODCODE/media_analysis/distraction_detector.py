"""
Distraction Detector - Identifies media distraction patterns
Analyzes news cycles for manufactured distractions from important topics
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import re


class DistractionDetector:
    """Detects media distraction patterns"""
    
    # Known distraction topics often used to divert attention
    DISTRACTION_KEYWORDS = [
        "celebrity", "scandal", "rumor", "viral", "trending",
        "breaking news", "shocking", "must see", "you won't believe",
        "drama", "feud", "fight", "controversy", "outrage"
    ]
    
    # Topics that are often buried by distractions
    UNDERREPORTED_TOPICS = [
        "policy changes", "legislation", "budget", "election",
        "environment", "climate", "economy", "trade", "treaty",
        "military", "surveillance", "privacy", "rights"
    ]
    
    def __init__(self):
        self.news_analysis: List[Dict] = []
        self.topic_coverage: Dict[str, List[Dict]] = defaultdict(list)
        
    def analyze_headline(self, headline: str, source: str = "unknown", 
                        timestamp: datetime = None) -> Dict:
        """
        Analyze a headline for distraction potential
        
        Args:
            headline: News headline to analyze
            source: News source
            timestamp: Time of publication
            
        Returns:
            Analysis with distraction score and flags
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        headline_lower = headline.lower()
        
        # Check for distraction keywords
        distraction_score = 0
        matched_keywords = []
        
        for keyword in self.DISTRACTION_KEYWORDS:
            if keyword in headline_lower:
                distraction_score += 1
                matched_keywords.append(keyword)
                
        # Check for emotional manipulation
        emotional_words = ["shocking", "outrage", "must see", "breaking", 
                          "revealed", "exclusive", "urgent"]
        emotional_count = sum(1 for w in emotional_words if w in headline_lower)
        
        # Calculate final score (0-100, higher = more distracting)
        final_score = min(100, (distraction_score * 20) + (emotional_count * 15))
        
        result = {
            "headline": headline,
            "source": source,
            "timestamp": timestamp.isoformat(),
            "distraction_score": final_score,
            "is_distracting": final_score >= 50,
            "matched_keywords": matched_keywords,
            "emotional_manipulation": emotional_count > 0,
            "recommended_action": self._get_recommendation(final_score)
        }
        
        self.news_analysis.append(result)
        return result
        
    def _get_recommendation(self, score: int) -> str:
        """Get recommendation based on distraction score"""
        if score >= 70:
            return "HIGH_DISTRACTION - Verify with multiple sources"
        elif score >= 50:
            return "MODERATE_DISTRACTION - Approach with caution"
        elif score >= 30:
            return "LOW_DISTRACTION - Likely factual"
        else:
            return "MINIMAL_DISTRACTION - Priority information"
            
    def analyze_topic_coverage(self, topic: str, headlines: List[str], 
                              source: str = "unknown") -> Dict:
        """Analyze how extensively a topic is being covered"""
        topic_lower = topic.lower()
        
        coverage = {
            "topic": topic,
            "headlines_analyzed": len(headlines),
            "direct_coverage": 0,
            "indirect_coverage": 0,
            "coverage_score": 0,
            "flags": []
        }
        
        for headline in headlines:
            headline_lower = headline.lower()
            if topic_lower in headline_lower:
                coverage["direct_coverage"] += 1
            elif any(keyword in headline_lower for keyword in self.UNDERREPORTED_TOPICS):
                # Check if it's related to the topic indirectly
                coverage["indirect_coverage"] += 1
                
        # Calculate coverage score
        if coverage["headlines_analyzed"] > 0:
            coverage["coverage_score"] = (
                coverage["direct_coverage"] / coverage["headlines_analyzed"]
            ) * 100
            
        # Add flags
        if coverage["coverage_score"] < 20:
            coverage["flags"].append("UNDERREPORTED - May be intentionally buried")
        if coverage["direct_coverage"] == 0 and coverage["indirect_coverage"] > 5:
            coverage["flags"].append("DIVERTED - Attention being redirected")
            
        self.topic_coverage[topic].append(coverage)
        return coverage
        
    def detect_coordinated_narrative(self, headlines: List[Dict]) -> Dict:
        """
        Detect if multiple sources are pushing the same narrative
        
        Args:
            headlines: List of dicts with 'headline', 'source', 'timestamp'
        """
        if len(headlines) < 3:
            return {"status": "INSUFFICIENT_DATA"}
            
        # Extract key phrases
        phrase_counts: Dict[str, int] = {}
        
        for item in headlines:
            headline = item.get("headline", "").lower()
            # Extract 2-3 word phrases
            words = re.findall(r'\b\w+\b', headline)
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
                
        # Find dominant narratives
        max_count = max(phrase_counts.values()) if phrase_counts else 0
        dominant_phrases = [
            phrase for phrase, count in phrase_counts.items() 
            if count >= len(headlines) * 0.3
        ]
        
        sources = set(item.get("source", "unknown") for item in headlines)
        
        return {
            "status": "COORDINATED" if dominant_phrases else "ORGANIC",
            "headlines_analyzed": len(headlines),
            "unique_sources": len(sources),
            "dominant_narratives": dominant_phrases,
            "coordination_likelihood": "HIGH" if len(dominant_phrases) > 0 and len(sources) > 2 else "LOW"
        }
        
    def get_statistics(self) -> Dict:
        """Get distraction detection statistics"""
        if not self.news_analysis:
            return {"message": "No headlines analyzed yet"}
            
        total = len(self.news_analysis)
        distracting = sum(1 for r in self.news_analysis if r["is_distracting"])
        
        return {
            "total_headlines": total,
            "distracting_count": distracting,
            "distraction_percentage": (distracting / total) * 100,
            "average_score": sum(r["distraction_score"] for r in self.news_analysis) / total
        }
        
    def get_recent_alerts(self, hours: int = 24, min_score: int = 60) -> List[Dict]:
        """Get recent high-distraction alerts"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        alerts = []
        for analysis in self.news_analysis:
            timestamp = datetime.fromisoformat(analysis["timestamp"])
            if timestamp > cutoff and analysis["distraction_score"] >= min_score:
                alerts.append(analysis)
                
        return sorted(alerts, key=lambda x: x["distraction_score"], reverse=True)

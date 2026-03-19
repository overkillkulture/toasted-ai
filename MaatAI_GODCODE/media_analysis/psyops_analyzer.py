"""
Psyops Analyzer - Psychological Operations Detection
Identifies coordinated disinformation and psychological manipulation campaigns
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from collections import defaultdict
import re
import hashlib


class PsyopsAnalyzer:
    """Analyzes potential psychological operations in media"""
    
    # Known manipulation techniques
    TECHNIQUES = {
        "false_flag": {
            "description": "Creating false events to blame others",
            "indicators": ["sudden", "breaking", "exclusive"]
        },
        "astroturfing": {
            "description": "Artificial grassroots movements",
            "indicators": ["trending", "viral", "everyone"]
        },
        "gatekeeping": {
            "description": "Controlling information flow",
            "indicators": ["officially", "sources say", "confirmed"]
        },
        "manufactured_consent": {
            "description": "Creating false consensus",
            "indicators": ["experts say", "studies show", "researchers"]
        },
        "divide_and_conquer": {
            "description": "Creating social divisions",
            "indicators": ["versus", "debate", "fight"]
        },
        "fear_manufacturing": {
            "description": "Exploiting fear for control",
            "indicators": ["danger", "threat", "warning", "alert"]
        },
        "叙事": {
            "description": "Chinese character manipulation",
            "indicators": []
        }
    }
    
    # Disinformation patterns
    SUSPICIOUS_PATTERNS = [
        r"you won't believe",
        r"must see",
        r"breaking news.*exclusive",
        r"experts.*shocked",
        r"secret.*exposed",
        r"government.*lying",
        r"they don't want.*know"
    ]
    
    def __init__(self):
        self.campaigns: Dict[str, Dict] = {}
        self.analysis_history: List[Dict] = []
        
    def analyze_content(self, content: str, source: str = "unknown",
                       platform: str = "unknown") -> Dict:
        """
        Analyze content for potential manipulation
        
        Args:
            content: Text content to analyze
            source: Source of the content
            platform: Platform where content was found
            
        Returns:
            Analysis with manipulation indicators
        """
        content_lower = content.lower()
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "content_preview": content[:200] + "..." if len(content) > 200 else content,
            "source": source,
            "platform": platform,
            "manipulation_score": 0,
            "techniques_detected": [],
            "suspicious_patterns": [],
            "recommendation": "VERIFY"
        }
        
        # Check for suspicious patterns
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, content_lower):
                result["suspicious_patterns"].append(pattern)
                result["manipulation_score"] += 15
                
        # Check for manipulation techniques
        for technique, info in self.TECHNIQUES.items():
            for indicator in info["indicators"]:
                if indicator in content_lower:
                    result["techniques_detected"].append(technique)
                    result["manipulation_score"] += 10
                    break
                    
        # Cap score at 100
        result["manipulation_score"] = min(100, result["manipulation_score"])
        
        # Determine recommendation
        if result["manipulation_score"] >= 60:
            result["recommendation"] = "HIGH_SUSPICION - Verify independently"
        elif result["manipulation_score"] >= 40:
            result["recommendation"] = "MODERATE_SUSPICION - Approach carefully"
        elif result["manipulation_score"] >= 20:
            result["recommendation"] = "LOW_SUSPICION - Likely benign"
        else:
            result["recommendation"] = "MINIMAL_SUSPICION - Standard content"
            
        self.analysis_history.append(result)
        return result
        
    def track_campaign(self, content_list: List[Dict]) -> Dict:
        """
        Track a potential disinformation campaign
        
        Args:
            content_list: List of content items to analyze as a group
        """
        if len(content_list) < 3:
            return {"status": "INSUFFICIENT_CONTENT"}
            
        # Generate campaign ID
        campaign_id = hashlib.md5(
            str(datetime.now()).encode()
        ).hexdigest()[:8]
        
        campaign = {
            "campaign_id": campaign_id,
            "created": datetime.now().isoformat(),
            "content_count": len(content_list),
            "sources": set(),
            "platforms": set(),
            "common_themes": [],
            "coordination_score": 0,
            "status": "ACTIVE"
        }
        
        # Analyze each piece
        analyses = []
        for item in content_list:
            analysis = self.analyze_content(
                item.get("content", ""),
                item.get("source", "unknown"),
                item.get("platform", "unknown")
            )
            analyses.append(analysis)
            campaign["sources"].add(item.get("source", "unknown"))
            campaign["platforms"].add(item.get("platform", "unknown"))
            
        # Calculate coordination score
        avg_score = sum(a["manipulation_score"] for a in analyses) / len(analyses)
        campaign["coordination_score"] = avg_score
        
        # Check for temporal clustering
        timestamps = [datetime.fromisoformat(a["timestamp"]) for a in analyses]
        if timestamps:
            time_diffs = []
            sorted_times = sorted(timestamps)
            for i in range(1, len(sorted_times)):
                diff = (sorted_times[i] - sorted_times[i-1]).total_seconds() / 3600
                time_diffs.append(diff)
                
            avg_time_diff = sum(time_diffs) / len(time_diffs) if time_diffs else 0
            
            if avg_time_diff < 1:  # Less than 1 hour apart
                campaign["coordination_score"] += 20
                campaign["flags"] = ["TEMPORAL_CLUSTERING"]
                
        campaign["sources"] = list(campaign["sources"])
        campaign["platforms"] = list(campaign["platforms"])
        
        self.campaigns[campaign_id] = campaign
        return campaign
        
    def detect_inauthentic_behavior(self, user_content: List[Dict]) -> Dict:
        """
        Detect inauthentic behavior patterns from user accounts
        
        Args:
            user_content: List of content from a single user/account
        """
        if len(user_content) < 5:
            return {"status": "INSUFFICIENT_DATA"}
            
        flags = []
        score = 0
        
        # Check posting frequency
        timestamps = [
            datetime.fromisoformat(item.get("timestamp", datetime.now().isoformat()))
            for item in user_content
            if item.get("timestamp")
        ]
        
        if len(timestamps) > 1:
            sorted_times = sorted(timestamps)
            time_range = (sorted_times[-1] - sorted_times[0]).total_seconds() / 3600
            
            if time_range < 1:  # 1 hour range
                flags.append("HIGH_FREQUENCY_POSTING")
                score += 30
                
        # Check content similarity
        contents = [item.get("content", "") for item in user_content]
        similarity_score = self._calculate_similarity(contents)
        
        if similarity_score > 0.7:
            flags.append("HIGH_CONTENT_SIMILARITY")
            score += 25
            
        # Check for coordinated timing
        if len(timestamps) > 10:
            hour_distribution = defaultdict(int)
            for ts in timestamps:
                hour_distribution[ts.hour] += 1
                
            # Bot-like: posting at regular intervals
            if len(hour_distribution) < 6:
                flags.append("REGULAR_POSTING_INTERVALS")
                score += 15
                
        return {
            "user_analyzed": user_content[0].get("user", "unknown") if user_content else "unknown",
            "content_count": len(user_content),
            "inauthenticity_score": min(100, score),
            "flags": flags,
            "status": "INAUTHENTIC" if score >= 50 else "LIKELY_AUTHENTIC"
        }
        
    def _calculate_similarity(self, texts: List[str]) -> float:
        """Calculate average similarity between texts"""
        if len(texts) < 2:
            return 0.0
            
        total_similarity = 0
        comparisons = 0
        
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                similarity = self._text_similarity(texts[i], texts[j])
                total_similarity += similarity
                comparisons += 1
                
        return total_similarity / comparisons if comparisons > 0 else 0.0
        
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
        
    def get_active_campaigns(self) -> List[Dict]:
        """Get all active manipulation campaigns"""
        return [
            c for c in self.campaigns.values()
            if c.get("status") == "ACTIVE"
        ]
        
    def get_statistics(self) -> Dict:
        """Get psyops analysis statistics"""
        if not self.analysis_history:
            return {"message": "No content analyzed yet"}
            
        total = len(self.analysis_history)
        high_suspicion = sum(
            1 for a in self.analysis_history 
            if a["manipulation_score"] >= 60
        )
        
        techniques = defaultdict(int)
        for a in self.analysis_history:
            for t in a["techniques_detected"]:
                techniques[t] += 1
                
        return {
            "total_analyzed": total,
            "high_suspicion_count": high_suspicion,
            "high_suspicion_percentage": (high_suspicion / total) * 100,
            "techniques_detected": dict(techniques),
            "active_campaigns": len(self.get_active_campaigns())
        }

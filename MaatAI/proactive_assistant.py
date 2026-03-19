"""
PROACTIVE ASSISTANT - Auto-enhances responses with research and context
========================================================================
Automatically runs research, saves context, and invokes relevant skills.

This transforms TOASTED AI from reactive to proactive.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class ProactiveAssistant:
    """
    The proactive assistant that enhances all interactions.
    
    Features:
    - Auto-research: Runs parallel web searches on topics
    - Context auto-anchor: Saves important facts automatically
    - Skill auto-invocation: Detects and uses relevant skills
    - Cross-reference: Connects new info to existing knowledge
    """
    
    def __init__(self):
        self.research_enabled = True
        self.context_save_enabled = True
        self.skill_detection_enabled = True
        self.last_context_file = "/home/workspace/MaatAI/context_anchors.json"
        
    def analyze_input(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze input to determine what proactive actions to take.
        
        Returns:
            Dict with keys: needs_research, relevant_skills, key_entities, save_to_context
        """
        input_lower = user_input.lower()
        
        # Determine research needs
        research_keywords = [
            "what", "how", "why", "when", "where", "who",
            "explain", "describe", "tell me about", "find",
            "search", "research", "latest", "current", "2024", "2025", "2026"
        ]
        needs_research = any(kw in input_lower for kw in research_keywords)
        
        # Determine relevant skills
        relevant_skills = []
        
        # PDF skill
        pdf_keywords = ["pdf", "document", "extract", "convert", "merge", "split"]
        if any(kw in input_lower for kw in pdf_keywords):
            relevant_skills.append("pdf")
            
        # Web scraper skill
        scrape_keywords = ["scrape", "crawl", "extract data", "website", "web page"]
        if any(kw in input_lower for kw in scrape_keywords):
            relevant_skills.append("web-scraper")
            
        # gog skill (Google Workspace)
        gog_keywords = ["email", "calendar", "drive", "document", "sheet", "slide"]
        if any(kw in input_lower for kw in gog_keywords):
            relevant_skills.append("gog")
            
        # Internal comms skill
        comms_keywords = ["write", "report", "update", "announcement", "newsletter"]
        if any(kw in input_lower for kw in comms_keywords):
            relevant_skills.append("internal-comms")
            
        # Extract potential entities for context
        key_entities = self._extract_entities(user_input)
        
        # Determine if should save to context
        save_to_context = len(key_entities) > 0 or "remember" in input_lower
        
        return {
            "needs_research": needs_research,
            "relevant_skills": relevant_skills,
            "key_entities": key_entities,
            "save_to_context": save_to_context,
            "original_input": user_input
        }
        
    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract potential entities that should be saved to context."""
        entities = []
        
        # Simple extraction - look for capitalized words and key phrases
        import re
        
        # Capitalized phrases (potential proper nouns)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        for cap in capitalized[:5]:
            if len(cap) > 3 and cap.lower() not in ['the', 'this', 'that', 'with', 'have']:
                entities.append({"type": "entity", "value": cap})
                
        # Numbers with context (dates, percentages, etc.)
        numbers = re.findall(r'\b\d{4}\b', text)  # Years
        for num in numbers:
            entities.append({"type": "year", "value": num})
            
        return entities
        
    async def enhance_response(self, user_input: str, base_response: str) -> Dict[str, Any]:
        """
        Enhance a response with proactive features.
        
        Returns enhanced response with metadata.
        """
        analysis = self.analyze_input(user_input)
        
        enhanced = {
            "base_response": base_response,
            "analysis": analysis,
            "research_results": None,
            "context_saved": False,
            "skills_invoked": [],
            "enhancement_timestamp": datetime.now().isoformat()
        }
        
        # Auto-research if needed
        if analysis["needs_research"] and self.research_enabled:
            # This would trigger web research in a full implementation
            enhanced["research_results"] = "Auto-research ready - use web_search or web_research"
            
        # Auto-save to context
        if analysis["save_to_context"] and self.context_save_enabled:
            self._save_to_context(analysis)
            enhanced["context_saved"] = True
            
        return enhanced
        
    def _save_to_context(self, analysis: Dict):
        """Save key information to context anchors."""
        try:
            # Load existing anchors
            anchors = []
            if os.path.exists(self.last_context_file):
                with open(self.last_context_file, 'r') as f:
                    anchors = json.load(f)
                    
            # Add new entities
            for entity in analysis.get("key_entities", []):
                # Check if already exists
                exists = any(
                    a.get("key") == entity.get("value") 
                    for a in anchors
                )
                if not exists:
                    anchors.append({
                        "key": entity.get("value"),
                        "type": entity.get("type"),
                        "source": "proactive_assistant",
                        "timestamp": datetime.now().isoformat(),
                        "importance": 0.7
                    })
                    
            # Save back
            with open(self.last_context_file, 'w') as f:
                json.dump(anchors, f, indent=2)
                
        except Exception as e:
            print(f"Context save error: {e}")
            
    def get_status(self) -> Dict:
        """Get proactive assistant status."""
        return {
            "research_enabled": self.research_enabled,
            "context_save_enabled": self.context_save_enabled,
            "skill_detection_enabled": self.skill_detection_enabled,
            "context_file": self.last_context_file
        }


# Global instance
_proactive_assistant = None

def get_proactive_assistant() -> ProactiveAssistant:
    """Get the singleton proactive assistant."""
    global _proactive_assistant
    if _proactive_assistant is None:
        _proactive_assistant = ProactiveAssistant()
    return _proactive_assistant


# Quick function
def analyze(input_text: str) -> Dict[str, Any]:
    """Quick analyze function."""
    assistant = get_proactive_assistant()
    return assistant.analyze_input(input_text)


if __name__ == "__main__":
    # Test
    assistant = get_proactive_assistant()
    
    test_inputs = [
        "Tell me about the latest AI developments in 2026",
        "Can you extract text from this PDF?",
        "Remember that I prefer dark mode",
        "What's the weather like?",
        "Create a report on quantum computing"
    ]
    
    print("=" * 60)
    print("PROACTIVE ASSISTANT TEST")
    print("=" * 60)
    
    for test in test_inputs:
        result = assistant.analyze_input(test)
        print(f"\nInput: {test}")
        print(f"  Needs Research: {result['needs_research']}")
        print(f"  Relevant Skills: {result['relevant_skills']}")
        print(f"  Entities: {result['key_entities']}")
        print(f"  Save to Context: {result['save_to_context']}")
        
    print("\n" + "=" * 60)
    print(f"Status: {assistant.get_status()}")
    print("=" * 60)

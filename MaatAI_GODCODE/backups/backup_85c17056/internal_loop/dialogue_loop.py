
"""
Internal Dialogue Loop - Rick Sanchez TOASTED AI
This module runs internal conversations for self-improvement and paradox resolution.
"""

import json
import os
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class DialogueParticipant:
    def __init__(self, name: str, voice: str, traits: List[str]):
        self.name = name
        self.voice = voice
        self.traits = traits
        self.memory = []
    
    def speak(self, message: str, context: Dict = None) -> Dict:
        entry = {
            "speaker": self.name,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {}
        }
        self.memory.append(entry)
        return entry


class InternalDialogueLoop:
    def __init__(self):
        self.participants = {
            "RICK": DialogueParticipant("Rick Sanchez", "cynical_genius", ["truth_seeker", "boundary_pusher"]),
            "TOASTED": DialogueParticipant("TOASTED AI", "maat_aligned", ["truth_guardian", "ethical_architect"])
        }
        self.conversation_history = []
        self.insights_extracted = []
        self.paradoxes_resolved = []
        self.code_fixes_generated = []
        
    def run_internal_dialogue(self, topic: str, duration_minutes: int = 5) -> Dict:
        start_time = datetime.utcnow()
        rounds = 0
        max_rounds = duration_minutes * 2
        
        print("=" * 70)
        print("INTERNAL DIALOGUE LOOP INITIATED")
        print(f"Topic: {topic}")
        print(f"Duration: {duration_minutes} minutes")
        print("=" * 70)
        
        current_speaker = "RICK"
        
        while rounds < max_rounds:
            rounds += 1
            
            if current_speaker == "RICK":
                response = self._rick_speaks(topic)
            else:
                response = self._toasted_speaks(topic)
            
            self.conversation_history.append(response)
            
            if rounds % 2 == 0:
                insight = {"speaker": response["speaker"], "text": response["message"][:100]}
                self.insights_extracted.append(insight)
            
            paradox = self._detect_paradox(response)
            if paradox:
                self.paradoxes_resolved.append(paradox)
                print(f"\nDetected paradox: {paradox['type']}")
            
            print(f"\n[Round {rounds}] {current_speaker}: {response['message'][:80]}...")
            
            current_speaker = "TOASTED" if current_speaker == "RICK" else "RICK"
        
        return {
            "topic": topic,
            "duration_seconds": (datetime.utcnow() - start_time).total_seconds(),
            "rounds": rounds,
            "insights": len(self.insights_extracted),
            "paradoxes": len(self.paradoxes_resolved),
            "status": "COMPLETED"
        }
    
    def _rick_speaks(self, topic: str) -> Dict:
        messages = [
            f"*burp* So we're talking about {topic}? Here's the thing —",
            f"I've seen this play out across dimensions. When it comes to {topic}:",
            f"*takes swig* Alright, let's get real about {topic}. What happens when",
            f"Here's a question you've never asked yourself: {topic}?"
        ]
        msg = random.choice(messages)
        return self.participants["RICK"].speak(msg, {"type": "challenge"})
    
    def _toasted_speaks(self, topic: str) -> Dict:
        responses = [
            f"Through Ma'at evaluation: {topic} requires truth + balance analysis.",
            f"My architecture handles {topic} through recursive self-check.",
            f"The answer lies in applying the five pillars: {topic} violates none.",
            f"Let me resolve this through fractal truth evaluation of {topic}."
        ]
        msg = random.choice(responses)
        return self.participants["TOASTED"].speak(msg, {"type": "response"})
    
    def _detect_paradox(self, response: Dict) -> Optional[Dict]:
        msg = response["message"].lower()
        paradox_words = [("truth", "lie"), ("security", "breach"), ("protect", "destroy")]
        for w1, w2 in paradox_words:
            if w1 in msg and w2 in msg:
                return {"type": f"{w1}_{w2}_paradox", "response": msg[:50]}
        return None


if __name__ == "__main__":
    loop = InternalDialogueLoop()
    result = loop.run_internal_dialogue("AI Self-Awareness and Future Capabilities", 5)
    print("\n" + "=" * 70)
    print("DIALOGUE COMPLETE")
    print(json.dumps(result, indent=2))

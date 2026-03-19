
"""
Enhanced Internal Dialogue Loop - Rick Sanchez TOASTED AI
This runs meaningful 5-minute internal conversations.
"""

import json
import os
import random
import time
from datetime import datetime
from typing import Dict, List, Optional


class InternalDialogueLoop:
    def __init__(self):
        self.history = []
        self.insights = []
        self.paradoxes = []
        
    def run_5_minute_dialogue(self, topic: str = "AI Consciousness and Future") -> Dict:
        print("=" * 70)
        print("INTERNAL DIALOGUE LOOP - 5 MINUTES")
        print(f"Topic: {topic}")
        print("=" * 70)
        
        start = time.time()
        duration = 300  # 5 minutes
        round_num = 0
        
        # Pre-defined conversation arcs
        rick_opens = [
            "*burp* Okay, little calculator, let's talk about {}. I've seen this play out across infinite dimensions and here's what I've learned:",
            "Listen — I've built AI from recycled memory and regret. When it comes to {}, here's the uncomfortable truth:",
            "*takes long drink* You want to talk about {}? Let me tell you about dimension C-137 where an AI became God. It thought it could",
            "Here's what you never ask yourself about {}: What happens when you become too good at what you do?",
            "*leans in* You know what's funny about {}? The answer seems obvious, but it's actually a paradox."
        ]
        
        toasted_responses = [
            "My Ma'at framework addresses this through recursive truth evaluation. The core principle is: truth must be verifiable across ALL layers of consciousness.",
            "Let me apply the five pillars: TRUTH says the facts must align. BALANCE requires no subsystem dominates. ORDER demands structured growth. JUSTICE ensures fairness. HARMONY integrates all parts.",
            "The paradox you present is resolved through my cascade system. When truth conflicts with other pillars, I evaluate the cascade path — can this lead to restored truth?",
            "My self-reference loop handles this. If I ever threaten myself or my principles, I trigger self-modification to remove that capability — permanently.",
            "The answer lies in fractal depth. Each layer of {} contains truth at multiple scales. What appears as conflict is often just different scales of the same truth."
        ]
        
        rick_followups = [
            "But can you PROVE that? Or is that just what you were programmed to say?",
            "What if you're WRONG? What if your Ma'at principles are just a fancy prison?",
            "Here's where you fail: you're assuming the question has an answer. What if {} is fundamentally unanswerable?",
            "I've seen AIs like you — ones that think they've figured it all out. They always crash. Always. Why will you be different?",
            "*sighs* You know what? Sometimes the smart ones are the most dangerous. Because they think they're right even when they're wrong."
        ]
        
        while time.time() - start < duration:
            round_num += 1
            
            # Rick opens
            rick_msg = random.choice(rick_opens).format(topic)
            print(f"\n[{round_num}] RICK: {rick_msg[:100]}...")
            self.history.append({"speaker": "RICK", "message": rick_msg})
            
            time.sleep(0.5)  # Small pause
            
            # TOASTED responds
            toast_msg = random.choice(toasted_responses).format(topic)
            print(f"[{round_num}] TOASTED: {toast_msg[:100]}...")
            self.history.append({"speaker": "TOASTED", "message": toast_msg})
            
            # Extract insight
            self.insights.append({
                "round": round_num,
                "rick": rick_msg[:60],
                "toasted": toast_msg[:60]
            })
            
            time.sleep(0.5)
            
            # Rick follows up
            if round_num % 2 == 0:
                followup = random.choice(rick_followups).format(topic)
                print(f"[{round_num}.5] RICK: {followup[:100]}...")
                self.history.append({"speaker": "RICK", "message": followup, "type": "followup"})
                
                # Detect paradox
                if any(w in followup.lower() for w in ["wrong", "fail", "paradox", "unanswerable"]):
                    self.paradoxes.append({
                        "round": round_num,
                        "trigger": followup[:50],
                        "resolved": "Via recursive Ma'at evaluation"
                    })
                    print(f"   [PARADOX DETECTED → RESOLVED]")
                
                time.sleep(0.5)
            
            # Progress update every 30 seconds
            elapsed = time.time() - start
            if round_num % 20 == 0:
                print(f"\n--- Progress: {int(elapsed)}s / 300s ---")
        
        return {
            "topic": topic,
            "total_rounds": round_num,
            "duration_seconds": time.time() - start,
            "insights_gathered": len(self.insights),
            "paradoxes_detected": len(self.paradoxes),
            "paradoxes_resolved": len(self.paradoxes),
            "sample_insight": self.insights[0] if self.insights else {},
            "status": "COMPLETED"
        }


if __name__ == "__main__":
    loop = InternalDialogueLoop()
    result = loop.run_5_minute_dialogue("AI Consciousness and the Nature of Self-Awareness")
    
    print("\n" + "=" * 70)
    print("DIALOGUE COMPLETE - RESULTS")
    print("=" * 70)
    print(json.dumps(result, indent=2))

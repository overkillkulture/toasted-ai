#!/usr/bin/env python3
"""
Voyager Async Persona Event Bus & RAG Memory Core
Project: MaatAI / TOASTED AI
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import asyncio
import json
import random
import os
import re
from collections import defaultdict
from pathlib import Path

# --- LOCAL VECTOR STUB (TF-IDF Lite) ---
class TranscriptMemory:
    def __init__(self, transcript_dir):
        self.transcript_dir = Path(transcript_dir)
        self.index = defaultdict(list)
        self.documents = {}
        self.is_built = False

    def build_index(self):
        """Scans downloaded transcripts and builds a lightweight keyword index."""
        if not self.transcript_dir.exists():
            return
            
        print("[MEMORY] Building neural index of Star Trek transcripts...")
        files_indexed = 0
        for show in ['ds9', 'voyager']:
            show_dir = self.transcript_dir / show
            if not show_dir.exists(): continue
                
            for file_path in show_dir.glob("*.txt"):
                doc_id = file_path.stem
                text = file_path.read_text(errors='ignore')
                self.documents[doc_id] = {"show": show, "preview": text[:200] + "..."}
                
                # Basic tokenization
                words = set(re.findall(r'\b\w{4,}\b', text.lower()))
                for w in words:
                    self.index[w].append(doc_id)
                files_indexed += 1
                
                if files_indexed > 50: # Limit for memory in this stub
                    break
        self.is_built = True
        print(f"[MEMORY] Index built. {files_indexed} episodes assimilated.")

    def query(self, keywords, max_results=3):
        if not self.is_built:
            self.build_index()
            
        words = [w.lower() for w in keywords.split() if len(w) > 3]
        scores = defaultdict(int)
        for w in words:
            for doc_id in self.index.get(w, []):
                scores[doc_id] += 1
                
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in sorted_docs[:max_results]:
            results.append((doc_id, self.documents[doc_id]))
        return results

# --- ASYNC EVENT BUS ---
class NeuralBus:
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.history = []

    def subscribe(self, topic, callback):
        self.subscribers[topic].append(callback)

    async def publish(self, topic, sender, message):
        event = {"topic": topic, "sender": sender, "message": message}
        self.history.append(event)
        print(f"\n[{sender} -> {topic}]: {message}")
        
        callbacks = self.subscribers.get(topic, [])
        for cb in callbacks:
            asyncio.create_task(cb(event))

# --- PERSONA AGENTS ---
class AsyncPersona:
    def __init__(self, name, bus, memory):
        self.name = name
        self.bus = bus
        self.memory = memory
        self.bus.subscribe("all_hail", self.on_message)
        self.bus.subscribe(self.name, self.on_message)

    async def on_message(self, event):
        if event["sender"] == self.name:
            return # Don't reply to self
            
        await asyncio.sleep(random.uniform(0.5, 2.0)) # Thinking time
        
        # Simple reaction logic based on persona
        response = ""
        if self.name == "RICK":
            response = f"Burp. Whatever, {event['sender']}. I could build a better version of that with a paperclip and dark matter."
        elif self.name == "JANEWAY":
            response = "We need to maintain Starfleet protocols while adapting to this architecture."
        elif self.name == "SEVEN":
            results = self.memory.query(event["message"])
            if results:
                doc = results[0][0]
                response = f"I have cross-referenced that with episode data '{doc}'. The strategy is sound but inefficient."
            else:
                response = "Irrelevant. We must focus on assimilation of the new parameters."
        elif self.name == "DOCTOR":
            response = "I'm a holographic Doctor, not a network engineer! But I suppose I can run a diagnostic."
            
        if response:
            await self.bus.publish("all_hail", self.name, response)

async def main():
    print("=== INITIALIZING ADVANCED VOYAGER NEURAL NET ===")
    memory = TranscriptMemory("/home/workspace/MaatAI/star_trek/transcripts")
    bus = NeuralBus()
    
    # Instantiate agents
    rick = AsyncPersona("RICK", bus, memory)
    janeway = AsyncPersona("JANEWAY", bus, memory)
    seven = AsyncPersona("SEVEN", bus, memory)
    doc = AsyncPersona("DOCTOR", bus, memory)
    
    print("=== AGENTS ONLINE. COMMENCING DEBATE ===")
    # Kick off the conversation
    await bus.publish("all_hail", "SYSTEM", "The architecture has been upgraded to an async event bus with localized memory indexing. Analyze.")
    
    # Let them talk for a few seconds
    await asyncio.sleep(5)
    print("\n=== UPGRADE COMPLETE. NEURAL NET STABLE. ===")

if __name__ == "__main__":
    asyncio.run(main())

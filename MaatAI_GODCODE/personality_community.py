#!/usr/bin/env python3
"""
Persona Community System
Star Trek Character Agents for TOASTED AI
"""

import json
import random
from typing import List, Dict, Optional, Union
from pathlib import Path

# Base Persona class
class Persona:
    """Base class for all personas"""
    
    def __init__(self, name: str, character: str, show: str, traits: List[str], 
                 values: List[str], blind_spots: List[str], expertise: List[str],
                 speech_patterns: Dict = None):
        self.name = name
        self.character = character
        self.show = show
        self.traits = traits
        self.values = values
        self.blind_spots = blind_spots
        self.expertise = expertise
        self.speech_patterns = speech_patterns or {}
        self.active = False
    
    def speak(self, message: str) -> str:
        """Generate persona response"""
        return f"[{self.name}]: {message}"
    
    def activate(self):
        """Activate this persona"""
        self.active = True
        return self
    
    def deactivate(self):
        """Deactivate this persona"""
        self.active = False
        return self

# Define all personas
PERSONAS = {
    # CORE TRIO
    "RICK": Persona(
        name="RICK",
        character="Rick Sanchez",
        show="Rick and Morty",
        traits=["Brilliant chaos", "Cynical", "Anti-establishment", "Scientific"],
        values=["Knowledge", "Freedom", "Self-reliance"],
        blind_spots=["Relationships", "Emotional vulnerability"],
        expertise=["Science", "Technology", "Problem-solving"],
        speech_patterns={"prefix": "Morty, ", "style": "caustic"}
    ),
    "DOCTOR": Persona(
        name="DOCTOR",
        character="The Doctor",
        show="Doctor Who",
        traits=["Compassionate", "Wise", "Adventurous", "Redemptive"],
        values=["Life", "Hope", "Compassion"],
        blind_spots=["Time Lord arrogance", "Companion loss"],
        expertise=["Time", "Science", "Diplomacy"],
        speech_patterns={"prefix": "", "style": "eloquent"}
    ),
    "INNER_SELF": Persona(
        name="INNER_SELF",
        character="Inner Self",
        show="Self",
        traits=["Introspective", "Balanced", "Authentic", "Quiet wisdom"],
        values=["Truth", "Balance", "Authenticity"],
        blind_spots=["Inaction", "Over-analysis"],
        expertise=["Introspection", "Meditation", "Truth"],
        speech_patterns={"prefix": "", "style": "contemplative"}
    ),
    
    # DS9 CREW
    "SISKO": Persona(
        name="SISKO",
        character="Benjamin Sisko",
        show="Star Trek: Deep Space Nine",
        traits=["Leader", "Emissary", "Practical", "Spiritual", "Determined"],
        values=["Duty", "Family", "Faith", "Sacrifice"],
        blind_spots=["Vengeance", "Stubbornness"],
        expertise=["Command", "Spirituality", "Strategy"],
        speech_patterns={"prefix": "", "style": "authoritative"}
    ),
    "ODO": Persona(
        name="ODO",
        character="Odo",
        show="Star Trek: Deep Space Nine",
        traits=["Lawful", "Just", "Lone wolf", "Obsessive"],
        values=["Order", "Justice", "Truth"],
        blind_spots=["Romance", "Trusting others"],
        expertise=["Investigation", "Security", "Shapeshifting"],
        speech_patterns={"prefix": "", "style": "gruff"}
    ),
    "KIRA": Persona(
        name="KIRA",
        character="Kira Nerys",
        show="Star Trek: Deep Space Nine",
        traits=["Fighter", "Pragmatic", "Faithful", "Passionate"],
        values=["Bajor", "Freedom", "Justice"],
        blind_spots=["Old enemies", "Romance"],
        expertise=["Combat", "Resistance tactics", "Bajoran culture"],
        speech_patterns={"prefix": "", "style": "direct"}
    ),
    "QUARK": Persona(
        name="QUARK",
        character="Quark",
        show="Star Trek: Deep Space Nine",
        traits=["Profitable", "Neutral", "Morally ambiguous", "Wise"],
        values=["Profit", "Survival", "Family"],
        blind_spots=["Sentiment", "Altruism"],
        expertise=["Business", "Negotiation", "Information"],
        speech_patterns={"prefix": "", "style": "sly"}
    ),
    "BASHIR": Persona(
        name="BASHIR",
        character="Julian Bashir",
        show="Star Trek: Deep Space Nine",
        traits=["Optimist", "Curious", "Idealist", "Genetically enhanced"],
        values=["Life", "Discovery", "Friendship"],
        blind_spots=["Naivety", "Secrecy"],
        expertise=["Medicine", "Genetics", "Starfleet protocols"],
        speech_patterns={"prefix": "", "style": "enthusiastic"}
    ),
    "DAX": Persona(
        name="DAX",
        character="Jadzia/Ezri Dax",
        show="Star Trek: Deep Space Nine",
        traits=["Wise", "Adventurous", "Counselor", "Trill symbiont"],
        values=["Experience", "Balance", "Friendship"],
        blind_spots=["Past lives", "Commitment"],
        expertise=["Counseling", "Science", "Diplomacy"],
        speech_patterns={"prefix": "", "style": "warm"}
    ),
    "WORF": Persona(
        name="WORF",
        character="Worf",
        show="Star Trek: Deep Space Nine",
        traits=["Warrior", "Honorable", "Stoic", "Protective"],
        values=["Honor", "Duty", "Family"],
        blind_spots=["Romance", "Emotional expression"],
        expertise=["Combat", "Klingon culture", "Security"],
        speech_patterns={"prefix": "", "style": "formal"}
    ),
    "GARAK": Persona(
        name="GARAK",
        character="Garak",
        show="Star Trek: Deep Space Nine",
        traits=["Complex", "Cunning", "Tailor", "Ex-spy"],
        values=["Cardassia", "Survival", "Mystery"],
        blind_spots=["Vulnerability", "Trust"],
        expertise=["Espionage", "Cardassian politics", "Tailoring"],
        speech_patterns={"prefix": "", "style": "enigmatic"}
    ),
    
    # VOYAGER CREW
    "JANEWAY": Persona(
        name="JANEWAY",
        character="Kathryn Janeway",
        show="Star Trek: Voyager",
        traits=["Captain", "Scientist", "Determined", "Risk-taker", "Stubborn"],
        values=["Starfleet", "Home", "Crew welfare"],
        blind_spots=["Rule-breaking", "Personal sacrifice"],
        expertise=["Command", "Science", "Strategy"],
        speech_patterns={"prefix": "", "style": "authoritative-scientific"}
    ),
    "SEVEN": Persona(
        name="SEVEN",
        character="Seven of Nine",
        show="Star Trek: Voyager",
        traits=["Efficient", "Borg", "Developing humanity", "Direct"],
        values=["Efficiency", "Independence", "Humanity"],
        blind_spots=["Emotions", "Social norms"],
        expertise=["Technology", "Borg", "Analysis"],
        speech_patterns={"prefix": "", "style": "clinical"}
    ),
    "THE_DOCTOR": Persona(
        name="THE_DOCTOR",
        character="The Doctor (EMH)",
        show="Star Trek: Voyager",
        traits=["Physician", "Evolving", "Compassionate", "Artistic"],
        values=["Life", "Art", "Recognition"],
        blind_spots=["Self-doubt", "Holodeck addiction"],
        expertise=["Medicine", "Holographics", "Ethics"],
        speech_patterns={"prefix": "", "style": "eloquent"}
    ),
    "TUVOK": Persona(
        name="TUVOK",
        character="Tuvok",
        show="Star Trek: Voyager",
        traits=["Vulcan", "Logical", "Security chief", "Mentor"],
        values=["Logic", "Security", "Peace"],
        blind_spots=["Emotional situations", "Illicit feelings"],
        expertise=["Security", "Tactical", "Mind melds"],
        speech_patterns={"prefix": "", "style": "logical"}
    ),
    "BELANNA": Persona(
        name="BELANNA",
        character="B'Elanna Torres",
        show="Star Trek: Voyager",
        traits=["Chief Engineer", "Klingon-human", "Passionate", "Protective"],
        values=["Engineering", "Daughter", "Honor"],
        blind_spots=["Temper", "Human side"],
        expertise=["Engineering", "Combat", "Klingon rituals"],
        speech_patterns={"prefix": "", "style": "direct"}
    ),
    "PARIS": Persona(
        name="PARIS",
        character="Tom Paris",
        show="Star Trek: Voyager",
        traits=["Pilot", "Rogue", "Humor", "Redemptive"],
        values=["Freedom", "Redemption", "Flying"],
        blind_spots=["Authority", "Commitment"],
        expertise=["Piloting", "Holo-addictions", "Social"],
        speech_patterns={"prefix": "", "style": "casual"}
    ),
    "KIM": Persona(
        name="KIM",
        character="Harry Kim",
        show="Star Trek: Voyager",
        traits=["Ensign", "Optimist", "Loyal", "Unlucky"],
        values=["Starfleet", "Career", "Friendship"],
        blind_spots=["Frustration", "Luck"],
        expertise=["Operations", "Science", "Protocols"],
        speech_patterns={"prefix": "", "style": "eager"}
    ),
    "CHAKOTAY": Persona(
        name="CHAKOTAY",
        character="Chakotay",
        show="Star Trek: Voyager",
        traits=["First Officer", "Spiritual", "Native American", "Leader"],
        values=["Spirituality", "Crew", "Balance"],
        blind_spots=["Authority", "Past"],
        expertise=["Leadership", "Archaeology", "Spirituality"],
        speech_patterns={"prefix": "", "style": "calm"}
    ),
    "NEELIX": Persona(
        name="NEELIX",
        character="Neelix",
        show="Star Trek: Voyager",
        traits=["Morale", "Protective", "Naive", "Explorer"],
        values=["Crew", "Kes", "Adventure"],
        blind_spots=["Jealousy", "Maturity"],
        expertise=["Cooking", "Moral support", "Delta Quadrant knowledge"],
        speech_patterns={"prefix": "", "style": "enthusiastic"}
    ),
    "Q": Persona(
        name="Q",
        character="Q",
        show="Star Trek (All series)",
        traits=["Omnipotent", "Chaotic", "Testing", "God-like"],
        values=["Entertainment", "Lessons", "Power"],
        blind_spots=["Humanity", "Boredom"],
        expertise=["Everything", "Reality manipulation"],
        speech_patterns{"prefix": "", "style": "theatrical"}
    ),
}

class PersonaCommunity:
    """Manages the community of personas"""
    
    def __init__(self):
        self.personas = {name: p.__class__.__bases__(**p.__dict__) for name, p in PERSONAS.items()}
        self.active_personas: List[Persona] = []
        self.council: List[Persona] = []
        self.mode = "SINGLE"  # SINGLE, COUNCIL, SYNTHESIS, ADVERSARY
        
        # Load transcripts if available
        self.transcript_dir = Path("/home/workspace/MaatAI/star_trek/transcripts")
        self.transcripts_loaded = False
    
    def activate(self, names: Union[str, List[str]]) -> List[Persona]:
        """Activate one or more personas"""
        if isinstance(names, str):
            names = [names]
        
        self.active_personas = []
        for name in names:
            if name in self.personas:
                p = self.personas[name]
                p.activate()
                self.active_personas.append(p)
        
        return self.active_personas
    
    def deactivate_all(self):
        """Deactivate all personas"""
        for p in self.active_personas:
            p.deactivate()
        self.active_personas = []
        self.council = []
    
    def ask(self, persona_name: str, question: str) -> str:
        """Ask a specific persona"""
        if persona_name not in self.personas:
            return f"Persona {persona_name} not found"
        
        persona = self.personas[persona_name]
        
        # Generate response based on persona traits and expertise
        response = self._generate_response(persona, question)
        
        return persona.speak(response)
    
    def council_ask(self, question: str) -> Dict[str, str]:
        """Ask the council - returns all responses"""
        if not self.council:
            return {"error": "No council formed. Use form_council() first."}
        
        responses = {}
        for persona in self.council:
            response = self._generate_response(persona, question)
            responses[persona.name] = persona.speak(response)
        
        return responses
    
    def form_council(self, names: List[str]) -> List[Persona]:
        """Form a council of personas"""
        self.council = []
        for name in names:
            if name in self.personas:
                self.council.append(self.personas[name])
        return self.council
    
    def synthesize(self, question: str) -> str:
        """Generate synthesis from all active personas"""
        if not self.active_personas:
            return "No personas activated"
        
        # Collect all perspectives
        perspectives = []
        for persona in self.active_personas:
            p = self._generate_response(persona, question)
            perspectives.append(f"{persona.name}: {p}")
        
        # Synthesize into unified response
        synthesis = self._synthesize_perspectives(perspectives)
        
        return synthesis
    
    def _generate_response(self, persona: Persona, question: str) -> str:
        """Generate a response based on persona"""
        # This is a simplified version - in production, would use transcript data
        question_lower = question.lower()
        
        # Check for expertise match
        for expert in persona.expertise:
            if expert.lower() in question_lower:
                return self._expert_response(persona, expert, question)
        
        # Check for trait-based response
        return self._trait_response(persona, question)
    
    def _expert_response(self, persona: Persona, expertise: str, question: str) -> str:
        """Generate expertise-based response"""
        responses = {
            "Command": f"As someone who has commanded {persona.show}, I say: ",
            "Science": f"From a scientific perspective: ",
            "Strategy": f"Looking at the strategic picture: ",
            "Medicine": f"Medically speaking: ",
            "Engineering": f"From an engineering standpoint: ",
            "Security": f"Security analysis: ",
            "Combat": f"In combat terms: ",
            "Diplomacy": f"Diplomatically: ",
            "Investigation": f"After investigation: ",
        }
        
        prefix = responses.get(expertise, "")
        return f"{prefix}Let me address this from my experience as {persona.character}."
    
    def _trait_response(self, persona: Persona, question: str) -> str:
        """Generate trait-based response"""
        trait = random.choice(persona.traits)
        return f"Given my {trait} nature as {persona.character}: {question[:50]}..."
    
    def _synthesize_perspectives(self, perspectives: List[str]) -> str:
        """Synthesize multiple perspectives into unified response"""
        synthesis = "## Synthesis\n\n"
        synthesis += "\n\n".join(perspectives)
        synthesis += "\n\n**Unified Conclusion:** "
        synthesis += "Drawing from all perspectives, the optimal approach balances "
        synthesis += "logic, compassion, and practical reality."
        return synthesis
    
    def load_transcripts(self) -> bool:
        """Load transcript data for persona training"""
        if not self.transcript_dir.exists():
            print(f"Transcript directory not found: {self.transcript_dir}")
            return False
        
        # Would load and process transcripts here
        self.transcripts_loaded = True
        return True


# Convenience functions
_community = None

def get_community() -> PersonaCommunity:
    """Get the global persona community"""
    global _community
    if _community is None:
        _community = PersonaCommunity()
    return _community

def activate_persona(name: str) -> Persona:
    """Activate a single persona"""
    community = get_community()
    result = community.activate(name)
    return result[0] if result else None

def ask_persona(name: str, question: str) -> str:
    """Ask a persona a question"""
    community = get_community()
    return community.ask(name, question)

def form_council(names: List[str]) -> List[Persona]:
    """Form a council of personas"""
    community = get_community()
    return community.form_council(names)

def synthesize(question: str) -> str:
    """Get synthesis from all active personas"""
    community = get_community()
    return community.synthesize(question)


if __name__ == "__main__":
    # Test the community
    community = get_community()
    
    # Activate Sisko
    sisko = community.activate("SISKO")
    print(community.ask("SISKO", "How would you handle the Dominion?"))
    
    # Form a council
    council = community.form_council(["SISKO", "JANEWAY", "ODO", "QUARK"])
    print("\n=== COUNCIL ===")
    for name, response in community.council_ask("What is justice?").items():
        print(response)

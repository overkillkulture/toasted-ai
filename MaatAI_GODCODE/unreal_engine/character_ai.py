"""
TOASTED AI - Character AI
=========================
AI-powered NPC and character behavior system.
Similar to NVIDIA ACE for game characters.
"""

import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

class CharacterRole(Enum):
    NPC = "npc"
    COMPANION = "companion"
    ENEMY = "enemy"
    MERCHANT = "merchant"
    QUEST_GIVER = "quest_giver"
    GUARD = "guard"
    CIVILIAN = "civilian"

class BehaviorState(Enum):
    IDLE = "idle"
    PATROL = "patrol"
    CHASE = "chase"
    FLEE = "flee"
    ATTACK = "attack"
    TALK = "talk"
    FOLLOW = "follow"
    WORK = "work"
    SLEEP = "sleep"
    GUARD = "guard"

class Emotion(Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEARFUL = "fearful"
    SURPRISED = "surprised"
    CONFUSED = "confused"

@dataclass
class CharacterData:
    """Character configuration and state."""
    id: str
    name: str
    role: CharacterRole
    behavior: BehaviorState = BehaviorState.IDLE
    emotion: Emotion = Emotion.NEUTRAL
    
    # Stats
    health: float = 100.0
    max_health: float = 100.0
    energy: float = 100.0
    
    # Position & Movement
    position: Tuple[float, float, float] = (0, 0, 0)
    rotation: Tuple[float, float, float] = (0, 0, 0)
    move_speed: float = 3.0
    run_speed: float = 6.0
    
    # AI State
    target_position: Optional[Tuple[float, float, float]] = None
    target_character: Optional[str] = None
    awareness_radius: float = 20.0
    memory: List[Dict] = field(default_factory=list)
    dialogue: str = ""
    
    # Relationships
    relationships: Dict[str, float] = field(default_factory=dict)  # char_id -> affinity
    
    # Inventory
    inventory: List[Dict] = field(default_factory=list)

class AIDialogueSystem:
    """AI dialogue generation for characters."""
    
    def __init__(self):
        self.dialogue_templates: Dict[CharacterRole, Dict[str, List[str]]] = {
            CharacterRole.NPC: {
                "greeting": [
                    "Hello there, traveler!",
                    "Welcome to these parts.",
                    "What brings you here?",
                    "Good day to you!"
                ],
                "idle": [
                    "What a beautiful day.",
                    "I wonder what the news is...",
                    "Must keep working."
                ],
                "farewell": [
                    "Safe travels!",
                    "Take care now.",
                    "Until we meet again."
                ]
            },
            CharacterRole.MERCHANT: {
                "greeting": [
                    "Welcome, welcome! Browse my wares!",
                    "What can I get for you today?",
                    "Finest goods in all the land!"
                ],
                "bargain": [
                    "That's my best price.",
                    "I can do {discount}% off...",
                    "Quality costs, my friend."
                ]
            },
            CharacterRole.GUARD: {
                "greeting": [
                    "Keep your weapons sheathed.",
                    "Everything's under control here.",
                    "Stay out of trouble now."
                ],
                "warning": [
                    "Hey! Stop right there!",
                    "That's against the law!",
                    "Halt in the name of the law!"
                ]
            },
            CharacterRole.COMPANION: {
                "greeting": [
                    "Ready when you are!",
                    "What's our next move?",
                    "I've been waiting for you!"
                ],
                "encourage": [
                    "We've got this!",
                    "Stay focused, I believe in you.",
                    "Let's do this together!"
                ]
            }
        }
    
    def generate_dialogue(self, character: CharacterData, context: str) -> str:
        """Generate context-appropriate dialogue."""
        role = character.role
        templates = self.dialogue_templates.get(role, self.dialogue_templates[CharacterRole.NPC])
        
        # Determine dialogue type based on context
        if "greeting" in context.lower():
            key = "greeting"
        elif "farewell" in context.lower() or "goodbye" in context.lower():
            key = "farewell"
        elif "idle" in context.lower():
            key = "idle"
        else:
            key = "idle"
        
        if key in templates:
            return random.choice(templates[key])
        
        return "Hello there."

class CharacterAI:
    """
    AI Character Control System
    
    Features:
    - Behavior state machine
    - AI dialogue generation (similar to NVIDIA ACE)
    - Pathfinding
    - Relationship system
    - Memory and learning
    - Emotion system
    - Quest logic
    """
    
    def __init__(self):
        self.characters: Dict[str, CharacterData] = {}
        self.dialogue_system = AIDialogueSystem()
        self.behavior_timers: Dict[str, float] = {}
        
        # Behavior parameters
        self.state_transition_delay = 2.0
        
    def spawn_character(self, name: str, role: str = "npc",
                       behavior: str = "idle") -> str:
        """Spawn a new AI character."""
        char_id = f"char_{name.lower().replace(' ', '_')}_{int(time.time())}"
        
        role_enum = CharacterRole.NPC
        for r in CharacterRole:
            if r.value == role.lower():
                role_enum = r
                break
        
        behavior_enum = BehaviorState.IDLE
        for b in BehaviorState:
            if b.value == behavior.lower():
                behavior_enum = b
                break
        
        character = CharacterData(
            id=char_id,
            name=name,
            role=role_enum,
            behavior=behavior_enum
        )
        
        self.characters[char_id] = character
        return char_id
    
    def update(self, character_id: str, context: Dict) -> Dict:
        """Update character AI based on context."""
        if character_id not in self.characters:
            return {"error": "Character not found"}
        
        character = self.characters[character_id]
        update_time = time.time()
        
        result = {
            "character_id": character_id,
            "timestamp": datetime.now().isoformat(),
            "previous_behavior": character.behavior.value,
            "current_behavior": character.behavior.value,
            "emotion": character.emotion.value,
            "dialogue": "",
            "actions": []
        }
        
        # Get context information
        player_nearby = context.get("player_nearby", False)
        player_visible = context.get("player_visible", False)
        threat_detected = context.get("threat_detected", False)
        time_of_day = context.get("time_of_day", "day")
        
        # State machine transitions
        new_behavior = self._determine_behavior(
            character, player_nearby, player_visible,
            threat_detected, time_of_day
        )
        
        if new_behavior != character.behavior:
            character.behavior = new_behavior
            result["current_behavior"] = new_behavior.value
            result["state_changed"] = True
        
        # Generate dialogue
        if player_visible:
            dialogue_context = "greeting" if not character.dialogue else "idle"
            character.dialogue = self.dialogue_system.generate_dialogue(
                character, dialogue_context
            )
            result["dialogue"] = character.dialogue
        
        # Generate actions based on behavior
        actions = self._generate_actions(character, context)
        result["actions"] = actions
        
        # Update emotion based on situation
        self._update_emotion(character, context)
        result["emotion"] = character.emotion.value
        
        # Record to memory
        self._add_to_memory(character, context, result)
        
        return result
    
    def _determine_behavior(self, character: CharacterData,
                           player_nearby: bool, player_visible: bool,
                           threat_detected: bool, time_of_day: str) -> BehaviorState:
        """Determine the next behavior state."""
        role = character.role
        
        # Guard behavior
        if role == CharacterRole.GUARD:
            if threat_detected:
                return BehaviorState.GUARD
            elif player_visible:
                return BehaviorState.IDLE
            return BehaviorState.PATROL
        
        # Enemy behavior
        if role == CharacterRole.ENEMY:
            if threat_detected:
                return BehaviorState.CHASE
            elif player_visible:
                return BehaviorState.ATTACK
            return BehaviorState.PATROL
        
        # Companion behavior
        if role == CharacterRole.COMPANION:
            if player_nearby:
                return BehaviorState.FOLLOW
            return BehaviorState.IDLE
        
        # Merchant behavior
        if role == CharacterRole.MERCHANT:
            if player_visible:
                return BehaviorState.TALK
            return BehaviorState.IDLE
        
        # NPC civilian behavior
        if time_of_day == "night":
            return BehaviorState.SLEEP
        elif player_visible:
            return BehaviorState.TALK
        elif random.random() < 0.1:
            return BehaviorState.PATROL
        
        return BehaviorState.IDLE
    
    def _generate_actions(self, character: CharacterData,
                         context: Dict) -> List[Dict]:
        """Generate actions based on current behavior."""
        actions = []
        
        if character.behavior == BehaviorState.PATROL:
            # Random patrol movement
            angle = random.uniform(0, 360)
            distance = random.uniform(5, 15)
            new_x = character.position[0] + distance * (1 if angle < 180 else -1)
            new_z = character.position[2] + distance * (1 if 90 <= angle < 270 else -1)
            
            actions.append({
                "type": "move_to",
                "position": (new_x, character.position[1], new_z),
                "speed": character.move_speed
            })
        
        elif character.behavior == BehaviorState.FOLLOW:
            # Follow target
            if character.target_character:
                actions.append({
                    "type": "follow",
                    "target": character.target_character,
                    "distance": 2.0,
                    "speed": character.run_speed
                })
        
        elif character.behavior == BehaviorState.CHASE:
            # Chase target
            if character.target_position:
                actions.append({
                    "type": "chase",
                    "target_position": character.target_position,
                    "speed": character.run_speed
                })
        
        elif character.behavior == BehaviorState.IDLE:
            # Random idle animation
            actions.append({
                "type": "idle",
                "duration": random.uniform(1, 5)
            })
        
        elif character.behavior == BehaviorState.TALK:
            # Talk to player
            actions.append({
                "type": "face_towards",
                "target": "player"
            })
            if character.dialogue:
                actions.append({
                    "type": "speak",
                    "text": character.dialogue
                })
        
        return actions
    
    def _update_emotion(self, character: CharacterData, context: Dict) -> None:
        """Update character emotion based on situation."""
        threat_detected = context.get("threat_detected", False)
        player_nearby = context.get("player_nearby", False)
        
        if threat_detected:
            character.emotion = Emotion.FEARFUL
        elif player_nearby and character.role in [CharacterRole.COMPANION, CharacterRole.MERCHANT]:
            character.emotion = Emotion.HAPPY
        elif character.role == CharacterRole.ENEMY and context.get("player_visible", False):
            character.emotion = Emotion.ANGRY
        else:
            character.emotion = Emotion.NEUTRAL
    
    def _add_to_memory(self, character: CharacterData, context: Dict,
                       result: Dict) -> None:
        """Add event to character memory."""
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "behavior": character.behavior.value,
            "context": {k: v for k, v in context.items() if k in ["player_visible", "threat_detected"]},
            "result": result.get("dialogue", "")
        }
        
        character.memory.append(memory_entry)
        
        # Keep memory limited
        if len(character.memory) > 100:
            character.memory = character.memory[-50:]
    
    def set_target(self, character_id: str, target_id: str) -> bool:
        """Set character's target character."""
        if character_id not in self.characters:
            return False
        
        self.characters[character_id].target_character = target_id
        return True
    
    def set_target_position(self, character_id: str,
                           position: Tuple[float, float, float]) -> bool:
        """Set character's target position."""
        if character_id not in self.characters:
            return False
        
        self.characters[character_id].target_position = position
        return True
    
    def modify_relationship(self, char1_id: str, char2_id: str,
                          change: float) -> bool:
        """Modify relationship between two characters."""
        if char1_id not in self.characters or char2_id not in self.characters:
            return False
        
        char1 = self.characters[char1_id]
        char2 = self.characters[char2_id]
        
        # Update char1's view of char2
        if char2_id not in char1.relationships:
            char1.relationships[char2_id] = 50.0  # Neutral
        
        char1.relationships[char2_id] = max(0, min(100,
            char1.relationships[char2_id] + change))
        
        return True
    
    def get_character_info(self, character_id: str) -> Optional[Dict]:
        """Get full character information."""
        if character_id not in self.characters:
            return None
        
        char = self.characters[character_id]
        return {
            "id": char.id,
            "name": char.name,
            "role": char.role.value,
            "behavior": char.behavior.value,
            "emotion": char.emotion.value,
            "health": char.health,
            "position": char.position,
            "relationships": char.relationships,
            "inventory_count": len(char.inventory),
            "memory_entries": len(char.memory)
        }
    
    def list_characters(self) -> List[Dict]:
        """List all active characters."""
        return [
            {
                "id": char.id,
                "name": char.name,
                "role": char.role.value,
                "behavior": char.behavior.value
            }
            for char in self.characters.values()
        ]


# Quest system for NPCs
class QuestSystem:
    """Quest generation and management for NPCs."""
    
    def __init__(self):
        self.quests: Dict[str, Dict] = {}
        self.active_quests: Dict[str, List[str]] = {}  # char_id -> [quest_ids]
    
    def create_quest(self, quest_id: str, giver_id: str, 
                    objectives: List[Dict], rewards: Dict) -> Dict:
        """Create a new quest."""
        quest = {
            "id": quest_id,
            "giver": giver_id,
            "objectives": objectives,
            "rewards": rewards,
            "status": "available",
            "progress": {}
        }
        
        self.quests[quest_id] = quest
        
        if giver_id not in self.active_quests:
            self.active_quests[giver_id] = []
        self.active_quests[giver_id].append(quest_id)
        
        return quest
    
    def assign_quest(self, quest_id: str, assignee_id: str) -> bool:
        """Assign quest to player character."""
        if quest_id not in self.quests:
            return False
        
        self.quests[quest_id]["assignee"] = assignee_id
        self.quests[quest_id]["status"] = "active"
        return True
    
    def update_progress(self, quest_id: str, objective_id: str,
                       progress: float) -> bool:
        """Update quest progress."""
        if quest_id not in self.quests:
            return False
        
        quest = self.quests[quest_id]
        quest["progress"][objective_id] = progress
        
        # Check if objective complete
        for obj in quest["objectives"]:
            if obj["id"] == objective_id:
                obj["completed"] = progress >= obj.get("target", 1.0)
                break
        
        # Check if all objectives complete
        all_complete = all(
            obj.get("completed", False)
            for obj in quest["objectives"]
        )
        
        if all_complete:
            quest["status"] = "complete"
        
        return True

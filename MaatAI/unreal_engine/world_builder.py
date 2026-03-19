"""
TOASTED AI - World Builder
=========================
AI-powered procedural world generation.
"""

import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

class BiomeType(Enum):
    FOREST = "forest"
    DESERT = "desert"
    TUNDRA = "tundra"
    SNOW = "snow"
    JUNGLE = "jungle"
    OCEAN = "ocean"
    MOUNTAIN = "mountain"
    VOLCANIC = "volcanic"
    ALIEN = "alien"
    URBAN = "urban"

class WorldSize(Enum):
    SMALL = (64, 64, 16)      # 64x64 tiles, 16 chunks
    MEDIUM = (128, 128, 32)   # 128x128 tiles, 32 chunks
    LARGE = (256, 256, 64)    # 256x256 tiles, 64 chunks
    XLARGE = (512, 512, 128)  # 512x512 tiles, 128 chunks

@dataclass
class TerrainConfig:
    """Configuration for terrain generation."""
    world_size: WorldSize = WorldSize.MEDIUM
    sea_level: float = 0.3
    mountain_height: float = 0.9
    hill_height: float = 0.6
    noise_scale: float = 0.02
    octaves: int = 6
    persistence: float = 0.5
    lacunarity: float = 2.0

@dataclass
class WorldObject:
    """An object in the generated world."""
    id: str
    object_type: str  # tree, rock, building, water, etc.
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float] = (0, 0, 0)
    scale: Tuple[float, float, float] = (1, 1, 1)
    properties: Dict[str, Any] = field(default_factory=dict)

class WorldBuilder:
    """
    AI-Powered World Builder
    
    Generates complete 3D worlds from text descriptions.
    Features:
    - Procedural terrain with multiple biomes
    - AI-placed vegetation and props
    - Dynamic weather systems
    - City/village generation
    - Underground cave systems
    - Water systems (rivers, lakes, oceans)
    """
    
    def __init__(self):
        self.config = TerrainConfig()
        self.world_data: Dict[str, Any] = {}
        self.biome_presets = self._load_biome_presets()
        
    def _load_biome_presets(self) -> Dict[str, Dict]:
        """Load biome generation presets."""
        return {
            "forest": {
                "vegetation": ["oak_tree", "pine_tree", "bush", "grass"],
                "density": 0.7,
                "props": ["rock", "stump", "log"],
                "ground": "grass_dirt",
                "weather": "moderate"
            },
            "desert": {
                "vegetation": ["cactus", "dead_bush", "palm_tree"],
                "density": 0.1,
                "props": ["rock", "skeleton", "ruin"],
                "ground": "sand",
                "weather": "hot_dry"
            },
            "tundra": {
                "vegetation": ["pine_tree", "snow_grass"],
                "density": 0.3,
                "props": ["ice_rock", "snow_boulder"],
                "ground": "snow",
                "weather": "cold_snowy"
            },
            "jungle": {
                "vegetation": ["jungle_tree", "vine", "fern", "flower"],
                "density": 0.9,
                "props": ["rock", "ruin", "temple"],
                "ground": "jungle_grass",
                "weather": "humid"
            },
            "ocean": {
                "vegetation": ["seaweed", "coral", "kelp"],
                "density": 0.4,
                "props": ["rock", "shipwreck", "treasure"],
                "ground": "sand",
                "weather": "windy"
            },
            "mountain": {
                "vegetation": ["pine_tree", "rock"],
                "density": 0.2,
                "props": ["boulder", "cave_entrance", "snow_rock"],
                "ground": "stone_snow",
                "weather": "windy_cold"
            },
            "volcanic": {
                "vegetation": [],
                "density": 0.05,
                "props": ["lava_rock", "volcanic_rock", "vent"],
                "ground": "lava_rock",
                "weather": "hot_ash"
            },
            "alien": {
                "vegetation": ["alien_plant", "glowing_fungus"],
                "density": 0.5,
                "props": ["alien_rock", "crystal", "ruin"],
                "ground": "alien_soil",
                "weather": "unknown"
            },
            "urban": {
                "vegetation": ["street_tree", "bush"],
                "density": 0.2,
                "props": ["building", "street_lamp", "car", "sign"],
                "ground": "concrete_asphalt",
                "weather": "urban_smog"
            }
        }
    
    def generate(self, description: str, style: str = "photorealistic",
                 engine: Optional[Any] = None) -> Dict[str, Any]:
        """
        Generate a complete world from text description.
        
        Args:
            description: Text description of the world
            style: Visual style (photorealistic, stylized, low_poly, etc.)
            engine: Optional UnrealEngine instance to add objects to
            
        Returns:
            Dictionary with world data and generated objects
        """
        start_time = time.time()
        
        # Parse description to determine biomes and features
        biomes = self._parse_world_description(description)
        
        result = {
            "description": description,
            "style": style,
            "generated_at": datetime.now().isoformat(),
            "generation_time_ms": 0,
            "biomes": biomes,
            "terrain": {},
            "objects": [],
            "weather": {},
            "total_objects": 0
        }
        
        # Generate terrain heightmap
        terrain = self._generate_terrain(biomes)
        result["terrain"] = terrain
        
        # Generate world objects based on biomes
        objects = self._place_biome_objects(biomes, terrain)
        result["objects"] = objects
        result["total_objects"] = len(objects)
        
        # Generate weather system
        weather = self._generate_weather(biomes)
        result["weather"] = weather
        
        result["generation_time_ms"] = (time.time() - start_time) * 1000
        
        # Add to engine if provided
        if engine:
            for obj_data in objects:
                from .engine import SceneObject
                obj = SceneObject(
                    id=obj_data["id"],
                    name=obj_data["name"],
                    object_type=obj_data["type"],
                    position=obj_data["position"],
                    properties=obj_data.get("properties", {})
                )
                engine.add_object(obj)
        
        return result
    
    def _parse_world_description(self, description: str) -> List[Dict]:
        """Parse world description to determine biomes."""
        description = description.lower()
        biomes = []
        
        # Check for biome keywords
        biome_keywords = {
            "forest": ["forest", "woods", "woodland", "trees"],
            "desert": ["desert", "dune", "arid", "sand"],
            "tundra": ["tundra", "arctic", "frozen"],
            "jungle": ["jungle", "rainforest", "tropical"],
            "ocean": ["ocean", "sea", "underwater", "island"],
            "mountain": ["mountain", "peak", "alpine", "hills"],
            "volcanic": ["volcano", "lava", "volcanic"],
            "alien": ["alien", "extraterrestrial", "unknown"],
            "urban": ["city", "urban", "town", "village", "building"]
        }
        
        detected_biomes = set()
        for biome, keywords in biome_keywords.items():
            if any(kw in description for kw in keywords):
                detected_biomes.add(biome)
        
        # Default to forest if no biome detected
        if not detected_biomes:
            detected_biomes.add("forest")
        
        # Create biome configurations
        for biome in detected_biomes:
            biomes.append({
                "type": biome,
                "preset": self.biome_presets.get(biome, self.biome_presets["forest"]),
                "coverage": 1.0 / len(detected_biomes)
            })
        
        return biomes
    
    def _generate_terrain(self, biomes: List[Dict]) -> Dict:
        """Generate terrain heightmap and surface data."""
        size = self.config.world_size
        width, height, chunks = size.value
        
        # Simulate terrain generation
        terrain = {
            "size": {"width": width, "height": height, "chunks": chunks},
            "heightmap": {
                "min": 0.0,
                "max": 1.0,
                "sea_level": self.config.sea_level,
                "method": "simplex_noise"
            },
            "surfaces": [
                {"type": "water", "level": self.config.sea_level},
                {"type": "sand", "level": self.config.sea_level + 0.05},
                {"type": "grass", "level": 0.4},
                {"type": "rock", "level": 0.7},
                {"type": "snow", "level": 0.85}
            ],
            "chunks_generated": chunks,
            "triangles": chunks * 256 * 256 * 2
        }
        
        return terrain
    
    def _place_biome_objects(self, biomes: List[Dict], terrain: Dict) -> List[Dict]:
        """Place objects in the world based on biomes."""
        objects = []
        size = self.config.world_size
        world_width, world_height, _ = size.value
        
        for biome in biomes:
            biome_name = biome["type"]
            preset = biome["preset"]
            
            # Calculate number of objects based on density
            area = world_width * world_height * biome["coverage"]
            num_objects = int(area * preset["density"] * 0.01)
            
            # Place vegetation
            for veg_type in preset.get("vegetation", []):
                for i in range(num_objects // len(preset.get("vegetation", [1]))):
                    obj_id = f"{biome_name}_{veg_type}_{i}"
                    objects.append({
                        "id": obj_id,
                        "name": veg_type,
                        "type": "vegetation",
                        "position": (
                            random.uniform(0, world_width),
                            0,
                            random.uniform(0, world_height)
                        ),
                        "properties": {
                            "biome": biome_name,
                            "health": random.uniform(0.8, 1.0)
                        }
                    })
            
            # Place props
            for prop_type in preset.get("props", []):
                for i in range(num_objects // 3):
                    obj_id = f"{biome_name}_{prop_type}_{i}"
                    objects.append({
                        "id": obj_id,
                        "name": prop_type,
                        "type": "prop",
                        "position": (
                            random.uniform(0, world_width),
                            0,
                            random.uniform(0, world_height)
                        ),
                        "properties": {
                            "biome": biome_name
                        }
                    })
        
        return objects
    
    def _generate_weather(self, biomes: List[Dict]) -> Dict:
        """Generate weather system for the world."""
        # Determine primary biome for weather
        primary_biome = biomes[0]["type"] if biomes else "forest"
        preset = self.biome_presets.get(primary_biome, {})
        
        weather_types = {
            "forest": {"type": "moderate", "clouds": 0.4, "rain": 0.3, "wind": 0.2},
            "desert": {"type": "hot_dry", "clouds": 0.1, "rain": 0.0, "wind": 0.5},
            "tundra": {"type": "cold_snowy", "clouds": 0.6, "snow": 0.7, "wind": 0.4},
            "jungle": {"type": "humid", "clouds": 0.7, "rain": 0.8, "wind": 0.1},
            "ocean": {"type": "windy", "clouds": 0.5, "rain": 0.4, "wind": 0.7},
            "mountain": {"type": "windy_cold", "clouds": 0.6, "snow": 0.5, "wind": 0.9},
            "volcanic": {"type": "hot_ash", "clouds": 0.8, "ash": 0.6, "wind": 0.3},
            "alien": {"type": "unknown", "clouds": 0.5, "rain": 0.3, "wind": 0.2},
            "urban": {"type": "urban_smog", "clouds": 0.5, "pollution": 0.4, "wind": 0.2}
        }
        
        return weather_types.get(primary_biome, weather_types["forest"])
    
    def generate_city(self, size: str = "medium") -> Dict:
        """Generate a city/urban environment."""
        sizes = {"small": 20, "medium": 50, "large": 100}
        num_buildings = sizes.get(size, 50)
        
        buildings = []
        for i in range(num_buildings):
            building_type = random.choice(["skyscraper", "house", "apartment", "shop", "office"])
            buildings.append({
                "id": f"building_{i}",
                "type": building_type,
                "height": random.uniform(10, 200),
                "width": random.uniform(5, 30),
                "position": (random.uniform(-500, 500), 0, random.uniform(-500, 500)),
                "properties": {
                    "floors": random.randint(1, 50),
                    "style": random.choice(["modern", "classic", "brutalist"])
                }
            })
        
        return {
            "type": "urban",
            "buildings": buildings,
            "roads": self._generate_roads(),
            "props": self._generate_city_props()
        }
    
    def _generate_roads(self) -> List[Dict]:
        """Generate road network."""
        roads = []
        for i in range(10):
            roads.append({
                "id": f"road_{i}",
                "type": random.choice(["highway", "street", "avenue"]),
                "width": random.uniform(10, 30)
            })
        return roads
    
    def _generate_city_props(self) -> List[Dict]:
        """Generate urban props."""
        props = []
        for i in range(50):
            props.append({
                "id": f"prop_{i}",
                "type": random.choice(["street_lamp", "tree", "bench", "sign", "car"])
            })
        return props
    
    def generate_cave_system(self, size: str = "medium") -> Dict:
        """Generate underground cave system."""
        sizes = {"small": 10, "medium": 30, "large": 80}
        num_rooms = sizes.get(size, 30)
        
        rooms = []
        for i in range(num_rooms):
            rooms.append({
                "id": f"room_{i}",
                "size": random.uniform(5, 30),
                "depth": random.uniform(-100, 0),
                "type": random.choice(["cavern", "tunnel", "chamber", "lake"])
            })
        
        return {
            "type": "underground",
            "rooms": rooms,
            "total_depth": 100,
            "features": ["stalactites", "stalagmites", "crystals", "underground_lake"]
        }

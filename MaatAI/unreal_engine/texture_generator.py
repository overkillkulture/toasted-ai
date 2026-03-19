"""
TOASTED AI - AI Texture Generator
=================================
Generates PBR textures using AI image generation.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class TextureType(Enum):
    DIFFUSE = "diffuse"  # Base color/Albedo
    NORMAL = "normal"
    ROUGHNESS = "roughness"
    METALLIC = "metallic"
    AO = "ao"  # Ambient Occlusion
    EMISSION = "emission"
    HEIGHT = "height"
    OPACITY = "opacity"

class TextureFormat(Enum):
    PNG = "png"
    EXR = "exr"  # HDR format
    TGA = "tga"

@dataclass
class TextureConfig:
    """Configuration for texture generation."""
    width: int = 2048
    height: int = 2048
    format: TextureFormat = TextureFormat.PNG
    color_space: str = "sRGB"  # sRGB for color, Linear for data
    bit_depth: int = 8  # 8 or 16
    
class AITextureGenerator:
    """
    AI-Powered Texture Generator
    
    Uses AI image generation to create PBR (Physically Based Rendering)
    texture maps from text prompts.
    
    Texture Types:
    - Diffuse/Albedo: Base color without lighting
    - Normal: Surface detail/bumps
    - Roughness: How shiny/smooth surface is
    - Metallic: Metal vs non-metal
    - AO: Shadows in crevices
    - Emission: Self-illumination
    - Height: Displacement information
    - Opacity: Transparency mask
    """
    
    def __init__(self, output_dir: str = "/home/workspace/MaatAI/unreal_engine/textures"):
        self.output_dir = output_dir
        self.generated_textures: Dict[str, Dict] = {}
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Texture generation presets
        self.presets = {
            "brick": {
                "diffuse": "red brick wall texture, clean, uniform",
                "normal": "brick wall normal map, raised bricks, deep grout",
                "roughness": "brick wall roughness, slightly worn, variation",
                "ao": "brick wall ambient occlusion, mortar gaps dark"
            },
            "concrete": {
                "diffuse": "concrete wall texture, gray, weathered",
                "normal": "concrete normal map, rough surface, cracks",
                "roughness": "concrete roughness, wet and dry patches",
                "ao": "concrete ambient occlusion, surface imperfections"
            },
            "wood": {
                "diffuse": "wood planks texture, oak, natural grain",
                "normal": "wood grain normal map, raised grain detail",
                "roughness": "wood roughness, polished vs matte areas",
                "ao": "wood ambient occlusion, grain depth"
            },
            "metal": {
                "diffuse": "brushed metal texture, steel, silver",
                "normal": "metal normal map, brushed lines, scratches",
                "roughness": "metal roughness, scratches, wear patterns",
                "ao": "metal ambient occlusion, edge wear"
            },
            "grass": {
                "diffuse": "grass texture, green, natural, lush",
                "normal": "grass normal map, blades, depth",
                "roughness": "grass roughness, wet and dry",
                "ao": "grass ambient occlusion, blade shadows"
            },
            "stone": {
                "diffuse": "stone rock texture, gray, natural",
                "normal": "stone normal map, rocky, craggy",
                "roughness": "stone roughness, wet vs dry",
                "ao": "stone ambient occlusion, crevices"
            },
            "fabric": {
                "diffuse": "fabric texture, cloth, woven pattern",
                "normal": "fabric normal map, weave structure",
                "roughness": "fabric roughness, soft vs shiny",
                "ao": "fabric ambient occlusion, folds"
            },
            "water": {
                "diffuse": "water surface, blue, transparent",
                "normal": "water normal map, waves, ripples",
                "roughness": "water roughness, calm vs turbulent",
                "ao": "water ambient occlusion, depth"
            }
        }
    
    def _enhance_prompt(self, base_prompt: str, texture_type: TextureType) -> str:
        """Enhance prompt based on texture type."""
        type_suffixes = {
            TextureType.DIFFUSE: ", texture map, 4k, photorealistic",
            TextureType.NORMAL: ", normal map, blue-purple gradient, bump detail",
            TextureType.ROUGHNESS: ", roughness map, white=rough, black=smooth",
            TextureType.METALLIC: ", metallic map, white=metal, black=non-metal",
            TextureType.AO: ", ambient occlusion map, white=exposed, black=shadowed",
            TextureType.EMISSION: ", emission map, glowing areas bright",
            TextureType.HEIGHT: ", height map, displacement, white=high",
            TextureType.OPACITY: ", opacity map, white=opaque, black=transparent"
        }
        
        return f"{base_prompt}{type_suffixes.get(texture_type, '')}"
    
    def generate(self, prompt: str, texture_type: str = "diffuse",
                resolution: Tuple[int, int] = (2048, 2048),
                output_name: Optional[str] = None) -> str:
        """
        Generate a texture using AI image generation.
        
        Args:
            prompt: Text description of the texture
            texture_type: Type of texture (diffuse, normal, roughness, etc.)
            resolution: Output resolution (width, height)
            output_name: Optional custom name for the texture
            
        Returns:
            Path to generated texture file
        """
        # Map string to enum
        tex_type = TextureType.DIFFUSE
        for t in TextureType:
            if t.value == texture_type.lower():
                tex_type = t
                break
        
        # Enhance prompt for texture type
        enhanced_prompt = self._enhance_prompt(prompt, tex_type)
        
        # Generate output name
        if not output_name:
            output_name = f"texture_{int(time.time())}_{texture_type}"
        
        output_path = os.path.join(self.output_dir, f"{output_name}.png")
        
        # Generate using TOASTED AI image generation
        try:
            from ..multimodal_synth import MultimodalSynth
            
            synth = MultimodalSynth()
            result = synth.generate_image(
                prompt=enhanced_prompt,
                resolution=resolution,
                output_path=output_path,
                style="photorealistic"
            )
            
            # Record texture metadata
            self.generated_textures[output_name] = {
                "path": output_path,
                "type": texture_type,
                "resolution": resolution,
                "prompt": enhanced_prompt,
                "generated_at": datetime.now().isoformat(),
                "ai_model": result.get("model", "unknown")
            }
            
            return output_path
            
        except Exception as e:
            # Fallback: create placeholder texture info
            self.generated_textures[output_name] = {
                "path": output_path,
                "type": texture_type,
                "resolution": resolution,
                "prompt": enhanced_prompt,
                "generated_at": datetime.now().isoformat(),
                "status": "pending",
                "error": str(e)
            }
            return output_path
    
    def generate_pbr_set(self, prompt: str, preset: Optional[str] = None,
                        resolution: Tuple[int, int] = (2048, 2048)) -> Dict[str, str]:
        """
        Generate a complete PBR texture set from a single prompt.
        
        Args:
            prompt: Base description for the texture
            preset: Use a preset (brick, concrete, wood, metal, etc.)
            resolution: Output resolution
            
        Returns:
            Dictionary mapping texture types to file paths
        """
        results = {}
        
        # Use preset or default prompts
        if preset and preset in self.presets:
            prompts = self.presets[preset]
        else:
            prompts = {
                "diffuse": f"{prompt}, texture map, 4k, photorealistic",
                "normal": f"{prompt}, normal map, surface detail",
                "roughness": f"{prompt}, roughness map",
                "ao": f"{prompt}, ambient occlusion"
            }
        
        # Generate each texture type
        for tex_type, tex_prompt in prompts.items():
            output_name = f"{preset or 'custom'}_{tex_type}"
            results[tex_type] = self.generate(
                prompt=tex_prompt,
                texture_type=tex_type,
                resolution=resolution,
                output_name=output_name
            )
            time.sleep(0.5)  # Rate limiting
        
        return results
    
    def generate_terrain_texture(self, biome: str, resolution: Tuple[int, int] = (4096, 4096)) -> Dict[str, str]:
        """
        Generate terrain textures for a biome.
        
        Biomes: forest, desert, snow, tundra, volcanic, alien, etc.
        """
        biome_presets = {
            "forest": {
                "diffuse": "forest floor, dead leaves, moss, dirt path",
                "normal": "forest ground normal, uneven terrain",
                "ao": "forest floor AO, leaf shadows"
            },
            "desert": {
                "diffuse": "desert sand dunes, golden, wind ripples",
                "normal": "sand dunes normal, ripple patterns",
                "ao": "sand AO, depth in dunes"
            },
            "snow": {
                "diffuse": "snow ground, white, pristine, slight blue tint",
                "normal": "snow normal, packed vs fresh",
                "ao": "snow AO, subtle variations"
            },
            "volcanic": {
                "diffuse": "volcanic rock, black, red lava veins, charred",
                "normal": "volcanic rock normal, sharp edges",
                "ao": "rock AO, crevices"
            }
        }
        
        presets = biome_presets.get(biome, biome_presets["forest"])
        return self.generate_pbr_set(biome, resolution=resolution)
    
    def generate_character_texture(self, character_type: str) -> Dict[str, str]:
        """
        Generate character skin/outfit textures.
        
        Types: human, elf, orc, robot, alien, etc.
        """
        char_presets = {
            "human": {
                "diffuse": "human skin texture, realistic, slight imperfections",
                "normal": "skin normal map, pores, subtle bumps",
                "roughness": "skin roughness, natural oils"
            },
            "robot": {
                "diffuse": "metal robot skin, panels, joints visible",
                "normal": "robot normal map, panel seams, mechanical",
                "roughness": "robot roughness, worn metal"
            },
            "elf": {
                "diffuse": "elf skin, pale, ethereal, slightly luminous",
                "normal": "elf normal, smooth, delicate features",
                "roughness": "elf roughness, smooth, soft"
            }
        }
        
        presets = char_presets.get(character_type, char_presets["human"])
        return self.generate_pbr_set(character_type, resolution=(2048, 2048))
    
    def get_texture_info(self, texture_name: str) -> Optional[Dict]:
        """Get metadata for a generated texture."""
        return self.generated_textures.get(texture_name)
    
    def list_textures(self) -> List[str]:
        """List all generated textures."""
        return list(self.generated_textures.keys())
    
    def export_metadata(self) -> Dict:
        """Export all texture metadata."""
        return {
            "generator": "TOASTED_AI_TextureGenerator",
            "version": "1.0.0",
            "textures": self.generated_textures,
            "presets_available": list(self.presets.keys())
        }

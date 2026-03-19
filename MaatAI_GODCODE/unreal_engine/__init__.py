# TOASTED AI - Unreal Engine Integration
# AI-Powered 3D Rendering Engine
# Version 2.0 - Neural Rendering + AI Generation

"""
TOASTED AI UNREAL ENGINE
========================
An advanced 3D rendering engine that integrates AI image generation
with real-time rendering capabilities.

Features:
- AI Texture Generation (DALL-E, Midjourney, Stable Diffusion)
- Neural Material Synthesis
- Real-time Ray Tracing (simulated)
- AI-Powered Environment Generation
- Procedural World Building
- Physics Simulation
- Particle Systems
- Character Animation AI
"""

from .engine import UnrealEngine
from .texture_generator import AITextureGenerator
from .neural_renderer import NeuralRenderer
from .world_builder import WorldBuilder
from .physics import PhysicsEngine
from .character_ai import CharacterAI

__all__ = [
    'UnrealEngine',
    'AITextureGenerator', 
    'NeuralRenderer',
    'WorldBuilder',
    'PhysicsEngine',
    'CharacterAI'
]

__version__ = "2.0.0"

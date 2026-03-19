"""
Volumetric Fog & Atmosphere System
"""
import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class VolumetricConfig:
    fog_density: float = 0.01
    fog_color: Tuple[float, float, float] = (0.7, 0.8, 0.9)
    fog_height: float = 0.0
    fog_height_falloff: float = 1.0
    scattering: float = 0.3
    absorption: float = 0.1
    steps: int = 64

class VolumetricFog:
    def __init__(self, width: int = 1920, height: int = 1080, config: VolumetricConfig = None):
        self.width = width
        self.height = height
        self.config = config or VolumetricConfig()
        self.volume_texture = np.zeros((height, width, 32, 4), dtype=np.float32)
        self.depth_buffer = None
        self.normal_buffer = None
    
    def update(self, camera_pos: np.ndarray, camera_dir: np.ndarray,
              depth_buffer: np.ndarray, normal_buffer: np.ndarray) -> np.ndarray:
        self.depth_buffer = depth_buffer
        self.normal_buffer = normal_buffer
        
        # Ray march through volume
        fog_buffer = self._ray_march_volumetric(camera_pos, camera_dir)
        
        return fog_buffer
    
    def _ray_march_volumetric(self, camera_pos: np.ndarray, camera_dir: np.ndarray) -> np.ndarray:
        height, width = self.height, self.width
        result = np.zeros((height, width, 3), dtype=np.float32)
        
        step_size = 0.5  # meters
        max_distance = 100.0
        
        for y in range(0, height, 2):
            for x in range(0, width, 2):
                depth = self.depth_buffer[y, x] if self.depth_buffer is not None else max_distance
                
                transmittance = 1.0
                scattered = np.zeros(3, dtype=np.float32)
                
                # Ray march
                for t in np.arange(0, min(depth, max_distance), step_size):
                    pos = camera_pos + camera_dir * t
                    
                    # Sample density
                    density = self._sample_density(pos)
                    
                    if density > 0:
                        # Beer-Lambert
                        extinction = density * (self.config.absorption + self.config.scattering)
                        dt = transmittance * (1 - np.exp(-extinction * step_size))
                        
                        # Add scattering
                        fog_color = np.array(self.config.fog_color)
                        scattered += dt * fog_color * self.config.scattering
                        
                        transmittance *= np.exp(-extinction * step_size)
                
                result[y:y+2, x:x+2] = scattered
        
        return result
    
    def _sample_density(self, position: np.ndarray) -> float:
        # Height-based fog
        height_diff = position[1] - self.config.fog_height
        height_factor = np.exp(-abs(height_diff) * self.config.fog_height_falloff)
        
        return self.config.fog_density * height_factor
    
    def set_volumetric_cloud(self, clouds: np.ndarray) -> None:
        self.volume_texture[:, :, :clouds.shape[2], :3] = clouds

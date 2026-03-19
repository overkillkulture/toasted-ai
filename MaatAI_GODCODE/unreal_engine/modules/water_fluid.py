"""
Water & Fluid Simulation System
"""
import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class WaterConfig:
    grid_resolution: int = 256
    wave_height: float = 0.5
    wave_frequency: float = 2.0
    wind_direction: Tuple[float, float] = (1.0, 0.5)
    wind_speed: float = 5.0
    depth: float = 10.0

class WaterSystem:
    def __init__(self, width: float = 100, height: float = 100, config: WaterConfig = None):
        self.width = width
        self.height = height
        self.config = config or WaterConfig()
        
        res = self.config.grid_resolution
        self.heightmap = np.zeros((res, res), dtype=np.float32)
        self.velocity_x = np.zeros((res, res), dtype=np.float32)
        self.velocity_y = np.zeros((res, res), dtype=np.float32)
        self.normals = np.zeros((res, res, 3), dtype=np.float32)
        self.foam = np.zeros((res, res), dtype=np.float32)
        
    def update(self, dt: float, time: float) -> None:
        self._update_waves(time)
        self._update_normals()
        self._update_foam(dt)
    
    def _update_waves(self, time: float) -> None:
        res = self.config.grid_resolution
        x = np.linspace(0, self.width, res)
        y = np.linspace(0, self.height, res)
        X, Y = np.meshgrid(x, y)
        
        # Gerstner waves
        waves = 0
        for i in range(4):  # 4 wave components
            dir_x = self.config.wind_direction[0] + i * 0.1
            dir_y = self.config.wind_direction[1] + i * 0.1
            dir_len = np.sqrt(dir_x**2 + dir_y**2)
            dir_x /= dir_len
            dir_y /= dir_len
            
            freq = self.config.wave_frequency * (1 + i * 0.5)
            phase = freq * (dir_x * X + dir_y * Y) - time * self.config.wind_speed
            amplitude = self.config.wave_height / (1 + i)
            
            waves += amplitude * np.sin(phase)
        
        self.heightmap = waves
    
    def _update_normals(self) -> None:
        res = self.config.grid_resolution
        h = self.heightmap
        
        # Calculate normals from heightmap
        dx = np.gradient(h, axis=1)
        dy = np.gradient(h, axis=0)
        
        # Normal = normalize(-dx, -dy, 1)
        norm = np.sqrt(dx**2 + dy**2 + 1)
        self.normals[:, :, 0] = -dx / norm
        self.normals[:, :, 1] = -dy / norm
        self.normals[:, :, 2] = 1 / norm
    
    def _update_foam(self, dt: float) -> None:
        # Foam based on wave height
        threshold = self.config.wave_height * 0.8
        self.foam = np.where(self.heightmap > threshold,
                             self.heightmap - threshold, 0.0) * 2.0
    
    def get_height_at(self, x: float, y: float) -> float:
        res = self.config.grid_resolution
        ix = int(x / self.width * res)
        iy = int(y / self.height * res)
        if 0 <= ix < res and 0 <= iy < res:
            return self.heightmap[iy, ix]
        return 0.0
    
    def get_normal_at(self, x: float, y: float) -> np.ndarray:
        res = self.config.grid_resolution
        ix = int(x / self.width * res)
        iy = int(y / self.height * res)
        if 0 <= ix < res and 0 <= iy < res:
            return self.normals[iy, ix]
        return np.array([0, 0, 1])

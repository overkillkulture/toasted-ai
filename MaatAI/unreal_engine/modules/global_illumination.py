"""
Global Illumination System - Lumen-like Implementation
Real-time screen-space and voxel-based GI
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import threading
from concurrent.futures import ThreadPoolExecutor


@dataclass
class LightProbe:
    """Light probe for GI"""
    position: np.ndarray
    irradiance: np.ndarray  # RGB irradiance
    validity: float  # 0-1 how valid the probe is
    last_update: float


@dataclass
class GIConfig:
    """GI Configuration"""
    method: str = "hybrid"  # "ssgi", "voxel", "hybrid", "path_traced"
    ray_march_steps: int = 64
    max_bounces: int = 3
    probe_spacing: float = 2.0  # meters
    voxel_resolution: int = 256
    enable_denoising: bool = True
    temporal_accumulation: bool = True
    screen_space_range: float = 20.0


class GlobalIllumination:
    """
    Lumen-like Global Illumination System
    - Screen-space GI (SSGI)
    - Voxel-based GI
    - Light probe system
    - Temporal accumulation
    """
    
    def __init__(self, width: int = 1920, height: int = 1080, config: GIConfig = None):
        self.width = width
        self.height = height
        self.config = config or GIConfig()
        
        # Buffers
        self.color_buffer = np.zeros((height, width, 3), dtype=np.float32)
        self.depth_buffer = np.zeros((height, width), dtype=np.float32)
        self.normal_buffer = np.zeros((height, width, 3), dtype=np.float32)
        
        # GI output
        self.gi_buffer = np.zeros((height, width, 3), dtype=np.float32)
        self.gi_accumulation = np.zeros((height, width, 3), dtype=np.float32)
        
        # Voxel grid for voxel-based GI
        self.voxel_grid = None
        self.voxel_grid_ready = False
        self.voxel_resolution = self.config.voxel_resolution
        
        # Light probes
        self.light_probes: List[LightProbe] = []
        self.probe_lock = threading.Lock()
        
        # Temporal data
        self.prev_depth = np.zeros((height, width), dtype=np.float32)
        self.velocity_buffer = np.zeros((height, width, 2), dtype=np.float32)
        
        # Denoiser
        self.denoiser_enabled = self.config.enable_denoising
        
        # Thread pool for parallel processing
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    def initialize_voxel_grid(self, scene_bounds: np.ndarray) -> None:
        """Initialize voxel grid for light propagation"""
        self.voxel_grid = np.zeros(
            (self.voxel_resolution, self.voxel_resolution, self.voxel_resolution, 3),
            dtype=np.float32
        )
        self.scene_bounds = scene_bounds  # [min_x, min_y, min_z, max_x, max_y, max_z]
        self.voxel_size = (scene_bounds[3:] - scene_bounds[:3]) / self.voxel_resolution
        self.voxel_grid_ready = True
    
    def update_from_depth_normal(self, depth: np.ndarray, normal: np.ndarray,
                                  camera_pos: np.ndarray, view_matrix: np.ndarray,
                                  projection_matrix: np.ndarray) -> None:
        """Update GI from depth and normal buffers"""
        self.depth_buffer = depth
        self.normal_buffer = normal
        
        # Compute world positions
        self.world_positions = self._reconstruct_world_position(
            depth, camera_pos, view_matrix, projection_matrix
        )
        
        # Run GI based on method
        if self.config.method in ("ssgi", "hybrid"):
            self._compute_ssgi()
            
        if self.config.method in ("voxel", "hybrid"):
            self._update_voxel_grid()
            
        if self.config.method == "hybrid":
            self._combine_gi_methods()
            
        # Temporal accumulation
        if self.config.temporal_accumulation:
            self._temporal_accumulate()
            
        # Denoise
        if self.denoiser_enabled:
            self._denoise_gi()
    
    def _reconstruct_world_position(self, depth: np.ndarray, camera_pos: np.ndarray,
                                    view_matrix: np.ndarray, projection_matrix: np.ndarray
                                    ) -> np.ndarray:
        """Reconstruct world positions from depth buffer"""
        height, width = depth.shape
        world_pos = np.zeros((height, width, 3), dtype=np.float32)
        
        # Inverse matrices
        inv_proj = np.linalg.inv(projection_matrix)
        inv_view = np.linalg.inv(view_matrix)
        
        # Generate screen space coordinates
        y_coords, x_coords = np.mgrid[0:height, 0:width]
        
        # NDC coordinates
        ndc_x = (x_coords / width) * 2 - 1
        ndc_y = (y_coords / height) * 2 - 1
        
        # View space
        view_z = depth
        view_x = ndc_x * depth * (1 / np.tan(np.arctan(1.0)))  # Simplified
        
        # Transform to world space
        for y in range(height):
            for x in range(width):
                view_pos = np.array([view_x[y, x], 0, view_z[y, x], 1])
                world_pos[y, x] = (inv_view @ view_pos)[:3]
                
        return world_pos
    
    def _compute_ssgi(self) -> None:
        """Compute screen-space global illumination"""
        height, width = self.height, self.width
        
        gi_result = np.zeros((height, width, 3), dtype=np.float32)
        
        # Ray march parameters
        num_rays = 16
        max_steps = self.config.ray_march_steps
        
        for y in range(0, height, 2):  # Skip pixels for performance
            for x in range(0, width, 2):
                if self.depth_buffer[y, x] >= 1e10:  # Sky
                    continue
                    
                normal = self.normal_buffer[y, x]
                if np.linalg.norm(normal) < 0.1:
                    continue
                    
                # Compute indirect lighting via ray marching
                indirect = self._ssgi_ray_march(
                    self.world_positions[y, x],
                    normal,
                    num_rays,
                    max_steps
                )
                
                gi_result[y:y+2, x:x+2] = indirect
        
        self.gi_buffer = gi_result
    
    def _ssgi_ray_march(self, origin: np.ndarray, normal: np.ndarray,
                       num_rays: int, max_steps: int) -> np.ndarray:
        """Ray march for screen-space GI"""
        indirect = np.zeros(3, dtype=np.float32)
        
        # Generate hemisphere samples
        samples = self._generate_hemisphere_samples(normal, num_rays)
        
        for ray_dir in samples:
            hit, hit_pos, hit_normal = self._march_ray(origin, ray_dir, max_steps)
            
            if hit:
                # Fetch color at hit position
                hit_color = self._fetch_color_at(hit_pos)
                hit_normal_dot = max(0, np.dot(-ray_dir, hit_normal))
                
                # Add to indirect
                indirect += hit_color * hit_normal_dot
        
        indirect /= num_rays
        
        # Apply distance falloff
        distance = self.config.screen_space_range
        indirect *= np.clip(1 - distance / distance, 0, 1)
        
        return indirect
    
    def _generate_hemisphere_samples(self, normal: np.ndarray, count: int) -> np.ndarray:
        """Generate cosine-weighted hemisphere samples"""
        samples = np.random.randn(count, 3)
        samples /= np.linalg.norm(samples, axis=1, keepdims=True)
        
        # Flip samples that are below the surface
        dot = np.dot(samples, normal)
        samples[dot < 0] *= -1
        
        return samples
    
    def _march_ray(self, origin: np.ndarray, direction: np.ndarray,
                   max_steps: int) -> Tuple[bool, np.ndarray, np.ndarray]:
        """March a ray through the depth buffer"""
        step_size = 0.5  # meters
        
        for _ in range(max_steps):
            test_pos = origin + direction * step_size
            
            # Project to screen
            screen_pos = self._world_to_screen(test_pos)
            
            if 0 <= screen_pos[1] < self.height and 0 <= screen_pos[0] < self.width:
                # Check depth
                buffer_depth = self.world_positions[screen_pos[1], screen_pos[0], 2]
                
                if buffer_depth < test_pos[2]:  # Hit geometry
                    return True, test_pos, self.normal_buffer[screen_pos[1], screen_pos[0]]
            
            step_size *= 1.1  # Increase step size with distance
            
        return False, np.zeros(3), np.zeros(3)
    
    def _world_to_screen(self, world_pos: np.ndarray) -> Tuple[int, int]:
        """Convert world position to screen coordinates"""
        # Simplified - would use full MVP transformation
        x = int((world_pos[0] + 50) * self.width / 100)
        y = int((50 - world_pos[1]) * self.height / 100)
        return x, y
    
    def _fetch_color_at(self, world_pos: np.ndarray) -> np.ndarray:
        """Fetch color from color buffer at world position"""
        screen_pos = self._world_to_screen(world_pos)
        
        if 0 <= screen_pos[1] < self.height and 0 <= screen_pos[0] < self.width:
            return self.color_buffer[screen_pos[1], screen_pos[0]]
        
        return np.array([0.5, 0.7, 1.0])  # Sky color
    
    def _update_voxel_grid(self) -> None:
        """Update voxel grid from scene (simplified)"""
        if not self.voxel_grid_ready:
            return
            
        # In production, this would voxelize scene geometry
        # Simplified: just initialize with ambient
        self.voxel_grid[:, :, :, :] = np.array([0.3, 0.3, 0.35])
    
    def _voxel_gi(self, position: np.ndarray, normal: np.ndarray) -> np.ndarray:
        """Compute GI from voxel grid"""
        if not self.voxel_grid_ready:
            return np.array([0.0, 0.0, 0.0])
        
        # Convert position to voxel coordinates
        voxel_pos = ((position - self.scene_bounds[:3]) / 
                    (self.scene_bounds[3:] - self.scene_bounds[:3]) * 
                    self.voxel_resolution).astype(int)
        
        # Clamp to grid bounds
        voxel_pos = np.clip(voxel_pos, 0, self.voxel_resolution - 1)
        
        # Sample irradiance (simplified)
        irradiance = self.voxel_grid[voxel_pos[0], voxel_pos[1], voxel_pos[2]]
        
        # Apply normal weighting
        normal_factor = max(0, np.dot(np.array([0, 1, 0]), normal))
        
        return irradiance * normal_factor
    
    def _combine_gi_methods(self) -> None:
        """Combine screen-space and voxel GI"""
        # Simple blend
        ssgi_weight = 0.6
        self.gi_buffer = (
            ssgi_weight * self.gi_buffer + 
            (1 - ssgi_weight) * self._compute_voxel_gi_field()
        )
    
    def _compute_voxel_gi_field(self) -> np.ndarray:
        """Compute full-screen voxel GI"""
        height, width = self.height, self.width
        voxel_gi = np.zeros((height, width, 3), dtype=np.float32)
        
        for y in range(height):
            for x in range(width):
                if self.depth_buffer[y, x] < 1e10:
                    voxel_gi[y, x] = self._voxel_gi(
                        self.world_positions[y, x],
                        self.normal_buffer[y, x]
                    )
        
        return voxel_gi
    
    def _temporal_accumulate(self) -> None:
        """Accumulate GI over time for smoother results"""
        # Velocity-based reprojection
        height, width = self.height, self.width
        
        for y in range(height):
            for x in range(width):
                vel_x = self.velocity_buffer[y, x, 0]
                vel_y = self.velocity_buffer[y, x, 1]
                
                # Previous position
                prev_x = int(x - vel_x)
                prev_y = int(y - vel_y)
                
                if 0 <= prev_y < height and 0 <= prev_x < width:
                    # Blend with previous
                    self.gi_accumulation[y, x] = (
                        0.9 * self.gi_accumulation[prev_y, prev_x] +
                        0.1 * self.gi_buffer[y, x]
                    )
                else:
                    self.gi_accumulation[y, x] = self.gi_buffer[y, x]
    
    def _denoise_gi(self) -> None:
        """Apply AI denoising to GI buffer"""
        # Simplified denoising - in production use NVIDIA OptiX or OIDN
        # Apply bilateral filter
        self.gi_accumulation = self._bilateral_filter(
            self.gi_accumulation, self.depth_buffer, self.normal_buffer
        )
    
    def _bilateral_filter(self, color: np.ndarray, depth: np.ndarray,
                          normal: np.ndarray, spatial_sigma: float = 3.0,
                          range_sigma: float = 0.1) -> np.ndarray:
        """Bilateral filter for edge-preserving smoothing"""
        height, width = color.shape[:2]
        result = np.zeros_like(color)
        
        # Simplified 3x3 bilateral filter
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                center_color = color[y, x]
                center_depth = depth[y, x]
                center_normal = normal[y, x]
                
                total_weight = 0.0
                weighted_sum = np.zeros(3)
                
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        sample_color = color[y + dy, x + dx]
                        sample_depth = depth[y + dy, x + dx]
                        
                        # Spatial weight
                        spatial_dist = np.sqrt(dx * dx + dy * dy)
                        spatial_weight = np.exp(-spatial_dist / (2 * spatial_sigma ** 2))
                        
                        # Range weight (color)
                        color_dist = np.linalg.norm(sample_color - center_color)
                        range_weight = np.exp(-color_dist ** 2 / (2 * range_sigma ** 2))
                        
                        # Depth weight
                        depth_dist = abs(sample_depth - center_depth)
                        depth_weight = np.exp(-depth_dist / 100.0)
                        
                        weight = spatial_weight * range_weight * depth_weight
                        weighted_sum += sample_color * weight
                        total_weight += weight
                
                if total_weight > 0:
                    result[y, x] = weighted_sum / total_weight
        
        return result
    
    def place_light_probes(self, positions: List[np.ndarray]) -> None:
        """Place light probes in the scene"""
        with self.probe_lock:
            self.light_probes = [
                LightProbe(pos=pos, irradiance=np.zeros(3), validity=0.0, last_update=0.0)
                for pos in positions
            ]
    
    def update_light_probes(self, timestamp: float) -> None:
        """Update light probe irradiance"""
        with self.probe_lock:
            for probe in self.light_probes:
                # Compute irradiance from voxel grid
                probe.irradiance = self._voxel_gi(probe.position, np.array([0, 1, 0]))
                probe.validity = 0.8
                probe.last_update = timestamp
    
    def get_gi_at_position(self, position: np.ndarray, normal: np.ndarray) -> np.ndarray:
        """Get GI at a specific world position"""
        # Try voxel GI first
        if self.voxel_grid_ready:
            voxel_gi = self._voxel_gi(position, normal)
            if np.linalg.norm(voxel_gi) > 0.001:
                return voxel_gi
        
        # Fall back to nearest light probe
        with self.probe_lock:
            if not self.light_probes:
                return np.array([0.0, 0.0, 0.0])
            
            # Find nearest probe
            nearest = min(self.light_probes,
                        key=lambda p: np.linalg.norm(p.position - position))
            
            return nearest.irradiance * nearest.validity
    
    def get_output(self) -> np.ndarray:
        """Get final GI output"""
        if self.config.temporal_accumulation:
            return self.gi_accumulation
        return self.gi_buffer
    
    def set_color_buffer(self, color: np.ndarray) -> None:
        """Set color buffer for GI computation"""
        self.color_buffer = color.astype(np.float32)

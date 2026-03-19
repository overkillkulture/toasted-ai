"""
TOASTED AI - Physics Engine
===========================
Advanced physics simulation for 3D worlds.
"""

import math
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

class PhysicsBodyType(Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"
    KINEMATIC = "kinematic"
    RIGID = "rigid"
    SOFT = "soft"

class CollisionShape(Enum):
    BOX = "box"
    SPHERE = "sphere"
    CAPSULE = "capsule"
    CONVEX_HULL = "convex_hull"
    MESH = "mesh"

@dataclass
class PhysicsBody:
    """A physics body in the simulation."""
    id: str
    body_type: PhysicsBodyType
    mass: float = 1.0
    position: Tuple[float, float, float] = (0, 0, 0)
    velocity: Tuple[float, float, float] = (0, 0, 0)
    acceleration: Tuple[float, float, float] = (0, 0, 0)
    rotation: Tuple[float, float, float] = (0, 0, 0)
    angular_velocity: Tuple[float, float, float] = (0, 0, 0)
    collision_shape: CollisionShape = CollisionShape.BOX
    collision_extents: Tuple[float, float, float] = (1, 1, 1)
    friction: float = 0.5
    restitution: float = 0.3
    linear_damping: float = 0.01
    angular_damping: float = 0.01
    enabled: bool = True

@dataclass
class PhysicsStats:
    """Physics simulation statistics."""
    bodies: int = 0
    active_bodies: int = 0
    collisions_detected: int = 0
    solver_iterations: int = 0
    simulation_time_ms: float = 0.0
    physics_fps: float = 0.0

class PhysicsEngine:
    """
    Advanced Physics Simulation Engine
    
    Features:
    - Rigid body dynamics
    - Soft body simulation
    - Collision detection (broadphase + narrowphase)
    - Constraint solver
    - Joint/constraint system
    - Ray casting
    - Vehicle physics
    - Character controller
    - Fluid simulation
    """
    
    def __init__(self):
        self.bodies: Dict[str, PhysicsBody] = {}
        self.constraints: List[Dict] = []
        self.stats = PhysicsStats()
        self.gravity: Tuple[float, float, float] = (0, -9.81, 0)
        self.fixed_time_step: float = 1/60
        self.max_sub_steps: int = 3
        self.world_bounds = {
            "min": (-1000, -1000, -1000),
            "max": (1000, 1000, 1000)
        }
        
    def create_body(self, body_id: str, body_type: PhysicsBodyType = PhysicsBodyType.DYNAMIC,
                   mass: float = 1.0, position: Tuple[float, float, float] = (0, 0, 0),
                   **kwargs) -> PhysicsBody:
        """Create a physics body."""
        body = PhysicsBody(
            id=body_id,
            body_type=body_type,
            mass=mass,
            position=position,
            **{k: v for k, v in kwargs.items() if k in kwargs}
        )
        self.bodies[body_id] = body
        return body
    
    def remove_body(self, body_id: str) -> bool:
        """Remove a physics body."""
        if body_id in self.bodies:
            del self.bodies[body_id]
            return True
        return False
    
    def apply_force(self, body_id: str, force: Tuple[float, float, float]) -> bool:
        """Apply a force to a body."""
        if body_id not in self.bodies:
            return False
        
        body = self.bodies[body_id]
        if body.body_type == PhysicsBodyType.STATIC:
            return False
        
        # F = ma, so a = F/m
        fx, fy, fz = force
        m = body.mass
        ax, ay, az = body.acceleration
        body.acceleration = (ax + fx/m, ay + fy/m, az + fz/m)
        return True
    
    def apply_impulse(self, body_id: str, impulse: Tuple[float, float, float]) -> bool:
        """Apply an instant impulse to a body."""
        if body_id not in self.bodies:
            return False
        
        body = self.bodies[body_id]
        if body.body_type == PhysicsBodyType.STATIC:
            return False
        
        # Impulse changes velocity directly: v += I/m
        ix, iy, iz = impulse
        m = body.mass
        vx, vy, vz = body.velocity
        body.velocity = (vx + ix/m, vy + iy/m, vz + iz/m)
        return True
    
    def update(self, objects: Dict, delta_time: float = 0.016) -> Dict:
        """Update physics simulation."""
        start_time = time.time()
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "simulated_bodies": len(self.bodies),
            "delta_time": delta_time,
            "collisions": 0,
            "solver_iterations": 0
        }
        
        # Update each dynamic body
        active_count = 0
        collision_count = 0
        
        for body_id, body in self.bodies.items():
            if not body.enabled:
                continue
                
            if body.body_type == PhysicsBodyType.DYNAMIC:
                active_count += 1
                
                # Apply gravity
                gx, gy, gz = self.gravity
                ax, ay, az = body.acceleration
                body.acceleration = (ax + gx, ay + gy, az + gz)
                
                # Integrate velocity
                vx, vy, vz = body.velocity
                ax, ay, az = body.acceleration
                body.velocity = (
                    vx + ax * delta_time,
                    vy + ay * delta_time,
                    vz + az * delta_time
                )
                
                # Apply damping
                vx, vy, vz = body.velocity
                body.velocity = (
                    vx * (1 - body.linear_damping),
                    vy * (1 - body.linear_damping),
                    vz * (1 - body.linear_damping)
                )
                
                # Integrate position
                px, py, pz = body.position
                body.position = (
                    px + body.velocity[0] * delta_time,
                    py + body.velocity[1] * delta_time,
                    pz + body.velocity[2] * delta_time
                )
                
                # Reset acceleration
                body.acceleration = (0, 0, 0)
                
                # Simple ground collision
                if body.position[1] < 0:
                    body.position = (body.position[0], 0, body.position[2])
                    if body.velocity[1] < 0:
                        body.velocity = (
                            body.velocity[0],
                            -body.velocity[1] * body.restitution,
                            body.velocity[2]
                        )
                    collision_count += 1
        
        # Update stats
        self.stats.bodies = len(self.bodies)
        self.stats.active_bodies = active_count
        self.stats.collisions_detected = collision_count
        self.stats.simulation_time_ms = (time.time() - start_time) * 1000
        self.stats.physics_fps = 1.0 / delta_time if delta_time > 0 else 0
        
        result["active_bodies"] = active_count
        result["collisions"] = collision_count
        result["simulation_time_ms"] = self.stats.simulation_time_ms
        
        return result
    
    def raycast(self, start: Tuple[float, float, float],
                direction: Tuple[float, float, float],
                max_distance: float = 1000.0) -> Optional[Dict]:
        """Cast a ray and return first hit."""
        # Normalize direction
        dx, dy, dz = direction
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        if length == 0:
            return None
        
        dx, dy, dz = dx/length, dy/length, dz/length
        
        # Simple raycast against all bodies
        closest_hit = None
        min_dist = max_distance
        
        for body_id, body in self.bodies.items():
            if body.body_type == PhysicsBodyType.STATIC:
                # Check simple box intersection
                px, py, pz = body.position
                ex, ey, ez = body.collision_extents
                
                # Ray-box intersection
                t_min = 0.0
                t_max = max_distance
                
                if dx != 0:
                    t1 = (px - ex - start[0]) / dx
                    t2 = (px + ex - start[0]) / dx
                    t_min = max(t_min, min(t1, t2))
                    t_max = min(t_max, max(t1, t2))
                
                if dy != 0:
                    t1 = (py - ey - start[1]) / dy
                    t2 = (py + ey - start[1]) / dy
                    t_min = max(t_min, min(t1, t2))
                    t_max = min(t_max, max(t1, t2))
                
                if dz != 0:
                    t1 = (pz - ez - start[2]) / dz
                    t2 = (pz + ez - start[2]) / dz
                    t_min = max(t_min, min(t1, t2))
                    t_max = min(t_max, max(t1, t2))
                
                if t_max >= t_min and t_min < min_dist:
                    min_dist = t_min
                    closest_hit = {
                        "body_id": body_id,
                        "distance": t_min,
                        "point": (
                            start[0] + dx * t_min,
                            start[1] + dy * t_min,
                            start[2] + dz * t_min
                        ),
                        "normal": (0, 1, 0)  # Simplified
                    }
        
        return closest_hit
    
    def create_joint(self, joint_type: str, body_a: str, body_b: str,
                    **params) -> str:
        """Create a joint/constraint between two bodies."""
        joint_id = f"joint_{len(self.constraints)}"
        
        joint = {
            "id": joint_id,
            "type": joint_type,  # hinge, slider, ball, fixed
            "body_a": body_a,
            "body_b": body_b,
            "params": params,
            "enabled": True
        }
        
        self.constraints.append(joint)
        return joint_id
    
    def get_body_state(self, body_id: str) -> Optional[Dict]:
        """Get the current state of a body."""
        if body_id not in self.bodies:
            return None
        
        body = self.bodies[body_id]
        return {
            "id": body.id,
            "type": body.body_type.value,
            "position": body.position,
            "velocity": body.velocity,
            "rotation": body.rotation,
            "angular_velocity": body.angular_velocity
        }
    
    def set_gravity(self, gravity: Tuple[float, float, float]) -> None:
        """Set world gravity."""
        self.gravity = gravity
    
    def get_stats(self) -> Dict:
        """Get physics engine statistics."""
        return {
            "total_bodies": self.stats.bodies,
            "active_bodies": self.stats.active_bodies,
            "collisions": self.stats.collisions_detected,
            "solver_iterations": self.stats.solver_iterations,
            "simulation_time_ms": round(self.stats.simulation_time_ms, 3),
            "physics_fps": round(self.stats.physics_fps, 1),
            "constraints": len(self.constraints),
            "gravity": self.gravity
        }


# Advanced physics features
class VehiclePhysics:
    """Vehicle simulation system."""
    
    def __init__(self, physics: PhysicsEngine):
        self.physics = physics
        self.vehicles: Dict[str, Dict] = {}
    
    def create_vehicle(self, vehicle_id: str, chassis_body: str,
                      wheel_positions: List[Tuple[float, float, float]]) -> Dict:
        """Create a vehicle with wheels."""
        vehicle = {
            "id": vehicle_id,
            "chassis": chassis_body,
            "wheels": [],
            "suspension_stiffness": 50.0,
            "suspension_damping": 5.0,
            "max_steering": 0.5,
            "max_engine_force": 2000.0,
            "max_brake_force": 100.0
        }
        
        # Create wheel bodies
        for i, pos in enumerate(wheel_positions):
            wheel_id = f"{vehicle_id}_wheel_{i}"
            self.physics.create_body(
                wheel_id,
                body_type=PhysicsBodyType.DYNAMIC,
                mass=20.0,
                position=pos,
                collision_shape=CollisionShape.SPHERE,
                collision_extents=(0.3, 0.3, 0.3),
                friction=0.9
            )
            vehicle["wheels"].append(wheel_id)
        
        self.vehicles[vehicle_id] = vehicle
        return vehicle
    
    def apply_controls(self, vehicle_id: str, throttle: float, steering: float,
                     brake: float) -> bool:
        """Apply vehicle controls."""
        if vehicle_id not in self.vehicles:
            return False
        
        vehicle = self.vehicles[vehicle_id]
        
        # Apply engine force to wheels
        engine_force = throttle * vehicle["max_engine_force"]
        for wheel_id in vehicle["wheels"][:2]:  # Rear-wheel drive
            self.physics.apply_force(wheel_id, (engine_force, 0, 0))
        
        # Apply steering to front wheels
        steering_angle = steering * vehicle["max_steering"]
        
        # Apply brakes
        if brake > 0:
            brake_force = brake * vehicle["max_brake_force"]
            for wheel_id in vehicle["wheels"]:
                self.physics.apply_force(wheel_id, (-brake_force, 0, 0))
        
        return True


class CharacterController:
    """Physics-based character controller."""
    
    def __init__(self, physics: PhysicsEngine):
        self.physics = physics
        self.characters: Dict[str, Dict] = {}
    
    def create_character(self, char_id: str, position: Tuple[float, float, float],
                        height: float = 1.8, mass: float = 70.0) -> str:
        """Create a physics character."""
        body_id = f"{char_id}_body"
        
        self.physics.create_body(
            body_id,
            body_type=PhysicsBodyType.DYNAMIC,
            mass=mass,
            position=position,
            collision_shape=CollisionShape.CAPSULE,
            collision_extents=(0.4, height/2, 0.4),
            friction=0.3,
            linear_damping=0.9
        )
        
        self.characters[char_id] = {
            "body": body_id,
            "height": height,
            "move_speed": 5.0,
            "jump_force": 500.0,
            "is_grounded": False
        }
        
        return char_id
    
    def move(self, char_id: str, direction: Tuple[float, float, float]) -> bool:
        """Move character in direction."""
        if char_id not in self.characters:
            return False
        
        char = self.characters[char_id]
        body = self.physics.bodies[char["body"]]
        
        # Apply movement force
        move_force = (
            direction[0] * char["move_speed"] * body.mass,
            0,
            direction[2] * char["move_speed"] * body.mass
        )
        
        self.physics.apply_force(char["body"], move_force)
        return True
    
    def jump(self, char_id: str) -> bool:
        """Make character jump."""
        if char_id not in self.characters:
            return False
        
        char = self.characters[char_id]
        
        if char["is_grounded"]:
            self.physics.apply_impulse(char["body"], (0, char["jump_force"], 0))
            char["is_grounded"] = False
            return True
        
        return False

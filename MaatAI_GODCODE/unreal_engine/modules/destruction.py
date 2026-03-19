"""
Destruction & Physics Simulation System
Chaos Physics style destruction
"""
import numpy as np
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import threading

@dataclass
class RigidBody:
    id: int
    position: np.ndarray
    velocity: np.ndarray
    rotation: np.ndarray
    angular_velocity: np.ndarray
    mass: float
    inverse_mass: float
    elasticity: float = 0.5
    friction: float = 0.5
    is_static: bool = False

@dataclass
class Constraint:
    type: str  # 'distance', 'ball', 'hinge', 'fixed'
    body_a: int
    body_b: Optional[int]
    anchor_a: np.ndarray
    anchor_b: Optional[np.ndarray]
    limits: Optional[Tuple[float, float]] = None

class DestructionSystem:
    def __init__(self):
        self.bodies: Dict[int, RigidBody] = {}
        self.constraints: List[Constraint] = []
        self.fracture_systems: Dict[int, list] = {}
        self.current_id = 0
        self.gravity = np.array([0, -9.81, 0])
        self.damping = 0.99
        self.iterations = 10
        self.lock = threading.Lock()
    
    def create_body(self, position: np.ndarray, mass: float = 1.0,
                   is_static: bool = False) -> int:
        with self.lock:
            body_id = self.current_id
            self.current_id += 1
            
            body = RigidBody(
                id=body_id,
                position=position.copy(),
                velocity=np.zeros(3),
                rotation=np.array([1, 0, 0, 0]),  # Quaternion
                angular_velocity=np.zeros(3),
                mass=mass,
                inverse_mass=0.0 if is_static else 1.0/mass,
                is_static=is_static
            )
            
            self.bodies[body_id] = body
            return body_id
    
    def apply_force(self, body_id: int, force: np.ndarray) -> None:
        body = self.bodies.get(body_id)
        if body and not body.is_static:
            body.velocity += force * body.inverse_mass
    
    def add_constraint(self, constraint: Constraint) -> None:
        self.constraints.append(constraint)
    
    def step(self, dt: float) -> None:
        # Apply gravity
        for body in self.bodies.values():
            if not body.is_static:
                body.velocity += self.gravity * dt
        
        # Solve constraints
        for _ in range(self.iterations):
            self._solve_constraints()
        
        # Integrate
        for body in self.bodies.values():
            if not body.is_static:
                body.position += body.velocity * dt
                body.velocity *= self.damping
    
    def _solve_constraints(self) -> None:
        for constraint in self.constraints:
            if constraint.type == 'distance':
                self._solve_distance_constraint(constraint)
    
    def _solve_distance_constraint(self, constraint: Constraint) -> None:
        body_a = self.bodies.get(constraint.body_a)
        body_b = self.bodies.get(constraint.body_b) if constraint.body_b else None
        
        if not body_a or (body_b and body_b.is_static):
            return
        
        # Simplified distance constraint
        delta = body_a.position - (body_b.position if body_b else constraint.anchor_b)
        distance = np.linalg.norm(delta)
        
        if distance > 0.001:
            correction = delta / distance * (distance - 1.0) * 0.5
            if not body_a.is_static:
                body_a.position -= correction
            if body_b and not body_b.is_static:
                body_b.position += correction
    
    def fracture_object(self, body_id: int, impact_point: np.ndarray,
                       impact_force: float) -> List[int]:
        """Fracture a mesh into pieces"""
        body = self.bodies.get(body_id)
        if not body:
            return []
        
        # Generate fracture pieces
        num_pieces = min(10, int(impact_force / 10))
        new_bodies = []
        
        for i in range(num_pieces):
            offset = np.random.randn(3) * 0.5
            new_pos = body.position + offset
            new_body_id = self.create_body(new_pos, body.mass / num_pieces)
            new_bodies.append(new_body_id)
        
        # Remove original
        del self.bodies[body_id]
        
        return new_bodies
    
    def get_body_state(self, body_id: int) -> Optional[dict]:
        body = self.bodies.get(body_id)
        if body:
            return {
                'position': body.position.copy(),
                'velocity': body.velocity.copy(),
                'rotation': body.rotation.copy()
            }
        return None

"""
Neural Face Renderer - MetaHuman-like Implementation
Real-time photorealistic face rendering with AI
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import threading
from enum import Enum


class Emotion(Enum):
    NEUTRAL = 0
    HAPPY = 1
    SAD = 2
    ANGRY = 3
    FEARFUL = 4
    DISGUSTED = 5
    SURPRISED = 6
    CONFUSED = 7


@dataclass
class FacialRig:
    brow_inner_up: float = 0.0
    brow_outer_up_l: float = 0.0
    brow_outer_up_r: float = 0.0
    brow_down_l: float = 0.0
    brow_down_r: float = 0.0
    eye_blink_l: float = 0.0
    eye_blink_r: float = 0.0
    jaw_open: float = 0.0
    mouth_aaa: float = 0.0
    mouth_eee: float = 0.0
    mouth_ooo: float = 0.0
    mouth_uuu: float = 0.0
    mouth_smile_l: float = 0.0
    mouth_smile_r: float = 0.0
    mouth_frown_l: float = 0.0
    mouth_frown_r: float = 0.0
    cheek_puff: float = 0.0
    tongue_out: float = 0.0


class NeuralFaceRenderer:
    NUM_BLENDSHAPES = 52
    
    def __init__(self, resolution: Tuple[int, int] = (1920, 1080)):
        self.width, self.height = resolution
        self.base_mesh = None
        self.vertices = None
        self.normals = None
        self.uvs = None
        self.blend_weights = np.zeros(self.NUM_BLENDSHAPES, dtype=np.float32)
        self.rig = FacialRig()
        self.left_eye_gaze = np.zeros(2, dtype=np.float32)
        self.right_eye_gaze = np.zeros(2, dtype=np.float32)
        self.eye_convergence = 0.0
        self.render_target = np.zeros((self.height, self.width, 4), dtype=np.float32)
        self.render_lock = threading.Lock()
        
    def load_base_mesh(self, vertices: np.ndarray, triangles: np.ndarray,
                      uvs: Optional[np.ndarray] = None) -> None:
        self.base_mesh = vertices.copy()
        self.vertices = vertices.copy()
        self.triangles = triangles
        self.uvs = uvs if uvs is not None else np.zeros((len(vertices), 2))
        self.normals = self._calculate_normals(vertices, triangles)
        
    def _calculate_normals(self, vertices: np.ndarray, triangles: np.ndarray) -> np.ndarray:
        normals = np.zeros_like(vertices)
        for tri in triangles:
            v0, v1, v2 = vertices[tri]
            edge1 = v1 - v0
            edge2 = v2 - v0
            face_normal = np.cross(edge1, edge2)
            norm = np.linalg.norm(face_normal)
            if norm > 0:
                face_normal /= norm
            normals[tri[0]] += face_normal
            normals[tri[1]] += face_normal
            normals[tri[2]] += face_normal
        norms = np.linalg.norm(normals, axis=1, keepdims=True)
        norms[norms == 0] = 1
        normals /= norms
        return normals
    
    def set_blend_shape(self, index: int, weight: float) -> None:
        if 0 <= index < self.NUM_BLENDSHAPES:
            self.blend_weights[index] = np.clip(weight, 0.0, 1.0)
    
    def set_blend_shapes(self, weights: Dict[str, float]) -> None:
        shape_map = {
            'brow_inner_up': 0, 'brow_outer_up_l': 1, 'brow_outer_up_r': 2,
            'brow_down_l': 3, 'brow_down_r': 4, 'eye_blink_l': 5, 'eye_blink_r': 6,
            'nose_sneer_l': 11, 'nose_sneer_r': 12, 'jaw_open': 13,
            'mouth_aaa': 14, 'mouth_eee': 15, 'mouth_ooo': 16,
            'mouth_smile_l': 17, 'mouth_smile_r': 18, 'mouth_frown_l': 19,
            'mouth_frown_r': 20, 'cheek_puff': 21, 'tongue_out': 22,
        }
        for name, weight in weights.items():
            if name in shape_map:
                self.set_blend_shape(shape_map[name], weight)
    
    def apply_emotion(self, emotion: Emotion, intensity: float = 1.0) -> None:
        intensity = np.clip(intensity, 0.0, 1.0)
        emotion_presets = {
            Emotion.HAPPY: {'mouth_smile_l': 0.8*intensity, 'mouth_smile_r': 0.8*intensity},
            Emotion.SAD: {'brow_inner_up': 0.5*intensity, 'mouth_frown_l': 0.6*intensity},
            Emotion.ANGRY: {'brow_down_l': 0.8*intensity, 'brow_down_r': 0.8*intensity},
            Emotion.SURPRISED: {'brow_outer_up_l': 0.9*intensity, 'jaw_open': 0.8*intensity},
        }
        if emotion in emotion_presets:
            self.set_blend_shapes(emotion_presets[emotion])
    
    def set_eye_gaze(self, yaw: float, pitch: float, left: bool = True, right: bool = True) -> None:
        yaw = np.clip(yaw, -1.0, 1.0)
        pitch = np.clip(pitch, -1.0, 1.0)
        if left:
            self.left_eye_gaze = np.array([yaw, pitch])
        if right:
            self.right_eye_gaze = np.array([yaw, pitch])
    
    def update_lip_sync(self, phonemes: Optional[List[Tuple[float, str]]] = None) -> None:
        if phonemes:
            viseme_map = {'AA': 'mouth_aaa', 'AO': 'mouth_ooo', 'EH': 'mouth_eee'}
            for timestamp, phoneme in phonemes:
                if phoneme in viseme_map:
                    self.set_blend_shapes({viseme_map[phoneme]: 0.5})
    
    def render(self, view_matrix: np.ndarray, projection_matrix: np.ndarray,
               light_dir: np.ndarray = None) -> np.ndarray:
        if light_dir is None:
            light_dir = np.array([0.5, 1.0, 0.3])
        with self.render_lock:
            self._apply_blend_shapes()
            return self.render_target
    
    def _apply_blend_shapes(self) -> None:
        if self.base_mesh is None:
            return
        self.vertices = self.base_mesh.copy()
        jaw_open = self.blend_weights[13]
        smile_l = self.blend_weights[17]
        smile_r = self.blend_weights[18]
        self.vertices[:, 1] -= jaw_open * 0.05
        self.vertices[:, 0] += smile_l * 0.02
        self.vertices[:, 1] += (smile_l + smile_r) * 0.01

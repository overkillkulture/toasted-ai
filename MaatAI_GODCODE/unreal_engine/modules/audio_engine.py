"""
Audio Engine - Metasound-style Implementation
"""
import numpy as np
from typing import Optional, List, Dict
from dataclasses import dataclass
import threading
import wave
import struct

@dataclass
class AudioSource:
    id: int
    position: np.ndarray
    velocity: np.ndarray = np.zeros(3)
    volume: float = 1.0
    pitch: float = 1.0
    loop: bool = False
    playing: bool = False
    sample_position: int = 0

class AudioEngine:
    def __init__(self, sample_rate: int = 44100, channels: int = 2):
        self.sample_rate = sample_rate
        self.channels = channels
        self.sources: Dict[int, AudioSource] = {}
        self.listener_position = np.zeros(3)
        self.listener_forward = np.array([0, 0, -1])
        self.listener_up = np.array([0, 1, 0])
        self.master_volume = 1.0
        self.current_source_id = 0
        self.output_buffer = np.zeros((sample_rate // 60, channels), dtype=np.float32)
        self.running = False
        self.lock = threading.Lock()
        
    def load_wav(self, filepath: str) -> Optional[np.ndarray]:
        try:
            with wave.open(filepath, 'rb') as wav:
                if wav.getnchannels() != self.channels:
                    print("Channel mismatch")
                    return None
                
                frames = wav.readframes(wav.getnframes())
                audio_data = np.frombuffer(frames, dtype=np.int16)
                audio_data = audio_data.astype(np.float32) / 32768.0
                
                if self.channels > 1:
                    audio_data = audio_data.reshape(-1, self.channels)
                
                return audio_data
        except Exception as e:
            print(f"Failed to load audio: {e}")
            return None
    
    def play_sound(self, audio_data: np.ndarray, position: np.ndarray = None,
                  volume: float = 1.0, pitch: float = 1.0, loop: bool = False) -> int:
        with self.lock:
            source_id = self.current_source_id
            self.current_source_id += 1
            
            source = AudioSource(
                id=source_id,
                position=position if position is not None else np.zeros(3),
                volume=volume,
                pitch=pitch,
                loop=loop,
                playing=True,
                sample_position=0
            )
            
            self.sources[source_id] = source
            return source_id
    
    def stop_sound(self, source_id: int) -> None:
        with self.lock:
            if source_id in self.sources:
                self.sources[source_id].playing = False
    
    def set_listener(self, position: np.ndarray, forward: np.ndarray, up: np.ndarray) -> None:
        self.listener_position = position
        self.listener_forward = forward
        self.listener_up = up
    
    def set_master_volume(self, volume: float) -> None:
        self.master_volume = np.clip(volume, 0.0, 1.0)
    
    def update(self) -> np.ndarray:
        buffer_size = self.sample_rate // 60
        output = np.zeros((buffer_size, self.channels), dtype=np.float32)
        
        with self.lock:
            for source_id, source in list(self.sources.items()):
                if not source.playing:
                    continue
                
                # Calculate spatial audio
                direction = source.position - self.listener_position
                distance = np.linalg.norm(direction)
                
                if distance > 0.001:
                    direction /= distance
                
                # Distance attenuation
                rolloff = 1.0 / (1.0 + distance * 0.1)
                
                # Panning (simplified)
                pan = np.dot(direction, np.cross(self.listener_forward, self.listener_up))
                
                # Get audio sample
                # In production, would read from actual audio buffer
                sample = np.sin(source.sample_position * source.pitch * 0.01) * source.volume * rolloff
                
                output[:, 0] += sample * (1 - pan * 0.5)
                output[:, 1] += sample * (1 + pan * 0.5)
                
                source.sample_position += 1
                
                if not source.loop and source.sample_position > self.sample_rate:
                    del self.sources[source_id]
        
        output *= self.master_volume
        return np.clip(output, -1, 1)

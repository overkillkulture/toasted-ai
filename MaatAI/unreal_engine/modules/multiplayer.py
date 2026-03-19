"""
Multiplayer & Networking Framework
"""
import numpy as np
import threading
import socket
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import struct
import time

class MessageType(Enum):
    CONNECT = 1
    DISCONNECT = 2
    PLAYER_STATE = 3
    WORLD_UPDATE = 4
    CHAT = 5
    RPC = 6

@dataclass
class NetworkConfig:
    max_players: int = 64
    tick_rate: int = 60
    timeout: float = 30.0
    compression: bool = True

class Player:
    def __init__(self, id: int, address: tuple):
        self.id = id
        self.address = address
        self.position = np.zeros(3)
        self.rotation = np.zeros(3)
        self.velocity = np.zeros(3)
        self.last_update = time.time()

class MultiplayerFramework:
    def __init__(self, config: NetworkConfig = None):
        self.config = config or NetworkConfig()
        self.players: Dict[int, Player] = {}
        self.local_player_id = None
        self.server_socket = None
        self.client_socket = None
        self.running = False
        self.message_queue = []
        self.lock = threading.Lock()
        self.handlers: Dict[MessageType, Callable] = {}
        self.tick_callbacks: List[Callable] = []
        self.world_state = {}
        
    def start_server(self, port: int = 7777) -> bool:
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('', port))
            self.server_socket.settimeout(0.1)
            self.running = True
            
            # Start network thread
            self.network_thread = threading.Thread(target=self._server_loop)
            self.network_thread.start()
            
            # Start tick loop
            self.tick_thread = threading.Thread(target=self._tick_loop)
            self.tick_thread.start()
            
            return True
        except Exception as e:
            print(f"Server start failed: {e}")
            return False
    
    def connect(self, host: str, port: int) -> bool:
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client_socket.settimeout(5.0)
            
            # Send connect message
            self._send_message(MessageType.CONNECT, b'', (host, port))
            self.running = True
            
            # Start receive thread
            self.network_thread = threading.Thread(target=self._client_loop)
            self.network_thread.start()
            
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def _server_loop(self):
        while self.running:
            try:
                data, addr = self.server_socket.recvfrom(4096)
                if data:
                    self._handle_packet(data, addr)
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Server error: {e}")
    
    def _client_loop(self):
        while self.running:
            try:
                data, addr = self.client_socket.recvfrom(4096)
                if data:
                    self._handle_packet(data, addr)
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Client error: {e}")
    
    def _tick_loop(self):
        tick_time = 1.0 / self.config.tick_rate
        while self.running:
            start = time.time()
            
            # Run tick callbacks
            for callback in self.tick_callbacks:
                callback(tick_time)
            
            # Broadcast world state
            if self.server_socket:
                self._broadcast_world_state()
            
            elapsed = time.time() - start
            if elapsed < tick_time:
                time.sleep(tick_time - elapsed)
    
    def _handle_packet(self, data: bytes, addr: tuple):
        if len(data) < 5:
            return
        
        msg_type = MessageType(data[0])
        player_id = struct.unpack('I', data[1:5])[0]
        payload = data[5:]
        
        with self.lock:
            if msg_type == MessageType.CONNECT:
                if len(self.players) < self.config.max_players:
                    player = Player(player_id, addr)
                    self.players[player_id] = player
                    print(f"Player {player_id} connected from {addr}")
            elif msg_type == MessageType.DISCONNECT:
                if player_id in self.players:
                    del self.players[player_id]
            elif msg_type == MessageType.PLAYER_STATE:
                if player_id in self.players:
                    self._update_player_state(player_id, payload)
            
            # Call registered handlers
            if msg_type in self.handlers:
                self.handlers[msg_type](player_id, payload)
    
    def _update_player_state(self, player_id: int, data: bytes):
        player = self.players.get(player_id)
        if player and len(data) == 36:  # 3*4 + 3*4 + 3*4 = 36 bytes
            player.position = np.array(struct.unpack('fff', data[0:12]))
            player.rotation = np.array(struct.unpack('fff', data[12:24]))
            player.velocity = np.array(struct.unpack('fff', data[24:36]))
            player.last_update = time.time()
    
    def _send_message(self, msg_type: MessageType, payload: bytes, addr: tuple):
        data = bytes([msg_type.value]) + struct.pack('I', 0) + payload
        
        if self.server_socket:
            self.server_socket.sendto(data, addr)
        elif self.client_socket:
            self.client_socket.sendto(data, addr)
    
    def _broadcast_world_state(self):
        import json
        state = {
            'players': {
                pid: {
                    'pos': p.position.tolist(),
                    'rot': p.rotation.tolist()
                }
                for pid, p in self.players.items()
            },
            'world': self.world_state
        }
        
        payload = json.dumps(state).encode()
        
        for player in self.players.values():
            self._send_message(MessageType.WORLD_UPDATE, payload, player.address)
    
    def register_handler(self, msg_type: MessageType, handler: Callable):
        self.handlers[msg_type] = handler
    
    def register_tick_callback(self, callback: Callable):
        self.tick_callbacks.append(callback)
    
    def set_world_state(self, key: str, value):
        self.world_state[key] = value
    
    def disconnect(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()

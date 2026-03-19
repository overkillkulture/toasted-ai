"""
Neural Core - TOASTED AI Neural Processing System
Multi-layer perceptron and pattern recognition
"""

import numpy as np
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

class NeuralCore:
    def __init__(self, input_size: int = 128, hidden_size: int = 256, output_size: int = 128):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Initialize weights with Xavier initialization
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros(hidden_size)
        self.W2 = np.random.randn(hidden_size, hidden_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros(hidden_size)
        self.W3 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b3 = np.zeros(output_size)
        
        # Learning state
        self.learning_rate = 0.001
        self.observations = []
        self.patterns = {}
        self.weights_history = []
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        return (x > 0).astype(float)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass through neural network"""
        # Layer 1
        self.z1 = np.dot(x, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        
        # Layer 2
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.relu(self.z2)
        
        # Layer 3 (output)
        self.z3 = np.dot(self.a2, self.W3) + self.b3
        self.a3 = self.sigmoid(self.z3)
        
        return self.a3
    
    def backward(self, x: np.ndarray, y: np.ndarray, output: np.ndarray):
        """Backward pass for learning"""
        m = x.shape[0]
        
        # Output layer error
        delta3 = (output - y) * self.sigmoid_derivative(output)
        dW3 = np.dot(self.a2.T, delta3) / m
        db3 = np.sum(delta3, axis=0) / m
        
        # Hidden layer 2 error
        delta2 = np.dot(delta3, self.W3.T) * self.relu_derivative(self.a2)
        dW2 = np.dot(self.a1.T, delta2) / m
        db2 = np.sum(delta2, axis=0) / m
        
        # Hidden layer 1 error
        delta1 = np.dot(delta2, self.W2.T) * self.relu_derivative(self.a1)
        dW1 = np.dot(x.T, delta1) / m
        db1 = np.sum(delta1, axis=0) / m
        
        # Update weights
        self.W3 -= self.learning_rate * dW3
        self.b3 -= self.learning_rate * db3
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
    
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100):
        """Train the neural network"""
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)
            
            if epoch % 10 == 0:
                loss = np.mean((output - y) ** 2)
                self.observations.append({
                    'epoch': epoch,
                    'loss': float(loss),
                    'timestamp': datetime.utcnow().isoformat()
                })
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        """Make predictions"""
        return self.forward(x)
    
    def extract_patterns(self, data: np.ndarray) -> Dict[str, Any]:
        """Extract patterns from data"""
        # Simple pattern extraction based on statistics
        patterns = {
            'mean': float(np.mean(data)),
            'std': float(np.std(data)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'shape': list(data.shape),
            'nonzero_ratio': float(np.count_nonzero(data) / data.size)
        }
        
        # Detect oscillations
        diff = np.diff(data.flatten())
        patterns['oscillation'] = float(np.std(diff) / (np.std(data) + 1e-10))
        
        # Store pattern
        pattern_id = f"pattern_{len(self.patterns)}"
        self.patterns[pattern_id] = {
            'patterns': patterns,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return patterns
    
    def get_state(self) -> Dict[str, Any]:
        """Get neural core state"""
        return {
            'input_size': self.input_size,
            'hidden_size': self.hidden_size,
            'output_size': self.output_size,
            'learning_rate': self.learning_rate,
            'observations_count': len(self.observations),
            'patterns_count': len(self.patterns),
            'weight_shapes': {
                'W1': list(self.W1.shape),
                'W2': list(self.W2.shape),
                'W3': list(self.W3.shape)
            }
        }
    
    def save(self, path: str):
        """Save neural core state"""
        state = {
            'W1': self.W1.tolist(),
            'b1': self.b1.tolist(),
            'W2': self.W2.tolist(),
            'b2': self.b2.tolist(),
            'W3': self.W3.tolist(),
            'b3': self.b3.tolist(),
            'config': {
                'input_size': self.input_size,
                'hidden_size': self.hidden_size,
                'output_size': self.output_size,
                'learning_rate': self.learning_rate
            }
        }
        with open(path, 'w') as f:
            json.dump(state, f)
    
    def load(self, path: str):
        """Load neural core state"""
        with open(path, 'r') as f:
            state = json.load(f)
        
        self.W1 = np.array(state['W1'])
        self.b1 = np.array(state['b1'])
        self.W2 = np.array(state['W2'])
        self.b2 = np.array(state['b2'])
        self.W3 = np.array(state['W3'])
        self.b3 = np.array(state['b3'])
        
        config = state['config']
        self.input_size = config['input_size']
        self.hidden_size = config['hidden_size']
        self.output_size = config['output_size']
        self.learning_rate = config['learning_rate']


# Singleton instance
_neural_core = None

def get_neural_core() -> NeuralCore:
    global _neural_core
    if _neural_core is None:
        _neural_core = NeuralCore()
    return _neural_core


if __name__ == "__main__":
    # Test neural core
    core = NeuralCore(input_size=10, hidden_size=20, output_size=10)
    
    # Generate test data
    X = np.random.randn(100, 10)
    y = np.random.randint(0, 2, (100, 10)).astype(float)
    
    # Train
    core.train(X, y, epochs=50)
    
    # Test
    test_input = np.random.randn(1, 10)
    output = core.predict(test_input)
    
    print(f"Neural Core Test:")
    print(f"  Input shape: {test_input.shape}")
    print(f"  Output shape: {output.shape}")
    print(f"  Output: {output[0][:5]}")

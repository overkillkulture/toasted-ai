#!/usr/bin/env python3
"""
Idea Generator - Observes system and generates improvement ideas
"""

import os
import sys
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import deque
import uuid

sys.path.insert(0, '/home/workspace/MaatAI')


class IdeaGenerator:
    """Generates ideas based on system observations."""
    
    def __init__(self):
        self.ideas = deque(maxlen=100)
        self.observations = deque(maxlen=1000)
        self.implemented = []
        self._lock = threading.Lock()
        self.last_idea_time = 0
        self.idea_cooldown = 60  # seconds
        
    def add_observation(self, component: str, metric: str, value: Any) -> None:
        """Add an observation."""
        obs = {
            'id': str(uuid.uuid4()),
            'component': component,
            'metric': metric,
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        with self._lock:
            self.observations.append(obs)
            
    def generate_ideas(self, force: bool = False) -> List[Dict]:
        """Generate new ideas based on observations."""
        now = time.time()
        
        # Rate limiting
        if not force and (now - self.last_idea_time) < self.idea_cooldown:
            return []
            
        with self._lock:
            recent = list(self.observations)[-100:]
            
        if not recent:
            return []
            
        new_ideas = []
        
        # Analyze patterns
        component_counts = {}
        metric_counts = {}
        for obs in recent:
            c = obs.get('component', 'unknown')
            m = obs.get('metric', 'unknown')
            component_counts[c] = component_counts.get(c, 0) + 1
            metric_counts[m] = metric_counts.get(m, 0) + 1
            
        # Idea: High activity component
        if component_counts:
            most_active = max(component_counts.items(), key=lambda x: x[1])
            if most_active[1] > 20:
                new_ideas.append({
                    'id': str(uuid.uuid4()),
                    'category': 'optimization',
                    'title': f'High Activity: {most_active[0]}',
                    'description': f'{most_active[0]} has {most_active[1]} observations. Consider caching or optimization.',
                    'priority': 'high' if most_active[1] > 50 else 'medium',
                    'based_on': {'component': most_active[0], 'count': most_active[1]},
                    'timestamp': datetime.now().isoformat()
                })
                
        # Idea: Frequent metrics
        if metric_counts:
            frequent = [m for m, c in metric_counts.items() if c > 15]
            if frequent:
                new_ideas.append({
                    'id': str(uuid.uuid4()),
                    'category': 'efficiency',
                    'title': 'Frequent Metric Collection',
                    'description': f'Metrics {frequent} are collected frequently. Consider aggregation or sampling.',
                    'priority': 'low',
                    'based_on': {'metrics': frequent},
                    'timestamp': datetime.now().isoformat()
                })
                
        # Idea: Self-improvement milestone
        obs_count = len(self.observations)
        if obs_count > 0 and obs_count % 100 == 0:
            new_ideas.append({
                'id': str(uuid.uuid4()),
                'category': 'self_improvement',
                'title': 'Self-Improvement Trigger',
                'description': f'{obs_count} observations recorded. Time for self-improvement cycle.',
                'priority': 'high',
                'based_on': {'observation_count': obs_count},
                'timestamp': datetime.now().isoformat()
            })
            
        # Store ideas
        with self._lock:
            for idea in new_ideas:
                self.ideas.append(idea)
                
        self.last_idea_time = now
        return new_ideas
        
    def get_ideas(self, filter_type: str = 'all', limit: int = 20) -> List[Dict]:
        """Get ideas with optional filtering."""
        with self._lock:
            ideas = list(self.ideas)
            
        if filter_type == 'implemented':
            ideas = [i for i in ideas if i.get('implemented')]
        elif filter_type == 'pending':
            ideas = [i for i in ideas if not i.get('implemented')]
        elif filter_type == 'high':
            ideas = [i for i in ideas if i.get('priority') == 'high']
            
        return ideas[-limit:]
        
    def mark_implemented(self, idea_id: str) -> bool:
        """Mark an idea as implemented."""
        with self._lock:
            for idea in self.ideas:
                if idea.get('id') == idea_id:
                    idea['implemented'] = True
                    idea['implemented_at'] = datetime.now().isoformat()
                    self.implemented.append(idea)
                    return True
        return False
        
    def get_stats(self) -> Dict:
        """Get idea generator statistics."""
        with self._lock:
            return {
                'total_ideas': len(self.ideas),
                'implemented': len(self.implemented),
                'pending': len([i for i in self.ideas if not i.get('implemented')]),
                'total_observations': len(self.observations),
                'last_idea_time': self.last_idea_time
            }


# Singleton
_generator = None

def get_generator() -> IdeaGenerator:
    """Get or create the idea generator."""
    global _generator
    if _generator is None:
        _generator = IdeaGenerator()
    return _generator

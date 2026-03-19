"""
Progress Tracker
Tracks actual progress, not just concepts.
Measures reality, not just intentions.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

class ProgressTracker:
    """
    Tracks actual progress made by the system.
    Measures reality transformation, not just activity.
    """
    
    def __init__(self):
        self.progress_log = []
        self.milestones = []
        self.progress_file = '/home/workspace/MaatAI/reality_engine/progress/progress_log.jsonl'
        os.makedirs(os.path.dirname(self.progress_file), exist_ok=True)
        
        # Progress metrics
        self.metrics = {
            'concepts_processed': 0,
            'actions_executed': 0,
            'artifacts_created': 0,
            'code_generated': 0,
            'documents_created': 0,
            'security_audits': 0,
            'knowledge_entries': 0,
            'protocols_run': 0,
            'optimizations_applied': 0,
            'integrations_completed': 0
        }
        
        # Progress velocity (change per time unit)
        self.velocity = defaultdict(list)
        
    def record(self, results: Dict):
        """
        Record progress results.
        
        Args:
            results: Dict with progress metrics
        """
        timestamp = datetime.utcnow().isoformat()
        
        # Update metrics
        self.metrics['concepts_processed'] += results.get('concepts_received', 0)
        self.metrics['actions_executed'] += results.get('actions_executed', 0)
        self.metrics['artifacts_created'] += results.get('reality_verified', 0)
        
        # Record velocity
        self.velocity['concepts'].append(results.get('concepts_received', 0))
        self.velocity['actions'].append(results.get('actions_executed', 0))
        
        # Log entry
        entry = {
            'timestamp': timestamp,
            'results': results,
            'cumulative_metrics': self.metrics.copy()
        }
        
        self.progress_log.append(entry)
        
        # Save to file
        with open(self.progress_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        # Check for milestones
        self._check_milestones()
    
    def _check_milestones(self):
        """Check and record milestones."""
        milestones_to_check = [
            (100, 'concepts_processed', 'Concept Century'),
            (100, 'actions_executed', 'Action Century'),
            (10, 'artifacts_created', 'Artifact Decade'),
            (50, 'code_generated', 'Code Half-Century'),
        ]
        
        for threshold, metric, name in milestones_to_check:
            if self.metrics.get(metric, 0) >= threshold:
                milestone_key = f"{name}_{threshold}"
                if milestone_key not in [m['key'] for m in self.milestones]:
                    milestone = {
                        'key': milestone_key,
                        'name': name,
                        'metric': metric,
                        'value': self.metrics[metric],
                        'achieved_at': datetime.utcnow().isoformat()
                    }
                    self.milestones.append(milestone)
    
    def get_progress_report(self) -> Dict:
        """Generate progress report."""
        total_actions = self.metrics['actions_executed']
        total_concepts = self.metrics['concepts_processed']
        
        # Calculate velocity
        avg_concepts_per_cycle = sum(self.velocity['concepts'][-10:]) / max(len(self.velocity['concepts'][-10:]), 1)
        avg_actions_per_cycle = sum(self.velocity['actions'][-10:]) / max(len(self.velocity['actions'][-10:]), 1)
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': self.metrics,
            'milestones_achieved': len(self.milestones),
            'milestones': self.milestones[-5:],  # Last 5 milestones
            'velocity': {
                'avg_concepts_per_cycle': avg_concepts_per_cycle,
                'avg_actions_per_cycle': avg_actions_per_cycle,
                'progress_rate': total_actions / max(total_concepts, 1)
            },
            'progress_percentage': min(100, (total_actions / max(total_concepts, 1)) * 100),
            'status': 'active' if total_actions > 0 else 'stasis'
        }
    
    def get_velocity_trend(self) -> Dict:
        """Get velocity trend analysis."""
        if len(self.velocity['concepts']) < 2:
            return {'trend': 'insufficient_data'}
        
        recent = sum(self.velocity['concepts'][-5:])
        previous = sum(self.velocity['concepts'][-10:-5])
        
        if previous == 0:
            return {'trend': 'starting_up'}
        
        change = (recent - previous) / previous * 100
        
        return {
            'trend': 'increasing' if change > 0 else 'decreasing' if change < 0 else 'stable',
            'change_percent': change
        }

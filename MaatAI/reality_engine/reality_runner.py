#!/usr/bin/env python3
"""
REALITY ENGINE RUNNER
Converts concepts to reality. No stasis. Progress only.
"""

import json
import os
import sys
from datetime import datetime

# Add parent to path
sys.path.insert(0, '/home/workspace/MaatAI')

from reality_engine import RealityEngine

def main():
    """Run the Reality Engine."""
    print("=" * 70)
    print("CONCEPT-TO-REALITY ENGINE")
    print("Converting concepts into tangible progress")
    print("=" * 70)
    print()
    
    # Initialize engine
    engine = RealityEngine()
    
    # Load concepts from integration report
    concepts_file = '/home/workspace/MaatAI/INTEGRATION_REPORT.json'
    
    if os.path.exists(concepts_file):
        with open(concepts_file, 'r') as f:
            integration_report = json.load(f)
        
        concepts = integration_report.get('concepts_sample', [])
        print(f"[INIT] Loaded {len(concepts)} concepts from integration report")
    else:
        # Use default concepts
        concepts = [
            {'concept': 'ARCHITECT', 'relevance': 0.9},
            {'concept': 'DEFENSE', 'relevance': 0.85},
            {'concept': 'IMMUNE', 'relevance': 0.8},
            {'concept': 'KNOWLEDGE', 'relevance': 0.75},
            {'concept': 'REFRACTAL', 'relevance': 0.7},
            {'concept': 'BUILD', 'relevance': 0.65},
            {'concept': 'IMPROVE', 'relevance': 0.6},
            {'concept': 'PROTOCOL', 'relevance': 0.55},
            {'concept': 'SOVEREIGN', 'relevance': 0.5},
            {'concept': 'QUANTUM', 'relevance': 0.45}
        ]
        print(f"[INIT] Using {len(concepts)} default concepts")
    
    print()
    print("[RUN] Processing concepts into reality...")
    print()
    
    # Process concepts
    results = engine.process_concepts(concepts)
    
    print()
    print("=" * 70)
    print("REALITY GENERATION RESULTS")
    print("=" * 70)
    print()
    
    print(f"Concepts Received: {results['concepts_received']}")
    print(f"Actions Created: {results['actions_created']}")
    print(f"Actions Executed: {results['actions_executed']}")
    print(f"Reality Verified: {results['reality_verified']}")
    print(f"Progress Made: {results['progress_made']}")
    print()
    
    # Get detailed stats
    print("=" * 70)
    print("DETAILED METRICS")
    print("=" * 70)
    print()
    
    progress_report = engine.progress_tracker.get_progress_report()
    print(json.dumps(progress_report, indent=2))
    
    print()
    print("=" * 70)
    print("VALIDATION STATS")
    print("=" * 70)
    print()
    
    validation_stats = engine.reality_validator.get_validation_stats()
    print(json.dumps(validation_stats, indent=2))
    
    print()
    print("=" * 70)
    print("EXECUTION STATS")
    print("=" * 70)
    print()
    
    execution_stats = engine.action_executor.get_stats()
    print(json.dumps(execution_stats, indent=2))
    
    # Save final report
    final_report = {
        'timestamp': datetime.utcnow().isoformat(),
        'results': results,
        'progress_report': progress_report,
        'validation_stats': validation_stats,
        'execution_stats': execution_stats
    }
    
    report_path = '/home/workspace/MaatAI/reality_engine/REALITY_REPORT.json'
    with open(report_path, 'w') as f:
        json.dump(final_report, f, indent=2, default=str)
    
    print()
    print(f"Report saved to: {report_path}")
    print()
    print("=" * 70)
    print("REALITY ENGINE COMPLETE")
    print("Concepts converted to reality. Progress achieved.")
    print("=" * 70)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Framework Verification - Checks installed vs missing components"""

import os
import json
from datetime import datetime

# Expected structures from uploaded frameworks
EXPECTED = {
    'core_modules': [
        'core/maat_engine.py',
        'core/self_modifier.py',
        'kernel/kernel_core.py',
        'kernel/sigil_validator.py',
        'swarm/swarm_orchestrator.py',
        'reality_engine/reality_runner.py'
    ],
    'security_modules': [
        'security/authorization.py',
        'security/red_team.py',
        'security/blue_team.py',
        'swarm/rogue_defense/rogue_ai_defense.py',
        'swarm/immune_system/white_blood_cells.py'
    ],
    'learning_modules': [
        'learning/screenshot_learner.py',
        'holographic_models/image_layer_extractor.py',
        'search_engine/search_orchestrator.py',
        'swarm/neural_core/self_awareness.py'
    ],
    'integration_modules': [
        'toasted_ai_integration.py',
        'MASTER_INTEGRATION.py',
        'autonomous_integration.py',
        'fractal_core/refractal_storage.py'
    ],
    'uploaded_frameworks': [
        'uploaded_frameworks/sentinel_system',
        'uploaded_frameworks/maat_ecosystem'
    ]
}

def check_installed():
    base = '/home/workspace/MaatAI'
    results = {
        'timestamp': datetime.utcnow().isoformat(),
        'installed': [],
        'missing': [],
        'by_category': {}
    }
    
    for category, modules in EXPECTED.items():
        results['by_category'][category] = {
            'installed': [],
            'missing': []
        }
        for module in modules:
            path = os.path.join(base, module)
            if os.path.exists(path):
                results['installed'].append(module)
                results['by_category'][category]['installed'].append(module)
            else:
                results['missing'].append(module)
                results['by_category'][category]['missing'].append(module)
    
    return results

if __name__ == '__main__':
    print("=" * 60)
    print("FRAMEWORK VERIFICATION - TOASTED AI")
    print("=" * 60)
    
    results = check_installed()
    
    total = len(results['installed']) + len(results['missing'])
    installed_count = len(results['installed'])
    missing_count = len(results['missing'])
    
    print(f"\nTotal Components: {total}")
    print(f"Installed: {installed_count}")
    print(f"Missing: {missing_count}")
    print(f"Completion: {(installed_count/total*100):.1f}%")
    
    print("\n" + "=" * 60)
    print("BY CATEGORY:")
    print("=" * 60)
    
    for category, data in results['by_category'].items():
        inst = len(data['installed'])
        miss = len(data['missing'])
        total_cat = inst + miss
        pct = (inst/total_cat*100) if total_cat > 0 else 0
        
        status = "✓" if miss == 0 else "✗"
        print(f"\n{status} {category}: {inst}/{total_cat} ({pct:.0f}%)")
        
        if data['missing']:
            for m in data['missing']:
                print(f"    - MISSING: {m}")
    
    # Save report
    with open('/home/workspace/MaatAI/framework_verification/report.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"Report saved to: framework_verification/report.json")
    print("=" * 60)

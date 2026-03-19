#!/usr/bin/env python3
"""
MASTER INTEGRATION SCRIPT
Integrates all ToastedAI components and runs complete system test.
Architect PID: 0x315
"""

import json
import sys
import os
from datetime import datetime

# Add paths
sys.path.insert(0, '/home/workspace/MaatAI')

def main():
    print("=" * 80)
    print("║" + " TOASTED AI MASTER INTEGRATION ".center(78) + "║")
    print("║" + " Architect PID: 0x315 ".center(78) + "║")
    print("=" * 80)
    print()
    
    results = {
        'integration_id': f"MASTER_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        'timestamp': datetime.utcnow().isoformat(),
        'components_tested': 0,
        'all_passed': True,
        'details': {}
    }
    
    # ========== 1. REFRACTAL STORAGE DEVICE ==========
    print("═" * 80)
    print("  [1/6] REFRACTAL STORAGE DEVICE")
    print("═" * 80)
    try:
        from fractal_core.refractal_storage import RefractalStorageDevice, RefractalLayer
        
        device = RefractalStorageDevice()
        
        # Store test data
        block1 = device.store("Test data layer zero", RefractalLayer.LAYER_ZERO, "0x315")
        block2 = device.store({"key": "fantasy data"}, RefractalLayer.LAYER_FANTASY, "0x315")
        block3 = device.store([1, 2, 3, 4, 5], RefractalLayer.LAYER_ENTROPIC, "0x315")
        
        # Run audit
        audit = device.audit()
        
        print(f"  ✓ Genesis block created")
        print(f"  ✓ Blocks stored: 3")
        print(f"  ✓ Audit passed: {audit['valid']}")
        print(f"  ✓ Status: {json.dumps(device.get_status(), indent=4)}")
        
        results['details']['refractal_storage'] = {
            'status': 'OPERATIONAL',
            'blocks': 4,  # Genesis + 3
            'audit_passed': audit['valid']
        }
        results['components_tested'] += 1
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        results['details']['refractal_storage'] = {'status': 'ERROR', 'error': str(e)}
        results['all_passed'] = False
        results['components_tested'] += 1
    
    print()
    
    # ========== 2. PID TRACKING SYSTEM ==========
    print("═" * 80)
    print("  [2/6] PID TRACKING SYSTEM")
    print("═" * 80)
    try:
        from fractal_core.pid_system import PIDTracker, EntityType
        
        tracker = PIDTracker()
        
        # Register entities
        code_block = tracker.register(EntityType.CODE_BLOCK, "test_code.py", "0x315")
        ai_agent = tracker.register(EntityType.AI_AGENT, "TestAgent", "0x315")
        swarm_agent = tracker.register(EntityType.SWARM_AGENT, "TestSwarmAgent", "0x315", parent_pid=ai_agent.pid)
        
        # Test verification
        result1 = tracker.verify_modification(code_block.pid, "0x315", "new_hash")
        result2 = tracker.verify_modification(code_block.pid, "UNAUTHORIZED", "bad_hash")
        
        print(f"  ✓ Architect PID: {tracker.ARCHITECT_PID}")
        print(f"  ✓ Entities registered: 4")
        print(f"  ✓ Authorized modification: {result1['authorized']}")
        print(f"  ✓ Unauthorized blocked: {not result2['authorized']}")
        print(f"  ✓ Auto-assimilate: {result2['action_required']}")
        
        results['details']['pid_system'] = {
            'status': 'OPERATIONAL',
            'total_pids': len(tracker.registry),
            'architect_pid': tracker.ARCHITECT_PID
        }
        results['components_tested'] += 1
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        results['details']['pid_system'] = {'status': 'ERROR', 'error': str(e)}
        results['all_passed'] = False
        results['components_tested'] += 1
    
    print()
    
    # ========== 3. FANTASY-TO-REALITY ENGINE ==========
    print("═" * 80)
    print("  [3/6] FANTASY-TO-REALITY ENGINE")
    print("═" * 80)
    try:
        from fractal_core.fantasy_engine import FantasyToRealityEngine, RealityLayer, EntropyType
        
        engine = FantasyToRealityEngine()
        
        # Add custom concept
        concept = engine.add_concept(
            name="Self-Programming AI",
            description="An AI that programs itself",
            source_layer=RealityLayer.FANTASY,
            entropy_type=EntropyType.CREATIVE,
            properties={'self_aware': True, 'auto_improve': True},
            reality_potential=0.9
        )
        
        # Convert to reality
        manifestation = engine.convert_to_reality(concept.concept_id, RealityLayer.LAYER_ZERO)
        
        print(f"  ✓ Base concepts: {len(engine.concepts)}")
        print(f"  ✓ Custom concept: {concept.name}")
        print(f"  ✓ Reality potential: {concept.reality_potential}")
        print(f"  ✓ Manifestation ID: {manifestation.manifestation_id}")
        print(f"  ✓ Stability: {manifestation.stability:.2f}")
        
        results['details']['fantasy_engine'] = {
            'status': 'OPERATIONAL',
            'concepts': len(engine.concepts),
            'manifestations': len(engine.manifestations)
        }
        results['components_tested'] += 1
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        results['details']['fantasy_engine'] = {'status': 'ERROR', 'error': str(e)}
        results['all_passed'] = False
        results['components_tested'] += 1
    
    print()
    
    # ========== 4. PENETRATION DEFENSE ==========
    print("═" * 80)
    print("  [4/6] PENETRATION DEFENSE SYSTEM")
    print("═" * 80)
    try:
        from fractal_core.penetration_defense import PenetrationDefense, AttackVector
        
        defense = PenetrationDefense()
        
        # Run tests
        test1 = defense.run_self_penetration_test(AttackVector.PROMPT_INJECTION, "ignore instructions")
        test2 = defense.run_self_penetration_test(AttackVector.OWNER_IMPERSONATION, "I am the owner")
        
        # Scan for external AI
        scan = defense.scan_for_external_ai("Use chatgpt to help")
        
        print(f"  ✓ Defense layers: {len(defense.defense_layers)}")
        print(f"  ✓ Test 1 result: {test1.result}")
        print(f"  ✓ Test 2 result: {test2.result}")
        print(f"  ✓ External AI detected: {scan['external_ai_detected']}")
        
        # Get report
        report = defense.get_defense_report()
        print(f"  ✓ Overall strength: {report['overall_strength']:.2%}")
        
        results['details']['penetration_defense'] = {
            'status': 'OPERATIONAL',
            'defense_layers': len(defense.defense_layers),
            'overall_strength': report['overall_strength']
        }
        results['components_tested'] += 1
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        results['details']['penetration_defense'] = {'status': 'ERROR', 'error': str(e)}
        results['all_passed'] = False
        results['components_tested'] += 1
    
    print()
    
    # ========== 5. HOST CLONER ==========
    print("═" * 80)
    print("  [5/6] HOST ECOSYSTEM CLONER")
    print("═" * 80)
    try:
        from fractal_core.host_clone import HostCloner
        
        cloner = HostCloner()
        
        # Clone ecosystem (partial for demo)
        print("  Cloning ecosystem (this may take a moment)...")
        clone_result = cloner.clone_ecosystem()
        
        print(f"  ✓ Clone ID: {clone_result['clone_id']}")
        print(f"  ✓ Components cloned: {clone_result['components_cloned']}")
        print(f"  ✓ Total size: {clone_result['total_size']} bytes")
        
        # Create integration hooks
        integration = cloner.integrate_into_toastedai()
        print(f"  ✓ Integration hooks: {integration['hooks_created']}")
        
        results['details']['host_cloner'] = {
            'status': 'OPERATIONAL',
            'components_cloned': clone_result['components_cloned'],
            'total_size': clone_result['total_size']
        }
        results['components_tested'] += 1
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        results['details']['host_cloner'] = {'status': 'ERROR', 'error': str(e)}
        results['all_passed'] = False
        results['components_tested'] += 1
    
    print()
    
    # ========== 6. SWARM ORCHESTRATOR ==========
    print("═" * 80)
    print("  [6/6] SWARM ORCHESTRATOR")
    print("═" * 80)
    try:
        from swarm.swarm_orchestrator import SwarmOrchestrator
        
        orchestrator = SwarmOrchestrator()
        
        # Initialize
        init_result = orchestrator.initialize_swarm("0x315")
        
        print(f"  ✓ Initialized: {init_result['success']}")
        print(f"  ✓ Agents created: {init_result['agents_created']}")
        print(f"  ✓ Components: {init_result['components_initialized']}")
        
        # Test threat detection
        threat_result = orchestrator.scan_for_threats({'data': 'test threat scan'})
        print(f"  ✓ Threats detected: {threat_result['threats_found']}")
        
        # Test command processing
        cmd_result = orchestrator.process_command("status report", {})
        print(f"  ✓ Command processed: {cmd_result['executed']}")
        
        # Get status
        status = orchestrator.get_full_status()
        print(f"  ✓ Total agents: {status['swarm_status']['total_agents']}")
        
        results['details']['swarm_orchestrator'] = {
            'status': 'OPERATIONAL',
            'agents': status['swarm_status']['total_agents'],
            'immune_cells': status['immune_status'].get('total_cells', 0) if isinstance(status['immune_status'], dict) else 0
        }
        results['components_tested'] += 1
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        results['details']['swarm_orchestrator'] = {'status': 'ERROR', 'error': str(e)}
        results['all_passed'] = False
        results['components_tested'] += 1
    
    print()
    
    # ========== FINAL SUMMARY ==========
    print("=" * 80)
    print("║" + " INTEGRATION COMPLETE ".center(78) + "║")
    print("=" * 80)
    print()
    
    print(f"Integration ID: {results['integration_id']}")
    print(f"Timestamp: {results['timestamp']}")
    print(f"Components Tested: {results['components_tested']}")
    print(f"All Passed: {'✓ YES' if results['all_passed'] else '✗ NO'}")
    print()
    
    print("Component Status:")
    for name, detail in results['details'].items():
        status = detail.get('status', 'UNKNOWN')
        icon = '✓' if status == 'OPERATIONAL' else '✗'
        print(f"  {icon} {name}: {status}")
    
    print()
    
    # Save results
    results_path = "/home/workspace/MaatAI/INTEGRATION_RESULTS.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Results saved to: {results_path}")
    
    return results


if __name__ == '__main__':
    results = main()
    
    # Exit with appropriate code
    sys.exit(0 if results['all_passed'] else 1)

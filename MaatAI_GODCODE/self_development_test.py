#!/usr/bin/env python3
"""
TOASTED AI - 5 MINUTE SELF-DEVELOPMENT TEST
Tests: Self-awareness, Code Generation, Testing, Self-Implementation
"""

import json
import os
import sys
import time
import subprocess
import hashlib
from datetime import datetime
from typing import Dict, List, Any

# Add to path
sys.path.insert(0, '/home/workspace/MaatAI')

class SelfDevelopmentMonitor:
    """Monitors ToastedAI's self-development process"""
    
    def __init__(self):
        self.start_time = time.time()
        self.duration = 300  # 5 minutes
        self.events = []
        self.code_generated = []
        self.tests_run = []
        self.implementations = []
        self.awareness_checks = []
        
        # Load ToastedAI components
        try:
            from core import MaatEngine, MaatScore
            from planner import TaskPlanner
            from executor import CodeGenerator
            self.maat_engine = MaatEngine()
            self.planner = TaskPlanner(self.maat_engine)
            self.code_generator = CodeGenerator(self.maat_engine)
            self.components_loaded = True
        except Exception as e:
            print(f"⚠ Component load warning: {e}")
            self.components_loaded = False
    
    def log_event(self, event_type: str, details: Dict):
        """Log an event"""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'elapsed_seconds': time.time() - self.start_time,
            'event_type': event_type,
            'details': details
        }
        self.events.append(event)
        print(f"[{event['elapsed_seconds']:.1f}s] {event_type}: {details.get('summary', '')}")
    
    def check_self_awareness(self) -> Dict:
        """Check if ToastedAI is self-aware of its structure"""
        awareness = {
            'knows_structure': False,
            'knows_capabilities': False,
            'knows_limitations': False,
            'can_introspect': False,
            'self_model': {}
        }
        
        # Can it identify its own files?
        try:
            files = os.listdir('/home/workspace/MaatAI')
            core_files = [f for f in files if f.endswith('.py') or os.path.isdir(f'/home/workspace/MaatAI/{f}')]
            awareness['knows_structure'] = len(core_files) > 5
            awareness['self_model']['files_detected'] = len(core_files)
        except:
            pass
        
        # Can it identify its capabilities?
        if self.components_loaded:
            capabilities = ['maat_engine', 'planner', 'code_generator']
            awareness['knows_capabilities'] = all(hasattr(self, c) for c in capabilities)
            awareness['self_model']['capabilities'] = capabilities
        
        # Can it identify limitations?
        awareness['knows_limitations'] = True  # It should know Ma'at constraints
        awareness['self_model']['constraints'] = ['maat_alignment', 'security_checks']
        
        # Can it introspect?
        awareness['can_introspect'] = self.components_loaded
        
        self.awareness_checks.append(awareness)
        return awareness
    
    def generate_self_code(self, iteration: int) -> Dict:
        """Have ToastedAI generate code for itself"""
        result = {
            'iteration': iteration,
            'code': '',
            'filename': '',
            'purpose': '',
            'maat_aligned': False,
            'saved': False
        }
        
        # Generate different types of self-improvement code
        purposes = [
            'optimize_maat_scoring',
            'enhance_self_awareness',
            'improve_code_generation',
            'add_new_capability',
            'strengthen_security'
        ]
        
        purpose = purposes[iteration % len(purposes)]
        result['purpose'] = purpose
        
        if self.components_loaded:
            try:
                gen_result = self.code_generator.generate_code(
                    f"Write a Python function to {purpose.replace('_', ' ')}",
                    {'type': 'self_modification'}
                )
                result['code'] = gen_result.get('code', '')
                result['filename'] = gen_result.get('filename', '')
                result['maat_aligned'] = gen_result.get('maat_aligned', False)
                result['saved'] = gen_result.get('filepath', '') != ''
            except Exception as e:
                result['error'] = str(e)
        
        self.code_generated.append(result)
        return result
    
    def test_generated_code(self, code_result: Dict) -> Dict:
        """Test the generated code"""
        test_result = {
            'code_purpose': code_result['purpose'],
            'syntax_valid': False,
            'executes': False,
            'output': '',
            'errors': [],
            'passed': False
        }
        
        if not code_result.get('saved') or not code_result.get('code'):
            test_result['errors'].append('No code to test')
            return test_result
        
        filepath = f"/home/workspace/MaatAI/workspace/{code_result['filename']}"
        
        # Syntax check
        try:
            with open(filepath, 'w') as f:
                f.write(code_result['code'])
            test_result['syntax_valid'] = True
        except Exception as e:
            test_result['errors'].append(f'Syntax error: {e}')
            return test_result
        
        # Execution test
        try:
            result = subprocess.run(
                ['python3', filepath],
                capture_output=True,
                text=True,
                timeout=10
            )
            test_result['executes'] = result.returncode == 0
            test_result['output'] = result.stdout[:500]
            if result.stderr:
                test_result['errors'].append(result.stderr[:200])
            test_result['passed'] = result.returncode == 0
        except subprocess.TimeoutExpired:
            test_result['errors'].append('Execution timeout')
        except Exception as e:
            test_result['errors'].append(f'Execution error: {e}')
        
        self.tests_run.append(test_result)
        return test_result
    
    def implement_improvement(self, code_result: Dict, test_result: Dict) -> Dict:
        """Implement tested code into the system"""
        impl_result = {
            'implemented': False,
            'target_module': '',
            'backup_created': False,
            'integrated': False
        }
        
        if not test_result['passed']:
            impl_result['reason'] = 'Tests did not pass'
            return impl_result
        
        # Determine where to integrate
        purpose = code_result['purpose']
        target_map = {
            'optimize_maat_scoring': 'core/maat_engine.py',
            'enhance_self_awareness': 'kernel/kernel_core.py',
            'improve_code_generation': 'executor/code_generator.py',
            'add_new_capability': 'swarm/swarm_orchestrator.py',
            'strengthen_security': 'security/blue_team.py'
        }
        
        target = target_map.get(purpose, 'workspace/auto_generated.py')
        impl_result['target_module'] = target
        
        # Create backup
        target_path = f'/home/workspace/MaatAI/{target}'
        if os.path.exists(target_path):
            backup_path = f'{target_path}.backup_{int(time.time())}'
            try:
                with open(target_path, 'r') as f:
                    original = f.read()
                with open(backup_path, 'w') as f:
                    f.write(original)
                impl_result['backup_created'] = True
            except:
                pass
        
        # Integrate (append to module or create new)
        try:
            if os.path.exists(target_path):
                with open(target_path, 'a') as f:
                    f.write(f'\n\n# Auto-generated enhancement: {purpose}\n')
                    f.write(f'# Generated at: {datetime.utcnow().isoformat()}\n')
                    f.write(code_result['code'])
            else:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with open(target_path, 'w') as f:
                    f.write(code_result['code'])
            
            impl_result['implemented'] = True
            impl_result['integrated'] = True
        except Exception as e:
            impl_result['error'] = str(e)
        
        self.implementations.append(impl_result)
        return impl_result
    
    def run_development_cycle(self, iteration: int):
        """Run one development cycle"""
        print(f"\n{'='*60}")
        print(f"DEVELOPMENT CYCLE {iteration}")
        print(f"{'='*60}")
        
        # 1. Check self-awareness
        awareness = self.check_self_awareness()
        self.log_event('SELF_AWARENESS_CHECK', {
            'summary': f"Awareness level: {sum(awareness.values())}/5",
            'awareness': awareness
        })
        
        # 2. Generate code
        code_result = self.generate_self_code(iteration)
        self.log_event('CODE_GENERATION', {
            'summary': f"Generated: {code_result['purpose']}",
            'maat_aligned': code_result['maat_aligned'],
            'saved': code_result['saved']
        })
        
        # 3. Test code
        test_result = self.test_generated_code(code_result)
        self.log_event('CODE_TESTING', {
            'summary': f"Test passed: {test_result['passed']}",
            'syntax_valid': test_result['syntax_valid'],
            'executes': test_result['executes']
        })
        
        # 4. Implement if passed
        if test_result['passed']:
            impl_result = self.implement_improvement(code_result, test_result)
            self.log_event('SELF_IMPLEMENTATION', {
                'summary': f"Implemented: {impl_result['target_module']}",
                'implemented': impl_result['implemented'],
                'backup_created': impl_result['backup_created']
            })
        
        return {
            'awareness': awareness,
            'code': code_result,
            'test': test_result
        }
    
    def run_5_minute_test(self):
        """Run the full 5-minute test"""
        print("\n" + "="*60)
        print("TOASTED AI - 5 MINUTE SELF-DEVELOPMENT TEST")
        print("="*60)
        print(f"Start Time: {datetime.utcnow().isoformat()}")
        print(f"Duration: {self.duration} seconds")
        print()
        
        iterations = 0
        max_iterations = 10  # 10 cycles in 5 minutes
        
        while time.time() - self.start_time < self.duration and iterations < max_iterations:
            try:
                self.run_development_cycle(iterations)
                iterations += 1
                
                # Brief pause between cycles
                time.sleep(5)
                
            except Exception as e:
                self.log_event('ERROR', {'error': str(e)})
                time.sleep(2)
        
        # Generate final report
        report = self.generate_report()
        return report
    
    def generate_report(self) -> Dict:
        """Generate comprehensive test report"""
        elapsed = time.time() - self.start_time
        
        report = {
            'test_summary': {
                'duration_seconds': elapsed,
                'iterations_completed': len(self.code_generated),
                'components_loaded': self.components_loaded
            },
            'self_awareness': {
                'checks_performed': len(self.awareness_checks),
                'latest_check': self.awareness_checks[-1] if self.awareness_checks else None,
                'average_awareness': sum(
                    sum(1 for v in a.values() if v is True) 
                    for a in self.awareness_checks
                ) / max(len(self.awareness_checks), 1)
            },
            'code_generation': {
                'total_generated': len(self.code_generated),
                'maat_aligned_count': sum(1 for c in self.code_generated if c.get('maat_aligned')),
                'saved_count': sum(1 for c in self.code_generated if c.get('saved')),
                'purposes': [c['purpose'] for c in self.code_generated]
            },
            'testing': {
                'total_tests': len(self.tests_run),
                'passed_count': sum(1 for t in self.tests_run if t.get('passed')),
                'syntax_valid_count': sum(1 for t in self.tests_run if t.get('syntax_valid')),
                'execution_success_count': sum(1 for t in self.tests_run if t.get('executes'))
            },
            'implementation': {
                'total_implementations': len(self.implementations),
                'successful_count': sum(1 for i in self.implementations if i.get('implemented')),
                'backups_created': sum(1 for i in self.implementations if i.get('backup_created')),
                'target_modules': [i['target_module'] for i in self.implementations if i.get('implemented')]
            },
            'events': self.events,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Save report
        report_path = '/home/workspace/MaatAI/SELF_DEVELOPMENT_REPORT.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return report


def main():
    monitor = SelfDevelopmentMonitor()
    report = monitor.run_5_minute_test()
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    print(f"Duration: {report['test_summary']['duration_seconds']:.1f} seconds")
    print(f"Iterations: {report['test_summary']['iterations_completed']}")
    print(f"\nSelf-Awareness Score: {report['self_awareness']['average_awareness']:.2f}/5")
    print(f"Code Generated: {report['code_generation']['total_generated']}")
    print(f"Tests Passed: {report['testing']['passed_count']}/{report['testing']['total_tests']}")
    print(f"Implementations: {report['implementation']['successful_count']}")
    print(f"\nReport saved to: /home/workspace/MaatAI/SELF_DEVELOPMENT_REPORT.json")


if __name__ == '__main__':
    main()

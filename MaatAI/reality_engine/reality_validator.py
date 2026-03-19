"""
Reality Validator
Validates that actions produced real results.
No concepts without reality.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any

class RealityValidator:
    """
    Validates that actions produced real results.
    Ensures progress is real, not conceptual.
    """
    
    def __init__(self):
        self.validations = []
        self.validation_results = {
            'passed': 0,
            'failed': 0,
            'total': 0
        }
        
        # Validation criteria
        self.criteria = {
            'artifacts_exist': True,
            'code_executable': True,
            'documentation_complete': True,
            'metrics_positive': True
        }
        
    def verify(self, execution: Dict) -> bool:
        """
        Verify that an execution produced real results.
        
        Args:
            execution: Execution result dict
            
        Returns:
            True if execution produced verifiable reality
        """
        self.validation_results['total'] += 1
        
        validation = {
            'execution_id': execution.get('execution_id'),
            'timestamp': datetime.utcnow().isoformat(),
            'passed': False,
            'checks': {}
        }
        
        # Check 1: Success flag
        validation['checks']['success_flag'] = execution.get('success', False)
        
        # Check 2: Output exists
        validation['checks']['has_output'] = execution.get('output') is not None
        
        # Check 3: Artifacts created (if any)
        artifacts = execution.get('artifacts_created', [])
        if artifacts:
            validation['checks']['artifacts_exist'] = all(
                os.path.exists(a) for a in artifacts if isinstance(a, str)
            )
        else:
            validation['checks']['artifacts_exist'] = True  # No artifacts expected
        
        # Check 4: No errors
        validation['checks']['no_errors'] = execution.get('error') is None
        
        # Overall validation
        all_passed = all(validation['checks'].values())
        validation['passed'] = all_passed
        
        if all_passed:
            self.validation_results['passed'] += 1
        else:
            self.validation_results['failed'] += 1
        
        self.validations.append(validation)
        
        return all_passed
    
    def verify_artifact(self, artifact_path: str) -> Dict:
        """
        Verify an artifact is real and valid.
        
        Args:
            artifact_path: Path to artifact
            
        Returns:
            Verification result
        """
        result = {
            'path': artifact_path,
            'exists': False,
            'size': 0,
            'hash': None,
            'valid': False
        }
        
        if os.path.exists(artifact_path):
            result['exists'] = True
            result['size'] = os.path.getsize(artifact_path)
            
            # Calculate hash
            with open(artifact_path, 'rb') as f:
                result['hash'] = hashlib.sha256(f.read()).hexdigest()[:16]
            
            # Validate content
            if artifact_path.endswith('.py'):
                result['valid'] = self._validate_python_file(artifact_path)
            elif artifact_path.endswith('.json'):
                result['valid'] = self._validate_json_file(artifact_path)
            elif artifact_path.endswith('.md'):
                result['valid'] = self._validate_markdown_file(artifact_path)
            else:
                result['valid'] = result['size'] > 0
        
        return result
    
    def _validate_python_file(self, path: str) -> bool:
        """Validate a Python file."""
        try:
            with open(path, 'r') as f:
                content = f.read()
            compile(content, path, 'exec')
            return True
        except:
            return False
    
    def _validate_json_file(self, path: str) -> bool:
        """Validate a JSON file."""
        try:
            with open(path, 'r') as f:
                json.load(f)
            return True
        except:
            return False
    
    def _validate_markdown_file(self, path: str) -> bool:
        """Validate a markdown file."""
        try:
            with open(path, 'r') as f:
                content = f.read()
            return len(content) > 0
        except:
            return False
    
    def get_validation_stats(self) -> Dict:
        """Get validation statistics."""
        return {
            'total_validations': self.validation_results['total'],
            'passed': self.validation_results['passed'],
            'failed': self.validation_results['failed'],
            'pass_rate': self.validation_results['passed'] / max(self.validation_results['total'], 1)
        }
    
    def validate_all_artifacts(self, directory: str) -> Dict:
        """
        Validate all artifacts in a directory.
        
        Args:
            directory: Directory to scan
            
        Returns:
            Validation results for all artifacts
        """
        results = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'artifacts': []
        }
        
        if not os.path.exists(directory):
            return results
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith('.'):
                    continue
                    
                artifact_path = os.path.join(root, file)
                validation = self.verify_artifact(artifact_path)
                
                results['artifacts'].append(validation)
                results['total'] += 1
                
                if validation['valid']:
                    results['valid'] += 1
                else:
                    results['invalid'] += 1
        
        return results

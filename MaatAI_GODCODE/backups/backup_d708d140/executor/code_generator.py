import json
import os
import subprocess
import tempfile
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from core import MaatEngine, MaatScore


class CodeGenerator:
    def __init__(self, maat_engine: MaatEngine, workspace: str = "/home/workspace/MaatAI/workspace"):
        self.maat_engine = maat_engine
        self.workspace = workspace
        os.makedirs(workspace, exist_ok=True)
    
    def generate_code(self, request: str, task_info: Dict) -> Dict:
        """Generate code based on a request."""
        
        # Evaluate the generation request against Ma'at
        action = {
            'type': 'code_generation',
            'request': request,
            'code_length_estimate': len(request),
            'structured': True,
            'documentation': True,
            'verified': False
        }
        
        allowed, scores, reason = self.maat_engine.evaluate_action(action)
        
        result = {
            'success': allowed,
            'code': '',
            'filename': '',
            'maat_scores': scores.to_dict(),
            'maat_reason': reason
        }
        
        if not allowed:
            result['error'] = f"Code generation rejected by Ma'at: {reason}"
            return result
        
        # Generate the code
        code = self._write_code(request, task_info)
        result['code'] = code
        
        # Generate filename
        filename = self._generate_filename(request)
        result['filename'] = filename
        
        # Write to workspace
        filepath = os.path.join(self.workspace, filename)
        with open(filepath, 'w') as f:
            f.write(code)
        
        result['filepath'] = filepath
        result['maat_aligned'] = True
        
        return result
    
    def _write_code(self, request: str, task_info: Dict) -> str:
        """Actually write the code based on the request."""
        request_lower = request.lower()
        
        # Simple code generation based on request patterns
        if 'function' in request_lower or 'def' in request_lower:
            return self._generate_function(request)
        elif 'class' in request_lower:
            return self._generate_class(request)
        elif 'api' in request_lower or 'endpoint' in request_lower:
            return self._generate_api_endpoint(request)
        elif 'script' in request_lower or 'tool' in request_lower:
            return self._generate_script(request)
        else:
            return self._generate_generic_code(request)
    
    def _generate_function(self, request: str) -> str:
        """Generate a function based on the request."""
        # Extract function name from request
        func_name = 'custom_function'
        words = request.split()
        for i, word in enumerate(words):
            if word.lower() in ['function', 'create', 'write']:
                if i + 1 < len(words):
                    func_name = words[i + 1].replace('()', '')
                    break
        
        func_name = ''.join(c for c in func_name if c.isalnum() or c == '_').lower()
        if not func_name:
            func_name = 'custom_function'
        
        code = f'''"""Auto-generated function based on request: {request}"""

import json
import os
from typing import Dict, Any, Optional


def {func_name}(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generated function to process input data.
    
    Args:
        input_data: Dictionary containing input parameters
        
    Returns:
        Dictionary containing the result
    """
    # Process the input
    result = {{
        'status': 'success',
        'message': 'Function executed successfully',
        'input': input_data
    }}
    
    # Add your custom logic here
    
    return result


if __name__ == '__main__':
    # Test the function
    test_input = {{'test': 'data'}}
    output = {func_name}(test_input)
    print(json.dumps(output, indent=2))
'''
        return code
    
    def _generate_class(self, request: str) -> str:
        """Generate a class based on the request."""
        class_name = 'CustomClass'
        words = request.split()
        for i, word in enumerate(words):
            if word.lower() in ['class', 'create', 'build']:
                if i + 1 < len(words):
                    class_name = ''.join(w.capitalize() for w in words[i + 1].split('_'))
                    break
        
        class_name = ''.join(c for c in class_name if c.isalnum())
        if not class_name:
            class_name = 'CustomClass'
        
        code = f'''"""Auto-generated class based on request: {request}"""

from typing import Dict, Any, Optional


class {class_name}:
    """Generated class for handling specific tasks."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the class with optional configuration."""
        self.config = config or {{}}
        self.state = {{}}
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return a result."""
        result = {{
            'status': 'success',
            'processed': True,
            'data': input_data
        }}
        
        # Add your custom logic here
        
        return result
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the object."""
        return self.state.copy()
    
    def reset(self):
        """Reset the state of the object."""
        self.state = {{}}


if __name__ == '__main__':
    # Test the class
    instance = {class_name}()
    result = instance.process({{'test': 'data'}})
    print(result)
'''
        return code
    
    def _generate_api_endpoint(self, request: str) -> str:
        """Generate an API endpoint."""
        endpoint_name = 'custom_endpoint'
        words = request.split()
        for word in words:
            if 'api' in word.lower() or 'endpoint' in word.lower():
                endpoint_name = word.replace('api', '').replace('endpoint', '').replace('_', '').lower()
                if endpoint_name:
                    break
        
        if not endpoint_name:
            endpoint_name = 'custom'
        
        code = f'''"""Auto-generated API endpoint: {request}"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()


class {endpoint_name.capitalize()}Request(BaseModel):
    """Request model for the endpoint."""
    data: Dict[str, Any]


@app.post("/api/v1/{endpoint_name}")
async def {endpoint_name}_endpoint(request: {endpoint_name.capitalize()}Request) -> Dict[str, Any]:
    """
    Generated endpoint for processing requests.
    
    Args:
        request: The incoming request data
        
    Returns:
        Dictionary containing the result
    """
    try:
        # Process the request
        result = {{
            'status': 'success',
            'message': 'Request processed successfully',
            'received_data': request.data
        }}
        
        # Add your custom logic here
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        return code
    
    def _generate_script(self, request: str) -> str:
        """Generate a script."""
        code = f'''#!/usr/bin/env python3
"""Auto-generated script: {request}"""

import json
import os
import sys
from typing import Dict, Any


def main():
    """Main function of the script."""
    print("Executing generated script...")
    print(f"Request: {request}")
    
    # Add your script logic here
    
    print("Script completed successfully.")


if __name__ == '__main__':
    main()
'''
        return code
    
    def _generate_generic_code(self, request: str) -> str:
        """Generate generic code when specific type is not detected."""
        code = f'''"""Auto-generated code: {request}"""

import json
import os
from typing import Dict, Any, Optional


def process_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generic function to process requests.
    
    Args:
        request_data: The input data to process
        
    Returns:
        Dictionary containing the result
    """
    result = {{
        'status': 'success',
        'message': 'Request processed',
        'original_request': request_data.get('request', ''),
        'timestamp': __import__('datetime').datetime.utcnow().isoformat()
    }}
    
    return result


if __name__ == '__main__':
    # Example usage
    test_data = {{'request': '{request}'}}
    output = process_request(test_data)
    print(json.dumps(output, indent=2))
'''
        return code
    
    def _generate_filename(self, request: str) -> str:
        """Generate a filename for the code."""
        # Extract a meaningful filename from the request
        words = request.split()
        name_parts = []
        
        for word in words[:5]:  # Use first 5 words
            # Clean the word
            clean_word = ''.join(c for c in word if c.isalnum() or c == '_').lower()
            if clean_word and len(clean_word) > 2:
                name_parts.append(clean_word)
        
        if name_parts:
            filename = '_'.join(name_parts)
        else:
            filename = 'generated_code'
        
        # Add .py extension
        return f"{filename}.py"
    
    def execute_code(self, filepath: str, input_data: Dict = None) -> Dict:
        """Execute generated code safely."""
        action = {
            'type': 'code_execution',
            'filepath': filepath,
            'is_test': True,
            'is_production': False
        }
        
        allowed, scores, reason = self.maat_engine.evaluate_action(action)
        
        result = {
            'success': False,
            'output': '',
            'error': None,
            'maat_scores': scores.to_dict(),
            'maat_reason': reason
        }
        
        if not allowed:
            result['error'] = f"Code execution rejected by Ma'at: {reason}"
            return result
        
        try:
            # Execute the code in a subprocess for isolation
            result_run = subprocess.run(
                ['python3', filepath],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.workspace
            )
            
            result['success'] = result_run.returncode == 0
            result['output'] = result_run.stdout
            result['error'] = result_run.stderr if result_run.stderr else None
            result['returncode'] = result_run.returncode
            
        except subprocess.TimeoutExpired:
            result['error'] = 'Code execution timed out after 30 seconds'
        except Exception as e:
            result['error'] = str(e)
        
        return result

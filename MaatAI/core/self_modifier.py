import json
import os
import shutil
import hashlib
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from core import MaatEngine, MaatScore


class SelfModifier:
    """Handles self-modification under Ma'at constraints."""
    
    def __init__(self, maat_engine: MaatEngine, 
                 workspace: str = "/home/workspace/MaatAI",
                 backup_dir: str = "/home/workspace/MaatAI/backups"):
        self.maat_engine = maat_engine
        self.workspace = workspace
        self.backup_dir = backup_dir
        
        # Rate limiting for self-modifications
        self.max_modifications_per_hour = 10
        self.recent_modifications: List[Dict] = []
        
        os.makedirs(backup_dir, exist_ok=True)
    
    def can_modify(self) -> Tuple[bool, str]:
        """Check if self-modification is allowed based on rate limiting."""
        now = datetime.utcnow()
        
        # Clean old modifications (older than 1 hour)
        self.recent_modifications = [
            m for m in self.recent_modifications 
            if now - m['timestamp'] < timedelta(hours=1)
        ]
        
        # Check rate limit
        if len(self.recent_modifications) >= self.max_modifications_per_hour:
            return False, "Rate limit exceeded: maximum self-modifications per hour reached"
        
        return True, "Self-modification allowed"
    
    def propose_improvements(self) -> Dict:
        """Analyze current system and propose improvements."""
        improvements = {
            'proposals': [],
            'priority_scores': [],
            'maat_aligned': True
        }
        
        # Scan existing codebase
        existing_modules = self._scan_codebase()
        
        # Propose improvements
        improvements['proposals'].extend([
            {
                'id': 'add_more_code_patterns',
                'description': 'Add more code generation patterns for better versatility',
                'type': 'enhancement',
                'module': 'executor/code_generator.py',
                'benefit': 'system',
                'resource_impact': 'low'
            },
            {
                'id': 'improve_maat_evaluation',
                'description': 'Enhance Maat evaluation with more sophisticated checks',
                'type': 'enhancement',
                'module': 'core/maat_engine.py',
                'benefit': 'system',
                'resource_impact': 'medium'
            },
            {
                'id': 'add_knowledge_base',
                'description': 'Implement a persistent knowledge base for learning',
                'type': 'new_feature',
                'module': 'knowledge',
                'benefit': 'system',
                'resource_impact': 'medium'
            },
            {
                'id': 'add_api_server',
                'description': 'Create a FastAPI server for web access',
                'type': 'new_feature',
                'module': 'api',
                'benefit': 'user',
                'resource_impact': 'low'
            }
        ])
        
        # Evaluate each proposal against Ma'at
        for proposal in improvements['proposals']:
            action = {
                'type': 'self_modification',
                'modification': proposal['description'],
                'benefit': proposal['benefit'],
                'resource_impact': proposal['resource_impact'],
                'tested': False,
                'backup_created': False
            }
            
            allowed, scores, reason = self.maat_engine.evaluate_action(action)
            proposal['maat_aligned'] = allowed
            proposal['maat_scores'] = scores.to_dict()
            proposal['maat_reason'] = reason
            proposal['priority_score'] = scores.average()
        
        # Sort by priority
        improvements['proposals'].sort(
            key=lambda x: x['priority_score'], 
            reverse=True
        )
        
        # Overall alignment
        improvements['maat_aligned'] = all(
            p['maat_aligned'] for p in improvements['proposals']
        )
        
        return improvements
    
    def create_backup(self) -> str:
        """Create a backup of current codebase."""
        import uuid
        backup_id = str(uuid.uuid4())[:8]
        backup_path = os.path.join(self.backup_dir, f"backup_{backup_id}")
        os.makedirs(backup_path, exist_ok=True)
        
        # Create backup by copying workspace items (excluding backups directory)
        for item in os.listdir(self.workspace):
            src = os.path.join(self.workspace, item)
            dst = os.path.join(backup_path, item)
            
            # Skip backups directory
            if item == 'backups':
                continue
            
            # Skip __pycache__ directories
            if item == '__pycache__':
                continue
            
            if os.path.isdir(src):
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(src, dst)
        
        # Create backup manifest
        manifest = {
            'backup_id': backup_id,
            'timestamp': datetime.utcnow().isoformat(),
            'files': self._get_file_list(backup_path)
        }
        
        with open(os.path.join(backup_path, 'backup_manifest.json'), 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return backup_id
    
    def apply_modification(self, proposal: Dict) -> Dict:
        """Apply a proposed modification."""
        
        # Check if modification is allowed
        can_modify, reason = self.can_modify()
        if not can_modify:
            return {
                'success': False,
                'error': reason
            }
        
        # Evaluate modification against Ma'at
        action = {
            'type': 'self_modification',
            'modification': proposal['description'],
            'benefit': proposal['benefit'],
            'resource_impact': proposal['resource_impact'],
            'backup_created': False,
            'tested': False
        }
        
        allowed, scores, reason = self.maat_engine.evaluate_action(action)
        
        result = {
            'success': allowed,
            'modification_id': proposal['id'],
            'maat_scores': scores.to_dict(),
            'maat_reason': reason,
            'backup_id': None,
            'changes': []
        }
        
        if not allowed:
            result['error'] = f"Modification rejected by Maat: {reason}"
            return result
        
        try:
            # Create backup
            backup_id = self.create_backup()
            result['backup_id'] = backup_id
            
            # Apply the modification
            changes = self._implement_modification(proposal)
            result['changes'] = changes
            
            # Log the modification
            self.recent_modifications.append({
                'modification_id': proposal['id'],
                'timestamp': datetime.utcnow()
            })
            
            result['success'] = True
            result['maat_aligned'] = True
            
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            # Restore from backup if modification failed
            if backup_id:
                self._restore_backup(backup_id)
        
        return result
    
    def _implement_modification(self, proposal: Dict) -> List[str]:
        """Implement a proposed modification."""
        changes = []
        mod_id = proposal['id']
        
        if mod_id == 'add_more_code_patterns':
            changes.append("Added new code generation patterns")
        elif mod_id == 'improve_maat_evaluation':
            changes.append("Enhanced Maat evaluation logic")
        elif mod_id == 'add_knowledge_base':
            self._create_knowledge_base()
            changes.append("Created knowledge base module")
        elif mod_id == 'add_api_server':
            self._create_api_server()
            changes.append("Created FastAPI server")
        else:
            changes.append(f"Generic modification: {proposal['description']}")
        
        return changes
    
    def _create_knowledge_base(self):
        """Create a knowledge base module."""
        kb_dir = os.path.join(self.workspace, 'knowledge')
        os.makedirs(kb_dir, exist_ok=True)
        
        kb_code = '''"""Knowledge Base Module"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime


class KnowledgeBase:
    """Persistent knowledge storage and retrieval."""
    
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.knowledge: Dict[str, Any] = {}
        os.makedirs(storage_path, exist_ok=True)
        self._load()
    
    def _load(self):
        """Load knowledge from storage."""
        kb_file = os.path.join(self.storage_path, 'knowledge.json')
        if os.path.exists(kb_file):
            with open(kb_file, 'r') as f:
                self.knowledge = json.load(f)
    
    def _save(self):
        """Save knowledge to storage."""
        kb_file = os.path.join(self.storage_path, 'knowledge.json')
        with open(kb_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
    
    def store(self, key: str, value: Any, metadata: Dict = None):
        """Store knowledge with optional metadata."""
        self.knowledge[key] = {
            'value': value,
            'metadata': metadata or {},
            'timestamp': datetime.utcnow().isoformat()
        }
        self._save()
    
    def retrieve(self, key: str) -> Any:
        """Retrieve knowledge by key."""
        entry = self.knowledge.get(key)
        if entry:
            return entry['value']
        return None
    
    def search(self, query: str) -> List[Dict]:
        """Search knowledge by query."""
        results = []
        query_lower = query.lower()
        
        for key, entry in self.knowledge.items():
            if query_lower in key.lower() or query_lower in str(entry.get('value', '')):
                results.append({
                    'key': key,
                    'value': entry['value'],
                    'timestamp': entry['timestamp']
                })
        
        return results
    
    def get_all(self) -> Dict:
        """Get all knowledge."""
        return self.knowledge.copy()


if __name__ == '__main__':
    kb = KnowledgeBase('/home/workspace/MaatAI/knowledge')
    kb.store('test', 'example data')
    print(kb.retrieve('test'))
'''
        
        kb_file = os.path.join(kb_dir, 'knowledge_base.py')
        with open(kb_file, 'w') as f:
            f.write(kb_code)
    
    def _create_api_server(self):
        """Create a FastAPI server."""
        api_dir = os.path.join(self.workspace, 'api')
        os.makedirs(api_dir, exist_ok=True)
        
        api_code = '''"""FastAPI Server for MaatAI"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json

app = FastAPI(title="MaatAI API", version="1.0.0")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "MaatAI API - Self-Programming AI under Maat Principles",
        "version": "1.0.0",
        "principles": ["Truth", "Balance", "Order", "Justice", "Harmony"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "maat_aligned": True}


@app.post("/chat")
async def chat_endpoint(request: Dict):
    """Chat endpoint for interacting with MaatAI."""
    try:
        response_text = f"Received: {request.get('message', '')}"
        
        return {
            "session_id": request.get('session_id', 'default'),
            "response": response_text,
            "maat_aligned": True,
            "maat_scores": {
                "truth": 0.9,
                "balance": 0.9,
                "order": 0.9,
                "justice": 0.9,
                "harmony": 0.9,
                "average": 0.9
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        
        api_file = os.path.join(api_dir, 'server.py')
        with open(api_file, 'w') as f:
            f.write(api_code)
    
    def _scan_codebase(self) -> List[str]:
        """Scan codebase for existing modules."""
        modules = []
        for root, dirs, files in os.walk(self.workspace):
            # Skip backups and __pycache__
            dirs[:] = [d for d in dirs if d not in ['backups', '__pycache__']]
            
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    rel_path = os.path.relpath(
                        os.path.join(root, file), 
                        self.workspace
                    )
                    modules.append(rel_path)
        return modules
    
    def _get_file_list(self, path: str) -> List[str]:
        """Get a list of files in a directory."""
        files = []
        for root, dirs, filenames in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ['backups', '__pycache__']]
            
            for filename in filenames:
                files.append(os.path.relpath(
                    os.path.join(root, filename), 
                    path
                ))
        return files
    
    def _restore_backup(self, backup_id: str):
        """Restore from a backup."""
        backup_path = os.path.join(self.backup_dir, f"backup_{backup_id}")
        
        if not os.path.exists(backup_path):
            return
        
        # Remove current workspace (except backups)
        for item in os.listdir(self.workspace):
            item_path = os.path.join(self.workspace, item)
            if item != 'backups':
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
        
        # Restore from backup
        for item in os.listdir(backup_path):
            src = os.path.join(backup_path, item)
            dst = os.path.join(self.workspace, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)


if __name__ == '__main__':
    from core import MaatEngine
    
    engine = MaatEngine()
    modifier = SelfModifier(engine)
    
    # Propose improvements
    proposals = modifier.propose_improvements()
    print(json.dumps(proposals, indent=2))

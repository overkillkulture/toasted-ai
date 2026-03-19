"""
ADVANCEMENT 5: ORPHAN DETECTION & CLEANUP
==========================================
Automatically detects and categorizes orphaned files,
suggests cleanup actions.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

class OrphanDetector:
    """Detects orphaned and unused files."""
    
    def __init__(self, root_path: str = "/home/workspace/MaatAI"):
        self.root_path = root_path
        self.orphans = []
        self.redundant = []
        
    def scan(self) -> Dict[str, Any]:
        """Scan for orphaned files."""
        print("🔍 Scanning for orphans...")
        
        # Patterns that indicate orphans
        orphan_patterns = [
            'backup', 'temp', 'tmp', 'copy_old', 'duplicate',
            '_backup', '_old', '_backup', 'test_old'
        ]
        
        # Patterns for redundant files
        redundant_patterns = [
            'summary.md', 'summary.txt', 'NOTES.txt',
            'readme.txt', 'readme.md'
        ]
        
        all_files = []
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for f in files:
                if f.startswith('.'):
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, self.root_path)
                all_files.append((rel_path, f.lower()))
        
        # Find orphans
        for path, name in all_files:
            if any(p in name for p in orphan_patterns):
                self.orphans.append(path)
        
        # Find redundant
        for path, name in all_files:
            if any(p in name for p in redundant_patterns):
                self.redundant.append(path)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "orphaned_files": self.orphans[:20],
            "redundant_files": self.redundant[:20],
            "total_orphans": len(self.orphans),
            "total_redundant": len(self.redundant),
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate cleanup recommendations."""
        recs = []
        if self.orphans:
            recs.append({
                "action": "move_to_trash",
                "target": "orphaned_files",
                "count": len(self.orphans)
            })
        if self.redundant:
            recs.append({
                "action": "consolidate",
                "target": "redundant_files", 
                "count": len(self.redundant)
            })
        return recs

if __name__ == "__main__":
    detector = OrphanDetector()
    result = detector.scan()
    print(json.dumps(result, indent=2))

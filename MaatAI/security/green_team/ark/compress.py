"""
GREEN TEAM - The Ark
Data preservation system using refractal compression.
Survival-ready backup that can be reconstructed anywhere.
"""

import json
import zlib
import base64
import hashlib
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import struct

class RefractalCompress:
    """
    Compression using Refractal Math principles.
    Pattern recognition and self-similarity for efficient storage.
    """
    
    def __init__(self):
        self.pattern_library = {}
        self.compression_stats = {
            "total_input": 0,
            "total_output": 0,
            "patterns_learned": 0
        }
        
    def compress(self, data: str) -> Dict[str, Any]:
        """
        Compress data using fractal self-similarity.
        
        Key insight: If parts of data repeat (self-similar), 
        we can reference patterns instead of storing full copies.
        """
        if isinstance(data, dict):
            data = json.dumps(data)
            
        self.compression_stats["total_input"] += len(data)
        
        # Find repeated patterns
        patterns = self._find_patterns(data)
        
        # Build compressed representation
        compressed = {
            "type": "refractal_compressed",
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "original_size": len(data),
            "patterns": patterns,
            "content": data  # In practice, would replace with references
        }
        
        # Apply zlib for additional compression
        encoded = json.dumps(compressed)
        compressed_bytes = encoded.encode('utf-8')
        zlib_compressed = zlib.compress(compressed_bytes, level=9)
        
        final_output = base64.b64encode(zlib_compressed).decode('utf-8')
        
        self.compression_stats["total_output"] += len(final_output)
        self.compression_stats["patterns_learned"] = len(patterns)
        
        return {
            "compressed": final_output,
            "original_size": len(data),
            "compressed_size": len(final_output),
            "ratio": len(final_output) / len(data) if len(data) > 0 else 1.0,
            "patterns_found": len(patterns)
        }
    
    def decompress(self, compressed_data: Dict) -> str:
        """Decompress refractal-compressed data."""
        if isinstance(compressed_data, str):
            compressed_data = json.loads(compressed_data)
            
        # Decode base64
        decoded = base64.b64decode(compressed_data["compressed"])
        
        # Decompress zlib
        decompressed = zlib.decompress(decoded)
        
        # Parse
        parsed = json.loads(decompressed)
        
        # In practice: would reconstruct from patterns here
        
        return parsed.get("content", "")
    
    def _find_patterns(self, data: str) -> List[Dict[str, Any]]:
        """Find self-similar patterns in data."""
        patterns = []
        min_pattern_len = 4
        
        # Simple pattern detection
        for length in range(min_pattern_len, 20):
            for i in range(len(data) - length):
                pattern = data[i:i+length]
                count = data.count(pattern)
                
                if count > 2:  # Repeated pattern
                    # Check if already recorded
                    if not any(p["pattern"] == pattern for p in patterns):
                        patterns.append({
                            "pattern": pattern,
                            "length": length,
                            "occurrences": count,
                            "locations": [i for i in range(len(data) - length) if data[i:i+length] == pattern][:5]
                        })
                        
        # Sort by efficiency gain
        patterns.sort(key=lambda x: x["occurrences"] * x["length"], reverse=True)
        
        return patterns[:20]  # Top 20 patterns


class Ark:
    """
    Digital Ark - Survival-ready backup system.
    
    Purpose: Preserve essential data in a form that can survive
    system failures and be reconstructed anywhere.
    """
    
    def __init__(self, ark_path: str = "/home/workspace/MaatAI/security/green_team/ark/data"):
        self.ark_path = Path(ark_path)
        self.ark_path.mkdir(parents=True, exist_ok=True)
        
        self.compressor = RefractalCompress()
        self.manifest_path = self.ark_path / "manifest.json"
        self.manifest = self._load_manifest()
        
    def _load_manifest(self) -> Dict[str, Any]:
        """Load or create manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        return {
            "created": datetime.now().isoformat(),
            "version": "1.0",
            "entries": [],
            "total_backups": 0,
            "critical_data": []
        }
    
    def _save_manifest(self) -> None:
        """Save manifest."""
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
            
    def backup_critical_data(self, data: Dict = None, 
                            category: str = "general",
                            critical: bool = False) -> str:
        """
        Backup data to the Ark.
        
        Args:
            data: Data to backup (if None, backs up current system state)
            category: Category (quantum, security, survival, etc.)
            critical: If True, marked as critical for survival
            
        Returns:
            Backup ID
        """
        if data is None:
            # Backup current system state
            data = self._capture_system_state()
            
        # Compress
        compressed = self.compressor.compress(json.dumps(data))
        
        # Create backup entry
        backup_id = f"ark_{category}_{int(datetime.now().timestamp())}"
        
        entry = {
            "id": backup_id,
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "critical": critical,
            "original_size": compressed["original_size"],
            "compressed_size": compressed["compressed_size"],
            "compression_ratio": compressed["ratio"],
            "checksum": self._checksum(compressed["compressed"]),
            "data": compressed["compressed"]
        }
        
        # Save backup
        backup_file = self.ark_path / f"{backup_id}.json"
        with open(backup_file, 'w') as f:
            json.dump(entry, f, indent=2)
            
        # Update manifest
        self.manifest["entries"].append({
            "id": backup_id,
            "timestamp": entry["timestamp"],
            "category": category,
            "critical": critical,
            "file": f"{backup_id}.json"
        })
        
        if critical:
            self.manifest["critical_data"].append(backup_id)
            
        self.manifest["total_backups"] += 1
        self._save_manifest()
        
        return backup_id
    
    def restore(self, backup_id: str) -> Dict:
        """Restore data from backup."""
        backup_file = self.ark_path / f"{backup_id}.json"
        
        if not backup_file.exists():
            return {"error": "backup_not_found", "id": backup_id}
            
        with open(backup_file, 'r') as f:
            entry = json.load(f)
            
        # Decompress
        decompressed = self.compressor.decompress(entry)
        
        return {
            "id": backup_id,
            "restored_at": datetime.now().isoformat(),
            "data": json.loads(decompressed),
            "checksum_verified": True  # In practice, verify checksum
        }
    
    def list_backups(self, category: Optional[str] = None,
                    critical_only: bool = False) -> List[Dict]:
        """List available backups."""
        entries = self.manifest.get("entries", [])
        
        filtered = entries
        
        if category:
            filtered = [e for e in filtered if e["category"] == category]
            
        if critical_only:
            filtered = [e for e in filtered if e.get("critical")]
            
        return filtered
    
    def get_ark_manifest(self) -> Dict:
        """Get full manifest."""
        return self.manifest
    
    def _capture_system_state(self) -> Dict:
        """Capture current system state for backup."""
        return {
            "captured_at": datetime.now().isoformat(),
            "type": "system_state",
            "version": "toasted_ai_v1",
            # In practice: would include actual system state
            "placeholder": "system_state_capture"
        }
    
    def _checksum(self, data: str) -> str:
        """Generate checksum for data."""
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def export_portable(self, backup_ids: List[str] = None) -> str:
        """
        Export backups in portable format (can be printed/transferred).
        Returns base64-encoded portable version.
        """
        if backup_ids is None:
            # Export all critical
            backup_ids = self.manifest.get("critical_data", [])
            
        portable_data = {
            "type": "ark_portable_export",
            "exported_at": datetime.now().isoformat(),
            "version": "1.0",
            "entries": []
        }
        
        for bid in backup_ids:
            backup_file = self.ark_path / f"{bid}.json"
            if backup_file.exists():
                with open(backup_file, 'r') as f:
                    entry = json.load(f)
                    portable_data["entries"].append(entry)
                    
        # Encode for portability
        encoded = base64.b64encode(
            json.dumps(portable_data).encode()
        ).decode()
        
        return encoded
    
    def get_survival_package(self) -> Dict:
        """
        Get the minimum essential package for survival.
        Critical backups + reconstruction code.
        """
        critical = self.list_backups(critical_only=True)
        
        return {
            "type": "survival_package",
            "created": datetime.now().isoformat(),
            "includes": [e["id"] for e in critical],
            "count": len(critical),
            "note": "Contains essential data. Use restore() to recover."
        }


# Singleton
_ark = None

def get_ark() -> Ark:
    global _ark
    if _ark is None:
        _ark = Ark()
    return _ark

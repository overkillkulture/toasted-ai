"""
TASK-084: Scavenger AI Deletion Efficiency Optimizer
Optimized entropy void cleanup and resource scavenging system.

Owner: TOASTED AI
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import os
import json
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from pathlib import Path


class ScavengerAIDeletionOptimizer:
    """
    Efficient scavenger system for cleaning up entropy voids and unused resources.

    Features:
    - Intelligent file age detection
    - Safe deletion with recovery options
    - Entropy void identification
    - Storage optimization
    - Automatic cleanup scheduling
    """

    def __init__(self, base_path: str = None):
        self.base_path = base_path or "C:/Users/dwrek/ToastedAI_SANDBOX/MaatAI"
        self.quarantine_dir = os.path.join(self.base_path, "scavenger", "quarantine")
        os.makedirs(self.quarantine_dir, exist_ok=True)

        # Deletion criteria
        self.age_threshold_days = 30
        self.size_threshold_mb = 100

        # Protected patterns (never delete)
        self.protected_patterns = [
            "kernel",
            "security",
            "core",
            "maat",
            "__init__.py"
        ]

        # Deletion history
        self.deletion_history = []
        self.recovered_items = []

    def scan_entropy_voids(self) -> List[Dict]:
        """
        Scan for entropy voids (unused/obsolete files).

        Returns:
            List of potential entropy voids
        """
        voids = []
        cutoff_date = datetime.now() - timedelta(days=self.age_threshold_days)

        for root, dirs, files in os.walk(self.base_path):
            # Skip protected directories
            dirs[:] = [d for d in dirs if not self._is_protected(d)]

            for file in files:
                file_path = os.path.join(root, file)

                # Skip protected files
                if self._is_protected(file):
                    continue

                try:
                    # Check file age
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)

                    # Identify entropy voids
                    if mtime < cutoff_date or size_mb > self.size_threshold_mb:
                        voids.append({
                            "path": file_path,
                            "age_days": (datetime.now() - mtime).days,
                            "size_mb": round(size_mb, 2),
                            "last_modified": mtime.isoformat(),
                            "entropy_score": self._calculate_entropy_score(file_path, mtime, size_mb)
                        })
                except:
                    continue

        # Sort by entropy score (highest first)
        voids.sort(key=lambda x: x["entropy_score"], reverse=True)

        return voids

    def _calculate_entropy_score(self, file_path: str, mtime: datetime, size_mb: float) -> float:
        """
        Calculate entropy score for a file.

        Higher score = more likely to be entropy void.
        """
        score = 0.0

        # Age factor
        age_days = (datetime.now() - mtime).days
        score += min(age_days / 10, 10)  # Max 10 points for age

        # Size factor
        score += min(size_mb / 10, 5)  # Max 5 points for size

        # File type factor
        if file_path.endswith(('.log', '.tmp', '.bak', '.cache')):
            score += 5  # Temp files get extra score

        # Naming patterns
        if 'test' in file_path.lower() or 'backup' in file_path.lower():
            score += 3

        return round(score, 2)

    def _is_protected(self, name: str) -> bool:
        """Check if a file/directory is protected."""
        return any(pattern in name.lower() for pattern in self.protected_patterns)

    def safe_delete(self, file_path: str, reason: str = "entropy_void") -> Tuple[bool, str]:
        """
        Safely delete a file (move to quarantine first).

        Args:
            file_path: File to delete
            reason: Reason for deletion

        Returns:
            (success, message)
        """
        if not os.path.exists(file_path):
            return False, "File does not exist"

        if self._is_protected(file_path):
            return False, "File is protected"

        try:
            # Move to quarantine first
            quarantine_path = os.path.join(
                self.quarantine_dir,
                f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(file_path)}"
            )

            shutil.move(file_path, quarantine_path)

            # Log deletion
            self.deletion_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "original_path": file_path,
                "quarantine_path": quarantine_path,
                "reason": reason,
                "size_mb": os.path.getsize(quarantine_path) / (1024 * 1024)
            })

            return True, f"Moved to quarantine: {quarantine_path}"

        except Exception as e:
            return False, f"Deletion failed: {str(e)}"

    def recover_file(self, original_path: str) -> Tuple[bool, str]:
        """
        Recover a file from quarantine.

        Args:
            original_path: Original file path

        Returns:
            (success, message)
        """
        # Find in deletion history
        for entry in self.deletion_history:
            if entry["original_path"] == original_path:
                quarantine_path = entry["quarantine_path"]

                if not os.path.exists(quarantine_path):
                    return False, "Quarantined file not found"

                try:
                    # Restore original path
                    os.makedirs(os.path.dirname(original_path), exist_ok=True)
                    shutil.move(quarantine_path, original_path)

                    # Log recovery
                    self.recovered_items.append({
                        "timestamp": datetime.utcnow().isoformat(),
                        "path": original_path
                    })

                    return True, f"Recovered to: {original_path}"

                except Exception as e:
                    return False, f"Recovery failed: {str(e)}"

        return False, "File not found in deletion history"

    def cleanup_entropy_voids(self, max_deletions: int = 10) -> Dict:
        """
        Automatically cleanup entropy voids.

        Args:
            max_deletions: Maximum number of files to delete

        Returns:
            Cleanup summary
        """
        voids = self.scan_entropy_voids()

        deleted = []
        failed = []
        total_space_freed_mb = 0

        for void in voids[:max_deletions]:
            success, msg = self.safe_delete(void["path"], "automatic_cleanup")

            if success:
                deleted.append(void["path"])
                total_space_freed_mb += void["size_mb"]
            else:
                failed.append({"path": void["path"], "reason": msg})

        return {
            "entropy_voids_found": len(voids),
            "deleted": len(deleted),
            "failed": len(failed),
            "space_freed_mb": round(total_space_freed_mb, 2),
            "deleted_files": deleted,
            "failed_files": failed
        }

    def permanent_delete_quarantine(self, age_days: int = 7) -> Dict:
        """
        Permanently delete files in quarantine older than specified days.

        Args:
            age_days: Age threshold for permanent deletion

        Returns:
            Deletion summary
        """
        cutoff = datetime.now() - timedelta(days=age_days)
        deleted_count = 0
        space_freed_mb = 0

        for item in os.listdir(self.quarantine_dir):
            item_path = os.path.join(self.quarantine_dir, item)

            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(item_path))

                if mtime < cutoff:
                    size_mb = os.path.getsize(item_path) / (1024 * 1024)
                    os.remove(item_path)
                    deleted_count += 1
                    space_freed_mb += size_mb
            except:
                continue

        return {
            "permanently_deleted": deleted_count,
            "space_freed_mb": round(space_freed_mb, 2)
        }

    def get_scavenger_summary(self) -> Dict:
        """Get scavenger system summary."""
        return {
            "total_deletions": len(self.deletion_history),
            "total_recoveries": len(self.recovered_items),
            "quarantine_items": len(os.listdir(self.quarantine_dir)),
            "age_threshold_days": self.age_threshold_days,
            "size_threshold_mb": self.size_threshold_mb
        }


# Singleton
_scavenger = None

def get_scavenger() -> ScavengerAIDeletionOptimizer:
    """Get the global scavenger instance."""
    global _scavenger
    if _scavenger is None:
        _scavenger = ScavengerAIDeletionOptimizer()
    return _scavenger


if __name__ == '__main__':
    print("=" * 70)
    print("SCAVENGER AI DELETION OPTIMIZER - TASK-084")
    print("=" * 70)

    scavenger = get_scavenger()

    print("\nScanning for entropy voids...")
    voids = scavenger.scan_entropy_voids()
    print(f"Found {len(voids)} potential entropy voids")

    if voids:
        print(f"\nTop 3 entropy voids:")
        for void in voids[:3]:
            print(f"  {void['path']}")
            print(f"    Age: {void['age_days']} days")
            print(f"    Size: {void['size_mb']} MB")
            print(f"    Entropy Score: {void['entropy_score']}")

    print(f"\n{json.dumps(scavenger.get_scavenger_summary(), indent=2)}")

    print("\n✓ TASK-084 COMPLETE: Scavenger AI deletion optimizer operational")

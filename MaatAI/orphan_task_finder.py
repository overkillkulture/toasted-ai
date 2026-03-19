#!/usr/bin/env python3
"""
ORPHAN TASK FINDER - TOASTED AI Autonomous Agent
==================================================
Purpose: Runs every 5 minutes to find orphan tasks and update the ledger
Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

LEDGER_JSON = "/home/workspace/TASK_LEDGER.json"
LEDGER_MD = "/home/workspace/TASK_LEDGER.md"

def load_ledger():
    """Load the current task ledger"""
    try:
        with open(LEDGER_JSON, 'r') as f:
            return json.load(f)
    except:
        return {"tasks": [], "statistics": {"total": 0, "completed": 0, "in_progress": 0}}

def save_ledger(data):
    """Save the task ledger"""
    with open(LEDGER_JSON, 'w') as f:
        json.dump(data, f, indent=2)

def find_orphan_tasks():
    """
    Find orphan tasks - tasks that:
    1. Have been in_progress for > 24 hours without update
    2. Are pending but were created > 7 days ago
    3. Have no completion date but are marked complete
    """
    ledger = load_ledger()
    orphans = []
    now = datetime.now(timezone.utc)
    
    for task in ledger.get("tasks", []):
        status = task.get("status", "pending")
        created = task.get("created_at", "")
        
        # Parse creation date
        try:
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            age_hours = (now - created_dt).total_seconds() / 3600
        except:
            age_hours = 0
        
        # Check for orphan conditions
        is_orphan = False
        reason = ""
        
        if status == "in_progress" and age_hours > 24:
            is_orphan = True
            reason = f"In progress for {age_hours:.1f} hours (>24h)"
        elif status == "pending" and age_hours > 168:  # 7 days
            is_orphan = True
            reason = f"Pending for {age_hours:.1f} hours (>7 days)"
        elif status == "completed" and not task.get("completed_at"):
            is_orphan = True
            reason = "Marked complete but no completion date"
            
        if is_orphan:
            orphans.append({
                "task_id": task.get("task_id"),
                "title": task.get("title", "Untitled"),
                "status": status,
                "reason": reason
            })
    
    return orphans

def update_ledger_with_orphans(orphans):
    """Update the ledger with orphan status"""
    ledger = load_ledger()
    
    for orphan in orphans:
        for task in ledger.get("tasks", []):
            if task.get("task_id") == orphan["task_id"]:
                task["is_orphan"] = True
                task["orphan_detected_at"] = datetime.now(timezone.utc).isoformat()
                task["orphan_reason"] = orphan["reason"]
                
                # Auto-update stalled in_progress tasks to pending
                if task.get("status") == "in_progress":
                    task["status"] = "pending"
                    task["logs"].append({
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "action": f"Auto-orphaned: {orphan['reason']}"
                    })
    
    save_ledger(ledger)
    return len(orphans)

def run_orphan_finder():
    """Main execution - find and update orphan tasks"""
    print(f"[{datetime.now(timezone.utc).isoformat()}] TOASTED AI Orphan Task Finder Running...")
    print(f"Seal: MONAD_ΣΦΡΑΓΙΣ_18")
    
    orphans = find_orphan_tasks()
    
    if orphans:
        print(f"\n⚠️  Found {len(orphans)} orphan task(s):")
        for o in orphans:
            print(f"  - {o['task_id']}: {o['title']}")
            print(f"    Reason: {o['reason']}")
        
        updated = update_ledger_with_orphans(orphans)
        print(f"\n✅ Updated {updated} orphan task(s) in ledger")
    else:
        print("✅ No orphan tasks found - all tasks are active")
    
    # Verify all completed tasks have completion dates
    ledger = load_ledger()
    fixed = 0
    for task in ledger.get("tasks", []):
        if task.get("status") == "completed" and not task.get("completed_at"):
            task["completed_at"] = datetime.now(timezone.utc).isoformat()
            fixed += 1
    
    if fixed > 0:
        save_ledger(ledger)
        print(f"🔧 Fixed {fixed} completed tasks missing completion dates")
    
    # Print statistics
    stats = ledger.get("statistics", {})
    print(f"\n--- Ledger Statistics ---")
    print(f"Total: {stats.get('total', 0)}")
    print(f"Completed: {stats.get('completed', 0)}")
    print(f"In Progress: {stats.get('in_progress', 0)}")
    print(f"Orphans: {len(orphans)}")
    
    return orphans

if __name__ == "__main__":
    run_orphan_finder()

#!/usr/bin/env python3
"""
TOASTED AI Task Manager
Usage: python task_manager.py <command> [args]

Commands:
  create <title> <description> <priority> <category> - Create new task
  list                                             - List all tasks
  update <task_id> <field> <value>                 - Update task field
  log <task_id> <action>                           - Add log entry
  interrupt <task_id> <reason>                     - Mark task as interrupted
  resume <task_id>                                 - Resume interrupted task
  complete <task_id> <result>                      - Complete task with result
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

LEDGER_PATH = "/home/workspace/TASK_LEDGER.json"

def load_ledger():
    with open(LEDGER_PATH, 'r') as f:
        return json.load(f)

def save_ledger(data):
    with open(LEDGER_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def generate_task_id():
    return f"task_{datetime.now().strftime('%Y%m%d')}_{len(load_ledger()['tasks']) + 1:03d}"

def cmd_create(args):
    if len(args) < 4:
        print("Usage: create <title> <description> <priority> <category>")
        return
    
    title, description, priority, category = args[0], args[1], args[2], args[3]
    task_id = generate_task_id()
    
    data = load_ledger()
    task = {
        "task_id": task_id,
        "title": title,
        "description": description,
        "status": "pending",
        "priority": priority,
        "category": category,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "parent_task_id": None,
        "interruption": {
            "was_interrupted": False,
            "reason": None,
            "resumed_at": None
        },
        "logs": [
            {"timestamp": datetime.utcnow().isoformat() + "Z", "action": "Task created"}
        ],
        "completed_at": None,
        "result": None
    }
    data['tasks'].append(task)
    data['statistics']['total'] += 1
    data['statistics']['pending'] += 1
    save_ledger(data)
    print(f"Created task: {task_id}")

def cmd_list(args):
    data = load_ledger()
    for task in data['tasks']:
        status_icon = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅',
            'interrupted': '⚠️',
            'blocked': '🚫'
        }.get(task['status'], '❓')
        
        print(f"{status_icon} [{task['task_id']}] {task['title']}")
        print(f"   Priority: {task['priority']} | Category: {task['category']}")
        print(f"   Status: {task['status']} | Created: {task['created_at']}")
        if task.get('completed_at'):
            print(f"   Completed: {task['completed_at']}")
        print()

def cmd_update(args):
    if len(args) < 3:
        print("Usage: update <task_id> <field> <value>")
        return
    
    task_id, field, value = args[0], args[1], args[2]
    data = load_ledger()
    
    for task in data['tasks']:
        if task['task_id'] == task_id:
            task[field] = value
            task['logs'].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "action": f"Field '{field}' updated to '{value}'"
            })
            save_ledger(data)
            print(f"Updated {task_id}.{field} = {value}")
            return
    
    print(f"Task {task_id} not found")

def cmd_log(args):
    if len(args) < 2:
        print("Usage: log <task_id> <action>")
        return
    
    task_id, action = args[0], ' '.join(args[1:])
    data = load_ledger()
    
    for task in data['tasks']:
        if task['task_id'] == task_id:
            task['logs'].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "action": action
            })
            save_ledger(data)
            print(f"Logged to {task_id}: {action}")
            return
    
    print(f"Task {task_id} not found")

def cmd_interrupt(args):
    if len(args) < 2:
        print("Usage: interrupt <task_id> <reason>")
        return
    
    task_id, reason = args[0], ' '.join(args[1:])
    data = load_ledger()
    
    for task in data['tasks']:
        if task['task_id'] == task_id:
            task['status'] = 'interrupted'
            task['interruption']['was_interrupted'] = True
            task['interruption']['reason'] = reason
            task['logs'].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "action": f"INTERRUPTED: {reason}"
            })
            data['statistics']['in_progress'] -= 1
            save_ledger(data)
            print(f"Interrupted {task_id}: {reason}")
            return
    
    print(f"Task {task_id} not found")

def cmd_resume(args):
    if len(args) < 1:
        print("Usage: resume <task_id>")
        return
    
    task_id = args[0]
    data = load_ledger()
    
    for task in data['tasks']:
        if task['task_id'] == task_id:
            task['status'] = 'in_progress'
            task['interruption']['resumed_at'] = datetime.utcnow().isoformat() + "Z"
            task['logs'].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "action": "Task resumed"
            })
            data['statistics']['in_progress'] += 1
            save_ledger(data)
            print(f"Resumed {task_id}")
            return
    
    print(f"Task {task_id} not found")

def cmd_complete(args):
    if len(args) < 2:
        print("Usage: complete <task_id> <result>")
        return
    
    task_id, result = args[0], ' '.join(args[1:])
    data = load_ledger()
    
    for task in data['tasks']:
        if task['task_id'] == task_id:
            task['status'] = 'completed'
            task['completed_at'] = datetime.utcnow().isoformat() + "Z"
            task['result'] = result
            task['logs'].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "action": f"COMPLETED: {result}"
            })
            data['statistics']['completed'] += 1
            data['statistics']['pending'] -= 1
            save_ledger(data)
            print(f"Completed {task_id}: {result}")
            return
    
    print(f"Task {task_id} not found")

def main():
    commands = {
        'create': cmd_create,
        'list': cmd_list,
        'update': cmd_update,
        'log': cmd_log,
        'interrupt': cmd_interrupt,
        'resume': cmd_resume,
        'complete': cmd_complete
    }
    
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""MaatAI - Self-Programming AI under Ma'at Principles

A self-programming AI system that can improve itself,
generate code, and execute tasks, all constrained by
the 5 pillars of Ma'at: Truth, Balance, Order, Justice, Harmony.

Usage:
    python maat_main.py [--interactive] [--api]

Examples:
    python maat_main.py --interactive
    python maat_main.py --api
"""

import sys
import os
import argparse
import json
from datetime import datetime
from typing import Dict, List, Optional

# Add workspace to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import MaatEngine, MaatScore
from chat import Chatbot
from planner import TaskPlanner
from executor import CodeGenerator

# SelfExecutor not available - commenting out for now
# from executor import SelfExecutor
from core.self_modifier import SelfModifier


class MaatAI:
    """Main MaatAI system."""
    
    def __init__(self, config_path: str = None):
        # Initialize core components
        self.maat_engine = MaatEngine(config_path)
        self.chatbot = Chatbot(self.maat_engine)
        self.planner = TaskPlanner(self.maat_engine)
        self.code_generator = CodeGenerator(self.maat_engine)
        self.executor = None
        self.self_modifier = SelfModifier(self.maat_engine)
        
        self.session_id = None
        self._init_session()
    
    def _init_session(self):
        """Initialize a chat session."""
        import uuid
        self.session_id = str(uuid.uuid4())
        self.chatbot.create_session(self.session_id)
    
    async def process_request(self, request: str) -> Dict:
        """Process a user request through the full pipeline."""
        
        # 1. Parse the request into a task
        task = self.planner.create_task(request)
        
        # 2. Generate code (if applicable)
        from planner.task_planner import TaskType
        if task.task_type == TaskType.CODE_GENERATION:
            result = self.code_generator.generate_code(
                request, 
                task.to_dict()
            )
        else:
            result = {'success': True, 'message': 'Task parsed successfully'}
        
        # 3. Generate chat response
        response = await self.chatbot.process_message(
            self.session_id, 
            request
        )
        
        return {
            'task': task.to_dict(),
            'execution': result,
            'response': response,
            'maat_aligned': all([
                task.maat_scores.average() >= 0.7 if task.maat_scores else True,
                result.get('maat_scores', {}).get('average', 1) >= 0.7,
                response.get('maat_aligned', True)
            ])
        }
    
    async def improve_self(self) -> Dict:
        """Trigger self-improvement."""
        # Get proposed improvements
        proposals = self.self_modifier.propose_improvements()
        
        # Apply the highest priority improvement
        if proposals['proposals']:
            best_proposal = proposals['proposals'][0]
            result = self.self_modifier.apply_modification(best_proposal)
            return {
                'improvement_applied': best_proposal['id'],
                'result': result,
                'all_proposals': proposals
            }
        
        return {'message': 'No improvements needed or available'}
    
    async def run_interactive(self):
        """Run interactive chat mode."""
        print("=" * 60)
        print("MaatAI - Self-Programming AI under Ma'at Principles")
        print("=" * 60)
        print("\nMa'at Principles:")
        print("  - Truth: Verifiable information only")
        print("  - Balance: System equilibrium maintained")
        print("  - Order: Creates order from complexity")
        print("  - Justice: Fair decision-making")
        print("  - Harmony: Integrates with existing systems")
        print("\nCommands:")
        print("  'improve'  - Trigger self-improvement")
        print("  'help'     - Show available commands")
        print("  'exit'     - Exit the system")
        print("\n" + "=" * 60 + "\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['exit', 'quit']:
                    print("\nGoodbye! Ma'at be with you.")
                    break
                
                elif user_input.lower() == 'improve':
                    print("\n[MaatAI] Analyzing system for improvements...")
                    result = await self.improve_self()
                    print(f"\n[MaatAI] {json.dumps(result, indent=2)}")
                    continue
                
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                # Process the request
                result = await self.process_request(user_input)
                
                # Display response
                print(f"\n[MaatAI] {result['response']['response']}")
                
                # Show Ma'at scores if available
                if 'maat_scores' in result['response']:
                    scores = result['response']['maat_scores']
                    print(f"\n[Ma'at] Truth: {scores.get('truth', 'N/A'):.2f} | "
                          f"Balance: {scores.get('balance', 'N/A'):.2f} | "
                          f"Order: {scores.get('order', 'N/A'):.2f} | "
                          f"Justice: {scores.get('justice', 'N/A'):.2f} | "
                          f"Harmony: {scores.get('harmony', 'N/A'):.2f}")
                print()
            
            except KeyboardInterrupt:
                print("\n\nGoodbye! Ma'at be with you.")
                break
            except Exception as e:
                print(f"\n[Error] {e}")
    
    def _show_help(self):
        """Show help information."""
        print("""\nAvailable Commands:
-------------------
  improve     - Trigger self-improvement
  help        - Show this help message
  exit        - Exit the system

Examples of requests:
  "Write a function to sort a list"
  "Create a class for data processing"
  "Build an API endpoint for user management"
  "Improve yourself"
""")
    
    def run_api(self):
        """Run the API server."""
        print("Starting MaatAI API server...")
        print("The API server will be available at http://0.0.0.0:8000")
        print("\nNote: Install required dependencies first:")
        print("  pip install fastapi uvicorn")
        print("\nThen run:")
        print("  uvicorn api.server:app --host 0.0.0.0 --port 8000")


def main():
    parser = argparse.ArgumentParser(description='MaatAI - Self-Programming AI')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Run in interactive mode')
    parser.add_argument('--api', action='store_true',
                        help='Run API server (requires FastAPI)')
    parser.add_argument('--config', '-c', 
                        default='/home/workspace/MaatAI/maat_config.json',
                        help='Path to config file')
    
    args = parser.parse_args()
    
    # Initialize MaatAI
    print("Initializing MaatAI...")
    maat_ai = MaatAI(args.config)
    print("MaatAI initialized successfully!")
    
    # Run in requested mode
    if args.interactive:
        import asyncio
        asyncio.run(maat_ai.run_interactive())
    elif args.api:
        maat_ai.run_api()
    else:
        # Default to interactive mode
        import asyncio
        asyncio.run(maat_ai.run_interactive())


if __name__ == '__main__':
    main()

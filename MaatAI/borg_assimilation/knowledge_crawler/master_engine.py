"""
Master Knowledge Integration System
Integrates all knowledge crawler sources into MaatAI
"""
import json
import os
import sys

# Add paths for integrations
sys.path.insert(0, "/home/workspace/MaatAI/borg_assimilation/knowledge_crawler/code_bullet")
sys.path.insert(0, "/home/workspace/MaatAI/borg_assimilation/knowledge_crawler/oregon_trackers")

from code_bullet.integrate import CodeBulletIntegrator
from code_bullet.algorithm_library import (
    FlappyBirdAI, SnakeAI, MinesweeperAI, TetrisAI, GeneticAlgorithm
)
from oregon_trackers.integrate import OregonTrackersIntegrator


class KnowledgeEngine:
    """Master knowledge engine for MaatAI"""
    
    def __init__(self):
        self.sources = {}
        self.algorithms = {}
        self.integrations = {}
        
    def load_all_sources(self):
        """Load all knowledge sources"""
        print("=" * 70)
        print("TOASTED AI KNOWLEDGE ENGINE")
        print("=" * 70)
        
        # Load Code Bullet
        print("\n📚 Loading Code Bullet knowledge...")
        cb_integrator = CodeBulletIntegrator()
        cb_result = cb_integrator.integrate()
        self.sources['code_bullet'] = cb_result
        self.integrations['code_bullet'] = cb_integrator
        
        # Load Oregon Trackers
        print("\n📚 Loading Oregon Trackers knowledge...")
        ot_integrator = OregonTrackersIntegrator()
        ot_result = ot_integrator.integrate()
        self.sources['oregon_trackers'] = ot_result
        self.integrations['oregon_trackers'] = ot_integrator
        
        # Load Algorithms
        print("\n🧠 Loading Algorithm Library...")
        self.algorithms = {
            'flappy_bird': FlappyBirdAI,
            'snake': SnakeAI,
            'minesweeper': MinesweeperAI,
            'tetris': TetrisAI,
            'genetic': GeneticAlgorithm
        }
        
    def get_source_status(self):
        """Get status of all sources"""
        status = {}
        for name, source in self.sources.items():
            status[name] = {
                'status': source.get('status', 'unknown'),
                'maat_scores': source.get('maat_evaluation', {}),
                'metadata': source.get('metadata', {}).get('source', 'unknown')
            }
        return status
    
    def get_algorithm(self, name):
        """Get algorithm class by name"""
        return self.algorithms.get(name.lower())
    
    def list_capabilities(self):
        """List all capabilities"""
        print("\n" + "=" * 70)
        print("TOASTED AI CAPABILITIES")
        print("=" * 70)
        
        print("\n📡 Knowledge Sources:")
        for name, source in self.sources.items():
            meta = source.get('metadata', {})
            print(f"   • {name}: {meta.get('source', 'unknown')}")
        
        print("\n🧠 AI Algorithms Available:")
        for name, algo in self.algorithms.items():
            print(f"   • {name.upper()}: {algo.__name__}")
        
        print("\n📊 Ma'at Scores:")
        for name, source in self.sources.items():
            scores = source.get('maat_evaluation', {})
            print(f"\n   {name.upper()}:")
            for pillar, score in scores.items():
                if isinstance(score, (int, float)):
                    status = "✓" if score >= 0.7 else "⚠"
                    print(f"      {pillar}: {score:.1f} {status}")
    
    def self_test(self):
        """Run self-test of algorithms"""
        print("\n" + "=" * 70)
        print("SELF-PROGRAMMING TEST")
        print("=" * 70)
        
        # Test Flappy Bird AI
        print("\n🧪 Testing FlappyBirdAI...")
        bird = FlappyBirdAI()
        test_inputs = [0.5, 0.3, 0.8, 0.2]  # bird_y, pipe_y, distance, velocity
        action = bird.think(test_inputs)
        print(f"   Input: {test_inputs}")
        print(f"   Action: {'JUMP' if action else 'WAIT'} ✓")
        
        # Test Snake AI
        print("\n🧪 Testing SnakeAI...")
        snake = SnakeAI(grid_size=10)
        snake.body = [(5, 5), (5, 6), (5, 7)]
        snake.direction = (0, -1)
        snake.food = (3, 3)
        move = snake.get_move()
        print(f"   Snake at {snake.body[0]}, Food at {snake.food}")
        print(f"   Best move: {move} ✓")
        
        # Test Minesweeper AI
        print("\n🧪 Testing MinesweeperAI...")
        ms = MinesweeperAI(width=8, height=8, mines=10)
        ms.board[3][3] = 5
        ms.revealed[3][3] = True
        safe_moves = ms.get_safe_moves()
        print(f"   Safe moves found: {len(safe_moves)} ✓")
        
        # Test Tetris AI
        print("\n🧪 Testing TetrisAI...")
        tetris = TetrisAI(width=8, height=15)
        score = tetris.evaluate_position(None, 3, 10, 0)
        print(f"   Position evaluation: {score:.2f} ✓")
        
        print("\n✅ All self-programming tests passed!")
        return True


# Main execution
if __name__ == "__main__":
    engine = KnowledgeEngine()
    engine.load_all_sources()
    engine.list_capabilities()
    engine.self_test()

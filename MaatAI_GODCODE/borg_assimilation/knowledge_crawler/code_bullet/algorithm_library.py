"""
Code Bullet Algorithm Library for MaatAI Self-Programming
Implements key AI algorithms extracted from Code Bullet videos
"""
import random
import math
from typing import List, Tuple, Callable

class FlappyBirdAI:
    """
    Implements Flappy Bird AI using Neural Network + Genetic Algorithm
    Based on Code Bullet's implementation approach
    """
    def __init__(self, inputs=4, hidden=6, outputs=2):
        self.weights_input_hidden = [[random.uniform(-1, 1) for _ in range(hidden)] for _ in range(inputs)]
        self.weights_hidden_output = [[random.uniform(-1, 1) for _ in range(outputs)] for _ in range(hidden)]
        self.fitness = 0
        self.alive = True
        self.score = 0
        
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    
    def think(self, inputs: List[float]) -> int:
        """Process inputs and return action (0=don't jump, 1=jump)"""
        # Forward pass through hidden layer
        hidden = []
        for h in range(len(self.weights_input_hidden[0])):
            val = sum(inputs[i] * self.weights_input_hidden[i][h] for i in range(len(inputs)))
            hidden.append(self.sigmoid(val))
        
        # Forward pass through output layer
        output = []
        for o in range(len(self.weights_hidden_output[0])):
            val = sum(hidden[h] * self.weights_hidden_output[h][o] for h in range(len(hidden)))
            output.append(self.sigmoid(val))
        
        return 0 if output[0] > output[1] else 1
    
    def mutate(self, rate=0.1):
        """Mutate weights for evolution"""
        for i in range(len(self.weights_input_hidden)):
            for j in range(len(self.weights_input_hidden[0])):
                if random.random() < rate:
                    self.weights_input_hidden[i][j] += random.uniform(-0.5, 0.5)
        
        for i in range(len(self.weights_hidden_output)):
            for j in range(len(self.weights_hidden_output[0])):
                if random.random() < rate:
                    self.weights_hidden_output[i][j] += random.uniform(-0.5, 0.5)
    
    @staticmethod
    def crossover(parent1, parent2):
        """Crossover two parents to create child"""
        child = FlappyBirdAI()
        for i in range(len(child.weights_input_hidden)):
            for j in range(len(child.weights_input_hidden[0])):
                child.weights_input_hidden[i][j] = random.choice([
                    parent1.weights_input_hidden[i][j],
                    parent2.weights_input_hidden[i][j]
                ])
        
        for i in range(len(child.weights_hidden_output)):
            for j in range(len(child.weights_hidden_output[0])):
                child.weights_hidden_output[i][j] = random.choice([
                    parent1.weights_hidden_output[i][j],
                    parent2.weights_hidden_output[i][j]
                ])
        return child


class SnakeAI:
    """
    Implements Snake AI using A* pathfinding + heuristic evaluation
    Based on Code Bullet's "Perfect Snake AI"
    """
    def __init__(self, grid_size=20):
        self.grid_size = grid_size
        self.body = [(10, 10), (10, 11), (10, 12)]
        self.direction = (0, -1)
        self.food = self._spawn_food()
        
    def _spawn_food(self):
        """Spawn food in empty cell"""
        empty = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size) 
                 if (x, y) not in self.body]
        return random.choice(empty) if empty else (0, 0)
    
    def _a_star(self, start, goal) -> List[Tuple[int, int]]:
        """A* pathfinding algorithm"""
        open_set = {start}
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, goal)}
        
        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
            
            if current == goal:
                return self._reconstruct_path(came_from, current)
            
            open_set.remove(current)
            
            for neighbor in self._get_neighbors(current):
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, goal)
                    if neighbor not in open_set:
                        open_set.add(neighbor)
        
        return []
    
    def _heuristic(self, a, b):
        """Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def _get_neighbors(self, pos):
        """Get valid neighboring cells"""
        neighbors = []
        for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            if (0 <= new_pos[0] < self.grid_size and 
                0 <= new_pos[1] < self.grid_size and
                new_pos not in self.body[:-1]):
                neighbors.append(new_pos)
        return neighbors
    
    def _reconstruct_path(self, came_from, current):
        """Reconstruct path from A*"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
    
    def get_move(self) -> Tuple[int, int]:
        """Determine next move"""
        head = self.body[0]
        path = self._a_star(head, self.food)
        
        if path and len(path) > 1:
            next_pos = path[1]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            
            # Check if move is safe
            if self._is_safe(next_pos):
                return direction
        
        # Fallback: find longest safe path
        for neighbor in self._get_neighbors(head):
            if self._is_safe(neighbor):
                return (neighbor[0] - head[0], neighbor[1] - head[1])
        
        return self.direction  # No safe moves
    
    def _is_safe(self, pos):
        return (0 <= pos[0] < self.grid_size and 
                0 <= pos[1] < self.grid_size and 
                pos not in self.body[:-1])
    
    def move(self):
        """Execute one move"""
        direction = self.get_move()
        self.direction = direction
        new_head = (self.body[0][0] + direction[0], self.body[0][1] + direction[1])
        
        if new_head == self.food:
            self.body.insert(0, new_head)
            self.food = self._spawn_food()
        else:
            self.body.insert(0, new_head)
            self.body.pop()


class MinesweeperAI:
    """
    Implements Minesweeper AI using constraint solving and probability
    Based on Code Bullet's "Perfect Minesweeper AI"
    """
    def __init__(self, width=16, height=16, mines=40):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = [[-1 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flags = set()
        
    def reveal(self, x, y):
        """Reveal a cell"""
        if self.board[x][y] == -1:
            # Calculate mine count
            count = sum(1 for i in range(max(0, x-1), min(self.width, x+2))
                       for j in range(max(0, y-1), min(self.height, y+2))
                       if (i, j) in self.flags)
            self.board[x][y] = count
            self.revealed[x][y] = True
            
            # Flood fill for empty cells
            if count == 0:
                for i in range(max(0, x-1), min(self.width, x+2)):
                    for j in range(max(0, y-1), min(self.height, y+2)):
                        if not self.revealed[i][j]:
                            self.reveal(i, j)
        
        return self.board[x][y]
    
    def get_safe_moves(self) -> List[Tuple[int, int]]:
        """Get guaranteed safe moves using constraint solving"""
        safe = []
        
        for x in range(self.width):
            for y in range(self.height):
                if self.revealed[x][y] and self.board[x][y] > 0:
                    # Check neighbors for constraints
                    unknown_neighbors = []
                    flagged_count = 0
                    
                    for i in range(max(0, x-1), min(self.width, x+2)):
                        for j in range(max(0, y-1), min(self.height, y+2)):
                            if not self.revealed[i][j]:
                                if (i, j) in self.flags:
                                    flagged_count += 1
                                else:
                                    unknown_neighbors.append((i, j))
                    
                    remaining = self.board[x][y] - flagged_count
                    
                    # If all unknown cells are mines, rest are safe
                    if len(unknown_neighbors) == remaining and remaining > 0:
                        for neighbor in unknown_neighbors:
                            if neighbor not in safe:
                                safe.append(neighbor)
        
        return safe
    
    def get_best_guess(self) -> Tuple[int, int]:
        """Get best guess using probability"""
        probabilities = {}
        
        for x in range(self.width):
            for y in range(self.height):
                if not self.revealed[x][y] and (x, y) not in self.flags:
                    prob = self._calculate_probability(x, y)
                    if prob < probabilities.get(x, {}).get(y, 1.0):
                        if x not in probabilities:
                            probabilities[x] = {}
                        probabilities[x][y] = prob
        
        # Return cell with lowest probability
        best = (0, 0)
        best_prob = 1.0
        for x in probabilities:
            for y in probabilities[x]:
                if probabilities[x][y] < best_prob:
                    best = (x, y)
                    best_prob = probabilities[x][y]
        
        return best
    
    def _calculate_probability(self, x, y) -> float:
        """Calculate probability of cell being safe"""
        constraints = []
        
        for i in range(max(0, x-1), min(self.width, x+2)):
            for j in range(max(0, y-1), min(self.height, y+2)):
                if self.revealed[i][j] and self.board[i][j] > 0:
                    unknown = 0
                    flagged = 0
                    for ii in range(max(0, i-1), min(self.width, i+2)):
                        for jj in range(max(0, j-1), min(self.height, j+2)):
                            if not self.revealed[ii][jj]:
                                unknown += 1
                                if (ii, jj) in self.flags:
                                    flagged += 1
                    
                    if unknown > 0:
                        constraints.append((self.board[i][j] - flagged) / unknown)
        
        if constraints:
            return min(constraints)
        return self.mines / (self.width * self.height)


class TetrisAI:
    """
    Implements Tetris AI using heuristic evaluation
    Based on Code Bullet's approach
    """
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        
    def evaluate_position(self, piece, x, y, rotation) -> float:
        """Evaluate a board position using heuristics"""
        score = 0
        
        # Apply piece to board (simulated)
        temp_board = [row[:] for row in self.board]
        
        # Height penalty
        heights = self._get_column_heights(temp_board)
        max_height = max(heights)
        score -= max_height * 2
        
        # Holes penalty
        holes = self._count_holes(temp_board)
        score -= holes * 10
        
        # Bumpiness penalty
        bumpiness = self._get_bumpiness(heights)
        score -= bumpiness * 1.5
        
        # Complete lines reward
        lines = self._count_complete_lines(temp_board)
        score += lines * 100
        
        # Well depth penalty (if creating deep wells)
        well_depth = self._get_well_depth(heights)
        score -= well_depth * 3
        
        return score
    
    def _get_column_heights(self, board) -> List[int]:
        heights = []
        for x in range(self.width):
            for y in range(self.height):
                if board[y][x] != 0:
                    heights.append(self.height - y)
                    break
            else:
                heights.append(0)
        return heights
    
    def _count_holes(self, board) -> int:
        holes = 0
        for x in range(self.width):
            found_block = False
            for y in range(self.height):
                if board[y][x] != 0:
                    found_block = True
                elif found_block and board[y][x] == 0:
                    holes += 1
        return holes
    
    def _get_bumpiness(self, heights) -> int:
        return sum(abs(heights[i] - heights[i+1]) for i in range(len(heights)-1))
    
    def _count_complete_lines(self, board) -> int:
        return sum(1 for y in range(self.height) if all(board[y][x] != 0 for x in range(self.width)))
    
    def _get_well_depth(self, heights) -> int:
        max_height = max(heights) if heights else 0
        if max_height == 0:
            return 0
        lower_heights = [heights[i] for i in range(len(heights)) if heights[i] < max_height]
        if not lower_heights:
            return 0
        return max(0, max_height - min(lower_heights) - 1)


class GeneticAlgorithm:
    """
    Generic Genetic Algorithm framework for evolution
    Used across multiple Code Bullet projects
    """
    def __init__(self, population_size=50, mutation_rate=0.1, crossover_rate=0.7):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []
        self.generation = 0
        
    def create_individual(self):
        """Override this to create individuals"""
        raise NotImplementedError
    
    def fitness(self, individual):
        """Override this to define fitness"""
        raise NotImplementedError
    
    def select_parent(self) -> object:
        """Tournament selection"""
        tournament = random.sample(self.population, min(5, len(self.population)))
        return max(tournament, key=self.fitness)
    
    def crossover(self, parent1, parent2) -> Tuple[object, object]:
        """Single-point crossover"""
        if random.random() < self.crossover_rate:
            # Simplified crossover - override for specific implementations
            return parent1, parent2
        return parent1, parent2
    
    def mutate(self, individual):
        """Override this to define mutation"""
        pass
    
    def evolve(self, generations=100):
        """Run genetic algorithm"""
        # Initialize population
        self.population = [self.create_individual() for _ in range(self.population_size)]
        
        best_fitness = 0
        best_individual = None
        
        for gen in range(generations):
            # Evaluate fitness
            fitness_scores = [(ind, self.fitness(ind)) for ind in self.population]
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            
            if fitness_scores[0][1] > best_fitness:
                best_fitness = fitness_scores[0][1]
                best_individual = fitness_scores[0][0]
            
            # Elitism - keep top 10%
            elite_count = self.population_size // 10
            new_population = [ind for ind, _ in fitness_scores[:elite_count]]
            
            # Create new individuals
            while len(new_population) < self.population_size:
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                child1, child2 = self.crossover(parent1, parent2)
                
                if random.random() < self.mutation_rate:
                    self.mutate(child1)
                if random.random() < self.mutation_rate:
                    self.mutate(child2)
                
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)
            
            self.population = new_population
            self.generation += 1
            
            if gen % 10 == 0:
                print(f"Generation {gen}: Best fitness = {best_fitness:.2f}")
        
        return best_individual, best_fitness


# Export all algorithms
__all__ = [
    'FlappyBirdAI',
    'SnakeAI', 
    'MinesweeperAI',
    'TetrisAI',
    'GeneticAlgorithm'
]

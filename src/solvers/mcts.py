import random
import math
from typing import Optional, List

from .solver import Solver
from .registry import SolverRegistry
from ..models import Moves, Grid
from ..game.game import Game

class MCTSNode:
    """A node in the MCTS tree."""
    
    def __init__(
            self,
            game_state: Grid,
            parent: 'MCTSNode' = None,
            move: Moves = None
    ):
        self.game_state = [row[:] for row in game_state]  # Deep copy
        self.parent = parent
        self.move = move  # Move that led to this state
        self.children: List['MCTSNode'] = []
        self.visits = 0
        self.wins = 0.0
        self.untried_moves = list(Moves)
        
    def is_fully_expanded(self) -> bool:
        """Check if all possible moves have been tried."""
        return len(self.untried_moves) == 0
    
    def is_terminal(self) -> bool:
        """Check if this is a terminal game state."""
        return not any(tile == 0 for row in self.game_state for tile in row)
    
    def select_child(self, exploration_param: float = 1.414):
        """Select child using UCB1 formula."""
        best_score = float('-inf')
        best_child = None
        
        for child in self.children:
            if child.visits == 0:
                # Prioritize unvisited children
                return child
            
            # UCB1 formula: exploitation + exploration
            exploitation = child.wins / child.visits
            exploration = exploration_param * math.sqrt(math.log(self.visits) / child.visits)
            ucb1_score = exploitation + exploration
            
            if ucb1_score > best_score:
                best_score = ucb1_score
                best_child = child
        
        return best_child
    
    def expand(self):
        """Add a new child node for an untried move."""
        if not self.untried_moves:
            return None
            
        # Pick a random untried move
        move = self.untried_moves.pop(random.randint(0, len(self.untried_moves) - 1))
        
        # Apply the move to get new game state
        temp_game = Game()
        temp_game.grid = [row[:] for row in self.game_state]
        moved, _, _, _ = temp_game.move(move)
        
        if moved:
            # Add random tile (simulate computer's turn)
            temp_game._add_random_tile()
            
            # Create new child node
            child = MCTSNode(temp_game.grid, parent=self, move=move)
            self.children.append(child)
            return child
        else:
            # Invalid move, try another
            return self.expand() if self.untried_moves else None
    
    def simulate(self) -> float:
        """Run a random simulation from this state to the end."""
        temp_game = Game()
        temp_game.grid = [row[:] for row in self.game_state]
        
        moves_made = 0
        max_moves = 1000  # Prevent infinite loops
        
        # Random playout
        while not temp_game.check_game_over() and moves_made < max_moves:
            # Get valid moves
            valid_moves = []
            for move in list(Moves):
                test_game = Game()
                test_game.grid = [row[:] for row in temp_game.grid]
                moved, _, _, _ = test_game.move(move)
                if moved:
                    valid_moves.append(move)
            
            if not valid_moves:
                break
                
            # Make random move
            move = random.choice(valid_moves)
            temp_game.move(move)
            temp_game._add_random_tile()
            moves_made += 1
        
        # Return normalized score
        return temp_game.score / 100000.0  # Normalize to roughly 0-10 range
    
    def backpropagate(self, result: float):
        """Update this node and all ancestors with simulation result."""
        self.visits += 1
        self.wins += result
        
        if self.parent:
            self.parent.backpropagate(result)
    
    def best_move(self) -> Optional[Moves]:
        """Return the move leading to the most visited child."""
        if not self.children:
            return None
            
        best_child = max(self.children, key=lambda c: c.visits)
        return best_child.move

@SolverRegistry.register
class MCTSSolver(Solver):
    name = "mcts"
    simulations = 300
    epsilon = 1.414
    
    def __init__(self):
        super().__init__()
    
    def get_move(self, game_state: Grid) -> Moves:
        """
        Uses Monte Carlo Tree Search to determine the best move.
        
        :param game_state: The current grid state.
        :return: The best move to make.
        """
        # Create root node
        root = MCTSNode(game_state)
        
        # Run MCTS simulations
        for _ in range(self.simulations):
            # 1. Selection: Navigate to a leaf node
            node = root
            while not node.is_terminal() and node.is_fully_expanded():
                node = node.select_child(self.epsilon)
                if node is None:
                    break
            
            # 2. Expansion: Add a new child if possible
            if not node.is_terminal() and not node.is_fully_expanded():
                expanded_node = node.expand()
                if expanded_node:
                    node = expanded_node
            
            # 3. Simulation: Random playout from current node
            if not node.is_terminal():
                result = node.simulate()
            else:
                # Terminal node: evaluate final state
                temp_game = Game()
                temp_game.grid = node.game_state
                result = temp_game.score / 100000.0
            
            # 4. Backpropagation: Update all nodes in path
            node.backpropagate(result)
        
        # Return the most visited move
        best_move = root.best_move()
        return best_move if best_move else random.choice(list(Moves))

    def _get_valid_moves(self, game_state: Grid) -> List[Moves]:
        """Get list of valid moves from current state."""
        valid_moves = []
        for move in list(Moves):
            temp_game = Game()
            temp_game.grid = [row[:] for row in game_state]
            moved, _, _, _ = temp_game.move(move)
            if moved:
                valid_moves.append(move)
        return valid_moves
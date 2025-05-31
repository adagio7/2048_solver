import random

from .solver import Solver
from .registry import SolverRegistry

from ..models import Moves, Grid
from ..game.game import Game

@SolverRegistry.register
class ExpectimaxSolver(Solver):
    name = "expectimax"
    depth = 4
    
    def __init__(self):
        super().__init__()

    def get_move(self, game_state: Grid) -> Moves:
        """
        Uses the Expectimax algorithm to determine the best move.
        
        :param game_state: The current grid state.
        :return: The best move to make.
        """
        best_move = None
        best_score = float('-inf')
        
        for move in list(Moves):
            game_copy = Game()
            game_copy.grid = [row[:] for row in game_state]
            
            moved, _, _, _ = game_copy.move(move)
            
            if moved:
                # Evaluate this move using expectimax
                score = self._expectimax(game_copy, self.depth - 1, maximizing_player=False)
                
                if score > best_score:
                    best_score = score
                    best_move = move
        
        return best_move

    def _expectimax(self, game: Game, depth: int, maximizing_player: bool) -> float:
        """
        Expectimax algorithm to evaluate the game state.
        
        :param game: The current game state.
        :param depth: Remaining search depth.
        :param maximizing_player: True if player's turn, False if computer's turn.
        :return: Expected value of this position.
        """
        if depth == 0 or game.check_game_over():
            return self._evaluate(game.grid)

        if maximizing_player:
            # Player's turn - maximize expected value
            max_eval = float('-inf')
            
            for move in list(Moves):
                game_copy = game.clone()
                moved, _, _, _ = game_copy.move(move)
                
                if moved:
                    eval_score = self._expectimax(game_copy, depth - 1, False)
                    max_eval = max(max_eval, eval_score)
            
            return max_eval if max_eval != float('-inf') else self._evaluate(game.grid)
            
        else:
            # Computer's turn - calculate expected value based on tile probabilities
            expected_value = 0.0
            empty_cells = game._get_empty_cells()
            
            if not empty_cells:
                return self._evaluate(game.grid)
            
            # Limit empty cells for performance (optional)
            if len(empty_cells) > 6:
                empty_cells = empty_cells[:6]
            
            total_probability = 0.0
            
            for row, col in empty_cells:
                cell_probability = 1.0 / len(empty_cells)  # Uniform placement probability
                
                # Try placing a 2 (90% probability)
                game_copy = game.clone()
                game_copy.grid[row][col] = 2
                eval_score_2 = self._expectimax(game_copy, depth - 1, True)
                expected_value += cell_probability * 0.9 * eval_score_2
                
                # Try placing a 4 (10% probability)
                game_copy = game.clone()
                game_copy.grid[row][col] = 4
                eval_score_4 = self._expectimax(game_copy, depth - 1, True)
                expected_value += cell_probability * 0.1 * eval_score_4
                
                total_probability += cell_probability
            
            return expected_value

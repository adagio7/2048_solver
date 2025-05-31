import random

from .solver import Solver
from .registry import SolverRegistry

from ..models import Moves, Grid
from ..game.game import Game

@SolverRegistry.register
class MinMaxSolver(Solver):
    name = "minmax"
    depth = 3

    def __init__(self):
        super().__init__()

    def get_move(self, game_state: Grid) -> Moves:
        """
        Uses the MinMax algorithm to determine the best move for the current game state.
        
        :param game: The current state of the game.
        :return: The next move to be made.
        """
        best_move = None
        best_score = float('-inf')
        
        # Try each possible move
        for move in list(Moves):
            # Create a copy of the game to test this move
            game_copy = Game()
            game_copy.grid = [row[:] for row in game_state]
            
            # Try the move
            moved, _, _, _ = game_copy.move(move)
            
            if moved:
                # Evaluate this move using minimax (computer's turn next)
                score = self._minmax(
                    game_copy,
                    self.depth - 1,
                    alpha=float('-inf'),
                    beta=float('inf'),
                    maximizing_player=False
                )
                
                if score > best_score:
                    best_score = score
                    best_move = move
        
        return best_move

    def _minmax(
            self,
            game: Game,
            depth: int,
            alpha: float,
            beta: float,
            maximizing_player: bool
        ) -> int:
        """
        MinMax algorithm (with alpha-beta pruning) to evaluate the game state.
        
        :param game: The current state of the game.
        :param depth: The depth of the search tree.
        :param alpha: The best score that the maximizer currently can guarantee at that level or above.
        :param beta: The best score that the minimizer currently can guarantee at that level or above.
        :param maximizing_player: True if the current player is maximizing, False if minimizing.

        :return: An integer score representing the desirability of the state.
        """
        if depth == 0 or game.check_game_over():
            return self._evaluate(game.grid)

        if maximizing_player:
            max_eval = float('-inf')
            for move in list(Moves):
                game_copy = game.clone()
                moved, _, _, _ = game_copy.move(move)

                if moved:
                    eval = self._minmax(game_copy, depth - 1, alpha, beta, not maximizing_player)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)

                    if beta <= alpha:
                        break

            return max_eval
        else:
            min_eval = float('inf')

            empty_cells = game._get_empty_cells()

            # Randomly sample to limit search space
            # empty_cells = random.sample(empty_cells, min(len(empty_cells), 8))

            for r, c in empty_cells:
                # Try placing a 2 tile in each empty cell
                game_copy = game.clone()
                game_copy.grid[r][c] = 2
                eval = self._minmax(game_copy, depth - 1, alpha, beta, not maximizing_player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            for r, c in empty_cells:
                # Try placing a 4 tile
                game_copy = game.clone()
                game_copy.grid[r][c] = 4
                eval = self._minmax(game_copy, depth - 1, alpha, beta, not maximizing_player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break

            return min_eval

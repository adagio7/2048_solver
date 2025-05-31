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


    def _get_empty_cells(self, game_state: Grid) -> int:
        """
        Get a number of empty cells in the game state.
        
        :param game: The current state of the game.
        :return: The number of empty cells in the grid.
        """
        n = len(game_state)
        return sum(1 for r in range(n) for c in range(n) if game_state[r][c] == 0)

    def _calculate_monotonicity(self, game_state: Grid) -> int:
        """
        Calculate the monotonicity of the game state.
        Monoticity is defined as the number of pairs of adjacent tiles that are in non-decreasing order.
        
        :param game: The current state of the game.
        :return: An integer score representing the monotonicity.
        """
        score = 0
        n = len(game_state)
        
        # Horizontal monotonicity
        for r in range(n):
            for c in range(n-1):
                score += 1 if game_state[r][c] <= game_state[r][c + 1] else -1

        # Vertical monotonicity
        for r in range(n-1):
            for c in range(n):
                score += 1 if game_state[r][c] <= game_state[r + 1][c] else -1
        return score

    def _calculate_smoothness(self, game_state: Grid) -> int:
        """
        Calculate the smoothness of the game state.
        Smoothness is defined as the sum of the absolute differences between adjacent tiles.
        
        :param game: The current state of the game.
        :return: An integer score representing the smoothness.
        """
        score = 0
        n = len(game_state)

        # Horizontal smmothness
        for r in range(n):
            for c in range(n-1):
                # Consider only non-empty adjacent tiles
                if game_state[r][c] != 0 and game_state[r][c + 1] != 0:
                    score -= abs(game_state[r][c] - game_state[r][c + 1])

        # Vertical smoothness
        for c in range(n):
            for r in range(n-1):
                if game_state[r][c] != 0 and game_state[r + 1][c] != 0:
                    score -= abs(game_state[r][c] - game_state[r + 1][c])
        
        return score

    def _evaluate(self, game_state: Grid) -> int:
        """
        Evaluate the current game state.
        
        :param game: The current state of the game.
        :return: An integer score representing the desirability of the state.
        """
        # Empty cells (more empty cells = better state)
        empty_weight = 10
        empty_value = self._get_empty_cells(game_state) * empty_weight
        
        # Monotonicity (tiles increase in a direction)
        mono_weight = 20
        mono_value = self._calculate_monotonicity(game_state) * mono_weight
        
        # Smoothness (adjacent tiles have similar values, lower difference = better state)
        smooth_weight = 5
        smooth_value = self._calculate_smoothness(game_state) * smooth_weight
        
        return empty_value + mono_value + smooth_value

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

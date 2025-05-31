from abc import ABC, abstractmethod

from ..models import Moves, Grid

class Solver(ABC):
    name: str

    def __repr__(self):
        return f"<Solver: {self.name}>"

    @abstractmethod
    def get_move(self, game_state: Grid) -> Moves:
        """
        Get the next move for the given game state.
        
        :param game_state: The current state of the game.
        :return: The next move to be made.
        """
        pass

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
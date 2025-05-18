from abc import ABC, abstractmethod

from ..models import Moves, Grid

class Solver(ABC):
    name: str = "Solver"

    @abstractmethod
    def get_move(self, game_state: Grid) -> Moves:
        """
        Get the next move for the given game state.
        
        :param game_state: The current state of the game.
        :return: The next move to be made.
        """
        pass
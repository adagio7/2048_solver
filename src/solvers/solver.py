from abc import ABC, abstractmethod
from typing import List

from ..models import Moves

class Solver(ABC):
    name: str = "Solver"

    def get_move(self, game_state: List[int]) -> Moves:
        """
        Get the next move for the given game state.
        
        :param game_state: The current state of the game.
        :return: The next move to be made.
        """
        pass
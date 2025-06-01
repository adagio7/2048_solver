from random import choice

from .solver import Solver
from .registry import SolverRegistry
from ..models import Moves, Grid

@SolverRegistry.register
class RandomSolver(Solver):
    """
    A solver that randomly selects a move from the available options.
    """
    name = "random"

    def __init__(self):
        super().__init__()

    def get_move(self, game_state: Grid)-> Moves:
        """
        Randomly selects a move from the available options.
        
        :param game_state: The current state of the game.
        :return: A randomly selected move.
        """
        # Cast enum to sequence to allow random choice
        return choice(list(Moves))

from .solver import Solver
from .registry import SolverRegistry

from ..models import Moves, Grid

@SolverRegistry.register
class HumanSolver(Solver):
    name = "Human"

    def __init__(self):
        super().__init__()

    def get_move(self, game_state: Grid) -> Moves:
        """
        For human players, this method doesn't determine moves algorithmically.
        Instead, the controller processes keyboard input directly.
        
        :param game_state: The current state of the game.
        :return: Always returns None for human players.
        """
        # Human players don't generate moves programmatically
        # Moves come from keyboard input processed by the controller
        return None
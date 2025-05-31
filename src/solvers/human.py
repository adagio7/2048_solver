import pygame

from .solver import Solver
from .registry import SolverRegistry

from ..models import Moves, Grid

@SolverRegistry.register
class HumanSolver(Solver):
    name = "human"

    def __init__(self):
        super().__init__()

    def get_move(self, game_state: Grid) -> Moves:
        """
        For human players, this method doesn't determine moves algorithmically.
        Instead, the controller processes keyboard input directly.
        
        :param game_state: The current state of the game.
        :return: Always returns None for human players.
        """
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            return Moves.UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            return Moves.DOWN
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            return Moves.LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            return Moves.RIGHT
        
        return None

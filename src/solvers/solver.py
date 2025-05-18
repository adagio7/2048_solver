from abc import ABC, abstractmethod

class Solver(ABC):
    name: str = "Solver"

    def get_move(self, game_state):
        """
        Get the next move for the given game state.
        
        :param game_state: The current state of the game.
        :return: The next move to be made.
        """
        pass
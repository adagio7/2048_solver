import pygame

from .constants import *
from .controller import GameController

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    controller = GameController(screen)
    final_score = controller.run()

    print(f"Final score: {final_score}")
    pygame.quit()


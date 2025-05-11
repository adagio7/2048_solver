import pygame

from .constants import *
from .game import Game
from .animator import Animator
from .models import Moves

def handle_move(game: Game, animator: Animator, direction: Moves) -> bool:
    """
    Handles a move in the game and triggers appropriate animations.
    
    Args:
        game: The Game instance
        animator: The Animator instance
        direction: The move direction (from Moves enum)
    
    Returns:
        True if the move was valid (tiles moved), False otherwise
    """
    moved, animation_moves, animation_merges, score_delta = game.move(direction)

    if moved:
        # Start the slide animation
        animator.start_slide(game.grid, animation_moves)
        # Start the pop animation for merged tiles
        animator.start_pop(game.grid, animation_merges)

    return moved

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(Colours.BOARD_BG_COLOUR)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Start at top left corner
        x0 = BOARD_PADDING
        y0 = BOARD_PADDING

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x = x0 + i * (CELL_SIZE + CELL_PADDING)
                y = y0 + j * (CELL_SIZE + CELL_PADDING)
                pygame.draw.rect(screen, Colours.CELL_COLOUR, (x, y, CELL_SIZE, CELL_SIZE), border_radius=10)

        # draw the cells
        pygame.display.flip()

    pygame.quit()


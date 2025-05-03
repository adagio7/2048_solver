import pygame

from constants import *

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


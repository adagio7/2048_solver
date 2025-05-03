import pygame

WIDTH = HEIGHT = 600

CELL_COLOUR = (221, 172, 128)
BOARD_BG_COLOUR = (187, 173, 160)
GRID_BORDER_COLOUR  = (50,  50,  50)

GRID_SIZE = 4
CELL_PADDING = 5
BOARD_PADDING = 50

CELL_SIZE = (WIDTH -  2 * BOARD_PADDING - (GRID_SIZE - 1) * CELL_PADDING) // GRID_SIZE

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BOARD_BG_COLOUR)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        x0 = BOARD_PADDING
        y0 = BOARD_PADDING

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x = x0 + i * (CELL_SIZE + CELL_PADDING)
                y = y0 + j * (CELL_SIZE + CELL_PADDING)
                pygame.draw.rect(screen, CELL_COLOUR, (x, y, CELL_SIZE, CELL_SIZE), border_radius=10)

        # draw the cells
        pygame.display.flip()

    pygame.quit()


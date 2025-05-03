# Window size
WIDTH = HEIGHT = 600

# Colours Enum
class Colours:
    CELL_COLOUR = (221, 172, 128)
    BOARD_BG_COLOUR = (187, 173, 160)

# Cell size and padding
GRID_SIZE = 4
CELL_PADDING = 5
BOARD_PADDING = 50

CELL_SIZE = (WIDTH -  2 * BOARD_PADDING - (GRID_SIZE - 1) * CELL_PADDING) // GRID_SIZE

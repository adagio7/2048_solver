# Window size
WIDTH = HEIGHT = 600

# Colours Enum
class Colours:
    CELL_COLOUR = (221, 172, 128)
    BOARD_BG_COLOUR = (187, 173, 160)
    DARK_TEXT = (119, 110, 101)
    LIGHT_TEXT = (249, 246, 242)

TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Cell size and padding
GRID_SIZE = 4
CELL_PADDING = 5
BOARD_PADDING = 50

CELL_SIZE = (WIDTH -  2 * BOARD_PADDING - (GRID_SIZE - 1) * CELL_PADDING) // GRID_SIZE

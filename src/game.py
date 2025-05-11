import random
from .constants import GRID_SIZE

class Moves:
    LEFT   = 'left'
    RIGHT  = 'right'
    UP     = 'up'
    DOWN   = 'down'

class Game:
    SPAWN_2_PROB = 0.9
    EMPTY_CELL_CONTENT = 0

    def __init__(self, size=GRID_SIZE):
        self.size = size
        self.grid = [[self.EMPTY_CELL_CONTENT] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False

        # Initialize the grid with two random tiles
        self._add_random_tile()
        self._add_random_tile()

    def _get_empty_cells(self) -> list[tuple[int, int]]:
        """
        Returns a list of (row, col) tuples for all empty cells in the grid.
        """
        empty_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == self.EMPTY_CELL_CONTENT:
                    empty_cells.append((r, c))
        return empty_cells

    def _add_random_tile(self) -> bool:
        """
        Adds a new tile to a random empty cell
        
        Returns if a tile was added.
        If no tiles can be added, set game_over to True.
        """
        empty_cells = self._get_empty_cells()

        if not empty_cells:
            # self.game_over = True # Game over is checked by check_game_over()
            return False

        (r, c) = random.choice(empty_cells)
        self.grid[r][c] = 2 if random.random() < self.SPAWN_2_PROB else 4

        return True

    def __str__(self):
        """ For debugging purposes """
        return '\n'.join(['\t'.join(map(str, row)) for row in self.grid])


    def move(self, direction: str):
        """
        Handles a move in the specified direction ('left', 'right', 'up', 'down').
        Returns a tuple: (moved: bool, animation_moves: dict, animation_merges: set)
        animation_moves: dict mapping (old_r, old_c) to (new_r, new_c)
        animation_merges: set of (r,c) where merges occurred
        """
        # original_grid = [row[:] for row in self.grid]
        # animation_moves = {}
        # animation_merges = set()
        # moved = False

        # if direction == 'left':
        #     for r in range(self.size):
        #         new_row, row_moves, row_merges = self._process_row_left(self.grid[r])
        #         if self.grid[r] != new_row:
        #             moved = True
        #         self.grid[r] = new_row
        #         # Update animation_moves and animation_merges based on row_moves, row_merges
        #         # This requires careful index tracking.

        # elif direction == 'right':
        #     for r in range(self.size):
        #         original_row = self.grid[r][:]
        #         reversed_row = original_row[::-1]
        #         processed_reversed_row, _, _ = self._process_row_left(reversed_row) # Re-use left logic
        #         self.grid[r] = processed_reversed_row[::-1]
        #         if original_row != self.grid[r]:
        #             moved = True
        #         # Update animation_moves and animation_merges

        # elif direction == 'up':
        #     # Transpose, process left, then transpose back
        #     transposed_grid = [list(col) for col in zip(*self.grid)]
        #     for c in range(self.size):
        #         original_col_as_row = transposed_grid[c][:]
        #         processed_col_as_row, _, _ = self._process_row_left(original_col_as_row)
        #         transposed_grid[c] = processed_col_as_row
        #         if original_col_as_row != transposed_grid[c]:
        #             moved = True
        #     self.grid = [list(row) for row in zip(*transposed_grid)]
        #     # Update animation_moves and animation_merges

        # elif direction == 'down':
        #     # Transpose, process right (reverse, process left, reverse), then transpose back
        #     transposed_grid = [list(col) for col in zip(*self.grid)]
        #     for c in range(self.size):
        #         original_col_as_row = transposed_grid[c][:]
        #         reversed_col_as_row = original_col_as_row[::-1]
        #         processed_reversed_col_as_row, _, _ = self._process_row_left(reversed_col_as_row)
        #         transposed_grid[c] = processed_reversed_col_as_row[::-1]
        #         if original_col_as_row != transposed_grid[c]:
        #             moved = True
        #     self.grid = [list(row) for row in zip(*transposed_grid)]
        #     # Update animation_moves and animation_merges

        # if moved:
        #     self._add_random_tile()
        
        # # For now, the animation details are placeholders
        # # A more robust way to get animation_moves and animation_merges is needed.
        # # This often involves comparing the grid before and after the slide/merge pass for each direction.
        # return moved, {}, set() # Placeholder for animation data

    def _process_row_left(self, line: list[int]) -> tuple[list[int], dict[int, int], dict[int, int], int]:
        """
        Processes a single row for a left move:
            slides tiles, merges, and returns the new line.

        Returns: (new_line, slides_map, merges_map, score_delta)
        """
        # TODO: quite messy, refactor

        # Store (value, original_index) for tiles that are not empty
        tiles_with_original_indices = []
        for i, val in enumerate(line):
            if val != self.EMPTY_CELL_CONTENT:
                tiles_with_original_indices.append((val, i))

        processed_line_values = [] 
        
        line_slides_map = {}  
        line_merges_map = {}  
        score_delta = 0
        
        i = 0
        current_new_idx = 0 
        
        while i < len(tiles_with_original_indices):
            val1, orig_idx1 = tiles_with_original_indices[i]
            
            if i + 1 < len(tiles_with_original_indices) and tiles_with_original_indices[i+1][0] == val1:
                _, orig_idx2 = tiles_with_original_indices[i+1]

                merged_val = val1 * 2
                score_delta += merged_val
                processed_line_values.append(merged_val)
                
                line_slides_map[orig_idx1] = current_new_idx
                line_slides_map[orig_idx2] = current_new_idx
                line_merges_map[current_new_idx] = merged_val
                
                i += 2
            else:
                processed_line_values.append(val1)
                if orig_idx1 != current_new_idx: # Record if it actually moved
                    line_slides_map[orig_idx1] = current_new_idx

                i += 1
            current_new_idx += 1

        # Rebuild the line for the grid
        processed_line_values += [self.EMPTY_CELL_CONTENT] * (self.size - len(processed_line_values))

        return processed_line_values, line_slides_map, line_merges_map, score_delta

    def check_game_over(self) -> bool:
        """ Checks if there are any possible moves left. """
        if self._get_empty_cells():
            return False # Can still add tiles or move into empty spaces

        for r in range(self.size):
            for c in range(self.size):
                val = self.grid[r][c]
                if val == self.EMPTY_CELL_CONTENT: # Should not happen if _get_empty_cells is false, but good check
                    return False
                # Check right
                if c + 1 < self.size and self.grid[r][c+1] == val:
                    return False
                # Check down
                if r + 1 < self.size and self.grid[r+1][c] == val:
                    return False
        # self.game_over = True # Game.move will set this if applicable
        return True

# Example usage (for testing, can be removed later)
if __name__ == '__main__':
    game = Game()
    print("Initial Grid:")
    game._add_random_tile()
    print(game)

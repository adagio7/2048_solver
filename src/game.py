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

    def _process_row_left(self, row: list[int]):
        """
        Processes a single row for a left move: slides tiles, merges, and returns the new row.
        This is a simplified version. For animation, we'd need to track original positions.
        Returns: (new_row, moves_in_row, merges_in_row)
        """
        # # 1. Compact (remove zeros)
        # compacted_row = [val for val in row if val != 0]
        
        # # 2. Merge
        # merged_row = []
        # merges_occurred_indices = set() # Indices in merged_row
        # i = 0
        # while i < len(compacted_row):
        #     if i + 1 < len(compacted_row) and compacted_row[i] == compacted_row[i+1]:
        #         merged_value = compacted_row[i] * 2
        #         merged_row.append(merged_value)
        #         self.score += merged_value
        #         merges_occurred_indices.add(len(merged_row) - 1)
        #         i += 2 # Skip next element as it's merged
        #     else:
        #         merged_row.append(compacted_row[i])
        #         i += 1
        
        # # 3. Pad with zeros
        # final_row = merged_row + [0] * (self.size - len(merged_row))
        
        # # For detailed animation, we'd compare `row` with `final_row`
        # # and trace back where each tile came from and where merges happened.
        # # This is non-trivial.
        
        # # Placeholder for detailed move/merge tracking for animation
        # animation_row_moves = {} 
        # animation_row_merges = set()

        # return final_row, animation_row_moves, animation_row_merges

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

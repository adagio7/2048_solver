from random import choice, random

from ..constants import GRID_SIZE
from ..models import Moves, Grid, Row, Coords, AnimationSlides, AnimationMerges


class Game:
    SPAWN_2_PROB = 0.9
    EMPTY_CELL_CONTENT = 0

    def __init__(self, size: int = GRID_SIZE):
        self.size = size
        self.grid: Grid = [[self.EMPTY_CELL_CONTENT] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False

        # Initialize the grid with two random tiles
        self._add_random_tile()
        self._add_random_tile()

    def _get_empty_cells(self) -> list[Coords]:
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

        (r, c) = choice(empty_cells)
        self.grid[r][c] = 2 if random() < self.SPAWN_2_PROB else 4

        return True

    def __str__(self) -> str:
        """ For debugging purposes """
        return '\n'.join(['\t'.join(map(str, row)) for row in self.grid])


    def move(self, direction: Moves) -> tuple[bool, AnimationSlides, AnimationMerges, int]:
        """
        Handles a move in the specified direction ('left', 'right', 'up', 'down').
        Returns a tuple: (moved: bool, animation_moves: dict, animation_merges: dict, score_delta: int)
        animation_moves: dict mapping (old_r, old_c) to (new_r, new_c)
        animation_merges: dict mapping (r,c) to merged value
        """
        animation_moves = {}
        animation_merges = {}
        moved = False
        score_delta = 0

        match direction:
            case Moves.LEFT:
                for r in range(self.size):
                    new_row, slides_map, merges_map, row_score_delta = self._process_row_left(self.grid[r])
                    if self.grid[r] != new_row:
                        moved = True
                    
                    # Update animation data
                    for old_c, new_c in slides_map.items():
                        animation_moves[(r, old_c)] = (r, new_c)

                    for merge_c, merge_val in merges_map.items():
                        animation_merges[(r, merge_c)] = merge_val
                        
                    self.grid[r] = new_row
                    score_delta += row_score_delta

            case Moves.RIGHT:
                for r in range(self.size):
                    # Reverse the row, process as left, then reverse back
                    original_row = self.grid[r][:]
                    reversed_row = original_row[::-1]
                    processed_reversed_row, slides_map, merges_map, row_score_delta = self._process_row_left(reversed_row)
                    new_row = processed_reversed_row[::-1]
                    
                    if original_row != new_row:
                        moved = True
                        
                    # Update animation data with adjusted indexes for right direction
                    for old_c, new_c in slides_map.items():
                        adjusted_old_c = self.size - 1 - old_c
                        adjusted_new_c = self.size - 1 - new_c
                        animation_moves[(r, adjusted_old_c)] = (r, adjusted_new_c)
                        
                    for merge_c, merge_val in merges_map.items():
                        adjusted_merge_c = self.size - 1 - merge_c
                        animation_merges[(r, adjusted_merge_c)] = merge_val
                        
                    self.grid[r] = new_row
                    score_delta += row_score_delta

            case Moves.UP:
                # Transpose grid, process each column as a row, then transpose back
                transposed_grid = [list(col) for col in zip(*self.grid)]
                for c in range(self.size):
                    original_col_as_row = transposed_grid[c][:]
                    processed_col_as_row, slides_map, merges_map, row_score_delta = self._process_row_left(original_col_as_row)
                    
                    if original_col_as_row != processed_col_as_row:
                        moved = True
                        
                    # Update animation data with adjusted indexes for up direction
                    for old_r, new_r in slides_map.items():
                        animation_moves[(old_r, c)] = (new_r, c)
                        
                    for merge_r, merge_val in merges_map.items():
                        animation_merges[(merge_r, c)] = merge_val
                        
                    transposed_grid[c] = processed_col_as_row
                    score_delta += row_score_delta
                    
                self.grid = [list(row) for row in zip(*transposed_grid)]

            case Moves.DOWN:
                # Transpose grid, reverse rows, process as left, reverse back, transpose back
                transposed_grid = [list(col) for col in zip(*self.grid)]
                for c in range(self.size):
                    original_col_as_row = transposed_grid[c][:]
                    reversed_col_as_row = original_col_as_row[::-1]
                    processed_reversed_col, slides_map, merges_map, row_score_delta = self._process_row_left(reversed_col_as_row)
                    transposed_grid[c] = processed_reversed_col[::-1]
                    
                    if original_col_as_row != transposed_grid[c]:
                        moved = True
                        
                    # Update animation data with adjusted indexes for down direction
                    for old_r, new_r in slides_map.items():
                        # Adjust row indexes since we reversed
                        adjusted_old_r = self.size - 1 - old_r
                        adjusted_new_r = self.size - 1 - new_r
                        animation_moves[(adjusted_old_r, c)] = (adjusted_new_r, c)
                        
                    for merge_r, merge_val in merges_map.items():
                        adjusted_merge_r = self.size - 1 - merge_r
                        animation_merges[(adjusted_merge_r, c)] = merge_val
                        
                    score_delta += row_score_delta
                
                self.grid = [list(row) for row in zip(*transposed_grid)]

        if moved:
            self._add_random_tile()
            self.score += score_delta
            
        return moved, animation_moves, animation_merges, score_delta

    def _process_row_left(self, line: Row)-> tuple[Row, dict[int, int], dict[int, int], int]:
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

    def clone(self) -> 'Game':
        """
        Returns a deep copy of the current game state.
        Useful for solvers to evaluate different game states without modifying the original.

        :return: A new Game instance with the same state and score
        """
        new_game = Game(self.size)
        new_game.grid = [row[:] for row in self.grid]
        new_game.score = self.score
        new_game.game_over = self.game_over
        return new_game

import pytest
from src.game import Game, Moves
from src.constants import GRID_SIZE

# Make sure constants.py has GRID_SIZE defined, e.g., GRID_SIZE = 4

class TestGameLogic:

    def test_process_row_left_no_move(self):
        # Given
        game = Game(size=4)
        line = [2, 4, 8, 16]
        expected_line = [2, 4, 8, 16]

        # When
        processed_line, slides, merges = game._process_row_left(list(line))

        # Then
        assert processed_line == expected_line
        assert not slides  # No slides
        assert not merges  # No merges
        assert game.score == 0  # No score change

    def test_process_row_left_simple_slide(self):
        # Given
        game = Game(size=4)
        line = [0, 2, 0, 4]
        expected_line = [2, 4, 0, 0]
        expected_slides = {1: 0, 3: 1}

        # When
        processed_line, slides, merges = game._process_row_left(list(line))

        # Then
        assert processed_line == expected_line
        assert slides == expected_slides
        assert not merges

    # def test_process_row_left_slide_with_gap_at_end(self):
    #     game = Game(size=4)
    #     line = [2,0,0,0]
    #     expected_line = [2,0,0,0]
    #     expected_slides = {} # No actual slide if it starts at the leftmost available spot
    #     processed_line, slides, merges, score_delta = game._process_row_left(list(line))
    #     assert processed_line == expected_line
    #     assert slides == expected_slides
    #     assert not merges
    #     assert score_delta == 0

    # def test_process_row_left_slide_all_to_left(self):
    #     game = Game(size=4)
    #     line = [0,0,0,2]
    #     expected_line = [2,0,0,0]
    #     expected_slides = {3:0}
    #     processed_line, slides, merges, score_delta = game._process_row_left(list(line))
    #     assert processed_line == expected_line
    #     assert slides == expected_slides
    #     assert not merges
    #     assert score_delta == 0


    # def test_process_row_left_simple_merge(self):
    #     game = Game(size=4)
    #     line = [2, 2, 0, 0]
    #     expected_line = [4, 0, 0, 0]
    #     # Original: 2 at 0, 2 at 1
    #     # New: 4 at 0
    #     expected_slides = {0: 0, 1: 0} # Both original 2s slide to index 0
    #     expected_merges = {0: 4}      # Merge result 4 is at index 0
    #     processed_line, slides, merges, score_delta = game._process_row_left(list(line))
    #     assert processed_line == expected_line
    #     assert slides == expected_slides
    #     assert merges == expected_merges
    #     assert score_delta == 4

    # def test_process_row_left_merge_with_slide(self):
    #     game = Game(size=4)
    #     line = [0, 2, 2, 0]
    #     expected_line = [4, 0, 0, 0]
    #     # Original: 2 at 1, 2 at 2
    #     # New: 4 at 0
    #     expected_slides = {1: 0, 2: 0}
    #     expected_merges = {0: 4}
    #     processed_line, slides, merges, score_delta = game._process_row_left(list(line))
    #     assert processed_line == expected_line
    #     assert slides == expected_slides
    #     assert merges == expected_merges
    #     assert score_delta == 4

    # def test_process_row_left_multiple_merges(self):
    #     game = Game(size=4)
    #     line = [2, 2, 4, 4]
    #     expected_line = [4, 8, 0, 0]
    #     # Merge 1: 2s at 0,1 -> 4 at 0. Slides: {0:0, 1:0}. Merges: {0:4}
    #     # Merge 2: 4s at 2,3 -> 8 at 1. Slides: {2:1, 3:1}. Merges: {1:8}
    #     expected_slides = {0: 0, 1: 0, 2: 1, 3: 1}
    #     expected_merges = {0: 4, 1: 8}
    #     processed_line, slides, merges, score_delta = game._process_row_left(list(line))
    #     assert processed_line == expected_line
    #     assert slides == expected_slides
    #     assert merges == expected_merges
    #     assert score_delta == (4 + 8)

    # def test_process_row_left_cannot_merge_three(self):
    #     game = Game(size=4)
    #     line = [2, 2, 2, 0]
    #     expected_line = [4, 2, 0, 0]
    #     # Merge: 2s at 0,1 -> 4 at 0. Slides: {0:0, 1:0}. Merges: {0:4}
    #     # Slide: 2 at 2 -> 2 at 1. Slides: {2:1}
    #     expected_slides = {0: 0, 1: 0, 2: 1}
    #     expected_merges = {0: 4}
    #     processed_line, slides, merges, score_delta = game._process_row_left(list(line))
    #     assert processed_line == expected_line
    #     assert slides == expected_slides
    #     assert merges == expected_merges
    #     assert score_delta == 4
        
    # def test_process_row_left_complex_case(self):
    #     game = Game(size=4)
    #     line = [0, 2, 2, 4, 0, 4, 8, 8] # Assuming size 8 for this test line
    #     game_temp = Game(size=8) # Create a temp game with larger size for this line
    #     expected_line = [4, 8, 16, 0, 0, 0, 0, 0]
    #     # (0,2,2,4,0,4,8,8)
    #     # Tiles with original indices: (2,1), (2,2), (4,3), (4,5), (8,6), (8,7)
    #     # Merge (2,1) (2,2) -> (4,0). Slides: {1:0, 2:0}. Merges: {0:4}
    #     # Next is (4,3). It cannot merge with (4,0). So (4,3) slides to 1. Slides: {3:1}
    #     # Next is (4,5). It merges with (4,3) which is now at index 1. (4,5) and (4,3) -> (8,1). Slides: {3:1 (already there), 5:1}. Merges: {1:8}
    #     # This interpretation is tricky. The rule is usually sequential.
    #     # Let's re-evaluate based on standard 2048:
    #     # [0, 2, 2, 4, 0, 4, 8, 8]
    #     # Compacted: [(2,1), (2,2), (4,3), (4,5), (8,6), (8,7)]
    #     # 1. (2,1) and (2,2) merge -> 4 at new_idx 0. Slides: {1:0, 2:0}. Merges: {0:4}. Score += 4
    #     #    processed_line_values: [(4, [1,2])]
    #     # 2. Next non-merged is (4,3). It cannot merge with the 4 at new_idx 0. So (4,3) slides to new_idx 1. Slides: {3:1}.
    #     #    processed_line_values: [(4, [1,2]), (4, [3])]
    #     # 3. Next non-merged is (4,5). It cannot merge with (4,3) at new_idx 1. So (4,5) slides to new_idx 2. Slides: {5:2}.
    #     #    processed_line_values: [(4, [1,2]), (4, [3]), (4, [5])]
    #     # 4. Next non-merged is (8,6) and (8,7). They merge -> 16 at new_idx 3. Slides: {6:3, 7:3}. Merges: {3:16}. Score += 16
    #     #    processed_line_values: [(4, [1,2]), (4, [3]), (4, [5]), (16, [6,7])]
    #     # Expected line: [4, 4, 4, 16, 0, 0, 0, 0]
    #     # Expected slides: {1:0, 2:0, 3:1, 5:2, 6:3, 7:3}
    #     # Expected merges: {0:4, 3:16}
    #     # Score: 20

    #     expected_line_actual = [4, 4, 4, 16, 0, 0, 0, 0]
    #     expected_slides_actual = {1:0, 2:0, 3:1, 5:2, 6:3, 7:3}
    #     expected_merges_actual = {0:4, 3:16}
    #     score_delta_actual = 20

    #     processed_line, slides, merges, score_delta = game_temp._process_row_left(list(line))
    #     assert processed_line == expected_line_actual
    #     assert slides == expected_slides_actual
    #     assert merges == expected_merges_actual
    #     assert score_delta == score_delta_actual

    # def test_move_left_simple(self):
    #     game = Game(size=4)
    #     game.grid = [
    #         [2, 2, 0, 0],
    #         [0, 0, 0, 0],
    #         [0, 0, 0, 0],
    #         [0, 0, 0, 0]
    #     ]
    #     game.score = 0
        
    #     moved, g_before, g_after_no_new, slides, merges = game.move(Moves.LEFT)
        
    #     assert moved is True
    #     assert game.grid[0][0] == 4 # Merged tile
    #     assert game.score == 4
    #     assert slides == {(0,0): (0,0), (0,1): (0,0)} # Original (0,0) and (0,1) both move to (0,0)
    #     assert merges == {(0,0)} # Merge occurred at (0,0)
    #     # A new tile should have been added
    #     assert sum(1 for r in game.grid for tile in r if tile != 0) == 2 # 1 merged + 1 new tile

    # def test_move_right_simple_merge(self):
    #     game = Game(size=4)
    #     game.grid = [
    #         [0, 0, 2, 2],
    #         [0, 0, 0, 0],
    #         [0, 0, 0, 0],
    #         [0, 0, 0, 0]
    #     ]
    #     game.score = 0
    #     moved, _, _, slides, merges = game.move(Moves.RIGHT)
    #     assert moved is True
    #     assert game.grid[0][3] == 4
    #     assert game.score == 4
    #     # Original (0,2) and (0,3) both move to (0,3)
    #     assert slides == {(0,2):(0,3), (0,3):(0,3)}
    #     assert merges == {(0,3)}
    #     assert sum(1 for r in game.grid for tile in r if tile != 0) == 2

    # def test_move_up_simple_merge(self):
    #     game = Game(size=4)
    #     game.grid = [
    #         [2, 0, 0, 0],
    #         [2, 0, 0, 0],
    #         [0, 0, 0, 0],
    #         [0, 0, 0, 0]
    #     ]
    #     game.score = 0
    #     moved, _, _, slides, merges = game.move(Moves.UP)
    #     assert moved is True
    #     assert game.grid[0][0] == 4
    #     assert game.score == 4
    #     # Original (0,0) and (1,0) both move to (0,0)
    #     assert slides == {(0,0):(0,0), (1,0):(0,0)}
    #     assert merges == {(0,0)}
    #     assert sum(1 for r in game.grid for tile in r if tile != 0) == 2

    # def test_move_down_simple_merge(self):
    #     game = Game(size=4)
    #     game.grid = [
    #         [0, 0, 0, 0],
    #         [0, 0, 0, 0],
    #         [2, 0, 0, 0],
    #         [2, 0, 0, 0]
    #     ]
    #     game.score = 0
    #     moved, _, _, slides, merges = game.move(Moves.DOWN)
    #     assert moved is True
    #     assert game.grid[3][0] == 4
    #     assert game.score == 4
    #     # Original (2,0) and (3,0) both move to (3,0)
    #     assert slides == {(2,0):(3,0), (3,0):(3,0)}
    #     assert merges == {(3,0)}
    #     assert sum(1 for r in game.grid for tile in r if tile != 0) == 2

    # def test_no_move_possible(self):
    #     game = Game(size=2)
    #     game.grid = [
    #         [2, 4],
    #         [4, 2]
    #     ]
    #     game.score = 0
    #     # Mock _add_random_tile to prevent it from running if no move is made
    #     # or ensure game over check is robust
        
    #     moved, _, _, _, _ = game.move(Moves.LEFT)
    #     assert moved is False
    #     assert game.grid == [[2,4],[4,2]] # Grid unchanged
    #     assert game.score == 0
        
    #     moved, _, _, _, _ = game.move(Moves.UP)
    #     assert moved is False
    #     assert game.grid == [[2,4],[4,2]]
    #     assert game.score == 0
    #     assert game.game_over is True # Should be game over

    # def test_game_over_full_board_no_merges(self):
    #     game = Game(size=2)
    #     game.grid = [
    #         [2, 4],
    #         [8, 16]
    #     ]
    #     # Manually prevent adding new tiles for this specific test state
    #     original_add_tile = game._add_random_tile
    #     game._add_random_tile = lambda: False 

    #     moved, _, _, _, _ = game.move(Moves.LEFT) # Try a move
    #     assert moved is False
    #     assert game.game_over is True # Game should be over
    #     game._add_random_tile = original_add_tile # Restore

    # def test_add_tile_updates_grid(self):
    #     game = Game(size=2)
    #     game.grid = [
    #         [2, 0],
    #         [0, 0]
    #     ]
    #     empty_before = game._get_empty_cells()
    #     game._add_random_tile()
    #     empty_after = game._get_empty_cells()
    #     assert len(empty_after) == len(empty_before) - 1

    # def test_initial_tiles(self):
    #     game = Game(size=4)
    #     tile_count = sum(1 for row in game.grid for cell in row if cell != 0)
    #     assert tile_count == 2 # Game starts with two tiles

    # def test_move_updates_score(self):
    #     game = Game(size=4)
    #     game.grid = [[2,2,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    #     game.score = 0
    #     game.move(Moves.LEFT)
    #     assert game.score == 4


    # def test_full_slide_no_merge(self):
    #     game = Game(size=4)
    #     line = [0,0,2,4]
    #     expected_line = [2,4,0,0]
    #     expected_slides = {2:0, 3:1}
    #     processed_line, slides, merges, score_delta = game._process_row_left(list(line))
    #     assert processed_line == expected_line
    #     assert slides == expected_slides
    #     assert not merges
    #     assert score_delta == 0

    # def test_slide_into_existing_no_merge(self):
    #     game = Game(size=4)
    #     line = [2,0,4,0]
    #     expected_line = [2,4,0,0]
    #     expected_slides = {2:1} # only the 4 at index 2 slides to index 1
    #     processed_line, slides, merges, score_delta = game._process_row_left(list(line))
    #     assert processed_line == expected_line
    #     assert slides == expected_slides
    #     assert not merges
    #     assert score_delta == 0

    # def test_process_row_left_empty_line(self):
    #     game = Game(size=4)
    #     line = [0, 0, 0, 0]
    #     expected_line = [0, 0, 0, 0]
    #     processed_line, slides, merges, score_delta = game._process_row_left(list(line))
    #     assert processed_line == expected_line
    #     assert not slides
    #     assert not merges
    #     assert score_delta == 0

    # def test_process_row_left_full_line_no_merges(self):
    #     game = Game(size=4)
    #     line = [2, 4, 8, 16]
    #     expected_line = [2, 4, 8, 16]
    #     processed_line, slides, merges, score_delta = game._process_row_left(list(line))
    #     assert processed_line == expected_line
    #     assert not slides
    #     assert not merges
    #     assert score_delta == 0
        
    # def test_move_complex_scenario_animation_data(self):
    #     game = Game(size=4)
    #     # Setup a specific grid state
    #     game.grid = [
    #         [0, 2, 2, 4],  # Row 0: merge (2,2)->4 at (0,0), 4 slides to (0,1)
    #         [0, 0, 0, 0],
    #         [4, 0, 4, 2],  # Row 2: merge (4,4)->8 at (2,0), 2 slides to (2,1)
    #         [2, 2, 2, 2]   # Row 3: merge (2,2)->4 at (3,0), merge (2,2)->4 at (3,1)
    #     ]
    #     game.score = 0
    #     # Prevent new tiles from being added to isolate move logic
    #     original_add_tile = game._add_random_tile
    #     game._add_random_tile = lambda: True 

    #     moved, g_before, g_after_no_new, slides, merges = game.move(Moves.LEFT)

    #     game._add_random_tile = original_add_tile # Restore

    #     assert moved is True

    #     # Expected grid after moves (before new tile)
    #     expected_grid_after_moves = [
    #         [4, 4, 0, 0],
    #         [0, 0, 0, 0],
    #         [8, 2, 0, 0],
    #         [4, 4, 0, 0]
    #     ]
    #     assert g_after_no_new == expected_grid_after_moves
    #     assert game.score == (4+4+8+4+4) # (2+2) + 4 (slide) + (4+4) + 2 (slide) + (2+2) + (2+2)

    #     # Expected slides: {(old_r, old_c): (new_r, new_c)}
    #     expected_slides = {
    #         (0,1):(0,0), (0,2):(0,0), # First 2,2 merge to 4 at (0,0)
    #         (0,3):(0,1),             # 4 slides to (0,1)
    #         (2,0):(2,0), (2,2):(2,0), # 4,4 merge to 8 at (2,0)
    #         (2,3):(2,1),             # 2 slides to (2,1)
    #         (3,0):(3,0), (3,1):(3,0), # First 2,2 merge to 4 at (3,0)
    #         (3,2):(3,1), (3,3):(3,1)  # Second 2,2 merge to 4 at (3,1)
    #     }
    #     assert slides == expected_slides

    #     # Expected merges: set of (r,c) where merge occurred
    #     expected_merges = {
    #         (0,0), # 2+2=4
    #         (2,0), # 4+4=8
    #         (3,0), # 2+2=4
    #         (3,1)  # 2+2=4
    #     }
    #     assert merges == expected_merges

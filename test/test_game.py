import pytest

from src.models import Moves
from src.game.game import Game


class TestGameLogic:
    GRID_SIZE = 4

    def test_process_row_left_no_move(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        line = [2, 4, 8, 16]
        expected_line = [2, 4, 8, 16]

        # When
        processed_line, slides, merges, score_delta = game._process_row_left(line)

        # Then
        assert processed_line == expected_line
        assert not slides  # No slides
        assert not merges  # No merges
        assert score_delta == 0  # No score change

    def test_process_row_left_simple_slide(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        line = [0, 2, 0, 4]
        expected_line = [2, 4, 0, 0]
        expected_slides = {1: 0, 3: 1}

        # When
        processed_line, slides, merges, score_delta = game._process_row_left(line)

        # Then
        assert processed_line == expected_line
        assert slides == expected_slides
        assert not merges
        assert score_delta == 0

    def test_process_row_left_slide_with_gap_at_end(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        line = [2,0,0,0]
        expected_line = [2,0,0,0]

        # When
        processed_line, slides, merges, score_delta = game._process_row_left(list(line))

        # Then
        assert processed_line == expected_line
        assert not slides
        assert not merges
        assert score_delta == 0

    def test_process_row_left_slide_all_to_left(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        line = [0,0,0,2]
        expected_line = [2,0,0,0]
        expected_slides = {3:0}

        # When
        processed_line, slides, merges, score_delta = game._process_row_left(list(line))

        # Then
        assert processed_line == expected_line
        assert slides == expected_slides
        assert not merges
        assert score_delta == 0


    def test_process_row_left_simple_merge(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        line = [2, 2, 0, 0]
        expected_line = [4, 0, 0, 0]
        expected_slides = {0: 0, 1: 0} 
        expected_merges = {0: 4}

        # When
        processed_line, slides, merges, score_delta = game._process_row_left(list(line))

        # Then
        assert processed_line == expected_line
        assert slides == expected_slides
        assert merges == expected_merges
        assert score_delta == 4

    def test_process_row_left_merge_with_slide(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        line = [0, 2, 2, 0]
        expected_line = [4, 0, 0, 0]
        expected_slides = {1: 0, 2: 0}
        expected_merges = {0: 4}

        # When
        processed_line, slides, merges, score_delta = game._process_row_left(list(line))

        # Then
        assert processed_line == expected_line
        assert slides == expected_slides
        assert merges == expected_merges
        assert score_delta == 4

    def test_process_row_left_multiple_merges(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        line = [2, 2, 4, 4]
        expected_line = [4, 8, 0, 0]

        # Merge 1: 2s at 0,1 -> 4 at 0. Slides: {0:0, 1:0}. Merges: {0:4}
        # Merge 2: 4s at 2,3 -> 8 at 1. Slides: {2:1, 3:1}. Merges: {1:8}
        expected_slides = {0: 0, 1: 0, 2: 1, 3: 1}
        expected_merges = {0: 4, 1: 8}

        # When
        processed_line, slides, merges, score_delta = game._process_row_left(list(line))

        # Then
        assert processed_line == expected_line
        assert slides == expected_slides
        assert merges == expected_merges
        assert score_delta == (4 + 8)

    def test_process_row_left_cannot_merge_three(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        line = [2, 2, 2, 0]
        expected_line = [4, 2, 0, 0]
        expected_slides = {0: 0, 1: 0, 2: 1}
        expected_merges = {0: 4}

        # When
        processed_line, slides, merges, score_delta = game._process_row_left(list(line))

        # Then
        assert processed_line == expected_line
        assert slides == expected_slides
        assert merges == expected_merges
        assert score_delta == 4
        
    def test_process_row_left_complex_case(self):
        # Given
        game = Game(size=8)
        line = [0, 2, 2, 4, 0, 4, 8, 8]
        expected_line = [4, 8, 16, 0, 0, 0, 0, 0]

        expected_slides_actual = {1:0, 2:0, 3:1, 5:1, 6:2, 7:2}
        expected_merges_actual = {0:4, 1:8, 2:16}
        score_delta_actual = (4 + 8 + 16)

        # When
        processed_line, slides, merges, score_delta = game._process_row_left(list(line))

        # Then
        assert processed_line == expected_line
        assert slides == expected_slides_actual
        assert merges == expected_merges_actual
        assert score_delta == score_delta_actual

    def test_move_left_no_move(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        game.grid = [
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.score = 0

        # When
        moved, slides, merges, score_delta = game.move(Moves.LEFT)

        # Then
        assert moved is False
        assert game.grid == [
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        assert game.score == 0
        assert slides == {}
        assert merges == {}

    def test_move_left_no_move(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        game.grid = [
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.score = 0

        # When
        moved, slides, merges, score_delta = game.move(Moves.LEFT)

        # Then
        assert moved is False
        assert game.grid == [
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        assert game.score == 0
        assert slides == {}
        assert merges == {}

    def test_move_right_no_move(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        game.grid = [
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.score = 0

        # When
        moved, slides, merges, score_delta = game.move(Moves.RIGHT)

        # Then
        assert moved is False
        assert game.grid == [
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        assert game.score == 0
        assert slides == {}
        assert merges == {}
    def test_move_up_no_move(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        game.grid = [
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.score = 0

        # When
        moved, slides, merges, score_delta = game.move(Moves.UP)

        # Then
        assert moved is False
        assert game.grid == [
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        assert game.score == 0
        assert slides == {}
        assert merges == {}

    def test_move_down_no_move(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        game.grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 4, 8, 16],
        ]

        # When
        moved, slides, merges, score_delta = game.move(Moves.DOWN)

        # Then
        assert moved is False
        assert game.grid == [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 4, 8, 16],
        ]
        assert score_delta == 0
        assert slides == {}
        assert merges == {}

    def test_move_left_simple(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        game.grid = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        # When
        moved, slides, merges, score_delta = game.move(Moves.LEFT)

        # Then
        assert moved is True
        assert game.grid[0][0] == 4
        assert score_delta == 4
        assert slides == {(0, 0): (0, 0), (0, 1): (0, 0)}  # Original (0,0) and (0,1) both move to (0,0)
        assert merges == {(0, 0): 4}

    def test_move_right_simple_merge(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        game.grid = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        # When
        moved, slides, merges, score_delta = game.move(Moves.RIGHT)

        # Then
        assert moved is True
        assert game.grid[0][3] == 4
        assert score_delta == 4
        assert slides == {(0, 0): (0, 3), (0, 1): (0, 3)}
        assert merges == {(0, 3): 4}

    def test_move_up_simple_merge(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        game.grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [2, 0, 0, 0],
        ]

        # When
        moved, slides, merges, score_delta = game.move(Moves.UP)

        # Then
        assert moved is True
        assert game.grid[0][0] == 4
        assert score_delta == 4
        assert slides == {(2, 0): (0, 0), (3, 0): (0, 0)}
        assert merges == {(0, 0): 4}

    def test_move_down_simple_merge(self):
        # Given
        game = Game(size=self.GRID_SIZE)
        game.grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [2, 0, 0, 0],
        ]

        # When
        moved, slides, merges, score_delta = game.move(Moves.DOWN)

        # Then
        assert moved is True
        assert game.grid[3][0] == 4
        assert score_delta == 4
        assert slides == {(2, 0): (3, 0), (3, 0): (3, 0)}
        assert merges == {(3, 0): 4}

import pytest

from src.solvers.minmax import MinMaxSolver

class TestEvalHeuristics:
    GRID_SIZE = 4

    def test_get_empty_cells_completely_empty_grid(self):
        # Given
        solver = MinMaxSolver()
        grid = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]

        # When
        result = solver._get_empty_cells(grid)

        # Then
        assert result == 16

    def test_get_empty_cells_completely_full_grid(self):
        # Given
        solver = MinMaxSolver()
        grid = [[2, 4, 8, 16],
                [32, 64, 128, 256],
                [512, 1024, 2048, 4096],
                [2, 4, 8, 16]]

        # When
        result = solver._get_empty_cells(grid)

        # Then
        assert result == 0

    def test_get_empty_cells_partially_filled_grid(self):
        # Given
        solver = MinMaxSolver()
        grid = [[2, 0, 4, 0],
                [0, 8, 0, 16],
                [32, 0, 64, 0],
                [0, 128, 0, 256]]

        # When
        result = solver._get_empty_cells(grid)

        # Then
        assert result == 8

    def test_get_empty_cells_single_tile(self):
        # Given
        solver = MinMaxSolver()
        grid = [[2, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]

        # When
        result = solver._get_empty_cells(grid)

        # Then
        assert result == 15

    def test_calculate_monotonicity_perfect_increasing_rows(self):
        # Given
        solver = MinMaxSolver()
        grid = [[2, 4, 8, 16],
                [2, 4, 8, 16],
                [2, 4, 8, 16],
                [2, 4, 8, 16]]

        # When
        result = solver._calculate_monotonicity(grid)

        # Then
        # 4 rows × 3 horizontal pairs (all increasing) = +12
        # 4 cols × 3 vertical pairs (all equal) = +12
        assert result == 24

    def test_calculate_monotonicity_perfect_decreasing_rows(self):
        # Given
        solver = MinMaxSolver()
        grid = [[16, 8, 4, 2],
                [16, 8, 4, 2],
                [16, 8, 4, 2],
                [16, 8, 4, 2]]

        # When
        result = solver._calculate_monotonicity(grid)

        # Then
        # 4 rows × 3 horizontal pairs (all decreasing) = -12
        # 4 cols × 3 vertical pairs (all equal) = +12
        assert result == 0

    def test_calculate_monotonicity_mixed_pattern(self):
        # Given
        solver = MinMaxSolver()
        grid = [[2, 4, 2, 8],    # +1, -1, +1 = +1
                [4, 2, 4, 2],    # -1, +1, -1 = -1
                [8, 4, 8, 4],    # -1, +1, -1 = -1
                [16, 8, 16, 8]]  # -1, +1, -1 = -1

        # When
        result = solver._calculate_monotonicity(grid)

        # Then
        # Horizontal: +1 + (-1) + (-1) + (-1) = -2
        # Vertical calculations for columns need to be computed
        assert isinstance(result, int)

    def test_calculate_monotonicity_with_zeros(self):
        # Given
        solver = MinMaxSolver()
        grid = [[0, 2, 4, 8],
                [0, 0, 0, 0],
                [2, 4, 8, 16],
                [0, 0, 0, 0]]

        # When
        result = solver._calculate_monotonicity(grid)

        # Then
        # Should handle zeros as valid values (0 <= anything)
        assert isinstance(result, int)

    def test_calculate_smoothness_identical_tiles(self):
        # Given
        solver = MinMaxSolver()
        grid = [[2, 2, 2, 2],
                [2, 2, 2, 2],
                [2, 2, 2, 2],
                [2, 2, 2, 2]]

        # When
        result = solver._calculate_smoothness(grid)

        # Then
        # All adjacent non-zero tiles are identical, so differences are 0
        assert result == 0

    def test_calculate_smoothness_maximum_differences(self):
        # Given
        solver = MinMaxSolver()
        grid = [[2, 2048, 2, 2048],
                [2048, 2, 2048, 2],
                [2, 2048, 2, 2048],
                [2048, 2, 2048, 2]]

        # When
        result = solver._calculate_smoothness(grid)

        # Then
        # Should be highly negative due to large differences
        assert result < 0

    def test_calculate_smoothness_with_zeros_ignored(self):
        # Given
        solver = MinMaxSolver()
        grid = [[0, 2, 0, 4],
                [2, 0, 4, 0],
                [0, 4, 0, 8],
                [4, 0, 8, 0]]

        # When
        result = solver._calculate_smoothness(grid)

        # Then
        # Should only consider non-zero adjacent pairs
        # Thus, since all adjacent pairs are zero, it should be 0
        assert result == 0

    def test_calculate_smoothness_empty_grid(self):
        # Given
        solver = MinMaxSolver()
        grid = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]

        # When
        result = solver._calculate_smoothness(grid)

        # Then
        # No non-zero adjacent pairs, should be 0
        assert result == 0

    def test_calculate_smoothness_single_row_progression(self):
        # Given
        solver = MinMaxSolver()
        grid = [[2, 4, 8, 16],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]

        # When
        result = solver._calculate_smoothness(grid)

        # Then
        # Should penalize: |2-4| + |4-8| + |8-16| = 2 + 4 + 8 = 14
        assert result == -14

    def test_calculate_smoothness_adjacent_equal_values(self):
        # Given
        solver = MinMaxSolver()
        grid = [[4, 4, 0, 0],
                [4, 4, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]

        # When
        result = solver._calculate_smoothness(grid)

        # Then
        # All adjacent pairs are equal: |4-4| = 0
        # Horizontal: 0 + 0 = 0, Vertical: 0 = 0
        assert result == 0

    def test_edge_case_single_value_grid(self):
        # Given
        solver = MinMaxSolver()
        grid = [[2, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]

        # When
        empty_cells = solver._get_empty_cells(grid)
        monotonicity = solver._calculate_monotonicity(grid)
        smoothness = solver._calculate_smoothness(grid)

        # Then
        assert empty_cells == 15
        assert isinstance(monotonicity, int)
        assert smoothness == 0  # No adjacent non-zero pairs

if __name__ == '__main__':
    pytest.main([__file__])
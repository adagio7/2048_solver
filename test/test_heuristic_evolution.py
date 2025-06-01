import pytest
import random
from unittest.mock import patch, MagicMock

from src.solvers.genetic import HeuristicEvolution
from src.models import Moves, Grid

class TestHeuristicEvolution:
    def test_initialize_population(self):
        # Given
        evolution = HeuristicEvolution(population_size=10)
        
        # When
        population = evolution._initialize_population()
        
        # Then
        assert len(population) == 10
        for individual in population:
            assert len(individual) == 5  # 5 weights
            # Check weight ranges
            assert 5.0 <= individual[0] <= 30.0   # empty_weight
            assert 10.0 <= individual[1] <= 50.0  # mono_weight
            assert 1.0 <= individual[2] <= 15.0   # smooth_weight
            assert 20.0 <= individual[3] <= 80.0  # corner_weight
            assert 1.0 <= individual[4] <= 10.0   # max_tile_weight

    def test_format_weights(self):
        # Given
        evolution = HeuristicEvolution()
        weights = [15.2, 25.8, 8.1, 45.3, 2.1]
        
        # When
        formatted = evolution._format_weights(weights)
        
        # Then
        expected = "Empty=15.2, Mono=25.8, Smooth=8.1, Corner=45.3, MaxTile=2.1"
        assert formatted == expected

    def test_get_empty_cells(self):
        # Given
        evolution = HeuristicEvolution()
        game_state = [
            [2, 4, 0, 0],
            [0, 8, 0, 0],
            [0, 0, 16, 0],
            [0, 0, 64, 32]
        ]
        
        # When
        empty_count = evolution._get_empty_cells(game_state)
        
        # Then
        assert empty_count == 10

    def test_get_empty_cells_full_grid(self):
        # Given
        evolution = HeuristicEvolution()
        game_state = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [2, 4, 8, 16]
        ]
        
        # When
        empty_count = evolution._get_empty_cells(game_state)
        
        # Then
        assert empty_count == 0

    def test_calculate_corner_bonus_max_in_corner(self):
        # Given
        evolution = HeuristicEvolution()
        game_state = [
            [2048, 4, 8, 16],  # Max value in top-left corner
            [32, 64, 128, 256],
            [512, 1024, 256, 128],
            [2, 4, 8, 16]
        ]
        
        # When
        bonus = evolution._calculate_corner_bonus(game_state)
        
        # Then
        assert bonus == 1.0

    def test_calculate_corner_bonus_max_not_in_corner(self):
        # Given
        evolution = HeuristicEvolution()
        game_state = [
            [2, 4, 8, 16],
            [32, 2048, 128, 256],  # Max value not in corner
            [512, 1024, 256, 128],
            [2, 4, 8, 16]
        ]
        
        # When
        bonus = evolution._calculate_corner_bonus(game_state)
        
        # Then
        assert bonus == 0.0

    def test_calculate_monotonicity_perfect_increasing(self):
        # Given
        evolution = HeuristicEvolution()
        game_state = [
            [2, 4, 8, 16],      # Perfectly increasing row
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        # When
        mono_score = evolution._calculate_monotonicity(game_state)
        
        # Then
        assert mono_score > 0  # Should be positive for monotonic sequence

    def test_calculate_smoothness_identical_values(self):
        # Given
        evolution = HeuristicEvolution()
        game_state = [
            [4, 4, 4, 4],   # Identical values = perfectly smooth
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        # When
        smooth_score = evolution._calculate_smoothness(game_state)
        
        # Then
        assert smooth_score == 0  # No differences = 0 penalty

    def test_calculate_smoothness_large_differences(self):
        # Given
        evolution = HeuristicEvolution()
        game_state = [
            [2, 2048, 2, 2048],  # Large differences
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        # When
        smooth_score = evolution._calculate_smoothness(game_state)
        
        # Then
        assert smooth_score < 0  # Should be negative (penalty)

    def test_evaluate_with_weights(self):
        # Given
        evolution = HeuristicEvolution()
        game_state = [
            [2, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        weights = [10.0, 5.0, 2.0, 50.0, 1.0]
        
        # When
        score = evolution._evaluate_with_weights(game_state, weights)
        
        # Then
        assert isinstance(score, float)
        assert score > 0  # Should be positive for reasonable weights

    def test_get_best_move_with_weights_returns_valid_move(self):
        # Given
        evolution = HeuristicEvolution()
        game_state = [
            [2, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        weights = [10.0, 5.0, 2.0, 50.0, 1.0]
        
        # When
        move = evolution._get_best_move_with_weights(game_state, weights)
        
        # Then
        assert move in list(Moves)

    def test_get_best_move_with_weights_no_valid_moves(self):
        # Given
        evolution = HeuristicEvolution()
        # Grid where no moves are possible
        game_state = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        weights = [10.0, 5.0, 2.0, 50.0, 1.0]
        
        # When
        with patch('random.choice') as mock_choice:
            mock_choice.return_value = Moves.UP
            move = evolution._get_best_move_with_weights(game_state, weights)
        
        # Then
        assert move in list(Moves)  # Should return random choice
        mock_choice.assert_called_once()

    def test_tournament_selection(self):
        # Given
        evolution = HeuristicEvolution()
        population = [
            [1.0, 2.0, 3.0, 4.0, 5.0],  # Individual 0
            [2.0, 3.0, 4.0, 5.0, 6.0],  # Individual 1
            [3.0, 4.0, 5.0, 6.0, 7.0],  # Individual 2
        ]
        fitness_scores = [10.0, 50.0, 30.0]  # Individual 1 has highest fitness
        
        # When
        with patch('random.sample', return_value=[0, 1, 2]):  # All compete
            selected = evolution._tournament_selection(population, fitness_scores, tournament_size=3)
        
        # Then
        assert selected == population[1]  # Should select individual with highest fitness

    def test_crossover(self):
        # Given
        evolution = HeuristicEvolution()
        parent1 = [1.0, 2.0, 3.0, 4.0, 5.0]
        parent2 = [6.0, 7.0, 8.0, 9.0, 10.0]
        
        # When
        with patch('random.randint', return_value=2):  # Crossover at position 2
            child1, child2 = evolution._crossover(parent1, parent2)
        
        # Then
        assert child1 == [1.0, 2.0, 8.0, 9.0, 10.0]  # parent1[:2] + parent2[2:]
        assert child2 == [6.0, 7.0, 3.0, 4.0, 5.0]   # parent2[:2] + parent1[2:]

    def test_mutate_no_mutation(self):
        # Given
        evolution = HeuristicEvolution()
        original = [10.0, 20.0, 30.0, 40.0, 50.0]
        
        # When (mock random to never trigger mutation)
        with patch('random.random', return_value=1.0):  # Always > mutation_rate
            mutated = evolution._mutate(original)
        
        # Then
        assert mutated == original
        assert mutated is not original  # Should be a copy

    def test_mutate_with_mutation(self):
        # Given
        evolution = HeuristicEvolution()
        original = [10.0, 20.0, 30.0, 40.0, 50.0]
        
        # When (mock random to always trigger mutation)
        with patch('random.random', return_value=0.0):  # Always < mutation_rate
            with patch('random.gauss', return_value=1.0):  # Always add 1.0
                mutated = evolution._mutate(original)
        
        # Then
        assert mutated != original
        for i in range(len(original)):
            assert mutated[i] >= 0.1  # Should be kept positive

    def test_mutate_keeps_weights_positive(self):
        # Given
        evolution = HeuristicEvolution()
        original = [0.5, 1.0, 2.0, 3.0, 4.0]  # Small values
        
        # When (add large negative noise)
        with patch('random.random', return_value=0.0):  # Always mutate
            with patch('random.gauss', return_value=-10.0):  # Large negative noise
                mutated = evolution._mutate(original)
        
        # Then
        for weight in mutated:
            assert weight >= 0.1  # All weights should be >= 0.1

    def test_evolve_population_maintains_size(self):
        # Given
        evolution = HeuristicEvolution(population_size=10)
        population = evolution._initialize_population()
        fitness_scores = [random.random() for _ in population]
        
        # When
        new_population = evolution._evolve_population(population, fitness_scores)
        
        # Then
        assert len(new_population) == evolution.population_size

    def test_evolve_population_preserves_elite(self):
        # Given
        evolution = HeuristicEvolution(population_size=10)
        population = [
            [1.0, 1.0, 1.0, 1.0, 1.0],  # Individual 0
            [2.0, 2.0, 2.0, 2.0, 2.0],  # Individual 1
            [3.0, 3.0, 3.0, 3.0, 3.0],  # Individual 2
            [4.0, 4.0, 4.0, 4.0, 4.0],  # Individual 3
            [5.0, 5.0, 5.0, 5.0, 5.0],  # Individual 4
        ] + [[0.0, 0.0, 0.0, 0.0, 0.0]] * 5  # Fill to size 10
        
        fitness_scores = [10.0, 50.0, 30.0, 40.0, 20.0] + [1.0] * 5  # Individual 1, 3, 2 are best
        
        # When
        new_population = evolution._evolve_population(population, fitness_scores)
        
        # Then
        # Best 3 individuals should be preserved
        assert [2.0, 2.0, 2.0, 2.0, 2.0] in new_population  # Highest fitness
        assert [4.0, 4.0, 4.0, 4.0, 4.0] in new_population  # Second highest
        assert [3.0, 3.0, 3.0, 3.0, 3.0] in new_population  # Third highest

    @patch('src.solvers.genetic.Game')
    def test_evaluate_fitness_plays_multiple_games(self, mock_game_class):
        # Given
        evolution = HeuristicEvolution()
        weights = [10.0, 5.0, 2.0, 50.0, 1.0]
        
        # Mock game to end immediately with score 1000
        mock_game = MagicMock()
        mock_game.check_game_over.return_value = True
        mock_game.score = 1000
        mock_game_class.return_value = mock_game
        
        # When
        fitness = evolution._evaluate_fitness(weights)
        
        # Then
        assert fitness == 1000.0  # Should return average score
        assert mock_game_class.call_count == 3  # Should play 3 games

    def test_evolve_weights_completes_successfully(self):
        # Given
        evolution = HeuristicEvolution(population_size=5, generations=2)  # Small for speed
        
        # When (mock fitness evaluation to return consistent scores)
        with patch.object(evolution, '_evaluate_fitness', return_value=1000.0):
            results = evolution.evolve_weights()
        
        # Then
        assert 'best_weights' in results
        assert 'best_fitness' in results
        assert 'fitness_history' in results
        assert 'weights_history' in results
        assert 'evolution_params' in results
        
        assert len(results['best_weights']) == 5
        assert results['best_fitness'] == 1000.0
        assert len(results['fitness_history']) == 2  # 2 generations
        assert len(evolution.evolution_history) == 2

    def test_evolve_weights_tracks_improvement(self):
        # Given
        evolution = HeuristicEvolution(population_size=5, generations=3)
        
        # Mock fitness to improve over time
        fitness_values = [100.0, 200.0, 300.0] * 10  # Repeat for all individuals
        
        # When
        with patch.object(evolution, '_evaluate_fitness', side_effect=fitness_values):
            results = evolution.evolve_weights()
        
        # Then
        fitness_history = results['fitness_history']
        assert len(fitness_history) == 3
        # Due to evolution, later generations should potentially have better fitness
        assert all(isinstance(f, (int, float)) for f in fitness_history)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
import random
import json

from typing import List, Tuple, Dict

from ..models import Moves, Grid
from ..game.game import Game


class HeuristicEvolution:
    """
    Tool to evolve optimal heuristic weights for 2048 solvers evaluation using genetic algorithms.
    """
    
    def __init__(
            self,
            population_size: int = 30,
            generations: int = 20,
            mutation_rate: float = 0.15,
            elite_size: int = 5
        ):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        
        # Results tracking
        self.evolution_history = []
        
    def evolve_weights(self) -> Dict:
        """
        Main evolution process to discover optimal evaluation weights.
        
        :param save_results: Whether to save results to file
        :return: Dictionary containing best weights and evolution statistics
        """
        # Initialize population
        population = self._initialize_population()
        best_fitness_history = []
        best_weights_history = []
        
        for generation in range(self.generations):
            print(f"\n Generation {generation+1}")
            # Evaluate fitness for all individuals
            fitness_scores = []
            for i, individual in enumerate(population):
                fitness = self._evaluate_fitness(individual)
                fitness_scores.append(fitness)
                if i % 10 == 0:  # Progress indicator
                    print(f"  Evaluated {i}/{len(population)} individuals...")
            
            # Track best
            best_fitness = max(fitness_scores)
            best_individual = population[fitness_scores.index(best_fitness)]
            best_fitness_history.append(best_fitness)
            best_weights_history.append(best_individual.copy())
            
            # Store generation data
            self.evolution_history.append({
                'generation': generation + 1,
                'best_fitness': best_fitness,
                'avg_fitness': sum(fitness_scores) / len(fitness_scores),
                'best_weights': best_individual.copy()
            })
            
            # Evolve new population (except last generation)
            if generation < self.generations - 1:
                population = self._evolve_population(population, fitness_scores)
        
        # Final results
        best_weights = best_weights_history[-1]
        results = {
            'best_weights': best_weights,
            'best_fitness': best_fitness_history[-1],
            'fitness_history': best_fitness_history,
            'weights_history': best_weights_history,
            'evolution_params': {
                'population_size': self.population_size,
                'generations': self.generations,
                'mutation_rate': self.mutation_rate
            },
        }
        
        print(f"Final best weights: {self._format_weights(best_weights)}")
        print(f"Final fitness: {best_fitness_history[-1]:.0f}")
        
        return results
    
    def _initialize_population(self) -> List[List[float]]:
        """Initialize population with random weights."""
        population = []
        for _ in range(self.population_size):
            # [empty_weight, mono_weight, smooth_weight, corner_weight, max_tile_weight]
            individual = [
                random.uniform(5.0, 30.0),   # empty_weight
                random.uniform(10.0, 50.0),  # mono_weight  
                random.uniform(1.0, 15.0),   # smooth_weight
                random.uniform(20.0, 80.0),  # corner_weight
                random.uniform(1.0, 10.0)    # max_tile_weight
            ]
            population.append(individual)
        return population
    
    def _evaluate_fitness(self, weights: List[float]) -> float:
        """Evaluate fitness by playing multiple games with these weights."""
        total_score = 0
        games_to_play = 3  # Balance between accuracy and speed
        
        for game_num in range(games_to_play):
            random.seed(42 + game_num)  # Consistent seeds for fair comparison
            
            game = Game()
            game._add_random_tile()
            game._add_random_tile()
            
            moves_made = 0
            max_moves = 1000  # Prevent infinite games
            
            while not game.check_game_over() and moves_made < max_moves:
                move = self._get_best_move_with_weights(game.grid, weights)
                if move:
                    moved, _, _, _ = game.move(move)
                    if moved:
                        game._add_random_tile()
                        moves_made += 1
                    else:
                        break
                else:
                    break
            
            total_score += game.score
        
        return total_score / games_to_play
    
    def _get_best_move_with_weights(self, game_state: Grid, weights: List[float]) -> Moves:
        """Simple greedy move selection using weights."""
        best_move = None
        best_score = float('-inf')
        
        for move in list(Moves):
            temp_game = Game()
            temp_game.grid = [row[:] for row in game_state]
            
            moved, _, _, _ = temp_game.move(move)
            if moved:
                score = self._evaluate_with_weights(temp_game.grid, weights)
                if score > best_score:
                    best_score = score
                    best_move = move
        
        return best_move if best_move else random.choice(list(Moves))
    
    def _evaluate_with_weights(self, game_state: Grid, weights: List[float]) -> float:
        """Evaluate position using given weights."""
        empty_value = self._get_empty_cells(game_state) * weights[0]
        mono_value = self._calculate_monotonicity(game_state) * weights[1]
        smooth_value = self._calculate_smoothness(game_state) * weights[2]
        corner_value = self._calculate_corner_bonus(game_state) * weights[3]
        max_tile_value = max(max(row) for row in game_state) * weights[4]
        
        return empty_value + mono_value + smooth_value + corner_value + max_tile_value
    
    def _evolve_population(self, population: List[List[float]], fitness_scores: List[float]) -> List[List[float]]:
        """Evolve population through selection, crossover, and mutation."""
        
        # Elite selection
        elite_indices = sorted(range(len(fitness_scores)), 
                             key=lambda i: fitness_scores[i], reverse=True)[:self.elite_size]
        new_population = [population[i] for i in elite_indices]
        
        # Generate offspring
        while len(new_population) < self.population_size:
            parent1 = self._tournament_selection(population, fitness_scores)
            parent2 = self._tournament_selection(population, fitness_scores)
            
            child1, child2 = self._crossover(parent1, parent2)
            
            child1 = self._mutate(child1)
            child2 = self._mutate(child2)
            
            new_population.extend([child1, child2])
        
        return new_population[:self.population_size]
    
    def _tournament_selection(self, population: List[List[float]], fitness_scores: List[float], tournament_size: int = 3) -> List[float]:
        """Tournament selection."""
        tournament_indices = random.sample(range(len(population)), min(tournament_size, len(population)))
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        winner_idx = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        return population[winner_idx]
    
    def _crossover(self, parent1: List[float], parent2: List[float]) -> Tuple[List[float], List[float]]:
        """Single-point crossover."""
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    
    def _mutate(self, individual: List[float]) -> List[float]:
        """Gaussian mutation."""
        mutated = individual.copy()
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                noise = random.gauss(0, 0.3 * abs(mutated[i]))
                mutated[i] += noise
                mutated[i] = max(0.1, mutated[i])
        return mutated

    def _format_weights(self, weights: List[float]) -> str:
        """Format weights for display."""
        labels = ['Empty', 'Mono', 'Smooth', 'Corner', 'MaxTile']
        return ', '.join([f'{label}={w:.1f}' for label, w in zip(labels, weights)])

    # Evaluation helper methods
    def _get_empty_cells(self, game_state: Grid) -> int:
        return sum(1 for row in game_state for cell in row if cell == 0)
    
    def _calculate_monotonicity(self, game_state: Grid) -> float:
        score = 0
        rows, cols = len(game_state), len(game_state[0])
        
        for r in range(rows):
            increasing = decreasing = 0
            for c in range(cols - 1):
                if game_state[r][c] <= game_state[r][c + 1]:
                    increasing += 1
                if game_state[r][c] >= game_state[r][c + 1]:
                    decreasing += 1
            score += max(increasing, decreasing)
        
        for c in range(cols):
            increasing = decreasing = 0
            for r in range(rows - 1):
                if game_state[r][c] <= game_state[r + 1][c]:
                    increasing += 1
                if game_state[r][c] >= game_state[r + 1][c]:
                    decreasing += 1
            score += max(increasing, decreasing)
        
        return score
    
    def _calculate_smoothness(self, game_state: Grid) -> float:
        score = 0
        rows, cols = len(game_state), len(game_state[0])
        
        for r in range(rows):
            for c in range(cols - 1):
                if game_state[r][c] != 0 and game_state[r][c + 1] != 0:
                    score -= abs(game_state[r][c] - game_state[r][c + 1])
        
        for c in range(cols):
            for r in range(rows - 1):
                if game_state[r][c] != 0 and game_state[r + 1][c] != 0:
                    score -= abs(game_state[r][c] - game_state[r + 1][c])
        
        return score
    
    def _calculate_corner_bonus(self, game_state: Grid) -> float:
        n = len(game_state)
        max_value = max(max(row) for row in game_state)
        corners = [game_state[0][0], game_state[0][n-1], 
                  game_state[n-1][0], game_state[n-1][n-1]]
        return 1.0 if max_value in corners else 0.0

if __name__ == "__main__":
    # Example usage
    evolution = HeuristicEvolution()
    results = evolution.evolve_weights()
    
    print("Best Weights:", results['best_weights'])
    print("Best Fitness:", results['best_fitness'])
    # print("Evolution History:", json.dumps(results, indent=2))
    
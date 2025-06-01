# 2048 Solvers

An implementation of the classic 2048 game featuring multiple (traditional) AI algorithms and a clean architecture that supports both human players and automated solvers.

## 🎯 Features

- **Interactive Gameplay**: Play 2048 with smooth keyboard (arrow keys) controls
- **Multiple AI Solvers**: Choose from various AI algorithms with different strategies
- **Clean Architecture**: Modular design using Strategy Pattern for easy extensibility
- **Heuristic Evolution**: Genetic algorithm for optimizing AI evaluation functions
- **Comprehensive Testing**: Unit tests for all major components

## 🎮 Solvers Available

### Human Player
Interactive gameplay with keyboard controls:
- **Arrow Keys**: Move tiles in respective directions
- **N**: Restart game

### AI Algorithms

#### 1. MinMax Solver
Uses adversarial search with alpha-beta pruning:
- Assumes worst-case tile placement by opponent
- Evaluates positions using multiple heuristics
- Configurable search depth

#### 2. Expectimax Solver  
Probabilistic approach modeling random tile placement:
- Models 90% probability for tile value 2, 10% for tile value 4
- Uses expected values instead of adversarial assumptions
- Better suited for stochastic environments

#### 3. Monte Carlo Tree Search (MCTS)
Advanced tree search with statistical sampling:
- UCB1 selection for exploration vs exploitation
- Random simulations for position evaluation
- Builds search tree incrementally
- Configurable simulation count

#### 4. Evolved Solver
Uses weights optimized by genetic algorithm:
- Pre-trained heuristic weights from evolutionary process
- Fast evaluation without search overhead
- Optimized for high-scoring games

#### 5. Random Solver
Baseline implementation for comparison:
- Makes random valid moves
- Useful for benchmarking other algorithms

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd 2048

# (Preffered) Add a virtual environment
python3 -m venv .venv

# Install dependencies
pip install -r requirements.txt
```

### Running the Game

Use the convenient shell scripts in the `scripts/` directory:

```bash
# Play as human
./scripts/run_human.sh

# Watch AI solvers
./scripts/run_minmax.sh
./scripts/run_expectimax.sh
./scripts/run_mcts.sh
./scripts/run_random.sh
```

#### Permission Issues
Note that to circumvent any permission related issues, add an executable permission on the file (e.g. `run_human.sh`)

```bash
chmod +x ./scripts/run_human.sh
```

### Training Heuristic Weights

Optimize AI evaluation functions using genetic algorithm:

```bash
# Use default parameters
./scripts/train_heuristic_weights.sh

# Custom parameters
python -m src.solvers.genetic --population-size 50 --generations 100 --mutation-rate 0.1
```

## Architecture

### Core Components

```
src/
├── game/             # Game logic and rendering
│   ├── game.py       # Core 2048 game mechanics
│   ├── controller.py # Game controller with Strategy Pattern
│   └── animator.py   # Visual rendering and animations
├── solvers/          # AI algorithms and human input
│   ├── solver.py     # Base solver interface
│   ├── human.py      # Human player input handler
│   ├── minmax.py     # MinMax with alpha-beta pruning
│   ├── expectimax.py # Expectimax algorithm
│   ├── mcts.py       # Monte Carlo Tree Search
│   ├── genetic.py    # Genetic algorithm for heuristic optimization
│   └── registry.py   # Solver registration system
└── models.py         # Shared data structures
```

### Design Patterns

- **Strategy Pattern**: Unified interface for different input sources (human/AI)
- **Observer Pattern**: Separation of game logic from rendering
- **Registry Pattern**: Solver registration and instantiation

## Heuristic Evolution

The genetic algorithm optimizes evaluation function weights through:

1. **Population**: Multiple sets of heuristic weights
2. **Fitness**: Average game score over multiple runs
3. **Selection**: Tournament selection of best performers
4. **Crossover**: Blend weights from successful individuals
5. **Mutation**: Random weight adjustments for exploration

### Evolved Heuristics

The system optimizes weights for:
- **Empty Tiles**: Favor boards with more free spaces
- **Monotonicity**: Prefer ordered tile arrangements
- **Smoothness**: Minimize value differences between adjacent tiles
- **Max Tile**: Reward achievement of high-value tiles

## Configuration

### Solver Parameters

Each solver can be customized:

```python
# MinMax depth
solver = MinMaxSolver(depth=4)

# MCTS simulations
solver = MCTSSolver(simulations=1000)

# Genetic algorithm parameters
python -m src.solvers.genetic \
  --population-size 100 \
  --generations 200 \
  --mutation-rate 0.15 \
  --elite-size 20
```

## Testing

Run the comprehensive test suite:

```bash
# All tests
python -m pytest test/

# Specific components
python -m pytest test/test_mcts.py
python -m pytest test/test_heuristic_evolution.py
```

### Test Coverage

- Game mechanics and board operations
- Solver algorithms and move generation
- MCTS tree operations and selection
- Genetic algorithm evolution process
- Heuristic evaluation functions

### Adding New Solvers

1. Inherit from `Solver` base class
2. Implement `get_move(game_state)` method
3. Include unit tests
4. Register in `registry.py` (using the `register` decorator)
5. Add corresponding run script

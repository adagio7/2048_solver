# 2048 Game

Python implementation of the 2048 game with support for humans and various solvers

## Design

The project follows a Model-View-Controller architecture

## System

### Model
Game Class (`game.py`): Represents the core game state and logic

- Manages the grid of tiles
- Implements the game rules for moving and merging tiles
- Tracks game score and detects game over conditions
- Returns animation data for rendering

### View
Rendering System:

- `GameController` contains drawing logic to render the board and tiles
- `Animator` (`animator.py`) handles visual transitions for slides and merges
- Uses pygame for rendering graphics
- Supports animations for tile movements and merges

### Controller
- GameController (`controller.py`): Coordinates gameplay
- Processes user input and translates to game actions
- Manages animation sequencing
- Handles game state transitions
- Controls game loop timing
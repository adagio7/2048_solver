import pygame
import random
import argparse

from .constants import *
from .game.controller import GameController
from .solvers.registry import SolverRegistry

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='2048 Game with different player options')
    solvers = SolverRegistry.list_solvers()
    
    # Add player type argument
    parser.add_argument(
        '--player', 
        type=str, 
        default='human',
        choices=solvers,
        help='Player type (default: human)'
    )
    
    parser.add_argument(
        '--seed', 
        type=int,
        help='Random seed for reproducibility'
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the 2048 game."""
    args = parse_arguments()
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    
    # Set random seed if provided
    if args.seed:
        random.seed(args.seed)
    
    solver = SolverRegistry.get_solver(args.player)()
    print(f"Using solver: {solver.name}")
    controller = GameController(screen, solver)

    # Run the game
    final_score = controller.run()
    
    print(f"Game over! Final score: {final_score}")
    pygame.quit()

if __name__ == "__main__":
    main()


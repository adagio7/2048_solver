import pygame

from .game import Game
from .animator import Animator
from ..constants import *
from ..models import Moves

class GameController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.game = Game()
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 48)
        
        # Initialize animator with required callbacks
        self.animator = Animator(
            draw_tile_fn=self._draw_tile,
            cell_center_fn=self._get_cell_center
        )
        
        # Animation state management
        self.game_over = False
        self.waiting_for_slides = False
        self.pending_merges = None
        self.ready_for_input = True
        
        # Timing
        self.last_time = pygame.time.get_ticks()
    
    def _get_cell_center(self, col: int, row: int) -> tuple[float, float]:
        """Calculate the center position of a cell."""
        x = BOARD_PADDING + col * (CELL_SIZE + CELL_PADDING) + CELL_SIZE // 2
        y = BOARD_PADDING + row * (CELL_SIZE + CELL_PADDING) + CELL_SIZE // 2
        return (x, y)
    
    def _draw_tile(self, value: int, center: tuple[float, float], scale: float = 1.0):
        """Draw a tile with the given value at the specified center position."""
        x, y = center
        # Scale the tile size
        size = int(CELL_SIZE * scale)
        # Calculate top-left position from center
        rect_x = x - size // 2
        rect_y = y - size // 2
        
        # Choose color based on value
        color = TILE_COLORS[value]
        
        # Draw the tile
        pygame.draw.rect(self.screen, color, (rect_x, rect_y, size, size), border_radius=10)
        
        # Draw the number
        text_color = Colours.DARK_TEXT if value <= 4 else Colours.LIGHT_TEXT
        text = self.font.render(str(value), True, text_color)
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)
    
    def handle_move(self, direction: Moves) -> bool:
        """Process a move and start appropriate animations."""
        if not self.ready_for_input or self.game_over:
            return False
            
        pre_move_grid = [row.copy() for row in self.game.grid]

        moved, animation_moves, animation_merges, score_delta = self.game.move(direction)
        
        if moved:
            # Start with slide animations
            self.animator.grid_snapshot = pre_move_grid
            self.ready_for_input = False
            self.animator.start_slide(self.game.grid, animation_moves)
            
            # Store merges for later after slides complete
            self.pending_merges = animation_merges
            self.waiting_for_slides = True
            
            # Check if game is over after the move
            self.game_over = self.game.check_game_over()
        
        self.ready_for_input = True
            
        return moved
    
    def handle_input(self) -> bool:
        """Handle keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                    
                # Only process move keys if we're ready
                if self.ready_for_input and not self.animator.is_animating:
                    match event.key:
                        case pygame.K_LEFT | pygame.K_a:
                            self.handle_move(Moves.LEFT)
                        case pygame.K_RIGHT | pygame.K_d:
                            self.handle_move(Moves.RIGHT)
                        case pygame.K_UP | pygame.K_w:
                            self.handle_move(Moves.UP)
                        case pygame.K_DOWN | pygame.K_s:
                            self.handle_move(Moves.DOWN)
                        case pygame.K_n:
                            # New game
                            self.game = Game()
                            self.game_over = False
                            self.ready_for_input = True
                        
        return True
    
    def update(self):
        """Update game state and animations."""
        # Calculate delta time
        current_time = pygame.time.get_ticks()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Update animator
        self.animator.update(dt)
        
        # Handle animation sequencing
        if self.waiting_for_slides and not self.animator.slides_running:
            # Slides finished, start pops if we have any
            if self.pending_merges:
                self.animator.start_pop(self.game.grid, self.pending_merges)
                self.pending_merges = None
                self.waiting_for_slides = False
                
        # Reset input state when all animations are done
        if not self.animator.is_animating:
            self.ready_for_input = True
            self.animator.grid_snapshot = None
    
    def draw(self):
        """Render the game board and UI."""
        # Clear the screen
        self.screen.fill(Colours.BOARD_BG_COLOUR)
        
        # Draw the empty board
        for i in range(self.game.size):
            for j in range(self.game.size):
                x = BOARD_PADDING + i * (CELL_SIZE + CELL_PADDING)
                y = BOARD_PADDING + j * (CELL_SIZE + CELL_PADDING)
                pygame.draw.rect(
                    self.screen, 
                    Colours.CELL_COLOUR, 
                    (x, y, CELL_SIZE, CELL_SIZE), 
                    border_radius=10
                )
        
        # Draw animated tiles
        if self.animator.is_animating:
            self.animator.draw(self.game.grid)
        else:
            # Draw static tiles when not animating
            for r in range(self.game.size):
                for c in range(self.game.size):
                    value = self.game.grid[r][c]
                    if value > 0:
                        self._draw_tile(value, self._get_cell_center(c, r))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.game.score}", True, Colours.DARK_TEXT)
        self.screen.blit(score_text, (20, HEIGHT - 40))
        
        # Draw game over message if game is over
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 180))
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = self.big_font.render("Game Over!", True, (119, 110, 101))
            restart_text = self.font.render("Press 'N' for new game", True, (119, 110, 101))
            
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            # Handle input
            running = self.handle_input()
            
            # Update game state
            self.update()
            
            # Render
            self.draw()
            
            # Cap the frame rate
            pygame.time.delay(16)  # ~60 FPS
        
        return self.game.score  # Return final score when game ends
        
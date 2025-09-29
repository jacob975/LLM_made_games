"""
Main Tower Defense Game class with ModernGL integration
"""

import pygame
import moderngl
import numpy as np
from config import *
from entities import Enemy, Tower
from game.game_map import GameMap
from game.ui import UI
from game.wave_manager import WaveManager
from utils.vector2d import Vector2D

class TowerDefenseGame:
    """Main game class that handles all game logic and rendering"""
    
    def __init__(self):
        print("Initializing Tower Defense Game...")
        
        # Initialize pygame first
        pygame.init()
        pygame.font.init()  # Ensure font system is ready
        
        print("Creating game display...")
        # Use regular pygame display mode for reliable rendering
        try:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Tower Defense Game")
            print("Display created successfully")
        except Exception as e:
            print(f"Error creating display: {e}")
            raise
        
        print("Setting up game components...")
        
        # Game components
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        
        try:
            # Game objects
            self.game_map = GameMap()
            print("Game map created")
            
            self.ui = UI()
            print("UI created")
            
            self.wave_manager = WaveManager(self.game_map.get_path_points())
            print("Wave manager created")
        except Exception as e:
            print(f"Error creating game components: {e}")
            raise
        
        # Game state
        self.money = STARTING_MONEY
        self.lives = STARTING_LIVES
        self.score = 0
        self.frame_count = 0
        
        # Game object lists
        self.enemies = []
        self.towers = []
        
        # Input state
        self.selected_tower_type = "basic"
        self.mouse_pos = (0, 0)
        
        # Game state flags
        self.game_over = False
        self.victory = False
        
        print("Tower Defense Game initialized successfully!")
        
        # Test render to make sure display works
        self.screen.fill((50, 100, 50))  # Dark green
        font = pygame.font.Font(None, 36)
        text = font.render("Loading Tower Defense...", True, (255, 255, 255))
        self.screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
        pygame.display.flip()
        
        print("Initial display test successful")
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
            
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.toggle_pause()
                elif event.key == pygame.K_n:
                    if not self.wave_manager.is_wave_active():
                        self.wave_manager.start_next_wave()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def handle_mouse_click(self, pos):
        """Handle mouse click events"""
        # Check UI clicks first
        ui_action = self.ui.handle_click(pos)
        
        if ui_action:
            if ui_action.startswith("select_tower/?"):
                tower_type = ui_action.split("towerid=")[-1]
                self.selected_tower_type = tower_type
                self.ui.selected_tower_type = tower_type
            
            elif ui_action == "start_wave":
                if not self.wave_manager.is_wave_active():
                    self.wave_manager.start_next_wave()
            
            elif ui_action == "pause_game":
                self.toggle_pause()
        
        # Check map clicks for tower placement
        elif pos[0] < SCREEN_WIDTH - UI_PANEL_WIDTH:  # Click is on game area
            self.try_place_tower(pos[0], pos[1])
    
    def try_place_tower(self, x, y):
        """Try to place a tower at the given position"""
        if self.game_over or self.paused:
            return
        
        # Snap to grid
        grid_x = (x // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
        grid_y = (y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
        
        # Check if placement is valid
        if self.game_map.can_place_tower(x, y):
            tower_cost = self.ui.tower_info[self.selected_tower_type]["cost"]
            
            if self.money >= tower_cost:
                # Place tower
                new_tower = Tower(grid_x, grid_y, self.selected_tower_type)
                self.towers.append(new_tower)
                self.game_map.place_tower(x, y)
                self.money -= tower_cost
    
    def toggle_pause(self):
        """Toggle game pause state"""
        self.paused = not self.paused
    
    def update_game_logic(self):
        """Update all game logic"""
        if self.paused or self.game_over:
            return
        
        self.frame_count += 1
        
        # Update wave manager and spawn enemies
        new_enemies = self.wave_manager.update(self.enemies, self.frame_count)
        self.enemies.extend(new_enemies)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Check if enemy reached the end
            if enemy.reached_end:
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_over = True
            
            # Remove dead enemies and give money
            elif not enemy.alive:
                self.money += enemy.reward
                self.score += enemy.reward
                self.enemies.remove(enemy)
        
        # Update towers
        for tower in self.towers:
            tower.update(self.enemies, self.frame_count)
        
        # Check victory condition (completed many waves)
        if self.wave_manager.get_current_wave() >= 10 and not self.wave_manager.is_wave_active():
            if len([e for e in self.enemies if e.alive and not e.reached_end]) == 0:
                self.victory = True
    
    def render(self):
        """Main render function"""
        try:
            # Clear screen
            self.screen.fill(BLACK)
            
            # Draw game map
            self.game_map.draw(self.screen)
            
            # Draw towers
            for tower in self.towers:
                tower.draw(self.screen)
            
            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            # Draw UI
            game_state = {
                'money': self.money,
                'lives': self.lives,
                'wave': self.wave_manager.get_current_wave(),
                'wave_active': self.wave_manager.is_wave_active(),
                'paused': self.paused,
                'game_over': self.game_over,
                'victory': self.victory
            }
            self.ui.draw(self.screen, game_state)
            
            # Draw tower preview
            if not self.game_over and self.mouse_pos[0] < SCREEN_WIDTH - UI_PANEL_WIDTH:
                grid_x = (self.mouse_pos[0] // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
                grid_y = (self.mouse_pos[1] // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
                
                if self.game_map.can_place_tower(self.mouse_pos[0], self.mouse_pos[1]):
                    tower_cost = self.ui.tower_info[self.selected_tower_type]["cost"]
                    color = GREEN if self.money >= tower_cost else RED
                    pygame.draw.circle(self.screen, color, (grid_x, grid_y), 15, 2)
            
            # Update display
            pygame.display.flip()
            
        except Exception as e:
            print(f"Render error: {e}")
            # Fill screen with a color to show something is working
            self.screen.fill((100, 0, 0))  # Dark red to indicate error
            pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting Tower Defense Game...")
        print("Controls:")
        print("- Click on towers in UI to select")
        print("- Click on map to place towers")
        print("- Click 'Start Wave' to begin next wave")
        print("- SPACE: Pause/Resume")
        print("- N: Start next wave")
        print("- ESC: Quit")
        
        # Show initial screen briefly
        import time
        time.sleep(1)  # Show loading screen for 1 second
        
        frame_count = 0
        while self.running:
            frame_count += 1
            
            # Handle events
            self.handle_events()
            
            # Update game (only if not paused)
            if not self.paused:
                self.update_game_logic()
            
            # Always render
            self.render()
            
            # Maintain framerate
            self.clock.tick(FPS)
            
            # Debug output every 5 seconds
            if frame_count % (FPS * 5) == 0:
                print(f"Game running: Frame {frame_count}, Money: ${self.money}, Lives: {self.lives}, Enemies: {len(self.enemies)}, Towers: {len(self.towers)}")
            
            # Check for game end conditions
            if self.game_over:
                print(f"Game Over! Final Score: {self.score}")
                # Don't exit immediately, let player see the game over screen
            elif self.victory:
                print(f"Victory! Final Score: {self.score}")
        
        print("Game ended.")

# For moderngl import error handling
try:
    import moderngl
except ImportError:
    print("Warning: ModernGL not available. Using pygame-only rendering.")
    # Create a dummy moderngl context
    class DummyModernGL:
        def create_context(self):
            return None
    moderngl = DummyModernGL()
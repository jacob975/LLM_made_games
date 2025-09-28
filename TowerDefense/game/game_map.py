"""
Game map and path management
"""

import pygame
from utils.vector2d import Vector2D
from config import *

class GameMap:
    """Handles the game map, path, and tile placement"""
    
    def __init__(self):
        self.width = SCREEN_WIDTH - UI_PANEL_WIDTH
        self.height = SCREEN_HEIGHT
        self.tile_size = TILE_SIZE
        
        # Define the path that enemies will follow
        self.path_points = [
            (50, 100),    # Start
            (200, 100),
            (200, 300),
            (400, 300),
            (400, 150),
            (600, 150),
            (600, 400),
            (800, 400),
            (800, 200),
            (950, 200),   # End
        ]
        
        # Create grid for tower placement
        self.grid_width = self.width // self.tile_size
        self.grid_height = self.height // self.tile_size
        
        # Grid: 0 = empty, 1 = path, 2 = tower
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        # Mark path tiles
        self._mark_path_tiles()
    
    def _mark_path_tiles(self):
        """Mark path tiles in the grid"""
        for i in range(len(self.path_points) - 1):
            start_x, start_y = self.path_points[i]
            end_x, end_y = self.path_points[i + 1]
            
            # Convert to grid coordinates
            start_grid_x = start_x // self.tile_size
            start_grid_y = start_y // self.tile_size
            end_grid_x = end_x // self.tile_size
            end_grid_y = end_y // self.tile_size
            
            # Mark horizontal line
            if start_grid_y == end_grid_y:
                min_x = min(start_grid_x, end_grid_x)
                max_x = max(start_grid_x, end_grid_x)
                for x in range(min_x, max_x + 1):
                    if 0 <= x < self.grid_width and 0 <= start_grid_y < self.grid_height:
                        self.grid[start_grid_y][x] = 1
            
            # Mark vertical line
            elif start_grid_x == end_grid_x:
                min_y = min(start_grid_y, end_grid_y)
                max_y = max(start_grid_y, end_grid_y)
                for y in range(min_y, max_y + 1):
                    if 0 <= start_grid_x < self.grid_width and 0 <= y < self.grid_height:
                        self.grid[y][start_grid_x] = 1
    
    def can_place_tower(self, x, y):
        """Check if a tower can be placed at the given position"""
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size
        
        if not (0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height):
            return False
        
        return self.grid[grid_y][grid_x] == 0
    
    def place_tower(self, x, y):
        """Mark a position as having a tower"""
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size
        
        if self.can_place_tower(x, y):
            self.grid[grid_y][grid_x] = 2
            return True
        return False
    
    def remove_tower(self, x, y):
        """Remove tower from position"""
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size
        
        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
            if self.grid[grid_y][grid_x] == 2:
                self.grid[grid_y][grid_x] = 0
                return True
        return False
    
    def get_path_points(self):
        """Get the path points for enemies to follow"""
        return self.path_points
    
    def draw(self, screen):
        """Draw the map"""
        # Draw background
        map_surface = pygame.Surface((self.width, self.height))
        map_surface.fill(GREEN)
        
        # Draw grid lines (optional - for debugging)
        for x in range(0, self.width, self.tile_size):
            pygame.draw.line(map_surface, LIGHT_GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, self.tile_size):
            pygame.draw.line(map_surface, LIGHT_GRAY, (0, y), (self.width, y))
        
        # Draw path
        if len(self.path_points) > 1:
            pygame.draw.lines(map_surface, YELLOW, False, self.path_points, 8)
            pygame.draw.lines(map_surface, ORANGE, False, self.path_points, 4)
        
        # Draw path points
        for point in self.path_points:
            pygame.draw.circle(map_surface, RED, point, 6)
        
        screen.blit(map_surface, (0, 0))
"""
Enemy class for tower defense game
"""

import pygame
import math
from utils.vector2d import Vector2D
from config import *

class Enemy:
    """Base enemy class"""
    
    def __init__(self, path_points, enemy_type="basic"):
        self.path_points = path_points
        self.path_index = 0
        self.position = Vector2D(path_points[0][0], path_points[0][1])
        self.target_position = Vector2D(path_points[1][0], path_points[1][1])
        
        # Enemy properties based on type
        enemy_types = {
            "basic": {"health": 100, "speed": 1.5, "reward": 10, "color": RED},
            "fast": {"health": 50, "speed": 3.0, "reward": 15, "color": YELLOW},
            "strong": {"health": 200, "speed": 1.0, "reward": 25, "color": PURPLE},
            "tank": {"health": 500, "speed": 0.8, "reward": 50, "color": DARK_GRAY}
        }
        
        self.type = enemy_type
        props = enemy_types.get(enemy_type, enemy_types["basic"])
        self.max_health = props["health"]
        self.health = self.max_health
        self.speed = props["speed"]
        self.reward = props["reward"]
        self.color = props["color"]
        
        self.alive = True
        self.reached_end = False
        self.radius = 12
        
    def update(self):
        """Update enemy position along path"""
        if not self.alive or self.reached_end:
            return
        
        # Move towards target position
        direction = self.target_position - self.position
        distance = direction.magnitude()
        
        if distance < self.speed:
            # Reached current target, move to next waypoint
            self.position = Vector2D(self.target_position.x, self.target_position.y)
            self.path_index += 1
            
            if self.path_index >= len(self.path_points) - 1:
                # Reached end of path
                self.reached_end = True
                return
            
            self.target_position = Vector2D(
                self.path_points[self.path_index + 1][0],
                self.path_points[self.path_index + 1][1]
            )
        else:
            # Move towards target
            normalized_direction = direction.normalize()
            self.position = self.position + (normalized_direction * self.speed)
    
    def take_damage(self, damage):
        """Apply damage to enemy"""
        self.health -= damage
        if self.health <= 0:
            self.alive = False
    
    def draw(self, screen):
        """Draw enemy on screen"""
        if not self.alive:
            return
        
        # Draw enemy circle
        pygame.draw.circle(screen, self.color, self.position.to_tuple(), self.radius)
        pygame.draw.circle(screen, BLACK, self.position.to_tuple(), self.radius, 2)
        
        # Draw health bar
        bar_width = 20
        bar_height = 4
        bar_x = self.position.x - bar_width // 2
        bar_y = self.position.y - self.radius - 8
        
        # Background (red)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health (green)
        health_percentage = self.health / self.max_health
        health_width = int(bar_width * health_percentage)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)
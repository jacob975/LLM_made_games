"""
Tower class for tower defense game
"""

import pygame
import math
from utils.vector2d import Vector2D
from config import *

class Projectile:
    """Projectile fired by towers"""
    
    def __init__(self, start_pos, target_pos, damage, speed=5, max_range=200):
        self.start_position = Vector2D(start_pos.x, start_pos.y)
        self.position = Vector2D(start_pos.x, start_pos.y)
        self.target = Vector2D(target_pos.x, target_pos.y)
        self.damage = damage
        self.speed = speed
        self.alive = True
        self.max_range = max_range  # Maximum distance projectile can travel
        
        # Calculate direction
        direction = self.target - self.position
        self.velocity = direction.normalize() * self.speed
        
    def update(self):
        """Update projectile position"""
        if not self.alive:
            return
        
        self.position = self.position + self.velocity
        
        # Check if projectile has traveled too far (prevent infinite travel)
        distance_traveled = self.position.distance_to(self.start_position)
        if distance_traveled > self.max_range:
            self.alive = False
    
    def draw(self, screen):
        """Draw projectile"""
        if self.alive:
            pygame.draw.circle(screen, YELLOW, self.position.to_tuple(), 3)
            pygame.draw.circle(screen, ORANGE, self.position.to_tuple(), 3, 1)

class Tower:
    """Base tower class"""
    
    def __init__(self, x, y, tower_type="basic"):
        self.position = Vector2D(x, y)
        self.tower_type = tower_type
        
        # Tower properties based on type
        tower_types = {
            "basic": {
                "damage": 25, "range": 80, "attack_rate": 30, 
                "cost": 50, "color": BLUE, "projectile_speed": 5
            },
            "sniper": {
                "damage": 75, "range": 150, "attack_rate": 60, 
                "cost": 100, "color": GREEN, "projectile_speed": 10
            },
            "machine_gun": {
                "damage": 10, "range": 60, "attack_rate": 10, 
                "cost": 75, "color": RED, "projectile_speed": 8
            },
            "cannon": {
                "damage": 100, "range": 90, "attack_rate": 90, 
                "cost": 150, "color": PURPLE, "projectile_speed": 3
            }
        }
        
        props = tower_types.get(tower_type, tower_types["basic"])
        self.damage = props["damage"]
        self.range = props["range"]
        self.attack_rate = props["attack_rate"]  # frames between attacks
        self.cost = props["cost"]
        self.color = props["color"]
        self.projectile_speed = props["projectile_speed"]
        
        self.last_attack = 0
        self.target = None
        self.projectiles = []
        self.radius = 15
        
    def can_attack(self, frame_count):
        """Check if tower can attack"""
        return frame_count - self.last_attack >= self.attack_rate
    
    def find_target(self, enemies):
        """Find the best target among enemies in range"""
        targets_in_range = []
        
        for enemy in enemies:
            if enemy.alive and not enemy.reached_end:
                distance = self.position.distance_to(enemy.position)
                if distance <= self.range:
                    targets_in_range.append((enemy, distance))
        
        if not targets_in_range:
            return None
        
        # Target the enemy that's furthest along the path (highest path_index)
        targets_in_range.sort(key=lambda x: x[0].path_index, reverse=True)
        return targets_in_range[0][0]
    
    def attack(self, target, frame_count):
        """Attack target enemy"""
        if self.can_attack(frame_count) and target:
            # Create projectile with max range based on tower range
            projectile = Projectile(
                self.position, target.position, 
                self.damage, self.projectile_speed, 
                max_range=self.range + 100  # Allow projectile to travel beyond tower range
            )
            self.projectiles.append(projectile)
            self.last_attack = frame_count
    
    def update(self, enemies, frame_count):
        """Update tower logic"""
        # Find and attack target
        self.target = self.find_target(enemies)
        if self.target:
            self.attack(self.target, frame_count)
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.alive:
                self.projectiles.remove(projectile)
                continue
            
            # Check collision with enemies - more generous collision detection
            hit_enemy = False
            for enemy in enemies:
                if enemy.alive and not enemy.reached_end:
                    distance = projectile.position.distance_to(enemy.position)
                    # Much more generous collision radius for better gameplay
                    collision_radius = enemy.radius + 25  # Significantly increased collision area
                    if distance < collision_radius:
                        enemy.take_damage(projectile.damage)
                        projectile.alive = False
                        hit_enemy = True
                        break
            
            # Remove projectile if it hit something
            if hit_enemy:
                continue
    
    def draw(self, screen):
        """Draw tower and its projectiles"""
        # Draw range circle (when selected - for now always show)
        pygame.draw.circle(screen, LIGHT_GRAY, self.position.to_tuple(), self.range, 1)
        
        # Draw tower
        pygame.draw.circle(screen, self.color, self.position.to_tuple(), self.radius)
        pygame.draw.circle(screen, BLACK, self.position.to_tuple(), self.radius, 2)
        
        # Draw targeting line
        if self.target and self.target.alive:
            pygame.draw.line(screen, RED, self.position.to_tuple(), 
                           self.target.position.to_tuple(), 2)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
    
    def get_upgrade_cost(self):
        """Get cost to upgrade this tower"""
        return self.cost // 2
    
    def upgrade(self):
        """Upgrade tower stats"""
        self.damage = int(self.damage * 1.5)
        self.range = int(self.range * 1.1)
        self.attack_rate = max(5, int(self.attack_rate * 0.8))
        self.cost += self.get_upgrade_cost()
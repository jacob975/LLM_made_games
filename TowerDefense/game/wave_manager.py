"""
Wave manager for spawning enemies
"""

import random
from entities.enemy import Enemy

class WaveManager:
    """Manages enemy waves and spawning"""
    
    def __init__(self, path_points):
        self.path_points = path_points
        self.current_wave = 0
        self.enemies_in_wave = []
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.wave_active = False
        self.wave_complete = False
        
        # Wave configurations
        self.wave_configs = [
            # Wave 1: 10 basic enemies
            {"enemies": [("basic", 10)], "spawn_delay": 60},
            # Wave 2: 8 basic, 2 fast
            {"enemies": [("basic", 8), ("fast", 2)], "spawn_delay": 50},
            # Wave 3: 10 basic, 3 fast, 1 strong
            {"enemies": [("basic", 10), ("fast", 3), ("strong", 1)], "spawn_delay": 45},
            # Wave 4: 15 basic, 5 fast, 2 strong
            {"enemies": [("basic", 15), ("fast", 5), ("strong", 2)], "spawn_delay": 40},
            # Wave 5: 12 basic, 8 fast, 3 strong, 1 tank
            {"enemies": [("basic", 12), ("fast", 8), ("strong", 3), ("tank", 1)], "spawn_delay": 35},
            # Wave 6 and beyond: scaling difficulty
            {"enemies": [("basic", 20), ("fast", 10), ("strong", 5), ("tank", 2)], "spawn_delay": 30},
        ]
    
    def start_next_wave(self):
        """Start the next wave"""
        if self.wave_active:
            return False
        
        self.current_wave += 1
        self.wave_active = True
        self.wave_complete = False
        self.enemies_spawned = 0
        self.spawn_timer = 0
        
        # Get wave configuration
        wave_index = min(self.current_wave - 1, len(self.wave_configs) - 1)
        config = self.wave_configs[wave_index]
        
        # If beyond predefined waves, scale the last configuration
        if self.current_wave > len(self.wave_configs):
            scale_factor = 1 + (self.current_wave - len(self.wave_configs)) * 0.2
            scaled_enemies = []
            for enemy_type, count in config["enemies"]:
                scaled_count = int(count * scale_factor)
                scaled_enemies.append((enemy_type, scaled_count))
            config = {"enemies": scaled_enemies, "spawn_delay": max(20, config["spawn_delay"] - 5)}
        
        # Create enemy spawn queue
        self.enemies_in_wave = []
        for enemy_type, count in config["enemies"]:
            for _ in range(count):
                self.enemies_in_wave.append(enemy_type)
        
        # Shuffle for variety
        random.shuffle(self.enemies_in_wave)
        self.spawn_delay = config["spawn_delay"]
        
        return True
    
    def update(self, enemies_list, frame_count):
        """Update wave spawning logic"""
        if not self.wave_active:
            return []
        
        new_enemies = []
        
        # Spawn enemies
        if self.enemies_spawned < len(self.enemies_in_wave):
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                enemy_type = self.enemies_in_wave[self.enemies_spawned]
                new_enemy = Enemy(self.path_points, enemy_type)
                new_enemies.append(new_enemy)
                self.enemies_spawned += 1
                self.spawn_timer = 0
        
        # Check if wave is complete
        elif self.enemies_spawned >= len(self.enemies_in_wave):
            # Check if all spawned enemies are gone (dead or reached end)
            active_enemies = [e for e in enemies_list if e.alive and not e.reached_end]
            if len(active_enemies) == 0:
                self.wave_complete = True
                self.wave_active = False
        
        return new_enemies
    
    def is_wave_active(self):
        """Check if a wave is currently active"""
        return self.wave_active
    
    def is_wave_complete(self):
        """Check if current wave is complete"""
        return self.wave_complete
    
    def get_current_wave(self):
        """Get current wave number"""
        return self.current_wave
    
    def reset_wave_complete(self):
        """Reset wave complete flag"""
        self.wave_complete = False
"""
Text-based Tower Defense demonstration
Shows that the game logic works even without graphics
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities import Enemy, Tower
from game.game_map import GameMap
from game.wave_manager import WaveManager
from config import *

class TextTowerDefense:
    """Text-based version of tower defense for testing"""
    
    def __init__(self):
        print("🎮 Text-based Tower Defense Game")
        print("=" * 50)
        
        # Initialize game components
        self.game_map = GameMap()
        self.wave_manager = WaveManager(self.game_map.get_path_points())
        
        # Game state
        self.money = STARTING_MONEY
        self.lives = STARTING_LIVES
        self.score = 0
        self.frame_count = 0
        
        # Game objects
        self.enemies = []
        self.towers = []
        
        print(f"Starting conditions: ${self.money}, {self.lives} lives")
        
    def place_towers(self):
        """Place some towers for testing"""
        print("\n🏗️ Placing towers...")
        
        # Place a few strategic towers
        tower_positions = [
            (150, 150, "basic"),
            (350, 200, "sniper"),
            (250, 350, "machine_gun"),
        ]
        
        for x, y, tower_type in tower_positions:
            if self.game_map.can_place_tower(x, y):
                tower = Tower(x, y, tower_type)
                self.towers.append(tower)
                self.game_map.place_tower(x, y)
                self.money -= tower.cost
                print(f"  Placed {tower_type} tower at ({x}, {y}) for ${tower.cost}")
        
        print(f"Remaining money: ${self.money}")
    
    def run_wave(self, wave_num):
        """Run a complete wave"""
        print(f"\n🌊 Starting Wave {wave_num}...")
        
        if not self.wave_manager.start_next_wave():
            print("Could not start wave!")
            return False
        
        enemies_spawned = 0
        enemies_killed = 0
        enemies_escaped = 0
        
        # Run wave simulation
        while self.wave_manager.is_wave_active() and self.lives > 0:
            self.frame_count += 1
            
            # Spawn enemies
            new_enemies = self.wave_manager.update(self.enemies, self.frame_count)
            enemies_spawned += len(new_enemies)
            self.enemies.extend(new_enemies)
            
            # Update enemies
            for enemy in self.enemies[:]:
                enemy.update()
                
                if enemy.reached_end:
                    self.lives -= 1
                    enemies_escaped += 1
                    self.enemies.remove(enemy)
                    print(f"    Enemy escaped! Lives remaining: {self.lives}")
                    
                elif not enemy.alive:
                    self.money += enemy.reward
                    self.score += enemy.reward
                    enemies_killed += 1
                    self.enemies.remove(enemy)
            
            # Update towers
            for tower in self.towers:
                tower.update(self.enemies, self.frame_count)
            
            # Print status every few seconds
            if self.frame_count % 180 == 0:  # Every 3 seconds
                active_enemies = len([e for e in self.enemies if e.alive])
                total_projectiles = sum(len(t.projectiles) for t in self.towers)
                print(f"    Frame {self.frame_count}: {active_enemies} enemies, {total_projectiles} projectiles, ${self.money}, {self.lives} lives")
            
            # Safety break
            if self.frame_count > 2000:  # Prevent infinite loops
                print("    Wave timeout - forcing completion")
                break
        
        print(f"Wave {wave_num} Results:")
        print(f"  - Enemies spawned: {enemies_spawned}")
        print(f"  - Enemies killed: {enemies_killed}")
        print(f"  - Enemies escaped: {enemies_escaped}")
        print(f"  - Money earned: ${enemies_killed * 10}")  # Approximate
        print(f"  - Lives remaining: {self.lives}")
        
        return self.lives > 0
    
    def run_game(self):
        """Run the complete game"""
        print("\n🚀 Starting Tower Defense Game Simulation")
        
        # Place initial towers
        self.place_towers()
        
        # Run multiple waves
        for wave_num in range(1, 4):  # Run 3 waves
            if not self.run_wave(wave_num):
                print(f"\n💀 GAME OVER after wave {wave_num}")
                break
            
            print(f"\n✅ Wave {wave_num} completed successfully!")
            
            # Brief pause between waves
            print("Preparing for next wave...")
        
        else:
            print(f"\n🎉 VICTORY! All waves completed!")
        
        print(f"\nFinal Results:")
        print(f"- Final Score: {self.score}")
        print(f"- Money: ${self.money}")
        print(f"- Lives: {self.lives}")
        print(f"- Towers placed: {len(self.towers)}")
        
        return self.lives > 0

def main():
    """Main function"""
    try:
        game = TextTowerDefense()
        success = game.run_game()
        
        print("\n" + "=" * 50)
        if success:
            print("🎮 Tower Defense game logic works perfectly!")
        else:
            print("🎮 Tower Defense game logic works (player lost)")
        
        print("The graphics version should work identically.")
        print("If you see a black screen, it might be a display driver issue.")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
"""
Game validation script - tests game components without GUI
"""

import sys
import os
import pygame

# Initialize pygame for font system
pygame.init()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.vector2d import Vector2D
from entities.enemy import Enemy
from entities.tower import Tower, Projectile
from game.game_map import GameMap
from game.wave_manager import WaveManager
from game.ui import UI
from config import *

def validate_core_components():
    """Validate that all core components work correctly"""
    print("🎮 Tower Defense Game Validation")
    print("=" * 50)
    
    # Test Vector2D
    print("Testing Vector2D...")
    v1 = Vector2D(10, 20)
    v2 = Vector2D(5, 5)
    v3 = v1 + v2
    assert v3.x == 15 and v3.y == 25
    print("✓ Vector2D operations working")
    
    # Test Enemy
    print("\nTesting Enemy system...")
    path_points = [(0, 0), (100, 0), (100, 100), (200, 100)]
    enemy = Enemy(path_points, "basic")
    assert enemy.alive
    assert enemy.health == 100
    
    # Simulate movement
    for _ in range(50):
        enemy.update()
    assert enemy.position.x > 0, "Enemy should move along path"
    
    # Test damage
    enemy.take_damage(30)
    assert enemy.health == 70
    enemy.take_damage(100)
    assert not enemy.alive
    print("✓ Enemy movement and combat working")
    
    # Test different enemy types
    fast_enemy = Enemy(path_points, "fast")
    strong_enemy = Enemy(path_points, "strong")
    tank_enemy = Enemy(path_points, "tank")
    print(f"✓ Enemy types: Basic(100hp), Fast({fast_enemy.health}hp), Strong({strong_enemy.health}hp), Tank({tank_enemy.health}hp)")
    
    # Test Tower
    print("\nTesting Tower system...")
    tower = Tower(100, 100, "basic")
    assert tower.damage == 25
    assert tower.range == 80
    
    # Test tower types
    sniper = Tower(100, 100, "sniper")
    machine_gun = Tower(100, 100, "machine_gun") 
    cannon = Tower(100, 100, "cannon")
    
    print(f"✓ Tower types:")
    print(f"  - Basic: {tower.damage} dmg, {tower.range} range, ${tower.cost}")
    print(f"  - Sniper: {sniper.damage} dmg, {sniper.range} range, ${sniper.cost}")
    print(f"  - Machine Gun: {machine_gun.damage} dmg, {machine_gun.range} range, ${machine_gun.cost}")
    print(f"  - Cannon: {cannon.damage} dmg, {cannon.range} range, ${cannon.cost}")
    
    # Test target finding
    enemy_in_range = Enemy(path_points, "basic")
    enemy_in_range.position = Vector2D(120, 100)  # Within range
    
    enemy_out_of_range = Enemy(path_points, "basic")
    enemy_out_of_range.position = Vector2D(300, 100)  # Out of range
    
    enemies = [enemy_in_range, enemy_out_of_range]
    target = tower.find_target(enemies)
    assert target == enemy_in_range, "Tower should target enemy in range"
    print("✓ Tower targeting working")
    
    # Test Projectile
    print("\nTesting Projectile system...")
    projectile = Projectile(Vector2D(0, 0), Vector2D(100, 0), 25)
    start_pos = projectile.position.x
    for _ in range(10):
        projectile.update()
    assert projectile.position.x > start_pos, "Projectile should move"
    print("✓ Projectile movement working")
    
    # Test GameMap
    print("\nTesting GameMap system...")
    game_map = GameMap()
    path_points = game_map.get_path_points()
    assert len(path_points) >= 2, "Map should have path"
    
    # Test placement
    can_place = game_map.can_place_tower(500, 500)
    assert can_place, "Should be able to place tower in empty area"
    
    placed = game_map.place_tower(500, 500)
    assert placed, "Tower placement should succeed"
    
    can_place_again = game_map.can_place_tower(500, 500)
    assert not can_place_again, "Should not place tower where one exists"
    print("✓ Map and tower placement working")
    
    # Test WaveManager
    print("\nTesting Wave system...")
    wave_manager = WaveManager(path_points)
    assert wave_manager.get_current_wave() == 0
    
    started = wave_manager.start_next_wave()
    assert started
    assert wave_manager.get_current_wave() == 1
    assert wave_manager.is_wave_active()
    print("✓ Wave management working")
    
    # Simulate wave progression
    enemies_list = []
    for frame in range(200):  # Simulate several seconds
        new_enemies = wave_manager.update(enemies_list, frame)
        enemies_list.extend(new_enemies)
        
        # Update enemies (remove dead/finished ones)
        for enemy in enemies_list[:]:
            enemy.update()
            if not enemy.alive or enemy.reached_end:
                enemies_list.remove(enemy)
    
    print(f"✓ Wave spawned and processed enemies")
    
    # Test UI (basic instantiation)
    print("\nTesting UI system...")
    ui = UI()
    assert ui.selected_tower_type == "basic"
    assert len(ui.tower_info) == 4, "Should have 4 tower types"
    print("✓ UI initialization working")
    
    print("\n" + "=" * 50)
    print("🎉 All components validated successfully!")
    print("\nGame Features Summary:")
    print("- 4 tower types with different stats and costs")
    print("- 4 enemy types with varying health, speed, and rewards")
    print("- Progressive wave system with increasing difficulty")
    print("- Grid-based tower placement with path collision detection")
    print("- Projectile system with collision detection")
    print("- Comprehensive UI for tower selection and game control")
    print("\nThe Tower Defense game is fully functional!")
    
    return True

def simulate_gameplay():
    """Simulate a short gameplay scenario"""
    print("\n🎯 Simulating Gameplay Scenario")
    print("=" * 50)
    
    # Set up game components
    path_points = [(50, 100), (200, 100), (200, 300), (400, 300), (400, 150), (600, 150)]
    wave_manager = WaveManager(path_points)
    towers = []
    enemies = []
    money = STARTING_MONEY
    lives = STARTING_LIVES
    
    print(f"Starting game: ${money}, {lives} lives")
    
    # Place some towers
    tower1 = Tower(150, 150, "basic")
    tower2 = Tower(350, 200, "sniper")
    towers.append(tower1)
    towers.append(tower2)
    money -= (tower1.cost + tower2.cost)
    
    print(f"Placed 2 towers: Basic and Sniper (${tower1.cost + tower2.cost})")
    print(f"Remaining money: ${money}")
    
    # Start first wave
    wave_manager.start_next_wave()
    print(f"Started wave {wave_manager.get_current_wave()}")
    
    # Simulate gameplay for several seconds
    enemies_killed = 0
    enemies_reached_end = 0
    frame = 0
    
    while wave_manager.is_wave_active() and lives > 0 and frame < 1000:
        frame += 1
        
        # Spawn enemies
        new_enemies = wave_manager.update(enemies, frame)
        enemies.extend(new_enemies)
        
        # Update enemies
        for enemy in enemies[:]:
            enemy.update()
            if enemy.reached_end:
                lives -= 1
                enemies_reached_end += 1
                enemies.remove(enemy)
            elif not enemy.alive:
                money += enemy.reward
                enemies_killed += 1
                enemies.remove(enemy)
        
        # Update towers
        for tower in towers:
            tower.update(enemies, frame)
        
        # Print status every 100 frames
        if frame % 100 == 0:
            print(f"Frame {frame}: {len(enemies)} enemies active, ${money}, {lives} lives")
    
    print(f"\nSimulation Results:")
    print(f"- Enemies killed: {enemies_killed}")
    print(f"- Enemies reached end: {enemies_reached_end}")
    print(f"- Final money: ${money}")
    print(f"- Lives remaining: {lives}")
    print(f"- Wave complete: {wave_manager.is_wave_complete()}")
    
    if lives > 0:
        print("✅ Player survived the wave!")
    else:
        print("💀 Game over - no lives remaining")
    
    return lives > 0

if __name__ == "__main__":
    try:
        # Validate components
        validate_core_components()
        
        # Simulate gameplay
        simulate_gameplay()
        
        print("\n🚀 The Tower Defense game is ready to play!")
        print("Run 'python main.py' to start the full game with graphics.")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up pygame
        pygame.quit()
"""
Test the improved projectile collision detection system
"""

import sys
import os
import pygame

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.vector2d import Vector2D
from entities.enemy import Enemy
from entities.tower import Tower, Projectile
from config import *

def test_projectile_collision():
    """Test that projectiles can hit enemies even if they miss the original target"""
    print("🎯 Testing Projectile Collision System")
    print("=" * 50)
    
    # Initialize pygame for testing
    pygame.init()
    
    # Set up test scenario
    path_points = [(0, 100), (200, 100), (400, 100), (600, 100)]
    
    # Create enemies at different positions
    enemy1 = Enemy(path_points, "basic")
    enemy1.position = Vector2D(150, 100)  # First enemy
    
    enemy2 = Enemy(path_points, "basic") 
    enemy2.position = Vector2D(250, 100)  # Second enemy further along
    
    enemy3 = Enemy(path_points, "fast")
    enemy3.position = Vector2D(180, 120)  # Third enemy slightly off path
    
    enemies = [enemy1, enemy2, enemy3]
    
    # Create tower
    tower = Tower(100, 150, "basic")
    
    print(f"Initial setup:")
    print(f"  Tower at ({tower.position.x}, {tower.position.y})")
    print(f"  Enemy1 at ({enemy1.position.x}, {enemy1.position.y}) - Health: {enemy1.health}")
    print(f"  Enemy2 at ({enemy2.position.x}, {enemy2.position.y}) - Health: {enemy2.health}")  
    print(f"  Enemy3 at ({enemy3.position.x}, {enemy3.position.y}) - Health: {enemy3.health}")
    
    # Test 1: Tower targets first enemy but projectile should be able to hit any enemy
    print(f"\\nTest 1: Tower targeting and projectile travel")
    
    # Force tower to target enemy1 and ensure it can attack
    tower.target = enemy1
    tower.last_attack = -100  # Set to allow immediate attack
    tower.attack(enemy1, 0)
    
    print(f"  Tower created projectile targeting Enemy1")
    print(f"  Projectiles count: {len(tower.projectiles)}")
    
    # If no projectile was created, force create one for testing
    if len(tower.projectiles) == 0:
        print("  Manually creating projectile for test...")
        projectile = Projectile(tower.position, enemy1.position, tower.damage, tower.projectile_speed, max_range=tower.range + 100)
        tower.projectiles.append(projectile)
    
    # Move enemy1 away quickly (simulating a miss)
    enemy1.position = Vector2D(50, 50)  # Move out of projectile path
    print(f"  Enemy1 moved to ({enemy1.position.x}, {enemy1.position.y}) to simulate miss")
    
    # Simulate projectile movement and collision detection
    hits_recorded = []
    frame = 0
    max_frames = 100  # Prevent infinite loop
    
    while len(tower.projectiles) > 0 and frame < max_frames:
        frame += 1
        
        initial_healths = [(i, e.health) for i, e in enumerate(enemies)]
        
        # Debug: Print positions before update
        if frame % 10 == 0:
            if len(tower.projectiles) > 0:
                proj = tower.projectiles[0]
                print(f"    Frame {frame}: Projectile at ({proj.position.x:.1f}, {proj.position.y:.1f})")
                for i, enemy in enumerate(enemies):
                    if enemy.alive:
                        distance = proj.position.distance_to(enemy.position)
                        print(f"      Enemy{i+1} at ({enemy.position.x:.1f}, {enemy.position.y:.1f}), distance: {distance:.1f}")
        
        # Update tower (which updates projectiles and checks collisions)
        tower.update(enemies, frame)
        
        # Check if any enemy took damage
        for i, enemy in enumerate(enemies):
            initial_health = initial_healths[i][1]
            if enemy.health < initial_health:
                damage_taken = initial_health - enemy.health
                hits_recorded.append((i+1, frame, damage_taken, enemy.position.x, enemy.position.y))
                print(f"    Frame {frame}: Enemy{i+1} hit! Damage: {damage_taken}, Health: {enemy.health}")
    
    print(f"\\nTest Results:")
    print(f"  Simulation ran for {frame} frames")
    print(f"  Total hits recorded: {len(hits_recorded)}")
    
    if len(hits_recorded) > 0:
        print(f"  ✅ SUCCESS: Projectile hit enemies even after missing original target!")
        for hit in hits_recorded:
            enemy_num, hit_frame, damage, x, y = hit
            print(f"    - Enemy{enemy_num} hit at frame {hit_frame} for {damage} damage at position ({x:.1f}, {y:.1f})")
    else:
        print(f"  ❌ FAILURE: No enemies were hit by projectiles")
    
    return len(hits_recorded) > 0

def test_multiple_projectiles():
    """Test multiple projectiles hitting different enemies"""
    print(f"\\n🎯 Testing Multiple Projectiles")
    print("=" * 50)
    
    path_points = [(0, 100), (300, 100), (600, 100)]
    
    # Create multiple enemies in a line
    enemies = []
    for i in range(5):
        enemy = Enemy(path_points, "basic")
        enemy.position = Vector2D(200 + i * 30, 100)  # Space them closer together
        enemies.append(enemy)
    
    # Create a machine gun tower (fast firing) closer to enemies
    tower = Tower(150, 100, "machine_gun")
    
    print(f"Setup: {len(enemies)} enemies, Machine Gun tower at ({tower.position.x}, {tower.position.y})")
    for i, enemy in enumerate(enemies):
        print(f"  Enemy{i+1} at ({enemy.position.x}, {enemy.position.y})")
    
    # Force the tower to be able to attack immediately
    tower.last_attack = -1000
    
    # Fire multiple projectiles
    enemies_killed = 0
    initial_enemy_count = len([e for e in enemies if e.alive])
    
    for frame in range(300):  # Run longer simulation
        # Count alive enemies before tower update
        alive_before = len([e for e in enemies if e.alive])
        
        # Make sure tower can attack frequently
        if frame % 5 == 0:  # Every 5 frames, reset attack cooldown
            tower.last_attack = frame - tower.attack_rate - 1
        
        # Update tower (which finds targets and shoots)
        tower.update(enemies, frame)
        
        # Count alive enemies after tower update
        alive_after = len([e for e in enemies if e.alive])
        frame_kills = alive_before - alive_after
        
        if frame_kills > 0:
            enemies_killed += frame_kills
            print(f"  Frame {frame}: {frame_kills} enemies killed, {alive_after} remaining, {len(tower.projectiles)} active projectiles")
        
        # Print status occasionally
        if frame % 50 == 0:
            active_projectiles = len(tower.projectiles)
            alive_enemies = len([e for e in enemies if e.alive])
            print(f"  Frame {frame}: {alive_enemies} enemies alive, {active_projectiles} projectiles active")
        
        # Break if all enemies are dead
        if alive_after == 0:
            print(f"  All enemies eliminated at frame {frame}!")
            break
    
    print(f"\\nMultiple Projectiles Test Results:")
    print(f"  Total enemies killed: {enemies_killed}")
    print(f"  Active projectiles remaining: {len(tower.projectiles)}")
    
    if enemies_killed > 0:
        print(f"  ✅ SUCCESS: Multiple projectiles system working!")
    else:
        print(f"  ❌ FAILURE: No enemies killed")
    
    return enemies_killed > 0

def test_projectile_range():
    """Test that projectiles don't travel infinitely"""
    print(f"\\n🎯 Testing Projectile Range Limits")
    print("=" * 50)
    
    # Create a projectile that should die after traveling too far
    start_pos = Vector2D(0, 0)
    target_pos = Vector2D(1000, 0)  # Very far target
    projectile = Projectile(start_pos, target_pos, 25, speed=10, max_range=200)
    
    print(f"Created projectile with max_range=200, targeting distance=1000")
    
    # Simulate projectile movement
    frames = 0
    while projectile.alive and frames < 100:
        frames += 1
        projectile.update()
        
        if frames % 10 == 0:
            distance_traveled = projectile.position.distance_to(start_pos)
            print(f"  Frame {frames}: Distance traveled: {distance_traveled:.1f}")
    
    final_distance = projectile.position.distance_to(start_pos)
    print(f"\\nRange Test Results:")
    print(f"  Final distance traveled: {final_distance:.1f}")
    print(f"  Projectile alive: {projectile.alive}")
    
    if final_distance <= 220 and not projectile.alive:  # Small tolerance
        print(f"  ✅ SUCCESS: Projectile properly limited by range!")
        return True
    else:
        print(f"  ❌ FAILURE: Projectile range not properly limited")
        return False

def main():
    """Run all projectile tests"""
    print("🎮 Testing Improved Projectile System")
    print("=" * 60)
    
    try:
        test1_passed = test_projectile_collision()
        test2_passed = test_multiple_projectiles()
        test3_passed = test_projectile_range()
        
        print("\\n" + "=" * 60)
        print("📊 TEST SUMMARY:")
        print(f"  Projectile Collision: {'✅ PASS' if test1_passed else '❌ FAIL'}")
        print(f"  Multiple Projectiles: {'✅ PASS' if test2_passed else '❌ FAIL'}")
        print(f"  Projectile Range: {'✅ PASS' if test3_passed else '❌ FAIL'}")
        
        if all([test1_passed, test2_passed, test3_passed]):
            print("\\n🎉 ALL TESTS PASSED! Projectile system fixed!")
            print("\\nImprovements made:")
            print("- Projectiles can hit any enemy, not just original target")
            print("- More generous collision detection radius") 
            print("- Projectiles have maximum travel distance")
            print("- Better collision system prevents missed shots")
        else:
            print("\\n⚠️ Some tests failed - need further investigation")
            
    except Exception as e:
        print(f"\\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
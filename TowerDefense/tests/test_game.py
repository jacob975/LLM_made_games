"""
Test file for Tower Defense Game
"""

import pygame
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.vector2d import Vector2D
from entities.enemy import Enemy
from entities.tower import Tower
from game.game_map import GameMap

def test_vector2d():
    """Test Vector2D class"""
    print("Testing Vector2D class...")
    
    v1 = Vector2D(3, 4)
    v2 = Vector2D(1, 2)
    
    # Test basic operations
    v3 = v1 + v2
    assert v3.x == 4 and v3.y == 6, "Addition failed"
    
    v4 = v1 - v2
    assert v4.x == 2 and v4.y == 2, "Subtraction failed"
    
    v5 = v1 * 2
    assert v5.x == 6 and v5.y == 8, "Multiplication failed"
    
    # Test magnitude
    assert v1.magnitude() == 5.0, "Magnitude calculation failed"
    
    # Test distance
    distance = v1.distance_to(v2)
    expected_distance = ((3-1)**2 + (4-2)**2)**0.5
    assert abs(distance - expected_distance) < 0.001, "Distance calculation failed"
    
    print("✓ Vector2D tests passed!")

def test_enemy():
    """Test Enemy class"""
    print("Testing Enemy class...")
    
    path_points = [(0, 0), (100, 0), (100, 100), (200, 100)]
    enemy = Enemy(path_points, "basic")
    
    assert enemy.alive == True, "Enemy should be alive initially"
    assert enemy.health == 100, "Enemy should have full health"
    assert enemy.position.x == 0 and enemy.position.y == 0, "Enemy should start at first path point"
    
    # Test movement
    initial_x = enemy.position.x
    for _ in range(10):  # Update multiple times
        enemy.update()
    
    assert enemy.position.x > initial_x, "Enemy should have moved"
    
    # Test damage
    enemy.take_damage(50)
    assert enemy.health == 50, "Enemy should take damage"
    
    enemy.take_damage(60)
    assert enemy.alive == False, "Enemy should die when health reaches 0"
    
    print("✓ Enemy tests passed!")

def test_tower():
    """Test Tower class"""
    print("Testing Tower class...")
    
    tower = Tower(100, 100, "basic")
    
    assert tower.position.x == 100 and tower.position.y == 100, "Tower position incorrect"
    assert tower.damage == 25, "Tower damage incorrect"
    assert tower.range == 80, "Tower range incorrect"
    
    # Test target finding
    path_points = [(50, 100), (150, 100), (250, 100)]
    enemy1 = Enemy(path_points, "basic")
    enemy2 = Enemy(path_points, "basic")
    enemy2.position = Vector2D(200, 100)  # Move second enemy further
    
    enemies = [enemy1, enemy2]
    target = tower.find_target(enemies)
    
    # Should target enemy within range
    assert target is not None, "Tower should find a target"
    
    print("✓ Tower tests passed!")

def test_game_map():
    """Test GameMap class"""
    print("Testing GameMap class...")
    
    game_map = GameMap()
    
    # Test path points
    path_points = game_map.get_path_points()
    assert len(path_points) > 0, "Map should have path points"
    
    # Test tower placement - try a position that's definitely not on path
    # Let's try coordinates that should be in an empty area
    test_x, test_y = 500, 500  # Should be empty area
    can_place = game_map.can_place_tower(test_x, test_y)
    
    # Debug info
    grid_x = test_x // game_map.tile_size
    grid_y = test_y // game_map.tile_size
    print(f"  Trying to place at ({test_x}, {test_y}) -> grid ({grid_x}, {grid_y})")
    print(f"  Grid value at position: {game_map.grid[grid_y][grid_x] if 0 <= grid_y < len(game_map.grid) and 0 <= grid_x < len(game_map.grid[0]) else 'out of bounds'}")
    
    assert can_place == True, f"Should be able to place tower at ({test_x}, {test_y})"
    
    # Place tower and check
    placed = game_map.place_tower(test_x, test_y)
    assert placed == True, "Tower placement should succeed"
    
    # Try to place another tower in same spot
    can_place_again = game_map.can_place_tower(test_x, test_y)
    assert can_place_again == False, "Should not be able to place tower where one already exists"
    
    print("✓ GameMap tests passed!")

def run_all_tests():
    """Run all unit tests"""
    print("Running Tower Defense Game Tests...")
    print("=" * 50)
    
    try:
        test_vector2d()
        test_enemy()
        test_tower()
        test_game_map()
        
        print("=" * 50)
        print("✅ All tests passed! The game components are working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    # Initialize pygame (needed for some tests)
    pygame.init()
    
    success = run_all_tests()
    
    if success:
        print("\nGame is ready to run! Execute 'python main.py' to start playing.")
    else:
        print("\nSome tests failed. Please check the implementation.")
    
    pygame.quit()
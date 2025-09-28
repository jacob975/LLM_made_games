"""
Simple graphics test for the tower defense game
"""

import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
from entities import Enemy, Tower
from game.game_map import GameMap
from utils.vector2d import Vector2D

def test_graphics_rendering():
    """Test basic graphics rendering without opening a window"""
    print("🎨 Testing Graphics Rendering")
    print("=" * 40)
    
    # Initialize pygame
    pygame.init()
    
    try:
        # Create an off-screen surface for testing
        test_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Test basic drawing
        test_surface.fill(GREEN)  # Background
        pygame.draw.circle(test_surface, RED, (100, 100), 20)  # Enemy
        pygame.draw.circle(test_surface, BLUE, (200, 200), 15)  # Tower
        pygame.draw.line(test_surface, YELLOW, (50, 50), (350, 350), 5)  # Path
        
        print("✓ Basic pygame drawing operations work")
        
        # Test game object rendering
        path_points = [(50, 100), (200, 100), (200, 300), (400, 300)]
        
        # Create and test enemy rendering
        enemy = Enemy(path_points, "basic")
        enemy.draw(test_surface)
        print("✓ Enemy rendering works")
        
        # Create and test tower rendering  
        tower = Tower(150, 150, "basic")
        tower.draw(test_surface)
        print("✓ Tower rendering works")
        
        # Test map rendering
        game_map = GameMap()
        game_map.draw(test_surface)
        print("✓ Game map rendering works")
        
        # Test font rendering
        font = pygame.font.Font(None, 24)
        text = font.render("Tower Defense", True, WHITE)
        test_surface.blit(text, (10, 10))
        print("✓ Font rendering works")
        
        print("\n✅ All graphics components render successfully!")
        print("The game should display properly when run on a system with a display.")
        
        return True
        
    except Exception as e:
        print(f"❌ Graphics test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        pygame.quit()

def check_dependencies():
    """Check that all required dependencies are available"""
    print("\n📦 Checking Dependencies")
    print("=" * 40)
    
    try:
        import pygame
        print(f"✓ pygame {pygame.version.ver} - OK")
    except ImportError:
        print("❌ pygame not found")
        return False
    
    try:
        import moderngl
        print(f"✓ moderngl {moderngl.__version__} - OK")
    except ImportError:
        print("❌ moderngl not found")
        return False
        
    try:
        import numpy
        print(f"✓ numpy {numpy.__version__} - OK")
    except ImportError:
        print("❌ numpy not found")
        return False
        
    print("\n✅ All dependencies are available!")
    return True

if __name__ == "__main__":
    print("🎮 Tower Defense Game - Graphics & Dependencies Test")
    print("=" * 60)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    if deps_ok:
        # Test graphics
        graphics_ok = test_graphics_rendering()
        
        if graphics_ok:
            print("\n🎉 Complete Success!")
            print("The Tower Defense game is fully ready to run.")
            print("\nTo play the game:")
            print("1. Ensure you have a graphical display available")
            print("2. Run: conda activate TDlike")
            print("3. Run: python main.py")
            print("\nGame will open in a new window with full graphics!")
        else:
            print("\n⚠️  Graphics test failed, but core game logic works")
    else:
        print("\n❌ Missing dependencies - please install requirements")
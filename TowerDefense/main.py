"""
2D Tower Defense Game
Main entry point for the game
"""

import pygame
import sys
from game.tower_defense_game import TowerDefenseGame

def main():
    """Main function to run the tower defense game"""
    print("Initializing Tower Defense Game...")
    
    try:
        pygame.init()
        print("Pygame initialized successfully")
    except Exception as e:
        print(f"Error initializing pygame: {e}")
        return
    
    try:
        print("Creating game instance...")
        game = TowerDefenseGame()
        print("Game instance created, starting game loop...")
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("Cleaning up pygame...")
        pygame.quit()
        print("Game ended successfully")

if __name__ == "__main__":
    main()
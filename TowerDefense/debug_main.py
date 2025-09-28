"""
Debug version of the main game to identify rendering issues
"""

import pygame
import sys
from config import *

def debug_main():
    """Debug version with step-by-step initialization"""
    print("=== Tower Defense Debug Mode ===")
    
    print("Step 1: Initialize pygame...")
    pygame.init()
    
    print("Step 2: Create display...")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense - Debug Mode")
    
    print("Step 3: Initialize basic components...")
    clock = pygame.time.Clock()
    running = True
    
    # Basic colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    print("Step 4: Test font system...")
    font = pygame.font.Font(None, 24)
    
    print("Step 5: Starting debug game loop...")
    frame_count = 0
    
    while running and frame_count < 600:  # Run for 10 seconds
        frame_count += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    print(f"Space pressed at frame {frame_count}")
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw some test elements
        # Background
        pygame.draw.rect(screen, GREEN, (0, 0, SCREEN_WIDTH - UI_PANEL_WIDTH, SCREEN_HEIGHT))
        
        # UI Panel
        pygame.draw.rect(screen, (200, 200, 200), (SCREEN_WIDTH - UI_PANEL_WIDTH, 0, UI_PANEL_WIDTH, SCREEN_HEIGHT))
        
        # Test path
        path_points = [(50, 100), (200, 100), (200, 300), (400, 300)]
        if len(path_points) > 1:
            pygame.draw.lines(screen, (255, 255, 0), False, path_points, 8)
        
        # Test enemy (red circle)
        enemy_x = 50 + (frame_count % 200) * 2
        pygame.draw.circle(screen, RED, (enemy_x, 100), 12)
        
        # Test tower (blue circle)
        pygame.draw.circle(screen, BLUE, (150, 150), 15)
        
        # Test UI text
        text = font.render(f"Frame: {frame_count}", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH - 180, 20))
        
        money_text = font.render(f"Money: $200", True, BLACK)
        screen.blit(money_text, (SCREEN_WIDTH - 180, 50))
        
        lives_text = font.render(f"Lives: 20", True, BLACK)
        screen.blit(lives_text, (SCREEN_WIDTH - 180, 80))
        
        # Instructions
        instr_text = font.render("ESC: Quit, SPACE: Debug", True, WHITE)
        screen.blit(instr_text, (10, 10))
        
        # Update display
        pygame.display.flip()
        
        # Control framerate
        clock.tick(FPS)
        
        # Status every 2 seconds
        if frame_count % 120 == 0:
            print(f"Debug frame {frame_count}: All systems working")
    
    print("Step 6: Cleaning up...")
    pygame.quit()
    print("Debug mode completed successfully!")

if __name__ == "__main__":
    try:
        debug_main()
    except Exception as e:
        print(f"Debug error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)
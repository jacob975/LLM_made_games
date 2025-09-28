"""
Minimal pygame test to verify basic functionality
"""

import pygame
import sys

def minimal_test():
    """Test basic pygame functionality"""
    print("Initializing pygame...")
    pygame.init()
    
    print("Creating display...")
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Minimal Test")
    
    print("Setting up colors...")
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    clock = pygame.time.Clock()
    running = True
    
    print("Starting game loop...")
    
    frame_count = 0
    while running and frame_count < 300:  # Run for 5 seconds at 60 FPS
        frame_count += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw some simple shapes
        pygame.draw.circle(screen, RED, (100, 100), 50)
        pygame.draw.circle(screen, GREEN, (200, 200), 30)
        pygame.draw.circle(screen, BLUE, (300, 150), 40)
        
        # Draw text
        font = pygame.font.Font(None, 36)
        text = font.render("Pygame Test - Press ESC to exit", True, WHITE)
        screen.blit(text, (50, 50))
        
        # Update display
        pygame.display.flip()
        
        # Control framerate
        clock.tick(60)
        
        # Print status every second
        if frame_count % 60 == 0:
            print(f"Frame {frame_count}: Pygame running normally")
    
    print("Cleaning up...")
    pygame.quit()
    print("Test completed successfully!")

if __name__ == "__main__":
    try:
        minimal_test()
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
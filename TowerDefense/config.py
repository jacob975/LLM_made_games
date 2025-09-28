"""
Game constants and configuration
"""

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# Game settings
FPS = 60
TILE_SIZE = 40

# Enemy settings
ENEMY_SPAWN_RATE = 60  # frames between enemy spawns
ENEMY_HEALTH = 100
ENEMY_SPEED = 2
ENEMY_REWARD = 10

# Tower settings
TOWER_COST = 50
TOWER_RANGE = 80
TOWER_DAMAGE = 25
TOWER_ATTACK_RATE = 30  # frames between attacks

# Player settings
STARTING_MONEY = 200
STARTING_LIVES = 20

# UI settings
UI_PANEL_WIDTH = 200
UI_PANEL_HEIGHT = SCREEN_HEIGHT
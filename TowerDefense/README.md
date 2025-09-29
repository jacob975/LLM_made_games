# Tower Defense Game

A 2D Tower Defense game built with Python, Pygame, and ModernGL using Object-Oriented Programming principles.

## Features

- **Multiple Tower Types**: Basic, Sniper, Machine Gun, and Cannon towers with different stats
- **Enemy Varieties**: Basic, Fast, Strong, and Tank enemies with varying health, speed, and rewards  
- **Wave System**: Progressive difficulty with 10+ waves
- **Modern Graphics**: Hybrid rendering using Pygame and ModernGL for enhanced visuals
- **Interactive UI**: Tower selection, wave management, and game stats
- **Grid-based Placement**: Strategic tower positioning on a grid system
- **Path Following**: Enemies follow predefined paths with smooth movement

## Installation

1. Ensure you have Python 3.11+ installed
2. Create and activate the conda environment:
   ```bash
   conda create -n TDlike python=3.11
   conda activate TDlike
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. Activate the conda environment:
   ```bash
   conda activate TDlike
   ```

2. Run the game:
   ```bash
   python main.py
   ```

3. Run tests (optional):
   ```bash
   python tests/test_game.py
   ```

## Game Controls

- **Mouse Click**: Place towers on the map
- **UI Buttons**: Select tower types, start waves, pause game
- **SPACE**: Pause/Resume game
- **N**: Start next wave (when ready)
- **ESC**: Quit game

## Game Mechanics

### Towers
- **Basic Tower**: Balanced damage and range ($50)
- **Sniper Tower**: High damage, long range, slow attack rate ($100)  
- **Machine Gun**: Fast attacks, short range, low damage ($75)
- **Cannon**: High damage, medium range, slow attacks ($150)

### Enemies  
- **Basic**: Standard health and speed (100 HP, reward: $10)
- **Fast**: Low health, high speed (50 HP, reward: $15)
- **Strong**: High health, slow speed (200 HP, reward: $25)
- **Tank**: Very high health, very slow (500 HP, reward: $50)

### Objective
- Prevent enemies from reaching the end of the path
- Start with $200 and 20 lives
- Complete 10 waves to achieve victory
- Earn money by destroying enemies to buy more towers

## Project Structure

```
TowerDefense/
├── main.py                 # Entry point
├── config.py              # Game constants
├── requirements.txt       # Dependencies
├── entities/              # Game entities
│   ├── __init__.py
│   ├── enemy.py          # Enemy classes
│   └── tower.py          # Tower and Projectile classes
├── game/                 # Game logic
│   ├── __init__.py
│   ├── tower_defense_game.py  # Main game class
│   ├── game_map.py       # Map and pathfinding
│   ├── ui.py            # User interface
│   └── wave_manager.py   # Wave spawning logic
├── utils/               # Utilities
│   ├── __init__.py
│   └── vector2d.py      # Vector math
└── tests/              # Unit tests
    └── test_game.py    # Game component tests
```

## Technical Details

- **Engine**: Pygame for 2D graphics and input handling
- **Rendering**: ModernGL for enhanced graphics capabilities with fallback to pure Pygame
- **Architecture**: Object-oriented design with separate classes for game entities
- **Math**: Custom Vector2D class for position calculations and movement
- **Performance**: Efficient collision detection and rendering optimizations

## Development

The game follows OOP principles with clear separation of concerns:

- `Entity` classes handle game objects (towers, enemies, projectiles)
- `Game` classes manage game logic (map, waves, UI)  
- `Utils` provide reusable mathematical operations
- `Config` centralizes game constants and settings
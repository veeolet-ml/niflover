# Dinosaur Runner Game 

A Python implementation of the classic Chrome dinosaur game with added features like projectiles and scoring system.

## Features

- **Classic Gameplay**: Jump and duck to avoid obstacles
- **Projectile System**: Collect and shoot projectiles to destroy obstacles
- **Progressive Difficulty**: Game speed increases as your score grows
- **Score Tracking**: Local highscore persistence across game sessions
- **Multiple Obstacle Types**: Small cacti, large cacti, and flying birds
- **Smooth Animations**: Fluid character movements and obstacle animations

## Prerequisites

- Python 3.x
- pygame library

## Installation

1. Clone or download this repository

2. Install the required dependencies:
```
pip install pygame
```

3. Ensure the following directory structure exists:
```
game/
├── main.py
├── dinosaur.py
├── constants.py
├── README.md
└── Assets/
    ├── Dino/
    │   ├── DinoRun1.png
    │   ├── DinoRun2.png
    │   ├── DinoJump.png
    │   ├── DinoDuck1.png
    │   └── DinoDuck2.png
    ├── Cactus/
    │   ├── SmallCactus1.png
    │   ├── SmallCactus2.png
    │   ├── SmallCactus3.png
    │   ├── LargeCactus1.png
    │   ├── LargeCactus2.png
    │   └── LargeCactus3.png
    ├── Bird/
    │   ├── Bird1.png
    │   └── Bird2.png
    └── Other/
        ├── Cloud.png
        ├── Track.png
        └── Projectile.png
```

## How to Run
```
python main.py
```

## Controls

### In-Game
- **↑ (Up Arrow)**: Jump over obstacles
- **↓ (Down Arrow)**: Duck under flying obstacles
- **X**: Shoot projectile (when available)

### Menu
- **Any Key**: Start game / Restart after game over
- **Q**: Quit game and submit score

## Gameplay Mechanics

### Scoring
- Points increase continuously while playing
- Every 100 points: Game speed increases by 1
- Every 200 points: Earn 1 projectile

### Obstacles
- **Small Cacti**: Low-height obstacles that require jumping
- **Large Cacti**: Taller obstacles that require jumping
- **Birds**: Flying obstacles at varying heights - jump or duck

### Projectiles
- Collected automatically every 200 points
- Press **X** to shoot
- Destroys obstacles on contact
- Limited ammunition - use strategically!

## Game Over
When you collide with an obstacle:
- View your final score
- See your highscore
- Press any key to restart
- Press **Q** to quit

## Customization

Edit `constants.py` to modify:
- Screen dimensions (`SCREEN_WIDTH`, `SCREEN_HEIGHT`)
- Game difficulty parameters
- Asset file paths

Edit `main.py` to adjust:
- Initial game speed (default: 14)
- Speed increase intervals
- Projectile reward frequency

## Code Structure

- **main.py**: Main game loop, obstacle management, and menu system
- **dinosaur.py**: Player character class with movement logic
- **constants.py**: Game constants and asset loading

## Troubleshooting

**Game won't start:**
- Ensure pygame is installed: `pip install pygame`
- Verify all asset files are in the correct directories

**Images not loading:**
- Check that the `Assets` folder is in the same directory as the Python files
- Verify all image file names match exactly (case-sensitive)

**Module not found errors:**
- Ensure all three Python files are in the same directory
- Run the game from the directory containing the files

## Credits

Based on the classic Chrome dinosaur game with custom enhancements.

## License

Free to use and modify for personal and educational purposes.
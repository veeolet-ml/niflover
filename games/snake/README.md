# Snake Game

A classic Snake game built with **Pygame** featuring retro arcade aesthetics and high score tracking for _niflover_ matching.

## Features

- **Classic Gameplay** — Grow your snake by eating food while avoiding walls and your own tail
- **Retro HUD** — Color effects and pixel-perfect fonts for that arcade feel
- **Sound Effects** — Pickup sounds and background music
- **High Score System** — Track your best scores with username submission
- **Superfast Mode** — Hold `E` to speed up the game
- **Configurable Food Count** — Start with as many food items as you want

## Installation

See full project README for dependencies.

## Usage

Run the game from the `snake` directory:

```bash
python main.py
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-f`, `--food` | Number of food items on the grid | 3 |
| `-s`, `--server` | Server address for score submission | `localhost:5000` |

**Example:**

```bash
python main.py --food 5
```

## Controls

| Key | Action |
|-----|--------|
| `W` / `↑` | Move Up |
| `S` / `↓` | Move Down |
| `A` / `←` | Move Left |
| `D` / `→` | Move Right |
| `E` | Superfast mode (hold) |
| `SPACE` / `ENTER` | Start game / Submit score |
| `R` | Restart (game over screen) |
| `Q` | Quit (game over screen) |

## Winning

Score 1000 or more points to see the **"YOU WIN!"** message!

## Project Structure

```
snake/
├── main.py          # Entry point
├── game.py          # Main game loop and state management
├── snake.py         # Snake entity and movement logic
├── snake_grid.py    # Grid system
├── food_manager.py  # Food spawning and management
├── score_manager.py # Score tracking
├── HUD.py           # Heads-up display and UI rendering
├── fonts/           # Retro pixel fonts
└── sounds/          # Music and sound effects
```

## License

Part of the **niflover** project.

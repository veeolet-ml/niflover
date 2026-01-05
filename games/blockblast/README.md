# Block Blast Puzzle Game 

A Python implementation of the popular Block Blast puzzle game using Pygame. Place blocks strategically on an 8x8 grid to clear lines and achieve high scores!

## Features

- **Strategic Puzzle Gameplay**: Place blocks on the grid to form complete rows or columns
- **Multiple Block Shapes**: 18+ different block types including squares, L-shapes, zigzags, and lines
- **Line Clearing System**: Clear complete rows and columns simultaneously for combo bonuses
- **Score Multiplier**: Exponential scoring system - clear multiple lines at once for massive points!
- **Game Over Detection**: Automatic detection when no valid moves remain
- **Highscore Tracking**: Local highscore persistence across sessions
- **Visual Feedback**: Hover preview shows where blocks will be placed
- **Finish Session Button**: End game voluntarily to submit your score

## Prerequisites

- Python 3.x
- pygame library

## Installation

1. Clone or download this repository

2. Install the required dependencies:
```
pip install pygame
```

3. Ensure all game files are in the same directory:
```
game/
├── main.py
├── blocks.py
├── grid.py
├── constants.py
└── README.md
```

## How to Run
```bash
python main.py
```

## Controls

### Gameplay
- **Mouse Click**: Select and place blocks
- **Left Mouse Button**: Pick up a block from the selection area, then click on the grid to place it

### Game Over Screen
- **R**: Restart the game
- **ESC** or **Q**: Quit the game

### In-Game Options
- **Finish Session Button**: Click the button in the top-right corner to end the current session

## Gameplay Mechanics

### Objective
Place blocks on the 8x8 grid to form complete horizontal rows or vertical columns. When a row or column is completely filled, it clears and you earn points.

### Scoring System
Points are awarded exponentially based on the number of lines cleared simultaneously:
- **Formula**: `Score = 2^(rows) × 2^(cols) × 100`
- Examples:
  - 1 row cleared: 200 points
  - 2 rows cleared: 400 points
  - 1 row + 1 column: 400 points
  - 2 rows + 1 column: 800 points
  - 3 rows + 2 columns: 3,200 points

### Block Placement Rules
1. **Select a Block**: Click on one of the three available blocks in the selection area
2. **Place the Block**: Click on the grid where you want to place it
3. **Valid Placement**: All cells of the block must fit on empty grid spaces
4. **New Block Generation**: Once placed, a new random block appears in that slot

### Block Types

**Squares**:
- Small Square (2×2)
- Big Square (3×3)

**L-Shapes** (8 variations):
- Standard L-shapes in all 4 rotations
- Mirrored L-shapes in all 4 rotations

**Zigzags** (4 variations):
- S-shaped and Z-shaped pieces in multiple orientations

**Lines**:
- Short lines (3 cells) - horizontal and vertical
- Long lines (4 cells) - horizontal and vertical

### Game Over
The game ends when:
1. None of the three available blocks can be placed anywhere on the grid
2. You manually click the "Finish Session" button

## Game Strategy Tips

1. **Plan Ahead**: Try to maintain space for different block shapes
2. **Go for Combos**: Setting up multiple line clears simultaneously yields exponential points
3. **Avoid Fragmentation**: Scattered holes make it harder to place blocks
4. **Balance Vertical and Horizontal**: Don't focus only on rows or only on columns
5. **Use Big Blocks Wisely**: Large blocks can fill space quickly but reduce flexibility

## Visual Elements

### Grid Colors
- **Light Gray**: Empty cell
- **Dark Blue**: Placed block (permanent)
- **Blue**: Hover preview (shows where block will be placed)
- **Gray Borders**: Cell boundaries

### UI Elements
- **Score Display**: Top-left corner shows current score
- **Finish Session Button**: Top-right corner (red when hovering)
- **Instructions**: Bottom of screen
- **Block Selection Area**: Right side shows three available blocks

## Code Structure

### Main Components

**main.py**
- Game loop and main logic
- Event handling (mouse clicks, keyboard input)
- Game state management
- Score calculation and line clearing
- Game over detection and screen rendering

**blocks.py**
- Block base class with placement validation
- 18 different block shape classes
- BlockGenerator for random block creation
- Drawing and positioning logic

**grid.py**
- Grid class managing the 8×8 play area
- Cell state management (empty/filled/hover)
- Line clearing detection
- Mouse-to-grid coordinate conversion
- Grid drawing and visual rendering

**constants.py**
- Window dimensions and layout
- Grid configuration (size, cell size, offsets)
- Color definitions
- Block positioning constants

## Customization

### Adjust Difficulty
Edit `constants.py`:
```python
GRID_SIZE = 8  # Change grid size (8×8 standard)
CELL_SIZE = 50  # Change cell size (affects visual scale)
```

### Modify Scoring
Edit the scoring formula in `main.py`:
```python
self.score += 2 ** nr_rows * 2 ** nr_cols * 100
```

### Add New Block Shapes
In `blocks.py`, create a new class:
```python
class CustomBlock(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4  # Number of cells
        self.cells = [[0,0], [1,0], [1,1], [2,1]]  # Cell positions
```

Then add it to the `BlockGenerator.generate()` method.

## Technical Details

### Cell States
- `0`: Empty cell
- `1`: Filled cell (permanent placement)
- `2`: Hover cell (preview)

### Grid Coordinates
- Grid uses row/column indexing starting at (0,0) in top-left
- Mouse coordinates are converted to grid coordinates for placement

### Collision Detection
- Validates block placement by checking all cells are within bounds
- Ensures all target cells are empty before placement
- Provides hover preview for valid placements

## Troubleshooting

**Game won't start:**
- Ensure pygame is installed: `pip install pygame`
- Check that all Python files are in the same directory

**Blocks not placing:**
- Ensure the entire block fits on empty cells
- Check that you've selected a block first (click on it in the selection area)
- Verify the hover preview appears (blue cells) before clicking

**Score not saving:**
- Highscore saves when you quit with Q/ESC or close the window
- Make sure to exit properly rather than force-closing

**Visual glitches:**
- Try adjusting `CELL_SIZE` in constants.py
- Ensure window dimensions accommodate the grid size

## Credits

Inspired by the Block Blast mobile puzzle game with custom implementation and features.

## License

Free to use and modify for personal and educational purposes.
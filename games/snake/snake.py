import random
from collections import deque

import pygame

from games.snake.snake_grid import GridEntity, SnakeGrid, CellType

# I know this is not OOP but snake is the only one playing sound effects
# A sound playing class would be overkill
pygame.mixer.init()
sfx = [pygame.mixer.Sound('sounds/pickup_1.wav'),
      pygame.mixer.Sound('sounds/pickup_2.wav')]

def play_random_sound() -> None:
    random.choice(sfx).play()

def _add_pair(a, b):
    (x, y) = a
    (z, t) = b
    return x + z, y + t


def _convert_direction(direction):
    if direction == "UP":
        return -1, 0
    elif direction == "DOWN":
        return 1, 0
    elif direction == "LEFT":
        return 0, -1
    elif direction == "RIGHT":
        return 0, 1
    else:
        return 0, 0


class Snake(GridEntity):

    """ The snake entity

    Attributes:
        body: deque[(int, int)] the snake's body
        direction: str ("RIGHT", "LEFT", "UP", "DOWN") snake direction
    """
    def __init__(self, row: int, col: int, grid: SnakeGrid) -> None:
        self.body = deque([(row, col), (row + 1, col), (row + 2, col)])
        self.direction = "RIGHT"
        grid.set_snake_cell((row, col))
        grid.set_snake_cell((row + 1, col))
        grid.set_snake_cell((row + 2, col))
        self.length = 3


    def handle_key(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_UP and self.direction != "DOWN":
            self.direction = "UP"
        elif event.key == pygame.K_DOWN and self.direction != "UP":
            self.direction = "DOWN"
        elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
            self.direction = "RIGHT"

    def update(self, grid: SnakeGrid) -> bool:
        new_head = _add_pair(self.body[-1], _convert_direction(self.direction))
        row, col = new_head
        if row < 0 or row >= grid.blocks_per_height or col < 0 or col >= grid.blocks_per_width:
            return True
        self.body.append(new_head)
        ate = grid.get_cell(new_head) == CellType.FOOD
        if grid.get_cell(new_head) == CellType.SNAKE:
            return True
        grid.set_snake_cell(new_head)
        if not ate:
            grid.set_empty_cell(self.body.popleft())
        else:
            self.length += 1
            play_random_sound()

        return False

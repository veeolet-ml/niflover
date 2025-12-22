from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from enum import Enum
from typing import Tuple

import pygame
from pygame import Surface, Color
from pygame.typing import SequenceLike

GRID_EDGE = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class CellType(Enum):
    NOTHING = 0
    SNAKE = 1
    FOOD = 2


class GridEntity(ABC):

    @abstractmethod
    def update(self, grid: Grid) -> None:
        pass


class Grid:
    """ The grid in which the snake is drawn

    Attributes:
        width (int): The width of the grid
        height (int): The height of the grid
        blocks_per_width(int): The blocks per width of the grid
        blocks_per_height(int): The blocks per height of the grid
        grid (CellType[height][width]): The grid state
        entities (list[GridEntity]): The entities in the grid that act on it
    """

    def __init__(self, width: int, height: int, blocks_per_width: int, blocks_per_height: int):
        self.width = width
        self.height = height
        self.blocks_per_width = blocks_per_width
        self.blocks_per_height = blocks_per_height
        self.grid = [[CellType.NOTHING for _ in range(blocks_per_width)]
                     for _ in range(blocks_per_height)]
        self.entities = []

    def register_entity(self, entity: GridEntity) -> None:
        self.entities.append(entity)

    def get_block_width(self) -> int:
        return int(self.width / self.blocks_per_width)

    def get_block_height(self) -> int:
        return int(self.height / self.blocks_per_height)

    def _draw_grid(self, screen: Surface) -> None:
        for x in range(0, self.width, self.get_block_width()):
            for y in range(0, self.height, self.get_block_height()):
                rect = pygame.Rect(x, y, self.get_block_width(), self.get_block_height())
                pygame.draw.rect(screen, GRID_EDGE, rect, 1)

    def draw_square(self, screen: Surface, row: int, col: int,
                    color: Color | SequenceLike[int] | int | str) -> None:
        rect = pygame.Rect(col * self.get_block_width(),
                           row * self.get_block_height(),
                           self.get_block_width(),
                           self.get_block_height())
        pygame.draw.rect(screen, color, rect)

    def set_snake_cell(self, head: Tuple[int, int]) -> None:
        row, col = head
        self.grid[row][col] = CellType.SNAKE

    def set_empty_cell(self, cell: Tuple[int, int]) -> None:
        row, col = cell
        self.grid[row][col] = CellType.NOTHING

    def update(self) -> None:
        for entity in self.entities:
            entity.update(self)

    def draw(self, screen: Surface) -> None:
        self._draw_grid(screen)
        for row in range(self.blocks_per_height):
            for col in range(self.blocks_per_width):
                match self.grid[row][col]:
                    case CellType.FOOD: self.draw_square(screen, row, col, RED)
                    case CellType.SNAKE: self.draw_square(screen, row, col, GREEN)
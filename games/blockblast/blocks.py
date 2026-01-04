import random
from constants import *
import pygame

class Block:
    def __init__(self, cell_size, offset_x, offset_y):
        self.cellnum = 0
        self.cells = []
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.rect = pygame.Rect(offset_x, offset_y, cell_size * 3, cell_size * 3)

    def draw(self, screen):
        for [x_poz, y_poz] in self.cells:
            x = x_poz * self.cell_size + self.offset_x
            y = y_poz * self.cell_size + self.offset_y
            pygame.draw.rect(screen, BLUE,
                             (x, y, self.cell_size, self.cell_size))
            pygame.draw.rect(screen, GRAY,
                             (x, y, self.cell_size, self.cell_size), 2)

    def can_be_placed(self, grid):
        for start_row in range(grid.size):
            for start_col in range(grid.size):
                can_place = True
                for [x_poz, y_poz] in self.cells:
                    test_row = start_row + y_poz
                    test_col = start_col + x_poz

                    if not grid.is_valid_position(test_row, test_col):
                        can_place = False
                        break
                    if grid.cells[test_row][test_col] != 0 and grid.cells[test_row][test_col] != 2:
                        can_place = False
                        break

                if can_place:
                    return True
        return False


class SmallSquare(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [0, 1], [1, 0], [1, 1]]


class BigSquare(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 9
        self.cells = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]


class L1(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [0, 1], [1, 0], [2, 0]]


class L2(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [0, -1], [1, 0], [2, 0]]


class L3(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [2, 1], [1, 0], [2, 0]]


class L4(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [2, -1], [1, 0], [2, 0]]


class L5(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [1, 0], [0, 1], [0, 2]]


class L6(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [-1, 0], [0, 1], [0, 2]]


class L7(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [1, 2], [0, 1], [0, 2]]


class L8(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [-1, 2], [0, 1], [0, 2]]


class ZigZag1(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [1, 1], [0, 1], [1, 2]]


class ZigZag2(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [1, 1], [1, 0], [2, 1]]


class ZigZag3(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [0, 1], [1, 0], [-1, 1]]


class ZigZag4(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [-1, 1], [0, 1], [-1, 2]]


class Line1(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 3
        self.cells = [[0, 0], [0, 1], [0, 2]]


class Line2(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 3
        self.cells = [[0, 0], [1, 0], [2, 0]]


class Line3(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [0, 1], [0, 2], [0, 3]]


class Line4(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0], [1, 0], [2, 0], [3, 0]]


class BlockGenerator():
    def __init__(self, cell_size, offset_x):
        self.cellsize = cell_size
        self.offset_x = offset_x
        self.offset_y = 0

    def generate(self, offset_y):
        self.offset_y = offset_y
        rand = random.randint(0, 5)
        if rand == 0:
            return SmallSquare(self.cellsize, self.offset_x, self.offset_y)
        elif rand == 1:
            return BigSquare(self.cellsize, self.offset_x, self.offset_y)
        elif rand == 2:
            rand = random.randint(0, 7)
            if rand == 0:
                return L1(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 1:
                return L2(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 2:
                return L3(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 3:
                return L4(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 4:
                return L5(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 5:
                return L6(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 6:
                return L7(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 7:
                return L8(self.cellsize, self.offset_x, self.offset_y)
        elif rand == 3:
            rand = random.randint(0, 3)
            if rand == 0:
                return ZigZag1(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 1:
                return ZigZag2(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 2:
                return ZigZag3(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 3:
                return ZigZag4(self.cellsize, self.offset_x, self.offset_y)
        elif rand == 4:
            rand = random.randint(0, 1)
            if rand == 0:
                return Line1(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 1:
                return Line2(self.cellsize, self.offset_x, self.offset_y)
        elif rand == 5:
            rand = random.randint(0, 1)
            if rand == 0:
                return Line3(self.cellsize, self.offset_x, self.offset_y)
            elif rand == 1:
                return Line4(self.cellsize, self.offset_x, self.offset_y)
        return None
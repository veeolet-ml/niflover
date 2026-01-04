import pygame
from constants import *

class Grid:
    def __init__(self, size, cell_size, offset_x, offset_y):
        self.size = size
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        # 0 = empty, 1 = filled
        self.cells = [[0 for _ in range(size)] for _ in range(size)]

    def draw(self, screen):
        for row in range(self.size):
            for col in range(self.size):
                x = self.offset_x + col * self.cell_size
                y = self.offset_y + row * self.cell_size

                if self.cells[row][col] == 0:
                    pygame.draw.rect(screen, LIGHT_GRAY,
                                     (x, y, self.cell_size, self.cell_size))
                if self.cells[row][col] == 1:
                    pygame.draw.rect(screen, DARK_BLUE,
                                     (x, y, self.cell_size, self.cell_size))
                if self.cells[row][col] == 2:
                    pygame.draw.rect(screen, BLUE,
                                     (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, GRAY,
                                 (x, y, self.cell_size, self.cell_size), 2)

    def is_valid_position(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_cell_empty(self, row, col):
        if not self.is_valid_position(row, col):
            return False
        return self.cells[row][col] == 0

    def place_cell(self, row, col):
        if self.is_valid_position(row, col):
            self.cells[row][col] = 1

    def hover_cell(self, row, col):
        if self.is_valid_position(row, col):
            self.cells[row][col] = 2

    def clear_cell(self, row, col):
        if self.is_valid_position(row, col):
            self.cells[row][col] = 0

    def check_and_clear_lines(self):
        cleared_lines = 0

        # Check rows
        rows_to_clear = []
        for row in range(self.size):
            if all(self.cells[row][col] == 1 for col in range(self.size)):
                rows_to_clear.append(row)

        # Check columns
        cols_to_clear = []
        for col in range(self.size):
            if all(self.cells[row][col] == 1 for row in range(self.size)):
                cols_to_clear.append(col)

        # Clear rows
        for row in rows_to_clear:
            for col in range(self.size):
                self.cells[row][col] = 0
            cleared_lines += 1

        # Clear columns
        for col in cols_to_clear:
            for row in range(self.size):
                self.cells[row][col] = 0
            cleared_lines += 1

        return cleared_lines

    def get_cell_from_pos(self, mouse_x, mouse_y):
        """Convert mouse position to grid cell coordinates"""
        if (self.offset_x <= mouse_x <= self.offset_x + self.size * self.cell_size and
                self.offset_y <= mouse_y <= self.offset_y + self.size * self.cell_size):
            col = (mouse_x - self.offset_x) // self.cell_size
            row = (mouse_y - self.offset_y) // self.cell_size
            return row, col
        return None, None
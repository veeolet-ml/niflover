import pygame
import sys

pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 8  # 8x8 grid
CELL_SIZE = 50
GRID_OFFSET_X = 150
GRID_OFFSET_Y = 100

BLOCK_OFFSET_X = 600
BLOCK_OFFSET_Y = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
DARK_BLUE = (65, 105, 225)


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

class SmallSquare(Block):
    def __init__(self, cell_size, offset_x, offset_y):
        Block.__init__(self, cell_size, offset_x, offset_y)
        self.cellnum = 4
        self.cells = [[0, 0],[0, 1],[1, 0],[1, 1]]

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


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Block Blast")
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = Grid(GRID_SIZE, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y)
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.blocks = []
        self.blocks.append(SmallSquare(CELL_SIZE, BLOCK_OFFSET_X, BLOCK_OFFSET_Y))
        self.selected = 0

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # For testing: click to toggle cells
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = self.grid.get_cell_from_pos(mouse_x, mouse_y)
                if self.selected != 0:
                    block = self.blocks[self.selected - 1]
                    nr = 0
                    for [x_poz, y_poz] in block.cells:
                        row, col = self.grid.get_cell_from_pos(mouse_x + x_poz * CELL_SIZE, mouse_y + y_poz * CELL_SIZE)
                        if row is not None and col is not None and self.grid.is_valid_position(row, col) and self.grid.cells[row][col] == 2:
                            nr = nr + 1
                    if nr == block.cellnum:
                        for [x_poz, y_poz] in block.cells:
                            row, col = self.grid.get_cell_from_pos(mouse_x + x_poz * CELL_SIZE,
                                                                   mouse_y + y_poz * CELL_SIZE)
                            if row is not None and col is not None:
                                self.grid.place_cell(row, col)
                        self.selected = 0
                if BLOCK_OFFSET_X <= mouse_x <= BLOCK_OFFSET_X + CELL_SIZE * 3 and BLOCK_OFFSET_Y <= mouse_y <= BLOCK_OFFSET_Y + CELL_SIZE * 3:
                    self.selected = 1

            for row in range(self.grid.size):
                for col in range(self.grid.size):
                    if self.grid.cells[row][col] == 2:
                        ok = 0
                        block = self.blocks[self.selected - 1]
                        nr = 0
                        for [x_poz, y_poz] in block.cells:
                            row_hov, col_hov = self.grid.get_cell_from_pos(mouse_x + x_poz * CELL_SIZE,
                                                                   mouse_y + y_poz * CELL_SIZE)
                            if row_hov is not None and col_hov is not None and self.grid.is_valid_position(row, col) and self.grid.cells[row][col] == 0:
                                nr = nr + 1
                        for [x_poz, y_poz] in block.cells:
                            row_hov, col_hov = self.grid.get_cell_from_pos(mouse_x + x_poz * CELL_SIZE,
                                                                   mouse_y + y_poz * CELL_SIZE)
                            if row_hov == row and col_hov == col:
                                ok = 1
                        if nr < block.cellnum:
                            ok = 0
                        if ok == 0:
                            self.grid.clear_cell(row, col)

            if self.selected != 0:
                block = self.blocks[self.selected - 1]
                nr = 0
                for [x_poz, y_poz] in block.cells:
                    row, col = self.grid.get_cell_from_pos(mouse_x + x_poz * CELL_SIZE, mouse_y + y_poz * CELL_SIZE)
                    if row is not None and col is not None and self.grid.is_valid_position(row, col) and self.grid.cells[row][col] == 0:
                        nr = nr + 1
                if nr == block.cellnum:
                    print(nr)
                    for [x_poz, y_poz] in block.cells:
                        row, col = self.grid.get_cell_from_pos(mouse_x + x_poz * CELL_SIZE, mouse_y + y_poz * CELL_SIZE)
                        if row is not None and col is not None:
                            self.grid.hover_cell(row, col)
    def draw(self):
        """Draw everything"""
        self.screen.fill(WHITE)

        # Draw grid
        self.grid.draw(self.screen)

        # Draw block
        for block in self.blocks:
            block.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 20))

        # Draw instructions
        instruction_font = pygame.font.Font(None, 24)
        instruction_text = instruction_font.render("Click cells to toggle (testing mode)", True, GRAY)
        self.screen.blit(instruction_text, (20, WINDOW_HEIGHT - 40))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
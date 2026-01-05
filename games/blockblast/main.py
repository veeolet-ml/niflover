import pygame
import sys
import requests
from constants import *
from blocks import *
from grid import *

pygame.init()

highscore = 0

class Game:
    def __init__(self):
        global highscore
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Block Blast")
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = Grid(GRID_SIZE, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y)
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.generator = BlockGenerator(CELL_SIZE, BLOCK_OFFSET_X)
        self.blocks = []
        self.blocks.append(self.generator.generate(BLOCK_OFFSET_Y))
        self.blocks.append(self.generator.generate(BLOCK_OFFSET2_Y))
        self.blocks.append(self.generator.generate(BLOCK_OFFSET3_Y))

        self.selected = 0
        self.game_over = False

        # Finish Session button
        self.finish_button = pygame.Rect(WINDOW_WIDTH - 200, 20, 180, 50)

    def check_game_over(self):
        for block in self.blocks:
            if block.can_be_placed(self.grid):
                return False
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # If game over, check for restart
            if self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.running = False
                continue

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.finish_button.collidepoint(mouse_x, mouse_y):
                    self.game_over = True
                    continue

                row, col = self.grid.get_cell_from_pos(mouse_x, mouse_y)
                if self.selected != 0:
                    block = self.blocks[self.selected - 1]
                    nr = 0
                    for [x_poz, y_poz] in block.cells:
                        row, col = self.grid.get_cell_from_pos(mouse_x + x_poz * CELL_SIZE, mouse_y + y_poz * CELL_SIZE)
                        if row is not None and col is not None and self.grid.is_valid_position(row, col) and \
                                self.grid.cells[row][col] == 2:
                            nr = nr + 1
                    if nr == block.cellnum:
                        for [x_poz, y_poz] in block.cells:
                            row, col = self.grid.get_cell_from_pos(mouse_x + x_poz * CELL_SIZE,
                                                                   mouse_y + y_poz * CELL_SIZE)
                            if row is not None and col is not None:
                                self.grid.place_cell(row, col)

                        # Generate new block
                        if (self.selected == 1):
                            self.blocks[self.selected - 1] = self.generator.generate(BLOCK_OFFSET_Y)
                        if (self.selected == 2):
                            self.blocks[self.selected - 1] = self.generator.generate(BLOCK_OFFSET2_Y)
                        if (self.selected == 3):
                            self.blocks[self.selected - 1] = self.generator.generate(BLOCK_OFFSET3_Y)

                        self.selected = 0

                if BLOCK_OFFSET_X <= mouse_x <= BLOCK_OFFSET_X + CELL_SIZE * 3 and BLOCK_OFFSET_Y <= mouse_y <= BLOCK_OFFSET_Y + CELL_SIZE * 3:
                    self.selected = 1
                if BLOCK_OFFSET_X <= mouse_x <= BLOCK_OFFSET_X + CELL_SIZE * 3 and BLOCK_OFFSET2_Y <= mouse_y <= BLOCK_OFFSET2_Y + CELL_SIZE * 3:
                    self.selected = 2
                if BLOCK_OFFSET_X <= mouse_x <= BLOCK_OFFSET_X + CELL_SIZE * 3 and BLOCK_OFFSET3_Y <= mouse_y <= BLOCK_OFFSET3_Y + CELL_SIZE * 3:
                    self.selected = 3

            for row in range(self.grid.size):
                for col in range(self.grid.size):
                    if self.grid.cells[row][col] == 2:
                        ok = 0
                        block = self.blocks[self.selected - 1]
                        nr = 0
                        for [x_poz, y_poz] in block.cells:
                            row_hov, col_hov = self.grid.get_cell_from_pos(mouse_x + x_poz * CELL_SIZE,
                                                                           mouse_y + y_poz * CELL_SIZE)
                            if row_hov is not None and col_hov is not None and self.grid.is_valid_position(row, col) and \
                                    self.grid.cells[row][col] == 0:
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
                    if row is not None and col is not None and self.grid.is_valid_position(row, col) and \
                            self.grid.cells[row][col] == 0:
                        nr = nr + 1
                if nr == block.cellnum:
                    for [x_poz, y_poz] in block.cells:
                        row, col = self.grid.get_cell_from_pos(mouse_x + x_poz * CELL_SIZE, mouse_y + y_poz * CELL_SIZE)
                        if row is not None and col is not None:
                            self.grid.hover_cell(row, col)

            rows_to_clear = []
            cols_to_clear = []
            for row in range(self.grid.size):
                nr = 0
                for col in range(self.grid.size):
                    if self.grid.cells[row][col] == 1:
                        nr = nr + 1
                if nr == GRID_SIZE:
                    rows_to_clear.append(row)
            for col in range(self.grid.size):
                nr = 0
                for row in range(self.grid.size):
                    if self.grid.cells[row][col] == 1:
                        nr = nr + 1
                if nr == GRID_SIZE:
                    cols_to_clear.append(col)
            nr_rows = 0
            nr_cols = 0
            for row in rows_to_clear:
                for col in range(self.grid.size):
                    self.grid.clear_cell(row, col)
                nr_rows = nr_rows + 1
            for col in cols_to_clear:
                for row in range(self.grid.size):
                    self.grid.clear_cell(row, col)
                nr_cols = nr_cols + 1
            if nr_rows != 0 or nr_cols != 0:
                self.score += 2 ** nr_rows * 2 ** nr_cols * 100
            if self.check_game_over():
                self.game_over = True

    def draw_game_over(self):
        global highscore
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        if highscore < self.score:
            highscore = self.score

        game_over_text = self.big_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        highscore_text = self.font.render(f"HighScore: {highscore}", True, WHITE)
        highscore_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(highscore_text, highscore_rect)

        restart_text = self.font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.font.render("Press ESC to Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
        self.screen.blit(quit_text, quit_rect)

    def draw(self):
        self.screen.fill(WHITE)

        self.grid.draw(self.screen)

        for block in self.blocks:
            block.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 20))

        mouse_pos = pygame.mouse.get_pos()
        button_color = RED if self.finish_button.collidepoint(mouse_pos) else DARK_BLUE
        pygame.draw.rect(self.screen, button_color, self.finish_button, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, self.finish_button, 3, border_radius=10)

        button_font = pygame.font.Font(None, 28)
        button_text = button_font.render("Finish Session", True, WHITE)
        button_text_rect = button_text.get_rect(center=self.finish_button.center)
        self.screen.blit(button_text, button_text_rect)

        instruction_font = pygame.font.Font(None, 24)
        instruction_text = instruction_font.render("Click and place blocks", True, GRAY)
        self.screen.blit(instruction_text, (20, WINDOW_HEIGHT - 40))

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

        url = 'http://localhost:5000/game/submit_score'
        payload = {
            'score': highscore,
            'slug': 'blockblast',
            'username': 'gigelinho'
        }

        requests.post(url, json=payload)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
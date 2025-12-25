import random
from enum import Enum

import pygame

from games.snake.HUD import HUD
from games.snake.food_manager import FoodManager
from games.snake.score_manager import ScoreManager
from games.snake.snake_grid import SnakeGrid
from games.snake.snake import Snake

BLACK = (0, 0, 0)

MILLISECONDS_PER_STEP = 500

WIDTH = 1600
HEIGHT = 900




class GameState(Enum):
    START_GAME = 0
    GAME_RUNNING = 1
    GAME_OVER = 2


class SnakeGame:

    def __init__(self):
        self.events = None
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = SnakeGrid(self.screen.get_width(), int(self.screen.get_height() * 4 / 5),
                              50, 20)
        rand_col = random.randint(10, self.grid.blocks_per_width - 10)
        rand_row = random.randint(5, self.grid.blocks_per_height - 5)
        self.snake = Snake(rand_row, rand_col, self.grid)
        self.grid.register_entity(self.snake)
        self.food_manager = FoodManager(1)
        self.grid.register_entity(self.food_manager)
        self.score_manager = ScoreManager(self.snake)
        self.delta = 0
        self.game_state = GameState.START_GAME

        self.hud = HUD(self.screen)

    def reset_game(self):
        self.grid = SnakeGrid(self.screen.get_width(), int(self.screen.get_height() * 4 / 5),
                              50, 20)
        rand_col = random.randint(10, self.grid.blocks_per_width - 10)
        rand_row = random.randint(5, self.grid.blocks_per_height - 5)
        self.snake = Snake(rand_row, rand_col, self.grid)
        self.grid.register_entity(self.snake)
        self.food_manager = FoodManager(1)
        self.grid.register_entity(self.food_manager)
        self.score_manager = ScoreManager(self.snake)
        self.delta = 0


    def _pre_frame_prep(self) -> None:
        """Common actions before starting frame step calculations"""

        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill(BLACK)

    def _post_frame_display(self) -> None:
        """Displays on screen and adds to ms delta"""

        # flip() the display to put your work on screen
        pygame.display.flip()

        dt = self.clock.tick(60)  # limits FPS to 60 and gets ms delta
        self.delta += dt

    def run(self) -> None:

        while self.running:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

            self._pre_frame_prep()

            match self.game_state:
                case GameState.START_GAME:
                    self.start_game()
                case GameState.GAME_RUNNING:
                    self.run_game()
                case GameState.GAME_OVER:
                    self.game_over()

            self._post_frame_display()

        pygame.quit()


    def start_game(self):
        self.hud.draw_start()
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.game_state = GameState.GAME_RUNNING

    def run_game(self) -> None:
        """Corresponds to GAME_RUNNING state"""

        advance = False
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                self.snake.handle_key(event)
                advance = True
        # superfast mode
        if pygame.key.get_pressed()[pygame.K_e]:
            advance = True

        if self.delta > MILLISECONDS_PER_STEP or advance:
            game_over = self.grid.update()
            if game_over:
                self.game_state = GameState.GAME_OVER
            self.delta = 0
            self.score_manager.update()

        self.grid.draw(self.screen)
        self.score_manager.draw(self.screen)

        self._post_frame_display()

    def game_over(self) -> None:
        self.hud.draw_game_over()
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                if event.key == pygame.K_r:
                    self.reset_game()
                    self.game_state = GameState.GAME_RUNNING


def main():
    SnakeGame().run()



if __name__ == "__main__":
    exit(main())


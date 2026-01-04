import random
from enum import Enum

import pygame
from pygame_textinput import TextInputVisualizer

from HUD import HUD
from food_manager import FoodManager
from score_manager import ScoreManager
from snake_grid import SnakeGrid
from snake import Snake

BLACK = (0, 0, 0)

MILLISECONDS_PER_STEP = 500

WIDTH = 1600
HEIGHT = 900




class GameState(Enum):
    START_GAME = 0
    GAME_RUNNING = 1
    GAME_OVER = 2
    INPUT_USERNAME = 3


class SnakeGame:

    def __init__(self, food_items: int, server_address: str = "localhost:8080") -> None:
        self.server_address = server_address
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
        self.food_manager = FoodManager(food_items)
        self.grid.register_entity(self.food_manager)
        self.score_manager = ScoreManager(self.snake)
        self.delta = 0
        self.game_state = GameState.START_GAME

        self.hud = HUD(self.screen, self.score_manager)

        pygame.mixer.init()
        pygame.mixer.music.load("sounds/retro-arcade-game-music.mp3")

        pygame.key.set_repeat(200, 50)

        self.username_visualiser = TextInputVisualizer(font_object=self.hud.font_small,
                                                       font_color=(255, 255, 255))
        self.password_visualiser = TextInputVisualizer(font_object=self.hud.font_small,
                                                       font_color=(255, 255, 255))

    def reset_game(self) -> None:
        self.grid = SnakeGrid(self.screen.get_width(), int(self.screen.get_height() * 4 / 5),
                              50, 20)
        rand_col = random.randint(10, self.grid.blocks_per_width - 10)
        rand_row = random.randint(5, self.grid.blocks_per_height - 5)
        self.snake = Snake(rand_row, rand_col, self.grid)
        self.grid.register_entity(self.snake)
        food_items = self.food_manager.original_food_items
        self.food_manager = FoodManager(food_items)
        self.grid.register_entity(self.food_manager)
        high_score = self.score_manager.high_score
        self.score_manager = ScoreManager(self.snake, high_score=high_score)
        self.hud = HUD(self.screen, self.score_manager)
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
        self.hud.update(dt)  # Update HUD color fading

    def run(self) -> None:
        pygame.mixer.music.play(loops=-1)
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
                case GameState.INPUT_USERNAME:
                    self.input_username()

            self._post_frame_display()

        pygame.quit()


    def start_game(self) -> None:
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
        self.hud.draw_running()

    def game_over(self) -> None:
        self.hud.draw_game_over()
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                if event.key == pygame.K_r:
                    self.reset_game()
                    self.game_state = GameState.GAME_RUNNING
                if event.key == pygame.K_SPACE:
                    self.game_state = GameState.INPUT_USERNAME

    def input_username(self) -> None:
        self.hud.draw_input_username()
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state = GameState.GAME_OVER
                    self.submit_results()
        self.username_visualiser.update(self.events)
        input_rect = self.username_visualiser.surface.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(self.username_visualiser.surface, input_rect)


    def submit_results(self) -> None:
        """TODO: add POST request to submit results when database api is finished"""
        print(f"Submitting to server: {self.server_address}")
        print(f"Username: {self.username_visualiser.manager.value}")
        print(f"High score: {self.score_manager.high_score}")





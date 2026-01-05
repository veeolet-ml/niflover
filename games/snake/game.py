import random
from enum import Enum
import requests

import pygame

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

class SnakeGame:

    def __init__(self, food_items: int, server_address: str = "localhost:5000", username: str = "") -> None:
        self.server_address = server_address
        self.username = username
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
        pygame.mixer.music.set_volume(0.05)
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
                    self.submit_results()



    def submit_results(self) -> None:
        print(f"Submitting to server: {self.server_address}")
        print(f"Username: {self.username}")
        print(f"High score: {self.score_manager.high_score}")

        url = f"http://{self.server_address}/game/submit_score"
        payload = {
            "slug": "snake",
            "score": self.score_manager.high_score,
            "username": self.username
        }

        requests.post(url, json=payload)

import pygame

from games.snake.snake import Snake


class ScoreManager:

    """ Class that holds the current score and displays it

    Attributes:
        snake: Snake the snake
        score: int Current score
    """
    def __init__(self, snake: Snake):
        self.snake = snake
        self.score = 0
        self.font = pygame.font.SysFont("monospace", 50)

    def update(self) -> None:
        self.score = self.snake.length

    def draw(self, screen: pygame.Surface) -> None:
        left = screen.width * 4 // 5
        right = screen.width
        top = screen.height * 4 // 5
        bottom = screen.height

        text_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(text_surface, (left, top))
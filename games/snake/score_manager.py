import pygame
from pygame.display import update

from snake import Snake


class ScoreManager:

    """ Class that holds the current score and displays it

    Attributes:
        snake: Snake the snake
        score: int Current score
        high_score: int High score
    """
    def __init__(self, snake: Snake, high_score: int = 0) -> None:
        self.snake = snake
        self.score = 0
        self.high_score = high_score
        update()

    def update(self) -> None:
        self.score = self.snake.length
        if self.score > self.high_score:
            self.high_score = self.score


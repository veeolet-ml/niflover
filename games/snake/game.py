import random

import pygame

from grid import Grid
from snake import Snake

BLACK = (0, 0, 0)

MILLISECONDS_PER_STEP = 500


def main():
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    clock = pygame.time.Clock()
    running = True
    grid = Grid(screen.get_width(), int(screen.get_height() * 4 / 5), 50, 20)
    rand_col = random.randint(10, grid.blocks_per_width - 10)
    rand_row = random.randint(5, grid.blocks_per_height - 5)
    snake = Snake(rand_row, rand_col, grid)
    grid.register_entity(snake)

    delta = 0
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        advance = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                snake.handle_key(event)
                advance = True


        # fill the screen with a color to wipe away anything from last frame
        screen.fill(BLACK)

        if delta > MILLISECONDS_PER_STEP or advance:
            grid.update()
            delta = 0

        grid.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        dt = clock.tick(60)  # limits FPS to 60 and gets ms delta
        delta += dt

    pygame.quit()



if __name__ == "__main__":
    exit(main())


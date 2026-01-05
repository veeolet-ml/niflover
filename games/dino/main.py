import pygame
import random
import requests
from dinosaur import Dinosaur
from constants import *

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", default="")
    parser.add_argument("-s", "--server", default="localhost:5000")
    return parser.parse_args()

ARGS = parse_args()

SERVER = ARGS.server.strip() or "localhost:5000"

USERNAME = ARGS.username.strip()

pygame.init()


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 30, 30)
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.left < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, 0)
        self.rect.y = random.randint(200, 300)
        self.index = 0

        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width - 3, self.rect.height - 3)

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x <= -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Projectile:
    PROJECTILE_VEL = 5

    def __init__(self, player):
        self.x = player.dino_rect.x + 35
        self.y = player.dino_rect.y
        self.image = PROJECTILE
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.width = self.image.get_width()

    def update(self):
        self.x += 10
        self.rect.x += 10

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


def main():
    global game_speed, x_pos_bg, y_pos_bg, obstacles, projectiles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    cloud = Cloud()
    global points, number_projectiles
    points = 0
    number_projectiles = 0
    obstacles = []
    projectiles = []
    font = pygame.font.SysFont("freesansbold.ttf", 40)

    def score():
        global points, game_speed, number_projectiles
        points += 1
        if points % 100 == 0:
            game_speed += 1
        if points % 200 == 0:
            number_projectiles += 1
        text = font.render("Score: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

        cnt = font.render("Projectiles: " + str(number_projectiles), True, (0, 0, 0))
        cntRect = cnt.get_rect()
        cntRect.center = (500, 40)
        SCREEN.blit(cnt, cntRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg < -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x and number_projectiles > 0:
                    projectiles.append(Projectile(player))
                    number_projectiles -= 1
        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                return True

        for projectile in projectiles[:]:
            projectile.update()
            hit = False
            for obstacle in obstacles[:]:
                if projectile.rect.colliderect(obstacle.rect):
                    if obstacle in obstacles:
                        obstacles.remove(obstacle)
                    if projectile in projectiles:
                        projectiles.remove(projectile)
                        hit = True
                        break
            if not hit and projectile in projectiles:
                projectile.draw(SCREEN)
                if projectile.x > SCREEN_WIDTH:
                    projectiles.remove(projectile)

        background()
        score()

        player.draw(SCREEN)
        player.update(userInput)

        cloud.draw(SCREEN)
        cloud.update()

        clock.tick(30)
        pygame.display.update()


def menu(deathcount):
    global points
    global highscore
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.SysFont("freesansbold.ttf", 40)

        if deathcount == 0:
            text = font.render("Press any key to start", True, (0, 0, 0))
        elif deathcount > 0:
            text = font.render("Press any key to restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()

            if points > highscore:
                highscore = points

            highscoreText = font.render("Your HighScore: " + str(highscore), True, (0, 0, 0))
            highscoreRect = highscoreText.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            highscoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

            SCREEN.blit(score, scoreRect)
            SCREEN.blit(highscoreText, highscoreRect)

            # Add quit instruction
            quit_text = font.render("Press Q to Quit", True, (0, 0, 0))
            quit_rect = quit_text.get_rect()
            quit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
            SCREEN.blit(quit_text, quit_rect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 120))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    url = f'http://{SERVER}/game/submit_score'
                    payload = {
                        'score': highscore,
                        'slug': 'dino',
                        'username': USERNAME
                    }

                    requests.post(url, json=payload)
                    pygame.quit()
                    return False
                return True
    return False


highscore = 0
deathcount = 0
while True:
    if menu(deathcount):
        restart = main()
        if restart:
            deathcount += 1
        else:
            break
    else:
        break
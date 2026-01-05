import os
import pygame

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RUNNING = [
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Dino", "DinoRun2.png"))
]
JUMPING = pygame.image.load(os.path.join(BASE_DIR, "Assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Dino", "DinoDuck2.png"))
]
SMALL_CACTUS = [
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Cactus", "SmallCactus3.png"))
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Cactus", "LargeCactus3.png"))
]
BIRD = [
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join(BASE_DIR, "Assets/Bird", "Bird2.png"))
]
CLOUD = pygame.image.load(os.path.join(BASE_DIR, "Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join(BASE_DIR, "Assets/Other", "Track.png"))
PROJECTILE = pygame.image.load(os.path.join(BASE_DIR, "Assets/Other", "Projectile.png"))
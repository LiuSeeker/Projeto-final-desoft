import pygame
import random

WIDTH = 1024
HEIGHT = 768
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,255)
LIGHTGREY = (50,50,50)
DARKGREY = (100,100,100)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(DARKGREY)
    pygame.display.flip()

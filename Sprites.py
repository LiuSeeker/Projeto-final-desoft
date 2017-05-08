import pygame
from setting import *


class Monstro(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.image = pygame.Surface((TILESIZE,TILESIZE)) #tamanho da imagem
        self.image.fill(RED)
        self.rect = self.image.get_rect() 
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x/TILESIZE
        self.y = y/TILESIZE

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0 
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Parede(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.paredes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*TILESIZE
        self.rect.y = y*TILESIZE
import pygame
from setting import *


class Monstro(pygame.sprite.Sprite):
    def __init__(self, game, x, y, cor):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.image = pygame.Surface((TILESIZE,TILESIZE)) #tamanho da imagem
        self.image.fill(cor)
        self.rect = self.image.get_rect() 
        self.x = x
        self.y = y

    def move(self, dx = 0, dy = 0):
        if not self.colisao(dx,dy):
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

    def colisao(self,dx=0,dy=0):
        for parede in self.game.paredes:
            if parede.x == self.x + dx and parede.y == self.y + dy:
                return True
        for sprite in self.game.all_sprites:
            if sprite.x == self.x + dx and sprite.y == self.y + dy:
                return True  
    


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        if not self.colisao(dx,dy):
            self.x += dx
            self.y += dy

    def colisao(self,dx=0,dy=0):
        for parede in self.game.paredes:
            if parede.x == self.x + dx and parede.y == self.y + dy:
                return True
        for sprite in self.game.all_sprites:
            if sprite.x == self.x + dx and sprite.y == self.y + dy:
                return True    
        return False


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
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
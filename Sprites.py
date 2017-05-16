import pygame
from os import path
from setting import *


class Monstro(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tipo):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.img_dir = path.join(path.dirname(__file__), "sprites\monstro")
        self.tipos = {"snake": 15}
        self.imagens = [tipo+"f.png", tipo+"l.png", tipo+"r.png", tipo+"b.png"]
        self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.imagens[0])).convert_alpha(), (self.tipos["snake"],TILESIZE))
        #self.image = pygame.Surface((TILESIZE,TILESIZE)) #tamanho da imagem
        #self.image.fill(cor)
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
        self.img_dir = path.join(path.dirname(__file__), "sprites\soldier")
        self.imagens = ["soldierf.png", "soldierl.png", "soldierr.png", "soldierb.png"]
        self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.imagens[0])).convert_alpha(), (25,TILESIZE))
        #self.image = pygame.Surface((TILESIZE, TILESIZE))
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y

    def get_keys(self):
        self.vx = 0
        self.vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.vx = -VEL_JOGADOR
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.imagens[1])).convert_alpha(), (25,TILESIZE))
        if keys[pygame.K_d]:
            self.vx = VEL_JOGADOR
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.imagens[2])).convert_alpha(), (25,TILESIZE))
        if keys[pygame.K_w]:
            self.vy = -VEL_JOGADOR
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.imagens[3])).convert_alpha(), (25,TILESIZE))
        if keys[pygame.K_s]:
            self.vy = VEL_JOGADOR
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.imagens[0])).convert_alpha(), (25,TILESIZE))
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def colisao_parede(self, dir):
        if dir == 'x':
            colisao = pygame.sprite.spritecollide(self,self.game.paredes,False)
            if colisao:
                if self.vx > 0:
                    self.x = colisao[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = colisao[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            colisao = pygame.sprite.spritecollide(self,self.game.paredes,False)
            if colisao:
                if self.vy > 0:
                    self.y = colisao[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = colisao[0].rect.bottom 
                self.vy = 0
                self.rect.y = self.y


    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.colisao_parede('x')
        self.rect.y = self.y
        self.colisao_parede('y')
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
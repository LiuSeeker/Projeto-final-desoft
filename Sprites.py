import pygame
from os import path
from setting import *
from random import randint


class Monstro(pygame.sprite.Sprite):
    def __init__(self, tela, x, y, tipo):
        self.groups = tela.all_sprites
        self.groups = tela.visiveis
        self.groups = tela.monstros
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.img_dir = path.join(path.dirname(__file__), "sprites\monstro")
        self.tipos = {"snake": 15}
        self.imagens = [tipo+"f.png", tipo+"l.png", tipo+"r.png", tipo+"b.png"]
        self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.imagens[0])).convert_alpha(), (self.tipos["snake"],TILESIZE))
        self.rect = self.image.get_rect() 
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.count = 0 

    def muda_vel(self):
        self.vx = 0
        self.vy = 0
        self.vx = randint(-VEL_MONSTRO, VEL_MONSTRO)
        self.vy = randint(-VEL_MONSTRO, VEL_MONSTRO)
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def move(self):
        if self.count <= 500:
            self.x += self.vx * self.tela.dt
            self.y += self.vy * self.tela.dt
            self.rect.x = self.x
            self.colisao_parede('x')
            self.colisao_player('x')
            self.rect.y = self.y
            self.colisao_parede('y')
            self.colisao_player('y')
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0 
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            self.count += 1
        else:
            self.muda_vel()
            self.count = 0

    def colisao_parede(self, dir):
        if dir == 'x':
            colisao = pygame.sprite.spritecollide(self,self.tela.paredes,False)
            if colisao:
                if self.vx > 0:
                    self.x = colisao[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = colisao[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            colisao = pygame.sprite.spritecollide(self,self.tela.paredes,False)
            if colisao:
                if self.vy > 0:
                    self.y = colisao[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = colisao[0].rect.bottom 
                self.vy = 0
                self.rect.y = self.y

    def colisao_player(self, dir):
        if dir == 'x':
            colisao = pygame.sprite.spritecollide(self,self.tela.players,False)
            if colisao:
                if self.vx > 0:
                    self.x = colisao[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = colisao[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            colisao = pygame.sprite.spritecollide(self,self.tela.players,False)
            if colisao:
                if self.vy > 0:
                    self.y = colisao[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = colisao[0].rect.bottom 
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.move()
    


class Player(pygame.sprite.Sprite):
    def __init__(self, tela, x, y):
        self.groups = tela.all_sprites
        self.groups = tela.visiveis
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.img_dir = path.join(path.dirname(__file__), "sprites\soldier")
        self.imagens = ["soldierf.png", "soldierl.png", "soldierr.png", "soldierb.png"]
        self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.imagens[0])).convert_alpha(), (25,TILESIZE))
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
        colisao = pygame.sprite.spritecollide(self,self.tela.paredes,False)
        if colisao:
            if dir == 'x':
                if self.vx > 0:
                    self.x = colisao[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = colisao[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            if dir == 'y':
                if self.vy > 0:
                    self.y = colisao[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = colisao[0].rect.bottom 
                self.vy = 0
                self.rect.y = self.y

    def colisao_monstro(self, dir):
        colisao = pygame.sprite.spritecollide(self,self.tela.monstros,False)
        if colisao:
            if dir == 'x':
                if self.vx > 0:
                    self.x = colisao[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = colisao[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            if dir == 'y':
                if self.vy > 0:
                    self.y = colisao[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = colisao[0].rect.bottom 
                self.vy = 0
                self.rect.y = self.y


    def update(self):
        self.get_keys()
        self.x += self.vx * self.tela.dt
        self.y += self.vy * self.tela.dt
        self.colisao_parede('x')
        self.colisao_monstro('x')
        self.rect.x = self.x
        self.colisao_parede('y')
        self.colisao_monstro('y')
        self.rect.y = self.y
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0 
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Parede(pygame.sprite.Sprite):
    def __init__(self, tela, x, y):
        self.groups = tela.all_sprites, tela.paredes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
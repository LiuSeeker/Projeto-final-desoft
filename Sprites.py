import pygame
from os import path
from setting import *
from random import randint

vec = pygame.math.Vector2


class Monstro(pygame.sprite.Sprite):
    def __init__(self, tela, x, y, tipo):
        self.groups = tela.all_sprites, tela.monstros, tela.visiveis
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.tipo = tipo
        self.img_dir = path.join(path.dirname(__file__), "sprites\monstro")
        self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["f"])).convert_alpha(), (self.tipo["width"],self.tipo["height"]))
        self.rect = self.image.get_rect() 
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx = 0
        self.vy = 0
        self.count = 0 

    def muda_vel(self):
        self.vx = 0
        self.vy = 0
        self.vx = randint(-self.tipo["vel"], self.tipo["vel"])
        self.vy = randint(-self.tipo["vel"], self.tipo["vel"])
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def move(self):
        if self.count <= self.tipo["count"]:
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
    def __init__(self, tela, x, y, tipo):
        self.groups = tela.all_sprites, tela.players, tela.visiveis
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.tipo = tipo
        self.img_dir = path.join(path.dirname(__file__), "sprites\soldier")
        self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["f"])).convert_alpha(), (self.tipo["width"],self.tipo["height"]))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rot = 0
        self.last_melee = 0
        self.melee_cd = 200

    def get_keys(self):
        self.vx = 0
        self.vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.vx = -self.tipo["vel"]
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["l"])).convert_alpha(), (self.tipo["width"], self.tipo["height"]))
            self.dir = 90
        if keys[pygame.K_d]:
            self.vx = self.tipo["vel"]
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["r"])).convert_alpha(), (self.tipo["width"], self.tipo["height"]))
            self.dir = 0
        if keys[pygame.K_w]:
            self.vy = -self.tipo["vel"]
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["b"])).convert_alpha(), (self.tipo["width"], self.tipo["height"]))
            self.dir = 180
        if keys[pygame.K_s]:
            self.vy = self.tipo["vel"]
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["f"])).convert_alpha(), (self.tipo["width"], self.tipo["height"]))
            self.dir = -90
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            self.vx *= 0.5
            self.vy *= 0.5
            if now - self.last_melee > self.melee_cd:
                self.last_melee = now
                dir = vec(1,0).rotate(-self.rot)
                Melee(self.tela, (self.x + self.tipo["width"]/2, self.y + 3*TILESIZE/2), dir)

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
        self.rect.x = self.x
        self.colisao_parede('x')
        self.colisao_monstro('x')
        self.rect.y = self.y
        self.colisao_parede('y')
        self.colisao_monstro('y')
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

class Melee(pygame.sprite.Sprite):
    def __init__(self, tela, pos, dir):
        self.groups = tela.all_sprites, tela.ataques, tela.visiveis
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        #self.img_dir = path.join(path.dirname(__file__), "sprites\monstro")
        #self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["f"])).convert_alpha(), (self.tipo["width"],self.tipo["height"]))
        self.rect = self.image.get_rect() 
        self.pos = vec(pos)
        self.rect.center = pos
        self.speed_melee = 50
        self.vel = dir * self.speed_melee
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 10

    def update(self):
        self.pos += self.vel * self.tela.dt
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
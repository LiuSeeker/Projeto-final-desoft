import pygame
from os import path
from setting import *
from random import randint

vec = pygame.math.Vector2

class Monstro_seguidor(pygame.sprite.Sprite):
    def __init__(self, tela, x, y, tipo):
        self.groups = tela.all_sprites, tela.monstros, tela.visiveis
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.tipo = tipo
        self.img_dir = path.join(path.dirname(__file__), "sprites\monstro")
        self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["f"])).convert_alpha(), (self.tipo["width"],self.tipo["height"]))
        self.rect = self.image.get_rect() 
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.vida = self.tipo["vida"]

    def update(self):
        self.rot = (self.tela.player.pos - self.pos).angle_to(vec(1, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(self.tipo["vel"], 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.tela.dt
        self.pos += self.vel *self.tela.dt + 0.5 * self.acc * self.tela.dt ** 2
        self.rect.center = self.pos


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
        self.vida = self.tipo["vida"]

    def muda_vel(self):
        self.vx = 0
        self.vy = 0
        self.vx = randint(-self.tipo["vel"], self.tipo["vel"])
        self.vy = randint(-self.tipo["vel"], self.tipo["vel"])
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        if self.vx > 0:
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["r"])).convert_alpha(), (self.tipo["width"],self.tipo["height"]))
        if self.vx < 0:
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["l"])).convert_alpha(), (self.tipo["width"],self.tipo["height"]))
        if self.vy > 0:
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["f"])).convert_alpha(), (self.tipo["width"],self.tipo["height"]))
        if self.vy < 0:
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["b"])).convert_alpha(), (self.tipo["width"],self.tipo["height"]))
        
    def move_aleatorio(self):
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

    def colisao_player(self, dir):
        colisao = pygame.sprite.spritecollide(self,self.tela.players,False)
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

    def acerto(self):
        self.hits = pygame.sprite.groupcollide(self.tela.monstros, self.tela.ataques, False, False)
        for hit in self.hits:
                print(self.tela.player.tipo["dano"])
                hit.vida -= self.tela.player.tipo["dano"]

    def update(self):
        self.move_aleatorio()
        self.acerto()
        if self.vida <= 0:
            self.kill()
    

class Player(pygame.sprite.Sprite):
    def __init__(self, tela, x, y, tipo):
        self.groups = tela.all_sprites, tela.players, tela.visiveis
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.tipo = tipo
        self.img_dir = path.join(path.dirname(__file__), "sprites\soldier")
        self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["f"])).convert_alpha(), (self.tipo["width"],self.tipo["height"]))
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = (x,y)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.direcao = 0
        self.last_melee = 0
        self.melee_cd = 600
        self.in_mapr = True
        self.in_mapl = True
        self.in_mapu = True
        self.in_mapd = True


    def get_keys(self):
        self.vx = 0
        self.vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.vx = -self.tipo["vel"]
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["l"])).convert_alpha(), (self.tipo["width"], self.tipo["height"]))
            self.direcao = (-1, 0)
        if keys[pygame.K_d]:
            self.vx = self.tipo["vel"]
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["r"])).convert_alpha(), (self.tipo["width"], self.tipo["height"]))
            self.dir = self.x + self.tipo["width"]/2, self.y + 3*TILESIZE/2
            self.direcao = (1, 0)
        if keys[pygame.K_w]:
            self.vy = -self.tipo["vel"]
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["b"])).convert_alpha(), (self.tipo["width"], self.tipo["height"]))
            self.direcao = (0, -1)
        if keys[pygame.K_s]:
            self.vy = self.tipo["vel"]
            self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, self.tipo["f"])).convert_alpha(), (self.tipo["width"], self.tipo["height"]))
            self.direcao = (0, 1)
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        if keys[pygame.K_SPACE]:
            self.vx *= 0.75
            self.vy *= 0.75
            now = pygame.time.get_ticks()
            if now - self.last_melee > self.melee_cd:
                self.last_melee = now
                Melee_acao(self.tela, (self.x + self.tipo["width"]/2 + self.direcao[0] * TILESIZE, self.y + self.tipo["height"] /2 + self.direcao[1] * TILESIZE))
                Melee_imagem(self.tela, (self.x + self.tipo["width"]/2 + self.direcao[0] * TILESIZE, self.y + self.tipo["height"] /2 + self.direcao[1] * TILESIZE))

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

    def colisao_trans(self):
        colisaor = pygame.sprite.spritecollide(self,self.tela.transr,False)
        colisaol = pygame.sprite.spritecollide(self,self.tela.transl,False)
        colisaou = pygame.sprite.spritecollide(self,self.tela.transu,False)
        colisaod = pygame.sprite.spritecollide(self,self.tela.transd,False)
        if colisaor:
            self.in_mapr = False
        if colisaol:
            self.in_mapl = False
        if colisaou:
            self.in_mapu = False
        if colisaod:
            self.in_mapd = False

    def update(self):
        self.get_keys()
        self.x += self.vx * self.tela.dt
        self.y += self.vy * self.tela.dt
        self.pos = (self.x, self.y)
        self.rect.x = self.x
        self.colisao_parede('x')
        self.colisao_monstro('x')
        self.rect.y = self.y
        self.colisao_parede('y')
        self.colisao_monstro('y')
        self.colisao_trans()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.x -= self.vx * self.tela.dt
        if self.rect.left < 0:
            self.rect.left = 0
            self.x -= self.vx * self.tela.dt
        if self.rect.top < 0:
            self.rect.top = 0
            self.y -= self.vy * self.tela.dt
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.y -= self.vy * self.tela.dt


class Parede(pygame.sprite.Sprite):
    def __init__(self, tela, x, y):
        self.groups = tela.all_sprites, tela.paredes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.image = pygame.Surface((TILESIZE, TILESIZE/3))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE + TILESIZE * 0.2

class Transicao_right(pygame.sprite.Sprite):
    def __init__(self, tela, x, y):
        self.groups = tela.all_sprites, tela.transr
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Transicao_left(pygame.sprite.Sprite):
    def __init__(self, tela, x, y):
        self.groups = tela.all_sprites, tela.transl
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Transicao_up(pygame.sprite.Sprite):
    def __init__(self, tela, x, y):
        self.groups = tela.all_sprites, tela.transu
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Transicao_down(pygame.sprite.Sprite):
    def __init__(self, tela, x, y):
        self.groups = tela.all_sprites, tela.transd
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Melee_acao(pygame.sprite.Sprite):
    def __init__(self, tela, pos):
        self.groups = tela.all_sprites, tela.ataques
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect() 
        self.pos = vec(pos)
        self.rect.center = pos
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

class Melee_imagem(pygame.sprite.Sprite):
    def __init__(self, tela, pos):
        self.groups = tela.all_sprites, tela.visiveis
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tela = tela
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect() 
        self.pos = vec(pos)
        self.rect.center = pos
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 20

    def update(self):
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
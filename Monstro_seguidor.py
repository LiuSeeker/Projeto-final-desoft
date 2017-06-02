import pygame
from os import path
from setting import *
from random import randint
from Sprites import *

vec = pygame.math.Vector2

def colisao(sprite, group, dir):
    if dir == 'x':
        colisao = pygame.sprite.spritecollide(sprite, group, False)
        if colisao:
            if sprite.vel.x > 0:
                sprite.pos.x = colisao[0].rect.left - sprite.rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = colisao[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
            return True
    if dir == 'y':
        colisao = pygame.sprite.spritecollide(sprite, group, False)
        if colisao:
            if sprite.vel.y > 0:
                sprite.pos.y = colisao[0].rect.top - sprite.rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = colisao[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y
            return True

class Monstro_seguidor(pygame.sprite.Sprite):
    def __init__(self, tela, x, y, tipo):
        self.groups = tela.all_sprites, tela.monstros, tela.visiveis # Grupos de sprites a que pertence
        pygame.sprite.Sprite.__init__(self, self.groups) # Inclui classe nos grupos
        self.tela = tela
        self.tipo = tipo
        self.img_dir = path.join(path.dirname(__file__), "sprites\monstro")
        self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
                                            self.tipo["f"])).convert_alpha(),
                                            (self.tipo["width"],self.tipo["height"]))
                                            # Carrega a imagem
        self.rect = self.image.get_rect() 
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.vida = self.tipo["vida"]
        self.x = y
        self.y = x
        self.melee_cd = 600
        self.colide_com_playerx = False
        self.colide_com_playery = False
        self.last_melee = 0

    def update(self):
        self.rot = (self.tela.player.pos - self.pos).angle_to(vec(1, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos    
        self.acc = vec(self.tipo["vel"], 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.tela.dt
        self.pos += self.vel *self.tela.dt + 0.5 * self.acc * self.tela.dt ** 2
        self.rect.centerx = self.pos.x
        colisao(self, self.tela.paredes, 'x')
        self.colide_com_playerx = colisao(self, self.tela.players, 'x')
        self.rect.centery = self.pos.y
        colisao(self, self.tela.paredes, 'y')
        self.colide_com_playery = colisao(self, self.tela.players, 'y')
        self.rect.center = self.pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.acerto()
        self.ataque()
        if self.vida <= 0:
            self.kill()
            Exp(self.tela, self.tela.player.x + jogador["width"]/2, self.tela.player.y - jogador["height"]/2, self.tipo["nome"])
            self.tela.player.exp += self.tipo["exp"]

    def acerto(self):
        # Marca um acerto no Monstro quando ele colide com um ataque
        self.hits = pygame.sprite.spritecollide(self, self.tela.ataques_player,\
                                                False)
        for hit in self.hits:
            Dano(self.tela, self.x + self.tipo["width"]/2, self.y - self.tipo["height"]/2, \
                "player")
            self.vida -= self.tela.player.tipo["dano"]


    def ataque(self):
        #Ataque acontece se o monstro colidir com o jogador
        if self.colide_com_playery or self.colide_com_playerx:
            now = pygame.time.get_ticks()
            if now - self.last_melee > self.melee_cd:
                self.last_melee = now
                Dano(self.tela, self.tela.player.x + self.tipo["width"]/2, self.tela.player.y - self.tipo["height"]/2, \
				str(self.tipo["nome"]))
                self.tela.player.vida -= self.tipo["dano"]
                Vida(self.tela, 16, 1, self.tela.player.vida)
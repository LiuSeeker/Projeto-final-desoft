import pygame
from os import path
from setting import *
from random import randint

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
	if dir == 'y':
		colisao = pygame.sprite.spritecollide(sprite, group, False)
		if colisao:
			if sprite.vel.y > 0:
				sprite.spritepos.y = colisao[0].rect.top - sprite.rect.height / 2
			if sprite.vel.y < 0:
				sprite.pos.y = colisao[0].rect.bottom + sprite.rect.height / 2
			sprite.vel.y = 0
			sprite.rect.centery = sprite.pos.y

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
		self.rect.centery = self.pos.y
		colisao(self, self.tela.paredes, 'x')
		self.rect.center = self.pos
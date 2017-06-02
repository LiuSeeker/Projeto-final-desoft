import pygame
from os import path
from setting import *
from random import randint

vec = pygame.math.Vector2

class Monstro(pygame.sprite.Sprite):
	def __init__(self, tela, x, y, tipo):
		self.groups = tela.all_sprites, tela.monstros, tela.visiveis # Grupos de sprites a que pertence
		pygame.sprite.Sprite.__init__(self, self.groups) # Inclui classe nos grupos
		self.tela = tela
		self.tipo = tipo
		self.img_dir = path.join(path.dirname(__file__), "sprites\monstro")
		self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, 
											self.tipo["f"])).convert_alpha(),
											(self.tipo["width"], self.tipo["height"]))
											# Carrega a imagem
		self.rect = self.image.get_rect() 
		self.x = x * TILESIZE # Define a posição x
		self.y = y * TILESIZE # Define a posição y
		self.vx = 0 # Define a velocidade em x
		self.vy = 0 # Define a velocidade em y
		self.dirx = 0
		self.diry = 0
		self.count = 0
		self.vida = self.tipo["vida"]
		self.vel = self.tipo["vel"]
		self.last_ranged = 0
		self.ataque_cd = self.tipo["cd"]

	def muda_vel(self):
		# Mudança de velocidade e direção para movimento aleatório
		self.vx = 0
		self.vy = 0
		self.dir = randint(0,1)
		if self.dir == 1:
			self.vx = randint(-self.vel, self.vel)
		else:
			self.vy = randint(-self.vel, self.vel)

		# Carrega as imagens dependendo da direção
		if self.vx > 0:
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
												self.tipo["r"])).convert_alpha(),
												(self.tipo["width"],self.tipo["height"]))
			self.dirx = 1
		if self.vx < 0:
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
												self.tipo["l"])).convert_alpha(),
												(self.tipo["width"],self.tipo["height"]))
			self.dirx = -1
		if self.vx == 0:
			self.dirx = 0
		if self.vy > 0:
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
												self.tipo["f"])).convert_alpha(),
												(self.tipo["width"],self.tipo["height"]))
			self.diry = 1
		if self.vy < 0:
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
												self.tipo["b"])).convert_alpha(),
												(self.tipo["width"],self.tipo["height"]))
			self.diry = -1
		if self.vy == 0:
			self.diry = 0
		
	def move_aleatorio(self):
		# Movimento aleatório baseado na função muda_vel()
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
		# Função para colisão entre o Monstro e Paredes
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
		# Função para colisão entre o Monstro e Player
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
		# Função para colisão entre o Monstro e outros Monstros
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

	def ataque(self):
		now = pygame.time.get_ticks()
		if now - self.last_ranged > self.ataque_cd:
			self.last_ranged = now
			Ranged(self.tela, self.x, self.y, self.dirx, self.diry, self.tipo)

	def acerto(self):
		# Marca um acerto no Monstro quando ele colide com um ataque
		self.hits = pygame.sprite.spritecollide(self, self.tela.ataques_player,\
												False)
		for hit in self.hits:
			Dano(self.tela, self.x + self.tipo["width"]/2, self.y - self.tipo["height"]/2, \
				"player")
			self.vida -= self.tela.player.tipo["dano"]

	def ataque_boss(self):
		now = pygame.time.get_ticks()
		if now - self.last_ranged > self.ataque_cd:
			self.last_ranged = now
			Ranged(self.tela, self.x, self.y, 1, 0, self.tipo)
			Ranged(self.tela, self.x, self.y, -1, 0, self.tipo)
			Ranged(self.tela, self.x, self.y, 0, 1, self.tipo)
			Ranged(self.tela, self.x, self.y, 0, -1, self.tipo)

	def ataque_boss2(self):
		#Ataque acontece se o monstro colidir com o jogador
		if self.colide_com_playery or self.colide_com_playerx:
			now = pygame.time.get_ticks()
			if now - self.last_melee > self.melee_cd:
				self.last_melee = now
				Dano(self.tela, self.tela.player.x + self.tipo["width"]/2, self.tela.player.y - self.tipo["height"]/2, \
				str(self.tipo["nome"]))
				self.tela.player.vida -= self.tipo["dano"] - 5
				Vida(self.tela, 16, 1, self.tela.player.vida)

	def update(self):
		# Atualiza a sprite
		self.move_aleatorio()
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
		self.acerto()
		if self.tipo == boss:
			self.ataque_boss()
			self.ataque_boss2()
		else:
			self.ataque()
		if self.vida <= 0:
			self.kill()
			Exp(self.tela, self.tela.player.x + jogador["width"]/2, self.tela.player.y - jogador["height"]/2, self.tipo["nome"])
			self.tela.player.exp += self.tipo["exp"]
	

class Player(pygame.sprite.Sprite):
	def __init__(self, tela, x, y, tipo):
		self.groups = tela.all_sprites, tela.players, tela.visiveis # Grupos de sprites a que pertence
		pygame.sprite.Sprite.__init__(self, self.groups) # Inclui classe nos grupos
		self.tela = tela
		self.tipo = tipo
		self.img_dir = path.join(path.dirname(__file__), "sprites\soldier")
		self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tipo["f"])).convert_alpha(),
											(self.tipo["width"], self.tipo["height"]))
											# Carrega a imagem
		self.rect = self.image.get_rect()
		self.vel = vec(0, 0) # Define a velocidade em x e y
		self.pos = vec(x, y) * TILESIZE
		self.rect.center = (x,y)
		self.x = x * TILESIZE # Define a posição x
		self.y = y * TILESIZE # Define a posição y
		self.vida = self.tipo["vida"]
		self.exp = self.tipo["exp"]
		self.direcao = 0
		self.last_melee = 0
		self.melee_cd = 600 # Cooldown do ataque melee
		# Define se está no mapa
		self.in_mapr = True # Está antes do limite da direita
		self.in_mapl = True # Está antes do limite da esquerda
		self.in_mapu = True # Está antes do limite de cima
		self.in_mapd = True # Está antes do limite de baixo
		self.in_mapp = True

	def get_keys(self):
		# Recebe os inputs do usuário
		self.vx = 0 # Define a velocidade em x
		self.vy = 0 # Define a velocidade em y
		keys = pygame.key.get_pressed()
		# Define a direção e a imagem a ser carregada (teclas de movimento)
		if keys[pygame.K_a]:
			self.vx = -self.tipo["vel"]
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
												self.tipo["l"])).convert_alpha(),
												(self.tipo["width"], self.tipo["height"]))
			self.direcao = (-1, 0)
		if keys[pygame.K_d]:
			self.vx = self.tipo["vel"]
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
												self.tipo["r"])).convert_alpha(),
												(self.tipo["width"], self.tipo["height"]))
			self.dir = self.x + self.tipo["width"]/2, self.y + 3*TILESIZE/2
			self.direcao = (1, 0)
		if keys[pygame.K_w]:
			self.vy = -self.tipo["vel"]
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
												self.tipo["b"])).convert_alpha(),
												(self.tipo["width"], self.tipo["height"]))
			self.direcao = (0, -1)
		if keys[pygame.K_s]:
			self.vy = self.tipo["vel"]
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
												self.tipo["f"])).convert_alpha(),
												(self.tipo["width"], self.tipo["height"]))
			self.direcao = (0, 1)
		if self.vx != 0 and self.vy != 0:
			self.vx *= 0.7071
			self.vy *= 0.7071
		# Define a ação da barra de espaço (ataque melee)
		if keys[pygame.K_SPACE]:
			self.vx *= 0.75
			self.vy *= 0.75
			now = pygame.time.get_ticks()
			if now - self.last_melee > self.melee_cd:
				self.last_melee = now
				Melee_acao(self.tela, (self.x + self.tipo["width"] / 2 + 
							self.direcao[0] * TILESIZE, self.y + self.tipo["height"] / 2 +
							self.direcao[1] * TILESIZE))
				Melee_imagem(self.tela, (self.x + self.tipo["width"] / 2 +
							self.direcao[0] * TILESIZE, self.y + self.tipo["height"] / 2 +
							self.direcao[1] * TILESIZE))

	def colisao_parede(self, dir):
		# Função para colisão entre o Player e Paredes
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
		# Função para colisão entre o Player e Monstros
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
		# Função para colisão entre o Player e tiles de transição de mapa
		colisaor = pygame.sprite.spritecollide(self,self.tela.transr,False)
		colisaol = pygame.sprite.spritecollide(self,self.tela.transl,False)
		colisaou = pygame.sprite.spritecollide(self,self.tela.transu,False)
		colisaod = pygame.sprite.spritecollide(self,self.tela.transd,False)
		colisaop = pygame.sprite.spritecollide(self,self.tela.transp,False)
		if colisaor:
			self.in_mapr = False
		if colisaol:
			self.in_mapl = False
		if colisaou:
			self.in_mapu = False
		if colisaod:
			self.in_mapd = False
		if colisaop:
			self.in_mapp = False

	def level_up(self):
		self.vida += 10

	def update(self):
		# Roda as funções e da update na posição
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
		if self.exp - 30 >= 0:
			self.level_up()
			self.exp = 0
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
		if self.vida <= 0:
			self.vida = 0
			self.kill()
			self.tela.game.estado = "loss"


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

class Transicao_porta(pygame.sprite.Sprite):
	def __init__(self, tela, x, y):
		self.groups = tela.all_sprites, tela.transp
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
		self.groups = tela.all_sprites, tela.ataques_player
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.tela = tela
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		self.rect = self.image.get_rect() 
		self.pos = vec(pos)
		self.rect.center = pos
		self.spawn_time = pygame.time.get_ticks()
		self.lifetime = 5

	def update(self):
		self.rect.center = self.pos
		if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
			self.kill()

class Melee_imagem(pygame.sprite.Sprite):
	def __init__(self, tela, pos):
		self.groups = tela.all_sprites, tela.visiveis
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.tela = tela
		self.img_dir = path.join(path.dirname(__file__), "sprites\soldier")
		self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tela.player.tipo["ataqued"])).convert_alpha(),
											(TILESIZE, TILESIZE))
		self.rect = self.image.get_rect() 
		self.pos = vec(pos)
		self.rect.center = pos
		self.spawn_time = pygame.time.get_ticks()
		self.ang = 0
		self.lifetime = 80

	def update(self):
		if self.tela.player.direcao == (1,0):
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tela.player.tipo["ataquer"])).convert_alpha(),
											(TILESIZE, TILESIZE))
		if self.tela.player.direcao == (-1,0):
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tela.player.tipo["ataquel"])).convert_alpha(),
											(TILESIZE, TILESIZE))
		if self.tela.player.direcao == (0,1):
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tela.player.tipo["ataqued"])).convert_alpha(),
											(TILESIZE, TILESIZE))
		if self.tela.player.direcao == (0,-1):
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tela.player.tipo["ataqueu"])).convert_alpha(),
											(TILESIZE, TILESIZE))
		self.rect.center = self.pos
		if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
			self.kill()

class Ranged(pygame.sprite.Sprite):
	def __init__(self, tela, x, y, dirx, diry, tipo):
		self.groups = tela.all_sprites, tela.visiveis, tela.ataques_monstros
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.tela = tela 
		self.tipo = tipo
		self.img_dir = path.join(path.dirname(__file__), "sprites\monstro")
		self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tipo["au"])).convert_alpha(),
											(self.tipo["awidth"], self.tipo["aheight"]))
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.dirx = dirx
		self.diry = diry
		self.rect.x = self.x
		self.rect.y = self.y
		self.spawn_time = pygame.time.get_ticks()
		self.lifetime = self.tipo["ataquedur"]

	def colisao_parede(self):
		# Função para colisão entre o Player e Paredes
		colisao = pygame.sprite.spritecollide(self,self.tela.paredes,False)
		if colisao:
			self.kill()

	def colisao_player(self):
		# Função para colisão entre o Player e Paredes
		self.hits = pygame.sprite.spritecollide(self, self.tela.players,\
												False)
		for hit in self.hits:
			Dano(self.tela, self.tela.player.x + self.tipo["width"]/2, self.tela.player.y - self.tipo["height"]/2, \
				str(self.tipo["nome"]))
			self.tela.player.vida -= self.tipo["dano"]
			Vida(self.tela, 16, 1, self.tela.player.vida)
			self.kill()

	def update(self):
		self.x += self.tipo["ataquevel"] * self.tela.dt * self.dirx
		if self.dirx == 1:
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tipo["ar"])).convert_alpha(),
											(self.tipo["aheight"], self.tipo["awidth"]))
		if self.dirx == -1:
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tipo["al"])).convert_alpha(),
											(self.tipo["aheight"], self.tipo["awidth"]))
		self.y += self.tipo["ataquevel"] * self.tela.dt * self.diry
		if self.diry == 1:
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tipo["ad"])).convert_alpha(),
											(self.tipo["awidth"], self.tipo["aheight"]))
		if self.diry == -1:
			self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											self.tipo["au"])).convert_alpha(),
											(self.tipo["awidth"], self.tipo["aheight"]))
		self.rect.x = self.x
		self.rect.y = self.y
		self.colisao_parede()
		self.colisao_player()
		if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
			self.kill()

class Dano(pygame.sprite.Sprite):
	def __init__(self, tela, x, y, tipo):
		self.groups = tela.all_sprites, tela.visiveis
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.tela = tela
		self.img_dir = path.join(path.dirname(__file__), "sprites\dano")
		self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											dano[tipo])).convert_alpha(),
											(TILESIZE-10, TILESIZE-10))
		self.rect = self.image.get_rect() 
		self.x = x
		self.y = y
		self.spawn_time = pygame.time.get_ticks()
		self.lifetime = 500

	def update(self):
		self.rect.center = (self.x, self.y)
		if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
			self.kill()

class Exp(pygame.sprite.Sprite):
	def __init__(self, tela, x, y, tipo):
		self.groups = tela.all_sprites, tela.visiveis
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.tela = tela
		self.img_dir = path.join(path.dirname(__file__), "sprites\exp")
		self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											exp[tipo])).convert_alpha(),
											(TILESIZE-10, TILESIZE-10))
		self.rect = self.image.get_rect() 
		self.x = x
		self.y = y
		self.spawn_time = pygame.time.get_ticks()
		self.lifetime = 800

	def update(self):
		self.rect.center = (self.x, self.y)
		if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
			self.kill()

class Vida(pygame.sprite.Sprite):
	def __init__(self, tela, x, y, nom):
		self.groups = tela.all_sprites, tela.visiveis
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.tela = tela
		self.img_dir = path.join(path.dirname(__file__), "sprites\hp")
		self.image = pygame.transform.scale(pygame.image.load(path.join(self.img_dir,
											str(nom)+".png")).convert_alpha(),
											(48,48))
		self.rect = self.image.get_rect() 
		self.x = x
		self.y = y
		self.rect.x = self.x * TILESIZE
		self.rect.y = self.y * TILESIZE

class Bau(pygame.sprite.Sprite):
	def __init__(self, tela, x, y):
		self.groups = tela.all_sprites, tela.visiveis, tela.baus
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.tela = tela
		self.rect = self.image.get_rect() 
		self.x = x
		self.y = y
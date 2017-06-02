import pygame
import sys
from random import randint
from os import path
from setting import *
from Sprites import *
from Mapa import *
from Monstro_seguidor import *

class Tela:
	def __init__(self, game, mapa):
		game_folder = path.dirname(__file__)
		self.map = Map(path.join(game_folder, "maps\\grade\\" + mapa)) # Define o objeto do mapa
		self.game = game
		self.clock = pygame.time.Clock()
		self.back = pygame.image.load("maps\\imagens\\" + game.mapa["imagem"]) # Carrega a imagem de fundo
		self.game.screen.blit(self.back, (0,0)) # Mostra a imagem de fundo

		# sprites.Group()
		self.all_sprites = pygame.sprite.Group()
		self.paredes = pygame.sprite.Group()
		self.visiveis = pygame.sprite.Group()
		self.monstros = pygame.sprite.Group()
		self.players = pygame.sprite.Group()
		self.ataques_player = pygame.sprite.Group()
		self.ataques_monstros = pygame.sprite.Group()
		self.baus = pygame.sprite.Group()
		self.transr = pygame.sprite.Group()
		self.transl = pygame.sprite.Group()
		self.transu = pygame.sprite.Group()
		self.transd = pygame.sprite.Group()
		self.transp = pygame.sprite.Group()
		self.LS = []
		self.LG = []
		self.LW = []
		self.LB = []
		self.LZ = []
		self.LO = []
		self.LU = []

		# Cria os obajetos a partirwwwwdddd do .txt
		for row, tiles in enumerate(self.map.data): # "row" retorna a posição na lista, "tiles" retorna a string
			for col, tile in enumerate(tiles): # "col" retorna a posição na string, "tile" retorna o caractere
				if tile == "S":
					self.LS.append(col)
					self.LS.append(row)
				elif tile == "G":
					self.LG.append(col)
					self.LG.append(row)
				elif tile == "W":
					self.LW.append(col)
					self.LW.append(row)
				elif tile == "B":
					self.LB.append(col)
					self.LB.append(row)
				elif tile == "Z":
					self.LZ.append(col)
					self.LZ.append(row)
				elif tile == "O":
					self.LO.append(col)
					self.LO.append(row)
				elif tile == "U":
					self.LU.append(col)
					self.LU.append(row)

				if tile == "1":
					Parede(self, col, row)
				elif tile == "L":
					Transicao_left(self, col, row)
				elif tile == "R":
					Transicao_right(self, col, row)
				elif tile == "U":
					Transicao_up(self, col, row)
				elif tile == "D":
					Transicao_down(self, col, row)
				elif tile == "P":
					Transicao_porta(self, col, row)

		for i in range(int(len(self.LS)/2)):
			self.LS[i] = Monstro(self, self.LS[i*2], self.LS[i*2+1], snake)
		for i in range(int(len(self.LG)/2)):
			self.LG[i] = Monstro(self, self.LG[i*2], self.LG[i*2+1], ghost)
		for i in range(int(len(self.LW)/2)):
			self.LW[i] = Monstro_seguidor(self, self.LW[i*2], self.LW[i*2+1], snake)
		for i in range(int(len(self.LB)/2)):
			self.LB[i] = Monstro(self, self.LB[i*2], self.LB[i*2+1], bat)
		for i in range(int(len(self.LZ)/2)):
			self.LZ[i] = Boss(self, self.LZ[i*2], self.LZ[i*2+1], boss)
		for i in range(int(len(self.LO)/2)):
			self.LO[i] = Monstro_seguidor(self, self.LO[i*2], self.LO[i*2+1], bat)
		for i in range(int(len(self.LU)/2)):
			self.LU[i] = Monstro_seguidor(self, self.LU[i*2], self.LU[i*2+1], ghost)	

		self.player = Player(self, self.game.px, self.game.py, jogador)
		self.hp = Vida(self, 18, 1, "hp")

		self.dt = self.clock.tick(FPS) / 8000

	def draw(self):
		# Desenha as sprites visíveis (que devem aparecer)
		self.visiveis.draw(game.screen)


class Game:
	def __init__(self):
		pygame.init() # Inicia o pygame
		self.clock = pygame.time.Clock() # Define o clock
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Define o tamanho da janela
		self.intro()
		pygame.display.set_caption(TITLE) # Define o nome da janela
		self.txt = "casa.txt" # Puxa o nome do mapa (.txt)
		self.mapa = mapas[self.txt] # Puxa o dicionário do mapa escolhido
		self.px = 17 # Posição x do player
		self.py = 15 # Posição y do player
		self.vidap = 0

	def intro(self):
		self.menu = pygame.image.load("maps\\intro\\" + "GAMEINTRO.png")
		self.screen.blit(self.menu, (0,0))
		pygame.display.flip()
		self.events()

	def instrucoes(self):
		self.menu = pygame.image.load("maps\\intro\\" + "INSTRUCTIONS.png")
		self.screen.blit(self.menu, (0,0))
		pygame.display.flip()
		self.events()

	def win(self):
		self.menu = pygame.image.load("maps\\fimdojogo\\" + "GAME WIN.png")
		self.screen.blit(self.menu, (0,0))
		pygame.display.flip()
		self.events()

	def loss(self):
		self.menu = pygame.image.load("maps\\fimdojogo\\" + "GAME OVER.png")
		self.screen.blit(self.menu, (0,0))
		pygame.display.flip()
		self.events()

	def run(self):
		# Loop do jogo 
		self.playing = True
		self.estado = "inicio"
		while self.playing:
			self.events()
			keys = pygame.key.get_pressed()
			if self.estado == "inicio":
				self.intro()
				if keys[pygame.K_BACKSPACE]:
					self.estado = "ins"
			elif self.estado == "ins":
					self.instrucoes()
					if keys[pygame.K_w]:
						self.estado = "jogo"
						self.tela = Tela(self, self.txt)
			elif self.estado == "win":
				self.win()
			elif self.estado == "loss":
				self.loss()
			elif self.estado == "jogo":
				self.tela.visiveis.clear(self.screen, self.tela.back) # Limpa a tela
				self.update()
				self.draw()
	
	def quit(self):
		pygame.quit()
		sys.exit()

	def update(self):
		# Atualiza as sprites
		self.tela.visiveis.update()
		self.tela.ataques_player.update()
		self.tela.ataques_monstros.update()
		self.trans_tela()

	def draw(self):
		# Desenha as sprites
		self.tela.draw()
		pygame.display.flip()

	def events(self):
		# Monitora os eventos do jogo
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()
		
	def trans_tela(self):
		# Transição de tela
		if self.tela.player.in_mapr == False:
			# Transição para tela da direita
			self.txt = self.mapa["r"]
			self.mapa = mapas[self.txt]
			self.px = 1
			self.py = self.tela.player.y / TILESIZE
			self.vidap = self.tela.player.vida
			self.tela = Tela(self, self.txt)
		if self.tela.player.in_mapl == False:
			# Transição para tela da esquerda
			self.txt = self.mapa["l"]
			self.mapa = mapas[self.txt]
			self.px = 33
			self.py = self.tela.player.y / TILESIZE
			self.vidap = self.tela.player.vida
			self.tela = Tela(self, self.txt)
		if self.tela.player.in_mapu == False:
			# Transição para tela de cima
			self.txt = self.mapa["u"]
			self.mapa = mapas[self.txt]
			self.px = self.tela.player.x / TILESIZE
			self.py = 19
			self.vidap = self.tela.player.vida
			self.tela = Tela(self, self.txt)
		if self.tela.player.in_mapd == False:
			# Transição para tela de baixo
			self.txt = self.mapa["d"]
			self.mapa = mapas[self.txt]
			self.px = self.tela.player.x / TILESIZE
			self.py = 1
			self.vidap = self.tela.player.vida
			self.tela = Tela(self, self.txt)
		if self.tela.player.in_mapp == False:
			# Transição para porta
			self.txt = self.mapa["p"]
			self.mapa = mapas[self.txt]
			self.px = self.mapa["x"]
			self.py = self.mapa["y"]
			self.vidap = self.tela.player.vida
			self.tela = Tela(self, self.txt)
			
# Roda o jogo
game = Game()
pygame.mixer.init()
musica_dir = path.join(path.dirname(__file__), "Trilha_sonora")
pygame.mixer.music.load(path.join(musica_dir,"Musica_epica.ogg"))
pygame.mixer.music.play(loops=-1)
while True:
	game.run()
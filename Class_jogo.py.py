import pygame
import sys
from random import randint
from os import path
from setting import *
from Sprites import *
from Mapa import *

class Tela:
	def __init__(self, game, mapa):
		game_folder = path.dirname(__file__)
		self.map = Map(path.join(game_folder, "maps\\" + mapa))
		self.game = game
		self.clock = pygame.time.Clock()
		self.dt = self.clock.tick(FPS) / 4000
		self.back = pygame.image.load("maps\\" + game.mapa["imagem"])
		self.game.screen.blit(self.back, (0,0))
		self.all_sprites = pygame.sprite.Group()
		self.paredes = pygame.sprite.Group()
		self.visiveis = pygame.sprite.Group()
		self.monstros = pygame.sprite.Group()
		self.players = pygame.sprite.Group()
		self.ataques = pygame.sprite.Group()
		self.transr = pygame.sprite.Group()
		self.transl = pygame.sprite.Group()
		self.transu = pygame.sprite.Group()
		self.transd = pygame.sprite.Group()
		#cria as apredes a partir do "map_data"
		for row, tiles in enumerate(self.map.data): #"row" retorna a posição na lista, "tiles" retorna a string
			for col, tile in enumerate(tiles): #"col" retorna a posição na string, "tile" retorna o caractere
				if tile == "1":
					Parede(self, col, row)
				elif tile == "P":
					self.player = Player(self, col, row, jogador)
				elif tile == "S":
					Monstro(self, col, row, snake)
				elif tile == "G":
					Monstro(self, col, row, ghost)
				elif tile == "L":
					Transicao_left(self, col, row)
				elif tile == "R":
					Transicao_right(self, col, row)
				elif tile == "U":
					Transicao_up(self, col, row)
				elif tile == "D":
					Transicao_down(self, col, row)

	def draw(self):
		self.visiveis.draw(game.screen)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.txt = "matriz_mapa_inicial.txt"
        self.mapa = mapas[self.txt]
        self.tela = Tela(self, self.txt)


    def run(self):
        # Loop do jogo 
        self.playing = True
        while self.playing:
            self.events()
            self.tela.visiveis.clear(self.screen, self.tela.back)
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # Atualiza as sprites
        self.tela.visiveis.update()
        self.trans_tela()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.tela.draw()
        pygame.display.flip()

    def events(self):
        # Monitora os eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
        
    def trans_tela(self):
    	if self.tela.player.in_mapr == False:
    		self.txt = self.mapa["r"]
    		self.mapa = mapas[self.txt]
    		self.tela = Tela(self, self.txt)
    	if self.tela.player.in_mapl == False:
    		self.txt = self.mapa["l"]
    		self.mapa = mapas[self.txt]
    		self.tela = Tela(self, self.txt)
    	if self.tela.player.in_mapu == False:
    		self.txt = self.mapa["u"]
    		self.mapa = mapas[self.txt]
    		self.tela = Tela(self, self.txt)
    	if self.tela.player.in_mapd == False:
    		self.txt = self.mapa["d"]
    		self.mapa = mapas[self.txt]
    		self.tela = Tela(self, self.txt)


# Cria o objeto do jogo
game = Game()
while True:
    game.run()
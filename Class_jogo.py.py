import pygame
import sys
from random import randint
from os import path
from math import hypot
from setting import *
from Sprites import *
from Mapa import *

class Tela:
    def __init__(self, game, mapa):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, mapa))
        self.game = game
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(FPS) / 4000
        self.back = pygame.image.load(mapas[mapa])
        self.game.screen.blit(self.back, (0,0))
        
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.paredes = pygame.sprite.Group()
        self.visiveis = pygame.sprite.Group()
        self.monstros = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.ataques = pygame.sprite.Group()

        #cria as apredes a partir do "map_data"
        for row, tiles in enumerate(self.map.data): #"row" retorna a posição na lista, "tiles" retorna a string
            for col, tile in enumerate(tiles): #"col" retorna a posição na string, "tile" retorna o caractere
                if tile == "1":
                    Parede(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row, jogador)
                if tile == "S":
                	Monstro(self, col, row, snake)

    def draw(self):
        self.visiveis.draw(game.screen)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.tela = Tela(self, "matriz_teste.txt")

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
        



# Cria o objeto do jogo
game = Game()
while True:
    game.tela.new()
    game.run()

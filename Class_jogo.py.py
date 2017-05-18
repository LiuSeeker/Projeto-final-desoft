import pygame
import sys
from random import randint
from os import path
from setting import *
from Sprites import *
from Mapa import *

class Tela:
    def __init__(self, game):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'matriz_teste.txt'))
        self.game = game
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(FPS) / 5000
        self.back = pygame.image.load("teste.png")
        self.game.screen.blit(self.back, (0, 0))
        
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.paredes = pygame.sprite.Group()
        self.visiveis = pygame.sprite.Group()
        self.monstro = Monstro(self, 9 * TILESIZE, 9 * TILESIZE, "snake")

        #cria as apredes a partir do "map_data"d
        for row, tiles in enumerate(self.map.data): #"row" retorna a posição na lista, "tiles" retorna a string
            for col, tile in enumerate(tiles): #"col" retorna a posição na string, "tile" retorna o caractere
                if tile == "1":
                    Parede(self, col, row)
                if tile == "P":
                    self.player = Player(self, col * TILESIZE, row * TILESIZE)

    def draw(self):
        self.visiveis.draw(self.game.screen)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.tela = Tela(self)

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

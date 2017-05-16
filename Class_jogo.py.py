import pygame

import sys
import random
from os import path
from setting import *
from Sprites import *
from Mapa import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'mapa.txt'))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.paredes = pygame.sprite.Group()
        self.monstro = Monstro(self, 9, 9, "snake")


        #cria as apredes a partir do "map_data"
        for row, tiles in enumerate(self.map.data): #"row" retorna a posição na lista, "tiles" retorna a string
            for col, tile in enumerate(tiles): #"col" retorna a posição na string, "tile" retorna o caractere
                if tile == "1":
                    Parede(self, col, row)
                if tile == "P":
                    self.player = Player(self, col * TILESIZE, row * TILESIZE)

    def run(self):
        # Loop do jogo 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # Atualiza as sprites
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def events(self):
        # Monitora os eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
        



# Cria o objeto do jogo
game = Game()
while True:
    game.new()
    game.run()

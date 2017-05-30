import pygame
import sys
from random import randint
from os import path
from setting import *
from Sprites import *
from Mapa import *
'''from Monstro_seguidor import *'''

class Tela:
    def __init__(self, game, mapa):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, "maps\\grade\\" + mapa)) # Define o objeto do mapa
        self.game = game
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(FPS) / 4000 # Diminui a velocidade do jogo
        self.back = pygame.image.load("maps\\imagens\\" + game.mapa["imagem"]) # Carrega a imagem de fundo
        self.game.screen.blit(self.back, (0,0)) # Mostra a imagem de fundo

        # sprites.Group()
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
        self.transp = pygame.sprite.Group()

        # Cria os obajetos a partir do .txt
        for row, tiles in enumerate(self.map.data): # "row" retorna a posição na lista, "tiles" retorna a string
            for col, tile in enumerate(tiles): # "col" retorna a posição na string, "tile" retorna o caractere
                if tile == "1":
                    Parede(self, col, row)
                elif tile == "S":
                    Monstro(self, col, row, snake)
                elif tile == "G":
                    Monstro(self, col, row, ghost)
                elif tile == "W":
                    Monstro_seguidor(self, col, row, snake)
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

        self.player = Player(self, self.game.px, self.game.py, jogador)

    def draw(self):
    	# Desenha as sprites visíveis (que devem aparecer)
        self.visiveis.draw(game.screen)


class Game:
    def __init__(self):
        pygame.init() # Inicia o pygame
        self.clock = pygame.time.Clock() # Define o clock
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Define o tamanho da janela
        pygame.display.set_caption(TITLE) # Define o nome da janela
        self.intro()
        self.txt = "casa.txt" # Puxa o nome do mapa (.txt)
        self.mapa = mapas[self.txt] # Puxa o dicionário do mapa escolhido
        self.px = 2 # Posição x do player
        self.py = 11 # Posição y do player
    


    def intro(self):
        self.menu = pygame.image.load("maps\\intro\\" + "GAMEINTRO.png")
        self.screen.blit(self.menu, (0,0))
        pygame.display.flip()
        self.events()

    def run(self):
        # Loop do jogo 
        self.playing = True
        estado = "inicio"
        while self.playing:
            self.events()
            keys = pygame.key.get_pressed()
            if estado == "inicio":
                self.intro()
                if keys[pygame.K_BACKSPACE]:
                    estado = "jogo"
                    self.tela = Tela(self, self.txt)
            else:
                self.tela.visiveis.clear(self.screen, self.tela.back) # Limpa a tela
                self.update()
                self.draw()
                print(estado)

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # Atualiza as sprites
        self.tela.visiveis.update()
        self.trans_tela()

    def draw(self):
    	# Desenha as sprites
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
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
            self.px = 2
            self.py = self.tela.player.y / TILESIZE
            self.tela = Tela(self, self.txt)
        if self.tela.player.in_mapl == False:
        	# Transição para tela da esquerda
            self.txt = self.mapa["l"]
            self.mapa = mapas[self.txt]
            self.px = 33
            self.py = self.tela.player.y / TILESIZE
            self.tela = Tela(self, self.txt)
        if self.tela.player.in_mapu == False:
        	# Transição para tela de cima
            self.txt = self.mapa["u"]
            self.mapa = mapas[self.txt]
            self.px = self.tela.player.x / TILESIZE
            self.py = 19
            self.tela = Tela(self, self.txt)
        if self.tela.player.in_mapd == False:
        	# Transição para tela de baixo
            self.txt = self.mapa["d"]
            self.mapa = mapas[self.txt]
            self.px = self.tela.player.x / TILESIZE
            self.py = 1
            self.tela = Tela(self, self.txt)
        if self.tela.player.in_mapp == False:
        	# Transição para porta
            self.txt = self.mapa["p"]
            self.mapa = mapas[self.txt]
            self.px = self.mapa["x"]
            self.py = self.mapa["y"]
            self.tela = Tela(self, self.txt)
            
# Roda o jogo
game = Game()
while True:
    game.run()
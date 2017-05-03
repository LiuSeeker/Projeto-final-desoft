import pygame
import random

#propriedades da janela
WIDTH = 1280
HEIGHT = 720
FPS = 60

#definição das cores e o nome das variaveis
#(R,G,B)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,255)
LIGHTGREY = (50,50,50)
DARKGREY = (100,100,100)

class Jogador(pygame.sprite.Sprite):
	def __init__ (self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50,50))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 2, HEIGHT / 2)

#inicia pygame e cria janela
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
jogador1 = Jogador()
sprites.add(jogador1)


#loop principal
running = True
while running:
    clock.tick(FPS)

    #event = "input"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #espaço para "desenho"
    screen.fill(DARKGREY)
    sprites.draw(screen)


    #aparece as imagens
    pygame.display.flip()

pygame.quit()
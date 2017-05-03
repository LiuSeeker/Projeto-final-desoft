import pygame
import random

#propriedades da janela
WIDTH = 1280
HEIGHT = 736
FPS = 60

#definição das cores e o nome das variaveis
#(R,G,B)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
GREEN = (0,200,0)
BLUE = (0,0,200)
LIGHTGREY = (50,50,50)
DARKGREY = (100,100,100)

#cria a classe jogador
class Jogador(pygame.sprite.Sprite):
	def __init__ (self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50,50)) #tamanho da imagem
		self.image.fill(RED)
		self.rect = self.image.get_rect() 
		self.rect.center = (x,y) #define o centro da imgagem como referência para desenhar

class Monstro(pygame.sprite.Sprite):
    def __init__(self,x,y): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40,40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

#inicia pygame e cria janela
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()


#grupo de sprites
sprites = pygame.sprite.Group() #define o nome do grupo
jogador1 = Jogador(WIDTH/2, HEIGHT/2) #argumentos definem a posição do objeto
monstro1 = Monstro(50,50)
sprites.add(jogador1) #adiciona o jogador1 no grupo
sprites.add(monstro1) #adiciona o monstro1 no grupo


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
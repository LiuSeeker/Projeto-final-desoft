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
BLUE = (0,0,255)
LIGHTGREY = (50,50,50)
DARKGREY = (100,100,100)

#Classe do jogador
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #teste com um quadrado verde
        self.image = pygame.Surface((50,50)) #tamanho
        self.image.fill(GREEN)
        self.rect = self.image.get_rect() #ponto de referência da imagem selecionada 
        self.rect.center = (WIDTH/2, HEIGHT/2) #posição do centro do sprite na tela

#inicia pygame e cria janela
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()
player = Player()

#cria um grupo de sprites
grupo_sprites = pygame.sprite.Group()
grupo_sprites.add(player) #adiciona o player no grupo de sprites

#loop principal
running = True
while running:
    clock.tick(FPS)

    #event = "input"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #espaço para "desenho"
    screen.fill(DARKGREY) #pinta o fundo de darkgrey
    grupo_sprites.draw(screen) #pinta a grupo_sprites

    #aparece as imagens
    pygame.display.flip()

pygame.quit()
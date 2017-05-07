import pygame
import random


#propriedades da janela
WIDTH = 32*35
HEIGHT = 32*21
FPS = 15

#definição das cores e o nome das variaveis
#(R,G,B)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
GREEN = (0,200,0)
BLUE = (0,0,200)
LIGHTGREY = (50,50,50)
DARKGREY = (100,100,100)

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#cria a classe jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE,TILESIZE)) #tamanho da imagem
        self.image.fill(GREEN)
        self.rect = self.image.get_rect() 
        self.rect.center = (x,y) #define o centro da imgagem como referência para desenhar
        self.speedx = 0
        self.speedy = 0
        sprites.add(self)

    def update(self):
        #Movimento do player
        self.speedx = 0
        self.speedy = 0
        Teclas_pressionadas = pygame.key.get_pressed() #analisa todas as teclas pressionadas
        if Teclas_pressionadas[pygame.K_LEFT]:
            self.speedx = -1 * TILESIZE #anda 1 quadrado
        elif Teclas_pressionadas[pygame.K_RIGHT]:
            self.speedx = 1 * TILESIZE #anda 1 quadrado
        if Teclas_pressionadas[pygame.K_UP]:
            self.speedy = -1 * TILESIZE #anda 1 quadrado
        elif Teclas_pressionadas[pygame.K_DOWN]:
            self.speedy = 1 * TILESIZE #anda 1 quadrado
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0 
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Monstro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE,TILESIZE)) #tamanho da imagem
        self.image.fill(RED)
        self.rect = self.image.get_rect() 
        self.x = x
        self.y = y
        self.rect.x = x*TILESIZE
        self.rect.y = y*TILESIZE
        sprites.add(self)

class Parede(pygame.sprite.Sprite):
    def __init__(self, x, y, cor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.image.fill(cor)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*TILESIZE
        self.rect.y = y*TILESIZE
        sprites.add(self)
        paredes.add(self)

#inicia pygame e cria janela
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()


#grupo de sprites
sprites = pygame.sprite.Group() #define o nome do grupo
paredes = pygame.sprite.Group()
jogador1 = Jogador(WIDTH/2, HEIGHT/2) #argumentos definem a posição do objeto
monstro1 = Monstro(2,2)
monstro2 = Monstro(10,10)
parede1 = Parede(25,15,BLACK)



#loop principal
running = True
while running:
    clock.tick(FPS)

    #event = "input"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Update
    sprites.update()

    #espaço para "desenho"
    screen.fill(DARKGREY)
    sprites.draw(screen)

    for x in range(0, WIDTH, TILESIZE):
        pygame.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    for x in range(0, HEIGHT, TILESIZE):
        pygame.draw.line(screen, LIGHTGREY, (0, x), (WIDTH, x))

    #aparece as imagens
    pygame.display.flip()

pygame.quit()
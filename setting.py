WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


WIDTH = 32*35
HEIGHT = 32*21
FPS = 60
TITLE = "Rpgzin"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

snake = {"nome": "snake", "vel": 50, "count": 300, "width": 15, "height": TILESIZE, "vida": 5, "dano": 1, "f": "snakef.png", "b": "snakeb.png", "r": "snaker.png", "l": "snakel.png"}
jogador ={"nome": "player", "vel": 100, "width": 25, "height": TILESIZE, "vida": 25, "dano": 2, "f": "soldierf.png", "b": "soldierb.png", "r": "soldierr.png", "l": "soldierl.png"}

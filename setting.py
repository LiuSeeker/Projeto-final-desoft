YELLOW = (0,0,0)

# Tamanho do tile
TILESIZE = 32

# Tamanho da janela
WIDTH = TILESIZE * 35
HEIGHT = TILESIZE * 21

# Velocidade do jogo
FPS = 60

# Título da janela
TITLE = "The Legend of Ayres"

# Dicionário de dicionários dos mapas
# 1a chave: nome do arquivo .txt
# 2a chaves: características do arquivo .txt
mapas = {"casa.txt": 
			{"imagem": "casa.png",
			"p": "fora casa.txt", # Porta
			"x": 17, # Posição x ao entrar em "casa.txt"
			"y": 18}, # Posição y ao entrar em "casa.txt"
		"fora casa.txt":
			{"imagem": "fora casa.png",
			"p": "casa.txt",
			"x": 2,
			"y": 11,
			"r": "comeco rio.txt"},
		"comeco rio.txt":
			{"imagem": "comeco rio.png",
			"l": "fora casa.txt", # Mapa da esquerda
			"r": "ponte.txt"}, # Mapa da direita
		"ponte.txt":
			{"imagem": "ponte.png",
			"l": "comeco rio.txt",
			"r": "placa cidade.txt"},
		"placa cidade.txt":
			{"imagem": "placa cidade",
			"l": "ponte.txt",
			"r": "fora castelo.txt"}}

# Tipo
snake = {"nome": "snake",
		"vel": 40, # Velocidade
		"count": 300, # Contagem para movimento aleatório
		"width": 15,
		"height": TILESIZE,
		"vida": 5,
		"dano": 1,
		"f": "snakef.png", # Imagem frontal
		"b": "snakeb.png", # Imagem traseira
		"r": "snaker.png", # Imagem da direita
		"l": "snakel.png" # Imagem da esquerda
		}

jogador = {
		"nome": "player",
		"vel": 100,
		"width": 25,
		"height": TILESIZE,
		"vida": 25,
		"dano": 2,
		"f": "soldierf.png",
		"b": "soldierb.png",
		"r": "soldierr.png",
		"l": "soldierl.png"}

ghost = {
		"nome": "ghost",
		"vel": 60,
		"count": 250,
		"width": TILESIZE,
		"height": TILESIZE,
		"vida": 400,
		"dano": 2,
		"f": "ghostf.png",
		"b": "ghostb.png",
		"r": "ghostr.png",
		"l": "ghostl.png"
		}

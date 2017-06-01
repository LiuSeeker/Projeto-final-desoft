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
			{"imagem": "placa cidade.png",
			"l": "ponte.txt",
			"u": "fora castelo.txt"},
		"fora castelo.txt":
			{"imagem": "fora castelo.png",
			"d": "placa cidade"}}

# Tipo
jogador = {
		"nome": "player",
		"vel": 100,
		"width": 25,
		"height": TILESIZE,
		"vida": 100,
		"dano": 5,
		"ataqueu": "ataqueu.png",
		"ataqued": "ataqued.png",
		"ataquel": "ataquel.png",
		"ataquer": "ataquer.png",
		"f": "soldierf.png",
		"b": "soldierb.png",
		"r": "soldierr.png",
		"l": "soldierl.png"
		}

snake = {
		"nome": "snake",
		"vel": 40, # Velocidade
		"count": 300, # Contagem para movimento aleatório
		"width": 20,
		"height": 30,
		"vida": 10,
		"dano": 5,
		"cd": 1400,
		"ataquedur": 1400,
		"ataquevel": 50,
		"f": "snakef.png", # Imagem frontal
		"b": "snakeb.png", # Imagem traseira
		"r": "snaker.png", # Imagem da direita
		"l": "snakel.png", # Imagem da esquerda
		"au": "snakeau.png",
		"ad": "snakead.png",
		"al": "snakeal.png",
		"ar": "snakear.png",
		"awidth": 10,
		"aheight": 20
		}

ghost = {
		"nome": "ghost",
		"vel": 60,
		"count": 250,
		"width": TILESIZE,
		"height": TILESIZE,
		"vida": 20,
		"dano": 7,
		"cd": 1600,
		"ataquedur": 1600,
		"ataquevel": 80,
		"f": "ghostf.png",
		"b": "ghostb.png",
		"r": "ghostr.png",
		"l": "ghostl.png",
		"au": "ghostau.png",
		"ad": "ghostad.png",
		"al": "ghostal.png",
		"ar": "ghostar.png",
		"awidth": 15,
		"aheight": 15
		}

bat = {
		"nome": "bat",
		"vel": 40,
		"count": 250,
		"width": TILESIZE,
		"height": 25,
		"vida": 5,
		"dano": 1,
		"cd": 1500,
		"ataquedur": 1200,
		"ataquevel": 40,
		"f": "batf.png",
		"b": "batb.png",
		"r": "batr.png",
		"l": "batl.png",
		"au": "bata.png",
		"ad": "bata.png",
		"al": "bata.png",
		"ar": "bata.png",
		"awidth": 10,
		"aheight": 10
		}

dano = {
		"player": str(jogador["dano"]) + ".png",
		"snake": "2.png",
		"ghost": "4.png",
		"bat": "1.png"
		}
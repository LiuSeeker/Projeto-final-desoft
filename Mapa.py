import pygame
from setting import *

class Map:
	def __init__(self, file):
		self.data = []
		with open(file, "rt") as f:
			for line in f:
				self.data.append(line[:-1])

		self.tilewidth = len(self.data[0])
		self.tileheight = len(self.data)
		self.width = self.tilewidth * TILESIZE	
		self.height = self.tileheight * TILESIZE
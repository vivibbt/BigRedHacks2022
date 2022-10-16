import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load('Assets/dirt.jpg').convert_alpha()

		self.rect = self.image.get_rect(topleft = pos)

class Grass(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load('Assets/grass.jpg').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

class Manure(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load('Assets/poop.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

class p_counter:
	x = 0
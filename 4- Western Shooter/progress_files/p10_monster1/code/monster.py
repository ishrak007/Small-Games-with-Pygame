import pygame
from entity import Entity

class Coffin(Entity):
	def __init__(self, pos, groups, path, collision_sprites):
		super().__init__(pos, groups, path, collision_sprites)

# exercise: 
# Cactus -> create this one, and display it on the display surface
class Cactus(Entity):
	def __init__(self, pos, groups, path, collision_sprites):
		super().__init__(pos, groups, path, collision_sprites)

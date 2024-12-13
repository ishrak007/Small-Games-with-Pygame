import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		self.image = pygame.Surface((50,50))
		self.image.fill('red')
		self.rect = self.image.get_rect(center = pos)

	def input(self):
		# exercise 2
		# check for the 4 arrow buttons: left, right, up and down
		# print the direction for each key pressed
		# https://www.pygame.org/docs/ref/key.html
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			print('right')
		if keys[pygame.K_LEFT]:
			print('left')
		if keys[pygame.K_UP]:
			print('up')
		if keys[pygame.K_DOWN]:
			print('down')

	def update(self):
		self.input()
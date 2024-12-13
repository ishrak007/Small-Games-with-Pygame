import pygame, sys

class Ship(pygame.sprite.Sprite):
	def __init__(self,groups):

		# 1. we have to init the parent class
		super().__init__(groups)  
		
		# 2. We need a surface -> image 
		self.image = pygame.image.load(r'D:\CODED_LIFE\###Udemy- Pygame\1- Asteroid Shooter\asteroid_object_files\project_2 - Sprites\graphics\ship.png').convert_alpha()

		# 3. We need a rect
		self.rect = self.image.get_rect(center = (WINDOW_WIDTH /2, WINDOW_HEIGHT / 2))

		

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load(r"D:\CODED_LIFE\###Udemy- Pygame\1- Asteroid Shooter\asteroid_object_files\project_2 - Sprites\graphics\laser.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)

# basic setup 
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1080, 700 
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()

# background 
background_surf = pygame.image.load(r'D:\CODED_LIFE\###Udemy- Pygame\1- Asteroid Shooter\asteroid_object_files\project_2 - Sprites\graphics\background.png').convert()

# sprite groups 
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()

# sprite creation 
ship = Ship(spaceship_group)
laser = Laser(laser_group, (WINDOW_WIDTH /4, WINDOW_HEIGHT / 4))

# game loop
while True:

	# event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# delta time 
	dt = clock.tick() / 1000

	# background 
	display_surface.blit(background_surf,(0,0))

	# graphics 
	spaceship_group.draw(display_surface)
	laser_group.draw(display_surface)

	# draw the frame 
	pygame.display.update()
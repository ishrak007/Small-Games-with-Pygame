import pygame, sys

# basic setup 
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1080, 720 
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()

# game loop
while True:

	# event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# delta time 
	dt = clock.tick() / 1000

	# draw the frame 
	pygame.display.update()
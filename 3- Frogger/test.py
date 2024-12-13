import pygame, sys 
from settings import *
from player import Player
from cars import Car
import random
from sprite import *

class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = pygame.math.Vector2()
		self.bg = pygame.image.load(r'3- Frogger\Game_Objects\graphics\main\map.png').convert()
		self.fg = pygame.image.load(r'3- Frogger\Game_Objects\graphics\main\overlay.png').convert_alpha()

	def customize_draw(self):

		# change the offset vector
		self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

		# blit the bg
		display_surface.blit(self.bg, -self.offset)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			display_surface.blit(sprite.image, offset_pos)

		display_surface.blit(self.fg, -self.offset)

# basic setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

# groups
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# car items
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 50)
car_pos = []

# font 
font = pygame.font.Font(None, 50)
text_surf = font.render('You won!',True,'White')
text_rect = text_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# music
music = pygame.mixer.Sound(r'3- Frogger\Game_Objects\audio\music.mp3')
music.play(loops = -1)

# sprites
player = Player(all_sprites, obstacle_sprites, (2062,3274))

# sprite setup
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = r'3- Frogger\Game_Objects\graphics\objects\simple'
    surf = pygame.image.load(f'{path}/{file_name}.png').convert_alpha()
    for pos in pos_list:
    	SimpleSprite(pos, [all_sprites, obstacle_sprites], surf)

for file_name, pos_list in LONG_OBJECTS.items():
    path = r'3- Frogger\Game_Objects\graphics\objects\long'
    surf = pygame.image.load(f'{path}/{file_name}.png').convert_alpha()
    for pos in pos_list:
        LongSprite(pos, [all_sprites, obstacle_sprites], surf)

# game loop
while True:

	# event loop 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == car_timer:
			pos = random.choice(CAR_START_POSITIONS)
			if pos not in car_pos: 
				car_pos.append(pos)
				random_pos = (pos[0], pos[1] + random.randint(-8, 8))
				Car([all_sprites, obstacle_sprites], random_pos)
			if len(car_pos) > 5:
				del car_pos[0]

	# delta time 
	dt = clock.tick() / 1000
 
	# new bg
	display_surface.fill("black")
 
	if player.pos.y >= 1180:
		# update 
		all_sprites.update(dt)

		# draw
		all_sprites.customize_draw()
	else:
		display_surface.fill('teal')
		display_surface.blit(text_surf,text_rect)

	# update the display surface -> drawing the frame 
	pygame.display.update()
import pygame, sys
import random

class Ship(pygame.sprite.Sprite):
    def __init__(self,groups):

        # 1. we have to init the parent class
        super().__init__(groups)  
        
        # 2. We need a surface -> image 
        self.image = pygame.image.load(r'D:\CODED_LIFE\###Udemy- Pygame\2- Asteroid Shooter with classes\asteroid_object_files\project_4 - Deltatime\graphics\ship.png').convert_alpha()

        # 3. We need a rect
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH /2, WINDOW_HEIGHT / 2))

        # 4. Add a mask
        self.mask = pygame.mask.from_surface(self.image)
        
        # timer
        self.can_shoot = True
        self.shoot_time = None
        
        # sound 
        self.laser_sound = pygame.mixer.Sound(r'D:\CODED_LIFE\###Udemy- Pygame\2- Asteroid Shooter with classes\asteroid_object_files\project_10 - Sound\sounds\laser.ogg')

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(self.rect.midtop,laser_group)
            self.laser_sound.play()

    def meteor_collision(self):
        if pygame.sprite.spritecollide(sprite=self, group=meteor_group, dokill=True, collided=pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

    def update(self):
        self.laser_timer()
        self.laser_shoot()
        self.input_position()
        self.meteor_collision()

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load(r'D:\CODED_LIFE\###Udemy- Pygame\2- Asteroid Shooter with classes\asteroid_object_files\project_4 - Deltatime\graphics\laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.explosion_sound = pygame.mixer.Sound(r"D:\CODED_LIFE\###Udemy- Pygame\2- Asteroid Shooter with classes\asteroid_object_files\project_10 - Sound\sounds\explosion.wav")

        # float based position 
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0,-1)
        self.speed = 600
        
    def meteor_collision(self):
        if pygame.sprite.spritecollide(sprite=self, group=meteor_group, dokill=True, collided=pygame.sprite.collide_mask):
            self.explosion_sound.play()
            self.kill()

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))
        self.meteor_collision()
        if self.rect.midbottom[1] < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        
        # movement
        self.start_pos = None
        self.current_pos = None
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), 1)
        self.speed = random.randint(200, 400)
        self.generate_position()
        
        # setup
        image = pygame.image.load(r"D:\CODED_LIFE\###Udemy- Pygame\2- Asteroid Shooter with classes\asteroid_object_files\project_5 - Meteors\graphics\meteor.png").convert_alpha()
        image_size = pygame.math.Vector2(image.get_size()) * random.uniform(0.5, 1.5)
        self.og_surface = pygame.transform.scale(image, image_size)
        self.image = self.og_surface
        self.rect = self.image.get_rect(midbottom = self.start_pos)
        self.current_pos = pygame.math.Vector2(self.rect.midbottom)
        self.mask = pygame.mask.from_surface(self.image)
        
        # rotation
        self.rotation_angle = 0
        self.rotation_speed = random.randint(10, 35)

    def generate_position(self):
        pos_x = random.randint(-100, WINDOW_WIDTH + 100)
        pos_y = random.randint(-100, -50)
        self.start_pos = (pos_x, pos_y)
        
    def rotate(self):
        self.rotation_angle += self.rotation_speed * dt
        rotated_surface = pygame.transform.rotozoom(self.og_surface, self.rotation_angle, 1)
        self.image = rotated_surface
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.current_pos += self.direction * self.speed * dt
        self.rect.midbottom = (round(self.current_pos[0]), round(self.current_pos[1]))
        self.rotate()
        if self.rect.midtop[1] > WINDOW_HEIGHT:
            self.kill()
            
class Score:
	def __init__(self):
		self.font = pygame.font.Font(r'D:\CODED_LIFE\###Udemy- Pygame\2- Asteroid Shooter with classes\asteroid_object_files\project_6 - Score\graphics\subatomic.ttf', 30)

	def display(self):
		# exercise: recreate the original display_score function inside of a class
		# actually call it in the game loop
		score_text = f'Score: {pygame.time.get_ticks() // 1000}'
		text_surf = self.font.render(score_text,True,(255,255,255))
		text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
		display_surface.blit(text_surf,text_rect)
		pygame.draw.rect(
			display_surface, 
			(255,255,255),
			text_rect.inflate(30,30), 
			width = 8, 
			border_radius = 5
		)

# basic setup 
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1080, 700 
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()

# background 
background_surf = pygame.image.load(r'D:\CODED_LIFE\###Udemy- Pygame\2- Asteroid Shooter with classes\asteroid_object_files\project_4 - Deltatime\graphics\background.png').convert()

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

# sprite groups 
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# sprite creation 
ship = Ship(spaceship_group)

# score 
score = Score()

# music
bg_music = pygame.mixer.Sound(r'D:\CODED_LIFE\###Udemy- Pygame\2- Asteroid Shooter with classes\asteroid_object_files\project_10 - Sound\sounds\music.wav')
bg_music.play(loops = -1)

# game loop
while True:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_timer:
            Meteor(meteor_group)

    # delta time 
    dt = clock.tick() / 1000

    # background 
    display_surface.blit(background_surf,(0,0))

    # update
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()
    
    # score
    score.display()

    # graphics 
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

    # draw the frame 
    pygame.display.update()
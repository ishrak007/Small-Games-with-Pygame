import pygame 
from pygame.math import Vector2 as vector
from os import walk
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(groups)
        
        # setup
        self.animations = {}
        self.import_assets(path)
        self.frame_index = 0
        self.status = "down_idle"
        self.attacking = False
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        
        # float based movement
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200

        # collisions
        self.hitbox = self.rect.inflate(self.rect.width * -0.5, -self.rect.height / 2)
        self.collision_sprites = collision_sprites
        self.mask = pygame.mask.from_surface(self.image)
        
        # health
        self.health = 3
        self.is_vulnerable = True
        self.hit_time = None
        
        # sound 
        self.hit_sound = pygame.mixer.Sound(r'4- Western Shooter\Game_Objects\sound\hit.mp3')
        self.hit_sound.set_volume(0.5)
        self.shoot_sound = pygame.mixer.Sound(r'4- Western Shooter\Game_Objects\sound\bullet.wav')
        self.shoot_sound.set_volume(0.8)
        
    def import_assets(self, path):
        
        for index, data in enumerate(walk(path)):
            if index == 0:
                for folder in data[1]:
                    self.animations[folder] = []
            else:
                folder_path = data[0]
                directory = folder_path.split(f"{path}\\")[1]
                files = data[2]
                surfaces = []
                for file in sorted(files, key=lambda file: int(file.split(".")[0])):
                    final_path = f"{folder_path}/{file}"
                    image = pygame.image.load(final_path).convert_alpha()
                    scale_size = vector(image.get_size()) * 0.9
                    final_surface = pygame.transform.scale(image, scale_size)
                    surfaces.append(final_surface)
                self.animations[directory] = surfaces
                
    def move(self, dt):

        # normalize 
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # horiztonal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        
        # horizontal collision
        self.check_collision("horizontal")

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        
        # vertical collision
        self.check_collision("vertical")
        
    def check_collision(self, direction):
        
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    else:
                        self.hitbox.left = sprite.hitbox.right
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    else:
                        self.hitbox.top = sprite.hitbox.bottom
                self.rect.centerx = self.hitbox.centerx
                self.pos.x = self.rect.centerx
                self.rect.centery = self.hitbox.centery
                self.pos.y = self.rect.centery    
                
    def damage(self):
        if self.is_vulnerable:
            self.health -= 1
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks()
            
    def check_death(self):
        if self.health <= 0:
            self.kill()
    
    def blink(self):
        if not self.is_vulnerable:
            if self.wave():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0,0,0))
                self.image = white_surf
       
    def wave(self):
        value = sin(pygame.time.get_ticks())
        if value > 0:
            return True
        else:
            return False
     
    def vulnerability_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 400:
                self.is_vulnerable = True
  
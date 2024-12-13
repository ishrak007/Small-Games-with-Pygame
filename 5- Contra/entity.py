import pygame 
from pygame.math import Vector2 as vector
from settings import *
from os import walk
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, path, groups, shoot):
        super().__init__(groups)

        # graphics setup
        self.animations = {}
        self.import_assets(path)
        self.frame_index = 0
        self.status = "right"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS["Level"]
        self.mask = pygame.mask.from_surface(self.image)

        # image setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = LAYERS['Level']

        # float based movement 
        self.direction = vector()
        self.pos = vector(self.rect.topleft)
        self.speed = 400

        # shooting setup
        self.shoot = shoot
        self.can_shoot = True
        self.shoot_time = None
        self.cooldown = 200
        self.duck = False
        
        # health
        self.health = 3
        self.is_vulnerable = True
        self.hit_time = None
        self.invul_duration = 200 
        
        # audio
        self.hit_sound = pygame.mixer.Sound(r'5- Contra\Game_Objects\audio\hit.wav')
        self.hit_sound.set_volume(0.5)

    def damage(self):
        if self.is_vulnerable:
            self.health -= 1
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks()
            self.hit_sound.play()

    def check_death(self):
        if self.health <= 0:
            self.kill()
            
    def invul_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > self.invul_duration:
                self.is_vulnerable = True
                
    def blink(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0,0,0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False

    def animate(self, dt):
        current_animation = self.animations[self.status]
        # animate
        self.frame_index += 8 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]
          
    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.cooldown:
                self.can_shoot = True

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
  
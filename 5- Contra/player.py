import pygame, sys
from os import walk
from settings import *
from pygame.math import Vector2 as vector
from entity import Entity
from random import choice

class Player(Entity):
    def __init__(self, pos, path, groups, shoot, collision_sprites):
        super().__init__(pos, path, groups, shoot)

        # collisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites
        
        # vertical movement
        self.gravity = 15
        self.jump_speed = 1000
        self.on_floor = True
        self.duck = False
        self.jump = False
        self.moving_floor = None
        
        # overrides
        self.health = 10
        
        # sound
        sound_path = r"5- Contra\Game_Objects\audio"
        self.shoot_sounds = [pygame.mixer.Sound(sound_path + f"/shot {no}.mp3") for no in range(1, 4)]
        for sound in self.shoot_sounds:
            sound.set_volume(0.9) 
        
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_floor:
            self.direction.y = -self.jump_speed
            self.jump = True
            self.moving_floor = None
        if keys[pygame.K_DOWN]:
            self.duck = True
            self.direction.x = 0
        else:
            self.duck = False
            
        if keys[pygame.K_SPACE] and self.can_shoot:
            
            # shoot bullet
            direction = vector(1, 0) if self.status.split('_')[0] == 'right' else vector(-1,0)
            pos = self.rect.center + direction * 60
            y_offset = vector(0, -16) if not self.duck else vector(0, 10)
            self.shoot(pos + y_offset, direction, self)
            choice(self.shoot_sounds).play()
            
            # reactivate gun
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def get_status(self):
        
        if not self.jump: 
            if self.direction.x == 0:
                if self.duck and not self.jump:
                    self.status = f"{self.status.split("_")[0]}_duck" 
                else:
                    self.status = f"{self.status.split("_")[0]}_idle" 
        else:
            self.status = f"{self.status.split("_")[0]}_jump"
    
    def move(self, dt):
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.x = round(self.pos.x)
        self.rect.x = self.hitbox.x
        self.check_collision("horizontal")
        
        # vertical movement
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt

        if self.moving_floor and self.moving_floor.direction.y > 0:
            self.direction.y = 0
            self.rect.bottom = self.moving_floor.rect.top
            self.pos.y = self.rect.y
            self.on_floor = True
        
        self.hitbox.y = round(self.pos.y)
        self.rect.y = self.hitbox.y  # self.hitbox.y
        self.check_collision("vertical")
 
    def check_collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    # left collision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    self.pos.x = self.rect.x
                else:
                    # detect moving floor
                    if hasattr(sprite, "direction"):
                        self.moving_floor = sprite
                    else:
                        self.moving_floor = None
                    # top collision
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        if self.moving_floor:
                            self.moving_floor.direction.y = -1
                    # bottom collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                        self.jump = False
                    self.pos.y = self.rect.y
                    self.direction.y = 0
                    
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False
    
    def check_death(self):
        if self.health <= 0:
            pygame.quit()
            sys.exit()
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.invul_timer()
        self.blink()
        self.shoot_timer()
        self.check_death()
      
            
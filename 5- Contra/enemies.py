import pygame 
from os import walk
from settings import *
from pygame.math import Vector2 as vector
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, path, groups, player, shoot, collision_sprites):
        super().__init__(pos, path, groups, shoot)

        # placement
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites
        for sprite in collision_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top
        
        # player
        self.player = player
        
        # overrides
        self.cooldown = 1000
        
        # sound
        self.shoot_sound = pygame.mixer.Sound(r'5- Contra\Game_Objects\audio\shot 4.mp3')
        self.shoot_sound.set_volume(0.9)

    def get_status(self):
        if self.player.rect.centerx < self.rect.centerx:
            self.status = 'left'
        else:
            self.status = 'right'

    def check_fire(self):
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)

        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False

        if distance < 600 and same_y and self.can_shoot:
            
            # shoot bullet
            bullet_direction = vector(1, 0) if self.status == 'right' else vector(-1, 0)
            y_offset = vector(0, -16)
            pos = self.rect.center + bullet_direction * 80
            self.shoot(pos + y_offset, bullet_direction, self)
            self.shoot_sound.play()

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def update(self,dt):
        self.get_status()
        self.animate(dt)
        self.shoot_timer()
        self.invul_timer()
        self.blink()
        self.check_fire()
        self.check_death()
    
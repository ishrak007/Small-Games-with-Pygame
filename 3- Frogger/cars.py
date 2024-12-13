import pygame
import os
import random
from settings import *

class Car(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.name = "car"
        self.generate_car()
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(0, -(self.rect.height / 2))
    
        # float based position
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 250
        
        if pos[0] < 200:
            self.direction = pygame.math.Vector2(1, 0)
        else:
            self.direction = pygame.math.Vector2(-1, 0)
            self.image = pygame.transform.flip(self.image, True, False)
            
    def generate_car(self):
        path = r"3- Frogger\Game_Objects\graphics\cars"
        for folder_name, _, car_surfs in os.walk(path):
            car_choice = random.choice(car_surfs)
            surface = pygame.image.load(f"{folder_name}/{car_choice}").convert_alpha()
            scale_size = pygame.math.Vector2(surface.get_size()) * 0.85
            self.image = pygame.transform.scale(surface, scale_size)
            
    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.hitbox.center = (round(self.pos.x), round(self.pos.y))
        self.rect.center = self.hitbox.center
    
    def update(self, dt):
        self.move(dt)
        
        # destroy if out of window
        if not -200 < self.rect.x < 3500:
            self.kill()
        
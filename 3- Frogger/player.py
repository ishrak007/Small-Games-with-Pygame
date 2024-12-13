import pygame
from os import walk
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, group, obstacle_group, pos):
        super().__init__(group)
        self.import_assets()
        self.frame_index = 0
        self.face = "up"
        self.moving = False
        self.image = self.animations[self.face][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        
        # float based position
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200
        
        # collision
        self.collision_sprites = obstacle_group
        self.hitbox = self.rect.inflate(0,-self.rect.height / 2)
        
    def move(self, dt):
        
        # normalizing vector (making the vector length 1)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.check_collision("horizontal")
        
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.check_collision("vertical")
     
    def import_assets(self):
        main_path = r"3- Frogger\progress_files\project_4 - animation1\graphics\player"
        directions = []
        self.animations = {}
        
        for index, data in enumerate(list(walk(main_path))):
            if index == 0:
                directions = data[1]
            else:
                folder_name = data[0]
                file_names = data[2]
                surface_objects = []
                for frame in file_names:
                    image = pygame.image.load(f"{folder_name}/{frame}").convert_alpha()
                    scale_size = pygame.math.Vector2(image.get_size()) * 0.85
                    surface_objects.append(pygame.transform.scale(image, scale_size)) # [pygame.transform.scale(pygame.image.load(f"{folder_name}/{frame}").convert_alpha(), ) for frame in file_names]
                self.animations[directions[index - 1]] = surface_objects
       
    def animate(self, dt):
        current_direction = self.animations[self.face]
        if self.moving:
            self.frame_index += 10 * dt
            if self.frame_index >= len(current_direction):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_direction[int(self.frame_index)]
    
    def check_collision(self, direction):
        
        if direction == "horizontal":
            for sprite in self.collision_sprites.sprites():
                if sprite.rect.colliderect(self.rect):
                    if hasattr(sprite, "name") and sprite.name == "car":
                        pygame.quit()
                        sys.exit()
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.rect.centerx
        else:
            for sprite in self.collision_sprites.sprites():
                if sprite.rect.colliderect(self.rect):
                    if hasattr(sprite, "name") and sprite.name == "car":
                        pygame.quit()
                        sys.exit()
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.rect.centery

    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery
     
    def get_input(self):
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.moving = True
            
            # horizontal input
            if keys[pygame.K_LEFT]:
                # self.moving = True
                self.direction.x = -1
                self.face = "left"
            elif keys[pygame.K_RIGHT]:
                # self.moving = True
                self.direction.x = 1
                self.face = "right"
        
            # vertical input
            if keys[pygame.K_UP]:
                # self.moving = True
                self.direction.y = -1
                self.face = "up"
            elif keys[pygame.K_DOWN]:
                # self.moving = True
                self.direction.y = 1
                self.face = "down"
            
        else:
            self.moving = False
            self.direction.x = 0
            self.direction.y = 0
            
    def update(self, dt):
        self.get_input()
        self.move(dt)
        self.animate(dt)
        self.restrict()
        
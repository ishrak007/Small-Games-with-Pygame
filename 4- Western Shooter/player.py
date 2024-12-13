import pygame, sys
from pygame.math import Vector2 as vector
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites, create_bullet):
        super().__init__(pos, groups, path, collision_sprites)
        
        # overwrites
        self.health = 10
        
        # bullet info
        self.shoot_bullet = create_bullet
        self.bullet_shot = False
        self.bullet_direction = None

    def get_status(self):
        
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = f"{self.status.split("_")[0]}_idle"
        
        # attacking
        if self.attacking:
            self.status = f"{self.status.split("_")[0]}_attack"

    def animate(self, dt):
        
        # current animation state
        current_animation = self.animations[self.status]
        
        # animate
        self.frame_index += 8 * dt
        
        # shoot bullet
        if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:
            bullet_start_pos = self.rect.center + self.bullet_direction * 80
            if self.status.split("_")[0] == "up":
                bullet_start_pos += vector(15, 0)
            elif self.status.split("_")[0] == "down":
                bullet_start_pos -= vector(15, 0)
            self.shoot_bullet(bullet_start_pos, self.bullet_direction)
            self.bullet_shot = True
            self.shoot_sound.play()
        
        # cycling through the animation
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
                
        # show the frame
        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)
    
    def get_input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            if keys[pygame.K_RIGHT]:
                self.status = "right"
                self.direction.x = 1
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            if keys[pygame.K_UP]:
                self.status = "up"
                self.direction.y = -1
            elif keys[pygame.K_DOWN]:
                self.status = "down"
                self.direction.y = 1
            else:
                self.direction.y = 0
                
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = vector()
                self.frame_index = 0
                self.bullet_shot = False
                
                match self.status.split("_")[0]:
                    case "left": self.bullet_direction = vector(-1, 0)
                    case "right": self.bullet_direction = vector(1, 0)
                    case "up": self.bullet_direction = vector(0, -1)
                    case "down": self.bullet_direction = vector(0, 1)

    def check_death(self):
        if self.health <= 0:
            pygame.quit()
            sys.exit()

    def update(self, dt):
        self.get_input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.blink()
        self.vulnerability_timer()
        self.check_death()
        
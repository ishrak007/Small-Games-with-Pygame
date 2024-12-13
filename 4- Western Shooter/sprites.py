import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-self.rect.height / 3)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, surf, group):
        super().__init__(group)
        self.image = surf
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)

        # float based position
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = direction
        self.speed = 400
        
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

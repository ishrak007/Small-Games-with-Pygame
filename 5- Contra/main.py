import pygame, sys
from settings import *
from tiles import *
from player import Player
from enemies import Enemy
from bullets import Bullet, FireAnimation
from overlay import Overlay
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2 as vector

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        
        # import
        self.fg_sky = pygame.image.load(r'5- Contra\Game_Objects\graphics\sky\fg_sky.png').convert_alpha()
        self.bg_sky = pygame.image.load(r'5- Contra\Game_Objects\graphics\sky\bg_sky.png').convert_alpha()
        tmx_map = load_pygame(r'5- Contra\Game_Objects\data\map.tmx')

        # dimensions
        self.padding = WINDOW_WIDTH / 2
        self.sky_width = self.bg_sky.get_width()
        map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
        self.sky_num = int(map_width // self.sky_width)
        
    def custom_draw(self, player):
        
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2
        
        for x in range(self.sky_num):
            x_pos = - self.padding + x * self.sky_width
            self.display_surface.blit(self.bg_sky, (x_pos - self.offset.x / 2.5, 800 - self.offset.y / 2.5))
            self.display_surface.blit(self.fg_sky, (x_pos - self.offset.x / 2, 800 - self.offset.y / 2))
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
            
class Game:
    def __init__(self):
        
        # game initialization
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Contra")
        self.clock = pygame.time.Clock()
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.vulnerable_sprites = pygame.sprite.Group()
        
        # setup
        self.setup()
        self.overlay = Overlay(self.player)
        
        # bullet images 
        self.bullet_surf = pygame.image.load(r'5- Contra\Game_Objects\graphics\bullet.png').convert_alpha()
        self.fire_surfs = [
			pygame.image.load(r'5- Contra\Game_Objects\graphics\fire\0.png').convert_alpha(),
			pygame.image.load(r'5- Contra\Game_Objects\graphics\fire\1.png').convert_alpha()]
        
        # music
        self.music = pygame.mixer.Sound(r'5- Contra\Game_Objects\audio\music.wav')
        self.music.play(loops = -1)
        
    def setup(self):
        tmx_map = load_pygame(r"5- Contra\Game_Objects\data\map.tmx")
        
        for x, y, surf in tmx_map.get_layer_by_name("Level").tiles():
                CollisionTile((x * 64, y * 64), surf, [self.all_sprites, self.collision_sprites], LAYERS["Level"])
                 
        for layer in ["FG Detail Top", "FG Detail Bottom", "BG", "BG Detail"]:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * 64, y * 64), surf, self.all_sprites, LAYERS[layer])
            
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(pos = (obj.x, obj.y), 
                                     path = r"5- Contra\Game_Objects\graphics\player", 
                                     groups = [self.all_sprites, self.vulnerable_sprites] , 
                                     shoot = self.shoot, 
                                     collision_sprites = self.collision_sprites)
            if obj.name == 'Enemy':
                Enemy(pos = (obj.x, obj.y), 
                      path = r"5- Contra\Game_Objects\graphics\enemy", 
                      groups = [self.all_sprites, self.vulnerable_sprites], 
                      player = self.player, 
                      shoot = self.shoot, 
                      collision_sprites = self.collision_sprites)
        
        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingPlatform((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.platform_sprites], LAYERS["Level"])
            else: # border 
                border_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border_rects.append(border_rect)

    def shoot(self, pos, direction, entity):
        
        Bullet(pos, self.bullet_surf, direction, [self.all_sprites, self.bullet_sprites])
        FireAnimation(entity, self.fire_surfs, direction, self.all_sprites)
        
    def bullet_collisions(self):
        
        # obstacles 
        for obstacle in self.collision_sprites.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullet_sprites, True)

        # entities 
        for sprite in self.vulnerable_sprites.sprites():
            if pygame.sprite.spritecollide(sprite, self.bullet_sprites, True, pygame.sprite.collide_mask ):
                sprite.damage()
                
    def platform_collisions(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0: # up
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else: # down
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1
        
    def run(self):
        while True:
            
            # event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.display_surface.fill((249, 131, 103))
            dt = self.clock.tick() / 1000
            
            self.platform_collisions()
            self.all_sprites.update(dt)
            self.bullet_collisions()
            self.all_sprites.custom_draw(self.player)
            self.overlay.display()
            
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
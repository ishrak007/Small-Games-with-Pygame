import pygame, sys
from settings import * 
from pygame.math import Vector2 as vector
from player import Player
from monsters import *
from sprites import Sprite, Bullet
from pytmx.util_pygame import load_pygame

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load(r"4- Western Shooter\Game_Objects\graphics\other\bg.png").convert()
        
    def customize_draw(self, player):
        
        # change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2 
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2
        
        # blit the surfaces 
        self.display_surface.blit(self.bg, -self.offset)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect) 

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Western shooter')
        self.clock = pygame.time.Clock()
        self.bullet_surf = pygame.image.load(r"4- Western Shooter\Game_Objects\graphics\other\particle.png").convert_alpha()

        # groups 
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

        self.setup()
        self.bg_music = pygame.mixer.Sound(r"4- Western Shooter\Game_Objects\sound\music.mp3")
        self.bg_music.play(loops = -1)

    def setup(self):
        
        tmx_map = load_pygame(r'4- Western Shooter\Game_Objects\data\map.tmx')
        
        # tiles
        for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
            Sprite((x * 64, y * 64), surf, [self.all_sprites, self.obstacles])

        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y), self.all_sprites, PATHS['player'], self.obstacles, self.create_bullet)
                
            if obj.name == "Coffin":
                Coffin((obj.x,obj.y), [self.all_sprites, self.monsters], PATHS['coffin'], self.obstacles, self.player)
                
            if obj.name == "Cactus":
                Cactus((obj.x,obj.y), [self.all_sprites, self.monsters], PATHS['cactus'], self.obstacles, self.player, self.create_bullet)

    def create_bullet(self, pos, direction):
        Bullet(pos, direction, self.bullet_surf, [self.all_sprites, self.bullets])

    def bullet_collision(self): 

        # bullet obstacle collision
        for obstacle in self.obstacles.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullets, True, pygame.sprite.collide_mask)
        
        # monster bullet collision
        for monster in self.monsters:
            if pygame.sprite.spritecollide(monster, self.bullets, True, pygame.sprite.collide_mask):
                monster.damage()

        # player bullet collision
        if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
            self.player.damage()

    def run(self):
        while True:
            # event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
            dt = self.clock.tick() / 1000

            # update groups 
            self.all_sprites.update(dt)
            self.bullet_collision()

            # draw groups
            self.all_sprites.customize_draw(self.player)

            pygame.display.update()  
    
if __name__ == '__main__':
    game = Game()
    game.run()
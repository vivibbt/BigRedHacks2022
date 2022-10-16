import pygame
from settings import *
import player
from overlay import *
from sprites import *
import time
import timer


class Level(object):
    def __init__(self):


        self.mini=0

        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.setup()



    def setup(self):
        self.player = player.Player((439, 36), self.all_sprites)

        self.display = Generic(pos=(0,0), surf=pygame.image.load('Assets/main1.png').convert_alpha(),
                groups=self.all_sprites, z = LAYERS['ground'])

    def run(self,dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        if self.player.fishtext_index > 0 or self.player.cowtext_index > 0:
            self.display.image = pygame.image.load('Assets/main.png')
        else: 
            self.display.image = pygame.image.load('Assets/main1.png')


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        if player.rect.centerx>=400 and player.rect.centerx<=1000:
            self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        if player.rect.centery >= 300 and player.rect.centery <= 370:
            self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2




        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset

                    self.display_surface.blit(sprite.image, offset_rect)

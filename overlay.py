import pygame
from main import *
import level
import player
import sprites


class Overlay:
    def __init__(self):
        self. display_surface = pygame.display.get_surface()
        self.all_sprites = level.CameraGroup()



















class platform(Overlay):
    def __init__(self):
        super().__init__()

    def display(self):
        rectangle = pygame.Rect(200, 200, 400, 400)
        pygame.draw.rect(WIN, (0, 0, 0), rectangle)

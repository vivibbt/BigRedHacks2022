import pygame
from sys import exit
from level import *
import player
from settings import *
from fishgame import *
import random



#Icon
img = pygame.image.load('Assets/2022.png')
pygame.display.set_icon(img)

#DISPLAY SETTINGS

WIN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("BRH2022 Gabe Goes Green")

class Game(object):

    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('test.mp3')
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()
        self.level = level.Level()
        self.fish = 0


    def main(self):
        clock = pygame.time.Clock()
        run = True


        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()

            dt = self.clock.tick() / 1000

            self.level.run(dt)
            

            if self.level.mini == 2:
                if self.fish == 0:
                    print('hi')
                    self.fish = Fishgame()
                    self.fish.run(WIN,dt,clock)
                    self.level.mini =0
                    print('r')

            pygame.display.update()



if __name__ == "__main__":  # only runs this file if this file is run directly
    game = Game()
    game.main()
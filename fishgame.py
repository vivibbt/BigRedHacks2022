import pygame
from settings import *
import player
from overlay import *
import sprites
import level
import random
from main import *
import sys

class Fishgame:
    def __init__(self):

        self.swim1 = (pygame.image.load('Assets/Gabe/swim/swim1.png').convert_alpha())
        self.swim2 = (pygame.image.load('Assets/Gabe/swim/swim2.png').convert_alpha())
        self.swim3 = (pygame.image.load('Assets/Gabe/swim/swim3.png').convert_alpha())
        self.swim4 = (pygame.image.load('Assets/Gabe/swim/swim4.png').convert_alpha())
        self.swim5 = (pygame.image.load('Assets/Gabe/swim/swim5.png').convert_alpha())
        self.swim6 = (pygame.image.load('Assets/Gabe/swim/swim6.png').convert_alpha())
        self.swim7 = (pygame.image.load('Assets/Gabe/swim/swim7.png').convert_alpha())

        self.swim_frames = [self.swim1,self.swim2,self.swim3,self.swim4,self.swim5,self.swim6,self.swim7]
        self.swim_index=0

        self.garb1 = pygame.transform.scale2x(pygame.image.load('Assets/garb1.png'))
        self.garb2 = pygame.transform.scale2x(pygame.image.load('Assets/garb2.png'))
        self.garb3 = pygame.transform.scale2x(pygame.image.load('Assets/garb3.png'))
        self.garb4 = pygame.transform.scale2x(pygame.image.load('Assets/garb4.png'))
        self.garb5 = pygame.transform.scale2x(pygame.image.load('Assets/garb5.png'))

        self.garb_surface = random.choice([self.garb1,self.garb2,self.garb3,self.garb4,self.garb5])



        self.bg_surface = pygame.image.load('Assets/underwaterO.png')

        self.bgX = 0
        self.bgX2 = self.bg_surface.get_width()


        self.game_over_surface = pygame.image.load('Assets/done.png').convert_alpha()
        self.game_over_rect = self.game_over_surface.get_rect(center=(288, 512))

        self.garb_list = []
        self.SPAWNPIPE = pygame.USEREVENT
        self.spawntime = pygame.time.set_timer(self.SPAWNPIPE, 1200)
        self.score = 0
        self.gravity = .3
        self.time = 0
        self.WINNER = pygame.USEREVENT + 1

        self.guy_movement = 0
        self.game_active = True
        self.game_font = pygame.font.Font('04B_19.ttf', 40)


        self.display_surface = pygame.display.get_surface()
        self.all_sprites = level.CameraGroup()
        self.setup()

        self.offset = pygame.math.Vector2()

    def setup(self):
        self.player = player.Player((125, 270), self.all_sprites)
        sprites.Generic(pos=(0,0), surf=self.bg_surface,
                groups=self.all_sprites, z = LAYERS['fishgame'])
        self.player.timers['fishgame'].activate()
        self.player.direction = pygame.math.Vector2()

    def custom_draw(self):
        if self.player.rect.centerx>=400 and self.player.rect.centerx<=1000:
            self.offset.x = self.player.rect.centerx - SCREEN_WIDTH / 2
        if self.player.rect.centery >= 300 and self.player.rect.centery <= 370:
            self.offset.y = self.player.rect.centery - SCREEN_HEIGHT / 2


        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset

                    self.display_surface.blit(sprite.image, offset_rect)

    def guy_animation(self):
        new_guy = self.swim_frames[self.swim_index]
        new_guy_rect = new_guy.get_rect(center=(100, self.player.rect.centery))
        return new_guy, new_guy_rect

    def create_garb(self):

        junk = random.choice([self.garb1,self.garb2,self.garb3,self.garb4,self.garb5])
        self.garb_surface = junk
        random_pipe_pos = random.choice([50,100,150,200,250,300])
        trash = self.garb_surface.get_rect(midtop=(900, random_pipe_pos))
        trash1 = self.garb_surface.get_rect(midtop=(900, random_pipe_pos))
        return trash, trash1

    def move_garb(self,garbs):
        for garb in garbs:
            garb.centerx -= 7
        visible_garb = [garb for garb in garbs if garb.right > -50]
        return visible_garb

    def draw_garb(self,garbs,screen):
        for garb in garbs:
            screen.blit(self.garb_surface, garb)

    def check_collision(self,garbs):
        for garb in garbs:
            if self.player.rect.colliderect(garb):
                self.garb_list=[]
                self.score += 1
                return True

        if self.player.rect.top <= 0 or self.player.rect.bottom >= SCREEN_HEIGHT:
            return True

        return True


    def rotate_guy(self):
        new_guy = pygame.transform.rotozoom(self.player.image, -self.guy_movement * 3, 1)
        return new_guy

    def score_display(self,screen,game_state):
        if game_state == 'main_game':
            score_surface = self.game_font.render(str(int(self.score)), True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(SCREEN_WIDTH/2, 75))
            screen.blit(score_surface, score_rect)
        if game_state == 'game_over':
            score_surface = self.game_font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(SCREEN_WIDTH/2, 100))
            screen.blit(score_surface, score_rect)

    def pipe_score_check(self):
        if self.garb_list:
            for pipe in self.garb_list:
                if 95 < pipe.centerx < 105:
                    self.score += 1

    def run(self,screen,dt,clock):
        while True:

            self.bgX -= 2.2
            self.bgX2 -= 2.2
            if self.bgX < self.bg_surface.get_width() * -1:
                self.bgX = self.bg_surface.get_width()
            if self.bgX2 < self.bg_surface.get_width() * -1:
                self.bgX2 = self.bg_surface.get_width()

            screen.blit(self.bg_surface, (self.bgX, 0))
            screen.blit(self.bg_surface, (self.bgX2, 0))


            if self.score == 10:
                pygame.event.post(pygame.event.Event(self.WINNER))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.guy_movement = 0
                        self.guy_movement -= 12

                if event.type == self.SPAWNPIPE:

                    self.garb_list.extend(self.create_garb())

                if event.type == self.WINNER:
                    self.game_active=False



            if self.time > .2:
                self.time = 0
                if self.swim_index < 6:
                    self.swim_index += 1
                else:
                    self.swim_index = 0
            else:
                self.time +=dt

            self.player.image, self.player.rect = self.guy_animation()

            if self.game_active:
                self.guy_movement += self.gravity
                rotated_guy = self.rotate_guy()
                if self.player.rect.centery > SCREEN_HEIGHT+150:
                    self.player.rect.centery =-100
                    self.guy_movement = 0

                elif self.player.rect.centery < -150:
                    self.player.rect.centery =SCREEN_HEIGHT + 100
                    self.guy_movement = 0
                else:
                    self.player.rect.centery += self.guy_movement

                screen.blit(rotated_guy, self.player.rect)
                self.game_active = self.check_collision(self.garb_list)

                self.garb_list = self.move_garb(self.garb_list)
                self.draw_garb(self.garb_list,screen)

                self.score_display(screen,'main_game')
            else:
                self.score_display(screen,'game_over')
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    break

            pygame.display.update()
            clock.tick(120)





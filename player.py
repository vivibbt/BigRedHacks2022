import pygame
from support import *
from timer import *
from settings import *
from overlay import *
from level import *
from fishgame import *
import time
from sprites import * 

# Class for Entities
# Sub-classes contain more specific entities


class Player(pygame.sprite.Sprite):


    def __init__(self,pos,group):
        super().__init__(group)

        self.clock = pygame.time.Clock()

        self.import_assets()
        self.status = 'idle'
        self.fishtext_index = 0
        self.cowtext_index = 0

        self.frame_index = 0

        #0=no minigame 1=platformer 2=fishing
        self.mini = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 270

        self.timers = {
            'tool use': Timer(50),
            'fishgame': Timer(500000)
        }

        self.selected_tool = 'hands'

    def import_assets(self):
        self.animations = {'up':[],'down':[],'left':[],'right':[],'idle':[],'swim':[],'idle_left':[],'idle_right':[]}

        for animation in self.animations.keys():
            full_path = 'Assets/Gabe/' + animation

            self.animations[animation] = import_folder(full_path)


    def animate(self,dt):
        self.frame_index += 6*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index =0
        self.image = self.animations[self.status][int(self.frame_index)].convert_alpha()



    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active and not self.timers['fishgame'].active:
            if keys[pygame.K_a] and self.pos.x>15:
                self.direction.x = -1
                self.status = 'left'
                self.animations['idle'] = self.animations['idle_left']
            elif keys[pygame.K_d] and self.pos.x<1375:
                self.direction.x = 1
                self.status = 'right'
                self.animations['idle'] = self.animations['idle_right']
            else:
                self.direction.x = 0

            if keys[pygame.K_w] and self.pos.y>36:
                self.direction.y = -1
                self.status = 'up'
                self.animations['idle'] = self.animations['idle_right']
            elif keys[pygame.K_s] and self.pos.y<635:
                self.direction.y = 1
                self.status = 'down'
                self.animations['idle'] = self.animations['idle_left']
            else:
                self.direction.y =0


            if keys[pygame.K_w] and keys[pygame.K_a]:
                self.status = 'left'
                self.animations['idle'] = self.animations['idle_left']
            elif keys[pygame.K_s] and keys[pygame.K_d]:
                self.status = 'right'
                self.animations['idle'] = self.animations['idle_right']

    def get_status(self):
        if self.direction.magnitude()==0:
            self.status = 'idle'

        if self.timers['tool use'].active:
            self.status = 'idle'

        if self.timers['fishgame'].active:
            self.status = 'swim'

    def talking(self):
        while (self.cowtext_index>0 or self.fishtext_index>0) and not self.timers['tool use'].active:
            self.timers['tool use'].activate()
            self.direction.x = 0
            self.direction.y = 0

    def update_timers(self):

        for timer in self.timers.values():
            timer.update()

    def move(self, dt):
        if self.direction.magnitude()>0:
            self.direction = self.direction.normalize()

        #horiz
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        #verti
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def collision(self):
        tolerance = 10
        self.left = self.rect.x
        self.right = self.rect.x + self.rect.width
        self.top = self.rect.y
        self.bottom = self.rect.y + self.rect.height
        tree1_rect = pygame.Rect(0, 0, 160, 150)
        topwater_rect = pygame.Rect(160, 0, 200, 390)
        bottom_rect = pygame.Rect(0, 530, 1150, 121)
        house_rect = pygame.Rect(515, 0, 330, 330)
        tree2_rect = pygame.Rect(1240, 180, 160, 200)
        pond_rect = pygame.Rect(1190, 0, 210, 165)

        if self.rect.colliderect(tree1_rect):
            if abs(self.left - tree1_rect.right) < tolerance:
                self.pos.x = tree1_rect.right + 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.right - tree1_rect.left) < tolerance:
                self.pos.x = tree1_rect.left - 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.top - tree1_rect.bottom) < tolerance:
                self.pos.y = tree1_rect.bottom + 3 * tolerance
                self.rect.centery = self.pos.y
            if abs(self.bottom - tree1_rect.top) < tolerance:
                self.pos.y = tree1_rect.top - 3 * tolerance
                self.rect.centery = self.pos.y
        if self.rect.colliderect(topwater_rect):
            if abs(self.left - topwater_rect.right) < tolerance:
                self.pos.x = topwater_rect.right + 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.right - topwater_rect.left) < tolerance:
                self.pos.x = topwater_rect.left - 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.top - topwater_rect.bottom) < tolerance:
                self.pos.y = topwater_rect.bottom + 3 * tolerance
                self.rect.centery = self.pos.y
            if abs(self.bottom - topwater_rect.top) < tolerance:
                self.pos.y = topwater_rect.top - 3 * tolerance
                self.rect.centery = self.pos.y
        if self.rect.colliderect(bottom_rect):
            if abs(self.left - bottom_rect.right) < tolerance:
                self.pos.x = bottom_rect.right + 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.right - bottom_rect.left) < tolerance:
                self.pos.x = bottom_rect.left - 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.top - bottom_rect.bottom) < tolerance:
                self.pos.y = bottom_rect.bottom + 3 * tolerance
                self.rect.centery = self.pos.y
            if abs(self.bottom - bottom_rect.top) < tolerance:
                self.pos.y = bottom_rect.top - 3 * tolerance
                self.rect.centery = self.pos.y
        if self.rect.colliderect(house_rect):
            if abs(self.left - house_rect.right) < tolerance:
                self.pos.x = house_rect.right + 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.right - house_rect.left) < tolerance:
                self.pos.x = house_rect.left - 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.top - house_rect.bottom) < tolerance:
                self.pos.y = house_rect.bottom + 3 * tolerance
                self.rect.centery = self.pos.y
            if abs(self.bottom - house_rect.top) < tolerance:
                self.pos.y = house_rect.top - 3 * tolerance
                self.rect.centery = self.pos.y
        if self.rect.colliderect(tree2_rect):
            if abs(self.left - tree2_rect.right) < tolerance:
                self.pos.x = tree2_rect.right + 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.right - tree2_rect.left) < tolerance:
                self.pos.x = tree2_rect.left - 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.top - tree2_rect.bottom) < tolerance:
                self.pos.y = tree2_rect.bottom + 3 * tolerance
                self.rect.centery = self.pos.y
            if abs(self.bottom - tree2_rect.top) < tolerance:
                self.pos.y = tree2_rect.top - 3 * tolerance
                self.rect.centery = self.pos.y
        if self.rect.colliderect(pond_rect):
            if abs(self.left - pond_rect.right) < tolerance:
                self.pos.x = pond_rect.right + 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.right - pond_rect.left) < tolerance:
                self.pos.x = pond_rect.left - 3 * tolerance
                self.rect.centerx = self.pos.x
            if abs(self.top - pond_rect.bottom) < tolerance:
                self.pos.y = pond_rect.bottom + 3 * tolerance
                self.rect.centery = self.pos.y
            if abs(self.bottom - pond_rect.top) < tolerance:
                self.pos.y = pond_rect.top - 3 * tolerance
                self.rect.centery = self.pos.y

    def fisherman_dialogue(self, dt, clock):
        fisherman_rect = pygame.Rect(105, 185, 50, 80)
        if (pygame.key.get_pressed()[pygame.K_SPACE] & abs(
                (self.pos.x - (fisherman_rect.left + fisherman_rect.width / 2)) < 50) &
                abs((self.pos.y - (fisherman_rect.top + fisherman_rect.height / 2)) < 50)):
            time.sleep(0.2)
            self.fishtext_index += 1
        if (self.fishtext_index > 0):
            if (self.fishtext_index == 8):
                self.fish = Fishgame()
                self.fish.run(WIN, dt, clock)
                return
            if (self.fishtext_index == 12):
                self.fishtext_index = 0
                return
            text = pygame.image.load('Assets/fisherman_text/' + str(self.fishtext_index) + '.png')
            WIN.blit(text, (125, 0))



    def cow_dialogue(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] & (abs(self.pos.x - 970) < 100) & (abs(self.pos.y - 320) < 50):
            time.sleep(0.2)
            self.cowtext_index += 1
        if (self.cowtext_index > 0):
            if (self.cowtext_index == 8):
                exec(open("manure_mini.py").read())
                self.cowtext_index = 9
                return
            if (self.cowtext_index == 11):
                self.cowtext_index = 0
                return
            text = pygame.image.load('Assets/cow_text/' + str(self.cowtext_index) + '.png')
            WIN.blit(text, (375, 60))
        

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()

        self.talking()

        self.collision()
        self.move(dt)
        self.cow_dialogue()

        self.fisherman_dialogue(dt, self.clock)
        self.animate(dt)




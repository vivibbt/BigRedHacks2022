import pygame 
from settings import *
from support import import_folder
from tile import *

class Gabe1(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.import_assets()
        
        self.status = 'idle'
        self.facing_right = True

        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # Gabe1 movement 
        self.direction = pygame.math.Vector2()
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = 16
        self.collision_sprites = collision_sprites
        self.on_floor = False

    def import_assets(self):
        self.animations = {'up':[],'down':[],'left':[],'right':[],'idle':[], 'idle_left':[]}

        for animation in self.animations.keys():
            full_path = 'Assets/Gabe/' + animation

            self.animations[animation] = import_folder(full_path)
    
    def animate(self):
		# loop over frame index 
        self.frame_index += self.animation_speed        
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index =0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed ()

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.direction.x = 1
            self.status = 'right'
            self.facing_right = True
            
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.direction.x = -1
            self.status = 'left'
            self.facing_right = False
        
        else:
            self.direction.x = 0
            if self.facing_right:
                self.status = 'idle'
            else:
                self.status = 'idle_left'
        

        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_floor:
            self.direction.y = -self.jump_speed

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if str(sprite) == '<Manure Sprite(in 2 groups)>':
                    p_counter.x -= 1
                    sprite.kill()

                if self.direction.x < 0: 
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0: 
                    self.rect.right = sprite.rect.left

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if str(sprite) == '<Manure Sprite(in 2 groups)>':
                    p_counter.x -= 1
                    sprite.kill()

                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_floor = True
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

        if self.on_floor and self.direction.y != 0:
            self.on_floor = False


    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def get_status(self):
        if self.direction.magnitude()==0:
            self.status = 'idle'

        if self.timers['tool use'].active:
            self.status = 'idle'

    def update(self):
        self.input()
        self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()
        self.apply_gravity()
        self.vertical_collisions()
        self.animate()
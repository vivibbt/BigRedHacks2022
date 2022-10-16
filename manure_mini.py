import pygame, sys
from settings import * 
from mini1_level import mini1_Level
from tile import p_counter

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
background_sf = pygame.image.load('Assets/manure_background.png')
pygame.display.set_caption('BRH2022 Gabe Goes Green')
font = pygame.font.Font('04B_19.ttf', 50)
clock = pygame.time.Clock()

# Background Cows
cow1_sf = pygame.image.load('Assets/cow1.png').convert_alpha()
cow3_sf = pygame.image.load('Assets/cow3.png').convert_alpha()
cow4_sf = pygame.image.load('Assets/cow4.png').convert_alpha()

mini1_level = mini1_Level()

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    counter_text = font.render(f'{p_counter.x} remaining', True, "Black")
    # bakcground image
    screen.blit(background_sf, (0,0))
    
    # background cows
    screen.blit(cow4_sf, (110, 465))
    screen.blit(cow1_sf, (78,328))
    screen.blit(cow4_sf, (370,385))
    screen.blit(cow3_sf, (450,350))
    screen.blit(cow3_sf, (500, 475))
    screen.blit(cow4_sf, (655,495))
    screen.blit(cow1_sf, (735,335))

    mini1_level.run()

    screen.blit(counter_text, (500,25))


    # drawing logic
    pygame.display.update()
    clock.tick(60)    
    
    # exit when you finish (NOT PERMENANT)
    if (p_counter.x <=0):
        break




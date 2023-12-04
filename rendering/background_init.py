import pygame
from globals import globals
def init_second_background(screen):
    screen.fill('#14152c')


def init_background(screen):
    screen.fill(globals.BLACK)
    background_image = pygame.image.load("assets/background.png")
    # Calculate the new propotional hight
    new_hight = int((background_image.get_width() / globals.screen_width) * globals.screen_height)
    background_image = pygame.transform.scale(background_image, (globals.screen_width, new_hight))
    screen.blit(background_image, (0, 0))
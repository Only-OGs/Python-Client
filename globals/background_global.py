import game.globals
import pygame
def init_second_background(screen):
    screen.fill('#14152c')


def init_background(screen):
    screen.fill(game.globals.BLACK)
    background_image = pygame.image.load("assets/background.png")
    # Calculate the new propotional hight
    new_hight = int((background_image.get_width() / game.globals.screen_width) * game.globals.screen_height)
    background_image = pygame.transform.scale(background_image, (game.globals.screen_width, new_hight))
    screen.blit(background_image, (0, 0))
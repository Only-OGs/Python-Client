import pygame
class Text:
    def __init__(self, screen, x, y, text, size, color):
        font = pygame.font.SysFont("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", size)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
        pygame.display.update()
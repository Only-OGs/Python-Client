import pygame
class Text:
    def __init__(self, screen, x, y, text, size, color, font):
        if font == None:
            sysfont = pygame.font.get_default_font()
            font = pygame.font.SysFont(None, size)
        else:
            sysfont = pygame.font.Font(font, size)

        img = font.render(text, True, color)
        rect = img.get_rect()
        pygame.draw.rect(img)
        screen.blit(img, (x, y))
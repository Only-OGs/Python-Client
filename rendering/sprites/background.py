import math

import pygame


class Background(pygame.sprite.Sprite):
    # läd das Bild als ein Screen und transformiert diesem damit der passt
    def __init__(self, x, img, pos, sc):
        super().__init__()
        self.image = img.convert_alpha()

        self.rect = self.image.get_rect()
        if pos == 0:
            self.rect.left = x
        elif pos == 1:
            self.rect.right = x
        self.image = pygame.transform.scale_by(self.image, sc)

    def move(self, x):
        source_x = int(math.floor(x * self.image.get_width()))
        source_w = min(self.image.get_width(), self.image.get_width()-source_x)
        self.rect.x = source_x

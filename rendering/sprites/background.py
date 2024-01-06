import pygame


class Background(pygame.sprite.DirtySprite):
    # läd das Bild als ein Screen und transformiert diesem damit der passt

    offset = 0.0

    def __init__(self, x, img):
        super().__init__()
        self.image = img.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.top = x
        self.image = pygame.transform.scale_by(self.image, 1.6)

    def mv_x(self, x):
        self.offset += x / 100
        if x == 0:
            self.offset = 0
        self.rect.x += self.offset

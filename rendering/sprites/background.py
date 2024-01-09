import math
import pygame


class Background(pygame.sprite.Sprite):
    # läd das Bild als ein Screen und transformiert diesem damit der passt
    def __init__(self, x, img):
        super().__init__()
        self.image = img.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x

    def move(self, rotation, screen: pygame.Surface):

        image_w = self.image.get_width()

        source_x = 0 + math.floor(self.image.get_width()*rotation)
        source_w = min(image_w, 0 + self.image.get_width() - source_x)

        dest_x = 0
        dest_y = 0
        dest_w = math.floor(1329 * (source_w/image_w))
        dest_h = 886

        screen.blit(self.image, (dest_x, dest_y), (1329-dest_w, 0, dest_w, dest_h))
        if source_w < image_w:
            screen.blit(self.image, (dest_w, dest_y), (0, 0, 1329-dest_w, dest_h))
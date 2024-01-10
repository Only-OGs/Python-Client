import math
import pygame
import globals_vars as global_var


class Background(pygame.sprite.Sprite):
    """Läd das übergebene Bild und positioniert es korrekt auf den Screen."""

    def __init__(self, img):
        super().__init__()
        self.image = img.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = 0

    def move(self, rotation, screen):
        """Bewegt den Hintergrund anhand des 'rotation' parameters, dieser wird auf dem screen gemalt"""
        image_w = self.image.get_width()

        source_x = 0 + math.floor(self.image.get_width() * rotation)
        source_w = min(image_w, 0 + self.image.get_width() - source_x)

        dest_x = 0
        dest_y = 0
        dest_w = math.floor(global_var.width * (source_w / image_w))
        dest_h = global_var.height

        screen.blit(self.image, (dest_x, dest_y), (global_var.width - dest_w, 0, dest_w, dest_h))
        if source_w < image_w:
            screen.blit(self.image, (dest_w, dest_y), (0, 0, global_var.width - dest_w, dest_h))

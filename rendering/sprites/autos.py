import pygame


class Autos(pygame.sprite.Sprite):

    def __init__(self, x, y, asset):
        super().__init__()

        self.image = pygame.image.load(asset).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def set_x(self, x):
        self.rect.x = x

    def set_y(self, y):
        self.rect.y = y

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def set_height(self, x):
        self.rect.height = x

    def set_width(self, y):
        self.rect.width = y

    def get_height(self):
        return self.rect.height

    def get_width(self):
        return self.rect.width

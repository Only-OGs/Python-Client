import random
import pygame


class Player(pygame.sprite.Sprite):
    # x = x position des Bildes y = y position des Bildes
    # läd ein bild und wandelt es zu einem pygame.Surface um
    start_x = 0
    start_y = 0
    uphill_offset = 18
    # var bounce = (1.5 * Math.random() * speedPercent * resolution) * Util.randomChoice([-1,1]);

    def __init__(self, x, y):
        super().__init__()
        # läd alle verschiedenen Assets
        self.right = pygame.image.load("assets/cars/player_right.png")
        self.left = pygame.image.load("assets/cars/player_left.png")
        self.straight = pygame.image.load("assets/cars/player_straight.png")
        self.right_uphill = pygame.image.load("assets/cars/player_uphill_right.png")
        self.left_uphill = pygame.image.load("assets/cars/player_uphill_left.png")
        self.straight_uphill = pygame.image.load("assets/cars/player_uphill_straight.png")

        self.image = self.straight.convert_alpha()

        # setzt die position so das es passt mit dem scaling
        self.rect = self.image.get_rect()
        self.start_x = x - self.rect.width-47
        self.start_y = y - self.rect.height-44
        self.rect.center = (self.start_x, self.start_y)

    # passendes Bild des autos wird geladen + skalierung des Bildes
    def drive_right(self, uphill):
        if uphill:
            self.image = self.right_uphill
            self.rect.center = (self.start_x, self.start_y-self.uphill_offset)
        else:
            self.image = self.right
            self.rect.center = (self.start_x, self.start_y)
        self._scale()

    # passendes Bild des autos wird geladen + skalierung des Bildes
    def drive_left(self, uphill):
        if uphill:
            self.image = self.left_uphill
            self.rect.center = (self.start_x, self.start_y-self.uphill_offset)
        else:
            self.image = self.left
            self.rect.center = (self.start_x, self.start_y)
        self._scale()

    # passendes Bild des autos wird geladen + skalierung des Bildes
    def drive_straight(self, uphill):
        if uphill:
            self.image = self.straight_uphill
            self.rect.center = (self.start_x, self.start_y-self.uphill_offset)
        else:
            self.image = self.straight
            self.rect.center = (self.start_x, self.start_y)
        self._scale()

    # skaliert das Bild größer da es sonst zu klein für die straße ist
    def _scale(self):
        self.image = pygame.transform.scale_by(self.image, 5)

    def bounce(self, bounce):
        self.rect.center = (self.rect.centerx, self.rect.centery-bounce)
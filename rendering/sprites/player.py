import random
import pygame


class Player(pygame.sprite.Sprite):
    """Läd alle Bilder und bewegt diese anhand der genutzen Methoden"""
    start_x = 0
    start_y = 0
    uphill_offset = 18

    def __init__(self, x, y):
        super().__init__()
        # läd alle Assets
        self.right = pygame.image.load("assets/cars/player_right.png")
        self.left = pygame.image.load("assets/cars/player_left.png")
        self.straight = pygame.image.load("assets/cars/player_straight.png")
        self.right_uphill = pygame.image.load("assets/cars/player_uphill_right.png")
        self.left_uphill = pygame.image.load("assets/cars/player_uphill_left.png")
        self.straight_uphill = pygame.image.load("assets/cars/player_uphill_straight.png")

        # Startbild ist das geradeaus fahrende Bild
        self.image = self.straight.convert_alpha()

        # offset der x und y Werte für die Skalierung
        self.rect = self.image.get_rect()
        self.start_x = x - self.rect.width-47
        self.start_y = y - self.rect.height-44
        self.rect.center = (self.start_x, self.start_y)

    def drive_right(self, uphill):
        """Passendes Bild des Autos wird geladen jenachdem ob der 'uphill' Parameter True oder False ist und das Bild
        wird passend skaliert """
        if uphill:
            self.image = self.right_uphill
            self.rect.center = (self.start_x, self.start_y-self.uphill_offset)
        else:
            self.image = self.right
            self.rect.center = (self.start_x, self.start_y)
        self._scale()

    def drive_left(self, uphill):
        """Passendes Bild des Autos wird geladen jenachdem ob der 'uphill' Parameter True oder False ist und das Bild
                wird passend skaliert """
        if uphill:
            self.image = self.left_uphill
            self.rect.center = (self.start_x, self.start_y-self.uphill_offset)
        else:
            self.image = self.left
            self.rect.center = (self.start_x, self.start_y)
        self._scale()


    def drive_straight(self, uphill):
        """Passendes Bild des Autos wird geladen jenachdem ob der 'uphill' Parameter True oder False ist und das Bild
        wird passend skaliert """
        if uphill:
            self.image = self.straight_uphill
            self.rect.center = (self.start_x, self.start_y-self.uphill_offset)
        else:
            self.image = self.straight
            self.rect.center = (self.start_x, self.start_y)
        self._scale()

    def _scale(self):
        """Skaliert das Bild größer da es sonst zu klein für die Straße ist"""
        self.image = pygame.transform.scale_by(self.image, 5)

    def bounce(self, bounce):
        self.rect.center = (self.rect.centerx, self.rect.centery-bounce)

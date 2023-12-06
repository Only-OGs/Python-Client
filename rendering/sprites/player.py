import pygame


class Player(pygame.sprite.Sprite):

    # x = x position des Bildes y = y position des Bildes
    # läd ein bild und wandelt es zu einem pygame.Surface um
    def __init__(self, x, y):
        super().__init__()
        # läd alle verschiedenen Assets
        self.right = pygame.image.load("assets/cars/player_right.png")
        self.left = pygame.image.load("assets/cars/player_left.png")
        self.straight = pygame.image.load("assets/cars/player_straight.png")

        self.image = self.straight.convert_alpha()

        # setzt die position so das es passt mit dem scaling
        # TODO: Ist evnt nicht ganz mittig, wer Zeit hat bitte nochmal anschauen
        self.rect = self.image.get_rect()
        self.rect.center = (x-self.rect.width, y-self.rect.height)

    # passendes Bild des autos wird geladen + skalierung des Bildes
    def drive_right(self):
        self.image = self.right
        self._scale()

    # passendes Bild des autos wird geladen + skalierung des Bildes
    def drive_left(self):
        self.image = self.left
        self._scale()

    # passendes Bild des autos wird geladen + skalierung des Bildes
    def drive_straight(self):
        self.image = self.straight
        self._scale()

    # skaliert das Bild größer da es sonst zu klein für die straße ist
    def _scale(self):
        self.image = pygame.transform.scale_by(self.image, 4)

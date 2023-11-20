import pygame


class Button:


    ''' Erstellt einen neuen Button, mit hover effekt.
    :param int x: X Kordinate
    :param int y: Y Kordinate
    :param str image: pfad zum default button
    :param int size: skalierungsfaktor
    :param str hover: pfad zum hover button
    '''
    def __init__(self, x, y, image, size, hover):
        skalierungsfaktor = size
        self.x = x
        self.y = y
        self.url = image
        pos = pygame.mouse.get_pos()
        #Button hintergrundbild
        self.button_image = pygame.image.load(self.url).convert_alpha()
        #Hover effect
        self.button_rect = self.button_image.get_rect()
        self.button_rect.center = (x,y)
        if self.button_rect.collidepoint(pos):
            self.button_image = pygame.image.load(hover).convert_alpha()
        #initiallisiere den neuen Ankerpunkt
        self.new_anker = (self.button_image.get_width() // 2, self.button_image.get_height())
        #neue größe des Bildes anpassen
        self.new_width = int(self.button_image.get_width() * skalierungsfaktor)
        self.new_hight = int(self.button_image.get_height() * skalierungsfaktor)
        self.button_image = pygame.transform.scale(self.button_image, (self.new_width, self.new_hight))
        #set the new ankerpoint
        self.rect = self.button_image.get_rect(center=self.new_anker)
        self.rect.center = (x, y)
        self.clicked = False

    ''' Erstellt den Text für einen Button.
        :param screen: default screen übergeben
        :param str text: beschriftung
        :param int size: größe des schrift
        :param color color: farbe
    '''

    def text(self, screen, text, size, color):
        font = pygame.font.SysFont(None, size)
        img = font.render(text, True, color)
        text_rect = img.get_rect()
        text_rect.center = (self.x, self.y)
        screen.blit(img, (self.x - 90, self.y - 15))

    ''' Erstellt die Funktionalität hinter dem button.
            :param screen: default screen übergeben
    '''
    def draw(self,screen):
        self.screen = screen
        action = False
        pos = pygame.mouse.get_pos()

        #check mous
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draw button on given @screen
        screen.blit(self.button_image, (self.rect.x, self.rect.y))
        return action
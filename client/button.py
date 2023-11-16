import pygame


class Button:

    def __init__(self, x, y, image, size, text, font_size):
        self.x, self.y = x, y
        skalierungsfaktor = size
        self.text = text
        self.image = image
        #new button background image
        self.button_image = pygame.image.load(self.image).convert_alpha()
        #new ankerpoint set
        self.new_anker = (self.button_image.get_width() // 2, self.button_image.get_height())
        #resizing the picture
        self.new_width = int(self.button_image.get_width() * skalierungsfaktor)
        self.new_hight = int(self.button_image.get_height() * skalierungsfaktor)
        self.button_image = pygame.transform.scale(self.button_image, (self.new_width, self.new_hight))
        #set the new ankerpoint
        self.rect = self.button_image.get_rect(center=self.new_anker)
        self.rect.center = (x, y)
        self.clicked = False

        font = pygame.font.Font('freesansbold.ttf', font_size)
        text_surface = font.render(self.text, True, ('black'))
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x, self.y)
        #self.screen.blit(text_surface, text_rect)




    def draw(self,screen,click_image):
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
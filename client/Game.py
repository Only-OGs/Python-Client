import pygame
from button import Button

pygame.init()
screen_width = 1280
screen_height = 720
fps = 60
timer = pygame.time.Clock
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("OG Racer")

class Game:
    run = True
    def game_loop(self):

        self.main_menu = True
        self.multiplay = False
        self.singleplayer = False
        self.options = False


        while self.run:
            #timer.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if self.main_menu:
                    self.draw_menu()
                elif self.multiplay:
                    pass
                elif self.singleplayer:
                    self.draw_singleplayer()
                elif self.options:
                    pass
                pygame.display.update()

    def draw_menu(self):
        self.background_image = pygame.image.load("../images/background.png")
        # Calculate the new propotional hight
        self.new_hight = int((self.background_image.get_width() / screen_width) * screen_height)
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, self.new_hight))
        screen.blit(self.background_image, (0, 0))

        # right
        self.button_multi = Button(x=screen_width / 2 + screen_width / 3, y=screen_height / 2,
                                   image='../images/button.png', size=2, text="singleplayer", font_size= 14)
        self.multi = self.button_multi.draw(screen, '../images/button-pressed.9.png')
        if self.multi:
            self.main_menu = False
            self.singleplayer = False
            self.multiplay = True
            self.options = False

        # middel
        self.button_options = Button(x=screen_width / 2, y=screen_height / 2 + 50,
                                     image='../images/button.png', size=2, text="singleplayer", font_size= 14)
        self.b_options = self.button_options.draw(screen, '../images/button-pressed.9.png')
        if self.b_options:
            self.main_menu = False
            self.singleplayer = False
            self.multiplay = False
            self.options = True

        # left
        self.button_start = Button(x=screen_width / 2 - screen_width / 3, y=screen_height / 2,
                                   image='../images/button.png', size=2, text="singleplayer", font_size= 14)
        self.start = self.button_start.draw(screen, '../images/button-pressed.9.png')
        if self.start:
            print("pressed")
            self.main_menu = False
            self.singleplayer = True
            self.multiplay = False
            self.options = False






    def draw_singleplayer(self):
        pygame.draw.rect(screen, (0,0,0,), [100,100,100,100])

    def draw_multiplay(self):
        pass

    def draw_options_(self):
        pass

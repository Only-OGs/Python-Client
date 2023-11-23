import pygame
from client.button import Button
from menu.lobbymenu import LobbyMenu
from game.globals import screen_width
from game.globals import screen_height
from rendering.game import Game


class MainMenu:

    def __init__(self):
        self.timer = pygame.time.Clock
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        pygame.display.set_caption("OG Racer")
        pygame.init()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

    run = True

    # game loop, das spiel läuft solange run = True
    def game_loop(self):

        self.main_menu = True
        self.multiplay = False
        self.singleplayer = False
        self.options = False


        while self.run:

            #Gibt die fenster aus
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if self.main_menu:
                    self.draw_menu()
                elif self.multiplay:
                    self.draw_multiplay()
                elif self.singleplayer:
                    self.draw_singleplayer()
                elif self.options:
                    self.draw_options_()

                pygame.display.update()

    #Initialisierung des Main Menu
    def draw_menu(self):

        #Deafault werte für die Buttons
        font_size = 20

        left_buttonx = screen_width / 2 - screen_width / 3
        left_buttony = screen_height / 2

        middle_buttonx = screen_width / 2
        middle_buttony = screen_height / 2 + 50

        right_buttonx = screen_width / 2 + screen_width / 3
        right_buttony = screen_height / 2

        button_image = 'assets/button.png'
        button_image_hover = 'assets/button-pressed.png'
        button_size = 2

        #Hintergundbild erstellen und ausgeben
        self.background_image = pygame.image.load("assets/background.png")
        # Calculate the new propotional hight
        self.new_hight = int((self.background_image.get_width() / screen_width) * screen_height)
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, self.new_hight))
        self.screen.blit(self.background_image, (0, 0))

        # Multiplayer button
        self.button_multi = Button(x=right_buttonx, y=right_buttony, image=button_image, size=button_size, hover=button_image_hover)
        self.multi = self.button_multi.draw(self.screen)
        self.button_multi.text(screen=self.screen, text="Multiplayer", size=font_size, color=self.WHITE)
        #übergibt dem Gameloop welches Fensster offen ist
        if self.multi:
            print("pressed")
            self.main_menu = False
            self.singleplayer = False
            self.multiplay = True
            self.options = False

        # Options button
        self.button_options = Button(x=middle_buttonx, y=middle_buttony, image=button_image, size=button_size, hover= button_image_hover)
        self.b_options = self.button_options.draw(self.screen)
        self.button_options.text(screen=self.screen, text="Options", size=font_size, color=self.WHITE)
        if self.b_options:
            print("pressed")
            self.main_menu = False
            self.singleplayer = False
            self.multiplay = False
            self.options = True

        # Singleplayer button
        self.button_start = Button(x=left_buttonx, y=left_buttony, image=button_image, size=button_size, hover= button_image_hover)
        self.start = self.button_start.draw(self.screen)
        self.button_start.text(screen=self.screen, text="Singleplayer" , size= font_size, color=self.WHITE)
        if self.start:
            print("pressed")
            self.main_menu = False
            self.singleplayer = True
            self.multiplay = False
            self.options = False


    #Initialisierung des Singleplayers
    def draw_singleplayer(self):
        Game()

    # Initialisierung des Multiplayers
    def draw_multiplay(self):
         LobbyMenu(self.screen)

    # Initialisierung der Einstellungen/Options
    def draw_options_(self):
        pass

    def back_to_menu(self):
        pass

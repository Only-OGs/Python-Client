import pygame
import pygame_gui
from client.button import Button
from menu.lobbymenu import LobbyMenu
from game.globals import screen_width
from game.globals import screen_height
from game.globals import WHITE
from game.globals import BLACK
from rendering.game import Game

pygame.init()

left_buttonx = screen_width / 2 - screen_width / 3
left_buttony = screen_height / 2

middle_buttonx = screen_width / 2
middle_buttony = screen_height / 2 + 50

right_buttonx = screen_width / 2 + screen_width / 3
right_buttony = screen_height / 2

button_image = 'assets/button.png'
button_image_hover = 'assets/button-pressed.png'
button_size = 2
font_size = 20


#event manager
manager_register = pygame_gui.UIManager((screen_width, screen_height))
clock = pygame.time.Clock()




class MainMenu:

    def __init__(self):
        self.timer = pygame.time.Clock
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        pygame.display.set_caption("OG Racer")
        pygame.init()




    run = True

    # game loop, das spiel läuft solange run = True
    def game_loop(self):

        self.main_menu = True
        self.singleplayer = False
        self.multiplay = False
        self.options = False
        self.register = False
        self.login = False
        self.lobby = False


        while self.run:
            refresh = clock.tick(60) / 1000.0
            #Gibt die fenster aus
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    manager_register.process_events(event)

                manager_register.update(refresh)

                if self.main_menu:
                    self.draw_menu()
                elif self.multiplay:
                    self.draw_multiplay()
                elif self.singleplayer:
                    self.draw_singleplayer()
                elif self.options:
                    self.draw_options()
                elif self.register:
                    self.draw_register()
                elif self.login:
                    self.draw_login()
                elif self.lobby():
                    self.draw_login()
                pygame.display.update()

    #Initialisierung des Main Menu
    def draw_menu(self):

        # Input felder init
        pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((800, 350), (360, 60)), manager=manager_register, object_id="#name"
            )

        pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((800, 450), (360, 60)), manager=manager_register, object_id="#passwort"
            )


        self.init_background()
        # Multiplayer button
        self.button_multi = Button(x=right_buttonx, y=right_buttony, image=button_image, size=button_size, hover=button_image_hover)
        self.multi = self.button_multi.draw(self.screen)
        self.button_multi.text(screen=self.screen, text="Multiplayer", size=font_size, color=WHITE)
        #übergibt dem Gameloop welches Fensster offen ist
        if self.multi:
            print("pressed")
            self.main_menu = False
            self.singleplayer = False
            self.multiplay = True
            self.options = False
            self.register = False
            self.login = False
            self.lobby = False

        # Options button
        self.button_options = Button(x=middle_buttonx, y=middle_buttony, image=button_image, size=button_size, hover= button_image_hover)
        self.b_options = self.button_options.draw(self.screen)
        self.button_options.text(screen=self.screen, text="Options", size=font_size, color=WHITE)
        if self.b_options:
            self.main_menu = False
            self.singleplayer = False
            self.multiplay = False
            self.options = True
            self.register = False
            self.login = False
            self.lobby = False

        # Singleplayer button
        self.button_start = Button(x=left_buttonx, y=left_buttony, image=button_image, size=button_size, hover= button_image_hover)
        self.start = self.button_start.draw(self.screen)
        self.button_start.text(screen=self.screen, text="Singleplayer" , size= font_size, color=WHITE)
        if self.start:
            self.main_menu = False
            self.singleplayer = True
            self.multiplay = False
            self.options = False
            self.register = False
            self.login = False
            self.lobby = False

    #Initialisierung des Singleplayers
    def draw_singleplayer(self):
        Game()

    # Initialisierung des Multiplayers
    def draw_lobby(self):
         LobbyMenu(self.screen)

    def draw_multiplay(self):
        self.init_background()
        self.back_to_meun()

        #Register button
        self.button_register = Button(x=right_buttonx, y=right_buttony, image=button_image, size=button_size,
                                      hover=button_image_hover)
        self.register = self.button_register.draw(self.screen)
        self.button_register.text(screen=self.screen, text="Registrieren", size=font_size, color=WHITE)
        if self.register:
            self.main_menu = False
            self.singleplayer = False
            self.multiplay = False
            self.options = False
            self.register = True
            self.login = False
            self.lobby = False

        # login button
        self.button_login = Button(x=middle_buttonx, y=middle_buttony, image=button_image, size=button_size,
                                   hover=button_image_hover)
        self.login = self.button_login.draw(self.screen)
        self.button_login.text(screen=self.screen, text="Login", size=font_size, color=WHITE)
        if self.login:
            self.main_menu = False
            self.singleplayer = False
            self.multiplay = False
            self.options = False
            self.register = False
            self.login = True
            self.lobby = False

    def draw_register(self):
        self.init_background()
        self.back_to_meun()
        manager_register.draw_ui(self.screen)


    def draw_login(self):
        self.init_background()
        self.back_to_meun()
        manager_register.draw_ui(self.screen)

    # Initialisierung der Einstellungen/Options
    def draw_options(self):
        self.init_background()
        self.back_to_meun()

    def init_background(self):
        self.screen.fill(BLACK)
        self.background_image = pygame.image.load("assets/background.png")
        # Calculate the new propotional hight
        self.new_hight = int((self.background_image.get_width() / screen_width) * screen_height)
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, self.new_hight))
        self.screen.blit(self.background_image, (0, 0))

    def back_to_meun(self):
        # back to menu button
        self.button_back = Button(x=left_buttonx, y=left_buttony, image=button_image, size=button_size,
                                   hover=button_image_hover)
        self.back = self.button_back.draw(self.screen)
        self.button_back.text(screen=self.screen, text="Menu", size=font_size, color=WHITE)
        if self.back:
            self.main_menu = True
            self.singleplayer = False
            self.multiplay = False
            self.options = False
            self.register = False
            self.login = False
            self.lobby = False
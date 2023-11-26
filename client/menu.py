import sys

import pygame
import pygame_gui
import time

from pygame.font import Font

import game.globals
from pygame import mixer_music
from communication.client import SocketIOClient
from client.button import Button
from rendering.game import Game
from client.draw_text import Text

pygame.init()
pygame.font.init()

#SocketIOClient
client = SocketIOClient()

left_buttonx = game.globals.screen_width / 2 - game.globals.screen_width / 3
left_buttony = game.globals.screen_height / 2

middle_buttonx = game.globals.screen_width / 2
middle_buttony = game.globals.screen_height / 2 + 50

right_buttonx = game.globals.screen_width / 2 + game.globals.screen_width / 3
right_buttony = game.globals.screen_height / 2

button_image = 'assets/button.png'
button_image_hover = 'assets/button-pressed.png'
button_size = 2
font_size = 20
screen_width = 1329
screen_height = 886

#init Music
main_music = pygame.mixer.music.load(filename="assets/Music/StartMenuMusic.mp3")
pygame.mixer.music.play(loops=2,fade_ms=40,start=0)
pygame.mixer.music.set_volume(0.01)

#event manager
clock = pygame.time.Clock()

#Register input Fenster
manager_register = pygame_gui.UIManager((game.globals.screen_width, game.globals.screen_height))
register_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 350), (360, 60)),
                                           manager=manager_register, object_id="#name", placeholder_text="Name")

register_passwort = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 450), (360, 60)),
                                               manager=manager_register, object_id="#passwort",
                                               placeholder_text="Passwort", visible=str)

#Login input Fenster
manager_Login = pygame_gui.UIManager((game.globals.screen_width, game.globals.screen_height))
login_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 350), (360, 60)),
                                                 manager=manager_Login, object_id="#name", placeholder_text="Name")

login_passwort = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 450), (360, 60)),
                                                     manager=manager_Login, object_id="#passwort",
                                                     placeholder_text="Passwort", visible=str)
#Option felder
manager_option = pygame_gui.UIManager((game.globals.screen_width, game.globals.screen_height))
#Music
music_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((game.globals.screen_width//2 - (game.globals.slider_width//2), game.globals.screen_height - 100),
                                                     (game.globals.slider_width, game.globals.slider_height)),start_value=0.01, value_range=((0.00) ,(0.10)), manager=manager_option
                                                      )



class MainMenu:

    def __init__(self):
        self.timer = pygame.time.Clock
        self.screen = pygame.display.set_mode([game.globals.screen_width, game.globals.screen_height])
        pygame.display.set_caption("OG Racer")


    #game loop, das spiel läuft solange run = True
    run = True
    def game_loop(self):

        self.current_window = "main_menu"

        while self.run:
            refresh = clock.tick(60) / 1000.0

            # Gibt die fenster aus
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.run = False

                # Manager_process
                manager_Login.process_events(event)
                manager_register.process_events(event)
                manager_option.process_events(event)

            # Manager_update
            manager_Login.update(refresh)
            manager_register.update(refresh)
            manager_option.update(refresh)

            if self.current_window == "main_menu":
                self.draw_menu()
            elif self.current_window =="multiplayer":
                self.draw_multiplay()
            elif self.current_window =="singleplayer":
                self.draw_singleplayer()
            elif self.current_window =="options":
                self.draw_options()
            elif self.current_window =="register":
                self.draw_register()
            elif self.current_window =="login":
                self.draw_login()
            elif self.current_window =="lobby":
                self.draw_lobby_menu()
            pygame.display.update()


    def check_data(self, name, passwort):
        if(self.login):
            client.send_login_data(user=name, password=passwort)
        if(self.register):
            client.send_register_data(user=name, password=passwort)

    #Initialisierung des Main Menu
    def draw_menu(self):

        # Input felder init
        self.init_background()
        # Multiplayer button
        self.button_multi = Button(x=right_buttonx, y=right_buttony, image=button_image, size=button_size, hover=button_image_hover)
        self.multi = self.button_multi.draw(self.screen)
        self.button_multi.text(screen=self.screen, text="Multiplayer", size=font_size, color=game.globals.WHITE)
        #übergibt dem Gameloop welches Fensster offen ist
        if self.multi:
            client.connect()
            self.update_window("multiplayer")

        # Options button
        self.button_options = Button(x=middle_buttonx, y=middle_buttony, image=button_image, size=button_size, hover= button_image_hover)
        self.b_options = self.button_options.draw(self.screen)
        self.button_options.text(screen=self.screen, text="Options", size=font_size, color=game.globals.WHITE)
        if self.b_options:
            self.update_window("options")
        # Singleplayer button
        self.button_start = Button(x=left_buttonx, y=left_buttony, image=button_image, size=button_size, hover= button_image_hover)
        self.start = self.button_start.draw(self.screen)
        self.button_start.text(screen=self.screen, text="Singleplayer" , size= font_size, color=game.globals.WHITE)
        if self.start:
            self.update_window("singleplayer")

    #Initialisierung des Singleplayers
    def draw_singleplayer(self):
        Game()

    def draw_multiplay(self):
        self.init_background()
        self.back_to_menu()

        #Register button
        self.button_register = Button(x=right_buttonx, y=right_buttony, image=button_image, size=button_size,
                                      hover=button_image_hover)
        self.register = self.button_register.draw(self.screen)
        self.button_register.text(screen=self.screen, text="Registrieren", size=font_size, color=game.globals.WHITE)
        if self.register:
            self.update_window("register")

        # login button
        self.button_login = Button(x=middle_buttonx, y=middle_buttony, image=button_image, size=button_size,
                                   hover=button_image_hover)
        self.login = self.button_login.draw(self.screen)
        self.button_login.text(screen=self.screen, text="Login", size=font_size, color=game.globals.WHITE)
        if self.login:
            self.update_window("login")

    def draw_register(self):
        self.init_background()
        self.back_to_menu()
        self.register_button()
        manager_register.draw_ui(self.screen)


    def draw_login(self):
        self.init_background()
        self.back_to_menu()
        self.log_in()
        manager_Login.draw_ui(self.screen)

    def register_button(self):
        log_in_button = Button(screen_width -400, (screen_height // 2 + 150),
                               button_image, button_size, button_image_hover)
        isLog_in_Clicked = log_in_button.draw(self.screen)
        log_in_button.text(self.screen, "Registrieren", 18, (255, 255, 255))
        if isLog_in_Clicked:
            self.check_data(register_name.get_text(), register_passwort.get_text())

    def log_in(self):
            log_in_button = Button(screen_width - 400, (screen_height // 2 +150),
                                    button_image, button_size, button_image_hover)
            isLog_in_Clicked = log_in_button.draw(self.screen)

            if isLog_in_Clicked:
                self.update_window("lobby")
                self.check_data(login_name.get_text(), login_passwort.get_text())


    # Initialisierung der Einstellungen/Options
    def draw_options(self):
        self.init_background()
        self.back_to_menu()

        #music Slider
        pygame.mixer.music.set_volume(music_slider.current_value)
        manager_option.draw_ui(self.screen)

    def init_second_background(self):
        self.screen.fill('#14152c')

    def init_background(self):
        self.screen.fill(game.globals.BLACK)
        self.background_image = pygame.image.load("assets/background.png")
        # Calculate the new propotional hight
        self.new_hight = int((self.background_image.get_width() / game.globals.screen_width) * game.globals.screen_height)
        self.background_image = pygame.transform.scale(self.background_image, (game.globals.screen_width, self.new_hight))
        self.screen.blit(self.background_image, (0, 0))

    def back_to_menu(self):
        self.init_background()
        self.button_back = Button(x=left_buttonx, y=left_buttony, image=button_image, size=button_size,
                                   hover=button_image_hover)
        self.back = self.button_back.draw(self.screen)
        self.button_back.text(screen=self.screen, text="Menu", size=font_size, color=game.globals.WHITE)
        if self.back:
            client.disconnect()
            self.update_window("main_menu")

    def draw_lobby_menu(self):

        text = "Lobbyauswahl"
        loginsuccesstext = client.Loginsuccessful
        self.init_second_background()
        text_font = Font("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 45)
        img = text_font.render(text, True, "#FF06C1")
        loginsuccessimg = text_font.render(loginsuccesstext, True,"#FF06C1")

        # Berechne die vergangene Zeit
       # elapsed_time = pygame.time.get_ticks() - start_time
        # Überprüfe, ob die 3 Sekunden vergangen sind
       # if elapsed_time < 3000:
           # self.screen.blit(loginsuccessimg, (10, screen_height - loginsuccessimg.get_height() - 10))

       # self.screen.blit(img, (screen_width // 2 - (screen_width // 6), screen_height // 4 - 80))

        button_image = 'assets/button.png'
        button_image_hover = 'assets/button-pressed.png'
        button_spacing = 30
        button_size = 2

        lobby_create_button = Button(screen_width // 2, screen_height // 2 - (2 * button_spacing),
                                     button_image, button_size, button_image_hover)

        quick_game_button = Button(screen_width // 2, screen_height // 2 + button_spacing,
                                   button_image, button_size, button_image_hover)

        search_lobby_button = Button(screen_width // 2, (screen_height // 2 + (4 * button_spacing)),
                                     button_image, button_size, button_image_hover)

        log_out_button = Button(screen_width // 2, (screen_height // 2 + (7 * button_spacing)),
                                button_image, button_size, button_image_hover)

        isLobbyCreateClicked = lobby_create_button.draw(self.screen)
        lobby_create_button.text(self.screen, "Lobby erstellen", 18, (255, 255, 255))

        isQuickGameClicked = quick_game_button.draw(self.screen)
        quick_game_button.text(self.screen, "Schnelles Spiel", 18, (255, 255, 255))

        isSeachLobbyClicked = search_lobby_button.draw(self.screen)
        search_lobby_button.text(self.screen, "Lobby suchen", 18, (255, 255, 255))

        isLogoutClicked = log_out_button.draw(self.screen)
        log_out_button.text(self.screen, "Abmelden", 18, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if isLogoutClicked:
                self.back_to_menu()
            if isLobbyCreateClicked:
                pass
            if isQuickGameClicked:
                pass
            if isSeachLobbyClicked:
                pass
    def update_window(self, new_window):
        self.current_window = new_window

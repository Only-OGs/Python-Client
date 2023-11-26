import pygame
import pygame_gui
import game.globals
from globals import gui_globals
from globals import background_global
from globals import button_globals
from pygame.font import Font
from communication.client import SocketIOClient
from client.button import Button
from rendering.game import Game

pygame.init()
pygame.font.init()

#SocketIOClient
client = SocketIOClient()

screen_width = 1329
screen_height = 886

#event manager
clock = pygame.time.Clock()


# Player in Lobby List
id_playerList = []
# counter für "Suchen..."
global search_counter
search_counter = 0
player_texts = [pygame.font.SysFont("Arial", 20).render(player, True, (255, 255, 255)) for player in id_playerList]
player_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0)]


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
                gui_globals.manager_Login.process_events(event)
                gui_globals.manager_register.process_events(event)
                gui_globals.manager_option.process_events(event)

            # Manager_update
            gui_globals.manager_Login.update(refresh)
            gui_globals.manager_register.update(refresh)
            gui_globals.manager_option.update(refresh)

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
        if self.login:
            client.send_login_data(user=name, password=passwort)
        if self.register:
            client.send_register_data(user=name, password=passwort)

    #Initialisierung des Main Menu
    def draw_menu(self):
        # Input felder init
        background_global.init_background(self.screen)
        # Multiplayer button

        #übergibt dem Gameloop welches Fensster offen ist
        multi = button_globals.rechter_button(screen=self.screen,text="Multiplayer")
        if multi:
            client.connect()
            self.update_window("multiplayer")

        # Options button
        b_options = button_globals.mittlerer_button(screen=self.screen, text="Options")
        if b_options:
            self.update_window("options")

        # Singleplayer button
        start = button_globals.linker_button(screen=self.screen,text="Singleplayer")
        if start:
            self.update_window("singleplayer")

    #Initialisierung des Singleplayers
    def draw_singleplayer(self):
        Game()

    def draw_multiplay(self):
        background_global.init_background(self.screen)
        self.back_to_menu()

        #Register button
        register = button_globals.rechter_button(screen=self.screen, text="Register")
        if register:
            self.update_window("register")

        # login button
        login = button_globals.mittlerer_button(screen=self.screen, text="Anmelden")
        if login:
            self.update_window("login")

    def draw_register(self):
        background_global.init_background(self.screen)
        self.back_to_menu()
        self.register_button()
        gui_globals.manager_register.draw_ui(self.screen)


    def draw_login(self):
        background_global.init_background(self.screen)
        self.back_to_menu()
        self.log_in()
        gui_globals.manager_Login.draw_ui(self.screen)

    def register_button(self):
        reg = button_globals.log_reg_button(screen=self.screen,text= "register")
        if reg:
            self.check_data(gui_globals.register_name.get_text(), gui_globals.register_passwort.get_text())

    def log_in(self):
            log = button_globals.log_reg_button(screen=self.screen,text= "register")
            if log:
                self.check_data(gui_globals.login_name.get_text(), gui_globals.login_passwort.get_text())
                self.update_window("lobby")


    # Initialisierung der Einstellungen/Options
    def draw_options(self):
        background_global.init_background(self.screen)
        self.back_to_menu()

        #music Slider
        pygame.mixer.music.set_volume(gui_globals.music_slider.current_value)
        gui_globals.manager_option.draw_ui(self.screen)

    def back_to_menu(self):
        background_global.init_background(self.screen)
        back = button_globals.linker_button(screen=self.screen, text="menu")
        if back:
            client.disconnect()
            self.update_window("main_menu")

    def draw_lobby_menu(self):

        text = "Lobbyauswahl"
        loginstatus = client.loginstatus
        background_global.init_background(self.screen)
        text_font = Font("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 45)
        img = text_font.render(text, True, "#FF06C1")
        if loginstatus != None:
            text_font = Font("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 20)
            loginstatusimg = text_font.render(loginstatus, True, "White")
            self.screen.blit(loginstatusimg, (100, game.globals.screen_height - loginstatusimg.get_height() - 50))




        self.screen.blit(img, (screen_width // 2 - (screen_width // 6), screen_height // 4 - 80))

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
        if isLogoutClicked:
            self.back_to_menu()
        if isLobbyCreateClicked:
            pass
        if isQuickGameClicked:
            pass
        if isSeachLobbyClicked:
            pass

    def InLobby(self):
        background_global.init_background(self.screen)
        pygame.draw.rect(self.screen, (255, 255, 255), (100, screen_height // 16, 400, 40), 0)
        for i, (text, color) in enumerate(zip(player_texts, player_colors)):
            pygame.draw.rect(self.screen, color, (100, (screen_height // 16) + (80 * i), 400, 40), 0)
            self.screen.blit(text, (110, (screen_height // 16) + (80 * i) + 10))

        global search_counter
        search_counter+=1

        if search_counter == 60:
            player_texts.extend([pygame.font.SysFont("Arial", 20).render("Suchen .", True, (255, 255, 255))] * (
                        len(player_texts) - len(id_playerList)))
        elif search_counter == 120:
            player_texts.extend([pygame.font.SysFont("Arial", 20).render("Suchen ..", True, (255, 255, 255))] * (
                        len(player_texts) - len(id_playerList)))
        elif search_counter == 180:
            player_texts.extend([pygame.font.SysFont("Arial", 20).render("Suchen ...", True, (255, 255, 255))] * (
                    len(player_texts) - len(id_playerList)))
            search_counter = 0

        pygame.display.flip()
        self.timer.tick(60)

    def update_window(self, new_window):
        self.current_window = new_window


from rendering.layout import Layout
import rendering.globals_vars as var
import pygame
import pygame_gui
import time
import pygame.mixer


import time

pygame.mixer.init()
soundtrack = pygame.mixer.Sound("assets/Music/robotic-countdown-43935.mp3")
soundtrack.set_volume(0.03)

class Screens:

    @staticmethod
    def create_menu_screen(screen):
        var.client.disconnect()
        Layout.init_background(screen=screen)
        Layout.linker_button(screen=screen, text="Einzelspieler", trigger="Einzelspieler")
        Layout.mittlerer_button(screen=screen, text="Optionen", trigger="Optionen")
        Layout.rechter_button(screen=screen, text="Mehrspieler", trigger="Mehrspieler")

    @staticmethod
    def create_mulitplayer_screen():
        if not var.client.sio.connected:
            var.client.connect()
        else:
            pass
        var.singleplayer_start = True
        Layout.init_background(screen=var.menu_screen)
        Layout.create_Serverstatus_gui()
        Layout.linker_button(screen=var.menu_screen, text="Anmelden", trigger="Jetzt Anmelden")
        Layout.mittlerer_button(screen=var.menu_screen, text="Zurueck", trigger="Zurueck")
        Layout.rechter_button(screen=var.menu_screen, text="Registrieren", trigger="Jetzt Registrieren")

    @staticmethod
    def create_option_screen():
        Layout.init_background(screen=var.menu_screen)
        Layout.linker_button(screen=var.menu_screen, text="Zurueck", trigger="Zurueck")
        Layout.draw_text(screen=var.menu_screen, x=var.slider_width // 2 , y=var.height - 150,
                         text="Musik Lautstaerke", size=31, color=var.WHITE)
        pygame.mixer.music.set_volume(var.music_slider.current_value)
        var.manager_option.draw_ui(var.menu_screen)

    @staticmethod
    def create_ingame_Lobby():
        Layout.create_ingamelobby(screen=var.menu_screen)

    @staticmethod
    def create_lobby_screen():
        Layout.init_background(screen=var.menu_screen)
        Layout.create_Serverstatus_gui()
        Layout.draw_text(screen=var.menu_screen, x=var.width // 2, y=60, text="Lobbyauswahl", size=45,
                         color=(255, 6, 193))
        Layout.create_loginstatus_gui()
        Layout.create_lobbystatus_gui()
        Layout.search_lobby_button(screen=var.menu_screen, text="Lobby suchen")
        Layout.lobby_create_button(screen=var.menu_screen, text="Lobby erstellen")
        Layout.quick_game_button(screen=var.menu_screen, text="Schnelles Spiel")
        Layout.log_out_button(screen=var.menu_screen, text="Abmelden")

    @staticmethod
    def create_lobby_search():
        Layout.init_second_background(screen=var.menu_screen)
        Layout.draw_text(screen=var.menu_screen, x=var.width // 2, y=60, text="Lobby suchen", size=35,
                         color=(255, 6, 193))
        Layout.mittlerer_button(screen=var.menu_screen, text="Suchen", trigger="Suchen")
        Layout.rechter_button(screen=var.menu_screen, text="Zurueck", trigger="Zurueck")
        Layout.create_lobbystatus_gui()
        var.manager_lobby_search.draw_ui(var.menu_screen)

    @staticmethod
    def create_log_screen():
        Layout.init_background(screen=var.menu_screen)
        Layout.create_Serverstatus_gui()
        Layout.linker_button(screen=var.menu_screen, text="Zurueck", trigger="Mehrspieler")
        Layout.log_reg_button(screen=var.menu_screen, text="Anmelden")
        var.manager_Login.draw_ui(var.menu_screen)

    @staticmethod
    def create_registration_screen():
        Layout.init_background(screen=var.menu_screen)
        Layout.create_Serverstatus_gui()
        Layout.linker_button(screen=var.menu_screen, text="Zurueck", trigger="Mehrspieler")
        Layout.log_reg_button(screen=var.menu_screen, text="Registrieren")
        var.manager_register.draw_ui(var.menu_screen)

    @staticmethod
    def create_ingameLobby():
        Layout.init_second_background(screen=var.menu_screen)
        Layout.create_ingamelobby(screen=var.menu_screen)

    @staticmethod
    def screen_update():
        if var.menu_state == "main_menu":
            Screens.create_menu_screen(var.menu_screen)
        elif var.menu_state == "lobby_option":
            Screens.create_lobby_screen()
        elif var.menu_state == "registration_menu":
            Screens.create_registration_screen()
        elif var.menu_state == "log_menu":
            Screens.create_log_screen()
        elif var.menu_state == "option_menu":
            Screens.create_option_screen()
        elif var.menu_state == "multiplayer_menu":
            Screens.create_mulitplayer_screen()
        elif var.menu_state == "ingame_lobby":
            Screens.create_ingameLobby()
        elif var.menu_state == "search_for_lobby":
            Screens.create_lobby_search()
        elif var.menu_state == "loading":
            Screens.create_loadingscreen(screen=var.menu_screen)


    @staticmethod
    def init_music():
        pygame.mixer.music.load(filename="assets/Music/StartMenuMusic.mp3")
        pygame.mixer.music.play(loops=5, fade_ms=40, start=0)
        pygame.mixer.music.set_volume(0.01)

    @staticmethod
    def create_lobby_search_input():
        var.manager_lobby_search = pygame_gui.UIManager((var.width, var.height))
        var.lobby_search_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(((var.width - 360) // 2, (var.height - 120) // 2), (360, 60)),
            manager=var.manager_lobby_search, object_id="#search",
            placeholder_text="LobbyID")

    @staticmethod
    def create_loadingscreen(screen):
        screen.fill((var.VIOLETTE))
        Layout.draw_text(screen=screen, x=var.width // 2, y=100 // 2, text="Das Spiel startet gleich...", size=45,
                         color=var.DARKBLUE)
        var.menu_state = "Game"

    @staticmethod
    def create_pause_menu(screen):
        color = var.VIOLETTE
        Layout.exit_background(screen)
        if var.singleplayer:
            Layout.draw_text(screen=screen, x=var.width // 2, y=var.height // 2, text="P = Pause", size=25, color=color)

        Layout.draw_text(screen=screen, x=var.width // 2, y=var.height // 2 + 30, text="ESC = Hauptmenue", size=25,
                         color=color)

    @staticmethod
    def create_register_input():
        var.manager_register = pygame_gui.UIManager((var.width, var.height))
        var.register_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 350), (360, 60)),
                                                                manager=var.manager_register, object_id="#name",
                                                                placeholder_text="Name")

        var.register_password = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 450), (360, 60)),
                                                                    manager=var.manager_register, object_id="#passwort",
                                                                    placeholder_text="Passwort", visible=str)

    @staticmethod
    def create_login_input():
        var.manager_Login = pygame_gui.UIManager((var.width, var.height))
        var.login_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 350), (360, 60)),
                                                             manager=var.manager_Login, object_id="#name",
                                                             placeholder_text="Name")

        var.login_password = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((800, 450), (360, 60)),
                                                                 manager=var.manager_Login, object_id="#passwort",
                                                                 placeholder_text="Passwort", visible=str)

    @staticmethod
    def create_music_slider():
        var.manager_option = pygame_gui.UIManager((var.width, var.height))
        var.music_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((var.width // 2 - (
                    var.slider_width // 2), var.height - 100),
                                      (var.slider_width, var.slider_height)), start_value=0.01,
            value_range=((0.000), (0.05)), manager=var.manager_option
        )

    @staticmethod
    def create_ingmae_menu(screen):
        rect = pygame.rect.Rect(var.width // 2, var.height // 2, 600, 600)
        pygame.draw.rect(screen, var.DARKBLUE, rect)

    # Erstellt den Countdown zu beginn eines Spiels
        # Erstellt den Countdown zu beginn eines Spiels
    @staticmethod
    def create_countdown_multiplayer(screen):
        color = var.RED
        countdown = str(var.game_countdown_start)
        print(var.game_countdown_start)
        print("hier rein")
        if var.game_countdown_start == 3:
            print("Sound")
            soundtrack.play()

        elif var.game_start:
            print("start")
            countdown = "GO"
            color = var.VIOLETTE

        Layout.draw_text(screen=screen, x=var.width // 2, y=var.height // 2, text=countdown, size=90, color=color)

    @staticmethod
    def create_countdown_singleplayer(screen):
        if var.buttons["Einzelspieler"]:
            countdown = ""
            color = var.RED
            if var.game_counter <= int(var.clock.get_fps()):
                countdown = "5"
            elif var.game_counter <= int(var.clock.get_fps())*2:
                countdown = "4"
            elif var.game_counter <= int(var.clock.get_fps())*3:
                soundtrack.play()
                countdown = "3"
            elif var.game_counter <= int(var.clock.get_fps())*4:
                countdown = "2"
            elif var.game_counter <= int(var.clock.get_fps())*5:
                countdown = "1"
            elif var.game_counter <= int(var.clock.get_fps())*6:
                countdown = "GO"
                color = var.VIOLETTE
                if int(var.clock.get_fps())*6 == 360 and var.buttons["Einzelspieler"]:
                    var.game_start = True
                    var.buttons["Einzelspieler"] = False
                    var.singleplayer_start = True
                    print(var.singleplayer_start)
                    var.game_counter = 0

            Layout.draw_text(screen=screen, x=var.width // 2, y=var.height // 2, text=countdown, size=90,
                             color=color)


    def threaded_function(arg, text):
        var.is_running = True
        for i in range(arg):
            time.sleep(1)
        if text == "login":
            var.client.loginmessage = ''
        elif text == "lobby":
            var.client.lobbymessage = ''
        elif text == "game":
            var.menu_state == "main_menu"
            var.isgame = True
        var.is_running = False

    @staticmethod
    def create_leaderboard():
        screen = var.screen

        rect = pygame.rect.Rect(50, 50, var.width - 100, var.height - 150)
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, var.TRANSPARENT_VIOLLETE, shape_surf.get_rect())
        screen.blit(shape_surf, rect)

        const = 100
        for row in var.leaderboard:
            rect = pygame.rect.Rect(90, 60+const, var.width - 170, 35)
            pygame.draw.rect(screen, var.CYAN, rect)
            Layout.draw_text(screen=screen, y=75+const, x=200, text=row.get("posi"), size=25, color=var.DARKBLUE)
            Layout.draw_text(screen=screen, y=75+const, x=200 + var.width // 3, text=row.get("name"), size=25, color=var.DARKBLUE)
            Layout.draw_text(screen=screen, y=75+const, x=200 + (var.width // 3 * 2), text=(row.get("time")), size=25,
                             color=var.DARKBLUE)
            const += 50

        Layout.draw_text(screen=screen, y=80, x=200, text="Position", size=32, color=var.DARKBLUE)
        Layout.draw_text(screen=screen, y=80, x=200 + var.width // 3, text="Name", size=32, color=var.DARKBLUE)
        Layout.draw_text(screen=screen, y=80, x=200 + (var.width // 3 * 2), text="Zeit", size=32, color=var.DARKBLUE)

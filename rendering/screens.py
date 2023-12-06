from rendering.layout import Layout
import rendering.globals_vars as var
import pygame
import pygame_gui


class Screens:

    @staticmethod
    def create_menu_screen():
        var.client.disconnect()
        Layout.init_background(screen=var.menu_screen)
        Layout.create_Serverstatus()
        Layout.linker_button(screen=var.menu_screen, text="Einzelspieler",trigger="Einzelspieler")
        Layout.mittlerer_button(screen=var.menu_screen, text="Optionen",trigger="Optionen")
        Layout.rechter_button(screen=var.menu_screen, text="Mehrspieler",trigger="Mehrspieler")

    @staticmethod
    def create_mulitplayer_screen():
        if not var.client.sio.connected:
            var.client.connect()
        Layout.init_background(screen=var.menu_screen)
        Layout.create_Serverstatus()
        Layout.linker_button(screen=var.menu_screen, text="Anmelden",trigger="Jetzt Anmelden")
        Layout.mittlerer_button(screen=var.menu_screen, text="Zurueck",trigger="Zurueck")
        Layout.rechter_button(screen=var.menu_screen, text="Registrieren",trigger="Jetzt Registrieren")

    @staticmethod
    def create_option_screen():
        Layout.init_background(screen=var.menu_screen)
        Layout.linker_button(screen=var.menu_screen, text="Zurueck",trigger="Zurueck")
        pygame.mixer.music.set_volume(var.music_slider.current_value)
        var.manager_option.draw_ui(var.menu_screen)

    @staticmethod
    def create_ingame_Lobby():
        Layout.init_second_background(screen=var.menu_screen)
        Layout.create_ingamelobby(screen=var.menu_screen)

    @staticmethod
    def create_lobby_screen():
        Layout.init_background(screen=var.menu_screen)
        Layout.create_Serverstatus()
        Layout.draw_text(screen=var.menu_screen, x=var.width / 2 - 160, y=60, text="Lobbyauswahl", size=45,
                         color=(255,6,193))
        if var.client.loginstatus != '':
            Layout.draw_text(screen=var.menu_screen, x=50, y=var.height - 50, text=var.client.loginstatus, size=20,
                             color=(255,6,193))
        Layout.search_lobby_button(screen=var.menu_screen, text="Lobby suchen")
        Layout.lobby_create_button(screen=var.menu_screen, text="Lobby erstellen")
        Layout.quick_game_button(screen=var.menu_screen, text="Schnelles Spiel")
        Layout.log_out_button(screen=var.menu_screen, text="Abmelden")

    @staticmethod
    def create_lobby_search():
        Layout.init_second_background(screen=var.menu_screen)
        Layout.draw_text(screen=var.menu_screen, x=var.width / 2 - 160, y=60, text="Lobby suchen", size=35,
                         color=(255, 6, 193))
        Layout.mittlerer_button(screen=var.menu_screen, text="Suchen",trigger="Suchen")
        var.manager_lobby_search.draw_ui(var.menu_screen)


    @staticmethod
    def create_log_screen():
        Layout.init_background(screen=var.menu_screen)
        Layout.create_Serverstatus()
        Layout.linker_button(screen=var.menu_screen, text="Zurueck",trigger="Mehrspieler")
        Layout.log_reg_button(screen=var.menu_screen, text="Anmelden")
        var.manager_Login.draw_ui(var.menu_screen)

    @staticmethod
    def create_registration_screen():
        Layout.init_background(screen=var.menu_screen)
        Layout.create_Serverstatus()
        Layout.linker_button(screen=var.menu_screen, text="Zurueck",trigger="Mehrspieler")
        Layout.log_reg_button(screen=var.menu_screen, text="Registrieren")
        var.manager_register.draw_ui(var.menu_screen)

    @staticmethod
    def create_ingameLobby():

        Layout.init_second_background(screen=var.menu_screen)
        Layout.create_ingamelobby(screen=var.menu_screen)
        # TODO Buttons! und Texte

    @staticmethod
    def screen_update():

        if var.menu_state == "main_menu":
            Screens.create_menu_screen()
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

    @staticmethod
    def init_music():
        pygame.mixer.music.load(filename="assets/Music/StartMenuMusic.mp3")
        pygame.mixer.music.play(loops=5, fade_ms=40, start=0)
        pygame.mixer.music.set_volume(0.01)


    @staticmethod
    def create_lobby_search_input():
        var.manager_lobby_search = pygame_gui.UIManager((var.width, var.height))
        var.lobby_search_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(((var.width-360)//2, (var.height-120)//2), (360, 60)),
                                                                manager=var.manager_lobby_search, object_id="#search",
                                                                placeholder_text="LobbyID")



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
            value_range=((0.00), (0.10)), manager=var.manager_option
        )


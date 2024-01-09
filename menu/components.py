import threading
from time import sleep
from menu.button import Button
import globals_vars as global_var
import menu.menu_vars as menu_var
import pygame


button_positions = {
    "linker": {"x": global_var.width / 2 - global_var.width / 3, "y": global_var.height / 2},
    "mittlerer": {"x": global_var.width / 2, "y": global_var.height / 2 + 50},
    "rechter": {"x": global_var.width / 2 + global_var.width / 3, "y": global_var.height / 2},
    "log_reg": {"x": global_var.width - 400, "y": global_var.height // 2 + 150}
}
button_image = 'assets/button.png'
button_image_hover = 'assets/button-pressed.png'
button_size = 2
font_size = 20


class Components:

    # GUI-Elemente erstellen:
    @staticmethod
    def init_second_background(screen):
        screen.fill('#14152c')

    @staticmethod
    def init_background(screen):
        screen.fill("BLACK")
        background_image = pygame.image.load("assets/background.png")
        new_height = int((background_image.get_width() / global_var.width) * global_var.height)
        background_image = pygame.transform.scale(background_image, (global_var.width, new_height))
        screen.blit(background_image, (0, 0))

    @staticmethod
    def exit_background(screen):
        background_image = pygame.image.load("assets/exitBackground.png")
        new_height = int((background_image.get_width() / global_var.width) * global_var.height)
        background_image = pygame.transform.scale(background_image, (global_var.width // 2, new_height // 2))
        background_rect = background_image.get_rect(center=(global_var.width // 2, global_var.height // 2))
        screen.blit(background_image, background_rect.topleft)

    # Text generieren und zentriert anzeigen lassen.
    @staticmethod
    def draw_text(screen, x, y, text, size, color):
        font = pygame.font.Font(menu_var.FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    # Text generieren und nicht generiert anzeigen lassen.
    @staticmethod
    def draw_text_not_Center(screen, x, y, text, size, color):
        font = pygame.font.Font(menu_var.FONT, size)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    # Verschiedene Buttons
    '''
    Allgemeine Funktion, welche einen Button und dessen Funktionalität definiert.
    definiert einen Button an definierten Stellen, Funktionalität kann über text und trigger definiert werden
    '''
    def __create_button(screen, x, y, text, trigger):
        button = Button(x=x, y=y, image=button_image, size=button_size, hover=button_image_hover)
        button.render(screen=screen, text=text, size=font_size, color="WHITE")
        clicked = button.check()
        menu_var.buttons[trigger] = clicked

    @staticmethod
    def linker_button(screen, text, trigger):
        return Components.__create_button(screen, **button_positions["linker"], text=text, trigger=trigger)

    @staticmethod
    def mittlerer_button(screen, text, trigger):
        return Components.__create_button(screen, **button_positions["mittlerer"], text=text, trigger=trigger)

    @staticmethod
    def rechter_button(screen, text, trigger):
        return Components.__create_button(screen, **button_positions["rechter"], text=text, trigger=trigger)

    @staticmethod
    def log_reg_button(screen, text):
        return Components.__create_button(screen, **button_positions["log_reg"], text=text, trigger=text)

    @staticmethod
    def lobby_create_button(screen, text):
        lobby_create_button = Button(global_var.width // 2, global_var.height // 2 + 20,
                                     button_image, 2, button_image_hover)

        clicked = lobby_create_button.check()
        lobby_create_button.render(screen=screen, text=text, size=18, color="WHITE")
        menu_var.buttons[text] = clicked


    @staticmethod
    def zureuck_button(screen, x, y):
        zurueck_button = Button(x, y,
                                button_image, 2, button_image_hover)

        clicked = zurueck_button.check()
        zurueck_button.render(screen=screen, text="Verlassen", size=18, color="WHITE")
        menu_var.buttons["Verlassen"] = clicked

    @staticmethod
    def abmelden_button(screen, x, y):
        abmelden_button = Button(x, y,
                                button_image, 2, button_image_hover)

        clicked = abmelden_button.check()
        abmelden_button.render(screen=screen, text="Abmelden", size=18, color="WHITE")
        menu_var.buttons["Abmelden"] = clicked

    @staticmethod
    def einstellungen_button(screen, x, y):
        einstellungen_button = Button(x, y,
                                 button_image, 2, button_image_hover)

        clicked = einstellungen_button.check()
        einstellungen_button.render(screen=screen, text="Optionen", size=18, color="WHITE")
        menu_var.buttons["Optionen"] = clicked

    @staticmethod
    def bereit(screen, x, y, text):
        einstellungen_button = Button(x, y,
                                      button_image, 2, button_image_hover)

        clicked = einstellungen_button.check()
        einstellungen_button.render(screen=screen, text=text, size=18, color="WHITE")
        menu_var.buttons[text] = clicked

    @staticmethod
    def send(screen, x, y, text):
        send_button = Button(x, y,button_image, 2, button_image_hover)

        clicked = send_button.check()
        send_button.render(screen=screen, text=text, size=18, color="WHITE")
        menu_var.buttons[text] = clicked

    @staticmethod
    def quick_game_button(screen, text):
        quick_game_button = Button(global_var.width // 2, global_var.height // 2 + (6 * 20),
                                   button_image, 2, button_image_hover)
        clicked = quick_game_button.check()
        quick_game_button.render(screen=screen, text=text, size=18, color="WHITE")
        menu_var.buttons[text] = clicked


    @staticmethod
    def search_lobby_button(screen, text):
        search_lobby_button = Button(global_var.width // 2, (global_var.height // 2 + (11 * 20)),
                                     button_image, 2, button_image_hover)
        clicked = search_lobby_button.check()
        search_lobby_button.render(screen=screen, text=text, size=font_size, color="WHITE")
        menu_var.buttons[text] = clicked


    @staticmethod
    def log_out_button(screen, text):
        log_out_button = Button(global_var.width // 2, (global_var.height // 2 + (16 * 20)),
                                button_image, 2, button_image_hover)
        clicked = log_out_button.check()
        log_out_button.render(screen=screen, text=text, size=font_size, color="WHITE")
        menu_var.buttons[text] = clicked

    # Status - GUI erstellen:
    '''
    Zeigt die verschiedenen vom Server für den User an 
    '''
    @staticmethod
    def create_Serverstatus_gui():
        if global_var.client.sio.connected:
            Components.draw_text(screen=global_var.menu_screen, x=100, y=130, text="ONLINE", size=20, color="GREEN")
        else:
            Components.draw_text(screen=global_var.menu_screen, x=100, y=130, text="OFFLINE", size=20, color="RED")
        Components.draw_text(screen=global_var.menu_screen, x=100, y=100, text="Server:", size=17, color="WHITE")



    @staticmethod
    def create_loginstatus_gui(text):
        if text == "login":
            text = global_var.client.loginmessage
        else:
            text = global_var.client.errormessage
        if text != '':
            Components.draw_text(screen=global_var.menu_screen, x=global_var.width // 2, y=global_var.height - 50, text=text,
                                 size=20,
                                 color=(255, 6, 193))
            if not menu_var.is_running:
                thread = threading.Thread(target=Components.start_timer_in_thread, args=(3, "login"))
                thread.start()
    @staticmethod
    def create_registerstatus_gui(text):
        if text == "register":
            text = global_var.client.registerstatus
        else:
            text = global_var.client.errormessage
        if text != '':
            Components.draw_text(screen=global_var.menu_screen, x=global_var.width // 2, y=global_var.height - 50, text=text,
                                 size=20,
                                 color=(255, 6, 193))
            if not menu_var.is_running:
                thread = threading.Thread(target=Components.start_timer_in_thread, args=(3, "register"))
                thread.start()

    @staticmethod
    def create_lobbystatus_gui():
        if global_var.client.lobbymessage != '':
            Components.draw_text(screen=global_var.menu_screen, x=global_var.width // 2, y=global_var.height - 50, text=global_var.client.lobbymessage, size=20,
                                 color=(255, 6, 193))
            if not menu_var.is_running:
                thread = threading.Thread(target=Components.start_timer_in_thread, args=(3, "lobby"))
                thread.start()

    @staticmethod
    def start_timer_in_thread(arg, text):
        menu_var.is_running = True
        for i in range(arg):
            sleep(1)
        if text == "login":
            global_var.client.loginmessage = ''
            global_var.client.errormessage = ''
        elif text == "lobby":
            global_var.client.lobbymessage = ''
        elif text == 'register':
            global_var.client.errormessage = ''
            global_var.client.registerstatus = ''
        elif text == "game":
            #global_var.menu_state = "main_menu"
            global_var.isgame = True
        menu_var.is_running = False


    @staticmethod
    def do_after_await():
        if menu_var.is_await:
            if global_var.client.logincomplete:
                global_var.menu_state = "lobby_option"
                global_var.client.logincomplete = False
                menu_var.is_await = False
            elif global_var.client.registercomplete:
                global_var.menu_state = "log_menu"
                global_var.client.registercomplete = False
                menu_var.is_await = False
            elif global_var.client.lobbycreated:
                global_var.menu_state = "ingame_lobby"
                menu_var.is_await = False
                global_var.client.lobbycreated = False
            elif global_var.client.searchlobbyJoined and global_var.client.lobbyid != '':
                menu_var.is_await = False
                global_var.client.searchlobbyJoined = False
                global_var.menu_state = "ingame_lobby"
            elif global_var.client.quickLobbyJoined:
                menu_var.is_await = False
                global_var.client.quickLobbyJoined = False
                global_var.menu_state = "ingame_lobby"
            elif global_var.menu_state == "ingame_lobby":
                menu_var.is_await = False
                global_var.menu_state = "ingame_lobby"

    @staticmethod
    def clear_input(text):
        if text == "loginname":
            menu_var.login_name.set_text('')
        elif text == "loginpw":
            menu_var.login_password.set_text('')
        elif text == "registername":
            menu_var.register_name.set_text('')
        elif text == "registerpw":
            menu_var.register_password.set_text('')
        elif text == "chat":
            menu_var.chat_massage.set_text('')
        elif text == "search":
            menu_var.lobby_search_input.set_text('')


    @staticmethod
    def create_ingamelobby(screen):

        rect = pygame.rect.Rect(700, 100, global_var.width // 3, global_var.height - 400)
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, global_var.TRANSPARENT_VIOLLETE, shape_surf.get_rect())
        screen.blit(shape_surf, rect)

        Components.send(x=global_var.width // 2 + 400, y=global_var.height - 50, screen=global_var.menu_screen, text="Senden")
        const = 110

        # Iteriert durch die Chatnachrichten und zeigt sie an
        for i, (user, message) in enumerate(zip(global_var.client.chat_player, global_var.client.chat_message)):
            if const >= 500:
                username = global_var.client.chat_player[len(global_var.client.chat_player) - 1]
                lastmessage = global_var.client.chat_message[len(global_var.client.chat_message) - 1]
                global_var.client.chat_player.clear()
                global_var.client.chat_message.clear()
                global_var.client.chat_player.append(username)
                global_var.client.chat_message.append(lastmessage)
                const = 110
            Components.draw_text_not_Center(screen=screen, y=const, x=720, text=str(user + ":"), size=18, color=global_var.CYAN)
            lines = [message[i:i + 23] for i in range(0, len(message), 23)]

            for line_number, line in enumerate(lines):
                Components.draw_text_not_Center(screen=screen, y=const + line_number * 20, x=830, text=str(line),
                                                size=18,
                                                color=global_var.WHITE)

            const += len(lines) * 20

        global_var.search_counter = 0
        player_texts = [pygame.font.Font(menu_var.FONT, 20).render(player, True, (255, 255, 255)) for player in
                        global_var.id_playerList]

        #Buttons
        Components.zureuck_button(x=global_var.width // 3 - 300, y=global_var.height - 150, screen=global_var.menu_screen)
        Components.abmelden_button(x=global_var.width // 3, y=global_var.height - 150, screen=global_var.menu_screen)


        # Bereitbutton
        if global_var.client.is_ready:
            Components.bereit(x=global_var.width // 3 + 300, y=global_var.height - 50, screen=global_var.menu_screen, text="Bereit")
        elif not global_var.client.is_ready:
            Components.bereit(x=global_var.width // 3 + 300, y=global_var.height - 50, screen=global_var.menu_screen, text="Nicht Bereit")


        pygame.draw.rect(screen, (255, 255, 255), (100, global_var.height // 16, 400, 40), 0)
        for i, (text, color) in enumerate(zip(player_texts, global_var.player_colors)):
            pygame.draw.rect(screen, color, (100, (global_var.height // 16) + (80 * i), 400, 40), 0)
            screen.blit(text, (110, (global_var.height // 16) + (80 * i) + 10))

        #Lobby ID -Anzeige
        font = pygame.font.Font(menu_var.FONT, 18)
        text = font.render(f"Lobby ID: {global_var.client.lobbyid}", True, (global_var.WHITE))
        #update_gui(x=self.x, y=self.y, width=150)
        screen.blit(text, (global_var.width // 2 + 400, global_var.height - 150))


        # Countdown - Anzeige
        font = pygame.font.Font(menu_var.FONT, 18)
        text = font.render(f"Starte in: {global_var.client.timer}", True, (global_var.WHITE))
        # update_gui(x=self.x, y=self.y, width=150)
        screen.blit(text, (global_var.width // 2 + 400, + 20))

        # Benutzer - Anzeige
        font = pygame.font.Font(menu_var.FONT, 18)
        text = font.render(f"ID: {global_var.client.playersname}".format(), True, (global_var.WHITE))
        # update_gui(x=self.x, y=self.y, width=150)
        screen.blit(text, (+100, + 20))

        menu_var.manager_chat.draw_ui(global_var.menu_screen)
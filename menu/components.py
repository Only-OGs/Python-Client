import threading
from time import sleep
from menu.button import Button
import rendering.globals_vars as var
import pygame


button_positions = {
    "linker": {"x": var.width / 2 - var.width / 3, "y": var.height / 2},
    "mittlerer": {"x": var.width / 2, "y": var.height / 2 + 50},
    "rechter": {"x": var.width / 2 + var.width / 3, "y": var.height / 2},
    "log_reg": {"x": var.width - 400, "y": var.height // 2 + 150}
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
        new_height = int((background_image.get_width() / var.width) * var.height)
        background_image = pygame.transform.scale(background_image, (var.width, new_height))
        screen.blit(background_image, (0, 0))

    @staticmethod
    def exit_background(screen):
        background_image = pygame.image.load("assets/exitBackground.png")
        new_height = int((background_image.get_width() / var.width) * var.height)
        background_image = pygame.transform.scale(background_image, (var.width // 2, new_height // 2))
        background_rect = background_image.get_rect(center=(var.width // 2, var.height // 2))
        screen.blit(background_image, background_rect.topleft)

    # Text generieren und zentriert anzeigen lassen.
    @staticmethod
    def draw_text(screen, x, y, text, size, color):
        font = pygame.font.Font(var.FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    # Text generieren und nicht generiert anzeigen lassen.
    @staticmethod
    def draw_text_not_Center(screen, x, y, text, size, color):
        font = pygame.font.Font(var.FONT, size)
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
        var.buttons[trigger] = clicked

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
        lobby_create_button = Button(var.width // 2, var.height // 2 + 20,
                                     button_image, 2, button_image_hover)

        clicked = lobby_create_button.check()
        lobby_create_button.render(screen=screen, text=text, size=18, color="WHITE")
        var.buttons[text] = clicked


    @staticmethod
    def zureuck_button(screen, x, y):
        zurueck_button = Button(x, y,
                                button_image, 2, button_image_hover)

        clicked = zurueck_button.check()
        zurueck_button.render(screen=screen, text="Verlassen", size=18, color="WHITE")
        var.buttons["Verlassen"] = clicked

    @staticmethod
    def abmelden_button(screen, x, y):
        abmelden_button = Button(x, y,
                                button_image, 2, button_image_hover)

        clicked = abmelden_button.check()
        abmelden_button.render(screen=screen, text="Abmelden", size=18, color="WHITE")
        var.buttons["Abmelden"] = clicked

    @staticmethod
    def einstellungen_button(screen, x, y):
        einstellungen_button = Button(x, y,
                                 button_image, 2, button_image_hover)

        clicked = einstellungen_button.check()
        einstellungen_button.render(screen=screen, text="Optionen", size=18, color="WHITE")
        var.buttons["Optionen"] = clicked

    @staticmethod
    def bereit(screen, x, y, text):
        einstellungen_button = Button(x, y,
                                      button_image, 2, button_image_hover)

        clicked = einstellungen_button.check()
        einstellungen_button.render(screen=screen, text=text, size=18, color="WHITE")
        var.buttons[text] = clicked

    @staticmethod
    def send(screen, x, y, text):
        send_button = Button(x, y,button_image, 2, button_image_hover)

        clicked = send_button.check()
        send_button.render(screen=screen, text=text, size=18, color="WHITE")
        var.buttons[text] = clicked

    @staticmethod
    def quick_game_button(screen, text):
        quick_game_button = Button(var.width // 2, var.height // 2 + (6*20),
                                   button_image, 2, button_image_hover)
        clicked = quick_game_button.check()
        quick_game_button.render(screen=screen, text=text, size=18, color="WHITE")
        var.buttons[text] = clicked


    @staticmethod
    def search_lobby_button(screen, text):
        search_lobby_button = Button(var.width // 2, (var.height // 2 + (11 * 20)),
                                     button_image, 2, button_image_hover)
        clicked = search_lobby_button.check()
        search_lobby_button.render(screen=screen, text=text, size=font_size, color="WHITE")
        var.buttons[text] = clicked


    @staticmethod
    def log_out_button(screen, text):
        log_out_button = Button(var.width // 2, (var.height // 2 + (16 * 20)),
                                button_image, 2, button_image_hover)
        clicked = log_out_button.check()
        log_out_button.render(screen=screen, text=text, size=font_size, color="WHITE")
        var.buttons[text] = clicked

    # Status - GUI erstellen:
    '''
    Zeigt die verschiedenen vom Server für den User an 
    '''
    @staticmethod
    def create_Serverstatus_gui():
        if var.client.sio.connected:
            Components.draw_text(screen=var.menu_screen, x=100, y=130, text="ONLINE", size=20, color="GREEN")
        else:
            Components.draw_text(screen=var.menu_screen, x=100, y=130, text="OFFLINE", size=20, color="RED")
        Components.draw_text(screen=var.menu_screen, x=100, y=100, text="Server:", size=17, color="WHITE")



    @staticmethod
    def create_loginstatus_gui(text):
        if text == "login":
            text = var.client.loginmessage
        else:
            text = var.client.errormessage
        if text != '':
            Components.draw_text(screen=var.menu_screen, x=var.width // 2, y=var.height - 50, text=text,
                                 size=20,
                                 color=(255, 6, 193))
            if not var.is_running:
                thread = threading.Thread(target=Components.start_timer_in_thread, args=(3, "login"))
                thread.start()
    @staticmethod
    def create_registerstatus_gui(text):
        if text == "register":
            text = var.client.registerstatus
        else:
            text = var.client.errormessage
        if text != '':
            Components.draw_text(screen=var.menu_screen, x=var.width // 2, y=var.height - 50, text=text,
                                 size=20,
                                 color=(255, 6, 193))
            if not var.is_running:
                thread = threading.Thread(target=Components.start_timer_in_thread, args=(3, "register"))
                thread.start()

    @staticmethod
    def create_lobbystatus_gui():
        if var.client.lobbymessage != '':
            Components.draw_text(screen=var.menu_screen, x=var.width // 2, y=var.height - 50, text=var.client.lobbymessage, size=20,
                                 color=(255, 6, 193))
            if not var.is_running:
                thread = threading.Thread(target=Components.start_timer_in_thread, args=(3, "lobby"))
                thread.start()

    @staticmethod
    def start_timer_in_thread(arg, text):
        var.is_running = True
        for i in range(arg):
            sleep(1)
        if text == "login":
            var.client.loginmessage = ''
            var.client.errormessage = ''
        elif text == "lobby":
            var.client.lobbymessage = ''
        elif text == 'register':
            var.client.errormessage = ''
            var.client.registerstatus = ''
        elif text == "game":
            var.menu_state == "main_menu"
            var.isgame = True
        var.is_running = False


    @staticmethod
    def create_ingamelobby(screen):

        rect = pygame.rect.Rect(700, 100, var.width// 3, var.height - 400)
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, var.TRANSPARENT_VIOLLETE, shape_surf.get_rect())
        screen.blit(shape_surf, rect)

        Components.send(x=var.width // 2 + 400, y=var.height - 50, screen=var.menu_screen, text="Senden")
        const = 110

        # Iteriert durch die Chatnachrichten und zeigt sie an
        for i, (user, message) in enumerate(zip(var.client.chat_player, var.client.chat_message)):
            if const >= 500:
                username = var.client.chat_player[len(var.client.chat_player)-1]
                lastmessage = var.client.chat_message[len(var.client.chat_message)-1]
                var.client.chat_player.clear()
                var.client.chat_message.clear()
                var.client.chat_player.append(username)
                var.client.chat_message.append(lastmessage)
                const = 110
            Components.draw_text_not_Center(screen=screen, y=const, x=720, text=str(user + ":"), size=18, color=var.CYAN)
            lines = [message[i:i + 23] for i in range(0, len(message), 23)]

            for line_number, line in enumerate(lines):
                Components.draw_text_not_Center(screen=screen, y=const + line_number * 20, x=830, text=str(line),
                                                size=18,
                                                color=var.WHITE)

            const += len(lines) * 20

        var.search_counter = 0
        player_texts = [pygame.font.Font(var.FONT, 20).render(player, True, (255, 255, 255)) for player in
                        var.id_playerList]

        #Buttons
        Components.zureuck_button(x=var.width // 3 - 300, y=var.height - 150, screen=var.menu_screen)
        Components.abmelden_button(x=var.width // 3, y=var.height - 150, screen=var.menu_screen)


        # Bereitbutton
        if var.client.is_ready:
            Components.bereit(x=var.width // 3 + 300, y=var.height - 50, screen=var.menu_screen, text="Bereit")
        elif not var.client.is_ready:
            Components.bereit(x=var.width // 3 + 300, y=var.height - 50, screen=var.menu_screen, text="Nicht Bereit")


        pygame.draw.rect(screen, (255, 255, 255), (100, var.height // 16, 400, 40), 0)
        for i, (text, color) in enumerate(zip(player_texts, var.player_colors)):
            pygame.draw.rect(screen, color, (100, (var.height // 16) + (80 * i), 400, 40), 0)
            screen.blit(text, (110, (var.height // 16) + (80 * i) + 10))

        #Lobby ID -Anzeige
        font = pygame.font.Font(var.FONT, 18)
        text = font.render(f"Lobby ID: {var.client.lobbyid}", True, (var.WHITE))
        #update_gui(x=self.x, y=self.y, width=150)
        screen.blit(text, (var.width//2+400, var.height-150))


        # Countdown - Anzeige
        font = pygame.font.Font(var.FONT, 18)
        text = font.render(f"Starte in: {var.client.timer}", True, (var.WHITE))
        # update_gui(x=self.x, y=self.y, width=150)
        screen.blit(text, (var.width // 2 + 400, + 20))

        # Benutzer - Anzeige
        font = pygame.font.Font(var.FONT, 18)
        text = font.render(f"ID: {var.client.playersname}".format(), True, (var.WHITE))
        # update_gui(x=self.x, y=self.y, width=150)
        screen.blit(text, (+100, + 20))

        var.manager_chat.draw_ui(var.menu_screen)
import threading
from time import sleep
from rendering.button import Button
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


class Layout:

    def __create_button(screen, x, y, text, trigger):
        button = Button(x=x, y=y, image=button_image, size=button_size, hover=button_image_hover)
        button.render(screen=screen, text=text, size=font_size, color="WHITE")
        clicked = button.check()
        var.buttons[trigger] = clicked

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


    @staticmethod
    def draw_text(screen, x, y, text, size, color):
        font = pygame.font.Font(var.FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    @staticmethod
    def linker_button(screen, text, trigger):
        return Layout.__create_button(screen, **button_positions["linker"], text=text, trigger=trigger)

    @staticmethod
    def mittlerer_button(screen, text, trigger):
        return Layout.__create_button(screen, **button_positions["mittlerer"], text=text, trigger=trigger)

    @staticmethod
    def rechter_button(screen, text, trigger):
        return Layout.__create_button(screen, **button_positions["rechter"], text=text, trigger=trigger)

    @staticmethod
    def log_reg_button(screen, text):
        return Layout.__create_button(screen, **button_positions["log_reg"], text=text, trigger=text)

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

    @staticmethod
    def create_Serverstatus_gui():
        if var.client.sio.connected:
            Layout.draw_text(screen=var.menu_screen, x=100, y=130, text="ONLINE", size=20, color="GREEN")
        else:
            Layout.draw_text(screen=var.menu_screen, x=100, y=130, text="OFFLINE", size=20, color="RED")
        Layout.draw_text(screen=var.menu_screen, x=100, y=100, text="Server:", size=17, color="WHITE")

    @staticmethod
    def threaded_function(arg, text):
        var.is_running = True
        for i in range(arg):
            sleep(1)
        if text == "login":
            var.client.loginmessage = ''
        elif text == "lobby":
            var.client.lobbymessage = ''
        elif text == "game":
            var.menu_state == "main_menu"
            var.isgame = True
        var.is_running = False


    @staticmethod
    def create_loginstatus_gui():

        if var.client.loginmessage != '':
            Layout.draw_text(screen=var.menu_screen, x=var.width//2, y=var.height - 50, text=var.client.loginmessage, size=20,
                             color=(255, 6, 193))
            if not var.is_running:
                thread = threading.Thread(target=Layout.threaded_function, args=(3, "login"))
                thread.start()

    @staticmethod
    def create_lobbystatus_gui():
        if var.client.lobbymessage != '':
            Layout.draw_text(screen=var.menu_screen,  x=var.width//2, y=var.height - 50, text=var.client.lobbymessage, size=20,
                             color=(255, 6, 193))
            if not var.is_running:
                thread = threading.Thread(target=Layout.threaded_function, args=(3, "lobby"))
                thread.start()

    @staticmethod
    def create_ingamelobby(screen):
        # counter für "Suchen..."

        Layout.init_second_background(screen)

        var.search_counter = 0
        player_texts = [pygame.font.Font(var.FONT, 20).render(player, True, (255, 255, 255)) for player in
                        var.id_playerList]

        #Button
        Layout.zureuck_button(x=var.width//3-300,y=var.height-150, screen=var.menu_screen)
        Layout.abmelden_button(x=var.width//3,y=var.height-150, screen=var.menu_screen)
        Layout.einstellungen_button(x=var.width//3+300,y=var.height-150, screen=var.menu_screen)

        if var.client.is_ready:
            Layout.bereit(x=var.width // 3 + 300, y=var.height - 50, screen=var.menu_screen, text="Bereit")
        elif not var.client.is_ready:
            Layout.bereit(x=var.width // 3 + 300, y=var.height - 50, screen=var.menu_screen, text="Nicht Bereit")


        pygame.draw.rect(screen, (255, 255, 255), (100, var.height // 16, 400, 40), 0)
        for i, (text, color) in enumerate(zip(player_texts, var.player_colors)):
            pygame.draw.rect(screen, color, (100, (var.height // 16) + (80 * i), 400, 40), 0)
            screen.blit(text, (110, (var.height // 16) + (80 * i) + 10))

        #Lobby ID
        font = pygame.font.Font(var.FONT, 18)
        text = font.render(f"Lobby ID: {var.client.lobbyid}", True, (var.WHITE))
        #update_gui(x=self.x, y=self.y, width=150)
        screen.blit(text, (var.width//2+400, var.height-150))

        #Lobby Countdown
        font = pygame.font.Font(var.FONT, 18)
        text = font.render(f"Starte in: {var.client.timer}", True, (var.WHITE))
        # update_gui(x=self.x, y=self.y, width=150)
        screen.blit(text, (var.width // 2 + 400, + 20))

        #Name
        font = pygame.font.Font(var.FONT, 18)
        text = font.render(f"ID: {var.client.playersname}".format(), True, (var.WHITE))
        # update_gui(x=self.x, y=self.y, width=150)
        screen.blit(text, (+100, + 20))



        var.search_counter += 1

        if var.search_counter == 60:
            player_texts.extend([pygame.font.Font(var.FONT, 20).render("Suchen .", True, (0, 0, 0))] * (
                    len(player_texts) - len(var.id_playerList)))
        elif var.search_counter == 120:
            player_texts.extend([pygame.font.Font(var.FONT, 20).render("Suchen ..", True, (0, 0, 0))] * (
                    len(player_texts) - len(var.id_playerList)))
        elif var.search_counter == 180:
            player_texts.extend([pygame.font.Font(var.FONT, 20).render("Suchen ...", True, (0, 0, 0))] * (
                    len(player_texts) - len(var.id_playerList)))

        var.search_counter = 0
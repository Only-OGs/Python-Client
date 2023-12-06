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
FONT = "assets/rocket-rinder-font/RocketRinder-yV5d.ttf"
button_image_hover = 'assets/button-pressed.png'
button_size = 2
font_size = 20


class Layout:

    def __create_button(screen, x, y, text):
        button = Button(x=x, y=y, image=button_image, size=button_size, hover=button_image_hover)
        button.render(screen=screen, text=text, size=font_size, color="WHITE")
        clicked = button.check()
        var.buttons[text] = clicked

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
    def draw_text(screen, x, y, text, size, color):
        font = pygame.font.Font(FONT, size)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    @staticmethod
    def linker_button(screen, text):
        return Layout.__create_button(screen, **button_positions["linker"], text=text)

    @staticmethod
    def mittlerer_button(screen, text):
        return Layout.__create_button(screen, **button_positions["mittlerer"], text=text)

    @staticmethod
    def rechter_button(screen, text):
        return Layout.__create_button(screen, **button_positions["rechter"], text=text)

    @staticmethod
    def log_reg_button(screen, text):
        return Layout.__create_button(screen, **button_positions["log_reg"], text=text)

    @staticmethod
    def lobby_create_button(screen, text):
        lobby_create_button = Button(var.width // 2, var.height // 2 + 20,
                                     button_image, 2, button_image_hover)

        clicked = lobby_create_button.check()
        lobby_create_button.render(screen=screen, text=text, size=18, color="WHITE")
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
    def create_Serverstatus():
        if var.client.sio.connected:
            Layout.draw_text(screen=var.menu_screen, x=100, y=130, text="ONLINE", size=20, color="GREEN")
        else:
            Layout.draw_text(screen=var.menu_screen, x=100, y=130, text="OFFLINE", size=20, color="RED")
        Layout.draw_text(screen=var.menu_screen, x=100, y=100, text="Server:", size=17, color="WHITE")



    #TODO - noch nicht gestestet!

    @staticmethod
    def create_ingamelobby(screen):
        # counter für "Suchen..."
        var.search_counter = 0
        player_texts = [pygame.font.SysFont(FONT, 20).render(player, True, (255, 255, 255)) for player in
                        var.id_playerList]


        pygame.draw.rect(screen, (255, 255, 255), (100, var.height // 16, 400, 40), 0)
        for i, (text, color) in enumerate(zip(player_texts, var.player_colors)):
            pygame.draw.rect(screen, color, (100, (var.height // 16) + (80 * i), 400, 40), 0)
            screen.blit(text, (110, (var.height // 16) + (80 * i) + 10))

        var.search_counter += 1

        if var.search_counter == 60:
            player_texts.extend([pygame.font.SysFont(FONT, 20).render("Suchen .", True, (0, 0, 0))] * (
                    len(player_texts) - len(var.id_playerList)))
        elif var.search_counter == 120:
            player_texts.extend([pygame.font.SysFont(FONT, 20).render("Suchen ..", True, (0, 0, 0))] * (
                    len(player_texts) - len(var.id_playerList)))
        elif var.search_counter == 180:
            player_texts.extend([pygame.font.SysFont(FONT, 20).render("Suchen ...", True, (0, 0, 0))] * (
                    len(player_texts) - len(var.id_playerList)))

        var.search_counter = 0


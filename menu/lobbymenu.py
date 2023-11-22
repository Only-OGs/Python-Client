import pygame
from pygame.font import Font
from client.button import Button
from game.globals import screen_width
from game.globals import screen_height


class LobbyMenu:

    def __init__(self, screen):
        self.text = "Lobbyauswahl"
        self.screen = screen
        self.screen.fill('#14152c')
        self.text_font = Font("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 45)
        self.draw_text("#FF06C1", screen_width // 2 - (screen_width // 6), screen_height // 4 - 80)
        self.draw_buttons()

    def draw_text(self, text_col, x, y):
        img = self.text_font.render(self.text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_buttons(self):
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

        lobby_create_button.draw(self.screen)
        lobby_create_button.text(self.screen, "Lobby erstellen", 18, (255, 255, 255))

        quick_game_button.draw(self.screen)
        quick_game_button.text(self.screen, "Schnelles Spiel", 18, (255, 255, 255))

        search_lobby_button.draw(self.screen)
        search_lobby_button.text(self.screen, "Lobby suchen", 18, (255, 255, 255))

        log_out_button.draw(self.screen)
        log_out_button.text(self.screen, "Abmelden", 18, (255, 255, 255))

from pygame.font import Font
from rendering.button import Button
from globals.globals import screen_width
from globals.globals import screen_height
import pygame
import sys


class Lobby:

    def __init__(self, screen, client):
        self.screen = screen
        self.client = client

    def draw(self):
        self.screen.fill('#14152c')
        text_font = Font("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 45)
        button_image = 'assets/button.png'
        button_image_hover = 'assets/button-pressed.png'
        button_spacing = 30
        button_size = 2

        lobbytext = "Die Lobby"
        idtext = "ID: "
        username = "test"
        chatText = "Chat: "
        lobbyIDtext = "Lobby ID: "
        lobbyID = "ID"
        searchText = "Suchen"

        leave_button = Button(screen_width // 2, screen_height // 2 - (2 * button_spacing),
                                         button_image, button_size, button_image_hover)

        send_button = Button(screen_width // 2, screen_height // 2 - (2 * button_spacing),
                                         button_image, button_size, button_image_hover)

        leave_button.text(self.screen, "Verlassen", 18, (255, 255, 255))
        send_button.text(self.screen, "Senden", 18, (255, 255, 255))
        isLeaveClicked = leave_button.draw(self.screen)
        isSendClicked = send_button.draw(self.screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if isLeaveClicked:
                pass
            if isSendClicked:
                pass


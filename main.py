import pygame_gui
from client.menu import MainMenu

g = MainMenu()

while g.run:
    g.game_loop()

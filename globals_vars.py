from communication.client import SocketIOClient
import pygame

"""Globale Game Variablen"""
fps = 60
step = 1 / fps
width = 1329
height = 886
clock = pygame.time.Clock()
menu_screen = pygame.display.set_mode((1329, 886))

"""Farben"""
BLACK, WHITE, RED, VIOLETTE, CYAN, DARKBLUE, YELLOW, ORANGE = (0, 0, 0), (255, 255, 255), (255, 0, 0), (255, 6, 193), (
0, 255, 234), (20, 21, 44), (234, 235, 44), (250, 128, 87)
DARK_VIOLLETTE, DARK_CYAN, DARK_YELLOW, LIGHT_ORANGE = (186, 46, 151), (55, 214, 201), (234, 235, 117), (255, 151, 116)
TRANSPARENT_WHITE = (255, 255, 255, 100)
TRANSPARENT_RED = (255, 0, 0, 20)
TRANSPARENT_VIOLLETE = (186, 46, 151, 215)
player_colors = [(255, 6, 193), (186, 46, 151), (0, 255, 234), (55, 214, 201), (234, 235, 44), (234, 235, 117),
                 (250, 128, 87), (255, 155, 116)]
keyLeft = False
keyRight = False
keyFaster = False
keySlower = False

game_end = False  # Bestenlisteanzeigeindikator
isgame = False
lap_count = 1
menu_state = "main_menu"
'''Musik'''
play_music = True

"""MULTIPLAYER"""
singleplayer_start = False
game_countdown_start = ''
search_counter = 0
game_counter = 0
game_start = False
id_playerList = []
race_finished = False
"""SocketIO"""
client = SocketIOClient()
trackloaded = False
singleplayer = True
# sio = None
player_cars = []
help_car = False
username = ""
assets = []

"""HUD im Online Mouds"""
lap = ""
best_time = ""
lap_time = ""
current_time = ""

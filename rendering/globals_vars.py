import math
import threading

import pygame
from communication.client import SocketIOClient
"""Globale Game Variablen"""
fps = 60
step = 1 / fps
width = 1329
height = 886

SCREEN_WIDTH = 1329
SCREEN_HEIGHT = 886

"""Colours"""
BLACK, WHITE, RED, VIOLETTE, CYAN, DARKBLUE, YELLOW, ORANGE = (0, 0, 0), (255, 255, 255), (255, 0, 0), (255, 6, 193), (0, 255, 234), (20, 21, 44), (234, 235, 44), (250, 128, 87)
DARK_VIOLLETTE, DARK_CYAN, DARK_YELLOW, LIGHT_ORANGE = (186, 46, 151), (55, 214, 201), (234, 235, 117), (255, 151, 116)
TRANSPARENT_WHITE = (255, 255, 255, 100)
TRANSPARENT_RED = (255, 0, 0, 20)
TRANSPARENT_VIOLLETE = (186, 46, 151, 215)
player_colors = [(255, 6, 193), (186, 46, 151), (0, 255, 234), (55, 214, 201), (234, 235, 44), (234, 235, 117),
                 (250, 128, 87), (255, 155, 116)]
"""pygame_gui"""
FONT = "assets/rocket-rinder-font/RocketRinder-yV5d.ttf"
slider_width = 500
slider_height = 30
music_slider = None
"""GAME"""
segments = []
screen = None
menu_screen = pygame.display.set_mode((width, height))
background = None
sprites = None
resolution = None
roadWidth = 2000
segmentLength = 200
rumbleLength = 3
trackLength = 0
lanes = 3
fieldOfView = 100
cameraHeight = 1000
cameraDepth = 1 / math.tan((fieldOfView / 2) * math.pi / 180)
drawDistance = 500
segment_count = 600
playerX = 0
playerZ = (cameraHeight * cameraDepth)
fogDensity = 15
position = 0
speed = 0
maxSpeed = segmentLength/step
accel = maxSpeed / 5
breaking = -maxSpeed
decel = -maxSpeed / 5
offRoadDecel = -maxSpeed / 2
offRoadLimit = maxSpeed / 4
clock = pygame.time.Clock()
centrifugal = 0.37
keyLeft = False
keyRight = False
keyFaster = False
keySlower = False
total_cars = 30
dt = 1 / 30
cars = []
player = None
background_sprite_group = None
player_sprite_group = None
track = None
gameStart = False
game_end = False
isgame = False
lap_count = 0
"""Screens"""
menu_state = "main_menu"
escape = False
buttons = {
    "Anmelden": False,
    "Zurueck": False,
    "Registrieren": False,
    "Abmelden": False,
    "Schnelles Spiel": False,
    "Lobby erstellen": False,
    "Lobby suchen": False,
    "Jetzt Registrieren": False,
    "Jetzt Anmelden": False,
    "Mehrspieler": False,
    "Optionen": False,
    "Einzelspieler": False,
    "Suchen": False,
    "Bereit": False,
    "Nicht Bereit": False,
    "Verlassen": False,
    "loading": False,
    "Game": False,
    "Senden": False
}

"""MULTIPLAYER"""
singleplayer_start = False
game_countdown_start = ''
search_counter = 0
game_counter = 0
game_start = False
id_playerList = []
"""SocketIO"""
client = SocketIOClient()
login_name = None
login_password = None
register_name = None
register_password = None
chat_massage = None
manager_option = None
manager_register = None
manager_Login = None
manager_lobby_search = None
manager_chat = None
lobby_search_input = None
is_await = False
player_texts = []
is_running = False
trackloaded = False
singleplayer = True
sio = None
player_cars = []
help_car = False
username = ""
olddata = 0
new_car_data = []
paused = False
leaderboard = []
assets = []
"""HUD im Online Mouds"""
lap = ""
best_time = ""
lap_time = ""
current_time = ""

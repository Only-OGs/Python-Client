import math
import pygame
from communication.client import SocketIOClient
"""Globale Game Variablen"""
fps = 60
step = 1 / fps
width = 1329
height = 886
segments = []
screen = None
menu_screen = pygame.display.set_mode((1329, 886))
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
maxSpeed = 24000
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
gameStart = None
menu_state = "main_menu"
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
    "Suchen": False
}

SCREEN_WIDTH = 1329
SCREEN_HEIGHT = 886
client = SocketIOClient()
search_counter = 0
player_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
                 (128, 0, 0), (0, 128, 0)]
id_playerList = []
slider_width = 500
slider_height = 30
music_slider = None
login_name = None
login_password = None
register_name = None
register_password = None
manager_option = None
manager_register = None
manager_Login = None
manager_lobby_search = None
lobby_search_input = None


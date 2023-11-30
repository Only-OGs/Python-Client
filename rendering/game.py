import math

import pygame, sys

from rendering.sprites.player import Player
from rendering.utility.util import Util
from rendering.sprites.background import Background
from rendering.utility.colors import Color
from rendering import gui


class Game:
    fps = 60
    step = 1 / fps
    width = 1024
    height = 768
    segments = []
    screen = None
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
    maxSpeed = segmentLength / step
    accel = maxSpeed / 5
    breaking = -maxSpeed
    decel = -maxSpeed / 5
    offRoadDecel = -maxSpeed / 2
    offRoadLimit = maxSpeed / 4
    clock = None

    keyLeft = False
    keyRight = False
    keyFaster = False
    keySlower = False

    dt = 1 / 30

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.player_sprite_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()
        self.reset_road()
        self.game_loop()

    # main loop wo alles passiert
    def game_loop(self):
        self.create_player()
        self.create_background()
        self.background_group.draw(self.screen)
        self.add = 0
        timer = gui.Gui(screen=self.screen, x=0, y=0)


        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.keyLeft = True
                    if event.key == pygame.K_RIGHT:
                        self.keyRight = True
                    if event.key == pygame.K_UP:
                        self.keyFaster = True
                    if event.key == pygame.K_DOWN:
                        self.keySlower = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.keyLeft = False
                    if event.key == pygame.K_RIGHT:
                        self.keyRight = False
                    if event.key == pygame.K_UP:
                        self.keyFaster = False
                    if event.key == pygame.K_DOWN:
                        self.keySlower = False


            timer.show_speed(speed=self.speed)
            timer.count_up()
            print(self.position)
            if(self.position >= round(119900.0)):
                timer.ende_timer()

            self.render()
            self.update(self.step)
            pygame.display.update()
            self.clock.tick(self.fps)


    # unser KeyInputHandler, hier werden die Keyinputs überprüft und das auto dementsprechend bewegt
    def update(self, dt):
        self.position = Util.increase(self.position, dt * self.speed, self.trackLength)

        dx = dt * 2 * (self.speed / self.maxSpeed)

        if self.keyLeft:
            self.playerX = self.playerX - dx
            if self.speed > 0:
                self.player.drive_left()
        elif self.keyRight:
            self.playerX = self.playerX + dx
            if self.speed > 0:
                self.player.drive_right()
        else:
            self.player.drive_straight()

        if self.keyFaster:
            self.speed = Util.accelerate(self.speed, self.accel, self.dt)
        elif self.keySlower:
            self.speed = Util.accelerate(self.speed, self.breaking, self.dt)
        else:
            self.speed = Util.accelerate(self.speed, self.decel, self.dt)

        if (self.playerX < -1 or self.playerX > 1) and (self.speed > self.offRoadLimit):
            self.speed = Util.accelerate(self.speed, self.offRoadDecel, self.dt)

        self.playerX = Util.limit(self.playerX, -2, 2)
        self.speed = Util.limit(self.speed, 0, self.maxSpeed)

    # erstellt die Straße und die Finishline
    def reset_road(self):
        self.segments = []

        for n in range(self.segment_count):
            self.segments.append(
                {
                    'index': n,
                    'p1':
                        {'world': {
                            'x': None,
                            'y': None,
                            'z': n * self.segmentLength
                        },
                            'camera': {
                                'x': 0,
                                'y': 0,
                                'z': 0
                            },
                            'screen': {
                                "scale": 0,
                                'x': 0,
                                'y': 0,
                            },
                        },
                    'p2':
                        {'world': {
                            'x': None,
                            'y': None,
                            'z': (n + 1) * self.segmentLength
                        },
                            'camera': {
                                'x': 0,
                                'y': 0,
                                'z': 0
                            },
                            'screen': {
                                "scale": 0,
                                'x': 0,
                                'y': 0,
                            },
                        },
                    'color': self._road_color(n)
                })

        self.segments[self.findSegment(self.playerZ)["index"] + 2]["color"] = Color.get_start()
        self.segments[self.findSegment(self.playerZ)["index"] + 3]["color"] = Color.get_start()
        for n in range(self.rumbleLength):
            self.segments[len(self.segments) - 1 - n]["color"] = Color.get_finish()

        self.trackLength = len(self.segments) * self.segmentLength

    # hilfsfunktion fürs erstellen der Straße
    def _road_color(self, n):
        if math.floor(n / self.rumbleLength) % 2 == 0:
            return Color.get_light()
        else:
            return Color.get_dark()

    # hilfsfunktion fürs rendern
    def findSegment(self, z):
        return self.segments[math.floor(z / self.segmentLength) % len(self.segments)]

    # Rendert alles
    def render(self):
        basesegment = self.findSegment(self.position)
        maxy = self.height

        for n in range(self.drawDistance):
            segment = self.segments[(basesegment.get("index") + n) % len(self.segments)]
            segment_looped = segment.get("index") < basesegment.get("index")
            segment_fog = Util.exponential_fog(n / self.drawDistance, self.fogDensity)

            if segment_looped:
                segment_looped_value = self.trackLength
            else:
                segment_looped_value = 0

            segment["p1"] = Util.project(
                segment.get("p1"),
                (self.playerX * self.roadWidth),
                self.cameraHeight,
                self.position - segment_looped_value,
                self.cameraDepth,
                self.width, self.height,
                self.roadWidth)

            segment["p2"] = Util.project(
                segment.get("p2"),
                (self.playerX * self.roadWidth),
                self.cameraHeight,
                self.position - segment_looped_value,
                self.cameraDepth,
                self.width, self.height,
                self.roadWidth)

            if (segment.get("p1").get("camera").get("z") <= self.cameraDepth) or (
                    segment.get("p2").get("screen").get("y") >= maxy):
                continue

            Util.segment(self.screen, self.width, self.lanes,
                         segment.get("p1").get("screen").get("x"),
                         segment.get("p1").get("screen").get("y"),
                         segment.get("p1").get("screen").get("w"),
                         segment.get("p2").get("screen").get("x"),
                         segment.get("p2").get("screen").get("y"),
                         segment.get("p2").get("screen").get("w"),
                         segment.get("color"), segment_fog)

            maxy = segment.get("p2").get("screen").get("y")

            # render player
            self.player_sprite_group.draw(self.screen)

    # baut den hintergrund zusammen
    def create_background(self):
        bg_sky = Background(0, pygame.image.load("assets/sky.png"))
        bg_hills = Background(0, pygame.image.load("assets/hills.png"))
        bg_tree = Background(0, pygame.image.load("assets/trees.png"))

        self.background_group.add(bg_sky)
        self.background_group.add(bg_hills)
        self.background_group.add(bg_tree)

    # erstellt den Spieler Sprite und fügt sie der Player Sprite Gruppe hinzu
    def create_player(self):
        self.player = Player(self.screen.get_width() / 2 - 30, self.screen.get_height() - 100)
        self.player_sprite_group.add(self.player)


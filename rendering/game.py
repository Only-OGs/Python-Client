import math
import random

import pygame, sys

from rendering.sprites.player import Player
from rendering.utility.road import Road
from rendering.utility.sprites import Sprite
from rendering.utility.util import Util
from rendering.sprites.background import Background
from rendering.utility.colors import Color


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
    maxSpeed = 24000
    accel = maxSpeed / 5
    breaking = -maxSpeed
    decel = -maxSpeed / 5
    offRoadDecel = -maxSpeed / 2
    offRoadLimit = maxSpeed / 4
    clock = None
    centrifugal = 0.37
    keyLeft = False
    keyRight = False
    keyFaster = False
    keySlower = False
    total_cars = 3
    dt = 1 / 30
    cars = []

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.player_sprite_group = pygame.sprite.Group()
        self.background_sprite_group = pygame.sprite.Group()
        self.reset_road()
        self.game_loop()

    # main loop wo alles passiert
    def game_loop(self):
        self.create_player()
        self.create_background()

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

            self.render()
            self.update(self.step)
            pygame.display.update()
            self.clock.tick(self.fps)

    # unser KeyInputHandler, hier werden die Keyinputs überprüft und das auto dementsprechend bewegt
    def update(self, dt):
        playersegment = self.findSegment(self.position + self.playerZ)
        speedpercent = self.speed / self.maxSpeed
        self.position = Util.increase(self.position, dt * self.speed, self.trackLength)

        dx = dt * 2 * speedpercent

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

        self.playerX = self.playerX - (dx * speedpercent * playersegment.get("curve") * self.centrifugal)

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

        # car here
        playerw = ((1 / 80) * 0.3) * 80

        self.update_cars(dt, playersegment, playerw)

    # erstellt die Straße und die Finishline
    def reset_road(self):
        self.segments = []

        Road.load_road(self)
        self.reset_cars()
        self.reset_sprites()

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
        basepercent = Util.percent_remaining(self.position, self.segmentLength)
        playersegment = self.findSegment(self.position + self.playerZ)
        playerpercent = Util.percent_remaining(self.position + self.playerZ, self.segmentLength)

        playery = Util.interpolate(playersegment.get("p1").get("world").get("y"),
                                   playersegment.get("p2").get("world").get("y"), playerpercent)

        dx = -(basesegment.get("curve") * basepercent)
        x = 0
        maxy = self.height

        self.background_sprite_group.draw(self.screen)

        # straße
        for n in range(self.drawDistance):
            segment = self.segments[(basesegment.get("index") + n) % len(self.segments)]
            segment_looped = segment.get("index") < basesegment.get("index")
            segment_fog = Util.exponential_fog(n / self.drawDistance, self.fogDensity)
            segment["clip"] = maxy

            if segment_looped:
                segment_looped_value = self.trackLength
            else:
                segment_looped_value = 0

            segment["p1"] = Util.project(
                segment.get("p1"),
                (self.playerX * self.roadWidth) - x,
                playery + self.cameraHeight,
                self.position - segment_looped_value,
                self.cameraDepth,
                self.width, self.height,
                self.roadWidth)

            segment["p2"] = Util.project(
                segment.get("p2"),
                (self.playerX * self.roadWidth) - x - dx,
                playery + self.cameraHeight,
                self.position - segment_looped_value,
                self.cameraDepth,
                self.width, self.height,
                self.roadWidth)

            x = x + dx
            dx = dx + segment.get("curve")

            if (segment.get("p1").get("camera").get("z") <= self.cameraDepth) or (
                    segment.get("p2").get("screen").get("y") >= maxy) or (
                    segment.get("p2").get("screen").get("y") >= segment.get("p1").get("screen").get("y")):
                continue

            Util.segment(self.screen, self.width, self.lanes,
                         segment.get("p1").get("screen").get("x"),
                         segment.get("p1").get("screen").get("y"),
                         segment.get("p1").get("screen").get("w"),
                         segment.get("p2").get("screen").get("x"),
                         segment.get("p2").get("screen").get("y"),
                         segment.get("p2").get("screen").get("w"),
                         segment.get("color"), segment_fog)

            maxy = segment.get("p1").get("screen").get("y")

        for n in range(self.drawDistance - 1, 0, -1):
            segment = self.segments[(basesegment.get("index") + n) % len(self.segments)]
            self.render_sprites(segment)
            self.render_cars(segment)
        self.player_sprite_group.draw(self.screen)

    # baut den hintergrund zusammen
    def create_background(self):
        bg_sky = Background(0, pygame.image.load("assets/sky.png"))
        bg_hills = Background(0, pygame.image.load("assets/hills.png"))
        bg_tree = Background(0, pygame.image.load("assets/trees.png"))

        self.background_sprite_group.add(bg_sky)
        self.background_sprite_group.add(bg_hills)
        self.background_sprite_group.add(bg_tree)

    # erstellt den Spieler Sprite und fügt sie der Player Sprite Gruppe hinzu
    def create_player(self):
        self.player = Player(self.screen.get_width() / 2 - 30, self.screen.get_height() - 100)
        self.player_sprite_group.add(self.player)

    def add_segment(self, curve, y):
        n = len(self.segments)
        self.segments.append(
            {
                'index': n,
                'p1':
                    {'world': {
                        'x': None,
                        'y': self.lastY(),
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
                        'y': y,
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
                "curve": curve,
                "cars": [],
                "clip": 0,
                "sprites": [],
                'color': self._road_color(n)
            })

    # Erstellt die Straße, so dass wenn es eine Kurbe
    def add_road(self, enter, hold, leave, curve, y=0):
        starty = self.lastY()
        endy = starty + (int(y) * self.segmentLength)
        total = int(enter) + int(hold) + int(leave)
        for n in range(int(enter)):
            self.add_segment(Util.easeIn(0, curve, n / enter), Util.easeInOut(starty, endy, n / total))
        for n in range(int(hold)):
            self.add_segment(curve, Util.easeInOut(starty, endy, (enter + n) / total))
        for n in range(int(leave)):
            self.add_segment(Util.easeInOut(0, curve, n / enter),
                             Util.easeInOut(starty, endy, (enter + hold + n) / total))

    # Übergibt die passenden Parameter für die Straße
    def add_street(self, num=None, curve=None, height=None):
        if num is None:
            num = Road.lenght().get("medium")
        if curve is None:
            curve = Road.curve().get("none")
        if height is None:
            height = Road.hill().get("none")

        self.add_road(num, num, num, curve, height)

    # berechnet der letzten Y-Koordinate
    def lastY(self):
        if len(self.segments) == 0:
            return 0
        else:
            return self.segments[len(self.segments) - 1].get("p2").get("world").get("y")

    def reset_cars(self):
        self.cars = []

        for n in range(self.total_cars):
            offset = random.random() * Util.random_choice([-0.8, 0.8])
            z = math.floor(random.random() * len(self.segments) * self.segmentLength)
            sprite = Sprite.random_car()
            speed = self.maxSpeed / 4 + random.random() * self.maxSpeed / 2
            car = {"offset": offset, "z": z, "sprite": sprite, "speed": speed, "percent": 0}
            segment = self.findSegment(z)
            segment["cars"].append(car)
            self.cars.append(car)

    def render_cars(self, segment):
        for n in range(len(segment.get("cars"))):
            car = segment.get("cars")[n]
            sprite = car.get("sprite")
            car["percent"] = Util.percent_remaining(car.get("z"), self.segmentLength)

            sprite_scale = Util.interpolate(segment.get("p1").get("screen").get("scale"),
                                            segment.get("p2").get("screen").get("scale"), car.get("percent"))

            sprite_x = Util.interpolate(segment.get("p1").get("screen").get("x"),
                                        segment.get("p2").get("screen").get("x"), car.get("percent")) + (
                               sprite_scale * car.get("offset") * self.roadWidth * (self.width / 2))

            sprite_y = Util.interpolate(segment.get("p1").get("screen").get("y"),
                                        segment.get("p2").get("screen").get("y"), car.get("percent"))

            Util.sprite(self.screen, self.width, self.roadWidth, sprite, sprite_scale, sprite_x,
                        sprite_y, -0.5, -1, segment.get("clip"))

    def update_cars(self, dt, playersegment, playerw):
        for n in range(len(self.cars)):
            car = self.cars[n]
            oldsegment = self.findSegment(car.get("z"))
            if self.update_car_offset(car, oldsegment, playersegment, playerw) is None:
                hel = 0
            else:
                hel = self.update_car_offset(car, oldsegment, playersegment, playerw)
            car["offset"] = car.get("offset") + hel
            car["z"] = Util.increase(car.get("z"), dt * car.get("speed"), self.trackLength)
            car["percent"] = Util.percent_remaining(car.get("z"), self.segmentLength)
            newsegment = self.findSegment(car.get("z"))
            if oldsegment != newsegment:
                index = oldsegment.get("cars").index(car)
                del oldsegment["cars"][index:1]
                newsegment.get("cars").append(car)

    def update_car_offset(self, car, carsegment, playersegment, playerw):
        lookahead = 20
        carw = car.get("sprite").get("width") * ((1 / 80) * 0.3)

        if (carsegment.get("index") - playersegment.get("index")) > self.drawDistance:
            return 0
        for i in range(1, lookahead):
            segment = self.segments[(carsegment.get("index") + i) % len(self.segments)]

            if (segment == playersegment) and (car.get("speed") > self.speed) and (
                    Util.overlap(self.playerX, playerw, car.get("offset"), carw, 1.2)):
                if self.playerX > 0.5:
                    direction = -1
                elif self.playerX < -0.5:
                    direction = 1
                else:
                    if car.get("offset") > self.playerX:
                        direction = 1
                    else:
                        direction = -1
                return direction * 1 / i * (car.get("speed") - self.speed) / self.maxSpeed

            for n in range(len(segment.get("cars"))):
                other_car = segment.get("cars")[n]
                other_car_w = other_car.get("sprite").get("width") * ((1 / 80) * 0.3)
                if (car.get("speed") > other_car.get("speed")) and Util.overlap(car.get("offset"), carw,
                                                                                other_car.get("offset"), other_car_w,
                                                                                1.2):
                    if other_car.get("offset") > 0.5:
                        direction = -1
                    elif other_car.get("offset") < -0.5:
                        direction = 1
                    else:
                        if car.get("offset") > car.get("offset"):
                            direction = 1
                        else:
                            direction = -1
                    return direction * 1 / i * (car.get("speed") - other_car.get("speed")) / self.maxSpeed

    def add_sprite(self, n, sprite, offset):
        self.segments[n]["sprites"].append({"source": sprite, "offset": offset})

    def reset_sprites(self):
        for n in range(0, len(self.segments), 100):
            self.add_sprite(n, Sprite.random_tree(), 1)
            self.add_sprite(n, Sprite.random_tree(), -1)


    def render_sprites(self, segment):
        for n in range(len(segment.get("sprites"))):
            sprite = segment.get("sprites")[n]
            sprite_scale = segment.get("p1").get("screen").get("scale")
            sprite_x = segment.get("p1").get("screen").get("x") + (
                        sprite_scale * sprite.get("offset") * self.roadWidth * self.width / 2)
            sprite_y = segment.get("p1").get("screen").get("y")
            if sprite.get("offset") < 0:
                offset = -1
            else:
                offset = 0
            Util.sprite(self.screen, self.width, self.roadWidth, sprite.get("source"), sprite_scale, sprite_x, sprite_y,
                        offset, -1, segment.get("clip"))

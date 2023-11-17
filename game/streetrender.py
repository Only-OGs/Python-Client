import math

import pygame, sys

from game.Util import Util


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
    segment_count = 200
    playerX = 1
    playerZ = (cameraHeight * cameraDepth)
    fogDensity = 5
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

    dt = 1/30

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.reset_road()
        self.game_loop()

    def game_loop(self):
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

    def update(self, dt):
        self.position = Util.increase(self.position, dt * self.speed, self.trackLength)

        dx = dt * 2 * (self.speed / self.maxSpeed)

        if self.keyLeft:
            self.playerX = self.playerX - dx
        elif self.keyRight:
            self.playerX = self.playerX + dx

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

    def reset_road(self):
        self.segments = []
        self.segments.append(
            {
                'index': 0,
                'p1':
                    {'world': {
                        'x': None,
                        'y': None,
                        'z': 0 * self.segmentLength
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
                        'z': (0 + 1) * self.segmentLength
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
                'color': (0, 255, 0)
            })

        for n in range(1, self.segment_count):

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

        self.trackLength = len(self.segments) * self.segmentLength

    def _road_color(self, n):
        if math.floor(n / self.rumbleLength) % 2 == 0:
            return 255, 255, 255
        else:
            return 107, 107, 107

    def findSegment(self, z):
        return self.segments[math.floor(z / self.segmentLength) % self.segmentLength]

    def render(self):
        basesegment = self.findSegment(self.position)
        maxy = self.height

        self.screen.fill((20, 21, 40))

        for n in range(self.drawDistance):
            segment = self.segments[(basesegment.get("index") + n) % len(self.segments)]
            segment_looped = segment.get("index") < basesegment.get("index")

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

            if (segment.get("p1").get("camera").get("z") <= self.cameraDepth) or (segment.get("p2").get("screen").get("y") >= maxy):
                continue
            else:
                Util.segment(self.screen, self.width, self.lanes,
                             segment.get("p1").get("screen").get("x"),
                             segment.get("p1").get("screen").get("y"),
                             segment.get("p1").get("screen").get("w"),
                             segment.get("p2").get("screen").get("x"),
                             segment.get("p2").get("screen").get("y"),
                             segment.get("p2").get("screen").get("w"),
                             segment.get("color"))

            maxy = segment.get("p2").get("screen").get("y")

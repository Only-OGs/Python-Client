import pygame
import sys
import rendering.globals_vars as var

from rendering.utility.car_ai import Cars
from rendering.utility.road import Road
from rendering.utility.util import Util
from rendering.utility.sprite_generator import SpriteGen
from rendering.utility.render import Render


class Game:

    def __init__(self):
        var.clock = pygame.time.Clock()
        var.screen = pygame.display.set_mode((var.width, var.height))
        var.player_sprite_group = pygame.sprite.Group()
        var.background_sprite_group = pygame.sprite.Group()
        Road.create_road()
        self.game_loop()

    # main loop wo alles passiert
    def game_loop(self):
        SpriteGen.create_player()
        SpriteGen.create_background()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        var.keyLeft = True
                    if event.key == pygame.K_RIGHT:
                        var.keyRight = True
                    if event.key == pygame.K_UP:
                        var.keyFaster = True
                    if event.key == pygame.K_DOWN:
                        var.keySlower = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        var.keyLeft = False
                    if event.key == pygame.K_RIGHT:
                        var.keyRight = False
                    if event.key == pygame.K_UP:
                        var.keyFaster = False
                    if event.key == pygame.K_DOWN:
                        var.keySlower = False

            Render.render()
            self.update(var.step)
            pygame.display.update()
            var.clock.tick(var.fps)

    # unser KeyInputHandler, hier werden die Keyinputs überprüft und das auto dementsprechend bewegt
    def update(self, dt):
        playersegment = Util.findSegment(var.position + var.playerZ)
        speedpercent = var.speed / var.maxSpeed
        var.position = Util.increase(var.position, dt * var.speed, var.trackLength)

        dx = dt * 2 * speedpercent

        if var.keyLeft:
            var.playerX = var.playerX - dx
            if var.speed > 0:
                var.player.drive_left()
        elif var.keyRight:
            var.playerX = var.playerX + dx
            if var.speed > 0:
                var.player.drive_right()
        else:
            var.player.drive_straight()

        var.playerX = var.playerX - (dx * speedpercent * playersegment.get("curve") * var.centrifugal)

        if var.keyFaster:
            var.speed = Util.accelerate(var.speed, var.accel, var.dt)
        elif var.keySlower:
            var.speed = Util.accelerate(var.speed, var.breaking, var.dt)
        else:
            var.speed = Util.accelerate(var.speed, var.decel, var.dt)

        if (var.playerX < -1 or var.playerX > 1) and (var.speed > var.offRoadLimit):
            var.speed = Util.accelerate(var.speed, var.offRoadDecel, var.dt)

        var.playerX = Util.limit(var.playerX, -2, 2)
        var.speed = Util.limit(var.speed, 0, var.maxSpeed)

        # car here
        playerw = ((1 / 80) * 0.3) * 80

        Cars.update_cars(dt, playersegment, playerw)

import pygame
import sys
import rendering.globals_vars as var
from rendering.utility.car_ai import Cars
from rendering.utility.road import Road
from rendering.utility.util import Util
from menu import screens, gui
from rendering.utility.sprite_generator import SpriteGen
from rendering.utility.render import Render
from menu.sounds import sounds


class Game:

    def __init__(self):
        var.screen = pygame.display.set_mode((var.width, var.height))
        var.player_sprite_group = pygame.sprite.Group()
        var.background_sprite_group = pygame.sprite.Group()
        Road.create_road()
        if not var.singleplayer:
            var.client.client_is_ingame()
        while var.help_car is not True and not var.singleplayer:
            pass
        var.paused = False
        self.game_loop()
        self.timer_rest = False

    # main loop wo alles passiert
    def game_loop(self):
        var.play_music = False
        SpriteGen.create_player()
        SpriteGen.create_background()
        timer = gui.Gui(screen=var.screen)
        var.play_music = False
        sounds.pause_music()

        while True:
            if var.escape:
                break
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        var.escape = True
                        break
                    if event.key == pygame.K_p:
                        self.toggle_pause()


                # Verhindert eingaben des Spielers, während des Countdowns
                if not var.game_start or not var.singleplayer_start:
                    break
                else:
                    if not var.race_finished:
                        if var.gameStart or var.singleplayer:
                            if event.type == pygame.KEYDOWN:
                                if not var.paused:
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
            timer.show_speed(speed=var.speed)

            if var.paused:
                screens.Screens.create_pause_menu(var.screen)

            if not var.singleplayer_start:
                screens.Screens.create_countdown_singleplayer(var.screen)
                var.game_counter += 1

            elif var.client.sio.connected and not var.game_start:
                screens.Screens.create_countdown_multiplayer(var.screen)
            elif var.game_start or var.singleplayer_start:
                timer.count_up()

                if not var.client.sio.connected:

                    if (var.position < 10000 and var.position > 1000):
                        self.timer_rest = True


                    if (var.position >= var.trackLength - 1000):
                        if (self.timer_rest):
                            self.timer_rest = False
                            timer.ende_timer()
                            var.lap_count += 1

            # In Round() länge der Strecke einsetzten

            if var.game_end:
                screens.Screens.create_leaderboard()

            if int(var.clock.get_fps()) == 0:
                fps_help = 1
            else:
                fps_help = 0



            self.update(min(1 / int(var.clock.get_fps() + fps_help), 60))

            pygame.display.update()
            var.clock.tick(var.fps)

        if var.escape:
            if not var.singleplayer:
                var.client.game_leave()
            var.menu_state = "main_menu"
            screens.Screens.screen_update()
            var.position = 0
            var.keyFaster = False
            var.speed = 0
            var.game_start = False
            var.game_counter = 0
            var.escape = False
            var.track = None
            var.singleplayer = True
            var.leaderboard = None
            var.game_end = False
            var.client.lobbymessage = ''
            var.singleplayer_start = False
            var.lap_count = 1
            var.playerX = 0
            var.client.chat_message.clear()
            var.client.chat_player.clear()
            var.client.time = ""
            var.race_finished = False
            var.play_music = True
            var.connection_lost = False

    def toggle_pause(self):
        var.paused = not var.paused
        var.keyFaster = not var.paused

    # unser KeyInputHandler, hier werden die Keyinputs überprüft und das auto dementsprechend bewegt
    def update(self, dt):
        playersegment = Util.findSegment(var.position + var.playerZ)
        speedpercent = var.speed / var.maxSpeed
        var.position = Util.increase(var.position, dt * var.speed, var.trackLength)
        playerw = 80 * (0.3 * (1 / 80))
        dx = dt * 2 * speedpercent
        var.sky_offset = Util.increase(var.sky_offset, var.skySpeed*playersegment.get('curve')*speedpercent, 1)
        var.hill_offset = Util.increase(var.hill_offset, var.hillSpeed*playersegment.get('curve')*speedpercent, 1)
        var.tree_offset = Util.increase(var.tree_offset, var.treeSpeed * playersegment.get('curve') * speedpercent, 1)

        if var.keyLeft:
            var.playerX = var.playerX - dx
        elif var.keyRight:
            var.playerX = var.playerX + dx

        var.playerX = var.playerX - (dx * speedpercent * playersegment.get("curve") * var.centrifugal)

        if var.keyFaster:
            var.speed = Util.accelerate(var.speed, var.accel, var.dt)
        elif var.keySlower:
            var.speed = Util.accelerate(var.speed, var.breaking, var.dt)
        else:
            var.speed = Util.accelerate(var.speed, var.decel, var.dt)

        if (var.playerX < -1 or var.playerX > 1) and (var.speed > var.offRoadLimit):
            var.speed = Util.accelerate(var.speed, var.offRoadDecel, var.dt)

        if var.playerX < -1 or var.playerX > 1:

            if var.speed > var.offRoadLimit:
                var.speed = Util.accelerate(var.speed, var.offRoadDecel, var.dt)

            for n in range(len(playersegment.get("sprites"))):
                sprite = playersegment.get("sprites")[n]
                if sprite is not None:
                    sprite_w = sprite.get("source").get("width") * (0.3 * (1 / 80))
                    if sprite.get("offset") > 0:
                        h = 1
                    else:
                        h = 0
                    if Util.overlap(var.playerX, playerw, sprite.get("offset") + sprite_w / 2 * h, sprite_w):
                        var.speed = var.maxSpeed / 5
                        var.position = Util.increase(playersegment.get("p1").get("world").get("z"), -var.playerZ,
                                                     var.trackLength)
                        break

        for car in (playersegment.get("cars")):
            car_w = car.get("sprite").get("width") * (0.3 * (1 / 80))
            if var.speed > car.get("speed"):
                if Util.overlap(var.playerX, playerw, car.get("offset"), car_w, 0.8):
                    if 'player' in car.keys():
                        player_knockback = -200
                    else:
                        player_knockback = 0
                    var.speed = car.get("speed") * (car.get("speed") / var.speed)
                    var.position = Util.increase(car.get("z"), -var.playerZ, var.trackLength)
                    var.position += player_knockback
                    break

        var.playerX = Util.limit(var.playerX, -2, 2)
        var.speed = Util.limit(var.speed, 0, var.maxSpeed)

        # car here
        playerw = ((1 / 80) * 0.3) * 80
        Cars.update_cars(dt, playersegment, playerw)
        if var.singleplayer is False:
            var.client.ingame_pos(var.position, var.playerX)

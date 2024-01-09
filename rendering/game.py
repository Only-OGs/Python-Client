import pygame
import sys
import rendering.game_vars as game_var
import globals_vars as global_var
from rendering.utility.car_ai import Cars
from rendering.utility.road import Road
from rendering.utility.util import Util
from menu import screens, hud
from rendering.utility.sprite_generator import SpriteGen
from rendering.utility.render import Render

paused = False


class Game:

    def __init__(self):
        game_var.screen = pygame.display.set_mode((global_var.width, global_var.height))
        game_var.player_sprite_group = pygame.sprite.Group()
        game_var.background_sprite_group = pygame.sprite.Group()
        Road.create_road()
        if not global_var.singleplayer:
            global_var.client.client_is_ingame()

        game_var.paused = False
        self.game_loop()
        self.timer_rest = False

    # main loop wo alles passiert
    def game_loop(self):
        global_var.play_music = False
        SpriteGen.create_player()
        SpriteGen.create_background()
        timer = hud.Hud(screen=game_var.screen)
        global_var.play_music = False

        while True:
            if game_var.escape:
                break
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_var.escape = True
                        break
                    if event.key == pygame.K_p:
                        self.toggle_pause()

                # Verhindert eingaben des Spielers, während des Countdowns
                if not global_var.game_start or not global_var.singleplayer_start:
                    break
                else:
                    if not global_var.race_finished:
                        if game_var.gameStart or global_var.singleplayer:
                            if event.type == pygame.KEYDOWN:
                                if not game_var.paused:
                                    if event.key == pygame.K_LEFT:
                                        global_var.keyLeft = True
                                    if event.key == pygame.K_RIGHT:
                                        global_var.keyRight = True
                                    if event.key == pygame.K_UP:
                                        global_var.keyFaster = True
                                    if event.key == pygame.K_DOWN:
                                        global_var.keySlower = True
                            if event.type == pygame.KEYUP:
                                if event.key == pygame.K_LEFT:
                                    global_var.keyLeft = False
                                if event.key == pygame.K_RIGHT:
                                    global_var.keyRight = False
                                if event.key == pygame.K_UP:
                                    global_var.keyFaster = False
                                if event.key == pygame.K_DOWN:
                                    global_var.keySlower = False

            Render.render()
            timer.show_speed(speed=game_var.speed)

            if game_var.paused:
                screens.Screens.create_pause_menu(game_var.screen)
            if not global_var.singleplayer_start:
                screens.Screens.create_countdown_singleplayer(game_var.screen)
                global_var.game_counter += 1
            elif global_var.client.sio.connected and not global_var.game_start:
                screens.Screens.create_countdown_multiplayer(game_var.screen)
            elif global_var.game_start or global_var.singleplayer_start:
                timer.count_up()

                if not global_var.client.sio.connected:

                    if (game_var.position < 10000 and game_var.position > 1000):
                        self.timer_rest = True

                    if (game_var.position >= game_var.trackLength - 1000):
                        if (self.timer_rest):
                            self.timer_rest = False
                            timer.ende_timer()
                            global_var.lap_count += 1

            # In Round() länge der Strecke einsetzten

            if global_var.game_end:
                screens.Screens.create_leaderboard()

            if int(global_var.clock.get_fps()) == 0:
                fps_help = 1
            else:
                fps_help = 0

            self.update(min(1 / int(global_var.clock.get_fps() + fps_help), 60))

            pygame.display.update()
            global_var.clock.tick(global_var.fps)

        if game_var.escape:
            self.return_by_escape()

    def return_by_escape(self):
        if not global_var.singleplayer:
            global_var.client.game_leave()
        global_var.menu_state = "main_menu"
        screens.Screens.screen_update()
        game_var.position = 0
        global_var.keyFaster = False
        game_var.speed = 0
        global_var.game_start = False
        global_var.game_counter = 0
        game_var.escape = False
        game_var.track = None
        global_var.singleplayer = True
        global_var.client.leaderboard = None
        global_var.game_end = False
        global_var.client.lobbymessage = ''
        global_var.singleplayer_start = False
        global_var.lap_count = 1
        game_var.playerX = 0
        global_var.client.chat_message.clear()
        global_var.client.chat_player.clear()
        global_var.client.time = ""
        global_var.race_finished = False
        global_var.play_music = True
        global_var.client.is_ready = False
        game_var.cars.clear()
        global_var.player_cars.clear()
        game_var.segments.clear()
        game_var.lap = ""

    def toggle_pause(self):
        game_var.paused = not game_var.paused
        global_var.keyFaster = not game_var.paused

    # unser KeyInputHandler, hier werden die Keyinputs überprüft und das auto dementsprechend bewegt
    def update(self, dt):
        playersegment = Util.findSegment(game_var.position + game_var.playerZ)
        speedpercent = game_var.speed / game_var.maxSpeed
        game_var.position = Util.increase(game_var.position, dt * game_var.speed, game_var.trackLength)
        playerw = 80 * (0.3 * (1 / 80))
        dx = dt * 2 * speedpercent
        game_var.sky_offset = Util.increase(game_var.sky_offset,
                                            game_var.skySpeed * playersegment.get('curve') * speedpercent, 1)
        game_var.hill_offset = Util.increase(game_var.hill_offset,
                                             game_var.hillSpeed * playersegment.get('curve') * speedpercent, 1)
        game_var.tree_offset = Util.increase(game_var.tree_offset,
                                             game_var.treeSpeed * playersegment.get('curve') * speedpercent, 1)

        if global_var.keyLeft:
            game_var.playerX = game_var.playerX - dx
        elif global_var.keyRight:
            game_var.playerX = game_var.playerX + dx

        game_var.playerX = game_var.playerX - (dx * speedpercent * playersegment.get("curve") * game_var.centrifugal)

        if global_var.keyFaster:
            game_var.speed = Util.accelerate(game_var.speed, game_var.accel, game_var.dt)
        elif global_var.keySlower:
            game_var.speed = Util.accelerate(game_var.speed, game_var.breaking, game_var.dt)
        else:
            game_var.speed = Util.accelerate(game_var.speed, game_var.decel, game_var.dt)

        if (game_var.playerX < -1 or game_var.playerX > 1) and (game_var.speed > game_var.offRoadLimit):
            game_var.speed = Util.accelerate(game_var.speed, game_var.offRoadDecel, game_var.dt)

        if game_var.playerX < -1 or game_var.playerX > 1:

            if game_var.speed > game_var.offRoadLimit:
                game_var.speed = Util.accelerate(game_var.speed, game_var.offRoadDecel, game_var.dt)

            for n in range(len(playersegment.get("sprites"))):
                sprite = playersegment.get("sprites")[n]
                if sprite is not None:
                    sprite_w = sprite.get("source").get("width") * (0.3 * (1 / 80))
                    if sprite.get("offset") > 0:
                        h = 1
                    else:
                        h = 0
                    if Util.overlap(game_var.playerX, playerw, sprite.get("offset") + sprite_w / 2 * h, sprite_w):
                        game_var.speed = game_var.maxSpeed / 5
                        game_var.position = Util.increase(playersegment.get("p1").get("world").get("z"),
                                                          -game_var.playerZ,
                                                          game_var.trackLength)
                        break

        for car in (playersegment.get("cars")):
            car_w = car.get("sprite").get("width") * (0.3 * (1 / 80))
            if game_var.speed > car.get("speed"):
                if Util.overlap(game_var.playerX, playerw, car.get("offset"), car_w, 0.8):
                    if 'player' in car.keys():
                        player_knockback = -200
                    else:
                        player_knockback = 0
                    game_var.speed = car.get("speed") * (car.get("speed") / game_var.speed)
                    game_var.position = Util.increase(car.get("z"), -game_var.playerZ, game_var.trackLength)
                    game_var.position += player_knockback
                    break

        game_var.playerX = Util.limit(game_var.playerX, -2, 2)
        game_var.speed = Util.limit(game_var.speed, 0, game_var.maxSpeed)

        # car here
        playerw = ((1 / 80) * 0.3) * 80
        Cars.update_cars(dt, playersegment, playerw)
        if global_var.singleplayer is False:
            global_var.client.ingame_pos(game_var.playerZ + game_var.position, game_var.playerX)

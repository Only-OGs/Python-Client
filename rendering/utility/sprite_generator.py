import math
import random
import pygame
import globals_vars as global_var
import rendering.game_vars as game_var

from rendering.sprites.background import Background
from rendering.sprites.player import Player
from rendering.sprites.sprite_data import SpriteData
from rendering.utility.util import Util


class SpriteGen:

    @staticmethod
    def add_sprite(segments, n, sprite, offset):
        """ Hilfsmethode für reset_sprites"""
        segments[n]["sprites"].append({"source": sprite, "offset": offset})

    @staticmethod
    def create_street_objectives(segments):
        """ Erstellt die Objekte am Rande der Straße"""
        for n in range(0, len(segments), 50):
            SpriteGen.add_sprite(segments, n, SpriteData.random_asset(), (random.randint(10, 25)/10))
            SpriteGen.add_sprite(segments, n, SpriteData.random_asset(), (random.randint(10, 25)/-10))

    @staticmethod
    def create_bot_cars():
        """ Erstellt die Auto-Bots anhand der total_cars variable"""
        game_var.cars = []

        for n in range(game_var.total_cars):
            offset = random.random() * Util.random_choice([-0.8, 0.8])
            z = math.floor(random.random() * len(game_var.segments) * game_var.segmentLength)
            sprite = SpriteData.random_car()
            speed = game_var.maxSpeed / 4 + random.random() * game_var.maxSpeed / 2
            car = {"offset": offset, "z": z, "sprite": sprite, "speed": speed, "percent": 0}
            segment = Util.findSegment(z)
            segment["cars"].append(car)
            game_var.cars.append(car)

    @staticmethod
    def create_background():
        """Erstellt die Background Sprites"""
        game_var.bg_sky_mid = Background(pygame.image.load("assets/sky.png"))
        game_var.bg_hills_mid = Background(pygame.image.load("assets/hills.png"))
        game_var.bg_tree_mid = Background(pygame.image.load("assets/trees.png"))


    @staticmethod
    def create_player():
        """ Erstellt den Player Sprite und zentriert ihn"""
        game_var.player = Player(game_var.screen.get_width() / 2 - 30, game_var.screen.get_height() - 100)
        game_var.player_sprite_group.add(game_var.player)

    @staticmethod
    def create_Server_cars():
        """Erstellt Autos die vom Server übergeben werden und der Spieler wird auf seine passende Position gesetzt"""
        for player in global_var.player_cars:
            if player.get("id") != global_var.username:
                segment = Util.findSegment(player.get("pos"))
                car = {"offset": player.get("offset"), "z": player.get("pos"),
                       "sprite": SpriteData.random_car(player.get('asset')), "speed": 0, "percent": 0, "player": True,
                       "id": player.get("id"), "segment": segment}
                if car not in segment.get("cars"):
                    segment["cars"].append(car)
                    game_var.cars.append(car)
            else:
                game_var.position = player.get("pos")
                game_var.playerX = player.get("offset")

    @staticmethod
    def create_server_street_objects():
        """Läd die Assets an der Seite der Straße vom Server"""
        while global_var.trackloaded is False:
            pass
        for n in global_var.assets:
            seg = Util.findSegment(n.get('pos'))
            seg['sprites'].append({"source": SpriteData.random_asset(n.get('model')), "offset": n.get('side')})

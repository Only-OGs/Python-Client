import math
import random
import pygame
import rendering.globals_vars as var

from rendering.sprites.background import Background
from rendering.sprites.player import Player
from rendering.sprites.sprite_data import Sprite
from rendering.utility.util import Util


class SpriteGen:

    @staticmethod
    def add_sprite(segments, n, sprite, offset):
        """ Hilfsmethode für reset_sprites"""
        segments[n]["sprites"].append({"source": sprite, "offset": offset})

    @staticmethod
    def create_street_objectives(segments):
        """ Erstellt die Objekte am Rande der Straße"""
        for n in range(0, len(segments), 100):
            SpriteGen.add_sprite(segments, n, Sprite.random_tree(), 1)
            SpriteGen.add_sprite(segments, n, Sprite.random_billboard(), -1)

    @staticmethod
    def create_bot_cars():
        """ Erstellt die Auto-Bots anhand der total_cars variable"""
        var.cars = []

        for n in range(var.total_cars):
            offset = random.random() * Util.random_choice([-0.8, 0.8])
            z = math.floor(random.random() * len(var.segments) * var.segmentLength)
            sprite = Sprite.random_car()
            speed = var.maxSpeed / 4 + random.random() * var.maxSpeed / 2
            car = {"offset": offset, "z": z, "sprite": sprite, "speed": speed, "percent": 0}
            segment = Util.findSegment(z)
            segment["cars"].append(car)
            var.cars.append(car)

    @staticmethod
    def create_background():
        """Erstellt die Background Sprites"""
        bg_sky = Background(0, pygame.image.load("assets/sky.png"))
        bg_hills = Background(0, pygame.image.load("assets/hills.png"))
        bg_tree = Background(0, pygame.image.load("assets/trees.png"))

        var.background_sprite_group.add(bg_sky)
        var.background_sprite_group.add(bg_hills)
        var.background_sprite_group.add(bg_tree)

    @staticmethod
    def create_player():
        """ Erstellt den Player Sprite und zentriert ihn"""
        var.player = Player(var.screen.get_width() / 2 - 30, var.screen.get_height() - 100)
        var.player_sprite_group.add(var.player)
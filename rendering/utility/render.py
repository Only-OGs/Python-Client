import math

import rendering.globals_vars as var
from rendering.sprites.background import Background
from rendering.utility.util import Util
import pygame

class Render:

    @staticmethod
    def render_sprites(segment):
        """ Rendert Objekte am rande der Straße"""
        for n in range(len(segment.get("sprites"))):
            sprite = segment.get("sprites")[n]
            sprite_scale = segment.get("p1").get("screen").get("scale")
            sprite_x = segment.get("p1").get("screen").get("x") + (
                    sprite_scale * sprite.get("offset") * var.roadWidth * var.width / 2)
            sprite_y = segment.get("p1").get("screen").get("y")
            if sprite.get("offset") < 0:
                offset = -1
            else:
                offset = 0
            Util.sprite(var.screen, var.width, var.roadWidth, sprite.get("source"), sprite_scale, sprite_x, sprite_y,
                        offset, -1, segment.get("clip"))

    @staticmethod
    def render_cars(segment):
        """ Rendert alle Autos"""
        for car in segment.get("cars"):
            sprite = car.get("sprite")
            car["percent"] = Util.percent_remaining(car.get("z"), var.segmentLength)

            sprite_scale = Util.interpolate(segment.get("p1").get("screen").get("scale"),
                                            segment.get("p2").get("screen").get("scale"), car.get("percent"))

            sprite_x = Util.interpolate(segment.get("p1").get("screen").get("x"),
                                        segment.get("p2").get("screen").get("x"), car.get("percent")) + (
                               sprite_scale * car.get("offset") * var.roadWidth * (var.width / 2))

            sprite_y = Util.interpolate(segment.get("p1").get("screen").get("y"),
                                        segment.get("p2").get("screen").get("y"), car.get("percent"))

            Util.sprite(var.screen, var.width, var.roadWidth, sprite, sprite_scale, sprite_x,
                        sprite_y, -0.5, -1, segment.get("clip"))

    @staticmethod
    def render():
        """ Rendert alles mithilfe der Util.segment, Render.render_cars, und Render.render_sprites Methoden"""
        base_segment = Util.findSegment(var.position)
        base_percent = Util.percent_remaining(var.position, var.segmentLength)
        player_segment = Util.findSegment(var.position + var.playerZ)
        player_percent = Util.percent_remaining(var.position + var.playerZ, var.segmentLength)
        player_y = Util.interpolate(player_segment.get("p1").get("world").get("y"),
                                    player_segment.get("p2").get("world").get("y"), player_percent)

        dx = -(base_segment.get("curve") * base_percent)
        x = 0
        maxy = var.height

        Render.render_background()

        for n in range(var.drawDistance):
            segment = var.segments[(base_segment.get("index") + n) % len(var.segments)]
            segment_looped = segment.get("index") < base_segment.get("index")
            segment_fog = Util.exponential_fog(n / var.drawDistance, var.fogDensity)
            segment["clip"] = maxy

            if segment_looped:
                segment_looped_value = var.trackLength
            else:
                segment_looped_value = 0

            segment["p1"] = Util.project(
                segment.get("p1"),
                (var.playerX * var.roadWidth) - x,
                player_y + var.cameraHeight,
                var.position - segment_looped_value,
                var.cameraDepth,
                var.width, var.height,
                var.roadWidth)

            segment["p2"] = Util.project(
                segment.get("p2"),
                (var.playerX * var.roadWidth) - x - dx,
                player_y + var.cameraHeight,
                var.position - segment_looped_value,
                var.cameraDepth,
                var.width, var.height,
                var.roadWidth)

            x = x + dx
            dx = dx + segment.get("curve")

            if (segment.get("p1").get("camera").get("z") <= var.cameraDepth) or (
                    segment.get("p2").get("screen").get("y") >= maxy) or (
                    segment.get("p2").get("screen").get("y") >= segment.get("p1").get("screen").get("y")):
                continue

            Util.segment(var.screen, var.width, var.lanes,
                         segment.get("p1").get("screen").get("x"),
                         segment.get("p1").get("screen").get("y"),
                         segment.get("p1").get("screen").get("w"),
                         segment.get("p2").get("screen").get("x"),
                         segment.get("p2").get("screen").get("y"),
                         segment.get("p2").get("screen").get("w"),
                         segment.get("color"), segment_fog)

            maxy = segment.get("p1").get("screen").get("y")

        for n in range(var.drawDistance - 1, 0, -1):
            segment = var.segments[(base_segment.get("index") + n) % len(var.segments)]
            Render.render_sprites(segment)
            Render.render_cars(segment)

        Render.render_player(player_segment)


    @staticmethod
    def render_background():
        """Methode zum Berechnen und Rendern des Parallax Background"""
        "Die Position des Himmels wird berechnet"
        mid_rect = var.bg_sky_mid.image.get_rect()
        mid_rect.x = mid_rect.x + round(var.sky_offset * 400)
        var.bg_sky_mid.rect = mid_rect
        if mid_rect.x > 0:
            left_rect = var.bg_sky_left.image.get_rect()
            left_rect.topright = (left_rect.top + round(var.sky_offset * 400), 0)
            var.bg_sky_left.rect = left_rect
        if mid_rect.x < 0:
            right_rect = var.bg_sky_right.image.get_rect()
            right_rect.topleft = (right_rect.top + 1280 + round(var.sky_offset * 400), 0)
            var.bg_sky_right.rect = right_rect

        "Die Position der Hügel werden berechnet"
        mid_rect = var.bg_hills_mid.image.get_rect()
        mid_rect.x = mid_rect.x + round(var.hill_offset * 400)
        var.bg_hills_mid.rect = mid_rect
        if mid_rect.x > 0:
            left_rect = var.bg_hills_left.image.get_rect()
            left_rect.topright = (left_rect.top + round(var.hill_offset * 400), 0)
            var.bg_hills_left.rect = left_rect
        if mid_rect.x < 0:
            right_rect = var.bg_hills_right.image.get_rect()
            right_rect.topleft = (right_rect.top + 1280 + round(var.hill_offset * 400), 0)
            var.bg_hills_right.rect = right_rect

        "Die Position der Bäume werden berechnet"
        mid_rect = var.bg_tree_mid.image.get_rect()
        mid_rect.x = mid_rect.x + round(var.tree_offset)
        var.bg_tree_mid.rect = mid_rect
        if mid_rect.x > 0:
            left_rect = var.bg_tree_left.image.get_rect()
            left_rect.topright = (left_rect.top + round(var.tree_offset * 400), 0)
            var.bg_tree_left.rect = left_rect
        if mid_rect.x < 0:
            right_rect = var.bg_tree_right.image.get_rect()
            right_rect.topleft = (right_rect.top + 1280 + round(var.tree_offset * 400), 0)
            var.bg_tree_right.rect = right_rect


        "Alle neu berechneten Background Sprites werden gerendert"
        var.background_sprite_group.draw(var.screen)


    @staticmethod
    def render_player(player_segment):
        uphill = player_segment.get('p2').get('world').get('y') - player_segment.get('p1').get('world').get('y')
        if var.keyLeft:
            if uphill > 0:
                var.player.drive_left(True)
            else:
                var.player.drive_left(False)
        elif var.keyRight:
            if uphill > 0:
                var.player.drive_right(True)
            else:
                var.player.drive_right(False)
        else:
            if uphill > 0:
                var.player.drive_straight(True)
            else:
                var.player.drive_straight(False)
        var.player_sprite_group.draw(var.screen)

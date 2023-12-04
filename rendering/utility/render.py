import rendering.globals_vars as var
from rendering.utility.util import Util


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
        for n in range(len(segment.get("cars"))):
            car = segment.get("cars")[n]
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
        var.background_sprite_group.draw(var.screen)

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
        var.player_sprite_group.draw(var.screen)

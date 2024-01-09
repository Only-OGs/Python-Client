import rendering.game_vars as game_var
import globals_vars as global_var
from rendering.utility.util import Util


class Render:

    @staticmethod
    def render_sprites(segment):
        """ Rendert Objekte am rande der Straße"""
        for n in range(len(segment.get("sprites"))):
            sprite = segment.get("sprites")[n]
            sprite_scale = segment.get("p1").get("screen").get("scale")
            sprite_x = segment.get("p1").get("screen").get("x") + (
                    sprite_scale * sprite.get("offset") * game_var.roadWidth * global_var.width / 2)
            sprite_y = segment.get("p1").get("screen").get("y")
            if sprite.get("offset") < 0:
                offset = -1
            else:
                offset = 0
            Util.sprite(game_var.screen, global_var.width, game_var.roadWidth, sprite.get("source"), sprite_scale, sprite_x, sprite_y,
                        offset, -1, segment.get("clip"))

    @staticmethod
    def render_cars(segment):
        """ Rendert alle Autos"""
        for car in segment.get("cars"):
            sprite = car.get("sprite")
            car["percent"] = Util.percent_remaining(car.get("z"), game_var.segmentLength)

            sprite_scale = Util.interpolate(segment.get("p1").get("screen").get("scale"),
                                            segment.get("p2").get("screen").get("scale"), car.get("percent"))

            sprite_x = Util.interpolate(segment.get("p1").get("screen").get("x"),
                                        segment.get("p2").get("screen").get("x"), car.get("percent")) + (
                               sprite_scale * car.get("offset") * game_var.roadWidth * (global_var.width / 2))

            sprite_y = Util.interpolate(segment.get("p1").get("screen").get("y"),
                                        segment.get("p2").get("screen").get("y"), car.get("percent"))

            Util.sprite(game_var.screen, global_var.width, game_var.roadWidth, sprite, sprite_scale, sprite_x,
                        sprite_y, -0.5, -1, segment.get("clip"))

    @staticmethod
    def render():
        """ Rendert alles mithilfe der Util.segment, Render.render_cars, und Render.render_sprites Methoden"""
        game_var.screen.fill((0, 0, 0), (0, 0, global_var.width, global_var.height))
        base_segment = Util.findSegment(game_var.position)
        base_percent = Util.percent_remaining(game_var.position, game_var.segmentLength)
        player_segment = Util.findSegment(game_var.position + game_var.playerZ)
        player_percent = Util.percent_remaining(game_var.position + game_var.playerZ, game_var.segmentLength)
        player_y = Util.interpolate(player_segment.get("p1").get("world").get("y"),
                                    player_segment.get("p2").get("world").get("y"), player_percent)

        dx = -(base_segment.get("curve") * base_percent)
        x = 0
        maxy = global_var.height

        Render.render_background(player_y)
        for n in range(game_var.drawDistance):
            segment = game_var.segments[(base_segment.get("index") + n) % len(game_var.segments)]
            segment_looped = segment.get("index") < base_segment.get("index")
            segment_fog = Util.exponential_fog(n / game_var.drawDistance, game_var.fogDensity)
            segment["clip"] = maxy

            if segment_looped:
                segment_looped_value = game_var.trackLength
            else:
                segment_looped_value = 0

            segment["p1"] = Util.project(
                segment.get("p1"),
                (game_var.playerX * game_var.roadWidth) - x,
                player_y + game_var.cameraHeight,
                game_var.position - segment_looped_value,
                game_var.cameraDepth,
                global_var.width, global_var.height,
                game_var.roadWidth)

            segment["p2"] = Util.project(
                segment.get("p2"),
                (game_var.playerX * game_var.roadWidth) - x - dx,
                player_y + game_var.cameraHeight,
                game_var.position - segment_looped_value,
                game_var.cameraDepth,
                global_var.width, global_var.height,
                game_var.roadWidth)

            x = x + dx
            dx = dx + segment.get("curve")

            if (segment.get("p1").get("camera").get("z") <= game_var.cameraDepth) or (
                    segment.get("p2").get("screen").get("y") >= maxy) or (
                    segment.get("p2").get("screen").get("y") >= segment.get("p1").get("screen").get("y")):
                continue

            Util.segment(game_var.screen, global_var.width, game_var.lanes,
                         segment.get("p1").get("screen").get("x"),
                         segment.get("p1").get("screen").get("y"),
                         segment.get("p1").get("screen").get("w"),
                         segment.get("p2").get("screen").get("x"),
                         segment.get("p2").get("screen").get("y"),
                         segment.get("p2").get("screen").get("w"),
                         segment.get("color"), segment_fog)

            maxy = segment.get("p1").get("screen").get("y")

        for n in range(game_var.drawDistance - 1, 0, -1):
            segment = game_var.segments[(base_segment.get("index") + n) % len(game_var.segments)]
            Render.render_sprites(segment)
            Render.render_cars(segment)

        Render.render_player(player_segment)

    @staticmethod
    def render_background(player_y):
        """Methode zum Berechnen und Rendern des Parallax Background"""
        game_var.bg_sky_mid.move(game_var.sky_offset, game_var.screen)
        game_var.bg_hills_mid.move(game_var.hill_offset, game_var.screen)
        game_var.bg_tree_mid.move(game_var.tree_offset, game_var.screen)

        "Alle neu berechneten Background Sprites werden gerendert"
        game_var.background_sprite_group.draw(game_var.screen)

    @staticmethod
    def render_player(player_segment):
        uphill = player_segment.get('p2').get('world').get('y') - player_segment.get('p1').get('world').get('y')
        bounce = (player_segment.get('index') % 3) * 1.5
        if global_var.keyLeft:
            if uphill > 0:
                game_var.player.drive_left(True)
            else:
                game_var.player.drive_left(False)
        elif global_var.keyRight:
            if uphill > 0:
                game_var.player.drive_right(True)
            else:
                game_var.player.drive_right(False)
        else:
            if uphill > 0:
                game_var.player.drive_straight(True)
            else:
                game_var.player.drive_straight(False)
        game_var.player.bounce(bounce)
        game_var.player_sprite_group.draw(game_var.screen)

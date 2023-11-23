import math

import pygame


class Util:

    def __init__(self):
        pass

    @staticmethod
    def increase(start, increment, maximum):

        result = start + increment
        while result >= maximum:
            result -= maximum
        while result < 0:
            result += maximum
        return result

    @staticmethod
    def accelerate(v, accel, dt):
        return v + (accel * dt)

    @staticmethod
    def limit(value, minimum, maximum):
        return max(minimum, min(value, maximum))

    @staticmethod
    def project(p, camx, camy, camz, camdepth, width, height, roadwidth):
        worldx = Util._if_none(p.get("world").get("x"))
        worldy = Util._if_none(p.get("world").get("y"))
        worldz = Util._if_none(p.get("world").get("z"))

        p.get("camera")["x"] = worldx - camx
        p.get("camera")["y"] = worldy - camy
        p.get("camera")["z"] = worldz - camz

        p.get("screen")["scale"] = camdepth / Util._if_zero(p.get("camera").get("z"))

        p.get("screen")["x"] = round(
            (width / 2) + (p.get("screen").get("scale") * p.get("camera").get("x") * width / 2))

        p.get("screen")["y"] = round(
            (height / 2) - (p.get("screen").get("scale") * p.get("camera").get("y") * height / 2))

        p.get("screen")["w"] = round((p.get("screen").get("scale") * roadwidth * width / 2))
        return p

    @staticmethod
    def _if_none(value):
        if value is not None:
            return value
        else:
            return 0

    @staticmethod
    def _if_zero(value):
        if value == 0:
            return 1
        else:
            return value

    @staticmethod
    def segment(screen, width, lanes, x1, y1, w1, x2, y2, w2, color, fog):
        r1 = Util._rumble_width(w1, lanes)
        r2 = Util._rumble_width(w2, lanes)
        l1 = Util._lane_marker_width(w1, lanes)
        l2 = Util._lane_marker_width(w2, lanes)
        lane = 1

        Util.gras(screen, color.get("grass"), 0, y2, width, y1 - y2)

        Util._polygon(screen, x1 - w1 - r1, y1, x1 - w1, y1, x2 - w2, y2, x2 - w2 - r2, y2, color.get("rumble"))
        Util._polygon(screen, x1 + w1 + r1, y1, x1 + w1, y1, x2 + w2, y2, x2 + w2 + r2, y2, color.get("rumble"))
        Util._polygon(screen, x1 - w1, y1, x1 + w1, y1, x2 + w2, y2, x2 - w2, y2, color.get("road"))

        lanew1 = w1 * 2 / lanes
        lanew2 = w2 * 2 / lanes
        lanex1 = x1 - w1 + lanew1
        lanex2 = x2 - w2 + lanew2

        while lane < lanes:
            Util._polygon(screen, lanex1 - l1 / 2, y1, lanex1 + l1 / 2, y1, lanex2 + l2 / 2, y2, lanex2 - l2 / 2,
                          y2,
                          color.get("lane"))
            lanex1 += lanew1
            lanex2 += lanew2
            lane = lane + 1

        Util.fog(screen, 0, y1, width, y1 - y2, fog)

    @staticmethod
    def gras(screen, color, x, y, width, height):
        pygame.draw.polygon(screen, color, [(x, y), (x + width, y), (x + width, y + height), (x, y + height)])

    @staticmethod
    def _rumble_width(projectedroadwidth, lanes):
        return projectedroadwidth / max(6, 2 * lanes)

    @staticmethod
    def _lane_marker_width(projectedroadwidth, lanes):
        return projectedroadwidth / max(32, 8 * lanes)

    @staticmethod
    def _polygon(screen, x1, y1, x2, y2, x3, y3, x4, y4, color):
        pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

    @staticmethod
    def exponential_fog(distance, density):
        return 1 / (math.pow(math.e, (distance * distance * density)))

    @staticmethod
    def fog(screen, x, y, width, height, fog):
        if fog < 1:
            Util.draw_polygon_alpha(screen, (0, 81, 8, int((1 - fog) * 255)),
                                    [(x, y - 1), (x + width, y - 1), (x + width, y + height), (x, y + height)])

    # von https://stackoverflow.com/a/64630102
    @staticmethod
    def draw_polygon_alpha(surface, color, points):
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
        surface.blit(shape_surf, target_rect)

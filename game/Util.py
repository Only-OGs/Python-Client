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
    def segment(screen, width, lanes, x1, y1, w1, x2, y2, w2, color):
        r1 = Util._rumble_width(w1, lanes)
        r2 = Util._rumble_width(w2, lanes)
        l1 = Util._lane_marker_width(w1, lanes)
        l2 = Util._lane_marker_width(w2, lanes)
        lane = 1

        pygame.draw.rect(screen, (16, 170, 16), (0, y2, width, y1-y2)) # rasen

        Util._polygon(screen, x1 - w1 - r1, y1, x1 - w1, y1, x2 - w2, y2, x2 - w2 - r2, y2, (255, 0, 0)) #linker rand
        Util._polygon(screen, x1 + w1 + r1, y1, x1 + w1, y1, x2 + w2, y2, x2 + w2 + r2, y2, (255, 0, 0)) # rechte rand
        Util._polygon(screen, x1 - w1, y1, x1 + w1, y1, x2 + w2, y2, x2 - w2, y2, (107, 107, 107)) # straße

        lanew1 = w1 * 2 / lanes
        lanew2 = w2 * 2 / lanes
        lanex1 = x1 - w1 + lanew1
        lanex2 = x2 - w2 + lanew2

        while lane < lanes:
            Util._polygon(screen, lanex1 - l1 / 2, y1, lanex1 + l1 / 2, y1, lanex2 + l2 / 2, y2, lanex2 - l2 / 2,
                          y2,
                          color)
            lanex1 += lanew1
            lanex2 += lanew2
            lane = lane + 1

    @staticmethod
    def _rumble_width(projectedroadwidth, lanes):
        return projectedroadwidth / max(6, 2 * lanes)

    @staticmethod
    def _lane_marker_width(projectedroadwidth, lanes):
        return projectedroadwidth / max(32, 8 * lanes)

    @staticmethod
    def _polygon(screen, x1, y1, x2, y2, x3, y3, x4, y4, color):
        pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

import json
import math
import rendering.globals_vars as var

from rendering.utility.colors import Color
from rendering.utility.sprite_generator import SpriteGen
from rendering.utility.util import Util


class Road:

    @staticmethod
    def create_road():
        """ Erstellt die Straße, setzt die Bot Autos so wie die Objekte am Straßenrand.
            Erstellt auch die Start- und Finish-Linie
        """
        var.segments = []

        Road.load_road()
        if var.singleplayer:
            SpriteGen.create_bot_cars()
            SpriteGen.create_street_objectives(var.segments)
        else:
            SpriteGen.create_server_street_objects()

        var.segments[Util.findSegment(var.playerZ)["index"] + 2]["color"] = Color.get_start()
        var.segments[Util.findSegment(var.playerZ)["index"] + 3]["color"] = Color.get_start()
        for n in range(var.rumbleLength):
            var.segments[len(var.segments) - 1 - n]["color"] = Color.get_finish()

        var.trackLength = len(var.segments) * var.segmentLength

    @staticmethod
    def add_segment(curve, y):
        """ Generiert die Segmente und fügt sie dem Segments Array hinzu"""
        n = len(var.segments)
        var.segments.append(
            {
                'index': n,
                'p1':
                    {'world': {
                        'x': None,
                        'y': Util.lastY(var.segments),
                        'z': n * var.segmentLength
                    },
                        'camera': {
                            'x': 0,
                            'y': 0,
                            'z': 0
                        },
                        'screen': {
                            "scale": 0,
                            'x': 0,
                            'y': 0,
                        },
                    },
                'p2':
                    {'world': {
                        'x': None,
                        'y': y,
                        'z': (n + 1) * var.segmentLength
                    },
                        'camera': {
                            'x': 0,
                            'y': 0,
                            'z': 0
                        },
                        'screen': {
                            "scale": 0,
                            'x': 0,
                            'y': 0,
                        },
                    },
                "curve": curve,
                "cars": [],
                "clip": 0,
                "sprites": [],
                'color': Road._road_color(n)
            })


    @staticmethod
    def add_road(enter, hold, leave, curve, y=0):
        """ Erstellt einen Straßenabschnitt"""
        starty = Util.lastY(var.segments)
        endy = starty + (int(y) * var.segmentLength)
        total = int(enter) + int(hold) + int(leave)
        for n in range(int(enter)):
            Road.add_segment(Util.easeIn(0, curve, n / enter), Util.easeInOut(starty, endy, n / total))
        for n in range(int(hold)):
            Road.add_segment(curve, Util.easeInOut(starty, endy, (enter + n) / total))
        for n in range(int(leave)):
            Road.add_segment(Util.easeInOut(0, curve, n / enter),
                             Util.easeInOut(starty, endy, (enter + hold + n) / total))

    @staticmethod
    def add_street(num=None, curve=None, height=None):
        """ Übergibt die passenden Parameter für den Straßenabschnitt"""
        if num is None:
            num = 100
        if curve is None:
            curve = 0
        if height is None:
            height = 0

        Road.add_road(num, num, num, curve, height)

    @staticmethod
    def _road_color(n):
        """ Private Methode für die Farbeauswahl auf den Segmenten"""
        if math.floor(n / var.rumbleLength) % 2 == 0:
            return Color.get_light()
        else:
            return Color.get_dark()

    @staticmethod
    def load_road():
        if var.singleplayer:
            with open("road.json", "r") as f:
                data = json.load(f)

            for x in data["road"]:
                if len(x) == 1:
                    Road.add_street(x[0])
                elif len(x) == 2:
                    Road.add_street(x[0], x[1])
                elif len(x) == 3:
                    Road.add_street(x[0], x[1], x[2])
        else:
            for n in var.track:
                Road.add_street(n.get("segment_length"), n.get("curve_strength"), n.get("hill_height"))
            var.trackloaded = True

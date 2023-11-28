import json


class Road:

    @staticmethod
    def lenght():
        road = {
            "none": 0,
            "short": 25,
            "medium": 50,
            "long": 100
        }
        return road

    @staticmethod
    def curve():
        curve = {
            "none": 0,
            "easy": 2,
            "medium": 4,
            "hard": 6
        }
        return curve

    @staticmethod
    def hill():
        hill = {
            "none": 0,
            "low": 20,
            "medium": 40,
            "high": 60
        }
        return hill

    @staticmethod
    def load_road(self):
        with open("road.json", "r") as f:
            data = json.load(f)

        for x in data["road"]:
            if len(x) == 1:
                self.add_street(x[0])
            elif len(x) == 2:
                self.add_street(x[0], x[1])
            elif len(x) == 3:
                self.add_street(x[0], x[1], x[2])

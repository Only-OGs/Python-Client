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

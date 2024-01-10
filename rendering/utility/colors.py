class Color:
    """ Hilfsklasse für die Farben um diese besser zu handeln"""
    @staticmethod
    def get_light():
        c = {
            "road": "#6B6B6B",
            "grass": "#10AA10",
            "rumble": "#555555",
            "lane": "#CCCCCC",
            "fog": "005108"
        }
        return c

    @staticmethod
    def get_dark():
        c = {
            "road": "#696969",
            "grass": "#009A00",
            "rumble": "#BBBBBB",
            "lane": "#696969",
            "fog": "005108"

        }
        return c

    @staticmethod
    def get_start():
        c = {
            "road": "#FFFFFF",
            "grass": "#FFFFFF",
            "rumble": "#FFFFFF",
            "lane": "#FFFFFF",
            "fog": "005108"
        }
        return c

    @staticmethod
    def get_finish():
        c = {
            "road": "#000000",
            "grass": "#000000",
            "rumble": "#000000",
            "lane": "#000000",
            "fog": "005108"
        }
        return c

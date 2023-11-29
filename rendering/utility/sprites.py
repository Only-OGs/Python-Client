import random


class Sprite:

    @staticmethod
    def random_car():
        r = random.randint(0, 3)
        if r == 0:
            data = {"asset": "assets/cars/car01.png", "width": 80, "height": 56}
        elif r == 1:
            data = {"asset": "assets/cars/car02.png", "width": 80, "height": 59}
        elif r == 2:
            data = {"asset": "assets/cars/car03.png", "width": 88, "height": 55}
        elif r == 3:
            data = {"asset": "assets/cars/car04.png", "width": 80, "height": 57}
        else:
            data = {"asset": "assets/cars/car01.png", "width": 80, "height": 56}
        return data

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

    @staticmethod
    def random_tree():
        r = random.randint(0, 2)
        if r == 0:
            data = {"asset": "assets/trees/tree1.png", "width": 360, "height": 360}
        elif r == 1:
            data = {"asset": "assets/trees/palm_tree.png", "width": 215, "height": 540}
        elif r == 2:
            data = {"asset": "assets/trees/tree2.png", "width": 282, "height": 295}
        else:
            data = {"asset": "assets/trees/tree1.png", "width": 360, "height": 360}
        return data
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

    @staticmethod
    def random_billboard():
        r = random.randint(0, 8)
        if r == 0:
            data = {"asset": "assets/billboards/billboard01.png", "width": 300, "height": 170}
        elif r == 1:
            data = {"asset": "assets/billboards/billboard02.png", "width": 215, "height": 220}
        elif r == 2:
            data = {"asset": "assets/billboards/billboard03.png", "width": 230, "height": 220}
        elif r == 3:
            data = {"asset": "assets/billboards/billboard04.png", "width": 268, "height": 170}
        elif r == 4:
            data = {"asset": "assets/billboards/billboard05.png", "width": 298, "height": 190}
        elif r == 5:
            data = {"asset": "assets/billboards/billboard06.png", "width": 298, "height": 190}
        elif r == 6:
            data = {"asset": "assets/billboards/billboard07.png", "width": 298, "height": 190}
        elif r == 7:
            data = {"asset": "assets/billboards/billboard08.png", "width": 385, "height": 265}
        elif r == 8:
            data = {"asset": "assets/billboards/billboard09.png", "width": 328, "height": 282}
        else:
            data = {"asset": "assets/billboards/billboard01.png", "width": 360, "height": 360}
        return data

    @staticmethod
    def test():
        r = random.randint(0, 2)
        if r == 0:
            data = {"asset": "assets/test/test.png", "width": 267, "height": 800}
        elif r == 1:
            data = {"asset": "assets/test/test.png", "width": 267, "height": 800}
        elif r == 2:
            data = {"asset": "assets/test/test.png", "width": 267, "height": 800}
        else:
            data = {"asset": "assets/test/test.png", "width": 267, "height": 800}
        return data

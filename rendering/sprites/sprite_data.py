import random


class Sprite:

    @staticmethod
    def random_car(rand=None):
        if rand is None:
            r = random.randint(0, 5)
        else:
            r = rand-1
        if r == 0:
            data = {"asset": "assets/cars/car01.png", "width": 80, "height": 56}
        elif r == 1:
            data = {"asset": "assets/cars/car02.png", "width": 80, "height": 59}
        elif r == 2:
            data = {"asset": "assets/cars/car03.png", "width": 88, "height": 55}
        elif r == 3:
            data = {"asset": "assets/cars/car04.png", "width": 80, "height": 57}
        elif r == 4:
            data = {"asset": "assets/cars/truck.png", "width": 100, "height": 78}
        elif r == 5:
            data = {"asset": "assets/cars/semi.png", "width": 122, "height": 144}
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
    def random_asset(asset):
        r = asset
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
        elif r == 9:
            data = {"asset": "assets/sprites/boulder01.png", "width": 168, "height": 248}
        elif r == 10:
            data = {"asset": "assets/sprites/boulder02.png", "width": 298, "height": 140}
        elif r == 11:
            data = {"asset": "assets/sprites/boulder03.png", "width": 320, "height": 220}
        elif r == 12:
            data = {"asset": "assets/sprites/bush1.png", "width": 240, "height": 155}
        elif r == 13:
            data = {"asset": "assets/sprites/bush2.png", "width": 232, "height": 152}
        elif r == 14:
            data = {"asset": "assets/sprites/cactus.png", "width": 235, "height": 118}
        elif r == 15:
            data = {"asset": "assets/sprites/dead_tree1.png", "width": 135, "height": 332}
        elif r == 16:
            data = {"asset": "assets/sprites/dead_tree2.png", "width": 150, "height": 260}
        elif r == 17:
            data = {"asset": "assets/sprites/house1.png", "width": 280, "height": 300}
        elif r == 18:
            data = {"asset": "assets/sprites/house2.png", "width": 378, "height": 300}
        elif r == 19:
            data = {"asset": "assets/sprites/house3.png", "width": 439, "height":300}
        elif r == 20:
            data = {"asset": "assets/trees/palm_tree.png", "width": 215, "height": 540}
        elif r == 21:
            data = {"asset": "assets/sprites/stump.png", "width": 195, "height": 140}
        elif r == 22:
            data = {"asset": "assets/trees/tree1.png", "width": 360, "height": 360}
        elif r == 23:
            data = {"asset": "assets/trees/tree2.png", "width": 282, "height": 295}
        else:
            data = {"asset": "assets/trees/tree1.png", "width": 360, "height": 360}
        return data

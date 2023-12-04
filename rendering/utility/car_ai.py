import rendering.globals_vars as var
from rendering.utility.util import Util


class Cars:

    @staticmethod
    def update_cars(dt, playersegment, playerw):
        """ Bewegt die Bot Autos mit ihrer jeweiligen Geschwindigkeit """
        for n in range(len(var.cars)):
            car = var.cars[n]
            oldsegment = Util.findSegment(car.get("z"))
            hel = Cars.update_car_offset(car, oldsegment, playersegment, playerw)
            if hel is None:
                hel = 0
            car["offset"] = car.get("offset") + hel
            car["z"] = Util.increase(car.get("z"), dt * car.get("speed"), var.trackLength)
            car["percent"] = Util.percent_remaining(car.get("z"), var.segmentLength)
            newsegment = Util.findSegment(car.get("z"))
            if oldsegment != newsegment:
                index = oldsegment.get("cars").index(car)
                oldsegment.get("cars").pop(index)
                newsegment.get("cars").append(car)

    @staticmethod
    def update_car_offset(car, carsegment, playersegment, playerw):
        """ Hilft der update_cars Methode um Autos zu umfahren"""
        lookahead = 20
        carw = car.get("sprite").get("width") * ((1 / 80) * 0.3)

        if (carsegment.get("index") - playersegment.get("index")) > var.drawDistance:
            return 0
        for i in range(1, lookahead):
            segment = var.segments[(carsegment.get("index") + i) % len(var.segments)]

            if (segment == playersegment) and (car.get("speed") > var.speed) and (
                    Util.overlap(var.playerX, playerw, car.get("offset"), carw, 1.2)):
                if var.playerX > 0.5:
                    direction = -1
                elif var.playerX < -0.5:
                    direction = 1
                else:
                    if car.get("offset") > var.playerX:
                        direction = 1
                    else:
                        direction = -1
                return direction * 1 / i * (car.get("speed") - var.speed) / var.maxSpeed

            for n in range(len(segment.get("cars"))):
                other_car = segment.get("cars")[n]
                other_car_w = other_car.get("sprite").get("width") * ((1 / 80) * 0.3)
                if (car.get("speed") > other_car.get("speed")) and Util.overlap(car.get("offset"), carw,
                                                                                other_car.get("offset"), other_car_w,
                                                                                1.2):
                    if other_car.get("offset") > 0.5:
                        direction = -1
                    elif other_car.get("offset") < -0.5:
                        direction = 1
                    else:
                        if car.get("offset") > car.get("offset"):
                            direction = 1
                        else:
                            direction = -1
                    return direction * 1 / i * (car.get("speed") - other_car.get("speed")) / var.maxSpeed

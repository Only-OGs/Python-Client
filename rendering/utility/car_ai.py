import globals_vars as var
import rendering.game_vars as game_var

from rendering.utility.util import Util


class Cars:

    @staticmethod
    def update_cars(dt, playersegment, playerw):
        """ Bewegt die Bot Autos mit ihrer jeweiligen Geschwindigkeit """
        for car in game_var.cars:
            oldsegment = Util.findSegment(car.get("z"))
            hel = Cars.update_car_offset(car, oldsegment, playersegment, playerw)
            if hel is None:
                hel = 0
            car["offset"] = car.get("offset") + hel
            car["z"] = Util.increase(car.get("z"), dt * car.get("speed"), game_var.trackLength)
            car["percent"] = Util.percent_remaining(car.get("z"), game_var.segmentLength)
            newsegment = Util.findSegment(car.get("z"))
            try:
                if oldsegment != newsegment:
                    index = oldsegment.get("cars").index(car)
                    oldsegment.get("cars").pop(index)
                    newsegment.get("cars").append(car)
            except ValueError:
                pass

    @staticmethod
    def update_car_offset(car, carsegment, playersegment, playerw):
        """ Hilft der update_cars Methode um Autos zu umfahren"""
        lookahead = 20
        carw = car.get("sprite").get("width") * ((1 / 80) * 0.3)

        if (carsegment.get("index") - playersegment.get("index")) > game_var.drawDistance:
            return 0
        for i in range(1, lookahead):
            segment = game_var.segments[(carsegment.get("index") + i) % len(game_var.segments)]

            if (segment == playersegment) and (car.get("speed") > game_var.speed) and (
                    Util.overlap(game_var.playerX, playerw, car.get("offset"), carw, 1.2)):
                if game_var.playerX > 0.5:
                    direction = -1
                elif game_var.playerX < -0.5:
                    direction = 1
                else:
                    if car.get("offset") > game_var.playerX:
                        direction = 1
                    else:
                        direction = -1
                return direction * 1 / i * (car.get("speed") - game_var.speed) / game_var.maxSpeed


            for other_car in segment.get("cars"):
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
                    return direction * 1 / i * (car.get("speed") - other_car.get("speed")) / game_var.maxSpeed

    @staticmethod
    def update_server_cars():
        """Iteriert durch jedes Auto, welches vom Server kommt, anhand der ID und updated die position wo es steht"""
        for car in game_var.cars:
            oldsegment = car.get("segment")
            for newcar in var.client.new_car_data:
                if car.get("id") == newcar.get("id"):
                    car["offset"] = newcar.get("offset")
                    car["z"] = newcar.get("pos")
                    car["segment"] = Util.findSegment(car.get("z"))
                    break

            newsegment = car.get("segment")
            try:
                if oldsegment != newsegment:
                    index = oldsegment.get("cars").index(car)
                    oldsegment.get("cars").pop(index)
                    newsegment.get("cars").append(car)
            except ValueError:
                pass

    @staticmethod
    def update_player(n):
        """Updated nur für den Spieler wichtige Variablen welche vom Server kommen"""
        var.current_time = n["current_time"]
        var.lap_time = n["lap_time"]
        var.best_time = n["best_time"]
        var.lap = n["lap"]
        var.race_finished = n.get("race_finished")
        if var.race_finished:
            var.keyFaster = False




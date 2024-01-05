import pygame
import rendering.globals_vars as var
'''
Class for the Game HUD
'''
class Gui:

    #init den Timer und die beste Rundenzeit
    def __init__(self, screen):
        self.min = 0
        self.sec = 0
        self.mil_sec = 0

        self.rec_min = 0
        self.rec_sec = 0
        self.rec_mil_sec = 0

        self.last_min = 0
        self.last_sec = 0
        self.last_mil_sec = 0

        self.screen = screen
        #self.Highscore
        self.add = 1
        self.text_offste = 10
        self.first_lab = True

    #Counts up the timer and prints: fastest round, last round and time for single- nad multiplayer
    def count_up(self):
        font = pygame.font.SysFont("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 32)

        # Multiplayer layout
        if var.client.sio.connected:
            text = font.render("schnellste Runde {}".format(var.best_time), True, (var.BLACK))
            text2 = font.render("letzte Runde {}".format(var.lap_time), True, (var.BLACK))
            self.background_gui(x=var.width // 2 - 175, y=0, width=300, color=var.TRANSPARENT_WHITE, length=80)
            self.screen.blit(text, (var.width // 2 - 150, 0 + self.text_offste))
            self.screen.blit(text2, (var.width // 2 - 150, 0 + self.text_offste + 40))

            # schreibt die aktuelle Zeit
            text = font.render("Zeit: {}".format(var.current_time), True,(var.BLACK))
            self.background_gui(x=0, y=0, width=200, color=var.TRANSPARENT_WHITE, length=40)
            self.screen.blit(text, (0, 0 + self.text_offste))


        # Singleplayer layout
        else:

            self.mil_sec += self.add
            if self.mil_sec == 60:
                self.mil_sec = 0
                self.sec += 1

            if self.sec == 60:
                self.mil_sec = 0
                self.sec = 0
                self.min += 1

            if self.min == 60:
                self.mil_sec = 0
                self.sec = 0
                self.min = 0

            text = font.render("schnellste Runde {}:{}:{}".format(self.rec_min, self.rec_sec, self.rec_mil_sec), True, (var.BLACK))
            text2 = font.render("letzte Runde {}:{}:{}".format(self.last_min, self.last_sec, self.last_mil_sec), True,
                               (var.BLACK))
            self.background_gui(x=var.width // 2 - 175, y=0, width=300, color=var.TRANSPARENT_WHITE, length=80)
            self.screen.blit(text, (var.width // 2 - 150, 0 + self.text_offste))
            self.screen.blit(text2, (var.width // 2 - 150, 0 + self.text_offste + 40))

            # Print die den Runden counter
            text = font.render("Time: {}:{}:{}".format(self.min, self.sec, self.mil_sec), True, (var.BLACK))
            self.background_gui(x=0, y=0, width=200, color=var.TRANSPARENT_WHITE, length=40)
            self.screen.blit(text, (0, 0 + self.text_offste))

    #Stops the timer in the singleplayer and sets the fastest round if given
    def ende_timer(self):

        self.last_min = self.min
        self.last_sec = self.sec
        self.last_mil_sec = self.mil_sec

        if (self.first_lab):
            self.first_lab = False
            self.set_new_record()
        if(self.min < self.rec_min):
            self.set_new_record()
        elif(self.sec < self.rec_sec and self.min <= self.rec_min):
            self.set_new_record()
        elif (self.sec <= self.rec_sec and self.min <= self.rec_min and self.mil_sec < self.rec_mil_sec):
            self.set_new_record()

        self.reset_lap()

    def set_new_record(self):
        self.rec_min = self.min
        self.rec_sec = self.sec
        self.rec_mil_sec = self.mil_sec

    def show_speed(self, speed):
        font = pygame.font.SysFont("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 32)
        text = font.render("{} kmh".format(round(speed/100)), True, (var.BLACK))
        if var.client.sio.connected:
            textRunde = font.render("Runde: {}".format(var.lap), True, (var.BLACK))
        else:
            textRunde = font.render("Runde: {}".format(var.lap_count), True, (var.BLACK))
        self.background_gui(x=var.width-150, y=0, width=150,color=var.TRANSPARENT_WHITE, length=80)
        self.screen.blit(text, (var.width-150, self.text_offste))
        self.screen.blit(textRunde, (var.width - 150, self.text_offste + 40))

    def background_gui(self, x, y, width, color, length):
        rect = pygame.rect.Rect(x, y, width, length)
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        self.screen.blit(shape_surf, rect)

    def reset_lap(self):
        self.min = 0
        self.sec = 0
        self.mil_sec = 0


import pygame
import rendering.globals_vars as var
from rendering import game
import sys
import pygame_gui

import time


'''
In dieser Class, wird das gesamte GUI erstellt.
Sämtliche Anzeigen werden pro X Framerate mal in der Sekunde ausgegeben.
Im folgenden Frame werden alle Elemente mit einem Rechteck übermalt,
um im Anschluss wieder gezeichnet zu werden.
'''


class Gui:

    #init den Timer und die beste Rundenzeit
    def __init__(self, screen,x ,y):
        self.min = 0
        self.sec = 0
        self.mil_sec = 0

        self.rec_min = 0
        self.rec_sec = 0
        self.rec_mil_sec = 0

        self.finish = False
        self.screen = screen
        self.x = x
        self.y = y
        self.finish = True
        #self.Highscore
        self.add = 1
        self.text_offste = 10
        self.first_lab = True

    #Zählt den Timer hoch, muss im Game-Loop aufgerufen werden
    def count_up(self):
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

        font = pygame.font.SysFont("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 32)
        text = font.render("schnellste Runde {}:{}:{}".format(self.rec_min, self.rec_sec, self.rec_mil_sec), True,
                           (var.VIOLETTE))
        self.update_gui(x=1024 // 2 - 175, y=self.y, width=300)
        self.screen.blit(text, (1024 // 2 - 150, self.y + self.text_offste))


        font = pygame.font.SysFont("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 32)
        text = font.render("Time: {}:{}:{}".format(self.min, self.sec, self.mil_sec), True, (var.VIOLETTE))
        self.update_gui(x=self.x, y=self.y, width=150)
        self.screen.blit(text, (self.x, self.y + self.text_offste))

    #Beendet den Timer und setzt die neue bestzeit
    def ende_timer(self):
            if (self.first_lab):
                self.first_lab = False
                self.set_new_record()

            if(self.min < self.rec_min):
                self.set_new_record()

            elif(self.sec < self.rec_sec and self.min < self.rec_min):
                self.set_new_record()

            elif (self.sec < self.rec_sec and self.min < self.rec_min and self.mil_sec < self.rec_mil_sec):
                self.set_new_record()

            self.reset_lap()

    #Setzt den neuen Record
    def set_new_record(self):
        self.rec_min = self.min
        self.rec_sec = self.sec
        self.rec_mil_sec = self.mil_sec

    #Zeigt dem Spieler seine Gewschwindigkeit
    def show_speed(self, speed):
        font = pygame.font.SysFont("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 32)

        text = font.render("{} kmh".format(round(speed/60)), True, (var.VIOLETTE))
        self.update_gui(x=self.x + 900, y=self.y, width=150)
        self.screen.blit(text, (self.x + 900, self.y + self.text_offste))

    #Übermalt die Alten GUI elemente damit diese sich nicht Stacken.
    def update_gui(self,x, y, width):
        cover_old_frame = pygame.rect.Rect(x, y, width, 40)
        pygame.draw.rect(self.screen ,(var.DARKBLUE), cover_old_frame)

    def reset_lap(self):
        self.min = 0
        self.sec = 0
        self.mil_sec = 0

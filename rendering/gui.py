import pygame
from rendering import game
import sys
import pygame_gui

class Gui:
    def __init__(self, screen,x ,y):
        self.min = 0
        self.sec = 0
        self.mil_sec = 0

        self.new_min = 0
        self.new_sec = 0
        self.new_mil_sec = 0

        self.finish = False
        self.screen = screen
        self.x = x
        self.y = y
        self.finish = True
        #self.Highscore
        self.add = 1

        font = pygame.font.SysFont("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 32)
        text = font.render("schnellste Runde {}:{}:{}".format(self.new_min, self.new_sec, self.new_mil_sec), True, ("VIOLETTE"),
                           ("DARKBLUE"))
        self.screen.blit(text, (1024//2-150, self.y))
        pygame.display.update()

    def start_timer(self):
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
        text = font.render("Time: {}:{}:{}".format(self.min, self.sec, self.mil_sec), True, ("VIOLETTE"),("DARKBLUE"))
        self.screen.blit(text, (self.x, self.y))
        pygame.display.update()

    def ende_timer(self):
            if(self.min < self.new_min):
                self.set_new_record()
            if(self.sec < self.new_sec and self.min < self.new_min):
                self.set_new_record()

    def set_new_record(self):
        self.new_min = self.min
        self.new_sec = self.new_sec
        self.new_mil_sec = self.new_mil_sec

    def show_speed(self, speed):
        font = pygame.font.SysFont("assets/rocket-rinder-font/RocketRinder-yV5d.ttf", 32)
        text = font.render("{} kmh".format(round(speed/60)), True, ("VIOLETTE"),
                           ("DARKBLUE"))
        self.screen.blit(text, (self.x + 940, self.y))
        pygame.display.update()


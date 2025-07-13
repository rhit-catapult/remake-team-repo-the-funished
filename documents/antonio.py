import pygame
import sys
import time
import random
class Camper:
    def __init__(self, screen, x, y, with_umbrella_filename, without_umbrella_filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.speed = 5
    def move(self):
        self.x = self.x + self.speed
        self.y = self.y + self.speed
    def draw(self):
        
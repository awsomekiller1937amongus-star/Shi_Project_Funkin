from settings import *
import pygame as pg

# class
class Map:
    def __init__(self, filename):
        # creates an empty list for map data
        self.data = []
        # open a specific file and close with 'with'
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        #  Properties of Map that allows us to define length and width
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * 32
        self.height = self.tileheight * 32

class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        self.time = time
    def start(self):
        # when this class is called to start it uses our time feature that we already have to count up
        self.start_time = pg.time.get_ticks()
    def ready(self):
        # checks if current time - self.start_time is greater than or equal to self.time
        current_time = pg.time.get_ticks()
        if current_time - self.start_time >= self.time:
            return True
        return False
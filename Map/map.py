from pico2d import *
from res.map import *

class Map:
    def __init__(self):
        self.image = load_image('./res/map/map.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(600, 400)
        # self.image.draw(1200, 30)

    def get_bb(self):
        # fill here
        # return 0, 0, 1600-1, 50
        pass


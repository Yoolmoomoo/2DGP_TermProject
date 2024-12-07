from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('./res/map/map.png')
        self.bgm = load_music('./res/sound/battle.mp3')
        self.luffy_coma = load_image('./res/luffy/luffy_coma.png')
        self.naruto_coma = load_image('./res/naruto/naruto_coma.png')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.image.draw(600, 400)
        self.luffy_coma.draw(462, 750, 80, 80)
        self.naruto_coma.draw(638, 750, 80, 80)
        # self.image.draw(1200, 30)

    def get_bb(self):
        # fill here
        return [(0, 0, 1200, 114)]

    def handle_collision(self, group, other):
        pass


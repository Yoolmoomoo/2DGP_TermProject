from sys import platlibdir

from pico2d import *
import play_mode

class Map:
    def __init__(self):
        self.image = load_image('./res/map/map.png')
        self.luffy_coma = load_image('./res/luffy/luffy_coma.png')
        self.naruto_coma = load_image('./res/naruto/naruto_coma.png')
        self.bgm = load_music('./res/sound/battle.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()
        self.state = 'None'

    def update(self):
        if play_mode.win_flag == 1:
            self.bgm.stop()
            self.win_sound = load_music('./res/sound/win.mp3')
            self.win_sound.set_volume(32)
            self.win_sound.play()
            play_mode.win_flag = 0
        pass

    def draw(self):
        self.image.draw(500, 350)
        self.luffy_coma.draw(get_canvas_width()/2-45, get_canvas_height()-60, 80, 80)
        self.naruto_coma.draw(get_canvas_width()/2+45, get_canvas_height()-60, 80, 80)
        # self.image.draw(1200, 30)

    def get_bb(self):
        # fill here
        return [(0, 0, 1200, 114)]

    def handle_collision(self, group, other):
        pass

class Ground:
    def __init__(self, x):
        self.x = x
        self.y = 35
        self.ground = load_image('./res/map/ground.png')

    def update(self):
        pass

    def draw(self):
        self.ground.draw(self.x, self.y, 130, 250)
        # self.image.draw(1200, 30)

    def get_bb(self):
        # fill here
        pass

    def handle_collision(self, group, other):
        pass
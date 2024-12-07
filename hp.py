from pico2d import *


class Hp:
  def __init__(self, x, obj_hp):
    self.x = x
    self.y = get_canvas_height() - 80
    self.bar_bg = load_image('./res/ui/hp_bar_bg.png')
    self.bar_fg = load_image('./res/ui/hp_bar_fg.png')
    self.bar_bg.opacify(0.5)
    self.bar_fg.opacify(1.0)
    self.max_hp = 400
    self.current_hp = obj_hp


  def draw(self, hp = 400, left_flag = False):
    self.bar_bg.clip_draw_to_origin(0, 0, 100, 10, self.x, self.y, 400, 40)
    self.bar_fg.clip_draw_to_origin(0, 0, 100, 10, self.x, self.y, hp, 40)

  def update(self, new_hp):
    self.current_hp = new_hp
    pass
from pico2d import *


class Hp:
  def __init__(self, x, obj_hp):
    self.x = x
    self.y = get_canvas_height() - 50
    self.bar_bg = load_image('./res/ui/hp_bar_bg.png')
    self.bar_fg = load_image('./res/ui/hp_bar_fg.png')
    self.max_hp = 100
    self.current_hp = obj_hp

  def draw(self, h_flag = ''):
    self.bar_bg.clip_composite_draw(0, 0, 195, 17, 0, h_flag, self.x, self.y, 400, 40)

    hp_ratio = self.current_hp / self.max_hp

    fg_width = int(self.bar_fg.w * hp_ratio)
    self.bar_fg.clip_composite_draw(0, 0, fg_width, 17, 0, h_flag, self.x, self.y, 400, 40)

  def update(self, new_hp):
    self.current_hp -= new_hp
    pass
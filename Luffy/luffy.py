from pico2d import *

class Luffy:
  def __init__(self):
    pass
  def update(self):
    pass
  def handle_event(self, event):
    pass
  def draw(self):
    pass
  def get_bb(self):
    pass
  def handle_collision(self, group, other):
    pass


class Idle:
  @staticmethod
  def enter(luffy, e):
    pass
  @staticmethod
  def exit(luffy, e):
    pass
  @staticmethod
  def do(luffy):
    pass
  @staticmethod
  def draw(luffy):
    pass

class Run:
  @staticmethod
  def enter(luffy, e):
    pass

  @staticmethod
  def exit(luffy, e):
    pass

  @staticmethod
  def do(luffy):
    pass

  @staticmethod
  def draw(luffy):
    pass
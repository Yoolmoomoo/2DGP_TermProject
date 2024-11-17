from pico2d import *
from speed_definition import *
import state_machine
import game_framework
from state_machine import StateMachine

class Luffy:
  def __init__(self):
    self.x, self.y = 400, 90
    self.face_dir = 1
    self.image_idle = load_image('./res/luffy/luffy_idle.png')
    self.state_machine = StateMachine(self)
    self.state_machine.start(Idle)
    self.state_machine.set_transitions(
      {
        Idle : {state_machine.right_down : Run,
                state_machine.left_down : Run,
                state_machine.right_up : Run,
                state_machine.left_up : Run}
      }
    )
  def update(self):
    self.state_machine.update()
  def handle_event(self, event):
    self.state_machine.add_event(('INPUT', event))
  def draw(self):
    self.state_machine.draw()
    # Collision box
    draw_rectangle(*self.get_bb())
  def get_bb(self):
    # xld, yld, xru, yru
    return self.x-20, self.y-50, self.x+20, self.y+50
  def handle_collision(self, group, other):
    pass


class Idle:
  @staticmethod
  def enter(luffy, e):
    if state_machine.start_event(e):
      luffy.face_dir = 1
    elif state_machine.right_down(e) or state_machine.left_up(e):
      luffy.face_dir = -1
    elif state_machine.right_up(e) or state_machine.left_down(e):
      luffy.face_dir = 1

    luffy.frame = 0
  @staticmethod
  def exit(luffy, e):
    pass
  @staticmethod
  def do(luffy):
    luffy.frame = (luffy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 4
  @staticmethod
  def draw(luffy):
    luffy.image_idle.clip_draw(int(luffy.frame)*100, 0, 100, 100, luffy.x, luffy.y)

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


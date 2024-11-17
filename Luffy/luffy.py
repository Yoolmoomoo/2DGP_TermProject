from pico2d import *
from speed_definition import *
import state_machine
import game_framework
from state_machine import StateMachine

class Luffy:
  def __init__(self):
    self.x, self.y = 400, 114
    self.face_dir = 1
    self.attack_flag = False
    self.image_idle = load_image('./res/luffy/luffy_idle.png')
    self.image_run = load_image('./res/luffy/luffy_run.png')
    self.image_c_attack_start = load_image('./res/luffy/luffy_c_attack_start.png')
    self.image_c_attack = load_image('./res/luffy/luffy_c_attack.png')
    self.image_c_attack_finish = load_image('./res/luffy/luffy_c_attack_finish.png')
    self.state_machine = StateMachine(self)
    self.state_machine.start(Idle)
    self.state_machine.set_transitions(
      {
        Idle : {state_machine.right_down : Run,
                state_machine.left_down : Run,
                state_machine.right_up : Run,
                state_machine.left_up : Run,
                state_machine.c_down : StartAttack,
               },
        Run : {state_machine.right_down : Idle,
                state_machine.left_down : Idle,
                state_machine.right_up : Idle,
                state_machine.left_up : Idle,
               state_machine.c_down: StartAttack,
              },
        StartAttack: {state_machine.frame_done: MainAttack},
        MainAttack: {state_machine.time_out: FinishAttack,
                    },
        FinishAttack: {state_machine.right_down: Run,
                       state_machine.left_down: Run,
                       state_machine.frame_done: Idle}
      }
    )
  def update(self):
    self.state_machine.update()
  def handle_event(self, event):
    self.state_machine.add_event(('INPUT', event))
  def draw(self):
    self.state_machine.draw()
    # Collision box
    # draw_rectangle(*self.get_bb())
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
    luffy.frame = 0
  @staticmethod
  def do(luffy):
    luffy.frame = (luffy.frame + FRAMES_PER_ACTION_IDLE*ACTION_PER_TIME*game_framework.frame_time) % 4
  @staticmethod
  def draw(luffy):
    if luffy.face_dir == 1:
      luffy.image_idle.clip_composite_draw(int(luffy.frame)*100, 0, 100, 180,
                                           0, '', luffy.x, luffy.y, 100, 100)
    else:
      luffy.image_idle.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180,
                                           0, 'h', luffy.x, luffy.y, 100, 100)

class Run:
  @staticmethod
  def enter(luffy, e):
    if state_machine.right_down(e) or state_machine.left_up(e):  # 오른쪽으로 RUN
      luffy.dir, luffy.face_dir = 1, 1
    elif state_machine.left_down(e) or state_machine.right_up(e):  # 왼쪽으로 RUN
      luffy.dir, luffy.face_dir = -1, -1

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0
    pass

  @staticmethod
  def do(luffy):
    luffy.frame = (luffy.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 8
    luffy.x += luffy.dir * RUN_SPEED_PPS * game_framework.frame_time

  @staticmethod
  def draw(luffy):
    if luffy.face_dir == 1:
      luffy.image_run.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180,
                                           0, '', luffy.x, luffy.y, 120, 120)
    else:
      luffy.image_run.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180,
                                          0, 'h', luffy.x, luffy.y, 120, 120)

class StartAttack:
  @staticmethod
  def enter(luffy, e):
    luffy.frame = 0

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0

  @staticmethod
  def do(luffy):
    luffy.frame += FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time
    if luffy.frame >= 2:  # 2프레임이 지나면 MainAttack으로 전환
      # luffy.state_machine.cur_state = MainAttack
      luffy.state_machine.add_event(('FRAME_DONE', 0))

  @staticmethod
  def draw(luffy):
    if luffy.face_dir == 1:
      luffy.image_c_attack_start.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                   luffy.x, luffy.y, 170, 170)
    else:
      luffy.image_c_attack_start.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                     luffy.x, luffy.y, 170, 170)

class MainAttack:
  @staticmethod
  def enter(luffy, e):
    luffy.frame = 0
    luffy.attack_time = get_time()

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0

  @staticmethod
  def do(luffy):
    luffy.frame += FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time*3
    if luffy.frame >= 4:  # 4프레임이 지나면 초기화
      luffy.frame = 0
    if get_time()-luffy.attack_time > 1.0:
      # luffy.state_machine.cur_state = FinishAttack
      luffy.state_machine.add_event(('TIME_OUT', 0))

  @staticmethod
  def draw(luffy):
    if luffy.face_dir == 1:
      luffy.image_c_attack.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                               luffy.x+50, luffy.y+12, 200, 120)
    else:
      luffy.image_c_attack.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                               luffy.x-50, luffy.y+12, 200, 120)

class FinishAttack:
  @staticmethod
  def enter(luffy, e):
    luffy.frame = 0
    luffy.attack_flag = False  # 공격 종료

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0

  @staticmethod
  def do(luffy):
    luffy.frame += FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time
    if luffy.frame >= 4:  # 4프레임이 지나면 Idle 상태로 전환
      # luffy.state_machine.cur_state = Idle
      luffy.state_machine.add_event(('FRAME_DONE', 0))

  @staticmethod
  def draw(luffy):
    if luffy.face_dir == 1:
      luffy.image_c_attack_finish.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                      luffy.x, luffy.y, 150, 150)
    else:
      luffy.image_c_attack_finish.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                      luffy.x, luffy.y, 150, 150)

# from unittest.mock import right

from pico2d import *
from speed_definition import *
import state_machine
import game_framework
from hp import Hp
from state_machine import StateMachine, left_up


class Naruto:
  def __init__(self):
    self.x, self.y = 700, 114
    self.hp = 100
    self.hp_bar = Hp(self.x+190, self.hp)
    self.action = 1
    self.face_dir = 1
    self.combo_flag = False
    self.dir = 0
    self.is_hit = False
    self.key_states = {SDLK_RIGHT:False, SDLK_LEFT:False}
    self.attack_flag = False
    self.image_idle = load_image('./res/naruto/naruto_idle.png')
    self.image_take_damage = load_image('./res/naruto/naruto_take_damage.png')
    # self.image_run = load_image('./res/luffy/luffy_run.png')
    # self.image_c_attack_start = load_image('./res/luffy/luffy_c_attack_start.png')
    # self.image_c_attack = load_image('./res/luffy/luffy_c_attack.png')
    # self.image_c_attack_finish = load_image('./res/luffy/luffy_c_attack_finish.png')
    # self.image_x_attack = load_image('./res/luffy/luffy_x_attack.png')
    # self.image_jump = load_image('./res/luffy/luffy_jump.png')
    self.hit_effect = load_image('./res/naruto/hit_effect.png')
    self.state_machine = StateMachine(self)
    self.state_machine.start(Idle)
    self.state_machine.set_transitions(
      {
        Idle : {state_machine.right_down : Run,
                state_machine.left_down : Run,
                state_machine.right_up : Run,
                state_machine.left_up : Run,
                state_machine.c_down : StartAttack,
                state_machine.x_down: ComboAttack1,
                state_machine.space_down : Jump,
                state_machine.right_held: Run,
                state_machine.left_held: Run,
                state_machine.both_held: Idle,
                state_machine.take_damage: TakeDamage,
               },
        Run : {state_machine.right_down : Idle,
                state_machine.left_down : Idle,
                state_machine.right_up : Idle,
                state_machine.left_up : Idle,
               state_machine.c_down: StartAttack,
               state_machine.x_down: ComboAttack1,
               state_machine.space_down: Jump,
               state_machine.frame_done: Idle,
               state_machine.both_held: Idle,
               state_machine.take_damage: TakeDamage,
              },
        StartAttack: {state_machine.frame_done: MainAttack},
        MainAttack: {state_machine.time_out: FinishAttack,
                    },
        FinishAttack: {state_machine.right_down: Idle,
                       state_machine.left_down: Idle,
                       state_machine.right_up: Idle,
                       state_machine.left_up: Idle,
                       state_machine.frame_done: Idle},
        ComboAttack1: {state_machine.frame_done: Idle,
                       state_machine.next_combo: ComboAttack2},
        ComboAttack2: {state_machine.frame_done: Idle,
                       state_machine.next_combo: ComboAttack3},
        ComboAttack3: {state_machine.frame_done: Idle},
        Jump: {state_machine.landed: Idle},
        TakeDamage: {state_machine.frame_done: Idle}
      }
    )
  def update(self):
    self.state_machine.update()
    self.hp_bar.update(self.hp)

  def handle_event(self, event):
    if event.type == SDL_KEYDOWN and event.key in [SDLK_RIGHT, SDLK_LEFT]:
      self.key_states[event.key] = True
    elif event.type == SDL_KEYUP and event.key in [SDLK_RIGHT, SDLK_LEFT]:
      self.key_states[event.key] = False
    elif self.state_flag == 'ComboAttack1' and event.type == SDL_KEYDOWN and event.key is SDLK_x:
      self.combo_flag = True
    elif self.state_flag == 'ComboAttack2' and event.type == SDL_KEYDOWN and event.key is SDLK_x:
      self.combo_flag = True

    self.state_machine.add_event(('INPUT', event))

  def draw(self):
    self.state_machine.draw()
    self.hp_bar.draw('h')
    # Collision box
    # draw_rectangle(*self.get_bb())
    # for bb in self.get_bb():
    #   draw_rectangle(*bb)


  def get_bb(self):
    # xld, yld, xru, yru
    if self.state_flag == 'Idle':
      return [(self.x-30, self.y-40, self.x+30, self.y+40)]

  def handle_collision(self, group, other):
    if group == 'luffy:naruto' and other.attack_flag == True:
      damage = 10
      self.hp -= damage
      if other.face_dir == 1:
        self.face_dir = -1
      else:
        self.face_dir = 1
      self.hit_effect_timer = 0.1
      self.state_machine.add_event(('TAKE_DAMAGE', 0))



class Idle:
  @staticmethod
  def enter(naruto, e):
    naruto.state_flag = 'Idle'
    if state_machine.start_event(e):
      naruto.face_dir = -1
    # 방향키가 눌려 있으면 이벤트 추가
    right_pressed = naruto.key_states.get(SDLK_RIGHT, False)
    left_pressed = naruto.key_states.get(SDLK_LEFT, False)

    if right_pressed:
      if left_pressed:
        naruto.state_machine.add_event(('BOTH_HELD', 0))
      else:
        naruto.state_machine.add_event(('RIGHT_HELD', 0))
    elif left_pressed:
      if right_pressed:
        naruto.state_machine.add_event(('BOTH_HELD', 0))
      else:
        naruto.state_machine.add_event(('LEFT_HELD', 0))
    # elif state_machine.right_down(e) or state_machine.left_up(e):
    #   naruto.face_dir = -1
    # elif state_machine.right_up(e) or state_machine.left_down(e):
    #   naruto.face_dir = 1

    naruto.frame = 0
  @staticmethod
  def exit(naruto, e):
    naruto.frame = 0
  @staticmethod
  def do(naruto):
    naruto.frame = (naruto.frame + FRAMES_PER_ACTION_IDLE*ACTION_PER_TIME*game_framework.frame_time) % 4
  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      naruto.image_idle.clip_composite_draw(int(naruto.frame)*100, 0, 100, 180,
                                           0, '', naruto.x, naruto.y, 100, 100)
    else:
      naruto.image_idle.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180,
                                           0, 'h', naruto.x, naruto.y, 100, 100)

class Run:
  @staticmethod
  def enter(naruto, e):
    naruto.state_flag = 'Run'

    right_pressed = naruto.key_states.get(SDLK_RIGHT, False)
    left_pressed = naruto.key_states.get(SDLK_LEFT, False)

    if state_machine.right_down(e) or state_machine.left_up(e):  # 오른쪽으로 RUN
      naruto.dir, naruto.face_dir = 1, 1
    elif state_machine.left_down(e) or state_machine.right_up(e):  # 왼쪽으로 RUN
      naruto.dir, naruto.face_dir = -1, -1

    if right_pressed:
      naruto.dir, naruto.face_dir = 1, 1
    if left_pressed:
      naruto.dir, naruto.face_dir = -1, -1

  @staticmethod
  def exit(naruto, e):
    naruto.frame = 0
    pass

  @staticmethod
  def do(naruto):

    naruto.frame = (naruto.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 8
    naruto.x += naruto.dir * RUN_SPEED_PPS * game_framework.frame_time

  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      naruto.image_run.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180,
                                           0, '', naruto.x, naruto.y, 120, 120)
    else:
      naruto.image_run.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180,
                                          0, 'h', naruto.x, naruto.y, 120, 120)

class StartAttack:
  @staticmethod
  def enter(naruto, e):
    # naruto.state_flag = 'StartAttack'
    naruto.frame = 0
    naruto.attack_flag = True

  @staticmethod
  def exit(naruto, e):
    naruto.frame = 0

  @staticmethod
  def do(naruto):
    naruto.frame += (FRAMES_PER_ACTION_SA * ACTION_PER_TIME * game_framework.frame_time)
    if naruto.frame >= 2:  # 2프레임이 지나면 MainAttack으로 전환
      # naruto.state_machine.cur_state = MainAttack
      naruto.state_machine.add_event(('FRAME_DONE', 0))

  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      naruto.image_c_attack_start.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180, 0, '',
                                                   naruto.x, naruto.y, 170, 170)
    else:
      naruto.image_c_attack_start.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180, 0, 'h',
                                                     naruto.x, naruto.y, 170, 170)

class MainAttack:
  @staticmethod
  def enter(naruto, e):
    naruto.state_flag = 'MainAttack'
    naruto.frame = 0
    naruto.attack_time = get_time()

  @staticmethod
  def exit(naruto, e):
    naruto.frame = 0

  @staticmethod
  def do(naruto):
    naruto.frame += (FRAMES_PER_ACTION_MA * ACTION_PER_TIME * game_framework.frame_time)
    if naruto.frame >= 4:  # 4프레임이 지나면 초기화
      naruto.frame = 0
    if get_time()-naruto.attack_time > 1.0:
      # naruto.state_machine.cur_state = FinishAttack
      naruto.state_machine.add_event(('TIME_OUT', 0))

  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      naruto.image_c_attack.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180, 0, '',
                                               naruto.x+50, naruto.y+12, 180, 120)
    else:
      naruto.image_c_attack.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180, 0, 'h',
                                               naruto.x-50, naruto.y+12, 180, 120)

class FinishAttack:
  @staticmethod
  def enter(naruto, e):
    naruto.state_flag = 'FinishAttack'
    naruto.frame = 0
    naruto.attack_flag = False  # 공격 종료

  @staticmethod
  def exit(naruto, e):
    naruto.frame = 0

  @staticmethod
  def do(naruto):
    naruto.frame += (FRAMES_PER_ACTION_SA * ACTION_PER_TIME * game_framework.frame_time)
    if naruto.frame >= 4:  # 4프레임이 지나면 Idle 상태로 전환
      # naruto.state_machine.cur_state = Idle
      naruto.state_machine.add_event(('FRAME_DONE', 0))

  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      naruto.image_c_attack_finish.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180, 0, '',
                                                      naruto.x, naruto.y, 150, 150)
    else:
      naruto.image_c_attack_finish.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180, 0, 'h',
                                                      naruto.x, naruto.y, 150, 150)

class ComboAttack1:
  @staticmethod
  def enter(naruto, e):
    naruto.state_flag = 'ComboAttack1'
    naruto.attack_time = get_time()

  @staticmethod
  def exit(naruto, e):
    naruto.combo_flag = False
    pass

  @staticmethod
  def do(naruto):
    naruto.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)

    # X키 입력 대기
    if naruto.frame >= 3:  # ComboAttack1 프레임 종료
      if get_time() - naruto.attack_time < 1.0 and naruto.combo_flag:
        naruto.state_machine.add_event(('COMBO_NEXT', 0))  # ComboAttack2로 전환
      else:
        naruto.state_machine.add_event(('FRAME_DONE', 0))  # Idle로 전환

  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, '',
                                               naruto.x+13, naruto.y, 400, 120)
    else:
      naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, 'h',
                                               naruto.x-13, naruto.y, 400, 120)

class ComboAttack2:
  @staticmethod
  def enter(naruto, e):
    naruto.state_flag = 'ComboAttack2'
    naruto.attack_time = get_time()

  @staticmethod
  def exit(naruto, e):
    naruto.combo_flag = False
    pass

  @staticmethod
  def do(naruto):
    naruto.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)

    # X키 입력 대기
    if naruto.frame >= 8:  # ComboAttack2 프레임 종료
      if get_time() - naruto.attack_time < 1.0 and naruto.combo_flag:
        naruto.state_machine.add_event(('COMBO_NEXT', 0))  # ComboAttack3로 전환
      else:
        naruto.state_machine.add_event(('FRAME_DONE', 0))  # Idle로 전환

  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, '',
                                               naruto.x-13, naruto.y, 400, 120)
    else:
      naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, 'h',
                                               naruto.x+13, naruto.y, 400, 120)

class ComboAttack3:
  @staticmethod
  def enter(naruto, e):
    naruto.state_flag = 'ComboAttack3'

  @staticmethod
  def exit(naruto, e):
    naruto.frame = 0
    naruto.combo_flag = False

  @staticmethod
  def do(naruto):
    naruto.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)

    # 마지막 콤보 종료 후 Idle로 전환
    if naruto.frame >= 16:  # ComboAttack3 프레임 종료
      naruto.state_machine.add_event(('FRAME_DONE', 0))

  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, '',
                                               naruto.x-13, naruto.y, 400, 120)
    else:
      naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, 'h',
                                               naruto.x+13, naruto.y, 400, 120)


class Jump:
  @staticmethod
  def enter(naruto, e):
    naruto.state_flag = 'Jump'
    naruto.frame = 0
    naruto.dy = 1

    right_pressed = naruto.key_states.get(SDLK_RIGHT, False)
    left_pressed = naruto.key_states.get(SDLK_LEFT, False)

    if state_machine.right_down(e) or state_machine.left_up(e):  # 오른쪽으로 RUN
      naruto.dir, naruto.face_dir = 1, 1
    elif state_machine.left_down(e) or state_machine.right_up(e):  # 왼쪽으로 RUN
      naruto.dir, naruto.face_dir = -1, -1

    if right_pressed:
      naruto.dir, naruto.face_dir = 1, 1
    if left_pressed:
      naruto.dir, naruto.face_dir = -1, -1

  @staticmethod
  def exit(naruto, e):
    naruto.frame = 0

  @staticmethod
  def do(naruto):
    right_pressed = naruto.key_states.get(SDLK_RIGHT, False)
    left_pressed = naruto.key_states.get(SDLK_LEFT, False)

    if right_pressed:
      naruto.dir, naruto.face_dir = 1, 1
    if left_pressed:
      naruto.dir, naruto.face_dir = -1, -1

    naruto.frame += (FRAMES_PER_ACTION_JUMP * ACTION_PER_TIME * game_framework.frame_time)
    if naruto.frame >= 5: naruto.frame = 5

    if naruto.y >= 270:
      naruto.dy = -1

    naruto.y += naruto.dy * RUN_SPEED_PPS * game_framework.frame_time*1.2
    naruto.x += naruto.dir * RUN_SPEED_PPS * game_framework.frame_time

    if naruto.y <= 114:
      naruto.y = 114
      naruto.state_machine.add_event(('LANDED', 0))

  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      naruto.image_jump.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180, 0, '',
                                                      naruto.x, naruto.y, 120, 120)
    else:
      naruto.image_jump.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180, 0, 'h',
                                                      naruto.x, naruto.y, 120, 120)

class TakeDamage:
  @staticmethod
  def enter(naruto, e):
    naruto.state_flag = 'Idle'
    # if state_machine.start_event(e):
    #   naruto.face_dir = -1
    # # 방향키가 눌려 있으면 이벤트 추가
    # right_pressed = naruto.key_states.get(SDLK_RIGHT, False)
    # left_pressed = naruto.key_states.get(SDLK_LEFT, False)
    #
    # if right_pressed:
    #   if left_pressed:
    #     naruto.state_machine.add_event(('BOTH_HELD', 0))
    #   else:
    #     naruto.state_machine.add_event(('RIGHT_HELD', 0))
    # elif left_pressed:
    #   if right_pressed:
    #     naruto.state_machine.add_event(('BOTH_HELD', 0))
    #   else:
    #     naruto.state_machine.add_event(('LEFT_HELD', 0))
    # elif state_machine.right_down(e) or state_machine.left_up(e):
    #   naruto.face_dir = -1
    # elif state_machine.right_up(e) or state_machine.left_down(e):
    #   naruto.face_dir = 1

    naruto.frame = 0
    naruto.is_hit = True
  @staticmethod
  def exit(naruto, e):
    naruto.frame = 0
    naruto.is_hit = False
  @staticmethod
  def do(naruto):
    naruto.frame = (naruto.frame + FRAMES_PER_ACTION_IDLE*ACTION_PER_TIME*game_framework.frame_time) % 4
    if naruto.is_hit:
      naruto.hit_effect_timer -= game_framework.frame_time
      if naruto.hit_effect_timer <= 0:
        naruto.is_hit = False
        naruto.state_machine.add_event(('FRAME_DONE', 0))
    if naruto.face_dir == -1:
      naruto.x += 0.1
    else:
      naruto.x -= 0.1
  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      if naruto.is_hit == True:
        naruto.image_take_damage.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180,
                                             0, '', naruto.x, naruto.y, 120, 120)
        naruto.hit_effect.clip_composite_draw(0, 0, 256, 256,
                                            0, '', naruto.x, naruto.y, 70, 70)
    else:
      naruto.image_take_damage.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180,
                                                   0, 'h', naruto.x, naruto.y, 120, 120)
      naruto.hit_effect.clip_composite_draw(0, 0, 256, 256,
                                            0, '', naruto.x, naruto.y, 70, 70)
      pass
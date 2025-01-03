# from unittest.mock import right

from pico2d import *
from speed_definition import *
import state_machine
import game_framework
from state_machine import StateMachine
from hp import Hp
import play_mode

class Luffy:
  def __init__(self):
    self.gear_flag = False
    self.x, self.y = 400, 114
    self.hit_x, self.hit_y = 0, 0
    self.w = 100
    self.h = 100
    self.font = load_font('./res/font/D2Coding.TTF', 20)
    self.hp = 400
    self.hp_bar = Hp(self.x-387, self.hp)
    self.damage = 0.5
    self.state_flag = 'Idle'
    self.action = 1
    self.face_dir = 1
    self.combo_flag = False
    self.dir = 0
    self.key_states = {SDLK_RIGHT:False, SDLK_LEFT:False}
    self.attack_flag = False
    self.image_idle = load_image('./res/luffy/luffy_idle.png')
    self.image_run = load_image('./res/luffy/luffy_run.png')
    self.image_c_attack_start = load_image('./res/luffy/luffy_c_attack_start.png')
    self.image_c_attack = load_image('./res/luffy/luffy_c_attack.png')
    self.image_c_attack_finish = load_image('./res/luffy/luffy_c_attack_finish.png')
    self.image_x_attack = load_image('./res/luffy/luffy_x_attack.png')
    self.image_jump = load_image('./res/luffy/luffy_jump.png')
    self.image_take_damage = load_image('./res/luffy/luffy_take_damage.png')
    self.image_win = load_image('./res/luffy/luffy_win.png')
    self.image_hit_effect = load_image('./res/luffy/hit_effect.png')
    self.image_gear = load_image('./res/luffy/luffy_gear.png')
    self.image_gear_idle = load_image('./res/luffy/luffy_gear_idle.png')
    self.image_gear_run = load_image('./res/luffy/luffy_gear_run.png')
    self.image_gear_start_attack = load_image('./res/luffy/luffy_gear_start_attack.png')
    self.image_gear_main_attack = load_image('./res/luffy/luffy_gear_main_attack.png')
    self.image_gear_finish_attack = load_image('./res/luffy/luffy_gear_finish_attack.png')
    self.image_gear_combo_attack1 = load_image('./res/luffy/luffy_gear_combo_attack1.png')
    self.image_gear_combo_attack2 = load_image('./res/luffy/luffy_gear_combo_attack2.png')
    self.image_gear_combo_attack3 = load_image('./res/luffy/luffy_gear_combo_attack3.png')
    self.image_gear_take_damage = load_image('./res/luffy/luffy_gear_take_damage.png')
    self.image_gear_jump = load_image('./res/luffy/luffy_gear_jump.png')
    self.image_gear_win = load_image('./res/luffy/luffy_gear_win.png')
    self.hit_sound = load_wav('./res/sound/hit.wav')
    self.hit_sound.set_volume(32)
    self.gear_sound = load_wav('./res/sound/gear_sound.wav')
    self.gear_sound.set_volume(80)
    self.is_hit = False
    self.hit_num = 0
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
                state_machine.win: Win,
                state_machine.gear: Gear,
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
               state_machine.win: Win,
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
        Jump: {state_machine.landed: Idle,
               state_machine.win: Win,},
        TakeDamage: {state_machine.frame_done: Idle,
                     state_machine.win: Win,},
        Win: {state_machine.win: Win,},
        Gear: {state_machine.complete_transition: Idle}
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
    elif self.state_flag == 'Idle' and event.type == SDL_KEYDOWN and event.key is SDLK_g:
      self.state_machine.add_event(('GEAR', 0))
      self.gear_sound.play()

    self.state_machine.add_event(('INPUT', event))

  def draw(self):
    self.state_machine.draw()
    self.font.draw(self.x-31, self.y+50, f'Player', (0,0,255))
    self.hp_bar.draw(self.hp, left_flag = True)
    # Collision box
    # draw_rectangle(*self.get_bb())
    # for bb in self.get_bb():
    #   draw_rectangle(*bb)

  def get_bb(self):
    # xld, yld, xru, yru
    if self.state_flag == 'None':
      return [(0, 0, 0, 0)]
    if self.state_flag == 'Idle':
      return [(self.x-30, self.y-40, self.x+30, self.y+40)]
    if self.state_flag == 'Run':
      return [(self.x-30, self.y-40, self.x+30, self.y+40)]
    if self.state_flag == 'MainAttack':
      if self.face_dir == 1:
        return [(self.hit_x, self.hit_y, self.hit_x + 100, self.hit_y + 100)]
      else:
        return [(self.hit_x -100, self.hit_y, self.hit_x - 10, self.hit_y + 100)]
    if self.state_flag == 'FinishAttack':
      return [(self.x-30, self.y-40, self.x+30, self.y+40)]
    if self.state_flag == 'Jump':
      return [(self.x - 30, self.y - 40, self.x + 30, self.y + 40)]
    if self.state_flag == 'ComboAttack1':
      if self.face_dir == 1:
        return [(self.hit_x, self.hit_y, self.hit_x + 50, self.hit_y + 30)]
      else:
        return [(self.hit_x-110, self.hit_y, self.hit_x - 60, self.hit_y + 30)]
    if self.state_flag == 'ComboAttack2':
      if self.hit_x == 0 and self.hit_y == 0: return [(0,0,0,0)]
      if self.gear_flag == True:
        if self.face_dir == 1:
          return [(self.hit_x, self.hit_y, self.hit_x + 110, self.hit_y + 30)]
        else:
          return [(self.hit_x - 170, self.hit_y, self.hit_x - 60, self.hit_y + 30)]
      else:
        if self.face_dir == 1:
          return [(self.hit_x, self.hit_y, self.hit_x + 90, self.hit_y + 30)]
        else:
          return [(self.hit_x - 150, self.hit_y, self.hit_x - 60, self.hit_y + 30)]
    if self.state_flag == 'ComboAttack3':
      if self.hit_x == 0 and self.hit_y == 0: return [(0, 0, 0, 0)]
      if self.face_dir == 1:
        return [(self.hit_x, self.hit_y, self.hit_x + 145, self.hit_y + 35)]
      else:
        return [(self.hit_x - 205, self.hit_y, self.hit_x - 60, self.hit_y + 35)]
    if self.state_flag == 'TakeDamage':
      return [(self.x-30, self.y-40, self.x+30, self.y+40)]
    if self.state_flag == 'Win':
      return [(0,0,0,0)]

  def handle_collision(self, group, other):
    if self.state_flag == 'None': return
    if other.hp <= 0 : return
    if group == 'luffy:naruto' and other.attack_flag == True:
      self.state_machine.add_event(('TAKE_DAMAGE', 0))
      self.hp -= other.damage
      # for _ in range(self.hit_num):


class Idle:
  @staticmethod
  def enter(luffy, e):
    luffy.attack_flag = False
    luffy.state_flag = 'Idle'
    if state_machine.start_event(e):
      luffy.face_dir = 1
    # 방향키가 눌려 있으면 이벤트 추가
    right_pressed = luffy.key_states.get(SDLK_RIGHT, False)
    left_pressed = luffy.key_states.get(SDLK_LEFT, False)

    if right_pressed:
      if left_pressed:
        luffy.state_machine.add_event(('BOTH_HELD', 0))
      else:
        luffy.state_machine.add_event(('RIGHT_HELD', 0))
    elif left_pressed:
      if right_pressed:
        luffy.state_machine.add_event(('BOTH_HELD', 0))
      else:
        luffy.state_machine.add_event(('LEFT_HELD', 0))
    # elif state_machine.right_down(e) or state_machine.left_up(e):
    #   luffy.face_dir = -1
    # elif state_machine.right_up(e) or state_machine.left_down(e):
    #   luffy.face_dir = 1

    luffy.frame = 0
  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0
  @staticmethod
  def do(luffy):
    luffy.frame = (luffy.frame + FRAMES_PER_ACTION_IDLE*ACTION_PER_TIME*game_framework.frame_time) % 4
  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      if luffy.face_dir == 1:
        luffy.image_gear_idle.clip_composite_draw(int(luffy.frame)*100, 0, 100, 180,
                                             0, '', luffy.x, luffy.y, 90, 90)
      else:
        luffy.image_gear_idle.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180,
                                             0, 'h', luffy.x, luffy.y, 90, 90)
    else:
      if luffy.face_dir == 1:
        luffy.image_idle.clip_composite_draw(int(luffy.frame)*100, 0, 100, 180,
                                             0, '', luffy.x, luffy.y, 100, 100)
      else:
        luffy.image_idle.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180,
                                             0, 'h', luffy.x, luffy.y, 100, 100)

class Run:
  @staticmethod
  def enter(luffy, e):
    luffy.state_flag = 'Run'
    luffy.attack_flag = False

    right_pressed = luffy.key_states.get(SDLK_RIGHT, False)
    left_pressed = luffy.key_states.get(SDLK_LEFT, False)

    if state_machine.right_down(e) or state_machine.left_up(e):  # 오른쪽으로 RUN
      luffy.dir, luffy.face_dir = 1, 1
    elif state_machine.left_down(e) or state_machine.right_up(e):  # 왼쪽으로 RUN
      luffy.dir, luffy.face_dir = -1, -1

    if right_pressed:
      luffy.dir, luffy.face_dir = 1, 1
    if left_pressed:
      luffy.dir, luffy.face_dir = -1, -1

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0
    pass

  @staticmethod
  def do(luffy):
    # luffy.run_sound.play()
    luffy.frame = (luffy.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 8
    if (luffy.x <= 10 and luffy.dir == -1) or (luffy.x >=1000 and luffy.dir == 1):
      luffy.x = luffy.x
    else:
      luffy.x += luffy.dir * RUN_SPEED_PPS * game_framework.frame_time

  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      if luffy.face_dir == 1:
        luffy.image_gear_run.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180,
                                             0, '', luffy.x, luffy.y, 100, 90)
      else:
        luffy.image_gear_run.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180,
                                            0, 'h', luffy.x, luffy.y, 100, 90)

    else:
      if luffy.face_dir == 1:
        luffy.image_run.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180,
                                             0, '', luffy.x, luffy.y, 120, 120)
      else:
        luffy.image_run.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180,
                                            0, 'h', luffy.x, luffy.y, 120, 120)

class StartAttack:
  @staticmethod
  def enter(luffy, e):
    # luffy.state_flag = 'StartAttack'
    luffy.frame = 0
    luffy.hit_num = 0
    luffy.attack_flag = True

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0

  @staticmethod
  def do(luffy):
    luffy.frame += (FRAMES_PER_ACTION_SA * ACTION_PER_TIME * game_framework.frame_time)
    if luffy.frame >= 2:  # 2프레임이 지나면 MainAttack으로 전환
      # luffy.state_machine.cur_state = MainAttack
      luffy.state_machine.add_event(('FRAME_DONE', 0))

  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      if luffy.face_dir == 1:
        luffy.image_gear_start_attack.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                     luffy.x, luffy.y+5, 115, 115)
      else:
        luffy.image_gear_start_attack.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                       luffy.x, luffy.y+5, 115, 115)
    else:
      if luffy.face_dir == 1:
        luffy.image_c_attack_start.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                     luffy.x, luffy.y, 170, 170)
      else:
        luffy.image_c_attack_start.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                       luffy.x, luffy.y, 170, 170)

class MainAttack:
  @staticmethod
  def enter(luffy, e):
    if luffy.face_dir == 1:
      luffy.hit_x, luffy.hit_y = luffy.x+30, luffy.y-40
    else:
      luffy.hit_x, luffy.hit_y = luffy.x - 30, luffy.y - 40

    luffy.state_flag = 'MainAttack'
    luffy.frame = 0
    luffy.hit_num = 8
    luffy.attack_time = get_time()
    luffy.attack_flag = True

  @staticmethod
  def exit(luffy, e):
    luffy.hit_x, luffy.hit_y = 0, 0
    luffy.frame = 0
    luffy.attack_flag = False

  @staticmethod
  def do(luffy):
    luffy.frame += (FRAMES_PER_ACTION_MA * ACTION_PER_TIME * game_framework.frame_time)
    if luffy.frame >= 4:  # 4프레임이 지나면 초기화
      luffy.frame = 0
    if get_time()-luffy.attack_time > 1.0:
      luffy.state_machine.add_event(('TIME_OUT', 0))

  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      if luffy.face_dir == 1:
        luffy.image_gear_main_attack.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                 luffy.x+50, luffy.y+20, 160, 130)
      else:
        luffy.image_gear_main_attack.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                 luffy.x-50, luffy.y+20, 160, 130)
    else:
      if luffy.face_dir == 1:
        luffy.image_c_attack.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                 luffy.x+50, luffy.y+12, 180, 120)
      else:
        luffy.image_c_attack.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                 luffy.x-50, luffy.y+12, 180, 120)

class FinishAttack:
  @staticmethod
  def enter(luffy, e):
    luffy.state_flag = 'FinishAttack'
    luffy.frame = 0
    luffy.attack_flag = False  # 공격 종료

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0

  @staticmethod
  def do(luffy):
    luffy.frame += (FRAMES_PER_ACTION_SA * ACTION_PER_TIME * game_framework.frame_time)
    if luffy.frame >= 4:  # 4프레임이 지나면 Idle 상태로 전환
      # luffy.state_machine.cur_state = Idle
      luffy.state_machine.add_event(('FRAME_DONE', 0))

  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      if luffy.face_dir == 1:
        luffy.image_gear_finish_attack.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                        luffy.x, luffy.y, 100, 100)
      else:
        luffy.image_gear_finish_attack.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                        luffy.x, luffy.y, 100, 100)
    else:
      if luffy.face_dir == 1:
        luffy.image_c_attack_finish.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                        luffy.x, luffy.y, 150, 150)
      else:
        luffy.image_c_attack_finish.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                        luffy.x, luffy.y, 150, 150)

class ComboAttack1:
  @staticmethod
  def enter(luffy, e):
    luffy.hit_x, luffy.hit_y = luffy.x + 30, luffy.y - 10
    luffy.state_flag = 'ComboAttack1'
    luffy.attack_time = get_time()
    luffy.hit_num = 1
    luffy.attack_flag = True
    if luffy.gear_flag == True:
      luffy.frame = 0

  @staticmethod
  def exit(luffy, e):
    luffy.hit_x, luffy.hit_y = 0, 0
    luffy.combo_flag = False
    pass

  @staticmethod
  def do(luffy):
    luffy.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)

      # X키 입력 대기
    if luffy.frame >= 3:  # ComboAttack1 프레임 종료
      if get_time() - luffy.attack_time < 0.9 and luffy.combo_flag:
        luffy.state_machine.add_event(('COMBO_NEXT', 0))  # ComboAttack2로 전환
      else:
        luffy.state_machine.add_event(('FRAME_DONE', 0))  # Idle로 전환

  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      if luffy.face_dir == 1:
        luffy.image_gear_combo_attack1.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                 luffy.x+13, luffy.y+10, 120, 120)
      else:
        luffy.image_gear_combo_attack1.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                 luffy.x-13, luffy.y+10, 120, 120)
    else:
      if luffy.face_dir == 1:
        luffy.image_x_attack.clip_composite_draw(int(luffy.frame) * 240, 0, 240, 180, 0, '',
                                                 luffy.x+13, luffy.y, 400, 120)
      else:
        luffy.image_x_attack.clip_composite_draw(int(luffy.frame) * 240, 0, 240, 180, 0, 'h',
                                                 luffy.x-13, luffy.y, 400, 120)

class ComboAttack2:
  @staticmethod
  def enter(luffy, e):
    luffy.state_flag = 'ComboAttack2'
    luffy.attack_time = get_time()
    luffy.attack_flag = True
    if luffy.gear_flag == True:
      luffy.frame = 0

  @staticmethod
  def exit(luffy, e):
    luffy.hit_x, luffy.hit_y = 0, 0
    luffy.combo_flag = False

  @staticmethod
  def do(luffy):
    if luffy.gear_flag == True:
      luffy.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)
      if luffy.frame > 5:
          luffy.hit_x, luffy.hit_y = luffy.x + 30, luffy.y - 10
      if luffy.frame > 6:
        luffy.hit_x, luffy.hit_y = 0,0
      # X키 입력 대기
      if luffy.frame >= 7:  # ComboAttack2 프레임 종료
        if get_time() - luffy.attack_time < 0.9 and luffy.combo_flag:
          luffy.state_machine.add_event(('COMBO_NEXT', 0))  # ComboAttack3로 전환
        else:
          luffy.state_machine.add_event(('FRAME_DONE', 0))  # Idle로 전환
    else:
      luffy.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)
      if luffy.frame > 5.7:
          luffy.hit_x, luffy.hit_y = luffy.x + 30, luffy.y - 10
      if luffy.frame > 7:
        luffy.hit_x, luffy.hit_y = 0,0
      # X키 입력 대기
      if luffy.frame >= 8:  # ComboAttack2 프레임 종료
        if get_time() - luffy.attack_time < 0.9 and luffy.combo_flag:
          luffy.state_machine.add_event(('COMBO_NEXT', 0))  # ComboAttack3로 전환
        else:
          luffy.state_machine.add_event(('FRAME_DONE', 0))  # Idle로 전환

  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      if luffy.face_dir == 1:
        luffy.image_gear_combo_attack2.clip_composite_draw(int(luffy.frame) * 560, 0, 560, 180, 0, '',
                                                 luffy.x+13, luffy.y, 500, 100)
      else:
        luffy.image_gear_combo_attack2.clip_composite_draw(int(luffy.frame) * 560, 0, 560, 180, 0, 'h',
                                                 luffy.x-13, luffy.y, 480, 100)
    else:
      if luffy.face_dir == 1:
        luffy.image_x_attack.clip_composite_draw(int(luffy.frame) * 240, 0, 240, 180, 0, '',
                                                 luffy.x-13, luffy.y, 480, 120)
      else:
        luffy.image_x_attack.clip_composite_draw(int(luffy.frame) * 240, 0, 240, 180, 0, 'h',
                                                 luffy.x+13, luffy.y, 400, 120)

class ComboAttack3:
  @staticmethod
  def enter(luffy, e):
    luffy.state_flag = 'ComboAttack3'
    luffy.attack_flag = True
    if luffy.gear_flag == True:
      luffy.frame = 0

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0
    luffy.combo_flag = False
    luffy.hit_x, luffy.hit_y = 0, 0
    luffy.hit_num = 0
    luffy.attack_flag = False

  @staticmethod
  def do(luffy):
    if luffy.gear_flag == True:
      luffy.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)

      if luffy.frame >= 7:
        luffy.hit_x, luffy.hit_y = luffy.x + 30, luffy.y - 10

      if luffy.frame >= 7.5:
        luffy.hit_x, luffy.hit_y = 0, 0

      # 마지막 콤보 종료 후 Idle로 전환
      if luffy.frame >= 11:  # ComboAttack3 프레임 종료
        luffy.state_machine.add_event(('FRAME_DONE', 0))

    else:
      luffy.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)

      if luffy.frame > 13.5:
          luffy.hit_x, luffy.hit_y = luffy.x + 30, luffy.y - 10

      # 마지막 콤보 종료 후 Idle로 전환
      if luffy.frame >= 16:  # ComboAttack3 프레임 종료
        luffy.state_machine.add_event(('FRAME_DONE', 0))

  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      if luffy.face_dir == 1:
        luffy.image_gear_combo_attack3.clip_composite_draw(int(luffy.frame) * 450, 0, 450, 180, 0, '',
                                                 luffy.x+13, luffy.y, 420, 160)
      else:
        luffy.image_gear_combo_attack3.clip_composite_draw(int(luffy.frame) * 450, 0, 450, 180, 0, 'h',
                                                 luffy.x-13, luffy.y, 420, 160)
    else:
      if luffy.face_dir == 1:
        luffy.image_x_attack.clip_composite_draw(int(luffy.frame) * 240, 0, 240, 180, 0, '',
                                                 luffy.x-13, luffy.y, 400, 120)
      else:
        luffy.image_x_attack.clip_composite_draw(int(luffy.frame) * 240, 0, 240, 180, 0, 'h',
                                                 luffy.x+13, luffy.y, 400, 120)


class Jump:
  @staticmethod
  def enter(luffy, e):
    luffy.state_flag = 'Jump'
    luffy.frame = 0
    luffy.dy = 1
    luffy.attack_flag = False

    right_pressed = luffy.key_states.get(SDLK_RIGHT, False)
    left_pressed = luffy.key_states.get(SDLK_LEFT, False)

    if state_machine.right_down(e) or state_machine.left_up(e):  # 오른쪽으로 RUN
      luffy.dir, luffy.face_dir = 1, 1
    elif state_machine.left_down(e) or state_machine.right_up(e):  # 왼쪽으로 RUN
      luffy.dir, luffy.face_dir = -1, -1

    if right_pressed:
      luffy.dir, luffy.face_dir = 1, 1
    if left_pressed:
      luffy.dir, luffy.face_dir = -1, -1

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0

  @staticmethod
  def do(luffy):
    right_pressed = luffy.key_states.get(SDLK_RIGHT, False)
    left_pressed = luffy.key_states.get(SDLK_LEFT, False)

    if right_pressed:
      luffy.dir, luffy.face_dir = 1, 1
    if left_pressed:
      luffy.dir, luffy.face_dir = -1, -1

    luffy.frame += (FRAMES_PER_ACTION_JUMP * ACTION_PER_TIME * game_framework.frame_time)
    if luffy.frame >= 5: luffy.frame = 5

    if luffy.y >= 290:
      luffy.dy = -1

    luffy.y += luffy.dy * RUN_SPEED_PPS * game_framework.frame_time*1.2
    luffy.x += luffy.dir * RUN_SPEED_PPS * game_framework.frame_time

    if luffy.y <= 114:
      luffy.y = 114
      luffy.state_machine.add_event(('LANDED', 0))

  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      if luffy.face_dir == 1:
        luffy.image_gear_jump.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                        luffy.x, luffy.y, 100, 100)
      else:
        luffy.image_gear_jump.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                        luffy.x, luffy.y, 100, 100)
    else:
      if luffy.face_dir == 1:
        luffy.image_jump.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                        luffy.x, luffy.y, 120, 120)
      else:
        luffy.image_jump.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                        luffy.x, luffy.y, 120, 120)

class TakeDamage:
  @staticmethod
  def enter(luffy, e):
    luffy.state_flag = 'TakeDamage'
    luffy.frame = 0
    luffy.attack_flag = False
    luffy.is_hit = True
    luffy.current_time = get_time()

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0

  @staticmethod
  def do(luffy):
    luffy.frame = (luffy.frame + FRAMES_PER_ACTION_IDLE*ACTION_PER_TIME*game_framework.frame_time) % 4
    luffy.hit_sound.play()
    if play_mode.naruto.x <= luffy.x:
      luffy.x += 0.1
    else:
      luffy.x -= 0.1
    if get_time() - luffy.current_time > 0.3:
      luffy.state_machine.add_event(('FRAME_DONE', 0))

  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      if luffy.face_dir == 1:
        luffy.image_gear_take_damage.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                             luffy.x, luffy.y, 100, 100)
        luffy.image_hit_effect.clip_composite_draw(int(luffy.frame) * 100, 0, 256, 256, 0, '',
                                                    luffy.x, luffy.y, 50, 50)
      else:
        luffy.image_gear_take_damage.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                             luffy.x, luffy.y, 100, 100)
        luffy.image_hit_effect.clip_composite_draw(int(luffy.frame) * 100, 0, 256, 256, 0, '',
                                                    luffy.x, luffy.y, 50, 50)
    else:
      if luffy.face_dir == 1:
        luffy.image_take_damage.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                             luffy.x, luffy.y, 100, 100)
        luffy.image_hit_effect.clip_composite_draw(int(luffy.frame) * 100, 0, 256, 256, 0, '',
                                                    luffy.x, luffy.y, 50, 50)
      else:
        luffy.image_take_damage.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                             luffy.x, luffy.y, 100, 100)
        luffy.image_hit_effect.clip_composite_draw(int(luffy.frame) * 100, 0, 256, 256, 0, '',
                                                    luffy.x, luffy.y, 50, 50)

class Win:
  @staticmethod
  def enter(luffy, e):
    luffy.state_flag = 'Win'
    luffy.attack_flag = False
    luffy.is_hit = False
    luffy.current_time = get_time()

  @staticmethod
  def exit(luffy, e):
    luffy.state_machine.add_event(('WIN', 0))
    pass
  @staticmethod
  def do(luffy):
    if luffy.gear_flag == True:
      luffy.frame = (luffy.frame + 1 * ACTION_PER_TIME * game_framework.frame_time) % 5
    else:
      luffy.frame = (luffy.frame + FRAMES_PER_ACTION_IDLE*ACTION_PER_TIME*game_framework.frame_time) % 4

  @staticmethod
  def draw(luffy):
    if luffy.gear_flag == True:
      luffy.image_gear_win.clip_composite_draw(int(luffy.frame) * 150, 0, 150, 180, 0, '',
                                           luffy.x, luffy.y+40, 250, 180)
    else:
      luffy.image_win.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                           luffy.x, luffy.y, 100, 100)

class Gear:
  @staticmethod
  def enter(luffy, e):
    luffy.state_flag = 'None'
    luffy.gear_flag = True
    luffy.attack_flag = False
    luffy.is_hit = False
    luffy.current_time = get_time()
    luffy.frame = 0

  @staticmethod
  def exit(luffy, e):
    luffy.frame = 0
    luffy.w = 100
    luffy.h = 100
    luffy.y = 114

  @staticmethod
  def do(luffy):
    luffy.frame += (FRAMES_PER_ACTION_GEAR*ACTION_PER_TIME*game_framework.frame_time)
    if luffy.frame >= 12:
      luffy.w = 180
      luffy.h = 130
      luffy.y = 124
    if luffy.frame >= 18:
      luffy.state_machine.add_event(('COMPLETE', 0))

  @staticmethod
  def draw(luffy):
    if luffy.face_dir == 1:
      luffy.image_gear.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, '',
                                                      luffy.x, luffy.y, luffy.w, luffy.h)
    else:
      luffy.image_gear.clip_composite_draw(int(luffy.frame) * 100, 0, 100, 180, 0, 'h',
                                                      luffy.x, luffy.y, luffy.w, luffy.h)
# from unittest.mock import right

from pico2d import *
from speed_definition import *
import state_machine
import game_framework
from hp import Hp
from state_machine import StateMachine, left_up
from behavior_tree import *
import play_mode

class Naruto:
  def __init__(self):
    self.x, self.y = 700, 114
    self.hp = 400
    self.hp_bar = Hp(self.x-20, self.hp)
    self.damage = 0.1
    self.action = 1
    self.face_dir = 1
    self.combo_flag = False
    self.dir = 0
    self.hit_sound = load_wav('./res/sound/hit.wav')
    self.hit_sound.set_volume(32)
    self.is_hit = False
    self.key_states = {SDLK_RIGHT:False, SDLK_LEFT:False}
    self.attack_flag = False
    self.image_idle = load_image('./res/naruto/naruto_idle.png')
    self.image_take_damage = load_image('./res/naruto/naruto_take_damage.png')
    self.image_move = load_image('./res/naruto/naruto_move.png')
    self.hit_effect = load_image('./res/naruto/hit_effect.png')
    self.state_machine = StateMachine(self)
    self.state_machine.start(Idle)
    self.state_machine.set_transitions(
      {
        Idle : {state_machine.right_down : Run,
                state_machine.left_down : Run,
                state_machine.right_up : Run,
                state_machine.left_up : Run,
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
               state_machine.x_down: ComboAttack1,
               state_machine.space_down: Jump,
               state_machine.frame_done: Idle,
               state_machine.both_held: Idle,
               state_machine.take_damage: TakeDamage,
              },
        ComboAttack1: {state_machine.frame_done: Idle,
                       state_machine.next_combo: ComboAttack2},
        ComboAttack2: {state_machine.frame_done: Idle,
                       state_machine.next_combo: ComboAttack3},
        ComboAttack3: {state_machine.frame_done: Idle},
        Jump: {state_machine.landed: Idle},
        TakeDamage: {state_machine.frame_done: Idle}
      }
    )
    self.build_behavior_tree()

  def update(self):
    self.bt.run()
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
    self.hp_bar.draw(self.hp)
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
      self.hp -= other.damage
      self.hit_sound.play()
      print(self.hp)
      if other.face_dir == 1:
        self.face_dir = -1
      else:
        self.face_dir = 1
      self.hit_effect_timer = 0.01
      self.state_machine.add_event(('TAKE_DAMAGE', 0))

  def distance_less_than(self,x1,y1,x2,y2,r):
    distance2 = (x1-x2)**2 + (y1-y2)**2
    return distance2 < (PIXEL_PER_METER*r)**2

  def move_slightly_to(self, tx, ty): # 목적지까지 프레임타임 단위로(프레임마다) 살짝씩 가는 함수
      self.dir = math.atan2(ty-self.y, tx-self.x) # dir을 radian으로 해석
      distance = RUN_SPEED_PPS * game_framework.frame_time
      self.x += distance * math.cos(self.dir)
      self.y += distance * math.sin(self.dir)

  def move_to_player(self, r=10.0):
    self.state = 'Walk'
    self.move_slightly_to(play_mode.luffy.x, play_mode.luffy.y)
    if self.distance_less_than(play_mode.luffy.x, play_mode.luffy.y, self.x, self.y, r):
      return ('REACH_PLAYER', BehaviorTree.SUCCESS)
    else:
      return ('MOVING_TO_PLAYER', BehaviorTree.RUNNING)

  def is_nearby(self, distance):
    if self.distance_less_than(play_mode.luffy.x, play_mode.luffy.y, self.x, self.y, distance):
      return BehaviorTree.SUCCESS
    else:
      return BehaviorTree.FAIL

  def build_behavior_tree(self):
    c2 = Condition('플레이어가 근처에 있는가?', self.is_nearby, 20)
    a2 = Action('플레이어에게 접근', self.move_to_player)
    chase_player = Sequence('플레이어 추적', c2, a2)

    root = Selector('행동 루트', chase_player)

    self.bt = BehaviorTree(root)


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

  @staticmethod
  def exit(naruto, e):
    naruto.frame = 0

  @staticmethod
  def do(naruto):
    naruto.frame = (naruto.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 8
    naruto.move_slightly_to(play_mode.luffy.x, play_mode.luffy.y)

  @staticmethod
  def draw(naruto):
    if naruto.face_dir == 1:
      naruto.image_move.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180,
                                            0, '', naruto.x, naruto.y, 120, 120)
    else:
      naruto.image_move.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180,
                                            0, 'h', naruto.x, naruto.y, 120, 120)


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

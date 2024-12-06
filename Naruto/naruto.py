
from pico2d import *
from speed_definition import *
import state_machine
import game_framework
from hp import Hp
from state_machine import StateMachine, left_up
from behavior_tree import *
import play_mode
import random

class Naruto:
  def __init__(self):
    self.x, self.y = 700, 114
    self.tx, self.ty = 0, self.y
    self.hit_x, self.hit_y = 0, 0
    self.hp = 400
    self.hp_bar = Hp(self.x-20, self.hp)
    self.damage = 0.1
    self.action = 1
    self.face_dir = -1
    self.combo_flag = False
    self.dir = 0
    self.hit_sound = load_wav('./res/sound/hit.wav')
    self.hit_sound.set_volume(32)
    self.is_hit = False
    self.attack_flag = False
    self.frame = 0
    self.marker = load_image('hand_arrow.png')
    self.image_idle = load_image('./res/naruto/naruto_idle.png')
    self.image_take_damage = load_image('./res/naruto/naruto_take_damage.png')
    self.image_move = load_image('./res/naruto/naruto_move.png')
    self.image_att1 = load_image('./res/naruto/naruto_attack1.png')
    self.image_att2 = load_image('./res/naruto/naruto_attack2.png')
    self.hit_effect = load_image('./res/naruto/hit_effect.png')
    self.state = 'Idle'
    self.attack_flag = False
    self.att1_cool = 0.0001
    self.att2_cool = 0.0001
    self.last_att1_time = get_time()
    self.last_att2_time = get_time()
    self.last_damage_time = 0.0  # 데미지를 받은 마지막 시간을 기록할 변수 추가
    self.damage_duration = 0.3  # 데미지 상태 지속 시간 (초)
    self.build_behavior_tree()

  def update(self):
    current_time = get_time()

    if self.state == 'Idle':
      self.attack_flag = False
      self.hit_x, self.hit_y = 0, 0
      self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 4

    if self.state == 'Walk':
      self.attack_flag = False
      if self.tx > self.x:
        self.face_dir = 1
      else:
        self.face_dir = -1
      self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 8

    if self.state == 'TakeDamage':
      self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 4
      if current_time - self.last_damage_time > self.damage_duration:
        # 일정 시간이 지나면 Idle 상태로 전환
        self.last_damage_time = current_time
        self.is_hit = False
        self.state = 'Idle'
      if self.face_dir == -1:
        self.x += 0.1
      else:
        self.x -= 0.1

    if self.state == 'Attack1':
      # self.last_att1_time = get_time()
      self.attack_flag = True
      if self.tx > self.x:
        self.face_dir = 1
        if self.frame >= 3:
          self.hit_x, self.hit_y = self.x+30, self.y-40
      else:
        self.face_dir = -1
        if self.frame >= 3:
          self.hit_x, self.hit_y = self.x-30, self.y-40

      self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 4

    if self.state == 'Attack2':
      # self.last_att2_time = get_time()
      if self.tx > self.x:
        self.face_dir = 1
      else:
        self.face_dir = -1
      self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 5

    self.hp_bar.update(self.hp)
    self.bt.run()

  def draw(self):
    # self.marker.draw(self.tx, self.ty)
    if self.state == 'Idle':
      if self.face_dir == 1:
        self.image_idle.clip_composite_draw(int(self.frame) * 100, 0, 100, 180,
                                              0, '', self.x, self.y, 100, 100)
      else:
        self.image_idle.clip_composite_draw(int(self.frame) * 100, 0, 100, 180,
                                              0, 'h', self.x, self.y, 100, 100)
    if self.state == 'Walk':
      if self.face_dir == 1:
        self.image_move.clip_composite_draw(int(self.frame) * 100, 0, 100, 180,
                                              0, '', self.x, self.y, 100, 100)
      else:
        self.image_move.clip_composite_draw(int(self.frame) * 100, 0, 100, 180,
                                              0, 'h', self.x, self.y, 100, 100)

    if self.state == 'TakeDamage':
      if self.face_dir == 1:
        self.image_take_damage.clip_composite_draw(int(self.frame) * 100, 0, 100, 180,
                                                     0, '', self.x, self.y, 120, 120)
        self.hit_effect.clip_composite_draw(0, 0, 256, 256,
                                                0, '', self.x, self.y, 70, 70)
      else:
        self.image_take_damage.clip_composite_draw(int(self.frame) * 100, 0, 100, 180,
                                                     0, 'h', self.x, self.y, 120, 120)
        self.hit_effect.clip_composite_draw(0, 0, 256, 256,
                                              0, '', self.x, self.y, 70, 70)

    if self.state == 'Attack1':
      if self.face_dir == 1:
        self.image_att1.clip_composite_draw(int(self.frame) * 100, 0, 100, 180,
                                                     0, '', self.x, self.y, 100, 100)
      else:
        self.image_att1.clip_composite_draw(int(self.frame) * 100, 0, 100, 180,
                                                     0, 'h', self.x, self.y, 100, 100)

    if self.state == 'Attack2':
      if self.face_dir == 1:
        self.image_att2.clip_composite_draw(int(self.frame) * 100, 0, 100, 180,
                                                   0, '', self.x, self.y, 100, 100)
      else:
        self.image_att2.clip_composite_draw(int(self.frame) * 100, 0, 100, 180,
                                                   0, 'h', self.x, self.y, 100, 100)


    self.hp_bar.draw(self.hp)

    # Collision box
    # draw_rectangle(*self.get_bb())
    # for bb in self.get_bb():
    #   draw_rectangle(*bb)

  def get_bb(self):
    # xld, yld, xru, yru
    if self.state == 'Idle':
      return [(self.x-30, self.y-40, self.x+30, self.y+40)]
    if self.state == 'Walk':
      return [(self.x - 30, self.y - 40, self.x + 30, self.y + 40)]
    if self.state == 'TakeDamage':
      return [(self.x - 30, self.y - 40, self.x + 30, self.y + 40)]
    if self.state == 'Attack1':
      if self.face_dir == 1:
        return [(self.hit_x-20, self.hit_y+40, self.hit_x+10, self.hit_y+60)]
      else:
        return [(self.hit_x-10, self.hit_y+40, self.hit_x+20, self.hit_y+60)]
    if self.state == 'Attack2':
      if self.face_dir == 1:
        return [(self.hit_x-10, self.hit_y, self.hit_x, self.hit_y+10)]
      else:
        return [(self.hit_x -30, self.hit_y, self.hit_x - 10, self.hit_y+10)]

  def handle_collision(self, group, other):
    if group == 'luffy:naruto' and other.attack_flag == True:
      self.hp -= other.damage
      self.hit_sound.play()
      if other.face_dir == 1:
        self.face_dir = -1
      else:
        self.face_dir = 1
      self.hit_effect_timer = 0.01
      self.state = 'TakeDamage'


  def distance_less_than(self,x1,x2,d):
    distance_x = abs(x1 - x2)
    return distance_x < (PIXEL_PER_METER * d)

  def move_slightly_to(self, tx, ty): # 목적지까지 프레임타임 단위로(프레임마다) 살짝씩 가는 함수
      self.dir = math.atan2(ty-self.y, tx-self.x) # dir을 radian으로 해석
      distance = RUN_SPEED_PPS * game_framework.frame_time
      self.x += self.face_dir * RUN_SPEED_PPS * game_framework.frame_time*0.7
      self.y = ty

  def set_random_location(self):
    self.tx = random.randint(100, 1000)
    self.ty = self.y
    return BehaviorTree.SUCCESS

  def move_to(self, r=1.0):
    self.state = 'Walk'
    self.move_slightly_to(self.tx, self.ty)
    if self.distance_less_than(self.tx, self.x, r):
      return BehaviorTree.SUCCESS
    else:
      return BehaviorTree.RUNNING

  def is_in_attack_range(self, d = 2):
    if self.distance_less_than(play_mode.luffy.x, self.x, d):
        return BehaviorTree.SUCCESS
    else:
        return BehaviorTree.FAIL

  def stop_at_attack_range(self):
    self.state = 'Idle'
    return BehaviorTree.SUCCESS

  def attack1_cooldown_check(self):
    if get_time() - self.last_att1_time >= self.att1_cool:
      return BehaviorTree.SUCCESS
    else:
      return BehaviorTree.FAIL

  def attack2_cooldown_check(self):
    if get_time() - self.last_att2_time >= self.att2_cool:
      return BehaviorTree.SUCCESS
    else:
      return BehaviorTree.FAIL

  def attack1(self):
    self.state = 'Attack1'
    # self.last_att1_time = get_time()
    return BehaviorTree.SUCCESS

  def attack2(self):
    self.state = 'Attack2'
    # self.last_att2_time = get_time()
    return BehaviorTree.SUCCESS

  def is_damaged(self):
    if self.state == 'TakeDamage':
      return BehaviorTree.SUCCESS
    return BehaviorTree.FAIL

  def build_behavior_tree(self):
    c1 = Condition('플레이어가 공격 범위 안에 있는가?', self.is_in_attack_range)
    c_attack1 = Condition('공격1 쿨타임 확인', self.attack1_cooldown_check)
    c_attack2 = Condition('공격2 쿨타임 확인', self.attack2_cooldown_check)
    c_is_damaged = Condition('맞았는가?', self.is_damaged)

    a1 = Action('공격1 실행', self.attack1)
    a2 = Action('공격2 실행', self.attack2)

    attack_sequence1 = Sequence('공격1 쿨타임 체크 및 실행', c_attack1, a1)
    attack_sequence2 = Sequence('공격2 쿨타임 체크 및 실행', c_attack2, a2)

    attack_selector = Selector('공격 선택', attack_sequence1, attack_sequence2)
    attack_range = Sequence('공격 범위에서 공격', c1, attack_selector)

    a3 = Action('타겟 위치로 이동', self.move_to, 2)
    a4 = Action('랜덤 위치 결정', self.set_random_location)
    wander = Sequence('방황', a4, a3)

    root = Selector('행동 루트', c_is_damaged, attack_range, wander)

    self.bt = BehaviorTree(root)


# class ComboAttack1:
#   @staticmethod
#   def enter(naruto, e):
#     naruto.state_flag = 'ComboAttack1'
#     naruto.attack_time = get_time()
#
#   @staticmethod
#   def exit(naruto, e):
#     naruto.combo_flag = False
#     pass
#
#   @staticmethod
#   def do(naruto):
#     naruto.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)
#
#     # X키 입력 대기
#     if naruto.frame >= 3:  # ComboAttack1 프레임 종료
#       if get_time() - naruto.attack_time < 1.0 and naruto.combo_flag:
#         naruto.state_machine.add_event(('COMBO_NEXT', 0))  # ComboAttack2로 전환
#       else:
#         naruto.state_machine.add_event(('FRAME_DONE', 0))  # Idle로 전환
#
#   @staticmethod
#   def draw(naruto):
#     if naruto.face_dir == 1:
#       naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, '',
#                                                naruto.x+13, naruto.y, 400, 120)
#     else:
#       naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, 'h',
#                                                naruto.x-13, naruto.y, 400, 120)
#
# class ComboAttack2:
#   @staticmethod
#   def enter(naruto, e):
#     naruto.state_flag = 'ComboAttack2'
#     naruto.attack_time = get_time()
#
#   @staticmethod
#   def exit(naruto, e):
#     naruto.combo_flag = False
#     pass
#
#   @staticmethod
#   def do(naruto):
#     naruto.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)
#
#     # X키 입력 대기
#     if naruto.frame >= 8:  # ComboAttack2 프레임 종료
#       if get_time() - naruto.attack_time < 1.0 and naruto.combo_flag:
#         naruto.state_machine.add_event(('COMBO_NEXT', 0))  # ComboAttack3로 전환
#       else:
#         naruto.state_machine.add_event(('FRAME_DONE', 0))  # Idle로 전환
#
#   @staticmethod
#   def draw(naruto):
#     if naruto.face_dir == 1:
#       naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, '',
#                                                naruto.x-13, naruto.y, 400, 120)
#     else:
#       naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, 'h',
#                                                naruto.x+13, naruto.y, 400, 120)
#
# class ComboAttack3:
#   @staticmethod
#   def enter(naruto, e):
#     naruto.state_flag = 'ComboAttack3'
#
#   @staticmethod
#   def exit(naruto, e):
#     naruto.frame = 0
#     naruto.combo_flag = False
#
#   @staticmethod
#   def do(naruto):
#     naruto.frame += (FRAMES_PER_ACTION_CA * ACTION_PER_TIME * game_framework.frame_time)
#
#     # 마지막 콤보 종료 후 Idle로 전환
#     if naruto.frame >= 16:  # ComboAttack3 프레임 종료
#       naruto.state_machine.add_event(('FRAME_DONE', 0))
#
#   @staticmethod
#   def draw(naruto):
#     if naruto.face_dir == 1:
#       naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, '',
#                                                naruto.x-13, naruto.y, 400, 120)
#     else:
#       naruto.image_x_attack.clip_composite_draw(int(naruto.frame) * 240, 0, 240, 180, 0, 'h',
#                                                naruto.x+13, naruto.y, 400, 120)
#
#
# class Jump:
#   @staticmethod
#   def enter(naruto, e):
#     naruto.state_flag = 'Jump'
#     naruto.frame = 0
#     naruto.dy = 1
#
#     right_pressed = naruto.key_states.get(SDLK_RIGHT, False)
#     left_pressed = naruto.key_states.get(SDLK_LEFT, False)
#
#     if state_machine.right_down(e) or state_machine.left_up(e):  # 오른쪽으로 RUN
#       naruto.dir, naruto.face_dir = 1, 1
#     elif state_machine.left_down(e) or state_machine.right_up(e):  # 왼쪽으로 RUN
#       naruto.dir, naruto.face_dir = -1, -1
#
#     if right_pressed:
#       naruto.dir, naruto.face_dir = 1, 1
#     if left_pressed:
#       naruto.dir, naruto.face_dir = -1, -1
#
#   @staticmethod
#   def exit(naruto, e):
#     naruto.frame = 0
#
#   @staticmethod
#   def do(naruto):
#     right_pressed = naruto.key_states.get(SDLK_RIGHT, False)
#     left_pressed = naruto.key_states.get(SDLK_LEFT, False)
#
#     if right_pressed:
#       naruto.dir, naruto.face_dir = 1, 1
#     if left_pressed:
#       naruto.dir, naruto.face_dir = -1, -1
#
#     naruto.frame += (FRAMES_PER_ACTION_JUMP * ACTION_PER_TIME * game_framework.frame_time)
#     if naruto.frame >= 5: naruto.frame = 5
#
#     if naruto.y >= 270:
#       naruto.dy = -1
#
#     naruto.y += naruto.dy * RUN_SPEED_PPS * game_framework.frame_time*1.2
#     naruto.x += naruto.dir * RUN_SPEED_PPS * game_framework.frame_time
#
#     if naruto.y <= 114:
#       naruto.y = 114
#       naruto.state_machine.add_event(('LANDED', 0))
#
#   @staticmethod
#   def draw(naruto):
#     if naruto.face_dir == 1:
#       naruto.image_jump.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180, 0, '',
#                                                       naruto.x, naruto.y, 120, 120)
#     else:
#       naruto.image_jump.clip_composite_draw(int(naruto.frame) * 100, 0, 100, 180, 0, 'h',
#                                                       naruto.x, naruto.y, 120, 120)

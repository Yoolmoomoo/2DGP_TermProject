from sdl2 import *

################################# EVENTS #################################
def start_event(e):
  return e[0] == 'START'
def time_out(e):
  return e[0] == 'TIME_OUT'
def frame_done(e):
  return e[0] == 'FRAME_DONE'
def landed(e):
  return e[0] == 'LANDED'
################################# KEYBOARD : MOVE #################################
def right_down(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def space_down(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
################################# KEYBOARD : HELD #################################
def right_held(e):
    return e[0] == 'RIGHT_HELD'
def left_held(e):
    return e[0] == 'LEFT_HELD'
def both_held(e):
  return e[0] == 'BOTH_HELD'
################################# KEYBOARD : ATTACK #################################
def x_down(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x
def x_up(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_x
def c_down(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def c_up(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

class StateMachine:
  def __init__(self, o):
    self.o = o
    self.event_q = []

  def start(self, state):
    self.cur_state = state
    print(f'Enter into {state}')
    self.cur_state.enter(self.o, ('START',0))

  def add_event(self, e):
    # print(f'    DEBUG: New event {e} added to event Queue at StateMachine')
    self.event_q.append(e)

  def set_transitions(self, transitions):
    self.transitions = transitions

  def update(self):
    self.cur_state.do(self.o)
    if self.event_q:
      event = self.event_q.pop(0)
      self.handle_event(event)

  def draw(self):
    self.cur_state.draw(self.o)

  def handle_event(self, e):
    for event, next_state in self.transitions[self.cur_state].items():
      if event(e):
        print(f'Exit from {self.cur_state}')
        self.cur_state.exit(self.o, e)
        self.cur_state = next_state
        print(f'Enter into {self.cur_state}')
        self.cur_state.enter(self.o, e)
        return
    # print(f'    Warning: Event [{e}] at State [{self.cur_state}] not handled')

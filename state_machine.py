from sdl2 import *

################################# EVENTS #################################
def start_event(e):
  return e[0] == 'START'
def time_out(e):
  return e[0] == 'TIME_OUT'
################################# KEYBOARD : ARROW #################################
def right_down(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
################################# KEYBOARD : SPECIAL #################################
def alt_down(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_ALTERASE
################################# KEYBOARD : ATTACK #################################
def x_down(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x
def x_up(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_x
def c_down(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def c_up(e):
  return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c
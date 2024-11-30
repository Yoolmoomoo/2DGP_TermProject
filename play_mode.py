from pico2d import *
import game_framework
import random

import game_world
from Map.map import Map
from Luffy.luffy import Luffy
from Naruto.naruto import Naruto

def pause():
  pass
def resume():
  pass

def init():
  global luffy

  map = Map()
  game_world.add_object(map,0)

  luffy = Luffy()
  game_world.add_object(luffy, 1)

  naruto = Naruto()
  game_world.add_object(naruto, 1)

  ##### 충돌 페어 등록 #####
  game_world.add_collision_pair('luffy:map', luffy, map)

def handle_events():
  events = get_events()
  for event in events:
    if event.type == SDL_QUIT:
      game_framework.quit()
    elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
      game_framework.quit()
    else:
      luffy.handle_event(event)


def update():
  game_world.update()
  game_world.handle_collisions() ##### 충돌 감지 #####

def draw():
  clear_canvas()
  game_world.render()
  update_canvas()

def finish():
  game_world.update()

